---
title: "Findings — verify-cheap-first"
category: findings
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.1
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-cheap-first

Stage-2 call, 2026-11-10: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1008 files, 3867 commits, 12 rules.

Stage-2 call, 2026-11-10: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1011 files, 3876 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-cheap-first/plan.md` +15 -15
> - `plans/changes/verify-cheap-first/spec.md` +1 -1
> - `scripts/ci_gates.py` +94 -22
> - `scripts/verify_all.sh` +31 -0
> - `tests/test_ci.py` +71 -23
> - `tests/test_verify_cheap_first.py` +737 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `tests/test_verify_cheap_first.py`.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ...s..F.....F........                                                    [100%]
> =================================== FAILURES ===================================
> _________________ test_early_stop_preserves_repair_diagnostics _________________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1839/popen-gw1/test_early_stop_preserves_repa0')
>
>     def test_early_stop_preserves_repair_diagnostics(tmp_path: Path) -> None:
>         """Criterion 8: the existing repair parser reads the early-stopped run as it read a full one.
>     
>         The failed gate's start frame, command, diagnostic and RED line survive
>         `red_sections`; the not-run summary produces no gate section of its own
>         and names no executed gate.
>         """
>         base = tmp_path / "diagnostics"
>         gates = [
>             _gate(base, "suite-minutes", "minutes"),
>             _gate(
>                 base,
>                 "quick-red",
>                 "seconds",
>                 command=(
>                     f"touch {base / 'quick-red.ran'}; echo quick-red >> {base / 'order.txt'}; "
>                     "echo 'E   cheap-diagnostic-line'; exit 1"
>                 ),
>             ),
>             _gate(base, "after-minutes", "minutes"),
>         ]
>         tree = _tree_files(base / "tree")
>         _write_gate_file(tree, gates)
>         done = _run_runner(tree)
>         assert done.returncode == 1, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
>         red = red_sections(done.stdout)
>         assert red is not None, done.stdout
> >       assert "── [quick-red] $ touch" in red, red
> E       AssertionError: ── [quick-red] $ lauf_cmd
> E         E   cheap-diagnostic-line
> E         ── [quick-red] RED (block) — der Lauf ist rot.
> E       assert '── [quick-red] $ touch' in '── [quick-red] $ lauf_cmd\nE   cheap-diagnostic-line\n── [quick-red] RED (block) — der Lauf ist rot.'
>
> tests/test_verify_cheap_first.py:623: AssertionError
> ________________ test_ci_mode_continues_after_blocking_failure _________________
> [gw5] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1839/popen-gw5/test_ci_mode_continues_after_b0')
>
>     def test_ci_mode_continues_after_blocking_failure(tmp_path: Path) -> None:
>         """Criterion 7: `--ci` stays exhaustive — a blocking failure suppresses no later selected gate.
>     
>         The same planted failure that stops a local run red lets the minutes gate
>         behind it execute in CI mode, without a not-run summary and with the red
>         verdict.
>         """
>         base = tmp_path / "ci-mode"
>         gates = [
>             _gate(base, "red-seconds", "seconds", ending="exit 1"),
>             _gate(base, "behind-minutes", "minutes"),
>         ]
>         tree = _tree_files(base / "tree")
>         _write_gate_file(tree, gates)
>         done = _run_runner(tree, "--ci")
>         assert done.returncode == 1, f"exit {done.returncode}\n{done.stdout}\n{done.stderr}"
>         assert "VERIFY RED" in done.stdout, done.stdout
>         assert "── [red-seconds] RED (block)" in done.stdout, done.stdout
> >       assert (base / "behind-minutes.ran").exists(), "--ci lost a later selected gate after a blocking failure"
> E       AssertionError: --ci lost a later selected gate after a blocking failure
> E       assert False
> E        +  where False = exists()
> E        +    where exists = (PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1839/popen-gw5/test_ci_mode_continues_after_b0/ci-mode') / 'behind-minutes.ran').exists
>
> tests/test_verify_cheap_first.py:581: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_verify_cheap_first.py::test_early_stop_preserves_repair_diagnostics
> FAILED tests/test_verify_cheap_first.py::test_ci_mode_continues_after_blocking_failure
> 2 failed, 18 passed, 1 skipped in 8.64s
> ```

