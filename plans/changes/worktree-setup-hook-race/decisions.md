---
title: "Decisions — worktree-setup-hook-race"
category: decisions
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
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: antigravity, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, worktree, tests]
---

# Decisions — worktree-setup-hook-race

Phase-1a record for `worktree-setup-hook-race` (bead `coding-harness-1ba3`, parent change `plans/changes/worktree-setup-hook/spec.md`).

## SKIP · interview

status: skipped
reason: "Bounded CI-flake fix discovered from merge-group run 45884026286 (PR #467, 2026-11-26) and run autonomously under the maintainer's bounded standing grant (2026-11-25): no product or architectural choice is open. Fix both `.beads/hooks/post-checkout` (compute `_ls_deadline` after `_ls_trusted` succeeds, immediately before the first setup step, keeping the managed Beads block untouched and avoiding sub-second clock dependencies) and `tests/test_worktree_setup_hook.py` (use a >=2s timeout budget in both timeout/budget tests so a whole-second `date +%s` boundary never exhausts the budget before `make venv` starts, and tighten assertions so `test_a_step_never_started_names_the_step_that_used_the_budget` deterministically hits the `not started` / `used up by make venv` path while `test_setup_timeout_stops_and_reports_step_and_limit` deterministically hits the step timeout path)."
