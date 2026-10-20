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
from .vacuum import VacuumProvider, VacuumStepProcessor

def make_linear_wave_pipeline(
    *,
    grid: int,
    seed_radius: float = 4.0,
    metric_threshold: float = 0.5,
    nonlinear_terms: tuple = (),
    extra_measure: tuple = (),
    vacuum: VacuumProvider | None = None,
) -> Pipeline:
    """
    ... (reszta docstringu bez zmian do momentu opisu vacuum) ...

    vacuum=None (the default) keeps the chain identical to the
    pre-vacuum preset; every existing demo and test is unaffected.

    vacuum=<instance> signals that the caller intends to run a vacuum
    variant. The preset adds VacuumProvider to external_provides and
    VacuumStepProcessor to the UPDATE stage. The instance itself is NOT
    injected into initial_features by this function; the caller must
    still pass it, e.g.:

        vacuum = PeriodicVacuum()
        pipeline = make_linear_wave_pipeline(..., vacuum=vacuum)
        Runner(...).run(..., initial_features=[..., vacuum])

    Passing vacuum= does not check the instance's capability flags.
    A processor that needs supports_reflection=True is expected to
    check them in its own setup() (see VacuumStepProcessor docstring).
    """
    external = (UnitSystem, BoundaryCondition, WCState)
    if vacuum is not None:
        external = external + (VacuumProvider,)

    p = Pipeline(
        error_policy=ErrorPolicy.FAIL_FAST,
        external_provides=external,
    )
    p.add(AllocateWaveField(nx=grid, ny=grid, nz=grid, dx=1.0))
    p.add(SeedMultiCenter(radius=seed_radius))
    p.add(ClearAccelerationProcessor())
    if vacuum is not None:
        p.add(VacuumStepProcessor())
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