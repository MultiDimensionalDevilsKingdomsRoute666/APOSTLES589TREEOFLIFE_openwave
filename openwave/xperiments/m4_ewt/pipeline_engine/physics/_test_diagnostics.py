"""
Tests for DiagnosticProcessor and the built-in stop conditions (plan
item 1.18).

Every test names the mutation it catches, or states explicitly that it
is a happy-path smoke check. The not-happy-path arms are:
  - `test_stop_condition_triggers_should_stop` (the forced violation
    the plan requires: run with a condition that always fires, verify
    the run stopped early);
  - `test_missing_stability_metrics_fails_at_build` (a condition that
    needs a feature the pipeline does not provide is rejected at build
    time, not at first call);
  - `test_requires_aggregated_from_conditions` (the requires union is
    computed from the conditions, and dropping a condition drops its
    require);
  - `test_empty_conditions_rejected` (an empty list is not a silent
    no-op).

Run from the project root:

    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._test_diagnostics
"""

import sys
import traceback

import taichi as ti

from ..pipeline import (
    BaseProcessor,
    ErrorPolicy,
    Pipeline,
    PipelineError,
    Stage,
)
from ..runner import Runner
from ..sinks import InMemorySink

from .allocator import AllocateWaveField
from .diagnostics import (
    DiagnosticProcessor,
    EnergyDriftCondition,
    LocalizationBelowCondition,
    MaxRhoCondition,
    SphericityBelowCondition,
    StopCondition,
)
from .features import EMCDensityField, EnergyBudget, StabilityMetrics
from .units import NaturalUnitSystem

_TI_INITIALIZED = False


def _ti_init():
    global _TI_INITIALIZED
    if not _TI_INITIALIZED:
        ti.init(arch=ti.cpu, log_level=ti.ERROR)
        _TI_INITIALIZED = True


# ======================================================================
# Test-only conditions
# ======================================================================


class _AlwaysTriggers(StopCondition):
    name = "AlwaysTriggers"
    requires = ()

    def __call__(self, ctx):
        return True


class _NeverTriggers(StopCondition):
    name = "NeverTriggers"
    requires = ()

    def __call__(self, ctx):
        return False


class _RaisingCondition(StopCondition):
    name = "RaisingCondition"
    requires = ()

    def __call__(self, ctx):
        raise RuntimeError("condition should not be called after should_stop")


class _SeedRho(BaseProcessor):
    """Fill EMCDensityField.rho with a constant at step 0. Test fixture."""

    name = "_SeedRho"
    stage = Stage.PRE_UPDATE
    order = 5
    requires = (EMCDensityField,)

    def __init__(self, value):
        self.value = float(value)

    def process(self, ctx):
        if ctx.sim.step > 0:
            return
        ctx.data.require(EMCDensityField).rho.fill(self.value)


def _run(pipeline, initial, dt=0.1, max_steps=1, check_stateless=False):
    return Runner({"session": InMemorySink()}, check_stateless=check_stateless).run(
        pipeline,
        name="diagnostics_test",
        params={},
        dt=dt,
        max_steps=max_steps,
        initial_features=initial,
    )


# ======================================================================
# Shape and construction
# ======================================================================


def test_stop_condition_is_callable():
    """
    The base StopCondition raises NotImplementedError from __call__.

    Mutation caught: __call__ silently returning False on the base,
    which would let a broken subclass no-op instead of failing.
    """
    c = StopCondition()
    try:
        c(None)
    except NotImplementedError:
        return
    raise AssertionError("expected NotImplementedError from base StopCondition")


def test_empty_conditions_rejected():
    """
    DiagnosticProcessor([]) raises ValueError at construction.

    Mutation caught: an empty list accepted, which turns the processor
    into a silent no-op and hides a caller mistake.
    """
    try:
        DiagnosticProcessor(conditions=[])
    except ValueError:
        return
    raise AssertionError("expected ValueError for empty conditions")


