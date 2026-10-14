"""
Runnable demo: K=10 golden-angle field as a wireframe xy mesh.

One xy plane at z = nz//2, vertices displaced along +z by |psi|
normalized to the current peak times --warp, drawn as a wireframe
instead of filled triangles. Colour from an orange gradient (or
ironbow / blueprint via --wave-menu).

This is the classic OpenWave flux-mesh look, on the pipeline_engine
substrate. It runs the same pipeline as _demo_k_sweep but is not a
sweep: one config, one window, interactive only.

The rendering base class (WindowedProcessor) handles the window
lifecycle; this module supplies setup_scene(ctx) and draw(ctx).

Run:
    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo_k10_wireframe

Options:
    --grid 64              grid size per axis
    --stride 1             mesh subsample (1 = every voxel)
    --warp 0.3             peak displacement, fraction of the domain
    --cam 2.0 2.5 2.0      camera position
    --wave-menu 1          1=orange, 2=ironbow, 3=blueprint

Not a test: this module opens a Taichi GGUI window and blocks until
you close it. It is not part of the CI test list and cannot be run
headless.

Note: no `from __future__ import annotations` here. Taichi kernel
definitions need live type objects.
"""

import argparse
from pathlib import Path

import numpy as np
import taichi as ti

from ..pipeline import ErrorPolicy, Pipeline
from ..runner import Runner
from ..sinks import InMemorySink

from .allocator import AllocateWaveField
from .seed import SeedMultiCenter
from .evolution import (
    ClearAccelerationProcessor,
    LaplacianProcessor,
    LeapfrogProcessor,
)
from .boundary import BoundaryProcessor
from .motion import NoOpRule, WCMotionProcessor
from .stability import StabilityMetricsUpdate
from .visualize import WindowedProcessor
from .features import (
    BoundaryCondition,
    PsiLongField,
    StabilityMetrics,
    WaveGrid,
)
from .units import NaturalUnitSystem, UnitSystem
from .wc_factory import build_wc_state
from .wc_types import WCState
from ..utils.viz_utils import find_peak, gradient_color, mesh_indices

_WAVELENGTH = 12.0
_SPACING = 12.0
_TOPOLOGY = "golden"
_K = 10
_DT = 0.2



# ======================================================================
# Kernels
# ======================================================================


@ti.kernel
def _warp_xy_plane(
    psi: ti.template(),
    verts: ti.template(),
    colors: ti.template(),
    k_fixed: ti.i32,
    nx: ti.i32,
    ny: ti.i32,
    mx: ti.i32,
    my: ti.i32,
    stride: ti.i32,
    max_dim: ti.f32,
    warp: ti.f32,
    inv_peak: ti.f32,
    wave_menu: ti.i32,
):
    for mi, mj in ti.ndrange(mx, my):
        i = mi * stride
        j = mj * stride
        a = psi[i, j, k_fixed].norm()
        z_base = ti.cast(k_fixed, ti.f32) / max_dim
        verts[mi * my + mj] = ti.Vector([
            ti.cast(i, ti.f32) / max_dim,
            ti.cast(j, ti.f32) / max_dim,
            z_base + a * inv_peak * warp,
        ])
        colors[mi * my + mj] = gradient_color(a * inv_peak, wave_menu)


# ======================================================================
# Processor
# ======================================================================


