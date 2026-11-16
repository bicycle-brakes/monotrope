---
title: "Decisions — runner-clock"
category: decisions
status: accepted
implementation_status: done
date: 2026-11-14
created: 2026-11-14
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-pph3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, flaky-tests, clock, runner]
---

# runner-clock — Decisions

Class: bounded (bead coding-harness-pph3).

## Q-1 · How the load-flaky timing tests become robust

asked: 2026-11-14
answer: "ja" to widening the bead to the class (after asking whether injecting a clock is a durable and smart solution): the runner reads time only through one clock function; a source test with no exemption list forbids any direct time read in the runner; both load-flaky tests and every other runner test with small real-time limits use an injected fake clock.
answered_by: maintainer
status: answered
context: |
  Topic: tests/test_stage2.py::test_verification_admission_is_outside_execution_timeout sets the step limit to 2 seconds and lets real processes sleep; a second test, test_before_admission_execution_budget_is_shared_and_wait_free, uses a real queue holder and a 30-second limit.
  Intention: under the load of several lanes both failed on 2026-11-14 and passed alone; one failure cost a phase-6 review with its full make verify of about ten minutes.
  Today: scripts/stage2.py reads time directly at 7 call sites (time.monotonic, time.time, time.sleep or time.perf_counter, counted 2026-11-14 on origin/main); the tests wait real seconds.
  Repository change: one clock function in the runner that every time read goes through, a source test that no runner code reads time directly, and the timing tests moved to a fake clock the test advances itself.
  Architecture change: none beyond one choke point for time in the runner, the same pattern as run_git.

In the context of tests that fail under machine load because they wait real seconds, facing a choice between an injected clock, larger margins and serial runs, we decided for one clock choke point with a source test and a fake clock in the tests, to achieve that the whole class of load-dependent timing tests closes instead of one test, accepting a change at every direct time read of the runner. — 2026-11-14

## Q-2 · How the clock guard closes instead of growing case by case

asked: 2026-11-15
answer: "stop case-by-case repair of the static clock guard; the runtime becomes the choke point": in the test session one autouse fixture wraps the machine-clock reads the runner could use (`time.monotonic`, `time.time`, `time.perf_counter` with their nanosecond variants, the conversions `localtime`, `gmtime`, `ctime`, `asctime` without an instant and `strftime` without a tuple, `clock_gettime` with its nanosecond variant, and `datetime.now`, `utcnow`, `today` and `date.today`); a read made from the runner's code but not through `clock_now` fails the test, decided from the caller frame, with the standard library, test code and `clock_now` itself allowed; the mechanism must not be bypassable by aliasing, defaults or `__call__`, so references bound at import are covered too. The static guard stays as a cheap advisory check, and its Boundary names the runtime check as the closing mechanism. Phase-6 rows F6-1 and F6-2 are closed by the runtime check.
answered_by: maintainer
status: answered
context: |
  Topic: the source test that forbids direct clock reads in the runner (spec criterion 2) reads the module's syntax tree; the phase-6 review found two more shapes it accepts, `time.monotonic.__call__()` and a default argument that reads the clock at import (findings rows F6-1 and F6-2).
  Intention: these were the sixth and seventh findings of the same mechanism after three review-loop rounds; each repair closed one spelling and the next review found another, so the static reading cannot reach a closed set.
  Today: tests/test_stage2.py holds a structural source guard with a measured set of clock functions; nothing checks at run time where a clock read comes from.
  Repository change: a test-session guard in tests/conftest.py and tests/runner_clock_guard.py wraps the clock functions before the runner is imported and fails a test on a runner read outside clock_now; the clock sets move there and the static guard imports them; spec criterion 2, its Boundary and the plan's ledger name the runtime check.
  Architecture change: none in production code; the choke point for the runner's time moves from a source reading to the test session's run time.

In the context of a static source guard that review keeps finding new bypasses of, facing a choice between repairing one more spelling and checking at run time, we decided for a runtime check in the test session that judges the calling frame of every machine-clock read, to achieve a closed mechanism that aliasing, defaults and `__call__` cannot bypass, accepting that only executed runner lines are checked and the static guard stays as an advisory reading for the rest. — 2026-11-15

[DETAIL] The guarded file is `scripts/stage2.py` alone, the runner as the spec's Terms define it; the other `scripts/stage2*.py` modules and the protected components keep their own clock boundaries.

[DETAIL] Census, 2026-11-15 at `6ecd3636` with the guard's wrappers recording instead of refusing over every `scripts/stage2*.py` file, running `tests/test_stage2*.py` in parallel: the real runner made no clock read outside `clock_now` (every recorded `stage2.py` read was a planted test snippet); `stage2_availability.py` (`now`), `stage2_research_run.py`, `stage2_research_dispatch.py`, `stage2_research_store.py`, `stage2_research_history.py` and `stage2_research_snapshot.py` read the clock directly and stay outside the guarded set.
