"""
Tests for ExperimentRunner (plan item 1.10).

No Taichi. Mock IRunner captures the call arguments and returns a
Context with an empty FeatureBag. This module tests the sweep
machinery, not any physics.

Run from the project root:
    python -m openwave.xperiments.m4_ewt.pipeline_engine._test_experiment_runner
"""

import sys
import traceback
from pathlib import Path

from .context import Context, Diagnostics, FeatureBag, LogContext, Params, RunContext, SimContext
from .experiments import ExperimentConfig, ExperimentRunner, ExperimentSummary
from .pipeline import Pipeline
from .sinks import InMemorySink

# ======================================================================
# Mock IRunner
# ======================================================================


class _MockRunner:
    """
    Records every run() call and returns a minimal Context.

    The FeatureBag is empty; the summarize callable in each test reads
    whatever it wants from ctx.run.name or ctx.params. Populating a
    feature would couple these tests to a physics feature, which is not
    the point here.
    """

    def __init__(self, *, crash_on_name: str | None = None):
        self.calls = []
        self._crash_on_name = crash_on_name

    def run(
        self,
        pipeline,
        *,
        name,
        params=None,
        output_dir="out",
        dt=1.0,
        max_steps,
        initial_features=None,
    ):
        self.calls.append(
            {
                "name": name,
                "params": dict(params or {}),
                "output_dir": Path(output_dir),
                "dt": dt,
                "max_steps": max_steps,
                "initial_features": list(initial_features or []),
                "pipeline": pipeline,
            }
        )
        if self._crash_on_name is not None and name == self._crash_on_name:
            raise RuntimeError(f"mock crash for {name}")
        return Context(
            run=RunContext(name=name, output_dir=Path(output_dir)),
            params=Params(params),
            sim=SimContext(dt=dt),
            data=FeatureBag(),
            log=LogContext(sinks={}),
            diag=Diagnostics(),
        )


def _make_pipeline():
    """A pipeline with no processors. Legal (build validates nothing)."""

    class P(Pipeline):
        def __init__(self):
            super().__init__()

    return P()


def _identity_summarize(ctx):
    """Summarize by echoing the run name. No features required."""
    return {"name": ctx.run.name}


# ======================================================================
# Config / Summary dataclasses
# ======================================================================


def test_config_defaults():
    """
    Every field has a documented default except name.

    Mutation caught: a default changed silently (e.g. dt=1.0 to dt=0.0),
    which would change every sweep that omitted the field.
    """
    c = ExperimentConfig(name="x")
    assert c.name == "x"
    assert dict(c.params) == {}
    assert c.initial_features == ()
    assert c.dt == 1.0
    assert c.max_steps == 100


def test_config_is_frozen():
    """
    ExperimentConfig is frozen: attempting to mutate raises.

    Mutation caught: frozen=True dropped, which would let a sweep
    mutate its own config mid-iteration.
    """
    c = ExperimentConfig(name="x")
    try:
        c.dt = 42.0  # type: ignore[misc]
    except Exception:
        return
    raise AssertionError("ExperimentConfig must be frozen")


def test_summary_defaults():
    """
    Every summary field has a documented default; crashed defaults False.

    Mutation caught: crashed default changed to True, which would make
    every successful run read as a crash.
    """
    s = ExperimentSummary(name="x", config={}, metrics={})
    assert s.errors == ()
    assert s.warnings == ()
    assert s.duration_s == 0.0
    assert s.crashed is False


# ======================================================================
# ExperimentRunner: sweep mechanics
# ======================================================================


def test_empty_config_list_returns_empty():
    """
    Empty input -> empty output. No factory called.

    Mutation caught: the loop overwritten to assume at least one config.
    """
    mock = _MockRunner()
    er = ExperimentRunner(
        runner_factory=lambda sinks: mock,
        sinks_factory=lambda cfg: {"session": InMemorySink()},
    )
    result = er.run_sweep(
        pipeline_factory=lambda cfg: _make_pipeline(),
        configs=[],
        summarize=_identity_summarize,
        output_dir=Path("out_test"),
    )
    assert result == []
    assert mock.calls == []


