# M5.20 method note: conservative dynamics of the regularized vortex loop, the radiation-mechanism search

**Task**: [`m5_20_task_details.md`](../tasks/m5_20_task_details.md) · **Spec**: Duda 2026-07-10 ([`m5_19_convo.md`](../tasks/m5_19_convo.md)): "instead of just energy minimization, there is required real evolution e.g. with Euler-Lagrange equations for the assumed Lagrangian, searching if there is a way to radiate this energy as some different field excitations". Predecessor: [`m5_19_method_note.md`](m5_19_method_note.md) (statics). Status: ✅ complete (audited; awaiting task review).

## 1. Equations first

**The assumed Lagrangian** (the load-bearing assumption, tracker [Q23](../m5_question_tracker.md#q23-detail)):

```text
L = ∫ 2πρ dρ dz [ (1/2) ||∂t M||_F²  −  u_curv  −  V ]

u_curv = 4 c₂ Σ_{μ<ν} ||[∂_μ M, ∂_ν M]||_F²          (c₂ = 1 sim units; the audited M5.17 form)
V      = w Σ_{p=1..3} (Tr M_sp^p − c_p)²,  c_p = 1   (the spectral potential, δ = 0, w = 7.24e-4 calibrated)
```

The kinetic term is the canonical sigma-model choice: the minimal completion of the sanctioned static functional. It is NOT derived from the author's Γ-variable Hamiltonian (his negative `−(Γ0¹Γ̃μⁱ − Γμ¹Γ̃0ⁱ)²` clock contributions have no counterpart here); that dictionary is the queued ask Q23. Everything below is conditional on this choice.

**Discrete EOM** (variational, on the M5.19 axisym reduction, mass matrix = the cell measure `w_cell = 2πρh²`):

```text
w_cell ∂t² M = − ∂E/∂M          (pinned far-field boundary; velocity-Verlet, symplectic)
```

**Sponge (radiation absorber)**: operator splitting; after each conservative step `v → v·exp(−γ dt)` inside the absorbing layer (quadratic ramp, width 16, γmax 0.5), and the kinetic energy removed is accumulated exactly:

```text
E_abs(t) = Σ_steps [ KE_before − KE_after ]   ⇒   KE + PE + E_abs = const  (up to Verlet drift)
```

**The linear spectrum around a uniform vacuum M₀** (derived, measured, and AUDIT-CORRECTED: the naive version of this lemma was refuted by the independent audit and is stated here in its correct form):

```text
Cartesian channels: [∂_μ(M₀+u), ∂_ν(M₀+u)] = [∂_μ u, ∂_ν u] = O(u²)  ⇒  O(u⁴) in u_curv,
BUT the equivariant azimuthal channel carries the BACKGROUND gradient A_φ = [J, M₀]/ρ,
so [A_pert, A_φ^bg] is LINEAR in u. Hence:

on J-COMMUTING vacua ([J, M₀] = 0, e.g. e3e3^T):
   quadratic action = ∫ [ (1/2)(∂t u)² − (1/2) u·V''(M₀)·u ],  no spatial derivatives
   ⇒ FLAT dispersion, zero group velocity, NO linear radiation channel
   (measured: e3 pulse spread 1.3e-6 cells over T = 60)

on e2e2^T (the M5.19 escaped far field): a linear channel EXISTS,
   quadratic curvature = 4(‖[∂ρu, B]‖² + ‖[∂zu, B]‖²)/ρ²,  B = e2e2^T
   ⇒ stiffness ∝ 1/ρ² (radially decaying): weak but nonzero
   (measured: eps² scaling, slopes 2.00; analytic coefficient matches numerics to 0.09%;
    e2 pulse spread +0.49 cells over T = 60)
```

The vacuum mass spectrum at the uniaxial vacuum diag(1,0,0) (audit-confirmed analytically): quadratic form `w·[(Tr X)² + 13X₁₁²]`, eigenvalues `{0,0,0,0, 2w(8−√38), 2w(8+√38)}`, ω = {0.05156, 0.14322}; the four zero modes = two director rotations + two directions that split the degenerate {0,0} pair (lifted only at quartic order: the linear face of the removability channel).

**The Dirichlet control** (the Q20 ambiguity made harmless): variant `dir` adds `c₁(||M_ρ||² + ||M_φ||² + ||M_z||²)`, c₁ = 0.5 ⇒ linear waves at speed `√(2c₁) = 1` (+ the V mass gap): a theory WITH a propagating channel, run side by side.

## 2. Equation-to-code map

| Term / instrument | Function | File |
| --- | --- | --- |
| `u_curv` (audited, M5.17) | `curvature_density_np` | [`m5_17_energy.py`](https://github.com/openwave-labs/openwave/blob/main/openwave/xperiments/m5_liquid_crystal/research/scripts/m5_17_energy.py) |
| spectral `V`, `dV/dM` | `potential_density_spec_np`, `dv_spec` | [`m5_18_spectral.py`](https://github.com/openwave-labs/openwave/blob/main/openwave/xperiments/m5_liquid_crystal/research/scripts/m5_18_spectral.py) |
| audited gradient | `energy_gradient_spec_np` | same |
| fast-path gradient (gate GF pins it: rel 0.0 seed / 1.3e-16 random) | `grad_fast` | [`m5_20_a1_dynamics.py`](https://github.com/openwave-labs/openwave/blob/main/openwave/xperiments/m5_liquid_crystal/research/scripts/m5_20_a1_dynamics.py) |
| velocity-Verlet + exact sponge ledger | `evolve` | same |
| Dirichlet control term + adjoints | `dir_density_np`, `dir_gradient_np` | same |
| sponge profile | `sponge_gamma` | same |
| pulse test (flat dispersion vs ballistic) | `gate_ga3` | same |
| loop seeds (M5.19 verbatim) | `loop_field_escaped` | [`m5_19_c1_loop.py`](https://github.com/openwave-labs/openwave/blob/main/openwave/xperiments/m5_liquid_crystal/research/scripts/m5_19_c1_loop.py) |
| z-escaped seed family (far field e3e3^T) | `loop_field_escaped_z` | `m5_20_a1_dynamics.py` |
| ring locator + guarded winding measure (M5.19) | `ring_by_m13`, `winding_measure` | [`m5_19_d1_relax.py`](https://github.com/openwave-labs/openwave/blob/main/openwave/xperiments/m5_liquid_crystal/research/scripts/m5_19_d1_relax.py) |
| endpoint verdicts + classifier | `classify` | [`m5_20_b1_verdicts.py`](https://github.com/openwave-labs/openwave/blob/main/openwave/xperiments/m5_liquid_crystal/research/scripts/m5_20_b1_verdicts.py) |
| endpoint maps + per-peak core hunt | `core_hunt` | [`m5_20_b2_maps.py`](https://github.com/openwave-labs/openwave/blob/main/openwave/xperiments/m5_liquid_crystal/research/scripts/m5_20_b2_maps.py) |
| remnant blob + breathing spectrum + vacuum mass Hessian | `m5_20_c1_blob.py` (all) | [`m5_20_c1_blob.py`](https://github.com/openwave-labs/openwave/blob/main/openwave/xperiments/m5_liquid_crystal/research/scripts/m5_20_c1_blob.py) |

## 3. Results, each next to its gate

| Result | Number | Gate / verification |
| --- | --- | --- |
| Instrument valid | endpoint drift ≤ 1.3e-5 (comm) / ≤ 4.2e-5 (dir) over 100k steps; dt² ratios 4.0006, 4.0001 | GF bit-level, GA0, GA1, GA2 (`data/m5_20_a1_gates.json`); audit C1 |
| Linear spectrum (corrected form, § 1) | e3 pulse spread 1.3e-6 cells / e2 pulse +0.49 cells over T = 60; eps² scaling on e2, analytic coefficient to 0.09% | GA3 + `m5_20_pulse_e3.json`; audit C2 (which refuted the naive form) |
| Vacuum mass spectrum | ω = {0.05156, 0.14322}, 4 zero modes (2 rotations + 2 removability-face) | audit C7, analytic `2w(8 ± √38)` |
| **All 10 production runs UNWIND** (2 seed classes × closed/sponge, corepin release × 2, z-family × 2, dir × 2) | zero surviving winding at any genuine core in every endpoint | pre-registered classifier + per-peak core hunt + the audit's independent instruments (bilinear winding, dense center map, spectral-gap hunt, net-charge circles); audit C3 |
| **Unwinding needs NO radiation** | closed boxes unwind with E conserved to ~1e-5 (corepin closed: 1.5e-6) | audit C4 (boundary/quench/dt/float32/axisym artifact readings each killed) |
| Gentle start is long-lived, not protected | corepin release: core amplitude m13_max ≈ 0.5 to t ≈ 300, < 0.1 by t ≈ 525-550 (vs t ≈ 100-160 quench) | audit-corrected metric (the centroid q(t) trace was noise) |
| Positive control | q = +0.5 machine-precision to t ≈ 387 with the core frozen; then a net −1/2 screening structure nucleates in 2 < r < 10 (ring at 4.5-5.7 from pin) | audit C5 (robust read: r2 guard 0.124, r10-12 guards 0.2-0.43) |
| Far-field structure controls dispersal | e3 far field: remnant energy fully trapped (sponge E_abs = 0.000, run indistinguishable from closed); e2 far field: corepin remnant 21.9% absorbed by T = 2000, still growing | the corrected § 1 lemma, corroborated by an independent run pair |
| Dirichlet control (the Q20 ambiguity) | dir loops radiate 99.8-99.9% of E0 into the sponge and unwind; no persistent structure left | verdicts on `melt_*_z_dir_sponge`; headline Q20-insensitive |
| **The localized remnant (breather candidate)** 🔶 | coherent blob at the ring site: E(r<8) osc 1.08-1.28 (15.5% of E0), s_min osc 0.64-0.77, broad comb ω ≈ 0.25 (FWHM 0.21-0.29), loss 5.2%/300 tu; present in closed AND sponge endpoints; absent in the dir theory | `m5_20_blob_corepin_release_closed.json`; audit C6; longevity beyond horizon UNMEASURED |

**The licensed close sentence**: within the sanctioned static functional plus the canonical kinetic term, in the axisymmetric sector, the regularized vortex loop is not protected: it unwinds under conservative real-time evolution with total energy conserved (no radiation required), the removability channel M5.19 found in statics operating dynamically, and this verdict is insensitive to the Q20 gradient-term ambiguity; what persists instead is a localized quasi-periodic oscillating remnant (breather candidate) whose lifetime exceeds the run horizon in the commutator theory.

## 4. Not computed

- The author's Γ-variable time sector (the negative `Γ·Γ̃` clock terms): no Γ↔M dictionary exists on our side (Q23). Every conclusion here is conditional on the canonical kinetic term.
- Full 3D (non-axisymmetric) evolution: the axisym reduction restricts the mode set. For the UNWINDING result this makes the negative stronger (a removal path exists already within the constraint); for radiation it removes non-axisymmetric channels (unmeasured).
- The relativistic boost / time-dilation frame of his closing remark (needs the clock machinery; M5.20.2).
- Blob longevity beyond the run horizon; blob existence in true unbounded vacuum (box + sponge is the instrument's proxy).
- δ ≠ 0 sectors (Q22 parked: "I don't know in this moment").

## 5. Audit record

Independent adversarial audit, 2026-07-11 (second agent, own instruments: bilinear-interpolated winding with reported guards, dense winding map over all centers, spectral-gap core hunt, net-charge circles; audit scripts kept out of the repo). Verdicts: C1 instrument CONFIRMED (drift wording tightened: endpoint ≤ 1.3e-5, intra-trajectory max 1.65e-5) · **C2 the naive flat-dispersion lemma REFUTED as stated** (correct form now in § 1; the production far field e2e2^T carries a 1/ρ² linear channel; headline unaffected, overdetermined) · C3 all-unwound CONFIRMED (zero surviving winding by independent instruments; every spurious ±0.5 read = the `winding_measure` guard-evasion bug, which biased labels AGAINST the headline) · C4 no-radiation-needed CONFIRMED (boundary/quench/dt/float32/axisym artifact readings each killed; axisym evolution is exact full dynamics for axisym data) · C5 positive control QUALIFIED (machine-0.5 to t ≈ 387; the robust screening statement replaces the sub-guard radius detail; screening ring located 4.5-5.7 from the pin) · C6 blob CONFIRMED (all numbers verified; loss may be partly linear transport) · C7 vacuum spectrum CONFIRMED analytically · C8 dir-vacuum CONFIRMED (machine precision) · C9 scope honesty QUALIFIED (the unconditional A2 wording + 2 overclaims found, all corrected in the task record and here). Full record: [`m5_20_task_details.md § ADVERSARIAL AUDIT RECORD`](../tasks/m5_20_task_details.md).

## 6. Queued asks

| ID | Ask |
| --- | --- |
| [Q23](../m5_question_tracker.md#q23-detail) | The kinetic/time term in M variables (or the Γ↔M map); should the negative `Γ·Γ̃` terms act already at the neutrino-loop level? Everything above is conditional on the canonical choice; if his time sector maintains the core (the clock as the protector), that is exactly what this Lagrangian lacks |
| [Q16 residual](../m5_question_tracker.md#q16-detail) | Given that "no radiation mechanism" does not protect (unwinding exports no energy), does the construction intend a structure the axisym single loop lacks (hedgehog embedding of the 1-vortex cross-section, Hopf link), or is the persistent object the OSCILLATING remnant rather than the wound loop? |

## 7. Close-out

Ten conservative-dynamics runs, three instruments, one adversarial audit (one lemma refuted and corrected, headline overdetermined). The statics negative (M5.19) extends to canonical conservative dynamics: winding is removable without energy export; what the functional actually sustains is a localized quasi-periodic oscillation. The gate to any reopening: a time sector that maintains the core (Q23/Q21), a topology the axisym sector cannot express (Q16 residual), or a δ-sector directive (Q22).
