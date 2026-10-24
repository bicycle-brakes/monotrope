---
title: "Findings — restore-symlink-parent"
category: findings
status: draft
implementation_status: partial
date: 2026-10-23
created: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-10w
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — restore-symlink-parent

Stage-2 call, 2026-10-23: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 533 files, 1915 commits, 12 rules.

Stage-2 call, 2026-10-23: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 536 files, 1916 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/restore-symlink-parent/plan.md` +7 -7
> - `scripts/stage2.py` +137 -26
> - `tests/test_stage2.py` +307 -17
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 185 lines of this gate left out …]
>     
>         monkeypatch.setattr(stage2, "run_work_model", model)
>         _no_checkpoint(monkeypatch)
>         world.script(claude=[{"stderr": "boom", "exit": 1, "plant": {"src/half.py": "x = 1\n"}}])
> >       assert world.run("implement") == 2
> E       AssertionError: assert 1 == 2
> E        +  where 1 = run('implement')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1142/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1142/popen-gw7/test_restore_baseline_refuses_1/state')).run
>
> tests/test_stage2.py:8171: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 23 files, 3 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> boom
> failed: claude call failed: exit 1 (boom); the attempt is saved at refs/stage2/attempts/demo/implement-attempt-1-20261023T173338920538Z (f4e9b535b1ca); `git diff ed00e78df857 refs/stage2/attempts/demo/implement-attempt-1-20261023T173338920538Z` shows it; the runner restored the worktree to ed00e78df857 (undone: src/half.py); rerun the verb or add --stage2-off.
> ____________ test_runner_early_refusal_recovers_self_linked_parent _____________
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/restore-symlink-parent/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1142/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1142/popen-gw4/test_runner_early_refusal_reco0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x1073bc620>
>
>     def test_runner_early_refusal_recovers_self_linked_parent(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
>         """F-3: Python 3.12 resolve raises RuntimeError on a loop; detach it and preserve the refusal."""
>         FakeClock(monkeypatch, UTC_START)
>         world.script(claude=[{"stdout": "done"}])
>         real_model = stage2.run_work_model
>         refusal = stage2.Refused("original post-call refusal")
>     
>         def model(*args, **kwargs):
>             answer = real_model(*args, **kwargs)
>             shutil.rmtree(world.plan.parent)
>             world.plan.parent.symlink_to(world.plan.parent.name, target_is_directory=True)
>             return answer
>     
>         def scan(*_args, **_kwargs):
>             raise refusal
>     
>         monkeypatch.setattr(stage2, "run_work_model", model)
>         monkeypatch.setattr(stage2, "remove_changed_credential", scan)
>         _no_checkpoint(monkeypatch)
>         with pytest.raises((stage2.Refused, RuntimeError, stage2.CallFailed)) as caught:
>             stage2.implement(world.root, "demo")
> >       assert caught.value is refusal
> E       AssertionError: assert RestorationRefused('restoration of plans/changes/demo/plan.md is refused: its parent plans/changes/demo cannot be resolved') is Refused('original post-call refusal')
> E        +  where RestorationRefused('restoration of plans/changes/demo/plan.md is refused: its parent plans/changes/demo cannot be resolved') = <ExceptionInfo RestorationRefused('restoration of plans/changes/demo/plan.md is refused: its parent plans/changes/demo cannot be resolved') tblen=5>.value
>
> tests/test_stage2.py:8997: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 22 files, 2 commits, 1 rules, 1 prompt texts
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_restore_work_input_refuses_external_parent_without_writes[nested]
> FAILED tests/test_stage2.py::test_restore_parent_resolution_failure_stops_without_writes
> FAILED tests/test_stage2.py::test_restore_baseline_refuses_external_parents_before_mutation[run]
> FAILED tests/test_stage2.py::test_runner_early_refusal_recovers_self_linked_parent
> 4 failed, 2476 passed, 16 skipped in 179.93s (0:02:59)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> scripts/stage2.py:4896:16: B023 Function definition does not bind loop variable `kept`
>      |
> 4894 |         def put_findings_back() -> None:
> 4895 |             """Put findings.md back, refusing first when its parent would carry the write outside."""
> 4896 |             if kept is not None:
>      |                ^^^^ B023
> 4897 |                 refuse_unsafe_recovery(root, ctx.findings)
> 4898 |                 restore_findings(kept)
>      |
>
> scripts/stage2.py:4898:34: B023 Function definition does not bind loop variable `kept`
>      |
> 4896 |             if kept is not None:
> 4897 |                 refuse_unsafe_recovery(root, ctx.findings)
> 4898 |                 restore_findings(kept)
>      |                                  ^^^^ B023
> 4899 |
> 4900 |         unmeasured: str | None = None
>      |
>
> tests/test_stage2.py:8087:52: ARG001 Unused function argument: `tmp_path`
>      |
> 8086 | def test_restore_parent_resolution_failure_stops_without_writes(
> 8087 |     world: World, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
>      |                                                    ^^^^^^^^ ARG001
> 8088 | ) -> None:
> 8089 |     """Criterion 4. Planted fault: a loop or resolution error permits mutation, fallback or an unnamed traceback."""
>      |
>
> Found 3 errors.
> ── [ruff-check] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 13199 earlier lines left out …]
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

Stage-2 call, 2026-10-23: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 536 files, 1916 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/restore-symlink-parent/plan.md` +7 -7
> - `scripts/stage2.py` +21 -6
> - `tests/test_stage2.py` +19 -14
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 28 lines of this gate left out …]
> ........................................................................ [ 75%]
> ........................................................................ [ 77%]
> ........................................................................ [ 80%]
> ........................................................................ [ 83%]
> ........................................................................ [ 86%]
> ........................................................................ [ 89%]
> ........................................................................ [ 92%]
> ........................................................................ [ 95%]
> ........................................................................ [ 98%]
> ................................................                         [100%]
> =================================== FAILURES ===================================
> _________ test_restore_parent_resolution_failure_stops_without_writes __________
> [gw6] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/restore-symlink-parent/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1145/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1145/popen-gw6/test_restore_parent_resolution0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x108e5caa0>
> capsys = <_pytest.capture.CaptureFixture object at 0x108c1dfd0>
>
>     def test_restore_parent_resolution_failure_stops_without_writes(
>         world: World, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
>     ) -> None:
>         """Criterion 4. Planted fault: a loop or resolution error permits mutation, fallback or an unnamed traceback."""
>         demo = world.root / "plans" / "changes" / "demo"
>         # A loop inside the change folder: resolving `demo/a` walks `a -> b -> a` and must refuse, named.
>         (demo / "a").symlink_to("b")
>         (demo / "b").symlink_to("a")
>         with pytest.raises(stage2.RestorationRefused) as expected:
>             stage2.restore_work_input(world.root, demo / "a" / "input.md", b"trusted bytes\n")
>         message = str(expected.value)
>         assert "plans/changes/demo/a/input.md" in message and "cannot be resolved" in message
>         assert isinstance(expected.value, stage2.Refused)
>         assert (demo / "a").is_symlink() and (demo / "b").is_symlink()
>         assert not (demo / "a").exists()
>     
>         # The same stop at run level: a self-linked `plans` makes every input's parent chain
>         # unresolvable, and the run ends as the named refusal without a write or a checkpoint.
>         head = git(world.root, "rev-parse", "HEAD")
>         real_model = stage2.run_work_model
>     
>         def model(*args, **kwargs):
>             answer = real_model(*args, **kwargs)
>             shutil.rmtree(world.root / "plans")
>             (world.root / "plans").symlink_to("plans", target_is_directory=True)
>             return answer
>     
>         monkeypatch.setattr(stage2, "run_work_model", model)
>         _no_checkpoint(monkeypatch)
>         world.script(claude=[{"stdout": "done", "plant": {"src/app.py": "value = 2\n"}}], make=[{"stdout": "green\n"}])
>         assert world.run("implement") == 2
>         err = capsys.readouterr().err
> >       assert "refused:" in err and "plans/changes/demo" in err and "cannot be resolved" in err
> E       assert ('refused:' in "refused: the worktree has pre-existing changes outside this change's findings.md: plans/changes/demo/a, plans/changes/demo/b\n" and 'plans/changes/demo' in "refused: the worktree has pre-existing changes outside this change's findings.md: plans/changes/demo/a, plans/changes/demo/b\n" and 'cannot be resolved' in "refused: the worktree has pre-existing changes outside this change's findings.md: plans/changes/demo/a, plans/changes/demo/b\n")
>
> tests/test_stage2.py:8116: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_restore_parent_resolution_failure_stops_without_writes
> 1 failed, 2479 passed, 16 skipped in 177.68s (0:02:57)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [ruff-check] $ lauf_cmd
> scripts/stage2.py:4704:26: PTH115 `os.readlink()` should be replaced by `Path.readlink()`
>      |
> 4702 |             seen.add(probe)
> 4703 |             try:
> 4704 |                 target = os.readlink(probe)
>      |                          ^^^^^^^^^^^ PTH115
> 4705 |             except OSError:
> 4706 |                 return f"{parent.relative_to(root).as_posix()} cannot be resolved"
>      |
>
> scripts/stage2.py:4707:53: PTH117 `os.path.isabs()` should be replaced by `Path.is_absolute()`
>      |
> 4705 |             except OSError:
> 4706 |                 return f"{parent.relative_to(root).as_posix()} cannot be resolved"
> 4707 |             probe = Path(os.path.normpath(target if os.path.isabs(target) else probe.parent / target))
>      |                                                     ^^^^^^^^^^^^^ PTH117
> 4708 |         try:
> 4709 |             resolved = probe.resolve()
>      |
>
> tests/test_stage2.py:9004:12: PTH115 `os.readlink()` should be replaced by `Path.readlink()`
>      |
> 9002 |     assert caught.value.__context__ is refusal, "the original refusal was dropped silently"
> 9003 |     assert world.plan.parent.is_symlink()
> 9004 |     assert os.readlink(world.plan.parent) == world.plan.parent.name
>      |            ^^^^^^^^^^^ PTH115
> 9005 |     assert git(world.root, "for-each-ref", "--format=%(refname)", "refs/stage2/attempts/demo/") == ""
> 9006 |     assert len(world.calls("claude")) == 1
>      |
>
> Found 3 errors.
> ── [ruff-check] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 13255 earlier lines left out …]
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

