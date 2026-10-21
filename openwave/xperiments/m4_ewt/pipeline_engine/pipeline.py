"""
Pipeline, stages, and the processor contract.

Contains:
    Stage             -- PRE_UPDATE, UPDATE, POST_UPDATE, MEASURE
    ErrorPolicy       -- FAIL_FAST, SOFT_STOP, CONTINUE
    PipelineStopSignal -- internal, used by SOFT_STOP
    PipelineError     -- raised on graph validation failure
    IProcessor        -- the processor protocol
    BaseProcessor     -- convenience base
    Pipeline          -- staged processor list with validation and error policy
"""

from __future__ import annotations

import time
from enum import Enum, auto
from typing import Callable, Protocol, runtime_checkable

from .context import Context

# ================================================================
# Stage and error policy
# ================================================================


class Stage(Enum):
    PRE_UPDATE = auto()
    UPDATE = auto()
    POST_UPDATE = auto()
    MEASURE = auto()


class ErrorPolicy(Enum):
    FAIL_FAST = auto()  # re-raise, stop the run immediately
    SOFT_STOP = auto()  # log, set should_stop, teardown, do not re-raise
    CONTINUE = auto()  # log, keep going with the next processor


class PipelineStopSignal(Exception):
    """Internal signal used by SOFT_STOP. Never escapes Pipeline.step()."""


class PipelineError(RuntimeError):
    """Raised on pipeline construction or validation failures."""


# ================================================================
# Processor
# ================================================================


@runtime_checkable
class IProcessor(Protocol):
    """
    Stateless processor. Configuration in __init__; runtime state in ctx.data.

    stage=None means lifecycle-only: only setup/teardown are called.
    stateless=False opts out of the stateless enforcement in Pipeline._safe.
    """

    name: str
    stage: Stage | None
    order: int
    requires: tuple[type, ...]
    provides: tuple[type, ...]
    stateless: bool

    def setup(self, ctx: Context) -> None: ...
    def process(self, ctx: Context) -> None: ...
    def teardown(self, ctx: Context) -> None: ...


class BaseProcessor:
    """Convenience base. Override what you need."""

    name: str = "BaseProcessor"
    stage: Stage | None = None
    order: int = 0
    requires: tuple[type, ...] = ()
    provides: tuple[type, ...] = ()
    stateless: bool = True

    def setup(self, ctx: Context) -> None:
        pass

    def process(self, ctx: Context) -> None:
        pass

    def teardown(self, ctx: Context) -> None:
        pass


# ================================================================
# Pipeline
# ================================================================


