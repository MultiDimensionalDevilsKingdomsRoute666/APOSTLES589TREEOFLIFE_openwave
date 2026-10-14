"""
Shared pipeline builders for demos and tests.

This is a precursor to plan item 1.22, not a realisation of it. Item
1.22's `make_pipeline_a` / `make_pipeline_b` require the VacuumProvider
(item 1.17, not built) and the scattering operator (variant B2d, plan
Section 7). What is here is the simpler shape every linear-wave demo
repeats: eight processors in the canonical order, with two hooks for
extra terms and extra measurement.

Once item 1.17 lands, 1.22 can build on these builders rather than on
the raw Pipeline class.
"""

from ..pipeline import ErrorPolicy, Pipeline
from .allocator import AllocateWaveField
from .boundary import BoundaryProcessor
from .evolution import (
    ClearAccelerationProcessor,
    LaplacianProcessor,
    LeapfrogProcessor,
)
from .features import BoundaryCondition, PsiLongField
from .motion import NoOpRule, WCMotionProcessor
from .seed import SeedMultiCenter
from .stability import StabilityMetricsUpdate
from .units import UnitSystem
from .wc_types import WCState


def make_linear_wave_pipeline(
    *,
    grid: int,
    seed_radius: float = 4.0,
    metric_threshold: float = 0.5,
    nonlinear_terms: tuple = (),
    extra_measure: tuple = (),
) -> Pipeline:
    """
    Build the standard linear-wave pipeline on a cube grid.

    Processor chain, in order of appearance (Pipeline.build() then
    sorts by each processor's order attribute):

        AllocateWaveField(grid, grid, grid, dx=1.0)
        SeedMultiCenter(radius=seed_radius)
        ClearAccelerationProcessor
        LaplacianProcessor
        ...nonlinear_terms
        LeapfrogProcessor
        BoundaryProcessor(PsiLongField)
        WCMotionProcessor(NoOpRule)
        StabilityMetricsUpdate(threshold=metric_threshold)
        ...extra_measure

    The caller must provide, through initial_features:

        UnitSystem         e.g. NaturalUnitSystem()
        BoundaryCondition  its kind must match BoundaryProcessor's
                           default, "dirichlet"
        WCState            consumed by SeedMultiCenter

    These are declared in external_provides, which the pipeline treats
    as a promise, not a check: build-time validation passes, and a
    caller that omits one of the three gets a KeyError at the first
    require() inside that processor's process(). Not at build time.

    The chain does not include a nonlinear term. nonlinear_terms
    accepts processors such as NonlinearCubic (order 15); they land
    between the Laplacian and the Leapfrog in the effective order.
    extra_measure is for visualizers, loggers, and diagnostic hooks
    that read the field after StabilityMetricsUpdate has run.

    error_policy is FAIL_FAST: a pipeline with the wrong features is a
    configuration error, not a run-time event to tolerate.
    """
    p = Pipeline(
        error_policy=ErrorPolicy.FAIL_FAST,
        external_provides=(UnitSystem, BoundaryCondition, WCState),
    )
    p.add(AllocateWaveField(nx=grid, ny=grid, nz=grid, dx=1.0))
    p.add(SeedMultiCenter(radius=seed_radius))
    p.add(ClearAccelerationProcessor())
    p.add(LaplacianProcessor())
    for proc in nonlinear_terms:
        p.add(proc)
    p.add(LeapfrogProcessor())
    p.add(BoundaryProcessor(field_type=PsiLongField))
    p.add(WCMotionProcessor(rule=NoOpRule()))
    p.add(StabilityMetricsUpdate(localization_threshold=metric_threshold))
    for proc in extra_measure:
        p.add(proc)
    return p
