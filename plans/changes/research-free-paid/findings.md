---
title: "Findings — research-free-paid"
category: findings
status: draft
implementation_status: none
date: 2026-11-05
created: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-08
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

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model hy4-preview · leak check clean over 919 files, 3523 commits, 12 rules.

Stage-2 call, 2026-11-07: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 919 files, 3536 commits, 12 rules.

Stage-2 call, 2026-11-07: review-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 919 files, 3571 commits, 12 rules.

Stage-2 call, 2026-11-07: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 919 files, 3588 commits, 12 rules.

## Phase 6 — Codex, 2026-11-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F6-1 | MAJOR | SPEC | Offline preparation contract | tests/test_pi_contract.py:1592 | `offline_world` inherits the `world` fixture, which replaces production `stage2.check_overlay` with a no-op (tests/test_stage2.py:665), and never restores it. If the pinned Pi rejects the activated catalog configuration, production review preparation refuses, but this contract still accepts its synthetic listing and seals a receipt. The promised preparation gate therefore cannot detect failures in the real overlay validator. [Acceptance criteria 9–10] | Codex | fixed — not a test — offline_world restores production stage2.check_overlay; ruff checks and all 17 required test cases pass. | — |

Phase 6 verdict: codex 01a1b74d-5b3c-7a80-a357-d4e1d2abe210, 2026-11-07
Reviewer session: codex 01a1b74d-5b3c-7a80-a357-d4e1d2abe210 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-11-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | diff | `decisions/answers/research-free-paid/adr.yaml` | The change adds the feature's ADR answer record (`answer: 'no'`, `answered_by: framework-architect`, `answered_at: 2026-11-06`) whose reason repeats the spec's own proposal text, while `plans/changes/research-free-paid/plan.md` says "do not write an ADR answer", `spec.md` states no maintainer answer is claimed or written, `design.md` states no answer "has been recorded by this draft", and `findings.md` still records the answer as owed to the maintainer. `scripts/check_adr_answers.py` checks format only and names the maintainer as the only writer, so this file turns the red `adr-answers` gate green without a recorded maintainer answer, and the four artefacts now contradict each other with no way to tell which is current. | deepseek-v4.1-flash | fixed — not a test — Spec, design and plan acknowledge the maintainer answer recorded at 0baba58f; the answer record remains unchanged. | no — not a test | disagree — Commit 0baba58f dokumentiert die Maintainer-Antwort aus Q-M2; veraltete Artefakte belegen keine erfundene Entscheidung. |
| L1-2 | MAJOR | SPEC | diff | `scripts/stage2_free.py::model_veto`, `scripts/stage2_availability.py::prepare_research` and `research_report` | The shared veto checks the declaration exclusion before paid admission (order `plain`, `excluded`, `paid`), so a `-free` id that is both in `modelle` and named by an `ausgeschlossen` entry is classified as excluded. The review's `free_drops` then names it only with the exclusion reason (before this change `free_drops` checked `paid` first and reported "a paid model"), and the research receipt carries it as `excluded-by-declaration`, a list `research_report` never prints, so the paid/free collision vanishes from the report; spec criterion 7 forbids exactly a report that "silently omits the collision". A test planting `beam-free` in an `ausgeschlossen` entry of the relevant class would show it. | deepseek-v4.1-flash | fixed — tests/test_stage2_free.py::test_paid_admission_reason_wins_over_declaration_exclusion | yes — tests/test_stage2_free.py::test_paid_admission_reason_wins_over_declaration_exclusion | agree |
| L1-3 | MINOR | MAINT | diff | `scripts/stage2_swarm.py::pi_reason` and `select_research_catalog` | Destination permission is still decided in the caller: `pi_reason` runs `stage2_go.url_problem(base, address.host)` before the shared selector sees the candidate and records any refusal as `"pi-malformed"`, so `chosen.refused_destination` stays empty for every research free candidate and the new mapping of it to `"pi-malformed"` in the candidate loop is unreachable. `design.md` says destination permission "moves to the shared selector's Go assessment rather than remaining a second host/base rule", and criterion 5 forbids duplicating it; the shared selector's destination refusal is therefore neither exercised nor testable through the research path, and a later repair of `pi_reason` would silently bypass the shared assessment. | deepseek-v4.1-flash | fixed — tests/test_stage2_free.py::test_research_destination_refusal_keeps_shared_assessment_reason | yes — tests/test_stage2_free.py::test_research_destination_refusal_keeps_shared_assessment_reason | agree |
| L1-4 | MINOR | MAINT | diff | `scripts/stage2_free.py::select`, `scripts/research_capture.py:822` | The component meant to guarantee that a paid admission wins makes `paid` and `exclusion` optional with permissive defaults (`paid=()`, `exclusion=None`), so the rule holds only as long as every caller passes the current declaration. `scripts/research_capture.py:822` already calls `select_research_catalog` without either argument and therefore selects free members with no paid veto; the next caller, or a slip in `prepare_research`, silently reintroduces the collision this change repairs, and no test notices because every test supplies the arguments itself. | deepseek-v4.1-flash | fixed — tests/test_stage2_free.py::test_selectors_require_admission_inputs | yes — tests/test_stage2_free.py::test_selectors_require_admission_inputs | agree |
| L1-5 | MAJOR | SPEC | free-swarm round 1 | decisions/answers/research-free-paid/adr.yaml (vs plans/changes/research-free-paid/plan.md, Scope and baseline, and spec.md, Definition of Done) | The change carries an ADR answer (answer 'no', answered_by framework-architect, answered_at 2026-11-06) although its own plan says do not write an ADR answer and its spec says no maintainer answer is claimed or written here and that an answer is recorded only after the maintainer states it; findings.md calls that answer the maintainer's and decisions.md records maintainer answers as answered_by maintainer, so nothing in the change shows the maintainer statement the spec conditions on. | mimo-v2.6-flash | fixed — tests/test_stage2_free.py::test_recorded_maintainer_adr_answer_is_reflected_in_change_contract | yes — tests/test_stage2_free.py::test_recorded_maintainer_adr_answer_is_reflected_in_change_contract | disagree — Commit 0baba58f nennt ausdrücklich die Maintainer-Aussage aus Q-M2 als Grundlage. |
| L1-6 | MINOR | MAINT | free-swarm round 1 | tests/test_pi_contract.py::test_both_preparation_contracts_detect_planted_faults | The four planted faults are credited from any AssertionError raised by five sequential full-contract runs on one shared offline_world, with the no-fault control run only before the first; if a repeat prepare-loop or prepare-explore on the already-prepared world fails for a reason unrelated to the planted fault, every iteration counts as detected and criterion 10 is proven vacuously, while plan step 6 requires the contract's own assertions to detect each fault. | mimo-v2.6-flash | fixed — not a test — Each planted fault has a fresh parametrized world, a clean control and its own expected assertion and diagnostic. | no — not a test | agree |
| L1-7 | MINOR | MAINT | free-swarm round 1 | scripts/stage2_swarm.py::select_research_catalog | The paid-admission veto and the public-web exclusion arrive as optional parameters defaulting to paid=() and exclusion=None, while the review side reads modelle from the declaration inside stage2.free_selection; a future research call site that omits them silently reopens the paid -free collision this change exists to close, and the selector's existing tests call it without paid, so the omission stays green. | mimo-v2.6-flash | fixed — tests/test_stage2_free.py::test_selectors_require_admission_inputs | yes — tests/test_stage2_free.py::test_selectors_require_admission_inputs | agree |
| L1-8 | MAJOR | MAINT | implementation | scripts/stage2_swarm.py — the candidate-reason mapping after the shared selection (`refused_destination` → `"pi-malformed"`) | A free candidate the destination assessment refuses is recorded with the reason code `pi-malformed` — the same code that means a non-plain model id — so a foreign or moved base URL reads as a malformed Pi row in `catalog.candidates`, the availability receipt and the report, while the actual refusal text from the Go assessment is thrown away; criterion 5 requires the omission to carry its reason and a maintainer diagnosing a foreign-host drop from the receipt gets the wrong cause. | glm-5.3-flash | fixed — tests/test_stage2_free.py::test_research_destination_refusal_keeps_shared_assessment_reason | yes — tests/test_stage2_free.py::test_research_destination_refusal_keeps_shared_assessment_reason | agree |
| L1-9 | MINOR | SPEC | implementation | scripts/stage2_swarm.py — `select_research_catalog`, the explicit-include eligibility raise | An explicitly included free id that the declaration refuses for the public web now hits the hard exclusion veto, leaves `chosen.eligible`, and raises the whole-preparation refusal `explicit free include is ineligible: <id>`; the previous flow prepared it, silently filtered it out of the free probes and listed it in the state's excluded set. This widens the preparation's error contract to a new refusal class; no test pins it and criterion 6 only asks that the existing refusal scope be retained. | glm-5.3-flash | fixed — tests/test_stage2_free.py::test_explicit_research_include_excluded_for_public_web_stays_optional | yes — tests/test_stage2_free.py::test_explicit_research_include_excluded_for_public_web_stays_optional | disagree — Das Design verlangt ausdrücklich die Ablehnung eines explizit angeforderten, ungeeigneten Forschermodells; ein hartes Ausschlusskriterium darf diese Prüfung auslösen. |
| L1-10 | MINOR | SPEC | implementation | scripts/stage2_free.py — `model_veto` order; reached from `scripts/stage2.py` `free_selection` and `stage2_swarm.py` | The shared vetoes check the declaration's exclusion before paid admission, so an id that is both admitted paid in `modelle` and named by an `ausgeschlossen` entry is dropped and reported with the exclusion reason; criterion 7 says a dropped paid-admitted free candidate's report names the paid-admission reason, and the previously published review reason for exactly this id (`a paid model; the free class does not admit it`) silently changes. No test plants an id carrying both flags. | glm-5.3-flash | fixed — tests/test_stage2_free.py::test_paid_admission_reason_wins_over_declaration_exclusion | yes — tests/test_stage2_free.py::test_paid_admission_reason_wins_over_declaration_exclusion | agree |
| L2-1 | MAJOR | MAINT | hy3 | tests/test_pi_contract.py::test_both_preparation_contracts_detect_planted_faults (the two "bypasses the shared selection" parametrizations) | The planted-fault rows meant to prove criterion 10 cannot pass: their `expected` is "the review/research preparation refused the shipped Go catalog", the message only raised by the genuinely-refusing faults, but a selection bypass does not make the preparation refuse — the unmonkeypatched call boundary `free_admission_problem`/`invocation_problem` still vetoes the paid id, so the preparation neither refuses nor selects it and a different later assertion fires (or none does); and their `diagnostic` ("refused: the model beam-free is a paid model; the free class does not admit it" / "refused: beam-free is a paid model; the free class does not admit it") is never printed by any code path because the refusal reasons omit the "refused: " prefix, so `assert diagnostic in capsys.readouterr().err` always fails. The contract therefore never actually exercises a shared-selection bypass and gives a misleading failure, leaving criterion 10's guard unreliable. | hy3 | rejected — measured false: tests/test_pi_contract.py -k planted_faults passes, 4 passed on 2026-11-07 in the change's worktree, so the bypass rows are exercised and their diagnostics are printed |  | disagree — Die Aufrufgrenzen werfen Refused; stage2.main gibt dabei „refused: …“ aus und beendet die Vorbereitung mit Fehlerstatus. |
| L3-1 | MAJOR | SPEC | promised, not done | tests/test_pi_contract.py — `offline_world`/`shipped_bridge` (plan step 6; design.md, "Interfaces") | The research leg of the offline contract replaces the production catalog bridge (`catalog_bridge`, which runs `scripts/stage2_research_catalog.mjs` against the pinned Pi) with a hand-built `shipped_bridge` envelope instead of serving the shipped catalog through local source stand-ins to that adapter as plan step 6 and design.md promise ("real pinned Pi version/listing/bridge parsing", transports replaced "not by replacing preparation"). The production research discovery path — the helper's Pi invocation, runtime baseline and bridge construction, the exact machinery the Pi move of decisions.md#Q-3 broke — is never exercised against the installed Pi, and the fabricated pi source (`http://127.0.0.1/api/models/providers/opencode-go`) is not even labelled synthetic as the design requires; a Pi or catalog move that breaks only that helper leaves `test_shipped_catalog_prepares_both_swarms_offline` and the fault proof green, so criterion 9 is met for the shared selection but not for the research preparation's catalog retrieval. | mimo-v2.6-pro | fixed — not a test — test-only repair runs production catalog_bridge and the pinned Pi helper against local sources serving the shipped catalog | no — not a test | agree |
| L3-2 | MINOR | MAINT | maintainer trip | scripts/stage2_swarm.py — `select_research_catalog`, explicit-include check (vs design.md, "Interfaces") | The two hard vetoes of `stage2_free.model_veto` get opposite treatments at the explicit-include boundary: a paid explicit include raises `ResearchCatalogError` and aborts the whole preparation with the misleading text "the Go catalog is unmeasured: explicit free include is ineligible: …", while a declaration-excluded explicit include is silently dropped and stays optional (tests/test_stage2_free.py, `test_explicit_research_include_excluded_for_public_web_stays_optional`). design.md's one sentence ("A hard-vetoed id is never admitted by an include; an explicitly requested ineligible researcher still receives the existing preflight refusal") describes a uniform behavior, so a maintainer cannot predict which veto aborts a run, and the abort message names an unmeasured catalog as the cause of an admission refusal. | mimo-v2.6-pro | fixed — tests/test_stage2_free.py::test_explicit_research_include_refuses_hard_veto | yes — tests/test_stage2_free.py::test_explicit_research_include_refuses_hard_veto | agree |
| L3-3 | MINOR | MAINT | maintainer trip | scripts/stage2.py — `select_free` (and `free_drops`) | The compatibility wrapper `select_free` calls the shared selector with `paid=()` and `exclusion=None`, so standing alone it silently re-admits paid and declaration-excluded ids; only `free_selection` adds the declaration vetoes, and no parity or admission test routes through `select_free` (its only caller is tests/test_stage2.py). The design allows wrappers but this one keeps a weaker admission than `free_admission_problem`; a future caller wiring it into a preparation reintroduces the paid/free collision this change exists to remove, with nothing turning red. | mimo-v2.6-pro | fixed — tests/test_stage2_free.py::test_select_free_preserves_declaration_vetoes | yes — tests/test_stage2_free.py::test_select_free_preserves_declaration_vetoes | agree |
| L4-1 | MAJOR | MAINT | round-4 review | `scripts/stage2.py:2096` `select_free(rule, catalog, *, root=None)` | The compatibility wrapper now decides cost class from `Path.cwd()` whenever the caller omits `root`: `free_selection(root if root is not None else Path.cwd(), …)` reads whatever `model-endpoints.yaml` the process happens to sit in, so the paid-admission veto silently follows the caller's working directory (or fails with an unhandled load error when there is none there), instead of the function staying pure as its docstring claims ("just like a local invocation"). No production caller passes `root`, and an existing caller in `tests/test_stage2.py` already relies on the current-directory form, so a test run started from outside the checkout — or any future caller — may read a foreign declaration and treat a paid id as free. Pass the root explicitly, or drop the two-argument form and let every caller name its repository. | hy4-preview | fixed — tests/test_stage2_free.py::test_select_free_requires_repository_root_from_another_directory | yes — tests/test_stage2_free.py::test_select_free_requires_repository_root_from_another_directory | agree |
| L4-2 | MAJOR | SPEC | round-4 review | `scripts/stage2_free.py:158-166` `select()` with `scripts/stage2_swarm.py:288-296` | In the shared selector the destination assessment only runs when the candidate has no caller-supplied problem (`elif problem is None and candidate.definition is not None and address is not None`), while the research adapter supplies its capability reason as `Candidate.problem`. So a free id with a refused destination that also lacks tool support (or any free id when the capability source is down and every id carries `capability-unavailable`) is never assessed and is reported with the capability reason, whereas before the change the destination check ran first in `pi_reason` and such an id was reported as refused for its destination. That leaves spec criterion 5 ("that candidate is omitted with its reason while admissible peers remain selectable", refuted by "Either preparation … duplicates destination policy") unmet for the conflict case, and it is untested: `tests/test_stage2_free.py::test_research_destination_refusal_keeps_shared_assessment_reason` only plants a foreign base on a model that does have tool support. Assess the destination independently of the capability reason and record it in the result. | hy4-preview | fixed — tests/test_stage2_free.py::test_research_reports_destination_and_capability_refusals | yes — tests/test_stage2_free.py::test_research_reports_destination_and_capability_refusals | agree |
| L4-3 | MINOR | SPEC | round-4 review | `plans/changes/research-free-paid/plan.md` ("Build sequence and files", "No files are deleted…") vs the diff's `scripts/ci_gates.py` and `scripts/research_capture.py` | The change edits two files its own plan never lists: steps 1-7 name the test files, `scripts/stage2.py`, `scripts/stage2_swarm.py`, `scripts/stage2_availability.py` and the new `scripts/stage2_free.py`, and the plan declares "agent/CI configuration" among the areas that must stay untouched and states that no held-path edit is needed, yet `scripts/ci_gates.py` gains an `OHNE_AUFRUFER` entry (which the earlier red run required) and `scripts/research_capture.py` gains a `yaml` import and the new selection arguments. A maintainer reading the plan would not expect these files in the pull request and cannot tell whether they were a deliberate bootstrap edit. Add both files to the plan's build sequence, or state in `plan.md` that the missing-caller entry forced a `ci_gates.py` edit. | hy4-preview | fixed — orchestrator hand edit 09541649 | no | agree |
| L4-4 | MINOR | MAINT | round-4 review | `scripts/ci_gates.py:153-157` `OHNE_AUFRUFER["stage2_free.py"]` | The declared reason says the helper belongs to "`scripts/stage2.py`, `scripts/stage2_availability.py` and `scripts/stage2_swarm.py`", but `stage2_availability.py` never imports `stage2_free` (it only passes paid ids and an exclusion callable into `stage2_swarm.select_research_catalog`), and the sentence is also split awkwardly ("never an entry point of its own: the one free-model selection…"). The reason is what a later maintainer reads to find the helper's callers, so it should name exactly `scripts/stage2.py` and `scripts/stage2_swarm.py` (plus the two test files), not a module that does not use it. | hy4-preview | fixed — not a test — The OHNE_AUFRUFER reason names only scripts/stage2.py and scripts/stage2_swarm.py as production importers and retains both test files. | no — not a test | disagree — stage2_availability nutzt den Helfer indirekt; die Formulierung behauptet keinen direkten Import und zeigt keinen Funktionsfehler oder verletzten Vertrag. |

