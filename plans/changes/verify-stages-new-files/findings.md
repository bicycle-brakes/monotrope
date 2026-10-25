---
title: "Findings — verify-stages-new-files"
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
tags: [findings, stage-2]
---

# Findings — verify-stages-new-files

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: both
cases of the new test failed before the edit (`git ls-files` during
`make verify` lacked `scripts/new_tool.py`). All 923 tests in
`test_stage2.py`, `test_stage2_runs.py` and `test_kit.py` pass except the
root-only one.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- `restore_baseline` runs `git restore --staged --worktree`, which drops
  an intent-to-add entry whose path the baseline lacks, and `git clean`
  removes the file; no entry outlives a restore.
- When a run fails without a restore, the entries stay; the next run's
  pre-existing-change check lists those paths as it listed the untracked
  files before, so nothing new slips through.
- `changed_paths` and the credential scans list the same paths as before:
  an intent-to-add file is still a change against `HEAD`.
