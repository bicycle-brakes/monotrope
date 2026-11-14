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
