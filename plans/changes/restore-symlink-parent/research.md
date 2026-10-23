---
title: "Research — restore-symlink-parent"
status: draft
implementation_status: none
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-10w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, runner, restore, symlink]
---

# restore-symlink-parent — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session itself at `origin/main` `7586f1a`
(2026-10-23): the scope is one reproduced finding, so no separate
exploration call was made.

## The finding

A runner audit at `378879a` (2026-10-21) reproduced, without model calls,
that the restore of a failed attempt followed a parent directory the model
had replaced by a symbolic link and overwrote a file outside the worktree
before a later safety check stopped the run. The code then restored each
differing input inline in the attempt loop with
`path.parent.mkdir(parents=True, exist_ok=True)` and `path.write_bytes(...)`,
which follow a symlinked parent.

## What exists today

Read in `scripts/stage2.py` at `7586f1a`:

- `restore_work_input` (added by the `runner-time-line` change, commit
  `4e6d022`) walks each input's parents from the worktree outward; a parent
  that is a symlink or a non-directory is **unlinked and recreated as a
  directory**, then the input is rewritten. It no longer writes through the
  link, so the outside write of the audit does not reproduce.
- It is called on the retry restore in the attempt loop (two places, before
  the next attempt) and when the plan's time entry is persisted
  (`persist_time_entry`).
- `tests/test_stage2.py` covers a symlinked plan parent ("parent-alias"
  case): the run refuses for another reason, the outside directory stays
  unchanged and the plan parent is a real directory again.
- `restore_baseline` (after a failed model call) uses `git restore` and
  `git clean` and unlinks gitignored paths the attempt created; whether a
  created path below a symlinked parent can reach it was not read.

## The gap to the maintainer's direction

The maintainer decided on 2026-10-22 (`decisions.md`, Q-1): when a restore
path resolves outside the worktree, the runner refuses and stops, writes
nothing, names the path and ends the run without a fallback model, like a
leak-check BLOCK. Today the runner silently replaces the alias and goes on
to the next attempt or route. The change makes that case a stop.

## Open questions

None for the maintainer: the direction is decided (`decisions.md`, Q-1).
Whether `restore_baseline` needs the same check is for the spec to settle
from the code.

## Draft investigation — 2026-10-23

Read at input commit `a20d786`; these are code-inspection findings, not a new
executed reproduction:

- `restore_baseline` computes tracked changes and newly created ignored
  paths, then runs `git restore` and `git clean` before deleting the ignored
  paths with `unlink` or `rmtree`. It has no parent-containment preflight.
  Its ignored-path deletion and empty-parent removal therefore belong to
  the same restoration boundary as input recovery.
- `run_attempts` restores input batches before retrying and when recovering
  the plan directory; it also restores repair findings on several error
  paths. A per-file check alone could restore an earlier safe input before
  discovering an unsafe later input.
- `persist_time_entry` calls `restore_work_input` on retries and rejected
  attempts. Its broad exception handler wraps `Refused` as `CallFailed`.
  The completed-attempt exception handler in `run_attempts` can invoke it
  after another refusal. Both boundaries need to preserve the terminal
  restoration refusal without another write.
- Existing tests explicitly expect recovery of an external parent alias:
  `test_runner_retry_replaces_parent_alias_without_following` and the
  `parent-alias` case of
  `test_runner_early_refusal_recovers_time_destination_safely`. Those
  expectations must change for the maintainer's decided stop; ordinary
  missing-parent, leaf-alias and hard-link recovery remain separate cases.
- `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent
  at this commit. The plan uses `prompts/03-plan.md` and the existing plan
  form; interview, criterion-ledger and registry checks remain available.
