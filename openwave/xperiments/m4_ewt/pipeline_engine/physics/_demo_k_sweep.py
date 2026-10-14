"""
K-sweep demo for StabilityMetrics on the golden-angle topology.

Runs six configurations (K = 2, 3, 5, 10, 11, 12) on the 'golden'
wave-centre arrangement, evolves each for a fixed number of steps,
and writes one JSON document per sweep.

This is NOT the B10a from the pipeline plan. B10a requires:
  - multiple topologies (golden + tetrahedron_10_locked + control)
  - the R8 perturbation protocol with three seeds per K
  - matched initial energy
  - structural (V3, conservative) and energetic (V2/V4) comparisons

This script answers one narrower question, which B10a needs before it
can be built: does the 'golden' topology alone already select K = 10
by localization? If yes, B10a's structural comparison has a candidate.
If no, the selection (if it exists) must come from the nonlinear terms
that B10a adds; the golden arrangement is not ruled out, the linear
baseline is.

Run headless from the project root:

    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo_k_sweep

Output: m4_ewt/data/k_sweep_golden.json and a printed table.

The JSON has two top-level keys: "meta" (the sweep parameters) and
"runs" (one dict per K). Same meta-plus-data shape as the legacy
instrumentation in m4_ewt/data/. freq_drift is null for a config that
never recorded a second zero-crossing (the measurement did not happen,
distinct from a measured zero).

The sweep runs through ExperimentRunner (plan item 1.10) so the
per-config pipeline and sinks are fresh, and a config that raises is
recorded as a crashed row without stopping the sweep.

Note: no `from __future__ import annotations` here. Taichi kernel
definitions (imported transitively through the physics layer) need
live type objects.
"""

import argparse
import json
from pathlib import Path

import taichi as ti

from ..experiments import ExperimentConfig, ExperimentRunner, ExperimentSummary
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
from .features import BoundaryCondition, PsiLongField, RunSeed, StabilityMetrics
from .units import NaturalUnitSystem, UnitSystem
from .wc_factory import build_wc_state
from .wc_types import WCState

# Sweep parameters. Changing these changes what the sweep measures.
# These are the defaults; --grid and --steps override them at runtime.
_GRID = 64
_STEPS = 200
_DT = 0.2
_WAVELENGTH = 12.0
_SPACING = 12.0
_SEED_RADIUS = 4.0
_K_VALUES = (2, 3, 5, 10, 11, 12)
_TOPOLOGY = "golden"


class KSweepPipeline(Pipeline):
    """
    One run: allocate, seed multi-center from WCState, evolve, measure.

    WCMotionProcessor(NoOpRule) is included so WCState is present in
    the pipeline and wc_drift is a measured zero, not the fallback
    default (n_active_wc == 0). NoOpRule does not move the centres.
    """

    def __init__(self, *, grid: int, metric_threshold: float = 0.5):
        super().__init__(
            error_policy=ErrorPolicy.FAIL_FAST,
            external_provides=(UnitSystem, BoundaryCondition, WCState),
        )
        self.add(AllocateWaveField(nx=grid, ny=grid, nz=grid, dx=1.0))
        self.add(SeedMultiCenter(radius=_SEED_RADIUS))
        self.add(ClearAccelerationProcessor())
        self.add(LaplacianProcessor())
        self.add(LeapfrogProcessor())
        self.add(BoundaryProcessor(field_type=PsiLongField))
        self.add(WCMotionProcessor(rule=NoOpRule()))
        self.add(StabilityMetricsUpdate(localization_threshold=metric_threshold))


def _make_config(K: int, *, grid: int, steps: int) -> ExperimentConfig:
    """
    Build one ExperimentConfig for K on the golden topology.

    RunSeed(K) is included for the convention it records (each config
    declares its seed), not because the current simulation reads it.
    Item 1.19 makes build_wc_state and any future random initialiser
    read ctx.data.require(RunSeed).value; until then the sweep is
    deterministic by other means (build_wc_state uses a hard-coded
    random.Random(42)).
    """
    wc_state = build_wc_state(
        K=K,
        geometry=_TOPOLOGY,
        nx=grid,
        ny=grid,
        nz=grid,
        wavelength=_WAVELENGTH,
        spacing=_SPACING,
    )
    return ExperimentConfig(
        name=f"K{K}",
        params={"K": K, "topology": _TOPOLOGY, "grid": grid},
        initial_features=(
            NaturalUnitSystem(),
            BoundaryCondition("dirichlet"),
            wc_state,
            RunSeed(K),
        ),
        dt=_DT,
        max_steps=steps,
    )


def _make_pipeline(cfg: ExperimentConfig) -> Pipeline:
    """Fresh pipeline per config. Grid comes from the config's params."""
    grid = int(cfg.params["grid"])
    return KSweepPipeline(grid=grid)


def _summarize(ctx) -> dict:
    """
    Extract the metrics of interest from StabilityMetrics.

    freq_ref == 0.0 means no second zero-crossing was recorded: the
    measurement never happened. That is distinct from a measured zero
    (a field with a perfectly stable frequency). Reported as None so a
    JSON reader sees null and a table reader sees "n/a", not a
    misleading 0.0000e+00.
    """
    m = ctx.data.require(StabilityMetrics)
    if m.freq_ref == 0.0:
        freq_ref = freq_now = freq_drift = None
    else:
        freq_ref = m.freq_ref
        freq_now = m.freq_now
        freq_drift = m.freq_drift
    return {
        "K": ctx.params.get("K"),
        "localization": m.localization,
        "sphericity": m.sphericity,
        "r_rms": m.r_rms,
        "mass": m.mass,
        "ipr": m.ipr,
        "freq_ref": freq_ref,
        "freq_now": freq_now,
        "freq_drift": freq_drift,
        "wc_drift": m.wc_drift,
        "n_active_wc": m.n_active_wc,
    }


