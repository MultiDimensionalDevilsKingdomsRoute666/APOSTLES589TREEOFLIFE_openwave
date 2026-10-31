"""
Tests for LaplacianVariableCoeffProcessor and the _laplacian_var_coeff
kernel: flux form correctness, accumulation contract, and the
discriminating energy-conservation test (flux form vs naive form).

Run from the project root:
    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._test_variable_coeff

Note: no `from __future__ import annotations` here. Taichi kernel
definitions need live type objects.
"""

import sys
import traceback

import numpy as np
import taichi as ti

from dataclasses import dataclass
from .units import UnitSystem

from .features import PsiBaseField, PsiLongField, WaveGrid, WaveSpeedField
from ..pipeline import BaseProcessor, Pipeline, Stage
from .allocator import AllocateWaveField, AllocateWaveSpeed
from .emc import UpdateEMCDensityProcessor, UpdateWaveSpeedProcessor
from .evolution import (
    ClearAccelerationProcessor,
    LaplacianProcessor,
    LaplacianVariableCoeffProcessor,
    LeapfrogProcessor,
    _clear_accel,
    _laplacian_var_coeff,
    _leapfrog,
)
from .units import NaturalUnitSystem, UnitSystem

_TI_INITIALIZED = False


def _ti_init():
    global _TI_INITIALIZED
    if not _TI_INITIALIZED:
        ti.init(arch=ti.cpu, log_level=ti.ERROR)
        _TI_INITIALIZED = True


@dataclass(frozen=True)
class _UnitsC2(UnitSystem):
    """
    UnitSystem with c = 2, so a mutation dropping the square in
    c0_sq = c**2 produces a factor-2 error, not an identity.
    """

    @property
    def c(self):
        return 2.0

    @property
    def wavelength(self):
        return 1.0

    @property
    def dx(self):
        return 0.5

    @property
    def dt(self):
        return 0.05

    @property
    def rho_0(self):
        return 1.0

    def to_physical_length(self, x):
        return x

    def to_physical_time(self, t):
        return t

    def to_physical_energy(self, E):
        return E

    def to_physical_density(self, r):
        return r


class _SeedBasesAtStep0(BaseProcessor):
    """
    Seed PsiBase and PsiLong from numpy arrays at step 0.

    PsiLong carries a sentinel (1e6). Any processor that ignores its
    field_type and reads or writes PsiLong instead of PsiBase will
    surface as a large diff in that sentinel.
    """

    name = "_SeedBasesAtStep0"
    stage = Stage.PRE_UPDATE
    order = 5
    requires = (WaveGrid, PsiBaseField, PsiLongField)
    provides = ()

    def __init__(self, base_np, long_np):
        self.base_np = base_np
        self.long_np = long_np

    def process(self, ctx):
        if ctx.sim.step > 0:
            return
        bf = ctx.data.require(PsiBaseField)
        lf = ctx.data.require(PsiLongField)
        zeros_b = np.zeros_like(self.base_np)
        zeros_l = np.zeros_like(self.long_np)
        bf.psi.from_numpy(self.base_np)
        bf.psi_prev.from_numpy(self.base_np)
        bf.psi_new.from_numpy(zeros_b)
        lf.psi.from_numpy(self.long_np)
        lf.psi_prev.from_numpy(self.long_np)
        lf.psi_new.from_numpy(zeros_l)