def test_requires_aggregated_from_conditions():
    """
    DiagnosticProcessor.requires is the union of every condition's
    requires, deduplicated.

    Mutation caught: requires hard-coded to () so a condition's feature
    is not checked at build time; or the union kept as a list with
    duplicates, which would just be noisy but still work.

    Uses LocalizationBelowCondition (requires StabilityMetrics) and
    SphericityBelowCondition (also requires StabilityMetrics) to
    exercise the dedupe.
    """
    proc = DiagnosticProcessor(
        conditions=[
            LocalizationBelowCondition(0.5),
            SphericityBelowCondition(0.5),
        ]
    )
    assert proc.requires == (StabilityMetrics,), proc.requires


def test_requires_empty_for_lambda():
    """
    A lambda has no `requires`; DiagnosticProcessor over a lambda has
    requires == (), so a pipeline with only lambdas does not fail
    validation on missing features.

    Mutation caught: getattr(c, "requires", ()) replaced by
    c.requires, which would AttributeError on a lambda.
    """
    proc = DiagnosticProcessor(conditions=[lambda ctx: False])
    assert proc.requires == (), proc.requires


# ======================================================================
# Behaviour: forced violation, no violation, idempotence
# ======================================================================


def test_stop_condition_triggers_should_stop():
    """
    A condition that always returns True stops a 10-step pipeline at
    step 1.

    This is the plan's required test: "run with a forced violation ->
    simulation stops early". Mutation caught: `ctx.sim.should_stop =
    True` removed, so the run completes all 10 steps.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(DiagnosticProcessor(conditions=[_AlwaysTriggers()]))

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=10)
    assert ctx.sim.step == 1, ctx.sim.step
    assert ctx.sim.should_stop is True, ctx.sim.should_stop


def test_stop_condition_reports_error():
    """
    A triggered condition writes a message to ctx.diag.errors, naming
    the condition and the step.

    Mutation caught: ctx.diag.error(msg) removed, so the run stops
    silently and the caller has no record of why.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(DiagnosticProcessor(conditions=[_AlwaysTriggers()]))

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=5)
    assert any("AlwaysTriggers" in e for e in ctx.diag.errors), ctx.diag.errors
    assert any("step 0" in e for e in ctx.diag.errors), ctx.diag.errors


def test_no_trigger_leaves_run_alone():
    """
    A condition that never returns True lets the pipeline complete all
    steps, with no errors reported.

    Mutation caught: `should_stop` set unconditionally, or
    `ctx.diag.error` written regardless of the outcome.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(DiagnosticProcessor(conditions=[_NeverTriggers()]))

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=5)
    assert ctx.sim.step == 5, ctx.sim.step
    assert ctx.sim.should_stop is False, ctx.sim.should_stop
    assert ctx.diag.errors == [], ctx.diag.errors


def test_multiple_conditions_all_reported():
    """
    Two conditions that both trigger produce a single message naming
    both.

    Mutation caught: only the first triggered condition reported (a
    `break` inside the loop), which hides the second.
    """
    _ti_init()

    class _AlwaysTriggers2(StopCondition):
        name = "AlwaysTriggers2"
        requires = ()

        def __call__(self, ctx):
            return True

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(DiagnosticProcessor(conditions=[_AlwaysTriggers(), _AlwaysTriggers2()]))

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=1)
    assert any(
        ("AlwaysTriggers" in e) and ("AlwaysTriggers2" in e) for e in ctx.diag.errors
    ), ctx.diag.errors


def test_should_stop_guard_skips_re_evaluation():
    """
    When ctx.sim.should_stop is already True, DiagnosticProcessor.process
    returns without calling any condition.

    Mutation caught: the `if ctx.sim.should_stop: return` guard removed,
    so a condition that raises on second call (or has side effects)
    is called anyway.

    The pipeline is set up so the second step would raise if the guard
    is missing; we drive the run two steps by clearing should_stop
    between them via a custom runner is overkill, so instead we call
    process() directly with should_stop pre-set.
    """
    _ti_init()

    proc = DiagnosticProcessor(conditions=[_RaisingCondition()])

    # Build a minimal ctx with should_stop already True.
    from ..context import (
        Context,
        Diagnostics,
        FeatureBag,
        LogContext,
        Params,
        RunContext,
        SimContext,
    )
    from pathlib import Path

    ctx = Context(
        run=RunContext(name="guard_test", output_dir=Path("out")),
        params=Params({}),
        sim=SimContext(should_stop=True),
        data=FeatureBag(),
        log=LogContext(sinks={}),
        diag=Diagnostics(),
    )
    # Should return without calling _RaisingCondition (which raises).
    proc.process(ctx)
    assert ctx.diag.errors == [], ctx.diag.errors


# ======================================================================
# Built-in conditions in isolation
# ======================================================================


def test_max_rho_condition_triggers_above_threshold():
    """
    MaxRhoCondition(1.0) fires when the seeded rho exceeds 1.0.

    Mutation caught: `>` flipped to `<` or to a different comparison.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(AllocateWaveField(nx=8, ny=8, nz=8, dx=1.0))
            self.add(_SeedRho(1.5))
            self.add(DiagnosticProcessor(conditions=[MaxRhoCondition(1.0)]))

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=5)
    assert ctx.sim.step == 1, ctx.sim.step
    assert any("MaxRhoCondition" in e for e in ctx.diag.errors), ctx.diag.errors


