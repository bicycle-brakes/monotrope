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
owner: framework-architect
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

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model hy3 · leak check clean over 917 files, 3487 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model hy3 · leak check clean over 917 files, 3493 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 917 files, 3499 commits, 12 rules.

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 917 files, 3505 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model hy4-preview · leak check clean over 917 files, 3517 commits, 12 rules.

Stage-2 call, 2026-11-07: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 917 files, 3527 commits, 12 rules.

## Phase 6 — Codex, 2026-11-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MAJOR | SPEC | Phase 6 | scripts/machine_facts.py:199,227 | Empty or malformed successful command output, such as `unexpected data\n`, becomes `0` registered worktrees or `none matched` jobs. Both cases were reproduced against the source functions. An unreadable table must produce a source-specific `not read`, preserving independent fields. [Acceptance criterion 6] | Codex | fixed — tests/test_machine_facts.py::test_malformed_command_tables_are_not_read | — |
| F6-2 | MINOR | SPEC | Phase 6 | scripts/machine_facts.py:81 | For a worktree whose directory name ends in whitespace, `answer.strip()` removes part of the actual Git-reported path. Resolution then fails or selects an existing neighbouring directory, losing the readable worktree count or reporting another filesystem's disk space. Preserve path characters when removing Git's output terminator. [Acceptance criteria 2 and 4] | Codex | fixed — tests/test_machine_facts.py::test_worktree_resolution_preserves_trailing_space | — |

