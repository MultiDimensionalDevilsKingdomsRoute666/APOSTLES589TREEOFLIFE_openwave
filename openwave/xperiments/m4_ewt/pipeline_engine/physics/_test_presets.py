"""
Tests for the shared pipeline builders.

The point is that the preset builds, declares the features it uses,
and that a required feature missing from initial_features surfaces as
a KeyError at its first require(), not at build time. The
processors it assembles are covered by their own tests; this module
does not re-test their physics.

Run from the project root:
    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._test_presets
"""

import sys
import traceback

import taichi as ti

from ..pipeline import BaseProcessor, Stage
from ..runner import Runner
from ..sinks import InMemorySink
from .allocator import AllocateWaveField
from .boundary import BoundaryProcessor
from .features import BoundaryCondition, PsiLongField
from .motion import NoOpRule
from .presets import make_linear_wave_pipeline
from .seed import SeedMultiCenter
from .stability import StabilityMetricsUpdate
from .units import NaturalUnitSystem, UnitSystem
from .wc_factory import build_wc_state
from .wc_types import WCState
from .vacuum import StaticVacuum, VacuumProvider, VacuumStepProcessor

_TI_INITIALIZED = False


def _ti_init():
    global _TI_INITIALIZED
    if not _TI_INITIALIZED:
        ti.init(arch=ti.cpu, log_level=ti.ERROR)
        _TI_INITIALIZED = True


_GRID = 16
_WAVELENGTH = 12.0
_SPACING = 12.0


def _wc_state(K=2):
    return build_wc_state(
        K=K,
        geometry="golden",
        nx=_GRID,
        ny=_GRID,
        nz=_GRID,
        wavelength=_WAVELENGTH,
        spacing=_SPACING,
    )


def _initial_features(wc_state=None):
    if wc_state is None:
        wc_state = _wc_state()
    return [
        NaturalUnitSystem(),
        BoundaryCondition("dirichlet"),
        wc_state,
    ]


def _run(pipeline, initial_features, max_steps=3):
    return Runner({"session": InMemorySink()}).run(
        pipeline,
        name="preset_test",
        params={},
        dt=0.1,
        max_steps=max_steps,
        initial_features=initial_features,
    )


# ======================================================================
# Build succeeds
# ======================================================================


def test_builds_and_runs():
    """
    The preset builds with the three required features and runs a few
    steps without errors.

    Mutation caught: any processor dropped from the chain, or a
    requires that cannot be satisfied by the declared provides.
    """
    _ti_init()
    p = make_linear_wave_pipeline(grid=_GRID)
    ctx = _run(p, _initial_features(), max_steps=3)
    assert ctx.diag.errors == [], ctx.diag.errors
    assert ctx.sim.step == 3


def test_declares_the_three_external_features():
    """
    The preset declares UnitSystem, BoundaryCondition and WCState in
    external_provides.

    Mutation caught: one of them dropped. A caller that provides the
    feature in initial_features still builds, since Runner.run() counts
    initial_features as provided; a caller that omits it then gets
    PipelineError at build instead of the KeyError at first use that
    the three tests below pin.
    """
    p = make_linear_wave_pipeline(grid=_GRID)
    ext = set(p._external_provides)
    assert UnitSystem in ext, ext
    assert BoundaryCondition in ext, ext
    assert WCState in ext, ext


# ======================================================================
# Missing features fail at first use
# ======================================================================


def test_missing_unitsystem_raises_at_first_use():
    """
    Removing UnitSystem from initial_features does not fail at
    Pipeline.build(): the engine trusts external_provides, so
    validation passes. The failure surfaces at the first require(),
    inside LaplacianProcessor.process, as a KeyError naming UnitSystem.

    This test pins the engine's contract: external_provides is a
    declaration, not a check. Runner.run() now also counts
    initial_features at build time, but only as an extra source, so an
    omitted instance still reaches this KeyError. If the engine ever
    grows a check that rejects a declared but absent feature at build
    time, this test goes red and the failure mode changes; the preset's
    docstring should be updated at the same time.

    Mutation caught: UnitSystem removed from the preset's
    external_provides. With the declaration gone, Pipeline.build()
    raises PipelineError naming UnitSystem, which the KeyError
    assertion below does not accept.
    """
    _ti_init()
    p = make_linear_wave_pipeline(grid=_GRID)
    initial = _initial_features()
    initial = [f for f in initial if not isinstance(f, UnitSystem)]
    try:
        _run(p, initial)
    except KeyError as e:
        assert "UnitSystem" in str(e), str(e)
        return
    raise AssertionError("expected KeyError naming UnitSystem")


