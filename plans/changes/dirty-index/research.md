---
title: "Research — dirty-index"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-0c8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, runner, dirty-tree]
---

# dirty-index — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `f8a6b33`
(2026-10-25). The scope is one reproduced finding, so no separate
exploration call was made.

## The finding

A runner audit at `378879a` (2026-10-21, the maintainer's other session)
reproduced without model calls: a change that exists only in the index
(`git add`, then the working file put back to its committed content) is
not seen by the runner's pre-existing-change check. The run starts, and its
checkpoint commit (`git add -A`) replaces the staged content with the working
file, so the staged change is lost (bead coding-harness-0c8).

## What exists today

Read in `scripts/stage2.py` at `f8a6b33`:

- `changed_paths(root, env, against="HEAD")` runs
  `git diff --no-renames --name-only -z <against>` plus
  `git ls-files --others --exclude-standard`. `git diff <commit>` compares
  the **working tree** with the commit; the index is not consulted. A path
  whose index entry differs from `HEAD` while its working file equals `HEAD`
  is therefore absent from the result.
- `implement`, `draft` and `repair` each refuse with "the worktree has
  pre-existing changes outside this change's findings.md" when
  `changed_paths(root)` holds anything but the change's `findings.md`.
- `checkpoint` stages with `git add -A` and commits; `git add -A` writes the
  working file over the index entry.
- Other callers of `changed_paths` (the touched-path scans after an attempt,
  `restore_baseline`'s listing, the commit guard, the whole-change listing)
  ask the same question — which paths differ from a commit — and an
  index-only difference is a difference for each of them.

## Options

1. Widen `changed_paths` with `git diff --cached --name-only <against>`:
   every caller sees index-only changes; the pre-existing check refuses them.
2. A separate index check only in the three pre-checks: narrower, but the
   other callers keep the blind spot (a post-attempt scan would miss a path an
   attempt staged and reverted).

Option 1 is the smaller code change and closes the blind spot everywhere.
Its only behaviour change is that more paths are listed; a path listed by
the index diff and by the working-tree diff stays one entry (a set).

## Sources

- Bead coding-harness-0c8 (description and repro summary).
- `scripts/stage2.py` at `f8a6b33`: `changed_paths`, `implement`, `draft`,
  `repair`, `checkpoint`.
- `git diff` documentation: `git diff <commit>` compares the working tree
  with the commit; `--cached` compares the index with it.