def _numpy_step(psi, prev, dx, dt2, beta_rho, c0_sq):
    """
    One production step, numpy float64, no Taichi.

    Mirrors the four kernels in order: _update_rho, _update_c2,
    _laplacian_var_coeff, _leapfrog. Interior-only where the Taichi
    kernels are interior-only.
    """
    rho = 1.0 - beta_rho * np.sum(psi * psi, axis=-1)
    c2 = c0_sq * rho

    interior = (slice(1, -1),) * 3
    c_ii = c2[interior]
    c2_xp = 0.5 * (c_ii + c2[2:, 1:-1, 1:-1])
    c2_xm = 0.5 * (c_ii + c2[:-2, 1:-1, 1:-1])
    c2_yp = 0.5 * (c_ii + c2[1:-1, 2:, 1:-1])
    c2_ym = 0.5 * (c_ii + c2[1:-1, :-2, 1:-1])
    c2_zp = 0.5 * (c_ii + c2[1:-1, 1:-1, 2:])
    c2_zm = 0.5 * (c_ii + c2[1:-1, 1:-1, :-2])
    inv_dx2 = 1.0 / (dx * dx)

    flux_x = c2_xp[..., None] * (psi[2:, 1:-1, 1:-1] - psi[interior]) - c2_xm[..., None] * (
        psi[interior] - psi[:-2, 1:-1, 1:-1]
    )
    flux_y = c2_yp[..., None] * (psi[1:-1, 2:, 1:-1] - psi[interior]) - c2_ym[..., None] * (
        psi[interior] - psi[1:-1, :-2, 1:-1]
    )
    flux_z = c2_zp[..., None] * (psi[1:-1, 1:-1, 2:] - psi[interior]) - c2_zm[..., None] * (
        psi[interior] - psi[1:-1, 1:-1, :-2]
    )

    new = np.zeros_like(psi)
    new[interior] = (flux_x + flux_y + flux_z) * inv_dx2
    new[interior] = 2.0 * psi[interior] - prev[interior] + dt2 * new[interior]

    psi_out = psi.copy()
    prev_out = prev.copy()
    prev_out[interior] = psi[interior]
    psi_out[interior] = new[interior]
    return psi_out, prev_out, rho, c2


# ======================================================================
# Kernel-level tests
# ======================================================================


def test_var_coeff_const_matches_const_laplacian():
    """
    Smoke check: c^2 = c0^2 everywhere -> _laplacian_var_coeff matches
    the constant-coefficient _laplacian at every interior voxel.

    This test runs at dx = 1, where 1 / dx and 1 / dx^2 agree, so it
    cannot catch a wrong dx power; the dx power is pinned by
    test_production_pipeline_vs_numpy on the flux kernel and by
    test_production_constant_laplacian_vs_numpy on the constant kernel,
    both at dx = 0.5.

    This test cannot catch a wrong half-grid average either, because
    with a constant c^2 every neighbour reads the same value. That arm
    is caught by test_var_coeff_missing_half_average_changes_result on
    a variable c^2 field. What this test does catch: wrong stencil
    shape, wrong interior scope, wrong coefficient sign.
    """
    _ti_init()
    from .evolution import _laplacian

    N = 16
    dx = 1.0
    c0 = 2.0
    c2_val = c0 * c0

    psi = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    c2 = ti.field(dtype=ti.f32, shape=(N, N, N))
    acc_var = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    acc_const = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))

    @ti.kernel
    def _fill(p: ti.template(), c: ti.template()):
        kx = 2.0 * ti.math.pi / 8.0
        for i, j, k in p:
            p[i, j, k] = ti.Vector(
                [
                    ti.sin(kx * ti.cast(i, ti.f32)),
                    ti.cos(kx * ti.cast(j, ti.f32)),
                    0.5 * ti.sin(kx * ti.cast(k, ti.f32)),
                ]
            )
            c[i, j, k] = c2_val

    _fill(psi, c2)
    acc_var.fill(0.0)
    acc_const.fill(0.0)

    _laplacian_var_coeff(psi, c2, acc_var, N, N, N, dx)
    _laplacian(psi, acc_const, N, N, N, dx, c0)

    a = acc_var.to_numpy()
    b = acc_const.to_numpy()
    diff = np.abs(a - b).max()
    assert diff < 1e-5, f"max diff {diff}"