def test_max_rho_condition_silent_below_threshold():
    """
    MaxRhoCondition(1.0) does not fire when rho stays below 1.0.

    Mutation caught: the same comparison flipped, which would fire
    below the threshold and stall every normal run.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(AllocateWaveField(nx=8, ny=8, nz=8, dx=1.0))
            self.add(_SeedRho(0.5))
            self.add(DiagnosticProcessor(conditions=[MaxRhoCondition(1.0)]))

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=5)
    assert ctx.sim.step == 5, ctx.sim.step
    assert ctx.diag.errors == [], ctx.diag.errors


def test_energy_drift_condition_uses_absolute_value():
    """
    EnergyDriftCondition fires on a negative dE_dt outside the band,
    not just a positive one.

    EnergyBudget comes from initial_features; Runner.run expands it
    through MRO before Pipeline.build, so no external_provides entry
    is needed.

    Mutation caught: abs() dropped, so a strongly negative drift passes
    silently while a strongly positive one is caught.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(DiagnosticProcessor(conditions=[EnergyDriftCondition(1.0)]))

    ctx = _run(
        P(),
        [NaturalUnitSystem(), EnergyBudget(dE_dt=-1e6)],
        max_steps=5,
    )
    assert ctx.sim.step == 1, ctx.sim.step
    assert any("EnergyDriftCondition" in e for e in ctx.diag.errors), ctx.diag.errors


def test_localization_below_condition_triggers():
    """
    LocalizationBelowCondition(0.5) fires when localization < 0.5.

    StabilityMetrics comes from initial_features; Runner.run expands
    it through MRO before Pipeline.build, so no external_provides
    entry is needed.

    Mutation caught: comparison flipped, so a well-localized field
    triggers and a spreading one does not.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(DiagnosticProcessor(conditions=[LocalizationBelowCondition(0.5)]))

    ctx = _run(
        P(),
        [NaturalUnitSystem(), StabilityMetrics(localization=0.1)],
        max_steps=5,
    )
    assert ctx.sim.step == 1, ctx.sim.step
    assert any("LocalizationBelowCondition" in e for e in ctx.diag.errors), ctx.diag.errors


def test_sphericity_below_condition_triggers():
    """
    SphericityBelowCondition(0.5) fires when sphericity < 0.5.

    StabilityMetrics comes from initial_features; Runner.run expands
    it through MRO before Pipeline.build, so no external_provides
    entry is needed.

    Mutation caught: comparison flipped.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(DiagnosticProcessor(conditions=[SphericityBelowCondition(0.5)]))

    ctx = _run(
        P(),
        [NaturalUnitSystem(), StabilityMetrics(sphericity=0.1)],
        max_steps=5,
    )
    assert ctx.sim.step == 1, ctx.sim.step
    assert any("SphericityBelowCondition" in e for e in ctx.diag.errors), ctx.diag.errors


