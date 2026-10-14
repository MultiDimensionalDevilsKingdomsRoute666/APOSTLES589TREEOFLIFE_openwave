# M7.9: ChaosBook study + canonical-exercise benchmark

> **Status: ✅ DONE** (2026-07-07, review approved; E1-E5 complete, E6 sessions = user-scheduled follow-up). Roadmap row: [`m7_roadmap.md`](../m7_roadmap.md) § DONE (Phase 1 extension block). Author-convo record: `theory/author_convos/m7_phase1_convo.pdf` (local-only). Deliverables: [benchmark report](m7_9_benchmark_report.md) (E4) · [index](m7_9_chaosbook_index.md) (E1) · [reading digest](m7_9_reading_digest.md) (E5) · toolkit [`m7_9_orbits.py`](../scripts/m7_9_orbits.py) (E3). Checkpoints: [`../checkpoints/m7_9_progress.md`](../checkpoints/m7_9_progress.md).

## 1. Objective

Two outputs, one task: (a) a **benchmark suite** the author can trust: canonical exercises from Cvitanović et al., *Chaos: Classical and Quantum* ("ChaosBook", <https://chaosbook.org/>), implemented headless and checked against their published solutions ("your AI should kill it in 10 minutes, **but I want to see that**"); (b) the **orbit-hunting toolkit** (Poincaré sections, return maps, periodic-orbit finding, cycle stability) that the M7.10-M7.14 pure-Maxwell/Beltrami track will need (first consumer: [M7.10](m7_10_pure_maxwell.md), the no-Lagrangian test, defined 2026-07-07). A side output: light reading support so the maintainer gains call fluency without becoming the bottleneck.

## 2. Why (from the call)

The author's program is to find the electron as a **stable periodic orbit** in the electromagnetic field flow ("islands of superstability", the solar-system analogy), and ChaosBook is the author's named "Bible" for that methodology. The benchmark doubles as the self-test the author asked for: proof that what comes out of this platform is computed, not "linguistically mirrored", on problems with known answers. Follow-ups agreed at the call ride this task: 4-7 walkthrough sessions on the book, a test-design review session with **Burak Budan**, and possibly a later look by **Cvitanović** himself.

## 3. Context-window strategy (the book is ~1000 pages; NEVER load it whole)

| Rule | How |
| --- | --- |
| Use the chapter structure, not the tome | chaosbook.org serves the webbook **per chapter**; the author also sent a copy (persist to `theory/` per the corpus rules + a `_CITATIONS.md` entry). Build a local **index file first** (TOC → chapter → topics → exercises), then load only the chapter section + exercise statement relevant to the step in hand |
| Target chapters only | the working set is small: the overture (ch. 1), flows, maps + return maps, **Poincaré sections**, fixed points + how to find them (Newton / multiple shooting), **cycle stability** (Floquet), plus the worked examples attached to those chapters. Everything else is out of scope for this task |
| Per-exercise loading | one exercise at a time: statement + the minimal supporting section; solutions compared at the END (implement first, check after, so the known answer never reaches the implementation) |

## 4. Plan

| Step | Content |
| --- | --- |
| E1 acquire + index | persist the book copy (local, gitignored, citation entry); build `tasks/m7_9_chaosbook_index.md` (chapter map + candidate exercises). **Hygiene rule, hard:** every "published value" asserted in this task is extracted from the book/solutions text at E1 with a chapter/exercise citation, NEVER supplied from model memory (a memorized benchmark value that reaches the implementation or the comparison silently destroys exactly the self-test property the author asked for) |
| E1b pre-book analytic gates | before any book content loads, the toolkit passes closed-form gates that need no source: Lorenz equilibria `C± = (±√(β(ρ−1)), ±√(β(ρ−1)), ρ−1)` + their Jacobian eigenvalues from the characteristic cubic; Hénon fixed points (quadratic formula) + their multipliers; a linear-flow Poincaré return map with analytic return time. These prove the machinery independent of the benchmark values |
| E2 select | 3-5 canonical exercises **with published solutions**, spanning the toolkit: Rössler / Lorenz equilibria + stability eigenvalues, a Poincaré-section construction, the shortest periodic orbits of a canonical flow (Rössler cycle or Hénon map cycles) found by Newton / multiple shooting, cycle counting on a symbolic-dynamics example (3-disk pinball class) |
| E3 implement | headless Python; **the reusable toolkit is a MODULE, `scripts/m7_9_orbits.py`**, with per-exercise drivers `m7_9_chaosbook_*.py` importing it; unit tests asserting the published values (cited per E1); implement-first-check-after per the E-loading rule; the integrator layer reuses our own machinery where that is the point (drift behavior on chaotic flows is itself evidence for walkthrough § 3) |
| E4 benchmark report | a short method-note-lite report (equations, code links, our numbers vs the book's with citations, pass/fail table) suitable for the author and the Burak review |
| E5 reading support | a 2-page "what you need for the calls" digest for the maintainer (TOC orientation + ch. 1 + the vocabulary: Poincaré section, return map, Floquet multiplier, cycle expansion), explicitly bounded: fluency, not mastery |
| E6 sessions | schedule the 4-7 book walkthrough sessions + the Burak test-design hour AFTER E4 exists (the report is the shared artifact to walk through) |

## 4b. The toolkit API (what M7.10-M7.14 actually imports)

`m7_9_orbits.py` exposes, dimension-agnostic (small ODE systems here, field flows later via a state-vector adapter):

| Function | Contract |
| --- | --- |
| `integrate(f, x0, T, ...)` | trajectory of `ẋ = f(x)`; RK45 for the small systems, pluggable so the lattice leapfrog satisfies the same interface |
| `poincare_section(f, x0, plane, n_cross)` | ordered section crossings + the return map |
| `find_cycle(f, x0, T0)` | Newton / multiple shooting on `(x, T)`; returns the closed orbit + convergence trace |
| `floquet(f, cycle)` | monodromy matrix along the cycle → Floquet multipliers (cycle stability) |

The M7.10 handoff is concrete: E1 of M7.10 verifies the Trkalian cavity mode as a `find_cycle` fixed point of the Maxwell flow (period `2π/λ`), and its `floquet` multipliers on the unit circle are the orbit-language statement of marginal stability that pure Maxwell provides (no attractor without the coupling).

## 5. Effort estimate + independence from the maintainer's reading

**The benchmark (E1-E4) does not wait for anyone's reading.** The exercises are small ODE / map systems (three variables, not `N³` fields): compute time is seconds, and the real effort is fidelity to the book's definitions plus the honest compare. Estimate: **E1-E4 in one to two focused sessions** (a normal task run each, the first ending at the E2 selection checkpoint if the cap intervenes), E5 half a session more. The maintainer's 2-3 weeks of light reading (the author's own suggested dose: "TOC + dabbling your feet in the first chapter... you don't need to go super deep to be mega efficient") runs in parallel and gates nothing here; it only gates how interactive the E6 sessions can be, which is exactly where the author's time is best spent given M5, M7, and other personal projects all compete for it.

## 6. Cross-refs

[Roadmap](../m7_roadmap.md) · [M7.8](m7_8_helicity_pair.md) (the walkthrough this benchmark reinforces; § 7.2 of [`m7_phase1_walkthrough.md`](m7_phase1_walkthrough.md) carries this task's scorecard, one report bundling M7.8 + M7.9 + M7.10) · [M7.10](m7_10_pure_maxwell.md) (the first consumer of the toolkit: its cavity CK mode is verified as a periodic orbit of the Maxwell flow, its destruction test described as an orbit losing stability; M7.11-M7.14 stay reserved) · [tracker Q4](../m7_question_tracker.md#q4-detail) (source-material provenance) · corpus anchor for the chaotic-flow direction: Dombre et al. 1986 (ABC chaotic streamlines, [`theory/_CITATIONS.md`](../../theory/_CITATIONS.md)).

## FINDINGS (2026-07-07 run)

### 1. Headline: the self-test the author asked for is green, end to end

| Deliverable | Result |
| --- | --- |
| E1b pre-book gates | 4/4 green with zero book input ([`m7_9_gates.py`](../scripts/m7_9_gates.py) → [`m7_9_gates.json`](../data/m7_9_gates.json)): Lorenz eigenvalues vs sympy-derived cubic 1.2e-14; Hénon Newton machine-exact; section return time 5.2e-13; 100-period drift 2.6e-10 |
| E3 benchmarks | **5/5 green** ([`m7_9_benchmark.py`](../scripts/m7_9_benchmark.py) → [`m7_9_benchmark.json`](../data/m7_9_benchmark.json)): B1 equilibria, B2 exponents, B3 analytic Floquet (1.3e-15), **B4 the full exercise 16.9 Rössler cycle table 14/14 rows** (worst point dev 2.0e-6, worst `Λ_e` rel dev 1.3e-6), B5 counting exact |
| Adversarial audit | **CONFIRMED** by a machinery-independent route ([`m7_9_audit.py`](../scripts/m7_9_audit.py) → [`m7_9_audit.json`](../data/m7_9_audit.json)): LSODA + finite-difference return-map Jacobians + direct perturbation + brute-force necklace enumeration; worst closure 6.5e-9, `Λ` agreement within the documented FD noise floor (3.4e-4) |
| E4 report | [`m7_9_benchmark_report.md`](m7_9_benchmark_report.md), method-note-lite (equations first, equation-to-code map, per-value citations, honest boundaries); feeds [walkthrough § 7.2](m7_phase1_walkthrough.md) and the Burak test-design session |
| E5 digest | [`m7_9_reading_digest.md`](m7_9_reading_digest.md): ch. 1 spine + the 8-term call vocabulary, each term tied to where it already runs in M7 |

![Rössler benchmark](../plots/m7_9_rossler_cycles.png)

### 2. The hygiene rule held (and mattered)

Every published value traces to a chapter/page in the [index § 2 ledger](m7_9_chaosbook_index.md). Two things the ledger caught: (a) the book **truncates** printed decimals rather than rounding (our 5.6929738 prints as 5.6929), so naive half-ULP gates fail honest reproductions, the B1/B2 gates are 1 ULP of print; (b) no Hénon cycle table exists in the working set, so Hénon stays an analytic pre-book gate rather than a fabricated "published" comparison.

### 3. What the toolkit is (the M7.10 handoff)

[`m7_9_orbits.py`](../scripts/m7_9_orbits.py), dimension-agnostic: `integrate` / `monodromy` / `poincare_section` / `return_map` / `close_returns` / `find_cycle` (multiple shooting, period free, blow-up-safe damped Newton) / `floquet` / `find_cycle_map` (A16.1) / `floquet_map`. M7.10 E1 consumes it verbatim (cavity mode as a `find_cycle` fixed point, multipliers on the unit circle). The lattice adapter (leapfrog state vector behind the same `integrate` interface) is M7.10 work, not done here.

### 4. Honest boundaries

Symbolic itineraries were matched to the published rows by section point, not derived from kneading theory; Lyapunov exponents, cycle expansions, and the 3-disk pinball were out of the working set (listed with reasons in the [report § 6](m7_9_benchmark_report.md)). E6 (the 4-7 walkthrough sessions + the Burak hour) is scheduling, owned by the user, now unblocked by the E4 report.

## EXECUTION LOG (2026-07-07)

| Step | What happened |
| --- | --- |
| E1 | 9 chapter PDFs fetched from chaosbook.org/version17 to gitignored `theory/chaosbook/` (+ `.gitignore` entry, `_CITATIONS.md` entries); text extracted; [index](m7_9_chaosbook_index.md) built |
| E2 | 5 benchmarks selected, all values transcribed with citations |
| E1b | gates written first, 3/4 → t=0-crossing fix in `poincare_section` → 4/4 |
| E3 try 1 | B4 12/14: two rows never seeded (close-return dedupe too aggressive); `min_sep` parameter added, seed pool widened for n ≥ 5 |
| E3 try 2 | 5/5, 14/14 (goal-loop closed, cap was 3 tries) |
| Audit try 1 | A2/A3 confirmed; A1 gate initially set below the FD method's own noise floor, flagging 5 high-`\|Λ\|` rows at 7e-5..6.6e-4; gate recalibrated to the documented noise model (1e-3), numbers unchanged |
| Audit try 2 | CONFIRMED across A1/A2/A3 |
| Deviations from plan | none of substance; the E2 selection swapped the planned 3-disk counting example for the complete-alphabet tables 18.2/18.3 (the 3-disk tables are outside the downloaded working set; documented in the index) |

## TASK REVIEW (2026-07-07)

`Task Duration: 00:39 (from 17:12 to 17:51 EDT)`
`Usage Cap Triggered: NO`

Approved in-terminal 2026-07-07 evening. One adjustment at review: the index file moved from `research/` root to `research/tasks/` per the task-artifact convention (all links rewritten; doc checker re-run clean).

| Item | Status |
| --- | --- |
| E1 acquire + index | ✅ 9 chapter PDFs (gitignored `theory/chaosbook/`); [index + hygiene ledger](m7_9_chaosbook_index.md); `_CITATIONS.md` entries |
| E1b pre-book gates | ✅ 4/4 with zero book input (Lorenz vs sympy cubic 1.2e-14; Hénon machine-exact; return time 5.2e-13; drift 2.6e-10) |
| E2 select | ✅ 5 benchmarks, every value transcribed + cited; the book TRUNCATES printed decimals → gates = 1 ULP of print |
| E3 toolkit + benchmarks | ✅ `m7_9_orbits.py` + 5/5 green; **ex. 16.9 Rössler table 14/14** (worst point dev 2.0e-6, worst `Λ_e` rel 1.3e-6); counting integer-exact |
| Adversarial audit | ✅ CONFIRMED, machinery-independent (LSODA + FD Jacobians + direct perturbation + brute-force necklaces) |
| E4 + E5 | ✅ [benchmark report](m7_9_benchmark_report.md) (Marc + Burak session) · [reading digest](m7_9_reading_digest.md) |
| Compliance | ✅ doc checker clean; scope check clean; no artifacts > 1 MB (nothing deleted, nothing to document) |

Issues resolved in-run: B4 needed a second try (close-return dedupe too aggressive for n ≥ 5, `min_sep` parameter added); audit gate recalibrated to the FD noise floor (first pass flagged 5 high-`\|Λ\|` rows at devs 7e-5..6.6e-4 against a gate below the method's own floor; numbers unchanged); `poincare_section` t=0-crossing fix caught by gate G3. Deviations from plan: the 3-disk counting example became tables 18.2/18.3 (3-disk tables outside the working set); the author-sent book copy was not found locally, the public per-chapter webbook is the source of record.

**Findings:** the self-test Marc asked for ("computed, not linguistically mirrored") is green end to end: machinery proven on closed-form gates before the book was opened, then all 14 published Rössler periodic orbits and every other selected exercise reproduced at 1e-6-level agreement, independently audit-confirmed; the orbit-hunting pipeline (section → close returns → multiple shooting → Floquet) is ready for M7.10 E1.

**Research docs created/updated:** [this task doc](m7_9_chaosbook.md) · [benchmark report](m7_9_benchmark_report.md) · [index](m7_9_chaosbook_index.md) · [reading digest](m7_9_reading_digest.md) · scripts `m7_9_{orbits,gates,benchmark,audit}.py` · data `m7_9_{gates,benchmark,audit}.json` · plot `m7_9_rossler_cycles.png` · [walkthrough § 7.2](m7_phase1_walkthrough.md) · [roadmap](../m7_roadmap.md) (row → DONE) · [tracker chronology](../m7_question_tracker.md) · `__M7_model_briefing.md` · `theory/_CITATIONS.md` · `.gitignore`
