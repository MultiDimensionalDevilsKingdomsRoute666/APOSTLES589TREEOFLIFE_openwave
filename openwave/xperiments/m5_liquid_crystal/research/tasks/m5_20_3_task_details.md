# M5.20.3: the 4×4 oscillation run: the constrained clock + radius breathing

**Status**: roadmap row at the top of [BACKLOG](../m5_roadmap.md) (PLAN-ready). Opens on Duda's constraint answer (promised for his morning of 2026-07-13, roughly 00:00-01:00 EDT) + the user's "go".

**Lineage**: [M5.20.2](m5_20_2_task_details.md) (the derived EOM, the boost runaway, the exact H(ω) clock, THE one question) · [M5.20.1](m5_20_1_task_details.md) (the spatial verdict + the measured core selection) · convo record [`m5_20_convo.md`](m5_20_convo.md) (the 2026-07-12 evening entry carries this plan's newest inputs: a ≈ δ/2 named, the radius-breathing mechanism) · combined outbound note [`../findings/m5_20_2_method_note.md`](../findings/m5_20_2_method_note.md) (§ II.3 = the question this task waits on) · tracker [Q18](../m5_question_tracker.md#q18-detail) / [Q19](../m5_question_tracker.md#q19-detail) / [Q23](../m5_question_tracker.md#q23-detail).

## TASK PLANNING (2026-07-12 evening, pre-go)

### Scope

Implement whatever constraint Duda names for the boost sector, re-verify well-posedness under it (the triage ladder), then run the first 4×4 `(g, 1, δ, 0)` oscillation production on the audited axisym stack and measure the oscillation observables he has now spec'd. Three deliverable measurements, in priority order:

| # | Measurement | His spec (2026-07-12 evening reply) |
| --- | --- | --- |
| 1 | Endpoint core spectrum from free minimization | "(g, 1, a, a) for a ~ delta/2": the first time the core VALUE is named; M5.20.1 already measured (1, δ/2, δ/2) in 3D, this task tests it in 4D under the constraint |
| 2 | Loop-radius breathing at conserved total energy | "radius of loop can also oscillate - to maintain total energy, which is density per length depending on flavor, times loop length": measure R(t), E/length, and their exchange |
| 3 | Oscillation spectra vs the 4×4 gap ladder | FFT of R(t) and of the core-spectrum trajectory λ_i(t), compared against the measured ladder ω = {0.0093, 0.0466, 0.1349, 78.28} |

NOT in scope: the full AMBer flavor fit (pre-registered as the long-run target, this task reports qualitatively only; observables scoreboard in [`../../theory/_CITATIONS.md`](../../theory/_CITATIONS.md), local `amber_neutrino_flavor_rl.pdf`); the flavor naming (which core state = e/μ/τ is author-gated, the note says "core states"); charges (3-equal core) and black holes (4-equal core, his regularization ladder): later tasks.

### Definition of done

| ✅ when | Bar |
| --- | --- |
| Constraint implemented + machine-checked | Implemented exactly as sanctioned, derivation section gated against the M5.18-verified Lagrangian (the M5.20.2 GB-gate pattern) |
| Well-posedness re-triaged UNDER the constraint | T1 dt scaling (max-deviation criterion, dt² ratios) + T2/T3 injection reruns: the boost runaway must be CLOSED by the constraint; GO/NO-GO pre-registered, production only on GO |
| Production oscillation runs landed | δ = 0.3 primary (the audit-clean regime) + one companion δ; T = 2000 baseline, dt ≤ 0.01 (the stiff g-mode ω = 78.28 bound); energy ledger ≤ 1e-5; seed + endpoint cross-section prints (flow-doc rule 2026-07-12) |
| The three measurements reported honestly | Core gate vs a ≈ δ/2; R(t) + E/length vs his conservation mechanism; spectra quoted WITH the FFT bin width Δω (the refuted "0.2% on-the-line" lesson) |
| Method note + audit + routing | New note `../findings/m5_20_3_method_note.md` (FIELD CONTENT box up front, plots embedded as they exist), independent adversarial audit (own instruments), tracker Q18/Q19/Q23 resolution routing, convo entry, outbound draft timed to land before 14:00 EDT (the comms window) |

### Gating

Roadmap `Gated By`: **Duda's constraint answer** (the Q18 + Q19 + Q23 fusion sent 2026-07-12) + user "go". At go: log his email verbatim + decode in [`m5_20_convo.md`](m5_20_convo.md), pick the folding-table row, move the roadmap row to In Progress, arm the resume ping, open `../checkpoints/m5_20_3_progress.md`.

### The constraint folding table (branch on his answer; pick ONE row at go)

| His answer names | Implementation | Cost |
| --- | --- | --- |
| Dirac treatment of the primary constraint (Ṁ ∝ η null direction) | Constrained integrator: project Ṁ onto the constraint surface each step (the M5.8.2c spectral-projection precedent); the projection energy ledger becomes its own gate | Heaviest: new gate ladder before production |
| Restriction to rotation orbits (the K_eff > 0 sector) | Dynamics on the rotation-generated subspace, or a penalty/projection removing boost directions from Ṁ | Medium: the generator split already exists in `m5_20_2_c_clock.py` |
| A branch or sign choice we missed (e.g. one_timelike, an η-convention flip) | Rerun the K_eff census on the sanctioned branch FIRST (minutes); if boosts turn positive there, unconstrained dynamics is back on and the task simplifies | Cheapest: census before any integrator work |
| The clock is ansatz-level (rigid orbits only) | No unstable integration at all: extend the exact H(ω) machinery; radius breathing = a quasi-static ladder of constrained minima in R | Light: statics stack exists (`m5_20_1_c_statics.py` FIRE) |
| Energy-minimization-first (the hint in his quick reply: "everything should come from energy minimization") | Constrained descent (FIRE/gradient flow) at fixed winding + fixed E_total; R(t) read from the quasi-static sequence | Light-medium |
| The answer does not close the sector | The hard cap fires (M5.20.2 precedent): document what his answer does give, ship partials + ONE sharp follow-up question | Bounded |

### THE ANSWER (2026-07-13/14, logged in [`m5_20_convo.md`](m5_20_convo.md)): the row that fires

His answer (group-cc'd 2026-07-13 evening): **"We don't want to add artificial restrictions, everything should come from evolution of field configuration of particle using assumed Lagrangian."** Decoded against the table: the **Dirac-treatment row fires, amended**: run free Euler-Lagrange evolution of HIS purely-quartic L (NOT the canonical completion), where handling the degenerate Legendre map (Ṁ ∝ η exact null, the M5.18-verified primary constraint) is the theory's OWN structure, not an added restriction: invert K(M) on its range / project the null direction, gate the projection ledger. His negative-Hamiltonian acknowledgment ("difficult to avoid in 3+1D, and seem necessary to propel neutrino oscillations or electron angular momentum") CONFIRMS the M5.20.2 census as physical.

| His prescription | Task consequence |
| --- | --- |
| Start: energy-minimized 3D vortex loop, extended to 4D by adding the 0th axis with the g eigenvalue in the time direction | Phase A/B seed = the M5.20.1 relaxed 3D loop states (or a fresh relax) with the block-diagonal −g time row; NO 4-target-imposed core: minimization decides (the measured-not-manual line stands) |
| Then: free EL evolution; expected to "stabilize leaving mostly neutrino oscillations, maybe also radiation (in neutrino rest frame)"; compare with experimental data | The production run + the pre-registered observables (R(t) breathing at conserved E_total, spectra vs the gap ladder, the a ≈ δ/2 core gate) |
| If the loop shrinks to R = 0 and vanishes: "calculate duration of such process" (time dilation makes lab-frame durations long for ultrarelativistic neutrinos) | Unwind DURATION becomes a first-class observable, not a failure: M5.20.1's measured unwind half-life (t ≈ 125-375) is the first draft of this number; re-measure under the quartic-kinetic EL evolution |
| If EL dives to −∞ energy: least-action two-point BVP (S-matrix style, fix initial + final configurations; "much more difficult") | Out of this task's scope: recorded as the successor branch if G-RUNAWAY fails under the true-L evolution |
| His two 3D→4D checks (direct email, 2026-07-14 morning): SO(1,3) not SO(4); η inside the trace products + modified c_p | ✅ BOTH already implemented + machine-verified: M5.18 check 1 (random boost + rotation, Λ ∈ SO(1,3), invariance ~1e-11, no-eta negative control 1b) and `v4_density` (powers of ηM = Tr((ηM)^p); C_p from the η-spectrum: g^p + 1 + δ^p). The next outbound answers both with equation-to-code permalinks |

Preconditions row updated: the answer is logged + decoded, the folding row is chosen. **Remaining gate: user "go".** The implementation weight shifts phase A to the quartic-kinetic EOM (K(M) M̈ term from his L, null direction projected): heavier than the canonical stack but exactly the M5.20.2-derived machinery (`kin_form_apply` is K(M) applied; its census already measured rank + negativity per state).

### Pre-registered gates

| Gate | Criterion |
| --- | --- |
| GC0 constraint consistency | The constrained EOM reduces to the M5.20.2 derived EOM when the constraint is inactive; FD gradient/force checks at 1e-7 level |
| GC1 census under constraint | K_eff census rerun with the constraint active: the boost sector must read closed (no negative unbounded directions reachable) |
| G-RUNAWAY | T2/T3 injection reruns under the constraint: no divergence over T = 400 (the t ≈ 21 runaway must be gone, not delayed) |
| G-DT | dt² max-deviation scaling (the patched T1 criterion); production dt ≤ 0.01 |
| G-CORE | Endpoint core spectrum reads (g, 1, a, a) with a ≈ δ/2 from free minimization; genuine-regime bar δ ≥ 0.3 (the M5.20.1 audit caveat: vacuum-confounded below) |
| G-RADIUS | Energy ledger ≤ 1e-5 while R(t) varies; test E_total ≈ (E/length) × 2πR against the measured trajectory |
| G-SPECTRUM | Every frequency claim quoted with Δω (bin width) and window length; band language, never "on-the-line", unless the peak is resolved by ≥ 3 bins |
| Cross-sections | Seed t = 0 AND endpoint field-state prints, embedded in the note (run-evidence rule) |

### Blindspot pass (unfamiliar territory: constrained 4×4 dynamics + oscillation observables)

| # | Unknown unknown surfaced | Fold into plan |
| --- | --- | --- |
| 1 | **The timescale race**: the spatial sector unwinds (pair_d0 half-life t ≈ 125-375; gap-ladder periods 2π/ω ≈ 47-676): the loop may unwind before one radius-oscillation period completes, unless the constraint changes protection | Measure BOTH clocks per run (unwind time vs oscillation period); a "unwinds first" outcome is a reportable result, not a failed run |
| 2 | Axisymmetry represents R(t) (the ring radius is a cross-section coordinate) but FORBIDS non-axisym decay channels and flavor modes | Scope-box in the note § honesty section, same pattern as M5.20.x § 4 |
| 3 | Constraint-projection integrators are not symplectic: the energy ledger cannot be inherited from the unconstrained stack | G-RADIUS re-validates the ledger UNDER the constraint before production |
| 4 | The g value: M5.20.2 used the engine-convention g; his answer may fix g differently (it sets the stiff mode ω = 78.28 and the dt bound) | One-census sensitivity spot-check at an alternate g (minutes); dt bound recomputed from the measured stiff ω |
| 5 | Wall-clock: M5.20.x production was ~4.5 h for 10 runs; the send window is 14:00 EDT | Production matrix capped at ~6 runs; primary δ = 0.3 first so the headline lands even if the tail is cut |
| 6 | Seeds: the M5.20.1 endpoint `_state.npz` files were deleted at close (> 1 MB rule) | Fresh seeds from the loop builder are the default; remnant states regenerate via `python3 m5_20_1_d_dynamics.py run <δ> <pairing> 2000 <mode>` if needed |

### Unknowns quadrants self-test

| Quadrant | Biggest unknown | Route |
| --- | --- | --- |
| Known knowns | EOM, gap map, dt bound, seeds, census machinery (M5.20.2 assets, frozen) | Reuse; GC0 guards the join |
| Known unknowns | THE constraint (author-gated, inbound tonight); δ value (sweep stands); whether a ≈ δ/2 emerges in 4D (machine-checkable) | Folding table; G-CORE |
| Unknown knowns | The user's delivery bar, now explicit: ONE Duda-legible note, 4×4 reinforced, outbound lands before 14:00 EDT | Wired into DoD |
| Unknown unknowns | The blindspot list above; whatever the audit finds | Deviations log at EXECUTE + independent adversarial audit at FINISH (cardinal rule) |

### Research-body destinations

| Artifact | Destination |
| --- | --- |
| Scripts | `../scripts/m5_20_3_a_constraint.py` (implementation + GC gates) · `m5_20_3_b_triage.py` · `m5_20_3_c_production.py` · `m5_20_3_d_observables.py` (R(t) tracker, E/length, core trajectory, spectra) · `m5_20_3_plots.py` |
| Data / plots | `../data/m5_20_3_*.json` (+ logs; > 1 MB raw deleted at FINISH with regen docs) · `../plots/m5_20_3_*.png` |
| Findings | `../findings/m5_20_3_method_note.md` (new note; the combined M5.20.x note stays the Part I + II record and gets a forward link) |
| Records | This file (FINDINGS + TASK REVIEW) · `m5_20_convo.md` (his answer + the outbound) · tracker Q18/Q19/Q23 · `../checkpoints/m5_20_3_progress.md` (opens at go, resume-complete for a model switch) |

### Sub-experiments (phase plan)

| Phase | Content | Gate |
| --- | --- | --- |
| A | Constraint implementation from his answer (folding-table row) + derivation section | GC0, GC1 |
| B | Triage under the constraint: T1 dt / T2 injections / T3 textures | G-RUNAWAY, G-DT → GO/NO-GO |
| C | Production: δ = 0.3 primary + one companion, T = 2000, closed box; cross-section prints | Energy ledger, G-CORE |
| D | Observables: R(t), E/length, λ_i(ρ→0, t), spectra vs the gap ladder | G-RADIUS, G-SPECTRUM |
| E | Method note + independent adversarial audit + routing + outbound draft | Doc checker exit 0; audit verdicts folded |

### Preconditions

| Precondition | State |
| --- | --- |
| Duda's morning email logged + decoded, folding row chosen | ✅ 2026-07-14 (three messages; § THE ANSWER above; [`m5_20_convo.md`](m5_20_convo.md)) |
| M5.20.2 assets on disk (`m5_20_2_a_eom.py`, hessian4, k_eff, protection machinery) | ✅ frozen at close |
| AMBer scoreboard reference | ✅ `../../theory/_CITATIONS.md` + local PDF |
| Resume ping + checkpoint file | 🚧 at go (user supplies resets_at) |

### Model + effort

Fable 5 high for Phase A (novel constraint derivation) and the audit brief; default effort for B-D (mechanical production against pre-registered gates, try cap 3 per gate). Independent agent with own instruments for the audit (cardinal rule).

### Contingencies + comms

| Trigger | Action |
| --- | --- |
| Hard cap (~1 day) | Ship partials + ONE sharp follow-up question (M5.20.2 precedent) |
| Fable-cap model switch mid-run | Checkpoint file is resume-complete (decision tree, relaunch commands); detached production processes survive |
| Results ready after ~13:00 EDT | Flag to the maintainer: holding for the next-day 14:00 EDT send costs nothing (deeper replies arrive his morning either way) |
| Outbound content | Next email opens with the brief timing apology (maintainer-voice bullet) + the one-sentence "measured, not manual" clarification + the a ≈ δ/2 prediction-confirmed line, then this task's results |

## M5.21 findings feed (2026-07-14, folded pre-go)

> **The decisive framing (measured at M5.21, seeded here by the user 2026-07-14): containment is exactly what the constraint must buy, and that is now a measured statement, not a hunch.** In the unconstrained canonical stack the defect's energy is not contained: the statics is a saddle-slide and a kinetic clock kick radiates away, while the topological charge and an intrinsic core-breathing oscillation survive. This task lands the constraint on the LOOP; [M5.21.1](m5_21_task_details.md) then puts the same constraint on the ELECTRON and reruns the identical clock-vs-noclock comparison against the M5.21 baseline. If the constrained clock contains the energy where the unconstrained kick radiated, that is "the particle clock creating particle stability" on film.

Series framing: [`../m5_particle_hunt.md`](../m5_particle_hunt.md) (M5.20 = the vortex-loop hunt, possibly the neutrino; M5.21 = the hedgehog hunt, possibly the electron). [M5.21](m5_21_task_details.md) (the electron particle-clock film strip, closed 2026-07-14) ran the SAME canonical-completion stack on the hedgehog and produced inputs this task should use. **Presentation boundary (user, 2026-07-14, SUPERSEDED same day by the film standard [`../m5_visualization.md`](../m5_visualization.md): both series now emit template-based film strips): the M5.20 series KEEPS its own cross-section spec** (the [`m5_20_1_seed_maps.png`](../plots/m5_20_1_seed_maps.png) / [`m5_20_1_endpoints.png`](../plots/m5_20_1_endpoints.png) seed + endpoint map format); the M5.21 film-strip panel format stays M5.21-series-only for now. **Reciprocal series rule: every M5.21-series run re-captures the latest M5.20-series results at PLAN.**

| M5.21 finding | Use in this task |
| --- | --- |
| The boost sector stayed EXACTLY 0.0 through 4 rotation-sector runs on full defect nonlinearity (noclock / twist ω=0.05 T=400 / global-axis / gentle) | Strengthens the census quarantine: rotation-sector dynamics alone never wakes the runaway; the constraint's job is specifically the boost/time sector, as framed in the folding table |
| The core of a defect RINGS coherently at ω ≈ 0.11-0.13, near (~15% below) the 0.1349 activated-face rung; softening consistent with large-amplitude anharmonicity; intrinsic (no clock kick needed) | Direct rehearsal for the radius-breathing + spectra observables: expect the measured lines NEAR but BELOW the analytic ladder at large amplitude; keep the FFT-bin honesty + quadratic-detrend + sub-bin parabolic-peak method (in [`../scripts/m5_21_c_clockrun.py`](../scripts/m5_21_c_clockrun.py) analysis and the checkpoint FFT snippets) |
| An unconstrained velocity kick (kinetic clock) stalls in ~1 sweep and radiates; it never becomes a persistent internal rotation | Sharpens the folding-table framing: the constraint is load-bearing for ANY persistent clock, not just for boost-sector safety; the oscillation production should not expect seeded rates to persist without it |
| dt = 0.02 gave ledgers 1e-6 to 4e-6 over T ≤ 400 with the time row on-branch (the 78.28 stiff mode never excited when unforced) | GD-triage prior: start the dt scan at (0.02, 0.01, 0.005); the stiff bound binds only if the constraint activates the time eigenvalue |
| Real-FD gradient checks hit a ~5e-6 roundoff floor at the g⁴ trace scale; the energy is polynomial in M, so COMPLEX-STEP directional derivatives are exact (1.75e-15 measured) | Gate any new constrained-EOM gradient with complex-step, not real FD (pattern in [`../scripts/m5_21_d_3dcheck.py`](../scripts/m5_21_d_3dcheck.py) `gate_gd3a`) |
| The fixed-radius meridional winding read branch-swaps (±1/0 flips) where λ1 ≈ λ2 after churn; endpoint-only reads mislead | The loop winding measure here (`winding_measure_biax`, multi-r_w) should keep the multi-radius + endpoint-plus-trace practice; treat single-radius q dips as suspect before calling unwinding |

## FINDINGS (2026-07-14)

Full technical record: [`../findings/m5_20_3_method_note.md`](../findings/m5_20_3_method_note.md) (equations first, code map, figures, audit). Instrument: the free-EL (true-L) dynamics stack [`../scripts/m5_20_3_a_constraint.py`](../scripts/m5_20_3_a_constraint.py), gates GC0a-e all PASS at complex-step precision (4e-16 to 7e-18).

### The headline: the free-EL IVP of the purely-quartic L is ill-posed, and every regularization blows up in finite time

| # | Finding | Status |
| --- | --- | --- |
| 1 | **The kinetic form K(M) is rank 5/10 EXACTLY on the loop background** (machine-zero nulls, first active eigenvalue ≥ 0.17 of cell max; rank 8 at core), with structural negative-inertia directions (two exact ± pairs + one unpaired positive on the vacuum: the η-signature; audit-corrected phrasing) and **98.6% of the static force in null(K) at from-rest release** | ✅ measured (GC1 census) |
| 2 | **Unregularized: blowup in a fixed STEP COUNT** (~3 steps at any dt, amplitude-independent over 3 decades): unbounded RHS, no Lipschitz bound: **the initial-value problem is ill-posed** | ✅ measured |
| 3 | **Regularized (any cutoff): genuine finite-time blowup**: t* dt-robust (1.96/1.9375/1.93125 at rc 1e-2); audit-CONFIRMED with an independent RK4 integrator AND a Tikhonov-damped alternative null treatment (t* = 1.825: not a projection artifact); t*(cutoff) monotone 0.08 → 3.4 (raw), 0.02 → 7.2 (recipe), NO plateau; every defect background blows (loop, recipe, unwound remnant, vacuum + time-mixing textures); the ONE stable case: a pure rotation-sector texture on the vacuum (T = 50, both dts, rc 1e-2) | ✅ measured |
| 4 | **The blowup dives to E → −∞, and the MECHANISM is measured**: a roundoff-seeded exponentially unstable boost-sector (time-mixing) mode on every non-vacuum background, rates σ = 6.31 to 80.9/t (cutoff-dependent); **t\* ≈ onset + ln(0.1/1e-16)/σ reproduces every blowup time** (E conserved to ≤ 5e-5 through 87% of life, drift not dt²-clean: projection-set chatter; the mode goes nonlinear at O(0.1) and the singularity fires): **exactly the owner's pre-named branch** ("if EL dives to −∞ → least-action BVP") | ✅ measured |
| 5 | **The topological charge NEVER unwinds through the blowup**: q_r4 = 0.500 exact at every finite snapshot at rc 1e-2 (canonical stack: unwound 10/10); at rc 1e-1 q = 0.500 through the trusted read window, then the degeneracy guard declines (no unwinding signature; churn-read caveat applied). The unwinding force has no inertia channel under the true L (finding 1) | ✅ measured |
| 6 | **G-CORE lands at the statics level**: frozen-time-row minimization at the intact-loop point reads (g, 1, a, a) with **a = 0.1269 = 0.85 × δ/2** (his a ≈ δ/2 prediction), pair split 0.021, box-independent 4e-10; the pair SPLITS as the loop dissolves (the equalized core is the LOOP's property) | ✅ measured |
| 7 | **The true-L vacuum ladder is ρ-CHIRPED**: ω₁(ρ) = 0.0674·ρ exactly through the origin (K10 ∝ ρ^−2.00 from the equivariant background); no negative ω² on the vacuum; replaces the flat canonical ladder for any spectral comparison (axisym sector) | ✅ measured |
| 8 | ~~Free 4D static minimization dives to E → −∞~~ **RETRACTED at audit (C8 REFUTED)**: the FIRE dive was a step-size instability (adaptive dt crossed the 2/√λ_max ≈ 0.0256 stiff-mode bound); monotone GD / L-BFGS / dt-capped FIRE all stay bounded from this seed. The M5.18 indefiniteness statement stands as M5.18's result only | ❌ retracted |
| 9 | The from-rest EL-inconsistency (finding 1) suggests the theory's consistent initial data lives on a Dirac secondary-constraint surface (RHS_null = 0); not derived here | 🔶 hypothesis |

### Deviations from the plan (logged as they happened)

| # | Deviation | Why |
| --- | --- | --- |
| 1 | GC1's "boost sector must read closed" criterion reinterpreted as a recorded census | his answer forbids added restrictions; the degeneracy structure IS the physics under test |
| 2 | GC0's "reduces to the M5.20.2 EOM" replaced by complex-step force/gradient/identity gates | the true-L EOM does not reduce to the canonical completion; the static sector reuse (GB0 lineage) is the actual join |
| 3 | T1 dts moved to (0.02, 0.01, 0.005) then the whole triage redesigned as B1-B5 discriminators | the first run blew up: the triage became the measurement |
| 4 | The recipe seed = the it-500 frozen-time-row relax state (q = 0.500 intact, E 2.68 → 0.34), not the full relax | full relaxation dissolves the loop (statics negative reproduced at 64×128); "energy-minimized loop" is otherwise not a loop |
| 5 | Phase C production re-scoped to the 4 instrumented anatomy runs up to t* | the pre-registered T = 2000 oscillation production is unreachable (headline) |
| 6 | Phase D re-scoped: G-RADIUS/G-SPECTRUM recorded NOT REACHED; core gate answered in statics; the chirped ladder replaces the flat-ladder comparison | honesty over ritual: the observables that survive are delivered, the rest declared |
| 7 | 64×128 primary grid (not 128×256) | the blowup verdict is grid-cheap; D1 box-independence spot-checked at 128×256; wall-clock spent on discriminators instead |
| 8 | The film-strip standard created mid-run (user direction, 2026-07-14): [`../m5_visualization.md`](../m5_visualization.md) + `m5_film.py`; `m5_20_3_sections.png` regenerated as a 6-frame basic-template strip | standardizes cross-series visualization; the per-series presentation boundary superseded |

### Data + large-file log

All `m5_20_3_*` data files are < 1 MB (summary JSONs + 8 small npz states); nothing deleted. Regen commands in the method note § 9.

## TASK REVIEW (2026-07-14, approved same day)

Task Duration: 03:42 (from 10:43 to 14:25 EDT)
Usage Cap Triggered: NO

| # | Result | Status |
| --- | --- | --- |
| 1 | The true-L instrument (free EL of the purely-quartic verified L, per-cell spectral solve, exact null-projection bookkeeping); GC0a-e at complex-step precision (4e-16 to 7e-18) | ✅ measured |
| 2 | **THE HEADLINE: the free-EL IVP is ill-posed; every regularization blows up in finite time, E → −∞: his pre-named BVP branch fires.** Rank-5-exact K(M); 98.6% null-force at rest; the roundoff-seeded boost-sector exponential (σ = 6.31-80.9/t, the t* law); audit-confirmed incl. independent RK4 + Tikhonov | ✅ measured |
| 3 | The topological charge NEVER unwinds through the blowup (q = 0.500 exact; canonical stack unwound 10/10) | ✅ measured |
| 4 | G-CORE: (g, 1, a, a) with a = 0.1269 = 0.85 × δ/2 from free minimization, box-independent 4e-10 | ✅ measured |
| 5 | The ρ-chirped true-L vacuum ladder: ω₁ = 0.0674·ρ exact (K ∝ ρ⁻², audit-proven) | ✅ measured |
| 6 | One stable evolution: rotation-sector texture on the vacuum (T = 50, both dts) | ✅ measured |
| 7 | G-RADIUS + G-SPECTRUM: NOT REACHED (honest disposition); unwind duration = regularization-dependent, undefined without the BVP | ❌ not reached |
| 8 | From-rest EL-inconsistency → Dirac secondary-constraint surface as consistent initial data | 🔶 hypothesis |
| 9 | First-draft "4D statics dive" | ❌ RETRACTED at audit (C8: FIRE step-size artifact) |

Audit: 6 CONFIRMED / 2 QUALIFIED / 1 REFUTED (method note § 8); all corrections folded and marked in place. Deviations: 8, logged in § FINDINGS. Mid-run additions at user direction: the film-strip standard ([`../m5_visualization.md`](../m5_visualization.md), `m5_film.py`, the 7-row blowup spacing) + the two-hunt Candidate-Score scorecard ([`../m5_particle_hunt.md`](../m5_particle_hunt.md)).

**Findings**: running Duda's prescription verbatim produced a decisive structural negative with three positives riding it: the free-EL dynamics of his quartic Lagrangian cannot serve as the theory's time evolution (his own least-action BVP is the formulation left standing, opened as [Q24](../m5_question_tracker.md#q24-detail)); the topological charge proved unconditionally protected under the true kinetic form; his core prediction landed quantitatively at statics (a = 0.85 δ/2); the vacuum spectrum acquired a falsifiable new shape (ρ-chirped). Both particle hunts now funnel into the single Q24 blocker.

**Research docs created/updated**: this file · [`../findings/m5_20_3_method_note.md`](../findings/m5_20_3_method_note.md) · [`../m5_visualization.md`](../m5_visualization.md) · [`../m5_particle_hunt.md`](../m5_particle_hunt.md) · [`../m5_question_tracker.md`](../m5_question_tracker.md) (Q24) · [`m5_20_convo.md`](m5_20_convo.md) (the outbound draft, user-gated) · [`../m5_roadmap.md`](../m5_roadmap.md) · scripts `m5_20_3_a/b/c/d_*.py`, `m5_film.py`, `m5_20_3_audit_check.py` + `data/m5_20_3_*` + `plots/m5_20_3_*`.