Stage-2 call, 2026-10-23: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 536 files, 1916 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +2 -2
> - `tests/test_stage2.py` +3 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [criterion-ledger] $ lauf_cmd
> plans/changes/restore-symlink-parent/plan.md:82: criterion 1: "test_restore_work_input_refuses_external_parent_without_writes" exists — remove `not yet written` from the entry
> plans/changes/restore-symlink-parent/plan.md:83: criterion 1: "test_runner_restore_preflights_all_destinations" exists — remove `not yet written` from the entry
> plans/changes/restore-symlink-parent/plan.md:84: criterion 1: "test_restore_baseline_refuses_external_parents_before_mutation" exists — remove `not yet written` from the entry
> plans/changes/restore-symlink-parent/plan.md:85: criterion 2: "test_runner_parent_escape_stops_without_fallback" exists — remove `not yet written` from the entry
> plans/changes/restore-symlink-parent/plan.md:86: criterion 3: "test_runner_parent_escape_stops_without_fallback" exists — remove `not yet written` from the entry
> plans/changes/restore-symlink-parent/plan.md:87: criterion 4: "test_restore_parent_resolution_failure_stops_without_writes" exists — remove `not yet written` from the entry
> plans/changes/restore-symlink-parent/plan.md:88: criterion 5: "test_runner_restore_refusal_bypasses_finalization" exists — remove `not yet written` from the entry
> ── [criterion-ledger] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 13315 earlier lines left out …]
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

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1917 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +7 -1
> - `tests/test_stage2.py` +40 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-1: tests/test_stage2.py::test_restore_parent_symlink_inspection_error_is_refused: the call of `tests/test_stage2.py::test_restore_parent_symlink_inspection_error_is_refused[False]` failed with OSError, not an AssertionError
> ```

Stage-2 call, 2026-10-23: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1917 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 536 files, 1918 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 536 files, 1918 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 536 files, 1918 commits, 12 rules.

Stage-2 call, 2026-10-23: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 536 files, 1918 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +45 -9
> - `tests/test_stage2.py` +246 -2
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L2-3: tests/test_stage2.py::test_baseline_cleanup_preflights_created_ignored_destination: the call of `tests/test_stage2.py::test_baseline_cleanup_preflights_created_ignored_destination[contained-chain]` failed with RestorationRefused, not an AssertionError
> - L2-6: tests/test_stage2.py::test_credential_scan_refuses_escaped_changed_parent: the call of `tests/test_stage2.py::test_credential_scan_refuses_escaped_changed_parent[scan]` failed with Failed, not an AssertionError
> ```