def test_var_coeff_accumulates_not_overwrites():
    """
    Applying twice must double the result at each interior voxel.

    Mutation: += changed to = -> second application matches first.
    """
    _ti_init()

    N = 16
    dx = 1.0

    psi = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    c2 = ti.field(dtype=ti.f32, shape=(N, N, N))
    acc = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))

    @ti.kernel
    def _fill(p: ti.template(), c: ti.template()):
        kx = 2.0 * ti.math.pi / 8.0
        for i, j, k in p:
            p[i, j, k] = ti.Vector(
                [
                    ti.sin(kx * ti.cast(i, ti.f32)),
                    0.0,
                    0.0,
                ]
            )
            c[i, j, k] = 1.0 + 0.5 * ti.sin(2.0 * kx * ti.cast(i, ti.f32))

    _fill(psi, c2)
    acc.fill(0.0)

    _laplacian_var_coeff(psi, c2, acc, N, N, N, dx)
    one = acc.to_numpy()[8, 8, 8].copy()
    _laplacian_var_coeff(psi, c2, acc, N, N, N, dx)
    two = acc.to_numpy()[8, 8, 8].copy()

    assert np.allclose(two, 2.0 * one, atol=1e-5), (one, two)


def test_var_coeff_missing_half_average_changes_result():
    """
    The production kernel and a no-average kernel must give different
    results on a variable c2 field.

    Naming: the no-average kernel is NOT a reference. It is a negative
    control. The production kernel is the correctly-averaged one; the
    local _laplacian_var_coeff_no_average is the mutation target.
    This test only shows the two kernels differ. Whether the production
    one is the flux form the plan pins is checked by
    test_flux_form_conserves_staggered_invariant.

    Mutation caught: _laplacian_var_coeff drops the half-grid average.
    """
    _ti_init()

    N = 16
    dx = 1.0

    psi = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    c2 = ti.field(dtype=ti.f32, shape=(N, N, N))
    acc_prod = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    acc_ref = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))

    @ti.kernel
    def _fill(p: ti.template(), c: ti.template()):
        kx = 2.0 * ti.math.pi / 8.0
        for i, j, k in p:
            p[i, j, k] = ti.Vector(
                [
                    ti.sin(kx * ti.cast(i, ti.f32)),
                    ti.cos(kx * ti.cast(j, ti.f32)),
                    0.0,
                ]
            )
            # c2 varies strongly with x
            c[i, j, k] = 1.0 + 0.5 * ti.sin(kx * ti.cast(i, ti.f32))

    _fill(psi, c2)
    acc_prod.fill(0.0)
    acc_ref.fill(0.0)

    _laplacian_var_coeff(psi, c2, acc_prod, N, N, N, dx)
    _laplacian_var_coeff_no_average(psi, c2, acc_ref, N, N, N, dx)

    a = acc_prod.to_numpy()
    b = acc_ref.to_numpy()
    diff = np.abs(a - b).max()
    assert diff > 1e-3, f"missing-average not detected, max diff {diff}"


@ti.kernel
def _laplacian_var_coeff_no_average(
    psi: ti.template(),
    c2: ti.template(),
    out: ti.template(),
    nx: ti.i32,
    ny: ti.i32,
    nz: ti.i32,
    dx: ti.f32,
):
    # Deliberately omits the half-grid average: uses c2 at the neighbor
    # directly. Different from production when c2 varies.
    inv_dx2 = 1.0 / (dx * dx)
    for i, j, k in ti.ndrange((1, nx - 1), (1, ny - 1), (1, nz - 1)):
        c2_xp = c2[i + 1, j, k]
        c2_xm = c2[i - 1, j, k]
        c2_yp = c2[i, j + 1, k]
        c2_ym = c2[i, j - 1, k]
        c2_zp = c2[i, j, k + 1]
        c2_zm = c2[i, j, k - 1]

        flux_x = c2_xp * (psi[i + 1, j, k] - psi[i, j, k]) - c2_xm * (
            psi[i, j, k] - psi[i - 1, j, k]
        )
        flux_y = c2_yp * (psi[i, j + 1, k] - psi[i, j, k]) - c2_ym * (
            psi[i, j, k] - psi[i, j - 1, k]
        )
        flux_z = c2_zp * (psi[i, j, k + 1] - psi[i, j, k]) - c2_zm * (
            psi[i, j, k] - psi[i, j, k - 1]
        )
        out[i, j, k] += (flux_x + flux_y + flux_z) * inv_dx2


# ======================================================================
# Energy conservation
# ======================================================================


