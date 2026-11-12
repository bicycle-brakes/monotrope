---
title: "Findings — targeted-check-more-verbs"
category: findings
status: draft
implementation_status: none
date: 2026-11-11
created: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-0swp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — targeted-check-more-verbs

Stage-2 call, 2026-11-11: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1014 files, 3938 commits, 12 rules.

Stage-2 call, 2026-11-11: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1017 files, 3953 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/targeted-check-more-verbs/plan.md` +12 -12
> - `scripts/stage2.py` +405 -118
> - `scripts/verify_duration.py` +375 -9
> - `tests/test_stage2.py` +1174 -297
> - `tests/test_verify_duration.py` +353 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/stage2.py`, `scripts/verify_duration.py`, `tests/test_stage2.py`, `tests/test_verify_duration.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> E                   TypeError: unsupported operand type(s) for |=: 'set' and 'tuple'
>
> scripts/stage2.py:6091: TypeError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 29 files, 2 commits, 1 rules, 1 prompt texts
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_failed_attempt_that_changed_nothing_says_so
> FAILED tests/test_stage2.py::test_a_failed_run_leaves_no_intent_to_add_entry
> FAILED tests/test_stage2.py::test_a_commit_message_holds_no_fragment_of_the_key
> FAILED tests/test_stage2.py::test_a_key_in_the_gate_output_never_reaches_the_next_attempt
> FAILED tests/test_stage2.py::test_a_passing_run_lists_each_format_line_in_its_commit_message
> FAILED tests/test_stage2.py::test_all_targeted_verbs_record_actual_scope[repair]
> FAILED tests/test_stage2.py::test_a_failed_stage2_off_attempt_leaves_its_block_without_reading_the_key
> FAILED tests/test_stage2.py::test_a_verify_that_cannot_start_still_leaves_the_block_and_the_findings_exit_line
> FAILED tests/test_stage2.py::test_a_key_the_gate_writes_under_venv_is_removed_and_refused
> FAILED tests/test_stage2.py::test_a_red_verify_fails_the_draft_attempt - Asse...
> FAILED tests/test_stage2.py::test_an_attempt_that_plants_the_registry_renderer_never_runs_it
> FAILED tests/test_stage2.py::test_all_targeted_verbs_record_actual_scope[implement]
> FAILED tests/test_stage2.py::test_a_failed_attempt_carries_its_format_line_first_in_its_diagnostics
> FAILED tests/test_stage2.py::test_a_long_file_list_is_cut_with_a_count - Type...
> FAILED tests/test_stage2.py::test_a_target_named_with_a_line_break_keeps_the_format_line_one_line
> FAILED tests/test_stage2.py::test_extended_targeted_routes_preserve_acceptance_guards[draft-time-heading]
> FAILED tests/test_stage2.py::test_extended_targeted_failures_never_checkpoint[timeout]
> FAILED tests/test_stage2.py::test_extended_targeted_routes_preserve_acceptance_guards[draft-missing-spec]
> FAILED tests/test_stage2.py::test_a_fallback_attempt_that_writes_the_key_leaves_no_blob_with_it
> FAILED tests/test_stage2.py::test_all_targeted_verbs_record_actual_scope[fallback]
> FAILED tests/test_stage2.py::test_discarded_model_changes_are_no_work[held-stamp]
> FAILED tests/test_stage2.py::test_each_failed_attempt_lists_only_the_files_its_model_changed
> FAILED tests/test_stage2.py::test_implement_refuses_uncovered_new_code_before_tests_or_fallback[baseline-only-test]
> FAILED tests/test_stage2.py::test_extended_targeted_failures_never_checkpoint[launch-error]
> FAILED tests/test_stage2.py::test_implement_preserves_full_fallback_boundaries[shared-infrastructure]
> FAILED tests/test_stage2.py::test_discarded_model_changes_are_no_work[index]
> FAILED tests/test_stage2.py::test_implement_refuses_uncovered_new_code_before_tests_or_fallback[covered-shell-fallback]
> FAILED tests/test_stage2.py::test_extended_targeted_failures_never_checkpoint[red-pytest]
> FAILED tests/test_stage2.py::test_implement_refuses_uncovered_new_code_before_tests_or_fallback[mixed-delta]
> FAILED tests/test_stage2.py::test_failed_check_diagnostics_redact_secret_rules_on_every_work_route[implement]
> FAILED tests/test_stage2.py::test_extended_targeted_routes_preserve_acceptance_guards[tool-tamper]
> FAILED tests/test_stage2.py::test_implement_preserves_full_fallback_boundaries[stage2-test-file]
> FAILED tests/test_stage2.py::test_discarded_model_changes_are_no_work[format-only]
> FAILED tests/test_stage2.py::test_extended_targeted_failures_never_checkpoint[red-gate]
> FAILED tests/test_stage2.py::test_implement_refuses_uncovered_new_code_before_tests_or_fallback[untracked-test-satisfies]
> FAILED tests/test_stage2.py::test_failed_check_diagnostics_redact_secret_rules_on_every_work_route[implement-off]
> FAILED tests/test_stage2.py::test_extended_targeted_routes_preserve_acceptance_guards[derived-order]
> FAILED tests/test_stage2.py::test_implement_routes_use_targeted_postchecks[initial]
> FAILED tests/test_stage2.py::test_draft_docs_check_keeps_admission_and_execution_limit
> FAILED tests/test_stage2.py::test_extended_targeted_routes_preserve_acceptance_guards[draft-card]
> FAILED tests/test_stage2.py::test_implement_routes_use_targeted_postchecks[fallback]
> FAILED tests/test_stage2.py::test_implement_refuses_uncovered_new_code_before_tests_or_fallback[existing-uncovered-fallback]
> FAILED tests/test_stage2.py::test_draft_docs_checks_preserve_preparation_and_artifact_guards
> FAILED tests/test_stage2.py::test_implement_refuses_uncovered_new_code_before_tests_or_fallback[before-tests]
> FAILED tests/test_stage2.py::test_implement_routes_use_targeted_postchecks[retry]
> FAILED tests/test_stage2.py::test_local_checks_preserve_nested_admission - Ke...
> FAILED tests/test_stage2.py::test_runner_time_logging_does_not_retry_red_verification
> FAILED tests/test_stage2.py::test_nonsecret_preparation_errors_stop_before_retry[implement]
> FAILED tests/test_stage2.py::test_make_verify_sees_the_attempts_new_files_in_git[implement]
> FAILED tests/test_stage2.py::test_sol_effort_changes_propagate_without_other_edits[repair-low-xhigh-medium]
> FAILED tests/test_stage2.py::test_secret_rules_outside_diagnostics_still_block_retry
> FAILED tests/test_stage2.py::test_targeted_selection_follows_import_chains_per_snapshot[chain]
> FAILED tests/test_stage2.py::test_make_verify_sees_the_attempts_new_files_in_git[repair]
> FAILED tests/test_stage2.py::test_sol_effort_changes_propagate_without_other_edits[repair-medium-high-xhigh]
> FAILED tests/test_stage2.py::test_targeted_repair_falls_back_to_full_on_uncovered_inputs[uncovered-code]
> FAILED tests/test_stage2.py::test_targeted_selection_follows_import_chains_per_snapshot[cycle]
> FAILED tests/test_stage2.py::test_targeted_selection_follows_import_chains_per_snapshot[no-cross-snapshot-fabrication]
> FAILED tests/test_stage2.py::test_first_implement_refreshes_derived_files_without_a_model_repair
> FAILED tests/test_stage2.py::test_targeted_selection_follows_import_chains_per_snapshot[rename]
> FAILED tests/test_stage2.py::test_targeted_mode_is_repair_only - TypeError: u...
> FAILED tests/test_stage2.py::test_targeted_stage2_test_file_requires_full_verification[0-linked]
> FAILED tests/test_stage2.py::test_targeted_stage2_test_file_requires_full_verification[1-touched]
> FAILED tests/test_stage2.py::test_targeted_stage2_test_file_requires_full_verification[0-touched]
> FAILED tests/test_stage2.py::test_targeted_stage2_test_file_requires_full_verification[1-linked]
> FAILED tests/test_stage2.py::test_targeted_selection_follows_import_chains_per_snapshot[retained-retry]
> FAILED tests/test_stage2.py::test_implement_and_fallback_repair_keep_full_verify_after_docs_draft
> FAILED tests/test_stage2.py::test_the_format_steps_writes_stay_out_of_the_models_file_list
> FAILED tests/test_verify_duration.py::test_targeted_history_preserves_safety_and_legacy_records
> FAILED tests/test_stage2.py::test_without_a_target_file_no_ruff_starts - Type...
> FAILED tests/test_stage2.py::test_when_every_attempt_fails_each_keeps_its_block_and_the_exit_names_findings
> FAILED tests/test_stage2.py::test_work_verbs_skip_escaped_scan_parent[implement-False]
> FAILED tests/test_stage2.py::test_implement_flash_has_file_tools_and_the_complete_contract
> 72 failed, 80 passed in 57.70s
> ```

