---
title: "Findings — verify-tmp-cleanup"
category: findings
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-11
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-tmp-cleanup

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1008 files, 3890 commits, 12 rules.

## Draft evidence — 2026-11-10

Drafted `spec.md` and `plan.md` against checkout `f035b46a`; implementation
has not started. The class remains bounded, so neither a design document nor
an ADR draft is due. No phase-2a review rows were present to resolve.

Checks run with the checkout's `.venv/bin/python3` and
`PYTHONDONTWRITEBYTECODE=1`, all exiting 0:

- `scripts/check_interview_minimums.py --change verify-tmp-cleanup`: green
  on the existing reasoned skip; no maintainer answer was added.
- `scripts/check_criterion_ledger.py`: green, including the new plan's
  not-yet-written test entries.
- `scripts/check_research_handoff.py --change verify-tmp-cleanup`: measured,
  exempt from swarm-specific obligations because no v2 evidence exists.
- `scripts/check_frontmatter_current.py`: green.
- A read-only structure check confirmed mandatory headers, eleven numbered
  criteria with refuting cases, the opening plan card and empty time section.

`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent in
this checkout. The plan follows the phase-3 prompt and existing plan form.
The full check, index regeneration, tracker-backed registry check and commit
remain the runner's work; no full verification result is claimed here.
The remote pull-request state was not read: `gh pr view` could not connect
to the GitHub API. The external session registry was not read, as this
attempt is restricted to the worktree and repository Git directory; no
tracker write was made.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-tmp-cleanup/findings.md` +28 -0
> - `plans/changes/verify-tmp-cleanup/plan.md` +158 -0
> - `plans/changes/verify-tmp-cleanup/spec.md` +169 -0
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/verify-tmp-cleanup/findings.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> plans/changes/verify-tmp-cleanup/plan.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> plans/changes/verify-tmp-cleanup/spec.md: stale — updated 2026-11-10 is older than its last change 2026-11-11 (uncommitted)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 36921 earlier lines left out …]
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
> ````

Stage-2 call, 2026-11-11: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 1011 files, 3901 commits, 12 rules.

## Draft repair evidence — 2026-11-11

Reviewed the existing spec and plan against `research.md`, `decisions.md`
and the available templates at checkout `f035b46a`. No open phase-2a rows
were present. The class, eleven criteria, decisions and plan card remain
unchanged; no design or ADR is due for this bounded change.

Updated only the spec and plan's `updated` and `last_reviewed` fields and
this findings record. Their creation dates remain 2026-11-10. The previous
attempt's frontmatter result above predates its failed post-run check;
the fresh checks below supersede that result.

Checks rerun with `.venv/bin/python3` and `PYTHONDONTWRITEBYTECODE=1`,
all exiting 0:

- `scripts/check_interview_minimums.py --change verify-tmp-cleanup`.
- `scripts/check_criterion_ledger.py`.
- `scripts/check_research_handoff.py --change verify-tmp-cleanup`:
  explicitly exempt because this change has no research-swarm/v2 evidence.
- `scripts/check_frontmatter_current.py`: every held document is current.
- A read-only structure check: required headers, eleven refuting cases,
  the opening plan card, empty time section and no open review rows.

