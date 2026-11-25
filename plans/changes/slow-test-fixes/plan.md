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

1. Before editing, record the base revision and measure each named test using the command below; repeat after editing on the same machine and record pytest durations and revisions for the pull request. Keep conditions comparable; report noise or a missing measurement rather than claiming a speedup.
2. In `tests/test_pi_contract.py`, retain the untrusted call, ordinary trusted baseline and MCP-control baseline; remove the other five repeated trusted baselines. Keep all six omitted-flag calls and their positive controls, the answer and request-count assertions in `call`, and both baseline trap assertions.
3. In `tests/test_stage2_research_catalog.py`, use `held_collect` with both `pi` and `metadata` held for the both-slow case, starting with a fresh event list and recording the arrivals at marker-write time; assert that both current-step starts precede that write, then restore source state for the next case. Preserve the start-order, event count, exit code, two request counts, timeout outcome, selection failure and successful Pi/metadata-timeout selection and explicit-include failure; retain helper guards and its single-deadline assertion.
4. In `tests/test_atomic_test_log.py`, keep the same test function and worker/drain parametrization, but run all six outcomes as individually named nested cases in each of four subprocesses. Assert exit 1, audit heading, raw-read message and the pass count expected for the bundled mix once per session; read each outcome node and the clean node from JUnit XML and assert their expected results, and require a raw-read violation entry for each outcome node ID so one cannot mask another. Keep the setup and finalizer access paths and drain behaviour distinct.
5. Change `plans/changes/slow-test-fixes/plan.md` to record phase-4 time and measurement evidence. The runner owns the findings, verification and commit; no held path requires an edit. No other files are created, changed or deleted.

## Criterion ledger

- 1: tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps — a baseline or positive control is lost; inspect call count as well.
- 2: tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — the both-slow case uses a real deadline; inspect the helper call.
- 3: tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — the marker is written before both current-step requests start.
- 4: tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — sequential starts, retry, wrong timeout or selection passes.
- 5: tests/test_atomic_test_log.py::test_runtime_check_keeps_every_access_until_session_finish — an outcome or worker/drain pair is absent; inspect the four subprocess invocations.
- 6: tests/test_atomic_test_log.py::test_runtime_check_keeps_every_access_until_session_finish — a wrong node result or missing outcome audit entry passes.
- 7: tests/test_atomic_test_log.py::test_runtime_check_keeps_every_access_until_session_finish — a wrong session result or clean-node result passes.
- 8: not a test — pull request evidence records the summed case and phase durations, machine, serial worker setting, load and revisions; missing or unmatched evidence refutes it.

## Verification and boundaries

Run before and after, on the same machine with the pinned environment and comparable load:

```bash
PYTEST_ADDOPTS= .venv/bin/python -m pytest -p no:xdist --durations=0 -q tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules tests/test_atomic_test_log.py::test_runtime_check_keeps_every_access_until_session_finish
```

For each function, sum the reported setup, call and teardown durations across all its parametrized cases on each side; record machine, worker setting, load and revisions. Confirm Pi actually runs rather than skips. Run the full gate:

```bash
make verify
```

Do not edit `tests/test_stage2_swarm.py`, production code, dependencies, gates or CI. Stop at the appetite and report unmet criteria.

## Time used

2026-11-25 03:25:22–03:27:22 UTC, 121 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 03:32:19–03:34:05 UTC, 106 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