Stage-2 call, 2026-11-10: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 1012 files, 3893 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-cheap-first/plan.md` +14 -14
> - `plans/changes/verify-cheap-first/spec.md` +1 -1
> - `scripts/verify_all.sh` +6 -3
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ '/Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/.venv/bin/python3' -m pytest tests/ -q -n auto
> [… 53 lines of this gate left out …]
> ........................................................................ [ 67%]
> ........................................................................ [ 69%]
> ........................................................................ [ 70%]
> ........................................................................ [ 71%]
> ........................................................................ [ 73%]
> ........................................................................ [ 74%]
> ........................................................................ [ 75%]
> ........................................................................ [ 77%]
> ........................................................................ [ 78%]
> ........................................................................ [ 79%]
> ........................................................................ [ 81%]
> ........................................................................ [ 82%]
> ........................................................................ [ 83%]
> ........................................................................ [ 85%]
> ........................................................................ [ 86%]
> ........................................................................ [ 87%]
> ........................................................................ [ 89%]
> ........................................................................ [ 90%]
> ........................................................................ [ 91%]
> ........................................................................ [ 93%]
> ........................................................................ [ 94%]
> ........................................................................ [ 95%]
> ........................................................................ [ 97%]
> ........................................................................ [ 98%]
> ........................................................................ [ 99%]
> ..................                                                       [100%]
> =================================== FAILURES ===================================
> ______ test_the_frames_red_sections_reads_are_the_ones_verify_all_prints _______
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/.venv/bin/python3
>
>     def test_the_frames_red_sections_reads_are_the_ones_verify_all_prints() -> None:
>         # runner-red-gate pre-mortem: verify_all.sh renames its frame lines and the parser finds nothing.
>         # The printed format, not the shell spelling (loop row L1-3): `── [<gate>] $ ` and `
> ── [<gate>] RED (block)`.
>         script = (REPO_ROOT / "scripts" / "verify_all.sh").read_text(encoding="utf-8")
> >       assert re.search(r"── \[\$\{?\w+\}?\] \$ ", script) and re.search(r"── \[\$\{?\w+\}?\] RED \(block\)", script)
> E       assert (None)
> E        +  where None = <function search at 0x105ef2c00>('── \\[\\$\\{?\\w+\\}?\\] \\$ ', '#!/usr/bin/env bash\n# verify_all.sh — the local runner of the ONE gate list.\n#\n# It holds no commands of its own: ... report above names it."\n    exit 1\nfi\necho "VERIFY GREEN — every local gate of the \'$JOB\' job passed."\nexit 0\n')
> E        +    where <function search at 0x105ef2c00> = re.search
>
> tests/test_stage2.py:2639: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=16589) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/tests/test_stage2.py:21277: DeprecationWarning: This process (pid=16587) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_the_frames_red_sections_reads_are_the_ones_verify_all_prints
> 1 failed, 5399 passed, 18 skipped, 5 warnings in 1381.41s (0:23:01)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> make: *** [verify] Error 1
> ```

Stage-2 call, 2026-11-11: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 1012 files, 3902 commits, 12 rules.

Stage-2 call, 2026-11-11: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM Flash failed twice; the Sonnet call of 01:01 UTC ended with exit 1 before changing anything; one test from green; the maintainer set the verify speed-up as first priority on 2026-11-10 · leak check clean over 1012 files, 3906 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1012 files, 3918 commits, 12 rules.

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model longcat-2.5-free · leak check clean over 1012 files, 3919 commits, 12 rules.

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1012 files, 3921 commits, 12 rules.

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1012 files, 3921 commits, 12 rules.

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 1012 files, 3921 commits, 12 rules.

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1012 files, 3921 commits, 12 rules.

