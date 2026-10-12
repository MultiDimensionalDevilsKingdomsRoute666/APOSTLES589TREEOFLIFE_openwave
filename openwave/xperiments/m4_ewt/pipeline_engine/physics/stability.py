"""
Stability metrics for the pipeline engine (plan Section 6, item 1.9).

Computes five metrics into StabilityMetrics:

    IPR          = integral |psi|^4 dV / (integral |psi|^2 dV)^2   [1/volume]
    localization = IPR / IPR_initial                               [dimensionless]
    r_rms        = sqrt( <r^2> ), relative to the grid center      [grid units]
    G_ij         = <r_i r_j>, mass-weighted gyration tensor        [grid units^2]
    sphericity   = lambda_min / lambda_max of G                    [dimensionless]
    wc_drift     = mean |r_wc - r_wc_initial| over active WCs      [grid units]
    freq_drift   = (freq_now - freq_ref) / freq_ref                [dimensionless]
    sol_lifetime = consecutive steps with localization > threshold [count]

Frequency signal (definition C, resolved 2026-10-12):

    s(t) = integral psi . (psi - psi_prev) dV

For a field oscillating around zero at angular frequency omega, s(t)
is proportional to sin(2*omega*t) plus a small DC offset. The processor
detects upward zero-crossings of s(t) and derives:

    delta_t = time between consecutive upward crossings
    f_field = 1 / (2 * delta_t)

The factor of 2 is because s(t) has half the field's period. See the
StabilityMetrics docstring for the full derivation and limitations
(reflection contamination, pipeline B, longitudinal-only).

The plan (Section 9, Q5) left the primary definition of "stability"
author-gated and listed freq_drift as a candidate metric. Definition C
is the author's chosen resolution. The TrackerFields signals (freq_local
at a single voxel, its three-plane average freq_global) are not
well-defined for a symmetric seed released from rest.

The reference center for r_rms and G is nx * 0.5, the same convention
as SeedPulse and SeedMultiCenter. WCState is optional (try_get, not
require); a field-only pipeline is a legal configuration.

The processor does not require UnitSystem: it measures in grid units
and leaves the conversion to the caller.

This processor holds Taichi fields on the instance (allocated in
setup, reused in process), the same pattern as EnergyBudgetUpdate.
The stateless guard compares repr() of instance fields; Taichi's repr
does not expose field contents, so the guard does not fire on writes
inside process(). If Taichi ever changes this, both this processor and
EnergyBudgetUpdate would need a different guard strategy.

Note: no `from __future__ import annotations` here. Taichi kernel
definitions need live type objects.
"""

import math

import numpy as np
import taichi as ti

from ..pipeline import BaseProcessor, Stage
from .features import PsiLongField, StabilityMetrics, WaveGrid
from .wc_types import WCState


# Placeholder threshold for the sol_lifetime counter. Any positive
# value gives the same qualitative behaviour (localization starts at
# 1.0 by construction). The specific number is not load-bearing; the
# plan's Q5 leaves the primary definition of "stability" author-gated.
_DEFAULT_LOCALIZATION_THRESHOLD = 0.5


@ti.kernel
def _accumulate_field_moments(
    psi: ti.template(),
    dv: ti.f32,
    nx: ti.i32,
    ny: ti.i32,
    nz: ti.i32,
    out_mass: ti.template(),
    out_quartic: ti.template(),
):
    """
    Accumulate mass (integral |psi|^2 dV) and quartic (integral |psi|^4 dV)
    over the full grid. Both are translation-invariant.

    ti.ndrange is a parallel loop. Taichi already makes += on a global
    field atomic there (EnergyBudgetUpdate relies on it); ti.atomic_add
    states it explicitly. The addends are cast to f64 explicitly,
    matching the field type.
    """
    out_mass[None] = 0.0
    out_quartic[None] = 0.0
    for i, j, k in ti.ndrange(nx, ny, nz):
        s = psi[i, j, k].norm_sqr()
        ti.atomic_add(out_mass[None], ti.cast(s * dv, ti.f64))
        ti.atomic_add(out_quartic[None], ti.cast(s * s * dv, ti.f64))


