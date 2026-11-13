---
title: "Decisions — swarm-report-format"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-10
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-4q9y
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm]
---

# swarm-report-format — Decisions

Class: bounded (bead coding-harness-4q9y). The change amends ADR 0020
(`docs/adr/0020-phase-1-research-swarm.md`, point 9), so five answers are
owed and the spec lists that file under `adr_files`.

The interview was first skipped by the orchestrator on 2026-11-09. The draft
then stopped on a conflict with the decided invocation budget, and the
maintainer answered five questions in the orchestrating conversation on
2026-11-10, each by choosing one of two options in a dialog that named the
downside of both. The answer lines restate the chosen option; the accepted
downside in each statement is the one the dialog named for it.

## Q-1 · May the invocation ceiling rise for a correction call

asked: 2026-11-10
answer: Option 1, yes — the invocation ceiling of a research-swarm run may rise from `39 + 3N` to at most `72 + 6N`, for one correction attempt per topic report.
answered_by: maintainer
status: answered
context: |
  Topic: ADR 0020, point 9, caps a research-swarm run at 39 + 3N model calls and allows no retry.
  Intention: seven topic reports were rejected in run 1938a24f (2026-11-09); a correction call needs room in the budget.
  Today: a rejected report fails its seat; a required failure prevents reconciliation.
  Repository change: the runner counts correction calls against a higher ceiling.
  Architecture change: amends ADR 0020, point 9 (33 + 3N topic contributions may each be corrected once).

In the context of the invocation budget of a research-swarm run, facing topic
reports rejected for their format with no room in the budget to ask again, we
decided that the ceiling rises from `39 + 3N` to at most `72 + 6N` for one
correction attempt per topic report, to achieve runs that complete despite
correctable format faults, accepting that a run in which many reports fail
costs up to about twice the model calls — 2026-11-10

## Q-2 · Does the report contract change

asked: 2026-11-10
answer: Draft option — the report contract stays unchanged: at most seven claims, the required fields, the topic-specific fields.
answered_by: maintainer
status: answered
context: |
  Topic: one rejection in run 1938a24f exceeded seven claims, one omitted a required topic field.
  Intention: decide whether the fix loosens the contract or only the handling around it.
  Today: the contract of ADR 0020, decision 5, is enforced strictly.
  Repository change: none to the contract; validation keeps its rules.
  Architecture change: none.

In the context of the report contract of the research swarm, facing reports
that broke it by one claim too many or one missing field, we decided that the
contract stays unchanged, to achieve that the judge keeps scoring comparable
reports, accepting that a good report with eight claims still costs a
correction call or drops out — 2026-11-10

## Q-3 · How tolerant extraction is of wrapping

asked: 2026-11-10
answer: Draft option — an answer that holds exactly one JSON object in exactly one fenced code block is accepted with text around it; an answer with two candidates stays invalid.
answered_by: maintainer
status: answered
context: |
  Topic: three of seven rejections in run 1938a24f were complete reports behind a sentence of prose or before tool residue.
  Intention: stop losing complete reports to their wrapping.
  Today: the runner accepts only bare JSON or a fence that is the entire answer.
  Repository change: report extraction in the runner.
  Architecture change: none.

In the context of extracting a report from a seat's answer, facing complete
reports rejected for the prose or tool residue around them, we decided that
exactly one JSON object in exactly one fenced block is accepted with text
around it and that two candidates stay invalid, to achieve that wrapping no
longer costs a report, accepting that an answer holding a draft and a final
object still costs the one correction call — 2026-11-10

## Q-4 · Who makes the correction attempt

asked: 2026-11-10
answer: Draft option — the same model receives its report and the reason for the rejection and answers once more.
answered_by: maintainer
status: answered
context: |
  Topic: who corrects a report with a real format fault.
  Intention: four of seven rejections in run 1938a24f were small contract breaks a model can fix when told which one.
  Today: no correction; the seat fails. The review loop already asks once more after a malformed answer.
  Repository change: one correction call in the runner, with the rejection reason in the prompt.
  Architecture change: the ceiling of Q-1 (ADR 0020, point 9), whose amendment says "the model that wrote it".

