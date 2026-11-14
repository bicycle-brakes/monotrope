---
title: "Findings — flaky-swarm-leak-test"
category: findings
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-yb1l
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — flaky-swarm-leak-test

Stage-2 call, 2026-11-13: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1043 files, 4097 commits, 12 rules.

Stage-2 call, 2026-11-13: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1046 files, 4107 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/flaky-swarm-leak-test/plan.md` +31 -8
> - `plans/changes/flaky-swarm-leak-test/spec.md` +1 -1
> - `tests/atomic_test_log.py` +83 -0
> - `tests/test_atomic_test_log.py` +407 -0
> - `tests/test_pi_install.py` +39 -25
> - `tests/test_stage2.py` +63 -71
> - `tests/test_stage2_research_availability.py` +13 -5
> - `tests/test_stage2_session.py` +19 -9
> - `tests/test_stage2_swarm.py` +22 -16
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_atomic_test_log.py`, `tests/test_pi_install.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ....FF.....                                                              [100%]
> =================================== FAILURES ===================================
> _________________ test_guard_detects_new_unlocked_log_appends __________________
> [gw6] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/flaky-swarm-leak-test/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-76/popen-gw6/test_guard_detects_new_unlocke0')
>
>     def test_guard_detects_new_unlocked_log_appends(tmp_path: Path) -> None:
>         """Criterion 5 (flaky-swarm-leak-test). Planted fault: a planted bypass passes the guard, or a safe operation is flagged.
>     
>         A new top-level log append, a new embedded stand-in append, and the
>         positional and keyword forms are each detected with their source location;
>         the safe non-append operations stay unflagged.
>         """
>         one = tmp_path / "top"
>         one.mkdir()
>         (one / "planted_top.py").write_text(_render(TOP_APPEND), encoding="utf-8")
>         found = find_append_bypasses(one)
> >       assert len(found) == 1 and "planted_top.py" in found[0] and ":2:" in found[0], found
> E       AssertionError: []
> E       assert (0 == 1)
> E        +  where 0 = len([])
>
> tests/test_atomic_test_log.py:379: AssertionError
> __________________ test_concurrent_log_snapshots_are_complete __________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/flaky-swarm-leak-test/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-76/popen-gw0/test_concurrent_log_snapshots_0')
>
>     def test_concurrent_log_snapshots_are_complete(tmp_path: Path) -> None:
>         """Criterion 1 (flaky-swarm-leak-test). Planted fault: the fixture observer reads a forced mid-append fragment.
>     
>         The child holds the shared sidecar lock and appends half of one large
>         record before the test lets it finish. An unlocked read at that moment is
>         the red control: it observes the fragment the pre-fix reader would have
>         parsed. The real `SwarmWorld.calls` observer must instead wait for the
>         completed record.
>         """
>         log = tmp_path / "calls.jsonl"
>         gap = tmp_path / "gap"
>         gap.mkdir()
>         append_record(log, {"seq": 0, "payload": "seed"})
>         script = tmp_path / "split_writer.py"
>         script.write_text(_render(SPLIT_WRITER), encoding="utf-8")
>         child = subprocess.Popen(
>             [sys.executable, str(script), str(log), str(gap), str(HERE), PAYLOAD],
>             stdout=subprocess.DEVNULL,
>             stderr=subprocess.PIPE,
>             text=True,
>         )
>         world = SwarmWorld(root=tmp_path, bin=tmp_path, home=tmp_path)
>         observed: dict = {}
>         try:
> >           _wait_for(gap / "started.marker", child)
>
> tests/test_atomic_test_log.py:248: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> marker = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-76/popen-gw0/test_concurrent_log_snapshots_0/gap/started.marker')
> child = <Popen: returncode: 1 args: ['/Users/mikypiky/coding-harness/.claude/worktre...>
>
>     def _wait_for(marker: Path, child: subprocess.Popen) -> None:
>         """Wait, bounded, for a child's file handshake; never an open-ended sleep."""
>         deadline = time.time() + 60
>         while not marker.exists():
>             if child.poll() is not None:
> >               pytest.fail(f"the split writer exited early with {child.returncode}")
> E               Failed: the split writer exited early with 1
>
> tests/test_atomic_test_log.py:197: Failed
> =========================== short test summary info ============================
> FAILED tests/test_atomic_test_log.py::test_guard_detects_new_unlocked_log_appends
> FAILED tests/test_atomic_test_log.py::test_concurrent_log_snapshots_are_complete
> 2 failed, 9 passed in 7.76s
> ```

