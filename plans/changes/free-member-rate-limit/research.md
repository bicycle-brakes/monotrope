---
title: "Research — free-member-rate-limit"
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
tags: [research, review-loop, free-swarm]
---

# free-member-rate-limit — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` (2026-10-25).

## The finding (bead coding-harness-pj98)

Measured 2026-10-24 about 02:40–02:50 UTC on change review-verdict-validated:
`prepare-loop` selected `longcat-2.5-preview-free` (its static probe
passed), and `review-loop` round 1 failed twice with
`pi call failed: exit 1 (429: Upstream request failed: Endpoint is unavailable.)`.
Every rerun started the same free model again; the runner offered no way
past it.

## How the code behaves today

- `stages_of` lists the free swarm first, unless `state["free"]["selected"]`
  is empty or `state["free"]["skipped"]` is set; then the Flash swarm, then
  one stage per remaining rung.
- `review_loop` already skips the free stage once in a call: with no
  implementation source diff it sets `state["free"]["skipped"]` and takes
  `next_stage(state)`. The notice reaches the round as
  `Notice: <skipped>.` while no stage is consumed.
- `run_swarm` returns each member's answer or its exception. When no
  member succeeded, `review_loop` raises `CallFailed` naming every member's
  failure: the attempt writes no record, consumes no stage and spends no
  availability receipt (ADR 0021, decision 6). The next call rediscovers or
  re-reads the same free members, so a member that is rate-limited at review
  size blocks every rerun.
- `fail` builds a Pi failure as `pi call failed: <reason> (<last stderr
  line>)`, so the provider's `429` or `unavailable` text reaches the
  exception's message. A time-out is `StepTimedOut`, a subclass of
  `CallFailed` with its own message.
- The snapshot (`Loop state:` line) is written only with a completed round.
  A drop that must survive a rerun therefore needs a completed round in the
  same call, or a new kind of record.

## Options

1. Within the call, when every free member failed with a rate-limit or
   unavailability error, mark the free stage skipped with the reason and
   run the next stage (the Flash swarm) in the same call; the round written
   carries the notice. No new record kind; the decision holds because the
   snapshot that carries `skipped` is written with that round.
2. Persist a dropped member without a round. Needs a new record before the
   first round, against ADR 0021 decision 6 (a failed attempt leaves no
   record).

Option 1 matches the maintainer's answer (decisions.md, Q-1) and needs no
new record.
