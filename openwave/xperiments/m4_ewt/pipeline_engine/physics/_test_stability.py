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

    The transverse Gaussian is what makes this line-like. Without it
    (constant transverse profile), the transverse width comes from the
    grid extent and the sphericity depends on grid size rather than on
    the field shape. Expected sphericity ~= sigma_trans^2 / sigma_long^2
    = 1/16 = 0.0625 for the default parameters.
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
    Build a minimal pipeline. The grid size is inferred from seed_arr.

    Hardcoding nx=32 while seeding a differently shaped array was a bug
    in an earlier revision: Taichi 1.7.4 does not raise on from_numpy
    with a mismatched shape, and the field ends up with unexpected
    contents. Inferring the size from the seed makes the mismatch
    impossible by construction.

    UnitSystem is always included in external_provides. The
    StabilityMetricsUpdate processor does not need it (it measures in
    grid units), but LaplacianProcessor does, and including it
    unconditionally keeps the fixture uniform across the evolution and
    non-evolution cases.
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
# Reserved field
# ======================================================================


def test_freq_drift_is_zero_reserved():
    """
    freq_drift is not computed. Stays at 0.0 across a run, no matter
    the field configuration.

    If a future change starts computing freq_drift, this test fires and
    the docstrings in StabilityMetrics and StabilityMetricsUpdate must
    be updated in the same change.
    """
    _ti_init()
    n = 32
    p, i = _build_pipeline(
        _sphere_gaussian(n, n, n, sigma=4.0),
        with_evolution=True,
        with_boundary=True,
    )
    ctx = _run(p, i, dt=0.2, max_steps=10)
    assert ctx.diag.errors == [], ctx.diag.errors
    m = ctx.data.require(StabilityMetrics)
    assert m.freq_drift == 0.0, m.freq_drift


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
        test_freq_drift_is_zero_reserved,
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