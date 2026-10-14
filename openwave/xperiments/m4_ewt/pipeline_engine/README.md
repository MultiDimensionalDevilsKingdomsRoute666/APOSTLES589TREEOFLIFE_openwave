# pipeline_engine

Domain-agnostic staged pipeline engine for M4. Runs a list of stateless
processors against a shared Context. Knows nothing about physics, waves,
or Taichi.

## What it is

The engine is a composition root for a simulation: you build a Pipeline
from processors, hand it to a Runner, and the Runner executes it step by
step. Each processor has one responsibility and is stateless; runtime
state lives in a typed FeatureBag inside the Context.

## Why

M4's wave_engine.py is a single monolithic solver where the update,
boundary condition, wave-center drive, trackers, and buffer swap all live
in one kernel. Adding a mode means editing several files; comparing two
modes means two branches of code. The engine offers composition instead:
a pipeline is a list of processors, and swapping one processor is the only
change needed to try a different physics model. wave_engine.py and the
launcher are left as they are; the engine sits alongside them.

## Quick start

    from openwave.xperiments.m4_ewt.pipeline_engine import (
        Pipeline, Runner, Stage, BaseProcessor,
        JsonSessionSink, LogProcessor,
    )

    class Increment(BaseProcessor):
        name = "Increment"
        stage = Stage.UPDATE
        order = 10
        # requires/provides default to empty

        def process(self, ctx):
            # runtime state goes in ctx.data, not self
            pass

    class MyPipeline(Pipeline):
        def __init__(self):
            super().__init__()
            self.add(Increment())

    runner = Runner({"session": JsonSessionSink("out/session.json")})
    ctx = runner.run(MyPipeline(), name="demo", max_steps=100)
    print(ctx.diag.errors)

## Design rules

Z1. Zero module-level state. Everything lives in Context or in instances.
Z2. Every mutation goes through a processor. No side effects from the runner.
Z3. Explicit requires/provides graph, validated at Pipeline.build().
Z4. setup/teardown are lifecycle hooks; process() is per-step.
Z5. The runner is an interface (IRunner). Runner is the default implementation.
Z6. Sinks are an interface (ILogSink). Several implementations included.
Z7. Measurement and logging are separate processors.
Z8. Parameters are typed and grouped separately from run identity.

## Stages

    PRE_UPDATE   -- runs before evolution. Example: seed, boundary pin, source.
    UPDATE       -- evolution. Example: Laplacian, nonlinearity, integrator.
    POST_UPDATE  -- runs after evolution. Example: boundary enforcement.
    MEASURE      -- read-only. Example: trackers, logging, visualization.

Processors with stage=None are lifecycle only: they run setup() once before
the first step and teardown() once after the last (allocators, subprocess
spawns, resource acquisition). There is no SETUP member in Stage.

## Context

Every processor sees one object, Context, with five sub-objects:

    run     -- immutable run identity (name, output_dir); the seed is the RunSeed feature
    params  -- typed read-only parameter access (get_int, require_float, ...)
    sim     -- mutable simulation clock (dt, t, step, should_stop)
    data    -- FeatureBag: typed container, key is the class
    log     -- sinks by name (LogContext)
    diag    -- errors, warnings, timings (Diagnostics)

A processor reaches state through ctx.data.require(SomeFeature). Adding a
new feature never changes any signature.

## Statelessness

Processors are stateless by default. With the guard enabled, the engine
compares the repr() of every instance field before and after process() and
raises on any difference, so both a rebind (self.n = self.n + 1) and an
in-place change to a list or dict (self.hist.append(...)) are caught. A change
that leaves the repr unchanged is not: the contents of a Taichi field, a NumPy
array of more than 1000 elements (NumPy abbreviates its repr), or the
attributes of an object whose repr does not show them. Runtime state belongs
in ctx.data. When memoization is genuinely required, set `stateless = False`
on the class.

The check is opt-in: Runner(..., check_stateless=True) enables it, and the
guard runs only when enabled. Processors with `stateless = False` are skipped.

## Error handling

