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

Bounded phase-1a decision for `worktree-setup-hook-race` (bead `coding-harness-1ba3`, parent change `plans/changes/worktree-setup-hook/spec.md`).

## Q-1 · Scope of the 1-second integer-second race fix

asked: 2026-11-27
answer: "Fix both the hook's deadline start and the two budget tests: in `.beads/hooks/post-checkout`, compute `_ls_deadline` after `_ls_trusted` succeeds (immediately before the first setup step runs) so trust verification never eats into the step budget; in `tests/test_worktree_setup_hook.py`, give both timeout/budget tests a >=2s timeout budget (guaranteeing >=1.0s real margin across any whole-second `date +%s` boundary) and tighten assertions so `test_a_step_never_started_names_the_step_that_used_the_budget` deterministically exercises the post-`make venv` not-started path (`used up by make venv`) and `test_setup_timeout_stops_and_reports_step_and_limit` deterministically exercises the step timeout path. Keep the managed Beads block untouched and leave sub-second clock dependencies out of `.beads/hooks/post-checkout`."
answered_by: orchestrator (bounded standing grant, 2026-11-25)
status: answered
context: |
  Topic: eliminating the 1-second integer-second race in `.beads/hooks/post-checkout` and `tests/test_worktree_setup_hook.py` (CI failure 45884026286).
  Intention: stop random merge-queue and CI flakes on worktree setup timeout tests without adding external runtime dependencies to the POSIX shell hook.
  Today: `_lane_setup` computes `_ls_deadline=$(($(date +%s) + _ls_limit))` before `_ls_trusted`, and both tests set `HARNESS_LANE_SETUP_TIMEOUT=1`, so crossing a whole-second boundary during `_ls_trusted` makes `_ls_left <= 0` before `make venv` starts (`used up by the setup`).
  Repository change: `.beads/hooks/post-checkout` (move `_ls_deadline` after `_ls_trusted`, outside the managed Beads block) and `tests/test_worktree_setup_hook.py` (2s+ budget & tightened deterministic assertions).
  Architecture change: none (bounded fix, no ADR change).

In the context of whole-second timeout arithmetic in `.beads/hooks/post-checkout` and its budget tests, facing wall-clock boundary flakes under `HARNESS_LANE_SETUP_TIMEOUT=1`, we decided to start `_ls_deadline` after `_ls_trusted` and raise the two tests' timeout budget to >=2s with tightened assertions, to achieve deterministic CI runs without adding sub-second shell dependencies, accepting ~1 second of additional wall-clock runtime in those two tests. — 2026-11-27
