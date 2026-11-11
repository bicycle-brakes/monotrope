---
title: "Findings — verify-cheap-first"
category: findings
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-11
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
