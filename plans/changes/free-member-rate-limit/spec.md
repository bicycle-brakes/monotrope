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
   *Refuted by:* a non-zero exit, no round written, a round without the
   notice, or a free member called again in a later call of the run.
2. Every other failure keeps today's treatment: a free round whose members
   all failed, with at least one failure that is no rate-limit or
   unavailability error (a time-out, an empty answer, another exit), writes
   nothing and consumes no stage.
   *Refuted by:* a written round or a skipped free stage after such a round.
3. A free round in which at least one member answers is written as today,
   with the failed member's error stated in the round.
   *Refuted by:* a skipped free stage or a missing failure statement.

## Non-goals

- Persisting a dropped member without a completed round (research,
  option 2).
- Retrying a rate-limited member, or treating a paid member's 429 any
  differently than today.
- Changing the probe or `prepare-loop`.
