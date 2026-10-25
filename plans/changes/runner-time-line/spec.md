---
title: "Spec — runner-time-line"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-9wp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, time-accounting]
class: bounded
appetite: 2
adr_files: []
---

# Spec — runner-time-line

The runner records the measured time of completed implementation and repair
attempts, so a model need not supply a measurement it cannot take (bead
`coding-harness-9wp` — runner time accounting). Research: `research.md`.
Maintainer's answer: `decisions.md`, Q-1 — runner-owned measurement without
retrying red tests.

## Problem

On 2026-10-20, all six repair attempts described in `research.md` failed the
added-time-line check, although the orchestrator later verified and booked
their code. At this worktree's input commit `8e7f2cf`, `verify_attempt` still
requires a model-added line, and `implementation_prompt` asks a model without
command tools to measure one. The shared `run_attempts` loop can measure both
implementation and repair calls and their post-run checks itself.

Four of those six attempts also met load-sensitive tests on another branch;
that separate cause is outside this change.

## Terms

- **Completed attempt:** a model call that returns successfully and reaches
  the runner's post-run checks, including checks that reject it.
- **Accepted/rejected:** the result of those checks, before checkpointing;
  this label does not claim that a later commit succeeded.

## Acceptance criteria

1. When a completed `implement` or `repair` attempt passes its post-run checks
   without adding a model-written time entry, it remains eligible for its
   checkpoint.
   *Refuted by:* an otherwise passing attempt retries or fails solely because
   the model left the time section unchanged.

2. When a completed attempt reaches its post-run verdict, the runner adds
   exactly one runner-measured entry for that attempt under `## Time used`.
   *Refuted by:* no runner entry, duplicate runner entries, or an entry outside
   that section, on either an accepted or a rejected attempt.

3. When the runner measures a completed attempt, its span starts immediately
   before the model invocation and ends after the available post-run checks.
   *Refuted by:* controlled clock readings show that model execution,
   preparation, formatting or verification time was excluded, or time between
   attempts was included.

4. When the runner writes an entry, it identifies the measured date, start,
   end, elapsed span, verb, attempt number, route, model, accepted/rejected
   result and the words "measured by the runner".
   *Refuted by:* a missing or wrong field, an estimated span, or ambiguous
   endpoints for a span crossing midnight.

5. When a rejected completed attempt is followed by input restoration and a
   retry, its runner entry remains in the plan's time section.
   *Refuted by:* the retry or eventual checkpoint loses an earlier rejected
   entry, or replaces it with the later attempt's span.

6. When a runner entry is inserted, existing time records and content outside
   the time section remain intact apart from the usual document date stamp.
   *Refuted by:* an older entry disappears or changes, a following section
   receives the entry, or routing evidence is moved into the time section.

7. While the prompts and workflow describe runner-driven attempts, they assign
   time measurement to the runner.
   *Refuted by:* an operative implement or repair instruction still demands a
   model-measured entry, or the interactive session's own measured-span rule
   is removed.

8. If an existing non-time-line check rejects an attempt, that rejection
   retains its existing effect on checkpointing and subsequent calls.
   *Refuted by:* a red verification is rerun merely to obtain green, a failed
   attempt is checkpointed, or a missing initial time heading reaches a model.

## Non-goals

- Repairing the research-swarm branch's wall-clock tests, or adding a retry
  rule for red tests.
- Changing model routing, attempt limits, leak checks, red-first evidence,
  appetite stops or checkpoint policy.
- Recording draft, explore, review or preflight time; changing the rollback
  policy of failed model processes. Such a process is not a completed attempt.
- Removing interactive sessions' responsibility to read their clock and log
  their own spans.
- A design document or ADR: phase 2b does not run for this bounded change.

## Protected areas

`scripts/stage2_availability.py`, `model-endpoints.yaml`, `decisions/`,
`docs/adr/`, `AGENTS.md` and other changes' implementation files: their
availability, governance and routing contracts do not change here.

## Definition of Done

- `make verify` green, with deterministic clock tests and their planted faults.
- Documentation changes in the same pull request: `docs/WORKFLOW.md` and
  `prompts/04-implement.md`; no model declaration or ADR changes.
- Protected areas untouched and non-goals unbuilt, shown by the file list.
- The pull request names the runner-time-accounting work under bead
  `coding-harness-9wp`; the orchestrator owns closure after the separately
  scoped test repair, rather than this partial change closing it early.
- No live model calls are needed as special verification runs.

## Open decisions

None open.

- `[DETAIL]` Rejected completed attempts count toward time used; their lines
  say `rejected`, as already recorded in research. Process-failure rollback
  remains unchanged because it restores the clean baseline needed for rerun.
- `[DETAIL]` Use UTC endpoint timestamps with second precision and a measured
  elapsed duration; this makes midnight crossings readable and permits
  deterministic checks without depending on local timezone or machine speed.
- `[DETAIL]` The appetite is two hours of phase 4 including repairs: a bounded
  stop for this correction, not an estimate or an extension of another change.
