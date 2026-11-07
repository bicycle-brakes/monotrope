---
title: "Findings — night-machine-facts"
category: findings
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-yql7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — night-machine-facts

Stage-2 call, 2026-11-06: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 910 files, 3355 commits, 12 rules.

## Draft validation — 2026-11-06

Drafted `spec.md` and `plan.md` against research and the reasoned interview
skip at base `fcbff4a3`. Class remains bounded; no design or ADR is due, no
maintainer answer was added, and no phase-2a finding rows were present.

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_interview_minimums.py --change night-machine-facts`: green; this change measured.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_criterion_ledger.py`: green, including the draft's not-yet-written tests.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_frontmatter_current.py`: green.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_research_handoff.py --change night-machine-facts`: explicitly exempt, no research-swarm/v2 evidence; not a measured swarm handoff.
- Local structural inspection: required headers, eight refuting cases and an
  empty `## Time used` section hold. Implementation tests have not been run;
  they do not exist yet.

`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at
this base. The plan follows the phase-3 prompt and existing plan form; the
absent validator was not reported green. Index regeneration, the full
registry/tracker check, document verification and the commit remain with the
runner. No files outside this change folder were changed.

Stage-2 call, 2026-11-06: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 913 files, 3357 commits, 12 rules.

> Attempt 1 (flash) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/orchestration.md` +31 -3
> - `plans/changes/night-machine-facts/plan.md` +7 -7
> - `scripts/machine_facts.py` +310 -0
> - `tests/test_machine_facts.py` +440 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_machine_facts.py`; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before `make verify`: `.venv/bin/ruff check` exited 1
> scripts/machine_facts.py:218:9: SIM105 Use `contextlib.suppress(run_report.SourceError)` instead of `try`-`except`-`pass`
>     |
> 216 |       changes = frozenset()
> 217 |       if worktree is not None:
> 218 | /         try:
> 219 | |             changes = frozenset(run_report.active_changes(worktree))
> 220 | |         except run_report.SourceError:
> 221 | |             pass  # attribution stays `not read`; readable rows still render
>     | |________________^ SIM105
> 222 |       try:
> 223 |           rows = run_report.parse_processes(run(["ps", "-axo", "pid,etime,command"]), changes)
>     |
>     = help: Replace with `contextlib.suppress(run_report.SourceError)`
>
> Found 1 error.
> ```

Stage-2 call, 2026-11-06: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 915 files, 3367 commits, 12 rules.

> Attempt 2 (flash-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/night-machine-facts/plan.md` +7 -7
> - `scripts/machine_facts.py` +4 -4
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 63 lines of this gate left out …]
> ........................................................................ [ 90%]
> ........................................................................ [ 91%]
> ........................................................................ [ 93%]
> ........................................................................ [ 94%]
> ........................................................................ [ 96%]
> ........................................................................ [ 97%]
> ........................................................................ [ 99%]
> ..........................................                               [100%]
> =================================== FAILURES ===================================
> _____________ test_every_script_has_a_caller_or_a_declared_reason ______________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/night-machine-facts/.venv/bin/python3
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
> E           machine_facts.py
> E         
> E         Either a step in ci.yml or a line in ci_gates.OHNE_AUFRUFER.
> E       assert not ['machine_facts.py']
>
> tests/test_ci.py:2663: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=18841) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/night-machine-facts/tests/test_stage2.py:18933: DeprecationWarning: This process (pid=18828) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
> 1 failed, 4848 passed, 17 skipped, 5 warnings in 1382.14s (0:23:02)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 31965 earlier lines left out …]
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

Stage-2 call, 2026-11-06: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 915 files, 3369 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model iceman-contributor-free · leak check clean over 915 files, 3372 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 915 files, 3373 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 917 files, 3441 commits, 12 rules.

Stage-2 call, 2026-11-06: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 917 files, 3443 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/orchestration.md` +1 -0
> - `plans/changes/night-machine-facts/plan.md` +13 -4
> - `plans/changes/night-machine-facts/research.md` +3 -10
> - `plans/changes/night-machine-facts/spec.md` +6 -2
> - `scripts/machine_facts.py` +12 -20
> - `tests/test_machine_facts.py` +118 -10
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-6: answered `not a test`, but the row is a code row; it needs a test that was red first
> - L1-7: answered `not a test`, but the row is a code row; it needs a test that was red first
> - L1-11: answered `not a test`, but the row is a code row; it needs a test that was red first
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/night-machine-facts/stage2/attempts/night-machine-facts/attempt-1-20261106T195640848113Z-30bc0d99.md
> ```

Stage-2 call, 2026-11-06: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 917 files, 3446 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/night-machine-facts/plan.md` +12 -2
> - `plans/changes/night-machine-facts/spec.md` +6 -1
> - `tests/test_machine_facts.py` +23 -0
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-4: tests/test_machine_facts.py::test_snapshot_is_local_and_read_only: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/night-machine-facts/stage2/attempts/night-machine-facts/attempt-2-20261106T195640848113Z-30bc0d99.md
> ```

Stage-2 call, 2026-11-07: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 917 files, 3455 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/night-machine-facts/plan.md` +10 -1
> - `tests/test_machine_facts.py` +32 -1
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed `tests/test_machine_facts.py`.
> - L1-5: answered `not a test`, but the row is a code row; it needs a test that was red first
> - L1-6: answered `not a test`, but the row is a code row; it needs a test that was red first
> - L1-7: answered `not a test`, but the row is a code row; it needs a test that was red first
> - L1-11: answered `not a test`, but the row is a code row; it needs a test that was red first
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/night-machine-facts/stage2/attempts/night-machine-facts/attempt-3-20261106T195640848113Z-30bc0d99.md
> ```

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 917 files, 3464 commits, 12 rules.
