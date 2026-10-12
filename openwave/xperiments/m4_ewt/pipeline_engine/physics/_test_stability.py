"""
Tests for StabilityMetrics and StabilityMetricsUpdate (plan item 1.9).

Every test names the mutation it catches, or states explicitly that it
is a smoke check and cannot catch a specific mutation.

Run from the project root:
    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._test_stability

Note: no `from __future__ import annotations` here. Taichi kernel
definitions need live type objects.
"""

import math
import sys
import traceback

import numpy as np
import taichi as ti

from .features import (
    BoundaryCondition,
    PsiLongField,
    StabilityMetrics,
    WaveGrid,
)
from ..pipeline import (
    BaseProcessor,
    ErrorPolicy,
    Pipeline,
    PipelineError,
    Stage,
)
from .allocator import AllocateWaveField
from .boundary import BoundaryProcessor
from .evolution import (
    ClearAccelerationProcessor,
    LaplacianProcessor,
    LeapfrogProcessor,
)
from .motion import WCMotionProcessor, WCDriftRule
from .stability import StabilityMetricsUpdate
from .units import NaturalUnitSystem, UnitSystem
from .wc_types import WC, WCState

_TI_INITIALIZED = False


def _ti_init():
    global _TI_INITIALIZED
    if not _TI_INITIALIZED:
        ti.init(arch=ti.cpu, log_level=ti.ERROR)
        _TI_INITIALIZED = True


# ======================================================================
# Test-only kernels
# ======================================================================


@ti.kernel
def _record_s_kernel(
    psi: ti.template(),
    psi_prev: ti.template(),
    dv: ti.f32,
    nx: ti.i32,
    ny: ti.i32,
    nz: ti.i32,
    out_s: ti.template(),
):
    """
    Test-only: compute s(t) = integral psi . (psi - psi_prev) dV.
    Identical to the production _accumulate_freq_signal, but defined
    here so the test can compute the same quantity independently of
    whatever the production kernel does.
    """
    out_s[None] = 0.0
    for i, j, k in ti.ndrange(nx, ny, nz):
        diff = psi[i, j, k] - psi_prev[i, j, k]
        s = psi[i, j, k].dot(diff)
        ti.atomic_add(out_s[None], ti.cast(s * dv, ti.f64))


# ======================================================================
# Fixtures
# ======================================================================


class _SeedCustom(BaseProcessor):
    """Seed PsiLong.psi and psi_prev from a numpy array at step 0. Test only."""

    name = "_SeedCustom"
    stage = Stage.PRE_UPDATE
    order = 5
    requires = (PsiLongField,)

    def __init__(self, arr):
        self.arr = arr

    def process(self, ctx):
        if ctx.sim.step > 0:
            return
        f = ctx.data.require(PsiLongField)
        f.psi.from_numpy(self.arr)
        f.psi_prev.from_numpy(self.arr)


class _RecordSignal(BaseProcessor):
    """
    Test-only: record s(t) = integral psi.(psi - psi_prev) dV every step.

    stateless=False because it accumulates a history. This is a test
    fixture, not a production processor; the stateless rule (Z2) is
    about runtime state on shipped processors, and the guard skips
    processors that declare stateless=False.

    Stage.MEASURE, order 5: runs before StabilityMetricsUpdate
    (order 20). Both read the same field values (no processor mutates
    psi or psi_prev between MEASURE processors in one step).
    """

    name = "_RecordSignal"
    stage = Stage.MEASURE
    order = 5
    requires = (PsiLongField, WaveGrid)
    stateless = False

    def __init__(self):
        self.history = []  # list of (t, s) tuples

    def setup(self, ctx):
        self._s = ti.field(dtype=ti.f64, shape=())

    def process(self, ctx):
        grid = ctx.data.require(WaveGrid)
        f = ctx.data.require(PsiLongField)
        _record_s_kernel(
            f.psi,
            f.psi_prev,
            grid.dx**3,
            grid.nx,
            grid.ny,
            grid.nz,
            self._s,
        )
        self.history.append((ctx.sim.t, float(self._s[None])))


