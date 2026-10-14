# M5.21: the particle-clock film strip: electron cross-section snapshots

**Status**: ✅ DONE (roadmap row in [DONE](../m5_roadmap.md); executed 2026-07-13, review approved 2026-07-14). The M5.21 **series**: this task = phase 1 (rotation clock, snapshot pipeline); successors staged in Backlog: **M5.21.1** = the electron hedgehog under the author's 2026-07-15 prescription ([`m5_21_1_task_details.md`](m5_21_1_task_details.md); supersedes the earlier "constrained clock" framing), **M5.21.2** = the 2-particle film strip + the antipair-annihilation arm (2026-07-16), **M5.21.3** = the μ + g-factor closure ([`m5_21_3_task_details.md`](m5_21_3_task_details.md)). **Series rule (user, 2026-07-14): before every M5.21-series "go", re-capture the latest M5.20-series results into the plan** (constraint form, well-posedness verdicts, observable lessons). **Film-strip standard (supersedes the per-series boundary, 2026-07-14 afternoon; single source [`../m5_visualization.md`](../m5_visualization.md)): every M5.21-series run (M5.21.1, M5.21.2, ...) generates BOTH templates, `basic` AND `thermal`,** via `m5_film.film_strip` (first row t = 0, steps-only titles, N_SNAP = 6 default); the M5.20 series emits `basic`.

