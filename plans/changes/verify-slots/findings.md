---
title: "Findings — verify-slots"
category: findings
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — verify-slots

Stage-2 call, 2026-11-09: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 981 files, 3785 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-slots/plan.md` +157 -0
> - `plans/changes/verify-slots/spec.md` +174 -0
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [question-context] $ lauf_cmd
>   - plans/changes/verify-slots/decisions.md: Q-1 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/verify-slots/decisions.md: Q-2 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
> question-context NOT MEASURED: 2 unreadable evidence — exit 3, nothing measured.
> ── [question-context] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 35465 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-09: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason the first draft attempt failed · leak check clean over 984 files, 3787 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`
> - `plans/changes/verify-slots/decisions.md`

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-slots/decisions.md` +7 -0
> - `plans/changes/verify-slots/plan.md` +11 -8
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [frontmatter-current] $ lauf_cmd
> plans/changes/verify-slots/findings.md: stale — updated 2026-11-09 is older than its last change 2026-11-10 (uncommitted)
> plans/changes/verify-slots/plan.md: stale — updated 2026-11-09 is older than its last change 2026-11-10 (uncommitted)
> plans/changes/verify-slots/spec.md: stale — updated 2026-11-09 is older than its last change 2026-11-10 (uncommitted)
> fix: python3 scripts/check_frontmatter_current.py --stamp
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
> ── [question-context] $ lauf_cmd
>   - plans/changes/verify-slots/decisions.md: Q-1 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/verify-slots/decisions.md: Q-2 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
> question-context NOT MEASURED: 2 unreadable evidence — exit 3, nothing measured.
> ── [question-context] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 35511 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-10: draft · attempt 3 · route glm · endpoint glm-coding-plan · model glm-5.3 · reason two Codex draft attempts failed · leak check clean over 984 files, 3792 commits, 12 rules.

> Attempt 3 (glm): the runner put back what a draft may not change:
> - `plans/INDEX.md`

> Attempt 3 (glm) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-slots/plan.md` +129 -106
> - `plans/changes/verify-slots/spec.md` +141 -107
>
> Diagnostics:
> ````text
> - `bash scripts/verify_all.sh --job docs` exited 1
> The gates that blocked, each with its last lines:
> ── [question-context] $ lauf_cmd
>   - plans/changes/verify-slots/decisions.md: Q-1 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
>   - plans/changes/verify-slots/decisions.md: Q-2 — the record states no decision statement beginning `In the context of`; the recording day cannot be read
> question-context NOT MEASURED: 2 unreadable evidence — exit 3, nothing measured.
> ── [question-context] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 35560 earlier lines left out …]
> templates/spec.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 127]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> ````

Stage-2 call, 2026-11-10: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 984 files, 3818 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +41 -25
> - `docs/how-it-works.md` +9 -5
> - `docs/orchestration.md` +12 -8
> - `plans/changes/verify-slots/measurements.md` +50 -0
> - `plans/changes/verify-slots/plan.md` +11 -11
> - `scripts/stage2.py` +6 -2
> - `scripts/verify_all.sh` +5 -3
> - `scripts/verify_lock.py` +337 -85
> - `tests/test_ci.py` +144 -1
> - `tests/test_stage2.py` +59 -1
> - `tests/test_verify_lock.py` +609 -13
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed `scripts/verify_lock.py`, `tests/test_ci.py`, `tests/test_verify_lock.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> tests/test_verify_lock.py:188:5: PTH105 `os.replace()` should be replaced by `Path.replace()`
>     |
> 186 |     fresh = root / f".{verify_lock.SLOTS_NAME}.{os.getpid()}"
> 187 |     fresh.write_text(content, encoding="utf-8")
> 188 |     os.replace(fresh, root / verify_lock.SLOTS_NAME)
>     |     ^^^^^^^^^^ PTH105
>     |
>
> Found 1 error.
> ```

