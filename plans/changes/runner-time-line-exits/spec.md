---
title: "Spec — runner-time-line-exits"
status: draft
implementation_status: none
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-9wp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, time-accounting]
class: bounded
appetite: 2
adr_files: []
---

# Spec — runner-time-line-exits

Every completed implementation or repair attempt retains its runner-measured
time entry even when a post-call check stops the run (bead
`coding-harness-9wp` — runner time accounting). Sources: `research.md` and
the maintainer's answered decision in `decisions.md`.

## Problem

The first post-call credential scan can refuse a successfully returned model
call before the runner computes its time entry. The phase-6 finding of
2026-10-22 reproduced this with zero calls to `time_entry` (remaining finding
F-6 of pull request #216, merged at `aed2999`). Research at `8acaa8b` also
identifies a refusal from `verify_attempt` before logging; inspection at
`2b16cb4` adds the post-call Git HEAD checks. Late credential refusal and an
unstartable verifier already log their rejected attempts and must keep doing so.

## Terms

- **Completed attempt:** an `implement` or `repair` model invocation that
  returns successfully; this includes an attempt stopped before verification.
  A `CallFailed` result, including an empty Codex answer, is not completion.
- **Verdict:** acceptance or rejection before checkpointing; acceptance does
  not promise that a later checkpoint succeeds.
- **Post-call exit:** any departure after completion and before checkpointing
  or another attempt, including a refusal, an unreadable Git HEAD or a moved HEAD.

## Acceptance criteria

1. When a completed attempt leaves its post-call processing, exactly one
   runner-measured entry for that attempt is present under `## Time used`
   before checkpointing, retrying or returning the failure.
   *Refuted by:* an accepted attempt, repairable rejection, first credential
   refusal, verifier refusal, late credential refusal, unstartable verifier,
   failed HEAD check or diagnostic refusal leaves zero or duplicate entries.

2. If a post-call condition stops the run without fallback, recording its
   rejected entry preserves that stop and its failure reason.
   *Refuted by:* logging starts another model or a checkpoint, hides the
   refusal, rewrites moved history, or leaves a detected credential unscrubbed.

3. When an entry records an early rejection, it retains the existing entry
   fields and runner clock measurement through the rejecting check.
   *Refuted by:* controlled clocks disagree with its UTC endpoints or monotonic
   duration, a field is missing or wrong, a rejection says accepted, or the
   span includes checkpointing or time between attempts.

4. When completion logging updates or restores the plan, trusted pre-call
   time records remain in order within their original section boundaries.
   *Refuted by:* a previous entry disappears, a rejected entry is lost on
   retry, model-written replacement time survives, or an entry lands in a
   following section.

5. If an early exit leaves a missing, unreadable or aliased plan destination,
   logging recovers the pre-call plan safely before recording the rejection.
   *Refuted by:* a recoverable plan loses its entry, a linked external target
   receives a write, or an unrecoverable write failure permits a checkpoint
   or fallback instead of reporting the logging failure with the original cause.

6. If an invocation fails before successful completion or preflight prevents
   it from starting, no completed-attempt time entry is added for it.
   *Refuted by:* a failed model process, empty Codex answer or rejected
   preflight receives a completed-attempt entry or different retry/rollback behavior.

## Non-goals

- Logging draft, explore, review, preflight or failed-model-process time.
- Changing routing, attempt limits, refusal rules, verification retries,
  credential-scan order, checkpoint policy or moved-HEAD recovery policy.
- Changing the time-entry format, interactive time accounting or the earlier
  change's artifacts; its historical criteria remain unchanged.
- A design document or ADR: phase 2b does not run for this bounded change.

## Protected areas

`prompts/`, `templates/`, `docs/WORKFLOW.md`, `docs/adr/`, `decisions/`,
`AGENTS.md`, `model-endpoints.yaml`, `.beads/` and other change folders:
the fix changes the existing runner implementation and its tests only.

## Definition of Done

- `make verify` green, with deterministic regression tests for each post-call
  exit and planted failures that demonstrate omitted or duplicate logging.
- Documentation changes: this change's research, spec and plan only; the
  runner maintains its findings and regenerates `plans/INDEX.md`.
- The pull request's file list respects the protected areas and non-goals.
- The pull request closes the runner-time-accounting bead
  `coding-harness-9wp`; its final commit carries `Closes-Bead: coding-harness-9wp`.
- Special runs: no live model calls; include regression evidence with its
  tested commit in the pull request.

## Open decisions

None open.

- [DETAIL] Keep failed invocations outside completion logging, matching the
  existing successful-return boundary and preserving their rollback contract.
- [DETAIL] Use the existing time format and a two-hour phase-4 appetite,
  repairs included: this is a bounded correction to the earlier time-accounting
  change, with no new format or architecture contract.
- [DETAIL] Include the already present HEAD and diagnostic refusal paths in
  the completion boundary because the maintainer required every post-call exit.