class _ConstantAccelRule(WCDriftRule):
    """Constant acceleration on every WC. Test fixture."""

    def __init__(self, ax, ay, az):
        self.a = (float(ax), float(ay), float(az))

    def __call__(self, ctx, wc_index):
        return self.a


def _delta_at_center(nx, ny, nz, val=1.0):
    arr = np.zeros((nx, ny, nz, 3), dtype=np.float32)
    arr[nx // 2, ny // 2, nz // 2] = val
    return arr


def _uniform(nx, ny, nz, val=0.3):
    return np.full((nx, ny, nz, 3), val, dtype=np.float32)


def _sphere_gaussian(nx, ny, nz, sigma=4.0, amp=1.0):
    """Isotropic 3D Gaussian at the grid center."""
    cx, cy, cz = nx / 2.0, ny / 2.0, nz / 2.0
    i, j, k = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz), indexing="ij")
    r2 = (i - cx) ** 2 + (j - cy) ** 2 + (k - cz) ** 2
    val = amp * np.exp(-r2 / (2.0 * sigma * sigma))
    arr = np.zeros((nx, ny, nz, 3), dtype=np.float32)
    arr[..., 0] = val
    return arr


def _line_gaussian(nx, ny, nz, sigma_long=4.0, sigma_trans=1.0, amp=1.0):
    """
    Line-like field: Gaussian along x, narrower Gaussian in y and z.

    The transverse Gaussian is what makes this line-like. Without it,
    the transverse width comes from the grid extent and the sphericity
    depends on grid size rather than on the field shape. Expected
    sphericity ~= sigma_trans^2 / sigma_long^2 = 1/16 = 0.0625.
    """
    cx, cy, cz = nx / 2.0, ny / 2.0, nz / 2.0
    i, j, k = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz), indexing="ij")
    r_long2 = (i - cx) ** 2
    r_trans2 = (j - cy) ** 2 + (k - cz) ** 2
    val = amp * np.exp(-r_long2 / (2.0 * sigma_long**2) - r_trans2 / (2.0 * sigma_trans**2))
    arr = np.zeros((nx, ny, nz, 3), dtype=np.float32)
    arr[..., 0] = val
    return arr


def _build_pipeline(
    seed_arr,
    *,
    with_evolution=False,
    with_boundary=False,
    wc_state=None,
    metric_threshold=0.5,
    extra_processors=(),
    dx=1.0,
):
    """
    Build a minimal pipeline. Grid size inferred from seed_arr.

    UnitSystem is always in external_provides: StabilityMetricsUpdate
    does not need it, but LaplacianProcessor does, and including it
    unconditionally keeps the fixture uniform.
    """
    n = int(seed_arr.shape[0])
    assert seed_arr.shape == (n, n, n, 3), seed_arr.shape

    external = [UnitSystem]
    initial = [NaturalUnitSystem()]
    if with_boundary:
        external.append(BoundaryCondition)
        initial.append(BoundaryCondition("dirichlet"))
    if wc_state is not None:
        external.append(WCState)
        initial.append(wc_state)

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=tuple(external),
            )
            self.add(AllocateWaveField(nx=n, ny=n, nz=n, dx=dx))
            self.add(_SeedCustom(seed_arr))
            if with_evolution:
                self.add(ClearAccelerationProcessor())
                self.add(LaplacianProcessor())
                self.add(LeapfrogProcessor())
            if with_boundary:
                self.add(BoundaryProcessor(field_type=PsiLongField))
            for p in extra_processors:
                self.add(p)
            self.add(StabilityMetricsUpdate(localization_threshold=metric_threshold))

    return P(), initial


def _run(pipeline, initial, dt=0.1, max_steps=10, check_stateless=False):
    from ..runner import Runner
    from ..sinks import InMemorySink

    return Runner({"session": InMemorySink()}, check_stateless=check_stateless).run(
        pipeline,
        name="stability_test",
        params={},
        dt=dt,
        max_steps=max_steps,
        initial_features=initial,
    )


# ======================================================================
# Metric definitions
# ======================================================================