class Pipeline:
    """
    Staged processor list.

    build()    validates the requires/provides graph.
    setup()    runs all processors' setup(); on failure, tears down the ones
               that succeeded and propagates the original exception.
    step()     runs the four stages in order.
    teardown() tears down, in reverse, only processors whose setup()
               succeeded. Idempotent.
    """

    def __init__(
        self,
        *,
        error_policy: ErrorPolicy = ErrorPolicy.SOFT_STOP,
        external_provides: tuple[type, ...] = (),
    ) -> None:
        self._all: list[IProcessor] = []
        self._by_stage: dict[Stage, list[IProcessor]] = {s: [] for s in Stage}
        self._built = False
        self._error_policy = error_policy
        self._external_provides = external_provides
        self._check_stateless = False
        self._setup_done: list[IProcessor] = []

    def enable_stateless_check(self) -> None:
        """Enable the stateless guard. Called by Runner when check_stateless=True."""
        self._check_stateless = True

    # --- Builder ---

    def add(self, p: IProcessor) -> "Pipeline":
        self._all.append(p)
        if p.stage is not None:
            self._by_stage[p.stage].append(p)
        self._built = False
        return self

    # --- Validation ---

    def build(self, extra_provides: tuple[type, ...] = ()) -> None:
        """
        Sort processors and validate the requires/provides graph.

        `extra_provides` lists feature classes that the caller has
        promised to supply through `initial_features`. `Runner.run()`
        passes the MRO expansion of `initial_features` here, so a
        feature passed as an instance satisfies a processor's requires
        without a matching entry in `external_provides`. A direct
        caller (a test that only inspects `_all` after build) can call
        this with no arguments; validation then sees only
        `external_provides` and processor `provides`.
        """
        self._all.sort(key=lambda p: p.order)
        for s in Stage:
            self._by_stage[s].sort(key=lambda p: p.order)
        self._validate(extra_provides)
        self._built = True

    def _validate(self, extra_provides: tuple[type, ...] = ()) -> None:
        """
        Check every processor's `requires` against the union of three
        sources: `external_provides`, `extra_provides` (the MRO
        expansion of `initial_features`, passed by `Runner.run`), and
        the `provides` of every processor that has already run.

        A `requires` entry not satisfied by any of the three raises
        `PipelineError` at build, not at the first `require()` inside
        a processor's `process()`. A feature that is declared (either
        via `external_provides` or by being in `initial_features`) but
        never actually written to `ctx.data` still raises `KeyError`
        at first use -- that is the "declaration, not check" half, and
        it remains.
        """
        available: set[type] = set(self._external_provides) | set(extra_provides)
        # Lifecycle-only processors first, in global order.
        for p in self._all:
            if p.stage is None:
                self._check_requires(p, available)
                available.update(p.provides)
        # Then per-stage, in stage order.
        for stage in Stage:
            for p in self._by_stage[stage]:
                self._check_requires(p, available)
                available.update(p.provides)

    @staticmethod
    def _check_requires(p: IProcessor, available: set[type]) -> None:
        for r in p.requires:
            if r not in available:
                raise PipelineError(
                    f"{p.name}: requires '{r.__name__}', " f"not provided by any earlier processor"
                )

    # --- Lifecycle ---

    def setup(self, ctx: Context) -> None:
        if not self._built:
            self.build()
        self._setup_done = []
        try:
            for p in self._all:
                self._safe(lambda p=p: p.setup(ctx), p, "setup", ctx, is_lifecycle=True)
                self._setup_done.append(p)
        except BaseException:
            self._teardown_completed(ctx)
            raise

    def step(self, ctx: Context) -> None:
        stopped = False
        try:
            for stage in Stage:
                for p in self._by_stage[stage]:
                    self._safe(lambda p=p: p.process(ctx), p, "process", ctx)
                    if ctx.sim.should_stop:
                        stopped = True
                        break
                if stopped:
                    break
        except PipelineStopSignal:
            ctx.sim.should_stop = True
        # Advance the clock exactly once, regardless of how the step ended.
        ctx.sim.step += 1
        ctx.sim.t += ctx.sim.dt

    def teardown(self, ctx: Context) -> None:
        self._teardown_completed(ctx)

    def _teardown_completed(self, ctx: Context) -> None:
        """
        Tear down, in reverse, only processors whose setup() succeeded.

        Idempotent: clearing the list makes a second call a no-op. This is
        what allows Runner's finally to call teardown after a failed setup
        without double-tearing anything.
        """
        for p in reversed(self._setup_done):
            try:
                p.teardown(ctx)
            except Exception as e:
                ctx.diag.error(f"{p.name}.teardown: {type(e).__name__}: {e}")
        self._setup_done = []

    # --- Error handling and stateless enforcement ---

    def _safe(
        self,
        fn: Callable[[], None],
        p: IProcessor,
        op: str,
        ctx: Context,
        *,
        is_lifecycle: bool = False,
    ) -> None:
        t0 = time.perf_counter()
        try:
            if op == "process" and self._check_stateless and getattr(p, "stateless", True):
                self._stateless_guard(fn, p)
            else:
                fn()
        except PipelineStopSignal:
            raise
        except Exception as e:
            msg = f"{p.name}.{op}: {type(e).__name__}: {e}"
            ctx.diag.error(msg)
            if is_lifecycle:
                # Setup is not subject to ErrorPolicy: either the whole run
                # can start, or it cannot. Propagate the original exception.
                raise
            if self._error_policy is ErrorPolicy.FAIL_FAST:
                raise
            if self._error_policy is ErrorPolicy.CONTINUE and op == "process":
                return
            raise PipelineStopSignal(msg) from e
        finally:
            ctx.diag.time(f"{p.name}.{op}", time.perf_counter() - t0)

    @staticmethod
    def _field_snapshot(p: IProcessor) -> dict[str, str]:
        return {k: repr(v) for k, v in p.__dict__.items()}

    @staticmethod
    def _stateless_guard(fn: Callable[[], None], p: IProcessor) -> None:
        """
        Detect any change to instance fields during fn().

        Compares repr() of each field, not id(). id() catches rebinding
        (self.x = new) but misses in-place mutation (self.hist.append).
        repr() catches both: the repr of a list, dict, or dataclass reflects
        its contents, and the repr of an opaque object (Taichi handles,
        files) is stable, so no false positives on Taichi resources.

        Only runs when check_stateless is enabled, so the extra cost is opt-in.
        """
        before = Pipeline._field_snapshot(p)
        fn()
        after = Pipeline._field_snapshot(p)
        changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        if changed:
            raise PipelineError(
                f"{p.name}: mutated instance fields in process(): {changed}. "
                f"Runtime state must live in ctx.data. "
                f"Set `stateless = False` if memoization is required."
            )
