---
title: "Decisions — repair-fixed-line-format"
status: draft
implementation_status: partial
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-hgvp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# repair-fixed-line-format — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · What the runner does with explanatory lines in a repair answer

context: |
  Topic: repair answers that are rejected with "several fixed lines".
  Intention: four Sonnet repairs on 2026-10-26 were rejected although the
  code was green; the night-run fallback to Sonnet depends on this path.
  Today: every line that starts with a taken row's id and a colon counts,
  so an explanatory line beside the fixed line fails the row; the answer
  is not kept, so the cause is inferred.
  Repository change: keep each attempt's answer and show the contested
  lines in the diagnostics; when exactly one line of an id is a fixed
  status, only it counts; two different fixed lines still fail.
  Architecture change: none.
asked: 2026-10-26, conversation 2026-10-26 (interview)
answer: "Keep the answer of every attempt and show the contested lines in the failure; when an id has exactly one 'fixed — …' line, only that line counts and explanatory lines are ignored; two different fixed lines for the same id stay an error"
answered_by: maintainer
status: answered

In the context of the repair verb's answer check, facing correct repairs
rejected for explanatory lines beside their fixed line, we decided that
only the fixed lines count and that every attempt's answer is kept, to
achieve that a format slip neither costs a green repair nor stays
unreadable, accepting that a stray explanation is silently ignored. — 2026-10-26

## Q-2 · Identical fixed lines [DETAIL]

Two fixed lines for one id that are identical after stripping count as
one. They state the same status, so refusing them would reject an answer
for repetition alone; two different fixed lines remain an error, as the
maintainer's answer says.

## Q-3 · Where the answer is kept [DETAIL]

The scrubbed answer is kept with the attempt evidence the runner already
keeps for a failed attempt, and the failure diagnostics name where it is
and quote each contested line (scrubbed). The answer never enters
`findings.md` whole: it can be long, and the diagnostics block is cut to
its last lines.