Rounds run: 5

Record digest: sha256:4488dce16444ae6b1ed570137a80bd7c79c4ea85b19b7a0c9463520d8d7c6e0c

Record identity: sha256:4ffb9ec8902fec92dc4d55156735f45e97e5a8dff106b7fc2b339e68f050d709

Cut rounds: 1, 2, 3, 4, 5

Loop state: {"availability": {"checked_at": "2026-11-06T17:02:52+00:00", "failed": {"crouton-alpha-free": "pi call failed: exit 1: opencode-go API error (403): {\"type\":\"RegionError\",\"message\":\"This model is not available in your country\"}", "glm-5.2": "pi call failed: exit 1: 403: {\"type\":\"permission_error\",\"message\":\"Model access is disabled\"}", "mimo-v2.5": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5 has been deprecated. Use mimo-v2.6-flash instead.\"}", "mimo-v2.5-pro": "pi call failed: exit 1: 410: {\"type\":\"ModelDeprecated\",\"message\":\"Model mimo-v2.5-pro has been deprecated. Use mimo-v2.6-pro instead.\"}"}, "reachable": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "skipped": {"beam-free": "a paid model; the free class does not admit it", "hy4": "not admitted; data terms have not been read", "muse-spark-1.2-contributor": "not admitted; data terms have not been read", "muse-spark-1.3-contributor": "not admitted; data terms have not been read"}, "slow": {}, "terms_skipped": ["qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured)", "gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured)", "claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured)", "minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured)", "qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured)", "qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured)", "grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint))", "gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor)", "kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))", "step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free)", "beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30))"], "terms_warnings": []}, "consumed": ["rung:glm-5.3-flash", "flash", "rung:hy3", "rung:mimo-v2.6-pro", "rung:hy4-preview", "rung:kimi-k2.7-code"], "free": {"billing": "not measured: pi.dev is a live catalog, not a billing statement", "catalog": [{"model": "beam-free", "provider": "opencode"}, {"model": "big-pickle", "provider": "opencode"}, {"model": "claude-fable-5", "provider": "opencode"}, {"model": "claude-fable-5-1", "provider": "opencode"}, {"model": "claude-haiku-4-5", "provider": "opencode"}, {"model": "claude-haiku-5-5", "provider": "opencode"}, {"model": "claude-opus-4-5", "provider": "opencode"}, {"model": "claude-opus-4-6", "provider": "opencode"}, {"model": "claude-opus-4-7", "provider": "opencode"}, {"model": "claude-opus-4-8", "provider": "opencode"}, {"model": "claude-opus-5", "provider": "opencode"}, {"model": "claude-opus-5-5", "provider": "opencode"}, {"model": "claude-sonnet-4-5", "provider": "opencode"}, {"model": "claude-sonnet-4-6", "provider": "opencode"}, {"model": "claude-sonnet-5", "provider": "opencode"}, {"model": "claude-sonnet-5-5", "provider": "opencode"}, {"model": "crouton-alpha-free", "provider": "opencode"}, {"model": "deepseek-v4-pro", "provider": "opencode"}, {"model": "deepseek-v4.1-flash", "provider": "opencode"}, {"model": "deepseek-v4.1-flash-free", "provider": "opencode"}, {"model": "flint-40b-free", "provider": "opencode"}, {"model": "gemini-3-flash", "provider": "opencode"}, {"model": "gemini-3.1-pro", "provider": "opencode"}, {"model": "gemini-3.5-flash", "provider": "opencode"}, {"model": "gemini-3.5-flash-lite", "provider": "opencode"}, {"model": "gemini-3.6-flash", "provider": "opencode"}, {"model": "gemini-3.7-flash", "provider": "opencode"}, {"model": "gemini-3.8-flash", "provider": "opencode"}, {"model": "gemini-4-argon", "provider": "opencode"}, {"model": "glm-5", "provider": "opencode"}, {"model": "glm-5.1", "provider": "opencode"}, {"model": "glm-5.2", "provider": "opencode"}, {"model": "glm-5.3", "provider": "opencode"}, {"model": "glm-5.3-flash", "provider": "opencode"}, {"model": "glm-5.3-flash-free", "provider": "opencode"}, {"model": "gpt-5", "provider": "opencode"}, {"model": "gpt-5-codex", "provider": "opencode"}, {"model": "gpt-5-nano", "provider": "opencode"}, {"model": "gpt-5.1", "provider": "opencode"}, {"model": "gpt-5.1-codex", "provider": "opencode"}, {"model": "gpt-5.1-codex-max", "provider": "opencode"}, {"model": "gpt-5.1-codex-mini", "provider": "opencode"}, {"model": "gpt-5.2", "provider": "opencode"}, {"model": "gpt-5.2-codex", "provider": "opencode"}, {"model": "gpt-5.3-codex", "provider": "opencode"}, {"model": "gpt-5.4", "provider": "opencode"}, {"model": "gpt-5.4-mini", "provider": "opencode"}, {"model": "gpt-5.4-nano", "provider": "opencode"}, {"model": "gpt-5.4-pro", "provider": "opencode"}, {"model": "gpt-5.5", "provider": "opencode"}, {"model": "gpt-5.5-pro", "provider": "opencode"}, {"model": "gpt-5.6-luna", "provider": "opencode"}, {"model": "gpt-5.6-sol", "provider": "opencode"}, {"model": "gpt-5.6-terra", "provider": "opencode"}, {"model": "gpt-6-astra", "provider": "opencode"}, {"model": "gpt-6-luna", "provider": "opencode"}, {"model": "gpt-6-sol", "provider": "opencode"}, {"model": "gpt-6.1-sol", "provider": "opencode"}, {"model": "grok-4.5", "provider": "opencode"}, {"model": "grok-4.6", "provider": "opencode"}, {"model": "grok-4.7", "provider": "opencode"}, {"model": "grok-build-0.1", "provider": "opencode"}, {"model": "kimi-k2.5", "provider": "opencode"}, {"model": "kimi-k2.6", "provider": "opencode"}, {"model": "kimi-k2.7-code", "provider": "opencode"}, {"model": "kimi-k3", "provider": "opencode"}, {"model": "mimo-v2.6-flash-free", "provider": "opencode"}, {"model": "minimax-m2.5", "provider": "opencode"}, {"model": "minimax-m2.7", "provider": "opencode"}, {"model": "minimax-m3", "provider": "opencode"}, {"model": "mistral-large-4", "provider": "opencode"}, {"model": "muse-spark-1.2", "provider": "opencode"}, {"model": "muse-spark-1.3", "provider": "opencode"}, {"model": "muse-wonder-1.0", "provider": "opencode"}, {"model": "nemotron-3.5-lightning-free", "provider": "opencode"}, {"model": "nemotron-3.5-super-vl-free", "provider": "opencode"}, {"model": "pulse-alpha-free", "provider": "opencode"}, {"model": "qwen3.5-plus", "provider": "opencode"}, {"model": "qwen3.6-plus", "provider": "opencode"}, {"model": "qwen3.8-flash", "provider": "opencode"}, {"model": "qwen3.8-max", "provider": "opencode"}, {"model": "beam-free", "provider": "opencode-go"}, {"model": "claude-haiku-5-5", "provider": "opencode-go"}, {"model": "crouton-alpha-free", "provider": "opencode-go"}, {"model": "deepseek-v4-pro", "provider": "opencode-go"}, {"model": "deepseek-v4.1-flash", "provider": "opencode-go"}, {"model": "gemini-4-argon", "provider": "opencode-go"}, {"model": "glm-5.2", "provider": "opencode-go"}, {"model": "glm-5.3", "provider": "opencode-go"}, {"model": "glm-5.3-flash", "provider": "opencode-go"}, {"model": "gpt-5.6-luna", "provider": "opencode-go"}, {"model": "gpt-6-luna", "provider": "opencode-go"}, {"model": "grok-4.7", "provider": "opencode-go"}, {"model": "hy3", "provider": "opencode-go"}, {"model": "hy4", "provider": "opencode-go"}, {"model": "hy4-preview", "provider": "opencode-go"}, {"model": "iceman-contributor-free", "provider": "opencode-go"}, {"model": "kimi-k2.7-code", "provider": "opencode-go"}, {"model": "kimi-k3", "provider": "opencode-go"}, {"model": "kimi-k3.1-pro", "provider": "opencode-go"}, {"model": "longcat-2.0", "provider": "opencode-go"}, {"model": "mimo-v2.5", "provider": "opencode-go"}, {"model": "mimo-v2.5-pro", "provider": "opencode-go"}, {"model": "mimo-v2.6-flash", "provider": "opencode-go"}, {"model": "mimo-v2.6-pro", "provider": "opencode-go"}, {"model": "minimax-m3", "provider": "opencode-go"}, {"model": "minimax-m3.1-flash", "provider": "opencode-go"}, {"model": "muse-spark-1.2-contributor", "provider": "opencode-go"}, {"model": "muse-spark-1.3-contributor", "provider": "opencode-go"}, {"model": "qwen3.7-plus", "provider": "opencode-go"}, {"model": "qwen3.8-flash", "provider": "opencode-go"}, {"model": "qwen3.8-max", "provider": "opencode-go"}, {"model": "step-5-preview", "provider": "opencode-go"}], "checked_at": "2026-11-06T16:58:42+00:00", "dropped": {"beam-free": "a paid model; the free class does not admit it"}, "models_store": {"opencode-go": {"checkedAt": 1793984320295, "etag": "W/\"2536099d28f32505b4840b309f9262c7\"", "lastModified": 1793973242000, "models": [{"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "beam-free", "input": ["text"], "maxTokens": 131072, "name": "Beam Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"forceAdaptiveThinking": true, "supportsMidConvoEffort": true, "supportsTemperature": false}, "contextWindow": 1000000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.05, "cacheWrite": 0.625, "input": 0.5, "inputTokensAbove": 100000, "output": 2.5}]}, "id": "claude-haiku-5-5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "Claude Haiku 5.5", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"max": "max", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "crouton-alpha-free", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 270000, "name": "Crouton Alpha Free", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.022, "cacheWrite": 0, "input": 0.66, "output": 1.98}, "id": "deepseek-v4-pro", "input": ["text"], "maxTokens": 384000, "name": "DeepSeek V4 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "requiresReasoningContentOnAssistantMessages": true, "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true, "thinkingFormat": "deepseek"}, "contextWindow": 1000000, "cost": {"cacheRead": 0.003, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "deepseek-v4.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 384000, "name": "DeepSeek V4.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "google-generative-ai", "baseUrl": "https://opencode.ai/inference/go/google/v1beta", "contextWindow": 1048576, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 2, "output": 10}, "id": "gemini-4-argon", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Gemini 4 Argon", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.2", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.2", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.26, "cacheWrite": 0, "input": 1.4, "output": 4.4}, "id": "glm-5.3", "input": ["text"], "maxTokens": 131072, "name": "GLM-5.3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.03, "cacheWrite": 0, "input": 0.15, "output": 0.5}, "id": "glm-5.3-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "GLM-5.3-Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "output": 1.2, "tiers": [{"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "inputTokensAbove": 272000, "output": 1.8}]}, "id": "gpt-5.6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-5.6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession", "supportsAdditionalTools": true, "supportsMidConvoSystemMessages": true}, "contextWindow": 1050000, "cost": {"cacheRead": 0.01, "cacheWrite": 0.125, "input": 0.1, "output": 0.5, "tiers": [{"cacheRead": 0.02, "cacheWrite": 0.25, "input": 0.2, "inputTokensAbove": 272000, "output": 0.75}]}, "id": "gpt-6-luna", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "GPT-6 Luna", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": "none", "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 500000, "cost": {"cacheRead": 0.5, "cacheWrite": 0, "input": 2, "output": 6, "tiers": [{"cacheRead": 1, "cacheWrite": 0, "input": 4, "inputTokensAbove": 200000, "output": 12}]}, "id": "grok-4.7", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 500000, "name": "Grok 4.7", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 256000, "cost": {"cacheRead": 0.035, "cacheWrite": 0, "input": 0.14, "output": 0.58}, "id": "hy3", "input": ["text"], "maxTokens": 128000, "name": "Hy3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Hy4", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1024000, "cost": {"cacheRead": 0.042, "cacheWrite": 0, "input": 0.834, "output": 2.501}, "id": "hy4-preview", "input": ["text"], "maxTokens": 64000, "name": "Hy4 preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": null, "max": null, "medium": null, "minimal": null, "off": "none", "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0, "cacheWrite": 0, "input": 0, "output": 0}, "id": "iceman-contributor-free", "input": ["text"], "maxTokens": 131072, "name": "Iceman Contributor Free", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 262144, "cost": {"cacheRead": 0.19, "cacheWrite": 0, "input": 0.95, "output": 4}, "id": "kimi-k2.7-code", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 262144, "name": "Kimi K2.7 Code", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.3, "cacheWrite": 3, "input": 3, "output": 15}, "id": "kimi-k3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": null, "low": null, "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsMidConvoSystemMessages": true, "supportsMidConvoToolAdditions": true, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.2, "cacheWrite": 2, "input": 2, "output": 10}, "id": "kimi-k3.1-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Kimi K3.1 Pro", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": null, "minimal": null, "off": null, "xhigh": null}, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.006, "cacheWrite": 0, "input": 0.3, "output": 1.2}, "id": "longcat-2.0", "input": ["text"], "maxTokens": 131072, "name": "LongCat-2.0", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.5", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 128000, "name": "MiMo V2.5", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.5-pro", "input": ["text"], "maxTokens": 128000, "name": "MiMo V2.5 Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.0028, "cacheWrite": 0, "input": 0.14, "output": 0.28}, "id": "mimo-v2.6-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1048576, "cost": {"cacheRead": 0.003625, "cacheWrite": 0, "input": 0.435, "output": 0.87}, "id": "mimo-v2.6-pro", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiMo-V2.6-Pro", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.06, "cacheWrite": 0, "input": 0.3, "output": 1.2, "tiers": [{"cacheRead": 0.12, "cacheWrite": 0, "input": 0.6, "inputTokensAbove": 512000, "output": 2.4}]}, "id": "minimax-m3", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "MiniMax-M3", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.015, "cacheWrite": 0, "input": 0.15, "output": 0.6}, "id": "minimax-m3.1-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 512000, "name": "MiniMax M3.1 Flash", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": "max", "medium": "medium", "minimal": null, "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.2-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.2 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "openai-responses", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"sessionAffinityFormat": "openai-nosession"}, "contextWindow": 1048576, "cost": {"cacheRead": 0.002, "cacheWrite": 0, "input": 0.1, "output": 0.2}, "id": "muse-spark-1.3-contributor", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Muse Spark 1.3 Contributor", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": "minimal", "off": null, "xhigh": "xhigh"}, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.04, "cacheWrite": 0.5, "input": 0.4, "output": 1.6, "tiers": [{"cacheRead": 0.12, "cacheWrite": 1.5, "input": 1.2, "inputTokensAbove": 256000, "output": 4.8}]}, "id": "qwen3.7-plus", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Qwen3.7 Plus", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "compat": {"allowEmptySignature": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.016, "cacheWrite": 0.2, "input": 0.15, "output": 0.47}, "id": "qwen3.8-flash", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Flash", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "anthropic-messages", "baseUrl": "https://opencode.ai/inference/go/anthropic", "contextWindow": 1000000, "cost": {"cacheRead": 0.25, "cacheWrite": 2.5, "input": 2, "output": 6}, "id": "qwen3.8-max", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 131072, "name": "Qwen3.8 Max", "provider": "opencode-go", "reasoning": true, "type": "chat"}, {"api": "openai-completions", "baseUrl": "https://opencode.ai/inference/go/openai/v1", "compat": {"maxTokensField": "max_tokens", "supportsDeveloperRole": false, "supportsStore": false, "supportsStrictMode": true}, "contextWindow": 1000000, "cost": {"cacheRead": 0.1, "cacheWrite": 0, "input": 1, "output": 2.7}, "id": "step-5-preview", "input": ["text", "image"], "inputLimits": {"images": {"resize": {"jpegQuality": 80, "maxBytes": 4718592, "maxHeight": 2000, "maxWidth": 2000}}}, "maxTokens": 65536, "name": "Step 5 Preview", "provider": "opencode-go", "reasoning": true, "thinkingLevelMap": {"high": "high", "low": "low", "max": null, "medium": "medium", "minimal": null, "off": null, "xhigh": null}, "type": "chat"}]}}, "notices": [], "overlay": ["beam-free", "claude-haiku-5-5", "crouton-alpha-free", "deepseek-v4-pro", "deepseek-v4.1-flash", "gemini-4-argon", "glm-5.2", "glm-5.3", "glm-5.3-flash", "gpt-5.6-luna", "gpt-6-luna", "grok-4.7", "hy3", "hy4", "hy4-preview", "iceman-contributor-free", "kimi-k2.7-code", "kimi-k3", "kimi-k3.1-pro", "longcat-2.0", "mimo-v2.5", "mimo-v2.5-pro", "mimo-v2.6-flash", "mimo-v2.6-pro", "minimax-m3", "minimax-m3.1-flash", "muse-spark-1.2-contributor", "muse-spark-1.3-contributor", "qwen3.7-plus", "qwen3.8-flash", "qwen3.8-max", "step-5-preview"], "pi_version": "1.5.0", "rule": {"exclude": [{"date": "2026-10-17", "id": "step-5-preview-free", "reason": "In the freshly fetched opencode-go overlay, but every call fails with \"Upstream request failed: Model is unavailable\" (loop round 1 and the runner's probe, both 2026-10-17); excluding it saves a call that fails every time until the model is served."}, {"date": "2026-11-06", "id": "iceman-contributor-free", "reason": "New in the live Go catalog on 2026-11-06 and picked as the whole free swarm by prepare-loop; \"contributor\" ids on Go have meant that request data may be used for training, and the maintainer's decision of 2026-10-17 (question Q-12) keeps such models off. The Go page's privacy table, read 2026-11-06, confirms it: 'Iceman Contributor Free | Yes | Not ZDR'. A bridge until one central per-use-case model policy exists (bead coding-harness-k0ub with coding-harness-wq1m); maintainer, 2026-11-06, morning question Q-M9, option A."}, {"date": "2026-11-06", "id": "cat-jam-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it, so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}, {"date": "2026-11-06", "id": "longcat-2.5-preview-free", "reason": "New in the live Go catalog on 2026-11-06; the privacy table of the Go page (https://opencode.ai/docs/go, read 2026-11-06) does not list it (only LongCat-2.0), so its training and retention terms are unknown. Excluded until the page lists it as not training on request data; maintainer, 2026-11-06."}], "hinweis": "Class admission instead of individual declarations: every id this run's forced live catalog refresh finds under the provider, matching the suffix or an include, reviews the implementation diff with no tools (ADR 0021, decision 3). The retention and training terms of these ids are NOT read; this acceptance covers the diff-only review purpose alone \u2014 no paid model, no Zen id and no interactive session runs on it.", "id_suffix": "-free", "include": [], "input": "implementation-diff", "provider": "opencode-go"}, "selected": [], "source": "pi.dev"}, "paid": {"flash": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0"], "ladder": ["deepseek-v4.1-flash", "mimo-v2.6-flash", "longcat-2.0", "glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"], "rungs": ["glm-5.3-flash", "hy3", "mimo-v2.6-pro", "hy4-preview", "kimi-k2.7-code", "deepseek-v4-pro", "glm-5.3", "kimi-k3"]}}

Kept from the loop record:

> Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).
> Notice: paid models skipped: qwen3.8-flash (the model qwen3.8-flash was skipped on 2026-10-17: wire API not measured); gpt-6-luna (the model gpt-6-luna was skipped on 2026-10-17: wire API not measured); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-10-17: wire API not measured); minimax-m3 (the model minimax-m3 was skipped on 2026-10-17: wire API not measured); qwen3.7-plus (the model qwen3.7-plus was skipped on 2026-10-22: wire API not measured); qwen3.8-max (the model qwen3.8-max was skipped on 2026-10-22: wire API not measured); grok-4.7 (the model grok-4.7 was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-10-30: wire API not measured (the Go page names the Responses endpoint)); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint); the live catalog lists only gemini-4-argon-contributor); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); minimax-m3.1-flash (the model minimax-m3.1-flash was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); step-5-preview (the model step-5-preview was skipped on 2026-10-30: not in the live Go catalog (2026-10-30); the catalog lists step-5-preview-free); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).
> Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor.
> longcat-2.0 failed: pi call failed: exit 1 (Response was truncated: the model reached its output token limit.); replaced by glm-5.3-flash
> The diff was cut: the change diff was cut at 2000 of 2089 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> The diff was cut: the change diff was cut at 2000 of 2547 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> The diff was cut: the change diff was cut at 2000 of 2549 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> The diff was cut: the change diff was cut at 2000 of 2596 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> kimi-k2.7-code reported no finding.
> The diff was cut: the change diff was cut at 2000 of 2667 lines. A clean answer over a cut diff does not end the loop; the rest of the change needs a round of its own.
> From kimi-k2.7-code:
> The answer was not only six-cell rows; what is not one is kept below as it came.
> 
> No finding.

<!-- End of released loop record -->

Stage-2 call, 2026-11-07: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 919 files, 3590 commits, 12 rules.

Stage-2 call, 2026-11-08: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 919 files, 3608 commits, 12 rules.
