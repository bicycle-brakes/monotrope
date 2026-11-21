---
title: "Findings — deadline-stop-flake"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-j1i5
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — deadline-stop-flake

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1162 files, 5257 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1165 files, 5261 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1165 files, 5267 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S1 | BLOCKER | SPEC | spec-review | plans/changes/deadline-stop-flake/spec.md:27, :54, :57, :62; decisions.md:28 | [AMBIGUITY] The spec does not say what happens if the trace finds no leak, and that is the likely result. The 2026-11-08 failure ran on an older test body that used real `sleep` 0.5 s / 10 s in `world.script` against a real 2 s round (archive/2026-11-16-address-drift-warning/findings.md:159-165). The runner-clock change, archived 2026-11-16 (plan.md:78), later moved this exact test to `FakeClock` + `ScriptedPrograms`. Yet decisions.md:28 still says "some part of the deadline path still reads real time" because of that failure, and tells the attempt to "name the one the fake clock does not cover". Reading A: a trace that finds no leak, plus its report (spec:62), is a finished change: a docs-only PR that carries `Closes-Bead: coding-harness-j1i5`, with the red/green item of the DoD waived. Reading B: finding no leak means the attempt stopped. There is no PR, the bead stays open, and the DoD (spec:54 red→green, :57 closes bead) cannot be met. Nothing in the spec says which reading holds, or whether spec:27 or decisions.md:28 decides whether a leak exists. | Opus | open | — |
| S2 | MAJOR | SPEC | spec-review | decisions.md:37-38; spec.md:38 | Missing decision: where the repair goes when the leak is not a clock read in `scripts/stage2.py`. decisions.md:38 decides only two cases: in the runner through `clock_now`, or in the test helper. But decisions.md:37 tells the trace to look at waits too (`threading` waits, `Event.wait`, `join` timeouts, subprocess timeouts). `clock_now` (`scripts/stage2.py:699`) only reads the time, so it cannot carry a wait. The launch path also leaves `stage2.py`: `launch` calls `verify_lock.end_lingering_group`, which calls `time.monotonic`/`time.sleep` directly (`scripts/verify_lock.py:918-922`), and `dispatch_go` calls into `stage2_go`. The spec does not say whether the attempt may add a wait seam to `stage2.py`, whether it may widen `tests/runner_clock_guard.py`, or whether `verify_lock.py`/`stage2_go.py` are in scope. Whoever implements it would have to decide that alone. | Opus | open | — |
| S3 | MAJOR | SPEC | spec-review | plans/changes/deadline-stop-flake/spec.md:38-39 | [AMBIGUITY] AC4 "all runner clock reads on the repaired path". Reading A: only `time`/`datetime` reads from `scripts/stage2.py` frames, which is everything the guard covers (`GUARDED_FILES`, `TIME_CLOCK_ATTRS`, tests/runner_clock_guard.py:55,63). A repair that replaces a real `Event.wait(t)`, `join(t)` or real-process timeout, or that edits `verify_lock.py`, then meets AC4 automatically, and the criterion can never fail. Reading B: every time read and timed wait on the review-loop deadline path, in any module. The existing guard cannot see those by design, so the refutation "the guard no longer catches such a bypass" cannot be built without widening the guard, and the word "existing" seems to rule that out. | Opus | open | — |
| S4 | MAJOR | SPEC | spec-review | plans/changes/deadline-stop-flake/spec.md:34-35 | [AMBIGUITY] AC2 "with the seconds granted for that call". The number in the record is computed in `run_reviewer` before `dispatch_go` (`scripts/stage2.py:3311-3313`). `launch` then recomputes the remaining time when it creates the process and hands it `min(timeout, left)` (`scripts/stage2.py:1066-1068`), with admission work in between. Reading A: the record contains a "seconds were left for this call" phrase. The current assertion (`tests/test_stage2.py:23831`) already checks that, so it holds today with no change. Reading B: the stated number must equal the timeout the replacement process actually got (`programs.waits()[…]["timeout"]`). That needs a new assertion, and it can fail today when the fake clock moves inside `dispatch_go`, which would force a change to the runner. The refutation names only a missing number, so under reading A a wrong number (a stale value, or "0 seconds" from `:.0f` on a sub-second remainder) does not fail AC2. | Opus | open | — |
| S5 | MAJOR | SPEC | spec-review | plans/changes/deadline-stop-flake/spec.md:32-33, :58, :62 | If no leak is found, no criterion can fail. AC1 starts "When the identified real-time dependency … is held", so with nothing identified it has no input. The fallback "stop and report the trace and measurements" (spec:62) has no criterion: nothing says what the trace must cover (which kinds of read or wait, which modules), so a one-line "nothing found" meets it. The DoD's "repeated targeted run" (spec:58) gives no repeat count and no parallel load. The bead's failure appeared only in a full `make verify` across six xdist lanes, and the test passed when run alone (decisions.md:26). A repeated run of the test alone stays green whether a load-dependent leak exists or not. | Opus | open | — |
| S6 | MINOR | SPEC | spec-review | plans/changes/deadline-stop-flake/spec.md:32, :34, :36 | [AMBIGUITY] Which test the criteria bind. The spec never names it; only decisions.md:26 does. AC1 says "a regression test", while AC2/AC3 say "the test". Reading A: AC1's forced regression is a new test, and AC2/AC3 bind `test_a_deadline_stop_names_the_round_limit` unchanged; it already asserts both (`tests/test_stage2.py:23830-23832`), so the normal, unforced path keeps its coverage. Reading B: the existing test is rewritten to hold the leak, AC2/AC3 bind the rewritten test, and the normal path is no longer tested. | Opus | open | — |
