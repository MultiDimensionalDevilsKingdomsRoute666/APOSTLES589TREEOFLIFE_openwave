# M5.27: the background-scalar time sector (the staged 4×4), entrainment pilot

**Status**: ✅ **CLOSED 2026-07-24** (phase A run complete: gates 8/8, tongue map NULL at all 40 points, adversarial audit 5/5; findings + review below, method note [`../findings/m5_27_note.md`](../findings/m5_27_note.md)). Planning locked and run the same day. Sanctioned by the author green light 2026-07-22. Proposed 2026-07-21 pending author go; the author's group reply the next morning granted standing permission for self-directed 4×4 work: "Sure, if Fable has idea how to move forward with 4x4 case, please work on it" ([`m5_22_convo.md § 2026-07-22`](m5_22_convo.md), the 4×4 green-light row), which covers this pilot as the third fork branch. No further ask needed to run; this runs on user "go". Roadmap: [`m5_roadmap.md § BACKLOG`](../m5_roadmap.md), **sequenced NEXT, ahead of [M5.22](m5_22_task_details.md)** (the 2026-07-24 user reorder: a single self-contained pilot fits before the long multi-phase nuclei run, whose main-priority standing and week-of-2026-07-27 start commitment are unchanged; supersedes the 2026-07-23 after-M5.22 slotting; Backlog row order = the run sequence). Offered as the THIRD branch of the fork left open at the [M5.21.3](m5_21_3_task_details.md) close (the fixed-J reading vs the T2η potential lift vs this), proposed to the author in the M5.21-series close round (sent 2026-07-21 17:06 EDT; [convo record](m5_21_convo.md)). **The M5.27.x series is PARKED** (user decision at the review; roadmap change-log 2026-07-24) and the sharpened 4×4 problem statement (non-commuting coupling required, mixed-block/Skyrme Lagrangian lane) is carried forward by [M5.22 § The M5.27 hand-off](m5_22_task_details.md), so the successor scope has a live trigger. **Author-channel record filed on this ID**: [`m5_27_convo.md`](m5_27_convo.md) (2026-07-25, public GitHub Discussions), the author's three-level ladder + the `λ` / `Λ` / `O` notation convention; its level-3 clause re-states the nonzero-time-derivative claim this pilot measured against, and the measured gap is unchanged by it.

## TASK PLANNING (2026-07-24)

**Scope**: Phase A of the § 2c phasing ONLY: the prescribed uniform background χ = A·cos(ω̄t), coupled by driving the V4 spectral targets (g → g + κχ), run on the verified-L η stack as the staged 4×4 (spatial block + time-time entry live; the (0,i) mixed block projected out per step, its removed-component norm logged AND its removed energy booked in the ledger). Deliverables: the lock-or-not verdict map (Arnold tongue), the J and μ re-reads under drive, the drive-power ledger, the eigenvalue-excursion read (§ 6b U3), the boost test, and a conditional Kapitza-window arm. Phase B (dynamical χ) stays out of scope (§ 2c).

**Definition of done** (freezes the § 9 draft at "go"):

| # | Item | Pass condition |
| --- | --- | --- |
| 1 | Pre-registration lock | The search spaces, verdict criteria, protocols P0-P6, and the boost protocol below are frozen BEFORE numerics; the two ω̄ windows (lock vs Kapitza) run as SEPARATE experiments (§ 6b U4) |
| 2 | Gates green | κ = 0 regression reproduces the fixed-J live hold (the delivered [M5.23.2](m5_23_2_task_details.md) L-gate anchor: J 0.19923 → 0.19865 over 100 steps) + the free-release decay baseline ([M5.21.3](m5_21_3_task_details.md)) on this harness; **G-vac: the defect-free driven box matches the adiabatic analytic vacuum response with no spurious interior gradients** (this gate also DECIDES the boundary handling, blindspot B7); the phase instrument validated on the live hold at known ω* (B9); the drive-power instrument passes the analytic driven-oscillator audit case; box + M00 spectrum pre-computed (§ 6b T4); dt cost pre-checked (§ 6b T5); statics re-measured at κ ≠ 0 (§ 6b T3) |
| 3 | The lock scan delivered | The (κ, ω̄) verdict map with the 4-way discriminator below; every point classified; the Arnold-tongue plot (or the measured absence of a tongue: a NULL map is a complete result) |
| 4 | Re-reads delivered | J budget under drive, μ per the [M5.21.5](m5_21_5_task_details.md) protocol, eigenvalue excursion vs κ (§ 6b U3), each vacuum-referenced |
| 5 | Audit + note | Adversarial audit (independent implementation) of any nontrivial claim BEFORE anything author-facing; method note per the house standard; findings doc + roadmap + tracker cross-linked |

**Gating**: user "go" only. The author sanction stands (2026-07-22 green light, status line above); no upstream task gates this; nothing downstream gates on it ([M5.28](m5_28_task_details.md) gates on [M5.22](m5_22_task_details.md) Phase 1). Consumes DELIVERED instruments only: the [M5.21.9](m5_21_9_task_details.md) fixed-J endpoints, the [M5.23.2](m5_23_2_task_details.md) npz loader (`engine1_seeds.load_npz_M`), the [M5.21.5](m5_21_5_task_details.md) J/μ protocol, the [M5.21.6](m5_21_6_task_details.md) kick protocol.

**Model/effort**: Fable 5 / high (deep-research default: novel driven-system physics + an audit arm).

**Implementation route (code-scoped 2026-07-24)**: the drive needs NO kernel surgery. Production engine files are consumed read-only; new kernels (mixed-block projection, drive-power sum) live in the task's own scripts (taichi-first).

