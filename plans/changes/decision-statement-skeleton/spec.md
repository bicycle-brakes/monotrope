---
title: "Spec — decision-statement-skeleton"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-nr6h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, interview, stage-2]
class: bounded
appetite: 3
adr_files: []
neighbours:
  - plans/changes/archive/2026-11-06-interview-context/spec.md
---

# Spec — decision-statement-skeleton

The interview records the downside the maintainer accepts with each answer,
and a draft spends no model attempt on an absent or unreadable decision
statement (bead coding-harness-nr6h). Research: `research.md`.
Decision: `decisions.md#Q-1`.

## Problem

- The interview template contains an `accepting` clause but does not require
  asking for its content; an agent can omit the statement or invent the
  downside. Read in `prompts/01a-interview.md`, recorded in `research.md`,
  2026-11-10.
- Draft preflight checks only that `decisions.md` can be read. The document
  check discovers missing statements after model calls, and retries cannot
  repair the protected answers. The interrupted-night handover records this
  failure for verify-slots and review-fewer-rounds on 2026-11-10
  (`research.md`, "The failure history").
- The existing question-context gate already reads the required statement
  and its date; adding another interpretation would create conflicting
  definitions of a readable record (`research.md`, "What the gate checks").

## Terms

**Readable statement:** the existing question-context gate can read exactly
one top-level `In the context of` statement with one ending `— YYYY-MM-DD`
calendar date, including its currently supported wraps and closing remark.
This checks form, not whether the prose faithfully restates an answer.

## Acceptance criteria

1. When the interview prompt instructs an agent to present a question, it
   requires asking which downside the maintainer accepts with the choice.
   *Refuted by:* the prompt leaves the downside to the agent or treats the
   question as an optional later step.
   *Basis:* decisions.md#Q-1.
2. When an interview answer settles the choice and its accepted downside,
   the prompt requires immediately recording their faithful decision
   statement with the answer's recording date.
   *Refuted by:* recording is deferred to drafting, the statement template
   loses a clause or date, or an unstated downside may be invented rather
   than left unresolved for the maintainer.
   *Basis:* decisions.md#Q-1.
3. If any answered question record in the selected change lacks a readable
   statement, `draft` refuses before its first model call with the decision
   file, question identifier, reason and instruction to complete the interview.
   *Refuted by:* a Codex or fallback call starts, a retry is consumed, or
   the refusal fails to identify the record and remedy.
   *Basis:* decisions.md#Q-1.
4. If the selected decision file cannot be read, `draft` refuses before any
   model call without repairing or replacing the file.
   *Refuted by:* an unreadable or invalidly encoded file becomes an empty
   passing interview, is rewritten, or reaches a model call.
   *Basis:* decisions.md#Q-1; research.md, "Where the draft verb finds a missing statement".
5. When all answered records in the selected file have readable statements,
   or it contains only open questions, skip records and fenced examples,
   the statement precheck permits the existing draft guards to continue.
   *Refuted by:* a supported wrapped statement is rejected, an open or
   example record requires a statement, or this precheck demands an ADR answer.
   *Basis:* decisions.md#Q-1; research.md, "What the gate checks".
6. While the selected file has readable statements, malformed statements in
   other changes do not cause this early statement check to refuse it.
   *Refuted by:* an unrelated live or archived decision file prevents the
   first call through this precheck; the later repository-wide check is separate.
   *Basis:* decisions.md#Q-1; research.md, "Where the draft verb finds a missing statement".

## Non-goals

- No record migration, invented answers, automatic downside selection,
  structured record store, new dependency or new gate.
- No stricter statement grammar or semantic grading by the gate; context,
  adoption dates, interview minimums and the missing-ADR-answer tolerance stay
  as they are. All answered occurrences retain the gate's current meaning.
- No change to `make change` or its generated files: the existing interview
  template is the record skeleton used by the chosen interview route.
- No design phase or ADR draft: this bounded change improves the existing
  interview and draft entry checks without an architectural decision.

## Protected areas

`decisions/`, `model-endpoints.yaml`, `provenance.yaml`, `AGENTS.md`, kit
policy and other changes' records: this work changes neither governance nor
past answers. Draft restore rules, credentials and leak checks are unchanged.

## Definition of Done

- `make verify` is green after the orchestrator's prompt edit; the targeted
  counterexamples show refusal before dispatch and unchanged passing routes.
- `prompts/01a-interview.md` and `docs/WORKFLOW.md` describe the behavior in
  the same pull request as code and tests; no model or ADR changes.
- The pull request's file list respects protected areas and non-goals.
- The pull request closes coding-harness-nr6h and its last commit carries
  `Closes-Bead: coding-harness-nr6h`.
- Special runs: none beyond the verification commands in `plan.md`.

## Open decisions

None open. The maintainer's answer in `decisions.md#Q-1` is the authority.

[DETAIL] Reuse the Markdown reader rather than adding a Pydantic model or
Jinja2 rendering: both could validate or render a new structured input, but
neither supplies the maintainer's accepted downside, and a second record
representation is unnecessary for this refusal. Keep the existing prompt
template as the skeleton instead of changing the scaffolder's output.

[DETAIL] Limit phase 4, including repairs, to three hours; stop and report
unfinished work at the limit. This is a reversible planning budget.
