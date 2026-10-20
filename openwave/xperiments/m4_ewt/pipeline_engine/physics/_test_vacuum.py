"""
Tests for VacuumProvider and its V1/V3 variants (plan item 1.17).

Design under test. `VacuumProvider` is a feature (abstract class with
behaviour), passed via `initial_features`. `VacuumStepProcessor` is the
single processor that drives `seed` (once) and `step` (every step).

Every test names the mutation it catches, or states explicitly that it is
a happy-path smoke check. The not-happy-path arms are:
  - `test_vacuum_step_processor_requires_all_four_features` (build-time
    rejection for each of the four requires, one at a time);
  - `test_vacuum_step_processor_missing_instance_raises_at_first_use`
    (declaration vs check);
  - `test_periodic_vacuum_step_matches_manual_composition` (wiring swap
    or dropped kernel);
  - `test_reflection_user_fails_with_static_vacuum` /
    `test_reflection_user_succeeds_with_periodic_vacuum` (capability
    mismatch at setup);
  - `test_vacuum_step_processor_calls_seed_once` (seed skipped).

This module imports Taichi kernels from `evolution.py` and `boundary.py`;
it does not define any `@ti.kernel` itself.

Note on `external_provides`: every pipeline that hosts
`VacuumStepProcessor` must declare `UnitSystem` in
`external_provides`, because `VacuumStepProcessor.requires` includes
`UnitSystem` (the union of what V1 and V3 need) and no processor
provides it. `WaveGrid` and `PsiBaseField` come from
`AllocateWaveField` and do not need to be declared. `VacuumProvider`
comes from `initial_features` but must still be declared, per the
"declaration, not check" contract.

Run from the project root:

    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._test_vacuum
"""

import sys
import traceback

import numpy as np
import taichi as ti

from ..context import FeatureBag
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
from .boundary import _boundary_periodic
from .evolution import _clear_accel, _laplacian, _leapfrog
from .features import PsiBaseField, WaveGrid
from .units import NaturalUnitSystem, UnitSystem
from .vacuum import (
    PeriodicVacuum,
    StaticVacuum,
    VacuumProvider,
    VacuumStepProcessor,
)

_TI_INITIALIZED = False


def _ti_init() -> None:
    global _TI_INITIALIZED
    if not _TI_INITIALIZED:
        ti.init(arch=ti.cpu, log_level=ti.ERROR)
        _TI_INITIALIZED = True


# ======================================================================
# Fixtures
# ======================================================================


def _seed_base_gaussian_on_np(arr, nx, ny, nz, amp, sigma):
    """Fill a (nx, ny, nz, 3) array with a Gaussian on x at grid centre."""
    cx, cy, cz = nx * 0.5, ny * 0.5, nz * 0.5
    i, j, k = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz), indexing="ij")
    r2 = (i - cx) ** 2 + (j - cy) ** 2 + (k - cz) ** 2
    arr[..., 0] = amp * np.exp(-r2 / (2.0 * sigma * sigma))


class _SeedBase(BaseProcessor):
    """Seed PsiBase from a Gaussian at step 0. Test fixture."""

    name = "_SeedBase"
    stage = Stage.PRE_UPDATE
    order = 5
    requires = (WaveGrid, PsiBaseField)

    def __init__(self, amp=0.3, sigma=4.0):
        self.amp = float(amp)
        self.sigma = float(sigma)

    def process(self, ctx):
        if ctx.sim.step > 0:
            return
        grid = ctx.data.require(WaveGrid)
        field = ctx.data.require(PsiBaseField)
        arr = np.zeros((grid.nx, grid.ny, grid.nz, 3), dtype=np.float32)
        _seed_base_gaussian_on_np(arr, grid.nx, grid.ny, grid.nz, self.amp, self.sigma)
        field.psi.from_numpy(arr)
        field.psi_prev.from_numpy(arr)