def test_three_configs_produce_three_summaries_in_order():
    """
    Three configs -> three summaries, in input order.

    Mutation caught: results appended unordered (e.g. sorted by name),
    or the loop dropping the last item.
    """
    mock = _MockRunner()
    er = ExperimentRunner(
        runner_factory=lambda sinks: mock,
        sinks_factory=lambda cfg: {"session": InMemorySink()},
    )
    configs = [
        ExperimentConfig(name="a", params={"i": 0}),
        ExperimentConfig(name="b", params={"i": 1}),
        ExperimentConfig(name="c", params={"i": 2}),
    ]
    result = er.run_sweep(
        pipeline_factory=lambda cfg: _make_pipeline(),
        configs=configs,
        summarize=_identity_summarize,
        output_dir=Path("out_test"),
    )
    assert len(result) == 3
    assert [s.name for s in result] == ["a", "b", "c"]
    assert [s.config["i"] for s in result] == [0, 1, 2]
    assert [s.metrics["name"] for s in result] == ["a", "b", "c"]


def test_pipeline_and_sinks_factories_called_once_per_config():
    """
    pipeline_factory and sinks_factory are called exactly once per
    config, and the pipeline instance differs between runs.

    Mutation caught: pipeline built once outside the loop (would break
    on pipelines that hold state across setup/teardown), or sink dict
    built once (would accumulate records across runs for a JsonSessionSink).
    """
    mock = _MockRunner()
    pipeline_calls = []
    sink_calls = []

    def pipeline_factory(cfg):
        p = _make_pipeline()
        pipeline_calls.append((cfg.name, id(p)))
        return p

    def sinks_factory(cfg):
        sink_calls.append(cfg.name)
        return {"session": InMemorySink()}

    er = ExperimentRunner(
        runner_factory=lambda sinks: mock,
        sinks_factory=sinks_factory,
    )
    configs = [ExperimentConfig(name=f"c{i}") for i in range(3)]
    er.run_sweep(
        pipeline_factory=pipeline_factory,
        configs=configs,
        summarize=_identity_summarize,
        output_dir=Path("out_test"),
    )
    assert [n for n, _ in pipeline_calls] == ["c0", "c1", "c2"]
    assert len({pid for _, pid in pipeline_calls}) == 3
    assert sink_calls == ["c0", "c1", "c2"]


def test_runner_factory_called_once_per_config():
    """
    runner_factory is called once per config, with the sinks that the
    sink factory produced for that config.

    Mutation caught: runner built once outside the loop (would defeat
    the per-config sinks), or the sink mapping not passed to the
    runner factory (would leave every runner with an empty sink dict).
    """
    calls = []

    class _TinyMock:
        def run(
            self,
            pipeline,
            *,
            name,
            params=None,
            output_dir="out",
            dt=1.0,
            max_steps,
            initial_features=None,
        ):
            return Context(
                run=RunContext(name=name, output_dir=Path(output_dir)),
                params=Params(params),
                sim=SimContext(dt=dt),
                data=FeatureBag(),
                log=LogContext(sinks={}),
                diag=Diagnostics(),
            )

    def runner_factory(sinks):
        calls.append({"sinks": sinks})
        return _TinyMock()

    def sinks_factory(cfg):
        return {"session": InMemorySink(), "tag": cfg.name}

    er = ExperimentRunner(
        runner_factory=runner_factory,
        sinks_factory=sinks_factory,
    )
    configs = [ExperimentConfig(name=f"c{i}") for i in range(3)]
    er.run_sweep(
        pipeline_factory=lambda cfg: _make_pipeline(),
        configs=configs,
        summarize=_identity_summarize,
        output_dir=Path("out_test"),
    )
    assert len(calls) == 3
    assert [c["sinks"]["tag"] for c in calls] == ["c0", "c1", "c2"]


