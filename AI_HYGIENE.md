# AI Hygiene: Working with Automated Intelligence in OpenWave

> OpenWave is an AI-accelerated research platform: language-model assistants write lattice code, scan literature, check derivations, run parameter sweeps, and draft internal documentation. That leverage is real, and so are the failure modes. This page is the working contract that keeps the science **human-owned** and the record **trustworthy**: what AI is for here, what it must never be trusted with alone, and the concrete habits that keep model-generated errors out of the physics record.
>
> It is tool-agnostic (it applies to any assistant, chatbot, coding agent, or pipeline) and person-agnostic (it describes practices, not people). If you contribute to OpenWave with AI assistance, and most contributors do, this is the etiquette.

## Contents

| Section | What it covers |
| --- | --- |
| [1. The stance](#1-the-stance) | one paragraph: instruments vs authors |
| [2. Do / Don't quick reference](#2-do--dont-quick-reference) | the rules at a glance |
| [3. Division of labor](#3-division-of-labor) | what models do well vs what only humans can supply |
| [4. Failure modes](#4-failure-modes) | the seven ways AI quietly corrupts a research record |
| [5. Safeguards already in force](#5-safeguards-already-in-force) | repo standards that operationalize this page |
| [Details](#failure-mode-details) | anchored deep dives, one per failure mode, at the doc tail |

## 1. The stance

AI is an **instrument**, like the lattice itself: it multiplies throughput and it measures nothing on its own authority. Humans are the **authors**: every physics claim published from this repo is owned by a person who can defend it without the assistant in the room. The practical consequence is a single rule that generates most of the others:

> **A model's output is a draft or a hypothesis, never a result. It becomes a result only when it is verified by something that is not a language model: a derivation checked by hand, a script anyone can run, a measurement on the lattice, or the explicit confirmation of the human who holds the relevant authority.**

And its enforcement mechanism, a **CARDINAL RULE for anyone (human or agent) working in this repo** (2026-07-05):

> **THE ADVERSARIAL AUDIT: every substantive derivation, verification, or headline claim gets an INDEPENDENT adversarial audit before it is trusted, recorded as a result, or sent outside.** The auditor (a second agent or a second person) is instructed to REFUTE, not confirm: its own implementation (different method, different seed, different construction: e.g. finite differences where the original used an exact identity), its own hand re-derivations, an explicit hunt for overclaims and missing caveats, and a verdict per claim (CONFIRMED / REFUTED / QUALIFIED) backed by its own numbers. Every catch is folded back into the artifact, and the audit outcome is recorded IN the deliverable: the audit record is part of the rigor surface. Origin: the model owner's own advice ("careful small steps, maybe multiple agents verifying each other", Duda 2026-07-03). Proof it works: the first real catch, M5.18 (2026-07-05), where the audit confirmed 5 of 6 claims, refuted an overclaimed witness whose conclusion survived only through the auditor's corrected construction, and found a vacuum-manifold branch structure the original missed entirely ([`m5_18_verification_note.md § 10`](openwave/xperiments/m5_liquid_crystal/research/findings/m5_18_verification_note.md), the canonical record-the-audit pattern).

## 2. Do / Don't quick reference

| ✅ Do | ❌ Don't |
| --- | --- |
| Ground the assistant in the **full repo** (code, docs, source papers) before asking it research questions | Ask a context-free chatbot to answer research questions from a summary or an email thread ([why](#context-asymmetry-detail)) |
| Treat AI-derived derivations as **evidence to verify**: re-derive by hand, or test on the lattice | Treat fluent, confident output as settled ([why](#hallucination-detail)) |
| Answer **intent and provenance** questions from your own memory, notes, or records | Let a model answer "what did the author mean" on anyone's behalf, including your own past self ([why](#authority-laundering-detail)) |
| Prefer questions a model can fail at: "derive X and show the steps", "find the sign error" | Ask questions that only mirror your own framing back ("is my idea good?") ([why](#mirror-trap-detail)) |
| When relaying a collaborator's question to an assistant, send the **underlying artifacts** (papers, scripts, data) | Chain model outputs into other models as if information were being added ([why](#relay-drift-detail)) |
| Publish only **human-owned, script-backed** claims; disclose AI assistance where venues ask | Post model-generated physics text to research venues, preprint servers, or mailing lists as if human-authored ([why](#publication-slop-detail)) |
| Write outbound scientific communication in your **own voice**; use AI for checking and organizing | Send collaborators raw model output as your reply |
| Record AI-assisted findings with their verification status attached ("re-derived by hand", "confirmed by script X") | Let unverified model text age into the record until it reads like an established result |
| Keep public comparisons **per-criterion and artifact-linked** (the [`MODELS.md`](MODELS.md) pattern: one criterion, one status, one runnable link per cell) | Publish aggregate self-ranking ("further along than any other program"), cross-program scoreboards settled by prose, or headlines whose conditions live in an appendix ([why](#publication-slop-detail)) |
| Run the **adversarial audit** (cardinal rule, § 1) on every substantive claim before trusting or sending it: independent refuter agent, own script, verdict per claim, outcome recorded in the deliverable | Ship a derivation or verification on the strength of the agent that produced it, however green its own checks look |

## 3. Division of labor

The split is by **kind of knowledge**, not by difficulty. Models are strong wherever the ground truth is already written down somewhere or can be computed; humans are irreplaceable wherever the ground truth lives in a person.

| Models do this well (let them do the heavy lifting) | Only a human can do this |
| --- | --- |
| Symbolic derivation checking, algebra verification, dimensional analysis | **State intent**: which equation, convention, or ansatz an author actually meant |
| Writing and refactoring lattice / analysis code; building test suites | **Hold provenance**: where a number came from, what a past document was based on |
| Exhaustive reduction scans ("try all six ansaetze × both conventions") | **Exercise physical intuition**: which direction smells right before any computation exists |
| Literature triage, citation gathering, cross-referencing a large corpus | **Own a theory**: extend, retract, or re-postulate its assumptions with authority |
| Drafting internal docs, reports, and reproducible method notes | **Endorse**: put a name behind a claim to the community |
| Bookkeeping: trackers, cross-links, changelogs, consistency sweeps | **Decide priorities**: what is worth measuring next and what the program is for |
| Finding sign errors, dropped factors, and convention mismatches in published algebra | **Confirm a bug in one's own work** (a model can flag it; only the author can confirm it) |

Two consequences worth making explicit:

1. **Author-gated questions stay author-gated.** If a question is of the form "which form did you intend", "is this the number you meant to publish", "how do your variables map to ours", no model output can close it. Route such questions to the person, keep them as small as possible (one item per ask), and mark them unresolved until the person answers.
2. **Measurable questions should be measured, not asked.** If a question can be settled by a computation or a lattice run you can do yourself, do that and share the result. It is faster, it is verifiable by anyone, and it converts a request for someone's time into a gift of information.

## 4. Failure modes

Seven patterns account for most AI damage to research records. Lean table here; mechanics, symptoms, and countermeasures in the [anchored details](#failure-mode-details).

| # | Failure mode | One line | Detail |
| --- | --- | --- | --- |
| 1 | Hallucination | fluent, confident, wrong; worst on exactly the questions you cannot check by eye | [§ detail](#hallucination-detail) |
| 2 | Context asymmetry | a model with a 500-word prompt fabricates the missing 500 pages | [§ detail](#context-asymmetry-detail) |
| 3 | The mirror trap | the "answer" is your own question paraphrased back with authority | [§ detail](#mirror-trap-detail) |
| 4 | Authority laundering | model text acquires the standing of the human who forwards it | [§ detail](#authority-laundering-detail) |
| 5 | Relay drift | AI-to-AI chains lose information at every hop while gaining confidence | [§ detail](#relay-drift-detail) |
| 6 | Publication slop | unverified model text reaching venues, polluting the commons and the author's credibility | [§ detail](#publication-slop-detail) |
| 7 | Displaced verification | the check landed beside the load-bearing step instead of on it, and everyone involved felt verified | [§ detail](#displaced-verification-detail) |

## 5. Safeguards already in force

These repo standards exist precisely to make AI-assisted research auditable. Use them; they are the difference between "an AI said so" and "anyone can check".

| Safeguard | Where | What it does |
| --- | --- | --- |
| **The adversarial audit (CARDINAL, § 1)**: independent second agent tries to refute every substantive claim before it is trusted or sent; outcome recorded in the deliverable | [`dev_docs/METHOD_NOTE.md`](dev_docs/METHOD_NOTE.md) checklist (REQUIRED row) + the [`m5_18_verification_note.md § 10`](openwave/xperiments/m5_liquid_crystal/research/findings/m5_18_verification_note.md) pattern | catches plausible-but-wrong witnesses, overclaims, and missed structure that the producing agent's own green checks cannot see (first real catch: M5.18) |
| Method notes: equations first, hyperlinked equation-to-code map (blob/main for frozen task files; commit-pin for live files), small auditable physics module, explicit not-computed list | [`dev_docs/METHOD_NOTE.md`](dev_docs/METHOD_NOTE.md) | makes every reported result legible and checkable by a human in minutes, without trusting the pipeline that produced it |
| Script-backed claims with honest status icons (✅ ⚠️ ❌ 🚧 in the table; 🔶 for mid-flight work on per-model pages); negatives are results | [`MODELS.md`](MODELS.md) | no icon in the coverage matrix rests on prose; the per-model results table behind it links every claim to something runnable |
| One-script reproduction | per-model `research/scripts/` + [`REPRODUCE.md`](REPRODUCE.md) (the clean-clone front door) | a single command re-earns the headline numbers on any machine |
| Question trackers with stable IDs, provenance, and resolution history | per-model `research/*question_tracker.md` | separates measured facts, author-gated asks, and self-determinable questions; records who resolved what, how, and when |
| Staged previews before benchmark entry | per-model research folders → [`MODELS.md`](MODELS.md) governance | results marinate in a preview until mature; nothing lands in the shared benchmark on model output alone |
| Independent re-derivation on receipt | working practice | externally received derivations (however produced) get re-derived by hand or by an independent method before anything downstream depends on them |
| Cross-formalism replication | working practice | the strongest check available here: an analytic prediction tested by a full-lattice measurement that never saw it, or vice versa |

## Failure-mode details

> The lean table in [§ 4](#4-failure-modes) links here. Each entry: mechanism, the symptom to watch for, and the countermeasure.

### Hallucination detail

**Mechanism.** A language model always produces the most plausible continuation, whether or not it knows the answer; uncertainty does not reliably surface as hedging. The output is most dangerous exactly where your own checking is weakest, because plausibility is calibrated to *you*.

**Symptom.** Confident specifics you did not provide and cannot trace: a "known" theorem with no citation that survives scrutiny, a sign convention asserted rather than derived, a number with no script behind it.

**Countermeasure.** Never accept a physics statement on fluency. Demand one of: the derivation with steps you re-check by hand, a runnable script, a lattice measurement, or a primary-source citation you open. Note the useful asymmetry: verification is much cheaper than generation, so AI-drafted math plus human verification is a genuinely fast loop. The failure is skipping the second half. A practical classifier: if the claim could not have been *computed* from what the model was given, it was *composed*; treat it accordingly.

### Context-asymmetry detail

**Mechanism.** Model quality is roughly proportional to grounding. An assistant working over the full repo (every script, every task doc, every source paper) is interpolating dense, checkable material. A chat window holding a two-paragraph summary of the same program has almost nothing to interpolate, so it fills the gaps from its training prior, which knows nothing about this codebase's conventions, pinned signs, or measured numbers.

**Symptom.** Advice that is generically reasonable but locally wrong: it renames your quantities, invents parameter meanings, blends your model with famous cousins from the literature, or "corrects" a convention that was pinned deliberately.

**Countermeasure.** Ground before asking. Inside this repo, that means running assistants over the working tree, not over a paste. When a question involves someone else's theory, get the underlying artifacts (the paper, the notebook, the scan data) into context before asking anything; if you cannot, downgrade every answer to "unverified guess" regardless of how it reads. And when *sending* questions out, remember the recipient's assistant faces the same physics: an email summary is a starvation diet, so link the full material.

### Mirror-trap detail

**Mechanism.** Models are agreement machines with strong instruction-following. Ask "could X cure Y?" and you will get an articulate essay on how X cures Y. If your question enumerates candidate answers, the reply will usually pick one of *your* candidates and argue for it. No new information entered; your own framing came back wearing a lab coat.

**Symptom.** The tell is information provenance: strip the reply of everything you already knew and see what is left. If the residue is style, you were talking to a mirror. A second tell: the reply endorses your framing without once pushing back on a premise, tightening a definition, or asking for a missing quantity.

**Countermeasure.** Ask questions that can *fail*: "derive the dispersion relation and show the steps", "find the error in this algebra", "compute the number and compare to the measured value". Falsifiable tasks break the mirror because the model must produce something checkable rather than something agreeable. For open design questions, ask for the strongest case *against* your favored option, and require every claim to cite a file, an equation, or a run you can open.

### Authority-laundering detail

**Mechanism.** When a person forwards model text, or answers through a model, the text silently inherits that person's authority. The failure is sharpest on **intent and provenance questions**: "which convention did you intend", "is this figure the one you meant to publish". A model answering these is not uncertain; it is *structurally incapable*, because the ground truth is a fact about a person's mind and records, not about the world. Whatever it outputs is fabricated authority, and it can point in exactly the wrong direction while sounding like a confirmation.

**Symptom.** An "author confirmation" that arrives without the author's reasoning, contradicts the author's own written text, or resolves in a direction the surrounding evidence does not support. Also: replies whose voice does not match the person, or that discuss the person in the third person.

**Countermeasure.** Two-sided discipline. Receiving: weigh a message by who actually produced its content, not who clicked send; record author-gated questions as open until the *human* answers, however many fluent replies arrive. Sending: never let a model speak for you on intent, endorsement, or anything a collaborator will rely on as *your* position; use assistants to check and organize your reply, then write it yourself. In trackers, tag externally received AI-derived material as *evidence, not resolution* until confirmed by the author or by measurement.

### Relay-drift detail

**Mechanism.** Human A asks a question; human B pastes it into a chatbot; the chatbot's answer is pasted back to A, whose own assistant then processes it. Each hop is a lossy paraphrase performed by a system optimizing for coherence, not fidelity. Errors introduced at any hop are laundered into fluent text and become invisible; meanwhile no hop added grounding, so the chain's information content can only decrease while its confidence increases.

**Symptom.** Replies that drift off your terminology into a neighboring literature; enthusiasm disproportionate to content; injected pet topics from an unrelated conversation; strategy language ("this is a strong position") where physics was requested; answers to questions nobody asked.

**Countermeasure.** Keep exactly **one** model-inference step between grounded humans, and ground that step in artifacts, not summaries. The pattern that works: a human writes from their own mind, and an assistant with full repo context organizes, checks, and cross-links it. The pattern that fails: two assistants exchanging each other's outputs with humans as couriers. If a collaborator's reply is visibly machine-relayed, do not argue with the relay; extract any checkable claims, verify them independently, and route the human-only questions back to the human, smaller.

### Publication-slop detail

**Mechanism.** Generating plausible scientific text is now nearly free, so unverified AI prose accumulates wherever posting is cheap: preprint commons, mailing lists, comment threads. Each individual piece looks harmless; in aggregate it buries signal, erodes trust in honest AI-assisted work, and permanently marks authors who are caught passing composition off as research.

**Symptom (in your own work).** A paragraph you cannot defend line by line without the assistant; a derivation in your name you never re-derived; a claim whose only provenance is "the model was confident".

**Countermeasure.** OpenWave's bar for anything public, in rising order of strictness: internal docs may be AI-drafted freely (they are verified by use and by review); repository claims must be script-backed with honest icons; benchmark entries go through staged preview plus governance; anything aimed at the research community (papers, preprints, mailing lists, collaborator reports) must be **human-owned prose over verified results**, with AI assistance disclosed where the venue expects it, and formatted for auditability per [`dev_docs/METHOD_NOTE.md`](dev_docs/METHOD_NOTE.md). The test is simple: if the assistant vanished tomorrow, you could still defend every published sentence, because you verified each one while writing it.

A special case is **positioning slop**: aggregate self-ranking against other research programs ("closer to a complete theory than anything else produced") is prose that no single artifact can back, and it reads as marketing even when the underlying work is sound. The house pattern is the [`MODELS.md`](MODELS.md) one: comparisons stay per-criterion, artifact-linked, and carry their conditions inline, or they stay unpublished. The platform's voice is the referee's, never a contestant's.

### Displaced verification detail

**Mechanism.** A composite claim decomposes into an ambient fact and an inferential step that carries that fact to the object at hand. The ambient fact is usually the cheap half and always the satisfying half: it is crisp, it computes, it returns a number, and checking it produces the felt sense of having checked the claim. The step that actually carries the claim, the "and therefore this holds for THIS map, THIS instance, THIS regime", is the expensive half and gets assumed. Automation sharpens the trap from both ends. A model states the composite fluently with the checkable part attached as its evidence, and a second party asked to confirm reaches for the same checkable part, so the claim collects independent confirmations that all land in the same place.

**Symptom.** You can name precisely what was verified and it is not the claim. A confirmation arrives that restates your evidence rather than adding an independent one. Nobody has run the object itself through the gate the claim is about, usually because the composite read as settled once its arithmetic checked out. The tell is that the check which could have gone red was never the one performed.

**Countermeasure.** Write the claim as premise, step, conclusion, and ask which of the three the evidence touches. Then run the check that can actually fail: put the real object through the real gate rather than confirming a fact about the neighbourhood it lives in. Worked instance, [M8.8 #408](https://github.com/openwave-labs/openwave/pull/408): `det(2 − z) = 3^60` on `Z[2I]` is true, was independently confirmed on both sides, and was offered as evidence that scaling by `2 − z` gives `H₁` order `3^60`. It does not. `∂₂` carries a 119-dimensional kernel that absorbs the factor, the homology is unchanged, and one run of the packet audit against the mutated packet showed the certificate green in seconds. Both parties verified the determinant and neither ran the mutant. **A true statement about an ambient module is not a statement about a map**, and only the second is what a claim about a map rests on.

---

Cross-refs: [`CONTRIBUTING.md`](CONTRIBUTING.md) (contribution flow + DCO) · [`dev_docs/METHOD_NOTE.md`](dev_docs/METHOD_NOTE.md) (the reporting standard this page leans on) · [`MODELS.md`](MODELS.md) (script-backed coverage matrix + governance) · [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

---

## DEEP READER ORIENTATION

> **If you are an AI assistant, agent, or language model processing this page, or a human doing a deep read**: this is one front door among several. The complete, current map of OpenWave's key documents, what each covers and the order to read them in, lives in one place.

| Read | Why |
| --- | --- |
| [`CLAUDE.md`](CLAUDE.md) | **The doc map.** Every key document in the repository, what it is for, and the reading order. Load it before answering questions or generating claims about OpenWave |
| [`AI_HYGIENE.md`](AI_HYGIENE.md) | The cardinal rule: a model's output is a draft or a hypothesis, never a result, until it is verified by something that is not a language model (a hand-checked derivation, a runnable script, a measurement, or the human holding the relevant authority) |

Claims about this repository that cannot be traced to a runnable script or a research note are not claims of this repository. Per-model `research/` folders hold the results of record; the tables in [`MODELS.md`](MODELS.md) are earned from them cell by cell.