ErrorPolicy selects what happens when a processor raises:

    FAIL_FAST  -- re-raise, stop immediately
    SOFT_STOP  -- log, set should_stop, run teardown, exit cleanly
    CONTINUE   -- log, skip to the next processor

Default is SOFT_STOP. The error is recorded in ctx.diag.errors either way.

The policy covers process() only. A failure in setup() always propagates the
original exception, after the processors already set up are torn down in
reverse.

## Units

Every dimensional constant the engine needs comes from a `UnitSystem`
feature. No processor contains a dimensional literal; the rule is enforced
by `_check_dimensional_literals.py`, which scans `physics/` for numeric
literals assigned to known dimensional names.

### The contract

    from openwave.xperiments.m4_ewt.pipeline_engine.physics.units import UnitSystem

    units = ctx.data.require(UnitSystem)
    c = units.c
    gamma = units.gamma
    dx = units.dx

Core fields: `c`, `wavelength`, `dx`, `dt`, `rho_0`.
Geometric fields: `A_pi`, `eps_M`, `N_geom`, `gamma`, `X_eff`, `N_nu_eff`.
Conversion methods: `to_physical_length`, `to_physical_time`,
`to_physical_energy`, `to_physical_density`.

### Implementations

Three implementations ship with the engine:

| Class | Units | Use |
| --- | --- | --- |
| `NaturalUnitSystem` | `lambda_nu = 1`, `c = 1` | Default for research |
| `OpenWaveUnitSystem` | attometres, rontoseconds | Legacy xparameters |
| `SIUnitSystem` | metres, seconds | Output conversion only |

The geometric fields are identical across all three: they are pure
numbers derived from the BCC lattice geometry and the manuscript's
fine-structure derivation, and they do not depend on the choice of unit
system.

### Registration

Register the unit system under the abstract `UnitSystem` key, not the
concrete class. The engine's `FeatureBag.set` registers a value under
its concrete type and every base class in its MRO (excluding `object`),
so requiring `UnitSystem` returns the concrete instance without an extra
registration step.

    runner.run(
        pipeline,
        name="...",
        params={},
        dt=units.dt,
        max_steps=100,
        initial_features=[units],     # FeatureBag.set keys by MRO
    )

`UnitSystem` is an abstract base class. A processor that declares
`requires = (UnitSystem,)` receives whatever concrete implementation the
caller registered.

### Adding a new unit system

Subclass `UnitSystem` and provide the core fields and conversion methods.
The geometric fields come from the shared mixin. Add the new name to
`make_unit_system`.

## Folder layout

    context.py    -- FeatureBag, Params, Context, Diagnostics, sub-contexts
    pipeline.py   -- Stage, ErrorPolicy, IProcessor, BaseProcessor, Pipeline
    sinks.py      -- ILogSink, JsonSessionSink, LiveJsonSink, InMemorySink
    loggers.py    -- LogProcessor (writes a ctx-derived payload to a sink)
    runner.py     -- IRunner, Runner
    experiments.py -- ExperimentConfig, ExperimentSummary, ExperimentRunner (sweep driver)
    processors/   -- domain-agnostic processors (checkpoint, monitor spawn, ...)
    physics/      -- physics processors and feature types (separate layer)

The engine never imports physics. The physics layer imports the engine.

## Testing

Smoke test (no Taichi required):

    python -m openwave.xperiments.m4_ewt.pipeline_engine._smoke_test

Runs six scenarios: a normal pipeline, a pipeline with an injected failure
(SOFT_STOP in action), a pipeline with file sinks, a pipeline reading a
caller-supplied feature (external_provides), and two regression checks, one
for the stateless guard and one for a failing setup().

Physics demo (requires Taichi):

    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo
    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo --k 10 --geometry tetrahedron_10_locked --no-window --steps 3000

## Adding a new processor

1. Subclass BaseProcessor.
2. Set name, stage, order, requires, provides.
3. Put configuration in __init__ (immutable).
4. Put runtime state in ctx.data (typed feature).
5. Implement setup/process/teardown as needed.

If the processor needs a feature that is not provided by any other
processor, either declare it via Pipeline(external_provides=...) and pass
an instance through Runner.run(..., initial_features=[...]), or add a
lifecycle processor that provides it in setup().