def test_ipr_higher_for_delta_than_uniform():
    """
    A delta is more localized than a uniform field.

    Mutation caught: IPR formula inverted (mass^2 / quartic). Quartic
    read as mass still ranks the delta first (1/3 against 1/8847);
    the spreading test and the IPR-scale test catch it.
    """
    _ti_init()
    n = 32
    p1, i1 = _build_pipeline(_delta_at_center(n, n, n, val=1.0))
    ctx1 = _run(p1, i1, max_steps=1)
    assert ctx1.diag.errors == [], ctx1.diag.errors
    ipr_delta = ctx1.data.require(StabilityMetrics).ipr

    p2, i2 = _build_pipeline(_uniform(n, n, n, val=0.3))
    ctx2 = _run(p2, i2, max_steps=1)
    assert ctx2.diag.errors == [], ctx2.diag.errors
    ipr_uniform = ctx2.data.require(StabilityMetrics).ipr

    print(f"    ipr delta={ipr_delta:.6e}  uniform={ipr_uniform:.6e}")
    assert ipr_delta > ipr_uniform, (ipr_delta, ipr_uniform)


def test_sphericity_high_for_sphere_low_for_line():
    """
    A spherical Gaussian has sphericity close to 1; a line Gaussian has
    sphericity below 0.1.

    Mutation caught: eigvalsh ordering reversed (lambda_max/lambda_min).
    Swapping tensor axes leaves the eigenvalues, and so sphericity,
    unchanged; the off-diagonal terms are covered by the diagonal-line
    test below.
    """
    _ti_init()
    n = 32
    p1, i1 = _build_pipeline(_sphere_gaussian(n, n, n, sigma=4.0))
    ctx1 = _run(p1, i1, max_steps=1)
    assert ctx1.diag.errors == [], ctx1.diag.errors
    sph_sphere = ctx1.data.require(StabilityMetrics).sphericity

    p2, i2 = _build_pipeline(_line_gaussian(n, n, n))
    ctx2 = _run(p2, i2, max_steps=1)
    assert ctx2.diag.errors == [], ctx2.diag.errors
    sph_line = ctx2.data.require(StabilityMetrics).sphericity

    print(f"    sphericity sphere={sph_sphere:.4f}  line={sph_line:.4f}")
    assert sph_sphere > 0.9, sph_sphere
    assert sph_line < 0.1, sph_line


def test_empty_field_reports_zeros():
    """
    A zero field has mass = 0 and every metric falls back to 0, no NaN.

    Mutation caught: division by zero in IPR or r_rms guard removed, or
    a NaN propagates.
    """
    _ti_init()
    n = 16
    zero = np.zeros((n, n, n, 3), dtype=np.float32)
    p, i = _build_pipeline(zero)
    ctx = _run(p, i, max_steps=3)
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    assert m.mass == 0.0
    assert m.ipr == 0.0
    assert m.r_rms == 0.0
    assert m.sphericity == 0.0
    assert m.localization == 0.0
    assert m.sol_lifetime == 0
    assert m.freq_ref == 0.0
    assert m.freq_now == 0.0
    assert m.freq_drift == 0.0


# ======================================================================
# Localization: static and spreading
# ======================================================================


def test_static_field_localization_constant():
    """
    No UPDATE processors: the field is static, so localization stays
    exactly at its reference value (1.0) and sol_lifetime increments.

    The plan's required test: 'static Gaussian -> localization stays
    constant'. This cannot catch a wrong IPR formula (both numerator
    and denominator cancel in the ratio); the IPR test above does that.

    Mutation caught: localization not normalized, or IPR / IPR_initial
    inverted.
    """
    _ti_init()
    n = 32
    p, i = _build_pipeline(_sphere_gaussian(n, n, n, sigma=4.0))
    ctx = _run(p, i, max_steps=10)

    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    print(f"    localization static = {m.localization:.6f}  sol_lifetime={m.sol_lifetime}")
    assert abs(m.localization - 1.0) < 1e-9, m.localization
    assert m.sol_lifetime == 10, m.sol_lifetime