class _ReflectionUser(BaseProcessor):
    """
    Test fixture: a processor that requires a reflection-capable vacuum.

    Checks `supports_reflection` in setup() and raises PipelineError if
    the registered provider cannot supply incoming waves. Mirrors the
    contract that a future scattering operator (variant B2d) will obey.
    """

    name = "_ReflectionUser"
    stage = Stage.UPDATE
    order = 10
    requires = (VacuumProvider,)

    def setup(self, ctx):
        vp = ctx.data.require(VacuumProvider)
        if not vp.supports_reflection:
            raise PipelineError(
                f"{self.name}: requires VacuumProvider.supports_reflection=True, "
                f"got {vp.name!r}"
            )

    def process(self, ctx):
        pass


class _RecordingVacuum(VacuumProvider):
    """
    Test fixture: counts seed() invocations. State on the instance is fine
    because a VacuumProvider is a feature, not a processor; the stateless
    guard only runs on processors.
    """

    name = "_RecordingVacuum"

    def __init__(self):
        self.seed_calls = 0

    def seed(self, ctx):
        self.seed_calls += 1

    def step(self, ctx):
        pass


def _run(pipeline, initial, dt=0.1, max_steps=1):
    return Runner({"session": InMemorySink()}).run(
        pipeline,
        name="vacuum_test",
        params={},
        dt=dt,
        max_steps=max_steps,
        initial_features=initial,
    )


# ======================================================================
# Feature shape
# ======================================================================


def test_vacuum_provider_is_abstract():
    """
    VacuumProvider cannot be instantiated; step() is @abstractmethod.

    Mutation caught: @abstractmethod removed from step(), so a subclass
    that forgets to implement it is created silently and runs no-ops.
    """
    try:
        VacuumProvider()  # type: ignore[abstract]
    except TypeError:
        return
    raise AssertionError("expected TypeError for abstract VacuumProvider()")


def test_static_vacuum_capability_flags():
    """
    V1 declares name, evolves=False, supports_reflection=False.

    Mutation caught: a capability flag flipped, so a downstream
    `_ReflectionUser` check passes against V1.
    """
    v = StaticVacuum()
    assert v.name == "StaticVacuum", v.name
    assert v.evolves is False, v.evolves
    assert v.supports_reflection is False, v.supports_reflection


def test_periodic_vacuum_capability_flags():
    """
    V3 declares name, evolves=True, supports_reflection=True.

    Mutation caught: a capability flag flipped, so a valid pipeline with
    `_ReflectionUser` turns into a setup-time error.
    """
    v = PeriodicVacuum()
    assert v.name == "PeriodicVacuum", v.name
    assert v.evolves is True, v.evolves
    assert v.supports_reflection is True, v.supports_reflection


# ======================================================================
# FeatureBag MRO keying
# ======================================================================


def test_static_vacuum_reachable_via_vacuum_provider():
    """
    Setting a StaticVacuum into a FeatureBag makes it reachable through
    VacuumProvider via MRO keying.

    Mutation caught: VacuumProvider dropped from StaticVacuum's bases,
    or FeatureBag.set changed to register only the concrete type.
    """
    bag = FeatureBag()
    v = StaticVacuum()
    bag.set(v)
    assert bag.require(VacuumProvider) is v
    assert bag.require(StaticVacuum) is v


def test_periodic_vacuum_reachable_via_vacuum_provider():
    """
    Same for V3.

    Mutation caught: same shape as above for V3.
    """
    bag = FeatureBag()
    v = PeriodicVacuum()
    bag.set(v)
    assert bag.require(VacuumProvider) is v
    assert bag.require(PeriodicVacuum) is v


# ======================================================================
# Processor: build-time requires
# ======================================================================


