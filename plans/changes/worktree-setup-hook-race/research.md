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
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-27", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, worktree, tests]
class: bounded
---

# Research — worktree-setup-hook-race

Harden the 1-second integer-second race in `tests/test_worktree_setup_hook.py::test_a_step_never_started_names_the_step_that_used_the_budget` (bead `coding-harness-1ba3`).

## Problem statement

In CI merge-group run `45884026286` (PR #467, 2026-11-26), `tests/test_worktree_setup_hook.py::test_a_step_never_started_names_the_step_that_used_the_budget` failed because setting `HARNESS_LANE_SETUP_TIMEOUT="1"` raced with whole-second `date +%s` arithmetic in `.beads/hooks/post-checkout`: when `_ls_deadline` was computed just before a wall-clock second boundary, `_ls_trusted` crossed into the next second and tripped the timeout before the first step (`venv`) started.

Stage-2 call, 2026-11-27: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1301 files, 6096 commits, 12 rules.

Stage-2 call, 2026-11-27: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1301 files, 6097 commits, 12 rules.

## Runner exploration — 2026-11-27

Phase 1 exploration for `worktree-setup-hook-race`, as prose for `research.md`. I have not written the file; the runner does that.

**What exists today**

- **The race site.** `.beads/hooks/post-checkout`, function `_lane_setup`, computes `_ls_deadline=$(($(date +%s) + _ls_limit))` as whole seconds. Then it runs `_ls_trusted` (two `git` calls: `rev-parse` and `merge-base --is-ancestor`) before the first `_ls_step "make venv"`. In `_ls_step`, `_ls_left=$((_ls_deadline - $(date +%s)))` is checked; if it is `<= 0`, the step is reported as not started.
- **The message for the first step.** In `_ls_step`, the not-started message reads `"<label> not started: the <limit>s limit (HARNESS_LANE_SETUP_TIMEOUT) was used up by ${_ls_prev:-the setup}"`. `_ls_prev` is empty for the first step, so the message for `make venv` says "used up by the setup", never "used up by make venv".
- **The failing assertion.** `tests/test_worktree_setup_hook.py::test_a_step_never_started_names_the_step_that_used_the_budget` (fixture `lane`) runs with `HARNESS_LANE_SETUP_TIMEOUT="1"` and `STUB_MAKE_SLEEP="3"`, and asserts `"not started" in text and "used up by make venv" in text or "make venv timed out" in text`. Python parses `and` before `or`, so the test passes only through the second branch, "make venv timed out", or through a "not started" line that names `make venv`. The first branch cannot match for the first step. So the test is green only when `make venv` actually starts and the watchdog or `timeout` path reports it.
- **Timing window.** The deadline is set at `_lane_setup`, before `_ls_trusted` and before the first `_ls_step`. The whole window is the duration of those git calls plus the perl check. If a wall-clock second boundary falls inside it, `_ls_left` is 0 at the first step and the test gets "not started … used up by the setup", which fails both branches. This matches the mechanism in the bead's problem statement.
- **The other test in the same window.** `test_setup_timeout_stops_and_reports_step_and_limit` (criterion 11, same file) also uses limit 1 and `STUB_MAKE_SLEEP="5"`. It asserts `"make venv"` and `\b1s\b` in the single failure line. The not-started line also satisfies both checks, so this test passes under the race without exercising the timeout path it names.
- **Other `date +%s` uses.** `_ls_step` at the watchdog check (after `wait`) and the `rc == 124` check in `_ls_step` both compare whole seconds against `_ls_deadline`. No fractional-time source (`%N`, `monotonic`, `date +%s.%N`) appears anywhere in `.beads/hooks/`.
- **The spec.** `plans/changes/worktree-setup-hook/spec.md` (criterion 11, `[DETAIL]` on the limit) says the setup limit is `HARNESS_LANE_SETUP_TIMEOUT`, default 600, and that a value of `0`, negative or non-numeric falls back to 600 with one warning (decisions S-8). It does not specify the clock's resolution or how a first step is treated when the limit is already spent.
- **Findings for the parent change.** `plans/changes/worktree-setup-hook/findings.md` records the L2-20 row for this test as a taken row, with its status and "broke a test" cells in the loop record outside the worktree (`/Users/mikypiky/.local/state/coding-harness/stage2/worktree-setup-hook@c00d7e82/loop.md`). That file is outside the allowed read scope, so I did not open it.
- **Test file.** The whole test file is `tests/test_worktree_setup_hook.py`; the hook is loaded from the versioned `.beads/hooks/post-checkout` and copied into a shared hooks directory by the `lane` fixture.

**What is unclear**

- **The CI run.** The header claim that merge-group run `45884026286` (PR #467, 2026-11-26) failed on this test is not verifiable in the tree. It comes from the research header only; the CI log is not in the repository.
- **Frequency.** How often the window is hit is not measured. The window is the duration of the git calls before the first step, so the probability depends on that duration; I did not time it.
- **Whether the hook is run by git here.** Whether `core.hooksPath` points at `.beads/hooks` in this checkout is not read; the explorer has no `git config` access. The test sets the path itself, so this does not block the question of the test's behaviour.
- **Spec for this change.** There is no `spec.md` in `plans/changes/worktree-setup-hook-race/`; only `research.md` exists. Whether a fix is test-only or touches the hook's `_ls_deadline` arithmetic is not decided anywhere in the tree.
- **The research header.** `plans/changes/worktree-setup-hook-race/research.md` has no `neighbours:` key, although the rules require one. Its stage-2 call lines are duplicated (6096 and 6097 commits). Its "Runner exploration" heading is also empty.
- **Git history.** I cannot run `git log` with my read-only tools, so I did not check when the `date +%s` arithmetic was introduced or whether a commit on `main` changed it.

**Files a change would have to touch (as found; no choice made)**

- `tests/test_worktree_setup_hook.py`: function `test_a_step_never_started_names_the_step_that_used_the_budget` (the disjunction and the limit); function `test_setup_timeout_stops_and_reports_step_and_limit` (same window, weak assertion).
- `.beads/hooks/post-checkout`: function `_lane_setup` (where `_ls_deadline` is set) and `_ls_step` (the `_ls_left` check). Its managed Beads block is outside the change, and `test_managed_beads_block_matches_origin_main` pins that block.
- `plans/changes/worktree-setup-hook-race/research.md`, the change's own folder (no spec, plan or decisions yet).

**Open questions for the runner**

1. Does the maintainer want the fix in the test only, in the hook's arithmetic only, or both? That decides the spec.
2. Should `worktree-setup-hook` be listed as a neighbour in the `neighbours:` header? It is the parent change and the only one that names the same functions.
