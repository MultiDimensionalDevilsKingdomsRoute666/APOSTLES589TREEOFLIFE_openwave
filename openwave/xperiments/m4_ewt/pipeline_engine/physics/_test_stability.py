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
            f.psi, f.psi_prev, grid.dx ** 3,
            grid.nx, grid.ny, grid.nz,
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
    val = amp * np.exp(-r_long2 / (2.0 * sigma_long ** 2) - r_trans2 / (2.0 * sigma_trans ** 2))
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
            self.add(AllocateWaveField(nx=n, ny=n, nz=n, dx=1.0))
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

    Mutation caught: IPR formula inverted (mass^2 / quartic), or
    quartic read as mass.
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

    Mutation caught: eigvalsh ordering reversed (lambda_max/lambda_min),
    or the tensor axes swapped.
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

    Mutation caught: localization not updated between steps, or IPR
    computed only once. Threshold is a soft bar; the qualitative check
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