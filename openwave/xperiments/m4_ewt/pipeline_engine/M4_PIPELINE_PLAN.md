# M4 Pipeline Engine — Implementation Plan

> **Status:** DRAFT (working document)
> **Scope:** The pipeline_engine as the realisation substrate for Enhanced EWT.
> **Audience:** Contributors implementing, testing, or extending M4.
> **Related:** `M4_engine_upgrade.md`, `M4_k_selectivity_Formalization.md`,
> `__M4_model_briefing.md`, manuscript v5.0.2 (Zenodo, DOI
> 10.5281/zenodo.22875996), Yee's EWT corpus.

---

## 0. Executive Summary

The pipeline_engine is a **composition root** for M4 simulations: a list of
stateless processors executed against a shared `Context`, with explicit
`requires`/`provides` contracts, swappable sinks, and a typed `FeatureBag`
for runtime state. It exists because the previous monolithic `wave_engine.py`
made it impossible to express the actual physics of Enhanced EWT — every
mechanism was a hard-coded branch, every variant a new file, every comparison
a code duplication.

This document captures:

1. **Why** the previous implementation only *simulated* EWT and did not
   *realise* it (Section 1).
2. **What** the core conceptual commitments are that the new engine must
   honour (Sections 2–5).
3. **How** to build the engine (Block 1) and the physics (Block 2), with
   concrete, checkable work items (Sections 6–7).
4. **What** from the old implementation is obsolete and should not be ported
   (Section 8).
5. **Which** questions remain genuinely open and require author input or
   further research (Section 9).
6. **What** is deferred to Milestone 2 (stability and K-selectivity,
   Section 15) and Milestone 3 (spin extension, Section 16).

Nothing in this document is a claim about nature. It is a **plan for a tool**,
written so that the tool can express the hypotheses we intend to test.

---

## 1. Why the previous implementation faked EWT

This section is diagnostic, not accusatory. The old `wave_engine.py` was an
honest attempt to translate EWT into code. It failed for structural reasons,
not for lack of effort.

### 1.1. Wave centres as pinned sources, not reflectors

Yee's EWT defines a wave centre as a **point at which incoming waves are
reflected to become outgoing waves**. The soliton is the standing-wave
interference of `Psi_in` and `Psi_out`, bounded by the particle radius.

The old implementation defined wave centres as **hard-pinned regions**:

```text
psi = A * sin(omega t + offset) * r_hat    inside a ball of radius R around each WC
```

This is a driven antenna, not a reflector. The field does not participate in
the WC's existence; the WC simply overwrites voxels. There is no reflection,
no `Psi_in`/`Psi_out` distinction, no conservation argument.

### 1.2. One field, not two

Yee's EWT distinguishes **longitudinal** (mass, charge) from **transverse**
(spin, magnetism), coupled through the fine-structure constant at the WC.
The old implementation had a single vector field `psi` with no mode split.

Consequence: the fine-structure constant had to be **imposed** through
`cos(offset)` and the mass of the electron through an analytic formula.
Neither emerged from dynamics.

### 1.3. Wavelength structure ignored

Yee's standing-wave geometry prescribes *decreasing* wavelengths from the core:

```text
r_wavelength(n) = 2K*lambda - 2n*lambda
r_x = (K + 2*sum_{n=1..x}(K-n)) * lambda
```

with a maximum radius `r_particle = K^2 * lambda`. The old implementation used
a single `base_wavelength` throughout. The electron's characteristic ring
structure — visible in the Lund stroboscope image — was absent.

### 1.4. Density profile fixed, not self-consistent

Enhanced EWT's gravitational sector is built on the **push-out** mechanism:
the soliton's energy density `rho_E` displaces Elastic Medium Constituents
(EMC), creating a local deficit `rho(r) < N_nu,stat`. The deficit is what the
outside vacuum presses against; the pressure gradient is what we call gravity.

The old implementation had `rho(r)` as a **fixed profile relative to the
domain centre**. When a WC drifted, the well did not follow. There was no
self-consistency between `|Psi|^2` and `rho(r)`.

### 1.5. Nonlinearity as an external potential, not a consequence of `c(rho)`

M4.9 established the microscopic relation:

```text
v_phys(eta) = a(eta) * sqrt(k(eta)/m0)  proportional to  eta^{+1/2}
```

where `eta = rho/rho_0`. The local wave speed depends on the local EMC
density. Because the soliton itself depletes EMC, `c^2(r) = c_0^2 * rho(r) /
rho_0`, and the wave equation becomes *automatically nonlinear*:

```text
d^2 Psi / dt^2 = div(c^2(rho) grad Psi) + c_0^2 (beta_rho/rho_0) |grad Psi|^2 Psi - 2 kappa beta_rho^2 Psi^3
```

where the second term is the Euler-Lagrange correction that keeps the
gradient energy `(1/2) c^2 |grad Psi|^2` conserved when `c^2` varies with the
field. The last two terms are the Euler-Lagrange corrections. See Section 5.2.

The old implementation instead injected a Klein-Gordon-style potential
`V(psi) = (c1/4)u^2 - (c2/6)u^3` with `u = |psi|^2`. Mathematically this
gives an NLS soliton. Physically it is a prosthesis: the coupling constants
`c1`, `c2` were fitted, not derived.

### 1.6. Gravity as `-grad E`, not as `-grad rho`

The old `compute_force_vector` used `F = -grad E_local`, where `E_local` was
a heuristic `rho * V * (f * A)^2` with `f` hard-coded to the base frequency.
This measured the *internal* energy gradient, not the *external* EMC density
gradient. The push-out picture requires `F_pressure = -alpha_p * grad rho(r)`,
where `rho(r)` is the EMC packing density, not the soliton's energy density.

### 1.7. Summary table

| EWT primitive | Old implementation | Why it is a fake |
|---|---|---|
| WC as reflector | WC as hard pin | No reflection, no in/out |
| `Psi_in` + `Psi_out` | Single `psi` | No distinction, no closure |
| Decreasing `lambda(n)` | One `base_wavelength` | Ring structure absent |
| `Psi_long` + `Psi_trans` | One vector field | Spin not emergent |
| `rho(r)` self-consistent | Fixed profile | No push-out feedback |
| `c^2(rho)` nonlinearity | External `V(psi)` | Coupling fitted |
| `F = -grad rho` gravity | `F = -grad E` | Measures wrong gradient |
| Boundary as EMC wall | Dirichlet `psi = 0` | No profile, no sign change |
| BCC lattice | Simple cubic stencil | Medium != medium of theory |

---

## 2. Conceptual commitments

These are the principles the new engine and physics must respect. They are
*not* claims about nature; they are constraints on the tool.

### 2.1. Conservation is structural, not imposed

Energy conservation in EWT is a consequence of the **unitarity of reflection
at the WC** and the **Hermiticity of the wave equation**, not an external
constraint. If the WC reflection satisfies

```text
|Psi_out|^2 + |Psi_spin|^2 = |Psi_in|^2
```

and the wave equation derives from a real Hamiltonian density, then energy
is conserved by construction. Any deviation is a bug, not a feature.

The engine must therefore expose enough structure to *measure* the energy
budget and *verify* that `dE/dt + flux ~ 0`.

Reflection is not assumed to be active by default. The default pipeline
realises the nonlinear soliton without a scattering operator: the wave
centres perturb the field through the density-modulated term, but they do
not reflect a base wave. A second pipeline adds the scattering operator
and the corresponding budget channel. The two pipelines share the same
field types and base processors, and differ only in which processors they
include and which vacuum variant they register. Section 5.4 defines the
two configurations.

### 2.2. The soliton is an open system in steady state