class WireframeViz(WindowedProcessor):
    """
    Single xy plane at z = nz//2, warped by |psi|, drawn as wireframe.

    setup_scene allocates the mesh buffers; draw refreshes vertices and
    colours from the field, then issues one scene.mesh call. The window
    lifecycle is the base class's.
    """

    name = "WireframeViz"
    requires = (WaveGrid, PsiLongField)

    def __init__(self, *, cam=(2.0, 2.5, 2.0), stride=1, warp=0.3, wave_menu=1):
        super().__init__(cam=cam)
        self.stride = max(1, int(stride))
        self.warp = float(warp)
        self.wave_menu = int(wave_menu)

    def setup_scene(self, ctx):
        grid = ctx.data.require(WaveGrid)
        nx, ny, nz = grid.nx, grid.ny, grid.nz
        s = self.stride
        mx = len(range(0, nx, s))
        my = len(range(0, ny, s))
        self._mx, self._my = mx, my
        self._stride = s
        self._max_dim = float(max(nx, ny, nz))
        self._k_fixed = nz // 2

        self._verts = ti.Vector.field(3, dtype=ti.f32, shape=(mx * my,))
        self._cols = ti.Vector.field(3, dtype=ti.f32, shape=(mx * my,))
        idx_np = mesh_indices(mx, my)
        self._idx = ti.field(dtype=ti.i32, shape=(idx_np.size,))
        self._idx.from_numpy(idx_np)
        self._peak = ti.field(dtype=ti.f32, shape=())

    def draw(self, ctx):
        grid = ctx.data.require(WaveGrid)
        field = ctx.data.require(PsiLongField)

        self._peak[None] = 1e-12
        find_peak(field.psi, self._peak, grid.nx, grid.ny, grid.nz)
        inv_peak = 1.0 / float(self._peak[None])

        _warp_xy_plane(
            field.psi, self._verts, self._cols,
            self._k_fixed,
            grid.nx, grid.ny,
            self._mx, self._my, self._stride,
            self._max_dim, self.warp, inv_peak, self.wave_menu,
        )

        try:
            self._render.scene.mesh(
                self._verts,
                indices=self._idx,
                per_vertex_color=self._cols,
                show_wireframe=True,
            )
        except TypeError:
            self._render.scene.mesh(
                self._verts,
                indices=self._idx,
                per_vertex_color=self._cols,
            )


# ======================================================================
# Pipeline
# ======================================================================


class K10VizPipeline(Pipeline):
    def __init__(self, *, grid, cam, stride, warp, wave_menu):
        super().__init__(
            error_policy=ErrorPolicy.FAIL_FAST,
            external_provides=(UnitSystem, BoundaryCondition, WCState),
        )
        self.add(AllocateWaveField(nx=grid, ny=grid, nz=grid, dx=1.0))
        self.add(SeedMultiCenter(radius=4.0))
        self.add(ClearAccelerationProcessor())
        self.add(LaplacianProcessor())
        self.add(LeapfrogProcessor())
        self.add(BoundaryProcessor(field_type=PsiLongField))
        self.add(WCMotionProcessor(rule=NoOpRule()))
        self.add(StabilityMetricsUpdate(localization_threshold=0.5))
        self.add(WireframeViz(cam=cam, stride=stride, warp=warp, wave_menu=wave_menu))


def main() -> None:
    p = argparse.ArgumentParser(description="M4 golden K=10 wireframe viz")
    p.add_argument("--grid", type=int, default=64)
    p.add_argument("--steps", type=int, default=1_000_000)
    p.add_argument("--cam", type=float, nargs=3, default=[2.0, 2.5, 2.0])
    p.add_argument("--stride", type=int, default=1)
    p.add_argument("--warp", type=float, default=0.3)
    p.add_argument("--wave-menu", type=int, default=1, choices=[1, 2, 3])
    args = p.parse_args()

    ti.init(arch=ti.gpu, log_level=ti.WARN)

    wc_state = build_wc_state(
        K=_K,
        geometry=_TOPOLOGY,
        nx=args.grid, ny=args.grid, nz=args.grid,
        wavelength=_WAVELENGTH,
        spacing=_SPACING,
    )

    pipeline = K10VizPipeline(
        grid=args.grid, cam=tuple(args.cam),
        stride=args.stride, warp=args.warp, wave_menu=args.wave_menu,
    )
    initial = [NaturalUnitSystem(), BoundaryCondition("dirichlet"), wc_state]

    print(f"K={_K} topology='{_TOPOLOGY}'  grid={args.grid}^3  stride={args.stride}")
    print(f"warp={args.warp}  wave_menu={args.wave_menu}")
    print("Wireframe xy plane. Close window (ESC) to stop.\n")

    out_dir = Path(__file__).resolve().parents[2] / "data"
    ctx = Runner({"session": InMemorySink()}).run(
        pipeline,
        name="k10_golden_wireframe",
        params={"grid": args.grid},
        output_dir=out_dir,
        dt=_DT,
        max_steps=args.steps,
        initial_features=initial,
    )

    if ctx.diag.errors:
        for e in ctx.diag.errors:
            print(f"  {e}")
        return

    m = ctx.data.require(StabilityMetrics)
    print(f"\nSteps: {ctx.sim.step}  localization={m.localization:.4f}")


if __name__ == "__main__":
    main()