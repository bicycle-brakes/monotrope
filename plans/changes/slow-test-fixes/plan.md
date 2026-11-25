---
title: "Plan — slow-test-fixes"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.16
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, tests, speed]
---

# Plan — slow-test-fixes

```text
For you:     Three existing tests avoid repeated work while keeping their checks.
Done when:   The preserved checks pass, before and after durations are recorded, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     The finder sleep, other speed work, production changes and verification-gate changes.
Pre-mortem:  suppose it failed: most likely because a bundled outcome hides a missing violation.
Starts unless you say stop.
```

Bounded change: no design or ADR. Explore used the Stage-1 route, `claude-haiku-5-5` via `claude-code-plan`, because GLM 5.3 Flash through Z.ai had reached its weekly limit until 2026-11-29 (research, 2026-11-25).

## Files and steps

1. Before editing, record the base revision and measure each named test using the command below; repeat after editing on the same machine and record pytest durations and revisions for the pull request. Record `platform.node()`, `platform.machine()`, the exact pytest command including its worker setting, and `os.getloadavg()[0]` immediately before each run; if a before/after pair differs by more than 1.0, repeat both measurements.
2. In `tests/test_pi_contract.py`, retain the untrusted call, ordinary trusted baseline and MCP-control baseline; remove the other five repeated trusted baselines. Keep all six omitted-flag calls and their positive controls, the answer and request-count assertions in `call`, and both baseline trap assertions.
3. In `tests/test_stage2_research_catalog.py`, use `held_collect` with both `pi` and `metadata` held for the both-slow case, starting with a fresh event list and recording the arrivals at marker-write time; assert that both current-step starts precede that write, then restore source state for the next case. Preserve the start-order, event count, exit code, two request counts, timeout outcome, selection failure and successful Pi/metadata-timeout selection and explicit-include failure; retain helper guards and its single-deadline assertion.
4. In `tests/test_atomic_test_log.py`, keep the same test function and worker/drain parametrization; use two nested sessions per pair with individually named outcome nodes. Put `error` and, when drain is off, `pass` in the self-failing session; put the other outcomes in the session with no self-failing nodes. Assert exit 1, audit heading, raw-read message and the pass count expected for each mix; parse JUnit XML for each node and the clean node, and require a raw-read violation entry for every outcome node ID. Keep setup and finalizer access paths and drain behaviour distinct. Assert the non-failing session still exits 1 when no node fails, so removing the audit's exit-status assignment is caught.
5. Change `plans/changes/slow-test-fixes/plan.md` to record phase-4 time and measurement evidence. The runner owns the findings, verification and commit; no held path requires an edit. No other files are created, changed or deleted.

## Criterion ledger

- 1: tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps — a baseline or positive control is lost; inspect call count as well.
- 2: tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — the both-slow case uses a real deadline; inspect the helper call.
- 3: tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — the marker is written before both current-step requests start.
- 4: tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — sequential starts, retry, wrong timeout or selection passes.
- 5: tests/test_atomic_test_log.py::test_runtime_check_keeps_every_access_until_session_finish — an outcome or worker/drain pair is absent; inspect the eight subprocess invocations and separation.
- 6: tests/test_atomic_test_log.py::test_runtime_check_keeps_every_access_until_session_finish — a wrong node result or missing outcome audit entry passes.
- 7: tests/test_atomic_test_log.py::test_runtime_check_keeps_every_access_until_session_finish — a wrong session result, clean-node result or missing audit exit-status assignment passes.
- 8: not a test — pull request evidence records the summed case and phase durations, machine name and architecture, exact command including serial worker setting, load and revisions; missing or unmatched evidence refutes it.

## Verification and boundaries

Run before and after, on the same machine with the pinned environment and comparable load:

```bash
PYTEST_ADDOPTS= .venv/bin/python -m pytest -p no:xdist --durations=0 -vv tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules tests/test_atomic_test_log.py::test_runtime_check_keeps_every_access_until_session_finish
```

For each function, sum the reported setup, call and teardown durations across all its parametrized cases on each side; record machine name and architecture, exact command including worker setting, load and revisions. Confirm Pi actually runs rather than skips. The existing test measured at `76ceacf6` on 2026-11-25 with zero nested workers produces these JUnit node results: `pass` is failure with drain off and passed with drain on; `error` is failure; `skip`, `xfail`, `setup`, and `finalizer` are skipped for both drain settings; the clean node passes. Preserve these outcomes for both worker settings. Run the full gate:

```bash
make verify
```

Do not edit `tests/test_stage2_swarm.py`, production code, dependencies, gates or CI. Stop at the appetite and report unmet criteria.

## Time used

2026-11-25 03:25:22–03:27:22 UTC, 121 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 03:32:19–03:34:05 UTC, 106 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 03:40:07–03:42:23 UTC, 136 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 03:49:13–03:50:24 UTC, 71 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