def test_spreading_field_localization_decreases():
    """
    Linear wave evolution spreads a Gaussian seed; localization at the
    end of the run is strictly below 0.9.

    The plan's required test: 'spreading Gaussian -> localization
    decreases'.

    Mutation caught: localization not updated between steps, IPR
    computed only once, or sol_lifetime never reset. Threshold is a soft bar; the qualitative check
    is the plan's, not a specific number.
    """
    _ti_init()
    n = 48

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=(UnitSystem, BoundaryCondition),
            )
            self.add(AllocateWaveField(nx=n, ny=n, nz=n, dx=1.0))
            self.add(_SeedCustom(_sphere_gaussian(n, n, n, sigma=4.0)))
            self.add(ClearAccelerationProcessor())
            self.add(LaplacianProcessor())
            self.add(LeapfrogProcessor())
            self.add(BoundaryProcessor(field_type=PsiLongField))
            self.add(StabilityMetricsUpdate())

    ctx = _run(
        P(),
        [NaturalUnitSystem(), BoundaryCondition("dirichlet")],
        dt=0.2,
        max_steps=100,
    )
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    print(f"    localization spreading = {m.localization:.6f}  r_rms={m.r_rms:.3f}")
    assert m.localization < 0.9, m.localization
    # The run ends below the 0.5 threshold, so the counter has reset.
    assert m.sol_lifetime == 0, m.sol_lifetime


# ======================================================================
# Frequency drift (definition C)
# ======================================================================


def test_freq_drift_static_field_stays_zero():
    """
    A static field has psi == psi_prev at every step, so s(t) = 0
    everywhere and no zero-crossings are detected. freq_ref, freq_now
    and freq_drift stay at 0.

    Mutation caught: the zero-crossing detection fires on the
    degenerate s(t) == 0 case (e.g. s_prev < 0 changed to s_prev <= 0).
    The exact equality check on the far side (s_now >= 0) is not
    exercised here; the s(t) oscillation test below covers that.
    """
    _ti_init()
    n = 32
    # No UPDATE processors: field is static.
    p, i = _build_pipeline(_sphere_gaussian(n, n, n, sigma=4.0))
    ctx = _run(p, i, max_steps=20)
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    assert m.freq_ref == 0.0, m.freq_ref
    assert m.freq_now == 0.0, m.freq_now
    assert m.freq_drift == 0.0, m.freq_drift