@ti.kernel
def _seed_zero_boundary(
    psi: ti.template(),
    psi_prev: ti.template(),
    c2: ti.template(),
    n: ti.i32,
):
    kx = ti.math.pi / ti.cast(n - 1, ti.f32)
    ky = ti.math.pi / ti.cast(n - 1, ti.f32)
    kz = ti.math.pi / ti.cast(n - 1, ti.f32)
    for i, j, k in psi:
        val = (
            0.1
            * ti.sin(kx * ti.cast(i, ti.f32))
            * ti.sin(ky * ti.cast(j, ti.f32))
            * ti.sin(kz * ti.cast(k, ti.f32))
        )
        v = ti.Vector([val, 0.0, 0.0])
        psi[i, j, k] = v
        psi_prev[i, j, k] = v
        c2[i, j, k] = 1.0 + 0.3 * ti.cos(2.0 * kx * ti.cast(i, ti.f32))


@ti.kernel
def _laplacian_naive(
    psi: ti.template(),
    c2: ti.template(),
    out: ti.template(),
    nx: ti.i32,
    ny: ti.i32,
    nz: ti.i32,
    dx: ti.f32,
):
    """
    c2 * laplacian(psi), no half-grid averaging. Local negative control:
    the naive form is the equation the plan refuses to ship, so it lives
    here and not in evolution.py.
    """
    inv_dx2 = 1.0 / (dx * dx)
    for i, j, k in ti.ndrange((1, nx - 1), (1, ny - 1), (1, nz - 1)):
        lap = (
            psi[i + 1, j, k]
            + psi[i - 1, j, k]
            + psi[i, j + 1, k]
            + psi[i, j - 1, k]
            + psi[i, j, k + 1]
            + psi[i, j, k - 1]
            - 6.0 * psi[i, j, k]
        ) * inv_dx2
        out[i, j, k] += c2[i, j, k] * lap


def _leapfrog_var_coeff_step(psi, psi_prev, psi_new, c2, nx, ny, nz, dx, dt2):
    """
    One production step in flux form. Calls the three kernels from
    evolution.py, so any mutation in _clear_accel, _laplacian_var_coeff
    or _leapfrog reaches this step.
    """
    _clear_accel(psi_new, nx, ny, nz)
    _laplacian_var_coeff(psi, c2, psi_new, nx, ny, nz, dx)
    _leapfrog(psi, psi_prev, psi_new, nx, ny, nz, dt2)


def _leapfrog_naive_step(psi, psi_prev, psi_new, c2, nx, ny, nz, dx, dt2):
    """
    One step with the naive laplacian (local) and the PRODUCTION
    _leapfrog. The naive laplacian is the negative control; the leapfrog
    half is production, so mutations to _leapfrog are caught here too.
    """
    _clear_accel(psi_new, nx, ny, nz)
    _laplacian_naive(psi, c2, psi_new, nx, ny, nz, dx)
    _leapfrog(psi, psi_prev, psi_new, nx, ny, nz, dt2)


def _measure_staggered_drift(step_fn, n_steps, N, dx, dt):
    """
    Run n_steps of step_fn on a fresh seed and return the maximum
    relative excursion of the staggered invariant from its first value.

    step_fn signature: (psi, psi_prev, psi_new, c2, nx, ny, nz, dx, dt2) -> None
    Returns a non-negative float; 0.0 means the invariant was constant.
    """
    psi = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    psi_prev = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    psi_new = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    c2 = ti.field(dtype=ti.f32, shape=(N, N, N))

    _seed_zero_boundary(psi, psi_prev, c2, N)

    step_fn(psi, psi_prev, psi_new, c2, N, N, N, dx, dt * dt)
    E0 = _staggered_energy(psi, psi_prev, c2, psi_new, N, dx, dt)
    worst = 0.0
    for _ in range(n_steps - 1):
        step_fn(psi, psi_prev, psi_new, c2, N, N, N, dx, dt * dt)
        E = _staggered_energy(psi, psi_prev, c2, psi_new, N, dx, dt)
        d = abs(E - E0) / abs(E0)
        if d > worst:
            worst = d
    return worst


