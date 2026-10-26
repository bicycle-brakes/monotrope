---
title: "Decisions — free-member-rate-limit"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-pj98
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# free-member-rate-limit — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).

## Q-1 · What the loop does with a free member that is rate-limited at review size

context: |
  Topic: the free stage of the review loop (phase 4b).
  Intention: a free model that passed the static probe but answers 429 or
  "unavailable" at review size blocked every rerun (bead coding-harness-pj98).
  Today: a round whose every member failed writes nothing, and the next call
  starts the same free members again.
  Repository change: the runner drops such a member for the run.
  Architecture change: none.
asked: 2026-10-24, conversation 2026-10-24 (interview)
answer: "a free member that fails its round with a rate-limit (429) or unavailability error is dropped for this run; the round counts as having no free member and the loop moves on to the Flash swarm; recorded in the loop record"
answered_by: maintainer
status: answered

In the context of the review loop's free stage, facing a free model that is
rate-limited or unavailable at review size, we decided that such a member is
dropped for the run and the loop moves on to the Flash swarm, recorded in the
loop record, to achieve that a rate-limited free model no longer blocks the
loop, accepting that the change then gets no free review. — 2026-10-24
(recorded from the bead's notes by the orchestrating session, 2026-10-25)

## DETAIL · decided by the orchestrating session

- **Which errors count.** A member's failure counts when it is a
  `CallFailed` that is not a time-out and its message holds `429`,
  "rate limit", "too many requests" or "unavailable" (any case). A time-out,
  an empty or unreadable answer and any other exit stay ordinary failures.
  Reason: the answer names rate-limit and unavailability errors only.
- **When the free stage is dropped.** When every free member of the round
  failed and every failure counts. Then the free stage is marked skipped
  with the members and their errors, and the next stage runs in the same
  call. Reason: the snapshot that holds the drop is written only with a
  completed round (research, option 1).
- **Mixed outcomes.** A round with at least one answering free member is
  written as today; the rate-limited member's failure stands in the round,
  and the free stage is consumed with it, so the member is gone for the run.
  When every member failed and only some failures count, the attempt fails
  as today: the drop needs a completed round, and an ordinary failure gives
  none. Reason: no new record kind (research, option 2 rejected).

## Q-2 · Where the mixed case goes

**Asked 2026-10-25, in the night run.** Phase 6 (F6-1) found that the spec
leaves out the mixed case, a round where one free member is rate-limited
and another fails another way. The maintainer had answered "also solve the
mixed case".

**Answer (maintainer, conversation, 2026-10-25):** "Ja, Teil 1 jetzt". This
change ships the case where every free member is rate-limited. The mixed
case, which remembers a dropped member without a written round, moves to
bead coding-harness-pj98. It needs an ADR 0021 amendment with its own
interview.