def test_initial_features_forwarded_to_runner():
    """
    Everything in initial_features reaches IRunner.run() as a list, in
    order. This is the path a RunSeed takes.

    Mutation caught: initial_features dropped or converted to something
    the FeatureBag cannot key by MRO (e.g. flattened).
    """
    mock = _MockRunner()
    er = ExperimentRunner(
        runner_factory=lambda sinks: mock,
        sinks_factory=lambda cfg: {"session": InMemorySink()},
    )

    class _Tag:
        def __init__(self, v):
            self.v = v

    t1, t2 = _Tag(1), _Tag(2)
    configs = [
        ExperimentConfig(
            name="a",
            initial_features=(t1, t2),
            dt=0.25,
            max_steps=33,
        )
    ]
    er.run_sweep(
        pipeline_factory=lambda cfg: _make_pipeline(),
        configs=configs,
        summarize=_identity_summarize,
        output_dir=Path("out_test"),
    )
    call = mock.calls[0]
    assert call["initial_features"] == [t1, t2]
    assert call["dt"] == 0.25
    assert call["max_steps"] == 33


def test_params_forwarded_to_runner():
    """
    ExperimentConfig.params reaches IRunner.run(params=...).

    Mutation caught: params dropped, or converted to a different mapping
    type that the Params wrapper does not accept.
    """
    mock = _MockRunner()
    er = ExperimentRunner(
        runner_factory=lambda sinks: mock,
        sinks_factory=lambda cfg: {"session": InMemorySink()},
    )
    configs = [
        ExperimentConfig(name="a", params={"k": 1, "topology": "golden"}),
    ]
    er.run_sweep(
        pipeline_factory=lambda cfg: _make_pipeline(),
        configs=configs,
        summarize=_identity_summarize,
        output_dir=Path("out_test"),
    )
    assert mock.calls[0]["params"] == {"k": 1, "topology": "golden"}


# ======================================================================
# Error handling
# ======================================================================


def test_on_error_continue_records_crash_and_keeps_going():
    """
    With on_error='continue', a crash in one config is captured as a
    summary with crashed=True, and the sweep finishes.

    Mutation caught: exception swallowed silently (crashed=False), or
    the loop exiting early on the first raise.
    """
    mock = _MockRunner(crash_on_name="b")
    er = ExperimentRunner(
        runner_factory=lambda sinks: mock,
        sinks_factory=lambda cfg: {"session": InMemorySink()},
        on_error="continue",
    )
    configs = [ExperimentConfig(name=n) for n in ("a", "b", "c")]
    result = er.run_sweep(
        pipeline_factory=lambda cfg: _make_pipeline(),
        configs=configs,
        summarize=_identity_summarize,
        output_dir=Path("out_test"),
    )
    assert len(result) == 3
    assert result[0].crashed is False
    assert result[1].crashed is True
    assert result[2].crashed is False
    assert any("RuntimeError" in e for e in result[1].errors)
    assert result[1].metrics == {}
    assert [call["name"] for call in mock.calls] == ["a", "b", "c"]


def test_on_error_fail_stops_at_first_crash():
    """
    With on_error='fail', the first raise propagates and later configs
    are not called.

    Mutation caught: fail policy silently downgraded to continue, or
    the exception wrapped in another so the caller cannot see the
    original type.
    """
    mock = _MockRunner(crash_on_name="b")
    er = ExperimentRunner(
        runner_factory=lambda sinks: mock,
        sinks_factory=lambda cfg: {"session": InMemorySink()},
        on_error="fail",
    )
    configs = [ExperimentConfig(name=n) for n in ("a", "b", "c")]
    try:
        er.run_sweep(
            pipeline_factory=lambda cfg: _make_pipeline(),
            configs=configs,
            summarize=_identity_summarize,
            output_dir=Path("out_test"),
        )
    except RuntimeError as e:
        assert "b" in str(e)
        assert [call["name"] for call in mock.calls] == ["a", "b"]
        return
    raise AssertionError("expected RuntimeError, none raised")