Stage-2 call, 2026-11-11: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Codex calls ended with exit 1 on 2026-11-11 · leak check clean over 1012 files, 3923 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `Makefile` +1 -1
> - `README.md` +1 -1
> - `docs/WORKFLOW.md` +1 -1
> - `docs/testing.md` +1 -1
> - `prompts/05-verify.md` +1 -1
> - `scripts/ci_gates.py` +2 -19
> - `scripts/stage2.py` +1 -1
> - `tests/test_verify_cheap_first.py` +7 -0
>
> Diagnostics:
> ````text
> - lifecycle fields: plans/changes/verify-cheap-first/plan.md, plans/changes/verify-cheap-first/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: red) because the targeted coverage was not safe: `Makefile` is an input kind the targeted selector does not cover
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ '/Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/.venv/bin/python3' -m pytest tests/ -q -n auto
> [… 78 lines of this gate left out …]
> ..................                                                       [100%]
> =================================== FAILURES ===================================
> ___________ test_verification_admission_is_outside_execution_timeout ___________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1950/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1950/popen-gw1/test_verification_admission_is0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10be40860>
>
>     def test_verification_admission_is_outside_execution_timeout(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
>         # Criterion 4 of the machine lock. Planted fault: the admission wait counted against the
>         # step limit — a short passing check times out after queueing — or the limit dropped, so
>         # a hung executing check escapes its group cleanup.
>         monkeypatch.setattr(stage2, "VERIFY_SECONDS", 2.0)
>         ready = world.state / "holder-ready"
>         holder = _real_holder(ready)
>         try:
>             _holder_acquired(ready)
>             problems: list[str] = []
>     
>             def attempt() -> None:
>                 problems.extend(stage2.verify_attempt(world.root, world.plan))
>     
>             world.script(make=[{"stdout": "green", "sleep": 1.5}])
>             queued = threading.Thread(target=attempt)
>             queued.start()
>             time.sleep(1.0)  # a real second of queueing while the holder owns the admission
>             holder.terminate()
>             holder.wait(timeout=30)
>             queued.join(timeout=90)
> >           assert problems == [], f"the admission wait consumed the step limit: {problems}"
> E           AssertionError: the admission wait consumed the step limit: ["`make verify` did not finish: make was stopped by the runner's step limit after 0.0 minutes"]
> E           assert ['`make verif... 0.0 minutes'] == []
> E             
> E             Left contains one more item: "`make verify` did not finish: make was stopped by the runner's step limit after 0.0 minutes"
> E             Use -v to get more diff
>
> tests/test_stage2.py:2222: AssertionError
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] waiting for admission: holder pid 74903 (/Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/.venv/bin/python3 -c import os, pathlib, time; pathlib.Path(os.environ['HOLDER_READY']).write_text(str(os.getpid())); time.sleep(30.0), started 2026-11-11T10:44:16)
> [verify-lock] admitted after 1s
> [verify-lock] available memory cannot be measured; proceeding without a reading
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=45837) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/tests/test_stage2.py:21277: DeprecationWarning: This process (pid=45838) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout
> 1 failed, 5400 passed, 17 skipped, 5 warnings in 1311.96s (0:21:51)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 37015 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/verify-cheap-first/stage2/attempts/verify-cheap-first/attempt-1-20261111T093905554612Z-478a9b6c.md
> ````

Stage-2 call, 2026-11-11: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1012 files, 3925 commits, 12 rules.

Runner restoration, 2026-11-11: repair · attempt 1 · route codex — lifecycle fields: plans/changes/verify-cheap-first/plan.md, plans/changes/verify-cheap-first/spec.md — unchanged; plans/changes/verify-cheap-first/plan.md, plans/changes/verify-cheap-first/spec.md — unchanged

Stage-2 call, 2026-11-11: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1012 files, 3928 commits, 12 rules.

> Runner verification scope:
> - Attempt 1 (codex): full `make verify` ran (result: green) because the targeted coverage was not safe: `Makefile` is an input kind the targeted selector does not cover

Runner restoration, 2026-11-11: repair · attempt 1 · route codex — lifecycle fields: plans/changes/verify-cheap-first/plan.md, plans/changes/verify-cheap-first/spec.md — unchanged

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1012 files, 3932 commits, 12 rules.

Stage-2 call, 2026-11-11: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1012 files, 3936 commits, 12 rules.

> Runner verification scope:
> - Attempt 1 (codex): full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/ci_gates.py` is shared execution infrastructure

Runner restoration, 2026-11-11: repair · attempt 1 · route codex — lifecycle fields: plans/changes/verify-cheap-first/plan.md, plans/changes/verify-cheap-first/spec.md — unchanged

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model hy3 · leak check clean over 1012 files, 3954 commits, 12 rules.

Stage-2 call, 2026-11-11: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1012 files, 3959 commits, 12 rules.

> Runner verification scope:
> - Attempt 1 (codex): full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/verify_all.sh` is shared execution infrastructure

Runner restoration, 2026-11-11: repair · attempt 1 · route codex — lifecycle fields: plans/changes/verify-cheap-first/plan.md, plans/changes/verify-cheap-first/spec.md — unchanged

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1012 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-11: review-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1012 files, 3961 commits, 12 rules.

Stage-2 call, 2026-11-12: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1012 files, 3964 commits, 12 rules.

## Phase 6 — Codex, 2026-11-12

Codex reported no finding.

The answer was not only six-cell rows; what is not one is kept below as it came.

> No finding.

