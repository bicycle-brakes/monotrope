---
title: "Decisions — swarm-report-format"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-10
updated: 2026-11-10
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