def test_invalid_on_error_rejected_at_construction():
    """
    on_error must be 'continue' or 'fail'; anything else raises at
    __init__ time, not at the first run.

    Mutation caught: invalid value silently accepted.
    """
    for bad in ("ignore", "raise", "", None, 0):
        try:
            ExperimentRunner(
                runner_factory=lambda sinks: _MockRunner(),
                sinks_factory=lambda cfg: {"session": InMemorySink()},
                on_error=bad,
            )
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for on_error={bad!r}")


def test_non_callable_runner_factory_rejected():
    """
    runner_factory must be callable. Passing an IRunner instance
    directly (the natural mistake, since the parameter used to be
    ``runner``) is caught here rather than at the first config.

    Mutation caught: TypeError check dropped, so the failure surfaces
    as a confusing not-callable error mid-sweep.
    """
    try:
        ExperimentRunner(
            _MockRunner(),  # type: ignore[arg-type]
            sinks_factory=lambda cfg: {"session": InMemorySink()},
        )
    except TypeError:
        return
    raise AssertionError("expected TypeError for non-callable runner_factory")


def test_non_callable_sinks_factory_rejected():
    """
    sinks_factory must be callable. A Mapping passed by mistake (the
    natural mistake, since a sink container is a dict) is caught here
    rather than at the first config.

    Mutation caught: TypeError check dropped, so the failure surfaces
    as a confusing not-callable error mid-sweep.
    """
    try:
        ExperimentRunner(
            runner_factory=lambda sinks: _MockRunner(),
            sinks_factory={"session": InMemorySink()},  # type: ignore[arg-type]
        )
    except TypeError:
        return
    raise AssertionError("expected TypeError for non-callable sinks_factory")


# ======================================================================
# Summary contents: what the runner copies from the run
# ======================================================================


class _DiagMock:
    """Returns a Context whose Diagnostics already hold known messages."""

    def __init__(self):
        self.output_dirs = []

    def run(
        self,
        pipeline,
        *,
        name,
        params=None,
        output_dir="out",
        dt=1.0,
        max_steps,
        initial_features=None,
    ):
        self.output_dirs.append(output_dir)
        diag = Diagnostics()
        diag.error(f"err1-{name}")
        diag.error(f"err2-{name}")
        diag.warn(f"warn1-{name}")
        diag.warn(f"warn2-{name}")
        return Context(
            run=RunContext(name=name, output_dir=Path(output_dir)),
            params=Params(params),
            sim=SimContext(dt=dt),
            data=FeatureBag(),
            log=LogContext(sinks={}),
            diag=diag,
        )


def test_run_diagnostics_copied_into_summary():
    """
    A run that completes with errors and warnings in ctx.diag reports
    them in its summary, per run, as tuples. crashed stays False.

    Mutation caught: errors or warnings dropped on the success path
    (a sweep would then report a run with recorded errors as clean).
    """
    mock = _DiagMock()
    er = ExperimentRunner(
        runner_factory=lambda sinks: mock,
        sinks_factory=lambda cfg: {"session": InMemorySink()},
    )
    result = er.run_sweep(
        pipeline_factory=lambda cfg: _make_pipeline(),
        configs=[ExperimentConfig(name="a"), ExperimentConfig(name="b")],
        summarize=_identity_summarize,
        output_dir=Path("out_test"),
    )
    assert [s.errors for s in result] == [("err1-a", "err2-a"), ("err1-b", "err2-b")]
    assert [s.warnings for s in result] == [("warn1-a", "warn2-a"), ("warn1-b", "warn2-b")]
    assert all(s.crashed is False for s in result)