Phase 6 verdict: codex 01a1cceb-9052-7c30-b006-f47246c78dcf, 2026-11-12
Reviewer session: codex 01a1cceb-9052-7c30-b006-f47246c78dcf — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-12

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | BLOCKER | correctness | base | scripts/ci_gates.py (SCHEMA_VERSION=3, cost validation) vs decisions/gates.yaml (scripts/ci_gates.py:79) | Schema 3 makes a missing or invalid `cost` a validation error, but no hunk in the diff updates decisions/gates.yaml; validate_schema would reject the repository's own gate list, so --check-schema, --commands and --generate-ci fail, and tests/test_ci.py::test_repository_gate_schema_is_v3 (which asserts schema 3 with costs on pytest/leerprobe) cannot pass. | longcat-2.5-free | rejected — measured false: decisions/gates.yaml declares schema 3 with a cost on all 24 gates since 56cdfe4e (held path, outside the reviewer's diff); `ci_gates.py --check-schema` and `--check-ci` pass; the full check is green at d289afcd (2026-11-11, VERIFY GREEN, 1515 s) and tests/test_ci.py::test_repository_gate_schema_is_v3 runs unskipped in it |  | disagree — The reviewed diff updates decisions/gates.yaml to schema 3 with costs; schema validation passes. |
| L1-2 | MAJOR | tests | base | tests/test_gate_catalog.py (HEADER/COLUMNS/_expected_cells) vs docs/governance/gate-catalog.md (tests/test_gate_catalog.py:30) | The catalogue test now requires a cost column in the committed generated block, but no hunk regenerates docs/governance/gate-catalog.md; the committed file still carries the old 8-column header, so the inventory-to-rendering comparison fails. | longcat-2.5-free | rejected — measured false: docs/governance/gate-catalog.md carries the regenerated nine-column inventory since 56cdfe4e; tests/test_gate_catalog.py passes; the full check is green at d289afcd (2026-11-11, VERIFY GREEN, 1515 s) and tests/test_ci.py::test_repository_gate_schema_is_v3 runs unskipped in it |  | disagree — The reviewed diff regenerates the catalogue with the cost column; it matches the generator. |
| L1-3 | BLOCKER | completeness | base | scripts/verify_all.sh (absent from the diff) (tests/test_ci.py:1728 and tests/test_verify_cheap_first.py) | The changed tests assert the runner stops at the first local blocking failure, names unreached gates as `──   [x] not run`, and leaves no history event for them, and the new test module's docstring requires scripts/verify_all.sh to implement that stop — but no hunk modifies verify_all.sh, so the copied runner is unchanged and every early-stop assertion fails. | longcat-2.5-free | rejected — measured false: scripts/verify_all.sh is changed by this branch (git diff origin/main...HEAD names it) and prints the not-run summary; tests/test_verify_cheap_first.py passes; the full check is green at d289afcd (2026-11-11, VERIFY GREEN, 1515 s) and tests/test_ci.py::test_repository_gate_schema_is_v3 runs unskipped in it |  | disagree — The reviewed diff changes verify_all.sh and implements stopping, skipped-gate reporting and execution-only history. |
| L2-1 | MINOR | MAINT | base | `docs/WORKFLOW.md` ("Verification runs through git and CI, not through the harness"), `docs/testing.md` ("Where tests run"), `prompts/05-verify.md` (the command block) | All three still define `make verify` as the full local run of every locally runnable gate and say nothing about the new stop; after this change a red local run ends at the first blocking gate and only names the rest as not run. The behaviour is described only in the generated gate catalogue and in `decisions/gates.yaml`, which the local-run sections do not point to, so the doctrine and the runner a reader is about to use disagree. | deepseek-v4.1-flash | fixed — not a test — docs/WORKFLOW.md and docs/testing.md describe early stopping and identify unexecuted gates. | no — not a test | agree |
| L2-2 | MINOR | MAINT | base | `scripts/ci_gates.py`, `deklarierte_schema_version` and the `--check-schema` success line in `main` | The helper is a leftover of the temporary version-2 dispatch the plan removes before delivery: it has no caller beyond the `--check-schema` success message, and its docstring still claims it drives the cost order and the catalogue, which it does not. It re-reads the gate file after validation has already passed and prints whatever it finds, so a file that becomes unreadable between the two reads yields "Gate-Datei ok … Schema 0" with exit green — a passing check reporting a schema the file never had, where the constant it validated would have been correct. | deepseek-v4.1-flash | fixed — tests/test_verify_cheap_first.py::test_schema_success_reports_validated_version_without_rereading | yes — tests/test_verify_cheap_first.py::test_schema_success_reports_validated_version_without_rereading | agree |
| L2-3 | MINOR | MAINT | base | docs/WORKFLOW.md:534, docs/testing.md:62, README.md:178, Makefile `help` | These four descriptions still present `make verify` as running every locally runnable gate ("the full local run of every gate that can measure on this machine", "all gates"), but the local runner now stops at the first blocking failure and names the remaining selected gates as not run; the gate catalogue prose was rewritten for the new behavior while these texts were not, so a maintainer reading them after a short red run reads it as a complete one — the exact misreading the not-run summary exists to prevent. | mimo-v2.6-flash | fixed — not a test — Makefile help describes cheap-first execution, blocking failure stops and unexecuted gates. | no — not a test | agree |
| L2-4 | MINOR | MAINT | base | scripts/stage2.py, `run_targeted` docstring | The docstring claims the selected gates run "in gate-list order through the locked interpreter, as `verify_all.sh` runs them", but after this change the local runner derives a cost order (seconds before minutes) and stops at the first blocking failure, while `run_targeted` still walks `ci_gates.gates()` in declaration order with the expensive suite before the cheap gates; the stated parity with the local runner no longer holds, and the repair path keeps the expensive-first order the change removes everywhere else. | mimo-v2.6-flash | fixed — not a test — run_targeted documents declaration order without claiming local-runner ordering. | no — not a test | agree |
| L2-5 | MINOR | MAINT | base | scripts/ci_gates.py, `validate_schema` and `deklarierte_schema_version` | A gate file declaring `schema_version: 3.0` passes validation, because the version is compared with `!=` and the float 3.0 equals the integer 3, and `--check-schema` then prints "Schema 0" — `deklarierte_schema_version` accepts only `int` — so a non-integer version is consumed as schema 3 while the success message contradicts the version the check enforces. | mimo-v2.6-flash | fixed — tests/test_verify_cheap_first.py::test_schema_version_requires_integer_three | yes — tests/test_verify_cheap_first.py::test_schema_version_requires_integer_three | agree |
| L3-1 | MAJOR | SPEC | base | `plan.md` "Limits and ownership", `spec.md` "Protected areas" vs the diff's `prompts/05-verify.md` and `scripts/stage2.py` hunks | The change's own scope statement forbids exactly the two files it edits: the plan says "No changes to `scripts/stage2.py` … prompts or model routes", the spec's protected areas say "No edits to … workflow prompts", and the Definition of Done claims "The pull request file list shows the protected scope and non-goals held". The prompt line and the runner docstring are edited anyway. Either the scope statements are wrong or the edits are; a decision pull request the maintainer merges on the strength of "protected scope held" cannot be checked as written. | qwen3.8-flash | fixed — orchestrator hand edit 898ebcee (maintainer chose to widen the scope, decisions Q-2) | no | agree |
| L3-2 | MAJOR | SPEC | base | `scripts/verify_all.sh` (the `stop_gate` branch in the gate loop) with `decisions.md` Q-1's [DETAIL] "Report and advisory gates never stop a run, wherever the sort places them. Reason: that is their meaning today; only the order changes" | A report or advisory gate can now be *skipped* rather than merely non-blocking, so what the decision calls "only the order changes" is false and criterion 6's promise ("its failure remains visible") holds only when the nonblocking gate happens to sort ahead of the failure. The runner's own draft check shows the cost: in the `docs` subset `plans-registry` (block) precedes `docs-links` (report), so a red plans-registry now hides every docs-links finding the same run used to print. No test covers a nonblocking gate *after* a blocking failure — `test_nonblocking_failures_continue_without_red_verdict` puts the failing report/advisory gate first and asserts the run stays green. | qwen3.8-flash | fixed — orchestrator hand edit 898ebcee (criterion 6 and the DETAIL name the not-run advisory gate) | no | agree |
| L3-3 | MAJOR | MAINT | base | `scripts/verify_all.sh`, the frame line `echo "── [$gid] $ $lauf_cmd"` | This fixes a pre-existing bug (the old line printed the literal word `lauf_cmd`, because `$ ` before a name is not an expansion) and the fix is named in no criterion, no decision and no plan step. It changes what every local gate frame prints: the frame now echoes the resolved interpreter, so `── [pytest] $ '/Users/<user>/…/.venv/bin/python3' -m pytest …` reaches the run log, and `red_sections` copies that line into `findings.md` and into the repair prompt sent to a foreign model — the diff's own findings.md hunk already shows such a line. A machine-local absolute path becoming part of the quoted repair evidence is a contract change facing outward and should be a declared, tested decision of its own, not a passenger in a cost-ordering change. | qwen3.8-flash | fixed — tests/test_verify_cheap_first.py::test_gate_frame_uses_declared_interpreter_without_absolute_path | yes — tests/test_verify_cheap_first.py::test_gate_frame_uses_declared_interpreter_without_absolute_path | agree |
| L3-4 | MAJOR | MAINT | base | `scripts/stage2.py`, `run_targeted` docstring ("gate-list order … as `verify_all.sh` runs them" → "declaration order") | The bead's failure mode — a cheap document gate red behind an expensive test gate — also exists in the runner's targeted check, which selects from `ci_gates.gates()` and still starts the expensive gate first; that is the most frequent verification path (every repair attempt). The diff does not order that path by cost, and its only edit there deletes the sentence that tied the two paths together, so nothing in the tree now says they *should* agree or why they do not. The spec's non-goals exclude "changing … targeted repair scheduling" but nowhere record that the runner's targeted path keeps the expensive-first order — the divergence is hidden by a wording change instead of decided. | qwen3.8-flash | rejected — scope: ordering the targeted check by cost changes the runner's behaviour, which this change does not (decisions Q-2); handed to bead coding-harness-0swp, which reworks run_targeted | no | disagree — Targeted repair scheduling is explicitly excluded from this change; retaining declaration order violates no promised behavior. |
| L3-5 | MINOR | MAINT | base | `docs/testing.md` header (`updated: 2026-11-02`, `last_reviewed: 2026-11-02`) vs its edited "Where tests run" table and new paragraph | The document's content now describes cheap-first and the early stop, but its header still claims 2026-11-02, while `docs/WORKFLOW.md` and `docs/governance/gate-catalog.md` were stamped for the same edit. Nothing catches this: `provenance.yaml` carries no prefix matching `docs/testing.md`, so `check_frontmatter_current.is_held()` reports False and the gate whose stated reason is "a header older than its document's last change misleads every reader" never measures the file — and `scripts/kit/manifest.yaml` classifies it as `mechanismus`, so the stale header is handed to every recipient repository. | qwen3.8-flash | fixed — not a test — Updated docs/testing.md's updated stamp to 2026-11-11. | no — not a test | agree |
| L3-6 | MINOR | MAINT | base | `scripts/verify_all.sh`, the `if [ -n "$stop_gate" ]` summary block | The header is printed for every blocking failure, including the case where the failing gate was the last selected one: the run then says "── not run — the run stopped at the blocking failure in [x]:" and names nothing. A reader cannot tell "nothing was skipped" from "the skipped list was cut off", which is the one confusion criterion 4 exists to prevent. Either print the header only when something is listed, or say explicitly "no gate was left". | qwen3.8-flash | fixed — tests/test_verify_cheap_first.py::test_last_blocking_failure_has_no_empty_not_run_summary | yes — tests/test_verify_cheap_first.py::test_last_blocking_failure_has_no_empty_not_run_summary | agree |
| L3-7 | MINOR | MAINT | base | `scripts/ci_gates.py` `gates()` (`"cost": g.get("cost")`) against `kostenordnung()` (`g["cost"] != "seconds"`) and `catalog_rows()` (`_zelle(g['cost'])`) | Three readers of the same field disagree about whether it can be missing: the record builder allows `None`, the sort then silently files that gate in the expensive class, and the catalogue would raise a `KeyError`. The `.get` is the residue of the temporary version-2 branch that plan step 4 says to remove ("it never ships"), and no test covers the hand-built-record path for a missing cost — every fixture in the new tests was simply given a `cost`. A gate can thus lose its place in the cheap class without any message. | qwen3.8-flash | fixed — tests/test_verify_cheap_first.py::test_gate_record_requires_cost_even_without_schema_validation | yes — tests/test_verify_cheap_first.py::test_gate_record_requires_cost_even_without_schema_validation | disagree — Schema validation rejects missing costs before record construction; the claimed silent fallback requires bypassing validation. |
| L3-8 | MINOR | MAINT | base | `scripts/ci_gates.py` `--list` branch (untouched) with `docs/WORKFLOW.md` "make gates — what the CI runs, read from decisions/gates.yaml" | The one thing this change makes a rule of — the order a local run will use — is visible in no command: `--list` still prints declaration order with no cost column, and the `--commands` sort only happens with `--placement lokal`. To see what `make verify` will actually do, a maintainer reads the generated catalogue table or the YAML by hand. A short cost column (or a cheap-first ordering in the list) in `--list` would keep the two documented commands able to answer their own questions. | qwen3.8-flash | fixed — tests/test_verify_cheap_first.py::test_list_exposes_each_gate_cost | yes — tests/test_verify_cheap_first.py::test_list_exposes_each_gate_cost | disagree — Declaration-order inventory is intentional; adding scheduling visibility to --list is an enhancement, not a demonstrated correctness fault. |
| L4-1 | MINOR | MAINT | base | scripts/verify_all.sh (not-run summary ≈ lines 308–318) and scripts/stage2.py (GATE_START/GATE_END, ≈ 5214–5215) | The not-run summary deliberately prints `──   [<gid>] not run` with three spaces after `──` so the repair-evidence parser's `^── \[...\]\ \$ ` regex (one space) never matches it. That space-count gap is the entire contract keeping skipped gates out of `red_sections`; the comment names `^── \[` but the real guard is the extra spaces. Any future loosening of the gate-frame regex (e.g. tolerating indentation/whitespace) would silently turn skipped gates into parsed repair-diagnostic sections with no test catching it. | hy3 | fixed — not a test — strengthened tests/test_verify_cheap_first.py::test_early_stop_preserves_repair_diagnostics to reject real not-run lines as gate frames; documented exact spacing. Planted regex fault fails; ruff and all 17 ledger cases pass. | no — not a test | disagree — Whitespace tolerance alone cannot create a skipped-gate section: the start pattern also requires the command marker `$ `. |
| L4-2 | MINOR | MAINT | base | scripts/stage2.py `targeted_selection` (≈ 5941) / `run_targeted` (≈ 6100) versus scripts/ci_gates.py `kostenordnung` and scripts/verify_all.sh | The cheap-first ordering is applied only through `verify_all.sh`'s `--commands --placement lokal` path; `run_targeted` and `targeted_selection` still read `gates()` in declaration order and never call `kostenordnung`, so the runner's own targeted verification step (the repair/targeted check described in docs/testing.md) does not get fast failure on a cheap gate. The docs promise cheap-first local verification without noting the targeted path diverges, so a maintainer would assume the speed-up everywhere. | hy3 | rejected — scope, same mechanism as L3-4: ordering the targeted check by cost changes the runner's behaviour, which this change excludes; the docs/testing.md row describes `make verify` only and is accurate |  | disagree — Targeted repair scheduling is an explicit non-goal; this repeats L3-4 without evidence of a violated contract. |