Stage-2 call, 2026-11-12: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1017 files, 3964 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/targeted-check-more-verbs/plan.md` +12 -12
> - `scripts/stage2.py` +14 -3
> - `scripts/verify_duration.py` +10 -1
> - `tests/test_stage2.py` +6 -4
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         else:
>             fields = {"run_id": text, "utc": timestamp}
>         if kind == RUN_START:
>             fields.update(
>                 {
>                     "repository": text,
>                     "job": text,
>                     "placement": text,
>                     "commit": lambda v: v is None or text(v),
>                     "config_sha256": lambda v: v is None or text(v),
>                     "dirty": lambda v: v is None or type(v) is bool,
>                     "workers": lambda v: v is None or text(v),
>                     "admission_id": lambda v: v is None or text(v),
>                     "admission_reused": lambda v: v is None or type(v) is bool,
>                     "admission_wait_seconds": lambda v: v is None or seconds(v),
>                     "memory_pct": lambda v: v is None or (seconds(v) and v <= 100),
>                     "correlation": lambda v: v is None or text(v),
>                 }
>             )
>         elif kind == GATE:
>             fields.update(
>                 {
>                     "gate": text,
>                     "seconds": seconds,
>                     "exit": lambda v: type(v) is int,
>                     "enforcement": lambda v: v in ("block", "advisory", "report"),
>                 }
>             )
>         elif kind == RUN_END:
>             fields.update({"seconds": seconds, "verdict": lambda v: v in ("green", "red")})
>         elif kind == TARGETED:
>             fields.update(
>                 {
>                     "repository": text,
>                     "worktree": text,
>                     "change": text,
>                     "verb": text,
>                     "tests": names,
>                     "gates": names,
>                     "outcome": lambda v: v in ("green", "red"),
>                     "config_sha256": lambda v: v is None or text(v),
>                     "tree": text,
>                     "commit": lambda v: v is None or text(v),
>                 }
>             )
>         else:
>             fields.update(
>                 {
>                     "repository": text,
>                     "failed_gates": names,
>                     "failed_tests": lambda v: v is None or names(v),
>                     "config_sha256": lambda v: v is None or text(v),
>                     "tree": text,
>                 }
>             )
>         invalid: list[str] = []
>         for name, check in fields.items():
>             # `correlation` arrived with coding-harness-0swp: version-1 records written before it
>             # carry no such field and must keep reading as valid, so absence is the unknown.
>             absent = name not in event and name not in START_OPTIONAL_FIELDS
> >           if absent or not check(event[name]):
> E           KeyError: 'correlation'
>
> scripts/verify_duration.py:701: KeyError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_failed_attempt_that_changed_nothing_says_so
> FAILED tests/test_stage2.py::test_a_passing_run_lists_each_format_line_in_its_commit_message
> FAILED tests/test_stage2.py::test_a_failed_attempt_carries_its_format_line_first_in_its_diagnostics
> FAILED tests/test_stage2.py::test_all_targeted_verbs_record_actual_scope[fallback]
> FAILED tests/test_stage2.py::test_a_target_named_with_a_line_break_keeps_the_format_line_one_line
> FAILED tests/test_stage2.py::test_a_long_file_list_is_cut_with_a_count - Valu...
> FAILED tests/test_stage2.py::test_implement_refuses_uncovered_new_code_before_tests_or_fallback[baseline-only-test]
> FAILED tests/test_stage2.py::test_extended_targeted_routes_preserve_acceptance_guards[tool-tamper]
> FAILED tests/test_stage2.py::test_implement_routes_use_targeted_postchecks[retry]
> FAILED tests/test_stage2.py::test_secret_rules_outside_diagnostics_still_block_retry
> FAILED tests/test_stage2.py::test_implement_and_fallback_repair_keep_full_verify_after_docs_draft
> FAILED tests/test_stage2.py::test_the_format_steps_writes_stay_out_of_the_models_file_list
> FAILED tests/test_stage2.py::test_without_a_target_file_no_ruff_starts - Asse...
> FAILED tests/test_verify_duration.py::test_targeted_history_preserves_safety_and_legacy_records
> 14 failed, 138 passed in 64.36s (0:01:04)
> ```

