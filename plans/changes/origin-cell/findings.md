---
title: "Findings — origin-cell"
category: findings
status: draft
implementation_status: partial
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-ywbh
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — origin-cell

Stage-2 call, 2026-11-07: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 923 files, 3580 commits, 12 rules.

Stage-2 call, 2026-11-08: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 926 files, 3621 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +8 -1
> - `plans/changes/origin-cell/plan.md` +9 -9
> - `scripts/stage2.py` +57 -0
> - `tests/test_stage2.py` +354 -16
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_stage2.py`.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ...........................F.....F.....                                  [100%]
> =================================== FAILURES ===================================
> _________ test_origin_workflow_assigns_provenance_to_the_orchestrator __________
> [gw3] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/origin-cell/.venv/bin/python3
>
>     def test_origin_workflow_assigns_provenance_to_the_orchestrator() -> None:
>         """Criterion 1. Planted fault: ownership or either causal meaning is dropped from the workflow."""
>         workflow = WORKFLOW.read_text(encoding="utf-8")
>         assert origin_workflow_problems(workflow) == []
>         for planted in (
>             workflow.replace("and that cell is the orchestrator's", "and that cell is the reviewer's", 1),
>             workflow.replace("`base` for a finding the review found", "`base` for a finding the repair caused", 1),
>             workflow.replace(
>                 "`fix-r<N>` for a finding that repair round `N` produced",
>                 "`fix-r<N>` for a finding the review found",
>                 1,
>             ),
>             workflow.replace(
>                 "the reviewer's Origin text is not a decision about provenance",
>                 "the reviewer's Origin text decides provenance",
>                 1,
>             ),
>         ):
> >           assert origin_workflow_problems(planted), planted[200:400]
> E           AssertionError: drafted-reviewed
> E             produced_by:
> E               kind: llm-session
> E               name: claude-code
> E               version: "2026-09-29"
> E             review:
> E               status: pending
> E               approved_by: null
> E               approved_at: null
> E             tags: [workflow, model-routing, agentic-
> E           assert []
> E            +  where [] = origin_workflow_problems('---\ntitle: "Workflow and model routing — phases and stages"\ncategory: governance\nstatus: current\ncreated: 2026-09... files despite good naming, add an LSP MCP\nserver — and only when that is not enough, think about a semantic index.\n')
>
> tests/test_stage2.py:11983: AssertionError
> _________________ test_origin_brake_survives_released_history __________________
> [gw6] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/origin-cell/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-826/popen-gw6...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-826/popen-gw6/test_origin_brake_survives_rel0/state'))
> capsys = <_pytest.capture.CaptureFixture object at 0x1087030e0>
>
>     def test_origin_brake_survives_released_history(world: World, capsys: pytest.CaptureFixture[str]) -> None:
>         """Criterion 8. Planted fault: a release or a taken-to-fixed transition resets the brake, or a rejected row counts."""
>         world.script(pi=[{"stdout": rows(1)}] * 2)
>         assert world.run("review-loop") == 0  # round 1: the free swarm
>         decide_record(world, status="taken — test_a")
>         set_round_origin(world, 1, "fix-r1")
>         world.write_findings(VERDICT)
>         assert world.run("release-loop") == 0  # round 1 is released history now
>         assert not world.record().exists()
>         world.script(pi=[{"stdout": rows(1)}] * 3)
> >       assert world.run("review-loop") == 0  # round 2: the Flash swarm
> E       AssertionError: assert 2 == 0
> E        +  where 2 = run('review-loop')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-826/popen-gw6...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-826/popen-gw6/test_origin_brake_survives_rel0/state')).run
>
> tests/test_stage2.py:12187: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 29 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 29 files, 2 commits, 1 rules, 1 prompt texts
> review-loop: round 1 written to /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-826/popen-gw6/test_origin_brake_survives_rel0/state/coding-harness/stage2/demo@4f8a59fa/loop.md: 2 rows from 2 of 2 members
> release-loop: 2 loop rows appended to plans/changes/demo/findings.md
> ----------------------------- Captured stderr call -----------------------------
> refused: taken rows are not repaired yet (L1-1, L1-2); run `repair` and make `make verify` green before the next round starts.
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_origin_workflow_assigns_provenance_to_the_orchestrator
> FAILED tests/test_stage2.py::test_origin_brake_survives_released_history - As...
> 2 failed, 37 passed in 15.48s
> ```