def test_missing_boundary_condition_raises_at_first_use():
    """
    Removing BoundaryCondition from initial_features does not fail at
    Pipeline.build(): external_provides declares it, and the engine
    trusts the declaration. The failure surfaces at the first require()
    inside BoundaryProcessor.process, as a KeyError naming
    BoundaryCondition.

    Mutation caught: BoundaryCondition removed from the preset's
    external_provides. With the declaration gone, Pipeline.build()
    raises PipelineError naming BoundaryCondition, which the KeyError
    assertion below does not accept.
    """
    _ti_init()
    p = make_linear_wave_pipeline(grid=_GRID)
    initial = _initial_features()
    initial = [f for f in initial if not isinstance(f, BoundaryCondition)]
    try:
        _run(p, initial)
    except KeyError as e:
        assert "BoundaryCondition" in str(e), str(e)
        return
    raise AssertionError("expected KeyError naming BoundaryCondition")


def test_missing_wcstate_raises_at_first_use():
    """
    Removing WCState from initial_features does not fail at
    Pipeline.build(): external_provides declares it, and the engine
    trusts the declaration. The failure surfaces at the first require()
    inside SeedMultiCenter.process, as a KeyError naming WCState.

    Mutation caught: WCState removed from the preset's
    external_provides. With the declaration gone, Pipeline.build()
    raises PipelineError naming WCState, which the KeyError assertion
    below does not accept.
    """
    _ti_init()
    p = make_linear_wave_pipeline(grid=_GRID)
    initial = _initial_features()
    initial = [f for f in initial if not isinstance(f, WCState)]
    try:
        _run(p, initial)
    except KeyError as e:
        assert "WCState" in str(e), str(e)
        return
    raise AssertionError("expected KeyError naming WCState")


# ======================================================================
# Parameters forwarded to the constructed processors
# ======================================================================


def test_seed_radius_forwarded():
    """
    seed_radius reaches SeedMultiCenter.

    Mutation caught: seed_radius dropped, hard-coded, or swapped with
    metric_threshold.
    """
    p = make_linear_wave_pipeline(grid=_GRID, seed_radius=7.5)
    seeds = [x for x in p._all if isinstance(x, SeedMultiCenter)]
    assert len(seeds) == 1, seeds
    assert seeds[0].radius == 7.5, seeds[0].radius


def test_metric_threshold_forwarded():
    """
    metric_threshold reaches StabilityMetricsUpdate.localization_threshold.

    Mutation caught: threshold dropped, hard-coded, or swapped with
    seed_radius.
    """
    p = make_linear_wave_pipeline(grid=_GRID, metric_threshold=0.9)
    trackers = [x for x in p._all if isinstance(x, StabilityMetricsUpdate)]
    assert len(trackers) == 1, trackers
    assert trackers[0].localization_threshold == 0.9, trackers[0].localization_threshold


def test_grid_and_dx_forwarded():
    """
    grid reaches AllocateWaveField on all three axes, with dx = 1.0.

    Uses a grid other than the module's _GRID, so a size hard-coded to
    the test grid is visible.

    Mutation caught: grid dropped or hard-coded on any axis, or dx
    changed.
    """
    p = make_linear_wave_pipeline(grid=12)
    allocs = [x for x in p._all if isinstance(x, AllocateWaveField)]
    assert len(allocs) == 1, allocs
    a = allocs[0]
    assert (a.nx, a.ny, a.nz, a.dx) == (12, 12, 12, 1.0), (a.nx, a.ny, a.nz, a.dx)


