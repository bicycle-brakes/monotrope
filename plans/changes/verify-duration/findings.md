---
title: "Findings — verify-duration"
category: findings
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-1um6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-duration

Stage-2 call, 2026-11-04: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 883 files, 3245 commits, 12 rules.

Stage-2 call, 2026-11-04: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 886 files, 3246 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-duration/plan.md` +11 -11
> - `scripts/kit/manifest.yaml` +6 -0
> - `scripts/verify_all.sh` +71 -2
> - `scripts/verify_duration.py` +449 -0
> - `scripts/verify_lock.py` +129 -2
> - `tests/test_ci.py` +235 -5
> - `tests/test_verify_duration.py` +458 -0
> - `tests/test_verify_lock.py` +115 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `scripts/verify_duration.py`, `scripts/verify_lock.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> 213 |         "utc": _utc_now(),
> 214 |         "repository": os.getcwd(),
>     |                       ^^^^^^^^^ PTH109
> 215 |         "commit": _git(["rev-parse", "HEAD"]),
> 216 |         # None means git could not answer; only an answer decides yes or no.
>     |
>
> scripts/verify_duration.py:336:39: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>     |
> 334 | def _fmt_seconds(value: object, unknown: str = "unknown") -> str:
> 335 |     """A duration for the console; a row without a number shows its unknown, never a crash."""
> 336 |     if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
>     |                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 337 |         return unknown
> 338 |     return f"{value:.3f}s"
>     |
>     = help: Convert to `X | Y`
>
> scripts/verify_lock.py:456:39: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>     |
> 454 | def _finite_wait(value: object) -> float | None:
> 455 |     """A published or inherited wait as a finite non-negative float, else None."""
> 456 |     if isinstance(value, bool) or not isinstance(value, (int, float)):
>     |                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 457 |         return None
> 458 |     return float(value) if math.isfinite(value) and value >= 0 else None
>     |
>     = help: Convert to `X | Y`
>
> tests/test_ci.py:2155:16: UP038 Use `X | Y` in `isinstance` call instead of `(X, Y)`
>      |
> 2153 |     assert gate_rows["beta"]["exit"] == 1 and gate_rows["beta"]["enforcement"] == "advisory", gate_rows["beta"]
> 2154 |     assert gate_rows["gamma"]["exit"] == 1
> 2155 |     assert all(isinstance(row["seconds"], (int, float)) and row["seconds"] >= 0 for row in gate_rows.values())
>      |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ UP038
> 2156 |     ends = [e for e in events if e["event"] == "run_end"]
> 2157 |     assert len(ends) == 1 and ends[0]["run_id"] == run_id and ends[0]["verdict"] == "red"
>      |
>      = help: Convert to `X | Y`
>
> tests/test_ci.py:2195:19: B007 Loop control variable `ending` not used within loop body
>      |
> 2193 |     history symlink to its victim.
> 2194 |     """
> 2195 |     for scenario, ending, verdict, banner in (
>      |                   ^^^^^^ B007
> 2196 |         ("green", "true", 0, "VERIFY GREEN"),
> 2197 |         ("red", "exit 1", 1, "VERIFY RED"),
>      |
>      = help: Rename unused `ending` to `_ending`
>
> tests/test_verify_duration.py:131:21: ARG001 Unused function argument: `monkeypatch`
>     |
> 130 | def test_history_appends_distinct_runs_and_marks_incomplete(
> 131 |     tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
>     |                     ^^^^^^^^^^^ ARG001
> 132 | ) -> None:
> 133 |     """A later run appends its own identity and an interrupted run never reads as complete.
>     |
>
> tests/test_verify_duration.py:321:21: ARG001 Unused function argument: `monkeypatch`
>     |
> 320 | def test_reader_selects_runs_and_diagnoses_truncated_history(
> 321 |     tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
>     |                     ^^^^^^^^^^^ ARG001
> 322 | ) -> None:
> 323 |     """Malformed lines are named gaps, valid records survive them, and an unfinished run stays one.
>     |
>
> tests/test_verify_duration.py:427:5: PTH108 `os.unlink()` should be replaced by `Path.unlink()`
>     |
> 426 |     # A FIFO in the file's place: refused without waiting on a writer that never comes.
> 427 |     os.unlink(root / verify_duration.HISTORY_NAME)
>     |     ^^^^^^^^^ PTH108
> 428 |     os.mkfifo(root / verify_duration.HISTORY_NAME)
> 429 |     code, _, err = _run(
>     |
>
> Found 8 errors.
> No fixes available (4 hidden fixes can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-04: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 888 files, 3246 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-duration/plan.md` +11 -11
> - `scripts/verify_duration.py` +2 -2
> - `scripts/verify_lock.py` +1 -1
> - `tests/test_ci.py` +2 -2
> - `tests/test_verify_duration.py` +3 -3
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_verify_duration.py`.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> E             }
> E             
> E             ── gates: job=verify ──────────────────────────────────────────────
> E             
> E             ── [probe] $ lauf_cmd
> E             ── [probe] gruen
> E             
> E             VERIFY GREEN — every local gate of the 'verify' job passed.
> E             
> E             [verify-lock] admitted
> E             [verify-lock] available memory 70% at or above the 0% floor; starting
> E             Traceback (most recent call last):
> E               File "<frozen runpy>", line 198, in _run_module_as_main
> E               File "<frozen runpy>", line 88, in _run_code
> E               File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-596/popen-gw0/test_duration_storage_failure_0/red/tree/scripts/verify_duration.py", line 449, in <module>
> E                 raise SystemExit(main())
> E                                  ^^^^^^
> E               File "/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-596/popen-gw0/test_duration_storage_failure_0/red/tree/scripts/verify_duration.py", line 410, in main
> E                 operations["clock"].set_defaults(handler=cmd_clock)
> E                 ~~~~~~~~~~^^^^^^^^^
> E             TypeError: '_SubParsersAction' object is not subscriptable
> E             verify-duration: measurement storage unusable — this run is not recorded; gates and verdicts continue unchanged
> E             
> E           assert 0 == 1
> E            +  where 0 = CompletedProcess(args=['/opt/homebrew/bin/bash', '/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-m...le\nverify-duration: measurement storage unusable — this run is not recorded; gates and verdicts continue unchanged\n').returncode
>
> tests/test_ci.py:2209: AssertionError
> _________ test_machine_context_preserves_unknowns_and_worker_override __________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-duration/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-596/popen-gw0/test_machine_context_preserves0')
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x106dfaab0>
> capsys = <_pytest.capture.CaptureFixture object at 0x106df81a0>
>
>     def test_machine_context_preserves_unknowns_and_worker_override(
>         tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
>     ) -> None:
>         """An unavailable reading is null, never zero, and a worker override is never guessed away.
>     
>         Fault this pins: unavailable memory becoming zero, a worker override
>         replaced by a derived count, or a missing admission context fabricated.
>         """
>         state = tmp_path / "state"
>         empty = tmp_path / "empty"
>         empty.mkdir()
>         monkeypatch.chdir(empty)
>         monkeypatch.delenv("PYTEST_XDIST_AUTO_NUM_WORKERS", raising=False)
>     
> >       code, run_id, _ = _run(capsys, "start", "--job", "verify", "--placement", "local")
>
> /Users/mikypiky/coding-harness/.claude/worktrees/verify-duration/tests/test_verify_duration.py:288: 
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
> /Users/mikypiky/coding-harness/.claude/worktrees/verify-duration/tests/test_verify_duration.py:57: in _run
>     code = verify_duration.main(list(argv))
> _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
>
> argv = ['start', '--job', 'verify', '--placement', 'local']
>
>     def main(argv: list[str] | None = None) -> int:
>         parser = argparse.ArgumentParser(description="Measured verification durations, recorded locally only.")
>         operations = parser.add_subparsers(dest="operation", required=True)
>     
>         operations.add_parser("clock", help="print one monotonic reading")
> >       operations["clock"].set_defaults(handler=cmd_clock)
> E       TypeError: '_SubParsersAction' object is not subscriptable
>
> /Users/mikypiky/coding-harness/.claude/worktrees/verify-duration/scripts/verify_duration.py:410: TypeError
> =========================== short test summary info ============================
> FAILED tests/test_verify_duration.py::test_monotonic_execution_excludes_admission_wait
> FAILED tests/test_verify_duration.py::test_reader_selects_runs_and_diagnoses_truncated_history
> FAILED tests/test_verify_duration.py::test_records_bind_results_to_revision_and_configuration
> FAILED tests/test_verify_duration.py::test_history_appends_distinct_runs_and_marks_incomplete
> FAILED tests/test_ci.py::test_timing_preserves_job_selection_enforcement_and_nested_admission
> FAILED tests/test_ci.py::test_runner_reports_each_gate_duration_and_raw_result
> FAILED tests/test_ci.py::test_runner_list_does_not_record_or_duplicate_runs
> FAILED tests/test_verify_duration.py::test_history_rejects_substituted_destinations
> FAILED tests/test_verify_lock.py::test_admission_measurement_survives_cli_and_inherited_context
> FAILED tests/test_ci.py::test_duration_storage_failure_warns_without_changing_verdict
> FAILED tests/test_verify_duration.py::test_machine_context_preserves_unknowns_and_worker_override
> 11 failed, 1 passed in 2.49s
> ```

Stage-2 call, 2026-11-04: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 888 files, 3246 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/verify_duration.py` +2 -2
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         readings = iter([10.0, 30.0])
>         monkeypatch.setattr(verify_lock, "read_available_memory", lambda _platform=None: next(readings))
>     
>         with verify_lock.hold_admission(["measured", "wait"]) as owned:
>             assert owned is not None, "an independent admission must own the lock"
>             active = verify_lock._ACTIVE
>             assert active is not None
>             assert active.wait_seconds == 60.0, "the memory recheck was not counted into the measured wait"
>             assert re.fullmatch(r"[0-9a-f]{32}", active.admission_id), active.admission_id
>             context = verify_lock.admission_context()
>             assert context == verify_lock.AdmissionContext(active.admission_id, 60.0, False)
>             holder = verify_lock.read_holder()
>             assert holder is not None
>             assert holder["admission_id"] == active.admission_id
>             assert holder["admission_wait"] == 60.0
>             # A fresh context travels to a local check as the child's own measurement.
>             env = verify_lock.inherit_env({"PATH": "/usr/bin:/bin"})
>             assert env[verify_lock.ADMISSION_ID_ENV] == active.admission_id
>             assert float(env[verify_lock.ADMISSION_WAIT_ENV]) == 60.0
>         assert verify_lock._ACTIVE is None, "the released admission stayed active"
>     
>         # An inherited admission resolves its context from the published ownership:
>         # an old-shape record (published before the field existed) reads unknowns.
>         monkeypatch.setenv(verify_lock.LOCK_ENV, str(os.getpid()))
>         monkeypatch.setenv(verify_lock.TOKEN_ENV, TEST_TOKEN)
>         with fake_holder(state, pid=os.getpid()):
>             context = verify_lock.admission_context()
>             assert context == verify_lock.AdmissionContext(None, None, True)
>             root = state / "coding-harness"
>             record = json.loads((root / verify_lock.HOLDER_NAME).read_text(encoding="utf-8"))
>             record["admission_id"] = "inherited-admission-id"
>             record["admission_wait"] = 7.5
>             (root / verify_lock.HOLDER_NAME).write_text(json.dumps(record), encoding="utf-8")
>             context = verify_lock.admission_context()
>             assert context == verify_lock.AdmissionContext("inherited-admission-id", 7.5, True)
>             # An unusable published wait stays unknown — never a guess, never zero.
>             record["admission_wait"] = "not-a-number"
>             (root / verify_lock.HOLDER_NAME).write_text(json.dumps(record), encoding="utf-8")
>             context = verify_lock.admission_context()
>             assert context == verify_lock.AdmissionContext("inherited-admission-id", None, True)
>             # An inherited context does not travel as a fresh measurement.
>             env = verify_lock.inherit_env({verify_lock.ADMISSION_ID_ENV: "should-not-travel"})
>             assert verify_lock.ADMISSION_ID_ENV not in env
>             assert verify_lock.ADMISSION_WAIT_ENV not in env
>             assert env[verify_lock.LOCK_ENV] == str(os.getpid())
>     
>         # The same fresh resolution through the supervisor's CLI: the protected
>         # command reads its context and the published record, and they agree.
>         monkeypatch.delenv(verify_lock.LOCK_ENV)
>         monkeypatch.delenv(verify_lock.TOKEN_ENV)
>         done = subprocess.run(
>             [sys.executable, "-m", "scripts.verify_lock", "--", sys.executable, "-c", CONTEXT_PROBE],
>             cwd=REPO_ROOT,
>             env=_env(state),
>             capture_output=True,
>             text=True,
>             timeout=60,
>             check=True,
>         )
>         seen = json.loads(done.stdout)
>         assert seen["reused"] is False, seen
>         assert re.fullmatch(r"[0-9a-f]{32}", seen["id"] or ""), seen
>         assert seen["wait"] is not None and seen["wait"] >= 0, seen
> >       assert seen["id"] == seen["holder_id"] and seen["wait"] == seen["holder_wait"], seen
> E       AssertionError: {'holder_id': 'ed3d28da9d314a0badc552ededfcf52d', 'holder_wait': 0.003219874983187765, 'id': 'ed3d28da9d314a0badc552ededfcf52d', 'reused': False, ...}
> E       assert ('ed3d28da9d31...552ededfcf52d' == 'ed3d28da9d31...552ededfcf52d'
> E         
> E           ed3d28da9d314a0badc552ededfcf52d and 0.00322 == 0.003219874983187765)
>
> tests/test_verify_lock.py:1277: AssertionError
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] admitted after 30s
> [verify-lock] available memory 10% below the 25% floor; rechecking every 30s
> [verify-lock] available memory 10% below the 25% floor; waiting
> [verify-lock] available memory 30% at or above the 25% floor; starting
> =========================== short test summary info ============================
> FAILED tests/test_verify_duration.py::test_monotonic_execution_excludes_admission_wait
> FAILED tests/test_ci.py::test_duration_storage_failure_warns_without_changing_verdict
> FAILED tests/test_verify_lock.py::test_admission_measurement_survives_cli_and_inherited_context
> 3 failed, 9 passed in 4.45s
> ```

Stage-2 call, 2026-11-04: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two GLM 5.3 Flash attempts failed their post-run checks on 2026-11-04 (tests red) · leak check clean over 888 files, 3247 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 888 files, 3254 commits, 12 rules.

Stage-2 call, 2026-11-04: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 888 files, 3257 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +10 -0
> - `plans/INDEX.md` +4 -4
> - `plans/changes/verify-duration/decisions.md` +1 -1
> - `plans/changes/verify-duration/plan.md` +4 -2
> - `plans/changes/verify-duration/research.md` +1 -1
> - `plans/changes/verify-duration/spec.md` +1 -1
> - `scripts/verify_duration.py` +24 -6
> - `tests/test_ci.py` +28 -5
> - `tests/test_verify_duration.py` +81 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-2: tests/test_verify_duration.py::test_reader_refuses_substituted_history: the call of `tests/test_verify_duration.py::test_reader_refuses_substituted_history[fifo]` failed with TimeoutExpired, which is neither Python's AssertionError nor pytest's own failed outcome (pytest.fail.Exception)
> - L1-4: tests/test_ci.py::test_timing_preserves_job_selection_enforcement_and_nested_admission: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - L1-8: tests/test_verify_duration.py::test_append_io_failure_is_named_refusal: the call of `tests/test_verify_duration.py::test_append_io_failure_is_named_refusal[lock]` failed with OSError, which is neither Python's AssertionError nor pytest's own failed outcome (pytest.fail.Exception)
> - L1-10: tests/test_ci.py::test_timing_preserves_job_selection_enforcement_and_nested_admission: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-duration/stage2/attempts/verify-duration/attempt-1-20261104T152956372948Z-0bc96a9d.md
> ```

Stage-2 call, 2026-11-04: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 888 files, 3269 commits, 12 rules.

Stage-2 call, 2026-11-05: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 888 files, 3293 commits, 12 rules.