Stage-2 call, 2026-11-13: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1048 files, 4132 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_atomic_test_log.py` +1 -1
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ python3 -m pytest tests/ -q -n auto
> [… 1380 lines of this gate left out …]
>   - leak check clean: 30 files, 3 commits, 1 rules, 1 prompt texts
> repair: the attempt's protected answer is saved at /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-95/popen-gw0/test_a_red_first_interpreter_t0/repo/.git/stage2/attempts/demo/attempt-1-20261113T210044341426Z-42f341dd.md
> repair: verified and committed · route codex · attempt 1
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> [verify-lock] admitted
> [verify-lock] available memory cannot be measured; proceeding without a reading
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=40105) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/flaky-swarm-leak-test/tests/test_stage2.py:21812: DeprecationWarning: This process (pid=40104) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_each_failed_attempt_lists_only_the_files_its_model_changed
> FAILED tests/test_stage2.py::test_no_work_attempt_is_rejected[implement-time-body-only]
> FAILED tests/test_stage2.py::test_no_work_attempt_is_rejected[repair-time-body-only]
> FAILED tests/test_stage2.py::test_bookkeeping_scenario_has_no_implicit_work[time-body-only]
> FAILED tests/test_stage2.py::test_runner_ledger_clearing_cannot_qualify_a_retry[implement-full]
> FAILED tests/test_stage2.py::test_runner_ledger_clearing_cannot_qualify_a_retry[repair-targeted]
> FAILED tests/test_stage2.py::test_standard_world_preserves_repair_and_review_dispatch
> FAILED tests/test_stage2.py::test_covered_repair_uses_targeted_verification
> FAILED tests/test_stage2.py::test_targeted_repair_runs_whole_touched_and_linked_test_files[linked-sibling]
> FAILED tests/test_stage2.py::test_an_invalid_change_name_takes_no_lock[review-loop]
> FAILED tests/test_stage2.py::test_an_invalid_change_name_takes_no_lock[release-loop]
> FAILED tests/test_stage2.py::test_an_invalid_change_name_takes_no_lock[prepare-loop]
> FAILED tests/test_stage2.py::test_an_invalid_change_name_takes_no_lock[review]
> FAILED tests/test_stage2.py::test_an_invalid_change_name_takes_no_lock[repair]
> FAILED tests/test_stage2.py::test_targeted_repair_runs_whole_touched_and_linked_test_files[retained-retry]
> FAILED tests/test_stage2.py::test_targeted_repair_checks_touched_python_after_formatting
> FAILED tests/test_stage2.py::test_targeted_repair_selects_declared_gates_and_enforcement[check_docs.py-False]
> FAILED tests/test_stage2.py::test_targeted_repair_selects_declared_gates_and_enforcement[check_criterion_ledger.py-True]
> FAILED tests/test_stage2.py::test_targeted_commands_run_without_verify_admission
> FAILED tests/test_stage2.py::test_a_failed_runs_derived_writes_do_not_block_the_next_run
> FAILED tests/test_stage2.py::test_targeted_pytest_timeout_rejects_without_full_fallback
> FAILED tests/test_stage2.py::test_targeted_failure_never_checkpoints_or_marks_fixed[red-pytest]
> FAILED tests/test_stage2.py::test_targeted_failure_never_checkpoints_or_marks_fixed[red-block-gate]
> FAILED tests/test_stage2.py::test_targeted_failure_never_checkpoints_or_marks_fixed[timeout]
> FAILED tests/test_stage2.py::test_targeted_failure_never_checkpoints_or_marks_fixed[launch-error]
> FAILED tests/test_stage2.py::test_targeted_repair_preserves_preparation_and_answer_proofs[derived-refresh]
> FAILED tests/test_stage2.py::test_repair_records_verification_scope_and_outcome[targeted]
> FAILED tests/test_stage2.py::test_repair_records_verification_scope_and_outcome[fallback]
> FAILED tests/test_stage2.py::test_repair_records_verification_scope_and_outcome[fallback-launch-failure]
> FAILED tests/test_stage2.py::test_a_red_first_interpreter_that_cannot_start_pytest_fails_the_attempt
> 30 failed, 5621 passed, 17 skipped, 5 warnings in 501.08s (0:08:21)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 40527 earlier lines left out …]
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

Stage-2 call, 2026-11-13: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1048 files, 4141 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/flaky-swarm-leak-test/plan.md` +7 -7
> - `tests/atomic_test_log.py` +17 -7
> - `tests/test_stage2.py` +1 -1
> - `tests/test_stage2_swarm.py` +6 -2
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ..................................F...................                   [100%]
> =================================== FAILURES ===================================
> _______________________ test_a_stand_in_contacts_nothing _______________________
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/flaky-swarm-leak-test/.venv/bin/python3
>
>     def test_a_stand_in_contacts_nothing() -> None:
>         rendered = STAND_IN.replace("@PYTHON@", "python3").replace("@PI@", "1.1.0")
>         rendered = rendered.replace(atomic_test_log.MARKER, ATOMIC_LOG_SOURCE)
>         tree = ast.parse(rendered)
>         imported = {
>             alias.name.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names
>         } | {node.module.split(".")[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
>         # The embedded log protocol (`fcntl`) locks the stand-in's own call log; it opens no connection.
> >       assert imported <= {"fcntl", "json", "os", "sys", "time", "pathlib"}
> E       AssertionError: assert {'fcntl', 'ha...', 'sys', ...} <= {'fcntl', 'js...'sys', 'time'}
> E         
> E         Extra items in the left set:
> E         'hashlib'
>
> tests/test_stage2.py:805: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_stand_in_contacts_nothing - AssertionErro...
> 1 failed, 53 passed in 18.54s
> ```

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1048 files, 4177 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1048 files, 4178 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1048 files, 4178 commits, 12 rules.

Loop attempt: 2026-11-14 — no round was written; the review-loop calls above consumed no stage; audit calls: 1

Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).

Notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base.

Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).

Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor.

Notice: the data terms of longcat-2.0 expire on 2026-11-16 (2 days left).

Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (2 days left).

Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (2 days left).

Notice: the data terms of gpt-6-luna expire on 2026-11-16 (2 days left).

Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (2 days left).

Notice: the data terms of minimax-m3 expire on 2026-11-16 (2 days left).

Notice: the data terms of glm-5.2 expire on 2026-11-21 (7 days left).

Notice: the data terms of glm-5.3 expire on 2026-11-21 (7 days left).

Notice: the data terms of hy3 expire on 2026-11-21 (7 days left).

Notice: the data terms of hy4-preview expire on 2026-11-21 (7 days left).

Notice: the data terms of mimo-v2.5 expire on 2026-11-21 (7 days left).

Notice: the data terms of mimo-v2.5-pro expire on 2026-11-21 (7 days left).

Notice: the data terms of mimo-v2.6-flash expire on 2026-11-21 (7 days left).

Notice: the data terms of qwen3.7-plus expire on 2026-11-21 (7 days left).

Notice: the data terms of qwen3.8-max expire on 2026-11-21 (7 days left).

Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1065 files, 4182 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1065 files, 4183 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1065 files, 4200 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model hy3 · leak check clean over 1065 files, 4211 commits, 12 rules.

Stage-2 call, 2026-11-14: review-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1065 files, 4213 commits, 12 rules.

Stage-2 call, 2026-11-14: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1065 files, 4213 commits, 12 rules.

> Runner verification scope:
> - Attempt 1 (codex): targeted verification, not the full `make verify`; result: green; test files `tests/test_atomic_test_log.py`, `tests/test_pi_install.py`, `tests/test_stage2_research_availability.py`, `tests/test_stage2_session.py`, `tests/test_stage2_swarm.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6

Runner restoration, 2026-11-14: repair · attempt 1 · route codex — lifecycle fields: plans/changes/flaky-swarm-leak-test/plan.md, plans/changes/flaky-swarm-leak-test/spec.md — unchanged

Stage-2 call, 2026-11-14: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1065 files, 4227 commits, 12 rules.

## Phase 6 — Codex, 2026-11-14

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MAJOR | SPEC | fix-r1 | tests/test_atomic_test_log.py:303 | The guard ignores keyword arguments: `open(file="calls.jsonl", mode="a")` and `open(file="calls.jsonl")` both produced zero findings in an in-memory probe, while positional access was detected. Ordinary unlocked writes and reads of a declared log therefore pass the guard and can reintroduce torn observations. [Acceptance criterion 5] | Codex | taken — the guard reads the file and mode of every open() from positional and keyword arguments alike (file=, mode=), a test holds both spellings for append and read of a declared log; same mechanism as the loop guard rows, repaired at the one place the guard resolves open() arguments | — |
| F6-2 | MAJOR | SPEC | base | tests/test_atomic_test_log.py:334–337 | The race test releases the split writer immediately after starting the reader thread, without establishing that the observer has attempted its read. If the observer runs after the writer completes, an unlocked reader passes. Reproduced with the unchanged test body and the original unlocked `SwarmWorld.calls` under that controlled in-memory schedule. The regression check therefore depends on scheduling despite requiring deterministic handshakes. [Acceptance criteria 1 and 7] | Codex | taken — the race test waits on a handshake that proves the observer has attempted its read before the split writer is released (no timing), so an unlocked reader fails deterministically | — |
| F6-3 | BLOCKER | SPEC | fix-r3 | plans/changes/flaky-swarm-leak-test/spec.md:59–68; tests/test_stage2_swarm.py:288; tests/atomic_test_log.py:82–88 | [DIVERGENT] The receipt contract says the stand-in uses `text_append` and its lock orders stand-in appends, then explicitly says those same appends remain outside the helper’s lock. The implementation always takes an exclusive lock through `text_append`. The specification gives opposite answers about whether receipt appends must acquire that lock; the required behavior needs reconciliation. [Receipt-log contract; acceptance criterion 4] | Codex | taken — not a test: the spec's receipt contract follows the implementation and loop row L2-6: the stand-in appends receipts through text_append under the helper's lock, which orders only the stand-in's own appends; the production writer stays outside it; the sentence placing the stand-in's appends on the unlocked path is removed | — |

Phase 6 verdict: codex 01a1db5c-50d7-7633-9870-3b48b722e9fc, 2026-11-14
Reviewer session: codex 01a1db5c-50d7-7633-9870-3b48b722e9fc — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-14

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | base | plans/changes/flaky-swarm-leak-test/spec.md (criterion 4) vs. tests/test_atomic_test_log.py:EXEMPT_OPERATIONS | The spec and research declare a complete inventory of 17 append-mode opens in five test files, but the guard's own exemption list documents at least three further append-mode opens in files that inventory never names: a `a+` probe in `tests/test_stage2_availability.py`, an append to an admission-order probe log in `tests/test_verify_lock.py`, and a binary append to the fixture research document in `tests/test_stage2_research_store.py`. Criterion 4's "any of the 15 data appends" therefore understates the set, and the `tests/test_verify_lock.py` site writes a log in append mode that the shared helper does not migrate and the spec does not mention. | deepseek-v4.1-flash | fixed — orchestrator hand edit c7215701 (Opus subagent, maintainer's word of 2026-11-14) | no | disagree — The additional sites are document mutations and production-lock probes outside the stand-in log inventory. |
| L1-2 | MAJOR | SPEC | base | tests/test_atomic_test_log.py:find_append_bypasses | The maintainer asked for a guard that fails when a test file opens a *log* for appending without the shared helper, but the implemented guard flags every append-mode `open`/`Path.open` under `tests/`, including document mutations, scenario text appends and lock probes. It already needs ten hand-written exemptions for existing non-log operations, and every future test that appends to any file now fails this required test until it is added to that list — a scope wider than the decision it implements. | deepseek-v4.1-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-3 | MAJOR | MAINT | base | tests/test_atomic_test_log.py::test_test_logs_use_the_shared_helper | The guard pins the exact stripped source lines of `tests/test_stage2_availability.py`, `tests/test_verify_lock.py` and `tests/test_stage2_research_store.py` and asserts each still exists, while the change declares every test file beyond its seven named files protected and untouched. An unrelated edit to any of those lines elsewhere in the repository fails this change's guard with "stale exemption", so the change couples the suite to lines it does not own. | deepseek-v4.1-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-4 | MAJOR | MAINT | base | tests/atomic_test_log.py:HoldLock, read_records | A missing log whose parent directory is also absent now raises `FileNotFoundError` from the sidecar open, whereas every replaced reader returned an empty list for any missing log (`if log.exists() else []`). The module docstring and criterion 4 promise that a missing data file reads as an empty snapshot, so the edge case where the directory is gone breaks the promised contract. | deepseek-v4.1-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-5 | MINOR | MAINT | base | tests/atomic_test_log.py:HoldLock | The sidecar lock is acquired with an unbounded blocking `flock`, and the new observer is called from inside the production gate's print. A stand-in that wedges while holding the lock therefore blocks the dispatcher's gate call indefinitely, replacing the torn-read flake with a hang, while the bounded handshake helper `_wait_for` guards only the child process, not the reader side. | deepseek-v4.1-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-6 | MINOR | MAINT | base | tests/atomic_test_log.py:append_record, lock_path | `append_record` cannot take a `lock_dir` although `text_append` can, and the stand-in passes `lock_dir=here` for scenario appends while every reader of the same file uses the default beside-the-data sidecar. The sidecar name for the `lock_dir` form is derived from `path.resolve()` in the writer's working directory, so two sides of one file can end up on different lock identities — the mismatch this change exists to remove. | deepseek-v4.1-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-7 | MINOR | SPEC | base | tests/test_stage2.py::test_a_stand_in_contacts_nothing | The plan promises to retain stdlib-only no-contact checks for every rendering of the stand-in constants and their alternate executable paths, but only `STAND_IN` of `tests/test_stage2.py` is parsed for imports. The four other stand-ins (installer, session, availability, swarm) now embed the whole helper source, prose included, and nothing asserts they stay free of new imports. | deepseek-v4.1-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-8 | MAJOR | MAINT | base | tests/test_atomic_test_log.py::find_append_bypasses; spec.md criterion 5 | The guard inspects only append-mode opens, so a new test that reads a stand-in log without the helper (a plain read_text or json.loads while a locked writer is mid-append) still observes a torn fragment and can redden the suite while the guard stays green. Q-2's answer promises the torn-read flake cannot return through a new test, but nothing in the change watches the read side. | mimo-v2.6-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-9 | MAJOR | SPEC | base | plans/changes/flaky-swarm-leak-test/findings.md, plans/changes/flaky-swarm-leak-test/plan.md | The change records no green run on the final head: the last recorded make verify (attempt 2) exited 2 with 30 failures across test_stage2.py tests unrelated to log appends, attempt 3's cheap check ended red on test_a_stand_in_contacts_nothing, and no later command output in the change shows those failures resolved or the five migrated suites run green, although the Definition of Done requires green targeted checks and plan step 6 requires recording commands and outcomes in this plan. | mimo-v2.6-flash | fixed — orchestrator hand edit c7215701 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-10 | MINOR | MAINT | base | plans/changes/flaky-swarm-leak-test/decisions.md; plans/changes/flaky-swarm-leak-test/research.md | decisions.md states that all 17 log appends in five test files write without a lock, while the inspected inventory in research.md and spec.md records 15 data appends of which three already took the local lock, plus two lock-only probes. A maintainer reading the decision record and the spec gets two different counts of unlocked sites (17 versus 12), and neither text marks the decision's figure as pre-inspection. | mimo-v2.6-flash | fixed — orchestrator hand edit c7215701 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-11 | MINOR | MAINT | base | tests/atomic_test_log.py::lock_path | The sidecar is named from the caller's raw path in the default branch but from path.resolve() when lock_dir is given, so two sides that reach one data file through different spellings (for example /var and its /private/var target on macOS) take different sidecars, silently stop excluding each other, and the torn read returns with the guard still green. | mimo-v2.6-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | disagree — Directory aliases such as /var and /private/var also resolve adjacent sidecars to the same inode; the mixed lock_dir problem is covered by L1-6. |
| L1-12 | MINOR | SPEC | base | plans/changes/flaky-swarm-leak-test/plan.md | Step 6 commands ten loaded runs pairing the refused-run test with the forced race on two workers and requires their outcomes in this plan; the evidence section states that loop was never run and substitutes a different workload whose background load overlapped only repetitions 1 to 19. The plan's declared gate therefore has no recorded result, yet the Verification block still presents those unrun commands as the check. | mimo-v2.6-flash | fixed — orchestrator hand edit c7215701 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-13 | MINOR | SPEC | base | plans/changes/flaky-swarm-leak-test/plan.md — "Criterion ledger" row 7 vs. "Red/green evidence — 2026-11-14" | Ledger row 7 promises "review dated red/green and ten-run loaded evidence ... in this plan and the PR", but the evidence section itself records that the ten-run loop "was not run separately" and was replaced by a 60-run loop; the ledger entry was never updated to the workload actually measured, so a maintainer reading the ledger looks for ten-run evidence that does not exist. | glm-5.3-flash | fixed — orchestrator hand edit c7215701 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-14 | MINOR | SPEC | base | plans/changes/flaky-swarm-leak-test/decisions.md — Q-1 context paragraph | The context the maintainer answered on states "17 log appends in five test files write without a lock", contradicting this change's own research addendum: of the 17 opens, two are lock-only opens that append nothing and three data appends already took the local lock, leaving 12 unlocked writes; a maintainer reading decisions.md alone is told a wrong inventory. | glm-5.3-flash | fixed — orchestrator hand edit c7215701 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-15 | MINOR | MAINT | base | tests/test_atomic_test_log.py — EXEMPT_OPERATIONS comment and find_append_bypasses | The comment promises "a moved or reworded line must be re-declared here, it is never silently carried along", but matching is by exact stripped line text per file: a moved exempted line stays exempt because the liveness check only confirms the snippet exists somewhere in the file, and one entry covers every identical line (the world.plan entry alone covers four call sites), so a new unlocked append with identical text in the same file passes the guard without review — against the spec's [DETAIL] that exemptions identify individual non-log operations. | glm-5.3-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L1-16 | MINOR | MAINT | base | tests/atomic_test_log.py — HoldLock.__init__ and read_records | read_records opens the sidecar before the missing-file check, so a destination whose parent directory does not exist raises FileNotFoundError from the sidecar open, where every old reader returned an empty snapshot via its log.exists() guard; spec criterion 4's refutation "a missing log fails" is therefore met on that edge. No migrated call site passes a missing directory today. | glm-5.3-flash | fixed — orchestrator hand edit 03418923 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L2-1 | MAJOR | SPEC | base | tests/atomic_test_log.py:34-41 (`STAND_IN_LOGS`), tests/test_atomic_test_log.py (`find_raw_log_access`) | Q-2 promises the guard "fails when a test file opens a log for appending without the shared atomic helper" so the flake "cannot return through a new test", but the guard only flags paths whose name is one of the six strings in `STAND_IN_LOGS`. A future suite that introduces a new stand-in log (e.g. `searches.jsonl`) appending concurrently is invisible to the guard and is not refused by `jsonl`-suffix or append-under-tests/ rules either, so the exact torn-read class returns through any name the helper does not already know. The narrowing is stated as a boundary in decisions.md, but it silently reduces Q-2's answered scope to "today's six names"; no criterion refutes the undeclared-new-log case. | qwen3.8-flash | fixed — orchestrator hand edit 88e28114 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L2-2 | MINOR | MAINT | base | tests/test_atomic_test_log.py `SAFE_OPERATIONS` (unlink asserted safe); tests/test_stage2_swarm.py:397-399 (`SwarmWorld.rewind`) and ~25 `(sworld.bin / "calls.jsonl").unlink()` sites | The helper docstring justifies locking the data file itself so "every spelling of one file meets one lock", but the suites still clear declared logs by plain `unlink()` while cancelled-but-running stand-ins may hold that inode's lock and append afterwards: the record lands on the detached inode (lost) or, after recreation, in the next run's fresh log while that run's readers lock the new inode — the lost/duplicated-record class criterion 2 refutes, arriving through the one operation the guard explicitly blesses. The helper offers no locked clear and no criterion or [DETAIL] names the unlink/recreate lock-identity split. | qwen3.8-flash | fixed — orchestrator hand edit 3c445876 (Opus subagent, maintainer's word of 2026-11-14) | no | disagree — Clearing intentionally discards the previous run’s records; completing an append on the removed inode correctly isolates it from the next run. |
| L2-3 | MINOR | MAINT | base | tests/test_atomic_test_log.py `_names_a_log` (`sub.value.endswith(declared)`) | The guard decides "is a declared log" by string suffix (`endswith`), while the helper decides it by exact `path.name` membership in `_declared`. They disagree for names like `old-calls.jsonl` or `mycalls.jsonl`: the helper (correctly) refuses them as undeclared, but the guard flags reads/appends of them, which is exactly what criterion 5's refuter forbids — "the guard flags ... an operation on a file that is not a declared log". The two membership tests should use one rule. | qwen3.8-flash | fixed — orchestrator hand edit 9b4e8527 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L2-4 | MINOR | MAINT | base | plans/changes/flaky-swarm-leak-test/decisions.md (Q-1 answer, Q-2 context) | Q-1's answer and Q-2's context both say "all 17 unlocked log appends", but Q-1's own context block, the research.md addendum table and spec criterion 4 establish that 17 counts every append-mode open of which only 15 append data, only 12 are unlocked, and two are lock-only opens. A maintainer taking the answered sentence literally audits the wrong number of sites; the recorded answer should match the inventory it explains ("all 17 append-mode opens" or "the 12 unlocked data appends"). | qwen3.8-flash | fixed — orchestrator hand edit 88e28114 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L2-5 | MINOR | MAINT | base | tests/test_stage2.py:805 (`test_a_stand_in_contacts_nothing`) | The change couples a shared helper to a hardcoded import allow-list in an unrelated suite: the rendered stand-in's imports must stay inside `{fcntl, json, os, sys, time, pathlib}`, so every future stdlib import added to `tests/atomic_test_log.py` (the guard design already grew it once — findings.md attempt 3 records this test failing on `hashlib` with 30 further tests red at attempt 2) turns red `test_stage2.py`, far from the helper's tests. `test_stand_ins_stay_visible_and_contact_free` already derives its check from `sys.stdlib_module_names`; this literal set should be derived from the helper module's own imports or the coupling documented. | qwen3.8-flash | fixed — orchestrator hand edit 6533fdb3 (Opus subagent, maintainer's word of 2026-11-14) | no | disagree — An explicit import allowlist is a legitimate no-contact guard; requiring its update for a future import is not a current correctness fault. |
| L2-6 | MINOR | SPEC | base | tests/test_stage2_swarm.py:286-288; scripts/stage2_research_tools.mjs:281 | The spec's Term "Test logs" lists the receipt logs among the inventoried test logs, and the stand-in's receipt append was migrated to `text_append` — but the same file `receipts.jsonl` is written concurrently by the production tool wrapper (`stage2_research_tools.mjs`), which cannot participate in the Python `flock`, and `receipts.jsonl` is deliberately not a declared log. Neither the Terms, the [DETAIL]s nor decisions.md's guard boundary state that the receipt log's protection therefore rests solely on O_APPEND single-write atomicity (small lines) rather than the helper's lock; a reader of the change cannot tell whether that mixed-writer case was weighed or dropped. | qwen3.8-flash | fixed — orchestrator hand edit 59ca9d91 (Opus subagent, maintainer's word of 2026-11-14) | no | agree |
| L3-1 | MAJOR | SPEC | base | plans/changes/flaky-swarm-leak-test/plan.md "Red/green evidence"; spec.md criterion 7 | The change demonstrates the fix only against a synthetically forced mid-append read, not the reported CI flake: the 60-run loaded loop on the actual pre-fix tree (079e0aac) passed 60 of 60, so the repeated refused-run checks carry no before/after signal that the fix addresses the real failure; criterion 7's "same workload passing after it, together with repeated refused-run checks under concurrent load" is met trivially because that workload never failed before, and the plan itself admits "The natural failure was not reproduced." | hy3 | fixed — orchestrator hand edit 2b0331fe (Opus subagent, maintainer's answer Q-4 of 2026-11-14) | no | disagree — The criterion allowed a forced torn-read reproduction alongside repeated loaded checks; it did not require reproducing the natural CI failure, which the evidence explicitly leaves unproven. |
| L3-2 | MINOR | MAINT | base | tests/test_atomic_test_log.py `_names_a_log` / `PATH_CALLS`; spec.md criterion 5 | The guard only recognizes a declared-log path as a string constant, a variable or dict key bound to one, or a path built through a fixed set of calls (Path, PurePath, str, join, joinpath, resolve, …). A raw `open`/`read_text`/`write_text` whose path is produced by any other call — for example a string method or a plain helper returning the file name — is invisible to it and passes, so a test can bypass the shared lock while `test_test_logs_use_the_shared_helper` stays green; the boundary doc calls this "obfuscation," but an ordinary function returning the name slips through the same hole. | hy3 | fixed — orchestrator hand edit 2b0331fe (Opus subagent, maintainer's answer Q-4 of 2026-11-14) | no | agree |
| L3-3 | MINOR | MAINT | base | tests/atomic_test_log.py `STAND_IN_LOGS` / `text_append`; test_stage2_swarm.py:288; spec.md Terms | `receipts.jsonl` is appended by the stand-in through the unlocked `text_append` and by the production tool, and is deliberately excluded from `STAND_IN_LOGS`, so it sits outside both the helper's lock and the guard; a test that reads it while the stand-in writes could still observe a torn line, and the spec's "non-goal" framing does not flag that one in-suite concurrent append remains on the unlocked path. | hy3 | fixed — orchestrator hand edit 2b0331fe (Opus subagent, maintainer's answer Q-4 of 2026-11-14) | no | disagree — text_append acquires an exclusive lock; the production writer’s nonparticipation does not make the stand-in append unlocked. |
| L3-4 | MINOR | MAINT | base | tests/atomic_test_log.py (top-level `import fcntl`) | The shared helper imports `fcntl` unconditionally, so every stage-2 test that imports it fails to import on any non-POSIX runner; the spec records no platform constraint, and a maintainer porting CI to Windows would hit a hard import failure across the whole suite rather than a localized skip. | hy3 | fixed — orchestrator hand edit 2b0331fe (Opus subagent, maintainer's answer Q-4 of 2026-11-14) | no | agree |
| L4-1 | MINOR | MAINT | base | tests/atomic_test_log.py:87-95 | `read_records` catches only `FileNotFoundError`; if a parent path component is a regular file, `NotADirectoryError` propagates instead of returning `[]`. The spec says "actual I/O errors propagate," so this is consistent — but a maintainer reading "missing-log-as-empty" in criterion 4 may expect all "log not accessible" cases to return empty, not just the missing-file/missing-directory cases. | qwen3.7-plus | fixed — not a test — Helper docstrings and criterion 4 clarify that only FileNotFoundError yields an empty snapshot; other I/O errors propagate. | no — not a test | disagree — Propagating NotADirectoryError follows the stated I/O-error contract; a possible contrary assumption is not a fault. |
| L4-2 | MINOR | MAINT | base | tests/atomic_test_log.py:68-77 | `text_append` performs no declaration check on the path, unlike `append_record` and `read_records`. The module docstring says "the JSON functions refuse any other name," which is accurate — but a maintainer glancing at the public API might assume all write functions enforce `STAND_IN_LOGS`, and accidentally call `text_append(declared_log, json.dumps(r)+"\n")` to bypass the JSON serialization while still being "guarded." The guard only catches raw `open`/`read_text`/etc., not `text_append` calls, so this would silently skip the declaration check. | qwen3.7-plus | fixed — not a test — text_append rejects declared log names; test_text_append_refuses_declared_logs verifies refusal without creating or altering logs. | no — not a test | disagree — The stated declaration restriction applied to JSON functions; text_append remained locked, and a hypothetical assumption about its API does not demonstrate a contract violation. |
| L4-3 | MINOR | MAINT | base | tests/test_atomic_test_log.py:89-100 | The `SPLIT_WRITER` subprocess script opens the data file without `encoding="utf-8"` (`data.open("a")`), while the helper's `text_append` uses `encoding="utf-8"`. The payload is ASCII-only and `json.dumps` escapes non-ASCII by default, so this is harmless today — but a maintainer modifying the payload to include non-ASCII characters or changing the JSON encoding settings could get silently different bytes on systems with non-UTF-8 locale defaults. | qwen3.7-plus | fixed — not a test — SPLIT_WRITER opens the data file with encoding="utf-8". | no — not a test | disagree — The exercised payload is ASCII and JSON escapes non-ASCII; the row identifies no failing current input. |

Rounds run: 4

Record digest: sha256:3958418d51e3ce57a7cd358f3c1973bc15b7af03f372583828be8c979b236e49

Record identity: sha256:f23e7281f07aeab7691d0edfafa38043d5826db7dc690d3d141af6c6f9c053d3

Cut rounds: 1, 2, 3, 4

Loop state: {"availability": {"checked_at": "2026-11-14T00:59:38+00:00", "failed": {"deepseek-v4-pro": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "glm-5.2": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "glm-5.3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "grok-4.7": "pi call failed: exit 1: opencode-go API error (403): {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "hy4-preview": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "kimi-k3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated. Use mimo-v2.6-pro instead.\"}"}, "reachable": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview", "qwen3.8-max"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "hy4": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 \"thinking.type.enabled is not supported for this model; use thinking.type.adaptive\" (a Pi adapter setting, bead coding-harness-36za evidence))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": ["the data terms of glm-5.3-flash expire on 2026-11-16 (2 days left)", "the data terms of qwen3.8-flash expire on 2026-11-16 (2 days left)", "the data terms of gpt-6-luna expire on 2026-11-16 (2 days left)", "the data terms of claude-haiku-5-5 expire on 2026-11-16 (2 days left)", "the data terms of minimax-m3 expire on 2026-11-16 (2 days left)", "the data terms of glm-5.2 expire on 2026-11-21 (7 days left)", "the data terms of glm-5.3 expire on 2026-11-21 (7 days left)", "the data terms of hy3 expire on 2026-11-21 (7 days left)", "the data terms of hy4-preview expire on 2026-11-21 (7 days left)", "the data terms of mimo-v2.5 expire on 2026-11-21 (7 days left)", "the data terms of mimo-v2.5-pro expire on 2026-11-21 (7 days left)", "the data terms of mimo-v2.6-flash expire on 2026-11-21 (7 days left)", "the data terms of qwen3.7-plus expire on 2026-11-21 (7 days left)", "the data terms of qwen3.8-max expire on 2026-11-21 (7 days left)"]}, "consumed": ["flash", "rung:qwen3.8-flash", "rung:hy3", "rung:qwen3.7-plus"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-fable-5-2", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "gemini-4-carbon", "provider": "opencode"}, {"model": "gemini-4-hydrogen", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "iceman-free", "provider": "opencode"}, {"model": "inkling-2-small-free", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "longcat-2.5-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "minimax-m3.1-flash-free", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-ember-1.0", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-14T00:56:48+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1794617808136, "etag": "W/\"23eb8dd30bc414d02f3010e266981c8f\"", "lastModified": 1794578255000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash 1017", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "LongCat 2.5 Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": ["opencode-go/gemini-4-argon: wire api \"google-generative-ai\" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base"], "overlay": ["beam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "longcat-2.5-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-11-13", "id": "longcat-2.5-free", "reason": "The maintainer took the longcat models out for good on 2026-11-13 (\"das scheint ein sehr langsames modell zu sein\"): longcat-2.0 timed out on all three online topics of that day's research swarm run; the free longcat id goes with it (bead coding-harness-363r.2)."}, {"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}, {"date": "2026-11-06", "id": "iceman-contributor-free", "reason": "New in the live Go catalog on 2026-11-06 and picked as the whole free swarm by prepare-loop; \"contributor\" ids on Go have meant that request data may be used for training, and the maintainer's decision of 2026-10-17 (question Q-12) keeps such models off. The Go page's privacy table, read 2026-11-06, confirms it: 'Iceman Contributor Free | Yes | Not ZDR'. A bridge until one central per-use-case model policy exists (bead coding-harness-k0ub with coding-harness-wq1m); maintainer, 2026-11-06, morning question Q-M9, option A."}, {"date": "2026-11-06", "id": "cat-jam-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it, so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}, {"date": "2026-11-06", "id": "longcat-2.5-preview-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it (only LongCat-2.0), so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": [], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview", "qwen3.8-max"], "rungs": ["qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "kimi-k2.7-code", "step-5-preview", "qwen3.8-max"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base.
> Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor.
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (2 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (2 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (2 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (2 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (2 days left).
> Notice: the data terms of glm-5.2 expire on 2026-11-21 (7 days left).
> Notice: the data terms of glm-5.3 expire on 2026-11-21 (7 days left).
> Notice: the data terms of hy3 expire on 2026-11-21 (7 days left).
> Notice: the data terms of hy4-preview expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.5 expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.5-pro expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.6-flash expire on 2026-11-21 (7 days left).
> Notice: the data terms of qwen3.7-plus expire on 2026-11-21 (7 days left).
> Notice: the data terms of qwen3.8-max expire on 2026-11-21 (7 days left).
> glm-5.3-flash was asked again with the format reminder: the first answer was malformed
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 2133 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From glm-5.3-flash:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> I have reviewed the diff against the worktree and the repository's own artifacts. Findings:
> 
> From glm-5.3-flash:
> glm-5.3-flash's first answer, which was not in the required format:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> Review complete. The migration itself is coherent: all 15 data appends and their readers move to one `fcntl`-locked sidecar helper, all render sites of every stand-in template replace the `@ATOMIC_LOG@` marker, the pinned-import no-contact checks were updated consistently (the hand-rolled FNV digest keeps the import set small), the guard's exemption list matches the live append-mode lines left in the tree, and the forced-race test has a deterministic handshake and an unlocked-reader red control. Two findings remain, both about the record and the evidence rather than the code:
> 
> | F-1 | MAJOR | SPEC | decisions.md Q-1 / plan.md §Red/green evidence / spec.md criterion 7 | The change promises "a reproduction under load before and after" (decision Q-1) and "repeated refused-run checks under concurrent load" (criterion 7); the recorded 60-repetition loop ran its background load run only alongside repetitions 1–19 of 60 (identically pre- and post-fix), the promised ten-run two-worker paired loop from the plan's own Verification section was never run, and the natural failure fired 0 times pre-fix — so the loaded pre-fix reproduction the decision promised does not exist and the repair's effect on the actual flake under sustained load is unmeasured; only the forced mid-append race demonstrates the mechanism. The plan discloses the shortfall but the criterion's wording and the decision's answer are not met as written. |
> | F-2 | MINOR | SPEC | decisions.md Q-1 vs research.md §Draft inspection addendum / spec.md [DETAIL] | Decision Q-1's premise and remedy say "17 unlocked log appends in five test files" migrated at "all 17 sites" (7+4+3+2+1), while the change's own repository inspection and the spec resolve the inventory to 15 data appends plus two lock-only opens that were deliberately left unmigrated; the decision record is never corrected, so a maintainer reading only decisions.md cannot tell that two of the counted sites were intentionally not migrated and may look for a missing migration. |
> 
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (2 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (2 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (2 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (2 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (2 days left).
> Notice: the data terms of glm-5.2 expire on 2026-11-21 (7 days left).
> Notice: the data terms of glm-5.3 expire on 2026-11-21 (7 days left).
> Notice: the data terms of hy3 expire on 2026-11-21 (7 days left).
> Notice: the data terms of hy4-preview expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.5 expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.5-pro expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.6-flash expire on 2026-11-21 (7 days left).
> Notice: the data terms of qwen3.7-plus expire on 2026-11-21 (7 days left).
> Notice: the data terms of qwen3.8-max expire on 2026-11-21 (7 days left).
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 2347 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (2 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (2 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (2 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (2 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (2 days left).
> Notice: the data terms of glm-5.2 expire on 2026-11-21 (7 days left).
> Notice: the data terms of glm-5.3 expire on 2026-11-21 (7 days left).
> Notice: the data terms of hy3 expire on 2026-11-21 (7 days left).
> Notice: the data terms of hy4-preview expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.5 expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.5-pro expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.6-flash expire on 2026-11-21 (7 days left).
> Notice: the data terms of qwen3.7-plus expire on 2026-11-21 (7 days left).
> Notice: the data terms of qwen3.8-max expire on 2026-11-21 (7 days left).
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 2461 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From hy3:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> Based on my review of the diff and the actual migrated code in the worktree, here are my findings.
> 
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (2 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (2 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (2 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (2 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (2 days left).
> Notice: the data terms of glm-5.2 expire on 2026-11-21 (7 days left).
> Notice: the data terms of glm-5.3 expire on 2026-11-21 (7 days left).
> Notice: the data terms of hy3 expire on 2026-11-21 (7 days left).
> Notice: the data terms of hy4-preview expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.5 expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.5-pro expire on 2026-11-21 (7 days left).
> Notice: the data terms of mimo-v2.6-flash expire on 2026-11-21 (7 days left).
> Notice: the data terms of qwen3.7-plus expire on 2026-11-21 (7 days left).
> Notice: the data terms of qwen3.8-max expire on 2026-11-21 (7 days left).
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 2510 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From qwen3.7-plus:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> After thorough examination of the change, I need to assess it across the three review categories: what it promises vs delivers, what it does unsolicited, and what would trip a maintainer.
> **Summary of the change:**
> - Creates `tests/atomic_test_log.py` — a shared helper using `fcntl.flock` on the data file itself for atomic test-log reads/writes
> - Creates `tests/test_atomic_test_log.py` — tests including a static-analysis guard that detects raw (unlocked) access to declared stand-in logs
> - Migrates 5 test files (15 data appends + corresponding readers) to use the shared helper
> - Adds planning documents (spec, plan, decisions, research, findings)
> **Key areas examined:**
> 1. **Concurrency correctness of `read_records`/`text_append`**: File is opened → lock acquired → operation → flush → unlock → close. The lock-release in `finally` inside the `with` block is correct — data is flushed before unlock, and the file close after unlock cannot corrupt the snapshot.
> 2. **Guard static analysis**: Tracks variables bound to log paths through `PATH_CALLS`, environment keys through dict assignments, embedded Python strings, and `STAND_IN_LOGS` attribute access. Limitations (f-strings, runtime-constructed paths, raw OS calls) are explicitly documented in the spec boundary.
> 3. **Error handling**: `read_records` catches `FileNotFoundError` for missing logs (returns `[]`). `NotADirectoryError` (parent component is a file) propagates — consistent with spec's "actual I/O errors propagate" principle.
> 4. **Declaration checking**: `append_record` and `read_records` enforce `STAND_IN_LOGS`; `text_append` deliberately does not (serves scenario text appends to arbitrary files). Documented in the module docstring ("the JSON functions refuse any other name").
> 5. **Embedded source**: Helper source is embedded verbatim at `@ATOMIC_LOG@` in stand-in templates. `test_stand_ins_stay_visible_and_contact_free` verifies ≥7 templates and stdlib-only imports.
> 6. **Clear-by-removal semantics**: Lock is on the data file's own inode. Unlinking creates a new inode for the next run; late writers on the old inode don't affect the new file. Tested by `test_a_cleared_log_starts_fresh_under_a_late_writer`.
> 7. **All 15 data appends migrated**: Verified through grep that all five test files use `read_records`/`append_record`/`text_append` from the helper. The guard test `test_test_logs_use_the_shared_helper` scans the entire `tests/` directory.

<!-- End of released loop record -->

Stage-2 call, 2026-11-14: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1065 files, 4227 commits, 12 rules.
