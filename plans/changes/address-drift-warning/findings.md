---
title: "Findings — address-drift-warning"
category: findings
status: draft
implementation_status: partial
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-x2g9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — address-drift-warning

Stage-2 call, 2026-11-07: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 923 files, 3592 commits, 12 rules.

Stage-2 call, 2026-11-08: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 926 files, 3632 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 926 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 926 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 926 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 926 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 926 files, 3639 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 926 files, 3639 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 926 files, 3639 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 926 files, 3639 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 926 files, 3640 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 926 files, 3640 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 926 files, 3640 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 926 files, 3640 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 926 files, 3640 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 926 files, 3640 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 926 files, 3640 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 926 files, 3642 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 926 files, 3643 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 926 files, 3643 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 926 files, 3643 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 926 files, 3643 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 926 files, 3648 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3650 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +5 -4
> - `scripts/stage2_go.py` +4 -3
> - `tests/test_stage2_go_access.py` +4 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-6: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/address-drift-warning/stage2/attempts/address-drift-warning/attempt-1-20261108T142102303880Z-3bb4b6d9.md
> ```

Stage-2 call, 2026-11-08: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 926 files, 3654 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-3: no fixed line
> - L1-4: no fixed line
> - L1-5: no fixed line
> - L1-6: no fixed line
> - L1-7: no fixed line
> - L1-10: no fixed line
> - L1-11: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/address-drift-warning/stage2/attempts/address-drift-warning/attempt-2-20261108T142102303880Z-3bb4b6d9.md
> ```

Stage-2 call, 2026-11-08: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 926 files, 3657 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_stage2_go_access.py` +16 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 66 lines of this gate left out …]
> ........................................................................ [ 94%]
> ........................................................................ [ 96%]
> ........................................................................ [ 97%]
> ........................................................................ [ 99%]
> ...............................................                          [100%]
> =================================== FAILURES ===================================
> __________________ test_a_deadline_stop_names_the_round_limit __________________
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/address-drift-warning/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-989/popen-gw3...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-989/popen-gw3/test_a_deadline_stop_names_the0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10c33a3f0>
>
>     def test_a_deadline_stop_names_the_round_limit(world: World, monkeypatch) -> None:
>         """Criterion 12 (DL-B-14): a call stopped by the round deadline names that limit, not 45 minutes."""
>         _flash_next(world)
>         monkeypatch.setattr(stage2, "REVIEWER_MINUTES", 2 / 60)
>         world.script(
>             pi=[
>                 {"model": "deepseek-v4.1-flash", "exit": 1, "stderr": "Rate limited", "sleep": 0.5},
>                 {"model": "mimo-v2.6-flash", "stdout": rows(1, "M")},
>                 {"model": "mimo-v2.6-pro", "stdout": rows(1, "P"), "sleep": 10},
>             ]
>         )
>         assert world.run("review-loop") == 0
>         text = world.record().read_text(encoding="utf-8")
> >       stop = next(line for line in text.splitlines() if line.startswith("mimo-v2.6-pro failed:"))
> E       StopIteration
>
> tests/test_stage2.py:18571: StopIteration
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 29 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 29 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> review-loop: round 2 written to /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-989/popen-gw3/test_a_deadline_stop_names_the0/state/coding-harness/stage2/demo@ab4abd7d/loop.md: 1 rows from 1 of 2 members
> ----------------------------- Captured stderr call -----------------------------
> review-loop: Notice: flash_swarm [deepseek-v4.1-flash, mimo-v2.6-flash] differs from the three cheapest admitted models [deepseek-v4.1-flash, mimo-v2.6-flash, mimo-v2.6-pro] by anfragen_5h; the list stays as declared.
> deepseek-v4.1-flash: Rate limited
> review-loop: deepseek-v4.1-flash failed: pi call failed: exit 1 (Rate limited); the round time limit expired; no replacement starts
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=3064) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/address-drift-warning/tests/test_stage2.py:19000: DeprecationWarning: This process (pid=3110) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_deadline_stop_names_the_round_limit - Sto...
> 1 failed, 4853 passed, 17 skipped, 5 warnings in 1100.31s (0:18:20)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 32433 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/address-drift-warning/stage2/attempts/address-drift-warning/attempt-3-20261108T142102303880Z-3bb4b6d9.md
> ````

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3659 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3660 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model hy3 · leak check clean over 926 files, 3666 commits, 12 rules.
