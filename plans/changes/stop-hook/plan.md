---
title: "Plan — stop-hook"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-788
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, hooks, verification]
---

# Plan — stop-hook

```text
For you:     A changed Python tree gets a quick check at turn end; red blocks once and a timeout warns.
Done when:   Hook and runner tests and make verify pass, and a live session demonstrates pass, block and warning.
Appetite:    2 hours of phase 4 in total, repairs included; stop at the limit.
Not now:     Full verification in the hook, enforcement-gate or kit-travel changes, other hook events.
Pre-mortem:  suppose it failed: most likely because the quick check times out often enough that its warning becomes noise.
Starts unless you say stop.
```

## Execution boundary

This is a bounded change: no design phase or ADR. Stage 2 explored with `glm-5.3-flash`; no Stage-1 fallback was recorded. The runner implementation attempt may change only non-held paths below; the orchestrator writes the held `.claude/` and `README.md` paths after the accepted attempt. The attempt must pass its own checks before acceptance: tests requiring held paths and the notice ratchet are added or changed by the orchestrator after the hand finish.

## Files and steps

1. **Runner:** create `scripts/stop_hook.py` for the probe and `tests/test_stop_hook.py` for criteria 2–12, 14 and the marked-session case of 15, exercising the helper directly, including criteria 19–21. Use isolated git repositories and controlled subprocesses; exercise staged plus unstaged and index-only changes, untracked and deleted files, renames, spaces in paths, all import forms, both ruff commands, pytest exit 5, missing dependencies, timeout process cleanup, JSON warnings, the retry flag, runner marker, nested-worktree `cwd`, and fallback checkout. Include a failing pytest case reported before a later stall, with a second case that stalls without reporting a failure; assert the first blocks and the second warns. Assert exact exit codes, streams, paths and that input files remain unchanged; use a short positive budget for timeout tests.
2. **Runner:** implement the probe in `scripts/stop_hook.py`: discover both index and worktree changes plus untracked files with NUL-safe git output, retain deleted and both rename paths, resolve the Stop input `cwd` to its Git top level (fall back to `CLAUDE_PROJECT_DIR`), map covering tests as defined in the spec, check dependencies, run ruff without writes then selected pytest with `-x` and per-test output, and enforce one wall-clock budget with process-group cleanup. An observed red wins over timeout; no pytest call has an empty path list. Treat a streamed failed-test line as red even if pytest is killed before exit; no red before timeout produces the JSON warning. Invalid budget values warn once per probing invocation, on stderr for a block and in `systemMessage` otherwise. Output exit 2 and stderr for blocks, or JSON `systemMessage` for warnings.
3. **Runner:** change `scripts/stage2.py` at `run_work_model`: set a runner-owned `HARNESS_STAGE2_STOP_HOOK_SKIP=1` in the environment passed to every Claude work launch, after selecting either normal or GLM environment. Do not infer it from a caller-supplied value. Change `scripts/stage2_research_run.py` at `claude_command` to set the same marker for research roles. Change `tests/test_stage2.py` and `tests/test_stage2_research_dispatch.py` to exercise both work-launch routes and the research-role launch and prove the marker reaches the child; keep other environment and restrictions intact.
4. **Orchestrator, after the accepted attempt:** create executable `.claude/hooks/session-stop/check-tests-green.sh`, which handles a missing interpreter and the runner marker and launches `scripts/stop_hook.py`; add integration cases for criteria 1 and 13 and the README case to `tests/test_stop_hook.py`. Change `.claude/settings.json` by adding only a Stop command for the hook with `timeout: 90`; preserve the existing SessionStart and permissions. Change `README.md` to remove only the stop-hook promise from the not-built list. Change the phase-5 row of `AGENTS.md` and the gate line in `prompts/05-verify.md` to describe the limited comfort probe, retaining `make verify` as phase-5 evidence. Commit the delivered hook and wiring before writing the notice: a commit cannot name its own hash.
5. **Orchestrator:** change `tests/test_workflow_entry.py` to move the hook from the notice's absent list to supplied and add checks for the notice's dated delivery commit, comfort paragraph and corrected doctrine sites. Change `docs/WORKFLOW.md` to rewrite the comfort paragraph per criterion 17, the phase table, verdicts paragraph and map per criterion 22, and cite the dated preceding delivery commit containing the hook in the notice while retaining the validator as absent. Change the stop-hook row in `docs/testing.md` to describe the limited probe. Change `plans/changes/stop-hook/findings.md` to record the live session evidence with date and commit, update this plan's ledger to written tests and fill `## Time used`; regenerate `plans/INDEX.md` using `python3 scripts/plans_registry.py --index`. No file is deleted.

