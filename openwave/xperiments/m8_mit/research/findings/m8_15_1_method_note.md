# M8.15.1 method note: locating the changes of type on T2/R4 and T3/R5

Task: [`tasks/m8_15_1_task_details.md`](../tasks/m8_15_1_task_details.md), governing SHA-256 `fc566c04…`, pre-registered in [#624](https://github.com/openwave-labs/openwave/pull/624), run on 2026-10-12 from the frozen locator at MIT `324fde3`, which reads the M8.15.x instrument at MIT `97a8c08`. The record is [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/c4e2f7f6d0af8a4a041817070f66004d1a69fc47/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/RECORD.md) beside the locator. Each primary bracket's index change is located, to the final intervals in § 4. The secondary's is not: its steps join two solutions (§ 5.2). No change of type is located. This note says why, against the frozen terms.

## 1. Equations first

`R = c = g = 1`, and vectors are in M8.15's real form, with `⟨a, b⟩_M = aᵀMb`. The law, the solver, the continuation and the linear verdict at a point are M8.15's and are inherited unchanged. This section states only what the locator adds.

### 1.1 The indices

`n(L)` counts the eigenvalues of `(L, M)` below `−tol_L`, with `tol_L = 10⁻⁹ max(1, |σ − λ₀,min|)`, by the frozen complete slice. `n(B|G_tol)` is the frozen cluster's count, and `h = n(L) − n(B|G_tol)` is the genuine index. A point balances when its slow Krein count `k_r + 2k_c + 2k_i⁻` equals `h`, as in M8.15.

### 1.2 The structural span

`P` is the top-`d` principal subspace, in the `M`-inner product, of the exact fibre generators' vectors (`iΦ`; in `R2` also `JΦ` and `iJΦ`) and the rotation vectors `X_aΦ`, each `M`-normalized. The phase partner `χ` is left out. `d` is frozen from the continuum: 3 for C2a, and 4 for C3, T2 and T3. The gate requires `σ_d/σ₁ ≥ 0.1` and, where a `(d+1)`-th value exists, `σ_{d+1}/σ₁ ≤ 0.05`.

### 1.3 The near-zero spectrum and the classes

- **The spectrum.** The `k_L` eigenpairs of `(L, M)` nearest `−10⁻⁶`, by shift-invert. `k_L = 16`, doubled to 32 and then 64 until `P`'s principal cosines with their span are all at least 0.9.
- **The classes.** An eigenvector is structural if its static `M`-overlap with `P` is at least 0.9, and genuine otherwise.
- **The structural subspace check.** Exactly `d` eigenvectors must be structural, and their span's principal cosines with `P` must all be at least 0.9. A point that fails it is Unresolved and cannot end a bisection.
- **`n_S`** counts the structural eigenvalues below `−tol_L`.
- **The slowest genuine pair** is the slowest pair of the slow spectrum outside the frozen cluster, the slow modes M8.15 sets aside. That classification is separate from the structural and genuine split of the eigenvectors of `L`. A point whose slowest genuine pair has a static overlap of 0.9 or more with `span{X_aΦ}` is Unresolved.

### 1.4 The steps

- **The grid and the bisection.** 8 grid sub-intervals; every sub-interval whose ends differ in `(n(L), n_S)` is bisected to `10⁻³` of its lower end.
- **The reading ends.** An end that does not balance moves outward to the first evaluated point that passes its checks, has the same counts and balances. The search stops at a point that fails its checks or changes counts, and the step is then Unresolved (no balanced reading end).
- **Between the reading ends:**
  - the crossing set, by the assignment problem on squared `M`-overlaps;
  - its identity, with principal cosines at least 0.9;
  - coverage: `Δn(L)` equals the signed number of crossing eigenvalues;
  - each crossing eigenvector's class, at both ends;
  - the bookkeeping: `Δn_S` equals the signed structural count, and `Δh` the signed genuine count.
- **The root** is the crossing eigenvalue's zero, interpolated between the reading ends.

### 1.5 The confirmation and the names

Genuine steps matched across levels are read at `r₃(1 ± d_j)` at level 3 and `r₂(1 ± d_j)` at level 2, for `d_j = 0.01, 0.02, 0.05, 0.10, 0.20`, by the frozen `decide(e₃, p₃, p₂, third=True)`. The guard region's end ladder points come last, read as the rerun ladder read them. A guard counts when each level's `h` there equals its step-end value on that side. The names, and the ceiling on positive results, are the terms' § NAMING.

## 2. Equation-to-code map

The links are pinned to MIT `324fde3` for the locator and `97a8c08` for the instrument.

| Equation | Code |
| --- | --- |
| `n(L)`, by the frozen complete slice | [`negative_index_L`](https://github.com/dmobius3/mode-identity-theory/blob/97a8c0884c5e3a0ed25afb345f3d668340c5b537/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x/m8_15x_solver/verdict.py#L115) |
| the verdict at a point, extracted from `run_branch` | [`decide`](https://github.com/dmobius3/mode-identity-theory/blob/97a8c0884c5e3a0ed25afb345f3d668340c5b537/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x/m8_15x_solver/m815_branch.py#L278), through [`decide_source`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L486) and [`bind_decide`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L501) |
| `P`, its dimension and its gap gate | [`structural_span`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L55) |
| the near-zero spectrum, coverage and the classes | [`near_zero_loop`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L135), [`near_zero_data`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L72) |
| the point checks: the gate, coverage, the structural subspace, the slowest pair | [`EvalPoint`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L85) |
| the fast-spectrum search, confined to full points | [`InstrumentEvaluator.evaluate`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L599) |
| the grid and the bisection | [`scan`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L276), [`bisect`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L247) |
| the reading ends, failing closed | [`reading_end`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L153) |
| the crossing set, identity, coverage, classes, bookkeeping and root | [`analyse_step`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L173) |
| matching across levels | [`match_levels`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L301) |
| the guards and the readings | [`offset_guard`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L321), [`region_end_guard`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L352), [`readings`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L365) |
| collisions, and the unbalanced points between the readings | [`collisions`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L375), [`unbalanced_between`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L388) |
| the names | [`name_step`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/locate.py#L402) |
| the guard on a target | [`validate_guard`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/t1_branch.py#L74) |

## 3. The run

- **Environment.** The driver records none of its own, and no environment check was recorded at the run. The instrument's manifest records the environment it was frozen in: Python 3.13.13, numpy 2.5.0, scipy 1.18.0, macOS 15.8 on arm64. The scripts pin one thread and fix the ARPACK starting vectors.
- **Before the run:** ten checks passed at 2026-10-12T02:53:20Z, among them the instrument's files and `freeze_numbers.json` against its manifest, both `SHA256SUMS`, the terms against the merged file, and the guard on the real instrument.
- **`FROZEN.json`** was written at 2026-10-12T02:53:20Z, before any target computation. It carries `freeze_numbers.json`'s values unchanged, the terms' SHA-256 and the go.
- **The targets:** T2/R4 from 2026-10-12T02:53:21Z to 2026-10-12T04:13:52Z, then T3/R5 to 2026-10-12T09:21:13Z. Both exited normally, with no crash record.
- **After the run:** the instrument's `SHA256SUMS` passes, `FROZEN.json` is unchanged, and every point record carries its own frozen record.
- **Deviations:** none. The orchestration lies outside the frozen set.

## 4. Results against the frozen terms

Both ladder reruns reproduce M8.15's ladder exactly. [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/c4e2f7f6d0af8a4a041817070f66004d1a69fc47/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/RECORD.md) gives every number.

| Bracket | Steps (final intervals) | The record's names | The adjudicated name (the maintainer's) |
| --- | --- | --- | --- |
| T2/R4, primary (16 to 22.6274) | level 3: Unresolved (structural subspace), 16.2589 to 16.3107<br>level 2: Unresolved (structural subspace), 16 to 16.8284 | no genuine crossing detected at level 3<br>an Unresolved step (structural subspace), at level 3<br>no genuine crossing detected at level 2<br>an Unresolved step (structural subspace), at level 2 | level 3: "no genuine crossing detected at level 3", with an Unresolved step (structural subspace), 16.2589 to 16.3107<br>level 2: "no genuine crossing detected at level 2", with an Unresolved step (structural subspace), 16 to 16.8284 |
| T3/R5, primary (11.3137 to 16) | level 3: structural, 13.1534 to 13.1626; root 13.1609; `Δn(L)`, `Δn_S`, `Δh` = -1, -1, 0<br>level 3: Unresolved (structural subspace), 15.7803 to 15.7986<br>level 2: Unresolved (structural subspace), 15.7071 to 16 | no genuine crossing detected at level 3<br>a structural step, at level 3<br>an Unresolved step (structural subspace), at level 3<br>no genuine crossing detected at level 2<br>an Unresolved step (structural subspace), at level 2 | level 3: "no genuine crossing detected at level 3", with a structural step, 13.1534 to 13.1626, root 13.1609, and an Unresolved step (structural subspace), 15.7803 to 15.7986<br>level 2: "no genuine crossing detected at level 2", with an Unresolved step (structural subspace), 15.7071 to 16 |
| T3/R5, secondary (22.6274 to 32) | level 3: Unresolved (no balanced reading end), 28.0276 to 28.0459; on the second solution path (§ 5.2)<br>level 3: Unresolved (no balanced reading end), 28.467 to 28.4853; its ends lie on different solutions (§ 5.2)<br>level 2: recorded genuine, 31.9817 to 32; recorded root 31.9934; `Δn(L)`, `Δn_S`, `Δh` = -1, 0, -1; its ends lie on different solutions, so it is neither an index change nor a root on one branch (§ 5.2) | no genuine crossing detected at level 3<br>an Unresolved step (no balanced reading end), at level 3<br>an Unresolved step (no balanced reading end), at level 3<br>an index crossing located; the change of type remains unresolved (cross-level disagreement) | level 3: "no genuine crossing detected at level 3", with two Unresolved steps (no balanced reading end)<br>level 2: **not located**: the step's two ends lie on different solutions (§ 5.2). The record's name is reported beside it |

- **No genuine step matched across levels in any bracket.** So no guard was read, and no change of type is located.
- **Each primary bracket holds a located index change that stayed unclassified** (structural subspace). "No genuine crossing detected at level 3" and "at level 2" are read in the terms' sense: no step qualified as genuine under the registered tests, which does not exclude a genuine crossing.
- **The secondary's level 2 is not named.** Its step joins two solutions (§ 5.2), so it is not an index change of `L` on a branch. Neither the record's name nor the terms' secondary label, "an index crossing located inside the Hyperbolic range", is given to it. The terms have no name for such a step: "not located" is the maintainer's description, not a frozen name. Where the code and the terms name the secondary differently, the terms govern; here the question is moot.
- **The ceiling has no positive result to restrict.** The fast-spectrum search did not run in either target run: every ladder point balanced, and no guard was evaluated.

## 5. Findings after the run

### 5.1 The primary crossings meet the structural subspace

- **The failing points.** At each primary unresolved candidate crossing, at both levels, the bisection's last midpoint, inside the final interval, fails the structural subspace check. It has two structural eigenvectors where four are required, and `n_S = 0` where both ends of the final interval have 2.
- **The consequence.** Such a point cannot end a bisection, so each step is Unresolved. The counts at the final interval's ends differ by `Δn(L) = ±2`, `Δn_S = 0` and `Δh = ±2`, matching the registered index arithmetic. The analysis stopped before it formed the crossing set, so the class of the crossing eigenvectors is the open question.
- **The slowest genuine pair at the failing points.**
  - **T3/R5:** it is the crossing mode, real and small at level 3 (`5.1×10⁻⁴`) and imaginary at level 2 (0.00471), with overlap 0.868 at level 3 and 0.892 at level 2. `n(B|G_tol)` falls there from 5 to 1 while the Krein count still balances, so the overlap may come from structural directions leaving the cluster, as well as from the crossing mode.
  - **T2/R4:** it is a different and much faster mode (imaginary, about 0.17), with overlap 0. At level 2's failing `ε`, level 3 reads 0.785. The record leaves open why.
- **A reading, not established here:** where the crossing eigenvalue of `L` passes zero, the crossing mode and two structural directions are close to degenerate, so the static classification does not separate them there.

### 5.2 The secondary's steps join two solutions

The maintainer's adjudication of #625 found this, and the records confirm it.

- **Two solution paths.** Below 27.31 the run records one solution path at each level. Above it, it evaluated points on two:
  - the ladder's path, on which one eigenvalue of `L` crosses zero between 27.31 and 28.485 at level 3, from −0.049 to +0.065. That crossing is the bracket's change of `n(L)` from 9 to 8;
  - a second path, on which that eigenvalue turns back.
- **How the run reached each.** The bracket's ends are the ladder's points. The grid chains point to point (`scan`), and the bisection reaches each midpoint by continuation from its current lower end (`bisect`), which is not always the point evaluated just before: 27.9727 at level 3 was reached from 27.8995, after 28.0459. At level 3 the bisection between 27.31 and 28.485 reached the second path from 27.90 up. At level 2 the grid reached it at 28.485 and stayed on it to 31.98.
- **The switch, read from the solution's `m`.** Along one path, the steps of 0.018 land within `6×10⁻⁷` of a linear prediction from the two points before them, and the step of that size just before each switch within `10⁻⁷`. Across level 2's step from 31.9817 to the ladder's point at 32, `m` misses by `1.9×10⁻²`, and across level 3's step from 28.467 to 28.4853 by `2.8×10⁻³`. The counts jump with it: at level 2, `n(L)`, `k_r` and `k_i⁻` go from 9, 2 and 1 to 8, 3 and 0.
- **What follows.**
  - Level 2's step is not a crossing along one solution. Its `Δn(L) = −1` is the difference between two solutions at nearly the same `ε`, and its root interpolates between them. Every one of its checks passed, because no registered check compares the solutions at a step's two ends.
  - Level 3's second step spans the same switch, and its first, 28.0276 to 28.0459, lies on the second path.
  - The secondary's index change on the ladder's branch is therefore not located by this run. It lies between 27.31 and 28.485 at level 3, and between 27.31 and 32 at level 2, and no evaluated point of that branch falls inside either interval.
  - The levels do not place one change far apart. Both show the same two paths, and the run switched between them at different `ε`.
- **The primaries lie on one path,** failing midpoints included: at every primary step of 0.026 or less, `m` lands within `4×10⁻⁷` of the same prediction.

### 5.3 A correction on the record

The terms' § Standing says no recorded point of the M8.15.x qualification ran the fast-spectrum search. One did: P5 in the qualification's `regress_verdict_before.json`, as the approval of #624 records. No rule, threshold or verdict rests on the sentence.

## 6. Provenance

- **Terms:** `tasks/m8_15_1_task_details.md`, merged at OpenWave `dcc63851`, SHA-256 `fc566c04…`.
- **Locator:** MIT `324fde3`. Its manifest pins 9 files and the extracted `decide`, and `SHA256SUMS` pins 83.
- **Instrument:** MIT `97a8c08`, with its manifest unchanged.
- **Record:** MIT [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/c4e2f7f6d0af8a4a041817070f66004d1a69fc47/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/RECORD.md). The target records, the run logs, the pre-run record and `FROZEN.json` are listed there with their SHA-256.
- **Reproduction:** the locator's `REPRODUCE.md`.

## 7. What this run does not verify

- **A change of type on either branch.** The primaries' index changes are located and stay unclassified, the secondary's is not located (§ 5.2), and no guard was read.
- **Whether a step's two ends lie on one solution.** No registered check compares them, and the secondary shows the gap (§ 5.2).
- **Whether the second path at the secondary bifurcates from the ladder's branch near 27.8.** The adjudication of #625 asks it.
- **Anything outside the registered brackets,** and anything about persistence.
- **The reading in § 5.1.** It is offered as an explanation of the failed checks, not as a result.

## 8. Audit record

Two independent agents reviewed this note and the record against the frozen terms, the frozen locator and the run's records, before filing. One checked every classification against the frozen terms and code. The other re-derived the point counts, every final interval and the points that do not balance from the frozen grid and bisection rules, found each of the code map's links on the function it names, and re-swept the JSON records for the correction in § 5.3. Neither found a fatal problem. Their changes are folded in:

- the custody of the seven records, and of the instrument's `SHA256SUMS` as it stood during the run, with the orchestration's hash;
- each Unresolved step's counts at its final ends;
- the slowest pair's eigenvalue beside its overlap, with the cluster count;
- wording that keeps an Unresolved step's crossing identity open;
- the record's names beside the adjudicated name, with the secondary's naming difference disclosed;
- the definitions in § 1, and the correction landing as a commit of its own after the record.

The maintainer's subsequent adjudication of #625 found the secondary's steps joining two solutions. § 4, § 5.2 and § 7 carry its result, § 5.1 its correction of the slowest pair at level 2, and § 3 no longer reports an environment check that the run did not record.
