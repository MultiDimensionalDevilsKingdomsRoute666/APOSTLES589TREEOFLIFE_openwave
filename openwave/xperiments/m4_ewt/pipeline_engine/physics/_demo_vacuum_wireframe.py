"""
Runnable demo: vacuum (base wave) as a wireframe xy mesh.

The pipeline runs the standard linear-wave soliton chain plus the
vacuum layer. The wireframe visualises `PsiBaseField`, the field the
vacuum variant owns: under a static vacuum (V1) the base wave stays at
its seed; under a periodic vacuum (V3) the base wave evolves under the
wave equation with a periodic boundary.

The soliton field (`PsiLongField`) is seeded by `SeedMultiCenter` from
the `wc_state` the caller passes, and evolves alongside, but this demo
does not render it. The `_demo_k10_wireframe.py` demo is the one that
renders the soliton.

Run:
    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo_vacuum_wireframe
    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo_vacuum_wireframe --vacuum static
    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo_vacuum_wireframe --grid 48 --stride 2 --warp 0.5

Options:
    --grid 64              grid size per axis
    --stride 1             mesh subsample (1 = every voxel)
    --warp 0.3             peak displacement, fraction of the domain
    --cam 2.0 2.5 2.0      camera position
    --wave-menu 1          1=orange, 2=ironbow, 3=blueprint
    --vacuum periodic      static (V1) or periodic (V3)

Not a test: opens a Taichi GGUI window and blocks until closed. Not in
the CI test list, cannot be run headless.

Note: no `from __future__ import annotations` here. Taichi kernel
definitions need live type objects.
"""

import argparse
from pathlib import Path

import numpy as np
import taichi as ti

from ..runner import Runner
from ..sinks import InMemorySink

from .visualize import WindowedProcessor
from .features import (
    BoundaryCondition,
    PsiBaseField,
    PsiLongField,
    StabilityMetrics,
    WaveGrid,
)
from .seed import SeedBaseWave
from .units import NaturalUnitSystem
from .vacuum import PeriodicVacuum, StaticVacuum
from .wc_factory import build_wc_state
from ..utils.viz_utils import find_peak, gradient_color, mesh_indices
from .presets import make_linear_wave_pipeline

_WAVELENGTH = 12.0
_SPACING = 12.0
_TOPOLOGY = "golden"
_K = 10
_DT = 0.2


# ======================================================================
# Kernel
# ======================================================================


@ti.kernel
def _warp_xy_plane_base(
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
        verts[mi * my + mj] = ti.Vector(
            [
                ti.cast(i, ti.f32) / max_dim,
                ti.cast(j, ti.f32) / max_dim,
                z_base + a * inv_peak * warp,
            ]
        )
        colors[mi * my + mj] = gradient_color(a * inv_peak, wave_menu)


# ======================================================================
# Processor
# ======================================================================


class VacuumWireframeViz(WindowedProcessor):
    """
    Single xy plane at z = nz//2, warped by |psi| of one field.

    Reads whichever field the caller passes in `field_type` (default
    `PsiBaseField`, the vacuum's base wave; `PsiLongField` renders the
    soliton instead). Same construction as `_demo_k10_wireframe.WireframeViz`;
    the only difference is which feature supplies `psi`.

    `requires` is set per-instance in `__init__` (the same pattern
    `BoundaryProcessor` uses) so the pipeline validates against the
    field this instance actually reads.
    """

    name = "VacuumWireframeViz"

    def __init__(
        self,
        *,
        cam=(2.0, 2.5, 2.0),
        stride=1,
        warp=0.3,
        wave_menu=1,
        field_type=PsiBaseField,
    ):
        super().__init__(cam=cam)
        self.stride = max(1, int(stride))
        self.warp = float(warp)
        self.wave_menu = int(wave_menu)
        self.field_type = field_type
        self.requires = (WaveGrid, field_type)

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
        field = ctx.data.require(self.field_type)

        self._peak[None] = 1e-12
        find_peak(field.psi, self._peak, grid.nx, grid.ny, grid.nz)
        inv_peak = 1.0 / float(self._peak[None])

        _warp_xy_plane_base(
            field.psi,
            self._verts,
            self._cols,
            self._k_fixed,
            grid.nx,
            grid.ny,
            self._mx,
            self._my,
            self._stride,
            self._max_dim,
            self.warp,
            inv_peak,
            self.wave_menu,
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
# Helpers
# ======================================================================


def _seed_base_array(nx, ny, nz, amp=0.5, sigma=8.0):
    """Gaussian on x at grid centre, shape (nx, ny, nz, 3)."""
    cx, cy, cz = nx * 0.5, ny * 0.5, nz * 0.5
    i, j, k = np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz), indexing="ij")
    r2 = (i - cx) ** 2 + (j - cy) ** 2 + (k - cz) ** 2
    arr = np.zeros((nx, ny, nz, 3), dtype=np.float32)
    arr[..., 0] = amp * np.exp(-r2 / (2.0 * sigma * sigma))
    return arr