| Fact (measured in code today) | Consequence for the run |
| --- | --- |
| `v4_of` / `dv4_of` / `evolve_M_eta_finish` take `sg` as a per-call argument; ALL g-dependence of V4 sits in the trace targets `C_p = sg^p + 1 + δ^p` (`../../engine2_pde.py` ≈ lines 985-1140) | The prescribed drive is host-side: pass `sg(t) = g + κA·cos(ω̄t)` each step; every kernel that receives `sg` receives the same time sample |
| Only the product κA enters the EOM for a prescribed drive | The phase-A knob space collapses from (κ, A, ω̄) to (κA, ω̄); register A ≡ 1, κ is the coupling knob, and the § 6b U3 read becomes κ ↦ excursion. The § 4 ledger form ½ρω̄²A² stays bookable at A ≡ 1 |
| The V4 stiff M00 mode sits at ω ≈ 78 (g = 8), the fixed-J clock band at ω* ≈ 0.2-1.0 | The lock window drives quasi-statically (the vacuum M00 adiabatically tracks −sg(t): the in-model background oscillation); dt already resolves ω ≈ 78, so the scan costs no dt tightening; ω̄ near 78 and box modes are excluded/marked bands |
| The vacuum minimum tracks diag(−sg(t), 1, δ, 0): the WHOLE BOX breathes under a global drive | Every defect read is vacuum-referenced: subtract a far-field probe, else the tongue map reads the box's response, not the defect's |
| Drive power is analytic: P(t) = (∂V4/∂sg)·ṡg summed over the grid | A small in-script kernel; audited against finite-difference V4 at paired sg values + the analytic driven-oscillator toy |
| On-disk seeds: `m5_21_9_fixedj{,_conj}_om{0.2,0.5,1}_end.npz` (32³ 4×4, h = 1.5), all 6 verified present 2026-07-24; g = 8.0, δ = 0.5 (`../../medium.py`) | The released fixed-J clock is the lock target; its measured ω* centers each ω̄ window. Load via `load_npz_M` WITH the covariant-flip check (post-load sanity: V4/cell ≈ 0; storage is +g, dynamics wants −g, the M5.23.2 loader handles it) |
| `set_fixed_j` / `read_carried_j` at `../../engine2_pde.py` lines 1557/1593; the release + ω\*-re-kick initialization is DELIVERED tech (the [M5.23.2](m5_23_2_task_details.md) live-hold protocol / `_topo_npz_electron` path) | P0/P1 start from a verified procedure, not new plumbing; the live-hold J numbers double as the κ = 0 regression anchor |
| The clock-phase time series Δφ(t) does NOT exist yet as an instrument (M5.21.9 logged kin/twist/J, not an unwrapped phase) | NEW arm-A deliverable: the phase instrument (core-axis azimuth from `eigen_decompose`, unwrapped, apolar mod-π handled, B9); validated on the live hold where the rate is known before any verdict uses it |

**Sub-experiments (protocols, pre-registered)**:

| ID | Protocol | Read |
| --- | --- | --- |
| P0 | Control: release a fixed-J endpoint (constraint OFF, drive OFF) | The free-decay baseline (the M5.21.3 result re-measured on this exact harness); the ledger noise floor |
| P1 | Capture: release + drive ON at ω̄ near the endpoint's ω* | Phase difference Δφ(t) defect-clock vs drive; mean drive power; frequency pulling ω_defect(ω̄) |
| P2 | Tongue map: the (κ, ω̄) grid, each point classified by the 4-way discriminator | The Arnold-tongue map (primary endpoint: conj om0.2; spot-checks om0.5/om1.0 at the best κ) |
| P3 | Drive-off discriminator: after any lock, switch the drive OFF | Persistence vs instant collapse (entrained self-oscillation vs forced response); expected = decay per M5.21.3, pre-registered honestly |
| P4 | Re-reads under drive: J budget, μ (M5.21.5 protocol), eigenvalue excursion vs κ (U3), statics gate (T3) | Does the drive supply the J-budget the fixed-J constraint hand-imposes (the § 3 decisive detail); does κ map monotonically onto excursion |
| P5 | Boost test: kicked defect (M5.21.6 protocol) under the uniform drive | Lock survival in motion + the modulation read (de Broglie signature, qualitative grade) |
| P6 | CONDITIONAL Kapitza window (runs only if P0-P4 leave budget): ω̄ ∈ [5, 20] | Can a fast drive stabilize the free clock that statics kills; separate experiment per § 6b U4 |
| AUD | Independent small-grid numpy reimplementation of the driven block-diag EOM + ledger; refuters on any lock claim (forced-response mimic, projection artifact, box-mode coincidence, f32 phase drift) | Audit verdicts per claim |

**Search spaces + verdict criteria (frozen at "go")**:

| Register | Value |
| --- | --- |
| Drive excursion ε = κA/g (A ≡ 1) | {0.003, 0.01, 0.03, 0.1} log grid + ONE flagged stress point 0.3; spectrum ordering preserved at all registered ε |
| ω̄ lock window | [0.4, 2.6] × the released state's measured ω* (covers the 1:1 AND the parametric 2:1 tongue, blindspot B10), 10 coarse points including registered points at exactly 1.0× and 2.0×, adaptive refinement near any response, cap 3 rounds (goal-loop try cap) |
| Drive ramp | κ ramps 0 → κ_target over ≥ 5 drive cycles (B8); verdict windows open post-ramp |
| Arena | 32³ h = 1.5 for scans; 64³ (and f64 if the measured f32 phase-noise floor demands) for the headline point only |
| Run windows | ≥ 50 drive cycles at the window's lowest ω̄; P0 control matched in length |
| LOCKED | abs(Δφ) net drift < π over the final 20 drive cycles AND mean drive power within the P0 noise floor AND rotation kin plateau (no decay) |
| DRIVEN RESPONSE | Response at ω̄ with sustained nonzero mean drive power (the § 3 outcome (b)) |
| MATHIEU UNSTABLE | Monotone ledger growth (§ 6b T2); recorded, excluded from the tongue |
| NULL | Decay indistinguishable from P0 |

