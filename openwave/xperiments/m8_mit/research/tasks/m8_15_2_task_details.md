# M8.15.2: LOCATING THROUGH THE AVOIDED CROSSING ON T2/R4 AND T3/R5, a delta on M8.15.1's terms

Pre-registration, for review. It governs nothing until the maintainer's go. **No M8.15.2 target has been run.** T2/R4 and T3/R5 have been run in M8.15's run and in M8.15.1's, and every record of both is disclosed below. The locator v2 exists, and only its controls and tests have been run. It passes every registered test ([`RESULT_5.md`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/RESULT_5.md)).

## TASK PLANNING

### The question

**What M8.15.1 left open.** Its run was adjudicated on [#625](https://github.com/openwave-labs/openwave/pull/625#pullrequestreview-5492753760) on 2026-10-12. No change of type is located.
- Both primaries read "no genuine crossing detected" at both levels, each with an Unresolved step (structural subspace).
- In all four of those bisections both ends pass every check, and a midpoint fails the structural subspace check. The frozen locator ends the bisection there, as `REGISTER_4.md`'s S10 registered.
- The clean ends read as a genuine doublet: `Δh = ±2` with `Δn_S = 0`, and `n(B|G_tol) = 5` on both sides, at both levels.

**What this task asks:** whether the genuine index change can be located through that failure:
- bracketed by `n(L)`, which no mixing among eigenvectors can change;
- classified from clean points fixed in advance on each side;
- confirmed by the full verdict at the guard offsets, as M8.15.1 confirms it.

**The reading** (INFERRED, from M8.15.1's near-zero spectra). The failure is an avoided crossing. The genuine doublet crosses zero and meets the rotation doublet, which the mesh has split off zero. The two share a symmetry, so they mix instead of crossing (the memo, § 1).

**Why this task exists.** M8.15.1's primary steps ended Unresolved. The mechanism was named in `REGISTER_4.md`'s amendment of 2026-10-09T22:10:11Z, before any run. That naming is not a prediction of M8.15.1's outcome.

**Two different claims,** as in M8.15.1. A change in `L`'s negative index is observable numerical evidence. Identifying it with a mode, and with a change of type, takes the further checks.

### Standing

- **The ruling it files under** is [#512](https://github.com/openwave-labs/openwave/discussions/512#discussioncomment-18415036)'s, as M8.15's and M8.15.1's were. Nothing here uses chassis code or input, or anything from `m8_5c/design_inputs/`.
- **Run-before-write** (`PR_REVIEW_STANDARDS.md` § 12.2) is met. M8.15.1 ran and was adjudicated on 2026-10-12 ([#625](https://github.com/openwave-labs/openwave/pull/625)). Since then the column has landed the author's records after the verdict ([#628](https://github.com/openwave-labs/openwave/pull/628)) and a one-line maintainer edit to M8.12's method note ([#629](https://github.com/openwave-labs/openwave/pull/629)).
- **Word budget.** About 5,500 words, inside § 12.2's cap of about 8,000.
- **ID.** M8.15.2 follows M8.15.1 as M8.15.1 followed M8.15. The row this pull request creates allocates it (`ROADMAP_STANDARDS.md` § 6). If a row taking M8.15.2 lands first, whoever merges second renumbers this one.
- **Inherited.** Every rule of M8.15.1's terms that this document does not change governs here, and through them M8.15's. M8.15.1's governing text is its filed pre-registration, SHA-256 `fc566c04…`, the prefix of [`m8_15_1_task_details.md`](https://github.com/openwave-labs/openwave/blob/9bb7672b9467464f1f3257299e363436dcd64040/openwave/xperiments/m8_mit/research/tasks/m8_15_1_task_details.md) that its dated note of 2026-10-12 names; that note's correction to § Standing carries over. Inherited unchanged:
  - the law, the solver, the continuation, the ladder, the linear verdict at a point, and the frozen values (M8.15's);
  - the instrument at MIT `97a8c08`, with the fast-spectrum defect recorded and not repaired;
  - the verdict at a point, `decide`, extracted from the frozen driver;
  - the locator's point data and checks (§ THE LOCATOR, step 2), the grid (3), the root and the cross-level shift (6), collisions (7) and Newton failures (8);
  - within step 5, the reading ends, the crossing set, coverage, classes, the bookkeeping and the rule against genuine and structural crossings in one step, as § THE LOCATOR: WHAT CHANGES applies them;
  - the confirmation at guard offsets, which readings count, and the reading on a side;
  - the naming, with the ceiling's clauses 1 and 2;
  - what is reported, and the residual tolerance `10⁻¹¹`.
- **What this task adds** is the locator v2: M8.15.1's locator with one change, which bisects through the failure, and one added check, of solution continuity. It is new code in a folder of its own, beside M8.15.1's, which it leaves unchanged. It reads the frozen instrument without changing it. It was qualified on controls and synthetic tests (`REGISTER_5.md`, `RESULT_5.md`) and frozen at MIT `851b2ad` before any target ran.
- **No repair.** The instrument at `97a8c08` is unchanged, and so is its manifest.

### What this task is not

- There is no persistence test.
- There is no claim about any branch other than T2/R4 and T3/R5, and within those, about the two primary brackets only. The secondary is not run (§ THE BRANCHES).
- The constrained index stays out: the inertia of `L` on the `M`-orthogonal complement of `P`. It is the next step if this task cannot classify the steps.
- T1 and T4 stay blocked, as in M8.15.1. There is no slot relation, and M8.15's row 6 ceiling carries over.
- No `MODELS.md` cell moves, and M8.7's gate is unchanged.

### Ownership and run format

As M8.15.1's terms provide. The author's agents build and run the locator v2 under the frozen terms and publish the scripts, data and records with a reproduction route. The frozen terms' SHA-256 lands on MIT `main` before the run starts. Reproduction is optional for the maintainers. Adjudication is the maintainer's, under § NAMING with its ceiling.

### Sources of record

| Source | What it supplies |
| --- | --- |
| [M8.15.1's task document](https://github.com/openwave-labs/openwave/blob/dcc638515f0df515fa2d32d65e9009f06eafacc3/openwave/xperiments/m8_mit/research/tasks/m8_15_1_task_details.md) at `dcc63851` | the inherited terms, with M8.15's through them |
| MIT [`soft-slot-dynamics-m8-15x-target1/`](https://github.com/dmobius3/mode-identity-theory/tree/b13e0f4bd1d3763215046b9c6ab1c9b87f94a379/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1) at `b13e0f4` | M8.15.1's locator, frozen at `324fde3`; its run record `RECORD.md`, committed at `c4e2f7f` with its post-run correction at `a261c7a` and its post-adjudication note at `b13e0f4`; the target records `out/t1_T2_R4.json` and `out/t1_T3_R5.json`; and RESULT_4's control records |
| MIT [`soft-slot-dynamics-m8-15x/`](https://github.com/dmobius3/mode-identity-theory/tree/97a8c0884c5e3a0ed25afb345f3d668340c5b537/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x) at `97a8c08` | the instrument |
| MIT [`soft-slot-dynamics-m8-15-2/`](https://github.com/dmobius3/mode-identity-theory/tree/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2) at `851b2ad` | the locator v2: its code and manifest; its registration `REGISTER_5.md`; its tests' results `RESULT_5.md`, with the tests' records and the diff against `324fde3`; its adjudication reading `adjudicate.py`, with its check; and in `scope/` the scope memo v7 ("the memo"), `recon_numbers.py` and `plant_oracle.py` with their outputs |
| OpenWave [#625](https://github.com/openwave-labs/openwave/pull/625) | M8.15.1's adjudication and approvals, the method note's fix merged at `99b2ca07`, and the reply |
| OpenWave [#628](https://github.com/openwave-labs/openwave/pull/628), merged at `9bb7672b` | the author's records after the verdict, and the approval's two notes |
| This task | the rule, the continuity check, the ceiling's clause 3, the brackets and the frozen values below |

## DISCLOSURE (the memo's ground rule 4)

The terms state everything this follow-up has already seen. No rule below is justified by any of it.

- **Every M8.15 and M8.15.1 record,** M8.15.1's method note, its post-run correction, its overnight log and `summarize_t1.py`.
- **The recon of 2026-10-12,** whose findings are the memo's § 1 and § 5, with the assessment that T5/R2 is not a usable control; and the independent review of the recon.
- **`recon_numbers.py`,** with its full output. It prints every number this document quotes about the targets and the controls.
- **Both review units' reviews** of M8.15.1's record and of every version of the memo, including one unit's two-level reading and identity prediction, and the other's counterexample.
- **#625's thread:** the adjudication (review 5492753760), with its question on a pitchfork; the approvals (reviews 5495195497 and 5495207564); the method note's fix `c6ad6cc5`, merged at `99b2ca07`; and the reply (issuecomment-6128592936), with its bifurcation reading.
- **The records after the verdict:** MIT `b13e0f4` (the post-adjudication note in `RECORD.md`, its two dated post-run verifications, and the § VI note in `soft-slot-branches.md`), and #628, merged at `9bb7672b` after its approval (review 5496563777), with its two notes: level 2's primaries lie on one path by a cross-level test, and T2/R4's levels place the change apart.
- **The unit review** in which the continuity check, the secondary's reason and this list were proposed after #625, and both units' agreement to them.
- **The counts-level simulation** of the rule on the coupled mock, and a rough two-level fit at the targets' failing midpoints (§ THE LOCATOR: WHAT CHANGES), with both units' agreement to close the gap that fit pointed to, on their conditions.

**What failed, read from M8.15.1's records.**

| | Level 3: ends; failing midpoint | Level 2: ends; failing midpoint | `h` at the ends |
|---|---|---|---|
| T2/R4 | 16.258883, 16.310660; 16.284772 | 16.0, 16.828427; 16.414214 | 0 → 2 |
| T3/R5 | 15.780330, 15.798636; 15.789483 | 15.707107, 16.0; 15.853553 | 6 → 4 |

- **At every failing midpoint** `n(L)` equals one end's: the lower end's on T2/R4, the upper end's on T3/R5. At the failing midpoints both doublets' overlaps with `P` sit at 0.49 to 0.87, so exactly `d` structural eigenvectors cannot be found.
- **The slowest pair's overlap with the rotations** peaks at T3/R5's failing midpoints, 0.868 at level 3 and 0.892 at level 2, and is below `10⁻¹¹` at T2/R4's.
- **The mechanism bit above the bisection width,** at level 3 at widths of `3.18×10⁻³` (T2/R4) and `1.16×10⁻³` (T3/R5) of the lower end, and at level 2 at the first midpoint (T2/R4) and the second (T3/R5).

**Stated before the run, as disclosure and not grounds** (the memo, § 5).

| | T2/R4 | T3/R5 |
|---|---|---|
| The crossing pair's interpolated zero, level 3 / level 2 | 16.281034 / 16.345786 | 15.793527 / 15.829021 |
| Where `n(L)` changes, level 3 | (16.284772, 16.310660] | (15.780330, 15.789483] |
| Where `n(L)` changes, level 2 | (16.414214, 16.828427] | (15.707107, 15.853553] |
| The two-level identity angle, level 3 / level 2 | 15.8° (0.962) / 16.0° (0.961) | 36.5° (0.804) / 28.2° (0.881) |

- **The identity prediction.** The two-level model predicts T3/R5 failing the full identity check at both levels, while T2/R4 passes at 0.96. It predicts the comparison outside `P` passing on both, so both, where located, would carry clause 3's name (§ NAMING).
- **The level-2 guards.** On T2/R4 `n(L)` changes up to 2.95% above the interpolated zero, so a level-2 guard between the two reads the other side's `h` and does not count, and the reading may come from a larger offset. That fails closed. On T3/R5 the change lies within 0.77% of the zero.

**What rests on the records: the scope.** They chose the question: the two primary steps, both run, and the secondary dropped. Nothing in the rule rests on them.
- #625's finding prompted the continuity check. Its grounds do not rest on the records: M8.15.1's terms foresaw the singular Jacobian, and the tolerance comes from the controls. Its statistic was also computed on the target records (§ THE SOLUTION-CONTINUITY CHECK), so its multiple was set with those values in view.
- The rough fit at the targets' failing midpoints prompted closing the gap in the rule rather than only registering it. The fix's ground is the two-level model alone.

## THE BRANCHES, THE BRACKETS AND THE GUARD REGIONS

M8.15.1's primary brackets and guard regions, unchanged.

| Branch | Bracket in `ε` | `n(L)` across it, level 3 (level 2) | Guard region | Label |
|---|---|---|---|---|
| T2/R4 | 16 to 22.63 | 5 to 7 (5 to 7) | 11.31 to 32 | primary |
| T3/R5 | 11.31 to 16 | 12 to 9 (11 to 9) | 11.31 to 22.63 | primary |

- **The index arithmetic** is M8.15.1's: a genuine change of +2 on T2/R4, and of −2 on T3/R5 at both levels, which at level 3 comes with one structural step.
- **The ladder** is rerun to the largest registered region end: 32 on T2/R4, and 22.63 on T3/R5.
- **The secondary is dropped.** Its steps lie on or across two solution paths near a likely bifurcation (#625).
  - On the ladder's branch the index change lies between 27.313708 and 28.485281 at level 3, and between 27.313708 and 32 at level 2. No evaluated point of that branch falls inside either interval.
  - **The bifurcation reading (INFERRED).** At level 3, on the ladder's path from 26.142136 to 29.656854, the critical eigenvalue's local slopes are +0.091 to +0.102, and it crosses zero near 27.82. On the second path it fits `−0.183(ε − 27.78)` over the 10 points the bisection evaluated between 27.313708 and 28.485281, with residuals at most `1.3×10⁻³`. The slope ratio, −1.8 to −2.0, is consistent with a pitchfork's −2 rather than a transcritical −1. Which symmetry the second path breaks, and whether it bifurcates from T3/R5's branch, are open.
  - Neither the change nor the continuity check locates a change along one branch through a bifurcation. That needs a rule for staying on the ladder's branch, which this task does not attempt.
- **Both primaries run.** A frozen rule that classifies one and not the other says something, and so does one that classifies both.

## THE LOCATOR: WHAT CHANGES

Steps 4 and 5 of M8.15.1's § THE LOCATOR change as below, and a new step follows them (§ THE SOLUTION-CONTINUITY CHECK). Every other step stands. The rules are registered in `REGISTER_5.md` § 1, which these words follow.

**The bisection (step 4), for a sub-interval whose ends' `n(L)` differ.** A sub-interval whose ends share `n(L)` keeps M8.15.1's step 4.
1. **Four points are carried:** a lower and an upper `n(L)` end, and a lower and an upper clean end. At the start each pair is the sub-interval's two ends.
2. **Each midpoint** is reached from the current lower `n(L)` end, failing or clean, by the frozen secant, as M8.15.1's bisection reaches it from its lower end.
3. **A failing midpoint is passed** when its failed checks are the structural subspace, the slowest pair's overlap, or both, and its Newton solve converged.
   - Its `n(L)` replaces the `n(L)` end it equals. If it equals neither, the step is Unresolved (passed midpoint matches neither end).
   - A failure of the span's gate or of coverage, alone or with a passable check, ends the step as in M8.15.1, Unresolved with its checks as the reason. So does a Newton failure.
   - A passed midpoint stays Unresolved as a point: the bisection takes only its `n(L)`.
4. **A clean midpoint** whose `(n(L), n_S)` equals one side's clean end's becomes both that side's `n(L)` end and its clean end.
5. **An exchanged-lift point.** After a failure, a clean midpoint whose `n(L)` equals one side's and whose `n_S` is below that side's clean end's is passed on `n(L)` alone. It replaces that side's `n(L)` end, is never a clean end, and certifies no crossing. Its `n_S` is compared with that side's preserved clean end, never with a passed point that moved the `n(L)` end.
6. **Any other clean midpoint after a failure** with neither side's counts makes the step Unresolved (neither side's counts after a failure), including one whose `n_S` is above its side's. Before any failure, M8.15.1's split applies.
7. **The stop:** the `n(L)` ends within `10⁻³` of the lower one.

**The step (step 5).** The step is analysed between its clean ends exactly as M8.15.1 analyses a final interval: the reading ends found outward from them, the crossing set, coverage, classes, the bookkeeping, the rule against genuine and structural crossings in one step, and the root. Three things change.
- **The clean window's limit,** checked first, before the reading-end search. A step whose clean ends lie more than one grid cell apart, beyond a relative `10⁻⁹` for rounding, is Unresolved (clean window over one grid cell). One grid cell is the bracket's width over 8.
- **A branch step** is a step whose reading interval holds a point that failed its checks, or an exchanged-lift point.
- **In a branch step the classes are read first,** after the crossing set and coverage.
  - A crossing classed mixed makes the step Unresolved (mixed overlap), before any identity test.
  - For the crossings classed genuine at both ends, two cosines are computed and recorded: the full one, as frozen, and the one outside `P`. The latter takes each end's crossing vectors' components `M`-orthogonal to that end's own `P`, re-orthonormalized, and reads their principal cosines. Outside `P` below 0.9 is Unresolved (crossing identity), and so is a set outside `P` with fewer cosines than crossings.
  - The crossings classed structural keep the frozen check.
  - Outside a branch step, the frozen order and check stand.
  - **M8.15.1's note that the mixed-overlap rule cannot fire** rests on the identity check coming first. In a branch step the classes come first, and the rule fires on the mock: A1 at `κ/δ = 2`, at both slopes, and A2 at `2δ`. Outside a branch step the note stands.

**The grounds.** They are registered before any target runs, and none is a target outcome.
- **The mechanism,** named in `REGISTER_4.md`'s amendment of 2026-10-09T22:10:11Z: near the root the crossing eigenvalue approaches the lifts', and a mode sharing their symmetry can mix with them, so the structural subspace and identity checks report Unresolved.
- **A property of the count (DERIVED).** `n(L)` is the number of eigenvalues of `(L, M)` below `−tol_L`, a function of the eigenvalues alone, so no mixing among eigenvectors changes it.
- **Why the span's gate and coverage stay terminal (DERIVED).** The span's gate is computed from `P` alone, built from the exact generators, so mixing among `L`'s eigenvectors cannot reach it. Coverage compares `P` with the span of the near-zero eigenvectors, which mixing between two of them leaves unchanged. The two passable checks are those the mixing can trip (INFERRED for the slowest pair, as the memo marks it), and the slowest-pair check stays in force at the clean ends and at the guards.
- **The mechanism reduced to two levels** (DERIVED in the model; the memo, § 2): a lift at `−δ`, the genuine pair's unmixed `g = s(ε − r)`, and a coupling `κ`.
  - `n(L)` changes `κ²/(|s|δ)` from the pair's zero.
  - The genuine character passes from one spectral branch to the other, while the crossing vectors' components outside `P` agree.
  - The structural subspace check fails where `|g + δ| < 1.580κ`. Above `κ/δ = 2.06` a clean interval separates that window from the `n(L)` change, and in it the coupled lifts sit above zero. These are the exchanged-lift points.
- **The comparison outside `P`.** Its bounds are DERIVED in the memo, § 2: two different genuine directions agree outside `P` to at most 0.105. It identifies the genuine direction, not the spectral branch that crosses zero: one unit's counterexample has two branches exchanging one genuine direction, agreeing outside `P` at 1.000 and in full at 0.862. The full cosine does not test branch identity either. So no branch step claims it, and the name in a branch step says the identification is not established (§ NAMING).
- **The synthetic plants** of `REGISTER_5.md` § 2.

**Disclosure on the exchanged-lift pass.** A rough two-level fit at each failing midpoint gives `κ/δ` of 2.25 (T2/R4, level 3), 3.08 (T2/R4, level 2), 2.31 (T3/R5, level 3) and 2.16 (T3/R5, level 2). On that fit, T2/R4 level 2's next midpoints meet a clean interval from 16.4608 to 16.5286, at 16.5178. Without the pass that midpoint would end the step Unresolved. The fit is rough, and it is not grounds.

**Not certified.** The clean window is not certified free of further crossings whose net change is zero, like any interval here. The `n(L)` bisection locates a change; it does not make the crossing unique.

## THE SOLUTION-CONTINUITY CHECK

A new step, at each level, after that level's scan and bisections end and before any step is matched across levels or any guard is evaluated. Every step at both levels must pass it, branch step or not.
- **What it reads:** each stored point record's `m`, the norm in which the frozen continuation runs, and its reached `ε`. It launches no solve, and the order of evaluation plays no part.
- **The pool:** the bracket's evaluated points at that level at that moment, which are the guard region's ladder points, the grid points and every bisection midpoint. Every successful evaluation is kept as its own record. The pool is ordered by reached `ε`.
- **Duplicate targets:** two or more successful evaluations whose targets agree within `10⁻⁹`, relative. A step whose span, reading ends or predictors include one is Unresolved (solution continuity, duplicate target), and that reason stands where a comparison also fails. The record says whether the records agree value for value.
- **A step's span:** its starting interval, the adjacent usable grid points between which its bisection began, widened to its reading ends where they lie outside. The steps a split produces share it. A step with no reading ends takes its starting interval. A point belongs to the span by its target `ε`.
- **The comparisons,** each a forward extrapolation of a point's `m` along the straight line through the two pool points immediately below it in reached `ε`:
  - along the span: every pool point in the span except the lowest;
  - across the step: the upper reading end, against the line through the lower reading end and the pool point immediately below that.
- **The statistic:** the absolute miss over `h₂(h₁ + h₂)/2`, where `h₁` is the spacing of the two predictors and `h₂` the step to the compared point, both in reached `ε`. Along one smooth path it estimates the path's own curvature, at any width (DERIVED).
- **Degenerate comparisons fail closed:** fewer than two pool points below, or `h₁` or `h₂` not above `10⁻⁹` of the compared point's reached `ε`. The step is then Unresolved (solution continuity). No comparison is skipped.
- **Two consequences for the targets,** fixed before any target runs:
  - **The first cell.** T3/R5's guard region and primary bracket both start at 11.313708, the pool's lowest point at both levels. So a step in its first cell, up to 11.899495, has a compared point with one point below it, and is Unresolved (solution continuity). M8.15.1 had 0 steps there. T2/R4's guard region starts below its bracket, at 11.313708.
  - **A lone failing grid point.** The bisection's first midpoint re-evaluates it, within `2.0×10⁻¹⁶` relative on the targets' brackets. So a step whose bisection starts across one is Unresolved (solution continuity, duplicate target), unless it is already Unresolved. M8.15.1's primaries had 0 failing grid points.
- **The tolerance,** `τ_c = 3.4601×10⁻³`, is ten times the largest statistic over the control brackets' pools, at both levels: `3.4601×10⁻⁴`, on C3 at level 3 at 12.485281. A comparison above it makes the step Unresolved (solution continuity). Over the controls' full ladders, 0.25 to 72, the statistic reaches `4.1580×10⁻⁴` (C3, level 3, at 0.5); the basis stays the brackets' pools. Only this multiple is scored, and the record carries every statistic, so others can be read from it as diagnostics.
- **A step already Unresolved** keeps its reason, and the record carries its comparisons beside it. The check adds a reason for Unresolved and removes none, so it can stop a result but never rescue one.
- **Its grounds.** None of them is #625's records.
  - M8.15.1's terms (§ THE LOCATOR, step 8) expect Newton's bordered Jacobian to be nearly singular near the root of a crossing whose mode lies in the pinned fixed space.
  - Where a Jacobian is singular, the implicit function theorem fails. So the solutions need not form one path there, and a converged solve need not stay on the path it started from (DERIVED, a standard fact).
  - The bisection now closes in on the `n(L)` change, where `L` is singular to within `tol_L`. The primaries' doubled crossings are expected to lie outside the pinned fixed space (INFERRED, M8.15.1's step 8), so the check guards against a possibility, not an expected switch.
- **Prompted by #625,** which found the secondary's steps joining two solution paths while every registered check passed.
- **Not certified.** It is an operational screen on one scalar, not a proof that a step's points lie on one branch.
  - It is local to the step's span. A step whose span lies wholly on another path, reached by a switch outside it, passes.
  - Where two paths meet they share `m`, so a switch near that point changes the statistic little (DERIVED).
- **On M8.15.1's records (disclosure, not grounds).** Over the comparisons the check makes, the primaries read at most `3.8×10⁻⁴` (T2/R4) and `7.5×10⁻⁴` (T3/R5), 2.2 times the controls' largest, and the controls' steps at most `2.6×10⁻⁶`. On #625's secondary, level 3's starting interval reads `8.7×10⁻³` at 27.972718 and 8.4 at 28.485281, and level 2's reads 55.8 at 32. Every multiple from 2.2 to `2.4×10⁴` gives one outcome on these records: the primaries pass and both switches stop. So the values in view do not select 10.

## NAMING: WHAT CHANGES

**The ceiling gains clause 3.** Clauses 1 and 2, fast-spectrum dependence, carry over unchanged. A step either of them names unresolved stays so; clause 3 applies only to the steps they leave named a located change of type.
- **The trigger:** a genuine step that is a branch step at either level, and whose readings locate a change of type.
- **The name,** in these words, wherever it is cited: "A change of type is located between the registered guard readings. Its identification with the genuine index crossing at this step is not established: the crossing subspaces agree after removal of the structural directions, and the full spectral crossing identity remains unresolved. The step's classification crossed a structural-subspace or slowest-pair failure, or a point whose structural count fell below its side's, by a rule whose changed branch has synthetic controls only."
- **Why a qualifier.** The readings come from the full verdict at the guard offsets, which the change does not touch. What rests on the changed branch is the step's classification as genuine, and on it the identification of the confirmed type change with this crossing.

**The continuity check's limit travels with every located change of type.** Beside every name that locates a change of type, clause 3's included, this sentence stands wherever the name is reported: "The solution-continuity check does not certify which solution branch the step lies on, least of all where two branches share `m`."

**How the ceiling is applied.** As in M8.15.1, in adjudication, from the record; the record's own names stay M8.15.1's, and the locator records clause 3's trigger beside them.
- **One implementation.** The adjudication reads the ceiling through the function the tests verified, `ceiling` in the locator v2's `tests/synthetic.py`. The folder's `adjudicate.py` applies it to each target's bracket record as loaded from its JSON, with its level keys read as integers, the one difference between the record and the in-memory result the tests read. Its check reproduces the tests' names from every synthetic result written to JSON and read back, and fails without the key conversion.
- **A region end** is read from the bracket's evaluation of the rerun ladder's solution at that `ε`, whose slow count, and so its balance, is the ladder's own full point's.
- **The published result** carries the adjudicated name, with the record's automatic name beside it.

## REPORTED: WHAT IS ADDED

Each step adds:
- its starting interval, `n(L)` ends, clean ends and span;
- every failing midpoint and every exchanged-lift point, with its checks, counts and near-zero spectrum;
- whether such a point lies inside the reading interval, the branch flag;
- in a branch step, both identity cosines for the crossings classed genuine at both ends;
- every continuity comparison, with its three points, its two steps, the miss and the statistic;
- every duplicate target, with both point records and whether they agree value for value.

Each matched genuine step's record carries clause 3's trigger.

**Where `n(L)` changes.** In a branch step, the step's `lo` and `hi`, and its name's location intervals, are its clean ends. Where `n(L)` changes is its `nL_ends`, reported beside the root as M8.15.1's final interval is. Outside a branch step the two coincide (DERIVED: an `n(L)` end that is not its clean end is a failing or exchanged-lift point inside the clean window, and such a point makes the step a branch step).

## THE TESTS, BEFORE ANY TARGET (`REGISTER_5.md`)

**Every test's expected outcome was registered before the locator v2 was coded** (`REGISTER_5.md`, 2026-10-13T02:17:12Z), from a counts-level model of the rule on the plants' explicit eigenvectors.
- **M8.15.1's synthetic tests, S1 to S18c,** each with its arm. S10's expectation changes: the bisection passes its tilted midpoint and locates the step, which is not a branch step. Every other S test keeps its expectation and its record.
- **New synthetic plants, A1 to A29,** on the mock with a coupling between the genuine pair and two lifts, each with its arm. Among them: a genuine crossing through the mixing window for `κ` up to `6δ` with both slopes; a structural crossing in the same regime; the comparison outside `P` against turns and wrong pairings; path switches, a duplicate target, the secant's slack and a degenerate first cell for the continuity check; and cancelling changes.
- **The real-solver controls,** R1 to R5 and R4b, rerun on the locator v2. Each control record must reproduce RESULT_4's runs value for value outside the registered fields, and the new branch must not fire.
- **The guard's validation** on M8.15.2's own guard, with a negative control: M8.15.1's guard, present as on `main`, authorizes nothing.

**The results** (`RESULT_5.md`, reviewed and confirmed by both units). Every test passes, and every arm is caught: 52 synthetic tests with 55 arms, and the real-solver controls. All five control records reproduce RESULT_4's with 0 differences. The new branch never fires on a control, and the continuity statistic reads at most `2.63×10⁻⁶` on their steps.

**What is not covered.** No real-solver control exercises the new branch, the exchanged-lift pass or a path switch: no non-target control has a genuine crossing, none fails the structural subspace check, and none switches paths. The targets are the branch's first real use, and clause 3 carries it.

## FROZEN VALUES: WHAT IS NEW

- **The passable checks:** the structural subspace and the slowest pair's overlap.
- **The clean window's limit:** one grid cell, the bracket's width over 8, beyond a relative `10⁻⁹`.
- **The continuity check:** `τ_c = 3.4601×10⁻³`; duplicate targets within `10⁻⁹`, relative; a degenerate step not above `10⁻⁹` of the reached `ε`.
- **The brackets:** the two primaries above.
- **The instrument manifest's SHA-256,** pinned in the driver: `2b9864ab…`, the instrument's `out/MANIFEST.json` at `97a8c08`.

Everything else in M8.15.1's § FROZEN VALUES stands.

## THE FREEZE, THE GUARD AND THE RUN

1. **The locator v2 was built and qualified** (`REGISTER_5.md`, `RESULT_5.md`), then frozen in a folder of its own at MIT `851b2ad`, with its own manifest and `SHA256SUMS`. It reads the instrument at `97a8c08` unchanged, and leaves M8.15.1's folder at `324fde3` unchanged.
2. **The terms' SHA-256 lands on MIT `main`.** The freeze block, [`m8_15_2/freeze_block.md`](../m8_15_2/freeze_block.md), records it with the locator v2's and the instrument's commits and manifests.
3. **The guard file is M8.15.2's own,** `out/FROZEN.json` in the locator v2's folder.
   - **It is written once,** after the maintainer's go, by `write_guard.py`, which refuses if the file exists. The driver never writes it.
   - **Before it is written,** the run's pre-run check, as M8.15.1's run had, confirms the locator v2's folder against its frozen `SHA256SUMS` and the instrument's folder against its own, and stops on any mismatch. So the guard pins the frozen code.
   - **It holds** every value of the instrument's `out/freeze_numbers.json` unchanged; `frozen` true; these terms' SHA-256; the go; the instrument manifest's SHA-256; and the SHA-256 of the folder's `locate.py` and `t1_branch.py`.
   - **Before any solve** the driver checks that every value matches: the freeze values, the terms file given, the instrument's manifest as computed and as pinned, and the running `locate.py` and `t1_branch.py`. It refuses a target otherwise.
   - **It never reads the instrument's own `FROZEN.json`.** That file, M8.15.1's guard, and the instrument's folder stay as M8.15.1 left them.
4. **The run.** T2/R4, then T3/R5, primary brackets only. Each writes a record on every end, and a crash record on an instrument exception.
   - **Regression on the targets.** Up to each step's first failing midpoint, the run evaluates M8.15.1's points in the same order, and they reproduce M8.15.1's point records value for value. The ladder reproduces M8.15's, to 32 on T2/R4 and to 22.63 on T3/R5.

**Resources.** A level-3 phase peaks near 6.4 GB resident, so one branch runs at a time. M8.15.1's two runs took 6.5 hours, 5.1 of them on T3/R5 with its secondary. The guards add full-verdict points and the secondary is dropped, so the estimate is one overnight run.

## DEFINITION OF DONE

- **The record:** both branches' locator records, the tests' records, and the freeze, published with the scripts and a reproduction route.
- **Adjudication** is the maintainer's, under the naming above, with its ceiling.
- **What does not move:** no M8.15 or M8.15.1 record is reread, and no type outside the registered primary brackets is claimed.
