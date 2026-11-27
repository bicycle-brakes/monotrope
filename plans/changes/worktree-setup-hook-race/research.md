---
title: "Research — worktree-setup-hook-race"
category: research
status: draft
implementation_status: none
date: 2026-11-27
created: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-1ba3
owner: Data Architect
provenance: human-written
produced_by: {kind: human, name: "orchestrator"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, worktree, tests]
class: bounded
---

# Research — worktree-setup-hook-race

Harden the 1-second integer-second race in `tests/test_worktree_setup_hook.py::test_a_step_never_started_names_the_step_that_used_the_budget` (bead `coding-harness-1ba3`).

## Problem statement

In CI merge-group run `45884026286` (PR #467, 2026-11-26), `tests/test_worktree_setup_hook.py::test_a_step_never_started_names_the_step_that_used_the_budget` failed because setting `HARNESS_LANE_SETUP_TIMEOUT="1"` raced with whole-second `date +%s` arithmetic in `.beads/hooks/post-checkout`: when `_ls_deadline` was computed just before a wall-clock second boundary, `_ls_trusted` crossed into the next second and tripped the timeout before the first step (`venv`) started.
