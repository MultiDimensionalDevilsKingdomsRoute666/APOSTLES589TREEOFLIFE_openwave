# M8.16.1 method note: the second and last qualification of the stationary harmonic Galerkin instrument

Task: [`tasks/m8_16_1_task_details.md`](../tasks/m8_16_1_task_details.md), governing SHA-256 `9d16712982e53889…`, pre-registered in [#650](https://github.com/openwave-labs/openwave/pull/650), run on 2026-10-25 from the instrument frozen at MIT `d1c0ec8`, under the maintainer's [go](https://github.com/openwave-labs/openwave/pull/650#issuecomment-6385959498) and the [freeze block](../m8_16_1/freeze_block.md) of [#652](https://github.com/openwave-labs/openwave/pull/652). The record is [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/292b158cf1a53902489ced3426e1f047699aeb62/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/RECORD.md) beside the instrument. The verdict, as the driver wrote it, is QUALIFIED: the instrument qualifies, and so do the nine rows, T1 to T4 in `R4` and `R5` and T5 in `R2`. T5's second member does not. This note says how the run reads against the frozen terms. Adjudication is the maintainers'.

## 1. Equations first

The instrument is M8.16's, byte for byte. Its law, discretization, exact kernel, bordered Newton, seeds and continuation, linear record and convergence rule are those of [M8.16's method note](../findings/m8_16_method_note.md), §§ 1.1 to 1.7, unchanged, in the same notation: `R = c = g = 1`, and `u = 2.22×10⁻¹⁶`. M8.16.1 adds the scoring: a bar read at the next order, the rows' checks, a ray that gates nothing, and T5's second member.

### 1.1 The next-order prediction

```text
Proposition N:   λ_g(ε) = εκs_g + ε² c_g + O(ε³),   each slow group g of a nondegenerate orbit
                 c_g = lᵀ T₁ r, read at the group's member in the closed first quadrant (+iτ for an imaginary pair);
                 a multiple group's correction is a multiple of the identity on its eigenspace
at cutoff N:     c_g(N) keeps exactly the channels at or below N: at N = 16 it drops level 18 in R4 and R5, and
                 levels 17 and 19 in R2; at N = 24 and 32 it drops none, and the two coincide
the ray:         c_g°(N), the prediction with the off-ray part left out
```

- **Proposition N** is DERIVED in [The Soft-Slot Branches](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/soft-slot-branches.md), § III.
- **The values** come from the reduced quartic alone, by `run/next_order_values.py`, with no solve on the instrument: exact up to the eigenvalue step at the algebraic cases, and at 50 digits at T4, whose representative is the interval-certified point. They are frozen in `run/next_order_values.json`, SHA-256 `b05fff5ddd71c29c…`, and carried in `FROZEN.json`.

### 1.2 The next-order bar

```text
points:     ε ∈ {0.25, 0.5, 1}, at each cutoff N = 16, 24 and 32
check 1:    at each point, accepted, its seed checked, K1 and converged; and the group's computed values assigned
            as K2 assigns them, one to one by class and Krein sign with multiplicity and the least total relative
            distance, but against εκs_g + ε²c_g(N)
h(ε):       (λ̄/ε − κs_g)/ε, with λ̄ the mean of the group's values at the ε reached
ĉ₂, ĉ₃:     h extrapolated to ε = 0, by Lagrange's rule, from the first two points and from all three
check 2:    each record group holding the values associated with one entry of the point's convergence summary, by its
            eigenvalue indices, and E_c = Σ |w_i| E_i / ε_i² ≤ 0.1 C_g(N), with E_i the entry's ‖P_g‖ max(‖R_g‖, u‖A‖)
            and w_i the weights of ĉ₃
check 3:    the spread, |ĉ₃ − ĉ₂|, at most C_g(N) = max(0.1 |c_g(N)|, 10⁻³ |κs_g|)
check 4:    |c_g(N) − ĉ₃| at most max(spread, 0.1 C_g(N))
reading:    pass when checks 1 to 4 hold at every cutoff; fail when check 3 or 4 fails where checks 1 and 2 hold;
            Unresolved otherwise, with the failing check and point named
```

