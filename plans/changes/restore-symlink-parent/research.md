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
