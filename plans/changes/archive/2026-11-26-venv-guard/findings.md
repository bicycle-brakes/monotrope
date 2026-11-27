---
title: "Findings — venv-guard"
category: findings
status: accepted
implementation_status: done
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-s55e
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — venv-guard

Stage-2 call, 2026-11-17: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1111 files, 4545 commits, 12 rules.

Stage-2 call, 2026-11-17: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1114 files, 4551 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/venv-guard/plan.md` +8 -8
> - `plans/changes/venv-guard/spec.md` +1 -1
> - `scripts/adoption.py` +5 -1
> - `scripts/archive_closed_changes.py` +5 -1
> - `scripts/check_adr_answers.py` +5 -1
> - `scripts/check_frontmatter_current.py` +5 -1
> - `scripts/check_interview_minimums.py` +5 -1
> - `scripts/check_question_context.py` +5 -1
> - `scripts/check_research_currency.py` +5 -1
> - `scripts/check_research_handoff.py` +5 -1
> - `scripts/ci_gates.py` +10 -1
> - `scripts/harness.py` +8 -4
> - `scripts/kit/manifest.yaml` +3 -0
> - `scripts/kit/probe.py` +5 -2
> - `scripts/omnigent_policy.py` +4 -0
> - `scripts/plans_registry.py` +5 -1
> - `scripts/pr_sync.py` +6 -2
> - `scripts/ramp_valves.py` +4 -0
> - `scripts/research_capture.py` +5 -1
> - `scripts/research_census.py` +5 -1
> - `scripts/stage2.py` +5 -1
> - `scripts/stage2_availability.py` +9 -5
> - `scripts/stage2_go.py` +5 -1
> - `scripts/stage2_research_limits.py` +5 -1
> - `scripts/stage2_research_refs.py` +5 -1
> - `scripts/stage2_session.py` +6 -2
> - `scripts/venv_guard.py` +152 -0
> - `tests/test_venv_guard.py` +489 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_venv_guard.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
>
> ==================================== ERRORS ====================================
> __________________ ERROR collecting tests/test_venv_guard.py ___________________
> ImportError while importing test module '/Users/mikypiky/coding-harness/.claude/worktrees/venv-guard/tests/test_venv_guard.py'.
> Hint: make sure your test modules/packages have valid Python names.
> Traceback:
> /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/importlib/__init__.py:90: in import_module
>     return _bootstrap._gcd_import(name[level:], package, level)
> tests/test_venv_guard.py:41: in <module>
>     import probe  # noqa: E402
> E   ModuleNotFoundError: No module named 'probe'
> =========================== short test summary info ============================
> ERROR tests/test_venv_guard.py
> 1 error in 0.42s
> ```

Stage-2 call, 2026-11-17: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1116 files, 4561 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/venv-guard/plan.md` +8 -8
> - `tests/test_venv_guard.py` +1 -0
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/ci_gates.py` is shared execution infrastructure
> - `make verify` exited 2
> templates/design.md:16 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/design.md:97 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Added"]
> templates/design.md:101 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Changed"]
> templates/design.md:105 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Removed"]
> templates/findings.md:18 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/findings.md:45:5 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:9 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:13 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:21 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:45:25 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> templates/findings.md:46:7 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:15 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:22 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:54 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:99 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:46:106 error MD060/table-column-style Table column style [Table pipe does not align with header for style "aligned"]
> templates/findings.md:63 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Severity"]
> templates/findings.md:71 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Dimension"]
> templates/findings.md:77 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Origin"]
> templates/findings.md:84 error MD036/no-emphasis-as-heading Emphasis used instead of a heading [Context: "Markers that override everythi..."]
> templates/findings.md:111:81 error MD013/line-length Line length [Expected: 80; Actual: 91]
> templates/findings.md:112:81 error MD013/line-length Line length [Expected: 80; Actual: 101]
> templates/findings.md:126:81 error MD013/line-length Line length [Expected: 80; Actual: 125]
> templates/handover.md:20:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:20:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> templates/handover.md:20:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> templates/handover.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 162]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/repo-settings.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 83]
> templates/repo-settings.md:23:81 error MD013/line-length Line length [Expected: 80; Actual: 85]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> templates/spec.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 122]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-11-18: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1116 files, 4561 commits, 12 rules.

