"""
Tests for pipeline_engine/utils/viz_utils.py.

mesh_indices is pure numpy and needs no Taichi. find_peak and
gradient_color are Taichi; their tests initialise a CPU context and
use small dedicated fields.

Run from the project root:
    python -m openwave.xperiments.m4_ewt.pipeline_engine._test_viz_utils
"""

import sys
import traceback

import numpy as np
import taichi as ti

from .utils.viz_utils import find_peak, gradient_color, mesh_indices

_TI_INITIALIZED = False


def _ti_init():
    global _TI_INITIALIZED
    if not _TI_INITIALIZED:
        ti.init(arch=ti.cpu, log_level=ti.ERROR)
        _TI_INITIALIZED = True


# ======================================================================
# mesh_indices
# ======================================================================


def test_mesh_indices_single_quad():
    """
    A 2x2 grid is one quad -> two triangles, in the documented winding.

    Vertex layout (row-major, n_b = 2):
        0 1
        2 3
    Triangles: (0, 2, 1) and (2, 3, 1).

    Mutation caught: winding flipped, vertex order swapped, or the
    (a, b) -> index mapping changed.
    """
    idx = mesh_indices(2, 2)
    assert idx.tolist() == [0, 2, 1, 2, 3, 1]


def test_mesh_indices_counts():
    """
    3x3 grid -> 4 quads -> 8 triangles -> 24 indices.

    Mutation caught: off-by-one in the loop bound, or a quad's triangles
    emitted twice.
    """
    idx = mesh_indices(3, 3)
    assert idx.size == 24
    assert idx.dtype == np.int32


def test_mesh_indices_all_in_range():
    """
    Every index is a valid vertex id in [0, n_a * n_b).

    Mutation caught: an off-by-one index that references a vertex one
    past the end of the buffer.
    """
    for n_a, n_b in [(2, 2), (3, 3), (4, 5), (2, 10), (10, 2)]:
        idx = mesh_indices(n_a, n_b)
        assert idx.min() >= 0, (n_a, n_b)
        assert idx.max() < n_a * n_b, (n_a, n_b)


def test_mesh_indices_adjacent_quads_share_vertices():
    """
    3x2 grid -> 2 adjacent quads. Vertices 2 and 3 are the shared seam;
    both quads' triangle pairs reference them.

    Mutation caught: a stray +1 or -1 that silently severs the seam
    (would produce a mesh that renders but with a hole).
    """
    idx = mesh_indices(3, 2)
    assert idx.size == 12
    assert set(idx.tolist()) == {0, 1, 2, 3, 4, 5}


def test_mesh_indices_rejects_degenerate():
    """
    Dimension < 2 raises ValueError.

    Mutation caught: the check removed, producing an empty (silent) mesh.
    """
    for n_a, n_b in [(1, 5), (5, 1), (0, 5), (5, 0), (1, 1)]:
        try:
            mesh_indices(n_a, n_b)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {n_a}x{n_b}")


# ======================================================================
# find_peak
# ======================================================================


def test_find_peak_empty_field_returns_floor():
    """
    Zero field -> out[None] stays at the 1e-12 initialization value.

    Mutation caught: initialization dropped, so atomic_max over zeros
    leaves out[None] at whatever default the field was created with
    (usually 0), and callers that divide by it get an inf.
    """
    _ti_init()
    n = 4
    psi = ti.Vector.field(3, dtype=ti.f32, shape=(n, n, n))
    psi.fill(0.0)
    peak = ti.field(dtype=ti.f32, shape=())
    find_peak(psi, peak, n, n, n)
    assert abs(float(peak[None]) - 1e-12) < 1e-20, float(peak[None])


def test_find_peak_uses_amplitude_not_squared():
    """
    A single voxel with |psi| = 2 must yield peak = 2, not 4.

    Mutation caught: norm_sqr() instead of norm().
    """
    _ti_init()
    n = 4
    psi = ti.Vector.field(3, dtype=ti.f32, shape=(n, n, n))
    psi.fill(0.0)
    psi[1, 1, 1] = ti.Vector([2.0, 0.0, 0.0])
    peak = ti.field(dtype=ti.f32, shape=())
    find_peak(psi, peak, n, n, n)
    assert abs(float(peak[None]) - 2.0) < 1e-6, float(peak[None])


