# M8.15.2 method note: locating through the avoided crossing on T2/R4 and T3/R5

Task: [`tasks/m8_15_2_task_details.md`](../tasks/m8_15_2_task_details.md), governing SHA-256 `c6da782b43bc13d2…`, a delta on M8.15.1's terms, pre-registered in [#630](https://github.com/openwave-labs/openwave/pull/630), run on 2026-10-13 from the frozen locator v2 at MIT `851b2ad`, which reads the M8.15.x instrument at MIT `97a8c08` unchanged. The record is [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/f1ebda711a83dd175e03ae585e1426b261955aac/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/RECORD.md) beside the locator v2. On T3/R5 a change of type is located between the guard readings, under the ceiling's clause 3. On T2/R4 the two levels disagree, and none is located. This note says why, against the frozen terms.

## 1. What the locator v2 changes

M8.15.1's method note, § 1, stands except as below. `R = c = g = 1`, and vectors are in M8.15's real form, with `⟨a, b⟩_M = aᵀMb`. `P` is the structural span, `n(L)` the negative index of `(L, M)` below `−tol_L`, `n_S` its structural part, and `h = n(L) − n(B|G_tol)` the genuine index, all as M8.15.1 defines them.

### 1.1 The bisection through a failure

For a grid sub-interval whose ends' `n(L)` differ:
- **Four points are carried:** a lower and an upper `n(L)` end, and a lower and an upper clean end, at first the sub-interval's two ends.
- **A failing midpoint is passed** when it fails only the structural subspace check, the slowest pair's overlap, or both, and its Newton solve converged. Its `n(L)` replaces the `n(L)` end it equals, and if it equals neither, the step is Unresolved. A failure of the span's gate or of coverage, or a Newton failure, still ends the step Unresolved.
- **A clean midpoint** with one side's `(n(L), n_S)` becomes that side's `n(L)` end and clean end. After a failure, a clean midpoint with one side's `n(L)` and an `n_S` below that side's clean end's, an exchanged lift, is passed on `n(L)` alone and is never a clean end. Any other clean midpoint after a failure makes the step Unresolved. Before any failure, M8.15.1's split applies.
- **The stop:** the `n(L)` ends within `10⁻³` of the lower one.
- **The ground (DERIVED).** `n(L)` is a function of the eigenvalues alone, so no mixing among eigenvectors changes it.

### 1.2 The step between its clean ends

The step is analysed between its clean ends as M8.15.1 analyses a final interval, with three changes.
- **The clean window:** clean ends more than one grid cell apart, the bracket's width over 8, beyond a relative `10⁻⁹`, make the step Unresolved.
- **A branch step** is one whose reading interval holds a failing or exchanged-lift point.
- **In a branch step the classes come first.** A crossing classed mixed makes the step Unresolved. For the crossings classed genuine at both ends, the identity is read outside `P`: each end's crossing vectors' components `M`-orthogonal to that end's own `P`, re-orthonormalized, must have principal cosines of at least 0.9, one per crossing. The full cosine is recorded beside it. The crossings classed structural keep the frozen check.

### 1.3 Solution continuity

At each level, before any step is matched across levels, each step's points are screened on `m`, the norm in which the frozen continuation runs. Each pool point in the step's span but the lowest is extrapolated forward from the two pool points immediately below it in reached `ε`, and the upper reading end from the lower reading end and the pool point below that. The statistic `|miss| / (h₂(h₁ + h₂)/2)` must not exceed `τ_c = 3.4601×10⁻³`, ten times the largest over the control brackets' pools. Degenerate comparisons and duplicate targets fail closed. The check screens one scalar. It does not certify which solution branch a step lies on.

### 1.4 The names

M8.15.1's names stand, and so do its ceiling's clauses 1 and 2. Clause 3 is new. A genuine step matched across levels, whose readings locate a change of type and which is a branch step at either level, takes the qualifier name of the terms' § NAMING. Beside every name that locates a change of type stands the continuity check's limit. The ceiling is applied in adjudication, from the record, through `ceiling` in the locator v2's `tests/synthetic.py`, which `adjudicate.py` applies to each target's record.