The unavailable template and validator noted above remain unavailable.
Full verification and the commit remain the runner's work. The existing
`plans/INDEX.md` modification was left untouched. Remote pull-request and
external session-registry state were not read under the worktree-only
restriction; no tracker write or git mutation was performed.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-11: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1011 files, 3961 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-tmp-cleanup/plan.md` +11 -11
> - `scripts/verify_all.sh` +25 -0
> - `scripts/verify_lock.py` +606 -15
> - `tests/test_ci.py` +329 -0
> - `tests/test_verify_lock.py` +368 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_ci.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> scripts/verify_lock.py:1214:13: PTH106 `os.rmdir()` should be replaced by `Path.rmdir()`
>      |
> 1212 |             finally:
> 1213 |                 os.close(nested)
> 1214 |             os.rmdir(name, dir_fd=dir_fd)
>      |             ^^^^^^^^ PTH106
> 1215 |         else:
> 1216 |             os.unlink(name, dir_fd=dir_fd)
>      |
>
> scripts/verify_lock.py:1216:13: PTH108 `os.unlink()` should be replaced by `Path.unlink()`
>      |
> 1214 |             os.rmdir(name, dir_fd=dir_fd)
> 1215 |         else:
> 1216 |             os.unlink(name, dir_fd=dir_fd)
>      |             ^^^^^^^^^ PTH108
>      |
>
> scripts/verify_lock.py:1234:5: PTH106 `os.rmdir()` should be replaced by `Path.rmdir()`
>      |
> 1232 |     finally:
> 1233 |         os.close(root_fd)
> 1234 |     os.rmdir(path)
>      |     ^^^^^^^^ PTH106
>      |
>
> tests/test_ci.py:2603:9: F841 Local variable `bash` is assigned to but never used
>      |
> 2601 |     _interpreter_wrapper(tree / ".venv" / "bin" / "python3", "venv", base / "log")
> 2602 |     with _held_holder(base / "state", pid=os.getpid()):
> 2603 |         bash = shutil.which("bash") or "/bin/bash"
>      |         ^^^^ F841
> 2604 |         done = subprocess.run(
> 2605 |             [
>      |
>      = help: Remove assignment to unused variable `bash`
>
> tests/test_verify_lock.py:1591:25: ARG001 Unused function argument: `args`
>      |
> 1589 |     monkeypatch.setenv("PYTEST_DEBUG_TEMPROOT", str(tmp_path / "spawn-root"))
> 1590 |
> 1591 |     def refusing_spawn(*args: object, **kwargs: object) -> subprocess.Popen[bytes]:
>      |                         ^^^^ ARG001
> 1592 |         raise OSError("spawn refused by the fixture")
>      |
>
> tests/test_verify_lock.py:1591:41: ARG001 Unused function argument: `kwargs`
>      |
> 1589 |     monkeypatch.setenv("PYTEST_DEBUG_TEMPROOT", str(tmp_path / "spawn-root"))
> 1590 |
> 1591 |     def refusing_spawn(*args: object, **kwargs: object) -> subprocess.Popen[bytes]:
>      |                                         ^^^^^^ ARG001
> 1592 |         raise OSError("spawn refused by the fixture")
>      |
>
> Found 6 errors.
> No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
> ```