Phase 6 verdict: codex 01a1b631-5d3d-7270-9d7d-a92e308d0f81, 2026-11-07
Reviewer session: codex 01a1b631-5d3d-7270-9d7d-a92e308d0f81 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | MAINT | base | plans/changes/night-machine-facts/research.md:1-30 | The research file still declares `provenance: human-written` and carries neither `produced_by:` nor `review:`, although its body is a model's appended exploration and the note left standing in the file demands `ai-drafted-reviewed` with both fields for exactly that case; the skeleton lines "this file is empty until it has run" and the instruction blockquote also remain above the finished text, so a reader is told the file is unfinished and human-written at the same time. | deepseek-v4.1-flash | fixed — not a test — Corrected research provenance, added producer and pending review, removed stale skeleton notices. | no — not a test | agree |
| L1-2 | MAJOR | SPEC | base | plans/changes/night-machine-facts/plan.md:106-111 and scripts/ci_gates.py:129 | The plan forbids edits to "gate definitions", yet the change adds a `machine_facts.py` entry to `scripts/ci_gates.py`'s `OHNE_AUFRUFER`; the plan's steps, its file list and the spec's "Code, tests and usage move together" sentence name only the script, its test and the doc page, so the delivered file set is wider than the change describes and the plan's own boundary is broken unnoticed. | deepseek-v4.1-flash | fixed — orchestrator hand edit 1e2de53c: plan.md records the OHNE_AUFRUFER entry as the required exception (Q-M1) | no | agree |
| L1-3 | MAJOR | SPEC | base | scripts/machine_facts.py:70-100 and tests/test_machine_facts.py:335-349 | The free-disk field is made to depend on `git rev-parse`: when that one call fails, the field reads `not read (worktree: not identified)` although `os.statvfs` on the invoking directory would still answer, so a single failed source removes an independent fact — the case criterion 6 names as a refutation — and the test fixes that coupling as intended behaviour. | deepseek-v4.1-flash | fixed — tests/test_machine_facts.py::test_sources_fail_independently_without_becoming_a_gate | yes — tests/test_machine_facts.py::test_sources_fail_independently_without_becoming_a_gate | agree |
| L1-4 | MAJOR | MAINT | base | tests/test_machine_facts.py:372-434 | The read-only proof watches the wrong directory for bytecode: the subprocess runs the repository's own `scripts/machine_facts.py`, so a lost `sys.dont_write_bytecode` would leave `__pycache__` beside the repository's scripts, while the test compares only the temporary worktree; its `sys.dont_write_bytecode` assertion runs after `machine_facts` and `run_report` were imported, and both set that flag themselves, so neither assertion can go red for the fault criterion 7 names. | deepseek-v4.1-flash | fixed — not a test — Strengthened the read-only test to watch scripts bytecode and check the flag before helper imports. | no — not a test | agree |
| L1-5 | MINOR | MAINT | base | docs/orchestration.md:62-88 and 118-131 | The new night-start step is described in prose but never entered in the page's "Stated, enforced, planned" table, which gives every other rule its standing; a reader of that table finds no machine-facts row and cannot tell the step is a hand-kept practice rather than an enforced one. | deepseek-v4.1-flash | fixed — orchestrator hand edit 1e2de53c: docs/orchestration.md table row for the machine-facts step | no | disagree — The display and recording instructions already establish manual practice; no acceptance criterion requires a separate table entry. |
| L1-6 | MINOR | MAINT | longcat-2.0 | plans/changes/night-machine-facts/research.md frontmatter and the blockquote under the title | The frontmatter still says `provenance: human-written` with no `produced_by:` and no `review:`, while the file carries the exploration prose drafted by a language model; the file's own notice and the provenance rules require `ai-drafted-reviewed` plus `produced_by:` and `review:` once a model fills it, so a maintainer reads a false provenance claim. | longcat-2.0 | fixed — not a test — Same provenance correction as L1-1. | no — not a test | agree |
| L1-7 | MINOR | SPEC | longcat-2.0 | plans/changes/night-machine-facts/plan.md "Boundaries and route" vs scripts/ci_gates.py | The plan says no edits to gate definitions, but the diff adds an `OHNE_AUFRUFER` entry to `scripts/ci_gates.py`; the plan lists no such step and records no exception, so a maintainer auditing the pull request against the plan finds a file the plan protects modified with no note. | longcat-2.0 | fixed — orchestrator hand edit 1e2de53c: same as L1-2 | no | agree |
| L1-8 | MINOR | MAINT | longcat-2.0 | plans/changes/night-machine-facts/plan.md step 5 vs tests/test_machine_facts.py | Step 5 promises a test matrix covering timeouts and malformed values, but the new test file has no timeout case; its docstring delegates the two-second bound to `tests/test_run_report.py`, so the plan's promised case is absent from the change's own tests. | longcat-2.0 | fixed — tests/test_machine_facts.py::test_timed_out_sources_preserve_independent_facts | yes — tests/test_machine_facts.py::test_timed_out_sources_preserve_independent_facts | agree |
| L1-9 | MINOR | MAINT | longcat-2.0 | scripts/machine_facts.py `worktree_records` | The docstring says `-z` makes a path with a newline unable to split a record, but the parser splits each NUL-separated chunk on newlines and strips lines; a worktree path containing a newline is split, and a path whose first character is a newline loses its `worktree ` line (stripped to `worktree`), so the count can be wrong. The test only covers internal whitespace. | longcat-2.0 | fixed — tests/test_machine_facts.py::test_worktree_paths_preserve_newlines | yes — tests/test_machine_facts.py::test_worktree_paths_preserve_newlines | agree |
| L1-10 | MINOR | SPEC | free-swarm · glm-5.3-flash | scripts/machine_facts.py `jobs_field` (≈ line 277) | With the shared runner definitions unavailable (`run_report.stage2 is None`) and an otherwise readable `ps` table whose rows match nothing, the jobs block prints the "runner recognition: not read" note and immediately below it "none matched" — the `none` clause is then false for runner work, because stage2-style invocations cannot be recognized at all in that state; spec criterion 5 names exactly this refutation ("runner recognition claims `none` when its definitions are gone"). A test with an empty-frozenset verb set, `stage2 is None` and a ps table with no verification rows demonstrates it. | glm-5.3-flash | fixed — tests/test_machine_facts.py::test_missing_runner_definitions_never_claim_none | yes — tests/test_machine_facts.py::test_missing_runner_definitions_never_claim_none | agree |
| L1-11 | MINOR | MAINT | free-swarm · glm-5.3-flash | scripts/ci_gates.py:129 (`OHNE_AUFRUFER`) vs plan.md "Boundaries and route" | The plan's boundary text forbids edits to "gate definitions", yet the diff also edits `scripts/ci_gates.py`. The edit itself is forced and justified — `tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason` (already shown red in the recorded attempt 2) requires every new script to carry either a `ci.yml` step or an `OHNE_AUFRUFER` reason, and the entry documents why no CI checkout can stand in — but neither spec ("Protected areas") nor plan anticipate or record this mandatory registry edit, so a maintainer reading the boundaries alone would call the diff out of bounds; the records should name the registry (or state it is not a gate definition) instead of the diff silently widening its own boundary. | glm-5.3-flash | fixed — orchestrator hand edit 1e2de53c: same as L1-2 | no | agree |
| L1-12 | MINOR | SPEC | free-swarm · glm-5.3-flash | tests/test_machine_facts.py module docstring vs plan.md step 5 | Plan step 5 promises "timeouts" as part of this change's test matrix, but no test in `tests/test_machine_facts.py` exercises a timeout on any swappable source: the docstring defers the two-second bound to `tests/test_run_report.py` and the failure cases here use injected `SourceError`s only. The deferral is defensible for the unchanged `run_command` bound itself, yet the coordination machine_facts depends on — every swappable source passing through that bounded runner, so no hung subprocess can stall a snapshot — is what spec criterion 6 ("hangs on an unbounded subprocess") asks to be proven, and it is not shown by any test in the change. | glm-5.3-flash | fixed — tests/test_machine_facts.py::test_timed_out_sources_preserve_independent_facts | yes — tests/test_machine_facts.py::test_timed_out_sources_preserve_independent_facts | agree |
| L2-1 | MAJOR | MAINT | implementation | scripts/machine_facts.py — collect_snapshot (disk/swap/worktree/jobs and resolve_worktree wrapped in `except Exception`) | Each field is caught by a bare `except Exception`, so an unexpected error (a future run_report API break, a typo, an attribute error) is relabelled as `not read (... internal error: <Type>)`. The tool's only output is the block, so a real defect in a reading path is indistinguishable from a benign missing source and leaves no traceback; a maintainer debugging a silently-wrong night-start block cannot tell a bug from an unavailable fact. | hy3 | rejected — the label 'internal error: <Type>' already separates a code fault from a missing source, and spec criterion of a block that always renders forbids a traceback in it; a stderr trace is a new guarantee outside this change |  | disagree — The diagnostic explicitly identifies an internal error; preserving independent readings and exiting zero does not demonstrate a correctness fault. |
| L2-2 | MINOR | MAINT | implementation | scripts/machine_facts.py — swap_field(run, proc_dir) | swap_field overloads the name `proc_dir`: `None` selects macOS while a `Path` selects Linux, the opposite of the `proc_dir` parameter of collect_snapshot/main where `None` means "auto-detect platform". The platform branch lives only in collect_snapshot's `where = proc_dir if proc_dir is not None else (None if darwin else Path("/proc"))`, far from the function that branches on it, so a caller passing `proc_dir=None` to swap_field directly gets macOS, not auto-detect. | hy3 | rejected — accepted style limit named in the PR: the parameter name is local and collect_snapshot is the only caller |  | disagree — The helper explicitly documents its source-selection convention, and its caller supplies the correct platform selection. |
| L2-3 | MINOR | SPEC | docs + implementation | docs/orchestration.md "Machine facts at the start of a night run" and scripts/machine_facts.py jobs_field | The docs promise "each row carries process id, elapsed time, verb and change attribution" under `running jobs:`, but jobs_field can also emit a non-process meta line `runner recognition: not read (runner verb definitions unavailable)` (and a bare `not read (ps: ...)` on ps failure) under the same header; a parser or maintainer expecting only PID-bearing rows meets a row with no PID or verb, described only obliquely as "when the shared runner definitions are unavailable". | hy3 | fixed — orchestrator hand edit 5e76e95a, b41f928b | no | agree |
| L2-4 | MINOR | MAINT | change artefacts | plans/changes/night-machine-facts/{findings,decisions,plan,spec,research}.md frontmatter | The change's own artefacts disagree on `owner` (findings.md says "Data Architect", the rest "framework-architect") and on `updated` (findings.md 2026-11-07 vs the change's 2026-11-06 date); a maintainer auditing the PR sees inconsistent provenance and ownership across one change's files. | hy3 | fixed — orchestrator hand edit 5e76e95a, b41f928b | no | disagree — Different update dates are expected after individual edits, and no requirement establishes identical ownership across these artifacts. |
| L3-1 | MINOR | SPEC | diff | scripts/machine_facts.py:256 (`collect_snapshot`/`disk_field`) | The free-disk figure is read from the invoking directory, not from the worktree root the script resolves: `collect_snapshot` passes `cwd` into `disk_field`, although the plan's step 3 names `os.statvfs(worktree)` on the worktree resolved by read-only Git in step 2, and the rendered label claims "filesystem of the invoking worktree". Run from a subdirectory that is a separate mount, the block reports that mount's space under the worktree's label — the wrong-filesystem case criterion 2 refutes; `test_disk_reports_worktree_available_space` only ever stats the directory it also uses as `cwd`, so the two paths are never different in the fixtures. | mimo-v2.6-pro | fixed — tests/test_machine_facts.py::test_disk_reports_worktree_available_space | yes — tests/test_machine_facts.py::test_disk_reports_worktree_available_space | agree |
| L3-2 | MINOR | MAINT | diff | docs/orchestration.md, "Machine facts at the start of a night run" | The description says "Two lines under `running jobs:` carry no process" and names the process-table error and the runner-recognition note, but the command prints a third line without a process — `none matched` — in the ordinary healthy case (`jobs_field`, scripts/machine_facts.py:241), so a maintainer comparing the documented block with a normal run finds an undocumented line; the count claim should cover it or name the note lines as such. | mimo-v2.6-pro | fixed — orchestrator hand edit 534954f6 | no | agree |
| L4-1 | MAJOR | MAINT | code | scripts/machine_facts.py, `collect_snapshot()` and `main()` | Every field is wrapped in a bare `except Exception` that renders `not read (…: internal error: <Type>)`, and `main()` returns 0 even then, so a real defect (for example a changed `run_report` signature or a `TypeError` in a renderer) is printed like an unreadable source, exits green, and no wrapper can distinguish a broken instrument from an unreadable one; none of the five internal-error arms is exercised by any test. | hy4-preview | rejected — same row as L2-1: the 'internal error: <Type>' label already separates a code fault from a missing source |  | disagree — No concrete incorrect reading is demonstrated; internal errors are identified explicitly, and missing tests for every exception arm alone do not establish a contract violation. |
| L4-2 | MINOR | SPEC | docs vs code | docs/orchestration.md, section "Machine facts at the start of a night run" | The usage text enumerates exactly three non-process lines under `running jobs:`, but the code can emit a fourth — `not read (ps: internal error: …)` — and each of the four fields can also print `internal error: <Type>`; a maintainer shown such a line cannot tell whether a source was unreadable or the script itself failed. | hy4-preview | fixed — orchestrator hand edit c84da24f | no | agree |
| L4-3 | MINOR | SPEC | docs vs code | scripts/machine_facts.py `disk_field()` against docs/orchestration.md | When `git rev-parse --show-toplevel` cannot identify the worktree, the free-disk line silently switches to the current directory's filesystem and prints the scope "filesystem of the invoking directory; worktree not identified"; the documented block promises "free disk on the invoking worktree's filesystem" and never mentions this fallback or its different meaning. | hy4-preview | fixed — orchestrator hand edit c84da24f | no | agree |
| L4-4 | MINOR | MAINT | test | tests/test_machine_facts.py::test_snapshot_is_local_and_read_only | The subprocess leg proves read-only only indirectly: its fake `git` answers every invocation that is not `rev-parse` with the same fixture table, and the argv the real CLI used is never recorded, so the exact read-only command set (and any command added later) is pinned only by the injected-run leg of the same test. | hy4-preview | rejected — accepted limit named in the PR (maintainer 2026-11-07: finish within one more hour): the injected-run leg pins the read-only command set |  | disagree — The injected-run leg checks the exact command set; the subprocess leg provides complementary coverage, without a demonstrated escaping mutation. |
| L4-5 | MINOR | MAINT | test | tests/test_machine_facts.py::test_timed_out_sources_preserve_independent_facts | The timeout test patches `machine_facts.sys.platform`, which is the process-wide `sys` module and not a copy, so every library in that worker sees "darwin" for the duration; the `sysctl` case depends on that global mutation — without it the case would read a different source on Linux and pass or fail for the wrong reason. | hy4-preview | rejected — accepted limit named in the PR (maintainer 2026-11-07): the platform patch is scoped to one test |  | disagree — The platform override deliberately exercises macOS behavior and is restored by monkeypatch; no concrete interference or incorrect result is demonstrated. |
| L4-6 | MINOR | MAINT | plan | plans/changes/night-machine-facts/plan.md, card and "Time used" | The card states "Appetite: 2 hours of phase 4, repairs included; stop at the limit", but the times recorded below it are 8841 s for the three implement attempts (already past the 7200 s card) plus 14643 s and 11464 s for two repair attempts, and nothing in the plan records a stop, a limit being reached or a revised appetite, so the document now contradicts its own stop rule. | hy4-preview | fixed — orchestrator hand edit c84da24f | no | agree |

