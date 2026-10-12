"""
Physics feature types. These are contracts between physics processors,
not part of the engine. The engine never imports this module.

models in the platform may use these features; per CROSS_MODEL_TESTING.md,
Section 2, a borrowed field is native and untwisted unless its docstring
says otherwise.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import taichi as ti

# =============================================================================
# Grid and statistics
# =============================================================================


@dataclass
class WaveGrid:
    """
    Grid geometry for a scalar/vector wave field.

    Holds grid dimensions and the voxel step only. The wave speed is
    not stored here: it comes from the UnitSystem feature, and a
    variable local speed from WaveSpeedField. Keeping c out of WaveGrid
    removes the ambiguity of two possible sources.
    """

    nx: int
    ny: int
    nz: int
    dx: float

    @property
    def max_size(self) -> int:
        return max(self.nx, self.ny, self.nz)

    @property
    def center(self) -> tuple[int, int, int]:
        return (self.nx // 2, self.ny // 2, self.nz // 2)


@dataclass
class WaveStats:
    """Mutable holder for measured quantities. Written by trackers."""

    amp_max: float = 0.0
    mass: float = 0.0


# =============================================================================
# Vector fields
# =============================================================================


@dataclass
class PsiTripleBuffer:
    """
    Three time levels of a vector field, for leapfrog integration.

    Base class. Subclasses name a specific mode (base wave, longitudinal,
    transverse). Processors should require the concrete subclass, not
    this base.

    Representation: a single ti.Vector.field(3, f32) per time level.
    Components are (x, y, z) in the engine's spatial axes. Not an
    internal triplet, not a complex scalar, not a director field.
    """

    psi: ti.Vector.field  # psi(t)
    psi_prev: ti.Vector.field  # psi(t - dt)
    psi_new: ti.Vector.field  # scratch / psi(t + dt)


@dataclass
class PsiBaseField(PsiTripleBuffer):
    """
    Background oscillation of the medium.

    In EWT this is the always-on base wave. It is not a particle
    disturbance; it is the ground state of the medium. Wave parameters
    (amplitude, wavelength, frequency) come from the UnitSystem feature
    and the experiment configuration.
    """

    pass


@dataclass
class PsiLongField(PsiTripleBuffer):
    """
    Longitudinal mode. Carries mass and charge in the EWT picture.

    This is the mode that responds to the EMC density gradient and
    participates in the push-out mechanism.
    """

    pass


@dataclass
class PsiTransField(PsiTripleBuffer):
    """
    Transverse mode. Carries spin and magnetism in the EWT picture.

    Coupled to the longitudinal mode at wave centres through the
    fine-structure constant. The conversion coefficient is loaded from
    GeometricConstants, not derived from the field.
    """

    pass


# =============================================================================
# Scalar fields
# =============================================================================


@dataclass
class EMCDensityField:
    """
    EMC packing density rho(r), single buffer.

    High away from matter (statutory background), low inside a soliton
    (push-out deficit). The gradient drives the pressure force on wave
    centres and modulates the local wave speed.

    Representation: scalar ti.field(f32), one value per voxel. Not a
    vector, not a tensor.
    """

    rho: ti.field


@dataclass
class EMCFluxField:
    """
    EMC flux through a surface, single buffer.

    Optional. Used by boundary processors and energy-budget trackers to
    account for EMC leaving or entering the simulated domain.

    Representation: scalar ti.field(f32), one value per voxel.
    """

    flux: ti.field


# =============================================================================
# Tracker fields
# =============================================================================


@dataclass
class TrackerFields:
    """
    Per-voxel tracker fields plus scalar global averages.

    Allocated by AllocateTrackers (order 20, after AllocateWaveField).
    Which fields get written, and how, is a physics decision (see the
    real TrackersUpdate in the physics layer). This class only fixes
    the shape.

    Per-voxel (shape = (nx, ny, nz), f32):
        amp_local           RMS amplitude envelope
        freq_local          zero-crossing frequency
        energy_long_local   longitudinal mode energy
        energy_trans_local  transverse mode energy
        rho_local           EMC density mirror; shares the buffer with
                            EMCDensityField.rho (same ti.field object,
                            see AllocateTrackers). Read-only for
                            Stage.MEASURE processors: a write here
                            rewrites the density the physics reads. The
                            test fixture may write it; a real
                            TrackersUpdate must not.
        last_crossing       timestamp of last positive-going zero crossing
                            (internal state for freq_local)

    Scalars (shape = (), f32):
        amp_global          RMS of amp_local over the three centre
                            planes, sqrt(<amp_local^2>)
        freq_global         three-plane average of freq_local
        energy_global       three-plane average of energy_long_local
    """

    amp_local: ti.field
    freq_local: ti.field
    energy_long_local: ti.field
    energy_trans_local: ti.field
    rho_local: ti.field
    last_crossing: ti.field
    amp_global: ti.field
    freq_global: ti.field
    energy_global: ti.field


@dataclass
class WaveSpeedField:
    """
    Per-voxel local wave speed squared c^2(rho).

    Written by the physics layer: UpdateWaveSpeedProcessor reads
    EMCDensityField.rho (normalised, 1.0 = statutory background) and
    writes c2_local = c0^2 * rho_norm. The absolute density rho_0 is
    not stored (it is ~3.3e52, beyond f32 range); the normalised form
    is used throughout the EMC chain.

    Read by LaplacianVariableCoeffProcessor, which uses the flux form
    div(c^2 grad psi) instead of the constant-coefficient Laplacian.
    The plan's item 1.23 requires this: a variable c^2 makes the naive
    c^2_i * laplacian(psi) form a different wave equation, not the one
    the plan specifies.

    Representation: scalar ti.field(f32), one value per voxel, in the
    unit system's squared speed units.
    """

    c2_local: ti.field


@dataclass
class BoundaryCondition:
    """
    Outer boundary kind and domain radius.

    kind: one of "dirichlet", "periodic", "reflecting". "absorbing"
        is reserved for a real absorber (plan item 1.7) and is
        rejected until one lands.
    r_domain: the domain radius the boundary applies at. Currently
        unused (the grid edges are the boundary); kept so a future
        non-rectangular domain can register it.

    Plan Section 6, item 1.7. The processor that consumes this feature
    is physics/boundary.py::BoundaryProcessor.
    """

    kind: str
    r_domain: float = 1.0

    def __post_init__(self):
        if self.kind not in ("dirichlet", "periodic", "reflecting"):
            raise ValueError(
                f"BoundaryCondition: kind must be 'dirichlet', "
                f"'periodic' or 'reflecting', got {self.kind!r}"
            )
        if self.r_domain <= 0.0:
            raise ValueError(f"BoundaryCondition: r_domain must be > 0, got {self.r_domain}")


@dataclass
class EnergyBudget:
    """
    Energy budget feature (plan Section 6, item 1.8).

    E_kin, E_grad, E_deform: the three components of the total.
    E_total = E_kin + E_grad + E_deform.

    E_prev and dE_dt are set by EnergyBudgetUpdate: dE_dt is
    (E_total - E_prev) / dt, taken before E_prev moves on, so after
    an update E_prev equals the current E_total, ready for the next
    step. On the first step dE_dt is 0.0, since there is no previous
    step.

    flux_boundary is reserved. No boundary in the current build
    transports energy out (dirichlet is a fixed-end wall, periodic
    and reflecting conserve), so it stays 0.0. It becomes meaningful
    once a real absorber lands (plan 1.7, deferred).

    All energies are in simulation units. Conversion to SI goes
    through UnitSystem.to_physical_energy, which is not called here.
    """

    E_kin: float = 0.0
    E_grad: float = 0.0
    E_deform: float = 0.0
    flux_boundary: float = 0.0
    E_prev: float = 0.0
    dE_dt: float = 0.0

    @property
    def E_soliton(self) -> float:
        return self.E_kin + self.E_grad

    @property
    def E_total(self) -> float:
        return self.E_kin + self.E_grad + self.E_deform

@dataclass
class StabilityMetrics:
    """
    Stability metrics feature (plan Section 6, item 1.9).

    Populated by StabilityMetricsUpdate. Read by loggers and diagnostics.
    Lengths are in grid units; the caller multiplies by WaveGrid.dx (or
    UnitSystem.to_physical_length) for physical units.

    Primary fields:
        localization  -- dimensionless concentration. 1.0 at the first
                         measurement, decreases if the field spreads,
                         increases if it collapses. Defined as
                         IPR / IPR_initial; the reference is captured
                         once, on the first non-empty step.
        sphericity    -- lambda_min / lambda_max of the mass-weighted
                         gyration tensor, relative to the grid center.
                         1.0 for a spherical field, 0.0 for a degenerate
                         (line or plane) field.
        wc_drift      -- mean Euclidean displacement of active wave
                         centers from their initial positions, grid
                         units. Zero when no WCState is in the pipeline.
        freq_drift    -- (freq_now - freq_ref) / freq_ref. Zero until the
                         first full field period is observed. See the
                         "Frequency signal" section below.
        sol_lifetime  -- consecutive steps with localization above a
                         processor-configured threshold. Resets to 0
                         when localization drops below it.

    Diagnostic fields:
        ipr, ipr_initial, r_rms, mass, n_active_wc -- as in earlier
                         revisions of this class.
        freq_ref      -- reference frequency, captured on the second
                         upward crossing of s(t) (the first completed
                         period). Zero if never captured.
        freq_now      -- most recent frequency measurement. Zero until
                         a period has been completed.

    Frequency signal (definition C, resolved 2026-10-12):
        The plan (item 1.9, Section 9 Q5) names freq_drift as a candidate
        metric without defining it. The implemented
        definition is a field-wide signal:

            s(t) = integral psi . (psi - psi_prev) dV

        s(t) is a signed scalar. For a field oscillating around zero at
        angular frequency omega, s(t) is proportional to sin(2*omega*t)
        plus a small DC offset (the offset scales as omega*dt and is
        negligible for omega*dt << 1). The processor detects upward
        zero-crossings of s(t) and derives the field frequency from
        the interval between consecutive crossings:

            delta_t  = time between consecutive upward crossings
            T_field  = 2 * delta_t           (s(t) has half the period)
            f_field  = 1 / T_field

        The TrackerFields signals, freq_local read at a single voxel
        and its three-plane average freq_global, are not well-defined
        for a symmetric seed released from rest. The
        author (2026-10-12) selected definition C as the primary one;
        the plan is amended accordingly.

    Known limitations (recorded so they are not read as results):
        1. Reflection contamination. In dirichlet or reflecting
           boundary modes, the outgoing wave reflects off the domain
           edge and returns to the center. From the moment of first
           return onward, s(t) is a superposition of the outgoing and
           reflected components, and the measured frequency is not the
           soliton's intrinsic frequency alone. The signal is
           meaningful only in the pre-reflection window. A variant that
           windows the signal or runs absorbing would remove this; the
           current build does not.
        2. Pipeline B (reflective vacuum). In the reflective pipeline
           (plan Section 5.4), PsiLongField carries both the soliton
           and its interaction with the base wave through the
           scattering operator. The measured frequency is the
           superposed signal, not the soliton alone.
        3. Longitudinal-only. s(t) reads the field named by
           field_type, default PsiLongField. A transverse (spin) signal
           would need a second measurement and is not implemented.
           freq_ref and freq_now are longitudinal-only.

    Other limitation:
        r_rms and the gyration tensor use the grid center as reference,
        not the field's center of mass. A center-of-mass variant needs
        a second kernel pass and is deferred. No test in the current
        suite exercises an off-center field.

    Internal zero-crossing state (updated each step, exposed for
    diagnostics and tests):
        s_prev           -- previous step's s(t), for crossing detection.
        t_last_crossing  -- simulation time of the last upward crossing.
                            -1.0 if no crossing has been recorded yet.
    """

    # Primary
    localization: float = 0.0
    sphericity: float = 0.0
    wc_drift: float = 0.0
    freq_drift: float = 0.0
    sol_lifetime: int = 0

    # Diagnostics
    ipr: float = 0.0
    ipr_initial: float = 0.0
    r_rms: float = 0.0
    mass: float = 0.0
    n_active_wc: int = 0
    freq_ref: float = 0.0
    freq_now: float = 0.0

    # Reference state, captured once
    wc_initial_positions: list = field(default_factory=list)

    # Internal zero-crossing state
    s_prev: float = 0.0
    t_last_crossing: float = -1.0