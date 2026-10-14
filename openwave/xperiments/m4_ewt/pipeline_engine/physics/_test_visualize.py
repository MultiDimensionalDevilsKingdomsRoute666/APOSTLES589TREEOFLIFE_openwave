"""
Tests for the visualization processor base classes.

WindowedProcessor's hooks are tested with a mock render module, so
nothing touches a real window. TaichiWindowProcessor is not tested
here (its window cannot be opened headless; its behaviour is
exercised by the _demo_ scripts that a human runs).

Run from the project root:
    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._test_visualize
"""

import sys
import traceback

import taichi as ti

from .allocator import AllocateWaveField
from .features import WaveGrid
from .visualize import WindowedProcessor
from ..pipeline import ErrorPolicy, Pipeline, Stage
from ..runner import Runner
from ..sinks import InMemorySink


_TI_INITIALIZED = False


def _ti_init():
    global _TI_INITIALIZED
    if not _TI_INITIALIZED:
        ti.init(arch=ti.cpu, log_level=ti.ERROR)
        _TI_INITIALIZED = True


# ======================================================================
# Mock render
# ======================================================================


class _FakeWindow:
    def __init__(self):
        self.running = True
        self.pressed = set()

    def is_pressed(self, key):
        return key in self.pressed


class _FakeRender:
    """Records calls to init_UI, init_scene, show_scene. No real window."""

    def __init__(self):
        self.window = _FakeWindow()
        self.calls = []

    def init_UI(self, universe_size, tick_spacing, cam):
        self.calls.append(
            ("init_UI", tuple(universe_size), float(tick_spacing), tuple(cam))
        )

    def init_scene(self, show_axis):
        self.calls.append(("init_scene", bool(show_axis)))

    def show_scene(self):
        self.calls.append(("show_scene",))


# ======================================================================
# Test subclasses
# ======================================================================


class _Tracking(WindowedProcessor):
    """Counts setup_scene and draw calls. Never draws anything."""

    name = "Tracking"
    requires = (WaveGrid,)
    stateless = False   # history counters on the instance

    def __init__(self, **kw):
        super().__init__(**kw)
        self.setup_calls = 0
        self.draw_calls = 0

    def setup_scene(self, ctx):
        self.setup_calls += 1

    def draw(self, ctx):
        self.draw_calls += 1


class _Static(WindowedProcessor):
    """Both hooks are no-ops. No instance mutation."""

    name = "Static"
    requires = (WaveGrid,)

    def setup_scene(self, ctx):
        pass

    def draw(self, ctx):
        pass


class _Pipeline(Pipeline):
    def __init__(self, proc):
        super().__init__(error_policy=ErrorPolicy.FAIL_FAST)
        self.add(AllocateWaveField(nx=8, ny=8, nz=8, dx=1.0))
        self.add(proc)


def _run(pipeline, max_steps=3, check_stateless=False):
    return Runner({"session": InMemorySink()}, check_stateless=check_stateless).run(
        pipeline,
        name="viz_test",
        params={},
        dt=0.1,
        max_steps=max_steps,
    )


# ======================================================================
# Defaults
# ======================================================================


def test_defaults():
    """
    Every optional kwarg has a documented default.

    Mutation caught: a default changed silently (cam, universe_size,
    tick_spacing, show_axis), which would affect every subclass that
    does not override them.
    """
    p = WindowedProcessor(render_module=_FakeRender())
    assert p.cam == [2.5, 2.0, 2.5]
    assert p.universe_size == [1.0, 1.0, 1.0]
    assert p.tick_spacing == 0.25
    assert p.show_axis is False
    assert p.stage is Stage.MEASURE
    assert p.order == 2000


# ======================================================================
# setup
# ======================================================================


def test_setup_calls_init_ui_and_setup_scene():
    """
    setup() calls render.init_UI once with the instance config, then
    calls the subclass's setup_scene exactly once.

    Mutation caught: init_UI dropped, called with wrong arguments, or
    setup_scene not invoked.
    """
    _ti_init()
    fake = _FakeRender()
    proc = _Tracking(cam=(1.0, 2.0, 3.0), render_module=fake)
    ctx = _run(_Pipeline(proc), max_steps=0)

    assert ctx.diag.errors == [], ctx.diag.errors
    assert proc.setup_calls == 1
    assert proc.draw_calls == 0
    init_ui_calls = [c for c in fake.calls if c[0] == "init_UI"]
    assert len(init_ui_calls) == 1
    assert init_ui_calls[0][1] == (1.0, 1.0, 1.0)
    assert init_ui_calls[0][2] == 0.25
    assert init_ui_calls[0][3] == (1.0, 2.0, 3.0)


