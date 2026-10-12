"""
K-sweep demo for StabilityMetrics on the golden-angle topology.

Runs six configurations (K = 2, 3, 5, 10, 11, 12) on the 'golden'
wave-centre arrangement, evolves each for a fixed number of steps,
and writes one CSV row per run.

This is NOT the B10a from the pipeline plan. B10a requires:
  - multiple topologies (golden + tetrahedron_10_locked + control)
  - the R8 perturbation protocol with three seeds per K
  - matched initial energy
  - structural (V3, conservative) and energetic (V2/V4) comparisons

This script answers one narrower question, which B10a needs before it
can be built: does the 'golden' topology alone already select K = 10
by localization? If yes, B10a's structural comparison has a candidate.
If no, B10a must use a different topology family.

Run headless from the project root:

    python -m openwave.xperiments.m4_ewt.pipeline_engine.physics._demo_k_sweep

Output: out_k_sweep/sweep.csv and a printed table.

Note: no `from __future__ import annotations` here. Taichi kernel
definitions (imported transitively through the physics layer) need
live type objects.
"""

import argparse
from pathlib import Path

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
from .features import BoundaryCondition, PsiLongField, StabilityMetrics
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


def _run_one(K: int, out_dir: Path, *, grid: int, steps: int):
    """
    Build and run one configuration, return a dict of the metrics.

    Returns a dict with the metrics plus an 'errors' count so the
    caller can spot a run that did not complete cleanly.
    """
    wc_state = build_wc_state(
        K=K,
        geometry=_TOPOLOGY,
        nx=grid, ny=grid, nz=grid,
        wavelength=_WAVELENGTH,
        spacing=_SPACING,
    )

    pipeline = KSweepPipeline(grid=grid)
    initial = [
        NaturalUnitSystem(),
        BoundaryCondition("dirichlet"),
        wc_state,
    ]

    runner = Runner({"session": InMemorySink()})
    ctx = runner.run(
        pipeline,
        name=f"k_sweep_K{K}",
        params={"K": K, "topology": _TOPOLOGY, "grid": grid},
        output_dir=out_dir,
        dt=_DT,
        max_steps=steps,
        initial_features=initial,
    )

    m = ctx.data.require(StabilityMetrics)
    return {
        "K": K,
        "localization": m.localization,
        "sphericity": m.sphericity,
        "r_rms": m.r_rms,
        "mass": m.mass,
        "ipr": m.ipr,
        "wc_drift": m.wc_drift,
        "n_active_wc": m.n_active_wc,
        "errors": len(ctx.diag.errors),
    }


def _write_csv(rows, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = [
        "K", "localization", "sphericity", "r_rms", "mass", "ipr",
        "wc_drift", "n_active_wc", "errors",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for row in rows:
            f.write(",".join(f"{row[h]}" for h in header) + "\n")


def _print_table(rows, *, grid: int, steps: int) -> None:
    print()
    print("=" * 96)
    print(f"K-sweep on topology '{_TOPOLOGY}'  grid={grid}  dt={_DT}  steps={steps}")
    print("=" * 96)
    hdr = (
        f"{'K':>3}  {'localization':>14}  {'sphericity':>11}  "
        f"{'r_rms':>8}  {'mass':>11}  {'ipr':>11}  {'n_wc':>5}"
    )
    print(hdr)
    print("-" * len(hdr))
    for row in rows:
        print(
            f"{row['K']:>3}  {row['localization']:>14.6e}  "
            f"{row['sphericity']:>11.4f}  {row['r_rms']:>8.3f}  "
            f"{row['mass']:>11.4e}  {row['ipr']:>11.4e}  "
            f"{row['n_active_wc']:>5d}"
        )
    print("=" * 96)


def main() -> None:
    p = argparse.ArgumentParser(description="M4 K-sweep stability demo")
    p.add_argument(
        "--grid", type=int, default=_GRID,
        help="grid size (default from module constants)",
    )
    p.add_argument(
        "--steps", type=int, default=_STEPS,
        help="steps per run (default from module constants)",
    )
    p.add_argument(
        "--out", type=str, default=None,
        help="output directory (default: ./out_k_sweep)",
    )
    args = p.parse_args()

    # Local bindings, not module-level mutation. Passing these down as
    # arguments keeps the module constants immutable and the test-visible
    # behaviour independent of how many times main() runs.
    grid = args.grid
    steps = args.steps

    ti.init(arch=ti.cpu, log_level=ti.WARN)

    out_dir = Path(args.out) if args.out else (Path(__file__).resolve().parent / "out_k_sweep")

    print(f"Running K-sweep: K = {list(_K_VALUES)}, topology = '{_TOPOLOGY}'")
    print(f"Each run: grid={grid}^3, dt={_DT}, steps={steps}, seed radius={_SEED_RADIUS}")
    print()

    rows = []
    for K in _K_VALUES:
        print(f"  K = {K:>2} ... ", end="", flush=True)
        row = _run_one(K, out_dir, grid=grid, steps=steps)
        rows.append(row)
        if row["errors"] > 0:
            print(f"done  (with {row['errors']} errors)")
        else:
            print("done")

    _print_table(rows, grid=grid, steps=steps)

    csv_path = out_dir / "sweep.csv"
    _write_csv(rows, csv_path)
    print(f"\nCSV written to: {csv_path}")


if __name__ == "__main__":
    main()