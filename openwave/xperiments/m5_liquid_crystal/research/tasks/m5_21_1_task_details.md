# M5.21.1: the electron hedgehog under the author's 2026-07-15 prescription (M5.21 phase 2)

**Status**: ✅ CLOSED 2026-07-16 (review approved same day; roadmap row in Done). All phases P0-P4 measured, films both templates rendered, adversarial audit run. Findings below; full record: [`../findings/m5_21_1_method_note.md`](../findings/m5_21_1_method_note.md). This plan REPLACES the earlier M5.21.1 framing (free-EL true-L clock on the electron): his redirect prescribes **minimization-first** (3D statics → 4D extension by energy minimization), which sidesteps the ill-posed IVP measured at [M5.20.3](m5_20_3_task_details.md). The free-EL clock question survives inside phase P2 as the orbit-class read, not as raw time integration.

**Lineage**: [M5.21](m5_21_task_details.md) (phase 1: snapshot instrument + the canonical-stack baseline: core rings ω ≈ 0.11-0.13, boost sector exactly 0.0, statics = a Q8 slide) · the M5.20 series kills that make minimization-first the honest route (M5.20.3 ill-posed IVP; M5.20.5 rigid-orbit level out) · [M5.17 phase D](m5_17_task_details.md) (the Fig. 9 ansatz transcription + conformance) · canonical [`../m5_theory_canonical.md`](../m5_theory_canonical.md) § 2 rows 4/4b.

## HIS PRESCRIPTION (2026-07-15, verbatim anchors)

| Element | His words (2026-07-15) | Measured object |
| --- | --- | --- |
| The object | "electron as hedgehog - which (in contrast to neutrino) has to be stable" | STABILITY is his own pre-registered bar: if the statics dissolves it, that is a formulation-level finding |
| The ansatz | "biaxial hedgehog ansatz for Gx, Gy, Gz rotation generators (from Fig. 9 in arXiv:2108.07896)" | `M = O·D·Oᵀ`, spatial `D = diag(1, δ, 0)`, `O = exp(θG_z)·exp(φG_y)·exp(ψG_x)` (M5.17 phase D transcription, conformance-checked) |
| Core structure | "vortex in z axis - requires regularization with two equal eigenvalues, and in the center all three spatial eigenvalues have to be equal" | 2-equal along the z-vortex line, 3-equal at the center (the M5.21 measured seed-adjacent core a = 0.4338 vs (1+δ)/3 = 0.4333 is the transient of exactly this) |
| Mass distribution | "its 511keV mass mainly in the center, vortex should be extremely light" (pairing opposite spins / Cooper pairs) | E(r) concentration (r50/r90) + the vortex-line energy per length |
| The chain | "minimizing energy in 3D ... getting static solution, then extending to 4D - where energy minimization should lead to angular momentum + gravitational mass" | P1 → P2 below |
| The twist limit | "For perpendicular low energy twists (as quantum phase) you should get Klein-Gordon-like equation" | P3 below (the canonical already carries the KG-is-geometric reproduction on the old spec; re-read on the new one) |

## TASK PLANNING (2026-07-16 draft; finalize at go)

### The M5.20-series re-capture (series rule, folded at PLAN)

| Lesson (M5.20.3-5, all audited) | How it binds this task |
| --- | --- |
| The free-EL IVP of the quartic L is ILL-POSED on non-trivial backgrounds (roundoff-seeded boost-sector exponential, E → −∞ in finite time) | NO raw time integration anywhere in this task; dynamics enters only as minimization, orbit classes, or spectra. The M5.21 baseline's boost-sector-exactly-0.0 does NOT license an IVP: the loop's blowup grew from rounding noise |
| The rigid conjugation-orbit level is measured OUT on the loop (directional block: static force 99.9997% time-row) | The a2x alignment diagnostic is on disk and cheap: run it on the HEDGEHOG background before believing any orbit-class claim (the hedgehog's static-force sector split is an open measurement, not assumed equal to the loop's) |
| The φ-averaged kinetic (band-limit gated, nphi = 5 exact) + the s2/qc EL library (9 gates ≤ 8e-16) | Reused as-is wherever 4D kinetic reads appear; band limits GATED, never assumed (the nphi lesson) |
| q never unwinds through blowups; winding instruments validated | The charge-1 hedgehog winding read carries over from M5.21 |
| Film standard | Every state-evolving figure via `m5_film.film_strip`; **BOTH templates, `basic` AND `thermal`** ([`../m5_visualization.md`](../m5_visualization.md)), first row t = 0 |

