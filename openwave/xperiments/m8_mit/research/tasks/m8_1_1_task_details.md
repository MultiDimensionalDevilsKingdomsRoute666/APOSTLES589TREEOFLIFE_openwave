# M8.1.1: SECOND BLIND RUN, the remaining bedrock theorems (gaps + asymmetry on S³)

> Roadmap row: [`../m8_roadmap.md`](../m8_roadmap.md) M8.1.1 (**maintainer-run**).
> Parent template: [`m8_1_task_details.md`](m8_1_task_details.md) (the worked blind-run
> protocol, reused as-is). Sources: the two bedrock papers the author shared on
> [#312](https://github.com/openwave-labs/openwave/discussions/312#discussioncomment-17758091)
> (2026-07-24): [SSRN 6968698](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6968698)
> and [SSRN 7129118](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7129118).

## TASK PLANNING (2026-07-24, registered; go pending)

### Scope

Blind independent verification, in the M8.1 sense (script and number by agents who have
not seen the derivations or the claimed values), of the two remaining MIT bedrock papers,
described by the author as establishing "gaps and asymetry on S3". Expected identification
from the briefing's key-inputs list: the **coexact spectral gap from McKay distance** (the
Yang-Mills mass-gap result on S³/2I) and the **E8-filling Galois pair** (the asymmetry
structure behind the three flat connections). This identification is a planning guess and
is CONFIRMED only at claim extraction: at planning time the papers were deliberately left
unread (see the quarantine note below).

### Why this task exists (the principled trigger, not courtesy)

| Point | Statement |
| --- | --- |
| Platform relevance | These theorems are target structure for the field-dynamics program: [M8.2](m8_2_task_details.md) pre-registers gap ratios among its observables and [M8.4](m8_4_task_details.md) aims the Lagrangian survey at the resulting slot structure. A pre-registered target should stand on verified structure. |
| The rule | Any analytic number that becomes a pre-registered target of the dynamics program gets blind-verified BEFORE M8.2 locks it. |
| Why maintainer-run BY CONSTRUCTION | The author's agents have read the papers; a self-run "verification" is a reproducer, not an independent recompute. Blindness is the one thing the platform can supply that the author structurally cannot. |
| What this task is NOT | A gate on the author's roadmap: M8.2, M8.3 and M8.6 are startable now and none of them wait for this run. It is also not a standing free-validation service; M8.1 was the certification gate, this run exists because of the pre-registered-target rule above. |

### Quarantine status (in effect since registration)

At registration (2026-07-24) the maintainers' planning session read ONLY the discussion
thread and the briefing's one-line paper descriptions, NOT the papers themselves; the
SSRN pages were not fetched. The M8.1 independence protocol therefore reuses cleanly at
go time:

| Role | Sees | Does not see |
| --- | --- | --- |
| Designer (go-time orchestrator) | the full papers (fetched to the session scratchpad, OUTSIDE the repo) | n/a |
| Solver agent | ONLY a self-contained spec sheet per paper (objects, operators, group data, boundary conditions) + task list | the claimed values, theorem statements' numeric content, the author's name/repo/papers, ALL repository docs |
| Audit agent | the same spec sheet + the solver's outputs + script | same blindness to the claims |
| Comparison to the claims | by the designer AFTER both agents return numbers | |

No-search rule: every computed number is reported; nothing is tuned toward the claims;
if the numbers land somewhere else, that IS the result.

### To be fixed at go time (BEFORE numerics)