Stage-2 call, 2026-11-12: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1017 files, 3969 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/verify_duration.py` +5 -2
> - `tests/test_stage2.py` +54 -32
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_stage2.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> ----------------------------- Captured stderr call -----------------------------
> failed: the draft failed after the allowed attempts; why each attempt failed and the files each changed: plans/changes/demo/findings.md
> __________ test_targeted_history_preserves_safety_and_legacy_records ___________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/targeted-check-more-verbs/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-86/popen-gw2/test_targeted_history_preserve0')
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x106e4f980>
> capsys = <_pytest.capture.CaptureFixture object at 0x106e4d010>
>
>     def test_targeted_history_preserves_safety_and_legacy_records(
>         tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
>     ) -> None:
>         """Criterion 11. Faults this pins: a new event kind breaking the version-1 reader or its
>         verdicts, raw output or a credential landing in a record, concurrent slip writers mixing or
>         doubling a row, a storage failure changing a verdict instead of being named, or a substituted
>         destination being written through by one of the new writers.
>         """
>         state = tmp_path / "state"
>         root = state / "coding-harness"
>         root.mkdir(parents=True)
>         path = root / verify_duration.HISTORY_NAME
>     
>         # The version-1 records read exactly as before, beside targeted and slip rows: the new
>         # kinds never join a run, so the old run keeps its green verdict and its detail view.
>         legacy = _valid_records("legacy-run")
>         targeted_row = {
>             "v": 1,
>             "event": "targeted",
>             "check_id": "check-one",
>             "utc": "2026-11-04T10:02:00+00:00",
>             "repository": str(REPO_ROOT),
>             "worktree": str(tmp_path),
>             "change": "demo",
>             "verb": "implement",
>             "tests": ["tests/test_demo.py"],
>             "gates": ["criterion-ledger"],
>             "outcome": "green",
>             "config_sha256": "e" * 64,
>             "tree": "f" * 40,
>             "commit": None,
>         }
>         slip_row = {
>             "v": 1,
>             "event": "slip",
>             "check_id": "check-one",
>             "run_id": "legacy-run",
>             "utc": "2026-11-04T10:03:00+00:00",
>             "repository": str(REPO_ROOT),
>             "failed_gates": ["pytest"],
>             "failed_tests": None,
>             "config_sha256": "e" * 64,
>             "tree": "f" * 40,
>         }
>         path.write_text("\n".join(json.dumps(row) for row in [*legacy, targeted_row, slip_row]) + "\n", encoding="utf-8")
>         code, out, _ = _run(capsys, "report")
>         assert code == 0, out
>         assert "run legacy-run" in out and "green" in out and "1.500s" in out, out
>         assert "history note:" not in out, "a targeted or slip row was mistaken for a version-1 record"
>         code, out, _ = _run(capsys, "report", "--run", "legacy-run")
> >       assert code == 0 and "probe" in out and "verdict: green" in out, out
> E       AssertionError: run legacy-run
> E           started (UTC): 2026-11-04T10:00:00+00:00
> E           repository: /repo · commit: unknown · dirty: unknown
> E           gate configuration (sha256): unknown
> E           job: verify · placement: local
> E           free memory at start: unknown
> E           workers: unset (xdist decides)
> E           admission: unknown · wait: unknown · reused: unknown
> E           gates:
> E             pytest  0.000s  exit 0  block
> E           execution: 1.500s · verdict: green
> E         
> E       assert (0 == 0 and 'probe' in 'run legacy-run\n  started (UTC): 2026-11-04T10:00:00+00:00\n  repository: /repo · commit: unknown · dirty: unknown\n ...· wait: unknown · reused: unknown\n  gates:\n    pytest  0.000s  exit 0  block\n  execution: 1.500s · verdict: green\n')
>
> tests/test_verify_duration.py:742: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_implement_refuses_uncovered_new_code_before_tests_or_fallback[baseline-only-test]
> FAILED tests/test_stage2.py::test_secret_rules_outside_diagnostics_still_block_retry
> FAILED tests/test_verify_duration.py::test_targeted_history_preserves_safety_and_legacy_records
> 3 failed, 149 passed in 64.00s (0:01:04)
> ```

