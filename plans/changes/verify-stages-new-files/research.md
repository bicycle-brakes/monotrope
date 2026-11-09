---
title: "Research — verify-stages-new-files"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-fdz
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, verify]
---

# verify-stages-new-files — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `f8a6b33`
(2026-10-25).

## The finding

On change `adr-owning-change` (2026-10-13), a Sonnet attempt under
`--stage2-off` failed only the leerprobe gate. `scripts/kit/probe.py`
builds its foreign repository from `git ls-files`, and the runner's
`verify_attempt` runs `make verify` before the checkpoint stages anything,
so the attempt's new script (`scripts/adoption.py`) was absent there. The
importing test module failed collection, and the gate reported a
misleading "1 red case" and "35 REIST_NICHT entries have no case".
Staging the files made it green with no code change (bead
coding-harness-fdz).

## What exists today

Read in `scripts/stage2.py` at `f8a6b33`:

- `verify_attempt` stamps and renders (`prepare_derived`), formats
  (`format_step`), then launches `make verify`; nothing is staged.
- `checkpoint` stages with `git add -A` only after a passing verify.
- `restore_baseline` runs `git restore --staged --worktree` and
  `git clean`, so an index entry for a new file goes with the file.

## Sources

- Bead coding-harness-fdz and its interview note of 2026-10-16.
- `scripts/stage2.py`: `verify_attempt`, `checkpoint`, `restore_baseline`;
  `scripts/kit/probe.py`.
