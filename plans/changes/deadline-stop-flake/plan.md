---
title: "Plan — deadline-stop-flake"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-j1i5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, flaky-test, review-loop]
---

# Plan — deadline-stop-flake

```text
For you:     The deadline-stop test reliably checks that a replacement is stopped by the shared round limit.
Done when:   A forced regression is red before the repair and green after it, repeated targeted checks and make verify pass.
Appetite:    2 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Longer limits, sleeps, retries, changed timeout policy or the separate research-dispatcher test.
Pre-mortem:  suppose it failed: most likely because a real wait or uncontrolled thread still escapes the fake clock.
Starts unless you say stop.
```

## Scope and sequence

Baseline `617de302` on 2026-11-21; `bounded` needs neither design nor ADR. There is no plan template in `templates/` at this baseline. Explore used the Stage-1 fallback `claude-haiku-5-5` via `claude-code-plan` because GLM 5.3 Flash refused with `claude-code:unrecognized_model` on 2026-11-21.

1. Trace clock reads and waits from the shared deadline through `review_loop`, `run_swarm`, `run_reviewer`, `dispatch_go`, `launch`, `FakeClock` and `ScriptedPrograms`, including thread scheduling, event waits, joins and subprocess timeouts. Identify the actual dependency before choosing a fix; the 2026-11-08 failure predates the present fake-clock fixture.
2. In `tests/test_stage2.py`, add `test_deadline_stop_survives_delayed_scheduling`: force the identified dependency past the relevant boundary with deterministic coordination and capture a failing run before the fix. Assert the replacement starts, receives a positive remaining allowance, times out, and writes the round-limit diagnostic with seconds; a wall-clock timeout may serve only as a deadlock watchdog. Keep `test_a_deadline_stop_names_the_round_limit` and its assertions; adjust its fixture or helper where the leak lies.
3. If the leak is in runner timing, change `scripts/stage2.py` at the existing clock seam and retain the guard in `tests/runner_clock_guard.py`; if it is confined to the test helper, change only `tests/test_stage2.py`. Do not add a second runner clock source or alter timeout semantics. If the trace shows another path is necessary, stop and report it to the orchestrator instead of silently expanding scope.
4. Run the forced regression against the original and repaired behavior, record both outcomes, then repeat the targeted tests and run `make verify`. If no dependency is found within the appetite, stop and record traced paths and measurements in `plans/changes/deadline-stop-flake/findings.md`; do not claim the criterion is met.

Do not touch the research dispatcher, the research runner, or held paths. `plans/changes/deadline-stop-flake/findings.md` changes only for the stop report; `tests/runner_clock_guard.py` is read and exercised, not changed. No other file is planned.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_deadline_stop_survives_delayed_scheduling — a forced scheduling dependency prevents the intended deadline-stop outcome
- 2: tests/test_stage2.py::test_a_deadline_stop_names_the_round_limit — the replacement is not stopped or its record lacks the round limit and granted seconds
- 2: not yet written tests/test_stage2.py::test_deadline_stop_survives_delayed_scheduling — delayed scheduling prevents the replacement timeout or its round-limit record
- 3: tests/test_stage2.py::test_a_deadline_stop_names_the_round_limit — the record says reviewer time limit instead of round limit
- 4: tests/test_stage2.py::test_runner_clock_is_the_only_time_source — a runner clock read bypasses the boundary
- 4: tests/test_stage2.py::test_runner_clock_guard_rejects_bypasses — the guard accepts a planted bypass

## Verification

```sh
python3 -m pytest -q tests/test_stage2.py::test_deadline_stop_survives_delayed_scheduling tests/test_stage2.py::test_a_deadline_stop_names_the_round_limit
for run in {1..10}; do python3 -m pytest -q tests/test_stage2.py::test_deadline_stop_survives_delayed_scheduling tests/test_stage2.py::test_a_deadline_stop_names_the_round_limit || break; done
make verify
```

Run the first command with the forced regression before and after the repair; the ten-run loop is supporting evidence, not a substitute for the forced red/green result.

## Time used

2026-11-21 18:01:53–18:04:22 UTC, 148 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
