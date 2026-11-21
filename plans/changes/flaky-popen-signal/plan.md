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

1. In `tests/test_stage2.py`, rewrite `test_a_signal_during_process_creation_leaves_no_child` to force the relevant order, using an isolated subprocess for real signals and an independent coordinator to release a blocked worker; join that worker before judging its child. Establish the actual order and collect child and leader state. Run a controlled reproduction against the faulty pre-fix production code or test helper first and record the command, commit, trace and failure; if the suspected window does not reproduce the observed failure, investigate the test's liveness and cleanup instead of asserting the hypothesis as fact. A watchdog bounds a stuck test, never supplies its verdict; clean up owned processes.
2. In `scripts/stage2.py`, if the controlled failure is in production, repair the established race at the shared launch/cancellation boundary, including worker and main-thread launches, without introducing a second process-launch route. If the cause instead lies in test liveness or cleanup, repair `tests/test_stage2.py` and record evidence that production cleanup is safe. Preserve cancellation, bounded drain and refusal of late launches.
3. In `tests/test_stage2.py`, cover SIGINT and SIGTERM on both launch threads, the forced ordering, actual child termination and reaping, late-launch refusal and the running-descendant case; ensure the child cannot pass by natural expiry. Investigate every recorded sibling failure, including Terminated on PR #404 and KeyboardInterrupt on PR #419, against the established mechanism; rewrite the existing sibling case where that mechanism applies. For each established different cause, record cause, evidence and test IDs under `Follow-up for the orchestrator` in the attempt record in `plans/changes/flaky-popen-signal/findings.md`; the orchestrator files the follow-up bead.
4. Inspect `scripts/verify_run.py` from `run_verification` through `gate_process` and its signal handler, including the calling thread and cleanup boundary. Record why the established race does or does not apply; if it does, change `scripts/verify_run.py` and add a controlled regression in `tests/test_ci.py`. Do not assume that its similarly named signal deferral makes it equivalent.
5. If the cause is test-only, record the evidence that production cleanup is safe. If no cause is established and reproduced within two hours, stop, report attempted interleavings and results to the orchestrator, and ship no speculative fix or test change. In `plans/changes/flaky-popen-signal/plan.md`, replace ledger markers when their tests exist; the runner owns the measured time and findings records. The orchestrator records the baseline, cause and both assessments in the pull request and handles any follow-up tracker write. No held path requires an implementation edit. No design, ADR or file deletion is planned.

Verification:

```sh
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_a_signal_during_process_creation_leaves_no_child — the controlled pre-fix result fails to expose the evidenced cause or the ordering is uncontrolled; the orchestrator records the baseline trace and commit.
- 2: not yet written tests/test_stage2.py::test_cancellation_during_timed_launch_stops_and_reaps_the_child — a child remains live or unreaped for either signal or launch thread.
- 3: tests/test_stage2.py::test_a_launch_after_the_interrupt_starts_no_program — a late launch writes its marker.
- 4: tests/test_stage2.py::test_an_interrupt_on_the_main_thread_kills_the_launched_group — the descendant survives or the leader is not reaped.
- 5: not a test — the phase-6 review checks each recorded sibling failure's assessment against its evidence; a missing or unsupported assessment fails.
- 6: not a test — the phase-6 review checks the verification-runner assessment and any required regression against the actual call path and cancellation behavior.
- 7: tests/test_stage2.py::test_a_signal_during_process_creation_leaves_no_child — the original test remains uncontrolled or a natural child exit, delay, retry or wider watchdog supplies the verdict; phase-6 review also checks the applicable sibling cases.
- 8: not a test — the phase-6 review checks the findings handoff for each different established cause, its evidence and test IDs; a missing detail fails.
- 9: not a test — on appetite expiry the orchestrator checks the stop report for tried interleavings and results and verifies that no speculative fix or test change is shipped; omission fails.
- 10: not a test — if the defect is test-only, the phase-6 review checks the production safety evidence against the observed ordering; unsupported safety fails.

## Time used

2026-11-21 15:35:02–15:37:19 UTC, 137 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 15:42:17–15:44:36 UTC, 140 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
