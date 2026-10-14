"""Physics processors. Domain layer on top of the pipeline engine."""

from .wc_types import WC, WCState
from .wc_factory import build_wc_state
from .features import (
    BoundaryCondition,
    EMCDensityField,
    EMCFluxField,
    EnergyBudget,
    PsiBaseField,
    PsiLongField,
    PsiTransField,
    PsiTripleBuffer,
    RunSeed,
    StabilityMetrics,
    TrackerFields,
    WaveGrid,
    WaveSpeedField,
    WaveStats,
)
from .units import (
    NaturalUnitSystem,
    OpenWaveUnitSystem,
    SIUnitSystem,
    UnitSystem,
    make_unit_system,
)
from .allocator import AllocateTrackers, AllocateWaveSpeed, AllocateWaveField
from .emc import UpdateEMCDensityProcessor, UpdateWaveSpeedProcessor
from .seed import SeedPulse, SeedMultiCenter
from .evolution import (
    ClearAccelerationProcessor,
    LaplacianProcessor,
    LaplacianVariableCoeffProcessor,
    LeapfrogProcessor,
)
from .motion import (
    GradRhoRule,
    NoOpRule,
    WCDriftRule,
    WCMotionProcessor,
)
from .nonlinearity import NonlinearCubic
from .boundary import BoundaryProcessor, DirichletBoundaryProcessor
from .measure import AmplitudeTracker
from .visualize import TaichiWindowProcessor, WindowedProcessor
from .seed import SeedBaseWave
from .energy import EnergyBudgetUpdate
from .stability import StabilityMetricsUpdate

__all__ = [
    # wave centers
    "WC",
    "WCState",
    "build_wc_state",
    # fields
    "PsiTripleBuffer",
    "PsiBaseField",
    "PsiLongField",
    "PsiTransField",
    "EMCDensityField",
    "EMCFluxField",
    "TrackerFields",
    "WaveSpeedField",
    "WaveGrid",
    "WaveStats",
    # units
    "UnitSystem",
    "NaturalUnitSystem",
    "OpenWaveUnitSystem",
    "SIUnitSystem",
    "make_unit_system",
    # processors
    "AllocateWaveField",
    "AllocateTrackers",
    "AllocateWaveSpeed",
    "SeedPulse",
    "SeedMultiCenter",
    "ClearAccelerationProcessor",
    "LaplacianProcessor",
    "LaplacianVariableCoeffProcessor",
    "LeapfrogProcessor",
    "NonlinearCubic",
    "DirichletBoundaryProcessor",
    "AmplitudeTracker",
    "TaichiWindowProcessor",
    "WindowedProcessor",
    "UpdateEMCDensityProcessor",
    "UpdateWaveSpeedProcessor",
    "SeedBaseWave",
    "BoundaryCondition",
    "BoundaryProcessor",
    "GradRhoRule",
    "NoOpRule",
    "WCDriftRule",
    "WCMotionProcessor",
    "EnergyBudget",
    "EnergyBudgetUpdate",
    "StabilityMetrics",
    "StabilityMetricsUpdate",
    "RunSeed",
]
