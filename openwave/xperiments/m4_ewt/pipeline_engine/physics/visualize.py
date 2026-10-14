"""
Interactive visualization processors.

Two flavors, different rendering layers:

    TaichiWindowProcessor -- 2D slice via ti.ui.Window's image canvas.
        Simple, no GGUI scene, one window per run.

    WindowedProcessor -- base class for GGUI 3D scenes via
        openwave.i_o.render. Subclasses override setup_scene(ctx) for
        one-time buffer setup and draw(ctx) for per-step drawing. The
        base handles the boilerplate: opening the window in setup(),
        checking window.running and ESC in process(), calling
        init_scene() before draw() and show_scene() after.

TaichiWindowProcessor cannot run headless. WindowedProcessor can, when
given a mock render module (used by its tests); with the real
openwave.i_o.render it opens a window and cannot.
"""

from pathlib import Path

from ..pipeline import BaseProcessor, Stage

import taichi as ti

from .features import PsiLongField, WaveGrid


class TaichiWindowProcessor(BaseProcessor):
    name = "TaichiWindow"
    stage = Stage.MEASURE
    order = 2000
    requires = (WaveGrid, PsiLongField)

    def __init__(
        self,
        size=(512, 512),
        scale=8,
        amp_scale=3.0,
        title="M4 wave demo",
        screenshot_every=0,
        screenshot_dir="out_demo",
    ):
        self.size = size
        self.scale = scale
        self.amp_scale = amp_scale
        self.title = title
        self.screenshot_every = screenshot_every
        self.screenshot_dir = Path(screenshot_dir)

    def setup(self, ctx) -> None:
        w, h = self.size
        self._img = ti.Vector.field(3, dtype=ti.f32, shape=(w, h))
        self._window = ti.ui.Window(self.title, (w, h))
        self._canvas = self._window.get_canvas()
        if self.screenshot_every > 0:
            self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def process(self, ctx) -> None:
        if not self._window.running:
            ctx.sim.should_stop = True
            return
        if self._window.is_pressed(ti.ui.ESCAPE):
            ctx.sim.should_stop = True
            return

        grid = ctx.data.require(WaveGrid)
        field = ctx.data.require(PsiLongField)
        w, h = self.size
        z = grid.nz // 2

        _render_slice(
            field.psi,
            self._img,
            grid.nx,
            grid.ny,
            z,
            w,
            h,
            self.scale,
            self.amp_scale,
        )
        self._canvas.set_image(self._img)
        self._window.show()

        if self.screenshot_every > 0 and ctx.sim.step % self.screenshot_every == 0:
            path = self.screenshot_dir / f"frame_{ctx.sim.step:06d}.png"
            self._window.save_image(str(path))

    def teardown(self, ctx) -> None:
        # Taichi handles window cleanup on process exit; nothing to do.
        pass


@ti.kernel
def _render_slice(
    psi: ti.template(),
    img: ti.template(),
    nx: ti.i32,
    ny: ti.i32,
    z: ti.i32,
    w: ti.i32,
    h: ti.i32,
    scale: ti.i32,
    amp: ti.f32,
):
    for px, py in ti.ndrange(w, h):
        i = px // scale
        j = py // scale
        if i < nx and j < ny:
            v = psi[i, j, z].norm() * amp
            v = ti.min(v, 1.0)
            # Simple blue -> red heatmap
            img[px, py] = ti.Vector([v, v * 0.4, 1.0 - v])
        else:
            img[px, py] = ti.Vector([0.0, 0.0, 0.0])


class WindowedProcessor(BaseProcessor):
    """
    Base class for GGUI 3D scene processors.

    Subclass contract:

        setup_scene(ctx)   allocate buffers, build static meshes.
                           Called once, by setup().
        draw(ctx)          draw the current step. Called by process()
                           after init_scene() and before show_scene().
                           Must not call show_scene().

    Neither hook is optional; a subclass that does not override one
    raises NotImplementedError at the point the hook is invoked.

    The base takes only what every scene needs: camera, universe size,
    tick spacing, and the show_axis flag. Everything else lives on the subclass.

    render_module is for tests: pass a mock to avoid calling the real
    openwave.i_o.render.init_UI in setup() (which opens a window).
    In production, leave it None; setup() imports the real module.
    """

    name = "WindowedProcessor"
    stage = Stage.MEASURE
    order = 2000

    def __init__(
        self,
        *,
        cam=(2.5, 2.0, 2.5),
        universe_size=(1.0, 1.0, 1.0),
        tick_spacing=0.25,
        show_axis=False,
        render_module=None,
    ):
        self.cam = list(cam)
        self.universe_size = list(universe_size)
        self.tick_spacing = float(tick_spacing)
        self.show_axis = bool(show_axis)
        self._render_module_override = render_module

    def setup(self, ctx) -> None:
        render = self._render_module_override
        if render is None:
            from openwave.i_o import render as _render

            render = _render
        self._render = render
        render.init_UI(self.universe_size, self.tick_spacing, self.cam)
        self.setup_scene(ctx)

    def process(self, ctx) -> None:
        if not self._render.window.running:
            ctx.sim.should_stop = True
            return
        if self._render.window.is_pressed(ti.ui.ESCAPE):
            ctx.sim.should_stop = True
            return
        self._render.init_scene(self.show_axis)
        self.draw(ctx)
        self._render.show_scene()

    def setup_scene(self, ctx) -> None:
        """One-time hook. Override in subclasses."""
        raise NotImplementedError(f"{type(self).__name__} must implement setup_scene(ctx)")

    def draw(self, ctx) -> None:
        """Per-step hook. Override in subclasses."""
        raise NotImplementedError(f"{type(self).__name__} must implement draw(ctx)")