Stage-2 call, 2026-11-18: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Sonnet fallback call failed at the Claude usage limit (23:18Z); two GLM Flash post-run checks red · leak check clean over 1114 files, 4566 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/venv-guard/plan.md` +7 -7
> - `scripts/adoption.py` +1 -0
> - `scripts/archive_closed_changes.py` +1 -0
> - `scripts/check_adr_answers.py` +1 -0
> - `scripts/check_frontmatter_current.py` +1 -0
> - `scripts/check_interview_minimums.py` +1 -0
> - `scripts/check_question_context.py` +1 -0
> - `scripts/check_research_currency.py` +1 -0
> - `scripts/check_research_handoff.py` +1 -0
> - `scripts/ci_gates.py` +1 -0
> - `scripts/export/manifest.yaml` +1 -0
> - `scripts/harness.py` +1 -0
> - `scripts/kit/manifest.yaml` +3 -0
> - `scripts/kit/probe.py` +4 -2
> - `scripts/omnigent_policy.py` +4 -1
> - `scripts/plans_registry.py` +1 -0
> - `scripts/pr_sync.py` +1 -0
> - `scripts/ramp_valves.py` +1 -0
> - `scripts/research_capture.py` +1 -0
> - `scripts/research_census.py` +1 -0
> - `scripts/stage2.py` +1 -0
> - `scripts/stage2_availability.py` +1 -0
> - `scripts/stage2_go.py` +1 -0
> - `scripts/stage2_research_limits.py` +1 -0
> - `scripts/stage2_research_refs.py` +1 -0
> - `scripts/stage2_session.py` +1 -0
> - `scripts/venv_guard.py` +102 -0
> - `tests/test_ci.py` +1 -0
> - `tests/test_pr_sync.py` +1 -1
> - `tests/test_stage2.py` +1 -1
> - `tests/test_venv_guard.py` +350 -0
> - `tests/test_verify_cheap_first.py` +2 -1
> - `tests/test_workflow_entry.py` +8 -1
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `scripts/ci_gates.py` is shared execution infrastructure
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 714 lines of this gate left out …]
>             make=[red] * 3,
>         )
>         assert world.run("implement") == 1
>         names = [call["name"] for call in world.calls()]
> >       assert names[:2] == ["claude", "make"], names[:2]
> E       AssertionError: ['claude', 'python3']
> E       assert ['claude', 'python3'] == ['claude', 'make']
> E         
> E         At index 1 diff: 'python3' != 'make'
> E         Use -v to get more diff
>
> tests/test_stage2_fail_fast.py:259: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 31 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 31 files, 2 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> failed: implementation post-run checks failed after the allowed attempts; why each attempt failed and the files it changed: plans/changes/demo/findings.md
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=76505) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/venv-guard/tests/test_stage2.py:23760: DeprecationWarning: This process (pid=76506) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_omnigent_deny_layers.py::test_policy_denies_denied_tools_and_leaves_allowed_ones
> FAILED tests/test_omnigent_deny_layers.py::test_policy_asks_about_asked_tools_and_nothing_else
> FAILED tests/test_omnigent_deny_layers.py::test_policy_protects_omnigents_config_file
> FAILED tests/test_omnigent_deny_layers.py::test_no_event_shape_raises_an_evaluation_error
> FAILED tests/test_omnigent_deny_layers.py::test_the_cli_merges_and_says_what_to_do_next
> FAILED tests/test_omnigent_deny_layers.py::test_installer_runs_end_to_end_in_a_temporary_home
> FAILED tests/test_stage2.py::test_the_format_step_runs_check_then_format_on_the_targets_before_verify
> FAILED tests/test_stage2.py::test_an_attempt_that_plants_the_registry_renderer_never_runs_it
> FAILED tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
> FAILED tests/test_stage2.py::test_a_red_first_interpreter_that_cannot_start_pytest_fails_the_attempt
> FAILED tests/test_stage2.py::test_first_implement_refreshes_derived_files_without_a_model_repair
> FAILED tests/test_stage2.py::test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics
> FAILED tests/test_stage2.py::test_a_failed_runs_derived_writes_do_not_block_the_next_run
> FAILED tests/test_stage2_fail_fast.py::test_empty_targets_skip_their_command
> FAILED tests/test_stage2_fail_fast.py::test_cheap_green_still_requires_full_verification
> 15 failed, 6327 passed, 17 skipped, 5 warnings in 577.73s (0:09:37)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 46905 earlier lines left out …]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:20:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:21:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:25:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:25:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:25:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:27:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:30:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:31:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:40:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:40:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:45:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:46:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:69:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:134:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:134:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:134:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:135:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:136:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:137:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1116 files, 4585 commits, 12 rules.

Stage-2 call, 2026-11-18: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4589 commits, 12 rules.

Runner restoration, 2026-11-18: repair · attempt 1 · route codex — lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1116 files, 4610 commits, 12 rules.

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1116 files, 4610 commits, 12 rules.

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1116 files, 4610 commits, 12 rules.

Stage-2 call, 2026-11-18: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4639 commits, 12 rules.

Runner restoration, 2026-11-18: repair · attempt 1 · route codex — lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1116 files, 4667 commits, 12 rules.

Stage-2 call, 2026-11-18: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4669 commits, 12 rules.

Runner restoration, 2026-11-18: repair · attempt 1 · route codex — lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged

Stage-2 call, 2026-11-18: review-loop · endpoint opencode-go · model hy3 · leak check clean over 1116 files, 4679 commits, 12 rules.

Stage-2 call, 2026-11-18: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4681 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_venv_guard.py` +5 -1
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> .....F..                                                                 [100%]
> =================================== FAILURES ===================================
> _________ test_guards_from_two_checkouts_replace_process_at_most_once __________
> [gw5] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/venv-guard/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1866/popen-gw5/test_guards_from_two_checkouts0')
>
>     def test_guards_from_two_checkouts_replace_process_at_most_once(tmp_path: Path) -> None:
>         first = _tree(tmp_path, framework=True, environment=True, name="first")
>         second = _tree(tmp_path, framework=True, environment=True, name="second")
>         for root in (first, second):
>             site = next((root / ".venv" / "lib").glob("python*/site-packages"))
>             for dependency in THIRD_PARTY:
>                 (site / f"{dependency}.py").unlink()
>         counter = tmp_path / "starts"
>         script = _write(
>             first,
>             "cross.py",
>             "import importlib.util\n"
>             "from pathlib import Path\n"
>             f"counter = Path({str(counter)!r})\n"
>             "count = int(counter.read_text()) + 1 if counter.exists() else 1\n"
>             "counter.write_text(str(count))\n"
>             "if count > 3: raise SystemExit('replacement loop')\n"
>             "import venv_guard\n"
>             f"spec = importlib.util.spec_from_file_location('other_guard', {str(second / 'scripts' / 'venv_guard.py')!r})\n"
>             "module = importlib.util.module_from_spec(spec)\n"
>             "spec.loader.exec_module(module)\n",
>         )
>     
>         result = _run([str(first / ".venv" / "bin" / "python3"), str(script)], tmp_path)
>     
> >       assert result.returncode == 0, result.stderr
> E       AssertionError: replacement loop
> E         
> E       assert 1 == 0
> E        +  where 1 = CompletedProcess(args=['/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1866/popen-...pen-gw5/test_guards_from_two_checkouts0/first/scripts/cross.py'], returncode=1, stdout='', stderr='replacement loop\n').returncode
>
> tests/test_venv_guard.py:401: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_venv_guard.py::test_guards_from_two_checkouts_replace_process_at_most_once
> 1 failed, 7 passed in 0.69s
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/venv-guard/stage2/attempts/venv-guard/attempt-1-20261118T220137204334Z-80d7586b.md
> ```

Stage-2 call, 2026-11-18: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1116 files, 4681 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; repair the taken rows of the loop record
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> .....F..                                                                 [100%]
> =================================== FAILURES ===================================
> _________ test_guards_from_two_checkouts_replace_process_at_most_once __________
> [gw5] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/venv-guard/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1869/popen-gw5/test_guards_from_two_checkouts0')
>
>     def test_guards_from_two_checkouts_replace_process_at_most_once(tmp_path: Path) -> None:
>         first = _tree(tmp_path, framework=True, environment=True, name="first")
>         second = _tree(tmp_path, framework=True, environment=True, name="second")
>         for root in (first, second):
>             site = next((root / ".venv" / "lib").glob("python*/site-packages"))
>             for dependency in THIRD_PARTY:
>                 (site / f"{dependency}.py").unlink()
>         counter = tmp_path / "starts"
>         script = _write(
>             first,
>             "cross.py",
>             "import importlib.util\n"
>             "from pathlib import Path\n"
>             f"counter = Path({str(counter)!r})\n"
>             "count = int(counter.read_text()) + 1 if counter.exists() else 1\n"
>             "counter.write_text(str(count))\n"
>             "if count > 3: raise SystemExit('replacement loop')\n"
>             "import venv_guard\n"
>             f"spec = importlib.util.spec_from_file_location('other_guard', {str(second / 'scripts' / 'venv_guard.py')!r})\n"
>             "module = importlib.util.module_from_spec(spec)\n"
>             "spec.loader.exec_module(module)\n",
>         )
>     
>         result = _run([str(first / ".venv" / "bin" / "python3"), str(script)], tmp_path)
>     
> >       assert result.returncode == 0, result.stderr
> E       AssertionError: replacement loop
> E         
> E       assert 1 == 0
> E        +  where 1 = CompletedProcess(args=['/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1869/popen-...pen-gw5/test_guards_from_two_checkouts0/first/scripts/cross.py'], returncode=1, stdout='', stderr='replacement loop\n').returncode
>
> tests/test_venv_guard.py:401: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_venv_guard.py::test_guards_from_two_checkouts_replace_process_at_most_once
> 1 failed, 7 passed in 0.74s
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/venv-guard/stage2/attempts/venv-guard/attempt-2-20261118T220137204334Z-80d7586b.md
> ```