Stage-2 call, 2026-11-10: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 985 files, 3822 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-slots/plan.md` +11 -11
> - `tests/test_verify_lock.py` +1 -1
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
>         assert _wait_until(lambda: "holder-b" in _log_lines(log)), "holder B never started"
>         waiter_one = _supervised(state, ORDER_BODY, extra("waiter-1", "0.2"))
> >       assert _wait_until(lambda: len(_records(state)) >= 3), "the first waiter never registered"
> E       AssertionError: the first waiter never registered
> E       assert False
> E        +  where False = _wait_until(<function test_slot_waiters_reserve_in_fifo_order.<locals>.<lambda> at 0x10882f9c0>)
>
> tests/test_verify_lock.py:1541: AssertionError
> __________________ test_shell_runner_obeys_two_slot_admission __________________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-slots/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1655/popen-gw0/test_shell_runner_obeys_two_sl0')
>
>     def test_shell_runner_obeys_two_slot_admission(tmp_path: Path) -> None:
>         """Criterion 8 of verify-slots: the shell runner and its CI entry obey the configured capacity.
>     
>         Fault this pins: a shell or CI run bypassing the capacity, a gate verdict
>         changed by it, or a nested run queueing behind its own ancestor's
>         admission instead of reusing it.
>         """
>         home = tmp_path / "home"
>     
>         # (A) capacity two: two concurrent runs overlap their gates, and each run's
>         # gate nests in the admission its own shell entry holds
>         base = tmp_path / "two"
>         _write_runner_capacity(base / "state", "2")
>         left = _slot_tree(base / "left", "left-gate", "3", probe=True)
>         right = _slot_tree(base / "right", "right-gate", "3")
>         runs = [_background_runner(left, home), _background_runner(right, home)]
>         outs = [run.communicate(timeout=120) for run in runs]
>         for run, (out, err) in zip(runs, outs, strict=True):
>             assert run.returncode == 0, f"exit {run.returncode}\n{out}\n{err}"
>             assert "VERIFY GREEN" in out, out
>         left_span, right_span = _gate_times(base, "left", "left-gate"), _gate_times(base, "right", "right-gate")
>         assert left_span[0] <= right_span[1] and right_span[0] <= left_span[1], (
>             f"the two runs did not overlap at capacity two: {left_span} vs {right_span}"
>         )
>         held_code = (base / "left" / "gates" / "left-gate.code").read_text(encoding="utf-8").strip()
>         assert held_code == "0", f"the gate did not nest in its run's own slot admission: {held_code}"
>     
>         # (B) one of two concurrent runs fails blocking: its verdict stays red, the other stays green
>         base = tmp_path / "verdict"
>         _write_runner_capacity(base / "state", "2")
>         failing = _slot_tree(base / "failing", "failing-gate", "2", ending="exit 1")
>         passing = _slot_tree(base / "passing", "passing-gate", "2")
>         runs = [_background_runner(failing, home), _background_runner(passing, home)]
>         outs = [run.communicate(timeout=120) for run in runs]
>         assert runs[0].returncode == 1 and "RED (block)" in outs[0][0], outs[0]
>         assert runs[1].returncode == 0 and "VERIFY GREEN" in outs[1][0], outs[1]
>         fail_span, pass_span = _gate_times(base, "failing", "failing-gate"), _gate_times(base, "passing", "passing-gate")
>         assert fail_span[0] <= pass_span[1], f"the failing run held the other run back: {fail_span} vs {pass_span}"
>     
>         # (C) capacity one: an independent second run's gate waits for the first run's slot
>         base = tmp_path / "one"
>         _write_runner_capacity(base / "state", "1")
>         first = _slot_tree(base / "first", "first-gate", "3")
>         second = _slot_tree(base / "second", "second-gate", "0.3")
>         runs = [_background_runner(first, home), _background_runner(second, home)]
>         outs = [run.communicate(timeout=120) for run in runs]
>         for run, (out, err) in zip(runs, outs, strict=True):
>             assert run.returncode == 0, f"exit {run.returncode}\n{out}\n{err}"
>         first_span, second_start = _gate_times(base, "first", "first-gate"), _gate_times(base, "second", "second-gate")[0]
> >       assert second_start >= first_span[1], f"capacity one was exceeded: {first_span} vs start {second_start}"
> E       AssertionError: capacity one was exceeded: (1794307174, 1794307177) vs start 1794307174
> E       assert 1794307174 >= 1794307177
>
> tests/test_ci.py:2473: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_verify_lock.py::test_nested_entries_use_their_own_slot_and_context
> FAILED tests/test_stage2.py::test_a_runner_check_hands_its_child_the_admission_token
> FAILED tests/test_verify_lock.py::test_default_two_slots_share_capacity_across_trees
> FAILED tests/test_verify_lock.py::test_release_keeps_the_lock_held_by_an_inherited_descriptor
> FAILED tests/test_stage2.py::test_slot_admission_descriptors_reach_local_checks
> FAILED tests/test_verify_lock.py::test_independent_entries_share_one_machine_lock
> FAILED tests/test_verify_lock.py::test_slot_release_preserves_peers_and_inherited_children
> FAILED tests/test_verify_lock.py::test_wait_logs_name_all_occupied_slots_without_tokens
> FAILED tests/test_verify_lock.py::test_shared_capacity_setting_and_live_decrease
> FAILED tests/test_verify_lock.py::test_slot_waiters_reserve_in_fifo_order - A...
> FAILED tests/test_ci.py::test_shell_runner_obeys_two_slot_admission - Asserti...
> 11 failed, 15 passed in 22.00s
> ```