def _staggered_energy(psi, psi_prev, c2, scratch, N, dx, dt):
    """
    E_stag = 0.5 * ||(psi^{n+1} - psi^n)/dt||^2
           + 0.5 * <psi^n, M psi^{n+1}>
    M = -L_var (flux form).
    """
    _clear_accel(scratch, N, N, N)
    _laplacian_var_coeff(psi, c2, scratch, N, N, N, dx)
    M_psi_np1 = -scratch.to_numpy()
    p_n = psi_prev.to_numpy()
    p_np1 = psi.to_numpy()
    v = (p_np1 - p_n) / dt
    return 0.5 * (v * v).sum() + 0.5 * (p_n * M_psi_np1).sum()


def test_flux_form_conserves_staggered_invariant():
    """
    Leapfrog + flux-form LaplacianVarCoeff, variable c^2, zero boundary
    seed. The staggered invariant is conserved over 50 steps.

    The step runs the production kernels from evolution.py:
    _clear_accel, _laplacian_var_coeff, _leapfrog. A mutation in any
    of them reaches this test.

    Mutation caught: half-grid average dropped or read from the wrong
    neighbour in _laplacian_var_coeff. A single-laplacian step cannot
    tell += from = after a clear, so that arm is not claimed here; it
    is caught by test_nonlinear_composes_with_laplacian_in_pipeline.
    """
    _ti_init()

    N = 32
    dx = 1.0
    dt = 0.01
    n_steps = 50

    psi = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    psi_prev = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    psi_new = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    c2 = ti.field(dtype=ti.f32, shape=(N, N, N))

    _seed_zero_boundary(psi, psi_prev, c2, N)

    _leapfrog_var_coeff_step(psi, psi_prev, psi_new, c2, N, N, N, dx, dt * dt)
    E0 = _staggered_energy(psi, psi_prev, c2, psi_new, N, dx, dt)

    Es = [E0]
    for _ in range(n_steps - 1):
        _leapfrog_var_coeff_step(psi, psi_prev, psi_new, c2, N, N, N, dx, dt * dt)
        Es.append(_staggered_energy(psi, psi_prev, c2, psi_new, N, dx, dt))

    drift = max(abs(e - E0) for e in Es) / abs(E0)
    print(f"  flux form relative drift: {drift:.3e}")
    assert drift < 1e-4, f"flux form drift too large: {drift}"


def test_naive_form_breaks_staggered_invariant():
    """
    Leapfrog + naive form c^2_i * laplacian(psi), same seed. Drift
    must be larger than the flux-form drift by a clear margin.

    The leapfrog half is production (_leapfrog from evolution.py); the
    laplacian half is _laplacian_naive, the local negative control,
    because the naive form is the equation the plan refuses to ship.

    Mutation caught: the naive form replaced by the flux form. The
    assertion is one-sided (drift > 5e-4), so a mutation that raises
    the drift above the threshold does not fire here. Sign flips in
    _leapfrog are caught by test_flux_form_conserves_staggered_invariant
    and by test_production_pipeline_vs_numpy, not by this test.

    Measured on N=32, dt=0.01, 50 steps, zero-boundary seed:
        flux form drift  5.6e-06   (f32 rounding)
        naive form drift 8.2e-04   (operator asymmetry)
    Ratio ~146x. The naive threshold 5e-4 leaves a 1.6x margin over
    the measured value; if the flux form were accidentally substituted,
    naive would drop below 1e-5 and the check would fail.
    """
    _ti_init()

    N = 32
    dx = 1.0
    dt = 0.01
    n_steps = 50

    psi = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    psi_prev = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    psi_new = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    c2 = ti.field(dtype=ti.f32, shape=(N, N, N))

    _seed_zero_boundary(psi, psi_prev, c2, N)

    _leapfrog_naive_step(psi, psi_prev, psi_new, c2, N, N, N, dx, dt * dt)
    E0 = _staggered_energy(psi, psi_prev, c2, psi_new, N, dx, dt)

    Es = [E0]
    for _ in range(n_steps - 1):
        _leapfrog_naive_step(psi, psi_prev, psi_new, c2, N, N, N, dx, dt * dt)
        Es.append(_staggered_energy(psi, psi_prev, c2, psi_new, N, dx, dt))

    drift = max(abs(e - E0) for e in Es) / abs(E0)
    print(f"  naive form relative drift: {drift:.3e}")
    assert drift > 5e-4, f"naive form drift unexpectedly small: {drift}"