def test_vacuum_step_processor_requires_all_four_features():
    """
    VacuumStepProcessor.requires is (VacuumProvider, WaveGrid, UnitSystem,
    PsiBaseField); dropping any one of them makes Pipeline.build() accept
    a pipeline that should have been rejected.

    For each require R, build a pipeline that declares the other three
    in `external_provides` and omits R, then add only VacuumStepProcessor.
    Pipeline.build() must raise PipelineError naming R.

    Each of the four requires is tested independently, so dropping one
    requirement does not hide the others. A single-arm check would only
    catch the first missing feature and would miss the rest.

    Mutation caught: any of the four dropped from requires.
    """
    _ti_init()

    requires = (VacuumProvider, WaveGrid, UnitSystem, PsiBaseField)
    for missing in requires:
        provided = tuple(f for f in requires if f is not missing)

        class P(Pipeline):
            def __init__(self):
                super().__init__(
                    error_policy=ErrorPolicy.FAIL_FAST,
                    external_provides=provided,
                )
                self.add(VacuumStepProcessor())

        try:
            _run(P(), [NaturalUnitSystem()], max_steps=1)
        except PipelineError as e:
            assert missing.__name__ in str(e), (missing.__name__, str(e))
            continue
        raise AssertionError(
            f"expected PipelineError naming {missing.__name__}, none raised"
        )


def test_vacuum_step_processor_missing_instance_raises_at_first_use():
    """
    A pipeline that declares VacuumProvider in `external_provides` but
    does not pass an instance in `initial_features` builds successfully
    and raises KeyError at first require() inside process().

    Mutation caught: the require() moved out of process(), or a build-
    time check added that would turn this KeyError into PipelineError.
    Either way, the documented contract ("declaration, not check")
    changes.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=(VacuumProvider, UnitSystem),
            )
            self.add(AllocateWaveField(nx=8, ny=8, nz=8, dx=1.0))
            self.add(VacuumStepProcessor())

    try:
        _run(P(), [NaturalUnitSystem()], max_steps=1)  # no vacuum instance
    except KeyError as e:
        assert "VacuumProvider" in str(e), str(e)
        return
    raise AssertionError("expected KeyError naming VacuumProvider")


# ======================================================================
# Functional: base field under V1 and V3
# ======================================================================


def test_static_vacuum_leaves_base_field_unchanged():
    """
    With StaticVacuum, PsiBase is unchanged after 20 steps.

    Mutation caught: V1.step() writes to field.psi or field.psi_prev
    (e.g. a copy of V3's body), so the base field changes.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=(VacuumProvider, UnitSystem),
            )
            self.add(AllocateWaveField(nx=16, ny=16, nz=16, dx=1.0))
            self.add(_SeedBase(amp=0.3, sigma=4.0))
            self.add(VacuumStepProcessor())

    ctx = _run(P(), [NaturalUnitSystem(), StaticVacuum()], dt=0.05, max_steps=20)
    assert not ctx.diag.errors, ctx.diag.errors

    field = ctx.data.require(PsiBaseField)
    grid = ctx.data.require(WaveGrid)
    ref = np.zeros((grid.nx, grid.ny, grid.nz, 3), dtype=np.float32)
    _seed_base_gaussian_on_np(ref, grid.nx, grid.ny, grid.nz, 0.3, 4.0)
    diff = float(np.abs(field.psi.to_numpy() - ref).max())
    assert diff < 1e-7, f"StaticVacuum changed PsiBase by {diff}"


