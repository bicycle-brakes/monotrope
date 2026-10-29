---
title: "Findings — run-report"
category: findings
status: draft
implementation_status: none
date: 2026-10-28
created: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-o2yc
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — run-report

Stage-2 call, 2026-10-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 728 files, 2520 commits, 12 rules.

Stage-2 call, 2026-10-28: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 731 files, 2532 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `Makefile` +10 -1
> - `docs/WORKFLOW.md` +25 -1
> - `plans/changes/run-report/plan.md` +14 -14
> - `scripts/run_report.py` +627 -0
> - `tests/test_run_report.py` +575 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `scripts/run_report.py`, `tests/test_run_report.py`.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 53 lines of this gate left out …]
> ........................................................................ [ 89%]
> ........................................................................ [ 90%]
> ........................................................................ [ 92%]
> ........................................................................ [ 94%]
> ........................................................................ [ 96%]
> ........................................................................ [ 97%]
> ........................................................................ [ 99%]
> ...........                                                              [100%]
> =================================== FAILURES ===================================
> _____________ test_every_script_has_a_caller_or_a_declared_reason ______________
> [gw2] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/run-report/.venv/bin/python3
>
>     def test_every_script_has_a_caller_or_a_declared_reason() -> None:
>         """A tool without a caller cannot be told apart from a forgotten one.
>     
>         On 2026-08-14, nine of twenty-one scripts had none — and nowhere did it say
>         which of them were intentional. Since then the rule is: every script —
>         `*.py` as well as `*.sh` — stands either in a `run:` step (`ci.yml`, both
>         jobs) or in `ci_gates.OHNE_AUFRUFER` with a reason (RB-G3).
>     
>         `ci_gates.py` itself is the caller of the local runner; it counts as wired
>         as soon as `verify_all.sh` starts it.
>         """
>         from ci_gates import OHNE_AUFRUFER
>     
>         ci = CI_FILE.read_text(encoding="utf-8")
>         runner = RUNNER.read_text(encoding="utf-8")
>     
>         heimatlos = _heimatlose_namen([p.name for p in _scripts()], ci, runner, OHNE_AUFRUFER)
> >       assert not heimatlos, (
>             "Without a caller and without a reason:\n  "
>             + "\n  ".join(heimatlos)
>             + "\n\nEither a step in ci.yml or a line in ci_gates.OHNE_AUFRUFER."
>         )
> E       AssertionError: Without a caller and without a reason:
> E           run_report.py
> E         
> E         Either a step in ci.yml or a line in ci_gates.OHNE_AUFRUFER.
> E       assert not ['run_report.py']
>
> tests/test_ci.py:1525: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=32802) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/run-report/tests/test_stage2.py:16534: DeprecationWarning: This process (pid=32812) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
> 1 failed, 4097 passed, 17 skipped, 5 warnings in 508.97s (0:08:28)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 21748 earlier lines left out …]
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

Stage-2 call, 2026-10-29: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 733 files, 2536 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model cat-jam-free · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model longcat-2.5-preview-free · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: review-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 733 files, 2537 commits, 12 rules.

Stage-2 call, 2026-10-29: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 733 files, 2539 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - L1-1: no fixed line
> - L1-2: no fixed line
> - L1-3: no fixed line
> - L1-4: no fixed line
> - L1-5: no fixed line
> - L1-6: no fixed line
> - L1-7: no fixed line
> - L1-9: no fixed line
> - L1-10: no fixed line
> - L1-12: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/run-report/stage2/attempts/run-report/attempt-1-20261029T000254185643Z-617d0118.md
> ```

Stage-2 call, 2026-10-29: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 733 files, 2540 commits, 12 rules.

Stage-2 call, 2026-10-29: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 733 files, 2541 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `scripts/run_report.py` +35 -23
> - `tests/test_run_report.py` +103 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `scripts/run_report.py`, `tests/test_run_report.py`.
> - L1-6: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/run-report/stage2/attempts/run-report/attempt-1-20261029T002307262083Z-f1844ea4.md
> ```

Stage-2 call, 2026-10-29: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 733 files, 2543 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-6: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/run-report/stage2/attempts/run-report/attempt-2-20261029T002307262083Z-f1844ea4.md
> ```

Stage-2 call, 2026-10-29: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 733 files, 2543 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-6: tests/test_run_report.py::test_shebang_runner_is_matched_without_matching_wrapper: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/run-report/stage2/attempts/run-report/attempt-3-20261029T002307262083Z-f1844ea4.md
> ```

Stage-2 call, 2026-10-29: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 733 files, 2550 commits, 12 rules.

Stage-2 call, 2026-10-29: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 733 files, 2552 commits, 12 rules.

Stage-2 call, 2026-10-29: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 733 files, 2575 commits, 12 rules.

Stage-2 call, 2026-10-29: review-loop · endpoint opencode-go · model hy3 · leak check clean over 733 files, 2580 commits, 12 rules.

Loop attempt: 2026-10-29 — no round was written; the review-loop calls above consumed no stage; audit calls: 1

Notice: the data terms of deepseek-v4.1-flash expire on 2026-10-31 (2 days left).

Notice: the data terms of deepseek-v4-pro expire on 2026-10-31 (2 days left).
