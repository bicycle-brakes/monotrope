---
title: "Findings — architecture-reconcile"
category: findings
status: draft
implementation_status: none
date: 2026-10-31
created: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-190
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — architecture-reconcile

Stage-2 call, 2026-10-31: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 802 files, 2898 commits, 12 rules.

## Draft validation — 2026-10-31

Baseline: `b58c72e75af3283f4cc9e39148ecfb02642026f9`, with this attempt's
uncommitted artifacts. No phase-2a rows were present to resolve.

- `python3 scripts/check_interview_minimums.py --change architecture-reconcile`:
  exit 0; the bounded change's existing reasoned skip is accepted.
- `python3 scripts/check_research_handoff.py --change architecture-reconcile`:
  exit 0; no research-swarm/v2 handoff applies.
- `python3 scripts/check_criterion_ledger.py`: exit 0; the new plan's eight
  criteria have review-based ledger entries. No new tests are proposed for
  this documentation comparison.
- `python3 scripts/check_docs.py --base plans/changes/architecture-reconcile`
  initially found missing `category` and `created` metadata in `research.md`
  and `decisions.md`. Only those header fields were supplied; the research,
  interview skip, class and decisions remain unchanged. The rerun exited 0.
- `python3 scripts/validate_change_artefacts.py --check`: exit 2; the script
  does not exist at this baseline. Its implementation is outside this change;
  the validator gate is not claimed green.
- Registry/index work and full verification remain with the runner or
  orchestrator. No tracker or live PR state was read: the tracker reader can
  resolve to storage outside the worktree, beyond this attempt's reading
  boundary. No commit, tracker write or source architecture edit was made.

> Attempt 1 (codex): the runner put back what a draft may not change:
> - `plans/changes/architecture-reconcile/decisions.md`

Stage-2 call, 2026-10-31: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 805 files, 2900 commits, 12 rules.

> The attempt edited findings.md; the runner restored it before the post-run checks, and the attempt passed them.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.2 · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 806 files, 2904 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model longcat-2.0 · leak check clean over 806 files, 2907 commits, 12 rules.

Stage-2 call, 2026-10-31: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 806 files, 2907 commits, 12 rules.

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
> - L1-8: no fixed line
> - L1-9: no fixed line
> - L1-10: no fixed line
> - L1-11: no fixed line
> - L1-12: no fixed line
> - L1-13: no fixed line
> - L1-14: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/architecture-reconcile/stage2/attempts/architecture-reconcile/attempt-1-20261031T172140035376Z-af9f6eae.md
> ```

Stage-2 call, 2026-10-31: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 806 files, 2908 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
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
> - L1-8: no fixed line
> - L1-9: no fixed line
> - L1-10: no fixed line
> - L1-11: no fixed line
> - L1-12: no fixed line
> - L1-13: no fixed line
> - L1-14: no fixed line
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/architecture-reconcile/stage2/attempts/architecture-reconcile/attempt-2-20261031T172140035376Z-af9f6eae.md
> ```

