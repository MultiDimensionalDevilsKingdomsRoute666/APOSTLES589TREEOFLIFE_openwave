"""
Experiment runner: iterate over a list of configurations, run each
through a Runner, collect summaries.

Contains:
    ExperimentConfig   -- frozen config for one run
    ExperimentSummary  -- result of one run
    ExperimentRunner   -- the sweep driver

Design:
    Composition, not inheritance. ExperimentRunner holds factories, not
    concrete objects. The IRunner stays the single execution backend;
    a test can pass a mock factory and skip Taichi entirely.

    Per-config freshness. Pipeline, sinks, and runner are all built
    fresh for each config, through three callables:

        pipeline_factory(config)   -> Pipeline
        sinks_factory(config)      -> Mapping[str, ILogSink]
        runner_factory(sinks)      -> IRunner

    Why three factories and not one runner instance: Runner holds its
    sinks in __init__ and reuses them across run() calls. A shared
    JsonSessionSink accumulates records across runs (its open() sets
    meta but does not clear the buffer), so a sweep with a single
    runner and a single sink dict would produce a merged log. The
    factory shape makes per-run isolation the default.

    The engine does not know what a metric is: the caller supplies a
    summarize(ctx) -> Mapping. This keeps the ExperimentRunner
    domain-agnostic (engine layer, no physics import).

    Summary is plain data (frozen dataclass), so a sweep result can be
    written to JSON, compared across runs, or hashed for artifact
    versioning (plan item 1.21) without further conversion.

Seeds. There is no seed field on ExperimentConfig. A caller that wants
determinism adds a RunSeed feature to initial_features:
initial_features=(..., RunSeed(42)). This keeps the seed reachable
through the same graph as every other runtime value (Z3), and leaves
the runner interface unchanged. Item 1.19 makes the simulation read
from RunSeed; this module only transports it.

Note: this module does not import Taichi, does not import physics.
"""

from __future__ import annotations

import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from .context import Context
from .pipeline import Pipeline
from .runner import IRunner
from .sinks import ILogSink


# Allowed values for ExperimentRunner.on_error. A string is used rather
# than an enum because the two policies are the two branches of a single
# try/except; adding a third would need its own branch, and that is the
# right moment to introduce an enum.
_ERROR_POLICIES = ("continue", "fail")


@dataclass(frozen=True)
class ExperimentConfig:
    """
    One run's configuration. Frozen: a sweep must not mutate its own
    configs while iterating.

    name              -- run name; goes into the sink metadata and the
                         summary. Must be unique within a sweep (the
                         runner does not enforce this; a duplicate name
                         silently overwrites in a sink that keys by
                         name, and appears twice in the summary list).
    params            -- arbitrary key/value, forwarded to
                         IRunner.run(params=...). Not interpreted by the
                         engine.
    initial_features  -- tuple of FeatureBag features passed to
                         IRunner.run(initial_features=...). A tuple, not
                         a list, so the frozen dataclass is hashable.
                         This is where a RunSeed goes when the caller
                         wants determinism.
    dt, max_steps     -- forwarded to IRunner.run.
    """

    name: str
    params: Mapping[str, object] = field(default_factory=dict)
    initial_features: tuple = ()
    dt: float = 1.0
    max_steps: int = 100


@dataclass(frozen=True)
class ExperimentSummary:
    """
    The result of one run. Plain data: no Context, no Pipeline, no
    Taichi handles. Safe to serialize, compare, or hash.

    name       -- the config's name, echoed for traceability.
    config     -- the config's params, echoed. The rest of the config
                  (dt, max_steps, initial_features) is not echoed
                  because initial_features may hold non-serializable
                  objects (Ti fields, WCState); a summary that cannot be
                  JSON-dumped would defeat the point.
    metrics    -- whatever summarize(ctx) returned.
    errors     -- ctx.diag.errors, copied as a tuple.
    warnings   -- ctx.diag.warnings, copied as a tuple.
    duration_s -- wall-clock seconds for this run, from
                  time.perf_counter(). Diagnostic; the engine does not
                  use it.
    crashed    -- True if summarize or the run raised before a summary
                  could be built (only reachable with on_error="continue").
                  When True, metrics is empty and the exception text is
                  in errors.
    """

    name: str
    config: Mapping[str, object]
    metrics: Mapping[str, object]
    errors: tuple = ()
    warnings: tuple = ()
    duration_s: float = 0.0
    crashed: bool = False