**Blindspot pass** (unknown unknowns surfaced at PLAN, beyond the § 6b tripwires):

| # | Blindspot | Fold-in |
| --- | --- | --- |
| B1 | A scalar drive moves eigenVALUE targets; the clock is a phase in eigenVECTOR space: at linear order a uniform spectral drive may not couple to the rotation phase at all (the coupling channel is indirect, through the defect profile's position-dependent excursions) | An empty tongue at all κ is a LIVE, informative outcome: it would say the time-time entry alone cannot entrain the clock, pointing at the deferred mixed block as the necessary coupling. Pre-registered as part of outcome (c) |
| B2 | Leapfrog + a time-dependent potential: the sg sample point (t vs t + dt/2) biases the work ledger at O(dt) | Fix ONE sampling convention, verify on the analytic driven-oscillator audit case before any scan |
| B3 | The global drive shakes the vacuum too | Vacuum-referenced reads everywhere (the far-field probe subtraction, implementation-route table) |
| B4 | f32 phase drift over ≥ 50-cycle windows can mimic or destroy a lock verdict | Measure the κ = 0 phase-noise floor FIRST; it sets the drift threshold; f64 fallback for the headline |
| B5 | A tongue narrower than the coarse ω̄ grid reads as a false NULL | The adaptive-refinement protocol (cap 3) + report the grid resolution next to any NULL claim |
| B6 | "Injection locking" textbook framing presumes a self-sustained oscillator; verified-L has none (M5.21.3) | Claim language pinned to the § 3 decisive detail: the question is whether the drive SUPPLIES the missing J-budget, not whether it locks an existing clock |
| B7 | Boundary pinning becomes an ANTENNA under a global drive: `evolve_M_eta_finish` updates the interior only, so boundary cells stay at the UNDRIVEN vacuum while the driven interior tracks −sg(t); the mismatch layer radiates spuriously | The G-vac gate (DoD 2): defect-free driven box FIRST, must match the adiabatic analytic response with no spurious interior gradients; the boundary handling (analytically track diag(−sg(t), spatial) vs stay pinned) is DECIDED at that gate and registered before any scan |
| B8 | Switching κ on as a step shocks C_p and launches a transient that can mask or fake a capture | The drive amplitude RAMPS adiabatically over ≥ 5 drive cycles (registered ramp profile); verdict windows open only after the ramp |
| B9 | The clock phase is read off an APOLAR axis (n ≡ −n, the spin-½ result): the raw azimuth is defined mod π, and naive unwrapping can double or halve a measured lock ratio | The phase instrument handles the mod-π degeneracy explicitly and is validated on the fixed-J live hold at known ω* before any verdict consumes it |
| B10 | A potential-modulation drive is PARAMETRIC: leading-order coupling sits at ω̄ ≈ 2ω* (the Mathieu/parametric-resonance structure), not at the 1:1 tongue; a window centered on 1:1 alone can miss the physics entirely | The ω̄ window covers BOTH tongues: [0.4, 2.6] × ω* with registered grid points AT 1.0× and 2.0×; verdicts report the lock RATIO (1:1 vs 2:1 vs other rational), and the mod-π care of B9 feeds this read |

**Research body**: scripts `../scripts/m5_27_*.py` (harness `m5_27_a_harness.py`, scan `m5_27_b_lockscan.py`, re-reads `m5_27_c_rereads.py`, boost `m5_27_d_boost.py`, conditional `m5_27_e_kapitza.py`, audit `m5_27_audit_check.py`), data `../data/m5_27_*` (arrays local-only + `_DATASETS.md` regen), plots `../plots/m5_27_*.png` (embedded inline), findings `../findings/m5_27_note.md` (method-note grade; created at close, linked then), checkpoint `../checkpoints/m5_27_progress.md` (updated on every sub-result). Engine files untouched unless a blocker forces an edit (logged as a deviation + the full selftest/regression suite rerun).

## 1. WHY NOW: the M5.21-series close diagnosis

The M5.21 electron series closed with a diagnostic pattern.

- Everything static-topological closes ✅ (charge quantization, spin-½, the annihilation ledgers, the lepton census),
- and everything that needs the TIME sector fails to close ❌  (free-clock existence, μ, g, force-law dynamics).

The Lagrangian has been frozen since the verified-L era by design; M5.17 → M5.21.4 was instrument-building, audits, and honest re-grading on a fixed L. The record now points at exactly one missing organ: the time sector.

| Task | Headline outcome | Model-evolution read |
| --- | --- | --- |
| [M5.21.3](m5_21_3_task_details.md) (the 4D lift, closed 07-18) | THE SADDLE: all 24 time-mixing curvatures negative (time derivatives WANT to be nonzero), BUT free 4×4 minimization finds NO stable dynamical electron: every rotation velocity costs energy, no finite stationary ω, statics wins outright. The clock survives only as a fixed-J CONSTRAINED state (ω\* = J/2kin, J imposed by hand). [Note](../findings/m5_21_3_note.md) | The first true 4×4 dynamics attempt came back existence-negative |
| [M5.21.5](m5_21_5_task_details.md) (μ + g, closed 07-21) | μ channel exists but is a parity-cancellation residue spanning 4 orders across preparations; g NO closure (8.5e-4 to 1.45); the canonical g = 1.97 RETRO-FLAGGED. [Note](../findings/m5_21_5_note.md) | The observable that needs the clock degraded |
| [M5.21.4](m5_21_4_task_details.md) (2-particle, closed 07-21) | Conduit annihilation mechanism audited (genuinely new, the antimatter row delivered); but NO static pair regime exists, Coulomb 1/d NOT confirmed at reachable d, string tension ansatz-grade. [Note](../findings/m5_21_4_note.md) | Mixed: dynamics instrument matured, force law open |

## 2. THE PROPOSAL

| Element | Content |
| --- | --- |
| Fields | M(x,t) 3×3 traceless symmetric, T2 term set, verified-L UNCHANGED (charge quantization, census, annihilation all inherited) + ONE real scalar χ(x,t) |
| Vacuum | χ = A·cos(ω̄t), spatially uniform: a vacuum rest-frame background oscillation |
| Coupling | Promote the g-eigenvalue of the author's own spectrum `D = diag(g, 1, δ, 0)` to `g + κχ(x,t)`: the 4×4's time-time entry made dynamical FIRST, the (0,i) mixed block deferred. A STAGED 4×4, not an alternative to the author's 4×4 selection |
| Economy | +1 field component vs +4 (M₀₀ + three M₀ᵢ); a standard sign-definite kinetic term, while the all-negative time-mixing curvatures ([M5.21.3](m5_21_3_task_details.md)) and the divergent regions of the author's analytical notebook live in the deferred mixed block (hypothesis, checkable against [M5.21.8](m5_21_8_task_details.md)) |
| First observables | Lock-or-not (Arnold tongue in κ, ω̄); J and μ re-read under lock (the [M5.21.5](m5_21_5_task_details.md) protocol re-run); the drive-power ledger; the eigenvalue-excursion read (§ 6b U3). The two-defect force under a shared background (the in-phase attraction channel) moves to phase B (§ 2c): it needs a dynamical χ the defects can source |
| Phasing | Phase A = prescribed uniform drive (this pilot); phase B = dynamical χ (an M5.27.x follow-on); the decision record is § 2c |

The economy argument in one line: promoting M to a 4×4 spacetime tensor adds ~4 awkwardly-signed components; a scalar background adds 1. The 4×4 route's persistent trouble may simply mean the time sector wants to be a SEPARATE FIELD, not extra indices on the order parameter.

## 2b. THE ONTOLOGY FRAME (open hypothesis, captured 2026-07-23 planning session)

Where χ comes from, stated as a layered claim (the 2026-07-23 planning voicenotes, organized):

| Layer | What it is | Owns |
| --- | --- | --- |
| Fundamental (intractable) | Planck-scale granules, oscillating; "the wave is a composition of that oscillation" | time itself (the oscillation IS the clock) |
| Wave layer | the fundamental waves those oscillations compose | time / the clock; gravity = spatial gradient of clock rates; drives magnetism (director circulation) |
| Order parameter (tractable) | the LC ellipsoid field `M`, a coarse-grained average of the layer below | electrostatics + the whole static-topological sector; "liquid crystal is a RESULT, not the substrate" |

One sharpening against the record: "liquid crystal is only for electrostatics" is too narrow. The verified 3×3 stack owns the whole static-topological sector (charge quantization, spin-½, annihilation, the lepton census), not just Coulomb. The clean statement: **`M` owns everything static-topological; the wave layer owns everything the time sector failed to close.** That maps exactly onto the § 1 diagnosis (statics ✅, time sector ❌), which is why the frame fits: it says the time sector failed on `M` because time never lived in `M`. It also upgrades the § 2 economy argument from parameter-counting to structure: χ is the tractable in-model representative of the wave layer, and `M` is the order parameter of the same layer's spatial structure. Two fields because two layers.

| Consistency point | Resolution on record |
| --- | --- |
| The course L11 emergence ledger says "the substrate does not wave; the wave is downstream", while this frame says waves are more fundamental than the LC | Not a contradiction, a scope statement: L11 is correct WITHIN M5 (the `M` field does not wave as a substrate). This frame proposes a layer BELOW M5's substrate; χ is the first in-model representative of that layer. L11 carries a dated scope addendum saying so ([`__M5_course.md § L11`](../../__M5_course.md)) |
| This task is author-facing as a "staged 4×4" (g → g+κχ), while the frame reads it as "time from waves, not from the 4×4 matrix" | Keep the staged-4×4 frame in anything author-facing (it is the diplomatic and technically true description); the wave-layer reading is the interpretive frame, documented as an open hypothesis, the same honesty grade the course gives the granule-covariance reading (L1 Q9) |
| The § 6 preferred-frame hazard | Reframed, not removed: if a wave layer is fundamental, a rest frame at that layer is EXPECTED, and Lorentz covariance must emerge from Doppler-consistent kinematics (the de Broglie 1924 construction, § 7). The boost test stays pre-registered |

Status: open ontological hypothesis, not something the pilot asserts or tests (§ 6b U1-U2); the pilot measures what the coupled system does.

## 2c. PHASING (design decision, 2026-07-23)

| Phase | χ status | Scope |
| --- | --- | --- |
| A (this pilot) | PRESCRIBED uniform drive: χ = A·cos(ω̄t) imposed, not evolved | The lock scan (Arnold tongue), the J/μ re-read under lock, the drive-power ledger, the boost test, the eigenvalue-excursion read (§ 6b U3) |
| B (an M5.27.x follow-on, out of pilot scope) | DYNAMICAL χ: own kinetic + potential term, defects can source it | Gravity (near-field frequency depression), the two-defect in-phase force (Bjerknes), background propagation (§ 6b U5) |

The reasoning (the § 6b T1 tripwire is the decision that shapes the whole run plan): phase A prescribed-drive first keeps the pilot falsifiable with three knobs and a clean ledger, and answers the fork question (entrain vs replace vs null) before paying for a dynamical χ sector. With a dynamical χ, ω̄ stops being a free knob (it becomes the χ potential's mass parameter), the defect gains a NEW radiation channel into χ, and the energy ledger gains a sector: phase B costs are real and only worth paying on a phase-A lock. The § 5 gravity and two-defect rows therefore read as PHASE B chances; a prescribed uniform drive cannot produce them (the background is unaffected by the defects by construction).

## 3. DESIGN DECISION: ENTRAIN, not REPLACE

| Argument | Why it lands on ENTRAIN |
| --- | --- |
| Energy honesty | At lock, an injection-locked oscillator draws ZERO average power from the drive; the soliton stays self-sustaining and Derrick escape is not secretly pumping. REPLACE makes rest energy drive-dependent: fake stability, broken ledger |
| The record | M5.8's self-starting clock is a ✅ in-platform result; REPLACE would contradict the column's own record |
| The M5.21.3 twist | On the verified-L stack the free clock does NOT self-start (rotation costs energy). The regime question is genuinely open, which makes it the FIRST pre-registered observable of this pilot, not an assumption |
| The decisive detail | The fixed-J constraint is a hand-imposed stand-in for exactly what a background drive supplies dynamically. If lock delivers a J-budget without imposing J, the constrained-state crutch disappears |

Pre-registered outcomes (all three are results): (a) an intrinsic mode locks to the background = ENTRAIN confirmed; (b) oscillation exists only while driven, with measured drive power = replace-like, the ledger flags it; (c) no coupling = null.

## 4. THE BACKGROUND ENERGY LEDGER (declared)

The background field's energy is booked with the classical energy density of an oscillating medium: `E/V = ½ρω²A²` (equivalently `ρ(fA)²` up to convention factors), quadratic in both amplitude and frequency. This is declared, not derived: it is the textbook harmonic form (acoustics, elasticity, cavity modes), and the pilot's job is to measure what the coupled system does with it, not to justify it.

| Reference anchor | Role in the ledger |
| --- | --- |
| Classical oscillating-medium energy density (Rayleigh; ½ρω²A² per mode) | The bookkeeping form itself; standard for any harmonic background |
| de Broglie's internal clock (1924): `m₀c² = hν₀` | The target identification the pilot tests: rest energy ↔ lock frequency, mass = coupling strength to the background mode; the column's ZBW clock re-reads are the measured side of the same identification |
| Planck-Einstein `E = ħω` | The quantum limit the entrained ledger must stay consistent with when the realistic-parameter bridge is crossed ([Q33](../m5_question_tracker.md#q33-detail) lineage); not used at toy parameters |
| Adler injection-locking power relation | The drive-power instrument: zero average power at lock, nonzero off-lock; the § 3 regime discriminator is read directly off this ledger line |

Discipline: all quantities in M5 program units; no physical constants enter the pilot; the three new knobs (κ, A, ω̄) come pre-registered with search spaces (§ 6), nothing tuned per observable.

## 5. CHANCES BY SECTOR (pre-run assessment)

The structural reason the import is attractive: each side's validated strength covers the other's recorded negative. M5's open sectors (free-clock existence, hierarchy origin, the 4×4 route, gravity) are exactly where a background wave has known mechanisms. Phase split (§ 2c): the clock, stability, and boost/de Broglie rows are phase A physics; gravity, the two-defect channel, and any near-field-modification mechanism need phase B's dynamical χ (a prescribed uniform background cannot be sourced or depressed by defects by construction).

| Sector | What the background brings | Known-physics anchor | Chance |
| --- | --- | --- | --- |
| Clock | Entrainment of the defect's oscillation to a universal reference; mass = coupling strength to the background mode | Driven-oscillator entrainment (Arnold tongues); M5.8 measured an intrinsic clock, so this is locking an existing oscillator, the easy case | HIGH |
| Particle stability | The drive supplies the time-periodicity M5's Derrick escape needs, externally sustained: parametric stabilization of otherwise-unstable configurations | Kapitza pendulum, Paul traps, ponderomotive trapping; all textbook | HIGH |
| Propulsion / de Broglie wave | A boosted standing wave Doppler-splits into carrier + modulation, which is how de Broglie derived the phase wave (1924) | Couder-Bush walking droplets: a particle propelled and guided by its own background standing wave, pilot-wave dynamics emerging | MEDIUM-HIGH |
| Gravity (weak field, clock sector) | Two coinciding mechanisms: (a) a defect near-field depresses the local background frequency, neighboring clocks slow, refractive attraction; (b) secondary Bjerknes force: oscillators phase-locked to the SAME background attract when in phase, amplitude-proportional (mass-proportional), universally attractive | Bjerknes forces between bubbles in ultrasound (measured, classical); analog-gravity refractive metrics | MEDIUM-HIGH for Newtonian + redshift |
| Gravity (full GR grade) | Scalar-background gravity historically fails light bending by the factor 2 (Nordström); recovering Schwarzschild needs the moving-medium metric (Gordon / Painlevé-Gullstrand flow), not a static index | Analog-gravity literature | LOW-MEDIUM without extra structure |
| μ + magnetic curl | Circulation of the near-field modification around the defect axis; could supply a first-principles bridge behind the currently underived K = 4/α factor | Vortex-carrying acoustic/optical near fields | MEDIUM (double-counting risk: M5 already has a μ channel) |
| Spin ½ | Little to add: the apolar mechanism already closed this ✅ machine-exact; a vector background could add photon-like helicity | | LOW need, keep M5's |
| Lepton hierarchy | A cavity background has a DISCRETE harmonic ladder; defects locking to different harmonics gives a discrete mass ladder, a mechanism M5 currently lacks entirely | LaFreniere mode numbers; the M8 column's spectral ladder | SPECULATIVE, but a mechanism where M5 has none |

## 6. HAZARDS

| Hazard | Why it bites |
| --- | --- |
| Preferred frame | A universal standing wave defines a rest frame; Lorentz invariance must emerge from Doppler-consistent wave kinematics. The deepest theoretical risk; needs a pre-registered boost test early |
| Energy bookkeeping | If defects draw stability from the background, the background is an energy reservoir; drive input vs soliton energy must be booked honestly or "stability" is just pumping |
| Replace vs entrain | Decided upfront (§ 3): ENTRAIN. An undecided hybrid would double-count the clock energy |
| Parameter growth | κ, A, ω̄ are new knobs; platform standards apply (derive or pre-register with search spaces, nothing tuned per observable) |

## 6b. UNKNOWNS MAP + TRIPWIRES (2026-07-23 planning session)

The planning-session question set, routed (machine-checkable in the pilot / author-gated / nature-gated):

| # | Question | Route | What the pilot can do |
| --- | --- | --- | --- |
| U1 | What IS the oscillation? (what medium does χ coarse-grain?) | Nature-gated | Documented as the § 2b frame; the pilot measures what the coupled system DOES, not what χ is |
| U2 | Are the granules tracing the ellipsoid? | Nature-gated | The course L1 Q9 covariance hypothesis, carried unchanged; untestable at pilot scope |
| U3 | "Amplitude gives the ellipsoid its eigenvalues" | Machine-checkable ✅ | NEW OBSERVABLE: track the local eigen-spectrum excursion of `M` under drive; does drive amplitude A map monotonically onto eigenvalue excursion? Cheap to instrument; directly tests the amplitude→shape reading |
| U4 | "The frequency is too high, so the ellipsoids gain structure" (time-averaging / scale separation) | Machine-checkable, and a design constraint | Exposes that § 5 mixes two regimes: entrainment lock needs ω̄ NEAR the intrinsic clock (Arnold tongue); Kapitza stabilization needs ω̄ FAR ABOVE it. One ω̄ scan cannot do both: the two windows are pre-registered as SEPARATE experiments (DoD 1) |
| U5 | The relationship between ellipsoids and the propagation of their oscillations | Machine-checkable at phase B only | A prescribed uniform χ has no propagation by construction; the question is the heart of the phase B dynamical-χ scope (§ 2c) |
| U6 | "The ellipsoid exists when multiple waves are colliding" (multi-particle dependence) | Partially machine-checkable | The two-defect shared-background test is the in-model handle (phase B); the full multi-wave-collision reading stays nature-gated |

Tripwires (named before numerics; each carries its guard):

| # | Tripwire | Guard |
| --- | --- | --- |
| T1 | Prescribed drive vs dynamical χ left undeclared: the two designs answer different questions and book energy differently | RESOLVED by § 2c: phase A prescribed, phase B dynamical, declared upfront |
| T2 | Lock vs parametric-instability confusion: parametric driving both stabilizes AND destabilizes (the Mathieu chart has tongues of INSTABILITY). Blow-up at some (κ, ω̄) is a Mathieu instability, not a failed lock; survival is not automatically entrainment | Pre-registered discriminator: lock = phase-locked clock at zero average drive power; instability = unbounded energy growth on the ledger; neither = null |
| T3 | Statics contamination at κ ≠ 0: the inherited ✅ sector was verified at κ = 0; a drive can shift static energies even where topology protects the invariants | Gate: re-measure the key static observables at κ ≠ 0 with the drive ON, beyond the κ = 0 regression |
| T4 | Box-mode interference: a standing background in a finite box interacts with the box's own eigenfrequencies; an ω̄ scan shows spurious structure at box modes | Pre-compute the box spectrum; mark those frequencies before reading any Arnold tongue |
| T5 | dt cost of the high-ω̄ (Kapitza) window: resolving ω̄ needs dt ≪ 2π/ω̄; the high-frequency window may be far more expensive than the lock window | Numerics pre-check before committing the scan budget |

## 7. ANTICIPATED OBJECTIONS (named upfront, answers on record)

| Objection | Answer |
| --- | --- |
| "This abandons the selected 4×4 route" | No: it is a STAGED 4×4 (the time-time entry first, the 0-row later) and the third branch of the fork the author left open at the M5.21.3 close, motivated by the author's own results (the saddle + the notebook divergences) |
| Preferred frame | Named in § 6, boost test pre-registered; de Broglie's 1924 phase-wave construction is the anchor for covariance emerging from a boosted oscillation |
| "Another field, another knob" | The § 2 economy row + § 6 parameter discipline: κ, A, ω̄ pre-registered, no per-observable tuning |
| "This imports oscillation theory" | The mechanism anchors (de Broglie, injection locking, Kapitza stabilization) are model-independent classical oscillator physics; the energy form is textbook. The convergence, if it appears, is platform triangulation, not adoption (§ 4) |

## 8. RELATION TO THE PROGRAM + SEQUENCING

| Item | Relation |
| --- | --- |
| The M5.21.3-close fork | This is the third branch (fixed-J reading vs T2η lift vs background scalar); the author's call |
| [M5.21.8](m5_21_8_task_details.md) (notebook verification) | Natural companion: the § 2 economy hypothesis (the pathology lives in the mixed block) is checkable against its results |
| [M5.23.1](m5_23_1_task_details.md) (rendering series) | Rendering proceeds regardless (sequenced BEFORE this pilot in the reordered Backlog). Note: M5.23.1 ports the fixed-J clock into production; if this pilot delivers a lock, the clock's origin story changes (a dynamically supplied J-budget vs the hand-imposed constraint), so the pilot tells us whether the port target is the final clock or the crutch |
| Gate | Author go ✅ granted 2026-07-22 (the 4×4 green light); runs on user "go", sequenced AHEAD of [M5.22](m5_22_task_details.md) (the 2026-07-24 user reorder; planning locked same day, § TASK PLANNING) |

## 9. DEFINITION OF DONE (pilot scope, draft; frozen at go)

| # | Item |
| --- | --- |
| 1 | Pre-registration lock: κ, A, ω̄ search spaces, with the two ω̄ windows (lock-resonant vs Kapitza-high, § 6b U4/T2) registered as SEPARATE experiments + the § 3 three-outcome table + the boost test protocol, frozen BEFORE numerics |
| 2 | Gates: 3D regression exact on the verified-L stack at κ = 0; χ-sector energy conservation; the drive-power ledger instrumented; the key static observables re-measured at κ ≠ 0 with the drive on (§ 6b T3); the box-mode spectrum pre-computed (§ 6b T4); the dt cost of the high-ω̄ window pre-checked (§ 6b T5) |
| 3 | The lock scan: defect response vs (κ, ω̄), Arnold-tongue map, regime verdict per § 3 (with the § 6b T2 lock-vs-instability discriminator) |
| 4 | J and μ re-read under lock (the M5.21.5 protocol) + the eigenvalue-excursion read (§ 6b U3). The two-defect force under a shared background is phase B scope (§ 2c), NOT in this pilot's DoD |
| 5 | Adversarial audit (independent implementation) before anything author-facing; method note per the house standard |

## FINDINGS (2026-07-24)

Full method note (equations first + equation-to-code map + audit record): [`../findings/m5_27_note.md`](../findings/m5_27_note.md).

**Headline**: phase A answers the fork branch with a measured, over-determined NO, and delivers the reason. A prescribed uniform background scalar coupled as `g → g + κχ` does not entrain the clock at any registered `(κ, ω̄)`; the drive is an eigenVALUE actuator (authority coefficient 1.000) with exactly zero torque on the eigenFRAME the clock lives in.

| # | Result | Grade |
| --- | --- | --- |
| 1 | **Tongue map NULL at all 40 registered points** (eps 0.003-0.1 x om_bar/om* 0.4-2.6, covering the 1:1 and the 2:1 parametric tongue). 7 raw SUSTAINED flags all REFUTED on 4 independent grounds (noise band, zero-crossing, no widening with drive amplitude, phase rates consistent with zero) | ✅ measured |
| 2 | **The mechanism**: `[dF/dsg, M]` = 4.5e-21 (machine zero) on the block-diagonal staged states vs 1.38e-02 with the mixed (0,i) block present. The uniform spectral drive moves eigenvalues and cannot torque the eigenframe | ✅ measured (algebraic, independent build) |
| 3 | **U3 answered sharply**: the time-time eigenvalue excursion equals the drive amplitude `g·eps` to ratio 0.999/0.996/0.999/0.999 across 1.5 decades (log-log slope alpha = 1.000), while the spatial spectrum shows no eps dependence | ✅ measured |
| 4 | **The mixed block is a dynamically INVARIANT manifold**: with the projection disabled and block-diagonal data, the largest (0,i) entry reached is exactly 0.0. The drive cannot even excite the channel that would carry the coupling | ✅ measured |
| 5 | **P0 control**: free release does not hold the clock (J 0.19923 -> 0.00673, -96.6% over t = 200; kin x100). The [M5.21.3](m5_21_3_task_details.md) no-free-clock result quantified on this harness | ✅ measured |
| 6 | **P7 seeded-mixed test = outcome (c)**: seeding the (0,i) block goes non-finite at t = 16.8 / 13.8, exactly as the M5.21.3 all-negative time-mixing curvatures predict. The dynamical test cannot isolate the coupling; the algebraic result stands alone | ✅ measured |
| 7 | Independent audit **5/5** on a separate numpy f64 build (own stencil, gradient, integrator): reproduces the null (control +0.088 vs driven 1:1 +0.052, 2:1 -0.125) and closes the energy ledger (dE +23.39 vs drive work +22.67) | ✅ measured |
| 8 | Recommendation: **do not build phase B (dynamical chi) on this coupling**. A dynamical chi coupled the same way inherits the same commutator and the same invariant manifold; it would add a radiation channel and an energy sector while still not reaching the clock | 🔶 judgement on measured grounds |

**The economy argument, re-graded honestly**: the proposal's "+1 field component instead of +4" is correct about parameter count and wrong about physics. The cheap component is cheap precisely because it does not touch the sector the time face needs. If the background-wave idea is carried forward, the coupling must act non-commutingly on `M` (the mixed (0,i) block), and that block is measured unstable under the current L, which routes the question back to the Lagrangian-level work the author flagged as needing soliton specialists.

## TASK REVIEW (2026-07-24)

**Task Duration:** 02:15 (from 17:36 to 19:51)
**Usage Cap Triggered:** NO

**Results**: see the FINDINGS table above. Gates 8/8 ✅, audit 5/5 ✅, tongue map NULL 40/40 ✅ measured, mechanism ✅ measured, recommendation 🔶 judgement.

**Issues / blockers**: none outstanding. The mixed-block instability (result 6) is a measured property of the current L, not a harness fault, and it is already the author's named open problem.

**Deviations from plan**:

| # | Deviation | Handling |
| --- | --- | --- |
| 1 | Ramp registered in drive CYCLES consumed most of a run at low om_bar (158 of 200 time units) | Re-registered as `RAMP_T = 60` TIME units (~2 clock periods); all affected measurements re-run |
| 2 | Blindspot B3 (vacuum referencing) was written for FIELD reads; it applies to the ENERGY LEDGER too (raw kin/power are ~90% box breathing) | `vacuum_reference()` added, paired defect-free run per (eps, om_bar); J and phase verified clean and used as the primary observables |
| 3 | The pre-registered SUSTAINED threshold (gain > 0.10) was frozen before the control's noise band was known and sat BELOW it (0.153) | Added the explicit refutation pass `m5_27_h_refute.py` with 4 independent refuters rather than silently relaxing a threshold |
| 4 | U3 as planned was buried under the state's own relaxation (excursion 0.319 at eps = 0) | Retargeted to the time-time eigenvalue on a non-kicked state; the read then came out exact (alpha = 1.000) |
| 5 | P7 as first written was a no-op (staged and mixed-live byte-identical) | Discovered the invariance property (a result in itself), then seeded the block by hand; outcome (c) |
| 6 | Model was Opus 5, not the planned Fable 5 (user switched at go) | Logged; no effect on artifacts |
| 7 | Primary endpoint stayed `conj_om0.2` as planned (the earlier cost concern that would have forced `conj_om1` did not materialize: Metal gave 0.197 ms/step) | No change needed |

**Action needed**:

| Item | Owner |
| --- | --- |
| Decide whether M5.27.x phase B is retired, re-scoped onto a non-commuting coupling, or parked (the note's § 11 recommends not building it on this coupling) | user |
| The M5.27 result is a clean negative worth carrying into the author channel when the next batch goes out (it answers the third fork branch he left open, and it sharpens WHY the 4x4 mixed block is the load-bearing part) | user-gated, batched |
| [M5.22](m5_22_task_details.md) nuclei is next in the Backlog, start committed for the week of 2026-07-27 | user "go" |

**Findings**: A prescribed uniform background scalar coupled to the spectral targets (`g → g + κχ`) does NOT entrain the M5 clock: the Arnold-tongue map is null at all 40 registered points, and the null is structural rather than a parameter miss. The drive force commutes with `M` on the block-diagonal states the staged 4×4 runs (machine zero 4.5e-21, vs 1.38e-02 once the mixed (0,i) block is present), so it has complete authority over eigenvalues (the time-time eigenvalue tracks the drive amplitude with slope 1.000 across 1.5 decades) and exactly none over the eigenframe that carries the clock; the block-diagonal sector is moreover dynamically invariant, so the drive cannot even excite the channel that would carry the coupling. Seeding that channel by hand destabilizes within t ≈ 15, as M5.21.3's all-negative time-mixing curvatures predict. The practical consequence: the proposal's economy argument (one scalar instead of four mixed components) is right about parameter count and wrong about physics, and phase B should not be built on this coupling.

**Research docs created / updated**:

| Doc | Content |
| --- | --- |
| [`../findings/m5_27_note.md`](../findings/m5_27_note.md) | the method note (equations first, equation-to-code map, gates, refutation, mechanism, not-computed list) |
| [`m5_27_task_details.md`](m5_27_task_details.md) | this record: TASK PLANNING (locked pre-run) + FINDINGS + review |
| [`../scripts/m5_27_a_harness.py`](../scripts/m5_27_a_harness.py) | the driven harness: host-side drive, ledger kernels, apolar phase instrument, boundary tracking |
| [`../scripts/m5_27_b_gates.py`](../scripts/m5_27_b_gates.py) · [`../data/m5_27_gates.json`](../data/m5_27_gates.json) | the 8/8 gate battery |
| [`../scripts/m5_27_c_lockscan.py`](../scripts/m5_27_c_lockscan.py) · [`../data/m5_27_lockscan.json`](../data/m5_27_lockscan.json) | P0-P3, the 40-point tongue map |
| [`../scripts/m5_27_h_refute.py`](../scripts/m5_27_h_refute.py) · [`../data/m5_27_verdicts.json`](../data/m5_27_verdicts.json) | the refutation pass (7/7 refuted) |
| [`../scripts/m5_27_d_audit.py`](../scripts/m5_27_d_audit.py) · [`../data/m5_27_audit.json`](../data/m5_27_audit.json) | the independent adversarial audit (5/5) |
| [`../scripts/m5_27_f_rereads.py`](../scripts/m5_27_f_rereads.py) · [`../data/m5_27_rereads.json`](../data/m5_27_rereads.json) | U3 eigenvalue authority + P5 boost |
| [`../scripts/m5_27_g_mechanism.py`](../scripts/m5_27_g_mechanism.py) · [`../data/m5_27_mechanism.json`](../data/m5_27_mechanism.json) | P7 invariance + seeded-mixed test |
| [`../scripts/m5_27_e_plots.py`](../scripts/m5_27_e_plots.py) | the figures |

Key plots: [`m5_27_tongue_map.png`](../plots/m5_27_tongue_map.png) (the null map + refuted verdicts), [`m5_27_baseline_panel.png`](../plots/m5_27_baseline_panel.png) (the control, driven traces, gain sweep vs the noise band), [`m5_27_rereads_panel.png`](../plots/m5_27_rereads_panel.png) (U3 eigenvalue authority).

![the tongue map and the verdict map](../plots/m5_27_tongue_map.png)

![P0 control, driven runs, and the gain sweep](../plots/m5_27_baseline_panel.png)

![U3 eigenvalue authority and the P5 boost test](../plots/m5_27_rereads_panel.png)
