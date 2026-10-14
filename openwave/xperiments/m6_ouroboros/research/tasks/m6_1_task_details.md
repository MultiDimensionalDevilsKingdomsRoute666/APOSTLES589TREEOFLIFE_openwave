# M6.1: The spec certification gate

> Roadmap row: [`../m6_roadmap.md`](../m6_roadmap.md) (In Progress). Feeds: M6.2 (THE DECISION GATE, pre-registers against this task's convention sheet), M6.3/M6.4 (consume the same pinned spec). Consumes: the refresh corpus ([`../../theory/_CITATIONS.md`](../../theory/_CITATIONS.md)) + the canonical ledger ([`../m6_theory_canonical.md`](../m6_theory_canonical.md) § 2/§ 4).

## TASK PLANNING

**Scope**: certify the specs the M6 program runs against, in citable form. Two arms. (a) FREEZE THE TARGET: pin the validation spec to LoE v11 (Zenodo [20357670](https://zenodo.org/records/20357670)) in one written convention sheet: the exact Lagrangian, field content, signature and units, the H functional term-by-term, the charge definition as printed, parameter values, the two candidate H/Q targets, and every notation-drift item across the record resolved into a stated convention. Each convention M6.2 needs is either FIXED-BY-PAPER (with the section cite) or FLAGGED-AS-GAP (M6.2 must derive it, no selection allowed). (b) CHARACTERIZE v4 (Zenodo [21447590](https://zenodo.org/records/21447590)) for the record: script-backed verification of what one day can check (EL equations, Hamiltonian boundedness under stated assumptions, dimensional analysis, the λ symbol collision, the m_φ 0.460 vs m_J 1.033 MeV split, the A-linearity mechanism) and a citable statement that C[φ] is unspecified, certifying the pre-analysis pin decision.

**Definition of done**:

| Arm | Testable criterion |
| --- | --- |
| a | `m6_1_v11_convention_sheet.md` exists; every M6.2-needed convention labeled FIXED-BY-PAPER (cite) or GAP (derive-only); notation-drift items from canonical § 2 each resolved or flagged; zero email-only content |
| b | `m6_1_v4_characterization.py` runs headless, emits JSON verdicts + plot(s); each caution row in canonical § 1 gets a verified/unverifiable verdict with the reason |
| both | method note per [`dev_docs/METHOD_NOTE.md`](../../../../../dev_docs/METHOD_NOTE.md); canonical § 1/§ 2 updated; adversarial audit run, verdicts recorded; doc checker exit 0 (try cap 3) |

**Gating**: user "go" ✅ 2026-07-20 22:09pm.

**Blindspot pass** (unknown unknowns surfaced):

| # | Risk | Route |
| --- | --- | --- |
| 1 | DOCX equation-extraction fidelity (the textutil trap already hit once on v4) | machine-checkable: cross-check the sheet's equations against the pandoc extraction AND the canonical § 2 lineage; note the extraction tool per equation |
| 2 | Email-only provenance reaching public docs | policy: public anchors only; the local `_PROVENANCE_NOTES.md` is never cited (privacy scoping rule) |
| 3 | "Characterize v4" sliding into refuting v4 (scope creep) | scope pin: characterization = day-checkable facts; refutation-grade claims are out of scope, route to M6.5-class work |
| 4 | Boundedness verdict depends on assumptions (λ > 0, ρ_n bounded compact support) | state assumptions explicitly in the verdict; the audit checks the assumption set |
| 5 | The physical H/Q target arithmetic assumed, not derived | derive e_nat = sqrt(4πα) in the sheet and verify 0.511/0.30282 = 1.6875 numerically in the script |

**Research body** (destinations): [`../m6_1_v11_convention_sheet.md`](../m6_1_v11_convention_sheet.md) (arm a, the M6.2 pre-registration target) · [`../m6_1_method_note.md`](../findings/m6_1_method_note.md) (the citable deliverable) · [`../scripts/m6_1_v4_characterization.py`](../scripts/m6_1_v4_characterization.py) · [`../data/m6_1_v4_characterization.json`](../data/m6_1_v4_characterization.json) · plots under [`../plots/`](../plots/) · canonical § 1/§ 2 updates ([`../m6_theory_canonical.md`](../m6_theory_canonical.md)).

**Sub-experiments**: (a1) v11 pandoc extraction + convention harvest; (a2) drift-resolution table; (b1) sympy EL + dimensional analysis; (b2) boundedness + shifted-vacuum numerics + U(φ) plot; (b3) Yukawa-range vs nuclear-radius A-linearity check; (audit) independent refutation agent over the substantive verdicts.

**Preconditions**: pandoc available (`/opt/anaconda3/bin/pandoc`, verified on v4) ✅ · corpus on disk (`theory/`, md5-verified) ✅ · model/effort: Fable 5 / high (research default; both arms are analysis-grade, no heavy compute).

## FINDINGS (2026-07-20)

**Deliverables**: [`../m6_1_v11_convention_sheet.md`](../m6_1_v11_convention_sheet.md) (arm a, the M6.2 pre-registration target) · [`../m6_1_method_note.md`](../findings/m6_1_method_note.md) (full results + equation-to-code map + audit) · canonical § 1/§ 2/§ 4/OQ6 updated ([`../m6_theory_canonical.md`](../m6_theory_canonical.md)).

### Arm (a): the v11 certification. Three structural findings, all script-verified

| # | Finding | Consequence |
| --- | --- | --- |
| F1 | **The printed EL pair is not the EL system of the printed Lagrangian** (symbolic, both signatures, residual-verified). The unique reconstruction preserving the printed interaction signs: `ℒ_ref = −¼F² − ¼G² + J·A − g(J·J)²` under mostly-plus signature (−,+,+,+), which v11 never states. Rescaling cannot repair the print: the −4g in (2.2) pins the scale | dynamics-of-record = the EL pair (what every artifact integrates); ℒ_ref + signature pre-registered in the sheet |
| F2 | **The § 5.1 production ansatz is identically zero as printed** (`r̂ × ∇φ(r) ≡ 0`) | the real configuration lives only in benchmark code; the M6.2 ansatz must be stated explicitly (sheet § 4 GAP) |
| F3 | **v11's headline arithmetic is internally inconsistent**: Table 2 scores 1.6969 vs 1.6875 as "0.30%" (arithmetically 0.557%); "Q_predicted = 0.3011 (not fitted)" = m_e/(H/Q) restated; R_phys = 191 fm needs an unprinted H_code = 0.4946; and ℏc/191 fm = 1.0331 MeV numerically equals the July papers' m_J = 1.033 MeV (identity ✅, interpretation 🔶) | the target-of-record for M6.2 is the physical 1.6875; 1.6969 comparison-only; new § 4 ledger row added |

Plus the certification core: H functional NEVER printed in v11, Q never operationally defined (and needs a time-window convention), both flagged as derive-only GAPs in the sheet's § 4 checklist, alongside the FIXED items (parameters g = λ = ω = 1, quartic `g s²`, Q_CS prefactor 1/(4π²), targets).

### Arm (b): the v4 characterization. Verified vs unverifiable, cleanly split

| Verdict | Items |
| --- | --- |
| ✅ verified as claimed | H is the Legendre transform of L (both sans C[φ]); boundedness below (λ > 0, bounded compact ρ_n); dimensional consistency; range arithmetic ℏc/0.460 MeV = 429.0 fm ≈ "~400 fm" |
| ✅ verified, weakens the claim | the "mass/range paradox" C[φ] resolves is a ≤ 2.3% effect over the paper's own 1-10 fm window (a 429 fm Yukawa IS 1/r there); A-linear energy is generic: normalization ∫ρ_n = A + long-rangedness gives E_int = gφ(0)A to ≤ 1.3% for ANY such field, incl. a standard per-nucleon Yukawa; the distinguishing physics (cross-sections) v4 itself defers |
| ❌ unverifiable as printed | the EL system (C[φ] never written; `δ_Σ` undefined); the value of φ in E_int ≈ gφA (no equation, no λ value; self-consistent in-medium minimum ≈ −34 MeV·λ^(−1/3), 74× m_φ); the legacy superrenormalizability claim (a dimensionless quartic is strictly renormalizable, not super) |

![v4 effective potential + Yukawa-vs-1/r](../plots/m6_1_v4_veff_range.png)

**Certification outcome**: the pre-analysis pin decision is certified in citable form. v11 is a real, decidable spec once the sheet's GAP items are derived and pre-registered (exactly M6.2's job); v4 as printed is not a closable dynamical system and its one derived structural claim (A-linearity) is generic. Artifacts: scripts [`../scripts/m6_1_v11_conventions_check.py`](../scripts/m6_1_v11_conventions_check.py) · [`../scripts/m6_1_v4_characterization.py`](../scripts/m6_1_v4_characterization.py), data [`../data/m6_1_v11_conventions.json`](../data/m6_1_v11_conventions.json) · [`../data/m6_1_v4_characterization.json`](../data/m6_1_v4_characterization.json), plot above.

**Adversarial audit** (cardinal rule; full record [`../m6_1_method_note.md § 6`](../findings/m6_1_method_note.md)): independent agent, own derivations + own scripts (preserved as [`../scripts/m6_1_audit_a1_el.py`](../scripts/m6_1_audit_a1_el.py) and siblings), 10 claims: **9 CONFIRMED, 1 PARTIAL** (A5: arithmetic confirmed; the July-5/8 attribution of m_J = 1.033 MeV was outside the auditor's sources, and it traced the value to the 2026-05-15 record, now recorded). The audit's break attempt on boundedness sharpened the claim (a delta-function ρ_n drives E → −∞, so v4's "any finite nucleon distribution" phrase overreaches; bounded compact support is load-bearing). Two auditor findings beyond the claims, both verified and recorded: AF1 (v4's § 3-vs-§ 4.1 contradictory A-linear derivations, volume vs surface ∝ A^(2/3)) → canonical caution 8; AF2 (v11's J·A term needs an unprinted mass² coefficient, voiding the "[g] = −4" power-counting input) → sheet § 4 μ² row + canonical § 4 ledger.

**Deviations from plan**: (1) added a second script (`m6_1_v11_conventions_check.py`) so arm (a)'s claims are script-backed too, not doc-only (within scope, strengthens auditability). (2) C6 needed two iterations to get the signature-dependent signs residual-verified (goal-loop, cap 3, closed at try 2). (3) No heavy arrays produced, so the dataset-manifest step reduces to the two tracked JSONs. (4) The auditor's 4 scripts were copied into `scripts/` under the `m6_1_audit_` prefix (scratchpad is session-local; the audit record must survive).

## TASK REVIEW (2026-07-20)

**Task Duration:** 00:31 (from 10:09pm to 10:40pm)
**Usage Cap Triggered:** NO

**Results**

| # | Result | Status |
| --- | --- | --- |
| 1 | v11 certified as the frozen validation spec: [`../m6_1_v11_convention_sheet.md`](../m6_1_v11_convention_sheet.md) pins every convention M6.2 needs as FIXED-BY-PAPER (parameters, quartic form, Q_CS prefactor, targets) or GAP (H functional never printed anywhere in v11; Q never operationally defined and window-dependent; ansatz; metric signature; implicit μ² = 1) | ✅ measured |
| 2 | The printed EL pair is not the EL system of the printed Lagrangian (symbolic, both signatures, audit-confirmed gauge-free): unique consistent reconstruction `ℒ_ref = −¼F² − ¼G² + J·A − g(J·J)²` under mostly-plus signature, which v11 never states; rescaling cannot repair it | ✅ measured |
| 3 | The § 5.1 production ansatz is identically zero as printed (`r̂ × ∇φ(r) ≡ 0`); the real electron configuration exists only in benchmark code | ✅ measured |
| 4 | v11's headline arithmetic is internally inconsistent: Table 2 scores 1.6969-vs-1.6875 as "0.30%" (arithmetically 0.557%); "Q_predicted = 0.3011 (not fitted)" = m_e/(H/Q) restated; R_phys = 191 fm needs an unprinted H_code = 0.4946; ℏc/191 fm = 1.0331 MeV = the corpus's m_J (traced to 2026-05-15; identity ✅, interpretation 🔶) | ✅ measured |
| 5 | v4 characterized, verdicts split honestly: boundedness VERIFIED (audit sharpened: bounded compact ρ_n is load-bearing, a point-source breaks it); H Legendre-consistent; EL system UNCLOSABLE (C[φ] never written); A-linear energy generic (≤ 1.3% for any long-range field given ∫ρ_n = A); the "mass/range paradox" is a ≤ 2.3% effect in the paper's own 1-10 fm window; dimensionless quartic = not superrenormalizable | ✅ measured |
| 6 | Audit bonus findings, both recorded: AF1 v4 carries contradictory volume-vs-surface derivations of its own A-linear scaling (surface ∝ A^(2/3)); AF2 v11's J·A term is dimensionally inconsistent without an unprinted mass² coefficient, voiding the "[g] = −4" superrenormalizability input | ✅ measured |

**Issues / blockers**: none. Audit verdict 9/10 CONFIRMED, 1 PARTIAL (A5: arithmetic confirmed; the July-5/8 attribution of m_J = 1.033 MeV rests on the corpus read; caveat recorded in all three docs).

**Deviations from plan**: see the log above the FINDINGS section (4 entries, all minor).

**Action needed**: M6.2 (THE DECISION GATE) is next, pre-registering against the [convention sheet § 4](../m6_1_v11_convention_sheet.md) checklist; user "go" gates it.

**Findings**: M6.1 certified the frozen v11 spec in citable form and the certification itself produced results: the printed Lagrangian, EL pair, ansatz, and dimension assignments of v11 are mutually inconsistent as printed (four script-verified print-level defects, now in the canonical § 4 ledger), so the spec of record is the EL pair plus the M6.1 reconstruction, and every quantity M6.2 needs that the paper never defines (H, Q, ansatz, signature, μ²) is now an explicit derive-only pre-registration item. v4's one derived structural claim (A-linearity) is generic bookkeeping, its dynamics unclosable as printed, and its boundedness claim is the one item that survives verification cleanly.

**Research docs created / updated**: this task_details · [`../m6_1_v11_convention_sheet.md`](../m6_1_v11_convention_sheet.md) · [`../m6_1_method_note.md`](../findings/m6_1_method_note.md) · [`../m6_theory_canonical.md`](../m6_theory_canonical.md) (§ 1 cautions 3/4/6/8, § 2 v11 row + reading rule, § 4 new ledger row, OQ6 ✅) · [`../../__M6_model_briefing.md`](../../__M6_model_briefing.md) (roadmap row) · [`../m6_roadmap.md`](../m6_roadmap.md) (M6.1 → Done) · scripts [`../scripts/m6_1_v11_conventions_check.py`](../scripts/m6_1_v11_conventions_check.py), [`../scripts/m6_1_v4_characterization.py`](../scripts/m6_1_v4_characterization.py), audit `../scripts/m6_1_audit_*.py` · data [`../data/m6_1_v11_conventions.json`](../data/m6_1_v11_conventions.json), [`../data/m6_1_v4_characterization.json`](../data/m6_1_v4_characterization.json) · plot [`../plots/m6_1_v4_veff_range.png`](../plots/m6_1_v4_veff_range.png)