def test_localization_and_sphericity_read_their_own_field():
    """
    Each StabilityMetrics condition reads its own field. The tests above
    seed one metric and leave the other at its default 0.0, which is
    below every threshold, so a condition reading the other field still
    fires there. Here the other metric sits at a healthy 1.0, both ways.

    Mutation caught: LocalizationBelowCondition reading `sphericity`, or
    SphericityBelowCondition reading `localization`.
    """
    _ti_init()

    def stopped(cond, metrics):
        class P(Pipeline):
            def __init__(self):
                super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
                self.add(DiagnosticProcessor(conditions=[cond]))

        ctx = _run(P(), [NaturalUnitSystem(), metrics], max_steps=5)
        return ctx.sim.step == 1

    low_loc = StabilityMetrics(localization=0.1, sphericity=1.0)
    low_sph = StabilityMetrics(localization=1.0, sphericity=0.1)
    assert stopped(LocalizationBelowCondition(0.5), low_loc)
    assert not stopped(LocalizationBelowCondition(0.5), low_sph)
    assert stopped(SphericityBelowCondition(0.5), low_sph)
    assert not stopped(SphericityBelowCondition(0.5), low_loc)


class _SeedRhoSpike(BaseProcessor):
    """Fill EMCDensityField.rho with `value`, then one voxel with `spike`."""

    name = "_SeedRhoSpike"
    stage = Stage.PRE_UPDATE
    order = 5
    requires = (EMCDensityField,)

    def __init__(self, value, spike, at=(2, 5, 3)):
        self.value = float(value)
        self.spike = float(spike)
        self.at = tuple(at)

    def process(self, ctx):
        if ctx.sim.step > 0:
            return
        rho = ctx.data.require(EMCDensityField).rho
        rho.fill(self.value)
        rho[self.at] = self.spike


