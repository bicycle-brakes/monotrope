---
title: "Spec — free-member-rate-limit"
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
tags: [spec, review-loop, free-swarm]
class: bounded
appetite: 1
adr_files: []
---

# Spec — free-member-rate-limit

A free model that is rate-limited or unavailable at review size no longer
blocks the review loop: the run drops the free stage and moves on to the
Flash swarm (bead coding-harness-pj98; decisions.md Q-1).

## Acceptance criteria

1. When every member of a free round fails with a rate-limit or
   unavailability error, the same `review-loop` call marks the free stage
   skipped and runs the next stage; the round written is that stage's round,
   and it carries a notice naming each free member and its error.
   Only a failed exit counts; an empty answer is no rate limit, whatever its
   standard error says.
   *Refuted by:* a non-zero exit, no round written, a round without the
   notice, or a free member called again in a call after the written round.
2. Every other failure keeps today's treatment: a free round whose members
   all failed, with at least one failure that is no rate-limit or
   unavailability error (a time-out, an empty answer, another exit), writes
   nothing and consumes no stage.
   *Refuted by:* a written round or a skipped free stage after such a round.
3. A free round in which at least one member answers is written as today,
   with the failed member's error stated in the round.
   *Refuted by:* a skipped free stage or a missing failure statement.
4. When the drop leaves no stage of the run, the call refuses and names the
   drop and the missing paid stage; nothing is written.
   *Refuted by:* a refusal that claims a round was spent, or a written
   record. Added after pre-review row P247-3, 2026-10-25.

## Non-goals

- Persisting a dropped member without a completed round (research,
  option 2). So the drop does not survive a call in which the next stage
  fails too, and a round whose members all failed, only some of them with a
  rate limit, fails as today: the rate-limited member is called again on the
  next call. This narrows the maintainer's answer (decisions.md, Q-1). The
  maintainer answered on 2026-10-25 that this change ships the all-rate-limited
  case and the mixed case moves to bead coding-harness-pj98, with an
  ADR 0021 amendment and its own interview (decisions.md, Q-2).
- The Flash round after a drop gets its own `REVIEWER_MINUTES` deadline, so
  one call can take up to two round limits.
- Retrying a rate-limited member, or treating a paid member's 429 any
  differently than today.
- Changing the probe or `prepare-loop`.