def _build_vacuum(kind):
    if kind == "static":
        return StaticVacuum()
    if kind == "periodic":
        return PeriodicVacuum()
    raise ValueError(f"unknown vacuum kind: {kind!r}")


# ======================================================================
# Main
# ======================================================================


def main() -> None:
    p = argparse.ArgumentParser(description="M4 vacuum wireframe viz")
    p.add_argument("--grid", type=int, default=64)
    p.add_argument("--steps", type=int, default=1_000_000)
    p.add_argument("--cam", type=float, nargs=3, default=[2.0, 2.5, 2.0])
    p.add_argument("--stride", type=int, default=1)
    p.add_argument("--warp", type=float, default=0.3)
    p.add_argument("--wave-menu", type=int, default=1, choices=[1, 2, 3])
    p.add_argument("--field", type=str, default="base", choices=["base", "soliton"])
    p.add_argument(
        "--vacuum", type=str, default="periodic", choices=["static", "periodic"]
    )
    args = p.parse_args()

    ti.init(arch=ti.gpu, log_level=ti.WARN)

    wc_state = build_wc_state(
        K=_K,
        geometry=_TOPOLOGY,
        nx=args.grid,
        ny=args.grid,
        nz=args.grid,
        wavelength=_WAVELENGTH,
        spacing=_SPACING,
    )

    vacuum = _build_vacuum(args.vacuum)

    base_seed = _seed_base_array(args.grid, args.grid, args.grid, amp=0.5, sigma=8.0)
    pipeline = make_linear_wave_pipeline(
        grid=args.grid,
        vacuum=vacuum,
        extra_measure=(
            VacuumWireframeViz(
                cam=tuple(args.cam),
                stride=args.stride,
                warp=args.warp,
                wave_menu=args.wave_menu,
                field_type=PsiLongField if args.field == "soliton" else PsiBaseField,
            ),
        ),
    )
    pipeline.add(SeedBaseWave(base_seed))

    initial = [NaturalUnitSystem(), BoundaryCondition("dirichlet"), wc_state, vacuum]

    print(f"K={_K} topology='{_TOPOLOGY}'  grid={args.grid}^3  stride={args.stride}")
    print(f"warp={args.warp}  wave_menu={args.wave_menu}  vacuum={args.vacuum}")
    print(
        f"vacuum evolves={vacuum.evolves}  "
        f"supports_reflection={vacuum.supports_reflection}"
    )
    print("Wireframe xy plane (PsiBaseField). Close window (ESC) to stop.\n")

    out_dir = Path(__file__).resolve().parents[2] / "data"
    ctx = Runner({"session": InMemorySink()}).run(
        pipeline,
        name=f"vacuum_{args.vacuum}_wireframe",
        params={"grid": args.grid, "vacuum": args.vacuum},
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