- **Reported beside it, unscored,** for every group and cutoff, as the terms list them: `c_g`, `ĉ₂`, `ĉ₃`, the spread, the ceiling and `E_c`; the two-term residual at `ε = 0.25`, `|λ − εκs_g − ε²c_g(N)| / (ε|κs_g|)`, beside 1%; and the deviation from leading order. `RECORD.md` § 11 gives them all.
- **Check 1's assignment** is against the next order because two groups of one class and sign whose next-order shifts match their separation would be exchanged against the leading order, as T5's two lowest are at `ε = 1`. The review of #650 found it (B1), and the terms were revised before the go.

### 1.3 The checks, as M8.16.1 changes them

```text
K3(a):    as M8.16's, with the slow band outside the in-span class read by the bar, its check 1 as K3(a) reads it:
          the point accepted, its seed checked, and the values assigned outside the in-span pair's class
K4:       the controls, as M8.16's; the pyramid at ε = 0.25: converged, Hyperbolic, (5, 1, 4), every seed checked,
          and its quartet and Krein-positive pair passing the bar
K5:       a row or a member: every seed checked; at ε = 0.25, K1 at every cutoff, and converged with the expected
          type and indices; every predicted slow group passing the bar
K6:       a ladder: every point accepted at every cutoff, every seed checked; at each read point, agrees, disagrees
          or unresolved against M8.15's record, by its type, K = n(B) − n(B|G_tol) and k_i⁻, with the branch identity
          between N = 24 and 32; no disagreement, and agreement at every read point with ε ≤ 2
the ray:  K1 and K2 at its four points; the bar on its three groups; and the discrimination: wherever checks 1 and
          2 hold, c_g°(N) fails check 4 at c_g's tolerance
```

### 1.4 The verdict

- **The instrument qualifies** if K1 to K4 pass on C1 to C3 and the pyramid, with K3 resolved. A failed check there stops the run, and the verdict is NOT QUALIFIED.
- **A row qualifies** if the instrument does, and the row passes K5, and K6 where it has a ladder. An `R5` row also needs C2a/R5's K1 and K4.
- **T5's second member** qualifies as a member, on its own K5. **The C3 ray** gates nothing.
- **The stop.** M8.16.1 is the instrument's last qualification, for the instrument and for each row. A row or member it does not qualify is not offered to this instrument again.

### 1.5 T5's second member

```text
u₂ = u p₀,   p₀ = (1 + k)/√2,   p₀ i p₀⁻¹ = j:     u₂ = (u − iΘu)/√2, read with i
the slow polynomials, exact in ν = s²:
  T5:    (20449ν + 153664)(418161601ν² + 6989958976ν + 28677390336)
  T5J:   (1859ν + 15680)(418161601ν² + 6605190592ν + 25491013632)
```