## 2. Equation-to-code map

The links are pinned to MIT `851b2ad` for the locator v2 and `97a8c08` for the instrument. M8.15.1's map covers everything else.

| Equation | Code |
| --- | --- |
| the bisection through a failure, with its four carried points | [`bisect`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/locate.py#L317) |
| the passed and exchanged-lift points, as recorded | [`midpoint_record`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/locate.py#L310) |
| the step between its clean ends: the clean window, the branch flag, the classes first | [`analyse_step`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/locate.py#L191) |
| the identity outside `P` | [`outside_P`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/locate.py#L183) |
| solution continuity | [`continuity`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/locate.py#L405) |
| the names, and clause 3's trigger | [`locate_bracket`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/locate.py#L637), [`name_step`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/locate.py#L605) |
| the ceiling, clauses 1 to 3 | [`ceiling`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/tests/synthetic.py#L432) |
| the adjudication reading, from the record | [`adjudicate`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/adjudicate.py#L28), [`int_levels`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/adjudicate.py#L19) |
| the guard file, written once | [`write`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/write_guard.py#L30) |
| the guard on a target | [`validate_guard`](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/t1_branch.py#L83) |
| the frozen numbers a target reads (§ 5.3) | [`frozen_numbers`](https://github.com/dmobius3/mode-identity-theory/blob/97a8c0884c5e3a0ed25afb345f3d668340c5b537/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x/m8_15x_solver/m815_branch.py#L42), called at [`t1_branch.py` line 152](https://github.com/dmobius3/mode-identity-theory/blob/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/t1_branch.py#L152) |

## 3. The run

- **Environment.** The run machine's Python, numpy, scipy and platform, checked before the run and after it, equal the instrument manifest's: Python 3.13.13, numpy 2.5.0, scipy 1.18.0, macOS 15.8 on arm64. The scripts pin one thread and fix the ARPACK starting vectors.
- **Before the run:** 13 checks passed at 2026-10-13T14:28:09Z, among them both `SHA256SUMS`, the terms against the merged file, the instrument's `FROZEN.json` against M8.15.1's record, and the guard written and checked on a scratch copy.
- **M8.15.2's guard file,** `out/FROZEN.json` in the locator v2's folder, was written once at 2026-10-13T14:28:09Z, before any target computation. It carries `freeze_numbers.json`'s values unchanged, the terms' SHA-256, the go, the instrument manifest's SHA-256 and the code's.
- **The targets:** T2/R4 from 2026-10-13T14:28:09Z to 2026-10-13T15:52:36Z, then T3/R5 from 2026-10-13T15:52:37Z to 2026-10-13T20:10:52Z. Both exited normally, with no crash record.
- **After the run:** both `SHA256SUMS` pass, both guard files are unchanged, and every point record carries its own frozen record.
- **The regression.** Both ladder reruns reproduce M8.15's. Every primary-bracket point of M8.15.1's two target records, and every ladder entry up to this run's last target, is evaluated again and reproduces value for value: 16 and 12 points on T2/R4's primary, and 22 and 12 on T3/R5's.
- **Deviations:** none. The orchestration lies outside the frozen set.

## 4. Results against the frozen terms

[`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/f1ebda711a83dd175e03ae585e1426b261955aac/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/RECORD.md) gives every number. Steps are given by their clean ends, with `Δn(L)`, `Δn_S`, `Δh`. A classified step's interpolated root is its crossing pair's interpolated zero, an estimate, not where `n(L)` changes.

| Bracket | Steps | The record's names | The ceiling, as `adjudicate.py` reads it (the adjudication is the maintainer's) |
| --- | --- | --- | --- |
| T2/R4, primary (16 to 22.6274) | level 3: genuine, 16.2589 to 16.2977; interpolated root 16.2807; 2, 0, 2; a branch step<br>level 2: Unresolved (index bookkeeping), 16 to 16.5307; a branch step | no genuine crossing detected at level 2<br>an Unresolved step (index bookkeeping), at level 2<br>an index crossing located; the change of type remains unresolved (cross-level disagreement) | no line: no genuine step is matched across levels, and the record's names stand |
| T3/R5, primary (11.3137 to 16) | level 3: structural, 13.1534 to 13.1626; interpolated root 13.1609; −1, −1, 0<br>level 3: genuine, 15.7803 to 15.7986; interpolated root 15.7935; −2, 0, −2; a branch step<br>level 2: genuine, 15.7437 to 16; interpolated root 15.8335; −2, 0, −2; a branch step | a structural step, at level 3<br>a located change of type | clauses 1 and 2 do not hold, and clause 3 does: the qualifier name, below |

- **T3/R5.** The genuine steps match across levels, so the guards are read. Each counts, and each of its points balances. The readings are Elliptic at `d = 0.01` (15.6356 at level 3, 15.6752 at level 2) and Hyperbolic at `d = 0.05` (16.5832, 16.6252). The upper guards at 0.01 and 0.02 are Unresolved (cross-level disagreement, level stability). No collision and no unbalanced point lies between the readings, and level 3's five unbalanced points lie inside the structural step's reading interval. The step is a branch step at both levels, so clause 3 holds. The name, in the terms' words:

  "A change of type is located between the registered guard readings. Its identification with the genuine index crossing at this step is not established: the crossing subspaces agree after removal of the structural directions, and the full spectral crossing identity remains unresolved. The step's classification crossed a structural-subspace or slowest-pair failure, or a point whose structural count fell below its side's, by a rule whose changed branch has synthetic controls only."

  Beside it: "The solution-continuity check does not certify which solution branch the step lies on, least of all where two branches share `m`."
- **Where.** The change of type is confirmed between the readings, and their evidence does not place it at the interpolated zeros. Those zeros, 15.7935 at level 3 and 15.8335 at level 2, a cross-level shift of `2.53×10⁻³`, are estimates for the genuine-classed crossing pairs. `n(L)` changes within 15.7803 to 15.7895 at level 3 and 15.7437 to 15.7529 at level 2, and neither zero lies inside them. On T2/R4, level 3's zero, 16.2807, likewise lies outside its `n(L)` ends, 16.2848 to 16.2977.
- **T2/R4.** Level 3's genuine step has no genuine match at level 2, so no guard is read and no change of type is located. The ceiling has nothing to restrict.
- **Solution continuity** passes at every step of both brackets. The largest statistic is `7.55×10⁻⁴`, at T3/R5's structural step, against `τ_c = 3.4601×10⁻³`.

## 5. Findings after the run

### 5.1 The genuine steps through the failures

- **The passed points.** Every failing point the bisections passed on `n(L)` failed the structural subspace check and nothing else: one at T2/R4's level 3 and one at its level 2, one at T3/R5's level 3 and four at its level 2. T2/R4's level 2 also passed one exchanged lift, at 16.5178. Each lies inside its step's reading interval. At T3/R5's failing points the counts are (9, 0, 1, 8), against (11, 2, 5, 6) and (9, 2, 5, 4) at the clean ends.
- **The identity.** At the three genuine steps, the crossing vectors' components outside `P` agree between the clean ends to cosines of 0.99990 to 0.999999, while the full cosines read 0.80 to 0.93. This is the pattern of the terms' two-level reduction of an avoided crossing, in which the genuine character passes between spectral branches while the components outside `P` agree (INFERRED: the reduction is a model, and these records are consistent with it). As the terms state, agreement outside `P` identifies the genuine direction, not the spectral branch that crosses zero.
- **Against the disclosure stated before the run.** Read as pass or fail against 0.9, the identity prediction held at three of the four steps whose crossings are classed genuine. T3/R5's full cosines read 0.804 and 0.824, below 0.9 at both levels, and T2/R4's level 3 read 0.931. Every comparison outside `P` passed. T2/R4's level 2 read 0.892 against the predicted 0.961: the prediction was computed at M8.15.1's final interval there, 16 to 16.8284, and this run's clean ends are 16 to 16.5307. At this run's clean ends the two-level angle gives all four recorded full cosines to three digits (INFERRED). The exchanged lift at 16.5178 came where the terms' rough fit placed it.

### 5.2 T2/R4's levels disagree

- **Level 3** classifies its step genuine, between clean ends 0.039 apart.
- **Level 2's** clean window is wider, 16 to 16.5307, and its upper clean end reads `n(B|G_tol) = 7` where the lower reads 5. So `h` is 0 at both ends against two genuine crossings, and the step is Unresolved (index bookkeeping).
- Whether level 2's cluster count takes in the crossing pair at 16.5307 is open.

### 5.3 Corrections on the record

- **A target run reads the instrument's own `FROZEN.json`.** The terms' § THE FREEZE, THE GUARD AND THE RUN, item 3, says M8.15.2's guard "never reads the instrument's own `FROZEN.json`". The approval of #630 records that the target path does: the driver takes `r_f`, `δ_lev` and `s₂` from it through the instrument's `frozen_numbers`. The pre-run check pinned that file to the SHA-256 M8.15.1's record gives it, and its values to `freeze_numbers.json`, and the post-run check found it unchanged. The same statement stands in `REGISTER_5.md`, in `validate_guard`'s docstring and in [the freeze block](../m8_15_2/freeze_block.md). The task document takes a dated note after the verdict.
- **`adjudicate.py`** prints one line per genuine step matched across levels, not "each bracket's adjudicated names" as its docstring and `REPRODUCE.md` say. For T2/R4 it prints nothing. No name rests on the wording.

## 6. Provenance

- **Terms:** `tasks/m8_15_2_task_details.md`, merged at OpenWave `1e8a6e2b`, SHA-256 `c6da782b43bc13d2…`.
- **Locator v2:** MIT [`851b2ad`](https://github.com/dmobius3/mode-identity-theory/tree/851b2ad82a562451defc036fe92b02d4cc666447/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2), with its manifest and `SHA256SUMS`, and its registration and qualification (`REGISTER_5.md`, `RESULT_5.md`).
- **Instrument:** MIT `97a8c08`, with its manifest unchanged.
- **Record:** MIT [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/f1ebda711a83dd175e03ae585e1426b261955aac/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15-2/RECORD.md). The target records, the run logs, the pre-run record, both guard files and the post-run checks are listed there with their SHA-256.
- **Reproduction:** the locator v2's `REPRODUCE.md`, and `RECORD.md` § 8.

## 7. What this run does not verify

- **That T3/R5's change of type is this crossing's.** The identification rests on the changed branch, which has synthetic controls only, and the full spectral crossing identity remains unresolved.
- **Which solution branch a step lies on.** The continuity check is a screen on one scalar.
- **That the two levels have the same type at one amplitude.** The matched-offset reading does not establish it (M8.15.1's terms, § THE CONFIRMATION), and the same-`ε` diagnostic is Unresolved at every offset up to 0.05.
- **A change of type on T2/R4,** anything outside the registered primary brackets, and anything about persistence.

## 8. Audit record

Two independent agents reviewed this note and the record against the frozen terms, the frozen locator v2 and the run's records, before filing. One checked every classification and the ceiling against the terms and the records, and compared both target records with M8.15.1's independently, finding no difference. The other reran `adjudicate.py` with its round-trip check and both record checks, recomputed the record's hashes and counts, and recomputed the two-level identity angle at this run's clean ends. Neither found a fatal problem. Their changes are folded in:
- the interpolated roots, named as estimates for the genuine-classed crossing pairs and set apart from the `n(L)` ends, which bracket where `n(L)` changes, here and in the record;
- § 5.1's reading of the result against the disclosure stated before the run.