Stage-2 call, 2026-11-12: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1011 files, 3964 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-tmp-cleanup/plan.md` +11 -11
> - `scripts/verify_lock.py` +3 -3
> - `tests/test_ci.py` +0 -1
> - `tests/test_verify_lock.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
>
> ==================================== ERRORS ====================================
> ______________________ ERROR collecting tests/test_ci.py _______________________
> In test_verify_rejects_external_basetemp_options: function uses no argument 'adddopts'
> ______________________ ERROR collecting tests/test_ci.py _______________________
> In test_verify_rejects_external_basetemp_options: function uses no argument 'adddopts'
> ______________________ ERROR collecting tests/test_ci.py _______________________
> In test_verify_rejects_external_basetemp_options: function uses no argument 'adddopts'
> ______________________ ERROR collecting tests/test_ci.py _______________________
> In test_verify_rejects_external_basetemp_options: function uses no argument 'adddopts'
> ______________________ ERROR collecting tests/test_ci.py _______________________
> In test_verify_rejects_external_basetemp_options: function uses no argument 'adddopts'
> ______________________ ERROR collecting tests/test_ci.py _______________________
> In test_verify_rejects_external_basetemp_options: function uses no argument 'adddopts'
> ______________________ ERROR collecting tests/test_ci.py _______________________
> In test_verify_rejects_external_basetemp_options: function uses no argument 'adddopts'
> ______________________ ERROR collecting tests/test_ci.py _______________________
> In test_verify_rejects_external_basetemp_options: function uses no argument 'adddopts'
> =========================== short test summary info ============================
> ERROR tests/test_ci.py - Failed: In test_verify_rejects_external_basetemp_opt...
> ERROR tests/test_ci.py - Failed: In test_verify_rejects_external_basetemp_opt...
> ERROR tests/test_ci.py - Failed: In test_verify_rejects_external_basetemp_opt...
> ERROR tests/test_ci.py - Failed: In test_verify_rejects_external_basetemp_opt...
> ERROR tests/test_ci.py - Failed: In test_verify_rejects_external_basetemp_opt...
> ERROR tests/test_ci.py - Failed: In test_verify_rejects_external_basetemp_opt...
> ERROR tests/test_ci.py - Failed: In test_verify_rejects_external_basetemp_opt...
> ERROR tests/test_ci.py - Failed: In test_verify_rejects_external_basetemp_opt...
> 8 errors in 1.09s
> ```

Stage-2 call, 2026-11-12: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1011 files, 3966 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-tmp-cleanup/plan.md` +11 -11
> - `tests/test_ci.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         root = tmp_path / "tmproot"
>         stop = tmp_path / "stop"
>         started = tmp_path / "started"
>         entry = _scoped(root, AREA_WRITER, {"PROBE_OUT": str(stop), "PROBE_STARTED": str(started)})
>         container = _container_of(root)
>         try:
> >           assert _wait_until(lambda: _areas(container)), "the entry never allocated its run area"
> E           AssertionError: the entry never allocated its run area
> E           assert False
> E            +  where False = _wait_until(<function test_temp_scope_signals_clean_after_process_group.<locals>.<lambda> at 0x10abc3060>)
>
> tests/test_verify_lock.py:1375: AssertionError
> _____________ test_temp_scope_signals_clean_after_process_group[2] _____________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-tmp-cleanup/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-43/popen-gw0/test_temp_scope_signals_clean_0')
> signum = <Signals.SIGINT: 2>
>
>     @pytest.mark.parametrize("signum", [signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT])
>     def test_temp_scope_signals_clean_after_process_group(tmp_path: Path, signum: int) -> None:
>         """Ledger criterion 4: a trapped signal ends the group first, then removes the area, keeping 128+signal.
>     
>         Fault this pins: a signal removing the area while the supervised group can
>         still write (the survivor re-creates its payload after the removal), a
>         payload left behind, or the existing 128-plus-signal status lost.
>         """
>         root = tmp_path / "tmproot"
>         stop = tmp_path / "stop"
>         started = tmp_path / "started"
>         entry = _scoped(root, AREA_WRITER, {"PROBE_OUT": str(stop), "PROBE_STARTED": str(started)})
>         container = _container_of(root)
>         try:
> >           assert _wait_until(lambda: _areas(container)), "the entry never allocated its run area"
> E           AssertionError: the entry never allocated its run area
> E           assert False
> E            +  where False = _wait_until(<function test_temp_scope_signals_clean_after_process_group.<locals>.<lambda> at 0x10935f1a0>)
>
> tests/test_verify_lock.py:1375: AssertionError
> _____________ test_temp_scope_signals_clean_after_process_group[1] _____________
> [gw7] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-tmp-cleanup/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-43/popen-gw7/test_temp_scope_signals_clean_0')
> signum = <Signals.SIGHUP: 1>
>
>     @pytest.mark.parametrize("signum", [signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT])
>     def test_temp_scope_signals_clean_after_process_group(tmp_path: Path, signum: int) -> None:
>         """Ledger criterion 4: a trapped signal ends the group first, then removes the area, keeping 128+signal.
>     
>         Fault this pins: a signal removing the area while the supervised group can
>         still write (the survivor re-creates its payload after the removal), a
>         payload left behind, or the existing 128-plus-signal status lost.
>         """
>         root = tmp_path / "tmproot"
>         stop = tmp_path / "stop"
>         started = tmp_path / "started"
>         entry = _scoped(root, AREA_WRITER, {"PROBE_OUT": str(stop), "PROBE_STARTED": str(started)})
>         container = _container_of(root)
>         try:
> >           assert _wait_until(lambda: _areas(container)), "the entry never allocated its run area"
> E           AssertionError: the entry never allocated its run area
> E           assert False
> E            +  where False = _wait_until(<function test_temp_scope_signals_clean_after_process_group.<locals>.<lambda> at 0x10752d4e0>)
>
> tests/test_verify_lock.py:1375: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_verify_lock.py::test_temp_scope_cleanup_preserves_unrelated_paths
> FAILED tests/test_verify_lock.py::test_failed_temp_scope_retention_is_explicit_and_reported
> FAILED tests/test_verify_lock.py::test_successful_temp_scope_never_retains - ...
> FAILED tests/test_ci.py::test_verify_runs_have_distinct_nested_temp_areas - A...
> FAILED tests/test_ci.py::test_verify_keeps_unrelated_and_refuses_malformed_addopts
> FAILED tests/test_ci.py::test_verify_pytest_sessions_and_workers_use_run_area
> FAILED tests/test_ci.py::test_temp_scope_preserves_runner_entry_contracts - A...
> FAILED tests/test_ci.py::test_verify_temp_cleanup_preserves_exit_status - Ass...
> FAILED tests/test_verify_lock.py::test_temp_scope_recovers_orphans_after_protected_work_ends
> FAILED tests/test_verify_lock.py::test_temp_scope_signals_clean_after_process_group[3]
> FAILED tests/test_verify_lock.py::test_temp_scope_storage_failures_are_visible_and_unsuccessful
> FAILED tests/test_verify_lock.py::test_temp_scope_signals_clean_after_process_group[15]
> FAILED tests/test_verify_lock.py::test_temp_scope_signals_clean_after_process_group[2]
> FAILED tests/test_verify_lock.py::test_temp_scope_signals_clean_after_process_group[1]
> 14 failed, 7 passed in 21.15s
> ```