def test_output_dir_forwarded_to_runner():
    """
    run_sweep's output_dir reaches IRunner.run(output_dir=...) for every
    config, as a Path, whether it was passed as a str or a Path.

    Mutation caught: output_dir dropped (the runner falls back to its
    own default directory, and the sweep's files land elsewhere).
    """
    for given in ("sweep_dir_x", Path("sweep_dir_x")):
        mock = _DiagMock()
        er = ExperimentRunner(
            runner_factory=lambda sinks: mock,
            sinks_factory=lambda cfg: {"session": InMemorySink()},
        )
        er.run_sweep(
            pipeline_factory=lambda cfg: _make_pipeline(),
            configs=[ExperimentConfig(name="a"), ExperimentConfig(name="b")],
            summarize=_identity_summarize,
            output_dir=given,
        )
        assert mock.output_dirs == [Path("sweep_dir_x"), Path("sweep_dir_x")]
        assert all(isinstance(d, Path) for d in mock.output_dirs), mock.output_dirs


def test_crashed_summary_echoes_config():
    """
    A crashed run's summary still carries its params, so a crashed row
    can be traced to the configuration that produced it.

    Mutation caught: the crash branch recording an empty config.
    """
    mock = _MockRunner(crash_on_name="b")
    er = ExperimentRunner(
        runner_factory=lambda sinks: mock,
        sinks_factory=lambda cfg: {"session": InMemorySink()},
    )
    result = er.run_sweep(
        pipeline_factory=lambda cfg: _make_pipeline(),
        configs=[
            ExperimentConfig(name="a", params={"K": 3}),
            ExperimentConfig(name="b", params={"K": 7}),
        ],
        summarize=_identity_summarize,
        output_dir=Path("out_test"),
    )
    assert [s.crashed for s in result] == [False, True]
    assert [s.config for s in result] == [{"K": 3}, {"K": 7}]


def test_non_mapping_summarize_is_a_run_failure():
    """
    summarize must return a Mapping. None, a list of pairs and a string
    are each a crashed row under on_error='continue' and a TypeError
    under on_error='fail', as the run_sweep docstring states.

    Mutation caught: the Mapping check dropped, so a list of pairs or an
    empty string reads as a successful run (dict() accepts both).
    """
    for bad, policy in [(b, p) for b in (None, [("a", 1)], "") for p in ("continue", "fail")]:
        er = ExperimentRunner(
            runner_factory=lambda sinks: _MockRunner(),
            sinks_factory=lambda cfg: {"session": InMemorySink()},
            on_error=policy,
        )
        try:
            result = er.run_sweep(
                pipeline_factory=lambda cfg: _make_pipeline(),
                configs=[ExperimentConfig(name="a")],
                summarize=lambda ctx, bad=bad: bad,
                output_dir=Path("out_test"),
            )
        except TypeError:
            assert policy == "fail"
            continue
        assert policy == "continue", "on_error='fail' must raise TypeError"
        assert result[0].crashed is True
        assert any("TypeError" in e for e in result[0].errors)


# ======================================================================
# Runner
# ======================================================================


def main() -> int:
    tests = [
        test_config_defaults,
        test_config_is_frozen,
        test_summary_defaults,
        test_empty_config_list_returns_empty,
        test_three_configs_produce_three_summaries_in_order,
        test_pipeline_and_sinks_factories_called_once_per_config,
        test_runner_factory_called_once_per_config,
        test_initial_features_forwarded_to_runner,
        test_params_forwarded_to_runner,
        test_on_error_continue_records_crash_and_keeps_going,
        test_on_error_fail_stops_at_first_crash,
        test_invalid_on_error_rejected_at_construction,
        test_non_callable_runner_factory_rejected,
        test_non_callable_sinks_factory_rejected,
        test_run_diagnostics_copied_into_summary,
        test_output_dir_forwarded_to_runner,
        test_crashed_summary_echoes_config,
        test_non_mapping_summarize_is_a_run_failure,
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