# ======================================================================
# Pipeline integration
# ======================================================================


class _SeedHarmonicLong(BaseProcessor):
    name = "_SeedHarmonicLong"
    stage = Stage.PRE_UPDATE
    order = 10
    requires = (WaveGrid, PsiLongField)
    provides = ()

    def __init__(self, amp: float = 0.3):
        self.amp = amp

    def process(self, ctx) -> None:
        if ctx.sim.step > 0:
            return
        grid = ctx.data.require(WaveGrid)
        field = ctx.data.require(PsiLongField)
        _seed_harmonic_long(field.psi, field.psi_prev, grid.nx, grid.ny, grid.nz, self.amp)


@ti.kernel
def _seed_harmonic_long(
    psi: ti.template(), prev: ti.template(), nx: ti.i32, ny: ti.i32, nz: ti.i32, amp: ti.f32
):
    kx = 2.0 * ti.math.pi / 8.0
    for i, j, k in ti.ndrange(nx, ny, nz):
        v = ti.Vector([amp * ti.sin(kx * ti.cast(i, ti.f32)), 0.0, 0.0])
        psi[i, j, k] = v
        prev[i, j, k] = v


def test_naive_form_discriminates_from_flux_form_by_ratio():
    """
    Same arena and step count for both arms. The naive-form drift
    divided by the flux-form drift must exceed 10.

    What this test catches that
    test_naive_form_breaks_staggered_invariant does not: a wiring swap
    that routes the naive-form step into the flux arm, or the flux-form
    step into the naive arm. Both leave the naive absolute drift above
    the other test's 5e-4 bar, so that test still passes; the ratio
    here falls to about 1, so this test fails.

    What this test does not catch: a mutation that scales both drifts
    equally up or down. The ratio is invariant under a common factor.
    The flux arm's absolute drift is pinned separately by
    test_flux_form_conserves_staggered_invariant; the naive arm's by
    test_naive_form_breaks_staggered_invariant.
    """
    _ti_init()

    N = 32
    dx = 1.0
    dt = 0.01
    n_steps = 50

    naive_drift = _measure_staggered_drift(_leapfrog_naive_step, n_steps, N, dx, dt)
    flux_drift = _measure_staggered_drift(_leapfrog_var_coeff_step, n_steps, N, dx, dt)

    print(f"  naive form relative drift: {naive_drift:.3e}")
    print(f"  flux form relative drift:  {flux_drift:.3e}")
    ratio = naive_drift / flux_drift if flux_drift > 0.0 else float("inf")
    print(f"  naive / flux ratio: {ratio:.1f}x")

    assert ratio > 10.0, (
        f"naive/flux ratio {ratio:.1f} below 10 "
        f"(naive {naive_drift:.3e}, flux {flux_drift:.3e}); "
        f"the naive form no longer discriminates from the flux form"
    )