Stage-2 call, 2026-11-18: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1116 files, 4682 commits, 12 rules.

Runner restoration, 2026-11-18: repair · attempt 3 · route stage-1 — lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged

Stage-2 call, 2026-11-19: review · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4736 commits, 12 rules.

## Phase 6 — Codex, 2026-11-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| R1 | MAJOR | SPEC | base | scripts/venv_guard.py:104 | When the caller’s interpreter already has PyYAML, Jinja2 and pydantic, a script continues under that interpreter even if the checkout has a usable `.venv`. The required checkout interpreter is therefore not used. [Acceptance criterion 1] | Codex | rejected — decisions.md Q-3 (maintainer, 2026-11-18) accepts that an interpreter which already carries PyYAML, Jinja2 and pydantic runs outside the lock; criterion 1 is aligned with Q-3 by an orchestrator hand edit of spec.md | — |
| R2 | MAJOR | SPEC | base | scripts/venv_guard.py:59 | When an entry script prints output or performs another action before importing a guarded module, re-execution starts the entry script again. For example, a line printed before the import appears twice instead of once. [Acceptance criteria 1 and 6] | Codex | fixed — orchestrator hand finish of Sonnet repair attempt 3 (ruff SIM101 merge only): tests/test_venv_guard.py::test_the_guard_check_rejects_effects_before_the_guard; Boundary in spec.md | no |
| R3 | MAJOR | SPEC | base | tests/test_venv_guard.py:203 | A new unguarded `import yaml` inside a `match` case passes the automated check: its block walker does not visit case bodies. The check therefore cannot enforce the guard for all direct imports under `scripts/`. [Acceptance criterion 5] | Codex | fixed — orchestrator hand finish of Sonnet repair attempt 3 (ruff SIM101 merge only): tests/test_venv_guard.py::test_guard_check_visits_match_cases | no |

