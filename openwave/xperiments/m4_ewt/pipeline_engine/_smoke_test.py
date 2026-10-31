"""
Smoke test for the pipeline engine. No Taichi, no physics.

Run from the OpenWave root:
    python -m openwave.xperiments.m4_ewt.pipeline_engine._smoke_test

or from inside the folder:
    python _smoke_test.py
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

try:
    from . import (
        BaseProcessor,
        Context,
        ErrorPolicy,
        InMemorySink,
        JsonSessionSink,
        LiveJsonSink,
        LogProcessor,
        Pipeline,
        PipelineError,
        Runner,
        Stage,
    )
    from .physics.units import NaturalUnitSystem
except ImportError:
    from context import Context
    from pipeline import BaseProcessor, ErrorPolicy, Pipeline, PipelineError, Stage
    from sinks import InMemorySink, JsonSessionSink, LiveJsonSink
    from loggers import LogProcessor
    from runner import Runner

    try:
        from physics.units import NaturalUnitSystem
    except ImportError:
        from openwave.xperiments.m4_ewt.pipeline_engine.physics.units import NaturalUnitSystem


# ================================================================
# Data features (runtime state lives in ctx.data)
# ================================================================


@dataclass
class Counter:
    value: int = 0


@dataclass
class History:
    values: list = field(default_factory=list)


@dataclass
class Tags:
    """Provided by the caller via initial_features; not by any processor."""

    label: str = ""


# ================================================================
# Processors
# ================================================================


class AllocateState(BaseProcessor):
    name = "AllocateState"
    stage = None
    order = 10
    provides = (Counter, History)

    def setup(self, ctx: Context) -> None:
        ctx.data.set(Counter())
        ctx.data.set(History())


class Increment(BaseProcessor):
    name = "Increment"
    stage = Stage.UPDATE
    order = 10
    requires = (Counter,)

    def process(self, ctx: Context) -> None:
        ctx.data.require(Counter).value += 1


class RecordValue(BaseProcessor):
    name = "RecordValue"
    stage = Stage.MEASURE
    order = 10
    requires = (Counter, History)

    def process(self, ctx: Context) -> None:
        c = ctx.data.require(Counter)
        h = ctx.data.require(History)
        h.values.append(float(c.value % 7))


class ReadExternal(BaseProcessor):
    """Reads a feature provided by the caller (Tags). Fails validation if absent."""

    name = "ReadExternal"
    stage = Stage.MEASURE
    order = 5
    requires = (Tags,)
    provides = ()

    def process(self, ctx: Context) -> None:
        # Read-only demo: pull the tag, do nothing with it here.
        _ = ctx.data.require(Tags).label


class BadProcessor(BaseProcessor):
    """Forces a failure to demonstrate ErrorPolicy.SOFT_STOP."""

    name = "BadProcessor"
    stage = Stage.UPDATE
    order = 90

    def process(self, ctx: Context) -> None:
        raise RuntimeError("intentional failure")


# ================================================================
# Pipelines
# ================================================================


def _payload(ctx: Context) -> Mapping[str, Any]:
    c = ctx.data.require(Counter)
    h = ctx.data.require(History)
    return {
        "counter": c.value,
        "last": h.values[-1] if h.values else 0.0,
        "history_len": len(h.values),
    }


class DemoPipeline(Pipeline):
    def __init__(self, *, inject_failure: bool = False) -> None:
        super().__init__(error_policy=ErrorPolicy.SOFT_STOP)
        self.add(AllocateState())
        self.add(Increment())
        if inject_failure:
            self.add(BadProcessor())
        self.add(RecordValue())
        self.add(LogProcessor("SessionLog", "session", _payload, every=10, order=50))
        self.add(LogProcessor("LiveLog", "live", _payload, every=1, order=60))


class ExternalFeaturePipeline(Pipeline):
    """Demonstrates external_provides + initial_features."""

    def __init__(self) -> None:
        super().__init__(
            error_policy=ErrorPolicy.SOFT_STOP,
            external_provides=(Tags,),
        )
        self.add(AllocateState())
        self.add(Increment())
        self.add(ReadExternal())
        self.add(RecordValue())
        self.add(LogProcessor("SessionLog", "session", _payload, every=10, order=50))


# ================================================================
# Helpers
# ================================================================


def _print_summary(label: str, ctx: Context) -> None:
    print(f"--- {label} ---")
    print(f"steps simulated : {ctx.sim.step}")
    print(f"counter         : {ctx.data.require(Counter).value}")
    print(f"errors          : {ctx.diag.errors}")
    print(f"warnings        : {ctx.diag.warnings}")
    slowest = sorted(
        ((k, sum(v) / len(v) * 1e6) for k, v in ctx.diag.timings.items()),
        key=lambda x: -x[1],
    )[:5]
    print("slowest operations (avg us):")
    for name, us in slowest:
        print(f"  {name:<28} {us:>10.2f}")
    print()


def _run_demo(*, inject_failure: bool, use_memory: bool, out_dir: Path) -> Context:
    sinks: dict = {}
    if use_memory:
        sinks["session"] = InMemorySink()
        sinks["live"] = InMemorySink()
    else:
        sinks["session"] = JsonSessionSink(out_dir / "session.json", flush_every=100)
        sinks["live"] = LiveJsonSink(out_dir / "live.json", history=200)

    pipeline = DemoPipeline(inject_failure=inject_failure)
    runner = Runner(sinks, check_stateless=True)

    return runner.run(
        pipeline,
        name="demo",
        params={"note": "engine-only demo", "amplitude": 1.0},
        output_dir=out_dir,
        dt=1.0,
        max_steps=200,
    )


def _run_external_feature(out_dir: Path) -> Context:
    sinks = {"session": InMemorySink()}
    pipeline = ExternalFeaturePipeline()
    runner = Runner(sinks, check_stateless=True)

    tags = Tags(label="external_demo")

    return runner.run(
        pipeline,
        name="external_feature_demo",
        params={"note": "external_provides demo"},
        output_dir=out_dir,
        dt=1.0,
        max_steps=50,
        initial_features=[tags, NaturalUnitSystem()],
    )


def test_stateless_guard() -> tuple[bool, str]:
    """Regression: in-place mutation of a stateless processor must be caught."""

    class InPlaceMutant(BaseProcessor):
        name = "InPlaceMutant"
        stage = Stage.UPDATE

        def __init__(self) -> None:
            self.hist: list[int] = []

        def process(self, ctx: Context) -> None:
            self.hist.append(ctx.sim.step)

    p = InPlaceMutant()
    runner = Runner({}, check_stateless=True)
    pipeline = Pipeline(error_policy=ErrorPolicy.FAIL_FAST).add(p)
    try:
        runner.run(
            pipeline, name="stateless_test", max_steps=5, initial_features=[NaturalUnitSystem()]
        )
    except PipelineError as e:
        if "mutated instance fields" in str(e):
            return True, "PipelineError raised on in-place mutation"
        return False, f"wrong PipelineError: {e}"
    except BaseException as e:
        return False, f"unexpected {type(e).__name__}: {e}"
    return False, "expected PipelineError, none raised"


def test_setup_failure() -> tuple[bool, str]:
    """Regression: setup failure must not leak PipelineStopSignal, and only
    processors whose setup() succeeded get torn down."""
    calls: list[str] = []

    def make(name: str, order: int, fail: bool = False) -> BaseProcessor:
        class P(BaseProcessor):
            stage = None

            def setup(self, ctx: Context) -> None:
                calls.append(f"{name}.setup")
                if fail:
                    raise RuntimeError("boom")

            def teardown(self, ctx: Context) -> None:
                calls.append(f"{name}.teardown")

        P.name = name
        P.order = order
        return P()

    pipeline = Pipeline()
    pipeline.add(make("A", 1))
    pipeline.add(make("B", 2, fail=True))
    pipeline.add(make("C", 3))

    runner = Runner({})
    try:
        runner.run(pipeline, name="setup_fail_test", max_steps=3)
    except RuntimeError as e:
        if str(e) != "boom":
            return False, f"wrong RuntimeError: {e}"
        expected = ["A.setup", "B.setup", "A.teardown"]
        if calls != expected:
            return False, f"call trace {calls} != {expected}"
        return True, "RuntimeError propagated, only A torn down"
    except BaseException as e:
        return False, f"wrong exception type: {type(e).__name__}: {e}"
    return False, "expected RuntimeError, none raised"


def test_initial_features_satisfy_base_class_requires() -> tuple[bool, str]:
    """Regression: Runner.run counts every base class of an initial_features
    instance as provided at build time, so a processor that requires a
    base class two levels up builds with no external_provides entry; and
    it re-validates on every run, so the same pipeline run again without
    the instance fails at build."""

    class BaseFeature:
        pass

    class MidFeature(BaseFeature):
        pass

    @dataclass
    class ConcreteFeature(MidFeature):
        label: str = "concrete"

    class NeedsBase(BaseProcessor):
        name = "NeedsBase"
        stage = Stage.UPDATE
        requires = (BaseFeature,)

        def process(self, ctx: Context) -> None:
            ctx.data.require(BaseFeature)

    pipeline = Pipeline(error_policy=ErrorPolicy.FAIL_FAST).add(NeedsBase())
    try:
        ctx = Runner({}).run(
            pipeline, name="mro_test", max_steps=3, initial_features=[ConcreteFeature()]
        )
    except BaseException as e:
        return False, f"unexpected {type(e).__name__}: {e}"
    if ctx.sim.step != 3 or ctx.diag.errors:
        return False, f"step {ctx.sim.step}, errors {ctx.diag.errors}"
    try:
        Runner({}).run(pipeline, name="mro_rerun_test", max_steps=3, initial_features=[])
    except PipelineError as e:
        if "BaseFeature" not in str(e):
            return False, f"wrong PipelineError on rerun: {e}"
        return True, "base-class requires satisfied two levels up; rerun re-validated"
    except BaseException as e:
        return False, f"unexpected {type(e).__name__} on rerun: {e}"
    return False, "rerun without the instance built; validation was not repeated"


def test_build_failure_opens_no_sink() -> tuple[bool, str]:
    """Regression: Runner.run validates the pipeline before opening any
    sink, so a build failure leaves no sink opened."""

    class Missing:
        pass

    class NeedsMissing(BaseProcessor):
        name = "NeedsMissing"
        stage = Stage.UPDATE
        requires = (Missing,)

        def process(self, ctx: Context) -> None:
            pass

    class RecordingSink(InMemorySink):
        def __init__(self) -> None:
            super().__init__()
            self.opened = 0

        def open(self, meta: Mapping[str, Any]) -> None:
            self.opened += 1
            super().open(meta)

    sink = RecordingSink()
    pipeline = Pipeline(error_policy=ErrorPolicy.FAIL_FAST).add(NeedsMissing())
    try:
        Runner({"session": sink}).run(pipeline, name="build_fail_test", max_steps=3)
    except PipelineError as e:
        if "Missing" not in str(e):
            return False, f"wrong PipelineError: {e}"
        if sink.opened:
            return False, f"sink opened {sink.opened} time(s) before the build failed"
        return True, "PipelineError raised before any sink opened"
    except BaseException as e:
        return False, f"unexpected {type(e).__name__}: {e}"
    return False, "expected PipelineError, none raised"


# ================================================================
# Entry point
# ================================================================


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "out_engine_smoke"

    print("=" * 64)
    print("Pipeline engine smoke test")
    print("=" * 64)
    print()

    # 1) Normal run, in-memory sinks
    ctx = _run_demo(inject_failure=False, use_memory=True, out_dir=out_dir)
    _print_summary("normal run (in-memory)", ctx)
    assert ctx.sim.step == 200, f"expected 200 steps, got {ctx.sim.step}"
    assert ctx.data.require(Counter).value == 200
    assert ctx.diag.errors == []

    # 2) Run with injected failure, in-memory sinks
    ctx = _run_demo(inject_failure=True, use_memory=True, out_dir=out_dir)
    _print_summary("failure run (in-memory)", ctx)
    assert ctx.sim.step == 1, f"expected 1 step, got {ctx.sim.step}"
    assert any("BadProcessor" in e for e in ctx.diag.errors)

    # 3) Normal run, file sinks
    ctx = _run_demo(inject_failure=False, use_memory=False, out_dir=out_dir)
    _print_summary("normal run (file sinks)", ctx)
    session_path = out_dir / "session.json"
    assert session_path.exists(), f"expected session log at {session_path}"
    print(f"session log written to: {session_path}")
    print()

    # 4) External feature run (external_provides + initial_features)
    ctx = _run_external_feature(out_dir)
    _print_summary("external feature run (in-memory)", ctx)
    assert ctx.sim.step == 50, f"expected 50 steps, got {ctx.sim.step}"
    assert ctx.diag.errors == []
    assert ctx.data.require(Tags).label == "external_demo"

    # 5) Stateless guard regression
    ok, msg = test_stateless_guard()
    print("--- stateless guard regression ---")
    print(f"result: {'PASS' if ok else 'FAIL'} ({msg})")
    assert ok, msg
    print()

    # 6) Setup failure regression
    ok, msg = test_setup_failure()
    print("--- setup failure regression ---")
    print(f"result: {'PASS' if ok else 'FAIL'} ({msg})")
    assert ok, msg
    print()

    # 7) Base-class requires satisfied by initial_features
    ok, msg = test_initial_features_satisfy_base_class_requires()
    print("--- initial_features MRO regression ---")
    print(f"result: {'PASS' if ok else 'FAIL'} ({msg})")
    assert ok, msg
    print()

    # 8) Build failure opens no sink
    ok, msg = test_build_failure_opens_no_sink()
    print("--- build-before-sinks regression ---")
    print(f"result: {'PASS' if ok else 'FAIL'} ({msg})")
    assert ok, msg
    print()

    print("=" * 64)
    print("SMOKE TEST PASSED")
    print("=" * 64)


if __name__ == "__main__":
    main()
