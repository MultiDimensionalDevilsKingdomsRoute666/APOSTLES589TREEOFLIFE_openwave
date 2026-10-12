# M8.15.1 method note: locating the changes of type on T2/R4 and T3/R5

Task: [`tasks/m8_15_1_task_details.md`](../tasks/m8_15_1_task_details.md), governing SHA-256 `fc566c04…`, pre-registered in [#624](https://github.com/openwave-labs/openwave/pull/624), run on 2026-10-12 from the frozen locator at MIT `324fde3`, which reads the M8.15.x instrument at MIT `97a8c08`. The record is [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/c4e2f7f6d0af8a4a041817070f66004d1a69fc47/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/RECORD.md) beside the locator. Each bracket's index change is located, to the final intervals in § 4, and no change of type is. This note says why, against the frozen terms.

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

- **Environment.** The driver records none of its own. The run machine's Python, numpy, scipy and platform, checked after the run, equal the instrument manifest's: Python 3.13.13, numpy 2.5.0, scipy 1.18.0, macOS 15.8 on arm64. The scripts pin one thread and fix the ARPACK starting vectors.
- **Before the run:** ten checks passed at 2026-10-12T02:53:20Z, among them the instrument's files and `freeze_numbers.json` against its manifest, both `SHA256SUMS`, the terms against the merged file, and the guard on the real instrument.
- **`FROZEN.json`** was written at 2026-10-12T02:53:20Z, before any target computation. It carries `freeze_numbers.json`'s values unchanged, the terms' SHA-256 and the go.
- **The targets:** T2/R4 from 2026-10-12T02:53:21Z to 2026-10-12T04:13:52Z, then T3/R5 to 2026-10-12T09:21:13Z. Both exited normally, with no crash record.
- **After the run:** the instrument's `SHA256SUMS` passes, `FROZEN.json` is unchanged, and every point record carries its own frozen record.
- **Deviations:** none. The orchestration lies outside the frozen set.

## 4. Results against the frozen terms

Both ladder reruns reproduce M8.15's ladder exactly. [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/c4e2f7f6d0af8a4a041817070f66004d1a69fc47/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/RECORD.md) gives every number.

| Bracket | Steps (final intervals) | The record's names | The adjudicated name (the maintainer's) |
| --- | --- | --- | --- |
| T2/R4, primary (16 to 22.6274) | level 3: Unresolved (structural subspace), 16.2589 to 16.3107<br>level 2: Unresolved (structural subspace), 16 to 16.8284 | no genuine crossing detected at level 3<br>an Unresolved step (structural subspace), at level 3<br>no genuine crossing detected at level 2<br>an Unresolved step (structural subspace), at level 2 | for adjudication |
| T3/R5, primary (11.3137 to 16) | level 3: structural, 13.1534 to 13.1626; root 13.1609; `Δn(L)`, `Δn_S`, `Δh` = -1, -1, 0<br>level 3: Unresolved (structural subspace), 15.7803 to 15.7986<br>level 2: Unresolved (structural subspace), 15.7071 to 16 | no genuine crossing detected at level 3<br>a structural step, at level 3<br>an Unresolved step (structural subspace), at level 3<br>no genuine crossing detected at level 2<br>an Unresolved step (structural subspace), at level 2 | for adjudication |
| T3/R5, secondary (22.6274 to 32) | level 3: Unresolved (no balanced reading end), 28.0276 to 28.0459<br>level 3: Unresolved (no balanced reading end), 28.467 to 28.4853<br>level 2: genuine, 31.9817 to 32; root 31.9934; `Δn(L)`, `Δn_S`, `Δh` = -1, 0, -1 | no genuine crossing detected at level 3<br>an Unresolved step (no balanced reading end), at level 3<br>an Unresolved step (no balanced reading end), at level 3<br>an index crossing located; the change of type remains unresolved (cross-level disagreement) | for adjudication |

- **No genuine step matched across levels in any bracket.** So no guard was read, and no change of type is located.
- **Each primary bracket holds a located index change that stayed unclassified** (structural subspace). "No genuine crossing detected at level 3" and "at level 2" are read in the terms' sense: no step qualified as genuine under the registered tests, which does not exclude a genuine crossing.
- **A naming difference between the code and the terms, on which no verdict rests.** The terms name the secondary "an index crossing located inside the Hyperbolic range", with no type claim. The frozen code gives that label only to steps matched across levels; an unmatched genuine step gets the primary's wording, "an index crossing located; the change of type remains unresolved", whatever its label. The secondary's adjudicated wording is the maintainer's.
- **The ceiling has no positive result to restrict.** The fast-spectrum search did not run in either target run: every ladder point balanced, and no guard was evaluated.

## 5. Findings after the run

### 5.1 The primary crossings meet the structural subspace

- **The failing points.** At each primary unresolved candidate crossing, at both levels, the bisection's last midpoint, inside the final interval, fails the structural subspace check. It has two structural eigenvectors where four are required, and `n_S = 0` where both ends of the final interval have 2.
- **The consequence.** Such a point cannot end a bisection, so each step is Unresolved. The counts at the final interval's ends differ by `Δn(L) = ±2`, `Δn_S = 0` and `Δh = ±2`, matching the registered index arithmetic. The analysis stopped before it formed the crossing set, so the class of the crossing eigenvectors is the open question.
- **The slowest genuine pair at the failing points.**
  - **T3/R5:** it is the crossing mode, real and small (`5.1×10⁻⁴` at level 3), with overlap 0.868 at level 3 and 0.892 at level 2. `n(B|G_tol)` falls there from 5 to 1 while the Krein count still balances, so the overlap may come from structural directions leaving the cluster, as well as from the crossing mode.
  - **T2/R4:** it is a different and much faster mode (imaginary, about 0.17), with overlap 0. At level 2's failing `ε`, level 3 reads 0.785. The record leaves open why.
- **A reading, not established here:** where the crossing eigenvalue of `L` passes zero, the crossing mode and two structural directions are close to degenerate, so the static classification does not separate them there.

### 5.2 The secondary's levels disagree

- At level 3 the change comes in two steps near 28.03 and 28.47, inside a stretch where no evaluated point balances, and both are Unresolved (no balanced reading end).
- At level 2 it is one genuine step, at 31.98 to 32.0.
- The levels therefore disagree, and the secondary makes no type claim in any case.

### 5.3 A correction on the record

The terms' § Standing says no recorded point of the M8.15.x qualification ran the fast-spectrum search. One did: P5 in the qualification's `regress_verdict_before.json`, as the approval of #624 records. No rule, threshold or verdict rests on the sentence.

## 6. Provenance

- **Terms:** `tasks/m8_15_1_task_details.md`, merged at OpenWave `dcc63851`, SHA-256 `fc566c04…`.
- **Locator:** MIT `324fde3`. Its manifest pins 9 files and the extracted `decide`, and `SHA256SUMS` pins 83.
- **Instrument:** MIT `97a8c08`, with its manifest unchanged.
- **Record:** MIT [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/c4e2f7f6d0af8a4a041817070f66004d1a69fc47/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/RECORD.md). The target records, the run logs, the pre-run record and `FROZEN.json` are listed there with their SHA-256.
- **Reproduction:** the locator's `REPRODUCE.md`.

## 7. What this run does not verify

- **A change of type on either branch.** The index changes are located; none is classified, and no guard was read.
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
