---
title: "Decisions — flaky-popen-signal"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-oag7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, flaky-test, signals, stage2-runner]
---

# flaky-popen-signal — Decisions

Class: bounded (bead coding-harness-oag7).

## What the bead and the CI log say (read 2026-11-21 by the orchestrator)

The explore could not read the tracker or the CI logs; the orchestrator read both.

- Bead: "tests/test_stage2.py::test_a_signal_during_process_creation_leaves_no_child failed on CI with 'a child survived cancellation during Popen' on main (run 44591912821, [True-SIGINT], 2026-11-19) and on PR #418 ([True-SIGTERM], 2026-11-20), each time as the only red test of about 6400; other runs of the same code passed. Find the race and make the test deterministic." Notes: a sibling, `test_an_interrupt_on_the_main_thread_kills_the_launched_group[KeyboardInterrupt]` ("descendant survived main's interrupt"), failed the same way on PR #419; the CI research swarm of 2026-11-21 adds runs 44352084851 (merge group of PR #410) and 44697459207, and says "Fix the race at its cause, no retry decorator."
- CI log of run 44591912821 (`gh run view --log-failed`): the failing case is `worker=True`, `SIGINT`; the runner printed "interrupted: the run stopped; 1 running program group(s) killed."; after the 5-second watchdog, `_child_alive` still reported the forked child alive (`tests/test_stage2.py:26497`). Both recorded failures are `worker=True`: the signal reaches the main thread while the worker thread is inside `subprocess._fork_exec`, before `Popen` returns the child to `launch`.

## SKIP · interview

status: skipped
reason: The bead fixes the goal and the constraint (find the race at its cause, make the test deterministic, no retry decorator); the maintainer approved this lane's kind of work for the run to 2026-11-23 10:00 and asked for no question windows until then. The details below are [DETAIL] items; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **First establish the interleaving, then fix.** The spec names the suspected window — a child whose `Popen` has not returned to `launch` in a worker thread when the main thread's handler kills "the live groups" — and requires a deterministic reproduction that forces that ordering (for example a barrier inside the patched `_fork_exec` that holds the worker until the main thread's handler has run), red on today's code. Reason: the bead says "find the race"; a forced reproduction is the proof, as in the earlier flaky-swarm-leak-test change (its row L3-1).
- **Fix at the cause, in production code when the race is there.** If the window is in `scripts/stage2.py` (`launch`, `defer_launch_signals`, `kill_live`), the fix makes a child created during an interrupt killed and reaped before `launch` returns or raises, whichever thread created it; the same pattern in `scripts/verify_run.py` (`_hold_launch_signals`) is checked and fixed alike or stated as not affected with its reason. If the window is only in the test's own cleanup or liveness verdict, the test is fixed instead and the spec says why production is safe. Reason: "no retry decorator"; one mechanism, both copies.
- **The sibling test is in scope** (`test_an_interrupt_on_the_main_thread_kills_the_launched_group[KeyboardInterrupt]`), when the same mechanism explains it; otherwise it gets its own bead. Reason: the bead's notes name it as the same failure shape.
- **No timing widening as the fix.** Raising the 5-second watchdog or adding sleeps is not a remedy. Reason: the watchdog bounds a wedged reap and is never the verdict (the test's own comment).