def test_boundary_follows_the_feature():
    """
    BoundaryProcessor acts on PsiLongField and takes its kind from the
    BoundaryCondition feature, with no override.

    Mutation caught: a kind_override that ignores the caller's
    BoundaryCondition, or the processor pointed at another field.
    """
    p = make_linear_wave_pipeline(grid=_GRID)
    bps = [x for x in p._all if isinstance(x, BoundaryProcessor)]
    assert len(bps) == 1, bps
    assert bps[0].kind_override is None, bps[0].kind_override
    assert bps[0].field_type is PsiLongField, bps[0].field_type


# ======================================================================
# Hooks: nonlinear_terms, extra_measure
# ======================================================================


class _Marker(BaseProcessor):
    """Distinct class for hook tests. No processing."""

    name = "Marker"
    stage = Stage.UPDATE
    order = 15

    def process(self, ctx):
        pass


class _Recorder(BaseProcessor):
    """Distinct class for extra_measure. Writes a metric into a feature."""

    name = "Recorder"
    stage = Stage.MEASURE
    order = 25  # after StabilityMetricsUpdate (20)

    def process(self, ctx):
        pass


def test_nonlinear_terms_added_before_leapfrog():
    """
    The nonlinear_terms processor is present in the pipeline and, after
    the build sort, appears before LeapfrogProcessor in Stage.UPDATE.

    Mutation caught: nonlinear_terms iterated but not added (the marker
    is absent from _all), or the marker's order changed to a value that
    sorts after Leapfrog's.
    """
    marker = _Marker()
    p = make_linear_wave_pipeline(grid=_GRID, nonlinear_terms=(marker,))
    assert marker in p._all, "marker not in pipeline"
    assert p._all.count(marker) == 1, "marker added more than once"
    p.build()  # triggers the sort
    update_order = [x for x in p._by_stage[Stage.UPDATE]]
    marker_idx = update_order.index(marker)
    leapfrog_idx = next(
        i for i, x in enumerate(update_order) if type(x).__name__ == "LeapfrogProcessor"
    )
    assert marker_idx < leapfrog_idx, (marker_idx, leapfrog_idx)


def test_extra_measure_added_after_stability():
    """
    extra_measure processors land in the pipeline after
    StabilityMetricsUpdate in the MEASURE stage's effective order.

    Mutation caught: extra_measure iterated but not added, or added
    with an order below 20.
    """
    rec = _Recorder()
    p = make_linear_wave_pipeline(grid=_GRID, extra_measure=(rec,))
    assert rec in p._all, "recorder not in pipeline"
    assert p._all.count(rec) == 1, "recorder added more than once"
    p.build()
    measure_order = p._by_stage[Stage.MEASURE]
    rec_idx = measure_order.index(rec)
    track_idx = next(
        i for i, x in enumerate(measure_order) if isinstance(x, StabilityMetricsUpdate)
    )
    assert rec_idx > track_idx, (rec_idx, track_idx)


def test_empty_hooks_are_no_ops():
    """
    With no nonlinear_terms and no extra_measure, the pipeline has
    exactly the eight preset processors and nothing else.

    Mutation caught: an off-by-one that adds a placeholder processor
    even when a hook is empty.
    """
    p = make_linear_wave_pipeline(grid=_GRID)
    expected_names = {
        "AllocateWaveField",
        "SeedMultiCenter",
        "ClearAcceleration",
        "Laplacian",
        "Leapfrog",
        "BoundaryProcessor",
        "WCMotionProcessor",
        "StabilityMetricsUpdate",
    }
    actual_names = {x.name for x in p._all}
    assert actual_names == expected_names, actual_names
    assert len(p._all) == len(expected_names), [x.name for x in p._all]


def test_default_rule_is_noop():
    """
    WCMotionProcessor defaults to NoOpRule in the preset.

    Mutation caught: a drift rule accidentally used as default, which
    would move wave centres in every preset run.
    """
    p = make_linear_wave_pipeline(grid=_GRID)
    from .motion import WCMotionProcessor as _WM

    motion = [x for x in p._all if isinstance(x, _WM)]
    assert len(motion) == 1
    assert isinstance(motion[0].rule, NoOpRule), type(motion[0].rule)

