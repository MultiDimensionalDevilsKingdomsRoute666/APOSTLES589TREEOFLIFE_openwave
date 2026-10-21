"""
Stop conditions and the diagnostic processor (plan item 1.18).

`StopCondition` is a callable protocol: `condition(ctx) -> bool`. When
any condition returns True inside `DiagnosticProcessor.process`, the
processor sets `ctx.sim.should_stop = True` and writes a diagnostic
message to `ctx.diag.errors`. `Pipeline.step()` checks
`ctx.sim.should_stop` after each MEASURE processor, so the run ends at
the end of that step; MEASURE processors with a higher order (the
`_demo.py` logger at 500, visualisation at 2000) do not run on the step
where a condition triggers. A `LogProcessor` below order 100 (its
default is 0; the smoke test uses 50 and 60) is not skipped on that
step: it writes it if its `every` interval falls on it.

A sweep driver (`ExperimentRunner`) records the diagnostic in the
run's summary and continues with the next config.

Four built-in conditions, matching plan 1.18:

    MaxRhoCondition            max(EMCDensityField.rho) > rho_max
    EnergyDriftCondition       |EnergyBudget.dE_dt| > threshold
    LocalizationBelowCondition StabilityMetrics.localization < threshold
    SphericityBelowCondition   StabilityMetrics.sphericity < threshold

Each condition declares its own `requires`, and `DiagnosticProcessor`
unions them, so `Pipeline.build()` rejects a pipeline that hosts a
condition whose features are absent. A caller-supplied lambda has no
`requires`; a lambda that reads a feature directly is expected to know
what it reads.

The processor is stateless. `self.conditions` and `self.requires` are
set in `__init__` and never mutated; `process()` writes only to
`ctx.diag` and to `ctx.sim.should_stop`.
"""

import numpy as np

from ..pipeline import BaseProcessor, Stage

from .features import (
    EMCDensityField,
    EnergyBudget,
    StabilityMetrics,
)


class StopCondition:
    """
    Callable protocol for a stop condition.

    Subclasses override `__call__` and may declare `requires` (a tuple
    of feature classes the condition reads). The default `requires` is
    empty, so a lambda wrapped in a minimal subclass is legal.

    `name` is reported in the diagnostic message when the condition
    triggers. Each built-in sets its own; a subclass that does not set
    one inherits "StopCondition". A plain callable without a `name`
    attribute is reported by its type name (a lambda reports as
    `function`).
    """

    name: str = "StopCondition"
    requires: tuple = ()

    def __call__(self, ctx) -> bool:
        raise NotImplementedError(f"{type(self).__name__} must implement __call__(ctx) -> bool")


class MaxRhoCondition(StopCondition):
    """
    CFL guard: stop when max(EMCDensityField.rho) exceeds `rho_max`.

    Under B4a and B4b the density is bounded by `rho_0` (plan Section
    2.3); a rho above `rho_max` means the assumed bound is violated and
    the run is unstable. For B4c, `rho_max` is the EMC Wall height
    (plan Section 3.2). Default `rho_max = 1.0` is the statutory
    background in normalised units, which is the B4a/B4b bound.

    Reads the whole grid through `to_numpy()`, so cost is O(N^3) per
    step. Fine for the sweep sizes this plan targets (up to ~128^3);
    replace with a Taichi atomic-max kernel if a real run needs it.
    """

    name = "MaxRhoCondition"
    requires = (EMCDensityField,)

    def __init__(self, rho_max: float = 1.0):
        if rho_max <= 0.0:
            raise ValueError(f"MaxRhoCondition: rho_max must be > 0, got {rho_max}")
        self.rho_max = float(rho_max)

    def __call__(self, ctx) -> bool:
        rho = ctx.data.require(EMCDensityField).rho
        return float(rho.to_numpy().max()) > self.rho_max


