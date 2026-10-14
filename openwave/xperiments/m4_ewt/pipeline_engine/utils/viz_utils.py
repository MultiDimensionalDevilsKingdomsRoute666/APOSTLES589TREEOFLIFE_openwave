"""
Small helpers shared by visualization processors.

Nothing here imports physics; every function takes a raw Taichi field
and grid dimensions, or a scalar and a palette id. This keeps the
utilities usable by any model's visualization on the pipeline_engine
substrate.

Contents:
    mesh_indices   -- triangle indices for a flat grid mesh (numpy; no Taichi)
    find_peak      -- maximum |psi| over a vector field (Taichi kernel)
    gradient_color -- colour from a normalized scalar (Taichi func)
"""

import numpy as np
import taichi as ti


def mesh_indices(n_a: int, n_b: int) -> np.ndarray:
    """
    Triangle indices for a flat grid mesh over n_a * n_b vertices.

    Two triangles per quad, in a fixed winding. Vertex layout is
    row-major with the second dimension fastest: index (a, b) maps to
    a * n_b + b. The caller decides the vertex positions; this function
    only builds the connectivity.

    Raises ValueError when either dimension is less than 2 (no quad to
    triangulate).
    """
    if n_a < 2 or n_b < 2:
        raise ValueError(f"mesh needs at least 2x2 vertices, got {n_a}x{n_b}")
    tris = []
    for a in range(n_a - 1):
        for b in range(n_b - 1):
            v00 = a * n_b + b
            v10 = (a + 1) * n_b + b
            v01 = a * n_b + (b + 1)
            v11 = (a + 1) * n_b + (b + 1)
            tris.extend([v00, v10, v01])
            tris.extend([v10, v11, v01])
    return np.array(tris, dtype=np.int32)


@ti.kernel
def find_peak(
    psi: ti.template(),
    out: ti.template(),
    nx: ti.i32,
    ny: ti.i32,
    nz: ti.i32,
):
    """
    Maximum |psi| over the grid, written to out[None].

    Initializes out[None] to 1e-12 before the reduction, so an empty
    field returns 1e-12 rather than 0. A caller that divides by the
    peak then gets a large but finite number for an empty field, not a
    division by zero.

    The reduced quantity is |psi|, not |psi|^2: use norm(), not
    norm_sqr().
    """
    out[None] = 1e-12
    for i, j, k in ti.ndrange(nx, ny, nz):
        ti.atomic_max(out[None], psi[i, j, k].norm())


@ti.func
def gradient_color(t: ti.f32, palette: ti.i32):
    """
    Colour from a normalized scalar t, clipped to [0, 1].

    palette:
        1 -> orange (dark -> bright)
        2 -> ironbow (dark red -> orange -> yellow -> white)
        3 -> blueprint (light blue -> white)
        any other value falls through to blueprint.

    Returns a 3-vector in [0, 1] per channel.
    """
    tc = ti.min(ti.max(t, 0.0), 1.0)
    out = ti.Vector([0.0, 0.0, 0.0])
    if palette == 1:
        out = ti.Vector([1.0, 0.4 + 0.6 * tc, 0.0])
    elif palette == 2:
        out = ti.Vector(
            [
                ti.min(1.0, 2.0 * tc),
                ti.min(1.0, ti.max(0.0, 2.0 * tc - 0.5)),
                ti.min(1.0, ti.max(0.0, 2.0 * tc - 1.0)),
            ]
        )
    else:
        out = ti.Vector([0.2, 0.4 + 0.6 * tc, 1.0])
    return out