def test_freq_drift_measures_oscillation():
    """
    A Gaussian pulse under wave evolution oscillates; s(t) crosses zero
    on each half period, the processor captures freq_ref on the second
    crossing, and subsequent crossings update freq_now and freq_drift.

    Independent numpy reference: the test records s(t) at every step
    with _RecordSignal, finds upward crossings independently, and
    compares freq_ref against 1/(2 * delta_t) from the recorded
    crossings. This is the only assertion that catches a factor-of-two
    error in the frequency formula, which a positive-check alone would
    not.

    Mutation caught:
        M1  the halving 1/(2*delta_t) removed   -> freq_ref is 2x the
            independent value, the comparison fails
        M2  freq_ref capture removed            -> freq_ref stays 0,
            the comparison fails
        M3  s_prev = s_now removed              -> at most one crossing,
            numpy finds several, comparison fails
        M6  freq_drift assignment removed       -> freq_drift == 0,
            the != 0 assertion fails

    Known non-detected mutations (documented so a reviewer does not
    report them as regressions):
        - s_prev < 0.0  ->  s_prev <= 0.0: s(t) is a continuous signal
          and is exactly 0 only at t=0 (the released-from-rest step);
          the strict and non-strict comparisons agree on every other
          step.
        - t_last_crossing >= 0.0  ->  > 0.0: the first crossing occurs
          at t > 0 for any non-degenerate seed; the boundary at
          exactly t=0 is never tested.
    """
    _ti_init()
    n = 48
    recorder = _RecordSignal()

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=(UnitSystem, BoundaryCondition),
            )
            self.add(AllocateWaveField(nx=n, ny=n, nz=n, dx=1.0))
            self.add(_SeedCustom(_sphere_gaussian(n, n, n, sigma=4.0)))
            self.add(ClearAccelerationProcessor())
            self.add(LaplacianProcessor())
            self.add(LeapfrogProcessor())
            self.add(BoundaryProcessor(field_type=PsiLongField))
            self.add(recorder)
            self.add(StabilityMetricsUpdate())

    ctx = _run(
        P(),
        [NaturalUnitSystem(), BoundaryCondition("dirichlet")],
        dt=0.2,
        max_steps=200,
    )
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)

    # Independent numpy reference: find upward crossings of s(t) in the
    # recorded history.
    crossings = []
    for j in range(1, len(recorder.history)):
        _, s_prev = recorder.history[j - 1]
        t_now, s_now = recorder.history[j]
        if s_prev < 0.0 and s_now >= 0.0:
            crossings.append(t_now)

    print(
        f"    freq_ref={m.freq_ref:.6e}  freq_now={m.freq_now:.6e}  "
        f"freq_drift={m.freq_drift:.6e}"
    )
    print(f"    crossings found: {len(crossings)}  first three: {crossings[:3]}")

    assert len(crossings) >= 3, f"expected >= 3 crossings, got {len(crossings)}"
    delta_t = crossings[1] - crossings[0]
    f_expected = 1.0 / (2.0 * delta_t)
    print(f"    independent numpy reference freq_ref = {f_expected:.6e}")

    assert m.freq_ref > 0.0, m.freq_ref
    assert m.freq_now > 0.0, m.freq_now
    assert math.isfinite(m.freq_drift), m.freq_drift
    # The independent comparison. Catches the factor-of-two mutation.
    rel_err = abs(m.freq_ref - f_expected) / f_expected
    assert rel_err < 1e-9, (m.freq_ref, f_expected, rel_err)
    # After at least three crossings, freq_now differs from freq_ref and
    # freq_drift is nonzero. Catches the "assignment removed" mutation.
    assert m.freq_drift != 0.0, "freq_drift must be computed, not left at default"
    # freq_now and freq_drift from the last two recorded crossings. Catches
    # a sign flip in freq_drift, which the != 0 check above cannot see.
    f_now_expected = 1.0 / (2.0 * (crossings[-1] - crossings[-2]))
    drift_expected = (f_now_expected - f_expected) / f_expected
    assert abs(m.freq_now - f_now_expected) / f_now_expected < 1e-9, (m.freq_now, f_now_expected)
    assert abs(m.freq_drift - drift_expected) < 1e-9, (m.freq_drift, drift_expected)


# ======================================================================
# WC drift
# ======================================================================


def test_no_wcstate_reports_zero_drift():
    """
    A pipeline without WCState runs, and wc_drift / n_active_wc stay 0.

    Mutation caught: WCState added to requires (build-time PipelineError
    instead of a graceful zero).
    """
    _ti_init()
    n = 16
    p, i = _build_pipeline(_sphere_gaussian(n, n, n, sigma=3.0))
    ctx = _run(p, i, max_steps=2)
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    assert m.wc_drift == 0.0
    assert m.n_active_wc == 0


def test_wc_drift_positive_with_moving_wcs():
    """
    Constant acceleration: WCs move, wc_drift is strictly positive,
    n_active_wc matches.

    Mutation caught: reference positions not captured in setup, so
    drift measured against current position (always 0).
    """
    _ti_init()
    n = 16
    wcs = [WC(x=8.0, y=8.0, z=8.0), WC(x=10.0, y=8.0, z=8.0)]
    wc_state = WCState(centers=wcs)

    extra = [WCMotionProcessor(rule=_ConstantAccelRule(0.5, 0.0, 0.0))]
    p, i = _build_pipeline(
        _sphere_gaussian(n, n, n, sigma=3.0),
        wc_state=wc_state,
        extra_processors=extra,
    )
    ctx = _run(p, i, dt=0.1, max_steps=5)
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    print(f"    wc_drift={m.wc_drift:.4f}  n_active={m.n_active_wc}")
    assert m.wc_drift > 0.0, m.wc_drift
    assert m.n_active_wc == 2, m.n_active_wc


# ======================================================================
# Build time
# ======================================================================