def test_periodic_vacuum_evolves_base_field():
    """
    With PeriodicVacuum, PsiBase differs from its seed after 5 steps.

    Mutation caught: V3.step() is a no-op, so the base field stays at
    its seed. The companion arm to the V1 test.

    Arena: amp=1.0, dt=0.1, 5 steps. The first step's change at the
    centre is dt^2 * |laplacian| ~ 0.01 * 0.18 = 1.8e-3, so 5 steps move
    the field above 1e-4 unless the cumulative change cancels almost
    exactly within the first half-period. The test asserts only what
    the field's seed and the scheme imply: the field must have moved.

    The earlier draft of this test used amp=0.3, dt=0.05, 20 steps and a
    1e-3 bar. That bar was marginal because the cumulative change
    oscillates with the field's own period and could drop below 1e-3 on
    some platforms within 20 steps.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=(VacuumProvider, UnitSystem),
            )
            self.add(AllocateWaveField(nx=16, ny=16, nz=16, dx=1.0))
            self.add(_SeedBase(amp=1.0, sigma=4.0))
            self.add(VacuumStepProcessor())

    ctx = _run(P(), [NaturalUnitSystem(), PeriodicVacuum()], dt=0.1, max_steps=5)
    assert not ctx.diag.errors, ctx.diag.errors

    field = ctx.data.require(PsiBaseField)
    grid = ctx.data.require(WaveGrid)
    ref = np.zeros((grid.nx, grid.ny, grid.nz, 3), dtype=np.float32)
    _seed_base_gaussian_on_np(ref, grid.nx, grid.ny, grid.nz, 1.0, 4.0)
    diff = float(np.abs(field.psi.to_numpy() - ref).max())
    assert diff > 1e-4, f"PeriodicVacuum did not evolve PsiBase: max diff {diff}"


# ======================================================================
# Structural: V3.step matches manual composition
# ======================================================================


def test_periodic_vacuum_step_matches_manual_composition():
    """
    Two calls to VacuumStepProcessor (V3) produce the same PsiBase as the
    manual sequence `_clear_accel -> _laplacian -> _leapfrog ->
    _boundary_periodic`, run twice on the same seed.

    Mutation caught:
        - `_boundary_periodic` dropped from V3.step -> mismatch at boundary;
        - `_laplacian` and `_leapfrog` swapped -> mismatch everywhere;
        - `_clear_accel` dropped -> mismatch on the second call (stale
          psi_new from the first).

    This is the not-happy-path arm that catches a wiring swap or a
    dropped kernel inside V3.step, which a plain "field changed" check
    cannot.
    """
    _ti_init()

    N = 16
    dt = 0.05

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=(VacuumProvider, UnitSystem),
            )
            self.add(AllocateWaveField(nx=N, ny=N, nz=N, dx=1.0))
            self.add(_SeedBase(amp=0.3, sigma=3.0))
            self.add(VacuumStepProcessor())

    ctx = _run(P(), [NaturalUnitSystem(), PeriodicVacuum()], dt=dt, max_steps=2)
    assert not ctx.diag.errors, ctx.diag.errors

    v3_field = ctx.data.require(PsiBaseField).psi.to_numpy()
    v3_prev = ctx.data.require(PsiBaseField).psi_prev.to_numpy()

    # Manual arm
    psi_ti = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    prev_ti = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))
    new_ti = ti.Vector.field(3, dtype=ti.f32, shape=(N, N, N))

    seed = np.zeros((N, N, N, 3), dtype=np.float32)
    _seed_base_gaussian_on_np(seed, N, N, N, 0.3, 3.0)
    psi_ti.from_numpy(seed)
    prev_ti.from_numpy(seed)
    new_ti.fill(0.0)

    units = NaturalUnitSystem()
    dt2 = dt * dt
    for _ in range(2):
        _clear_accel(new_ti, N, N, N)
        _laplacian(psi_ti, new_ti, N, N, N, 1.0, float(units.c))
        _leapfrog(psi_ti, prev_ti, new_ti, N, N, N, dt2)
        _boundary_periodic(psi_ti, prev_ti, N, N, N)

    manual_psi = psi_ti.to_numpy()
    manual_prev = prev_ti.to_numpy()

    d_psi = float(np.abs(v3_field - manual_psi).max())
    d_prev = float(np.abs(v3_prev - manual_prev).max())
    assert d_psi < 1e-5, f"V3 psi mismatches manual composition by {d_psi}"
    assert d_prev < 1e-5, f"V3 prev mismatches manual composition by {d_prev}"


# ======================================================================
# Capability mismatch: reflection
# ======================================================================


def test_reflection_user_fails_with_static_vacuum():
    """
    A processor that requires supports_reflection=True raises
    PipelineError at setup when the registered vacuum is V1.

    Mutation caught: the supports_reflection check in
    _ReflectionUser.setup removed, so the pipeline runs silently with
    an unsupported vacuum.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=(VacuumProvider, UnitSystem),
            )
            self.add(AllocateWaveField(nx=8, ny=8, nz=8, dx=1.0))
            self.add(_ReflectionUser())

    try:
        _run(P(), [NaturalUnitSystem(), StaticVacuum()], max_steps=1)
    except PipelineError as e:
        assert "supports_reflection" in str(e), str(e)
        return
    raise AssertionError("expected PipelineError, none raised")


