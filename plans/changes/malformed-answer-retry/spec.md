---
title: "Spec — malformed-answer-retry"
status: draft
implementation_status: partial
date: 2026-10-26
last_reviewed: 2026-10-26
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-70rw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, review-loop]
class: bounded
appetite: 2
adr_files: []
---

# Spec — malformed-answer-retry

A review-loop member whose answer is malformed is asked once more with the
format reminder (bead coding-harness-70rw). Research: `research.md`.
Decisions: `decisions.md`, Q-1 and Q-2.

## Terms

- **Malformed answer:** an answer with no six-cell row that is not
  exactly `No finding.`.
- **Format reminder:** a fixed runner sentence that the previous answer
  was not in the required format, followed by `ANSWER_FORMAT`.

## Acceptance criteria

1. A member whose first answer is malformed is called once more, with its
   prompt followed by the format reminder; a valid second answer counts as
   the member's answer for the round.
   *Refuted by:* a round with a malformed first and valid second answer
   that fails or omits the second answer's rows.
2. The loop record keeps both answers: a runner line names the member and
   says it was asked again, and the first answer is quoted.
   *Refuted by:* a round record without the first answer's text.
3. A second malformed answer fails the member as today; a member is asked
   again at most once per round.
   *Refuted by:* a third call to the same member, or a round that passes
   on two malformed answers.
4. The second call is a stage-2 call: its prompt passes the leak check
   before it starts, and its call line is written to `findings.md` and
   counted in the no-round line's audit calls.
   *Refuted by:* a second call without its own call line, or one made
   after a leak-check BLOCK.
5. No second call starts once the round's deadline has passed; the member
   then fails as today and the record says why.
   *Refuted by:* a second call after the deadline.

## Out of scope

- A malformed phase-6 verdict (Codex `review`).
- Rows without a closing pipe and a malformed row beside a valid one
  (beads coding-harness-2i9j, coding-harness-vque).
