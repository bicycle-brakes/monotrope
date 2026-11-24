---
title: "ADR 0026 — Isolate writing attempts in detached worktrees"
category: adr
status: accepted
created: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, attempts]
---

# ADR 0026 — Isolate writing attempts in detached worktrees

* Status: proposed until the decision pull request merges; partially supersedes ADR 0017 decision 2 and ADR 0016 decision 4 on failed writing calls.
* Review: maintainer chose the direction on 2026-11-22 and re-sliced it on 2026-11-24; Decider: maintainer; prepared by Codex.
* Date: 2026-11-24; takes effect on merge.

## Context

Failed writing attempts damaged their lane, and failed calls stalled repairs (research and decisions for isolated-writing-attempts, 2026-11-22 and 2026-11-24). A narrower first slice makes the change reviewable (Q-25).

## Decision Drivers

* Protect lane state and runner inputs while keeping attempts inexpensive.
* Make route switches visible and preserve leak refusals.

## Considered Options

* Detached worktrees: cheap local isolation, with shared Git and environment state.
* Containers: stronger isolation at greater operational cost.
* Keep writing in the lane: no new lifecycle, but manual recovery remains.

## Decision

Chosen option: detached attempt worktrees through one writing-attempt lifecycle. Repair is isolated first; draft and implement follow in a later rollout. Failed writing calls fall through to the next declared route with saved state and a visible reason; leak refusals and internal failures stop. Attempt machine state is schema-validated JSON. Review isolation, a lifecycle CLI, post-merge ref cleanup and the later-rollout gate are separate follow-ups.

## Consequences

* Worktrees and retained refs consume local resources; cleanup is follow-up work.
* Shared environments require checksums and recovery; network and foreign reads remain outside this decision.
* A worktree does not prevent access to the lane through linked environment parents; changes to tracked and untracked lane paths, and selected shared Git state, are detected; ignored lane files and whole runner-owned files are outside that check. Checksums cover package and Pi versions, not arbitrary bytes.

## Validation

* Structural and lifecycle tests and `make verify` exercise writing routes, isolation, state validation and failure handling.
