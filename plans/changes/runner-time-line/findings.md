---
title: "Findings — runner-time-line"
category: findings
status: draft
implementation_status: none
date: 2026-10-20
created: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-9wp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — runner-time-line

Stage-2 call, 2026-10-20: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 499 files, 1634 commits, 12 rules.

Stage-2 call, 2026-10-20: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 502 files, 1648 commits, 12 rules.

Stage-2 call, 2026-10-20: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM model name refused by Claude Code (bead coding-harness-6th); Codex paused by the maintainer · leak check clean over 502 files, 1648 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +4 -4
> - `plans/changes/runner-time-line/plan.md` +10 -8
> - `prompts/04-implement.md` +5 -2
> - `scripts/stage2.py` +99 -18
> - `tests/test_stage2.py` +208 -28
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `scripts/stage2.py`, `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 2908 lines of this gate left out …]
>
>     def test_a_failed_stage2_off_attempt_leaves_its_block_without_reading_the_key(
>         world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
>     ) -> None:
>         # Criterion 15. Planted fault: the block reads the key to scrub it.
>         monkeypatch.setattr(stage2, "read_secret", lambda name: pytest.fail(f"read secret on Stage 1: {name}"))
>         world.script(claude=[{"stdout": "nothing"}], make=[{"stdout": "green"}])
> >       assert world.run("implement", "demo", "--stage2-off", "Z.ai unavailable") == 1
> E       AssertionError: assert 0 == 1
> E        +  where 0 = run('implement', 'demo', '--stage2-off', 'Z.ai unavailable')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-255/popen-gw5...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-255/popen-gw5/test_a_failed_stage2_off_attem0/state')).run
>
> tests/test_stage2.py:3790: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 22 files, 2 commits, 1 rules, 1 prompt texts
> implement: verified and committed · route stage-1 · attempt 1
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_implement_flash_has_file_tools_and_the_complete_contract
> FAILED tests/test_stage2.py::test_a_leak_between_work_attempts_stops_before_fallback
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[plan-first]
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[plan-second]
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[plan-both]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[spec-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[spec-2]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[plan-1]
> FAILED tests/test_stage2.py::test_a_failed_attempt_quotes_its_diagnostics_below_its_audit_line
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[plan-2]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[decisions-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[decisions-2]
> FAILED tests/test_stage2.py::test_a_failed_attempt_that_changed_nothing_says_so
> FAILED tests/test_stage2.py::test_an_unmeasured_file_list_says_why_and_changes_nothing_else
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[design-1]
> FAILED tests/test_stage2.py::test_a_failure_after_the_first_snapshot_says_why_and_changes_nothing_else
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[design-2]
> FAILED tests/test_stage2.py::test_an_unmeasured_reason_stays_one_line_with_one_full_stop
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[phase-prompt-1]
> FAILED tests/test_stage2.py::test_a_malformed_numstat_record_says_not_measured_and_the_run_goes_on
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[phase-prompt-2]
> FAILED tests/test_stage2.py::test_a_passing_attempt_leaves_only_its_audit_line[after-a-failure]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[agent-rules-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[agent-rules-2]
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[all-inputs-first]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[all-inputs-1]
> FAILED tests/test_stage2.py::test_repair_retry_starts_after_a_completed_attempt_deletes_plan[all-inputs-2]
> FAILED tests/test_stage2.py::test_when_every_attempt_fails_each_keeps_its_block_and_the_exit_names_findings
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[all-inputs-second]
> FAILED tests/test_stage2.py::test_a_restore_after_a_dead_model_keeps_the_earlier_blocks
> FAILED tests/test_stage2.py::test_repair_retry_restores_non_utf8_prompt_inputs[all-inputs-both]
> FAILED tests/test_stage2.py::test_repair_retry_restores_aliased_and_directory_inputs_without_following
> FAILED tests/test_stage2.py::test_repair_prompts_keep_the_initial_input_snapshot[plan-1]
> FAILED tests/test_stage2.py::test_repair_prompts_keep_the_initial_input_snapshot[plan-2]
> FAILED tests/test_stage2.py::test_the_format_steps_writes_stay_out_of_the_models_file_list
> FAILED tests/test_stage2.py::test_a_passing_run_lists_each_format_line_in_its_commit_message
> FAILED tests/test_stage2.py::test_a_long_file_list_is_cut_with_a_count - Valu...
> FAILED tests/test_stage2.py::test_a_failed_stage2_off_attempt_leaves_its_block_without_reading_the_key
> 38 failed, 2261 passed, 16 skipped in 343.52s (0:05:43)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> scripts/stage2.py:3085:5: ARG001 Unused function argument: `baseline_time`
>      |
> 3083 |     root: Path,
> 3084 |     plan: Path,
> 3085 |     baseline_time: str,
>      |     ^^^^^^^^^^^^^ ARG001
> 3086 |     key: str | None = None,
> 3087 |     formatted: list[str] | None = None,
>      |
>
> Found 1 error.
> ── [ruff-check] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12244 earlier lines left out …]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````