def test_pipeline_runs_with_variable_coeff_chain():
    """
    Full chain: ClearAcceleration -> UpdateEMCDensity -> UpdateWaveSpeed
    -> LaplacianVariableCoeff -> Leapfrog. Runs 20 steps without error.

    Mutation: any processor's requires wrong -> PipelineError at build.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(external_provides=(UnitSystem,))
            self.add(AllocateWaveField(nx=16, ny=16, nz=16, dx=1.0))
            self.add(AllocateWaveSpeed())
            self.add(_SeedHarmonicLong(amp=0.3))
            self.add(ClearAccelerationProcessor())
            self.add(UpdateEMCDensityProcessor(beta_rho=0.1))
            self.add(UpdateWaveSpeedProcessor())
            self.add(LaplacianVariableCoeffProcessor())
            self.add(LeapfrogProcessor())

    from ..runner import Runner
    from ..sinks import InMemorySink

    runner = Runner({"session": InMemorySink()})
    ctx = runner.run(
        P(),
        name="var_coeff_chain",
        params={},
        dt=0.05,
        max_steps=20,
        initial_features=[NaturalUnitSystem()],
    )
    assert ctx.diag.errors == [], ctx.diag.errors
    assert ctx.sim.step == 20


def test_production_pipeline_vs_numpy():
    """
    Run the production chain (Allocate + Clear + EMCDensity + WaveSpeed
    + LaplacianVarCoeff + Leapfrog) for a few steps and compare PsiBase
    to a numpy float64 reference.

    Arena deliberately hostile to the common mutations:
      - non-cubic grid (6, 8, 10)
      - dx = 0.5, so 1/dx and 1/dx^2 differ by 2x
      - c = 2, so c and c^2 differ by 2x
      - psi has all three components non-zero and axis-asymmetric,
        so a rho = 1 - beta*psi[0]^2 reading sees a different field
      - PsiLong carries a 1e6 sentinel, so field_type confusion is
        loud
      - c2 varies along all three axes, so an x-neighbour read in a
        y-face term sees a different value

    Mutation: each of the following leaves the pipeline-level tests
    green but changes the output here: 1/dx for 1/dx^2, c for c^2,
    field_type ignored, rho from psi[0] only, AllocateWaveSpeed shaped
    (nx, nx, nx), wrong neighbour index in a c2 half-grid average.
    """
    _ti_init()

    nx, ny, nz = 6, 8, 10
    dx = 0.5
    dt = 0.05
    dt2 = dt * dt
    beta_rho = 0.1
    n_steps = 3
    c0 = 2.0
    c0_sq = c0 * c0

    rng = np.random.default_rng(seed=607_002)
    base_np = rng.standard_normal((nx, ny, nz, 3)).astype(np.float32) * 0.3
    long_np = np.full((nx, ny, nz, 3), 1e6, dtype=np.float32)

    # Arena invariant: the three components must be distinguishable.
    # A rho reading that picks psi[..., 0] only would otherwise see the
    # same value as the correct sum on a symmetric seed.
    per_comp = np.abs(base_np).sum(axis=(0, 1, 2))
    assert per_comp.min() > 1.0, (
        f"arena error: a component is too small ({per_comp}); a psi[0]-only "
        f"rho reading might slip through"
    )

    class P(Pipeline):
        def __init__(self):
            super().__init__(external_provides=(UnitSystem,))
            self.add(AllocateWaveField(nx=nx, ny=ny, nz=nz, dx=dx))
            self.add(AllocateWaveSpeed())
            self.add(_SeedBasesAtStep0(base_np, long_np))
            self.add(ClearAccelerationProcessor(field_type=PsiBaseField))
            self.add(UpdateEMCDensityProcessor(field_type=PsiBaseField, beta_rho=beta_rho))
            self.add(UpdateWaveSpeedProcessor())
            self.add(LaplacianVariableCoeffProcessor(field_type=PsiBaseField))
            self.add(LeapfrogProcessor(field_type=PsiBaseField))

    from ..runner import Runner
    from ..sinks import InMemorySink

    runner = Runner({"session": InMemorySink()})
    ctx = runner.run(
        P(),
        name="stage2_prod_vs_numpy",
        params={},
        dt=dt,
        max_steps=n_steps,
        initial_features=[_UnitsC2()],
    )
    assert ctx.diag.errors == [], ctx.diag.errors

    psi_prod = ctx.data.require(PsiBaseField).psi.to_numpy()
    long_after = ctx.data.require(PsiLongField).psi.to_numpy()

    # Sentinel: PsiLong must be exactly where the seed put it, since no
    # processor in the chain names PsiLongField. A field_type confusion
    # in any of them shows up here.
    assert np.allclose(long_after, long_np, atol=1e-6), (
        f"PsiLong sentinel changed; a processor ignored field_type. "
        f"max diff {np.abs(long_after - long_np).max()}"
    )

    psi_ref = base_np.astype(np.float64).copy()
    prev_ref = psi_ref.copy()
    for _ in range(n_steps):
        psi_ref, prev_ref, _, _ = _numpy_step(psi_ref, prev_ref, dx, dt2, beta_rho, c0_sq)

    diff = np.abs(psi_prod - psi_ref).max()
    assert diff < 1e-3, f"production vs numpy, {n_steps} steps: max diff {diff}"


def test_production_constant_laplacian_vs_numpy():
    """
    The constant-coefficient chain (Allocate + Clear + Laplacian +
    Leapfrog) on the arena of test_production_pipeline_vs_numpy, against
    a numpy float64 reference of psi_tt = c^2 lap(psi).

    test_production_pipeline_vs_numpy runs LaplacianVariableCoeff, so it
    never reaches LaplacianProcessor. This test pins that processor's
    wiring: c read from UnitSystem (c = 2, so 1, c and c^2 all differ),
    1/dx^2 with dx = 0.5, and field_type (the PsiLong sentinel).

    Mutation caught: LaplacianProcessor ignores units.c or passes c^2,
    swaps dx and c, ignores field_type; _laplacian uses 1/dx for 1/dx^2.
    """
    _ti_init()

    nx, ny, nz = 6, 8, 10
    dx = 0.5
    dt = 0.05
    dt2 = dt * dt
    n_steps = 3
    c0_sq = 4.0

    rng = np.random.default_rng(seed=607_003)
    base_np = rng.standard_normal((nx, ny, nz, 3)).astype(np.float32) * 0.3
    long_np = np.full((nx, ny, nz, 3), 1e6, dtype=np.float32)

    class P(Pipeline):
        def __init__(self):
            super().__init__(external_provides=(UnitSystem,))
            self.add(AllocateWaveField(nx=nx, ny=ny, nz=nz, dx=dx))
            self.add(_SeedBasesAtStep0(base_np, long_np))
            self.add(ClearAccelerationProcessor(field_type=PsiBaseField))
            self.add(LaplacianProcessor(field_type=PsiBaseField))
            self.add(LeapfrogProcessor(field_type=PsiBaseField))

    from ..runner import Runner
    from ..sinks import InMemorySink

    runner = Runner({"session": InMemorySink()})
    ctx = runner.run(
        P(),
        name="prod_const_laplacian_vs_numpy",
        params={},
        dt=dt,
        max_steps=n_steps,
        initial_features=[_UnitsC2()],
    )
    assert ctx.diag.errors == [], ctx.diag.errors

    psi_prod = ctx.data.require(PsiBaseField).psi.to_numpy()
    long_after = ctx.data.require(PsiLongField).psi.to_numpy()
    assert np.allclose(long_after, long_np, atol=1e-6), (
        f"PsiLong sentinel changed; a processor ignored field_type. "
        f"max diff {np.abs(long_after - long_np).max()}"
    )

    # beta_rho = 0 makes rho = 1 and c2 = c0^2 everywhere, so the
    # flux-form reference reduces to c0^2 * lap(psi) exactly.
    psi_ref = base_np.astype(np.float64).copy()
    prev_ref = psi_ref.copy()
    for _ in range(n_steps):
        psi_ref, prev_ref, _, _ = _numpy_step(psi_ref, prev_ref, dx, dt2, 0.0, c0_sq)

    diff = np.abs(psi_prod - psi_ref).max()
    assert diff < 1e-3, f"production vs numpy, {n_steps} steps: max diff {diff}"


# ======================================================================
# Runner
# ======================================================================


def main() -> int:
    tests = [
        test_var_coeff_const_matches_const_laplacian,
        test_var_coeff_accumulates_not_overwrites,
        test_var_coeff_missing_half_average_changes_result,
        test_flux_form_conserves_staggered_invariant,
        test_naive_form_breaks_staggered_invariant,
        test_pipeline_runs_with_variable_coeff_chain,
        test_naive_form_discriminates_from_flux_form_by_ratio,
        test_production_pipeline_vs_numpy,
        test_production_constant_laplacian_vs_numpy,
    ]
    passed = 0
    for t in tests:
        try:
            t()
        except AssertionError as e:
            print(f"FAIL: {t.__name__}: {e}")
            traceback.print_exc()
        except Exception as e:
            print(f"ERROR: {t.__name__}: {type(e).__name__}: {e}")
            traceback.print_exc()
        else:
            print(f"PASS: {t.__name__}")
            passed += 1
    print(f"\n{passed}/{len(tests)} tests passed")
    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