Stage-2 call, 2026-11-10: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 985 files, 3822 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/verify-slots/plan.md` +11 -11
> - `scripts/stage2.py` +2 -1
> - `scripts/verify_lock.py` +16 -4
> - `tests/test_ci.py` +13 -3
> - `tests/test_verify_lock.py` +6 -4
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - Runner cheap checks before post-run verification: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ..............F........F..                                               [100%]
> =================================== FAILURES ===================================
> ___________ test_verification_admission_is_outside_execution_timeout ___________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-slots/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1656/popen-gw...s/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1656/popen-gw2/test_verification_admission_is0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x106aaf140>
>
>     def test_verification_admission_is_outside_execution_timeout(world: World, monkeypatch: pytest.MonkeyPatch) -> None:
>         # Criterion 4 of the machine lock. Planted fault: the admission wait counted against the
>         # step limit — a short passing check times out after queueing — or the limit dropped, so
>         # a hung executing check escapes its group cleanup.
>         monkeypatch.setattr(stage2, "VERIFY_SECONDS", 2.0)
>         # capacity one: the runner's admission must genuinely queue behind the holder, the way the
>         # wait that this test pins only happens when the capacity is fully occupied
>         (world.state / "coding-harness").mkdir(parents=True, exist_ok=True)
>         (world.state / "coding-harness" / verify_lock.SLOTS_NAME).write_text("1", encoding="utf-8")
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
> tests/test_stage2.py:2207: AssertionError
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] waiting for admission: slot 0: holder pid 63590 (/Users/mikypiky/coding-harness/.claude/worktrees/verify-slots/.venv/bin/python3 -c import os, pathlib, time; pathlib.Path(os.environ['HOLDER_READY']).write_text(str(os.getpid())); time.sleep(30.0), started 2026-11-10T11:42:17)
> [verify-lock] admitted after 1s
> [verify-lock] available memory cannot be measured; proceeding without a reading
> ___________________ test_slot_waiters_reserve_in_fifo_order ____________________
> [gw4] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/verify-slots/.venv/bin/python3
>
> tmp_path = PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-1656/popen-gw4/test_slot_waiters_reserve_in_f0')
>
>     def test_slot_waiters_reserve_in_fifo_order(tmp_path: Path) -> None:
>         """Criterion 4. Live waiters reserve freed slots in registration order, without waiting for all to empty.
>     
>         Fault this pins: a later waiter overtaking an earlier live registration,
>         or a free slot kept idle until every other holder has finished.
>         """
>         state = tmp_path / "state"
>         log = tmp_path / "order.log"
>         extra = lambda name, seconds: {"PROBE_LOG": str(log), "PROBE_NAME": name, "PROBE_SLEEP": seconds}  # noqa: E731
>         holder_a = _supervised(state, ORDER_BODY, extra("holder-a", "6"))
>         assert _wait_until(lambda: "holder-a" in _log_lines(log)), "holder A never started"
>         holder_b = _supervised(state, ORDER_BODY, extra("holder-b", "6"))
>         assert _wait_until(lambda: "holder-b" in _log_lines(log)), "holder B never started"
>         waiter_one = _supervised(state, ORDER_BODY, extra("waiter-1", "0.2"))
>         # admitted holders have left the queue: only the live waiters keep a record
> >       assert _wait_until(lambda: len(_records(state)) >= 1), "the first waiter never registered"
> E       AssertionError: the first waiter never registered
> E       assert False
> E        +  where False = _wait_until(<function test_slot_waiters_reserve_in_fifo_order.<locals>.<lambda> at 0x10b697ce0>)
>
> tests/test_verify_lock.py:1542: AssertionError
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout
> FAILED tests/test_verify_lock.py::test_slot_waiters_reserve_in_fifo_order - A...
> 2 failed, 24 passed in 30.69s
> ```