def test_max_rho_condition_reads_the_maximum():
    """
    MaxRhoCondition fires on a single voxel above rho_max in a field
    that is otherwise below it. A uniform fill cannot tell the maximum
    from the mean, the minimum or any one voxel.

    Mutation caught: `.max()` replaced by `.mean()` or `.min()`.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(AllocateWaveField(nx=8, ny=8, nz=8, dx=1.0))
            self.add(_SeedRhoSpike(0.5, 1.5))
            self.add(DiagnosticProcessor(conditions=[MaxRhoCondition(1.0)]))

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=5)
    assert ctx.sim.step == 1, ctx.sim.step
    assert any("MaxRhoCondition" in e for e in ctx.diag.errors), ctx.diag.errors


def test_energy_drift_condition_both_signs_and_band():
    """
    EnergyDriftCondition fires on a large positive dE_dt too, and stays
    silent inside the band on either side.

    Mutation caught: abs() replaced by a negation (only negative drift
    caught), or the comparison flipped.
    """
    _ti_init()

    def stopped(dE_dt):
        class P(Pipeline):
            def __init__(self):
                super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
                self.add(DiagnosticProcessor(conditions=[EnergyDriftCondition(1.0)]))

        ctx = _run(P(), [NaturalUnitSystem(), EnergyBudget(dE_dt=dE_dt)], max_steps=5)
        return ctx.sim.step == 1

    assert stopped(+1e6)
    assert not stopped(+0.5)
    assert not stopped(-0.5)


def test_requires_union_spans_distinct_features():
    """
    The requires union covers conditions with different requirements.
    test_requires_aggregated_from_conditions uses two conditions that
    both need StabilityMetrics, so it cannot see a union that reads only
    the first condition.

    Mutation caught: requires taken from the first condition only.
    """
    proc = DiagnosticProcessor(
        conditions=[
            EnergyDriftCondition(1.0),
            LocalizationBelowCondition(0.5),
            MaxRhoCondition(1.0),
        ]
    )
    assert set(proc.requires) == {EnergyBudget, StabilityMetrics, EMCDensityField}, proc.requires
    assert len(proc.requires) == 3, proc.requires


_ORDER_PROBE_CALLS = []


class _OrderProbe(BaseProcessor):
    """Record (order, step) for each process() call. Test fixture."""

    name = "_OrderProbe"
    stage = Stage.MEASURE

    def __init__(self, order):
        self.order = order

    def process(self, ctx):
        _ORDER_PROBE_CALLS.append((self.order, ctx.sim.step))


def test_processors_after_diagnostic_skip_the_stop_step():
    """
    On the step where a condition fires, a MEASURE processor below
    order 100 runs and one above it (the visualisers' 2000) does not.

    Mutation caught: DiagnosticProcessor.order moved above the
    visualisers, so they draw the step that is being stopped.
    """
    _ti_init()
    _ORDER_PROBE_CALLS.clear()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(_OrderProbe(50))
            self.add(DiagnosticProcessor(conditions=[_AlwaysTriggers()]))
            self.add(_OrderProbe(2000))

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=5)
    assert ctx.sim.step == 1, ctx.sim.step
    assert _ORDER_PROBE_CALLS == [(50, 0)], _ORDER_PROBE_CALLS


# ======================================================================
# Build-time validation
# ======================================================================


def test_missing_stability_metrics_fails_at_build():
    """
    A DiagnosticProcessor whose only condition needs StabilityMetrics
    is rejected at Pipeline.build() when the pipeline does not provide
    StabilityMetrics.

    Mutation caught: the requires aggregation in __init__ removed, so
    the processor has requires == () and the pipeline builds, only
    to fail at first call with KeyError.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(DiagnosticProcessor(conditions=[LocalizationBelowCondition(0.5)]))

    try:
        _run(P(), [NaturalUnitSystem()], max_steps=1)
    except PipelineError as e:
        assert "StabilityMetrics" in str(e), str(e)
        return
    raise AssertionError("expected PipelineError naming StabilityMetrics")


def test_stateless_guard_passes():
    """
    DiagnosticProcessor passes the engine's stateless guard: its
    instance fields (conditions, requires) are set once and never
    mutated by process().

    Mutation caught: a counter on self incremented in process(), which
    the guard would catch and raise PipelineError on.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
            self.add(DiagnosticProcessor(conditions=[_NeverTriggers()]))

    ctx = _run(P(), [NaturalUnitSystem()], max_steps=3, check_stateless=True)
    assert ctx.diag.errors == [], ctx.diag.errors


# ======================================================================
# Runner
# ======================================================================


def main() -> int:
    tests = [
        test_stop_condition_is_callable,
        test_empty_conditions_rejected,
        test_requires_aggregated_from_conditions,
        test_requires_empty_for_lambda,
        test_stop_condition_triggers_should_stop,
        test_stop_condition_reports_error,
        test_no_trigger_leaves_run_alone,
        test_multiple_conditions_all_reported,
        test_should_stop_guard_skips_re_evaluation,
        test_max_rho_condition_triggers_above_threshold,
        test_max_rho_condition_silent_below_threshold,
        test_energy_drift_condition_uses_absolute_value,
        test_localization_below_condition_triggers,
        test_sphericity_below_condition_triggers,
        test_localization_and_sphericity_read_their_own_field,
        test_max_rho_condition_reads_the_maximum,
        test_energy_drift_condition_both_signs_and_band,
        test_requires_union_spans_distinct_features,
        test_processors_after_diagnostic_skip_the_stop_step,
        test_missing_stability_metrics_fails_at_build,
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