class ExperimentRunner:
    """
    Drive a sweep: for each config, build a fresh pipeline, a fresh set
    of sinks, and a fresh runner, then run one experiment and collect
    the summary.

    Parameters
    ----------
    runner_factory : Callable[[Mapping[str, ILogSink]], IRunner]
        Called once per config with the sinks the sink factory produced.
        In production: ``lambda sinks: Runner(sinks)``. In tests: a mock
        that ignores the sinks.
    sinks_factory : Callable[[ExperimentConfig], Mapping[str, ILogSink]]
        Called once per config; must return a fresh dict of sinks per
        call. Sharing instances across configs is a caller's explicit
        choice; see the module docstring for why it is not the default.
    on_error : {"continue", "fail"}
        "continue" (default): a run that raises is recorded as a crashed
        summary, the sweep moves to the next config.
        "fail": the first raise propagates and the sweep stops. The
        configs before it are not returned.
    """

    def __init__(
        self,
        runner_factory: Callable[[Mapping[str, ILogSink]], IRunner],
        *,
        sinks_factory: Callable[[ExperimentConfig], Mapping[str, ILogSink]],
        on_error: str = "continue",
    ):
        if on_error not in _ERROR_POLICIES:
            raise ValueError(
                f"ExperimentRunner: on_error must be one of {_ERROR_POLICIES}, "
                f"got {on_error!r}"
            )
        if not callable(runner_factory):
            raise TypeError(
                "ExperimentRunner: runner_factory must be callable "
                "(takes the sinks mapping, returns an IRunner)"
            )
        if not callable(sinks_factory):
            raise TypeError(
                "ExperimentRunner: sinks_factory must be callable "
                "(takes an ExperimentConfig, returns a Mapping); "
                "if you have a Mapping, wrap it: lambda cfg: my_dict"
            )
        self._runner_factory = runner_factory
        self._sinks_factory = sinks_factory
        self._on_error = on_error

    def run_sweep(
        self,
        *,
        pipeline_factory: Callable[[ExperimentConfig], Pipeline],
        configs: Sequence[ExperimentConfig],
        summarize: Callable[[Context], Mapping[str, object]],
        output_dir: Path | str,
    ) -> list[ExperimentSummary]:
        """
        Run every config once. Returns one ExperimentSummary per config,
        in input order.

        pipeline_factory(config) -> Pipeline    fresh pipeline per run
        summarize(ctx)          -> Mapping     caller's metric extraction

        summarize must return a Mapping. Returning None (or any
        non-Mapping) raises TypeError inside dict(), caught by the same
        on_error policy as a run failure.

        output_dir is passed to IRunner.run() as the run's output
        directory. Its concrete use (subdirectory per run, per-sweep
        log, nothing at all) is up to the sinks the factory returns.
        """
        out_dir = Path(output_dir)
        summaries: list[ExperimentSummary] = []

        for cfg in configs:
            t0 = time.perf_counter()
            try:
                pipeline = pipeline_factory(cfg)
                sinks = self._sinks_factory(cfg)
                runner = self._runner_factory(sinks)
                ctx = runner.run(
                    pipeline,
                    name=cfg.name,
                    params=cfg.params,
                    output_dir=out_dir,
                    dt=cfg.dt,
                    max_steps=cfg.max_steps,
                    # Runner.run takes a list; the config stores a tuple
                    # for hashability. Convert here.
                    initial_features=list(cfg.initial_features),
                )
                metrics = dict(summarize(ctx))
                duration = time.perf_counter() - t0
                summaries.append(
                    ExperimentSummary(
                        name=cfg.name,
                        config=dict(cfg.params),
                        metrics=metrics,
                        errors=tuple(ctx.diag.errors),
                        warnings=tuple(ctx.diag.warnings),
                        duration_s=duration,
                        crashed=False,
                    )
                )
            except Exception as e:
                if self._on_error == "fail":
                    raise
                duration = time.perf_counter() - t0
                summaries.append(
                    ExperimentSummary(
                        name=cfg.name,
                        config=dict(cfg.params),
                        metrics={},
                        errors=(f"{type(e).__name__}: {e}",),
                        warnings=(),
                        duration_s=duration,
                        crashed=True,
                    )
                )

        return summaries