# M8.8: Independent-method reproduction of the M8.3 torsion closed forms

> Roadmap row: [`../m8_roadmap.md`](../m8_roadmap.md). Status: ✅ DONE (2026-08-22, closeout complete
> with the author's provenance layer, [#459](https://github.com/openwave-labs/openwave/pull/459)); § 8 category `convention difference`; record:
> [`../findings/m8_8_adjudication_record.md`](../findings/m8_8_adjudication_record.md).
> Protocol author: the model author (2026-08-02); implementer: a fresh context
> (commission 5, [history](../m8_8_cleanroom/COMMISSION_HISTORY.md)).

## Why this task exists

[M8.3](m8_3_task_details.md) ✅ landed the mass-formula reproducer and corrected a defect in
the published page. Its method note lists one claim it does not verify: the corrected
Reidemeister-torsion closed forms rest on a **single implementation**, since the script and the
mode-identity-theory artifact use closely related rather than disjoint methods
([`m8_3_method_note.md § 4`](../findings/m8_3_method_note.md)).

That obligation was recorded as "queued (M8.5)". The
[M8.5-A protocol § 0](../findings/m8_5a_reproduction_protocol.md) then placed it outside both
M8.5 sub-deliverables, which left the two documents pointing at each other with no task owning
the work. This row closes that loop; the scope statement below is the one both documents now
point at.

## Scope (stub level)

| Piece | Content |
| --- | --- |
| Target | the corrected torsion closed forms: the irrep forms, both Galois ratios, both sector products. `T^2(R0) = 1` is carried as a declared convention rather than a gated form (see the 2026-08-03 section), matching [`m8_3_method_note.md § 4`](../findings/m8_3_method_note.md) |
| Method | disjoint from [`m8_3_mass_reproducer.py`](../scripts/m8_3_mass_reproducer.py) and from the mode-identity-theory artifact; the overlap is disclosed, not assumed absent |
| Not in scope | the mass comparison itself (M8.3 verified its arithmetic), and the dead-zone entries' physical status (open on the source page) |
| Precedent to follow | the M8.5-A shape: gates that can go red, a coverage-enforced mutation harness, an explicit list of what is not verified |

**The implementer must be a fresh context** (author direction, 2026-07-30). Whoever runs this
may not be the context that produced the M8.3 computation, on the same reasoning that shaped
M8.5-A: a context holding the closed forms and their derived fixtures cannot serve as its own
reproducer however separately the second implementation is written. The owner therefore stays
deliberately unassigned rather than defaulting to the nearest available context. Protocol
authorship can be assigned later without compromising the reproduction, and nothing on the
dynamics path waits on either.

## Protocol authorship and group input (2026-08-02)

The author took the protocol half of this task
([#405 comment](https://github.com/openwave-labs/openwave/pull/405#issuecomment-5159525049),
2026-08-02), on the M8.5-A terms: the answer-holding author writes the reproduction protocol,
the maintainer reviews and freezes it, and a fresh context implements under the resulting
firewall. Three maintainer calls were made with the go:

| Call | Decision |
| --- | --- |
| Protocol authorship | Go. The stub already provided for assigning it without compromising the reproduction |
| Group input | The audited M8.5-A raw generator packet ([`../data/m8_5a_packet.json`](../data/m8_5a_packet.json)) may serve, confirmed to contain no derived data relevant to the torsion target (raw `(a + b*phi)/2` quaternion generators, minimal polynomial, basis, format tag only). Condition: the M8.8 protocol names the packet by its published hash and declares its own forbidden-inputs list, and the packet audit is RE-RUN against that list at freeze, not inherited from the [M8.5-A audit record](../data/m8_5a_packet_audit.json) |
| Timing | Protocol drafting begins on the author's schedule; if its review ever lands together with the M8.5-B implementation review, B takes precedence |

The M8.5-A structural claim ceiling applies unchanged: the torsion closed forms are published
on the source page, so prior corpus exposure cannot be excluded for an AI implementer, and
isolation buys provenance rather than the label.

## Construction input: the second packet (2026-08-03)

Pre-draft recon raised a second input-boundary question
([#402 comment](https://github.com/openwave-labs/openwave/pull/402#issuecomment-5166892675),
2026-08-03). The M8.5-A packet pins the group, but a combinatorial torsion calculation also needs
the 3-cell: a balanced presentation gives a 2-complex with `chi = 1` while the closed orientable
quotient has `chi = 0`, so Fox calculus supplies `d1` and `d2` and the torsion product still
consumes `d3`, which requires the identity among relations or an equivalent resolution.

| Call | Decision |
| --- | --- |
| Construction packet | Go. A second public packet carrying a based cellular chain complex or a truncated periodic `Z[2I]`-resolution, boundary maps in abstract generators explicitly matched to the M8.5-A quaternion generators, carrying no evaluated irreducible matrices, determinants, torsion values, ratios, products, or target forms |
| Reference-allowance alternative | Declined, on the precedent that already declined a web allowlist for M8.5-A: the literature carrying the period-4 resolution for this group carries the torsion formulas with it, so an allowance re-opens the path the firewall exists to close |
| Packet audit | Maintainer-side, independent, and mechanical, run from the packet alone, per the [M8.5-A § 4 rule](../findings/m8_5a_reproduction_protocol.md) that the author knows the answers and the audit is the guard against author-side disclosure. Any author-side verification artifacts ship in a separate archive that stays outside the room and is set side by side afterwards, as in [M8.5-A](m8_5_task_details.md) |
| Packet roles | The construction packet is public before the run because it is permitted input; the canonical answer packet stays quarantined until commitment because it is only an adjudication reference |
| Claim | Narrows as the author states: an independent reproduction of the torsion calculation, not an independent derivation of the supplied model. The supplied complex is verified rather than trusted, since `d d = 0`, the rank and `chi` census, the integral homology of a `Z`-homology 3-sphere, and per-irrep acyclicity are all gates that can go red |

**Why the disjointness is stronger than it looks.** M8.3 computed the torsions analytically, from
the spectral-zeta definition (`log T^2 = zeta'_coexact(0) - 2 zeta'_scalar(0)`, the Ray-Singer
combination on `S^3/2I`), not from any chain complex. Nothing in a construction packet was an
input to M8.3, and the equality of the analytic and combinatorial routes is the Cheeger-Müller
theorem rather than a shared construction, so a disagreement is ASSESSABLE instead of
unresolvable.

Assessable is not the same as attributable, and the protocol's § 1 is the stricter reading. A
mismatch is assessed against a structured diagnostic partition of four preregistered branches:
an implementation error in one route, a convention-bridge mismatch, a failed hypothesis of the
theorem, and a supplied-model or provenance error. Each branch carries its own gate, every branch
its evidence does not exclude is reported, and no unique attribution is forced. The fourth is
bounded rather than excluded, since the packet is author-supplied and the model gates establish
that the complex behaves correctly without identifying which model it is; the maintainer-side
packet audit and the maintainer-held provenance record sit beside them for that reason.

Two protocol points settled before drafting, to keep them out of the freeze review:

| Point | Content |
| --- | --- |
| Normalization anchor | Combinatorial torsion is pinned only once the basing is pinned. The packet supplies that, but the correspondence to M8.3's analytic normalization still needs one declared anchor. M8.3 fixed the overall sign once on the `R7` closed form and declared it, leaving the rest genuine checks; the protocol declares its anchor the same way and before the run |
| The trivial representation | `T^2(R0) = 1` is a declared convention in M8.3, not a gated result, because the twisted complex is not acyclic for the trivial representation. The same obstruction appears in the combinatorial route, so `R0` is carried as convention there too rather than counted as a reproduced form |

**Gated by**: M8.3 ✅ (2026-07-28) and an owner. The sign convention is fixed once on the `R7`
closed form and declared, so the remaining forms are genuine checks rather than circular
([`m8_3_method_note.md § 4`](../findings/m8_3_method_note.md)).

## Protocol and construction packet landed (2026-08-11)

The author filed both halves as a single pull request,
[#408](https://github.com/openwave-labs/openwave/pull/408), merged 2026-08-11:
[`m8_8_reproduction_protocol.md`](../findings/m8_8_reproduction_protocol.md) and
[`m8_8_construction_packet.json`](../data/m8_8_construction_packet.json). The merge is not the
freeze: § 12 binds from the § 8 lock commit, which has not been made.

**Maintainer verification, run independently of the packet audit.** The review rebuilt the
complex from the group packet and the construction packet alone: the 120-element closure from the
two packet generators, the enumeration digest reproduced from the declared sort key, `d2` against
the Fox jacobian of the two declared relators, `d d = 0` over `Z[2I]`, the augmented homology, the
exact ranks, and exact maximal minors of determinant ±1 in all three degrees. 35 gates, each
mutation-tested so a green result is not a check that cannot fail. No torsion value was computed
or evaluated at any point, so nothing in the review can become target material in the base the
clean room opens from.

**The § 9 gap, and its fix.** The universal-cover gate stated its conclusion in all four degrees
while naming an establishment procedure covering degree 2 alone (`im d3 = ker d2`), leaving
degrees 0 and 1 resting on the exact ranks, which are the rational statement the row itself warns
is blind to finite index. The gap is reachable. Scaling one row of `d2` and the COMPLEMENTARY
column of `d3` by the central non-unit `2 - z` preserves `d3 d2 = 0` (each term of the two-term
product picks up exactly one factor), has augmentation 1 so nothing computed through `eps` moves,
and acts invertibly on every irrep, so it passes every model gate as written while `H1(C_*)`
acquires order `3^60`, the determinant of multiplication by `2 - z` on `Z[2I]`. The merged gate
now requires an exact saturation certificate for `im d1`, `im d2` and `im d3`.

**What the existing audit already rejects.** Run against that mutant,
[`m8_8_packet_audit.py`](../scripts/m8_8_packet_audit.py) FAILS A10 (each `d2` row must be the Fox
jacobian of its declared relator) and PASSES A11, so the maintainer side already catches this
construction, by provenance rather than by lattice certificate. An A12 mirroring the widened § 9
in `im d1` and `im d2` is available hardening, not a repair.

⚠️ **The `2 - z` example above is WRONG, and the correction is below.** It is left standing
because it is what review sent the author and what the merged § 9 analysis cell now carries.
The gap it was offered as evidence for is real; the construction is not evidence for it.

## Correction: the § 9 example does not reach the homology (2026-08-11)

Adding A12 to the audit surfaced it. The mutation was written to make A12 go red and A12
stayed GREEN, so either the new check or the old claim was wrong. It was the old claim.

| Claim | Status |
| --- | --- |
| Scaling one `d2` row and the complementary `d3` column by `2 - z` preserves `d d = 0`, the augmentation, and per-irrep acyclicity | ✅ holds, measured |
| `det` of multiplication by `2 - z` on `Z[2I]` is `3^60` | ✅ holds, and it does appear in individual maximal minors |
| Therefore `H_1(C_*)` acquires order `3^60` | ❌ FALSE |

`d2` has rank 121 of 240, and `ker(d2)` absorbs the factor: the image lattice is unchanged,
so the homology is unchanged. Two independent measurements, one from the audit's unit-pivot
certificate and one from a separately written elimination: rank over `F_3` is 119, 121, 119,
exactly the rational ranks, for the mutant as much as for the packet. No 3-torsion anywhere.

**Why review got it wrong.** The review-side check tested ONE maximal minor, at pivot
positions taken from the baseline, and read `|det| != 1` as "not saturated". That inference is
invalid in that direction: saturation is the gcd over ALL maximal minors, so `|det| = 1`
proves saturation and `|det| != 1` proves nothing. The minor it happened to test was `3^60`,
which is why the number looked confirmatory. The audit's `saturation_certificate` clears the
same matrix with 121 unit pivots, which is a proof rather than a sample.

**The gap is real, and here is a construction that reaches it.** Scale ALL of `d2` by the
central non-unit `6 - 5z`. Augmentation 1, so the trivial sector does not move; central, so
every chain relation survives; invertible in every irreducible, so acyclicity does not move.
It acts as 11 on every faithful irreducible, so A7's prime list `{2, 3, 5, 7, 10007}` cannot
see it: mod 3 the ranks are still 119, 121, 119. Mod 11 the rank of `d2` falls to 61 from 121,
so `H_1` carries 11-torsion and the complex is not the one of `S^3`. A4, A5, A6, A7, A8 and
A11 all stay green; A12 is the check that reddens. This is the exact degree 1 analogue of the
`d3 -> 11 d3` case that made A11 load-bearing one degree up.

So the widened § 9 gate is justified, by this construction rather than by the one review
gave. What needs correcting is the EXAMPLE in the § 9 analysis cell, not the gate.

Two further changes landed. § 4.4's `convention_map` row, whose "the evaluation convention"
phrasing had produced a real defect, now names four explicit items and states that the § 4.2
basing reference and the `basing.evaluation` declaration are distinct, neither substituting for
the other. And a new § 4 paragraph makes implementer ineligibility permanent for any context
exposed to the target-source records or to the answer packet, no teardown or fresh prompt
restoring it.

**Open at landing**, all inside the pre-lock window where in-place edits are still legal:

| Item | State |
| --- | --- |
| § 11 pins | five read `[PIN at landing]`; four are maintainer-derivable and were supplied at review, the answer-packet hash being the author's to record |
| § 10.3 packaging | "one document, one merge", with the audit artifact entering the same pull request at step 9, no longer fits: the audit landed ahead of the protocol and the protocol has now merged, so the run's later commits need a stated home |
| § 5.5 separation | confirmed at review rather than deferred to it: the `(dim, chi(s), chi(t), chi(st))` row signature separates all nine irreps, with `chi(t)` load-bearing (7 of 9 without it) and margin on the other two |

The first two closed the same day, below. The third needed nothing.

## Pre-lock cleanup: the pins filled, the packaging clause corrected (2026-08-11)

[#430](https://github.com/openwave-labs/openwave/pull/430) merged 2026-08-11, protocol text
only across three commits and two review rounds. The protocol is `a6730e82…` at the merge;
both packets are untouched, so `df00c022…` and the answer packet's `adjudicates` commitment
stand.

| Change | Content |
| --- | --- |
| § 11 filled | five pins. Four maintainer-derivable values recomputed at the head, the answer-packet hash the author's to record. The method-note row was reworded as well as filled, since the "verification record" it named is not a separate artifact: M8.3's verification is the § 3.2 gate results and the § 5 audit record, inside the note |
| § 11 drafted-against | `a0c33e56`, the parent of the `d866b0d9` that created the file, rather than #408's base. Verified an ancestor of `main`, so the pin resolves in this repository and not only in a fork |
| § 10.3 rewritten | the run's artifacts MAY land across separate commits or pull requests, and merge order need not match § 8 execution order. Binding is by the hash commitments and manifests § 8 requires, never by co-location, and § 8's ordering is explicitly untouched |
| referent sweep | with the single-pull-request clause gone, four definite references lost their antecedent (§ 8 steps 1 and 2, § 10.3, § 12). All four repaired; the two survivors are generic mass nouns |
| § 12 corrected | "the pinned paths of § 11" had no referent in any of the eight versions of the file, § 11 having never carried a path. Now the pinned VALUES may not change after the lock commit, with renaming or relocating a pinned artifact explicitly not a breach and substituting one explicitly a breach |

**Why the § 12 word was worth a round before the lock.** A defect deferred past the lock
becomes a dated addendum, but anything cosmetic deferred past the lock becomes impossible,
since the fix would be an in-place edit and § 12 forbids those outright. The same asymmetry
took the two over-long lines the in-place edits had left; the file returned to the long-line
profile it merged with.

**Method note on the last round**, since a rewrap and a content change arrived in one commit.
The check was mechanical rather than by reading: both versions unwrapped into blocks, holding
fences and table rows verbatim, then diffed. Exactly one content block differed, and the
structural census was identical across the two heads. One measurement in the thread counts
lines in BYTES; in characters the prose count is four rather than six, the two that drop out
being 93 and 91 characters made long by `∂` and subscript digits at three bytes each.

## Adjudication, § 8 steps 6 to 9: reproduced under the global inverse (2026-08-22)

The full record is [`../findings/m8_8_adjudication_record.md`](../findings/m8_8_adjudication_record.md);
this section is the task-side summary and the sequence as it happened.

| Step | What happened | Where |
| --- | --- | --- |
| 6 | the author delivered the packet ciphertext on an orphan commit of the fork (`9a0d3fd5`, ciphertext SHA-256 `6e0dea53…`, armored age, one X25519 stanza); decrypted by the maintainer alone; plaintext SHA-256 `744c7f25…` = the § 11 pin, 12088 bytes, canonical form unchanged | [#408](https://github.com/openwave-labs/openwave/pull/408) thread |
| 7, attempt 1 | the committed harness (`ea3452d3`) REFUSED before applying the indexing map: the packet's `source_domain` is `packet_rows_canonical_position`, the harness accepted only the [#453](https://github.com/openwave-labs/openwave/pull/453) placeholder `answer_packet.rows`. § 8 category `structural failure`; nothing past the gate executed | [`../data/m8_8_adjudication_attempt1_refusal.json`](../data/m8_8_adjudication_attempt1_refusal.json), `46be3d08…` |
| repair | [#457](https://github.com/openwave-labs/openwave/pull/457): the literal replaced (old spelling refused, C3k), the terminal printer extracted (C17), self-test 98/98, both controls redden; attempt 1's disposition fixed in the commit message before the official run on `main` and before any category was disclosed, at the author's request (the maintainer's branch-side run had already executed); merged `a3ae231d` | [#457](https://github.com/openwave-labs/openwave/pull/457) |
| 7 and 8, attempt 2 | the official run on `main`: map applied, convention map validated, `R7` selection = GLOBAL INVERSE, 8/8 rows equal in `Q(φ)`, 4/4 identities equal, sector coverage 8/8. § 8 category `convention difference`, a success | [`../data/m8_8_adjudication.json`](../data/m8_8_adjudication.json), `a6036744…` |
| control | `ea3452d3` + the one-string substitution writes the byte-identical record, then dies on the `ea3452d3` printer defect: the rerun's result is the one-string correction alone | [`../scripts/m8_8_control_byte_identity.py`](../scripts/m8_8_control_byte_identity.py) |
| 9 | answer packet `744c7f25…` and the construction-audit artifact `d5bb04b9…` (held since 2026-08-11 on a maintainer-side orphan commit) published beside both attempt records, each verified against its frozen hash | [`../findings/m8_8_adjudication_record.md`](../findings/m8_8_adjudication_record.md) |

**What the category means.** `convention difference` is not a caveat on the agreement: it
is full agreement under the opposite native orientation, the two categories disjoint and
both successes by the frozen § 8 table, with the orientation recorded. The implementer's
§ 5.4 declared orientation and the packet's differ by the global inverse at `R7`, the
selection rule resolves it, and every value then matches exactly.

**Governance, recorded rather than amended.** The protocol did not address comparator repair
after a post-reveal structural refusal. The record states the gap, the three facts that made
this one repair acceptable (replacement literal frozen pre-reveal by the author's builder,
attempt 1 stopped before any value comparison, mutation-backed semantic nonmovement), and
that it is the last such repair: a second packet-facing incompatibility would have stopped
the run. No § 11 pin and no protocol text changed; § 12 carries no addendum for it.

**Provenance of the seam.** The refused string was the author's builder's own, frozen
pre-reveal; the accepted one was a maintainer placeholder. The author's reading on #457 is
adopted: the seam belongs to the interface between the two sides, since the #451 answer gave
the destination literal and only prose for the source. The `p2_schema.py:205` pin is
author-asserted until the builder bytes published in #459; the record says so.

**Author layer, published ([#459](https://github.com/openwave-labs/openwave/pull/459)).** The provenance archive plaintext (hash on the #408
thread, ciphertext `2ba72660…` at tag `m8.8-provenance-02`) at `data/m8_8_provenance/`, and
the builder bytes behind the `p2_schema.py:205` pin at `m8_8_answer_builder/`; the chain
regenerates the § 11 packet pin from the pinned sources. Nothing is left outstanding.

## DEVIATIONS LOG

| Date | Deviation | Disposition |
| --- | --- | --- |
| 2026-08-22 | post-reveal comparator repair (#457) after the step-7 refusal; not contemplated by the frozen protocol | accepted under three recorded facts, attempt 1 kept as `structural failure`, last such repair; [record](../findings/m8_8_adjudication_record.md) |

## FINDINGS

| # | Finding | Evidence |
| --- | --- | --- |
| 1 | The M8.3 torsion closed forms are reproduced by a context-isolated independent-method run from a based chain complex, § 8 category `convention difference` (global inverse at `R7`, 8/8 rows and 4/4 identities exact in `Q(φ)`). The supplied topological model was verified, not independently derived; the § 2 ceiling applies | [`../data/m8_8_adjudication.json`](../data/m8_8_adjudication.json) `a6036744…`; [record](../findings/m8_8_adjudication_record.md) |
| 2 | The pre-reveal harness failed closed on a one-string interface mismatch (attempt 1, `structural failure`); the repair moved no record byte, shown by a control reproducible from public objects | [`../data/m8_8_adjudication_attempt1_refusal.json`](../data/m8_8_adjudication_attempt1_refusal.json) `46be3d08…`; [`../scripts/m8_8_control_byte_identity.py`](../scripts/m8_8_control_byte_identity.py) |
