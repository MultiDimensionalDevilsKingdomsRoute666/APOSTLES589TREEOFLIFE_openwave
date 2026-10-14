# M8.15.1: LOCATING THE CHANGES OF TYPE ON T2/R4 AND T3/R5, a pre-registered index-crossing locator with the full verdict read at guard offsets

Pre-registration, for review. It governs nothing until the maintainer's go. **No M8.15.1 target has been run.** T2/R4 and T3/R5 have been solved only in M8.15's run, and every record of that run is disclosed below. The revised instrument and the locator exist, and only their controls and tests have been run. The instrument's qualification reproduced every closing control ([`RESULT_3.md`](https://github.com/dmobius3/mode-identity-theory/blob/ae3ad04d551c078f089a6509acd35922ae01ffdf/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x/qualification/RESULT_3.md)); the candidate cluster rule did not qualify and is not part of it. The locator passes every registered test ([`RESULT_4.md`](https://github.com/dmobius3/mode-identity-theory/blob/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/RESULT_4.md)).

## TASK PLANNING

### The question

**What M8.15 left open.** M8.15 found T2/R4 and T3/R5 Elliptic at small amplitude and Hyperbolic at larger amplitude. The change of type was not located:
- every step from the last Elliptic ladder point to the first Hyperbolic one passes through an Unresolved point;
- so the frozen change-of-type bisection, which runs only between adjacent points of different decided type, never ran (M8.15's record, § 2).

**What this task asks:** on each of the two branches, where does the index change, and is it a change of type?
- **The candidate mechanism.** M8.15's bookkeeping suggests a genuine zero crossing: an imaginary pair passing through zero into a real pair, with one eigenvalue of the stationary Jacobian `L` changing sign per pair.
- **What is located.** Every index change of `L` that the registered grid and refinement detect inside the registered bracket, at both mesh levels, is localized and classified as genuine or structural.
- **What is not certified.** An interval without a detected change is not certified free of crossings. A grid cell can hold two crossings whose net change is zero, and only an interval certificate could exclude them. Nor is a step's reading interval certified free of a fast-spectrum quartet that forms and dissolves inside it (§ NAMING, the ceiling).
- **The confirmation.** The full Hamiltonian verdict is read at frozen guard offsets on each side of every genuine crossing.

**Two different claims.** A change in `L`'s negative index is observable numerical evidence. Identifying it with a particular mode, and with a change of type, takes the further checks below.

**Theorems.** Nothing about where a change of type happens is a theorem. The small-amplitude types are theorems (Theorem R), and they are not re-tested.

### Standing

- **The ruling it files under** is [#512](https://github.com/openwave-labs/openwave/discussions/512#discussioncomment-18415036)'s, as M8.15's was: a new program gets a new identity, filed as a BACKLOG row with its task doc in the pull request that carries the pre-registration. The law, and the solver's separation from the closed chassis, are M8.15's and are inherited below. Neither the instrument's revisions nor the locator use chassis code or input, or anything from `m8_5c/design_inputs/`.
- **Run-before-write** (`PR_REVIEW_STANDARDS.md` § 12.2) is met. M8.15 ran and was adjudicated on 2026-10-08 ([#620](https://github.com/openwave-labs/openwave/pull/620)). Since then the column has landed only the author's records after the verdict ([#621](https://github.com/openwave-labs/openwave/pull/621)).
- **Word budget.** About 6,200 words, inside § 12.2's cap of about 8,000.
- **ID.** M8.15.1 follows M8.15 as M8.1.1 and M8.1.2 followed M8.1. The row this pull request creates allocates it (`ROADMAP_STANDARDS.md` § 6). If a row taking M8.15.1 lands first, whoever merges second renumbers this one.
- **On MIT's side** this task is M8.15.x's Target 1, and the locator and its registration use that name.
- **Inherited.** Every rule of M8.15's terms (OpenWave `4b1177c8`) that this document does not change governs here. That covers:
  - the law, the solver and the continuation;
  - the ladder;
  - the linear verdict at a point: the cluster `G_tol` by the 0.9 rule, the Krein count, the fast-spectrum search, level stability and the cross-level check;
  - the numerical floors and frozen values: `r_f`, `τ₀`, `τ_Re`, `δ_lev`, `d₃` and `s₂`.
- **The instrument** is the M8.15.x solver at MIT `97a8c08`. It is M8.15's solver revised. The changes that matter here are these; its `REPRODUCE.md` lists the rest:
  - the stopping test repaired, with every multiplier included;
  - a record written on every end;
  - the gauge multipliers recorded;
  - the angle solve for slice cases, which is unused here.

  Its qualification on 2026-10-09 reproduced every closing control. Its manifest records each outcome.
- **A defect in the inherited fast-spectrum search, recorded and not repaired.**
  - **What it is.** The search tries 82 shifts. At its two real ones, `10⁻³` and `ω/40`, the frozen shift-invert operator builds a real factorization, and the search hands it to a complex eigensolver. The operator is then exact on real vectors and wrong on complex ones: the solve casts its right-hand side to real, while the second block, `y₁ + s z`, keeps `y₁`'s imaginary part, and the eigensolver passes complex vectors from its first step. So those two steps are not valid shift-invert steps.
  - **What it does not touch:** the other 80 shifts; the slow spectrum, which runs in real arithmetic; `n(L)` and the locator's near-zero spectrum, which use their own real symmetric solves; the controls' check, which uses imaginary shifts.
  - **What it can do.** Every eigenvalue the search keeps passes a backward-error test against the true matrices. That test does not prove the kept eigenvalues distinct and correctly classified, so the defect is not shown to act only by missing modes. If it does act only so, a miss leaves the count unbalanced and the point Unresolved, except inside a threshold window where the genuine index reads too low: there a miss can hide an instability. An exception from the eigensolver at either shift ends the branch with a crash record (§ THE FREEZE, THE GUARD AND THE RUN, 4).
  - **Where it has run.** In no record of the committed runs: every recorded point of M8.15's run and of the M8.15.x qualification shows the search unrun. On the bench it ran in one run only, the locator's first test run, at two C2a points inside a threshold window, before the search was confined (`REGISTER_4.md`, the amendment after R1). That run is archived and superseded, and it recorded no search result.
  - **Why it is not repaired.** A repair would change the verdict these terms inherit from M8.15's, and the repaired instrument would not be the one the qualification qualified. The instrument's `REPRODUCE.md` carries a dated note on it, every point records what the search did, and no positive result rests on the search (§ NAMING, the ceiling).
- **The verdict at a point** is the frozen driver's own function, `decide` in `m815_branch.py`.
  - The locator extracts it from the frozen file through its syntax tree.
  - It binds the function's free names exactly as `run_branch` binds them, with `sch` built from the full ladder, `ladder(0.25, EPS_MAX[slot])`, as `run_branch` builds it.
  - It records the SHA-256 of the extracted source.
- **What this task adds** is the locator. It is new code, kept in a folder of its own, and it reads the frozen instrument without changing it. It was qualified on controls and synthetic tests (`REGISTER_4.md`, `RESULT_4.md`) and frozen at MIT `324fde3` before any target ran.
- **The residual tolerance stays at `10⁻¹¹`.** A solve that cannot meet it is reported as a Newton failure with its residual history, never relaxed (§ THE LOCATOR, step 8).

### What this task is not

- There is no persistence test.
- There is no claim about any branch other than T2/R4 and T3/R5. Within those two, the claims are about the registered brackets only.
- T1 and T4 stay blocked:
  - the candidate cluster rule of the memo's § 2 did not qualify;
  - the paired-lift floor (the memo's 2b) is open.
- There is no slot relation, and M8.15's row 6 ceiling carries over.
- No `MODELS.md` cell moves, and M8.7's gate is unchanged.

### Ownership and run format

- **The author's agents build and run** the locator under the frozen terms, and publish the scripts, data and records with a reproduction route (the locator's `REPRODUCE.md`).
- **The frozen terms' SHA-256 lands on MIT `main` before the run starts** (§ THE FREEZE, THE GUARD AND THE RUN).
- **No obligation on the maintainers.** Reproduction is optional and declinable per run. A claim of a defect in the frozen text is reproduced by the maintainer with independent code before it is ratified, as M8.15's terms provide.
- **Adjudication** is the maintainer's, under § NAMING with its ceiling.

### Sources of record

| Source | What it supplies |
| --- | --- |
| [M8.15's task document](https://github.com/openwave-labs/openwave/blob/4b1177c8fb02e393bb418029cefe29fb98c8eb21/openwave/xperiments/m8_mit/research/tasks/m8_15_task_details.md) at `4b1177c8` | the inherited terms: the law, the solver, the continuation, the ladder, the linear verdict at a point, the numerical floors and the frozen values |
| MIT [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/28c8a7648a88c9234d32be753cbbe3563ea2eec3/files/framework/files/working/files/scripts/soft-slot-dynamics/RECORD.md) at `28c8a76` | M8.15's run record: the per-branch record (§ 2), whose committed branch records give the brackets and the disclosures below |
| MIT [`soft-slot-branches.md`](https://github.com/dmobius3/mode-identity-theory/blob/d0de8ca61f8e166586731b6167ab895c09368630/files/framework/files/working/files/soft-slot-branches.md) at `d0de8ca` | the targets, and their small-amplitude types (Theorem R), as M8.15 cites them |
| MIT [`soft-slot-dynamics-m8-15x/`](https://github.com/dmobius3/mode-identity-theory/tree/97a8c0884c5e3a0ed25afb345f3d668340c5b537/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x) at `97a8c08` | the instrument: the M8.15.x solver, its manifest and its `REPRODUCE.md` |
| the same folder at [`ae3ad04`](https://github.com/dmobius3/mode-identity-theory/tree/ae3ad04d551c078f089a6509acd35922ae01ffdf/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x) | the instrument's dated note (the guard file's exclusion and the fast-spectrum defect), and the qualification's record in `qualification/`, with the scope memo `M8_15x_instrument_memo_v4.md` ("the memo") |
| MIT [`soft-slot-dynamics-m8-15x-target1/`](https://github.com/dmobius3/mode-identity-theory/tree/324fde3eda26924f028f4b6850d2e5efa80ae6fa/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1) at `324fde3` | the locator: its code and manifest, its registration `REGISTER_4.md`, its tests' results `RESULT_4.md`, the span checks `span_gate_continuum.out` and `span_rank_controls.out`, and the tests' records |
| This task | the brackets, the locator's rules, the guard reading, the naming and the frozen values below |

## DISCLOSURE (the memo's rule 4)

The terms state everything this follow-up has already seen. No rule below is justified by any of it.

- **Every M8.15 target record,** among them:
  - T1's 4.99% and 5.3%;
  - T4's end at the seed, with its post-run diagnostics;
  - the level-2 bench check at T4's slice-constrained point.
- **T2/R4 near its change, read for this draft from M8.15's committed branch record.** At each ladder point, level 3 then level 2: `n(L)`, `n(B|G_tol)`, and the slowest genuine pair. The pair is doubled throughout.

  | `ε` | level 3 | level 2 |
  |---|---|---|
  | 11.31 | 5, 5; imaginary at `2.07×10⁻²` | 5, 5; imaginary at `2.11×10⁻²` |
  | 16 | 5, 5; imaginary at `6.60×10⁻³` | 5, 5; imaginary at `8.27×10⁻³` |
  | 22.63 | 7, 5; real at `4.03×10⁻²` | 7, 5; real at `3.97×10⁻²` |
  | 32 | 7, 5; real at `8.05×10⁻²` | 7, 5; real at `8.01×10⁻²` |

  The types are Elliptic to 11.31, Unresolved at 16 and 22.63 (cross-level disagreement; at 22.63, level stability too), and Hyperbolic from 32.
- **T3/R5 near its changes, read the same way.**

  | `ε` | level 3 | level 2 |
  |---|---|---|
  | 11.31 | 12, 6; three Krein-negative imaginary pairs, the slowest doubled at `3.74×10⁻²` | 11, 5; the same, at `3.76×10⁻²` |
  | 16 | 9, 5; a doubled real pair at `1.01×10⁻²`, and a Krein-negative pair at `8.36×10⁻²` | 9, 5; real at `9.54×10⁻³`, imaginary at `8.39×10⁻²` |
  | 22.63 | 9, 5; two real pairs, one Krein-negative pair at `6.96×10⁻²` | 9, 5; the same, at `7.01×10⁻²` |
  | 32 | 8, 5; three real pairs | 8, 5; three real pairs |

  The types are Elliptic to 11.31, Unresolved at 16 (cross-level disagreement and level stability), and Hyperbolic at 22.63 and 32.
- **An independent review's continuum figures,** from public spectra:
  - T2's slowest pair, the one that crosses zero, has a static overlap with the rotations of 0.64 at small amplitude;
  - T3's genuine slow modes have none.
- **The residual margins on M8.15's committed records** (the M8.15.x qualification's results):
  - T2/R4 at level 3, `ε = 16`: `8.04×10⁻¹²`;
  - T3/R5 at level 2, `ε = 8`: `7.97×10⁻¹²`;
  - T2/R5 at level 2, `ε = 22.63`: `8.99×10⁻¹²`;
  - T5/R2 at level 3, `ε = 5.66`: `9.72×10⁻¹²`.

  A control, C2b/R2 at level 2, `ε = 11.31`, reaches `9.22×10⁻¹²`.
- **Where these values enter.** They were read while drafting. Only the brackets come from them, by the memo's rule, and those are unscored.
  - The bisection width, the guard offsets, the near-zero count and the span's gap gate are set below from the frozen tolerances, the continuum and the controls.
  - The guard reading is set from the square-root law near a simple crossing.

## THE BRANCHES, THE BRACKETS AND THE GUARD REGIONS

The brackets are where M8.15's level-3 `n(L)` changes between adjacent ladder points. The guard region on each side runs to the nearest ladder point whose type M8.15 decided.

| Branch | Bracket in `ε` | `n(L)` across it, level 3 (level 2) | Guard region | Label |
|---|---|---|---|---|
| T2/R4 | 16 to 22.63 | 5 to 7 (5 to 7) | 11.31 to 32 | primary |
| T3/R5 | 11.31 to 16 | 12 to 9 (11 to 9) | 11.31 to 22.63 | primary |
| T3/R5 | 22.63 to 32 | 9 to 8 (9 to 8) | 22.63 to 32 | secondary |

**The index arithmetic.** Across each bracket, `Δn(L)` and `Δn(B|G_tol)` imply these genuine changes:
- T2/R4: +2;
- T3/R5 primary: −2 at both levels. At level 3 that comes with one structural step;
- the secondary: −1.

**The secondary result.** It is an index change inside the Hyperbolic range: the genuine index falls from 4 to 3, with `k_i⁻` falling from 1 to 0 and `k_r` rising from 2 to 3.
- It is located the same way.
- It carries no claim of a change of type or of persistence, and it cannot affect how the primary results are scored.
- The memo's stronger statement, that one tracked block makes the transition, needs the block tracking of the memo's § 2. That tracking did not qualify, so the stronger statement is not available: the secondary reports the location and the bookkeeping only.

## THE LOCATOR

It runs on each branch and each bracket, at levels 3 and 2 independently.

1. **The ladder.** The branch is rerun from `ε_min` under the frozen continuation, at both levels, up to the guard region's upper end, with the frozen verdict at every ladder point.
   - This repeats M8.15's ladder with the qualified instrument.
   - Any difference from M8.15's record in a type, `n(L)` or `n(B|G_tol)` is reported. It changes no rule.
2. **The point data.** These are computed at every evaluated point: the guard region's ladder points, grid points, bisection midpoints and guard points.
   - **The frozen point data:** the cluster, the slow spectrum with Krein signs, `n(L)`, `n(B|G_tol)` and the counts.
   - **The fast-spectrum search.**
     - It can run only where the full frozen point is built (on the rerun ladder, at the offset guards, and for the same-`ε` diagnostic). Even there, it runs only when that point's slow count does not balance.
     - At grid points, bisection midpoints and the locator's re-evaluations of the guard region's ladder points, only counts are read, and it is skipped.
     - Each point records it as not needed (the slow count balances), skipped, or run, and where it ran, what it found.
     - Its two real shifts carry a defect (§ Standing).
   - **The locator's structural span `P`.**
     - It is built from the exact fibre generators' vectors (`iΦ`; in R2 also `JΦ` and `iJΦ`) and the rotation vectors `X_aΦ`, each `M`-normalized.
     - It leaves out the phase partner `χ = (2ω/c²) dΦ/dσ`. `χ` is not a near-zero direction of `L`, since `Lχ ∝ MΦ`.
     - `P` is specific to the locator. It is not the cluster rule's span `U`, which includes `χ`.
     - **Its dimension `d` is frozen per case from the continuum:** the rank of the phase and rotation generators at the representative. It is 4 for T2 and T3.
     - **`P` is the top-`d` principal subspace** of those vectors, in the `M`-inner product.
     - **The gate.** The discrete span must show a clear gap: `σ_d/σ₁ ≥ 0.1` and, where a `(d+1)`-th value exists, `σ_{d+1}/σ₁ ≤ 0.05`. Otherwise the point is Unresolved (structural span). The gate is an operational check, not a theorem about the classification.
     - **Its expected values.** The statistic depends on the frame, so each case's continuum value is registered in its frozen frame, the orientation in the instrument's `out/orientations.json`. They are the same at both levels (`span_gate_continuum.out`, continuum only, no solve):
       - `σ_d/σ₁`: 0.3587 for C2a (with `σ₄ = 0`), 1.0 for C3, 0.966 for T2/R4 and 0.408 for T3/R5;
       - over random frames, the continuum minimum is 0.315, 1.00, 0.964 and 0.382, so the gate keeps a margin of at least 3 in every frame.
     - **Why `d` is frozen.** On the mesh, the generators of a span that is degenerate in the continuum are not exactly dependent.
       - At C2a's coherent state `X_zΦ` lies along `iΦ` in the continuum. At level 2 it leaves a residual of `7×10⁻³` of the largest singular value (a control measurement, `span_rank_controls.out`). A rank read at a small threshold would count that residual.
       - C2a's third value, 0.3588 at level 2, is its frozen frame's continuum value, 0.3587, not a mesh effect.
   - **The near-zero spectrum.** The `k_L` eigenpairs of `(L, M)` nearest the shift `−10⁻⁶`, by shift-invert, starting at `k_L = 16`.
     - Each eigenvalue is classed as negative if it lies below `−tol_L`, the frozen threshold `n(L)` uses, and as nonnegative otherwise. So a crossing and a change in `n(L)` are read by the same rule.
   - **Coverage.**
     - The `d` principal cosines between `P` and the span of the `k_L` eigenvectors must all be at least 0.9.
     - If they are not, `k_L` doubles to 32, then to 64.
     - If 64 still fails, the point is Unresolved (spectral coverage). No missing eigenpair is assumed absent.
   - **The structural subspace.** Each eigenvector's static `M`-overlap with `P` is computed and recorded; structural at 0.9 or more, genuine otherwise.
     - Exactly `d` eigenvectors must be structural.
     - Their span's `d` principal cosines with `P` must all be at least 0.9.
     - Otherwise the point is Unresolved (structural subspace), and it cannot end a bisection.
   - **`n_S`** is the number of structural eigenvalues classed negative.
   - **The slowest genuine pair's static overlap** with `span{X_aΦ}` is recorded (the memo's § 2, fallback). At 0.9 or more the point is Unresolved.
3. **The grid.** The bracket is split into 8 equal sub-intervals, and the 7 interior points are evaluated in increasing order, each reached from the previous point by the frozen secant (`Branch.goto`).
4. **The bisection.** Every sub-interval whose ends differ in `n(L)` or `n_S` is bisected until its width is at most `10⁻³` of its lower end.
   - A midpoint whose counts match neither end splits the sub-interval in two, and both halves are bisected.
   - Each midpoint is reached from the current lower end by the frozen secant, as M8.15's bisection reaches it.
   - A root that falls on an evaluated point is classed by the same rule as every eigenvalue. So it is located once, on its negative side, and never twice.
5. **The steps.** A step is a final interval `[lo, hi]`.
   - **Its reading ends.**
     - The instrument reads `n(L)` and `n(B|G_tol)` against different thresholds. So a slowly crossing structural eigenvalue can leave points where the slow Krein count does not balance. C2a at level 3 does, between `ε ≈ 33.93` and 34.0.
     - An end that does not balance therefore moves outward, point by evaluated point. The move stops at the first point that fails its checks or whose `(n(L), n_S)` differs, and takes the first point that passes its checks, has the same counts and balances.
     - **With none, the step is Unresolved (no balanced reading end).** It is never classified from an unbalanced end.
     - **A genuine crossing can leave such a window too.** It lies where the crossing eigenvalue of `L` is between `−tol_L` and 0, or where its Hamiltonian pair is real but below `τ_Re` in modulus, so that `n(L)` and the Krein count fall on opposite sides of the crossing. A Krein-negative imaginary pair counts at any size. On a target step, a reading end that moves across such a window is therefore an expected outcome, not a new finding.
     - Everything below is read between the reading ends. The final interval is reported with them.
   - **Its crossing set.** The near-zero eigenvectors at `lo` and `hi` are matched by the assignment problem on their squared `M`-overlaps. Those whose eigenvalues change class form the crossing set.
   - **The crossing identity.** The crossing set's span at `lo` and its span at `hi` must have all principal cosines at least 0.9. Otherwise the step is Unresolved (crossing identity). So a doubled crossing whose computed basis rotates inside its eigenspace is matched as a subspace, and is neither lost nor split.
   - **Spectral coverage.**
     - `Δn(L)`, from the complete slice, must equal the signed number of crossing eigenvalues found.
     - If it does not, `k_L` is enlarged as in step 2.
     - If the mismatch survives, the step is Unresolved (spectral coverage).
   - **Each crossing eigenvector is classified by its overlap with `P` at both ends:**
     - structural if at least 0.9 at both;
     - genuine if below 0.9 at both;
     - otherwise the step is Unresolved (mixed overlap). Given the structural subspace and crossing identity checks, this rule cannot fire (DERIVED, `REGISTER_4.md`'s amendment of S8); it stays as a backstop.
   - **The bookkeeping.** Each of these must equal the signed count it is read against:
     - `Δn_S` must equal the signed number of structural crossings;
     - `Δ(n(L) − n(B|G_tol))` must equal the signed number of genuine ones.

     If either does not, the step is Unresolved (index bookkeeping).
   - **A genuine step** has only genuine crossing eigenvectors, with every check passing. **A structural step** has only structural ones. A step holding both is Unresolved (genuine and structural crossings in one step).
6. **The root and the cross-level shift.**
   - **Each step's root** is its crossing eigenvalue's zero, interpolated linearly between the reading ends: the mean over the crossing set's eigenvalues, kept inside the reading interval.
     - **Three quantities are named separately:**
       - the final interval, where the count changes;
       - the reading interval, between the reading ends;
       - the root, an estimate read from the reading interval.
     - **What the record carries.** Each crossing's unclamped zero, whether the clamp applied, and the final interval's midpoint.
     - **The root has no `10⁻³` guarantee of position.** It can lie outside the final interval, by up to about `tol_L/|slope|`, because `n(L)` counts below `−tol_L`, not below zero. C2a at level 3: final interval 33.916 to 33.942, root 34.042.
     - **Why not the midpoint.** A midpoint is off by up to half the width, `5×10⁻⁴` relative. At a 1% matched offset that moves the crossing pair by up to 2.5%, against level stability's 1% (found on the mock, before any recorded test).
   - **Matching across levels.** Genuine steps are matched between the two levels by their order within the bracket and their signed counts. Unequal numbers of genuine steps at the two levels are a cross-level disagreement.
   - **The cross-level shift** `δ = (root⁽²⁾ − root⁽³⁾)/root⁽³⁾` is reported once, as a cross-level shift, not as a discretization error, since the memo's § 3 is deferred.
7. **Collisions.** A genuine quartet (`k_c > 0`) at any evaluated point between a step's two readings, at either level, is recorded as a collision. A collision prevents the static crossing alone from being identified with the change of type.
   - **Every unbalanced evaluated point between the readings is listed beside the collisions.** The collision check reads the slow `k_c`, so these are the only places a fast-spectrum quartet could sit. The ceiling in § NAMING reads them.
8. **Newton failures.**
   - A solve that fails at an evaluated point, after the frozen retries, ends that bisection.
   - The step is reported over the bracket reached, as Unresolved (Newton failure), with the failed solve's residual at every Newton iteration.
   - **Why a solve may fail.** Near the root of a crossing whose mode lies in the pinned fixed space, Newton's bordered Jacobian is nearly singular.
     - The doubled crossings at T2 and T3 are expected to lie outside that space, since a doubled mode of the pinned `D₃` carries its two-dimensional representation (INFERRED).
     - The secondary's single crossing may lie inside it.

## THE CONFIRMATION: THE FULL VERDICT AT GUARD OFFSETS

**Where, per genuine step matched across levels.** Each level is read at its own root's offset: level 3 at `r₃(1 ± d_j)` and level 2 at `r₂(1 ± d_j)`, for `d_j = 0.01, 0.02, 0.05, 0.10, 0.20` in that order.
- Both points of a guard must lie inside the guard region.
- **The region's end ladder points come last.** Each reads as the rerun ladder's own verdict at that point, with the ladder's `third`, and is named as a region-end reading. So a region end reads exactly as the ladder read it when M8.15 decided it.
- Every guard is evaluated, so that a disagreement between decided guards on one side is always seen.

**What is read.** At each offset guard, the pair goes to the frozen verdict, `decide(e, p3, p2, third=True)`, with the level-3 guard's `ε` as `e`. This is how M8.15's bisection read a midpoint, with the cross-level check always applied.

**When a guard is decided,** region ends included: only if the verdict is Elliptic or Hyperbolic and both of its points pass the locator's own checks (§ THE LOCATOR, step 2). A point that fails any of them is Unresolved, whatever the verdict.

**Why each level is read at its own offset.** Near a simple zero crossing the pair follows `λ² ≈ c(ε − r)`: imaginary below the root and real above it.
- **At one `ε`.** Two levels whose roots differ by `δ` give crossing eigenvalues that differ by about `δ/(2d)` of their size at an offset `d`. The cross-level check allows 1%, and level stability allows 1%, so a same-`ε` reading would fail both for every `d` below about `50δ`.
- **At matched offsets.** The checks judge each level's slope `c` instead, which is what they were built to compare.
- **The cost.** At matched offsets the two levels sit at `ε` values about `δ` apart. So every other slow mode differs between levels by about `δ` times its logarithmic slope in `ε`, which is about 1 for modes scaling like `ε`. The frozen 1% then bounds the confirmation to roughly: `|δ|` plus the modes' own level difference at one `ε`, at most about 1%. Beyond that, the readings are expected to be Unresolved, and the result is named accordingly.
- **The same-`ε` reading** is recorded beside each guard as a diagnostic. It is never a reading.
- **What the matched reading establishes.** It is a new cross-level comparison, not M8.15's same-amplitude check. It can support a finite-mesh confirmation of a change of type. It does not establish that the two levels have the same type at one identical amplitude.
- **Its standing under the memo's rule 2.** This reading is new. It rests on the square-root law and the frozen tolerances, not on any record. No non-target control holds a genuine crossing, so it is tested on the mock evaluator only (`REGISTER_4.md`). The review is asked to accept that explicitly.

**Which readings count.** A guard counts only if each level's genuine index there, `n(L) − n(B|G_tol)`, equals that level's step-end value on that side. So the readings bracket this crossing and no other. A structural step, such as T3/R5's at level 3, does not disqualify a guard.

**The reading on a side** is the verdict at its nearest counting guard that is decided, Elliptic or Hyperbolic.
- A side with no such guard has no reading.
- If two counting decided guards on one side disagree, the side is mixed.
- At every guard point, the slowest genuine pair's overlap, every crossing eigenvector's overlap and any collision are recorded.

**Why these offsets.** The smallest is ten times the bisection width. The largest is about half the ladder's relative spacing of `√2`. They are not fitted to any record.

## NAMING

**For each genuine step:**
- **A located change of type**, if all of these hold:
  - the readings are Elliptic on one side and Hyperbolic on the other;
  - no side is mixed;
  - no collision lies between the readings;
  - the step's checks hold at both levels.
- **The report then gives two separate things:**
  - the location of the index crossing: both roots, with their final intervals and the cross-level shift;
  - the interval over which the types are confirmed: each reading's offset, and its `ε` at each level.

  The type change is confirmed between the readings. Their evidence does not place it at the root's midpoint.
- **When a reading comes from a region's end ladder point,** the name says so. The confirmation is then no finer than M8.15's ladder.
- **Otherwise:** "an index crossing located; the change of type remains unresolved", with the reason.

**The ceiling: no positive result rests on the fast-spectrum search.** It is applied in adjudication, from the record; the record's own names do not apply it. A step otherwise named a located change of type is named "an index crossing located; the change of type remains unresolved", with the reason "fast-spectrum dependence, pending independent verification", if either of these holds at either level:
1. **A reading has an unbalanced point.** An offset guard or a region end whose level-3 or level-2 point does not balance may owe its verdict to the search. An offset guard's two points are in its guard record. A region end's are the rerun ladder's own full points at that `ε`, at both levels.
2. **An unbalanced point lies between the readings, outside the reading interval of every genuine or structural step at its level.** A fast-spectrum quartet, which the collision check cannot see, could sit there. Every evaluated point at that level is read, undecided guards and the same-`ε` diagnostic's points included.

- **The exemption is an accepted limitation, not a proof.** It does not show that every unbalanced point inside a reading interval comes from that step's own window. It rests on two facts:
  - every evaluated point in a step's own threshold window (§ THE LOCATOR, step 5) ends inside its reading interval: the bisection's ends only close in, and each reading end moves out past the unbalanced points to the first balanced one;
  - both reading ends balance, and every term of the Krein count is nonnegative, so the fast spectrum contributes nothing at either end.
- **Why it is needed.** Without it, a structural step between a genuine step's readings, which § Which readings count allows, would likely put the genuine step under the ceiling. The genuine step's own window could too, if an evaluated point lands in it.
- **Why only classified steps.** An Unresolved step's reading interval was never shown to hold only a window, so it is not exempt.
- **What it leaves open.** A fast-spectrum quartet that forms and dissolves inside a genuine or structural step's reading interval is not excluded. It can change neither reading. It bears only on whether the change of type is identified with the static crossing in that interval.
- **The result is the adjudicated name.** The published result carries it, with the record's automatic name reported beside it.
- **Verification** lies outside this run. A later dated note may report it; the record and the adjudication stand as made.

**Structural steps** are reported as such, and are never a change of type.

**A bracket with no genuine step detected at a level:** "no genuine crossing detected at level `h`".

**The secondary result** is named under its own label: "an index crossing located inside the Hyperbolic range". Its readings and bookkeeping are reported, and no type claim is made.

**A genuine step inside a structural window.** T3/R5's level-3 bracket holds a structural step. If a genuine step's end lies inside that step's threshold window, the genuine step reads Unresolved (index bookkeeping, or no balanced reading end), and that result stands.

## REPORTED

- **The rerun ladder,** with its types and any difference from M8.15's record.
- **At every evaluated point:**
  - the frozen point data;
  - the near-zero spectrum of `L`, with each eigenvector's overlap with `P`;
  - `k_L`, the coverage cosines, `n(L)`, `n_S`, `n(B|G_tol)` and the structural subspace's cosines;
  - the slowest genuine pair's overlap;
  - the Newton residual.
- **Each step:** its final interval, its reading interval, its crossing set with classes and overlaps, its checks, and its root at each level, with each crossing's unclamped zero and the clamp flag.
- **Each point's fast-spectrum state,** with what the search found wherever it ran, and the unbalanced points between each step's readings.
- **An Unresolved step's `root` field** is its final interval's midpoint, used for ordering only. It is not a root.
- **The cross-level shifts,** and every guard's two points and verdict with its reasons, together with the same-`ε` diagnostic.
- **The collisions and the names.**
- **Every Newton failure,** with its residual history.
- **The SHA-256 of the extracted `decide` source.**

## THE TESTS, BEFORE ANY TARGET (`REGISTER_4.md`)

**Each test's expected outcome is registered before the locator is coded.**
- **Synthetic tests on a mock evaluator,** each with a mutation arm. The mock plants spectra, not verdicts, and the frozen `decide` reads them. Among the cases:
  - a 0.5% cross-level shift, unresolved under the same-`ε` reading and located under matched offsets;
  - a 2% shift, which reaches the matched reading's registered limit;
  - roots on and off grid points;
  - spectral coverage;
  - a doubled crossing whose computed basis rotates inside its eigenspace;
  - which readings count, with region ends read as the ladder read them.
- **C2a/R4, a structural crossing (a non-target).** Its level-3 `n(L)` and `n(B|G_tol)` fall from 2 to 0 together between 32 and 45.25, and its level-2 ones between 11.31 and 16 (the controls' committed records). The locator must locate a structural step there at each level, and no genuine step.
- **C3/R4, no crossing (a non-target):** over 11.31 to 16, no step at either level.
- **A forced Newton failure** on C2a. It must be recorded as Unresolved (Newton failure), with its residual history.
- **The verdict:**
  - the extracted `decide` reproduces the qualification's C3/R4 and C2a/R4 ladder types and reasons exactly;
  - each of its nine Unresolved reasons is triggered on constructed point pairs.
- **The guard's validation.** A target is refused without `FROZEN.json`, with frozen numbers that differ from the instrument's `freeze_numbers.json`, or with a terms hash that differs from the terms'.

**A failed test stops the run** before any target is evaluated.

## FROZEN VALUES

- **From M8.15's freeze:**
  - `r_f⁽³⁾ = 1.040×10⁻⁶` and `r_f⁽²⁾ = 3.970×10⁻⁵`, so `τ₀ = τ_Re = 10 r_f`;
  - `δ_lev = 10⁻²`;
  - `s₂ = 6.739×10⁻⁴` (R4) and `9.547×10⁻⁴` (R5);
  - the ladder; the residual tolerance `10⁻¹¹`.
- **New:**
  - `k_L = 16`, enlarged to 32 and then 64, with the shift `−10⁻⁶`;
  - the overlap, coverage and subspace thresholds 0.9, inherited from the cluster rule;
  - the span's dimension `d` per case (3 for C2a; 4 for C3, T2 and T3) and its gap gate, 0.1 and 0.05;
  - 8 grid sub-intervals;
  - a bisection width of `10⁻³` relative;
  - the guard offsets `d_j`, read at each level's own root;
  - the brackets and the guard regions above.

## THE FREEZE, THE GUARD AND THE RUN

1. **The locator was built and qualified** (`REGISTER_4.md`), then frozen in a folder of its own at MIT `324fde3`, with its own manifest and `SHA256SUMS`. It reads the instrument at `97a8c08` unchanged.
2. **The terms' SHA-256 lands on MIT main.** The freeze block, [`m8_15_1/freeze_block.md`](../m8_15_1/freeze_block.md), records it with the locator's and the instrument's commits and manifests.
3. **The guard file is written** in the instrument's `out/` (`FROZEN.json`), as M8.15's was.
   - It carries the values of the instrument's `out/freeze_numbers.json` unchanged, which the frozen driver reads for a target, together with the terms' SHA-256 and the go.
   - The instrument's freeze check was first amended to exclude that file, at MIT `ae3ad04`. A dated note in the instrument's `REPRODUCE.md` records the amendment and the fast-spectrum defect (§ Standing). The check, `REPRODUCE.md` and `SHA256SUMS` changed, and the qualification's record was added beside them; the instrument's files and its `MANIFEST.json`, which every locator record cites, did not.
   - Before any target runs, the locator checks that every value equals `freeze_numbers.json`'s, that the terms hash matches, and that the go is present. It refuses a target otherwise.
4. **The run.** T2/R4, then T3/R5. Each writes a record on every end, and a crash record on an instrument exception.

**Resources.** A level-3 phase peaks near 6.4 GB resident, so one branch runs at a time. The estimate is about 3 to 6 hours per branch, more wherever the fast-spectrum search is needed.

## DEFINITION OF DONE

- **The record:** both branches' locator records, the tests' records, and the freeze. They are published with the scripts and a reproduction route.
- **Adjudication** is the maintainer's, under the naming above.
- **What does not move:** no M8.15 record is reread, and no type outside the registered brackets is claimed.

## Dated note, 2026-10-12: after the verdict

Everything above this heading is the filed pre-registration, byte for byte: its 39,375 bytes are a prefix of this file and hash to the governing `fc566c04…`.

The maintainer adjudicated the run on [#625](https://github.com/openwave-labs/openwave/pull/625#pullrequestreview-5492753760), and the roadmap's Done row states that verdict. No change of type is located. Each primary holds an index change that stays unclassified. The secondary's steps join two solution paths, so its index change is not located. The author's dated notes record it on MIT, at the foot of the run's [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/b13e0f4bd1d3763215046b9c6ab1c9b87f94a379/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-15x-target1/RECORD.md) and in [The Soft-Slot Branches, § VI](https://github.com/dmobius3/mode-identity-theory/blob/b13e0f4bd1d3763215046b9c6ab1c9b87f94a379/files/framework/files/working/files/soft-slot-branches.md#vi-what-stays-open).

**A correction to § Standing.** Its "Where it has run" says that every recorded point of the M8.15.x qualification shows the fast-spectrum search unrun. One does not: P5 in the qualification's `regress_verdict_before.json`, as the approval of [#624](https://github.com/openwave-labs/openwave/pull/624#pullrequestreview-5485856574) records. No rule, threshold or verdict rests on the sentence.
