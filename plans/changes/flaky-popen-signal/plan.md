---
title: "Plan — flaky-popen-signal"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-oag7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, signals, stage2-runner]
---

# Plan — flaky-popen-signal

```text
For you:     Interrupted process launches leave no child running, and the flaky signal test has a controlled verdict.
Done when:   A controlled baseline exposes the cause, regression tests pass, and make verify is green.
Appetite:    2 hours for phase 4, including repairs; stop at the limit.
Not now:     CI retries, timing workarounds, and unrelated process-supervision changes.
Pre-mortem:  suppose it failed: most likely because the test does not force the actual failure ordering.
Starts unless you say stop.
```

## Implementation

1. In `tests/test_stage2.py`, isolate a real-signal reproduction in a subprocess and synchronize the worker after child creation and before `Popen` returns, cancellation on the main thread, and release through an independent coordinator; establish the actual order and collect child and leader state. Run it against the unmodified baseline first and record the command, commit, trace and failure; if that suspected window does not reproduce the observed failure, investigate the test's liveness and cleanup evidence instead of asserting the hypothesis as fact. A watchdog bounds a stuck test, never supplies its verdict; always clean up the owned processes.
2. In `scripts/stage2.py`, if the controlled failure is in production, repair the established race at the shared launch/cancellation boundary, including worker and main-thread launches, without introducing a second process-launch route. If the cause instead lies in test liveness or cleanup, repair `tests/test_stage2.py` and record evidence that production cleanup is safe. Preserve cancellation, bounded drain and refusal of late launches.
3. In `tests/test_stage2.py`, cover SIGINT and SIGTERM on both launch threads, the forced ordering, actual child termination and reaping, late-launch refusal and the running-descendant case; ensure the child cannot pass by natural expiry. Compare the sibling failure with the established mechanism and record the evidence. If its cause differs, hand the evidence and a separate follow-up request to the orchestrator, the sole tracker writer.
4. Inspect `scripts/verify_run.py` from `run_verification` through `gate_process` and its signal handler, including the calling thread and cleanup boundary. Record why the established race does or does not apply; if it does, change `scripts/verify_run.py` and add a controlled regression in `tests/test_ci.py`. Do not assume that its similarly named signal deferral makes it equivalent.
5. In `plans/changes/flaky-popen-signal/plan.md`, replace ledger markers when their tests exist; the runner owns the measured time and findings records. The orchestrator records the baseline, cause and both assessments in the pull request and handles any follow-up tracker write. No held path requires an implementation edit. No design, ADR or file deletion is planned.

Verification:

```sh
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_process_creation_cancellation_forces_the_failure_order — the pre-fix result does not expose the evidenced failure or the ordering is uncontrolled; the orchestrator records the baseline trace and commit.
- 2: not yet written tests/test_stage2.py::test_cancellation_during_timed_launch_stops_and_reaps_the_child — a child remains live or unreaped for either signal or launch thread.
- 3: tests/test_stage2.py::test_a_launch_after_the_interrupt_starts_no_program — a late launch writes its marker.
- 4: tests/test_stage2.py::test_an_interrupt_on_the_main_thread_kills_the_launched_group — the descendant survives or the leader is not reaped.
- 5: not a test — the phase-6 review checks the sibling assessment and, for a different cause, the orchestrator's follow-up handoff against its evidence.
- 6: not a test — the phase-6 review checks the verification-runner assessment and any required regression against the actual call path and cancellation behavior.
- 7: not yet written tests/test_stage2.py::test_process_creation_cancellation_forces_the_failure_order — a natural child exit, delay, retry or wider watchdog supplies the verdict; phase-6 review also inspects the signal tests for those workarounds.

## Time used

2026-11-21 15:35:02–15:37:19 UTC, 137 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