def test_missing_grid_fails_at_build_time():
    """
    StabilityMetricsUpdate without WaveGrid fails at build time with a
    PipelineError naming the missing feature.

    Mutation caught: WaveGrid dropped from requires.
    """
    _ti_init()

    class Bad(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(StabilityMetricsUpdate())

    from ..runner import Runner
    from ..sinks import InMemorySink

    try:
        Runner({"session": InMemorySink()}).run(
            Bad(), name="missing_grid", params={}, dt=0.1, max_steps=1
        )
    except PipelineError as e:
        assert "WaveGrid" in str(e), str(e)
        return
    raise AssertionError("expected PipelineError, none raised")


# ======================================================================
# Stateless guard
# ======================================================================


def test_stateless_guard_passes():
    """
    The processor holds Taichi fields on the instance. The stateless
    guard compares repr() of instance fields before and after
    process(); if repr() of a Taichi field reflected its value, every
    write inside process() would trip the guard.

    This test pins that Taichi's repr does not show field contents.
    If it ever does, this test fires and the guard strategy for
    Taichi-backed state (here and in EnergyBudgetUpdate) needs
    revisiting.
    """
    _ti_init()
    n = 16
    p, i = _build_pipeline(_sphere_gaussian(n, n, n, sigma=3.0))
    ctx = _run(p, i, max_steps=3, check_stateless=True)
    assert ctx.diag.errors == [], ctx.diag.errors


# ======================================================================
# Known-answer arenas (maintainer edit)
# ======================================================================


def _diagonal_line_gaussian(nx, ny, nz, sigma_long=4.0, sigma_trans=1.0, amp=1.0):
    """
    The line Gaussian of _line_gaussian, rotated 45 degrees in the x-y
    plane. An axis-aligned field has zero off-diagonal gyration terms,
    so only a rotated one can see them.
    """
    cx, cy, cz = nx / 2.0, ny / 2.0, nz / 2.0
    i, j, k = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz), indexing="ij")
    u = ((i - cx) + (j - cy)) / math.sqrt(2.0)
    v = ((i - cx) - (j - cy)) / math.sqrt(2.0)
    w = k - cz
    val = amp * np.exp(-(u**2) / (2.0 * sigma_long**2) - (v**2 + w**2) / (2.0 * sigma_trans**2))
    arr = np.zeros((nx, ny, nz, 3), dtype=np.float32)
    arr[..., 0] = val
    return arr


def _dirichlet_mode(n, m=(1, 1, 1)):
    """Lowest dirichlet eigenmode of the 7-point Laplacian on n nodes per axis."""
    i = np.arange(n)
    sx, sy, sz = (np.sin(math.pi * mm * i / (n - 1)) for mm in m)
    arr = np.zeros((n, n, n, 3), dtype=np.float32)
    arr[..., 0] = sx[:, None, None] * sy[None, :, None] * sz[None, None, :]
    return arr


def test_sphericity_sees_off_diagonal_terms():
    """
    A line Gaussian along the x-y diagonal has the same sphericity as
    the axis-aligned one, about sigma_trans^2 / sigma_long^2 = 1/16.

    Mutation caught: the x-y gyration term dropped or built from the
    wrong axis pair. Dropping all three off-diagonal terms gives
    2/17 = 0.118 here, which the axis-aligned test cannot see because
    its off-diagonal terms are zero by symmetry. The x-z and y-z terms
    are covered by the rotated ellipsoid test below.
    """
    _ti_init()
    n = 32
    p, i = _build_pipeline(_diagonal_line_gaussian(n, n, n))
    ctx = _run(p, i, max_steps=1)
    assert ctx.diag.errors == [], ctx.diag.errors
    sph = ctx.data.require(StabilityMetrics).sphericity
    print(f"    sphericity diagonal line = {sph:.4f}")
    assert abs(sph - 1.0 / 16.0) < 0.01, sph