| Item | Note |
| --- | --- |
| Paper identification confirmed | match the two SSRN IDs to the briefing's named bedrock inputs; update this doc |
| Pre-registered claims tables (C1..Cn per paper) | the M8.1 § "Pre-registered claims" format, one table per paper; sub-runs S-A (gap paper) and S-B (asymmetry paper) |
| Feasibility triage | the Möbius operator was 1D-reducible; a coexact gap on S³/2I carries representation theory and may need a spectral method in 2I-symmetric harmonics (see [`../m8_platform_pointers.md § 6`](../m8_platform_pointers.md)); if a claim is not boundable as a numerical check, say so and scope it out honestly |
| Blindspot pass | redo the M8.1 blindspot table for the new operators (sector completeness, quotient identification maps, seam/gluing analogues) |
| Citations sync | add both papers to [`../../theory/_CITATIONS.md`](../../theory/_CITATIONS.md) (or adopt the author's PR if it lands first) |

### Definition of done (skeleton, finalized at go)

| # | Item |
| --- | --- |
| 1 | Per-paper solver runs with converged numbers, scripts + JSON in the repo (`m8_1_1_` prefixes) |
| 2 | Adversarial audit with its own method, per-claim verdicts |
| 3 | Designer comparison against the pre-registered claims, all numbers stated |
| 4 | Method note `findings/m8_1_1_method_note.md` (equations first, eq-to-code map, embedded plots, audit record) |
| 5 | Doc sync: canonical + briefing + MODELS.md cells + roadmap row |
| 6 | Doc checker exit 0; TASK REVIEW presented |

### Scheduling

Maintainer-run at maintainer pace; registered 2026-07-24, run when maintainer resources
free up (communicated on #312: not in the next days). Not on the author's critical path.

---

## GO-TIME PRE-REGISTRATION (2026-07-28, go 18:28 EDT)

Frozen BEFORE any numerics ran, and answering the "to be fixed at go time" checklist
above. Nothing below was edited after the first solver launched.

### Paper identification (confirmed)

| Sub-run | Paper | Source of record |
| --- | --- | --- |
| S-A | *Coexact Spectral Gaps from McKay Distance for Flat Bundles on Homogeneous Spherical Space Forms* | [SSRN 6968698](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6968698); text obtained as `bedrock/files/coexact-gap.md` from the author repo `dmobius3/mode-identity-theory` at commit `13a5c2b815f5d159f400f3f830bc55d1980f0bb3`, held in the session scratchpad only |
| S-B | *An Affine Rho-Index Conversion and the Galois Pair on the Poincaré Homology Sphere* | [SSRN 7129118](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7129118); `bedrock/files/galois-pair.md`, same commit and handling |

The planning guess of 2026-07-24 (the coexact gap paper + the E8-filling Galois pair) is
CONFIRMED by this identification. Both papers are already registered in
[`../../theory/_CITATIONS.md`](../../theory/_CITATIONS.md), so no citations sync is owed.
The author's own `galois-pair.test.py` was downloaded with the papers and is designer-only
material: it is quarantined from every agent and is not used as a check.

### Blindness protocol (as run)

| Role | Sees | Does not see |
| --- | --- | --- |
| Designer (this session) | both papers, the author's test script, all repo docs | n/a |
| Solver A / Solver B | ONE self-contained spec sheet in the session scratchpad (objects, groups, operators, task list) | the claimed values, the theorem statements, the papers, the author, the repo, each other's work |
| Audit A / Audit B | the same spec sheet + the solver's script and outputs | the same blindness to the claims |
| Comparison to the claims | designer only, AFTER the agents return numbers | |

Withheld from every agent: the words the claims turn on (McKay, Galois, rho, the model,
the author), every claimed constant (4/R², 36/R², the affine coefficients, the rational
rho and charge values, the virtual character and its augmentation), and every theorem
number. Agents write into the scratchpad, never the repo, so no repository markdown can
expose a target; the designer copies the scripts into `research/scripts/` unmodified at
FINISH.

No-search rule: every computed number is reported; nothing is tuned toward the claims; if
the numbers land somewhere else, that IS the result.

### Pre-registered claims, S-A (the coexact gap paper)

Units: R = 1 throughout, so every gap is reported as the pure number λ·R². "Blind" means
computed by an agent that never saw the value.

| ID | Claim (from the paper, exact) | Pass condition | Fail condition |
| --- | --- | --- | --- |
| A1 | The twisted coexact 1-form spectrum on X = S³/Γ is exactly {m² : m ≥ 2, a constituent of τ occurs in W_m = V_m\|Γ ⊕ V_(m−2)\|Γ}, with multiplicity μ_τ(m) = (m−1)·dim Hom_Γ(τ\*, V_m\|Γ) + (m+1)·dim Hom_Γ(τ\*, V_(m−2)\|Γ) | blind invariant-subspace dimensions equal μ_τ(m) for every (Γ, τ, m) tested, by two internal methods (exact character trace + numerical projector rank) | any mismatch at any (Γ, τ, m) |
| A2 (the first-occurrence engine) | The least a with an irreducible σ ⊂ V_a\|Γ equals the graph distance d(σ) from the trivial node in the representation-ring adjacency graph; and if −I ∈ Γ, occurrence forces a ≡ d(σ) (mod 2) | blind first-occurrence level = blind graph distance for EVERY irreducible of EVERY tested Γ; the parity statement holds wherever −I ∈ Γ | one counterexample |
| A3 | First coexact level e(σ) = 2 for d(σ) = 0; e(σ) = d(σ) for d(σ) ≥ 2 with no hypothesis on Γ; e(σ) = 3 for d(σ) = 1 when −I ∈ Γ. Hence q_τ is the minimum over constituents, and d_τ ≥ 2 gives bottom = d_τ² | blind e(σ) matches all three branches across all tested Γ | any deviation |
| A4 (THE HEADLINE) | For every irreducible flat SU(2) connection ρ on every S³/Γ with Γ ⊂ SU(2) finite, the bottom of the adjoint coexact spectrum is 4, with EXACTLY ONE exception over all pairs (Γ, ρ): one of the two 2I connections gives 36. Also d_(Sym²ρ) ≥ 2 always | blind gaps = 4 for every (Γ, ρ) tested except exactly one 2I connection, which returns 36 | a second exception, no exception, or any other value |
| A5 | Branching of V_a\|2I for a = 0..6 is 1, Q, Sym²Q, 4, 5, 6, and 4′ ⊕ Sym²Q′ at a = 6; the distance-six 3-dimensional irreducible is absent from V_a\|2I for every a < 6 | blind decomposition reproduces all seven rows including the level-6 split into two irreducibles | any row differs |
| A6 | The full twisted 1-form gap equals the coexact gap: the exact summand's bottom is d(d+2), i.e. 8 in the generic case and 48 in the exceptional one, each exceeding its coexact bottom | blind exact-summand bottoms = 8 and 48, both above their coexact bottoms | mismatch, or an exact bottom below the coexact one |
| A7 | Untwisted: q_1 = 2, so the untwisted coexact gap is 4 on every S³/Γ. For Γ = Z_n with n odd, a distance-one character first occurs at m = 2 exactly when n = 3, and at m = 3 for every other odd n | blind untwisted gaps all 4; the odd-cyclic pattern reproduced including the n = 3 special case | any deviation |

### Pre-registered claims, S-B (the affine conversion / asymmetry paper)

Two currencies are handed to the agents WITHOUT their names or meaning: the defect sum
S(α) = (1/\|Γ\|)·Σ_(g≠I) (χ_α(g) − dim α)·cot²(φ_g/2) and the character sum
D(α) = (1/\|Γ\|)·Σ_(g≠I) χ_α(g)/det(I₂ − g). In the paper's language S is ρ_α(Y_Γ⁺) and D
is D_α.

| ID | Claim (from the paper, exact) | Pass condition | Fail condition |
| --- | --- | --- | --- |
| B1 (the conversion identity) | ρ_α = dim α + 4·(D_α − dim α·D_1) for EVERY finite Γ ⊂ SU(2) and every flat unitary twist α with no trivial constituent | the blind affine fit of S against (dim α, D_α, dim α·D_1) returns the coefficient triple (1, 4, −4) exactly, universally over all tested Γ and α, at zero residual | a different triple, a Γ-dependent triple, or a nonzero residual |
| B2 | Sharpness: a trivial constituent of multiplicity m shifts the identity by exactly m; worked instance α = Q ⊕ 1 gives right side −29/30 against ρ_Q = −59/30 | blind offset = m exactly for every tested α carrying trivial constituents, and the worked instance reproduces | offset ≠ m |
| B3 | For Γ = 2I: D_1 = 1079/1440, D_Q = 73/144, D_Q′ = −67/720, D_(Sym²Q) = 9/32, D_(Sym²Q′) = −19/160 | all five blind exact rationals match | any mismatch |
| B4 | On the link orientation: ρ_Q = −59/30, ρ_Q′ = −131/30, ρ_(Sym²Q) = −73/15, ρ_(Sym²Q′) = −97/15 | all four blind defect sums match | any mismatch |
| B5 | ρ_(Sym²Q′) − ρ_(Sym²Q) = 4·(D_(Sym²Q′) − D_(Sym²Q)) = 4·(−2/5) = −8/5, supported EXACTLY on the four conjugacy classes of element order 5 and 10; the four other non-identity classes contribute −57/4 (times 1/\|Γ\|) to each of the two character sums alike, while those four classes contribute +48 and 0 | blind per-class contribution table reproduces the difference AND the exact support split | the difference matches but the support does not, or either number differs |
| B6 | Consistency web: 2·D_1 = 1079/720; (1/\|Γ\|)·Σ_(g≠I) cot²(φ_g/2) = 361/180 for 2I; and D_1 + (1/8)·that sum = 1 | all three blind values match | any mismatch |
| B7 | Charges k(α) = dim α·D_1 − D_α are 119/120, 191/120, 59/30, 71/30 in the four sectors (Q, Q′, Sym²Q, Sym²Q′), with fractional parts 119/120, 71/120, 29/30, 11/30 and adjoint-sector difference +2/5 | all four blind charges and their fractional parts match, and the adjoint difference is +2/5 | any mismatch |
| B8 | With A the matrix of multiplication by the defining representation on the representation ring, solving (2·Id − A)H = e_Q − e_Q′ with the trivial coordinate set to 0 gives H = (0, 0, −1, −2, −3, −4, −3, −2, −2) ordered by increasing distance, augmentation ⟨H, δ⟩ = −72, and k(Q) − k(Q′) = D_Q′ − D_Q = −72/120 = −3/5 exactly | blind solve reproduces the vector, the augmentation, and the exact charge difference | any component, the augmentation, or the difference differs |
| B9 | The E8 package: H₂(W; Z₂) = Z₂⁸ with the mod-2 form alternating and nondegenerate; the mod-4 refinement takes values {0, 2} with 136 and 120 classes; the 240 norm-(−2) lattice vectors reduce two-to-one onto exactly those 120 classes; the reflection group is transitive on them | blind lattice computation returns 240 → 120, the 136/120 split, and a single orbit | any count differs, or more than one orbit |
| B10 | csc²(φ_g/2) = 4/(2 − χ_Q(g)) for every g ≠ I | the blind identity holds on every element of every tested Γ | any element fails |
| B11 | Up to conjugacy 2I carries exactly two irreducible SU(2)-valued flat connections besides the trivial one, exchanged by the nontrivial automorphism of the character field | blind enumeration of 2-dimensional determinant-one irreducibles returns exactly two, with characters conjugate over a real quadratic field | a different count, or rational characters |

### Feasibility triage: what is NOT numerically boundable (scoped out, stated up front)

| Item | Why it is out of scope for a blind recompute |
| --- | --- |
| The classical geometric inputs (the Atiyah-Patodi-Singer defect formula computing ρ, Degeratu's Dirac-eta identity, the Kronheimer-Nakajima index integral, the Ikeda-Taniguchi round-sphere coexact spectrum) | long-known theorems of the literature, not this author's claims. They are handed to the solvers AS the definitions, so what this run tests is every step the papers build ON them |
| Theorem 1.3(ii) of the asymmetry paper (the restriction-route decoupling) | a structural proof about localization terms across a class of identities, with no finite object to compute; read-only |
| The comparisons to printed literature values (Anvari, BHKK) | external-source agreement, not a recompute. The blind run instead evaluates the same quantities from their definitions, which is the stronger check available here |
| The novelty claims (which statements are new to the literature) | priority claims, not computable ones |

Consequence: S-A verifies its paper end to end above the classical spectral input; S-B
verifies the arithmetic and representation-theoretic content (B1-B11) and explicitly does
NOT verify the differential-geometric identifications that give those numbers their names.

### Blindspot pass (redone for these operators)

| Blindspot | Mitigation |
| --- | --- |
| The solver reconstructs the target rule instead of measuring it (representation theory can be done "the paper's way" by accident) | the specs route the computation through explicit 2×2 matrix generators, group closure, explicit symmetric powers and averaging projectors; graph distances come from BFS on an adjacency matrix built out of inner products, never from a Dynkin label |
| A character-table shortcut from a library would smuggle in the classification | agents build every group, every irreducible character and every branching from generators and linear algebra; no group-theory package tables |
| A truncated level range hides the exceptional case (a gap at level 6 is invisible if m stops at 4) | the specs require levels to m = 12 and symmetric powers to a = 14, well past anything either paper needs |
| A dual / conjugate convention (τ vs τ\*) silently flips a multiplicity | the specs require BOTH conventions computed and reported, so convention sensitivity is visible rather than chosen |
| Floating-point rank estimates fake an invariant subspace | invariant dimensions are computed as exact character sums AND as SVD ranks with a stated tolerance; disagreement is a reportable defect |
| Exact rationals silently become floats, hiding a small discrepancy | exact arithmetic is required wherever a claim is a rational number, with the exact value reported alongside any decimal |
| Only 2I is exercised, so a "unique exception" claim goes untested | the specs require the full ADE list (cyclic, binary dihedral, 2T, 2O, 2I), so uniqueness is measured, not assumed |
| Independence breach through the repository | agents write to the session scratchpad and are instructed to open no repository file; the papers never enter the repo |

### Definition of done (finalized at go)

| # | Item |
| --- | --- |
| 1 | Solver A + Solver B return converged numbers with scripts + JSON (`m8_1_1_` prefixes) |
| 2 | Audit A + Audit B recompute by their own methods, audit the solver scripts, and give per-claim verdicts |
| 3 | Designer comparison against A1-A7 and B1-B11, every number stated |
| 4 | Method note `findings/m8_1_1_method_note.md` (equations first, equation-to-code map, embedded plots, audit record, not-computed list) |
| 5 | Doc sync: canonical, briefing, MODELS.md cells if a cell moves, roadmap row |
| 6 | Doc checker exit 0; TASK REVIEW presented in the terminal |

## DEVIATIONS LOG

| Date | Deviation | Disposition |
| --- | --- | --- |
| 2026-07-28 | The method-note standard asks for the equations to live in a small single-purpose module. The two solver scripts are monoliths (1116 and 1751 lines) because a blind agent wrote each one end to end | Kept UNMODIFIED and landed as-is. Provenance was judged the higher value: any designer refactor would break the claim that the landed code is the blind agent's own. Compensated by an exhaustive equation-to-code line map in the method note § 3 |
| 2026-07-28 | The agents wrote into the session scratchpad rather than directly into the repository | Deliberate hardening of the blindness protocol beyond what M8.1 did: an agent that never opens the repo cannot find a claimed value in it. The designer copied the scripts and JSON in afterwards, unmodified |
| 2026-07-28 | Spec sheet A's task T7 asks for the least level `k >= 0` at which the twist occurs, which returns `k = 0` for the trivial twist (the constants) | A spec artifact, not a claim failure: constants carry no exact 1-form. Recorded rather than silently dropped, and the substantive statement was checked separately by looking at the least `k >= 1`, which is 0 occurrences at level 1 for every nontrivial group |

## FINDINGS

Full record with equations, the code map, figures and the audit:
[`../findings/m8_1_1_method_note.md`](../findings/m8_1_1_method_note.md).

| ID | Finding |
| --- | --- |
| F1 | **BOTH PAPERS VERIFY.** All 18 pre-registered claims (A1-A7, B1-B11) are CONFIRMED by blind agents that never saw a claimed value, and neither adversarial audit refuted anything: audit A returned all-confirmed over a widened 34-group family, audit B returned 139 confirmed, 1 partial, 0 refuted over 37 groups and 6912 twists |
| F2 | **The headline classification survives an attack designed to break it.** The adjoint coexact bottom is 4 for every irreducible flat SU(2) connection except one, which is 36. The audit widened from 14 connections to 41 (binary dihedral out to n = 12) and q² took exactly TWO values across all of them: 4 on forty, 36 on one. The exception is the distance-7 connection of the order-120 group, whose adjoint sits at distance 6 |
| F3 | **The blind agents reconstructed the affine E8 diagram from matrix generators.** Distances `[0, 7, 1, 2, 6, 3, 6, 4, 5]` over dimensions `[1, 2, 2, 3, 3, 4, 4, 5, 6]`, the branch node, and the two three-dimensional adjoints at distances 2 and 6, none of it supplied. The first-occurrence rule (least symmetric power = graph distance) held for all 344 irreducibles tested, with the parity restriction holding exactly where the group contains −I and failing where it does not |
| F4 | **The exact rational arithmetic of the second paper reproduces to the digit**, including the five character sums, the four defect sums, the four charges with their fractional parts, the vector H with the distance-6 assignment the paper specifies, the augmentation −72 by two independent routes, and the lattice package (240 roots, 120 mod-2 classes, counts 136 / 120, a single reflection orbit) |
| F5 | **The asymmetry's support is exactly where the paper says.** The two adjoints differ on precisely the four conjugacy classes of element order 5 and 10; the other four non-identity classes contribute an identical −19/160 to each, which is the paper's −57/4 over the group order, and the differing classes contribute 2/5 and 0, which is its 48 and 0 over the group order |
| F6 | ⚠️ **The conversion identity is FORCED, not contingent, and my first writeup overstated it.** Audit B derived in two lines that `S(f) = f(I) + 4 D(f) - 4 f(I) D(1) - <f,1>` for any finite subgroup and any class function, so the coefficient triple `(1, 4, -4)` and the offset-equals-multiplicity result cannot come out otherwise. The paper agrees: it calls its Theorem 1.1 elementary and locates its novelty in recording the exact form. The blind fit therefore tests the group construction and the arithmetic, not a law that could have failed. The overclaim was the platform's, not the author's |
| F7 | **Four checks that cannot fail were found across the two solvers**, plus one mutation that ran green while the E8 Cartan matrix had been swapped for D8. The numbers are unaffected (the audit verified the diagram independently), but the lattice section of any successor script needs an assertion on the diagram itself. This is the M8.2 standing rule paying off a second time |
| F8 | **Scope, stated honestly:** this run verifies the representation-theoretic and arithmetic content of both papers. It does NOT verify the classical geometric inputs they build on (the defect formula computing the rho invariant, the Dirac-eta identity, the index integral, the round-sphere coexact spectrum), the topology proofs of the second paper's § 7, or the agreement with printed literature values, which is external-source comparison rather than recompute |

## TASK REVIEW (2026-07-28)

`Task Duration: 01:35 (from 18:28 to 20:03 EDT)`
`Usage Cap Triggered: NO`

| Item | Outcome |
| --- | --- |
| S-A claims A1-A7 | ✅ ALL CONFIRMED blind: 18 groups, 114 irreducibles, two internal methods agreeing on 1408 of 1408 multiplicity cases |
| S-B claims B1-B11 | ✅ ALL CONFIRMED blind, exact rational arithmetic throughout |
| Audit A (exact GF(p), isotypic splitting) | ✅ all confirmed, nothing refuted; widened to 34 groups, 344 irreducibles, 41 connections |
| Audit B (presentations, induced characters, element sums, a field-free rational route) | ✅ 139 confirmed, 1 partial, 0 refuted; widened to 37 groups and 6912 twists including virtual characters |
| The headline classification | ✅ bottom 4 on forty connections, 36 on exactly one, two distinct values across the widened family |
| B1 / B2 evidential weight | ⚠️ CORRECTED DOWNWARD: the identity is algebraically forced (§ 5.1 of the method note) |

**Issues**: four checks that cannot fail were found across the two solvers, and one mutation
ran green with the E8 Cartan matrix swapped for D8, so nothing asserts the diagram is the
one claimed. No number is affected. The substantive issue was the platform's own framing
of B1 and B2 as an empirical discovery, corrected in the note and marked as excluded
evidence rather than dropped; the paper itself calls the theorem elementary, so the
overclaim was never the author's.

**Deviations from plan**: three, logged in the DEVIATIONS LOG above.

**Action needed**: doc sync applied at review (MODELS.md confinement cell prose with the
icon deliberately unmoved, the canonical registry's two bedrock rows, the briefing row);
the author is to be tagged on the PR carrying this task, with a link to the method note.

**Findings**: Both remaining MIT bedrock papers survive blind independent verification: the
coexact-gap classification (bottom 4 for every irreducible flat SU(2) connection with
exactly one exception at 36, holding across a widened 41-connection family) and the full
arithmetic of the affine conversion paper (character sums, defect sums, charges, the
augmentation −72 by two independent routes, and the 240 → 120 lattice package). Two blind
agents reconstructed the affine E8 diagram from matrix generators alone. The one
substantive qualification is a downgrade the platform owes itself rather than the author:
the conversion identity is algebraically forced, so the blind fit tests the arithmetic and
not a falsifiable law, which leaves the gap classification as the run's genuinely
contingent result.

**Research documents created / updated**:
[`m8_1_1_task_details.md`](m8_1_1_task_details.md) (this doc),
[`../findings/m8_1_1_method_note.md`](../findings/m8_1_1_method_note.md),
[`../m8_theory_canonical.md`](../m8_theory_canonical.md) (both bedrock rows flip),
[`../m8_roadmap.md`](../m8_roadmap.md) (M8.1.1 → Done),
[`../../__M8_model_briefing.md`](../../__M8_model_briefing.md) (the mass-gap row),
[`MODELS.md`](../../../../../MODELS.md) (M8 confinement cell prose, icon unmoved).

Artifacts: `scripts/m8_1_1_coexact_solver.py`, `m8_1_1_defect_solver.py`,
`m8_1_1_plots.py`, `m8_1_1_audit_a/`, `m8_1_1_audit_b/`;
`data/m8_1_1_{coexact,defect,coexact_audit,defect_audit}.json` + the raw solver output;
`plots/m8_1_1_{gap_by_connection,first_occurrence,2i_graph,affine_relation,golden_support}.png`
(all embedded in the method note).
