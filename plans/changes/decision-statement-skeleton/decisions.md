---
title: "Decisions — decision-statement-skeleton"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-nr6h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, draft]
---

# decision-statement-skeleton — Decisions

Class: bounded (bead coding-harness-nr6h).

## Q-1 · Where a missing decision statement is prevented

asked: 2026-11-10
answer: "Kann bei sowas pydantic oder jinja 2 helfen? A" — option A of the dialog, which was "both": the interview asks the accepted downside with every question and writes the statement at once, and `draft` refuses before its first model call when a statement is missing. The question about pydantic and Jinja2 in the same answer is recorded as a [GAP] for the spec.
answered_by: maintainer
status: answered
context: |
  Topic: where it is made sure that every interview answer carries its decision statement in decisions.md.
  Intention: in the night of 2026-11-10 two changes (verify-slots, review-fewer-rounds) lost three draft attempts each on the missing statement alone.
  Today: the interview prompt holds a template line for the statement; the accepted downside is not asked; a draft notices the gap only after its model calls, in the document check.
  Repository change: the interview prompt, the runner's draft verb and tests; no new gate.
  Architecture change: none.

In the context of the decision statement that every answered interview record
needs, facing drafts that failed after their model calls on the missing
statement alone, we decided that the interview asks the accepted downside
with every question and writes the statement at once, and that `draft`
refuses before its first model call when a statement is missing, to achieve
that no draft attempt is spent on a missing statement, accepting that every
interview question gets a little longer, because the maintainer chooses the
downside with the answer — 2026-11-10

## For the spec to weigh

[GAP] The maintainer asked whether pydantic or Jinja2 can help. Both are
pinned dependencies of this repository already (`pyproject.toml`, read
2026-11-10: Jinja2 3.1.6, pydantic 2.13.5). One way they could: a record
model with required parts (context, facing, decided, to achieve, accepting,
date) that refuses a record with a part missing, and a template that renders
the statement from those parts, so that its form cannot be wrong. Whether
that is worth a second representation of a record beside the Markdown the
gates read today is for the spec to weigh against the plain way (the prompt
asks, the runner refuses early); it is not decided here.

## Q-2 · Whether the rule also holds for questions of the later phases

asked: 2026-11-11
answer: Include it now — the question form for decisions raised while writing spec, design or plan (`prompts/02-spec.md`) gets the same rule in this change.
answered_by: maintainer
status: answered
context: |
  Topic: whether the new rule "every question names the downside you accept" holds only in the interview or for every question to the maintainer.
  Intention: review round 3 found (row L3-4) that the rule was written into the interview prompt only; questions that come up later follow a form of their own that ends at "What is lost" and never asks for the accepted downside, yet their answers become records in decisions.md, where the new check demands the complete statement.
  Today: bead and spec name the interview only; the change is complete by them but leaves this second source of records without the rule.
  Repository change: the held prompt file prompts/02-spec.md gets the rule, with a test; or the spec names the gap as a limit and a follow-up bead closes it.
  Architecture change: none.

In the context of questions raised while writing spec, design or plan,
facing a question form that never asks for the accepted downside although
its answers become records the new check reads, we decided that this form
gets the same rule in this change, to achieve that no source of answered
records lacks the accepted downside, accepting that the scope grows by a
further held file and a test, that the change is already far past its
appetite and that every further review round costs a full check
— 2026-11-11