> **The M5.21.1 seed framing (user-approved 2026-07-14, carry into its TASK PLANNING verbatim): containment is exactly what the constraint must buy, and that is now a measured statement, not a hunch.** [M5.20.3](m5_20_3_task_details.md) lands the constraint on the loop; M5.21.1 puts it on this same electron and reruns the identical clock-vs-noclock comparison against this task's baseline (`data/m5_21_b_relaxed_state.npz` + the noclock/prod/control/gentle records). If the constrained clock contains the energy where the unconstrained kick radiated, that is "the particle clock creating particle stability" on film. M5.21.2 (the 2-particle strip) inherits the same bar: containment first, then interaction.
>
> **The constraint ANSWER landed 2026-07-13/14** ([`m5_20_convo.md`](m5_20_convo.md) + [`m5_20_3_task_details.md § THE ANSWER`](m5_20_3_task_details.md)), so "constrained clock" is now concrete: **free Euler-Lagrange evolution of the purely-quartic L itself** (no artificial restrictions; the degenerate-kinetic null direction handled as the theory's own structure), starting from the energy-minimized 3D hedgehog extended by the g time row. The clock is expected to EMERGE from the dynamics (his negative Hamiltonian terms "seem necessary to propel ... electron angular momentum"), not be seeded as a velocity kick: M5.21.1 compares the true-L evolution against this task's canonical-stack records.

**Series framing**: [`../m5_particle_hunt.md`](../m5_particle_hunt.md) (shapes measured vs identifications hypothesized: M5.20 = the vortex-loop hunt, possibly the neutrino; M5.21 = the hedgehog hunt, possibly the electron).

**Lineage**: [M5.20.2](m5_20_2_task_details.md) (the 4×4 EOM machinery + the census this task rides: all rotation generators K_eff > 0, rotation injections measured stable over T = 400) · [M5.16](m5_16_task_details.md) (the audited axisym hedgehog minimizer + parameter lock; the **Q8 saddle finding** this task probes dynamically) · [M5.11](m5_11_task_details.md) (Faber electron statics, 511 keV) · [`m5_4b_rendering_features.md`](m5_4b_rendering_features.md) (the viz framework this task previews headlessly: Part 4 observable catalog, § 4.1.1 the clock-visibility recipe, § 5.3 placeholder-sample strategy) · [M5.23.3](m5_23_3_task_details.md) (the future on-screen demo suite this feeds).

## TASK PLANNING (2026-07-13, specs interview folded)

### Interview outcomes (user decisions, 2026-07-13)

| Decision | Chosen |
| --- | --- |
| Clock sector | **Phased**: rotation sector now (ungated), full constrained 4×4 later (M5.21.1, gated with M5.20.3) |
| Geometry | **Axisym (ρ,z) primary + one 3D spot-check** (the saddle direction the axisym box freezes) |
| Plot style | **Ellipse glyphs + heat maps**, film-strip at chosen timesteps |
| Audience | **Internal preview + feeder for the rendering block**: the snapshot pipeline is itself a deliverable, previewing the future full-3D Taichi production engine's viz features. The [`m5_4b`](m5_4b_rendering_features.md) framework catalog it feeds, per the user's 2026-07-13. This task's panels cover the electron-relevant subset; the rest are future pipeline cases (the 2-particle film-strip is the natural next reuse). Promote to a Duda-facing note only if the movie earns it |

- flux mesh of energies
- electric/magnetic field
- scalar + vector viz
- magnitude + direction views
- glyphs

enumeration:

- charge
- mass/energy
- deBroglie clock/ZBW, particle stability
- LC director vector
- angular momentum, spin, magnetic moment
- **2-particle attraction/repulsion**
- **Coulomb**, force fields (ele-mag-grav)
- EM waves
- and thermal energy in the future if it lands

### Scope

Two deliverables, in order:

| # | Deliverable | Content |
| --- | --- | --- |
| 1 | **The reusable snapshot instrument** (headless matplotlib, no GUI/Taichi rendering) | Given a field state M (axisym cross-section or a 3D slice), render one panel set; a film-strip = the panel set at chosen timesteps. Channel mapping mirrors the launcher features so the pipeline is a 1:1 headless preview of the future engine |
| 2 | **The electron rotation-clock movie** | Hedgehog charge defect (Duda's 3-equal core prescription) evolved under the M5 Lagrangian in the 4×4 tensor, a rotation-sector clock seeded on it; film-strip showing the clock ticking while the defect holds (or fails to hold): "see the particle clock creating particle stability" |

**Particle size (the user's feasibility question, answered at PLAN)**: the electron is NOT harder due to size. In lattice units the defect core is a few cells regardless of species; the physical fm scale is the M5.16 unit map applied afterwards (parameter-free `r_half = 2.926 fm` already demonstrated). The real difficulty axes are time-integration well-posedness (dodged by staying in the measured-stable rotation sector) and 3D-vs-axisym geometry (handled by the axisym-primary + 3D-spot-check decision).

**The hidden physics question (upgrade from preview to measurement)**: M5.16's Q8 found the spherical hedgehog is a SADDLE of the unconstrained statics (perturbed relax drops 35%, melt moves off-origin). This task watches the same object under conservative DYNAMICS with a rotation clock on it: does the clock stabilize what statics calls unstable? Either answer is a real finding.

**Visual bar** (the user-named inspiration, to be upgraded with the glyph layer):

![t = 0: the seeded loop, both pairings at delta = 0.3](../plots/m5_20_1_seed_maps.png)

![endpoints at t = 2000](../plots/m5_20_1_endpoints.png)

### The panel set (one snapshot)

| Panel | Observable | Launcher-feature analog ([`m5_4b`](m5_4b_rendering_features.md)) |
| --- | --- | --- |
| Ellipse glyph field | Eigenvalues = radii, eigenvectors = axes, grayness = activated potential V(M) (Duda's diagram language), **plus the δ-axis tick per glyph** (the middle eigenvector): the § 4.1.1 correction says the director is the axle, ONLY the δ-axis sweeping shows the spin: without the tick the clock is invisible | Glyph states 0/1 (Director / Director + Delta) |
| Amplitude A | Frobenius deviation from vacuum (heat map, ironbow-like) | WM2 Amp |
| Clock rate | Ṁ Frobenius norm (heat map, blueprint-like) | WM3 Clock ω |
| Energy density | Hamiltonian density (heat map) | WM4 Energy H |
| Charge | Director-splay magnitude at cross-section (gauge-safe: magnitude or defect-relative sign, per the § 3 sign caveat) | WM6 EM div |
| Circulation | Curl magnitude (the B analog; near-zero for the static charge, lights up with the clock: the "B appears with motion" reading) | WM7 EM curl |

Layout: film-strip rows = timesteps (t = 0, then log- or event-spaced), columns = panels; plus a per-run trace figure (E(t), core spectrum λ_i(ρ→0, t), clock phase read-back, charge Q(t)).

**Magnitude + direction views (the launcher's glyph size/color toggles, previewed)**: the glyph panels render in the two launcher variants: `unit + single` (every glyph same length, flat color: the structure-everywhere / far-field view) and `magnitude + gradient` (shaft scales with field strength, color carries the signed value: the field-strength view). Default film-strip uses the structure view for the frame panel and the strength view for the E/B panels; both variants are one flag in the instrument so the future Taichi engine's toggles have a validated headless twin.

### Definition of done

| ✅ when | Bar |
| --- | --- |
| Instrument validated BEFORE physics (the § 5.3 placeholder pattern) | Glyph + panel renderer reproduces analytic placeholder fields exactly: uniform vacuum (no glyph structure), analytic hedgehog (splay 2/r matched, curl ≈ 0), synthetic rotating texture (rendered δ-axis phase == seeded phase, read-back ω == seeded ω) |
| Electron baseline reproduced | Axisym statics re-run reproduces the M5.16-class hedgehog (3-equal core per Duda's charge prescription) before any dynamics |
| The movie landed | Rotation-clock run(s) with the film-strip rendered; energy ledger ≤ 1e-5; seed + endpoint cross-sections (standing rule) plus the intermediate frames (this task's point) |
| The stability question answered honestly | Q8-dynamic verdict instrumented (E localization, core spectrum, topological charge conservation, drift of the defect center), labeled ✅ measured / 🔶 / ⚠️, axisym scope-boxed |
| 3D spot-check run | One short small-grid 3D run probing the saddle direction axisymmetry freezes; slice snapshots through the same pipeline |
| Record + reuse | Findings page (internal) with film-strips embedded; the snapshot instrument documented as a reusable module (the rendering-block feeder); doc checker exit 0 |

### Gating

Ungated (phase 1). The roadmap `Gated By` notes only: M5.20.2 assets (present) + the rotation-sector stability result it rides. M5.21.1 (phase 2) inherits the M5.20.3 gate.

### Pre-registered gates

| Gate | Criterion |
| --- | --- |
| GV0 placeholders | The three analytic placeholder renders above, exact (rendering validated before the physics produces it) |
| GS statics | Axisym hedgehog baseline: energy + core spectrum consistent with the M5.16 lock; 3-equal core reads (a, a, a) at center |
| GD ledger | dt² max-deviation scaling on the dynamics stack; production dt from the measured stiffest mode (4-target V: the g-restoring ω = 78.28 bound applies if the time eigenvalue is active; recompute if the electron sector changes it) |
| GR clock read-back | Seeded rotation ω recovered from the rendered δ-axis phase sweep AND from the Ṁ channel, matching to the FFT bin honesty bar |
| GB runaway watch | The rotation sector is measured stable, but the hedgehog + clock nonlinearity could couple into boost directions: monitor the boost-sector projection per snapshot; if it grows, the documented fallback is the frozen-time-row run (still shows the spatial clock) and the finding is reported, not hidden |
| GQ stability instruments | Topological charge (winding/degree) conserved; defect-center drift; E localization fraction vs t |

### Blindspot pass (unfamiliar territory: electron dynamics + glyph rendering)

| # | Unknown unknown surfaced | Fold into plan |
| --- | --- | --- |
| 1 | The clock is invisible on the director alone (the § 4.1.1 correction: a line has no roll feature; the director is the axle) | The δ-axis tick is REQUIRED in the glyph panel; GR reads the clock from it |
| 2 | Charge-sign gauge flips under evolution (the § 3 caveat: apolar director, neighbouring sign drift) | Charge panel uses magnitude or the defect-relative gauge fix; the conserved charge is the topological winding (GQ), never the splay sign |
| 3 | The Q8 saddle may be an axisym artifact OR may be hidden by axisymmetry (the unstable direction could be non-axisym) | The 3D spot-check exists exactly for this; axisym verdicts scope-boxed |
| 4 | Near-degenerate eigenvalues at the 3-equal core make eigenvector fields noisy there (spurious glyph orientation at the core, the known near-degenerate-zone amplification) | Glyph panel masks or fades glyphs where the eigenvalue gap is below a floor; the core is read via the spectrum trace, not the glyph |
| 5 | Rotation about WHICH axis: three rotation generators exist; the physical ZBW is the twist about the director | Seed the J aligned with the hedgehog's radial structure per Duda's charge picture; one alternate-axis control run |
| 6 | Wall-clock + file size: film-strips at many timesteps can bloat plots/ | Fixed frame budget (~8-12 frames/run); > 1 MB raw state files deleted at FINISH with regen docs (standing rule) |

### Unknowns quadrants self-test

| Quadrant | Biggest unknown | Route |
| --- | --- | --- |
| Known knowns | Rotation-sector stability, the EOM, the axisym stacks, the statics lock | Reuse; GS/GD guard the joins |
| Known unknowns | Does the clock stabilize the Q8 saddle (machine-checkable, THE run); the right rotation axis (control run) | GQ + blindspot 5 |
| Unknown knowns | The user's visual bar: the M5.20.1 maps + Duda's ellipse diagram + the launcher features (now explicit via the interview) | Wired into the panel set |
| Unknown unknowns | The blindspot list; whatever the audit finds | Deviations log at EXECUTE + adversarial audit on any substantive stability claim |

### Research-body destinations

| Artifact | Destination |
| --- | --- |
| Scripts | `../scripts/m5_21_a_snap.py` (the reusable snapshot instrument + GV0 placeholders) · `m5_21_b_electron.py` (statics baseline + seeds) · `m5_21_c_clockrun.py` (rotation dynamics + snapshot hooks) · `m5_21_d_3dcheck.py` |
| Data / plots | `../data/m5_21_*.json` · `../plots/m5_21_*` (film-strips + traces) |
| Findings | `../findings/m5_21_films.md` (internal findings page, film-strips embedded; promote-to-Duda decision at REVIEW) |
| Records | This file (FINDINGS + TASK REVIEW) · `../checkpoints/m5_21_progress.md` at go · Q8 cross-link back to the M5.16 record |

### Sub-experiments (phase plan)

| Phase | Content | Gate |
| --- | --- | --- |
| A | The snapshot instrument against analytic placeholders (§ 5.3 pattern) | GV0 |
| B | Electron statics baseline + clock seeding (rotation sector, axis per blindspot 5) | GS |
| C | Rotation-clock production run(s) + film-strips + the Q8-dynamic verdict | GD, GR, GB, GQ |
| D | 3D spot-check (small grid, short run, slices through the same pipeline) | GQ (3D) |
| E | Findings page + (if a substantive stability claim emerged) adversarial audit + REVIEW | Doc checker exit 0 |

### Preconditions

| Precondition | State |
| --- | --- |
| M5.20.2 EOM + census machinery | ✅ frozen on disk |
| M5.16 minimizer + parameter lock | ✅ frozen on disk |
| The rendering-features doc (panel mapping source) | ✅ [`m5_4b_rendering_features.md`](m5_4b_rendering_features.md) Parts 3-5 |
| Resume ping + checkpoint file | 🚧 at go |

### Model + effort

Default effort for A/B/D (instrument + mechanical baselines, try cap 3 per gate); high for C if the Q8-dynamic result is surprising (it becomes a finding needing careful claims); independent agent for the audit if any stability claim is substantive.

### Contingencies

| Trigger | Action |
| --- | --- |
| Boost coupling fires (GB) | Fall back to the frozen-time-row run; report the coupling as a measured finding |
| Duda's constraint answer arrives mid-run | M5.20.3 takes priority (program-critical); M5.21 checkpoints and resumes after (both are checkpoint-complete by construction) |
| The movie is Duda-gold (clock visibly stabilizing the electron) | Promotion decision at REVIEW: method-note standard + audit before any outbound (never auto-send) |

## FINDINGS (2026-07-13)

Full record: [`findings/m5_21_films.md`](../findings/m5_21_films.md) (film-strips embedded there). Scripts: [`m5_21_a_snap.py`](../scripts/m5_21_a_snap.py) · [`m5_21_b_electron.py`](../scripts/m5_21_b_electron.py) · [`m5_21_c_clockrun.py`](../scripts/m5_21_c_clockrun.py) · [`m5_21_d_3dcheck.py`](../scripts/m5_21_d_3dcheck.py).

| # | Finding | Status |
| --- | --- | --- |
| 1 | **The snapshot instrument works and is validated before physics** (GV0: vacuum exact-zero channels + mask firing; hedgehog splay 2/r at 3.1e-4 and energy 8/r⁴ at 1.4e-3; rotator phase/ω read-back at 1e-16). Reusable `film_strip` API = the headless twin of the launcher viz features, incl. both glyph variants (structure/strength), log scales, δ-axis clock tick | ✅ measured |
| 2 | **Duda's 3-equal core is the seed-adjacent transient, not the deep static preference**: at it 300 the core reads mean 0.4338 vs predicted (1+δ)/3 = 0.4333 (spread 0.044); the deep FIRE relax splits it ((0.591, 0.483, 0.284)) while descending without plateau: the V4 hedgehog statics is a slide (Q8-consistent), charge intact throughout (q 0.956) | ✅ measured |
| 3 | **The rotation sector never touches the boost sector**: time-mixing stays exactly 0.0 through every run (noclock, prod T=400, control, gentle): the M5.20.2 census quarantine holds on the full electron nonlinearity; the frozen-time-row fallback was never needed | ✅ measured |
| 4 | **The unconstrained kinetic twist is not a persistent clock**: exact at t=0 (Ṁ read-back 4e-16), it does ~one apolar sweep, stalls (long-run slope ≈ 0), and radiates; amplitude-robust (ω = 0.05 and 0.02) | ✅ measured |
| 5 | **THE HEADLINE: the core rings**: the core spectrum oscillates coherently ~8 cycles over T=400 at ω ≈ 0.11-0.13 (FFT 0.1255 ± 0.0078; detrended 0.111-0.116), NEAR but ~15% below the 0.1349 activated-face rung of the analytic gap ladder: consistent with large-amplitude anharmonic softening of the vacuum's gapped eigenvalue mode. Intrinsic (rings in noclock too; the twist pumps it). The surviving particle clock = core breathing, the same internal-oscillation theme as the author's 2026-07-12 radius-breathing prediction, seen on the hedgehog | ✅ measured (bin-honest: "near the rung, softened", NOT "at the rung") |
| 6 | **Q8-dynamic verdict**: the rotation clock does NOT stabilize the saddle in this stack (the canonical completion); the kick radiates and accelerates the melt restructuring; the topological winding survives regardless (noclock q = 1.000 at all radii). M5.21.1 (the constrained clock, M5.20.3-gated) now has its comparison baseline | ✅ measured, axisym scope-boxed |
| 7 | Energy ledger 1.1e-6 to 4.2e-6 across all runs (bar: 1e-5); GD dt² ratios 3.92/4.06 | ✅ measured |
| 8 | **3D spot-check**: the equivariant embed is exact (a_break 2.8e-15); an l=2 non-axisym perturbation + clock grows SLOWLY and decelerating (4.0e-4 → 1.1e-2 over T=50; tail e-rate ≈ 0.022/t; grows-vs-saturates undecided): no fast hidden instability; axisym verdicts safe on T ≲ 50, flagged beyond. 3D ledger 7.2e-7; 3D gradient complex-step-exact (1.75e-15) | ✅ measured (small-box caveat: boundary reflections after t ≈ 12) |

**Instrument caveats logged**: the fixed-radius meridional q read flips (±1/0) in churned regions where λ1 ≈ λ2 (director branch-swap): NOT read as charge inversion; branch-tracking winding = future work. The defect-center instrument follows the amplitude cloud (incl. radiation), not the topological core.

### Deviations from plan

| Deviation | Handling |
| --- | --- |
| GS2's 3-equal-core bar became a two-stage measurement (holds seed-adjacent, splits at depth): the statics baseline is a slide, not a stationary point | The noclock control carries the baseline burden; reported as finding 2 |
| GS "consistent with the M5.16 lock" read structurally (the lock is LdG-based; this stack is the V4 4-target): correspondence recorded, not numeric equality | Noted at PLAN-to-EXECUTE hand-off, held |
| GV0b curl bound 1e-4 replaced by an h-refinement truncation proof (ratio 3.73 ≈ 4) at try 2 | Stronger gate than the arbitrary constant |
| GQ drift gate (< 3 cells) assumed a quiet baseline; the measured baseline slides by itself | Gate reinterpreted as the drift MEASUREMENT (4.2 noclock / 5.0 gentle / 5.4 control / 14.2 prod-T400) |
| One extra run added (gentle, ω = 0.02) for kick-amplitude dependence | Within the run budget |
| GD3a FD bar at N = 24 was roundoff-floor-limited (g⁴ trace scale: 4.4e-6 at eps 1e-6, worse at 1e-5): upgraded to COMPLEX-STEP at try 3 of cap 3 (the energy is polynomial in M) → 1.75e-15 PASS | Gate code on disk = complex-step; the run JSON's GD3a entry patched with the note |
| Phase D's per-snap `core_lams` recorded the near-axis z-PROFILE (48 cells × 3) instead of one cell | Kept: richer data; the JSON holds the profile |

### Raw-data regen (large files deleted at FINISH per the standing rule)

| File | Size | Status | Regen |
| --- | --- | --- | --- |
| `data/m5_21_c_final_noclock.npz` | 1.9 MB | deleted | `python3 scripts/m5_21_c_clockrun.py noclock` (~7 min; needs the relaxed npz) |
| `data/m5_21_c_final_prod.npz` | 3.7 MB | deleted | `python3 scripts/m5_21_c_clockrun.py prod` (~28 min) |
| `data/m5_21_c_final_control.npz` | 2.9 MB | deleted | `python3 scripts/m5_21_c_clockrun.py control` (~7 min) |
| `data/m5_21_c_final_gentle.npz` | 3.2 MB | deleted | `python3 scripts/m5_21_c_clockrun.py gentle` (~7 min) |
| `data/m5_21_b_relaxed_state.npz` | 0.8 MB | KEPT (under the 1 MB bar; the reusable baseline every phase-C/D run loads) | `python3 scripts/m5_21_b_electron.py 12000` (~13 min) |

## TASK REVIEW (2026-07-13, approved 2026-07-14)

Task Duration: 2:05 (from 12:32 to 14:37 EDT, 2026-07-13)
Usage Cap Triggered: NO

| # | Result | Status |
| --- | --- | --- |
| 1 | The snapshot instrument (deliverable 1): reusable `film_strip` API, 6 launcher-analog panels, both glyph variants, GV0-validated before physics (vacuum exact; hedgehog splay 2/r at 3.1e-4, energy 8/r⁴ at 1.4e-3, curl h²-truncation-proven; rotator phase/ω read-back at 1e-16) | ✅ measured |
| 2 | The movie (deliverable 2): the δ-ticks appear + sweep as the clock runs (invisible at rest: azimuthal δ-axis); 10 frames, T=400, ledger 4.2e-6 | ✅ landed |
| 3 | THE HEADLINE: the core RINGS ~8 cycles at ω ≈ 0.11-0.13 (FFT 0.1255 ± 0.0078; detrended 0.111-0.116), near but ~15% below the 0.1349 gap-ladder rung (anharmonic softening); intrinsic (rings in noclock) | ✅ measured (bin-honest: "near the rung, softened") |
| 4 | Q8-dynamic: the unconstrained kinetic twist does NOT stabilize (stalls ~1 sweep, radiates, amplitude-robust); winding survives (noclock q = 1.000 at all radii) | ✅ measured, axisym scope-boxed |
| 5 | Boost sector exactly 0.0 through all 4 runs (the M5.20.2 quarantine holds on full nonlinearity) | ✅ measured |
| 6 | Duda's 3-equal core = seed-adjacent transient (0.4338 vs 0.4333 at it 300); deep relax splits it (the statics is a slide) | ✅ measured |
| 7 | 3D spot-check: embed exact (2.8e-15); slow decelerating non-axisym growth (~0.02/t tail); no fast instability; T ≲ 50 safe | ✅ measured (small-box reflections after t ≈ 12) |

Deviations from plan: six, logged in the FINDINGS deviations table. Issues: fixed-radius q read branch-swaps in churned regions (documented limit); 3D grows-vs-saturates undecided at T = 50.

**Review Q&A (user, 2026-07-14): "energy is not being contained, the particle is not stable yet: is it because we did not run the 4×4 matrix?"** Answer: the runs DID use the full 4×4 tensor (the M5.20.2 stack: η-curvature + 4-target V4, g-timelike branch; the boost watch proves the time sector was live and stayed quiet). What was NOT run is the CONSTRAINED dynamics: our time term is the canonical-kinetic regularization of the author's purely-quartic L, and the twist was a plain velocity kick. In that unconstrained stack there is nothing to hold the energy in: the statics is a Q8 slide (no minimum to sit in) and the kick radiates. What survives is the topological charge and the intrinsic core-breathing clock. The candidate stabilizer is exactly the constraint Duda's answer supplies (M5.20.3), tested on the electron as M5.21.1: this task measured its comparison baseline.

Close-out actions (2026-07-14): roadmap row moved to Done (appended at the END); M5.21.1 + M5.21.2 stub rows added to Backlog; the M5.20-re-capture series rule recorded in the Status line, both stub rows, and here; the M5.21-relevant findings fed into [`m5_20_3_task_details.md`](m5_20_3_task_details.md) (§ M5.21 findings feed) with the M5.20-series cross-section spec kept unchanged (seed + endpoint maps, not the film-strip format).

Findings: the film-strip instrument works end to end; the electron's surviving clock is an intrinsic core-breathing mode ringing near (softened ~15% below) the 0.1349 gap-ladder rung, while an unconstrained kinetic twist stalls and radiates without stabilizing the Q8 saddle: M5.21.1 (the constrained clock) is now sharply posed with its baseline measured.

Research docs created/updated: this file · [`../findings/m5_21_films.md`](../findings/m5_21_films.md) (the record, film-strips embedded) · scripts `m5_21_{a,b,c,d}_*.py` · plots `m5_21_a_placeholders/rotator_strip`, `m5_21_b_baseline`, `m5_21_c_film/traces_{noclock,prod,control,gentle}`, `m5_21_d_slices/traces` · data 7 JSON + the kept 0.8 MB baseline npz (4 final-state npz > 1 MB deleted, regen in the FINDINGS table) · [`../m5_roadmap.md`](../m5_roadmap.md) (Done append + M5.21.1/M5.21.2 stubs) · [`m5_20_3_task_details.md`](m5_20_3_task_details.md) (findings feed).