@ti.kernel
def _accumulate_gyration(
    psi: ti.template(),
    cx: ti.f32,
    cy: ti.f32,
    cz: ti.f32,
    dv: ti.f32,
    nx: ti.i32,
    ny: ti.i32,
    nz: ti.i32,
    out_r2: ti.template(),
    out_xx: ti.template(),
    out_yy: ti.template(),
    out_zz: ti.template(),
    out_xy: ti.template(),
    out_xz: ti.template(),
    out_yz: ti.template(),
):
    """
    Accumulate mass-weighted <r^2> and the six independent components of
    the gyration tensor, all relative to (cx, cy, cz).

    Same atomic_add reasoning as _accumulate_field_moments.
    """
    out_r2[None] = 0.0
    out_xx[None] = 0.0
    out_yy[None] = 0.0
    out_zz[None] = 0.0
    out_xy[None] = 0.0
    out_xz[None] = 0.0
    out_yz[None] = 0.0
    for i, j, k in ti.ndrange(nx, ny, nz):
        s = psi[i, j, k].norm_sqr()
        rx = ti.cast(i, ti.f32) - cx
        ry = ti.cast(j, ti.f32) - cy
        rz = ti.cast(k, ti.f32) - cz
        ti.atomic_add(out_r2[None], ti.cast((rx * rx + ry * ry + rz * rz) * s * dv, ti.f64))
        ti.atomic_add(out_xx[None], ti.cast(rx * rx * s * dv, ti.f64))
        ti.atomic_add(out_yy[None], ti.cast(ry * ry * s * dv, ti.f64))
        ti.atomic_add(out_zz[None], ti.cast(rz * rz * s * dv, ti.f64))
        ti.atomic_add(out_xy[None], ti.cast(rx * ry * s * dv, ti.f64))
        ti.atomic_add(out_xz[None], ti.cast(rx * rz * s * dv, ti.f64))
        ti.atomic_add(out_yz[None], ti.cast(ry * rz * s * dv, ti.f64))


@ti.kernel
def _accumulate_freq_signal(
    psi: ti.template(),
    psi_prev: ti.template(),
    dv: ti.f32,
    nx: ti.i32,
    ny: ti.i32,
    nz: ti.i32,
    out_s: ti.template(),
):
    """
    Accumulate s(t) = integral psi . (psi - psi_prev) dV.

    A signed scalar. For a field oscillating around zero at angular
    frequency omega, s(t) is proportional to sin(2*omega*t) plus a
    small DC offset (the offset scales as omega*dt and is negligible
    for omega*dt << 1). Used for upward zero-crossing detection in
    the freq_drift metric.

    Uses ti.atomic_add for the same reason as the other two kernels.
    """
    out_s[None] = 0.0
    for i, j, k in ti.ndrange(nx, ny, nz):
        diff = psi[i, j, k] - psi_prev[i, j, k]
        s = psi[i, j, k].dot(diff)
        ti.atomic_add(out_s[None], ti.cast(s * dv, ti.f64))


def _sphericity_from_gyration(xx, yy, zz, xy, xz, yz):
    """
    Smallest-to-largest eigenvalue ratio of the 3x3 symmetric gyration
    tensor.

    Returns 0.0 when the tensor is degenerate (largest eigenvalue <= 0,
    which happens for an empty field or a field localized at a point).
    Tiny negative eigenvalues from floating-point noise on the smallest
    component are clamped to zero.
    """
    g = np.array([[xx, xy, xz], [xy, yy, yz], [xz, yz, zz]], dtype=np.float64)
    eigvals = np.linalg.eigvalsh(g)
    lam_max = float(eigvals[-1])
    if lam_max <= 0.0:
        return 0.0
    lam_min = max(0.0, float(eigvals[0]))
    return lam_min / lam_max