Phase 6 verdict: codex 01a1f2d1-dc8c-7db0-ba64-b8dad04fdc9b, 2026-11-19
Reviewer session: codex 01a1f2d1-dc8c-7db0-ba64-b8dad04fdc9b — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MINOR | correctness | base | scripts/venv_guard.py: HINT/ensure() | The hint says the checkout has no usable .venv, but _install_hint() is installed for every framework checkout, including when sys.prefix is already that .venv or when re-exec was skipped by the marker; a missing dependency in a working venv gets the false instruction to run make venv. | hy4-flash-free | fixed — tests/test_venv_guard.py::test_active_environment_missing_dependency_has_no_absent_environment_hint | yes — tests/test_venv_guard.py::test_active_environment_missing_dependency_has_no_absent_environment_hint | disagree — A venv missing the required dependency is unusable for that invocation, so the hint is appropriate. |
| L1-2 | MAJOR | correctness | base | scripts/venv_guard.py: MARKER check in ensure() | The marker only suppresses re-exec for the exact VENV path; a process in checkout A's venv that imports checkout B's guard replays A's original argv with B's interpreter, then A's guard replays it with A's interpreter. The claim that the marker prevents invocation loops is false for multiple checkouts. | hy4-flash-free | fixed — tests/test_venv_guard.py::test_guards_from_two_checkouts_replace_process_at_most_once | yes — tests/test_venv_guard.py::test_guards_from_two_checkouts_replace_process_at_most_once | agree |
| L2-1 | MAJOR | SPEC | base | `scripts/omnigent_policy.py:378,393,417` | The plan lists `scripts/omnigent_policy.py` among the files that "invoke the shared guard before their third-party imports", but the file is untouched: its three lazy `import yaml` calls still run under whatever `python3` the caller used, so the documented `python3 scripts/omnigent_policy.py --write` (its own docstring, lines 21–26, and `tools/omnigent/README.md:22–23`) still dies with a bare `ModuleNotFoundError` on a checkout whose `.venv` holds PyYAML. The exemption that hides this from the new scan (`NOT_GUARDED` in `tests/test_venv_guard.py`) gives "runs under Omigent's own Python, never re-executed into the checkout's .venv", a reason that holds only for the merge call in `tools/omnigent/install.sh:29–36`, not for the human invocation the script advertises. | deepseek-v4.1-flash | fixed — not a test — Omnigent exemption documented in the plan and spec | no — not a test | disagree — The spec explicitly exempts the Omnigent policy script from the guard. |
| L2-2 | MAJOR | SPEC | base | `scripts/venv_guard.py:52,84-95` | A framework checkout whose `.venv` exists and is executable but no longer carries PyYAML, Jinja2 or pydantic re-executes the caller into that environment and then dies with the untouched `ModuleNotFoundError` and no `make venv` line: `_usable()` asks only for an executable file, and `ensure()` installs the hint exclusively in the branch where that file is missing. The spec calls a broken environment unusable and wants the hint whenever a required third-party dependency is missing, so the same class of failure the change exists for still ends in a bare traceback — now reached through an extra exec that also hides the real interpreter from the operator. `tests/test_venv_guard.py::test_active_environment_missing_dependency_has_no_absent_environment_hint` pins this as intended, so the row is spec-level, not a test gap. | deepseek-v4.1-flash | fixed — tests/test_venv_guard.py::test_active_environment_missing_dependency_reports_hint | yes — tests/test_venv_guard.py::test_active_environment_missing_dependency_reports_hint | disagree — The current guard installs the hint in every framework checkout, including an active venv with a missing dependency. |
| L2-3 | MAJOR | MAINT | fix-r1 | `scripts/venv_guard.py:36,78,89` | `MARKER` is written into `os.environ` before `os.execv` and never cleared, so it survives in the replaced process and in every descendant, while `ensure()` only tests for its presence (`MARKER not in os.environ`) and never compares the venv path it stores. A child that starts a guarded script of a different checkout — worktrees each carry their own `.venv` — is therefore never re-executed into *its* environment although a usable one exists, and because `_usable()` is true there it also gets no hint. The "marker … names the environment already entered" that the module docstring promises is not what the code implements. | deepseek-v4.1-flash | fixed — tests/test_venv_guard.py::test_foreign_marker_allows_checkout_entry | yes — tests/test_venv_guard.py::test_foreign_marker_allows_checkout_entry | disagree — The current guard removes the marker on entry and compares its value with the checkout’s venv path. |
| L2-4 | MAJOR | MAINT | base | `scripts/venv_guard.py:87-88`, `scripts/verify_all.sh:45-52` | Every call of a guarded script replaces the process with `<checkout>/.venv/bin/python3` even when the caller named another interpreter deliberately: `PYTHON=/opt/python3.12 make verify` — the documented escape hatch at `verify_all.sh:45-52`, "whoever needs another place sets $PYTHON" — runs `scripts/ci_gates.py` and any `python3 -m pytest` under the venv interpreter again as soon as the first guarded module is imported, mid-run. That is the spec's non-goal "changing the verify runner's interpreter-selection contract" happening as a side effect, and it silently overrides an explicit operator choice such as running the suite under a second interpreter that carries the locked packages. | deepseek-v4.1-flash | fixed — tests/test_venv_guard.py::test_available_dependencies_keep_selected_interpreter | yes — tests/test_venv_guard.py::test_available_dependencies_keep_selected_interpreter | disagree — The guard does not re-execute when all three dependencies are available to the selected interpreter. |
| L2-5 | MINOR | MAINT | base | `scripts/stage2.py:6107-6126` | `trusted_registry` now drops `.venv` from the mirror, but its docstring still promises that "every other entry of the worktree is linked into the mirror", and neither the comment nor a test says why a mirror must not carry the environment. Two consequences for a later reader: the mirrored root silently disables the new guard (a mirror script started with the caller's bare `python3` no longer reaches any environment), and the rule that `scripts/` is the only exclusion is now false, so an extension of the mirror inherits a contract the code has stopped keeping. | deepseek-v4.1-flash | fixed — not a test — trusted registry docstring explains the environment exclusion | no — not a test | disagree — The current docstring and comment explicitly describe the `.venv` exclusion and its security reason. |
| L2-6 | MINOR | MAINT | base | `plans/changes/venv-guard/plan.md` | "Files and limits" omits `scripts/export/manifest.yaml`, which the change edits to give the guard a `carry` verdict, and the six existing test files it touches (`tests/test_ci.py`, `tests/test_pr_sync.py`, `tests/test_stage2.py`, `tests/test_verify_cheap_first.py`, `tests/test_workflow_entry.py`); the plan's own next paragraph says the remaining files stay untouched. A later reader cannot tell the intended edits from scope creep, and the plan's verification section names only the new test file plus `make verify`. | deepseek-v4.1-flash | fixed — not a test — plan lists the edited files | no — not a test | agree |
| L2-7 | MAJOR | SPEC | base | `plans/changes/venv-guard/plan.md`, "Files and limits" and build step 3; `tests/test_venv_guard.py`, `NOT_GUARDED` | The plan promises the guard in `scripts/omnigent_policy.py` ("invoke the shared guard before their third-party imports"), but the change adds no guard there: the file keeps three direct `import yaml` calls (lines 378, 393, 417) and the new test simply exempts it via `NOT_GUARDED`, an exemption recorded nowhere in spec.md or decisions.md. A maintainer comparing plan to tree cannot tell whether the guard or the plan is wrong, and any new unguarded PyYAML import in that file passes criterion 5's automated check, whose refutation is exactly "an unguarded new or reordered PyYAML ... import passes the check". | mimo-v2.6-flash | fixed — not a test — Omnigent exemption documented in the plan and spec | no — not a test | disagree — The spec explicitly exempts the Omnigent policy script. |
| L2-8 | MAJOR | SPEC | base | `scripts/venv_guard.py`, `_usable` and `ensure`; `tests/test_venv_guard.py::test_active_environment_missing_dependency_has_no_absent_environment_hint` | `_usable` counts only "file exists and is executable", so a `.venv` that starts but was never populated (interrupted `make venv`, or one missing only Jinja2/pydantic) counts as usable: the guard re-executes into it, and the `make venv` hint — gated in `ensure()` on `not _usable(python)` — never prints, leaving the bare `ModuleNotFoundError: No module named 'yaml'` that criterion 3's refutation names ("the caller sees only a missing-module traceback"). The new test locks this in (asserts "make venv" not in stderr), while the repository's own interpreter fitness test probes `import yaml` (scripts/verify_all.sh:54), and the HINT text itself says "this checkout has no usable .venv" — the very state it is suppressed in. Where the caller's original interpreter had the dependency, the re-exec additionally turns a working invocation into a failing one, criterion 1's refutation. | mimo-v2.6-flash | fixed — tests/test_venv_guard.py::test_active_environment_missing_dependency_reports_hint | yes — tests/test_venv_guard.py::test_active_environment_missing_dependency_reports_hint | disagree — The current guard installs the hint in the active venv even when a dependency is missing. |
| L2-9 | MAJOR | MAINT | fix-r1 | `scripts/venv_guard.py:61` (writes `VENV_GUARD_ENTERED` with the environment's path) and `:94` (reads only its presence) | The anti-loop marker's value is written but never consulted: `ensure()` checks `MARKER not in os.environ` only. Every child of a re-executed process inherits the marker, so any later guarded script it starts — same checkout, another worktree, bare `python3` — silently skips the re-exec and dies on its third-party import, and a script started in a different checkout runs under the parent's interpreter instead of its own, refuting criterion 1's unconditional promise; `VENV_GUARD_ENTERED=x python3 scripts/new_change.py` reproduces the original bead failure in one line. The comment in `tests/test_venv_guard.py` above the `marked` probe says the marker "names the environment a replacement already entered", but no code ever compares that name, and presence-only semantics also mean a marker naming a foreign environment blocks a legitimate entry. | mimo-v2.6-flash | fixed — tests/test_venv_guard.py::test_foreign_marker_allows_checkout_entry | yes — tests/test_venv_guard.py::test_foreign_marker_allows_checkout_entry | disagree — The current guard removes the marker and compares its value with the checkout’s venv path. |
| L2-10 | MAJOR | SPEC | base | `scripts/ramp_valves.py:121-127`, `_roster_handles` | Build step 3 requires the guard before third-party imports "including conditional imports", but here the guard sits inside `try: ... except Exception: return set()`. In a framework checkout without `.venv` the missing PyYAML is swallowed: the excepthook hint installed by `ensure()` never fires (the exception never reaches the hook) and `_roster_handles` returns an empty roster as if provenance.yaml were empty — a silent wrong answer with no `make venv` anywhere. That is precisely the "misleading success" criterion 3's refutation names, unreachable at the attachment point the change itself chose. | mimo-v2.6-flash | fixed — tests/test_venv_guard.py::test_roster_missing_yaml_is_not_swallowed | yes — tests/test_venv_guard.py::test_roster_missing_yaml_is_not_swallowed | disagree — Both imports now precede the `try` block, so the missing dependency is not swallowed there. |
| L2-11 | MINOR | MAINT | base | `scripts/venv_guard.py`, `_original_command`, `_reexec`, `ensure` | When the command line cannot be replayed (`sys.argv[0]` in `("", "-")`, i.e. a script piped on stdin, or `execv` raising OSError), `_reexec` returns silently and `ensure()` still suppresses the hint because the venv is usable, so in a framework checkout with a usable `.venv` the caller keeps the original interpreter and gets the bare ModuleNotFoundError. This carve-out exists only in `_original_command`'s docstring; spec.md's criteria 1 and 3 carry no such exception, so a maintainer reading the spec expects either a re-exec or a `make venv` line and gets neither. | mimo-v2.6-flash | fixed — tests/test_venv_guard.py::test_unreplayable_or_broken_environment_reports_hint | yes — tests/test_venv_guard.py::test_unreplayable_or_broken_environment_reports_hint | disagree — The hint is installed for framework checkouts even when re-execution cannot proceed. |
| L2-12 | MINOR | MAINT | base | `plans/changes/venv-guard/research.md`, "Neighbours (for the header)" | The closing sentence states "no active sibling change folder exists under `plans/changes/` besides this one", but `plans/changes/` holds a dozen non-archived change folders and `plans/INDEX.md` lists several as draft or partial within days of this change (bd-1-3-4 dated 2026-11-14, flaky-swarm-leak-test 2026-11-13 with partial plan and spec, swarm-test-speed with partial implementation). A maintainer trusting the Neighbours section is sent past the change's actual siblings. | mimo-v2.6-flash | fixed — not a test — research names existing sibling changes | no — not a test | agree |
| L2-13 | MAJOR | SPEC | base | scripts/omnigent_policy.py:378, 393, 417; tests/test_venv_guard.py (NOT_GUARDED) | The plan's build step 3 and "Files and limits" list `scripts/omnigent_policy.py` among the files that "invoke the shared guard before their third-party imports", and spec criterion 5 promises the automated check fails for any unguarded direct PyYAML import in `scripts/`; the shipped tree leaves that script's three unguarded yaml imports in place and instead hardcodes a `NOT_GUARDED` exemption in the test whose reason ("runs under Omnigent's own Python") appears in no plan, spec or decisions record, so the shipped tree passes the check exactly as criterion 5's refutation describes — a deviation from the change's own documents that no reviewer without the test file would see. | glm-5.3-flash | fixed — not a test — Omnigent exemption documented in the plan and spec | no — not a test | disagree — The spec explicitly exempts the Omnigent policy script. |
| L2-14 | MAJOR | MAINT | fix-r1 | scripts/venv_guard.py (`_reexec` sets MARKER; `ensure` skips on presence) | The re-exec marker is presence-checked and never value-compared, and it is inherited by every descendant process: a guarded script started by a process a guard already replaced — concretely, the stage-2 runner itself re-exec'd under the main checkout's `.venv`, later spawning `python3 scripts/...` in another worktree — is skipped by its own guard and runs under the wrong interpreter, reintroducing the missing-PyYAML failure in the runner lane the change claims to repair; the tests cover only the in-process two-guard case and a marked direct invocation, never the inherited-marker subprocess case, and the test comment justifying presence-only ("a replacement that did not land cannot loop") describes a path that actually pops the marker on OSError. | glm-5.3-flash | fixed — tests/test_venv_guard.py::test_foreign_marker_allows_checkout_entry | yes — tests/test_venv_guard.py::test_foreign_marker_allows_checkout_entry | disagree — The current guard removes the marker on entry and includes a descendant-process test. |
| L2-15 | MINOR | MAINT | base | scripts/venv_guard.py (`_usable`, `_reexec`, `ensure`) | "Usable" is only `is_file` + `X_OK`, so two broken-environment shapes get no `make venv` hint although the environment is effectively unusable: an interpreter that exists and is executable but fails at execv (corrupt binary, wrong format — the guard pops the marker and silently continues under the system interpreter with the hint never installed), and an environment entered with flags replayed from `sys.orig_argv` such as `-S` or `-I`, where the dependency import still fails after the re-exec; a maintainer who already ran `make venv` in either case is left with a bare ModuleNotFoundError. | glm-5.3-flash | fixed — tests/test_venv_guard.py::test_unreplayable_or_broken_environment_reports_hint | yes — tests/test_venv_guard.py::test_unreplayable_or_broken_environment_reports_hint | disagree — The hint is installed in framework checkouts before either case reaches a missing dependency. |
| L2-16 | MINOR | SPEC | base | scripts/stage2.py (`trusted_registry`, exclusion of `.venv` from the mirror) | The change alters the trusted-mirror contents beyond the promised guard insertion, with a comment calling a re-exec into the checkout's `.venv` a fault — but running a script that reaches a third-party dependency under the checkout's interpreter is exactly what acceptance criterion 1 mandates, and no spec sentence, plan entry or test covers excluding `.venv` from the mirror or the registry-trust implications of that exclusion; a maintainer reading only the spec cannot tell why shared execution infrastructure changed. | glm-5.3-flash | fixed — not a test — spec and trusted registry docstring explain the mirror boundary | no — not a test | disagree — The spec explicitly requires the trusted mirror to exclude `.venv`. |
| L3-1 | BLOCKER | SPEC | base | `scripts/ramp_valves.py` ~118–125 | `_roster_handles()` had `import yaml` inside `try: … except Exception: return set()`, which was its deliberate graceful-degradation contract: when PyYAML is absent the function silently returned an empty set and the ramp-valve evaluation continued. The change moves `import yaml` to module scope ahead of the `try` block without any compensating caller-side change, so every path that reaches `_roster_handles()` under a missing-PyYAML interpreter now raises an unhandled `ModuleNotFoundError` (with the `make venv` hint) instead of returning `set()`. The spec covers adding the guard, not altering the error-handling contract of existing functions; the plan's step 3 says "place the guard before direct third-party imports", not "restructure the surrounding control flow". The test `test_roster_missing_yaml_is_not_swallowed` confirms the new behavior is intentional, but no spec criterion or decision justifies the change in observable function semantics. | qwen3.8-flash | rejected — deliberate, decided as row L2-10: a silent empty roster when PyYAML is missing is the misleading success criterion 3 refutes; scripts/ramp_valves.py is not exported to the kit (scripts/export/manifest.yaml), so criterion 4 is untouched | — | disagree — The framework failure is required by criterion 3; the separate kit behavior is addressed by L4-1. |
| L3-2 | MAJOR | MAINT | fix-r2 | `scripts/venv_guard.py` `ensure()` | `importlib.util.find_spec(name)` can raise `ImportError` (or other exceptions) when a package is partially installed or its spec loader itself is broken, not only return `None`. The three calls inside the `any(...)` generator are not guarded by any exception handler. If any of them raises, the exception propagates out of `ensure()` and therefore out of `import venv_guard`, breaking every script that loads the guard — which is the exact failure mode the module exists to prevent. A `try/except (ImportError, ValueError): return True` around each `find_spec` call (treating a broken spec as "missing") would keep the guard resilient in the edge case it cannot control. | qwen3.8-flash | fixed — tests/test_venv_guard.py::test_broken_dependency_spec_is_treated_as_missing | yes — tests/test_venv_guard.py::test_broken_dependency_spec_is_treated_as_missing | disagree — `_missing()` catches `ImportError` and `ValueError`. |
| L3-3 | MAJOR | SPEC | base | `tests/test_venv_guard.py` `_is_guard()` | The AST helper only recognises a bare `import venv_guard` (an `ast.Import` node whose alias is `"venv_guard"`). A writer who uses `from venv_guard import ensure` — which executes the same module and triggers `ensure()` just as effectively — is rejected by the automated criterion-5 check as an unguarded file, forcing them to rewrite an equivalent statement to satisfy the scanner. The plan step 4 says "Require an effective guard before each import"; the check is not effective in both directions. A matching `ast.ImportFrom` node with `module == "venv_guard"` would close the gap. | qwen3.8-flash | rejected — the check is stricter than needed, never weaker: the one documented guard form is `import venv_guard`, and an equivalent form is rewritten, not missed | — | agree |
| L3-4 | MINOR | MAINT | fix-r2 | `scripts/venv_guard.py` `_reexec()` | When `os.execv` succeeds (the normal path), `os.environ[MARKER]` stays set in the replaced process. That process now runs a guarded script; any `subprocess.run(…, env=None)` call inherits `os.environ` and therefore the `VENV_GUARD_ENTERED` marker. If the spawned process starts a guarded script from a *different* checkout (different `.venv` path), the marker value does not match that checkout's `str(VENV)`, so the guard correctly re-execs — the cross-checkout case is tested. But if the spawned process starts a script from the *same* checkout using an explicit `sys.executable` that is not the venv python (e.g., a subprocess call to `python3` on PATH), the marker matches and the guard is skipped, potentially causing a `ModuleNotFoundError` the guard would otherwise have fixed. The marker's lifetime should be narrowed: `_reexec` should only set it for the `execv` call and restore it before returning, or the child should clear it before re-entering. | qwen3.8-flash | fixed — tests/test_venv_guard.py::test_reentered_process_does_not_pass_marker_to_child | yes — tests/test_venv_guard.py::test_reentered_process_does_not_pass_marker_to_child | disagree — The replaced process removes the marker on guard entry, before it starts descendants. |
| L3-5 | MINOR | SPEC | base | `scripts/venv_guard.py` `ensure()` | Spec criterion 3 says the `make venv` hint is shown "when the framework checkout has no usable `.venv` and a required third-party import is missing". The implementation installs the `sys.excepthook` hint *before* the missing/re-exec check, so the hint fires even when `.venv` exists and is usable but the re-exec itself fails (e.g., the venv interpreter crashes on a broken shared library). In that case the hint says "run `make venv`", but the environment already exists — the user is directed to rebuild a venv that is already there rather than to investigate why the venv's interpreter cannot start. | qwen3.8-flash | rejected — by design, decisions.md Q-3: the make-venv hint is installed in every framework checkout; rebuilding a .venv whose interpreter cannot start is the right remedy | — | disagree — An interpreter that cannot start is unusable for the invocation; the spec does not prohibit the hint in that case. |
| L4-1 | MAJOR | SPEC | base | scripts/ramp_values.py (`_roster_handles`) | Placing the guard before its third-party import moved `import yaml` out of the surrounding `try/except Exception`, so in a kit instance (no `.venv`, no PyYAML) the guard does nothing and the missing dependency now raises `ModuleNotFoundError` at import time instead of being caught and returning an empty roster; this contradicts acceptance criterion 4 ("the guard leaves its existing interpreter and dependency behavior unchanged") and the decision's kit fallback, and only `test_roster_missing_yaml_is_not_swallowed` covers the framework path, so the kit regression has no test. | hy3 | rejected — same as L3-1: scripts/ramp_valves.py does not travel with the kit (scripts/export/manifest.yaml: only scripts/kit/ and named files carry; everything else drops), so no kit instance runs it and criterion 4 is untouched; the framework behaviour is the deliberate decision of row L2-10 | — | agree |
| L4-2 | MINOR | MAINT | fix-r2 | tests/test_venv_guard.py::test_guards_from_two_checkouts_replace_process_at_most_once | The test's name and body claim to prove guards from two checkouts re-exec at most once, but both fixture venvs carry the stub `yaml`/`jinja2`/`pydantic`, so `_missing` is always False and `ensure()` never re-execs; the `assert ... <= 2` therefore passes vacuously and would not catch a broken marker, so the Q-3 cross-checkout fix is not actually exercised by this test. | hy3 | fixed — not a test — I rewrote `tests/test_venv_guard.py::test_guards_from_two_checkouts_replace_process_at_most_once` so a re-exec really happens. I haven't run it; the runner runs the checks. | no — not a test | disagree — The test removes all three dependency stubs from the first venv and asserts exactly two starts. |

Rounds run: 4

Record digest: sha256:b2598042d212d39761d725dbb8c9832637d45a4cb1eacfb9caf6eaf92667d35f

Record identity: sha256:f2eb7e11ea6d759f98e3c54387b90441367136b28b96e90612191fe1b00b99d7

Loop state: {"availability": {"checked_at": "2026-11-18T12:10:57+00:00", "failed": {"deepseek-v4-pro": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "glm-5.2": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "glm-5.3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "grok-4.7": "pi call failed: exit 1: opencode-go API error (403): {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "hy4-preview": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "kimi-k3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated. Use mimo-v2.6-pro instead.\"}", "qwen3.8-max": "pi call failed: exit 1: 403 {\"type\":\"error\",\"error\":{\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}}"}, "reachable": ["hy4-flash-free", "deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "hy4": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read", "qwen4-max": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 \"thinking.type.enabled is not supported for this model; use thinking.type.adaptive\" (a Pi adapter setting, bead coding-harness-36za evidence))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": []}, "consumed": ["free", "flash", "rung:qwen3.8-flash", "rung:hy3"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-fable-5-2", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "gemini-4-carbon", "provider": "opencode"}, {"model": "gemini-4-hydrogen", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "gpt-6.2-astra", "provider": "opencode"}, {"model": "gpt-6.2-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "hy4-flash-free", "provider": "opencode"}, {"model": "iceman-free", "provider": "opencode"}, {"model": "inkling-2-small-free", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "longcat-2.5-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-ember-1.0", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4", "provider": "opencode-go"}, {"model": "hy4-flash-free", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "qwen4-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-18T12:06:47+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1795003606457, "etag": "W/\"c1263bc64c19af4fce6a4b7eb3393cb0\"", "lastModified": 1795000948000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash 1017", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "hy4-flash-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4 flash Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 1048576, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 1048576, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "LongCat 2.5 Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.075, "cacheWrite": 1.875, "input": 1.5, "output": 4.5}, "id": "qwen4-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Qwen4 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": ["opencode-go/gemini-4-argon: wire api \"google-generative-ai\" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base"], "overlay": ["beam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4", "hy4-flash-free", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "longcat-2.5-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "qwen4-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-11-13", "id": "longcat-2.5-free", "reason": "The maintainer took the longcat models out for good on 2026-11-13 (\"das scheint ein sehr langsames modell zu sein\"): longcat-2.0 timed out on all three online topics of that day's research swarm run; the free longcat id goes with it (bead coding-harness-363r.2)."}, {"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}, {"date": "2026-11-06", "id": "iceman-contributor-free", "reason": "New in the live Go catalog on 2026-11-06 and picked as the whole free swarm by prepare-loop; \"contributor\" ids on Go have meant that request data may be used for training, and the maintainer's decision of 2026-10-17 (question Q-12) keeps such models off. The Go page's privacy table, read 2026-11-06, confirms it: 'Iceman Contributor Free | Yes | Not ZDR'. A bridge until one central per-use-case model policy exists (bead coding-harness-k0ub with coding-harness-wq1m); maintainer, 2026-11-06, morning question Q-M9, option A."}, {"date": "2026-11-06", "id": "cat-jam-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it, so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}, {"date": "2026-11-06", "id": "longcat-2.5-preview-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it (only LongCat-2.0), so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": ["hy4-flash-free"], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview"], "rungs": ["qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base.
> Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor, qwen4-max.
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> From qwen3.8-flash:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> |
> 
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> From hy3:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> Based on my review of the diff and verification against the actual files, here are my findings:

<!-- End of released loop record -->

Stage-2 call, 2026-11-19: review (loop marks) · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4736 commits, 12 rules.

Stage-2 call, 2026-11-19: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4739 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_venv_guard.py` +8 -0
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files `tests/test_venv_guard.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - R2: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/venv-guard/stage2/attempts/venv-guard/attempt-1-20261119T080207420916Z-112dc25a.md
> ```

Stage-2 call, 2026-11-19: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1116 files, 4739 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files `tests/test_venv_guard.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; repair the taken rows of the loop record
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/venv-guard/stage2/attempts/venv-guard/attempt-2-20261119T080207420916Z-112dc25a.md
> ```

Stage-2 call, 2026-11-19: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1116 files, 4739 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/venv_guard.py` +36 -2
> - `tests/test_venv_guard.py` +10 -0
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed `scripts/venv_guard.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> scripts/venv_guard.py:81:16: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>    |
> 79 |             isinstance(statement, ast.Expr)
> 80 |             and isinstance(statement.value, ast.Constant)
> 81 |             or isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
>    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 82 |             or isinstance(statement, (ast.Assign, ast.AnnAssign))
> 83 |             and not any(isinstance(node, ast.Call) for node in ast.walk(statement))
>    |
>    = help: Convert to `X | Y`
>
> scripts/venv_guard.py:82:16: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>    |
> 80 |             and isinstance(statement.value, ast.Constant)
> 81 |             or isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
> 82 |             or isinstance(statement, (ast.Assign, ast.AnnAssign))
>    |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 83 |             and not any(isinstance(node, ast.Call) for node in ast.walk(statement))
> 84 |         ):
>    |
>    = help: Convert to `X | Y`
>
> Found 2 errors.
> No fixes available (2 hidden fixes can be enabled with the `--unsafe-fixes` option).
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/venv-guard/stage2/attempts/venv-guard/attempt-3-20261119T080207420916Z-112dc25a.md
> ```

Stage-2 call, 2026-11-19: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4742 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files none; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - no work done: the attempt left no model work after runner bookkeeping, derived preparation and formatting; repair the taken rows of the loop record
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/venv-guard/stage2/attempts/venv-guard/attempt-1-20261119T084545957362Z-c7422ab7.md
> ```

Stage-2 call, 2026-11-19: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1116 files, 4742 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/venv-guard/spec.md` +2 -0
> - `tests/test_venv_guard.py` +7 -0
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files `tests/test_venv_guard.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - R2: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/venv-guard/stage2/attempts/venv-guard/attempt-2-20261119T084545957362Z-c7422ab7.md
> ```

Stage-2 call, 2026-11-19: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1116 files, 4742 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/venv-guard/spec.md` +1 -1
> - `tests/test_venv_guard.py` +68 -0
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> tests/test_venv_guard.py:259:13: SIM101 Multiple `isinstance` calls for `statement`, merge into a single call
>     |
> 257 |               return lines
> 258 |           harmless = (
> 259 | /             isinstance(statement, ast.Import | ast.ImportFrom | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)
> 260 | |             or isinstance(statement, ast.Assign | ast.AnnAssign)
> 261 | |             or (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant))
> 262 | |             or _is_path_setup(statement)
>     | |________________________________________^ SIM101
> 263 |           )
> 264 |           if not harmless:
>     |
>     = help: Merge `isinstance` calls for `statement`
>
> Found 1 error.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/venv-guard/stage2/attempts/venv-guard/attempt-3-20261119T084545957362Z-c7422ab7.md
> ```

Stage-2 call, 2026-11-19: review · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4743 commits, 12 rules.

## Phase 6 — Codex, 2026-11-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| R4 | MAJOR | SPEC | base | scripts/venv_guard.py:67 | When a caller uses `python -S` and the checkout’s usable `.venv` contains the missing dependency, the replacement retains `-S`, which disables the virtual environment’s site-packages. The import still fails instead of using the available dependency. [Acceptance criterion 1] | Codex | fixed — tests/test_venv_guard.py::test_site_disabled_invocation_enters_checkout_environment | no |
| R5 | MAJOR | SPEC | base | tests/test_venv_guard.py:258 | The check accepts `result = print("started")` before `import venv_guard`, because it treats every assignment as harmless. If the guard restarts the script, the message is printed twice. This is new evidence for the previously fixed finding about repeated effects: the check also misses calls inside assignments, decorators and class bodies. [Boundary; acceptance criterion 1] | Codex | fixed — tests/test_venv_guard.py::test_guard_check_detects_calls_in_early_definitions | no |
| R6 | MAJOR | SPEC | base | tests/test_venv_guard.py:195 | A script containing `import yaml, venv_guard` passes the guard-order check because the statement contains `venv_guard`, although Python imports `yaml` first. A caller missing PyYAML therefore fails before the guard can select the checkout environment. [Acceptance criterion 5] | Codex | fixed — tests/test_venv_guard.py::test_guard_check_rejects_combined_guard_import | no |

Phase 6 verdict: codex 01a1f32a-d3b9-7020-a7bf-a427c7c3287e, 2026-11-19
Reviewer session: codex 01a1f32a-d3b9-7020-a7bf-a427c7c3287e — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check

Stage-2 call, 2026-11-19: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4744 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/kit/probe.py` +4 -4
> - `scripts/venv_guard.py` +16 -1
> - `tests/test_venv_guard.py` +50 -3
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: targeted verification, not the full `make verify`; result: green; test files `tests/test_adoption.py`, `tests/test_archive_closed_changes.py`, `tests/test_bead_render.py`, `tests/test_check_adr_answers.py`, `tests/test_check_criterion_ledger.py`, `tests/test_check_interview_minimums.py`, `tests/test_check_question_context.py`, `tests/test_explore_provenance.py`, `tests/test_frontmatter_current.py`, `tests/test_gate_machinery.py`, `tests/test_harness_decide_adr.py`, `tests/test_harness_time_log.py`, `tests/test_kit.py`, `tests/test_lock.py`, `tests/test_pi_contract.py`, `tests/test_pr_sync.py`, `tests/test_ramp_valves.py`, `tests/test_regelwerk.py`, `tests/test_research_capture.py`, `tests/test_research_currency.py`, `tests/test_research_handoff.py`, `tests/test_run_report.py`, `tests/test_stage2_availability.py`, `tests/test_stage2_declaration.py`, `tests/test_stage2_free.py`, `tests/test_stage2_go_access.py`, `tests/test_stage2_repository_pathlock.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_catalog.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_stage2_research_judge.py`, `tests/test_stage2_research_limits.py`, `tests/test_stage2_research_map.py`, `tests/test_stage2_research_refs.py`, `tests/test_stage2_research_report.py`, `tests/test_stage2_session.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_terms_expiry.py`, `tests/test_templates.py`, `tests/test_this_repository_adoption.py`, `tests/test_touch_map.py`, `tests/test_venv_guard.py`, `tests/test_verify_cheap_first.py`, `tests/test_workflow_entry.py`; extra ruff targets none beyond the cheap checks; gates `leerprobe` (block), `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6
> - R5: tests/test_venv_guard.py::test_guard_check_detects_calls_in_early_definitions: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - R6: tests/test_venv_guard.py::test_guard_check_rejects_combined_guard_import: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/venv-guard/stage2/attempts/venv-guard/attempt-1-20261119T135909817451Z-066cb004.md
> ```

Stage-2 call, 2026-11-19: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1116 files, 4745 commits, 12 rules.

Runner restoration, 2026-11-19: repair · attempt 2 · route codex-repair — lifecycle fields: plans/changes/venv-guard/plan.md, plans/changes/venv-guard/spec.md — unchanged

Stage-2 call, 2026-11-19: review · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1116 files, 4746 commits, 12 rules.

## Phase 6 — Codex, 2026-11-19

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| R7 | MAJOR | SPEC | base | scripts/venv_guard.py:120 | A script that needs only PyYAML is restarted when the caller already has PyYAML but lacks an unrelated dependency such as pydantic. If the checkout’s PyYAML has different behavior, the script gets a different result even though its required dependency was available to the caller. [Acceptance criterion 1] | Codex | rejected — decisions.md Q-3 (maintainer, 2026-11-18): the guard re-executes when any of the three required dependencies is missing, as one set; a per-script dependency list was not chosen | — |
| R8 | MAJOR | SPEC | base | scripts/kit/probe.py:121 | A guarded script can print before calling a function that imports `venv_guard` and then `yaml`. The effect check returns an empty list when there is no top-level guard, so the check passes; if the function triggers a restart, the print occurs twice. [Boundary; acceptance criterion 1] | Codex | rejected — named Boundary in spec.md (AGENTS.md: a mechanism no choke point closes gets a Boundary): third further case of effects before the guard after Q-4; the static check covers top-level statements only, a lazy guard inside a function is outside it | — |
| R9 | MAJOR | SPEC | base | scripts/kit/probe.py:133 | The effect check accepts `os.environ["COUNT"] = "1"` before a top-level guard because it treats assignments without calls as harmless. Assignments to a subscript or attribute can change state, which is then applied again after a restart. This is a further case beyond calls inside assignments. [Boundary; acceptance criterion 1] | Codex | rejected — named Boundary in spec.md, same mechanism as R8: an assignment to a subscript or attribute before the guard counts as no effect for the static check | — |

Phase 6 verdict: codex 01a1f439-ef91-7532-aa81-cad36e366a3b, 2026-11-19
Reviewer session: codex 01a1f439-ef91-7532-aa81-cad36e366a3b — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check
