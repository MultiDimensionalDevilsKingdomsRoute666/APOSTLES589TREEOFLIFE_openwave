# M7.5, validate the clock in real time + stability

> Task **M7.5** (M7 / HydroBoros). taskID = M7.N iteration. Status: **Done** (2026-07-03, review approved; gate outcomes in [`§ FINDINGS 5`](#5-gates-vs-the-plan--what-moves-where)) · Roadmap: [`../m7_roadmap.md`](../m7_roadmap.md)

This doc is the task's full record: planning + findings + future planning + documentation. **Repositioned 2026-07-02**: in the time-harmonic frame the de Broglie clock is IN the soliton from M7.1 (the fixed-ω minimization, [`../m7_background.md § 5a`](../m7_background.md)); this task does not "add" a clock, it **validates the harmonic reduction against real-time dynamics** and establishes stability.

---

## Plan

| Step | What | Gate |
| --- | --- | --- |
| 1 | evolve the relaxed M7.3/M7.4 states with the **constrained Minkowski leapfrog** (full time-dependent EOM, no harmonic assumption) | energy conserved to integrator tolerance over the run |
| 2 | **clock validation**: measure the emergent oscillation frequency from the evolution | matches the input harmonic `ω` (the reduction is self-consistent); reported vs Dirac `ω_D` |
| 3 | **stability**: long runs (many periods), perturbation kicks (amplitude + shape) | persists, no collapse / expansion mode; perturbations ring down or orbit |
| 4 | **`β*` threshold probe** (Werbos v5 Test 1, corpus #10): drive small-amplitude fluctuations below / above the nonlinear coupling threshold | sub-threshold fluctuations behave linear-Maxwell (vacuum stability); the threshold located, if it exists in this sector |
| 5 | energy-minimizing-clock check (the M5.8 mechanism, Duda's prescription in the [roadmap](../m7_roadmap.md) Phase A note): scan `E_ω(ω)` around the soliton | the soliton's ω sits at the energy minimum of the scan |

Honest outcomes: a drift between the emergent and input ω quantifies the harmonic reduction's error (report it, do not hide it); an instability found here invalidates the M7.4 state and sends it back with the measured unstable mode.

Artifacts: `scripts/m7_5_clock_stability.py` + `data/m7_5_*.npz` + `plots/m7_5_*.png` (ω spectrogram, energy trace, perturbation response, `E_ω(ω)` scan).

---

## FINDINGS (2026-07-03, execution)

Artifacts: [`../scripts/m7_5_clock_stability.py`](../scripts/m7_5_clock_stability.py) (modes `smoke` / `disp` / `vacuum` / `main` / `scan` / `residual` / `analyze`) · data [`m7_5_disp.json`](../data/m7_5_disp.json) · [`m7_5_vacuum.json`](../data/m7_5_vacuum.json) · [`m7_5_evolve.json`](../data/m7_5_evolve.json) · [`m7_5_scan.json`](../data/m7_5_scan.json) · [`m7_5_residual.json`](../data/m7_5_residual.json) · [`m7_5_smoke.json`](../data/m7_5_smoke.json). Deleted raw data (>1 MB rule): `data/m7_5_state.npz` (25.2 MB, the regenerated M7.4 winner doublet; regen: `python m7_5_clock_stability.py main` re-relaxes and re-caches it, ~4 min).

### Plots

![`../plots/m7_5_clock_traces.png`](../plots/m7_5_clock_traces.png)
![`../plots/m7_5_tachyon_scan.png`](../plots/m7_5_tachyon_scan.png)

### 1. The real-time theory and its exactness gates ✅

Pure-vector sector (scalars frozen, = the M7.4 sector), temporal gauge: `T = ½\|Ȧ\|² + ½\|J̇\|²`, `V = ½\|∇×A\|² + ½\|∇×J\|² + A·J + f(\|J\|²)` with the repulsive `f` (the M7.4 Q6 verdict). Two gates pin the translation before any physics claim:

| Gate | Result |
| --- | --- |
| `⟨E_real(t)⟩` over one period on the doublet = `E_ω` | dev **1.85e-14**: the harmonic functional IS the period-averaged energy of this real-time theory, exactly (incl. the exact quartic average) |
| leapfrog energy drift is O(dt²) | drift 0.59 → 0.148 at half dt (ratio 4.0): the integrator is correct; the later drift is the runaway stiffening, not integrator failure |

### 2. THE HEADLINE: the vacuum is unconditionally tachyonic at long wavelength ❌ (theory-level finding)

The linearized transverse sector around `A = J = 0` has the frequency matrix `M(k) = [[k², −1], [−1, k² + 2c1]]`, and `det M(0) = −1` for **any** `c1`: a bilinear `A·J` coupling with a massless `A` always has a negative band at small `k`. Quantitatively (canonical `g = λ = 1`):

| Convention | Tachyon band | Max amplitude growth rate (at k = 0) |
| --- | --- | --- |
| repulsive (`c1 = +½`) | `k² < (√5−1)/2 = 0.618`, `k* = 0.7862` | 0.7862 |
| focusing (`c1 = −½`) | `k² < (1+√5)/2 = 1.618`, `k* = 1.2720` | 1.2720 |

Numerical confirmation (vacuum noise, N = 48): measured amplitude growth rate **0.7850 vs analytic 0.7862 (0.15%)** at ε = 1e-6, and the rate is amplitude-independent (0.756 at ε = 1e-4; ε = 1e-2 saturates early): the instability is **linear**. Werbos-v5 Test 1 verdict for this truncation: **there is no β\* amplitude threshold: the vacuum is unstable at any amplitude**. The box does not save it (the band `k < 0.786` is resolved by any box with `L ≳ 8`; the soliton itself needs `L ≳ 12`). This unifies the M7.4 scalar-sector runaway (same disease, its `k = 0` face) and it is why the released soliton is destroyed: its own tail (`r90 = 5.7 → k ≈ 0.55`) lives inside the band; `\|A\|²` doubles by `t = 0.41 T` and the state never completes one clean period.

### 3. Why the harmonic frame works anyway: the clock rides above the tachyonic band ✅ (the ω\* threshold discovery)

The `E_ω` quadratic form gains the `ω²` stiffness that the real-time potential lacks: it is PSD **iff `ω ≥ ω\* = k\* = 0.7862`** (repulsive, canonical parameters). The fixed-`H_A` ω scan tests the prediction directly:

| ω | Fate | E\* | `Q_J` | `Q_can` |
| --- | --- | --- | --- | --- |
| 0.70 | ❌ runaway condensate (`\|g\| = 8.7e-4`, `maxf` 2.7) | −144.9 | 2224 | 4064 |
| 0.75 | ❌ runaway (`\|g\| = 4.8e-4`) | −16.8 | 778 | 1225 |
| 0.79 | ✅ converges (`\|g\| = 1.2e-6`), near-critical | +2.760 | 14.6 | 24.3 |
| 0.85 / 0.90 / 1.00 / 1.10 / 1.20 | ✅ clean solitons | 4.02 / 4.89 / 6.36 / 7.57 / 8.64 | 9.1 / 6.7 / 3.7 / 2.1 / 1.3 | 18.7 / 16.4 / 13.2 / 11.2 / 10.2 |

The existence boundary lands **between 0.75 and 0.79, bracketing the predicted 0.786**, with the J-condensate diverging as `ω → ω*⁺` (near-critical softening). And the family passes the clock's Legendre gate: the envelope theorem gives `dE*/dω = Q_can` exactly at fixed fields, and the measured finite-difference slope matches `Q_can` to ~1-2% at every interior point (e.g. 16.54 vs 16.38 at ω = 0.90, 13.41 vs 13.20 at ω = 1.0): **ω and `Q_can` are verified conjugates in full 3D**: the de Broglie clock has the correct Legendre structure even though `E*(ω)` itself is monotone at fixed `H_A` (the energy-minimizing-clock statement lives in the fixed-`Q_can` frame, where ω is the multiplier).

### 4. The clock verdict: the reduction error is the FRAME, not the ansatz

Three measurements on the regenerated winner (blend/repulsive, N = 64, `E_ω = 6.35803`, matching M7.4's 6.3580):

| Measurement | Result | Meaning |
| --- | --- | --- |
| sector norms | `avs = jvs = 0` exactly | the M7.4 winner is a **STANDING-wave doublet**: the cos-only subspace is gradient-invariant and the relaxation never left it; the rotating (Fleury m = 1) sector was never explored: M7.6 must seed `a_s ≠ 0` rotating pairs |
| ω-projected EOM residual, decomposed on `{a_c, 2∇×a_c}` | `α = −1.978` (analytic: `−2ω² = −2`), `β = −0.786` (→ helicity multiplier `μ = −0.393`), orthogonal rest 0.12 | the fixed-`H_A` minimizer misses being a real-time orbit by exactly the `−2ω²` frame term M7.3 identified (the ω²-sign flip): **the real-time-consistent objective is fixed-`Q_can` extremization**; note `μ = −0.393` numerically ≈ M7.4's universal `H_cross/H_A = −0.390` |
| 3ω residual of the J equation | **0.002** relative | the RWA/harmonic truncation is essentially exact; nothing about the doublet ansatz itself is broken |
| released real-time evolution | no ω = 1 tick; FFT peaks 0.62-0.64 on all probes; destroyed in ~2 T | the emergent-ω gate is **unmeasurable in this truncation**: the tachyon's rate (0.786) is comparable to the clock rate (1.0), so the state cannot complete a clean period; the 0.63 peak is the runaway's characteristic frequency (band-edge modes), not a clock |

### 5. Gates vs the plan + what moves where

| Plan gate | Outcome |
| --- | --- |
| energy conserved to integrator tolerance | ✅ O(dt²) verified (pre-runaway window) |
| persists many periods, no collapse mode | ❌ destroyed in ~2 T by the **vacuum** tachyon (state-independent): the honest-outcome clause fires, but the instability does NOT invalidate the M7.4 state (it is a property of the truncated theory's vacuum, and the harmonic frame at ω = 1 > ω\* is immune) |
| emergent ω matches input ω | ❌ unmeasurable (§ 4); replaced by two sharper validated statements: the Legendre conjugacy `dE*/dω = Q_can` (~1%) and the ω\* existence threshold (bracketed 0.75-0.79 vs predicted 0.786) |
| ω vs Dirac `ω_D` | deferred to M7.6 with the unit contract; the structural note stands (bilinears at 2ω = the Zitter structure) |
| β\* threshold probe | ✅ answered decisively: **no amplitude threshold exists in this truncation**: the linearized vacuum is tachyonic (0.785 measured vs 0.786 analytic); v5 Test 1 fails for the pure-vector sector: prime Werbos question (new **Q14**) |
| `E_ω(ω)` scan, soliton at the energy minimum | ✅ run; `E*(ω)` monotone at fixed `H_A` (correct frame for the minimum statement = fixed `Q_can`); bonus: the ω\* threshold confirmed |

Follow-ups seeded: (a) M7.6 relaxes at **fixed `Q_can` (+ `H_A`)** and seeds **rotating** (`a_s ≠ 0`) pairs: both the frame and the standing/rotating question are now design inputs, and the ball-vs-torus question gets its fair test; (b) the M6 1D benchmark's real-time stability claim deserves the same 1D check (the band is dimension-independent); (c) Q14 to Werbos: what cures the vacuum tachyon in the full model (A-mass from a condensate vacuum? the scalar/Gauss sector? a finite-universe IR cutoff? Werbos's `k > 0` stable islands suggest a cured region is known); (d) outward reports follow the new [`METHOD_NOTE.md`](../../../../../dev_docs/METHOD_NOTE.md) standard (equations first, equation-to-code map, small physics module: the M7.7 consolidation extracts it).

---

Cross-refs: roadmap [`../m7_roadmap.md`](../m7_roadmap.md) (M7.5) · background [`../m7_background.md`](../m7_background.md) (§ 5a frame, § 5c leapfrog) · Q9/Q11/Q13/**Q14** (the tachyon + the v5 `β*` context) in [`../m7_question_tracker.md`](../m7_question_tracker.md) · upstream [`m7_4_charged_soliton.md`](m7_4_charged_soliton.md) · downstream [`m7_6_observables.md`](m7_6_observables.md).

---

## TASK REVIEW (2026-07-03)

**Task Duration:** 01:28 (from 18:57 to 20:25 EDT)
**Usage Cap Triggered:** NO (finished before the 9:10pm reset; resume ping parked without firing)

**Results** (full detail: [`§ FINDINGS`](#findings-2026-07-03-execution)):

| Gate | Outcome |
| --- | --- |
| translation exactness | ✅ `⟨E_real(t)⟩ = E_ω` on the doublet to 1.85e-14; leapfrog drift O(dt²) (0.59 → 0.148 at half dt) |
| THE HEADLINE (Q14 opener) | the linearized vacuum is **unconditionally tachyonic at long wavelength** (`det M(0) = −1` for any `f`); measured vacuum growth rate **0.7850 vs analytic 0.7862 (0.15%)**, amplitude-independent |
| β\* probe (Werbos v5 Test 1) | ✅ answered: **no amplitude threshold exists** in the vector truncation (linear instability) |
| the ω\* threshold discovery | ✅ `E_ω` PSD iff `ω ≥ ω* = k* = 0.786`; scan confirmed: 0.70/0.75 runaway, 0.79+ solitons, `Q_J` → ∞ toward ω\* (the clock IS the stabilizer) |
| Legendre gate | ✅ `dE*/dω = Q_can` to ~1-2% at every interior scan point: ω-`Q_can` conjugacy verified in 3D |
| persistence / emergent ω | ❌ honest: destroyed in ~2 T by the vacuum tachyon (state-independent); no ω = 1 tick measurable |
| reduction verdict | ✅ residual `α = −1.978 ≈ −2ω²` (frame term), 3ω component of the J residual 0.2% (ansatz fine); the M7.4 winner is a **standing-wave doublet** (`a_s = j_s = 0`) |

**Issues / blockers:** Q14 blocks any real-time program (M7.18) until answered or cured in-model; the ball-vs-torus question was never fairly tested (standing states only); `m7_5_state.npz` (25.2 MB) deleted per the >1MB rule (regen: `python m7_5_clock_stability.py main`, ~4 min).

**Action needed:** M7.6 with the two design changes (fixed-`Q_can` + `H_A` relaxation; rotating `a_s ≠ 0` seeds); M7.7 milestone stop with both METHOD_NOTE-compliant packages, Q14 leading the Werbos one.

**Question audit (per the standing rule):** Q14 opened; **Q6 RESOLVED-empirical** (the written `f = gs²` is the program's branch, decided by our own runs; residual confirm folded into Q12); Q13/Q11/Q9 gained evidence, remain asks. Count: 5 ask-Marc, 5 ask-Werbos, 0 self-determine, 4 resolved.

**Findings**: M7.5 set out to validate the clock in real time and instead found why it cannot tick there: the written theory's vacuum is unconditionally tachyonic at long wavelength (a one-line determinant fact, confirmed on the lattice to 0.15%), and the harmonic soliton exists precisely because its frequency sits above the tachyonic band, a measured existence threshold at ω\* = 0.786 that makes the de Broglie clock load-bearing rather than decorative. The reduction itself is vindicated: the harmonic functional is exactly the period-averaged energy, the RWA error is 0.2%, and the ω-`Q_can` Legendre structure passes at the percent level; what fails is the truncated theory's vacuum, now Q14, the sharpest question the program has for Werbos.

**Research docs created / updated**:

- [this task doc](m7_5_clock_stability.md) (§ FINDINGS 1-5, plots inline)
- [`../scripts/m7_5_clock_stability.py`](../scripts/m7_5_clock_stability.py) (modes `smoke`/`disp`/`vacuum`/`main`/`scan`/`residual`/`analyze`)
- [`../data/m7_5_disp.json`](../data/m7_5_disp.json) · [`m7_5_vacuum.json`](../data/m7_5_vacuum.json) · [`m7_5_evolve.json`](../data/m7_5_evolve.json) · [`m7_5_scan.json`](../data/m7_5_scan.json) · [`m7_5_residual.json`](../data/m7_5_residual.json) · [`m7_5_smoke.json`](../data/m7_5_smoke.json)
- [`../plots/m7_5_clock_traces.png`](../plots/m7_5_clock_traces.png) · [`../plots/m7_5_tachyon_scan.png`](../plots/m7_5_tachyon_scan.png) (key plot: the tachyon + scan triptych)
- [`../m7_question_tracker.md`](../m7_question_tracker.md) (Q14 opened; Q6 → RESOLVED-empirical; Q13/Q11/Q9 addenda; comms plan updated; count 5/5/0/4)