Stage-2 call, 2026-11-10: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM Flash failed the post-run checks after the allowed attempts (2026-11-10) · leak check clean over 985 files, 3824 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2.py` +5 -3
> - `tests/test_verify_lock.py` +4 -3
>
> Diagnostics:
> ````text
> - Runner format before post-run verification: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 9269 lines of this gate left out …]
> FAILED tests/test_stage2_research_catalog.py::test_each_run_forces_a_fresh_go_catalog
> FAILED tests/test_stage2_research_catalog.py::test_removed_shipped_free_ids_do_not_return
> FAILED tests/test_stage2_research_catalog.py::test_free_eligibility_requires_text_chat_and_explicit_tools
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_capabilities_intersect_only_fresh_pi_ids
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[http-500]
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[http-404]
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[unparsable]
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[timeout]
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[not-an-object]
> FAILED tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots[no-provider]
> FAILED tests/test_stage2_research_catalog.py::test_capability_document_faults_and_candidate_faults_are_distinct
> FAILED tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules
> FAILED tests/test_stage2_research_catalog.py::test_nonempty_selection_keeps_both_sources_and_exclusion_evidence
> FAILED tests/test_stage2_research_catalog.py::test_duplicate_raw_keys_or_claimed_ids_exclude_all_free_candidates[{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"alpha-free":{"id":"alpha-free","tool_call":true},"beta-free":{"id":"beta-free","tool_call":true}}}}]
> FAILED tests/test_stage2_research_catalog.py::test_duplicate_raw_keys_or_claimed_ids_exclude_all_free_candidates[{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","tool_call":true},"beta-free":{"id":"alpha-free","tool_call":true}}}}]
> FAILED tests/test_stage2_research_catalog.py::test_duplicate_raw_keys_or_claimed_ids_exclude_all_free_candidates[{"opencode-go":{"models":{"alpha-free":{"id":"alpha-free","id":"alpha-free","tool_call":true},"beta-free":{"id":"beta-free","tool_call":true}}}}]
> FAILED tests/test_stage2_research_catalog.py::test_missing_metadata_id_excludes_only_that_candidate
> ERROR tests/test_pi_contract.py::test_real_catalog_move_uses_locked_pi_1_5_0
> ERROR tests/test_pi_contract.py::test_real_catalog_move_contains_new_go_models
> ERROR tests/test_pi_contract.py::test_real_catalog_move_keeps_messages_catalog_base
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-0]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[synthetic-protocol-check-free-946684800000]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-0]
> ERROR tests/test_pi_contract.py::test_real_refreshed_definition_resolves_without_newer_server_date[deepseek-v4.1-flash-946684800000]
> ERROR tests/test_pi_contract.py::test_real_resolution_uses_the_assessed_base[synthetic-protocol-check-free]
> ERROR tests/test_pi_contract.py::test_real_resolution_uses_the_assessed_base[deepseek-v4.1-flash]
> ERROR tests/test_pi_contract.py::test_real_reviewer_tool_contract - Failed: t...
> ERROR tests/test_pi_contract.py::test_real_free_reviewer_has_only_the_implementation_diff
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps
> ERROR tests/test_pi_contract.py::test_real_reviewer_ignores_ambient_credentials
> ERROR tests/test_pi_contract.py::test_real_extension_tool_input_and_result - ...
> ERROR tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads
> ERROR tests/test_pi_contract.py::test_real_session_binding_holds_the_assessed_base
> ERROR tests/test_pi_contract.py::test_real_model_listing_is_a_provider_table
> ERROR tests/test_pi_contract.py::test_real_opencode_provider_contracts - Fail...
> ERROR tests/test_pi_contract.py::test_contract_prerequisites_and_failures_are_mandatory
> ERROR tests/test_pi_contract.py::test_real_truncated_pi_print_failure_is_refused
> ERROR tests/test_pi_contract.py::test_real_context_overflow_fails_without_compaction
> ERROR tests/test_pi_contract.py::test_contract_environment_excludes_parent_provider_keys
> ERROR tests/test_pi_contract.py::test_real_catalog_headers_remain_literal - F...
> ERROR tests/test_pi_contract.py::test_shipped_catalog_prepares_both_swarms_offline
> ERROR tests/test_pi_contract.py::test_both_preparation_contracts_detect_planted_faults[review preparation refuses-the review preparation refused the shipped Go catalog-planted: the review preparation refuses]
> ERROR tests/test_pi_contract.py::test_both_preparation_contracts_detect_planted_faults[research preparation refuses-the research preparation refused the shipped Go catalog-planted: the research preparation refuses]
> ERROR tests/test_pi_contract.py::test_both_preparation_contracts_detect_planted_faults[research catalog helper refuses-the research preparation refused the shipped Go catalog-planted: the production research catalog helper refuses]
> ERROR tests/test_pi_contract.py::test_both_preparation_contracts_detect_planted_faults[review bypasses the shared selection-the review preparation refused the shipped Go catalog-refused: the model beam-free is a paid model; the free class does not admit it]
> ERROR tests/test_pi_contract.py::test_both_preparation_contracts_detect_planted_faults[research bypasses the shared selection-the research preparation refused the shipped Go catalog-refused: beam-free is a paid model; the free class does not admit it]
> 111 failed, 5111 passed, 17 skipped, 5 warnings, 29 errors in 1250.26s (0:20:50)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [leerprobe] $ lauf_cmd
> BLOCK (1):
>   - 1 red case(s) without a declared reason
>       tests.test_verify_lock::test_each_slot_checks_memory_before_work
>       
>       Add them with: python3 scripts/kit/probe.py --messen
>
> INFO  (1):
>   - 1383 of 1428 cases carry into a foreign repository (96 %)
>       mechanismus 113 · bestand 872 file(s)
>
> BLOCK (1), repeated last:
>   - 1 red case(s) without a declared reason
> ── [leerprobe] RED (block) — der Lauf ist rot.
> ── [plans-registry] $ lauf_cmd
> [… 199 lines of this gate left out …]
>   - Bead 'coding-harness-680l' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-680l` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-6ie' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-6ie` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-788' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-788` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-8v2c.1' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-8v2c.1` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-9ycy' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-9ycy` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-bvy' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-bvy` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-c99h' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-c99h` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-cjf9' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-cjf9` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-g19n' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-g19n` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-ibde' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-ibde` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-k93f' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-k93f` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-mfth' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-mfth` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-nr6h' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-nr6h` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-p3xq' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-p3xq` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-t83' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-t83` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-tlr4' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-tlr4` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-twvx' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-twvx` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-ut8q' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-ut8q` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-uxa9' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-uxa9` -- or set the bead back to 'open' if nobody is working on it.
>   - Bead 'coding-harness-xul8' is 'in_progress' but has no artefact under plans/changes/
>       The tracker says work is going on here; the workflow never heard of it. Fix: `make change NAME=<name> BEAD=coding-harness-xul8` -- or set the bead back to 'open' if nobody is working on it.
>
> INFO  (2):
>   - 28 running beads checked, 27 without artefact
>   - 535 artefacts checked
>
> BLOCK (1), repeated last:
>   - plans/changes/verify-slots/measurements.md: no readable frontmatter
> ── [plans-registry] RED (block) — der Lauf ist rot.
> ── [frontmatter-current] $ lauf_cmd
> docs/WORKFLOW.md: stale — updated 2026-11-09 is older than its last change 2026-11-10 (a258d445)
> plans/changes/verify-slots/measurements.md: no-frontmatter
> fix: python3 scripts/check_frontmatter_current.py --stamp
> (no-frontmatter and duplicate need a hand edit; the stamp names them and leaves them alone.)
> ── [frontmatter-current] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 35659 earlier lines left out …]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:3:81 error MD013/line-length Line length [Expected: 80; Actual: 117]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:85:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tests/fixtures/research_refs/plan-prompt-d862bc2.md:99 error MD040/fenced-code-language Fenced code blocks should have a language specified [Context: "```"]
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
> tools/claude-code/README.md:67:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:99:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:99:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:99:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:100:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:101:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:102:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> tools/pi/README.md:65:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-11-10: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM Flash failed its post-run checks on 2026-11-10; the first Sonnet attempt ran without the pinned Pi in the worktree · leak check clean over 985 files, 3841 commits, 12 rules.

Stage-2 call, 2026-11-10: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM Flash failed its post-run checks on 2026-11-10; the earlier Sonnet call ended with exit 1 before it changed code · leak check clean over 985 files, 3845 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +1 -1
> - `docs/how-it-works.md` +1 -1
> - `docs/orchestration.md` +1 -1
> - `plans/changes/verify-slots/measurements.md` +17 -0
> - `tests/test_verify_lock.py` +26 -26
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file.
> - `make verify` did not finish: make was stopped by the runner's step limit after 30 minutes
> ```