def test_setup_scene_not_overridden_raises():
    """
    Direct call to the base hook raises NotImplementedError.

    Mutation caught: the base hook turned into a no-op, which would let
    a subclass that forgot to override it silently do nothing.
    """
    base = WindowedProcessor(render_module=_FakeRender())
    try:
        base.setup_scene(None)
    except NotImplementedError:
        return
    raise AssertionError("expected NotImplementedError")


# ======================================================================
# process: normal path
# ======================================================================


def test_process_normal_path_calls_init_scene_draw_show():
    """
    process() with a running window and no ESC: init_scene(show_axis),
    then draw(), then show_scene(), in that order, per step.

    Mutation caught: init_scene or show_scene dropped, called in the
    wrong order, or draw called before init_scene.
    """
    _ti_init()
    fake = _FakeRender()
    proc = _Tracking(render_module=fake)
    ctx = _run(_Pipeline(proc), max_steps=3)

    assert ctx.diag.errors == [], ctx.diag.errors
    assert proc.draw_calls == 3
    sequence = [c[0] for c in fake.calls if c[0] in ("init_scene", "show_scene")]
    assert sequence == ["init_scene", "show_scene"] * 3


def test_process_passes_show_axis_flag():
    """
    The show_axis flag passed to init_scene() matches the instance.

    Mutation caught: hard-coded False, or the flag dropped.
    """
    _ti_init()
    fake = _FakeRender()
    proc = _Tracking(show_axis=True, render_module=fake)
    _run(_Pipeline(proc), max_steps=1)

    init_scene_calls = [c for c in fake.calls if c[0] == "init_scene"]
    assert len(init_scene_calls) == 1
    assert init_scene_calls[0][1] is True


# ======================================================================
# process: stop conditions
# ======================================================================


def test_process_stops_when_window_closed():
    """
    window.running == False: should_stop set, draw not called,
    show_scene not called.

    Mutation caught: the running check dropped, so a closed window
    keeps drawing into a dead canvas.
    """
    _ti_init()
    fake = _FakeRender()
    fake.window.running = False
    proc = _Tracking(render_module=fake)
    ctx = _run(_Pipeline(proc), max_steps=2)

    assert proc.draw_calls == 0
    assert ctx.sim.should_stop is True
    assert not any(c[0] == "show_scene" for c in fake.calls)


def test_process_stops_on_escape():
    """
    ESC pressed: should_stop set, draw not called.

    Mutation caught: the ESC branch dropped.
    """
    _ti_init()
    fake = _FakeRender()
    fake.window.pressed.add(ti.ui.ESCAPE)
    proc = _Tracking(render_module=fake)
    ctx = _run(_Pipeline(proc), max_steps=2)

    assert proc.draw_calls == 0
    assert ctx.sim.should_stop is True


def test_draw_not_overridden_raises():
    """
    Direct call to the base draw hook raises NotImplementedError.

    Mutation caught: the base hook turned into a no-op.
    """
    base = WindowedProcessor(render_module=_FakeRender())
    try:
        base.draw(None)
    except NotImplementedError:
        return
    raise AssertionError("expected NotImplementedError")


# ======================================================================
# Stateless guard
# ======================================================================


def test_stateless_guard_passes():
    """
    A subclass that holds no mutable state passes the stateless guard
    with check_stateless=True.

    Mutation caught: WindowedProcessor storing something on the
    instance inside process() (e.g. a counter), which would break the
    guard for every subclass at once.
    """
    _ti_init()
    fake = _FakeRender()
    proc = _Static(render_module=fake)
    ctx = _run(_Pipeline(proc), max_steps=2, check_stateless=True)
    assert ctx.diag.errors == [], ctx.diag.errors


# ======================================================================
# Runner
# ======================================================================


def main() -> int:
    tests = [
        test_defaults,
        test_setup_calls_init_ui_and_setup_scene,
        test_setup_scene_not_overridden_raises,
        test_process_normal_path_calls_init_scene_draw_show,
        test_process_passes_show_axis_flag,
        test_process_stops_when_window_closed,
        test_process_stops_on_escape,
        test_draw_not_overridden_raises,
        test_stateless_guard_passes,
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