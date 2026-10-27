---
title: "Research — tolerate-derived-leftovers"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-b5w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, runner]
---

# tolerate-derived-leftovers — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `f8a6b33`
(2026-10-25).

## The finding

After a failed `implement`, `repair` or `draft` run, the runner's own
writes stay in the worktree: the rendered `plans/INDEX.md` and the
`updated:` stamps from `prepare_derived`. The next run of the same verb
refuses them as "pre-existing changes outside this change's findings.md".
The orchestrator restores them by hand today, and tests paper over it
with `clear_derived_leftovers` (bead coding-harness-b5w; found by
review-loop round 3 on change `codex-drafts`, row L3-3, 2026-10-13).

## What exists today

Read in `scripts/stage2.py` at `f8a6b33`:

- `implement`, `draft` and `repair` each carry the same pre-existing-change
  refusal over `changed_paths(root) - {findings.md}`.
- `prepare_derived` stamps the `updated:` line of every changed held
  document and re-renders `plans/INDEX.md` before every verify.
- In this test world the renderer's import also leaves `__pycache__`
  bytecode under `scripts/` (the real repository ignores it).

## Sources

- Bead coding-harness-b5w and its interview note of 2026-10-16.
- `scripts/stage2.py`: `implement`, `draft`, `repair`, `prepare_derived`;
  `tests/test_stage2.py` `clear_derived_leftovers`.