In the context of correcting a rejected topic report, facing the choice
between the seat's own model and a cheap second model that only reformats, we
decided that the same model is asked once more with the reason for the
rejection, to achieve that a report stays the work of the seat it is
attributed to, accepting that a model which does not understand the format
often fails a second time and that call is then lost — 2026-11-10

## Q-5 · Unknown extra fields

asked: 2026-11-10
answer: Draft option — an unknown extra field stays a rejection with its reason, followed by the one correction attempt of Q-4.
answered_by: maintainer
status: answered
context: |
  Topic: a report that carries fields the contract does not know.
  Intention: two rejections in run 1938a24f came from extra fields around usable content.
  Today: any unknown field invalidates the whole report and the seat fails.
  Repository change: validation stays strict and triggers the correction call; nothing is dropped silently.
  Architecture change: none beyond the ceiling of Q-1.

In the context of unknown extra fields in a topic report, facing usable
reports rejected for one surplus field, we decided that the field stays a
rejection answered by the one correction attempt, to achieve that content
written into a wrongly named field is never lost unseen, accepting that a
good report costs an extra call for one surplus field and drops out when the
correction fails — 2026-11-10

## Q-6 · How much phase-4 time this change may still take

asked: 2026-11-12
answer: "maxhe a mit opus sub, erstelle einen bead für die reparatur" — option A: an Opus sub-agent repairs the three text rows of the second review-loop round (L2-1, L2-12, L2-14) by hand, the runner repair reruns for the code rows only, the appetite rises to 9 hours, and the runner flaw gets a bead of its own (coding-harness-kz5r).
answered_by: maintainer
status: answered
context: |
  Topic: the phase-4 time budget (appetite) of this change after the second runner repair was lost.
  Intention: the time used had passed the budget, so no further runner call was allowed without the maintainer.
  Today: plan.md recorded 6.98 hours of measured phase-4 time against an appetite the maintainer had already raised from 3 to 6 hours earlier that day (recorded in the bead's notes only; the plan card still said 3). The second runner repair of the round-2 rows was discarded whole because it also edited prompts/01-explore.md, a path a runner run may not commit.
  Repository change: the plan card's appetite reads 9 hours; the three text rows are edited by hand, the code rows go back to the runner repair.
  Architecture change: none.

In the context of a change whose measured phase-4 time had passed its raised
appetite after a runner repair was discarded over one held path, facing the
choice between stopping the change and spending more time on it, we decided
to raise the appetite to nine hours, to have the three text rows edited by
hand and to rerun the runner repair for the code rows only, to achieve that
the repairs already understood are not lost to one misplaced edit, accepting
that this bounded change now takes three times its first budget and that the
runner flaw behind the discard stays open in its own bead — 2026-11-12

## Q-7 · A loose JSON object beside the one fenced block

asked: 2026-11-13
answer: "Ja" to option A — the fenced block is the protocol: only fenced blocks are candidates; text outside the one fenced block is never read; two fenced blocks with objects stay invalid. Spec criterion 3 follows. A bead for structured output instead of text parsing is opened.
answered_by: maintainer
status: answered
context: |
  Topic: the change swarm-report-format (bead coding-harness-4q9y), when a model answer counts as a report.
  Intention: review round 6 reported a BLOCKER (L6-1): spec criterion 3 refuted a bare object beside a fenced object, while the code after loop row L4-3 no longer reads text outside the fenced block.
  Today: the maintainer's answer of 2026-11-12 ~14:20 UTC said no brace scanning selects anything; four findings in three rounds came from scanning prose for objects.
  Repository change: one sentence in spec criterion 3 and this record.
  Architecture change: none.

In the context of model answers that wrap their report in prose,
facing four findings from heuristics that scan prose for JSON objects,
we decided that the one fenced block is the report and text outside it is never read,
to achieve one unambiguous delimiter instead of guessing,
accepting that a stray object a model writes into its prose is ignored rather than refused — 2026-11-13
