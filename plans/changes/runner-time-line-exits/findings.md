---
title: "Findings — runner-time-line-exits"
category: findings
status: draft
implementation_status: none
date: 2026-10-23
created: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-9wp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — runner-time-line-exits

Stage-2 call, 2026-10-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 527 files, 1884 commits, 12 rules.

Stage-2 call, 2026-10-23: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 530 files, 1885 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/runner-time-line-exits/plan.md` +10 -10
> - `scripts/stage2.py` +285 -204
> - `tests/test_stage2.py` +283 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`; ruff check left findings without a safe fix or a file that does not parse; ruff format exited 2.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 199 lines of this gate left out …]
>             assert record.get("training") == "Not used", f"{model} permits training or leaves it unread"
>             assert record.get("aufbewahrung"), f"{model} leaves retention unread"
>             admitted.append(model)
>         assert set(admitted) | set(skipped) == set(modelle)
>     
>         import sys
>     
>         sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
> >       import stage2
> E         File "/Users/mikypiky/coding-harness/.claude/worktrees/runner-time-line-exits/scripts/stage2.py", line 5028
> E           raise CallFailed(closing)
> E       SyntaxError: expected 'except' or 'finally' block
>
> tests/test_model_endpoints.py:447: SyntaxError
> __ test_the_gate_command_may_run_the_live_test_in_other_ways[the-whole-suite] __
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/runner-time-line-exits/.venv/bin/python3
>
> command = 'RULESET_ASSERT=1 python3 -m pytest tests -q -x'
>
>     @pytest.mark.parametrize(
>         "command",
>         [
>             pytest.param(f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs", id="the-gate-as-it-is"),
>             pytest.param(f"{LIVE_ENV}=1 python3 -m pytest {LIVE_TEST} -q", id="the-live-test-alone"),
>             pytest.param(f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -k master", id="selected-by-name"),
>             pytest.param(f"{LIVE_ENV}=1 python3 -m pytest tests -q -x", id="the-whole-suite"),
>         ],
>     )
>     def test_the_gate_command_may_run_the_live_test_in_other_ways(command: str) -> None:
>         """The tie asks whether the live test runs, not whether the words are the usual ones."""
> >       assert _command_findings(command) == []
> E       AssertionError: assert ['command doe...ired_checks`'] == []
> E         
> E         Left contains one more item: 'command does not run `tests/test_repo_settings.py::test_master_has_a_ruleset_with_required_checks`'
> E         Use -v to get more diff
>
> tests/test_repo_settings.py:1063: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_model_endpoints.py::test_free_selection_exceptions_require_dates_and_reasons
> FAILED tests/test_model_endpoints.py::test_every_new_paid_model_carries_its_terms_reading
> FAILED tests/test_repo_settings.py::test_the_gate_command_may_run_the_live_test_in_other_ways[the-whole-suite]
> ERROR tests/test_pi_contract.py
> ERROR tests/test_stage2.py
> ERROR tests/test_stage2_availability.py
> ERROR tests/test_stage2_runs.py
> ERROR tests/test_stage2_session.py
> 3 failed, 1488 passed, 16 skipped, 5 errors in 33.71s
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> scripts/stage2.py:5028:5: SyntaxError: Expected `except` or `finally` after `try` block
>      |
> 5026 |                     )
> 5027 |                 raise
> 5028 |     raise CallFailed(closing)
>      |     ^
>      |
>
> tests/test_stage2.py:8467:24: ARG001 Unused function argument: `root`
>      |
> 8465 |         return answer
> 8466 |
> 8467 |     def broken_restore(root, path, content):
>      |                        ^^^^ ARG001
> 8468 |         raise OSError("the worktree is full")
>      |
>
> tests/test_stage2.py:8467:30: ARG001 Unused function argument: `path`
>      |
> 8465 |         return answer
> 8466 |
> 8467 |     def broken_restore(root, path, content):
>      |                              ^^^^ ARG001
> 8468 |         raise OSError("the worktree is full")
>      |
>
> tests/test_stage2.py:8467:36: ARG001 Unused function argument: `content`
>      |
> 8465 |         return answer
> 8466 |
> 8467 |     def broken_restore(root, path, content):
>      |                                    ^^^^^^^ ARG001
> 8468 |         raise OSError("the worktree is full")
>      |
>
> Found 4 errors.
> ── [ruff-check] RED (block) — der Lauf ist rot.
> ── [ruff-format] $ lauf_cmd
> 69 files already formatted
> ── [ruff-format] RED (block) — der Lauf ist rot.
> ── [ruleset] $ lauf_cmd
> ........................................................................ [ 80%]
> ..........F.......                                                       [100%]
> =================================== FAILURES ===================================
> __ test_the_gate_command_may_run_the_live_test_in_other_ways[the-whole-suite] __
>
> command = 'RULESET_ASSERT=1 python3 -m pytest tests -q -x'
>
>     @pytest.mark.parametrize(
>         "command",
>         [
>             pytest.param(f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -rs", id="the-gate-as-it-is"),
>             pytest.param(f"{LIVE_ENV}=1 python3 -m pytest {LIVE_TEST} -q", id="the-live-test-alone"),
>             pytest.param(f"{LIVE_ENV}=1 python3 -m pytest tests/test_repo_settings.py -q -k master", id="selected-by-name"),
>             pytest.param(f"{LIVE_ENV}=1 python3 -m pytest tests -q -x", id="the-whole-suite"),
>         ],
>     )
>     def test_the_gate_command_may_run_the_live_test_in_other_ways(command: str) -> None:
>         """The tie asks whether the live test runs, not whether the words are the usual ones."""
> >       assert _command_findings(command) == []
> E       AssertionError: assert ['command doe...ired_checks`'] == []
> E         
> E         Left contains one more item: 'command does not run `tests/test_repo_settings.py::test_master_has_a_ruleset_with_required_checks`'
> E         Use -v to get more diff
>
> tests/test_repo_settings.py:1063: AssertionError
> 1 failed, 89 passed in 6.57s
> ── [ruleset] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12931 earlier lines left out …]
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

Stage-2 call, 2026-10-23: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 530 files, 1885 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/runner-time-line-exits/plan.md` +10 -10
> - `scripts/stage2.py` +197 -198
> - `tests/test_stage2.py` +1 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 215 lines of this gate left out …]
>         monkeypatch.setattr(stage2, "restore_work_input", broken_restore)
>         _no_checkpoint(monkeypatch)
>         assert world.run("implement") == 1
>         err = capsys.readouterr().err
> >       assert "could not write the attempt's time entry" in err
> E       assert "could not write the attempt's time entry" in 'failed: claude call failed: the answer is empty; the attempt is saved at refs/stage2/attempts/demo/implement-attempt-...b8b5 refs/stage2/attempts/demo/implement-attempt-1-20261023T100041237485Z` shows it; the worktree needed no restore.\n'
>
> tests/test_stage2.py:8475: AssertionError
> ___________ test_runner_does_not_log_uncompleted_calls[empty-answer] ___________
> [gw6] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/runner-time-line-exits/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1040/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1040/popen-gw6/test_runner_does_not_log_uncom1/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10ace97f0>
> kind = 'empty-answer'
>
>     @pytest.mark.parametrize("kind", ["failed-process", "empty-answer", "preflight"])
>     def test_runner_does_not_log_uncompleted_calls(world: World, monkeypatch: pytest.MonkeyPatch, kind: str) -> None:
>         """Criterion 6. Planted fault: an invocation that never completes acquires a completed-attempt entry."""
>         FakeClock(monkeypatch, UTC_START)
>         baseline = git(world.root, "rev-parse", "HEAD")
>         if kind == "empty-answer":
>             seed_tests(world)
>             world.write_record([("L1-1", "taken — test_a", "no")])
>             world.script(codex=[codex_ok("TR1", "")], make=[{"stdout": "green\n"}])
>             verb = "repair"
>         elif kind == "preflight":
>             world.plan.unlink()
>             verb = "implement"
>         else:
>             world.script(claude=[{"stdout": "boom", "exit": 1}])
>             verb = "implement"
>         _no_checkpoint(monkeypatch)
>         assert world.run(verb) != 0
>         if kind == "preflight":
>             assert not world.plan.exists()
>         else:
>             assert runner_entries(world.plan) == []
>         assert len(repair_calls(world)) == (0 if kind == "preflight" else 1)
> >       assert git(world.root, "rev-list", "--count", f"{baseline}..HEAD") == "0"
> E       AssertionError: assert '1' == '0'
> E         
> E         - 0
> E         + 1
>
> tests/test_stage2.py:8506: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 23 files, 3 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> failed: codex: the answer is empty; the attempt is saved at refs/stage2/attempts/demo/repair-attempt-1-20261023T100043163528Z (af01e09cd4a7); `git diff ee457d6743ca refs/stage2/attempts/demo/repair-attempt-1-20261023T100043163528Z` shows it; the worktree needed no restore.
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_runner_early_refusal_recovers_time_destination_safely[deleted]
> FAILED tests/test_stage2.py::test_runner_early_refusal_recovers_time_destination_safely[alias]
> FAILED tests/test_stage2.py::test_runner_early_refusal_recovers_time_destination_safely[parent-alias]
> FAILED tests/test_stage2.py::test_runner_time_write_failure_keeps_original_cause
> FAILED tests/test_stage2.py::test_runner_does_not_log_uncompleted_calls[empty-answer]
> 5 failed, 2449 passed, 16 skipped in 182.49s (0:03:02)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 12987 earlier lines left out …]
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

Stage-2 call, 2026-10-23: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 530 files, 1885 commits, 12 rules.