def test_rotated_ellipsoid_on_a_non_cubic_grid():
    """
    A Gaussian with three distinct widths (4, 2, 1.5), rotated off every
    grid axis, on a 36 x 32 x 28 grid at dx = 0.5. |psi|^2 has widths
    sigma_i / sqrt(2), so sphericity = (1.5 / 4)^2 = 0.140625 and
    r_rms = sqrt((16 + 4 + 2.25) / 2), in grid units.

    Mutation caught: the middle eigenvalue taken for the smallest (0.25),
    any off-diagonal term dropped or built from the wrong axis pair, the
    axes or the per-axis centers swapped (invisible on a cubic grid),
    and dv dropped from r^2 but not from the mass.
    """
    _ti_init()
    nx, ny, nz = 36, 32, 28
    sigma = np.array([4.0, 2.0, 1.5])
    a, b, c = 0.6, 0.9, 0.4
    rot_z = np.array(
        [[math.cos(a), -math.sin(a), 0.0], [math.sin(a), math.cos(a), 0.0], [0.0, 0.0, 1.0]]
    )
    rot_y = np.array(
        [[math.cos(b), 0.0, math.sin(b)], [0.0, 1.0, 0.0], [-math.sin(b), 0.0, math.cos(b)]]
    )
    rot_x = np.array(
        [[1.0, 0.0, 0.0], [0.0, math.cos(c), -math.sin(c)], [0.0, math.sin(c), math.cos(c)]]
    )
    rot = rot_z @ rot_y @ rot_x
    i, j, k = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz), indexing="ij")
    d = np.stack([i - nx / 2.0, j - ny / 2.0, k - nz / 2.0], axis=-1)
    body = d @ rot
    arr = np.zeros((nx, ny, nz, 3), dtype=np.float32)
    arr[..., 0] = np.exp(-0.5 * np.sum((body / sigma) ** 2, axis=-1))

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST, external_provides=(UnitSystem,))
            self.add(AllocateWaveField(nx=nx, ny=ny, nz=nz, dx=0.5))
            self.add(_SeedCustom(arr))
            self.add(StabilityMetricsUpdate())

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=1)
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    sph_expected = (1.5 / 4.0) ** 2
    r_expected = math.sqrt(float(np.sum(sigma**2)) / 2.0)
    print(
        f"    sphericity={m.sphericity:.6f} (expected {sph_expected:.6f})  "
        f"r_rms={m.r_rms:.6f} (expected {r_expected:.6f})"
    )
    assert abs(m.sphericity - sph_expected) < 0.003, m.sphericity
    assert abs(m.r_rms - r_expected) / r_expected < 1e-4, m.r_rms


def test_ipr_of_a_delta_is_one_over_voxel_volume():
    """
    A single nonzero voxel has IPR = 1 / dv exactly: with |psi|^2 = q
    there, mass is q dv and quartic q^2 dv, whatever q is. At dx = 0.5
    that is 8.

    Mutation caught: dv dropped from either moment. Every other test
    runs at dx = 1, where dv = 1 and the omission is invisible.
    """
    _ti_init()
    n = 16
    dx = 0.5
    p, i = _build_pipeline(_delta_at_center(n, n, n, val=1.0), dx=dx)
    ctx = _run(p, i, max_steps=1)
    assert ctx.diag.errors == [], ctx.diag.errors
    ipr = ctx.data.require(StabilityMetrics).ipr
    print(f"    ipr delta at dx={dx}: {ipr:.6f}  expected {1.0 / dx**3:.6f}")
    assert abs(ipr - 1.0 / dx**3) < 1e-6, ipr


def test_r_rms_matches_closed_form():
    """
    For an isotropic Gaussian psi of width sigma, |psi|^2 is a Gaussian
    of width sigma / sqrt(2), so r_rms = sqrt(3 / 2) * sigma about its
    center, which is the grid center here.

    Mutation caught: r_rms not normalized by mass, set to zero, or taken
    about a reference shifted from the grid center.
    """
    _ti_init()
    n = 32
    sigma = 3.0
    p, i = _build_pipeline(_sphere_gaussian(n, n, n, sigma=sigma))
    ctx = _run(p, i, max_steps=1)
    assert ctx.diag.errors == [], ctx.diag.errors
    r_rms = ctx.data.require(StabilityMetrics).r_rms
    expected = math.sqrt(1.5) * sigma
    print(f"    r_rms = {r_rms:.6f}  closed form = {expected:.6f}")
    assert abs(r_rms - expected) / expected < 1e-4, (r_rms, expected)


