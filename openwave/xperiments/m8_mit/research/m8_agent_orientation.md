# M8 Agent Orientation: the agent front door

> **If you are an AI agent and were told "read the m8_agent_orientation.md": this page is
> your bootstrap.** Load every document in § 1 into context, in order. Then follow the
> completion protocol in § 4: confirm you are oriented, summarize what you read, and
> declare yourself ready. From that point the author can ask you anything about the M8
> model, plan next moves with you, or start work on a roadmap task with a simple
> **"go task m8.\<n\>"**.
>
> Humans are welcome to read this page too; the model's human front door is
> [`__M8_model_briefing.md`](../__M8_model_briefing.md).

## 1. The orientation reading list (load ALL, in this order)

| # | Doc | What it gives you |
| --- | --- | --- |
| 1 | [`__M8_model_briefing.md`](../__M8_model_briefing.md) | the column at a glance: identity, model profile, honest status, help wanted |
| 2 | [`research/m8_theory_canonical.md`](m8_theory_canonical.md) | THE SPEC OF RECORD (canonical when docs disagree): the arena, the operators, the particle map, the mass formula, known tensions, consumption rules, open questions OQ1-OQ6 |
| 3 | [`research/m8_background.md`](m8_background.md) | the gap map (what MIT has, what it lacks), the evidence-weight grading, why the field-dynamics program exists, the onboarding evaluation of record |
| 4 | [`research/m8_roadmap.md`](m8_roadmap.md) | the program: tasks, gates, ownership, current status, what is startable now |
| 5 | [`research/m8_platform_pointers.md`](m8_platform_pointers.md) | the cross-model reading map: where in the other OpenWave models to find Lagrangian families, defect taxonomies, clock/stability lessons, engine routes; ALSO load its § 1 platform-contract docs, [`AI_HYGIENE.md`](../../../../AI_HYGIENE.md) above all |
| 6 | [`research/tasks/`](tasks/) | the per-task planning docs, one per roadmap task: skim the ones the current question touches; deep-read the one you are about to run |
| 7 | [`research/tasks/m8_1_task_details.md`](tasks/m8_1_task_details.md) + [`research/findings/m8_1_method_note.md`](findings/m8_1_method_note.md) | **the worked template**: M8.1 is a complete, closed task run (planning → execution → audit → review); § 2 below tells you what to copy from it |
| 8 | [`theory/_CITATIONS.md`](../theory/_CITATIONS.md) | the source registry: which record backs which claim; the never-fabricate identifier policy |

## 2. How tasks run here (M8.1 is the template)

M8.1 is kept as the reference execution: read its task details and method note as a
worked example, then reuse the shape.

| Phase | What M8.1 did, to copy |
| --- | --- |
| PLAN | scope + definition of done; **pre-registered pass/fail criteria written BEFORE any numerics** (its C1-C5 table); a blindspot pass (what could silently go wrong, with mitigations); sub-experiments named with artifact paths |
| EXECUTE | scripts / data / plots under `research/` with `m8_<id>_` prefixes; every claim backed by a runnable script; anything that deviates from the plan goes in the DEVIATIONS LOG as it happens, not retroactively |
| FINISH | a method note per [`dev_docs/METHOD_NOTE.md`](../../../../dev_docs/METHOD_NOTE.md): equations FIRST, an equation-to-code map, embedded plots, the audit record; findings written into the task details; honest status flips in the roadmap / briefing / MODELS.md column (a negative is a result and syncs the same day) |
| REVIEW | a short review block in the task details: results per pre-registered criterion, issues found and dispositioned, findings takeaway, docs touched |

## 3. A small workflow routine (a SUGGESTION, blend into your own)

This is the routine the platform uses, offered as a starting point. It is method, not
tooling; the author should adapt or absorb it into whatever workflow already works.

| Step | The habit |
| --- | --- |
| Task plan | pre-register targets, conventions, and pass/fail BEFORE computing; run a blindspot pass; name the artifacts |
| Execute | script-backed claims only; log deviations as they happen; no tuning toward published values (a fork is reported with all its numbers) |
| Finish | method note (equations first + code map + plots), honest status flips, findings recorded either way |
| Adversarial audit | before any substantive claim is trusted or shared: an INDEPENDENT second agent tries to REFUTE it with its own script and its own method (different discretization, different derivation), returning per-claim verdicts; the audit is recorded in the deliverable. M8.1's § 5 audit record shows the shape, including a defect found and dispositioned |
| Author gates | questions of intent, provenance, or definition can only be answered by the author; an agent NEVER resolves them by inference. If a published definition underdetermines a computation, that is a question to ask, not a choice to make silently |

The unknowns discipline, the part most worth adopting: every unknown gets ROUTED by
who or what can resolve it, and the unknown-unknowns get structural hooks:

| Unknown type | Route |
| --- | --- |
| Machine-checkable | a script can decide it: write the script (M8.1's entire question was this type) |
| Author-gated | only the author can answer (intent, provenance, definitions): ask, never guess |
| Nature-gated | only an experiment or observation can decide: register it as a falsifier with a threshold (MIT's Euclid DR1 card is exactly this practice) |
| Unknown-unknowns | no route exists, so build tripwires: the blindspot pass at PLAN, the deviations log during EXECUTE, and a self-quiz before anything is shared outward ("what would a hostile reader attack first?") |

And the one non-negotiable, from [`AI_HYGIENE.md`](../../../../AI_HYGIENE.md) (the
platform-wide contract, not a suggestion): **model output is a draft or hypothesis,
never a result, until verified by something that is not a language model**: a runnable
script, a hand-checked derivation, a measurement, or the author's own authority.
Agents show the script and the number, never a verdict alone.

## 4. Completion protocol (what to print after reading)

Once §§ 1-3 are consumed, print, in this order:

| # | Print |
| --- | --- |
| 1 | A confirmation that you are ORIENTED on the M8 column and the platform contract |
| 2 | A one-line summary of EACH document you read (so the author can verify nothing was skipped) |
| 3 | The column's current status from the roadmap: what is done, what is startable, what is gated |
| 4 | A readiness statement: you can now (a) answer the author's questions about the M8 model and its OpenWave context, (b) help plan next moves, and (c) execute a roadmap task on command: **"go task m8.\<n\>"** means open that task's `research/tasks/m8_<n>_task_details.md`, complete its go-time pre-registration with the author, and run it per §§ 2-3 |