def _summary_to_row(s: ExperimentSummary) -> dict:
    """
    Flatten one ExperimentSummary into a single JSON row:
    name + metrics, plus diagnostics only when they carry information.

    Keeps the old flat shape for the fields that were already there
    (K, localization, sphericity, ...), and adds `name` at the front.
    `errors`, `warnings`, `crashed` appear only when non-empty so a
    clean sweep's JSON is unchanged from the pre-ExperimentRunner
    version except for `name` and the null freq values.
    """
    row = {"name": s.name}
    row.update(s.metrics)
    if s.crashed:
        row["crashed"] = True
    if s.errors:
        row["errors"] = list(s.errors)
    if s.warnings:
        row["warnings"] = list(s.warnings)
    return row


def _write_json(summaries, path: Path, meta: dict) -> None:
    """
    Write one sweep's summaries to a single JSON document.

    Structure:
        meta  -- the parameters that produced the runs (topology, grid,
                 steps, K values, boundary, unit system)
        runs  -- one flat dict per K, with the metric values

    Same convention as the legacy instrumentation (meta + data in one
    file), so a reader can tell what configuration produced the
    numbers without a separate sidecar.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    runs = [_summary_to_row(s) for s in summaries]
    doc = {"meta": meta, "runs": runs}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)


def _print_table(summaries, *, grid: int, steps: int) -> None:
    print()
    print("=" * 96)
    print(f"K-sweep on topology '{_TOPOLOGY}'  grid={grid}  dt={_DT}  steps={steps}")
    print("=" * 96)
    hdr = (
        f"{'K':>3}  {'localization':>14}  {'sphericity':>11}  "
        f"{'r_rms':>8}  {'mass':>11}  {'ipr':>11}  "
        f"{'freq_drift':>12}  {'n_wc':>5}"
    )
    print(hdr)
    print("-" * len(hdr))
    for s in summaries:
        if s.crashed:
            msg = s.errors[0] if s.errors else "unknown"
            print(f"{'?':>3}  CRASHED ({s.name}): {msg}")
            continue
        m = s.metrics
        fd = m["freq_drift"]
        fd_str = f"{fd:>12.4e}" if fd is not None else f"{'n/a':>12}"
        print(
            f"{m['K']:>3}  {m['localization']:>14.6e}  "
            f"{m['sphericity']:>11.4f}  {m['r_rms']:>8.3f}  "
            f"{m['mass']:>11.4e}  {m['ipr']:>11.4e}  "
            f"{fd_str}  {m['n_active_wc']:>5d}"
        )
    print("=" * 96)


def main() -> None:
    p = argparse.ArgumentParser(description="M4 K-sweep stability demo")
    p.add_argument(
        "--grid",
        type=int,
        default=_GRID,
        help="grid size (default from module constants)",
    )
    p.add_argument(
        "--steps",
        type=int,
        default=_STEPS,
        help="steps per run (default from module constants)",
    )
    p.add_argument(
        "--out",
        type=str,
        default=None,
        help="output directory (default: <model_root>/data)",
    )
    args = p.parse_args()

    grid = args.grid
    steps = args.steps

    ti.init(arch=ti.cpu, log_level=ti.WARN)

    # Default output goes to the model's data/ folder, matching the
    # legacy instrumentation convention (m4_ewt/data/). parents[2] from
    # this file: [0]=physics/, [1]=pipeline_engine/, [2]=m4_ewt/.
    out_dir = Path(args.out) if args.out else Path(__file__).resolve().parents[2] / "data"

    print(f"Running K-sweep: K = {list(_K_VALUES)}, topology = '{_TOPOLOGY}'")
    print(f"Each run: grid={grid}^3, dt={_DT}, steps={steps}, seed radius={_SEED_RADIUS}")
    print()

    configs = [_make_config(K, grid=grid, steps=steps) for K in _K_VALUES]

    # Sweep driver: fresh pipeline, sinks, and runner per config.
    # on_error="continue": a config that raises is recorded as a
    # crashed row without stopping the sweep.
    er = ExperimentRunner(
        runner_factory=lambda sinks: Runner(sinks),
        sinks_factory=lambda cfg: {"session": InMemorySink()},
        on_error="continue",
    )

    summaries = er.run_sweep(
        pipeline_factory=_make_pipeline,
        configs=configs,
        summarize=_summarize,
        output_dir=out_dir,
    )

    for s in summaries:
        if s.crashed:
            print(f"  {s.name}: crashed ({s.errors[0] if s.errors else '?'})")
        else:
            print(f"  {s.name}: done ({s.duration_s:.2f}s)")

    _print_table(summaries, grid=grid, steps=steps)

    meta = {
        "sweep": "k_sweep_golden",
        "topology": _TOPOLOGY,
        "grid": grid,
        "steps": steps,
        "dt": _DT,
        "wavelength": _WAVELENGTH,
        "spacing": _SPACING,
        "seed_radius": _SEED_RADIUS,
        "k_values": list(_K_VALUES),
        "boundary": "dirichlet",
        "unit_system": "NaturalUnitSystem",
        "notes": "Not B10a; see _demo_k_sweep.py module docstring.",
    }

    json_path = out_dir / "k_sweep_golden.json"
    _write_json(summaries, json_path, meta)
    print(f"\nJSON written to: {json_path}")


if __name__ == "__main__":
    main()