Rounds run: 5

Record digest: sha256:078c3ec13a17aca10ff3f37cd8e1a21669ecb7823e920693b49027cc721f9a88

Record identity: sha256:80a32599232741ec42bf291f3f67045d480a3cb85ce7601baab91701c74d3d38

Cut rounds: 1, 2, 3, 4, 5

Loop state: {"availability": {"checked_at": "2026-11-11T08:11:35+00:00", "failed": {"deepseek-v4-pro": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "glm-5.2": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "glm-5.3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "grok-4.7": "pi call failed: exit 1: opencode-go API error (403): {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "kimi-k3": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled. Change model access at https://opencode.ai/console/org_01M4B95TJJFHPCVG762QQEEA05/models.\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated. Use mimo-v2.6-pro instead.\"}"}, "reachable": ["longcat-2.5-free", "deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "hy4-preview", "kimi-k2.7-code", "step-5-preview", "qwen3.8-max"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "hy4": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 \"thinking.type.enabled is not supported for this model; use thinking.type.adaptive\" (a Pi adapter setting, bead coding-harness-36za evidence))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 \"Model access is disabled\")", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": ["the data terms of longcat-2.0 expire on 2026-11-16 (5 days left)", "the data terms of glm-5.3-flash expire on 2026-11-16 (5 days left)", "the data terms of qwen3.8-flash expire on 2026-11-16 (5 days left)", "the data terms of gpt-6-luna expire on 2026-11-16 (5 days left)", "the data terms of claude-haiku-5-5 expire on 2026-11-16 (5 days left)", "the data terms of minimax-m3 expire on 2026-11-16 (5 days left)"]}, "consumed": ["free", "rung:glm-5.3-flash", "flash", "rung:qwen3.8-flash", "rung:hy3", "rung:qwen3.7-plus"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-fable-5-2", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "iceman-free", "provider": "opencode"}, {"model": "inkling-2-small-free", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "longcat-2.5-free", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "minimax-m3.1-flash-free", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-ember-1.0", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "longcat-2.5-free", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-11T08:04:19+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1794384258215, "etag": "W/\"b5b0db66a128f2404bed0bc661f5f369\"", "lastModified": 1794318971000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "longcat-2.5-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "LongCat 2.5 Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": ["opencode-go/gemini-4-argon: wire api \"google-generative-ai\" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base"], "overlay": ["beam-free", "claude-haiku-5-5", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "longcat-2.5-free", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}, {"date": "2026-11-06", "id": "iceman-contributor-free", "reason": "New in the live Go catalog on 2026-11-06 and picked as the whole free swarm by prepare-loop; \"contributor\" ids on Go have meant that request data may be used for training, and the maintainer's decision of 2026-10-17 (question Q-12) keeps such models off. The Go page's privacy table, read 2026-11-06, confirms it: 'Iceman Contributor Free | Yes | Not ZDR'. A bridge until one central per-use-case model policy exists (bead coding-harness-k0ub with coding-harness-wq1m); maintainer, 2026-11-06, morning question Q-M9, option A."}, {"date": "2026-11-06", "id": "cat-jam-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it, so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}, {"date": "2026-11-06", "id": "longcat-2.5-preview-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it (only LongCat-2.0), so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": ["longcat-2.5-free"], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "hy4-preview", "kimi-k2.7-code", "step-5-preview", "qwen3.8-max"], "rungs": ["glm-5.3-flash", "qwen3.8-flash", "hy3", "qwen3.7-plus", "minimax-m3.1-flash", "mimo-v2.6-pro", "minimax-m3", "hy4-preview", "kimi-k2.7-code", "step-5-preview", "qwen3.8-max"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base.
> Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor.
> Notice: the data terms of longcat-2.0 expire on 2026-11-16 (5 days left).
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (5 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (5 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (5 days left).
> longcat-2.5-free was asked again with the format reminder: the first answer was malformed
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the free diff of tests/test_verify_cheap_first.py was cut at 400 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From longcat-2.5-free:
> longcat-2.5-free's first answer, which was not in the required format:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> </longcat_tool_call>
> 
> Notice: the data terms of longcat-2.0 expire on 2026-11-16 (5 days left).
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (5 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (5 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (5 days left).
> longcat-2.0 failed: pi call failed: exit 1 (Stream ended without finish_reason); replaced by glm-5.3-flash
> glm-5.3-flash failed: /Users/mikypiky/coding-harness/.claude/worktrees/verify-cheap-first/tools/pi/pi was stopped by the round time limit of 45 minutes (175 seconds were left for this call); the round time limit expired; no replacement starts
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 2434 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Notice: the data terms of longcat-2.0 expire on 2026-11-16 (5 days left).
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (5 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (5 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (5 days left).
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 2715 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> Notice: the data terms of longcat-2.0 expire on 2026-11-16 (5 days left).
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (5 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (5 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (5 days left).
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> The diff was cut: the change diff was cut at 2000 of 2840 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From hy3:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> Based on my review of the diff, the core mechanism is implemented and well-tested. I found two maintainer-facing issues.
> 
> Notice: the data terms of longcat-2.0 expire on 2026-11-16 (5 days left).
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (5 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (5 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (5 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (5 days left).
> qwen3.7-plus was asked again with the format reminder: the first answer was malformed
> Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base
> qwen3.7-plus reported no finding.
> The diff was cut: the change diff was cut at 2000 of 2860 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From qwen3.7-plus:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> No finding.
> 
> From qwen3.7-plus:
> qwen3.7-plus's first answer, which was not in the required format:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> After thorough analysis of the diff, I find no issues with the change.
> 
> The implementation correctly delivers all promised behavior:
> 
> 1. **Schema 3 with required cost field** — `validate_schema` rejects missing, null, non-string, unknown, boolean, and empty cost values on every gate kind, including advisory, hosted-only, and drift gates.
> 
> 2. **Cheap-first ordering** — `kostenordnung()` uses a stable sort (`g["cost"] != "seconds"` yields False=0 for seconds, True=1 for minutes), preserving declaration order within each class. Sorting applies only when `--placement lokal`, not for CI or other placements.
> 
> 3. **Early stop at first blocking failure** — The shell script sets `stop_gate` after a blocking gate fails, then skips subsequent gates by accumulating them in `verbleibend`. Non-blocking failures (report/advisory) don't trigger the stop.
> 
> 4. **Not-run summary** — Uses `──   [$gid] not run` (3 spaces) to avoid collision with gate frames (`── [$gid]` with 1 space). Tests verify that `GATE_START` and `GATE_END` don't match summary lines, and `red_sections()` returns `None` when fed only summary lines.
> 
> 5. **CI stays exhaustive** — `CI_MODE=1` prevents `stop_gate` from being set, so all gates run regardless of failures.
> 
> 6. **Repair parser compatibility** — The frame format `echo "── [$gid] $ $cmd"` prints the raw command (with literal `python3`), not the resolved interpreter path. This is intentional ("Keep machine-local interpreter paths out of logs and repair evidence") and tested by `test_gate_frame_uses_declared_interpreter_without_absolute_path`.
> 
> 7. **History honesty** — Only executed gates receive timing events. The `run_end` event has the red verdict. Skipped gates produce no events.
> 
> 8. **Kit transfer** — The test copies mechanism files to a recipient tree with renamed gate IDs and verifies cheap-first behavior without importing source-tree modules.
> 
> 9. **Documentation** — All docs (`WORKFLOW.md`, `testing.md`, `gate-catalog.md`, `README.md`, `Makefile`, `prompts/05-verify.md`) are updated consistently. The catalog explains cost classes in prose.
> 
> 10. **Test coverage** — Comprehensive tests cover schema validation, cost ordering, early stop, not-run summary, green runs, non-blocking failures, CI mode, repair diagnostics, history, kit transfer, and real gate list activation.
> 
> No finding.

<!-- End of released loop record -->

Stage-2 call, 2026-11-12: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 1012 files, 3964 commits, 12 rules.