Stage-2 call, 2026-11-12: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason fourth run from attempt 3's saved state on the maintainer's answer of 2026-11-12 (bead coding-harness-0swp); three tests still red: test_implement_refuses_uncovered_new_code_before_tests_or_fallback[baseline-only-test], test_secret_rules_outside_diagnostics_still_block_retry, test_targeted_history_preserves_safety_and_legacy_records · leak check clean over 1040 files, 3990 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/targeted-check-more-verbs/plan.md` +12 -12
> - `tests/test_stage2.py` +7 -2
> - `tests/test_verify_duration.py` +3 -2
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: the whole tests/test_stage2.py requires full verification until coding-harness-vg9 splits it
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 562 lines of this gate left out …]
>                 {"stdout": "must not run"},
>                 {"stdout": "must not run"},
>             ],
>             ruff=[{}] * 8,
>             python3=[{}] * 3,
>             make=[red] * 3,
>         )
>         assert world.run("implement") == 1
>         names = [call["name"] for call in world.calls()]
> >       assert names[:7] == ["claude", "ruff", "ruff", "ruff", "ruff", "python3", "make"], names[:7]
> E       AssertionError: ['claude', 'ruff', 'ruff', 'claude', 'ruff', 'ruff', ...]
> E       assert ['claude', 'r..., 'ruff', ...] == ['claude', 'r...python3', ...]
> E         
> E         At index 3 diff: 'claude' != 'ruff'
> E         Use -v to get more diff
>
> tests/test_stage2_fail_fast.py:223: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 29 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 32 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 32 files, 2 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: implementation post-run checks failed after the allowed attempts; why each attempt failed and the files it changed: plans/changes/demo/findings.md
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=94603) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=94604) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/targeted-check-more-verbs/tests/test_stage2.py:21830: DeprecationWarning: This process (pid=94603) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_bash_call_beside_the_document_check_runs_the_real_bash
> FAILED tests/test_stage2.py::test_runner_preserves_precall_time_on_final_verdict[False]
> FAILED tests/test_stage2.py::test_a_failed_attempt_quotes_its_diagnostics_below_its_audit_line
> FAILED tests/test_stage2.py::test_an_unmeasured_file_list_says_why_and_changes_nothing_else
> FAILED tests/test_stage2.py::test_a_failure_after_the_first_snapshot_says_why_and_changes_nothing_else
> FAILED tests/test_stage2.py::test_an_unmeasured_reason_stays_one_line_with_one_full_stop
> FAILED tests/test_stage2.py::test_a_malformed_numstat_record_says_not_measured_and_the_run_goes_on
> FAILED tests/test_stage2.py::test_a_passing_attempt_leaves_only_its_audit_line[first-try]
> FAILED tests/test_stage2.py::test_a_passing_attempt_leaves_only_its_audit_line[after-a-failure]
> FAILED tests/test_stage2.py::test_ruff_gets_the_verify_environment_without_credentials
> FAILED tests/test_stage2.py::test_a_passing_attempt_that_was_formatted_leaves_only_its_audit_line
> FAILED tests/test_stage2_fail_fast.py::test_empty_targets_skip_their_command
> FAILED tests/test_stage2_fail_fast.py::test_cheap_green_still_requires_full_verification
> 13 failed, 5653 passed, 17 skipped, 5 warnings in 1447.97s (0:24:07)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 38338 earlier lines left out …]
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

Stage-2 call, 2026-11-12: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason fifth run from attempt 4's saved state with the correction of decisions.md Q-6 (maintainer 2026-11-12, bead coding-harness-0swp): follow the plan section 'Correction for the fifth run' · leak check clean over 1040 files, 3999 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +17 -12
> - `scripts/time_records.py` +9 -2
> - `tests/test_stage2.py` +53 -21
> - `tests/test_stage2_fail_fast.py` +27 -10
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> .......F................................................................ [ 66%]
> ....................................                                     [100%]
> =================================== FAILURES ===================================
> ________ test_a_bash_call_beside_the_document_check_runs_the_real_bash _________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/targeted-check-more-verbs/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-165/popen-gw0...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-165/popen-gw0/test_a_bash_call_beside_the_do0/state'))
>
>     def test_a_bash_call_beside_the_document_check_runs_the_real_bash(world):
>         # The stand-in shadows bash for every test; a call that is not the document check must neither
>         # consume a scripted step nor answer green for a command no test scripted.
>         world.script(docs=[{"stdout": "scripted", "exit": 0}])
>         out = subprocess.run([str(world.bin / "bash"), "-c", "echo real; exit 3"], capture_output=True, text=True)
>         assert (out.returncode, out.stdout) == (3, "real\n"), "a non-document bash call was stubbed"
>         assert world.calls("bash") == [], "a non-document bash call was recorded as a document check"
>         assert json.loads((world.bin / "scenario.json").read_text())["_bash"] == REAL_BASH != str(world.bin / "bash")
>         world.script(bash=[{"stdout": "stub"}])
>         out = subprocess.run([str(world.bin / "bash"), "-c", "echo real"], capture_output=True, text=True)
> >       assert out.returncode == 97 and "not served" in out.stderr, "a scripted bash step was silently dropped"
> E       AssertionError: a scripted bash step was silently dropped
> E       assert (0 == 97)
> E        +  where 0 = CompletedProcess(args=['/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-165/popen-gw0/test_a_bash_call_beside_the_do0/bin/bash', '-c', 'echo real'], returncode=0, stdout='real\n', stderr='').returncode
>
> tests/test_stage2.py:4579: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_bash_call_beside_the_document_check_runs_the_real_bash
> 1 failed, 107 passed in 109.07s (0:01:49)
> ```