Stage-2 call, 2026-11-08: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 926 files, 3621 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/origin-cell/plan.md` +9 -9
> - `scripts/stage2.py` +7 -3
> - `tests/test_stage2.py` +25 -8
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `scripts/stage2.py`.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 72 lines of this gate left out …]
> =================================== FAILURES ===================================
> _____________ test_a_released_taken_row_also_holds_the_next_round ______________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/origin-cell/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-837/popen-gw2...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-837/popen-gw2/test_a_released_taken_row_also0/state'))
> capsys = <_pytest.capture.CaptureFixture object at 0x109b988c0>
>
>     def test_a_released_taken_row_also_holds_the_next_round(world: World, capsys: pytest.CaptureFixture[str]) -> None:
>         """Criterion 9. Planted fault: the repair check reads the record alone, not the released rows."""
>         world.write_record([("L1-1", "taken — test_a", "no")], state=loop_state(("free",)))
>         world.write_findings(VERDICT)
>         assert world.run("release-loop") == 0
>         capsys.readouterr()
> >       assert world.run("review-loop") == 2
> E       AssertionError: assert 1 == 2
> E        +  where 1 = run('review-loop')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-837/popen-gw2...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-837/popen-gw2/test_a_released_taken_row_also0/state')).run
>
> tests/test_stage2.py:19631: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 30 files, 2 commits, 1 rules, 1 prompt texts
> ----------------------------- Captured stderr call -----------------------------
> review-loop: Notice: flash_swarm [deepseek-v4.1-flash, mimo-v2.6-flash] differs from the three cheapest admitted models [deepseek-v4.1-flash, mimo-v2.6-flash, mimo-v2.6-pro] by anfragen_5h; the list stays as declared.
> review-loop: deepseek-v4.1-flash was asked again with the format reminder: the first answer was malformed
> review-loop: mimo-v2.6-flash was asked again with the format reminder: the first answer was malformed
> review-loop: deepseek-v4.1-flash failed: malformed finding output: the answer is empty; expected six-cell findings or exactly 'No finding.'; replaced by mimo-v2.6-pro
> review-loop: mimo-v2.6-pro was asked again with the format reminder: the first answer was malformed
> review-loop: mimo-v2.6-pro failed: malformed finding output: the answer is empty; expected six-cell findings or exactly 'No finding.'; no replacement is left on the ladder
> review-loop: mimo-v2.6-flash failed: malformed finding output: the answer is empty; expected six-cell findings or exactly 'No finding.'; no replacement is left on the ladder
> failed: deepseek-v4.1-flash failed: malformed finding output: the answer is empty; expected six-cell findings or exactly 'No finding.'; mimo-v2.6-flash failed: malformed finding output: the answer is empty; expected six-cell findings or exactly 'No finding.'; mimo-v2.6-pro failed: malformed finding output: the answer is empty; expected six-cell findings or exactly 'No finding.'
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=76056) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/origin-cell/tests/test_stage2.py:19357: DeprecationWarning: This process (pid=76056) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_a_released_taken_row_also_holds_the_next_round
> 1 failed, 4883 passed, 17 skipped, 5 warnings in 1076.37s (0:17:56)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 32405 earlier lines left out …]
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

Stage-2 call, 2026-11-08: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 926 files, 3622 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/stage2.py` +7 -4
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - Runner cheap checks before `make verify`: `.venv/bin/python3 -m pytest -q -n auto` exited 1
> bringing up nodes...
> bringing up nodes...
>
> ................................F.......                                 [100%]
> =================================== FAILURES ===================================
> _________________ test_origin_brake_survives_released_history __________________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/origin-cell/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-846/popen-gw1...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-846/popen-gw1/test_origin_brake_survives_rel0/state'))
> capsys = <_pytest.capture.CaptureFixture object at 0x1066bf5f0>
>
>     def test_origin_brake_survives_released_history(world: World, capsys: pytest.CaptureFixture[str]) -> None:
>         """Criterion 8. Planted fault: a release or a taken-to-fixed transition resets the brake, or a rejected row counts."""
>         world.script(pi=[{"stdout": rows(1)}] * 2)
>         assert world.run("review-loop") == 0  # round 1: the free swarm
>         decide_record(world, status="taken — test_a")
>         set_round_origin(world, 1, "fix-r1")
>         world.write_findings(VERDICT)
>         assert world.run("release-loop") == 0  # round 1 is released history now
>         assert not world.record().exists()
>         world.script(pi=[{"stdout": rows(1)}] * 3)
> >       assert world.run("review-loop") == 0  # round 2: the Flash swarm
> E       AssertionError: assert 2 == 0
> E        +  where 2 = run('review-loop')
> E        +    where run = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-846/popen-gw1...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-846/popen-gw1/test_origin_brake_survives_rel0/state')).run
>
> tests/test_stage2.py:12204: AssertionError
> ----------------------------- Captured stdout call -----------------------------
> INFO  (1):
>   - leak check clean: 29 files, 2 commits, 1 rules, 1 prompt texts
> INFO  (1):
>   - leak check clean: 29 files, 2 commits, 1 rules, 1 prompt texts
> review-loop: round 1 written to /private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-846/popen-gw1/test_origin_brake_survives_rel0/state/coding-harness/stage2/demo@16caff8a/loop.md: 2 rows from 2 of 2 members
> release-loop: 2 loop rows appended to plans/changes/demo/findings.md
> ----------------------------- Captured stderr call -----------------------------
> refused: taken rows are not repaired yet (L1-1, L1-2); run `repair` and make `make verify` green before the next round starts.
> =========================== short test summary info ============================
> FAILED tests/test_stage2.py::test_origin_brake_survives_released_history - As...
> 1 failed, 39 passed in 14.35s
> ```

Stage-2 call, 2026-11-08: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash attempts and one Sonnet attempt each failed one test; attempt 3 saved at refs/stage2/attempts/origin-cell/orchestrator-saved-20261108 · leak check clean over 926 files, 3628 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 926 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 926 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 926 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 926 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 926 files, 3638 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 926 files, 3639 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 926 files, 3639 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 926 files, 3639 commits, 12 rules.

Stage-2 call, 2026-11-08: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 926 files, 3639 commits, 12 rules.

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

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 926 files, 3648 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3655 commits, 12 rules.

Stage-2 call, 2026-11-08: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 926 files, 3694 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3696 commits, 12 rules.

Stage-2 call, 2026-11-09: review-loop · endpoint opencode-go · model hy3 · leak check clean over 926 files, 3702 commits, 12 rules.

Stage-2 call, 2026-11-09: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3710 commits, 12 rules.

Stage-2 call, 2026-11-09: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 926 files, 3716 commits, 12 rules.

Stage-2 call, 2026-11-09: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3740 commits, 12 rules.

Stage-2 call, 2026-11-09: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3761 commits, 12 rules.

## Phase 6 — Codex, 2026-11-09

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | — | scripts/stage2.py:3467–3470 | An earlier phase-6 row with Status `taken — test_a` and Origin `invalid` escapes validation once a newer phase-6 block exists, even if that block says `No finding.`. Reproduced with the source functions: `origin_refusal(None, text)` returns `None`, while `repair_targets` still selects that earlier row with no waiting decision. Consequently, `repair` can call a model to repair an accepted finding whose provenance remains invalid. Validate outstanding repair targets across phase-6 blocks before allowing effects. [Acceptance criterion 2] | Codex | accepted limit — follow-up bead coding-harness-3h96 (maintainer 2026-11-09: PR now, MAJOR as follow-up bead) | — |

The answer was not only six-cell rows; what is not one is kept below as it came.

> Guard evidence: tests/test_stage2.py::test_uppercase_accepted_status_holds_invalid_origin — fault: `STAGE2_PLANT_FAULT=1` replaces the real `accepted_row` predicate with a case-sensitive version, allowing uppercase `TAKEN` with invalid provenance to escape validation — catches without switch: yes; if that defect exists in the implementation, the unchanged test exercises uppercase `TAKEN` through all four verbs and requires an invalid-Origin refusal, unchanged findings and record bytes, and no model calls.

Phase 6 verdict: codex 01a1c182-0b6b-74e3-9660-581039290b9c, 2026-11-09
Reviewer session: codex 01a1c182-0b6b-74e3-9660-581039290b9c — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-09

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MINOR | SPEC | base | `plans/changes/origin-cell/spec.md:4`, `plan.md:4`, `decisions.md:4`, `research.md:4`, `findings.md:5`, and the regenerated rows at `plans/INDEX.md:267-271` | All five artefacts still declare `implementation_status: none` and the index prints `none` beside each row, although the branch carries the implemented validator, the new fixtures and the nine ledger regressions, and `plan.md` "Time used" records the implement attempt as `accepted`; `plans/_README.md:50` and `docs/WORKFLOW.md:322-325` define the field as moving when the code moves, and sibling in-flight changes read `partial`. A maintainer scanning the index reads that no code exists where it does. | deepseek-v4.1-flash | fixed — orchestrator hand edit 3b445589 | no | agree |
| L1-2 | MAJOR | MAINT | base | `plans/changes/origin-cell/research.md:13` (frontmatter) and the retained skeleton text at `research.md:19-24` | The file declares `provenance: human-written` and omits `produced_by:`/`review:`, yet its body is a model-written Stage-2 exploration naming `glm-5.3-flash`, and it still says "this file is empty until it has run"; the note it keeps says whoever fills it with a language model must set `ai-drafted-reviewed` and add `produced_by:` and `review:`, the class whose `review_required` is `true` while `human-written` is `false`. A change whose subject is a trustworthy provenance cell mis-declares its own provenance and drops the review obligation. | deepseek-v4.1-flash | fixed — orchestrator hand edit 3b445589 | no | agree |
| L1-3 | MINOR | SPEC | base | `docs/WORKFLOW.md:1509-1512` against `scripts/stage2.py:3982-3995` | The new sentence says `release-loop` refuses while a taken or fixed row carries an invalid Origin, but `release-loop --restart` and `release-loop --stage-failed` return before `release()`'s check and still append to `findings.md` (`restart_loop`, `stage2.py:3978`) or write the loop record (`retire_stage`, `stage2.py:3947`); the spec scopes the refusal to "ordinary `release-loop`" (criterion 2) and the workflow does not, so the documented guarantee is wider than the enforced one. | deepseek-v4.1-flash | fixed — not a test — Workflow scopes refusal to ordinary release-loop and documents both Origin-check exceptions. | no — not a test | agree |
| L1-4 | MAJOR | MAINT | base | scripts/stage2.py:3437 (`origin_refusal`); plans/changes/attempt-diagnostics/findings.md:54; plans/changes/malformed-answer-retry/findings.md:101 | The guard reads every released block and phase-6 table of the selected change, and this tree already holds rows it rejects: the released row L2-3 of attempt-diagnostics carries Origin `impl` with a `taken` status, and the released row L1-12 of malformed-answer-retry carries Origin `diff reading` with a `fixed` status — both are still draft changes with more such rows (L3-2, L3-3 with Origin `round 3`). Pointing `repair`, `review`, `release-loop` or `review-loop` at either refuses before any call or write, so the only way past it is hand-editing released history, which this change performs no migration for; neither the refusal, the new workflow paragraph nor any test tells the orchestrator that releases written before this change are already affected. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_legacy_released_origin_does_not_hold_verbs | yes — tests/test_stage2.py::test_legacy_released_origin_does_not_hold_verbs | agree |
| L1-5 | MAJOR | MAINT | base | docs/WORKFLOW.md:1511; scripts/stage2.py:3815 (`release`), :2931 (`record_identity`); tests/test_stage2.py (`test_invalid_origin_holds_release_reconciliation`) | The remedy the change adds to the workflow — correct the cell and run the verb again — does not hold on the release-retry path it was written for: `record_identity` hashes the first seven cells of every record row, Origin included, and `record_digest` hashes the whole record, so correcting an invalid Origin in a record that already has a released block destroys the match the reconciliation branch needs. The retry then refuses a second time with the overlap refusal that hands the work back to the maintainer for manual reconciliation, where the uncorrected state would have been reconciled automatically. The new test asserts only the first refusal and never runs the documented second attempt after the cell is corrected. | mimo-v2.6-flash | fixed — tests/test_stage2.py::test_invalid_origin_holds_release_reconciliation | yes — tests/test_stage2.py::test_invalid_origin_holds_release_reconciliation | agree |
| L1-6 | MINOR | MAINT | base | docs/WORKFLOW.md:1506-1512; scripts/stage2.py:3982-3988 (`release_loop`), :3951 (`restart_loop`), `retire_stage` | The workflow sentence names `release-loop` as one of four verbs that refuse while an accepted row carries any other value, but two of its forms return before `release` is ever entered: `release-loop --restart` goes straight into `restart_loop` and appends a `Loop restarted:` line, and `release-loop --stage-failed` goes into `retire_stage` and writes the record, both with the invalid Origin still in place. The paragraph carries no qualifier, so a maintainer who reads only it expects every `release-loop` invocation to refuse. | mimo-v2.6-flash | fixed — not a test — Workflow explicitly exempts --restart and --stage-failed from Origin validation. | no — not a test | agree |
| L1-7 | MINOR | MAINT | base | plans/changes/origin-cell/research.md:12, :21-24, :27 | The file ships `provenance: human-written` with no `produced_by:` and no `review:` although its body is a Stage-2 model run (its own audit line: explore, model glm-5.3-flash) and its callout says in so many words that whoever fills the file with a language model must set `ai-drafted-reviewed` and add both fields. Every other change's research.md in this tree does; this one refutes its own instruction and claims a provenance nobody can defend. | mimo-v2.6-flash | fixed — orchestrator hand edit 3b445589 | no | agree |
| L1-8 | MINOR | SPEC | base | plans/changes/origin-cell/plan.md (Build sequence, step 4); tests/test_stage2.py:8143-8151; scripts/stage2.py:3422 (`accepted_row`) | Step 4 of the plan promises the ledger tests cover "status case handling", but every status the new tests plant is lowercase (`taken — test_a`, `fixed — tests/test_x.py::test_y`), and no test anywhere feeds a non-lowercase accepted Status such as `TAKEN` through the four verbs. Deleting the `.lower()` from `accepted_row` — the read on which this refusal fires at all — would turn the case-insensitivity off and leave the whole suite green. | mimo-v2.6-flash | fixed — guard test — tests/test_stage2.py::test_uppercase_accepted_status_holds_invalid_origin | yes — guard test — tests/test_stage2.py::test_uppercase_accepted_status_holds_invalid_origin | agree |
| L2-1 | MAJOR | SPEC | fix-r1 | docs/WORKFLOW.md:1540 vs scripts/stage2.py:2931 (`record_identity`) | The record-identity contract in code changed to exclude the Origin cell (`row[:3] + row[4:7]`), but the release-loop section of the workflow document still describes the identity hash as covering "the first seven cells of each record row, excluding Status and Broke a test" — which includes Origin — so the governing documentation no longer says what the identity is; the change's Definition of Done promises documentation moved with the code and only the row-decision paragraph was updated, and no test pins this sentence (demonstrable: correcting Origin alone changes the digest but preserves identity, contradicting the documented cell set). | glm-5.3-flash | fixed — not a test — docs/WORKFLOW.md now describes identity excluding Origin and compatibility with earlier identities. | no — not a test | agree |
| L2-2 | MINOR | MAINT | fix-r1 | scripts/stage2.py:2931 (`record_identity`), test_stage2.py origin tests | Reconciliation with already-released history regresses silently: a block released before this change stores an identity computed with the Origin-including formula, which the recomputed identity can now never match, so a crash leftover whose record was afterwards edited only in repair marks or the stage snapshot — a case that reconciled in place before — now falls through to the "no phase-6 verdict line after the last release" refusal instead; the new tests generate legacy blocks with the new formula (released_cells/ `release_block`), so this legacy path is unexercised, and the workflow change only documents that legacy Origin values are never re-checked, not that legacy identity lines cannot match. | glm-5.3-flash | fixed — tests/test_stage2.py::test_legacy_release_identity_reconciles_crash_leftover | yes — tests/test_stage2.py::test_legacy_release_identity_reconciles_crash_leftover | agree |
| L3-1 | MINOR | MAINT | base | plans/changes/origin-cell/decisions.md (Q-1) vs scripts/stage2.py `origin_refusal`/`accepted_row` | The decision record states the runner "refuses a taken row whose Origin is neither `base` nor `fix-r<N>`", but the implementation and spec cover both `taken` and `fixed` accepted rows (`accepted_row` matches `taken`/`fixed`, and `origin_refusal` uses it); a maintainer reading only the decision could wrongly assume `fixed` rows bypass the check. | hy3 | fixed — not a test — clarified the decision context that accepted rows include both taken and fixed statuses; ruff checks passed and all 35 ledger test cases passed | no — not a test | disagree — The decision faithfully records the maintainer’s answer and does not exempt fixed rows; the spec explicitly defines fixed rows as accepted. No contradictory behavior follows. |
| L4-1 | BLOCKER | SPEC | fix-r1 | scripts/stage2.py, `origin_refusal` (phase-6 rows from `findings_rows`) | The check re-scans every phase-6 table in findings.md on all four verbs, including rows of rounds released long before this change, while the workflow text promises "already released history is never re-checked, including legacy rows released before this check existed" and the spec detail promises legacy rows (it names attempt-diagnostics and malformed-answer-retry) "never block a verb". A pre-existing change whose decided phase-6 rows carry reviewer-supplied Origins such as `impl` or `scope` (attempt-diagnostics' own F-1 and F-2 rows, status `fixed`) now refuses at review-loop, review, release-loop and repair, and the only way past is editing released history, which the spec's protected areas forbid. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_legacy_released_origin_does_not_hold_verbs | yes — tests/test_stage2.py::test_legacy_released_origin_does_not_hold_verbs | agree |
| L4-2 | MAJOR | SPEC | fix-r2 | scripts/stage2.py, `release` reconciliation branch (`released_identity` vs `record_identity`) | The documented remedy for an invalid Origin — correct the cell and run the verb again — defeats the compatibility path added in the same block. A crash-leftover release written before this change carries the earlier identity, which hashes the Origin cell; correcting the cell (the only remedy, since the Origin check refuses first) makes neither the new identity nor the accepted earlier formula match, so the retry passes the Origin check and is then refused at a later gate (no verdict after the leftover release, then row overlap with "the maintainer must reconcile the extended record"), never reconciling the leftover block and record that this branch exists to clean up. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_invalid_origin_holds_release_reconciliation | yes — tests/test_stage2.py::test_invalid_origin_holds_release_reconciliation | agree |
| L4-3 | MINOR | MAINT | base | tests/test_stage2.py, the new origin test block | The workflow's stated exemption — `release-loop --restart` and `release-loop --stage-failed` do not check Origin — holds only because those flags dispatch to `restart_loop`/`retire_stage` before the checked `release`, and no test pins that boundary; a refactor routing either flag through `release` would silently contradict the documented contract while every new test stays green. | mimo-v2.6-pro | fixed — tests/test_stage2.py::test_origin_release_controls_keep_distinct_validation_scopes | yes — tests/test_stage2.py::test_origin_release_controls_keep_distinct_validation_scopes | agree |

Rounds run: 4

Record digest: sha256:276545e5296421f03b49094f2e4c49002ae9726afc91358d07c10351bebd06ae

Record identity: sha256:b46224e0932437fba26772cd07afa33633f91ba7994477d2e5ed516def67ac1d

Loop state: {"availability": {"checked_at": "2026-11-08T13:34:51+00:00", "failed": {"crouton-alpha-free": "pi call failed: exit 1: opencode-go API error (403): {\"type\":\"RegionError\",\"message\":\"This model is not available in your country\"}", "glm-5.2": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated. Use mimo-v2.6-pro instead.\"}"}, "reachable": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "hy4": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured)", "gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured)", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured)", "minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured)", "qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured)", "qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured)", "grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free)", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": []}, "consumed": ["flash", "rung:glm-5.3-flash", "rung:hy3", "rung:mimo-v2.6-pro"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "crouton-alpha-free", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "pulse-alpha-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "crouton-alpha-free", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-08T13:28:00+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1794144478921, "etag": "W/\"2536099d28f32505b4840b309f9262c7\"", "lastModified": 1793973242000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "crouton-alpha-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 270000, "name": "Crouton Alpha Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": [], "overlay": ["beam-free", "claude-haiku-5-5", "crouton-alpha-free", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}, {"date": "2026-11-06", "id": "iceman-contributor-free", "reason": "New in the live Go catalog on 2026-11-06 and picked as the whole free swarm by prepare-loop; \"contributor\" ids on Go have meant that request data may be used for training, and the maintainer's decision of 2026-10-17 (question Q-12) keeps such models off. The Go page's privacy table, read 2026-11-06, confirms it: 'Iceman Contributor Free | Yes | Not ZDR'. A bridge until one central per-use-case model policy exists (bead coding-harness-k0ub with coding-harness-wq1m); maintainer, 2026-11-06, morning question Q-M9, option A."}, {"date": "2026-11-06", "id": "cat-jam-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it, so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}, {"date": "2026-11-06", "id": "longcat-2.5-preview-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it (only LongCat-2.0), so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": [], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "rungs": ["glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: paid models skipped: qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured); gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured); minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured); qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured); qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured); grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor.
> longcat-2.0 was asked again with the format reminder: the first answer was malformed
> longcat-2.0 failed: /Users/mikypiky/coding-harness/.claude/worktrees/origin-cell/tools/pi/pi was stopped by the round time limit of 45 minutes (806 seconds were left for this call); the round time limit expired; no replacement starts
> From longcat-2.0:
> longcat-2.0's first answer, which was not in the required format:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> From glm-5.3-flash:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> Review complete. I verified the origin-refusal wiring at all four verbs, the reconciliation/identity change, the brake interaction, the test fixtures, and the workflow documentation.
> 
> Notice: the data terms of longcat-2.0 expire on 2026-11-16 (7 days left).
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (7 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (7 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (7 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (7 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (7 days left).
> From hy3:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> After a thorough review of the implementation diff against the spec (`plans/changes/origin-cell/spec.md`), the decision record, the `docs/WORKFLOW.md` additions, and the test suite, the core logic is sound:
> - `origin_refusal` is wired at all four boundaries (`review_loop` before model calls, `review` before the Codex call, `release` before the reconciliation rewrite/removal, `repair` after the `waiting` check) and correctly bypasses `--restart`/`--stage-failed` (those route to `restart_loop`/`retire_stage`, never through `release`).
> - `record_identity` correctly excludes Origin by default and offers the legacy include-origin formula for reconciliation; `release_block` writes the new identity; both old (include) and new (exclude) released identities reconcile.
> - The regex `base|fix-r[1-9][0-9]*` matches the documented vocabulary and rejects `fix-r`, `fix-r0`, `fix-r01`, `FIX-R1`, `BASE`, etc.
> - Phase-6 rows become accepted via orchestrator decision then `repair`, so the phase-6 branch of `origin_refusal` is genuinely reachable and not dead code.
> The one concrete, defensible discrepancy I can demonstrate is a doc/scope inconsistency in the change's own artifacts.
> 
> Notice: the data terms of longcat-2.0 expire on 2026-11-16 (7 days left).
> Notice: the data terms of glm-5.3-flash expire on 2026-11-16 (7 days left).
> Notice: the data terms of qwen3.8-flash expire on 2026-11-16 (7 days left).
> Notice: the data terms of gpt-6-luna expire on 2026-11-16 (7 days left).
> Notice: the data terms of claude-haiku-5-5 expire on 2026-11-16 (7 days left).
> Notice: the data terms of minimax-m3 expire on 2026-11-16 (7 days left).

<!-- End of released loop record -->

Stage-2 call, 2026-11-09: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 926 files, 3761 commits, 12 rules.