## Verification

After the orchestrator's hand finish and notice update:

```sh
.venv/bin/python3 -m pytest tests/test_stop_hook.py tests/test_workflow_entry.py tests/test_stage2.py tests/test_stage2_research_dispatch.py tests/test_omnigent_deny_layers.py tests/test_merge_guard.py -q
make verify
```

Also observe a real Claude Code session at the implementation commit: green probe passes, a planted failure blocks with both relevant names, and a forced timeout shows the warning. Restore the planted file after the observation and record evidence in `findings.md`.

## Criterion ledger

- 1: not yet written tests/test_stop_hook.py::test_settings_wire_executable_hook_with_timeout — missing hook, incorrect timeout, or altered existing settings
- 2: not yet written tests/test_stop_hook.py::test_unchanged_tree_starts_no_probe — a clean or Markdown-only tree starts a probe or blocks
- 3: not yet written tests/test_stop_hook.py::test_green_probe_covers_all_changed_states — a changed path is omitted or a green probe blocks
- 4: not yet written tests/test_stop_hook.py::test_ruff_red_blocks_without_writing — format or lint red passes, names the wrong file or rewrites it
- 5: not yet written tests/test_stop_hook.py::test_ruff_red_stops_before_pytest — pytest runs after red or timeout overrides the red
- 6: not yet written tests/test_stop_hook.py::test_failing_test_blocks_with_both_paths_on_stderr — exit or either named path is wrong
- 7: not yet written tests/test_stop_hook.py::test_deleted_python_runs_covering_tests_without_ruff_path — deletion skips tests or reaches ruff
- 8: not yet written tests/test_stop_hook.py::test_covering_test_selection_includes_dotted_imports — a matching import is missed or a substring misselected
- 9: not yet written tests/test_stop_hook.py::test_empty_covering_set_never_runs_bare_pytest — pytest starts without paths
- 10: not yet written tests/test_stop_hook.py::test_pytest_nothing_collected_is_green — exit 5 blocks
- 11: not yet written tests/test_stop_hook.py::test_timeout_warns_visibly_and_kills_process_group — timeout blocks, lacks JSON warning or leaves a process-group member
- 12: not yet written tests/test_stop_hook.py::test_invalid_budget_warns_and_uses_default — invalid value applies, warning is missing or red is suppressed
- 13: not yet written tests/test_stop_hook.py::test_missing_probe_dependency_blocks_with_fix — missing Python, ruff or pytest passes or fix is absent
- 14: not yet written tests/test_stop_hook.py::test_active_stop_passes_with_visible_warning — retry runs probe, blocks or lacks JSON warning
- 15: not yet written tests/test_stage2.py::test_work_model_marks_claude_sessions_to_skip_stop_hook — either runner launch lacks the marker
- 15: not yet written tests/test_stage2_research_dispatch.py::test_research_claude_launch_marks_session_to_skip_stop_hook — the research role does not receive the marker
- 15: not yet written tests/test_stop_hook.py::test_runner_marker_skips_probe_only_for_marked_session — marked session probes or ordinary session skips
- 16: tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands — wrong list, missing validator or reference to a commit without the hook
- 17: not yet written tests/test_workflow_entry.py::test_stop_hook_comfort_paragraph_records_probe — any decided probe fact is absent
- 18: not yet written tests/test_stop_hook.py::test_readme_not_built_yet_names_no_stop_hook — the missing list still names the hook
- 19: not yet written tests/test_stop_hook.py::test_reported_pytest_failure_blocks_even_when_probe_times_out — an already reported failure is lost when the process stalls
- 20: not yet written tests/test_stop_hook.py::test_stop_cwd_selects_nested_checkout — a changed worktree is missed in favor of the project checkout
- 21: not yet written tests/test_stop_hook.py::test_missing_or_nongit_cwd_falls_back_to_project — the fallback checkout is not inspected
- 22: not yet written tests/test_workflow_entry.py::test_stop_hook_doctrine_describes_limited_probe — any doctrine site promises every red tree blocks

## Do not touch

The enforcement gate list and its runners, CI, kit manifest and probe, provenance, user-level hooks, other prompts, templates, model endpoints and tracker stay untouched. Preserve `.claude/settings.json` SessionStart and permissions. The only runner changes are the child-session markers.

## Time used

2026-11-21 15:36:39–15:39:53 UTC, 195 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:48:26–15:51:13 UTC, 167 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
