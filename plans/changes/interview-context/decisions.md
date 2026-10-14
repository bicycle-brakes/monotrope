---
title: "Decisions — interview-context"
status: draft
implementation_status: partial
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-zs7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, adhd, questions]
---

# Every question carries its context — Decisions

Phase 1a for bead coding-harness-zs7, asked by the orchestrating Claude Code
session on 2026-10-14 in interview form, each question with its context
first. The trigger: the phase 2a findings of change sol-effort were asked
without context, and one (S-3) could not be answered until it was explained.
The maintainer then asked that the rule become part of Coding Harness,
recorded as an ADR.

## Q-1 · Which questions the rule covers

asked: 2026-10-14
answer: every question an agent puts to the maintainer — interview, spec decisions, review ambiguities, the plan card and the conversation itself, in every harness.
answered_by: maintainer
status: answered

In the context of a rule that stood only in the interview prompt, facing the
choice between the interview, the workflow's questions and every question,
we decided on every question to achieve that no question reaches the
maintainer without its context, accepting that the rule moves into
`AGENTS.md` and binds the conversation too. — 2026-10-14

## Q-2 · Whether a gate checks the rule

asked: 2026-10-14
answer: yes — each answered record in `decisions.md` keeps the context that was shown, in a field of its own, and a gate in `make verify` goes red when it is missing.
answered_by: maintainer
status: answered

In the context of a prompt rule nobody checks, facing the choice between a
writing rule only and a recorded field with a gate, we decided on the field
and the gate to achieve that later readers see what the maintainer answered
to, accepting that the gate proves presence, not clarity. — 2026-10-14

## Q-3 · How the rule travels to other repositories

asked: 2026-10-14
answer: for everyone — the kit carries it as the principle "plain language, context first", with ADHD named as its reason; nothing to switch on or off.
answered_by: maintainer
status: answered

In the context of a kit that carries the prompts into other repositories,
where other people may be asked, facing the choice between a principle for
all and a personal profile, we decided on the principle for all to achieve
one rule without configuration, accepting that every instance writes its
questions this way. — 2026-10-14

## Q-4 · The form of the context

asked: 2026-10-14
answer: a fixed form, and it must also say why we do this — the intention — and what changes in the repository and its architecture.
answered_by: maintainer
status: answered

The maintainer's words, 2026-10-14, choosing the fixed form: "feste form, ich
will auch warum wir das machen, was die intention ist, und was sich dadurch in
der repo und der architektur ändert". The exact headings of the form are left
to the spec; they cover at least: what it is about, why we do it (the
intention), what happens today, what changes in the repository and its
architecture, and the question itself last.

In the context of free sentences that are built differently each time, facing
the choice between free text and a fixed form, we decided on a fixed form
that names the intention and the effect on repository and architecture to
achieve that the maintainer finds each part in the same place, accepting a
longer question. — 2026-10-14

## Q-5 · Whether the gate reaches older records

asked: 2026-10-14
answer: only from its adoption — the gate checks answers recorded on or after the day it merges; older `decisions.md` files stay as they are.
answered_by: maintainer
status: answered

In the context of many existing records without a context field, facing the
choice between a cut-off date and backfilling every old record, we decided on
the cut-off date to achieve a gate that holds from day one without
reconstructed context, accepting that older answers show no context. —
2026-10-14
