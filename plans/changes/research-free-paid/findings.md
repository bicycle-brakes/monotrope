---
title: "Findings — research-free-paid"
category: findings
status: draft
implementation_status: none
date: 2026-11-05
created: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-wb40
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — research-free-paid

Stage-2 call, 2026-11-05: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 902 files, 3322 commits, 12 rules.

ADR answer owed: decisions/answers/research-free-paid/adr.yaml does not exist and the gate tolerated that for this run; the answer is the maintainer's (python3 scripts/harness.py decide adr).

Stage-2 call, 2026-11-05: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM 5.3 Flash failed twice and Sonnet 5.5 once on 2026-11-05 (the last with two red tests: test_shared_selection_preserves_optional_research_eligibility, test_shipped_catalog_prepares_both_swarms_offline) · leak check clean over 906 files, 3345 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-free-paid/plan.md` +11 -11
> - `plans/changes/research-free-paid/spec.md` +1 -1
> - `scripts/stage2.py` +74 -47
> - `scripts/stage2_availability.py` +10 -2
> - `scripts/stage2_free.py` +176 -0
> - `scripts/stage2_swarm.py` +52 -12
> - `tests/test_pi_contract.py` +239 -0
> - `tests/test_stage2_availability.py` +25 -0
> - `tests/test_stage2_free.py` +238 -0
> - `tests/test_stage2_research_availability.py` +71 -0
> - `tests/test_stage2_research_catalog.py` +14 -1
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed `scripts/stage2.py`.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 63 lines of this gate left out …]
> ........................................................................ [ 90%]
> ........................................................................ [ 92%]
> ........................................................................ [ 93%]
> ........................................................................ [ 95%]
> ........................................................................ [ 96%]
> ........................................................................ [ 98%]
> ........................................................................ [ 99%]
> ......                                                                   [100%]
> =================================== FAILURES ===================================
> _____________ test_every_script_has_a_caller_or_a_declared_reason ______________
> [gw1] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-free-paid/.venv/bin/python3
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
> E           stage2_free.py
> E         
> E         Either a step in ci.yml or a line in ci_gates.OHNE_AUFRUFER.
> E       assert not ['stage2_free.py']
>
> tests/test_ci.py:2382: AssertionError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=76498) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/research-free-paid/tests/test_stage2.py:18933: DeprecationWarning: This process (pid=76500) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
> 1 failed, 4812 passed, 17 skipped, 5 warnings in 1296.35s (0:21:36)
> ── [pytest] RED (block) — der Lauf ist rot.
> ── [adr-answers] $ lauf_cmd
> adr-answers: research-free-paid: no answer — plans/changes/research-free-paid/spec.md is a feature and decisions/answers/research-free-paid/adr.yaml does not exist; fix: python3 scripts/harness.py decide adr
> ── [adr-answers] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 31596 earlier lines left out …]
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

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model crouton-alpha-free · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 919 files, 3423 commits, 12 rules.

Stage-2 call, 2026-11-06: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 919 files, 3425 commits, 12 rules.

Stage-2 call, 2026-11-06: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 919 files, 3428 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-free-paid/design.md` +3 -1
> - `plans/changes/research-free-paid/plan.md` +4 -1
> - `plans/changes/research-free-paid/spec.md` +6 -4
> - `scripts/research_capture.py` +5 -0
> - `scripts/stage2.py` +2 -0
> - `scripts/stage2_availability.py` +5 -1
> - `scripts/stage2_free.py` +5 -5
> - `scripts/stage2_swarm.py` +9 -6
> - `tests/test_pi_contract.py` +52 -9
> - `tests/test_stage2_free.py` +91 -0
> - `tests/test_stage2_go_access.py` +9 -1
> - `tests/test_stage2_research_catalog.py` +3 -2
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-5: answered `not a test`, but the row is a code row; it needs a test that was red first
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/research-free-paid/stage2/attempts/research-free-paid/attempt-1-20261106T175015787736Z-3554805b.md
> ```

Stage-2 call, 2026-11-06: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 919 files, 3438 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-free-paid/design.md` +6 -3
> - `plans/changes/research-free-paid/plan.md` +4 -1
> - `plans/changes/research-free-paid/spec.md` +6 -4
> - `tests/test_stage2_free.py` +16 -0
>
> Diagnostics:
> ````text
> - Runner format before `make verify`: ruff changed no file.
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 101 lines of this gate left out …]
> tests/test_close_merged_beads.py:659: AssertionError
> ___________ test_verification_admission_is_outside_execution_timeout ___________
> [gw0] darwin -- Python 3.12.15 /Users/mikypiky/coding-harness/.claude/worktrees/research-free-paid/.venv/bin/python3
>
> world = World(root=PosixPath('/private/var/folders/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-141/popen-gw0...rs/44/yc0m3m456b51nyzwyfjptgm40000gn/T/pytest-of-mikypiky/pytest-141/popen-gw0/test_verification_admission_is0/state'))
> monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10b90e210>
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
> tests/test_stage2.py:2177: AssertionError
> ----------------------------- Captured stderr call -----------------------------
> [verify-lock] waiting for admission: holder pid 99327 (/Users/mikypiky/coding-harness/.claude/worktrees/research-free-paid/.venv/bin/python3 -c import os, pathlib, time; pathlib.Path(os.environ['HOLDER_READY']).write_text(str(os.getpid())); time.sleep(30.0), started 2026-11-06T21:02:49)
> [verify-lock] admitted after 1s
> [verify-lock] available memory cannot be measured; proceeding without a reading
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=74257) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/research-free-paid/tests/test_stage2.py:18933: DeprecationWarning: This process (pid=74256) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_close_merged_beads.py::test_startup_budget_reserves_publication
> FAILED tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout
> 2 failed, 4865 passed, 17 skipped, 5 warnings in 1074.02s (0:17:54)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 32052 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/research-free-paid/stage2/attempts/research-free-paid/attempt-2-20261106T175015787736Z-3554805b.md
> ````

Stage-2 call, 2026-11-06: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 919 files, 3443 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-free-paid/design.md` +3 -1
> - `plans/changes/research-free-paid/plan.md` +2 -1
> - `plans/changes/research-free-paid/spec.md` +5 -4
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-6: tests/test_pi_contract.py::test_fault_proof_rejects_unrelated_contract_failure: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/research-free-paid/stage2/attempts/research-free-paid/attempt-3-20261106T175015787736Z-3554805b.md
> ```

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 919 files, 3455 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/research-free-paid/design.md` +3 -1
> - `plans/changes/research-free-paid/plan.md` +3 -1
> - `plans/changes/research-free-paid/spec.md` +5 -4
> - `scripts/research_capture.py` +6 -0
> - `scripts/stage2.py` +2 -0
> - `scripts/stage2_availability.py` +3 -2
> - `scripts/stage2_free.py` +5 -5
> - `scripts/stage2_swarm.py` +10 -6
> - `tests/test_pi_contract.py` +40 -10
> - `tests/test_stage2_free.py` +91 -1
> - `tests/test_stage2_go_access.py` +9 -1
> - `tests/test_stage2_research_catalog.py` +3 -3
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - L1-5: answered `not a test`, but the row is a code row; it needs a test that was red first
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/research-free-paid/stage2/attempts/research-free-paid/attempt-1-20261107T005305744145Z-48790cf5.md
> ```

Stage-2 call, 2026-11-07: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 919 files, 3466 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model hy3 · leak check clean over 919 files, 3487 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 919 files, 3499 commits, 12 rules.

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 919 files, 3506 commits, 12 rules.