Their resultant is nonzero. So for small `ε` the two members' slow spectra are disjoint, and no element of the action's symmetry group carries one member's standing wave to the other's (DERIVED; the terms, § T5'S SECOND MEMBER, state the proposition with its range). The member's outcome is its own: it neither carries the verdict on T5's registered member, nor takes it.

## 2. Equation-to-code map

The links are pinned to MIT `d1c0ec8`, the frozen instrument. The instrument's own map is M8.16's note, § 2. The new code is in `run/`: `next_order_values.py`, the values; `cases.py`, the cases, which tie the values to the frozen spectra; `checks.py`, the scoring; `seeds.py`, the two new seeds; `driver.py`, the run; and `write_guard.py` and `freeze_block.py`, the freeze.

| Equation | Code |
| --- | --- |
| § 1.1 the values, by case, group and cutoff | [`algebraic_case`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/next_order_values.py#L217), [`t4_case`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/next_order_values.py#L373), [`main`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/next_order_values.py#L424) |
| § 1.1 the values tied to the frozen spectra | [`_tie`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/cases.py#L160), [`_next_order`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/cases.py#L195) |
| § 1.2 the next-order prediction | [`predicted_next`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L313) |
| § 1.2 check 1's assignment | [`mode_values`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L325) |
| § 1.2 check 2's association | [`association`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L362) |
| § 1.2 the extrapolation's weights | [`lagrange0`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L308) |
| § 1.2 checks 1 to 4 at a cutoff | [`bar_cutoff`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L386) |
| § 1.2 the reading | [`bar_group`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L437), [`bar`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L458) |
| § 1.3 K3 | [`k3`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L496) |
| § 1.3 K4 at the pyramid | [`check_pyramid_k4`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L568) |
| § 1.3 K5 | [`check_row_k5`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L583) |
| § 1.3 K6 | [`check_row_k6`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L690), [`m815_point`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L683) |
| § 1.3 the ray | [`check_ray`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L606) |
| § 1.4 the stop and the verdict | [`stop_checks`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L734), [`k6_holds`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L751), [`verdict`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/checks.py#L757) |
| § 1.5 the new seeds | [`representative`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/seeds.py#L38), [`seed_state`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/seeds.py#L51) |
| the run: its order, the gate record and the row gate | [`main`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/driver.py#L462), [`write_gate`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/driver.py#L432), [`row_gate`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/driver.py#L447) |
| the resume | [`resume`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/driver.py#L400) |
| the freeze: the values checked, the targets copied, written once | [`next_order_values`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/write_guard.py#L56), [`copy_targets`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/write_guard.py#L92), [`write`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/write_guard.py#L110) |
| the freeze block | [`build`](https://github.com/dmobius3/mode-identity-theory/blob/d1c0ec889b09b4a93d5f08e63280080e25e83e2e/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/run/freeze_block.py#L40) |

## 3. The run

- **The environment.** Python 3.13.13, NumPy 2.5.0 and SciPy 1.18.0, on Accelerate's BLAS and LAPACK at default threading, under macOS 15.8 (24H23) on one Apple M3, as `run/ENVIRONMENT.json` records it. It was read again before and after the run, with no difference.
- **The order of the freeze.** The instrument on MIT `main` at `d1c0ec8`, with its manifest pin, `8cc2d7e2d01a72fc…`; the maintainer's go; `run/write_guard.py`'s `FROZEN.json` at 2026-10-25T01:40:57Z, with its pin, `c258e299b8f0268e…`; the freeze block, whose pull request opened before the run and merged during it; then the run. The driver refuses a sealed case unless the freeze validates.
- **The run.** `python3 -I -B -u run/driver.py` started at 2026-10-25T01:57:38Z, on mains power at its launch, with sleep held off for its length. Its log records the manifest pin at the start. The cases ran in the terms' order: the controls; the pyramid, where the driver wrote the gate record; the C3 ray; the samples of T1 and T4 in both slots and of T5J; then the ladders of T2 and T3 in both slots and of T5. The verdict was written at 2026-10-25T16:35:38Z, 52680 s after the start, against 52681 s by its own clock.
- **Deviations.** None in the run.

## 4. Results against the frozen terms

The record is per case. [`RECORD.md`](https://github.com/dmobius3/mode-identity-theory/blob/292b158cf1a53902489ced3426e1f047699aeb62/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1/RECORD.md) gives every number, with its check, and every group's next-order reading at every cutoff in its § 11.

| Case | Role | Slot | Checks | The next-order bar | Outcome |
| --- | --- | --- | --- | --- | --- |
| C1 | control | `R3` | K1, K4 |  | passed |
| C2a | control | `R4` | K1, K2, K4 |  | passed |
| C2b | control | `R2` | K1, K2, K4 |  | passed |
| C3 | control | `R4` | K1, K4 |  | passed |
| C2a/R5 | R5gate | `R5` | K1, K4 |  | passed |
| P5 | pyramid | `R4` | K1 to K4, K3 resolved | 2 groups pass | passed |
| C3R/R4 | ray | `R4` | K1, K2, the discrimination | 3 groups pass | passed, gating nothing |
| T1/R4 | row | `R4` | K5 | 5 groups pass | qualified |
| T1/R5 | row | `R5` | K5 | 5 groups pass | qualified |
| T4/R4 | row | `R4` | K5 | 4 groups pass | qualified |
| T4/R5 | row | `R5` | K5 | 4 groups pass | qualified |
| T5J/R2 | member | `R2` | K5 fails | 3 groups Unresolved | not qualified |
| T2/R4 | row | `R4` | K5, K6 | 2 groups pass | qualified |
| T2/R5 | row | `R5` | K5, K6 | 2 groups pass | qualified |
| T3/R4 | row | `R4` | K5, K6 | 2 groups pass | qualified |
| T3/R5 | row | `R5` | K5, K6 | 2 groups pass | qualified |
| T5/R2 | row | `R2` | K5, K6 | 3 groups pass | qualified |

- **The verdict,** as the driver wrote it: QUALIFIED. The instrument qualifies, with K3 resolved, and the `R5` gate passed. The rows it qualifies: T1/R4, T1/R5, T4/R4, T4/R5, T2/R4, T2/R5, T3/R4, T3/R5, T5/R2. The member not qualified: T5J/R2. The C3 ray: passed.
- **The pyramid** passes K1 to K4. Its quartet lies 5.76%, 5.78% and 5.78% from Theorem R's leading order at `ε = 0.25`, at `N = 16, 24` and 32, where M8.16 stopped, and passes the bar at every cutoff: its spread is 0.024, 0.026 and 0.026 of the ceiling, and its two-term residual 0.19%, 0.20% and 0.20%. K3's (a) to (d) hold at every cutoff. This is a known outcome, not a check of Proposition N passed (§ 5.1).
- **The C3 ray** passes K1, K2 and the bar on its three groups, and its discrimination holds: the off-ray prediction `c_g°(N)` lies at least 44 tolerances from `ĉ₃`.
- **The rows.** Every sample and ladder passes K5, every one of its groups passing the bar. Every ladder passes K6, with no disagreement with M8.15 and agreement at every read point with `ε ≤ 2`.
- **T5's second member** fails K5. Its three groups read Unresolved by check 1 at `ε = 0.25`, at every cutoff, where the convergence rule reads the point Unresolved (§ 5.2).
- **The controls'** largest deviation from leading order at `ε = 0.25` is 0.46% to 0.93%, at `N = 32`.

## 5. Findings after the run

The interpretations in this section are post-run findings, not additional qualification tests. Their underlying K5 and K6 readings retain their registered scoring effect. No new outcome is assigned here.

### 5.1 The pyramid at the next order

M8.16's run stopped on the pyramid's quartet, 5.78% from leading order at `ε = 0.25` against a bar of 5%, and [its method note](../findings/m8_16_method_note.md), § 5.1, read the departure as a next-order term (INFERRED). Proposition N then gave that term in closed form, and M8.16.1 froze it before the go. Read against `εκs_g + ε²c_g(N)`, the same quartet passes checks 1 to 4 at every cutoff, its two-term residual 0.19%, 0.20% and 0.20% at `ε = 0.25`, and the Krein-positive pair's 0.0010%, 0.0007% and 0.0007%. What M8.16's note inferred, Proposition N now predicts, frozen before the go. The run reproduces M8.16's pyramid, its group centres equal bit for bit (`RECORD.md` § 3), so this agreement is the known outcome the terms name, read as INFERRED, and not a check of Proposition N passed (the terms, § Known outcomes; the reading note of [#650's first review](https://github.com/openwave-labs/openwave/pull/650#pullrequestreview-5631395680)). What this run adds is the rows, the C3 ray and T5's second member, none of them solved on this instrument before the freeze. Nor does the bar bound a remainder: a pure `ε³` term of any size passes checks 3 and 4, since `h` is then linear in `ε` and both extrapolations return `c_g`. The margin behind check 1 is measured, not certified, as the approval of #650 notes.

### 5.2 T5's second member

At `ε = 0.25` the point is accepted at every cutoff, K1 holds, and its three slow groups are assigned; in the convergence rule's reading they converge, with relative change at most 1.15×10⁻⁹ between the two highest cutoffs. The rule reads the point once, from its three cutoffs, and reads it Unresolved on a partner set near `6.015i`: each slow group's partner, its nearest imaginary group of opposite Krein sign, which the rule reads wherever it lies. That Krein-positive set's change from `N = 24` to 32, 4.8×10⁻⁶, exceeds both its change from 16 to 24, 9.7×10⁻⁷, and the floor, 4.1×10⁻⁷: it is non-contracting above the floor. At `ε = 0.5` and 1 the point converges, Elliptic, as expected; at `ε = 2`, reported, the rule reads Unresolved again, on a partner set near `5.934i` whose count differs between cutoffs. The member's `ε = 0.25` points lie below the calibration's fitted range of `m`, down to 0.148 against `0.204`, as T5's registered member's do, and those converge. Why this partner set does not contract is OPEN.

### 5.3 The ladders above `ε = 2`

K6 requires agreement with M8.15 at every read point through `ε = 2`, and no disagreement at any read point. Above `ε = 2`, an Unresolved point neither agrees nor disagrees, and does not itself fail K6; an actual disagreement would fail the row. Such a point is not typed (the terms, § STATED LIMITS: WHAT IS ADDED). **T2/R4** agrees at all 9 read points above 2, Hyperbolic at `ε = 32, 45.3, 64, 72`, as M8.15 read it, and Elliptic at the others it types. **T2/R5** agrees at all 8 read points above 2, Elliptic at each. **T3/R4** agrees at 7 of the 10 read points above 2, Elliptic at each; the rule reads Unresolved at `ε = 16, 45.3, 64`. **T3/R5** agrees at all 7 read points above 2, Hyperbolic at `ε = 22.6, 32`, as M8.15 read it, and Elliptic at the others it types. **T5/R2** agrees at 2 of the 10 read points above 2, Elliptic at each; the rule reads Unresolved at `ε = 5.66, 8, 11.3, 16, 22.6, 32, 64, 90.5`. The census run's adequacy tests apply at every Unresolved point.

## 6. Provenance

- **Terms:** `tasks/m8_16_1_task_details.md` at OpenWave `164288f9`, SHA-256 `9d16712982e53889…`.
- **Instrument:** MIT `d1c0ec8`. Its manifest pins 48 files, `8cc2d7e2d01a72fc…`, and `SHA256SUMS` lists every file of the folder.
- **Freeze:** `run/FROZEN.json`, pin `c258e299b8f0268e…`, carried in full by [the freeze block](../m8_16_1/freeze_block.md).
- **Record:** MIT [`292b158`](https://github.com/dmobius3/mode-identity-theory/tree/292b158cf1a53902489ced3426e1f047699aeb62/files/framework/files/working/files/scripts/soft-slot-dynamics-m8-16-1). It holds `RECORD.md`, `run/out/`, the freeze's files, M8.15's target records as copied, and the post-run files.
- **Reproduction:** `REPRODUCE.md` beside the instrument, and `RECORD.md` § 12.

## 7. What this run does not verify

- **Finite-amplitude adequacy at the top of a ladder.** A point the convergence rule leaves Unresolved is not typed, and qualification does not establish adequacy there. The census run's adequacy tests apply (§ 5.3).
- **Qualification of T5's second member at `ε = 0.25`.** Its three slow groups are matched and converge across the cutoffs, but the point-wide convergence rule is Unresolved on a distant partner set. Check 1 and K5 therefore do not pass, and the member is not qualified. Why that partner set fails to contract is OPEN (§ 5.2).
- **The margin's ten-fold headroom beyond the controls.** M8.16's terms fit the margin on the controls, where its ten-fold headroom holds. On this run the zero cluster lies less than ten times below its gray zone's lower edge at 54 points, in 7 cases (P5, T5J/R2, T2/R4, T2/R5, T3/R4, T3/R5 and T5/R2), down to 4.6 times at T3/R5 (`N = 24`, `ε = 4`), and points the bar scores are among them. Every cluster stays separated, as K1 asks, and no constant moves (`RECORD.md` § 2).
- **The persistence of any Elliptic stretch.** It needs a pre-registration of its own, outside this admission.
- **A bound on the next order's remainder.** A pure `ε³` term passes checks 3 and 4 at any size (§ 5.1), and the margin behind check 1 is measured, not certified.
- **Custody before the run.** The published order, from the instrument's commit to the freeze block, fixes when files appeared, not when anything was computed, as the approval of #652 notes.
- **Other machines.** The run is on one machine, and bitwise agreement is not claimed.
- **The platform's criteria.** No `MODELS.md` cell moves, and M8.7's gate is unchanged.

## 8. Audit record

Before filing, the record and this note were checked in two rounds against the frozen terms, the frozen code and the run's files. The checks rebuilt `RECORD.md` from the files; rescored the next-order bar with separate code across all 37 groups, matching § 11's numeric cells to their printed digits; reproduced a rerun on a complete `run/out/`; recomputed the margin's headroom from all 381 points; and checked this note's equations and code map against the pinned functions. They led to § 11 reporting every quantity the terms list; the diagnosis at T1 and T4; T5J's cause, read as one convergence reading on a partner set its three slow groups share; the pyramid's pass, stated as a known outcome, with its reproduction of M8.16 computed; the margin's headroom; five bounds rounded outward; and three wording changes here. All were adopted, and no reading changed.