Rounds run: 4

Record digest: sha256:44e88e581afe2f9dcb11f9ef77c1d58e76ccdc5014e3ab20f764a3ee38cecfd1

Record identity: sha256:c05e550cdce7da14e8bb52203a866ecfd3a4cf5a7e73a72db031957b14df8711

Loop state: {"availability": {"checked_at": "2026-11-06T19:36:38+00:00", "failed": {"crouton-alpha-free": "pi call failed: exit 1: opencode-go API error (403): {\"type\":\"RegionError\",\"message\":\"This model is not available in your country\"}", "glm-5.2": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated. Use mimo-v2.6-pro instead.\"}", "mimo-v2.6-flash": "pi call failed: the answer is empty"}, "reachable": ["deepseek-v4.1-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "hy4": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured)", "gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured)", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured)", "minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured)", "qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured)", "qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured)", "grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free)", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": []}, "consumed": ["flash", "rung:hy3", "rung:mimo-v2.6-pro", "rung:hy4-preview"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "crouton-alpha-free", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "pulse-alpha-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "crouton-alpha-free", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-06T19:32:17+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1793993536144, "etag": "W/\"2536099d28f32505b4840b309f9262c7\"", "lastModified": 1793973242000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "crouton-alpha-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 270000, "name": "Crouton Alpha Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": [], "overlay": ["beam-free", "claude-haiku-5-5", "crouton-alpha-free", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}, {"date": "2026-11-06", "id": "iceman-contributor-free", "reason": "New in the live Go catalog on 2026-11-06 and picked as the whole free swarm by prepare-loop; \"contributor\" ids on Go have meant that request data may be used for training, and the maintainer's decision of 2026-10-17 (question Q-12) keeps such models off. The Go page's privacy table, read 2026-11-06, confirms it: 'Iceman Contributor Free | Yes | Not ZDR'. A bridge until one central per-use-case model policy exists (bead coding-harness-k0ub with coding-harness-wq1m); maintainer, 2026-11-06, morning question Q-M9, option A."}, {"date": "2026-11-06", "id": "cat-jam-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it, so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}, {"date": "2026-11-06", "id": "longcat-2.5-preview-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it (only LongCat-2.0), so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": [], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "longcat-2.0", "glm-5.3-flash"], "ladder": ["deepseek-v4.1-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "rungs": ["hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: paid models skipped: qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured); gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured); minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured); qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured); qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured); grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor.
> hy3 was asked again with the format reminder: the first answer was malformed
> From hy3:
> hy3's first answer, which was not in the required format:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> | F-1 | MINOR | SPEC | night-machine-facts | scripts/machine_facts.py `collect_snapshot` (`disk = disk_field(statvfs, cwd)`) and `disk_field` | The disk field is read from `cwd` (the invoking directory), not the git-resolved invoking worktree that the other three fields use; criterion 2 promises the filesystem *containing the invoking worktree*, so when `cwd` and the git toplevel lie on different mounts (symlinked or bind-mounted checkout, or a launch directory outside the toplevel) the free-disk figure describes the wrong volume while the rest of the block describes the worktree. The `disk_field` parameter is even named `worktree` but receives `cwd`, hiding the divergence from reviewers.
> | F-2 | MINOR | MAINT | night-machine-facts | scripts/machine_facts.py module top (`sys.dont_write_bytecode = True` set before imports) | Setting `sys.dont_write_bytecode = True` at import time mutates process-global interpreter state; if this module is ever imported as a library by a larger tool, every later import in that process silently skips bytecode caching, and the flag is never restored.
> | F-3 | MINOR | MAINT | night-machine-facts | scripts/machine_facts.py `main()` outer `except Exception` (returns 0) and the per-field `internal error` fallbacks in `collect_snapshot` | A genuine defect inside a source reader (any exception other than the expected `SourceError`) is caught and rendered as `not read (… internal error: <Type>)` while the command still exits 0, so a broken reader ships disguised as a legitimate unreadable source and the night step passes green; only an unrealistic `Path.cwd()`/`now()` failure would surface as the printed "not printed" line, and the type name is easy to miss in a long night log.
> | F-4 | MINOR | MAINT | night-machine-facts | plans/changes/night-machine-facts/plan.md "Criterion ledger" section | The ledger numbers criterion 7 twice — once for `tests/test_machine_facts.py::test_snapshot_is_local_and_read_only` and again for the "not a test — phase-6 diff review" item — so it does not map 1:1 onto the spec's criteria 1–8 and a reviewer cannot tell which ledger line covers the read-only criterion versus the display criterion.

<!-- End of released loop record -->

Stage-2 call, 2026-11-07: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 917 files, 3529 commits, 12 rules.

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 917 files, 3532 commits, 12 rules.

Stage-2 call, 2026-11-07: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 917 files, 3571 commits, 12 rules.

## Phase 6 — Codex, 2026-11-07

Codex reported no finding.

The answer was not only six-cell rows; what is not one is kept below as it came.

> No finding.

Phase 6 verdict: codex 01a1b740-09d2-7551-9104-125c12f168cf, 2026-11-07
Reviewer session: codex 01a1b740-09d2-7551-9104-125c12f168cf — a fresh session reviewed: an earlier ## Phase 6 block makes this a re-check