Stage-2 call, 2026-10-31: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 806 files, 2909 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/research/2026-10-31-architecture-reconciliation.md` +21 -19
> - `plans/changes/architecture-reconcile/decisions.md` +3 -1
> - `plans/changes/architecture-reconcile/plan.md` +3 -2
> - `plans/changes/architecture-reconcile/research.md` +7 -11
> - `plans/changes/architecture-reconcile/spec.md` +1 -1
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [pytest] $ lauf_cmd
> [… 74 lines of this gate left out …]
>         Fault this pins: a dead holder or waiter blocking progress forever, a
>         signal releasing the lock before the child's group is gone, and a
>         supervisor releasing ownership while its protected child still runs.
>         """
>         state = tmp_path / "state"
>         holder_file = state / "coding-harness" / verify_lock.HOLDER_NAME
>     
>         # a holder killed mid-run cannot obstruct the next admission
>         started = tmp_path / "started-a.json"
>         victim = _supervised(state, RECORD_BODY, {"PROBE_SLEEP": "30", "PROBE_STARTED": str(started)})
>         assert _wait_until(holder_file.is_file), "the victim never acquired admission"
>         assert _wait_until(started.is_file), "the victim never started its protected child"
>         child_pid = int(started.read_text(encoding="utf-8"))
>         os.kill(victim.pid, signal.SIGKILL)
>         os.kill(child_pid, signal.SIGKILL)
>         victim.wait(timeout=10)
>         after = tmp_path / "after-a.json"
>         survivor = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(after), "PROBE_SLEEP": "0.1"})
>         assert survivor.wait(timeout=60) == 0 and after.is_file(), "a dead holder blocked the next admission"
>     
>         # a waiter killed in the queue cannot obstruct the survivors either
>         with fake_holder(state):
>             waiter = _supervised(state, RECORD_BODY, {"PROBE_SLEEP": "30"})
>             assert _wait_until(lambda: len(_records(state)) >= 1), "the waiter never registered"
>             os.kill(waiter.pid, signal.SIGKILL)
>             waiter.wait(timeout=10)
>         after_two = tmp_path / "after-b.json"
>         follower = _supervised(state, RECORD_BODY, {"PROBE_OUT": str(after_two), "PROBE_SLEEP": "0.1"})
>         assert follower.wait(timeout=60) == 0 and after_two.is_file(), "a dead waiter blocked the survivor"
>     
>         # SIGTERM: the child's group is cleaned up, then the lock is released
>         started_c = tmp_path / "started-c.json"
>         out_c = tmp_path / "child-c.json"
>         interrupted = _supervised(
>             state, RECORD_BODY, {"PROBE_SLEEP": "5", "PROBE_STARTED": str(started_c), "PROBE_OUT": str(out_c)}
>         )
>         assert _wait_until(started_c.is_file), "the interrupted entry never started its protected child"
> >       child_c = int(started_c.read_text(encoding="utf-8"))
> E       ValueError: invalid literal for int() with base 10: ''
>
> tests/test_verify_lock.py:438: ValueError
> =============================== warnings summary ===============================
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[findings-no-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-record]
> tests/test_stage2.py::test_review_refuses_a_held_record_lock[no-findings-no-record]
>   /opt/homebrew/Cellar/python@3.12/3.12.15_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=42322) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     self.pid = os.fork()
>
> tests/test_stage2.py::test_a_failed_record_write_leaves_the_record_as_it_was
>   /Users/mikypiky/coding-harness/.claude/worktrees/architecture-reconcile/tests/test_stage2.py:17138: DeprecationWarning: This process (pid=42335) is multi-threaded, use of fork() may lead to deadlocks in the child.
>     pid = os.fork()
>
> -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
> =========================== short test summary info ============================
> FAILED tests/test_verify_lock.py::test_exit_interrupt_and_dead_waiter_release_admission
> 1 failed, 4390 passed, 17 skipped, 5 warnings in 580.15s (0:09:40)
> ── [pytest] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 24933 earlier lines left out …]
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
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/architecture-reconcile/stage2/attempts/architecture-reconcile/attempt-3-20261031T172140035376Z-af9f6eae.md
> ````

Stage-2 call, 2026-10-31: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 806 files, 2912 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 806 files, 2915 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model hy3 · leak check clean over 806 files, 2916 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 806 files, 2917 commits, 12 rules.

Stage-2 call, 2026-10-31: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 806 files, 2921 commits, 12 rules.

Stage-2 call, 2026-10-31: review-loop · endpoint opencode-go · model hy4-preview · leak check clean over 806 files, 2923 commits, 12 rules.

## Orchestrator check — 2026-10-31

`python3 scripts/check_docs.py --base docs/research` at `ee44684c`: no finding
in `docs/research/2026-10-31-architecture-reconciliation.md`; the 23 findings
the run lists sit in older research notes this change does not touch
(missing `category`/`created` fields). Recorded for review row L5-3.

Stage-2 call, 2026-10-31: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 806 files, 2924 commits, 12 rules.