def test_find_peak_max_over_grid():
    """
    Peak is the largest |psi| across the grid, not the sum, not the last
    write.

    Mutation caught: sum instead of max, or the wrong axis order.
    """
    _ti_init()
    n = 4
    psi = ti.Vector.field(3, dtype=ti.f32, shape=(n, n, n))
    psi.fill(0.0)
    psi[0, 0, 0] = ti.Vector([1.0, 0.0, 0.0])
    psi[2, 3, 1] = ti.Vector([0.0, 3.0, 0.0])
    psi[3, 3, 3] = ti.Vector([0.0, 0.0, 2.0])
    peak = ti.field(dtype=ti.f32, shape=())
    find_peak(psi, peak, n, n, n)
    assert abs(float(peak[None]) - 3.0) < 1e-6, float(peak[None])


# ======================================================================
# gradient_color
# ======================================================================


@ti.kernel
def _gradient_kernel(t_in: ti.template(), palette: ti.i32, out: ti.template()):
    for i in t_in:
        out[i] = gradient_color(t_in[i], palette)


def _run_gradient(ts, palette):
    _ti_init()
    n = len(ts)
    t_field = ti.field(dtype=ti.f32, shape=(n,))
    out = ti.Vector.field(3, dtype=ti.f32, shape=(n,))
    t_field.from_numpy(np.array(ts, dtype=np.float32))
    _gradient_kernel(t_field, palette, out)
    return out.to_numpy()


def test_gradient_color_palette_orange():
    """
    Palette 1 is orange: r = 1, g grows from 0.4 to 1.0, b = 0.

    Mutation caught: swapped channels, wrong midpoint.
    """
    result = _run_gradient([0.0, 0.5, 1.0], palette=1)
    assert np.allclose(result[0], [1.0, 0.4, 0.0], atol=1e-6), result[0]
    assert np.allclose(result[1], [1.0, 0.7, 0.0], atol=1e-6), result[1]
    assert np.allclose(result[2], [1.0, 1.0, 0.0], atol=1e-6), result[2]


def test_gradient_color_palette_blueprint():
    """
    Palette 3 is blueprint: r = 0.2, g grows 0.4 -> 1.0, b = 1.

    Mutation caught: blueprint and orange swapped.
    """
    result = _run_gradient([0.0, 1.0], palette=3)
    assert np.allclose(result[0], [0.2, 0.4, 1.0], atol=1e-6), result[0]
    assert np.allclose(result[1], [0.2, 1.0, 1.0], atol=1e-6), result[1]


def test_gradient_color_clips_t():
    """
    t values outside [0, 1] are clipped to the endpoints.

    Mutation caught: the clip removed, so a peak value > 1 blows out
    the colour and a negative t flips channels.
    """
    result = _run_gradient([-0.5, 1.5, 2.0], palette=1)
    assert np.allclose(result[0], [1.0, 0.4, 0.0], atol=1e-6), result[0]
    assert np.allclose(result[1], [1.0, 1.0, 0.0], atol=1e-6), result[1]
    assert np.allclose(result[2], [1.0, 1.0, 0.0], atol=1e-6), result[2]


def test_gradient_color_unknown_palette_falls_back():
    """
    Any palette id other than 1 or 2 gives the blueprint palette.

    Mutation caught: else branch dropped, or an extra palette added
    silently.
    """
    result = _run_gradient([0.5], palette=99)
    expected = _run_gradient([0.5], palette=3)
    assert np.allclose(result, expected, atol=1e-6)


# ======================================================================
# Runner
# ======================================================================


def main() -> int:
    tests = [
        test_mesh_indices_single_quad,
        test_mesh_indices_counts,
        test_mesh_indices_all_in_range,
        test_mesh_indices_adjacent_quads_share_vertices,
        test_mesh_indices_rejects_degenerate,
        test_find_peak_empty_field_returns_floor,
        test_find_peak_uses_amplitude_not_squared,
        test_find_peak_max_over_grid,
        test_gradient_color_palette_orange,
        test_gradient_color_palette_blueprint,
        test_gradient_color_clips_t,
        test_gradient_color_unknown_palette_falls_back,
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