def test_include_vacuum_extends_external_provides_and_chain():
    """
    With vacuum=<instance>, the preset declares VacuumProvider in
    external_provides and adds VacuumStepProcessor to the chain.

    Mutation caught: vacuum= ignored in the external_provides
    tuple or in the add() calls, so a pipeline that asked for vacuum
    support builds without the declaration or without the processor,
    and the caller's VacuumProvider instance is silently unused.
    """
    p = make_linear_wave_pipeline(grid=_GRID, vacuum=StaticVacuum())
    ext = set(p._external_provides)
    assert VacuumProvider in ext, ext
    assert any(isinstance(x, VacuumStepProcessor) for x in p._all), [
        type(x).__name__ for x in p._all
    ]


def test_include_vacuum_default_off_keeps_preset_unchanged():
    """
    With vacuum= omitted, the preset's external_provides and
    chain match the pre-vacuum shape: VacuumProvider not declared,
    VacuumStepProcessor not in the chain.

    Mutation caught: the vacuum branch taken for vacuum=None, which changes
    the external_provides contract for every existing caller and breaks
    every test that documents the three-feature declaration.
    """
    p = make_linear_wave_pipeline(grid=_GRID)
    ext = set(p._external_provides)
    assert VacuumProvider not in ext, ext
    assert not any(isinstance(x, VacuumStepProcessor) for x in p._all), [
        type(x).__name__ for x in p._all
    ]


def test_vacuum_preset_evolves_base_and_leaves_soliton_unchanged():
    """
    End to end through Runner.run: with vacuum=PeriodicVacuum() the base
    field moves off its seed, without vacuum= it stays there, and the
    soliton field is bit-identical in both runs.

    Mutation caught: VacuumStepProcessor not added by the preset (the
    base field stays at its seed), or the vacuum step writing into
    PsiLongField (the soliton runs differ). The second half is the
    VacuumStepProcessor docstring's claim that base and soliton are
    independent in the current build.
    """
    import numpy as np

    from .features import PsiBaseField
    from .seed import SeedBaseWave
    from .vacuum import PeriodicVacuum

    _ti_init()
    n = _GRID
    i, j, k = np.meshgrid(np.arange(n), np.arange(n), np.arange(n), indexing="ij")
    r2 = (i - n / 2) ** 2 + (j - n / 2) ** 2 + (k - n / 2) ** 2
    seed = np.zeros((n, n, n, 3), dtype=np.float32)
    seed[..., 0] = np.exp(-r2 / (2.0 * 4.0**2))

    runs = {}
    for label, vacuum in (("off", None), ("on", PeriodicVacuum())):
        p = make_linear_wave_pipeline(grid=n, vacuum=vacuum)
        p.add(SeedBaseWave(seed))
        initial = _initial_features()
        if vacuum is not None:
            initial.append(vacuum)
        ctx = _run(p, initial, max_steps=10)
        assert ctx.diag.errors == [], (label, ctx.diag.errors)
        runs[label] = (
            ctx.data.require(PsiBaseField).psi.to_numpy(),
            ctx.data.require(PsiLongField).psi.to_numpy(),
        )

    base_off, long_off = runs["off"]
    base_on, long_on = runs["on"]
    assert float(np.abs(base_off - seed).max()) == 0.0, "base moved without a vacuum"
    moved = float(np.abs(base_on - seed).max())
    assert moved > 1e-3, f"PeriodicVacuum did not evolve the base field: {moved}"
    assert np.array_equal(long_on, long_off), (
        "soliton field differs with the vacuum on: "
        f"max {float(np.abs(long_on - long_off).max())}"
    )

# ======================================================================
# Runner
# ======================================================================


def main() -> int:
    tests = [
        test_builds_and_runs,
        test_declares_the_three_external_features,
        test_missing_unitsystem_raises_at_first_use,
        test_missing_boundary_condition_raises_at_first_use,
        test_missing_wcstate_raises_at_first_use,
        test_seed_radius_forwarded,
        test_metric_threshold_forwarded,
        test_grid_and_dx_forwarded,
        test_boundary_follows_the_feature,
        test_nonlinear_terms_added_before_leapfrog,
        test_extra_measure_added_after_stability,
        test_empty_hooks_are_no_ops,
        test_default_rule_is_noop,
        test_include_vacuum_extends_external_provides_and_chain,
        test_include_vacuum_default_off_keeps_preset_unchanged,
        test_vacuum_preset_evolves_base_and_leaves_soliton_unchanged,
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
