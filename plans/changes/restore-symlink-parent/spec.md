---
title: "Spec — restore-symlink-parent"
status: draft
implementation_status: partial
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-10w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, restore, symlink]
class: bounded
appetite: 5
adr_files: []
---

# Spec — restore-symlink-parent

The runner refuses restoration through a parent resolving outside its
worktree, leaves that recovery unwritten and stops without another model
(bead `coding-harness-10w` — refuse unsafe restoration parents).
Sources: `research.md` and the maintainer's answered record in `decisions.md`.

## Problem

The audit at `378879a` on 2026-10-21 reproduced an outside write during
restoration of a failed attempt. At the research baseline `7586f1a`,
`restore_work_input` instead removes a symbolic-link parent and recreates a
directory, preventing that reproduced write but continuing the run. This
does not meet the maintainer's 2026-10-22 decision to refuse without writing
and stop without fallback. Inspection at `a20d786` also finds unguarded
baseline cleanup and exception-time logging paths that can bypass or undo
a restoration refusal (`research.md`, draft investigation).

## Terms

- **Recovery operation:** restoration of an implementation or repair
  attempt's snapshotted inputs or findings, recovery for time persistence,
  or failed-call baseline rollback, including ignored-path cleanup.
- **Unsafe parent:** an ancestor below the worktree root whose resolved
  location is outside the canonical worktree root. Relative links, links at
  any ancestor depth and links to missing external targets count too.
- **Recovery batch:** every destination a recovery operation can mutate;
  checking a safe prefix of the batch does not authorize partial recovery.

## Acceptance criteria

1. When any destination in a recovery batch has an unsafe parent, the
   operation refuses before its first filesystem mutation.
   *Refuted by:* a preceding safe destination, the alias itself, an external
   sentinel or a cleanup target is created, rewritten, removed or stamped
   before the unsafe destination stops the batch.

2. If unsafe-parent recovery is refused, the runner terminates as a refusal
   without another attempt, a fallback model or a checkpoint.
   *Refuted by:* the command succeeds, returns an ordinary repairable
   failure, starts another model, or advances HEAD with a runner checkpoint.

3. When the runner refuses unsafe-parent recovery, its standard-error
   diagnostic identifies the affected worktree-relative destination and
   says that restoration was refused because its parent escapes the worktree.
   *Refuted by:* standard error omits the path or reason, or reports only a
   generic time-write or model-call failure.

4. If a destination's parent chain cannot be resolved, recovery refuses
   without mutation and ends the run with a diagnostic naming that path.
   *Refuted by:* a resolution error or symlink loop permits recovery,
   another model or a checkpoint, or escapes as an unnamed traceback.

5. While a restoration safety refusal propagates, enclosing recovery,
   diagnostic persistence and time finalization perform no filesystem writes.
   *Refuted by:* a handler replaces the alias, restores findings, appends a
   time entry, saves an attempt or runs further cleanup after the refusal.

6. When parent chains are resolvable and remain inside the worktree,
   recovery retains the existing behavior for ordinary files, missing
   directories, leaf aliases and hard links.
   *Refuted by:* a safe retry loses trusted input bytes or measured time,
   ordinary failed-call rollback stops working, or detaching a leaf alias or
   hard link changes its external target.

## Non-goals

- Changing routing, attempt limits, verification or checkpoint policy for
  runs without a restoration safety refusal.
- Rejecting a leaf-file alias solely because its target is external when
  its parents are contained and existing recovery safely detaches the leaf.
- OS-level isolation or race-proofing against concurrent filesystem mutation.
- Extending this fix to draft, review or unrelated runner verbs.
- A design document or ADR: phase 2b does not run for this bounded change.

## Protected areas

`AGENTS.md`, `prompts/`, `templates/`, `docs/WORKFLOW.md`, `docs/adr/`,
`decisions/`, `model-endpoints.yaml`, `.beads/` and other change folders:
the fix applies the existing maintainer decision within the runner and its tests.

## Definition of Done

- `make verify` green, with deterministic regressions for the unsafe paths
  and safe recovery controls; new refusal tests are shown red before the fix.
- Documentation: this change's `research.md`, `spec.md` and `plan.md`;
  the runner maintains `findings.md` and regenerates `plans/INDEX.md`.
- The pull request's file list respects the protected areas and non-goals.
- The pull request closes the unsafe-parent-restoration bead
  `coding-harness-10w`; its final commit carries `Closes-Bead: coding-harness-10w`.
- Special runs: local stand-ins only; regression evidence names its tested
  commit in the pull request, with no live model calls needed by the tests.

## Open decisions

None open; the maintainer's refusal direction is already answered.

- [DETAIL] Check the whole recovery batch before mutation, including baseline
  and ignored cleanup: a per-file check would leave a partially written recovery.
- [DETAIL] Treat unresolvable parents as unsafe because containment cannot be
  established; use the existing refusal exit code, 2, for both cases.
- [DETAIL] A safety refusal takes precedence over persisting time or findings:
  writing either would contradict the maintainer's explicit no-write stop.
- [DETAIL] Preserve safe leaf-alias recovery because the answered question
  concerns replaced parent directories, and leaf detachment needs no write
  through the external target.
- [DETAIL] The current phase-4 appetite is five hours, repairs included, for
  this bounded correction; reaching it stops implementation rather than widening
  the change. The original appetite was two hours; the maintainer raised it on
  2026-10-24 (conversation), after the review loop ran until clean past those
  first two hours.