class StabilityMetricsUpdate(BaseProcessor):
    """
    Measure stability metrics into StabilityMetrics. Stage.MEASURE,
    order 20.

    Order rationale: after EnergyBudgetUpdate (order 5) and
    AmplitudeTracker (order 10), before any LogProcessor (order 500+).
    All MEASURE processors read the same field; the order between them
    is a convention for readability, not a dependency.

    Requires WaveGrid and the field named by field_type (default
    PsiLongField). Provides StabilityMetrics (allocated in setup).

    WCState is optional (try_get). The reference positions are captured
    in setup(), before any step runs. The pipeline order is PRE_UPDATE,
    UPDATE, POST_UPDATE, MEASURE; capturing in process() at step 0 would
    read the positions after WCMotionProcessor's first step, not the
    initial ones.

    localization_threshold: sol_lifetime counts consecutive steps where
    localization > threshold. Default is a placeholder (see module
    docstring); the plan's Q5 leaves the primary definition author-gated.
    """

    name = "StabilityMetricsUpdate"
    stage = Stage.MEASURE
    order = 20
    provides = (StabilityMetrics,)

    def __init__(
        self,
        field_type=PsiLongField,
        localization_threshold: float = _DEFAULT_LOCALIZATION_THRESHOLD,
    ):
        self.field_type = field_type
        self.localization_threshold = float(localization_threshold)
        self.requires = (WaveGrid, field_type)

    def setup(self, ctx) -> None:
        metrics = StabilityMetrics()
        ctx.data.set(metrics)

        # f64 accumulators for summation across the grid. f32 loses
        # precision on 100k+ voxels; EnergyBudgetUpdate makes the same
        # choice for the same reason.
        self._mass = ti.field(dtype=ti.f64, shape=())
        self._quartic = ti.field(dtype=ti.f64, shape=())
        self._r2 = ti.field(dtype=ti.f64, shape=())
        self._xx = ti.field(dtype=ti.f64, shape=())
        self._yy = ti.field(dtype=ti.f64, shape=())
        self._zz = ti.field(dtype=ti.f64, shape=())
        self._xy = ti.field(dtype=ti.f64, shape=())
        self._xz = ti.field(dtype=ti.f64, shape=())
        self._yz = ti.field(dtype=ti.f64, shape=())
        self._s_signal = ti.field(dtype=ti.f64, shape=())

        # Capture wave-centre reference positions before any step runs.
        # WCState is provided through initial_features, which Runner
        # sets before pipeline.setup(). try_get: a field-only pipeline
        # is a legal configuration.
        wc_state = ctx.data.try_get(WCState)
        if wc_state is not None:
            metrics.wc_initial_positions = [
                (wc.x, wc.y, wc.z) for wc in wc_state.centers
            ]

    def process(self, ctx) -> None:
        grid = ctx.data.require(WaveGrid)
        field = ctx.data.require(self.field_type)
        metrics = ctx.data.require(StabilityMetrics)

        dv = grid.dx ** 3

        # Pass 1: mass and quartic (translation-invariant)
        _accumulate_field_moments(
            field.psi, dv, grid.nx, grid.ny, grid.nz,
            self._mass, self._quartic,
        )
        mass = float(self._mass[None])
        quartic = float(self._quartic[None])

        # Pass 2: r^2 and gyration tensor, relative to the grid center
        # nx * 0.5, the same convention as SeedPulse and SeedMultiCenter
        cx = grid.nx * 0.5
        cy = grid.ny * 0.5
        cz = grid.nz * 0.5
        _accumulate_gyration(
            field.psi, cx, cy, cz, dv,
            grid.nx, grid.ny, grid.nz,
            self._r2,
            self._xx, self._yy, self._zz,
            self._xy, self._xz, self._yz,
        )
        r2_sum = float(self._r2[None])

        # IPR, r_rms, sphericity
        if mass > 0.0:
            ipr = quartic / (mass * mass)
            r_rms = math.sqrt(r2_sum / mass)
            inv_mass = 1.0 / mass
            sphericity = _sphericity_from_gyration(
                float(self._xx[None]) * inv_mass,
                float(self._yy[None]) * inv_mass,
                float(self._zz[None]) * inv_mass,
                float(self._xy[None]) * inv_mass,
                float(self._xz[None]) * inv_mass,
                float(self._yz[None]) * inv_mass,
            )
        else:
            ipr = 0.0
            r_rms = 0.0
            sphericity = 0.0

        # Capture the reference IPR once, at the first non-empty step.
        if metrics.ipr_initial == 0.0 and ipr > 0.0:
            metrics.ipr_initial = ipr

        metrics.ipr = ipr
        metrics.mass = mass
        metrics.r_rms = r_rms
        metrics.sphericity = sphericity

        if metrics.ipr_initial > 0.0 and ipr > 0.0:
            metrics.localization = ipr / metrics.ipr_initial
        else:
            metrics.localization = 0.0

        if metrics.localization > self.localization_threshold:
            metrics.sol_lifetime += 1
        else:
            metrics.sol_lifetime = 0

        # Optional: wave-centre drift. Reference positions were captured
        # in setup() if WCState was present at that point; if not, the
        # pipeline has no WCs and both fields stay at zero.
        wc_state = ctx.data.try_get(WCState)
        if wc_state is not None and metrics.wc_initial_positions:
            self._update_wc_drift(wc_state, metrics)
        else:
            metrics.wc_drift = 0.0
            metrics.n_active_wc = 0

        # Pass 3: frequency signal s(t) = integral psi . (psi - psi_prev) dV.
        # Upward zero-crossings give the field period (times two, because
        # s(t) has half the field's period). See the module docstring for
        # the derivation and the class docstring for the limitations.
        _accumulate_freq_signal(
            field.psi, field.psi_prev, dv,
            grid.nx, grid.ny, grid.nz,
            self._s_signal,
        )
        s_now = float(self._s_signal[None])
        t_now = ctx.sim.t

        if metrics.s_prev < 0.0 and s_now >= 0.0:
            # Upward zero-crossing of s(t).
            if metrics.t_last_crossing >= 0.0:
                delta_t = t_now - metrics.t_last_crossing
                if delta_t > 0.0:
                    f_measured = 1.0 / (2.0 * delta_t)
                    if metrics.freq_ref == 0.0:
                        metrics.freq_ref = f_measured
                    metrics.freq_now = f_measured
                    metrics.freq_drift = (
                        (metrics.freq_now - metrics.freq_ref) / metrics.freq_ref
                    )
            metrics.t_last_crossing = t_now

        metrics.s_prev = s_now

    @staticmethod
    def _update_wc_drift(wc_state, metrics) -> None:
        """
        Mean Euclidean displacement of active wave centres from their
        reference positions, captured in setup().

        Deactivated WCs are skipped (their position is stale).
        zip() truncates at the shorter of the two sequences.
        """
        drifts = []
        for wc, (x0, y0, z0) in zip(wc_state.centers, metrics.wc_initial_positions):
            if not wc.active:
                continue
            rx = wc.x - x0
            ry = wc.y - y0
            rz = wc.z - z0
            drifts.append(math.sqrt(rx * rx + ry * ry + rz * rz))
        if drifts:
            metrics.wc_drift = sum(drifts) / len(drifts)
            metrics.n_active_wc = len(drifts)
        else:
            metrics.wc_drift = 0.0
            metrics.n_active_wc = 0