class EnergyDriftCondition(StopCondition):
    """
    Stop when |EnergyBudget.dE_dt| exceeds `threshold`.

    `dE_dt` is set by `EnergyBudgetUpdate` in the same MEASURE stage
    (order 5), before `DiagnosticProcessor` (order 100) runs, so the
    value is current. A pipeline that hosts this condition without an
    `EnergyBudgetUpdate` or an `EnergyBudget` in `initial_features`
    fails at build time.
    """

    name = "EnergyDriftCondition"
    requires = (EnergyBudget,)

    def __init__(self, threshold: float):
        if threshold <= 0.0:
            raise ValueError(f"EnergyDriftCondition: threshold must be > 0, got {threshold}")
        self.threshold = float(threshold)

    def __call__(self, ctx) -> bool:
        budget = ctx.data.require(EnergyBudget)
        return abs(budget.dE_dt) > self.threshold


class LocalizationBelowCondition(StopCondition):
    """
    Stop when StabilityMetrics.localization drops below `threshold`.

    Reads `StabilityMetrics`, which `StabilityMetricsUpdate` writes in
    the same MEASURE stage (order 20), before `DiagnosticProcessor`
    (order 100).
    """

    name = "LocalizationBelowCondition"
    requires = (StabilityMetrics,)

    def __init__(self, threshold: float):
        if threshold < 0.0:
            raise ValueError(
                f"LocalizationBelowCondition: threshold must be >= 0, got {threshold}"
            )
        self.threshold = float(threshold)

    def __call__(self, ctx) -> bool:
        m = ctx.data.require(StabilityMetrics)
        return m.localization < self.threshold


class SphericityBelowCondition(StopCondition):
    """
    Stop when StabilityMetrics.sphericity drops below `threshold`.

    Reads `StabilityMetrics`, which `StabilityMetricsUpdate` writes in
    the same MEASURE stage (order 20), before `DiagnosticProcessor`
    (order 100).
    """

    name = "SphericityBelowCondition"
    requires = (StabilityMetrics,)

    def __init__(self, threshold: float):
        if threshold < 0.0:
            raise ValueError(f"SphericityBelowCondition: threshold must be >= 0, got {threshold}")
        self.threshold = float(threshold)

    def __call__(self, ctx) -> bool:
        m = ctx.data.require(StabilityMetrics)
        return m.sphericity < self.threshold


class DiagnosticProcessor(BaseProcessor):
    """
    Evaluate stop conditions each step and set `ctx.sim.should_stop`
    when any of them returns True.

    Stage.MEASURE, order 100. Sits after the measurement processors
    (`EnergyBudgetUpdate` at 5, `AmplitudeTracker` at 10,
    `StabilityMetricsUpdate` at 20) and before visualisation (2000), so
    the conditions see the step's fresh values, and processors above it
    (the `_demo.py` logger at 500, the visualisers at 2000) do not run on
    a step that is about to be stopped. A `LogProcessor` below order 100
    (its default is 0) is not skipped on that step.

    Requires is the union of every condition's `requires`, computed in
    `__init__` from the conditions. A condition that reads a feature
    the pipeline does not provide fails at `Pipeline.build()`, not at
    first call.

    Stateless: `self.conditions` and `self.requires` are set once and
    never mutated; `process()` writes only to `ctx.diag` and
    `ctx.sim.should_stop`.

    At least one condition is required; a diagnostic processor with an
    empty list is a no-op that hides the mistake, so it raises at
    construction instead.
    """

    name = "DiagnosticProcessor"
    stage = Stage.MEASURE
    order = 100
    provides = ()

    def __init__(self, conditions):
        conditions = tuple(conditions)
        if not conditions:
            raise ValueError("DiagnosticProcessor: at least one condition is required")
        self.conditions = conditions
        req = set()
        for c in conditions:
            req.update(getattr(c, "requires", ()))
        self.requires = tuple(req)

    def process(self, ctx) -> None:
        if ctx.sim.should_stop:
            return
        triggered = []
        for c in self.conditions:
            if c(ctx):
                name = getattr(c, "name", type(c).__name__)
                triggered.append(name)
        if triggered:
            msg = (
                f"{self.name}: stop condition(s) triggered at step "
                f"{ctx.sim.step}: {', '.join(triggered)}"
            )
            ctx.diag.error(msg)
            ctx.sim.should_stop = True


__all__ = [
    "StopCondition",
    "MaxRhoCondition",
    "EnergyDriftCondition",
    "LocalizationBelowCondition",
    "SphericityBelowCondition",
    "DiagnosticProcessor",
]
