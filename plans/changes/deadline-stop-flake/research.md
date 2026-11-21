---
title: "Research — deadline-stop-flake"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-j1i5
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# deadline stop flake — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1161 files, 5250 commits, 12 rules.

Stage-2 call, 2026-11-21: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash refuses with claude-code:unrecognized_model on 2026-11-21 (bead coding-harness-b5pu) · leak check clean over 1161 files, 5254 commits, 12 rules.

## Runner exploration — 2026-11-21

## Runner exploration: deadline-stop-flake, 2026-11-21

The change folder holds only the skeleton, with no spec, no decisions and no bead text. The bead `coding-harness-j1i5` sits in the Dolt tracker, which this phase cannot read. So the topic below is inferred from the code and the change name. The inference is the most likely reading, not a confirmed one.

### Suggested header addition

```
neighbours:
  - plans/changes/flaky-swarm-leak-test/research.md  (active, draft, same family: a load-timing or race flake in the swarm test suite, bead coding-harness-yb1l)
  - plans/changes/swarm-test-speed/spec.md           (active, bounded; names the same dispatcher and runner scripts as protected areas)
  - plans/changes/archive/2026-11-06-swarm-time-limits/spec.md (introduced the round deadline and the per-call allowance this change concerns)
  - plans/changes/archive/2026-11-06-research-swarm/spec.md    (introduced the dispatcher; records earlier load-timing flakes repaired by widening margins or by file handshakes)
```

The header of `research.md` carries no `neighbours:` list and no class declaration yet. The runner needs both before a complete swarm run.

### What exists today

- **The deadline logic is in the research dispatcher.** `scripts/stage2_research_dispatch.py`, function `dispatch`, takes a `deadline`, a `reserve` and a `clock` (default `time.monotonic`). Its inner `remaining()` returns `deadline - reserve - clock()`, and `out_of_time()` tests whether that is at or below zero. `launch_next` checks `out_of_time()` twice: once before the gate and once after the audit. Either check finishes the slot as `not-started-deadline`. The child's allowance is `min(slot.role_allowance, remaining())` (the launch step in `launch_next`). `supervise` kills the child as `timed-out` when `clock() - began >= allowance`, or as `cancelled` when the stage stops. A `grace` period applies while the child is reaped.
- **The round deadline is set in the stage2 runner.** `scripts/stage2.py` (the review-loop path, near `REVIEWER_MINUTES`) sets `deadline = monotonic_now() + REVIEWER_MINUTES * 60` once per round and shares it with replacements. The helper `remaining(deadline)` in the same file gives a replacement what is left of the round, and no fresh limit (DL-B-14). The research runner passes the same kind of deadline through `scripts/stage2_research_run.py` (`self.deadline`, the `CLOCK` injection point, and `PREPARATION_SECONDS`).
- **Most deadline tests inject a fake clock.** In `tests/test_stage2.py` the tests around the round deadline (for example `test_the_remaining_time_never_outlives_the_round_deadline`, `test_no_second_call_after_the_round_deadline`, `test_a_deadline_stop_names_the_round_limit`) use `FakeClock` with `run_past(deadline)`. In `tests/test_stage2_research_dispatch.py` the tests `test_deadline_rechecked_after_gate_before_launch`, `test_no_launch_inside_reserve_and_free_not_started_is_not_incomplete` and `test_child_allowance_is_lesser_of_role_and_remaining_before_reserve` also pass a constant `clock` lambda. In `tests/test_stage2_research_catalog.py` the deadline tests wait on a marker file or an event (bead coding-harness-jik), not on wall-clock delays.
- **One dispatcher test runs on the real clock.** `tests/test_stage2_research_dispatch.py`, `test_queue_wait_counts_against_total_and_child_times_out_at_allowance`, sets `deadline = time.monotonic() + 0.8`, `reserve=0.5`, `grace=0.5`, `per_provider_limit=1`. The first slot runs `sleeper(30)`, a child that prints `start`, sleeps 30 seconds and prints `end`. The test asserts that the first slot ends `timed-out` and started, that its stdout contains `"start"`, and that the second slot ends `not-started-deadline`. Its real-time window is about 0.3 s between the call and the first launch (`0.8 - 0.5`), and the first child's allowance is also about 0.3 s, measured from launch.
- **The Python helper timing is part of that window.** The `sleeper` template prints `start` only after the interpreter has booted. Interpreter boot therefore falls inside the 0.3 s allowance.
- **Checked and not there.** The grep over `scripts/` and `tests/` for `deadline` found no other test that combines a real `time.monotonic()` deadline with a sub-second margin. The polling loops that remain (`tests/test_stage2.py` around lines 2656 and 27001, `tests/test_stage2_research_catalog.py`) are watchdogs or use events.

### Where it lives

- Dispatcher: `scripts/stage2_research_dispatch.py` — `dispatch`, `launch_next`, `supervise`, `remaining`, `out_of_time`, `_stop_and_reap`, `TICK`, `PER_PROVIDER_LIMIT`.
- Round deadline: `scripts/stage2.py` — `remaining`, the review-loop round deadline near `REVIEWER_MINUTES`, `run_swarm`, `run_reviewer`.
- Research runner: `scripts/stage2_research_run.py` — `CLOCK`, the run `deadline` property, `PREPARATION_SECONDS`.
- Tests: `tests/test_stage2_research_dispatch.py` (helpers `module`, `sleeper`, `make_slot`, `Harness`, `run`, `by_id`; the real-clock test at the end of the deadline group), `tests/test_stage2.py` (`FakeClock`, the deadline tests around lines 1256–1280, 9325–9420, 21722, 23703–23840), `tests/test_stage2_research_catalog.py` (deadline tests on events).

### What is unclear

- **The bead's failure is not known.** Neither the bead text nor the CI logs were readable. The real-clock dispatcher test is the only candidate I found that fits a "deadline stop" flake, but I have not confirmed that it is the one the change means. [GAP]
- **The mechanism is inferred, not reproduced.** The likely chain: under load, the time from `dispatch` start to the first launch exceeds the 0.3 s window, so the first slot ends `not-started-deadline`, or the child is killed before it prints `start`, so `"start" in stdout` fails. No reproduction was run (read-only tools). [GAP]
- **Which assertion fails is not known.** The failing assertion would show whether the first slot never launched or launched and was killed before its first output.
- **Repetition is unmeasured.** No repetition protocol for this test exists in the tree.
- **The intended repair boundary is not written anywhere.** Whether the fix belongs in the test (a fake clock like the neighbouring tests use) or in the production code's timing is not stated in any artifact. The swarm-test-speed spec protects `scripts/stage2_research_dispatch.py` and `scripts/stage2_research_run.py` ("the call-boundary and scan behaviour stays intact", `plans/changes/swarm-test-speed/spec.md`), so a production change there needs that spec's boundary read first.

### Which files a change would have to touch

- `tests/test_stage2_research_dispatch.py` — the real-clock test and possibly its helper `sleeper`, if the fix replaces wall-clock timing with an injected clock or a marker file.
- `scripts/stage2_research_dispatch.py` — only if the fix moves a production timing rule. The swarm-test-speed spec protects this file.
- `tests/test_stage2_research_dispatch.py` may also need a `FakeClock`-style helper, which the neighbouring tests in `tests/test_stage2.py` already have in a different form.
- No evidence points to `scripts/stage2.py` or `scripts/stage2_research_run.py` for this flake. They are named here only because they hold the deadline's producer side.