Stage-2 call, 2026-10-23: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 536 files, 1918 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 536 files, 1919 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 536 files, 1919 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 536 files, 1919 commits, 12 rules.

Stage-2 call, 2026-10-23: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 536 files, 1919 commits, 12 rules.

Stage-2 call, 2026-10-24: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 546 files, 1962 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model hy3 · leak check clean over 546 files, 1964 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model hy3 · leak check clean over 546 files, 1964 commits, 12 rules.

Stage-2 call, 2026-10-24: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 546 files, 1965 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 546 files, 1966 commits, 12 rules.

Stage-2 call, 2026-10-24: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 546 files, 1969 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/restore-symlink-parent/plan.md` +2 -2
> - `scripts/stage2.py` +21 -24
> - `tests/test_stage2.py` +122 -40
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L6-1: tests/test_stage2.py::test_work_verbs_skip_escaped_scan_parent: the call of `tests/test_stage2.py::test_work_verbs_skip_escaped_scan_parent[checkpoint-True]` failed with RestorationRefused, not an AssertionError
> - L6-2: tests/test_stage2.py::test_credential_scan_skips_escaped_changed_parent: the call of `tests/test_stage2.py::test_credential_scan_skips_escaped_changed_parent[scan]` failed with RestorationRefused, not an AssertionError
> ```

Stage-2 call, 2026-10-24: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 546 files, 1970 commits, 12 rules.

Stage-2 call, 2026-10-24: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 546 files, 1973 commits, 12 rules.

Stage-2 call, 2026-10-24: review-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 546 files, 1974 commits, 12 rules.

Stage-2 call, 2026-10-24: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 546 files, 1974 commits, 12 rules.