def test_reflection_user_succeeds_with_periodic_vacuum():
    """
    The same processor with V3 passes its setup check.

    Mutation caught: PeriodicVacuum.supports_reflection flipped to False,
    which turns a valid pipeline into a setup-time error.
    """
    _ti_init()

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=(VacuumProvider, UnitSystem),
            )
            self.add(AllocateWaveField(nx=8, ny=8, nz=8, dx=1.0))
            self.add(_ReflectionUser())

    ctx = _run(P(), [NaturalUnitSystem(), PeriodicVacuum()], max_steps=1)
    assert not ctx.diag.errors, ctx.diag.errors


# ======================================================================
# Lifecycle: seed once
# ======================================================================


def test_vacuum_step_processor_calls_seed_once():
    """
    VacuumStepProcessor calls seed(ctx) exactly once, at step 0, and not
    on later steps.

    Mutation caught: `if ctx.sim.step == 0: vp.seed(ctx)` removed (seed
    never fires) or moved outside the guard (seed fires every step).
    Neither V1 nor V3 can detect this on its own because both have
    no-op seed(); a recording variant is needed.
    """
    _ti_init()

    recording = _RecordingVacuum()

    class P(Pipeline):
        def __init__(self):
            super().__init__(
                error_policy=ErrorPolicy.FAIL_FAST,
                external_provides=(VacuumProvider, UnitSystem),
            )
            self.add(AllocateWaveField(nx=8, ny=8, nz=8, dx=1.0))
            self.add(VacuumStepProcessor())

    _run(P(), [NaturalUnitSystem(), recording], max_steps=5)
    assert recording.seed_calls == 1, recording.seed_calls


# ======================================================================
# Energy budget
# ======================================================================


def test_energy_budget_zero_for_both_variants():
    """
    Both V1 and V3 report energy_budget() == 0.0: they are conservative.

    Mutation caught: energy_budget() overridden to return a non-zero
    constant, which would make a downstream budget check believe the
    vacuum is injecting or absorbing energy.
    """
    v1 = StaticVacuum()
    v3 = PeriodicVacuum()
    assert v1.energy_budget() == 0.0, v1.energy_budget()
    assert v3.energy_budget() == 0.0, v3.energy_budget()


# ======================================================================
# Runner
# ======================================================================


def main() -> int:
    tests = [
        test_vacuum_provider_is_abstract,
        test_static_vacuum_capability_flags,
        test_periodic_vacuum_capability_flags,
        test_static_vacuum_reachable_via_vacuum_provider,
        test_periodic_vacuum_reachable_via_vacuum_provider,
        test_vacuum_step_processor_requires_all_four_features,
        test_vacuum_step_processor_missing_instance_raises_at_first_use,
        test_static_vacuum_leaves_base_field_unchanged,
        test_periodic_vacuum_evolves_base_field,
        test_periodic_vacuum_step_matches_manual_composition,
        test_reflection_user_fails_with_static_vacuum,
        test_reflection_user_succeeds_with_periodic_vacuum,
        test_vacuum_step_processor_calls_seed_once,
        test_energy_budget_zero_for_both_variants,
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