### Steps

| Step | Content | Kill / survive (pre-registered) |
| --- | --- | --- |
| P0 | **The `(-g)^p` spec correction, both signs (his correction 1)**: potential targets from the η-spectrum of BOTH branch representatives, `ηM = diag(+g,1,δ,0)` (= the current verified build) and `ηM = diag(−g,1,δ,0)` (the corrected reading); gates: target-pinning exactness per sign; loop + hedgehog statics regression per sign (which sign preserves the M5.16/M5.18 anchors: r_half, core spectrum, the a = 0.85·δ/2 read?) | both signs measured; a sign that kills the known-good statics anchors is flagged, not silently adopted |
| P1 | **3D hedgehog statics (his chain, step 1)**: energy-minimize the Fig. 9 biaxial hedgehog on the audited axisym stack (+ 3D spot-check); measure his three structural claims: 2-equal regularization along the z-vortex, 3-equal center, mass-in-center (r50/r90 + vortex-line energy per length vs core energy). Reconcile with the M5.21 Q8-slide finding: does HIS regularization language pin the slide, or does the slide survive (= the stability bar fires) | a stable (or slide-characterized) static solution with the core structure measured either way; "has to be stable" is HIS bar: a dissolve is a headline, not a failure |
| P2 | **4D extension by minimization (his chain, step 2)**: add the g time row (sign per P0), minimize within the rotation-sector orbit class (boost sector quarantined per the M5.21 measurement + the M5.20.2 census; the a2x alignment read on the hedgehog background FIRST, minutes, decides whether rigid conjugation even couples here); read the emergent ANGULAR MOMENTUM + the mass/energy split (his "energy minimization should lead to angular momentum + gravitational mass") | the alignment read is decisive either way; a converged 4D minimizer with J ≠ 0 = his prediction landing; J = 0 or no coupling = the measured characterization goes back sharpened |
| P3 | **The KG twist limit (his chain, step 3)**: perpendicular low-energy twists on the P1/P2 background → dispersion read vs Klein-Gordon (the canonical's KG-is-geometric row re-checked on the new spec) | dispersion measured; KG-like = his Fig. 9 closed on the new stack |
| P4 | **The (g, δ) scaling ladder (his correction 2)**: physical values (δ ~ 1e-10, g ~ 1e10, signs open; paper anchors δ² ~ ħc, g⁴ ~ 1e38) are unreachable directly ("need practical approximations", his words): chart the toy-regime scaling laws of the P1-P3 observables (core spectrum a(δ), r50/r90, J, ω ladder) over a feasible (g, δ) grid so every claim carries its regime qualifier + extrapolation direction | monotone/fitted scaling per observable, or the honest "does not extrapolate" flag |
| P5 | Observables + films: BOTH templates (basic + thermal) on every evolving/relaxing sequence; the mass-in-center + light-vortex panel; optional diagnostic: the positive-vs-negative term balance along any energy descent (his message-2 prevention claim, read on our data) | rendered + embedded in the method note |

NOT in scope: the vortex-loop/neutrino side (parked: [M5.20.6](m5_20_6_task_details.md) archived reserve, [M5.20.7](m5_20_7_task_details.md) parked after the M5.21 series); any IVP time integration; the 2-particle runs (M5.21.2).

### Blindspot pass (finalize at go)

| # | Unknown unknown surfaced | Fold |
| --- | --- | --- |
| 1 | "Energy minimization in 4D" is not well-defined under an indefinite H (M5.18: boost×rotation textures unbounded below) | P2 minimizes within the rotation-sector orbit class with the boost sector quarantined; if his intent differs, that is an author-gated question, flagged not guessed |
| 2 | The `(-g)^p` flip could silently move the vacuum branch structure (M5.18: 4 disjoint orbit branches) | P0 re-runs the branch enumeration per sign before any physics |
| 3 | The hedgehog's static-force sector split may differ completely from the loop's 99.9997%-time-row | measure it (a2x on the hedgehog) before importing ANY loop-side conclusion |
| 4 | The Q8 slide (M5.21 statics) vs his "has to be stable": possible contradiction at the toy δ | treat as P1's central measurement; a slide that VANISHES along the P4 δ-ladder is a resolution, not a contradiction |
| 5 | Scaling sweeps multiply cost | budget from the measured M5.16/M5.21 statics costs; grid pre-registered at go, no silent extension |
| 6 | Two spec knobs moving at once (sign of g, δ-ladder) confounds attribution | one-knob-at-a-time protocol: P0 fixes the sign story on the anchors BEFORE P4 moves δ |

### Definition of done

| ✅ when | Bar |
| --- | --- |
| P0 verdict | both-sign targets gated + statics regression table (which sign keeps the anchors) |
| P1 verdict | the 3D static solution characterized against his three structural claims (2-equal vortex, 3-equal center, mass-in-center) + the stability read |
| P2 verdict | the hedgehog alignment read + a converged 4D minimizer (J, mass split) OR the measured characterization of what blocks |
| Records | method note `../findings/m5_21_1_method_note.md` (equations first, equation-to-code map, both-template films embedded); independent adversarial audit (cardinal rule); tracker + roadmap + checkpoint routing; > 1 MB raw data deleted with regen docs |

### Research-body destinations

| Artifact | Destination |
| --- | --- |
| Scripts | `../scripts/m5_21_1_a_spec.py` (P0) · `m5_21_1_b_statics.py` (P1) · `m5_21_1_c_4d.py` (P2/P3) · `m5_21_1_d_scaling.py` (P4) · `m5_21_1_plots.py` |
| Data / plots | `../data/m5_21_1_*.json` (+ npz ≤ 1 MB) · `../plots/m5_21_1_*.png` (film standard, both templates) |
| Findings | `../findings/m5_21_1_method_note.md` |
| Records | this file (FINDINGS + TASK REVIEW) · [`../m5_question_tracker.md`](../m5_question_tracker.md) (Q24 detail carries the redirect) · `../checkpoints/m5_21_1_progress.md` (opens at go) |

### Gating

Roadmap `Gated By`: **Duda's 2026-07-15 electron redirect (landed: this plan IS the fold) + user "go"**. The M5.20-series re-capture is folded above (series rule satisfied at PLAN); re-verify freshness at go if other tasks run in between.

### Model + effort

Fable 5 high for P0 (branch/vacuum re-enumeration) and P2 (the 4D minimization design); default for the mechanical gates + sweeps; independent agent for the audit (cardinal rule).

## FINDINGS (2026-07-16)

Full auditable record (equations first, equation-to-code map, gates, films embedded): [`../findings/m5_21_1_method_note.md`](../findings/m5_21_1_method_note.md). One-line per phase:

| Phase | Headline | Status |
| --- | --- | --- |
| P0 the `(-g)^p` correction | Pinning exact + 4 disjoint vacuum branches per sign; **the pre-registered mirror-equivalence claim was REFUTED by its own gate**: odd-p cross terms make the sign a genuine statics-level knob (~1% in E, same-state gap +0.1296; s = +1 LOWER); anchors (q, r_half, core) sign-robust ≤ 2e-3; boost-texture sign sensitivity onsets at quartic order | ✅ measured |
| P1 deep 3D statics | **NO convergence at toy (g, δ): the Q8 slide survives his regularization language as a SPREADING dilution** (E 21.5 → 8.57 over 48k iters, dE tail −5e-5/it, center pinned; r50/r90 8/32 → 15/51, core-ball frac 0.52 → 0.20, core spread 0.03 → 0.44, q → 0.92). His stability bar fires at toy parameters. C1 vortex 2-equalness fails at toy but the P4 law makes it exact in his physical limit; C3 light-vortex holds directionally (line energy falls to 1.8e-3/len) | ✅ measured |
| P1 stability probes | The endpoint is a **SADDLE of the full 4x4 energy: every probed block-diagonal direction positive (+3.5e5), every time-mixing direction NEGATIVE (−0.4)**: the M5.18 indefiniteness lands at second order on the defect background. 3D spot-check: the slide continues in full 3D axisymmetrically (a_break flat), not an axisym artifact | ✅ measured |
| P2 4D by minimization | **No localized rotating equilibrium in the rigid rotation class**: Ω = 0.05 stalls at rel residual 0.86 (a2x: cos ≤ +0.44, best-any-ω residual ≥ 0.90); Ω ≥ 0.1349 = catastrophic centrifugal instability, ~10 orders down into a deep FINITE well of grid-scale artifact states (audit-corrected: NOT unbounded; V4 ~ amp^8 closes the landscape), both signs. Boost Q2 crossings at χ ≈ 0.02-0.05 (an order closer than the loop): the quarantine is load-bearing. His "minimization → J" does NOT land through rigid orbits; the deferred Q24 least-action structure is the missing piece | ✅ measured |
| P3 KG twist limit | **NOT KG-like at toy regime: a roton-like dispersion minimum at k ≈ 0.1 on BOTH grids** (R² of m² + c²k²: 0.69/0.17); canonical-metric gap ω ≈ 0.10 lands in the M5.21 ring band; caveat: sliding background (no converged toy background exists) | ✅ measured |
| P4 (g, δ) ladder | Two extrapolating laws: **axis split ∝ δ^1.03 (R² 0.9998)** (his 2-equal regularization = exact in the physical limit, O(δ) in the toy regime) and **stiff mode ∝ g^2.99 (R² 0.999998)** (direct sims at g ~ 1e10 impossible: his "need practical approximations" confirmed as the scaling-law obligation). Core pins exactly by g = 32; confinement saturates at 8/27; twist gap is a soft-sector scale | ✅ measured |

**The consolidated message back to the author (for the next outbound round, user-gated)**: his prescription ran end-to-end; the structure claims land asymptotically (2-equal vortex exact as δ → 0; 3-equal core pinned as g → ∞) but the toy-regime object is not a statics minimum (spreading slide) and is a saddle against time-mixing; rigid-rotation minimization cannot produce J (runaway measured); the twist sector carries his clock (gap in the ring band) but with a roton-like dip, not clean KG. Everything sharpens his deferred Q24 least-action elaboration as the missing structure.

### Artifacts

| Type | Files |
| --- | --- |
| Scripts | [`m5_21_1_a_spec.py`](../scripts/m5_21_1_a_spec.py) · [`m5_21_1_b_statics.py`](../scripts/m5_21_1_b_statics.py) · [`m5_21_1_c_4d.py`](../scripts/m5_21_1_c_4d.py) · [`m5_21_1_d_scaling.py`](../scripts/m5_21_1_d_scaling.py) · [`m5_21_1_audit_check.py`](../scripts/m5_21_1_audit_check.py) (the independent audit) |
| Data | `m5_21_1_a_spec.json` · `m5_21_1_b_statics.json` · `m5_21_1_c_4d.json` · `m5_21_1_d_scaling.json` · `m5_21_1_audit.json` + state npz files (all < 1 MB, none deleted) |
| Plots / films | both templates per the film standard: `m5_21_1_b_film_basic/thermal.png` (P1), `m5_21_1_c_film_basic/thermal.png` (P2 runaway = direct evidence), `m5_21_1_d_film_basic/thermal.png` (P4); `m5_21_1_a_spec.png` · `m5_21_1_b_profiles.png` · `m5_21_1_c_a2x.png` · `m5_21_1_c_kg.png` · `m5_21_1_d_scaling.png` |
| Findings | [`../findings/m5_21_1_method_note.md`](../findings/m5_21_1_method_note.md) (equations first + code map + audit § 11) |
| Checkpoint | [`../checkpoints/m5_21_1_progress.md`](../checkpoints/m5_21_1_progress.md) (run log + deviations) |

## TASK REVIEW (2026-07-16)

**Task Duration:** 2:41 (from 11:06 to 13:47 EDT)
**Usage Cap Triggered:** NO (ping parked unfired; watchdog stopped)

**Results** (full per-phase table in `## FINDINGS` above; the method note is the auditable record):

| Phase | Result | Label |
| --- | --- | --- |
| P0 `(-g)^p` both signs | Pinning exact, 4 disjoint vacuum branches per sign, gap-map FD 1.7e-11; the pre-registered mirror-equivalence claim REFUTED by its own gate (odd-p cross terms; same-state gap +0.1296, audit-reproduced to 6.7e-13); s = +1 lower; anchors sign-robust ≤ 2e-3; boost-texture sensitivity onsets at quartic order | ✅ measured |
| P1 deep statics (48k iters) | NO convergence at toy (g, δ): his stability bar fires; spreading dilution (E 21.5 → 8.57, core-ball fraction 0.52 → 0.20, q → 0.92, center pinned), interior spreading not spill into the boundary band (0.32% in the band); 3D spot-check: the slide continues axisymmetrically | ✅ measured |
| P1 curvature probes | The endpoint is a SADDLE of the full 4x4 energy: block-diagonal directions positive (+3.5e5), time-mixing directions negative (−0.4, audit-confirmed by plain FD to 6 digits); the M5.18 indefiniteness lands at second order on the defect background | ✅ measured |
| P2 4D by minimization | No localized rotating equilibrium in the rigid rotation class: Ω = 0.05 stalls (a2x cos ≤ +0.44, best-any-ω residual ≥ 0.90); Ω ≥ 0.1349 catastrophic centrifugal instability ~10 orders into a deep FINITE well (audit-corrected wording; V4 ~ amp^8 closes the landscape); boost Q2 crossings at χ ≈ 0.02-0.05: the quarantine is load-bearing | ✅ measured |
| P3 KG twist limit | NOT KG-like at toy regime: roton-like dispersion minimum at k ≈ 0.1 on both grids (audit-confirmed, two envelopes + plain FD); canonical gap ω ≈ 0.10 in the M5.21 ring band; caveat: sliding background | ✅ measured |
| P4 (g, δ) ladder | Two extrapolating laws (audit-refit): axis split ∝ δ^1.03 (R² 0.9998, his 2-equal vortex regularization exact in the physical limit) + stiff mode ∝ g^2.99 (R² 0.999998, direct sims at his scales impossible; scaling laws are the vehicle); 3-equal core pins exactly by g = 32 | ✅ measured |
| His msg-2 blowup question | The static terms never go negative along any descent (curvature-negative part exactly 0.0); the hazards are the rotating-frame kinetic term and the time-mixing curvature, both 4D-sector | ✅ measured |
| Adversarial audit | 5/6 CONFIRMED by independent methods; 1 real catch adopted ("R unbounded below" → deep finite well); 3 precision notes folded (§ 11 of the method note) | ✅ measured |

**Issues / blockers**: eigsh + shifted power iteration could not converge extreme Hessian eigenvalues (327k dims, spectral range 2.4e6); the directional witnesses carry the SB2 finding instead. No other blockers.

**Deviations from plan**: three, logged in the checkpoint: (1) the P0 SP4 bar encoded an analytic claim the gate refuted (the finding, not an error); (2) c2's runaway flag initially tested only non-finite energies, fixed post-hoc with the JSON rows as unmodified evidence; (3) P4 first run diverged at g = 32 (flat FIRE step), re-run clean with dt0 ∝ 8/g.

**Action needed**: the Q24 tracker detail sharpened (this run pins what his deferred least-action elaboration must supply); canonical-registry + particle-hunt + briefing sweeps (done at this close); no Duda checkpoint for now (user decision 2026-07-16); successor spec-review task [M5.21.1e](m5_21_1e_task_details.md) opened at this close (user directive); M5.21.2/M5.21.3 stay gated (M5.21.3's re-plan-on-best-measured-state clause is live: no converged verified-L state landed).

**Findings**: His prescription ran end-to-end and the structure claims land asymptotically (2-equal vortex exact as δ → 0, 3-equal core pinned as g → ∞), but at toy parameters the electron hedgehog is not a statics minimum (it spreads without converging), is a saddle against time-mixing dressing, and rigid-rotation minimization cannot produce its angular momentum (catastrophic centrifugal instability measured). The twist sector carries the surviving clock (gap in the M5.21 ring band) with a roton-like dip instead of clean Klein-Gordon, and the `(-g)^p` sign is a measurable physics knob (~1% statics-level). Everything converges on his deferred Q24 least-action structure as the missing piece.

**Research docs created / updated**:

- [`../findings/m5_21_1_method_note.md`](../findings/m5_21_1_method_note.md) (equations first, code map, gates, films embedded, audit § 11)
- this task_details (`## FINDINGS` + this review)
- scripts [`m5_21_1_a_spec.py`](../scripts/m5_21_1_a_spec.py) · [`m5_21_1_b_statics.py`](../scripts/m5_21_1_b_statics.py) · [`m5_21_1_c_4d.py`](../scripts/m5_21_1_c_4d.py) · [`m5_21_1_d_scaling.py`](../scripts/m5_21_1_d_scaling.py) · [`m5_21_1_audit_check.py`](../scripts/m5_21_1_audit_check.py)
- data `m5_21_1_{a_spec,b_statics,c_4d,d_scaling,audit}.json` + state npz (all < 1 MB, nothing deleted)
- key plots: `m5_21_1_b_film_basic/thermal.png` (the slide), `m5_21_1_c_film_basic/thermal.png` (the runaway), `m5_21_1_c_kg.png` (the dip), `m5_21_1_d_scaling.png` (the two laws)