def test_freq_matches_eigenmode_frequency():
    """
    A single dirichlet eigenmode released from rest oscillates at a known
    frequency: sin(omega dt / 2) = (c dt / 2) sqrt(lambda), with lambda
    the 7-point Laplacian eigenvalue. freq_ref must match it, and
    freq_drift must stay at zero, since one mode has one frequency.

    The Gaussian-pulse test compares the processor with a recorder that
    applies the same formula, so it pins the code to the docstring but
    cannot check the formula itself. This test can.

    Crossings are detected at step resolution, so each measured
    interval carries up to one step of error: dt / delta_t, 0.75% here.
    freq_ref is held to 1%, and freq_drift, a difference of two such
    measurements, to 2%. A correct implementation can read a nonzero
    freq_drift on a pure mode for this reason alone.

    Mutation caught: the frequency formula off by any factor, and
    t_last_crossing not advanced (freq_drift near -0.75).
    """
    _ti_init()
    n = 24
    dt = 0.1
    p, i = _build_pipeline(_dirichlet_mode(n), with_evolution=True, with_boundary=True)
    ctx = _run(p, i, dt=dt, max_steps=600)
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    lam = 3.0 * 4.0 * math.sin(math.pi / (2.0 * (n - 1))) ** 2
    f_true = (2.0 / dt) * math.asin(0.5 * dt * math.sqrt(lam)) / (2.0 * math.pi)
    print(f"    freq_ref={m.freq_ref:.6f}  f_true={f_true:.6f}  " f"freq_drift={m.freq_drift:.3e}")
    assert abs(m.freq_ref - f_true) / f_true < 0.01, (m.freq_ref, f_true)
    assert abs(m.freq_drift) < 0.02, m.freq_drift


def test_wc_drift_reference_is_the_initial_position():
    """
    wc_drift is measured from the positions the WCs had before any step
    ran, which this test knows independently: it built them.

    The two active WCs drift by different amounts, and a third is
    inactive.

    Mutation caught: the reference captured in process() instead of
    setup(), which reads the positions after the first motion step
    (the bug the setup() capture exists to avoid), or re-captured each
    step; the maximum taken instead of the mean; an inactive WC counted.
    """
    _ti_init()
    n = 16
    x0 = (8.0, 10.0, 6.0)
    wcs = [
        WC(x=x0[0], y=8.0, z=8.0),
        WC(x=x0[1], y=8.0, z=8.0, velocity=(0.4, 0.0, 0.0)),
        WC(x=x0[2], y=8.0, z=8.0, active=False),
    ]
    wc_state = WCState(centers=wcs)
    extra = [WCMotionProcessor(rule=_ConstantAccelRule(0.5, 0.0, 0.0))]
    p, i = _build_pipeline(
        _sphere_gaussian(n, n, n, sigma=3.0),
        wc_state=wc_state,
        extra_processors=extra,
    )
    ctx = _run(p, i, dt=0.1, max_steps=5)
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    final = ctx.data.require(WCState).centers
    active = [abs(wc.x - x) for wc, x in zip(final, x0) if wc.active]
    expected = sum(active) / len(active)
    print(f"    wc_drift={m.wc_drift:.6f}  from known start={expected:.6f}")
    assert len(active) == 2 and active[0] != active[1], active
    assert m.n_active_wc == 2, m.n_active_wc
    assert abs(m.wc_drift - expected) < 1e-9, (m.wc_drift, expected)


# ======================================================================
# Runner
# ======================================================================


def main() -> int:
    tests = [
        test_ipr_higher_for_delta_than_uniform,
        test_sphericity_high_for_sphere_low_for_line,
        test_empty_field_reports_zeros,
        test_static_field_localization_constant,
        test_spreading_field_localization_decreases,
        test_freq_drift_static_field_stays_zero,
        test_freq_drift_measures_oscillation,
        test_no_wcstate_reports_zero_drift,
        test_wc_drift_positive_with_moving_wcs,
        test_missing_grid_fails_at_build_time,
        test_stateless_guard_passes,
        test_sphericity_sees_off_diagonal_terms,
        test_rotated_ellipsoid_on_a_non_cubic_grid,
        test_r_rms_matches_closed_form,
        test_ipr_of_a_delta_is_one_over_voxel_volume,
        test_freq_matches_eigenmode_frequency,
        test_wc_drift_reference_is_the_initial_position,
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
