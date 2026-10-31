"""
Vacuum layer: swappable provider for the base wave (plan item 1.17).

Design in one paragraph. `VacuumProvider` is a FEATURE (an abstract class
with behaviour, not a processor): it holds one variant's configuration and
its `seed`/`step`/`energy_budget` methods, and is passed by the caller in
`initial_features`, the same way `UnitSystem` and `BoundaryCondition` are.
`VacuumStepProcessor` is the single PROCESSOR that drives the lifecycle:
`seed` once at step 0, `step` every step. This is the same feature/processor
split the boundary layer already uses (`BoundaryCondition` vs
`BoundaryProcessor`), chosen so that the pipeline does not need to know
which variant it hosts.

Two variants ship:

    StaticVacuum     V1 - base wave set once, does not evolve.
    PeriodicVacuum   V3 - base wave evolves under the wave equation on a
                     periodic box. This is the shape K-selectivity needs.

Deferred, not implemented here:

    V2 passive/leaky        - no injection, energy lost at boundary.
    V4 absorbing+reinject   - requires a real absorbing boundary, which
                              plan item 1.7 deliberately does not ship
                              (`BoundaryCondition` rejects "absorbing");
                              V4 becomes buildable once an absorber lands.
    V5 self-consistent      - hardest, deferred to research.

`energy_budget()` returns what the provider contributed (positive) or
removed (negative) since the run started. Both V1 and V3 are conservative,
so both return 0.0. A stateful variant (V2/V4) must carry its ledger in a
feature (the Z2 rule in `pipeline_engine/README.md`); it must not mutate
`self` inside `step()`, because the statelessness guard cannot see
features that a processor touches indirectly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..pipeline import BaseProcessor, Stage

from .boundary import _boundary_periodic
from .evolution import _clear_accel, _laplacian, _leapfrog
from .features import PsiBaseField, WaveGrid
from .units import UnitSystem

# ======================================================================
# Feature: VacuumProvider and its variants
# ======================================================================


class VacuumProvider(ABC):
    """
    Feature: one vacuum variant's configuration and behaviour.

    Not a processor. The caller registers an instance through
    `initial_features`, and the engine's `FeatureBag` keys it under both
    the concrete type and `VacuumProvider` by MRO, so a downstream
    processor that declares `requires=(VacuumProvider,)` receives
    whichever variant the caller provided.

    Subclasses must implement `step(ctx)`. They may override `seed(ctx)`
    (default no-op) and `energy_budget()` (default 0.0).

    Capability flags:
        evolves             - base wave evolves in time.
        supports_reflection - base wave can supply incoming waves to
                              wave centres. A scattering operator that
                              needs this declares `requires=(VacuumProvider,)`
                              and checks the flag in its `setup()`,
                              raising `PipelineError` on a mismatch.
    """

    name: str = "VacuumProvider"
    evolves: bool = False
    supports_reflection: bool = False

    def seed(self, ctx) -> None:
        """
        Called once by `VacuumStepProcessor` at step 0. Default no-op.

        Subclasses that need to fill `PsiBaseField` at t=0 override this.
        V1 and V3 do not: the base field's initial contents are the
        caller's responsibility (via `SeedBaseWave` or a fixture).
        """
        pass

    @abstractmethod
    def step(self, ctx) -> None:
        """
        Called by `VacuumStepProcessor` every step, including step 0.

        Base class raises NotImplementedError; every concrete variant
        must decide what "evolve the vacuum" means (V1: nothing;
        V3: Laplacian + Leapfrog + periodic boundary on `PsiBaseField`).
        """
        raise NotImplementedError(f"{type(self).__name__} must implement step(ctx)")

    def energy_budget(self) -> float:
        """
        Net energy the provider has contributed (positive) or removed
        (negative) since the run started. Default 0.0.

        Conservative variants (V1, V3) return 0.0 by construction. A
        stateful variant (V2/V4) must carry its ledger in a feature; it
        must not add instance state here, per Z2.
        """
        return 0.0


class StaticVacuum(VacuumProvider):
    """
    V1 - static vacuum (plan Section 5.4).

    The base wave is set once and does not evolve. The soliton evolves on
    top of a fixed background. No energy exchange; the base field stays at
    whatever the caller (or `SeedBaseWave`) wrote.

    Capabilities: `evolves=False`, `supports_reflection=False`. A
    scattering operator that needs incoming waves must not run with V1.
    """

    name = "StaticVacuum"
    evolves = False
    supports_reflection = False

    def step(self, ctx) -> None:
        # No evolution: the base field is left untouched.
        pass


class PeriodicVacuum(VacuumProvider):
    """
    V3 - periodic box (plan Section 5.4).

    The base wave evolves under the constant-coefficient wave equation on a
    periodic domain: `ClearAcceleration -> Laplacian -> Leapfrog`, then
    the periodic boundary is applied to `PsiBaseField.psi` and
    `PsiBaseField.psi_prev`. Energy is conserved by the leapfrog up to
    the standard O(dt^2) drift plus the wrap-around artefacts when the
    wave meets its own copy.

    Uses the same kernels the production pipeline uses for the
    longitudinal field (`evolution._clear_accel`, `evolution._laplacian`,
    `evolution._leapfrog`, `boundary._boundary_periodic`), so a mutation
    that swaps or drops one of them surfaces in the manual-composition
    test as a mismatch.

    Capabilities: `evolves=True`, `supports_reflection=True`. A
    scattering operator that needs incoming waves can run with V3.
    """

    name = "PeriodicVacuum"
    evolves = True
    supports_reflection = True

    def step(self, ctx) -> None:
        grid = ctx.data.require(WaveGrid)
        units = ctx.data.require(UnitSystem)
        field = ctx.data.require(PsiBaseField)

        _clear_accel(field.psi_new, grid.nx, grid.ny, grid.nz)
        _laplacian(
            field.psi,
            field.psi_new,
            grid.nx,
            grid.ny,
            grid.nz,
            grid.dx,
            float(units.c),
        )
        dt2 = ctx.sim.dt * ctx.sim.dt
        _leapfrog(
            field.psi,
            field.psi_prev,
            field.psi_new,
            grid.nx,
            grid.ny,
            grid.nz,
            dt2,
        )
        _boundary_periodic(
            field.psi,
            field.psi_prev,
            grid.nx,
            grid.ny,
            grid.nz,
        )


# ======================================================================
# Processor: VacuumStepProcessor
# ======================================================================


class VacuumStepProcessor(BaseProcessor):
    """
    Drive the vacuum lifecycle: `seed` once at step 0, `step` every step.

    Stage.UPDATE, order=5. Sits between `ClearAccelerationProcessor`
    (order=0) and `LaplacianProcessor` (order=10) in the soliton chain,
    so the per-step read is "clear -> vacuum evolves -> soliton wave
    equation -> leapfrog". Base and soliton fields are independent in
    the current build, so the ordering does not affect correctness; it
    is a readability choice that anticipates the coupled pipeline
    (plan Q10, Strang splitting).

    Requires `VacuumProvider` (from `initial_features`), and
    `WaveGrid`, `UnitSystem`, `PsiBaseField` (from `AllocateWaveField`
    and `initial_features`). The `requires` tuple is the union of what
    the shipped variants need; V1 does not read `UnitSystem` or
    `PsiBaseField` at step time, but declares them so V3 fits the same
    processor. A future variant that needs fewer features would still
    pay this declaration cost; the alternative (per-variant processors)
    was rejected because it puts the variant name in the pipeline code.

    Note on `external_provides`: under `Runner.run()`, a provider
    instance in `initial_features` satisfies `requires` at build time
    by MRO, with or without a declaration. Without an instance,
    `VacuumProvider` must be declared in the pipeline's
    `external_provides` (or provided by an earlier processor), otherwise
    `Pipeline.build()` raises `PipelineError`. If the pipeline declares
    it but the caller omits the instance, `process()` raises `KeyError`
    at step 0. This is the same "declaration, not check" behaviour the
    preset tests document.
    """

    name = "VacuumStepProcessor"
    stage = Stage.UPDATE
    order = 5
    requires = (VacuumProvider, WaveGrid, UnitSystem, PsiBaseField)
    provides = ()

    def process(self, ctx) -> None:
        vp = ctx.data.require(VacuumProvider)
        if ctx.sim.step == 0:
            vp.seed(ctx)
        vp.step(ctx)