The medium carries an always-on base wave (Yee: "waves flow through all of
matter"). This wave supplies `Psi_in` to the WC. The WC reflects part of it
as `Psi_out` and converts part of it into transverse spin. In steady state:

```text
flux_in = flux_out + flux_spin
```

The soliton is a **dissipative structure** in the Prigogine sense — a local
concentration of energy maintained by continuous exchange with the medium,
not a closed system isolated from it.

This is a deliberate commitment to **variant B** (coupled dynamics), not
variant A (static background). It is harder to implement, but it is what
the manuscript describes.

This picture applies to the reflective pipeline (Section 5.4, pipeline B).
The default pipeline (A) uses the same field types but does not model
reflection; it is the simpler non-reflective case.

### 2.3. The EMC density field is dynamic and self-consistent

`rho(r)` is not an input. It is a solution of

```text
d rho / dt = D * laplacian(rho) - gamma_rho * (rho - rho_0) - beta_rho * |Psi|^2
```

in the simplest model (B4b), or a richer evolution with inertia (B4c). In
steady state, `rho(r)` and `|Psi(r)|^2` are mutually consistent.

**The EMC Wall peak, `rho > rho_0`, arrives with B4c, not with B4b.** The
B4b equation is linear parabolic with a source term that is always
non-positive (`-beta_rho |Psi|^2 <= 0`), so by the maximum principle the
density never exceeds `rho_0` from an initial condition at `rho_0`: the
soliton depletes EMC, diffusion redistributes the deficit, and no peak can
form. The overshoot is a property of the inertial equation (B4c), where the
second time derivative removes the maximum principle. Section 3.2 and item
1.16 follow the same distinction. If a future variant is meant to produce a
peak under B4b, the equation itself needs a term that can move EMC outward
(for instance an advective or flux-limited transport term); the current
B4b equation cannot.

### 2.4. The tail is analytic; the soliton neighbourhood is simulated

The far-field deficit

```text
rho(r) -> N_stat * (1 - r_s/r)   for r >> r_core
```

is taken as analytic input (granted in M4.4; derivation in the manuscript).
The pipeline does not re-derive it and does not simulate it. The simulated
domain covers the soliton and its immediate neighbourhood; the tail beyond
is analytic.

This separation is deliberate: the soliton neighbourhood is where the
wave-centre structure lives and where K-selectivity must emerge; the tail
is a solved analytic problem that does not need a discretised field.

### 2.5. Units are pluggable

No processor contains a dimensional constant. Every constant comes from a
single `UnitSystem` feature. Three implementations are anticipated:

- `NaturalUnitSystem` — `lambda = 1`, `c = 1`. For research and algorithm testing.
- `OpenWaveUnitSystem` — `am`, `rs`, as in the legacy xparameters.
- `SIUnitSystem` — for output conversion and cross-checking against CODATA.

The same pipeline runs under any of them. Results are comparable after
conversion.

### 2.6. Topology and geometry are hypotheses, not assumptions

The 1-3-6 arrangement and the `n * lambda` spacing of wave centres are
**candidate** configurations, not given truths. The engine must allow
systematic variation of:

- Topology (1-3-6, golden-angle, BCC, line, random).
- Spacing (exact `n * lambda`, exact `(n+1/2) * lambda`, perturbed, swept).
- Coupling (none, push-out only, push-out with feedback).

Only then can we say which of these factors is necessary, sufficient, or
irrelevant for stability.

### 2.7. What alpha is, and what it is not

The manuscript defines `alpha` as a purely geometric ratio:

```text
alpha = x^2 / S = 1 / (4 pi^3 + pi^2 + pi)
```

where `S` is the emission surface (sphere plus cone) and `x` is a bookkeeping
amplitude that cancels. With the BCC correction:

```text
alpha = 1 / (A_pi - eps_M) ~ 7.29733855e-03
```

This is the value the engine loads from `GeometricConstants`. It is a
**parameter**, not a derived quantity. The engine uses it as the reflection
coefficient at a wave centre; it does not derive it from the field.

A dynamic counterpart — whether some field ratio at a WC coincides with
this value — is a **consistency observation**, not a second derivation. The
engine measures several candidate ratios (Section 7, item 2.2, variant B2b)
so that the coincidence, if any, can be recorded. A mismatch is not a
failure of the plan; it means the geometric ratio has no direct dynamic
manifestation in this engine.

---

## 3. The unit system

### 3.1. Contract

A `UnitSystem` is a feature providing at least:

```text
c            : wave speed in these units
lambda       : fundamental wavelength (lambda_nu)
dx           : grid step in these units
dt           : time step in these units
rho_0        : statutory background density (N_nu,stat)
A_pi         : 4 pi^3 + pi^2 + pi
eps_M        : 1 / (N_geom * pi^3)
N_geom       : 8 pi^4 * (1 - zeta)
gamma        : 1 / eps_M
X_eff        : geometric dilution factor
N_nu_eff     : effective volume deficit
A_base       : base wave amplitude
r_domain     : simulated domain radius
r_core       : soliton extent (K^2 lambda), theoretical scale
c_max        : maximum local wave speed, for the CFL bound
```

Plus conversion methods:

```text
to_physical_length(x)   -> metres
to_physical_time(t)     -> seconds
to_physical_energy(E)   -> joules
to_physical_density(r)  -> 1/m^3
```

### 3.2. Implementations

**NaturalUnitSystem** (default for research):

```text
c      = 1
lambda = 1
dx     = 1 / K_grid     (e.g. 0.05 for 20 voxels/lambda)
dt     = CFL_SAFETY * dx / (c_max * sqrt(3)),   CFL_SAFETY ~ 0.9
```

The 3D leapfrog bound is `dx / (c * sqrt(3))`. `CFL_SAFETY = 0.9` of that
bound gives `dt ~ 0.52 * dx / c`. A 1D run may use `dt = CFL_SAFETY * dx / c`
as a validation figure; the default is 3D and takes the `sqrt(3)` factor.

The timestep `dt` is computed against a maximum wave speed `c_max`, not the
nominal `c_0`:

- For **B4a** (instantaneous, slaved density) the density is bounded by the
  field, `rho <= rho_0`, so `c(rho) <= c_0` and `c_max = c_0`.
- For **B4b** (relaxation) the maximum principle keeps `rho <= rho_0`, so
  the local speed is likewise bounded by `c_0` and `c_max = c_0`. The
  overshoot that would justify a larger `c_max` does not occur in this
  variant (Section 2.3).
- For **B4c** (inertial) the density carries a second time derivative, the
  maximum principle does not apply, and a local peak `rho > rho_0` can form
  at the EMC Wall. Then `c_max = c_0 * sqrt(rho_max/rho_0) > c_0`.

The unit system exposes both `c` (nominal) and `c_max` (for the CFL bound):

```text
dt = CFL_SAFETY * dx / (c_max * sqrt(3))
```

If the density exceeds the assumed `rho_max` during a run, the simulation
is unstable by construction; the maximum must be bounded either by the EMC
Wall height parameter or by an explicit check in `DiagnosticProcessor`
(item 1.18).

**OpenWaveUnitSystem**:

```text
c      = 0.3 am/rs
lambda = EWAVE_LENGTH / ATTOMETER   (~ 28.5 am)
dx     = lambda / 12
dt     = CFL_SAFETY * dx / (c_max * sqrt(3))
```

**SIUnitSystem**:

```text
c      = 299792458 m/s
lambda = 2.8540965e-17 m
dx     = r_e / 200
dt     = CFL_SAFETY * dx / (c_max * sqrt(3))
```

Used primarily for output conversion.

### 3.3. Consequences for processors

A processor must never write `c = 1` or `gamma = 2.4e4` or `lambda = 28.5`.
It must always write:

```python
units = ctx.data.require(UnitSystem)
c = units.c
gamma = units.gamma
```

This rule is checkable by inspection: grep for numeric literals in
`physics/*.py`. If a processor contains a dimensional constant, it is a bug.

---

## 4. Simulation domain and boundary

The pipeline simulates the soliton and its immediate neighbourhood. The
far-field tail of the EMC deficit extends far beyond any tractable domain
and is treated analytically (Section 2.4); it is not simulated.

Two length scales matter, and they are not the same:

- **The soliton extent**, `r_core = K^2 * lambda`. For K = 10 this is
  100 lambda_nu, for K = 12 it is 144 lambda_nu. It is a theoretical scale
  of the standing-wave region. The EMC tail continues beyond it, and the
  tail is analytic.

- **The wave-centre neighbourhood.** The region the K-sweep actually
  measures. Its size is set by the largest distance from the configuration
  centre to a wave centre, plus a buffer of a few lambda. From the geometry
  tests, the measured configuration radii at K = 10 are 2.00 lambda_nu
  (tetrahedron_10_locked) and 0.36 lambda_nu (golden angle); the `line`
  negative control at K = 12 has radius 5.50 lambda_nu. A domain of
  `r_domain ~ 10 lambda_nu` covers every topology in the sweep with a wide
  margin.

The simulation runs on the wave-centre neighbourhood. The soliton extent
and the tail are not resolved; they are analytic inputs.

At `dx = 0.05` (20 voxels per lambda_nu) and `r_domain = 10 lambda_nu`, the
box is 400 voxels in diameter, about 6.4e7 voxels in 3D. Tractable. A
domain that instead resolved the soliton extent `r_core = K^2 lambda` would
be 1.9e11 voxels at K = 12 and is not.

The boundary at `r = r_domain` is one of:

- **Absorbing** — waves leave and do not return. Default for isolated
  soliton tests.
- **Periodic** — the domain wraps. No leakage, at the cost of wrap-around
  artefacts when the soliton's tail meets itself.
- **Reflecting** — waves bounce. Use only when the test specifically
  requires reflections.

The choice is per experiment, not global. There is no attempt to model the
tail at the boundary; the tail is analytic elsewhere.

**Validation with K = 1.** The neutrino has a single wave centre and no
extended soliton structure. It fits inside the domain trivially and serves
as the validation case for the local dynamics before the K > 1 runs begin.

---

## 5. Vacuum layer

### 5.1. What the base wave is

The base wave is the always-on ground-state oscillation of the medium. In
natural units:

```text
Psi_base(r, t) = A_0 * cos(k*r - omega*t)
```

with `k = 2 pi / lambda = 2 pi` and `omega = 2 pi c / lambda = 2 pi`.

### 5.2. The conservation check

The energy budget excludes `E_base`. The check is:

```text
E_soliton     = integral ( (1/2) |dPsi/dt|^2 + (1/2) c^2(rho) |grad Psi|^2 ) dV
E_deformation = integral (1/2) kappa (rho - rho_0)^2 dV
E_total       = E_soliton + E_deformation
check:          dE_total/dt + flux_through_boundary = 0
```

The kinetic term is required: without it, a standing wave's gradient-only
integral oscillates at `2 omega` and the conservation test fails by
construction. The deformation term uses `kappa`, the stiffness supplied by
the unit system.

The budget has two forms, one per pipeline.

**Pipeline A (non-reflective).** There is no `E_base` channel and no
scattering operator. The check is

```text
dE_total/dt + flux_through_boundary + P_deform = 0
```

where `P_deform` is the dissipation ledger of B4b (zero for B4a and B4c).

**Pipeline B (reflective).** `E_base` participates as a separate feature.
The scattering operator exchanges energy between `E_base` and the soliton
by moving the incoming wave into the outgoing wave; the exchange is
internal to the system, so no external channel is needed. The check keeps
the same form as pipeline A, with `E_base` included in the total:

```text
dE_total/dt + flux_through_boundary + P_deform = 0
E_total includes E_base for pipeline B.
```

For an isolated steady soliton, the scattering term averages to zero over
one period of the standing wave. A non-zero average means the soliton is
either growing (absorbing base energy) or decaying (leaking to base).

The wave equation is implemented in the Euler-Lagrange form derived from
the Lagrangian

```text
L = (1/2) |dPsi/dt|^2 - (1/2) c^2(|Psi|^2) |grad Psi|^2 - V(Psi)
```

`V` is the sum of the potentials the selected variants contribute, by the
same rule the budget follows. Under B4a the slaved density
`rho = rho_0 - beta_rho |Psi|^2` makes the deformation energy a potential
in the field, `V = (1/2) kappa (rho - rho_0)^2 = (1/2) kappa beta_rho^2
Psi^4` in the real one-component case, which gives

```text
d^2 Psi / dt^2 = div(c^2(rho) grad Psi) + c_0^2 (beta_rho/rho_0) |grad Psi|^2 Psi - 2 kappa beta_rho^2 Psi^3
```

where the second term is the variation of `c^2` with respect to `|Psi|^2`
(one-component case, `c^2 = c_0^2 (1 - beta_rho |Psi|^2 / rho_0)`) and the
third is `- dV/dPsi`. This is the same equation as the one in Section 1.5,
and the Hamiltonian of this `L` is `E_total` term for term, which is what
makes the budget a check rather than a restatement of the stepper. The
plain divergence form `div(c^2 grad Psi)` alone does not conserve the
gradient energy `(1/2) c^2 |grad Psi|^2` when `c^2` depends on the field:
the exchange term `(1/2) integral d(c^2)/dt * |grad Psi|^2` appears on the
right-hand side of the identity and does not vanish when `c^2` moves. The
Euler-Lagrange form above cancels it exactly, so the budget holds as
written.

The alternative was to drop `E_deformation` under B4a entirely, treating
the slaved density as bookkeeping rather than a second energy. This plan
takes R2: the density has energy in every variant, and the equation pays
for it, by the `V` term above.

For the EMC density dynamics variants (item 2.4):

- **B4a (instantaneous):** the density is a function of `|Psi|^2` at each
  step, and the equation carries the extra term `-2 kappa beta_rho^2 Psi^3`
  from the deformation potential. `E_total` is conserved to numerical
  tolerance. The maximum principle holds: `rho <= rho_0`.
- **B4b (relaxation):** the `D laplacian(rho)` and `-gamma_rho(rho - rho_0)`
  terms dissipate. The budget carries a ledger entry `P_deform` for the
  rate at which the deformation energy is lost, and the check becomes
  `dE_total/dt + flux + P_deform = 0`. `P_deform > 0` means the deformation
  is dissipating; `P_deform < 0` means it is being driven. The maximum
  principle also holds here (Section 2.3): no peak forms.
- **B4c (inertial):** the density carries its own kinetic energy. The
  deformation energy becomes
  `E_deformation = integral ( (1/2) |d rho/dt|^2 / c_rho^2 + (1/2) kappa |grad rho|^2 + (1/2) kappa (rho - rho_0)^2 ) dV`,
  and the budget includes it. B4c is deferred until the extra term is added
  to the tracker. WARNING: the three terms above do not share a single
  `[kappa]`: the gradient and spring terms differ by a factor of length
  squared and `kappa` multiplies both, so it cancels between them and no
  choice of `[kappa]` makes all three energy densities. Pinning the density
  wave speed at `sqrt(kappa) * c_rho`, or redefining `c_rho`, reaches only
  the kinetic term. The formula needs a length scale, or a second
  stiffness, before the variant is implemented from it. B4c is the only
  variant in which a local peak `rho > rho_0` can form; `c_max > c_0`
  applies to B4c alone.

**Rule.** The budget enumerates every term the selected variants put in
the equation. A variant that adds a potential to the Lagrangian adds its
matching term to the stepper and its energy to `E_total`. The B6a
recommended start, for instance, adds `F = gamma_nl (1 - rho/rho_0) |Psi|^2
Psi`, which under B4a is `gamma_nl (beta_rho/rho_0) Psi^5` and carries its
own potential `-gamma_nl (beta_rho/rho_0) Psi^6 / 6`; without that term the
drift does not converge. WARNING: that potential is unbounded below, so B6a
has no ground state and a large-amplitude run can collapse rather than
converge. The term is kept on the empirical ground above; the property is
recorded here so it is a known limit of the variant rather than a surprise
in a sweep. The budget is not a fixed formula, it is the sum of the active
terms.

> **Physical reading of the unbounded potential.**
> The absence of a ground state is not a defect of the variant; it is the
> signature of the saturation mechanism described in the manuscript as the
> Onion Model. The energy of a soliton scales as `r^5` while the available
> volume scales as `r^3`; when the amplitude pushes the energy past what the
> single shell can absorb, the soliton can no longer remain single-shelled.
> In a Milestone 1 run there is no second shell to move into, so the field
> collapses; in the full theory the collapse is the point at which a
> recursive shell forms. The amplitude at which B6a loses its ground state
> is therefore a **measurable threshold**, not a numerical failure: it
> marks the capacity of a single-shell soliton at that `K`.
>
> The `r^5/r^3` disparity and its role in shell formation are derived in
> the manuscript, v5.0.2 or later, Chapter 15 "Geometric Validation: The
> Fundamental Identity and the Base AMM State (a_e)", Section 15.2
> "Physical Origin of the r^5 Scaling: Geometric Energy Density".
> DOI: 10.5281/zenodo.22875996.

### 5.3. Coupling to the soliton

The soliton interacts with the base wave only **at the WC**, through
reflection. There is no volume coupling. This preserves the locality of
the interaction and avoids the "pumping" problem: a volume-coupled base
wave would continuously inject energy everywhere, and the soliton would
either grow without bound or require an explicit damping term.

### 5.4. The vacuum layer is swappable

Energy should not disappear. But the simulation domain is finite, waves
reflect off its boundaries, and there is no obvious way to keep a
non-equilibrium steady state running forever without either injecting
energy or bleeding it. The problem is real and not resolved here.

The plan's response is to make the vacuum layer **swappable**. The
interface is fixed; the implementations are variants:

```text
VacuumProvider:
    seed(ctx)         # called once, at t = 0
    step(ctx)         # called every step; may inject or absorb
    energy_budget()   # returns what the provider contributed or removed
```

Candidate implementations, in order of increasing physical fidelity:

- **V1 — static vacuum.** `Psi_base` is set once and does not evolve. The
  soliton evolves on top of a fixed background. No energy exchange, no
  reflection problem from the vacuum side, but the background does not
  respond to the soliton.
- **V2 — passive vacuum.** `Psi_base` evolves with the wave equation but is
  never re-driven. Energy leaks through the boundary and is lost. Simple,
  but not conservative.
- **V3 — periodic box.** The domain wraps. No leakage. The vacuum is
  conserved by construction, at the cost of wrap-around artefacts when the
  soliton's tail meets itself.
- **V4 — absorbing boundary with re-injection.** Waves leaving the domain
  are absorbed; an equal flux is injected at the boundary to keep the total
  energy constant. Conservative in the budget sense, but the injection is
  artificial and can seed artifacts.
- **V5 — self-consistent vacuum.** `Psi_base` and the soliton are coupled;
  the base wave responds to the soliton's presence and the total energy is
  conserved by a Hamiltonian structure. The most physical, but also the
  hardest to implement and the most likely to be numerically stiff.

The plan starts with **V1** for testing the engine, moves to **V3** for
K-selectivity (where the wrap-around artefacts may be tolerable if the
domain is large enough), and leaves **V4** and **V5** as research targets.
Which one is physically correct is author-gated (Section 9, Q2).

Two pipeline configurations share the same field types and the same base
processors.

**Pipeline A — non-reflective.** Vacuum V1 (static), no scattering
operator, budget without `E_base`. This is the default pipeline. It tests
the nonlinear soliton as a `c(rho)` structure.

**Pipeline B — reflective.** Vacuum V3 (periodic), scattering operator
present, `E_base` in the budget. This is the optional pipeline that
realises the Yee picture: wave centres as reflectors of an incoming base
wave. `PsiInField` and `PsiOutField` are introduced as separate features in
this pipeline only.

**Capability flags.** A `VacuumProvider` exposes two flags that the
pipeline uses for compatibility checks:

```text
evolves              : bool   # base wave evolves in time
supports_reflection  : bool   # base wave can supply incoming waves
```

V1 has both `False`; V2, V3, V4, V5 have both `True`. A processor that
requires reflection (like the scattering operator) declares
`requires=(VacuumProvider, ...)` and checks `supports_reflection` in
`setup()`, raising `PipelineError` if the registered vacuum cannot support
it. This makes incompatibility a build-time or setup-time error, not a
silent no-op in the middle of a run.

Neither pipeline modifies the other. Switching between them is switching
the processor list and the registered vacuum variant, nothing else.

---

## 6. Block 1 — Engine implementation

Infrastructure only. No specific physics. Each item is a work unit.

### 1.0 — `UnitSystem` feature

- [ ] Define the `UnitSystem` protocol (fields + conversion methods).
- [ ] Implement `NaturalUnitSystem`, `OpenWaveUnitSystem`, `SIUnitSystem`.
- [ ] Add `UnitSystem` to `Pipeline.external_provides`.
- [ ] Wire `Runner.run(..., initial_features=[units])`.
- [ ] Add a linter rule: no dimensional literal in `physics/*.py`.
- [ ] Document in `README.md`.

### 1.1 — Multi-field FeatureBag

- [ ] Define `PsiBaseField`, `PsiLongField`, `PsiTransField`,
      `EMCDensityField`, `EMCFluxField` (optional) as separate features.
- [ ] Each field is a `ti.Vector.field(3, ti.f32, shape=grid)` with a
      triple-buffer variant for time integration.
- [ ] Ensure `FeatureBag` handles these as distinct types without aliasing.
- [ ] Add a test: allocate all five, write distinct values, read back.
- [ ] `PsiInField`, `PsiOutField` — optional, used only by the reflective
      pipeline (B). They carry the incoming and outgoing components of the
      longitudinal field near wave centres.
- [ ] `PsiTransField` is allocated by `AllocateWaveField` only when the
      `allocate_trans` flag is set. Pipelines that do not use the
      transverse mode leave it unallocated. The feature type stays in the
      codebase so that a future spin variant can enable it without touching
      the allocator.

### 1.2 — Trackers per voxel

- [ ] Define `TrackerFields` feature.
- [ ] Fields: `energy_long_local`, `energy_trans_local`, `amp_local`,
      `freq_local`, `rho_local`.
- [ ] Implement `TrackersUpdate` processor in `Stage.MEASURE`.
- [ ] Implement 3-plane sampling (as in the legacy `sample_avg_trackers`)
      to compute global averages without full reductions.
- [ ] Add a test: uniform field -> uniform tracker values.

### 1.3 — Multi-field evolution

- [ ] Generalise `LaplacianProcessor` to accept a field name in `__init__`.
- [ ] Generalise `LeapfrogProcessor` similarly.
- [ ] Define a coupling contract: `Psi_long -> Psi_trans` conversion at
      WCs, with a tunable coefficient.
- [ ] Add a test: two coupled fields, no coupling coefficient -> independent
      evolution; with coefficient -> energy transfers.

### 1.4 — Source terms (additive, not overwrite)

- [ ] Define the contract: a source term **adds** to `psi_new`, never
      overwrites `psi_am`.
- [ ] Implement `SeedBaseWave` — seeds `Psi_base` once.
- [ ] Implement `SourceTermInterface` — base class for additive sources.
- [ ] Implement `ScatteringOperatorInterface` — separate base class for
      operators that redistribute energy between two fields. A scattering
      operator adds to one field and subtracts from another, and records
      the exchanged amount in the budget. `SourceTermInterface` and
      `ScatteringOperatorInterface` are distinct: sources inject,
      scatterers exchange. A scattering operator is unitary by contract:
      the field magnitude that enters equals the field magnitude that
      leaves, per wave centre.
- [ ] Add a test: two sources, superposition holds.

### 1.5 — Reflector interface

- [ ] Extend `WCState` with `reflect_coeff_long`, `reflect_coeff_trans`,
      `phase_shift`.
- [ ] These are *attributes*, not yet *behaviours*. The values are set by
      the experiment, not computed.
- [ ] Document the contract clearly: a reflector is a WC that satisfies
      unitarity on `Psi_in`, `Psi_out`, `Psi_spin`.
- [ ] The scattering operator is introduced in item 2.2, variant B2d. The
      reflector interface here defines only the attributes; the operator
      that reads them is separate.
- [ ] Add a test: reflection of a plane wave from a single reflector
      preserves energy.

### 1.6 — WC motion (drift)

- [ ] Extend `WCState` with `velocity`, `force`.
- [ ] Implement `WCMotionProcessor` in `Stage.POST_UPDATE`.
- [ ] Implement `WCDriftRule` contract: a callable that returns a force
      vector given local field values.
- [ ] Provide a default rule (`F = -grad rho`) and a no-op (`F = 0`).
- [ ] Add a test: no-op drift -> positions unchanged; default drift on a
      static `rho` -> WCs move to minimum.

### 1.7 — Boundary condition

- [ ] Define `BoundaryCondition` feature: `kind` (`absorbing` | `periodic`
      | `reflecting`), `r_domain`.
- [ ] Implement `BoundaryProcessor` in `Stage.POST_UPDATE`.
- [ ] Absorbing: waves leave without reflection. Periodic: wrap.
      Reflecting: mirror.
- [ ] Add a test: wave hitting absorbing boundary leaves the domain without
      reflection, energy accounted for in `flux_boundary`.

### 1.8 — Energy budget tracker

- [ ] Define `EnergyBudget` feature.
- [ ] Fields: `E_kin`, `E_grad`, `E_deform`, `flux_boundary`, `dE_dt`.
- [ ] `E_soliton = E_kin + E_grad` with `E_kin = integral (1/2) |dPsi/dt|^2
      dV` and `E_grad = integral (1/2) c^2(rho) |grad Psi|^2 dV`;
      `E_total = E_soliton + E_deform`.
- [ ] Implement `EnergyBudgetUpdate` in `Stage.MEASURE`.
- [ ] Add a test: 1D harmonic oscillator -> `dE/dt ~ 0` to machine
      precision.

### 1.9 — Stability metrics

- [ ] Define `StabilityMetrics` feature.
- [ ] Fields: `sol_lifetime`, `localization`, `sphericity`, `freq_drift`,
      `wc_drift`.
- [ ] Implement `StabilityMetricsUpdate` in `Stage.MEASURE`.
- [ ] Add a test: static Gaussian -> `localization` stays constant;
      spreading Gaussian -> `localization` decreases.

    **`freq_drift` definition (2026-10-12).** Field-wide signal
    `s(t) = integral psi . (psi - psi_prev) dV`; upward zero-crossings
    give `f = 1 / (2 * delta_t)`. Supersedes the earlier candidate
    definitions (single-voxel probe, three-plane average), which are not
    well-defined for a symmetric seed released from rest. Three
    limitations (reflection contamination, pipeline B, longitudinal-only)
    are recorded in the `StabilityMetrics` docstring.

### 1.10 — Experiment runner

- [ ] Implement `ExperimentRunner`: takes a list of configuration dicts,
      runs each, records summary.
- [ ] Output: CSV with one row per run, columns = config + final metrics.
- [ ] Support deterministic seeds per run.
- [ ] Add a test: 3-run sweep produces 3-row CSV.

### 1.11 — Geometric constants provider

- [ ] Define `GeometricConstants` feature.
- [ ] Implement `ComputeGeometry` lifecycle processor that imports from
      `m4_7_ewt_emergence_engine.py` and populates the feature.
- [ ] Wire as `external_provides` for pipelines that need it.
- [ ] Add a test: computed `A_pi`, `eps_M`, `N_geom` match the engine.

### 1.12 — Units and conversions

This is folded into 1.0. Listed separately only for traceability.

### 1.13 — Checkpoint / restart

- [ ] Define `CheckpointProcessor` (lifecycle + periodic).
- [ ] Serialise `FeatureBag` to disk (Taichi fields -> numpy -> npz).
- [ ] Deserialise on startup.
- [ ] Add a test: run 100 steps, checkpoint, run 100 more; run 200 from
      scratch; compare.

### 1.14 — Live monitor

- [ ] Adapt `live_monitor_viewer.py` for pipeline_engine.
- [ ] Panels: energy (long/trans/emc), boundary flux, WC drift, freq.
- [ ] Reads `live.json` written by `LiveJsonSink`.
- [ ] Add a test: launch monitor, run 100 steps, monitor updates.

### 1.15 — Research logging schema

- [ ] Define the output layout: `run_meta.json`, `timeseries.parquet` (or
      CSV), `summary.json`, `events.json`.
- [ ] `run_meta.json`: config, seed, code hash, unit system.
- [ ] `timeseries`: full time series per metric, with configurable cadence.
- [ ] `summary`: final metrics for sweep aggregation.
- [ ] `events`: annihilation, boundary hits, instability detected.
- [ ] Add a test: schema validates against a JSON schema.

### 1.16 — Simulation domain configuration

This is the decision documented in Section 4. Work items:

- [ ] Add `r_domain`, `r_core` and `c_max` to `UnitSystem`; compute `c_max`
      from `rho_max`, the maximum density the EMC Wall can reach. For B4a
      and B4b, `c_max = c_0` (Section 2.3, Section 3.2). For B4c,
      `c_max = c_0 * sqrt(rho_max/rho_0)`.
- [ ] Implement the boundary condition processor (1.7).
- [ ] Document the choice: `r_domain ~ 10 lambda_nu`.
- [ ] Add a test: for K = 1, the whole soliton fits inside `r_domain`.

### 1.17 — Vacuum layer provider

This is the decision documented in Section 5. Work items:

- [ ] Define `VacuumProvider` interface: `seed`, `step`, `energy_budget`,
      and the two capability flags `evolves` and `supports_reflection`.
- [ ] Implement V1 (static, `evolves=False`, `supports_reflection=False`).
- [ ] Implement V3 (periodic, both `True`).
- [ ] Implement V4 (absorbing with re-injection, both `True`).
- [ ] V2 and V5 are deferred.
- [ ] Wire the provider as an external feature.
- [ ] Implement the conservation check excluding `E_base` in pipeline A and
      including it in pipeline B.
- [ ] Add a test: base wave alone -> `dE_soliton/dt = 0` trivially.
- [ ] Add a test: a processor that requires `supports_reflection` raises
      `PipelineError` when registered with V1.

### 1.18 — Diagnostic hooks

- [ ] Define a stop-condition contract: `StopCondition` callable.
- [ ] Implement `DiagnosticProcessor` in `Stage.MEASURE`.
- [ ] Built-in conditions: `dE/dt > threshold`, `localization < threshold`,
      `sphericity < threshold`, `max(rho) > rho_max` (CFL guard).
- [ ] Add a test: run with a forced violation -> simulation stops early.

### 1.19 — Deterministic seeds

- [ ] Add `seed` to `RunContext` (already present).
- [ ] All random initialisation reads from `ctx.run.seed`.
- [ ] Add a test: two runs with same seed within a backend -> bit-identical
      output; two runs across backends -> equal to a stated tolerance at
      the parsed-value level.

### 1.20 — Parameter sweep DSL

- [ ] Define YAML/JSON schema for sweeps: `topologies`, `spacings`,
      `couplings`, `K`, `seeds`.
- [ ] Implement `SweepRunner` that consumes the schema and drives
      `ExperimentRunner`.
- [ ] Add a test: 2x2 sweep produces 4 rows.

### 1.21 — Artifact versioning

- [ ] Hash the configuration + code state.
- [ ] Store results in `output_dir / <hash> /`.
- [ ] Provide `list_runs()` and `load_run(hash)` utilities.
- [ ] Add a test: same config -> same hash; different config -> different.

### 1.22 — Pipeline presets

- [ ] Define `make_pipeline_a(...)` — non-reflective. Registers
      `VacuumProvider V1`, no scattering operator, budget without
      `E_base`. This is the default.
- [ ] Define `make_pipeline_b(...)` — reflective. Registers
      `VacuumProvider V3`, allocates `PsiInField` and `PsiOutField`, adds
      the scattering operator (variant B2d), budget includes `E_base`.
- [ ] Both presets return a `Pipeline` instance with the fields and
      processors set. Callers may extend the returned pipeline but not
      modify the shared base processors.
- [ ] Add a test: pipeline A builds and runs without `PsiInField`;
      pipeline B builds and runs with it; a scattering operator dropped
      into pipeline A raises `PipelineError` at build time.

### 1.23 — Conservative discretisation of the variable-coefficient Laplacian

- [ ] Implement `LaplacianVariableCoeff` using the conservative stencil:
      the flux form on half-grids, with `c^2_{i+1/2} = (1/2)(c^2_i +
      c^2_{i+1})` (and similarly for `j`, `k`). This is the discrete
      variation of `E_grad = sum (1/2) c^2_{i+1/2} ((Psi_{i+1} -
      Psi_i)/dx)^2 dx`.
- [ ] Test 1: constant `c^2` -> recovers the standard 6-point Laplacian.
- [ ] Test 2: variable `c^2`, harmonic wave, flux form -> the **staggered
      leapfrog invariant** is conserved to machine precision over 1000
      steps. The staggered invariant is
      `E_stag = (1/2) |(Psi^{n+1} - Psi^n)/dt|^2 + (1/2) Psi^n . A . Psi^{n+1}`
      where `A` is the flux-form stiffness operator (the negative of
      `LaplacianVariableCoeff`). This is the quantity the leapfrog
      conserves exactly; the Section 5.2 energy `E_soliton` is not
      conserved exactly by leapfrog on any stencil and carries the
      standard O(dt^2) offset, so it is not the right test for machine
      precision. If `E_soliton` is scored instead, the bar is O(dt^2)
      convergence under refinement, not machine precision.
- [ ] Test 3: the same test with the naive `c^2_i * laplacian(Psi)` form
      fails the staggered invariant by many orders of magnitude; this is
      the discriminating test.
- [ ] The flux form is the only form used in pipeline A and pipeline B.
      The naive form is a bug.

---

**Resolved (2026-10-12).** `freq_drift` uses the field-wide
signal above (see item 1.9). `localization`, `sphericity` and the
placeholder `sol_lifetime` threshold stand as before.


## 7. Block 2 — Physics implementation

Each item is a *variant*. The engine (Block 1) is variant-agnostic; the
physics layer supplies the specific mechanisms.

### 2.0 — Soliton assembly

Before any specific mechanism, define how the pieces compose:

```text
Psi_total = Psi_base + Psi_soliton
rho(r)    = rho_0 - beta_rho |Psi_soliton|^2        (initial guess)
c^2(r)    = c_0^2 * rho(r) / rho_0
```

The soliton exists as a *fixed point* of the coupled system: `Psi_soliton`
and `rho` are mutually consistent. This composition is the foundation; all
variants below are refinements.

- [ ] Implement `SolitonAssembly` as a documented contract.
- [ ] Add a test: static `Psi_soliton`, no coupling -> no soliton, only
      dispersion.

### 2.1 — Vacuum implementation

- [ ] **V1**: static vacuum.
- [ ] **V2**: passive vacuum (leaky).
- [ ] **V3**: periodic box.
- [ ] **V4**: absorbing boundary with re-injection.
- [ ] **V5**: self-consistent vacuum (deferred).
- [ ] Recommended start: **V1** for engine tests, **V3** for K-selectivity.

### 2.2 — WC as reflector

The reflection coefficient `alpha` is **loaded from
`GeometricConstants`**, not derived. Its value is
`alpha = 1/(A_pi - eps_M) ~ 7.29733855e-03`, fixed by the geometric
derivation in the manuscript.

- [ ] **B2a**: perfect reflection, no spin conversion
      (`reflect_coeff_trans = 0`).
- [ ] **B2b**: reflection with conversion, `|Psi_spin| = sqrt(alpha) *
      |Psi_in|` (coefficient multiplies amplitude). Unitarity:
      `|Psi_out|^2 + |Psi_spin|^2 = |Psi_in|^2`.
- [ ] **B2c**: geometry-dependent reflection (local `alpha`, if variants
      warrant).
- [ ] **B2d**: scattering operator. Implements the WC as a reflector for
      the reflective pipeline (Section 5.4, pipeline B). Reads
      `PsiInField` in the neighbourhood of each wave centre, applies the
      reflection with `reflect_coeff_long` (and `reflect_coeff_trans` when
      the transverse mode is enabled), writes to `PsiLongField`, subtracts
      the corresponding amount from `PsiBaseField`, and records the
      exchanged energy in the budget. Unitarity is enforced per wave
      centre: `|Psi_out|^2 + |Psi_spin|^2 = |Psi_in|^2`. On the current
      spin-disabled configuration, this reduces to `|Psi_out| =
      |Psi_in|`.
- [ ] **B2d** (continued): integration via Strang splitting (Q10). The
      scattering operator is applied between two half-steps of the
      leapfrog, not as a post-step overwrite.
- [ ] Recommended start: **B2b** for the reflective pipeline when the spin
      channel is enabled; **B2d** with the spin channel off when it is
      not. The spin channel is added later (item 2.3, variant B3a) once
      the in/out decomposition is validated.

**Optional consistency observation (not a derivation).** The engine may
record three candidate ratios near a WC:

```text
r1 = |Psi_spin|^2 / |Psi_in|^2   (Yee's spin energy fraction)
r2 = |Psi_out|  / |Psi_in|       (amplitude reflection ratio)
r3 = |Psi_out|^2 / |Psi_in|^2    (energy reflection ratio)
```

Each is compared with the geometric `alpha`. A match is evidence that the
corresponding field quantity is what the geometric ratio describes, but
only on a variant that does not load `alpha` at the wave centre (B2c, if
implemented). On B2b the conversion is set to the loaded `alpha`, so r1
equals the loaded value by construction and r2, r3 follow from unitarity.
A mismatch for all three means the geometric `alpha` has no direct dynamic
counterpart in this engine; that is a valid observation, not a failure of
the plan.

### 2.3 — Longitudinal <-> transverse coupling

- [ ] **B3a**: conversion at WCs only.
- [ ] **B3b**: volume conversion proportional to `|Psi_long|^2`.
- [ ] **B3c**: with relaxation (`Psi_trans -> Psi_long` possible).
- [ ] Recommended start: **B3a** — local, clean, matches Yee.

### 2.4 — EMC density dynamics

- [ ] **B4a**: instantaneous (`rho = rho_0 - beta_rho |Psi|^2`).
- [ ] **B4b**: relaxation dynamics
      (`d rho/dt = D laplacian(rho) - gamma_rho (rho - rho_0) - beta_rho |Psi|^2`).
- [ ] **B4c**: inertial dynamics (full wave equation for `rho`).
- [ ] Recommended start: **B4a** for tests; promote to **B4b** for
      self-consistent solitons.

### 2.5 — Wave speed modulation

- [ ] **B5a**: `c^2(rho) = c_0^2 * rho/rho_0`.
- [ ] **B5b**: power law `c^2 = c_0^2 * (rho/rho_0)^n`.
- [ ] **B5c**: anisotropic `c(rho, grad rho)`.
- [ ] Recommended start: **B5a** — matches M4.9.

### 2.6 — Density-modulated nonlinearity

- [ ] **B6a**: `F = gamma_nl * (1 - rho/rho_0) * |Psi|^2 * Psi`.
- [ ] **B6b**: explicit profile `mod(r)` instead of local `rho`.
- [ ] **B6c**: nonlinearity in `c^2(rho)` instead of in `F`.
- [ ] Recommended start: **B6a** — matches manuscript Variant B.

### 2.7 — WC motion rule

- [ ] **B7a**: `F = -grad rho` (EMC density gradient).
- [ ] **B7b**: `F = -grad |Psi|^2` (energy gradient).
- [ ] **B7c**: `F = -grad (rho + |Psi|^2)`.
- [ ] **B7d**: `F = 0` (control).
- [ ] Recommended start: **B7a** — matches push-out.

### 2.8 — WC topology

- [ ] **B8a**: `tetrahedron_10_locked` (r1 = 1 lambda, r2 = 2 lambda).
- [ ] **B8b**: `tetrahedron_10_unlocked` (legacy r1, r2).
- [ ] **B8c**: `golden_angle`.
- [ ] **B8d**: `bcc_lattice`.
- [ ] **B8e**: `line` (negative control).
- [ ] **B8f**: `random` (negative control).

### 2.9 — WC spacing

- [ ] **B9a**: sweep spacing at fixed topology.
- [ ] **B9b**: `n*lambda` vs `(n+1/2)*lambda`.
- [ ] **B9c**: perturbation +/-10%, +/-20%.

### 2.10 — K-selectivity

The sweep runs on **vacuum variants**, not on pipeline presets. The
structural half uses V3 (conservative); the energetic half uses V2 or V4
(dissipative). Either pipeline preset (A or B) may host the sweep; the
preset chooses the processor list, the vacuum variant chooses what the
conservation check means. The two are orthogonal.

**Structural (V3, conservative).** For each K, run from three perturbed
initial conditions at matched initial energy. Measure:

- localization: does the configuration stay bounded, or spread?
- sphericity: does it stay compact?
- WC return-to-initial: after the perturbation, do the wave centres
  return to their starting configuration?
- configuration fidelity: does the final state resemble the initial
  topology, or has it drifted?

K = 10 is structurally selected if it is the only K whose configuration
survives all three perturbations.

**Energetic (V2 or V4, dissipative).** For each K, run from three
perturbed initial conditions and let the dynamics settle. Measure:

- final energy: is E(K = 10) below E(K = 9) and E(K = 11)?
- convergence: do the three seeds land in the same final state?

K = 10 is energetically selected if it has the lowest final energy and its
seeds converge.

- [ ] B10a: sweep K = 2..12 at fixed topology, spacing, coupling, on V3.
- [ ] B10b: same sweep on V2 or V4.
- [ ] B10c: K x topology sweep.
- [ ] B10d: K x spacing sweep.
- [ ] B10e: structural comparison (V3) — three initial conditions at
      matched energy.
- [ ] B10f: energetic comparison (V2/V4) — three initial conditions,
      final energies and convergence.
- [ ] B10g: perturbation sweep. For each topology and each K, sweep the
      perturbation amplitude over {1%, 2%, 5%} of the
      nearest-neighbour spacing, run three seeds per amplitude, and
      classify each wave centre as return / bounded / escape. Report the
      survival threshold per `(topology, K)` (the return / bounded /
      escape classes and the survival threshold are defined in R8,
      Section 15).

### 2.11 — Energy conservation verification

- [ ] **B11a**: measure `dE_total/dt` for isolated soliton, using the
      definition from Section 5.2 (`E_kin` without `/c^2`, `E_grad` with
      `c^2(rho)`) and including the deformation term of the active
      variant.
- [ ] **B11b**: measure boundary flux.
- [ ] **B11c**: compare stable vs unstable K.

---

## 8. What is dropped from the old implementation

The following should **not** be ported. Each is listed with the reason.

| Old element | Reason for dropping |
|---|---|
| `interact_wc_dirichlet` | Hard pin, superseded by reflector (1.5, 2.2) |
| `interact_wc_neumann` | Hard pin variant, superseded |
| `interact_wc_soft` | Additive pin, at most one source variant, not the mechanism |
| `V_MODE = 1` (pure cubic) | Prosthesis, superseded by 2.6 |
| `V_MODE = 2` (quintic) | Prosthesis, superseded by 2.6 |
| `V_MODE = 3` (double-well) | Not relevant to EWT |
| `V_MODE = 4,5,6,7,9,10` | Simplified profiles, superseded by 2.4 |
| `energy_local_aJ` with hardcoded `base_frequency` | Superseded by `EnergyBudget` |
| `compute_force_vector` (`F = -grad E`) | Superseded by `F = -grad rho` (2.7) |
| `DirichletBoundaryProcessor` (`psi = 0`) | Superseded by `BoundaryCondition` (1.7) |
| Simple cubic Laplacian | To be replaced by BCC stencil if needed |
| `seed_wave` modes 0, 1 | Kept as utilities, not central |
| `detect_annihilation` | Deferred until reflectors work |
| `select_voxels` | Already removed |

**Kept from the old implementation** (as utilities, not as core):

- Idea of flux mesh (rendering, Block 3).
- Idea of granule motion (rendering, Block 3).
- `constants.EWAVE_*` (absorbed into `OpenWaveUnitSystem`).
- `m4_7_ewt_emergence_engine.py` formulas (absorbed into
  `GeometricConstants`).

---

## 9. Open questions and working assumptions

Each entry is either an open question (author-gated, do not resolve by
inference) or a working assumption (a draft answer that can be revised as
the work progresses). Assumptions are marked as such.

### Q2. Which vacuum implementation is physically correct?

Open question. The plan offers five (`V1`-`V5`, Section 5.4) and starts
with `V1` for engine tests and `V3` for K-selectivity. The choice is a
compromise: physical fidelity against numerical tractability. Author-gated.

### Q4. What is the correct unit system for research?

Natural units are recommended for tractability. The manuscript's
predictions are in SI. The choice affects how `gamma` enters the dynamics.
Not blocking; the `UnitSystem` abstraction (item 1.0) makes the choice
revisitable.

### Q5. What is the correct definition of "stability"?

Several candidates: lifetime, localization, sphericity, frequency
stability. All are measured (item 1.9). The primary definition is
author-gated.

### Q6. Should the WC motion be continuous or discrete?

Open question. Yee's picture suggests continuous drift toward amplitude
minima; "lock-in" language suggests discrete jumps. Both are testable
(item 2.7). Author-gated. Related to item 2.7 (WC motion rule variants).
Not currently part of Milestone 2.

### Q7 (working assumption). K = 10: topological or energetic?

The two readings are distinguished by what the K-sweep can measure, and
that in turn depends on the vacuum implementation (Section 5.4).

- **On a conservative box (V3):** final energy equals initial energy by
  construction. Comparing final energies across K compares the seeds, not
  the physics, and "different seeds give different final states" is
  expected on any conservative dynamics — not a falsifier. The observable
  that does discriminate on V3 is **structural**: does the configuration
  stay localized, keep its shape, and avoid collapse under perturbation?
  If only K = 10 survives at fixed initial energy, the selection is
  structural.

- **On a dissipative box (V2, V4):** the dynamics can relax, so final
  energies and attractors are meaningful. Different seeds converging to
  the same low-energy state is evidence for energetic selection.

**Working assumption:** run the sweep on both, and let the two
observables stand as separate tests.

- Primary: structural comparison on V3 (localization, sphericity,
  WC return-to-initial after perturbation, configuration fidelity).
- Secondary: energy comparison on V2 or V4 (final energies across K,
  convergence to a shared attractor across seeds).

If the structural test shows K = 10 is uniquely stable, the selection is
topological or geometric regardless of the energy. If the energy test
shows K = 10 is the unique minimum on a dissipative box, the selection is
energetic. If neither holds, neither reading is supported by the engine
as written.

This is a working assumption, not a settled answer. Update as the sweep
runs.

### Q8 (working assumption). Does spin stabilise the soliton?

Draft: start with longitudinal-only dynamics. If K-selectivity emerges
without spin (item 2.10), spin is not necessary for the selection
mechanism. Add spin later (items 2.2b, 2.3) to see if it changes the
picture.

The rationale: the K-selectivity question is separable from the spin
question. If spin turns out to be necessary, the test in 2.10 will show
different results with and without the transverse coupling. Until then,
starting without spin keeps the first round of tests simpler.

This is a working assumption, not a settled answer. Update if the K-sweep
or the stability metrics show that spin is load-bearing.

### Q9. How is the in/out decomposition defined in 3D?

Open question, relevant to variant B2d. In 1D the decomposition is the
standard characteristic split (`d_t Psi -+ c d_x Psi`). In 3D there is no
pointwise split; three candidate schemes exist:

- Spherical harmonic projection on a small ball around the wave centre
  (accurate, expensive).
- Local gradient estimate (`Psi_in ~ (Psi - r_hat . grad Psi . Delta)/2`,
  cheap, inaccurate for wavelengths comparable to the centre size).
- Directional characteristics along the BCC axes (intermediate).

Author-gated, to be settled with a 1D toy model first and a 3D validation
second.

### Q10. Integration of the scattering operator into leapfrog

The operator is integrated by Strang splitting on the timestep:

```text
Psi(t)  ->  U(dt/2)  ->  V(dt)  ->  U(dt/2)  ->  Psi(t+dt)
```

where `U` is the free evolution (Laplacian + nonlinearity, the existing
Stage.UPDATE sequence) and `V` is the scattering operator at the wave
centres. `U(dt/2)` is the free flow over `dt/2`, which in velocity-Verlet
terms is a half kick **and** the corresponding half drift; a kick alone
advances the velocity and leaves the field where it was, so "one kick"
would give a first-order scheme. This plan means the full half-step.

This requires `LeapfrogProcessor` to expose a half-step mode, or a
separate `LeapfrogHalfProcessor`. The half-step preserves the symplectic
structure and second-order accuracy; a post-step overwrite does not.

The alternative "local acceleration modification" (adjust the acceleration
at WC voxels inside `LeapfrogProcessor`'s kernel) is equivalent to Strang
splitting to second order but is less transparent about what it does. This
plan prefers the explicit split.

Author-gated: which of the two is used, and whether the half-step warrants
a dedicated processor. Settled with the 1D toy model.

### Q11. Is the B6a ground-state threshold the K-selectivity mechanism?

Open question, and out of scope for Milestone 2 (Section 15). Milestone 2
tests structural stability and K-selectivity at fixed amplitude; the B6a
threshold is a different observable.

The B6a threshold is the amplitude at which the single-shell soliton loses
its ground state and would need a recursive shell (Onion Model) to
continue. If this threshold depends on K, and if it peaks at K = 10, then
K-selectivity may be a **capacity selection** rather than a structural
one.

The measurement: for each K-agnostic topology (golden-angle, BCC), sweep
the amplitude at fixed K, record where the ground state disappears, and
repeat for every K in 2..12. The discriminating feature is whether
`threshold(K)` has a peak at K = 10 or only a knee; a knee does not select
K = 10 over its larger neighbours.

Author-gated. Deferred until Milestone 2 has settled whether K = 10 is
structurally selected. If it is not, capacity selection is a candidate for
the source.

Related tests: Milestone 2, Section 15. Q11 asks about **capacity**
selection; R6 and R7 ask about **structural** selection. They are
complementary, not alternatives.

---

## 10. Recommended execution order

**Phase A — Engine foundation (Block 1.0-1.3)**

1.0 (UnitSystem) -> 1.1 (Multi-field) -> 1.2 (Trackers) -> 1.3
(Multi-field evolution)

**Phase B — Physics interfaces (Block 1.4-1.7)**

1.4 (Source terms) -> 1.5 (Reflector interface) -> 1.6 (WC motion) -> 1.7
(Boundary condition)

**Phase C — Measurement (Block 1.8-1.9)**

1.8 (Energy budget) -> 1.9 (Stability metrics)

**Phase D — Research infrastructure (Block 1.10-1.23)**

1.10 (Experiment runner) -> 1.11 (Geometry provider) -> 1.13 (Checkpoint)
-> 1.14 (Live monitor) -> 1.15 (Logging schema) -> 1.16 (Domain config) ->
1.17 (Vacuum layer) -> 1.18 (Diagnostics) -> 1.19 (Seeds) -> 1.20 (Sweep
DSL) -> 1.21 (Artifacts) -> 1.22 (Pipeline presets) -> 1.23 (Conservative
Laplacian)

**Phase E — Physics variants (Block 2)**

In the order 2.0 -> 2.1 -> 2.2 -> 2.3 -> 2.4 -> 2.5 -> 2.6 -> 2.7 -> 2.8
-> 2.9 -> 2.10 -> 2.11.

**Phase F — Rendering (Block 3, out of scope here)**

Port the flux mesh, granule motion, and interactive controls from the old
launcher. Only after the physics is validated in headless mode.

---

## 11. Glossary

- **EMC** — Elastic Medium Constituent. The spherical unit of the vacuum lattice.
- **BCC** — Body-Centred Cubic. The lattice geometry of the EMC arrangement.
- **WC** — Wave Centre. A point that reflects incoming waves into outgoing waves.
- **`K`** — Number of wave centres in a soliton. `K = 1` neutrino, `K = 10` electron.
- **`K^2 lambda`** — Maximum standing-wave radius of a soliton with `K` centres.
- **`lambda_nu`** — Neutrino wavelength. The fundamental length scale in natural units.
- **`rho_E`** — Energy density (high inside a soliton).
- **`rho`** — EMC packing density (low inside a soliton).
- **`N_nu,stat`** — Statutory background EMC density (undisturbed vacuum).
- **`N_nu,eff`** — Effective EMC density inside the soliton.
- **`X_eff`** — Geometric dilution factor. `X_eff = A_pi * 3 * K_WC * sqrt(2) / C_unif`,
  with `C_unif = 1/K_WC + 1 + alpha/(pi L_p)`. Converts `N_nu,stat` into
  `N_nu,eff`.
- **Push-out** — The mechanism by which `rho_E` displaces EMC, creating
  `rho < N_stat`.
- **Tail** — The far-field deficit `rho(r) -> N_stat (1 - r_s/r)`.
  Analytic; not simulated (Section 2.4).
- **`alpha`** — Fine-structure constant. Geometric value:
  `alpha = 1/(A_pi - eps_M) ~ 7.29733855e-03`. Loaded from
  `GeometricConstants`, used as the reflection coefficient at a WC. The
  dynamic interpretation (whether a field ratio coincides with this value)
  is a consistency observation, not a derivation.
- **`eps_M`** — Magnetic deficit. `1/(N_geom pi^3) ~ 1/(8 pi^7 (1 - zeta))`.
- **`A_pi`** — Geometric core of the soliton. `4 pi^3 + pi^2 + pi`.
- **`N_geom`** — Effective BCC stiffness. `8 pi^4 (1 - zeta)`.
- **`gamma`** — Nonlinear coupling. `1/eps_M`.
- **`beta_rho`** — Rate coefficient in the EMC density evolution (Section
  2.3, item 2.4).
- **`gamma_nl`** — Coupling coefficient in the density-modulated
  nonlinearity (item 2.6, variant B6a). Under B4a it contributes
  `gamma_nl (beta_rho/rho_0) Psi^5` to the equation and
  `-gamma_nl (beta_rho/rho_0) Psi^6 / 6` to the deformation potential.
- **`kappa`** — Stiffness of the EMC density deformation. Enters
  `E_deformation` as `(1/2) kappa (rho - rho_0)^2`.
- **`c_rho`** — Characteristic wave speed of the density field, used by B4c.
- **`c_max`** — Maximum local wave speed, for the CFL bound.
  `c_max = c_0` under B4a and B4b; `c_max = c_0 sqrt(rho_max/rho_0)` under
  B4c.
- **NESS** — Non-Equilibrium Steady State. The soliton's dynamical regime.
- **Reflector** — A WC that satisfies `|Psi_out|^2 + |Psi_spin|^2 = |Psi_in|^2`.
- **Feature** — A typed object stored in `FeatureBag`, keyed by its class.
- **Processor** — A stateless pipeline stage that reads and writes features.
- **VacuumProvider** — The swappable vacuum layer (Section 5.4).
- **`PsiInField`, `PsiOutField`** — optional features, used only by the
  reflective pipeline (B). Carry the incoming and outgoing components of
  the longitudinal field near wave centres.
- **`ScatteringOperator`** — a processor that redistributes energy between
  two fields. Unitary by contract. Distinct from a source term, which
  injects.
- **`VacuumProvider.supports_reflection`** — capability flag. True when
  the base wave can supply incoming waves to wave centres (V2, V3, V4,
  V5). False for the static vacuum V1.
- **`PipelinePreset`** — a named pipeline composition (`make_pipeline_a`,
  `make_pipeline_b`) that fixes the vacuum variant and the processor list.
- **Onion Model** — the recursive shell structure of the lepton hierarchy
  in the manuscript (Chapter 16). The `r^5/r^3` saturation that motivates
  it is derived in Section 15.2 of v5.0.2.
- **Nodal lock-in** — the hypothesis that the wave centres settle into
  discrete BCC nodes rather than a continuum. Open (Q6); not currently
  part of Milestone 2.

---

## 12. How to use this document

This document is a **working plan**, not a specification. It records:

- **Why** the tool exists (Sections 1-2).
- **What** the tool must express (Sections 3-5).
- **How** to build it (Sections 6-7).
- **What** to skip (Section 8).
- **What** remains unresolved (Sections 9, 15 and 16).

Update it as decisions are made. Each work item in Blocks 1 and 2 should
be promoted to a `tasks/m4_<n>_task_details.md` when it is picked up, with
pre-registered pass/fail criteria. The roadmap row in `m4_roadmap.md`
references that task document.

When a work item is complete, mark the checkbox and add a one-line note in
Section 17 (Changelog).

---

## 13. Document scope and precedence

**What this document is** — a design rationale and a work plan for the
pipeline_engine. It explains *why* the tool exists, *what* it must express,
and *how* the work is organised.

**What this document is not** — a roadmap, a task document, or a findings
note. It does not replace `m4_roadmap.md`, `tasks/m4_<n>_task_details.md`,
or `findings/`. Those documents carry the criteria, the numbers, and the
verdicts.

The correct flow for a work item is:

```text
this document  ->  m4_roadmap.md row  ->  tasks/m4_<n>_task_details.md
                (design intent)        (preview)               (the record)
                                       |
                              scripts/m4_<n>_*.py
                              data/m4_<n>_*.csv
                              plots/m4_<n>_*.png
                              findings/m4_<n>_*.md
```

When this document and a task document disagree, the task document wins.
When this document and the manuscript disagree, the manuscript wins. When
the manuscript and the model author disagree, the author wins.

---

## 14. TaskID mapping

The following TaskIDs are proposed for the roadmap. They are assigned in
creation order and are never reused. The list is a proposal until the pull
request that adds the rows; the IDs are allocated there and re-checked
against the live roadmap for collisions.

**Block 1 — Engine**

| Proposed ID | Item | Depends on |
|---|---|---|
| M4.20 | UnitSystem feature | — |
| M4.21 | Multi-field FeatureBag | M4.20 |
| M4.22 | Trackers per voxel | M4.21 |
| M4.23 | Multi-field evolution | M4.21 |
| M4.24 | Source terms (additive) | M4.23 |
| M4.25 | Reflector interface | M4.23 |
| M4.26 | WC motion (drift) | M4.25 |
| M4.27 | Boundary condition | M4.20 |
| M4.28 | Energy budget tracker | M4.22, M4.23 |
| M4.29 | Stability metrics | M4.22 |
| M4.30 | Experiment runner | M4.20 |
| M4.31 | Geometric constants provider | M4.20 |
| M4.32 | Checkpoint / restart | M4.21 |
| M4.33 | Live monitor | M4.22 |
| M4.34 | Research logging schema | M4.30 |
| M4.35 | Simulation domain configuration | M4.20 |
| M4.36 | Vacuum layer provider | M4.20 |
| M4.37 | Diagnostic hooks | M4.29 |
| M4.38 | Deterministic seeds | M4.30 |
| M4.39 | Parameter sweep DSL | M4.30 |
| M4.40 | Artifact versioning | M4.30 |
| M4.53 | Pipeline presets | M4.36 |
| M4.54 | Conservative variable-coefficient Laplacian | M4.23 |

**Block 2 — Physics**

| Proposed ID | Item | Depends on |
|---|---|---|
| M4.41 | Soliton assembly contract | M4.23, M4.24 |
| M4.42 | Vacuum implementation variants | M4.36 |
| M4.43 | WC reflector variants | M4.25, M4.41 |
| M4.44 | Longitudinal<->transverse coupling | M4.25 |
| M4.45 | EMC density dynamics | M4.21, M4.27 |
| M4.46 | Wave speed modulation | M4.45 |
| M4.47 | Density-modulated nonlinearity | M4.45, M4.46 |
| M4.48 | WC motion rule variants | M4.26, M4.45 |
| M4.49 | WC topology variants | M4.23 |
| M4.50 | WC spacing variants | M4.49 |
| M4.51 | K-selectivity sweep | M4.47-M4.50 |
| M4.52 | Energy conservation verification | M4.28, M4.51 |

IDs `M4.1`-`M4.13` are used or reserved by the existing roadmap. IDs
`M4.14`-`M4.19` are currently unassigned. The proposed assignment continues
the sequence without collision.

---

## 15. Milestone 2 — Stability and K-selectivity

Milestone 1 tests the 1-3-6 arrangement as a given initial condition and
sweeps K at fixed topology. It does not ask whether 1-3-6 is the right
arrangement at K = 10, nor whether K = 10 is the right count. Milestone 2
asks those two questions.

Milestone 2 is deferred until Milestone 1's first K-sweep (item 2.10,
B10a-B10b) has produced baseline stability results for the 1-3-6 initial
condition. Until then the tests below are specified but not run.

### Two questions, one variable each

- **Arrangement at fixed count (R6).** With K held at 10, is 1-3-6 the
  stable arrangement, and do the other arrangements item 2.8 names at
  K = 10 fail?
- **Count at fixed arrangement (R7).** With the winning arrangement held
  fixed, does K = 10 stay stable when one node is removed (K = 9) or added
  (K = 11)?

Both use the same perturbation protocol (R8). The two questions isolate
the arrangement and the count respectively; a result on one does not
decide the other.

### R6. Arrangement at K = 10: does 1-3-6 win?

Test: fix K = 10. Run each of these arrangements from item 2.8 at
K = 10 — `tetrahedron_10_locked` (1-3-6), `golden_angle`, `bcc_lattice`,
`line`, `random` (`bcc_lattice` and `random` are not built yet: B8d and
B8f) — through the perturbation protocol (R8).
Record, for each arrangement, whether the wave centres return to near
their initial positions, stay bounded, or escape.

Prediction: only 1-3-6 returns (or stays bounded). The others break under
the same perturbation.

If two or more arrangements survive equally, K = 10 alone does not select
1-3-6; the arrangement is not what matters.

### R7. Count at fixed arrangement: does K = 10 win over K = 9 and K = 11?

Test: take the arrangement that won R6 (predicted to be 1-3-6). Build the
K = 9 and K = 11 analogues of that arrangement by removing one node from
one of the shells (K = 9) and adding one node to one of the shells
(K = 11, for instance extending the outer shell to seven nodes, i.e.
1-3-7). Run each through the perturbation protocol (R8). Record, as in
R6, whether the wave centres return, stay bounded, or escape.

Prediction: K = 10 returns (or stays bounded); K = 9 and K = 11 break
under the same perturbation.

Which node is removed and which shell the extra node is added to are
implementation details; the claim under test is that any such change to
the count breaks the arrangement.

Building the K = 9 and K = 11 analogues is a new work item: the factory
(`physics/wc_factory.py`) currently refuses `tetrahedron_10_locked` at any
K other than 10. The plan records the requirement, not the specific
topology of the analogues.

Optional cross-check: if R7 holds on the winning arrangement, repeat it
on a second arrangement family (golden-angle or BCC). If K = 10 also wins
there, the K = 10 selection is arrangement-independent. If it wins only
on 1-3-6, the selection is arrangement-coupled.

### R8. Perturbation protocol

The two tests above share a single perturbation protocol.

For each configuration:

- Displace every wave centre by a random vector of magnitude `epsilon`
  around its nominal position.
- Sweep `epsilon` over a range, expressed as fractions of the
  nearest-neighbour spacing; the specific values are to be settled at
  implementation.
- Run three seeds per `epsilon`.
- Classify each wave centre at the end of the run:
  - **return**: converged back to within a small tolerance of its
    nominal position;
  - **bounded**: drifts but stays inside a small ball of radius `r_bound`
    around its nominal position;
  - **escape**: leaves `r_bound` and does not return.
- Report the fraction of centres in each class, and the `epsilon` at
  which the escape fraction crosses a stated level (for example 50%).

The specific numeric values — perturbation magnitudes, tolerance,
`r_bound`, the escape threshold — are not fixed here. Which single metric
best captures "the wave centres do not drift apart" is also open; Q5 and
item 1.9 name the candidates (`wc_drift`, `localization`, `sphericity`).
The test reports the metric that is chosen; the plan does not predefine
a threshold.

### Cross-check between R6 and R7

R6 asks whether the arrangement is special at the fixed count K = 10;
R7 asks whether the count is special at the fixed arrangement. The two
answers can differ:

- R6 selects 1-3-6, R7 does not → the selection is arrangement-driven.
- R7 selects K = 10, R6 does not → the selection is count-driven.
- Both select → the selection is both arrangement- and count-specific.
- Neither selects → K-selectivity is not a Milestone 2 outcome and the
  source must be elsewhere (Q11's capacity argument, or the spin
  extension in Milestone 3).

### Not in Milestone 2

Two questions are deliberately outside Milestone 2:

- **The excess-amplitude threshold.** The amplitude at which the
  single-shell soliton loses its ground state, and whether it depends on
  K, is a separate observable. It is Q11 in Section 9, and is out of
  scope here.
- **Nodal lock-in vs continuous drift.** Whether the wave centres settle
  on discrete BCC nodes or on a continuum is a mechanism question for the
  WC motion rule (item 2.7, Q6). It is not tested in Milestone 2.

---

## 16. Milestone 3 — Spin extension

Milestones 1 and 2 are the non-reflective and reflective pipelines
without spin (Sections 1-15). Milestone 3 adds the transverse mode back.
The plan is built so that the transverse mode can be enabled without
restructuring: `PsiTransField` already exists, the reflector interface
already carries `reflect_coeff_trans`, and item 2.3 already lists the
L<->T coupling variants. What is missing is the dynamics of the
transverse field and its interaction with the rest of the system.

This milestone is deferred, not abandoned. If K-selectivity does not
emerge in Milestones 1 and 2, or if the other criteria (spin-dependent
observables) require it, Milestone 3 becomes the next step. A possible
Milestone 4 (the Onion Model recursion) is flagged in Q11 but not scoped
here; it would add the mechanism by which a saturated single-shell soliton
transfers its excess energy into a second shell. Without that mechanism,
the B6a threshold in Milestone 1 is a signal, not a transition.

The five items below must be settled before the transverse mode is
enabled, because each one changes the stepper, the CFL bound, or the
budget in ways that are not additively compatible with the Milestone 1
configuration.

### R1. Equation for the transverse field

The transverse field needs its own evolution equation. Three candidates:

- **(a) Massless**, same as the longitudinal field:
  `d^2 Psi_t/dt^2 = c^2 laplacian(Psi_t)`. The transverse mode is a second
  propagating component. Simplest, but then the two modes are not
  physically distinguished and the split buys nothing.
- **(b) Massive**: `d^2 Psi_t/dt^2 = c^2 laplacian(Psi_t) - m^2 Psi_t`.
  The transverse mode is a bound oscillation at the wave centre. The mass
  `m` sets a natural length `1/m`, which can be tied to the soliton extent
  `r_core`. The numerical cost is an extra term in the stepper and an
  extra `c_trans` in the CFL bound.
- **(c) Damped**: `d^2 Psi_t/dt^2 = c^2 laplacian(Psi_t) - gamma d_t
  Psi_t`. The transverse mode decays; spin is a transient. Only defensible
  if the physics requires a decaying spin.

The choice determines everything else below. Author-gated.

### R2. CFL bound with a second wave speed

If `c_trans != c_long`, the timestep is computed against the larger of the
two local speeds:

```text
c_max = max over (long, trans) of local c
dt    = CFL_SAFETY * dx / (c_max * sqrt(3))
```

`UnitSystem` gains `c_trans` (and `c_trans_max` if the transverse speed
also depends on the density). The `dt` in Section 3.2 is then the same
formula with the broader maximum. This is an additive change to Milestone
1, not a replacement.

### R3. Energy budget with the transverse field

The budget gains a transverse energy term:

```text
E_trans = E_kin_trans + E_grad_trans  (+ E_mass_trans for R1b)
E_total = E_soliton + E_trans + E_deformation
check:    dE_total/dt + flux + P_deform + P_spin = 0
```

`P_spin` is the dissipation ledger for R1c (zero for R1a and R1b). The
rule from Section 5.2 applies: the budget enumerates every term the
active variants put in the equation.

### R4. Three-port scattering operator

With spin enabled, the scattering operator is a three-port device:
incoming longitudinal `Psi_in` produces outgoing longitudinal `Psi_out`
and outgoing transverse `Psi_spin`. The conversion is a 3x3 matrix `S`
with `S^dagger S = 1` (unitarity in the complex space). Whether this
matrix is also symplectic in the phase space of `(Psi, d_t Psi)` for both
fields is a separate requirement that must be verified before the Strang
splitting in Q10 generalises to three ports. This is not guaranteed by
unitarity alone and needs its own proof.

### R5. Spin from base vs spin from soliton

Two mechanisms can generate transverse energy:

- **Spin from base**: the scattering operator at the wave centre converts
  part of `Psi_in` from the base wave into `Psi_spin`. Requires
  `evolves = True` and `supports_reflection = True` (pipeline B). `alpha`
  enters as the conversion coefficient in the scattering matrix.
- **Spin from soliton**: the longitudinal field couples to the transverse
  field inside the soliton (variants B3a/B3b/B3c) without any base wave.
  Works in both pipeline A and pipeline B.

Both can operate at once, but they are distinct and must be selectable
independently. The variants in item 2.3 (B3a/B3b/B3c) cover the second
mechanism; the conversion coefficient in item 2.2 (B2b) covers the first.
When spin is enabled, the plan must state which mechanism is active in
each pipeline configuration.

### When Milestone 3 becomes active

Two signals would move the spin extension from deferred to active:

1. **K-selectivity fails without spin.** If the K-sweeps in Milestones 1
   and 2 show no unique ground state, the missing ingredient may be the
   transverse mode.
2. **Observables that depend on spin** (magnetic moment, spin quantum
   number, the full unitarity relation) require the transverse channel to
   be present for their measurement, even if they are not the target of
   Milestone 1.

The AMM does not activate Milestone 3: it is a static geometric quantity
(Section 2.7), loaded from `GeometricConstants` and not derived from the
transverse dynamics.

Absent either of the two signals, Milestones 1 and 2 are the complete tool
for the K-selectivity, structural stability, and energy-conservation
studies.

> **Reference.** The recursive shell formation (Onion Model) is derived
> in the manuscript, v5.0.2 or later, Chapter 16 "The Recursive Lepton
> Hierarchy: Nodal Shell Resonance Model". DOI: 10.5281/zenodo.22875996.

---

## 17. Changelog

| Date | Change | Author |
|---|---|---|
| 2026-09-17 | Initial draft. | Lukasz Smolinski |
| 2026-09-18 | Renamed to `M4_PIPELINE_PLAN.md`. B1: CFL bound with `sqrt(3)`. B2: item 2.13 removed; `alpha` treated as loaded geometric parameter; glossary and Section 2.7 updated. B3: kinetic term added to energy budget. Vacuum layer made swappable (V1-V5). Tail treated as analytic; wall peak not simulated. Section 4 shortened. Q1, Q3 removed. Q2 reformulated as vacuum-choice question. Q7, Q8 converted to working assumptions with drafts. Renamed `beta` to `beta_nl` / `beta_rho`. Added `X_eff`, `N_nu_eff`, `VacuumProvider` to glossary. | Lukasz Smolinski |
| 2026-09-20 | Section 4 rewritten: soliton neighbourhood simulated (`r_domain ~ 10 lambda_nu`), soliton extent `K^2 lambda` and the tail treated as analytic input. Section 2.4 header and body aligned. Section 5.2: equation stated in divergence form, dissipation ledger added for B4b. Item 2.2: coefficient multiplies amplitude; consistency observation conditional on not loading `alpha`. Item 2.10 rewritten: structural (V3) and energetic (V2/V4) tests. Q7 rewritten as two-observable test. Section 1.7 table row for `alpha` removed. Section 3.1: `r_core` labelled theoretical scale. | Lukasz Smolinski |
| 2026-09-20 | Round three. Section 1.5 and Section 5.2: equation in Euler-Lagrange form with the exchange term `c_0^2 (beta_rho/rho_0) |grad Psi|^2 Psi`; the plain divergence form does not conserve the gradient energy when `c^2` depends on the field. B4c: `E_deformation` gains the density kinetic term `(1/2) |d rho/dt|^2 / c_rho^2`, deferred until added. Section 4: `r_domain` sized by half the largest wave-centre pair separation plus a buffer, with measured numbers. Section 2.7: reference to "item 2.2, variant B2b". Section 14 preamble: IDs allocated by the author at row creation. | Lukasz Smolinski |
| 2026-09-21 | Round four. R2 applied: `E_total` carries the deformation energy in every variant; the equation gains `-2 kappa beta_rho^2 Psi^3` under B4a. Section 5.2 states the budget as the sum of the active variant's terms (B6a rule). Section 1.5 equation aligned. Section 4: `r_domain` sized by the configuration radius about its centre, with the measured values. Glossary: `beta_nl` removed; `gamma_nl`, `kappa`, `c_rho` added. Item 1.8 and item 2.11 B11a aligned with the new definition. | Lukasz Smolinski |
| 2026-09-21 | Round five. Added the reflective pipeline (B) as an optional configuration alongside the default non-reflective pipeline (A). New features `PsiInField` and `PsiOutField`; `PsiTransField` allocation is conditional. New `ScatteringOperatorInterface`, distinct from `SourceTermInterface` (sources inject, scatterers exchange). New variant B2d in item 2.2. New item 1.22 (pipeline presets, TaskID M4.53). `VacuumProvider` gains the capability flags `evolves` and `supports_reflection`, and item 1.17 is extended to test them. Budget split into pipeline A (no `E_base`) and pipeline B (`E_base` included). Sections 2.1, 2.2, 5.4 extended. Glossary updated. Q9 and Q10 added. | Lukasz Smolinski |
| 2026-09-21 | Round six. Section 3.2 and item 1.16: CFL bound computed against `c_max`, the maximum local wave speed; `c_max` added to `UnitSystem` and to the glossary. New item 1.23 and TaskID M4.54: conservative discretisation of the variable-coefficient Laplacian on half-grids, the only form used in either pipeline. Q10 updated: scattering operator integrated via Strang splitting, not as a post-step overwrite; `LeapfrogProcessor` half-step mode noted. Section 15 added: Milestone 2 (spin extension) as a deferred work package with five items to settle before the transverse mode is enabled, and two activation signals. | Lukasz Smolinski |
| 2026-09-21 | Round seven. Section 5.2: the unbounded B6a potential is reinterpreted as the physical saturation signature of the Onion Model, not a numerical failure; the amplitude at which the ground state disappears is a measurable threshold. Reference to manuscript v5.0.2, Chapter 15, Section 15.2 (DOI 10.5281/zenodo.22875996). New Q11: is the B6a threshold the K-selectivity mechanism (capacity selection)? Section 15: third activation signal removed (the AMM is a static geometric quantity, Section 2.7, not a transverse-mode requirement); possible Milestone 3 (Onion recursion) flagged. Glossary: Onion Model entry added. | Lukasz Smolinski |
| 2026-09-22 | Round eight. Milestone 2 renamed from "Spin extension" to "Nodal lock-in"; new Section 15 with tests R6 (attractor), R7 (discrete vs continuous minima), R8 (attractor count per K). Spin extension moved to Section 16 as Milestone 3. Section 17 is the changelog. Section 12 references updated. Q6 linked to Milestone 2 R7; Q11 explicitly linked to Milestone 2 as the complementary capacity-selection test. Glossary: `Nodal lock-in` entry added. | Lukasz Smolinski |
| 2026-09-22 | Round nine (review response). Section 2.10 lead-in changed from "pipeline A" to "vacuum variants"; the structural half runs on V3 and the energetic half on V2 or V4, irrespective of the pipeline preset, which is orthogonal. Section 2.3 and Section 3.2 corrected: the EMC Wall peak `rho > rho_0` arrives with B4c only; B4b obeys the maximum principle and `c_max = c_0` for both B4a and B4b. Item 1.16 aligned. Item 1.23 test 2 now names the staggered leapfrog invariant as the machine-precision quantity, and states that the Section 5.2 energy is scored by O(dt^2) convergence under refinement. Q10 tightened: `U(dt/2)` is a half kick and half drift, not a kick alone. Q11 given the turnover mechanism: capacity selection peaks at K = 10 because larger K redistributes the same energy over more centres. Comment-tier fixes: "(updated)" dropped from the Q10 heading. Applied as maintainer edits at merge: trailing newline restored (MD047); `theory/_CITATIONS.md` extended with the v5.0.2 row (DOI 10.5281/zenodo.22875996, published 2026-09-21). | Lukasz Smolinski |
| 2026-09-22 | Round ten (post-merge). Section 15 restructured: R6 split, with a cross-check paragraph; R8 moved to the topology x K grid; a new "Two independent axes" paragraph added ahead of R6a. Q11 rewritten: the prediction is stated for both topologies, and a peak at K=10 is told apart from a knee. The earlier "energy redistributed over centres" wording is removed. | Lukasz Smolinski |
| 2026-09-25 | Round eleven (restart). Section 15 rewritten around two questions, one variable each: arrangement at fixed count (R6) and count at fixed arrangement (R7), both using one perturbation protocol (R8). The previous R6a-R6d, R7 and R8 are replaced; the section is renamed from "Nodal lock-in" to "Stability and K-selectivity". The reviewer's note on the 1-3-6 K axis is addressed by removing the claim that 1-3-6 exists at any K other than 10: the K = 9 and K = 11 analogues are a new work item, and which node is added or removed is left as an implementation detail. Q11 (Section 9) restated as out of Milestone 2 scope: it is the excess-amplitude question, deferred. Item 2.10 B10g now points to R8 for the return / bounded / escape classes. Section 16 lead and activation signal widened from Milestone 1 to Milestones 1 and 2; its opening sentence updated to Sections 1-15. Glossary "Nodal lock-in" reference updated (Q6, not R7). Q6 tail reference updated. Applied as maintainer edits at merge: R6 and the Section 15 lead name the item 2.8 arrangements rather than the factory's, since `bcc_lattice` and `random` are not built yet (B8d, B8f); trailing newline restored (MD047). | Łukasz Smoliński |

---

*End of document.*
