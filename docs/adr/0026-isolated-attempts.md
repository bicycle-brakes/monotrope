---
title: "ADR 0026 — Isolate model attempts in detached worktrees"
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

# ADR 0026 — Isolate model attempts in detached worktrees

* Status: proposed until the decision pull request merges; partially supersedes ADR 0017 decision 2 on failed calls, and amends the runner-only entry rule.
* Review: maintainer chose the direction on 2026-11-22 and 2026-11-24; Decider: maintainer; prepared by Codex.
* Date: 2026-11-24; takes effect on merge.

## Context

Failed writing attempts damaged their lane, and failed calls stalled repairs (research and decisions of isolated-attempts, 2026-11-22 and 2026-11-24). A single runner entry also prevented other harnesses from reusing the lifecycle directly.

## Decision Drivers

* Protect the lane and later prompts while keeping attempts inexpensive.
* Make route switches visible and preserve the leak refusal boundary.
* Allow other harnesses to use the same protections.

## Considered Options

* Detached worktree per attempt: inexpensive local isolation, with shared Git state.
* Container per attempt: broader isolation at greater operational cost.
* Keep the current lane and stop on failed calls: no new lifecycle, but manual recovery remains.

## Decision

Chosen option: detached attempt worktrees through one reusable lifecycle. Implement, repair, draft and review use that lifecycle; its direct command entry enforces the same protections. Writing calls that fail fall through to the next declared route with saved state and a visible reason; leak refusals and restoration refusals stop. Repair is isolated in the first pull request; draft and implement follow after one night. Review is isolated; the review loop's routing is unchanged. The detailed boundaries and retention rules are in the change's spec.

## Consequences

* Attempts use extra worktrees and retained refs; cleanup removes those refs after merge.
* The shared environment needs read-only access, checksum checks and recovery; network and foreign reads remain outside this decision.
* The extra entry must maintain identical protections; the maintainer merges the decision pull request.

## Validation

* Structural and lifecycle tests plus `make verify` exercise the shared entry, isolation, failure handling and retention; the first rollout is observed for one night before the second.
