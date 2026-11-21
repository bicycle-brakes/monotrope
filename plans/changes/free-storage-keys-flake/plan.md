---
title: "Plan — free-storage-keys-flake"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-068l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, flaky-test, research-swarm]
---

# Plan — free-storage-keys-flake

```text
For you:     The intermittent free-model storage-key test failure is investigated and its demonstrated cause fixed.
Done when:   A forced regression fails before the fix and passes after it, the six existing cases pass, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Retries, longer timeouts, skipped tests, unrelated swarm changes or speculative fixes.
Pre-mortem:  suppose it failed: most likely because the failing interleaving did not recur under the available load.
Starts unless you say stop.
```

Baseline `ecb43b4c`, 2026-11-21. This bounded change needs no design phase or
ADR. There is no `templates/plan.md` in this checkout; this follows the plan
prompt. The reported failing case was the long model name, `failed=False`;
25 serial repetitions of the six cases and one random-order run passed at
`ee349b78` on 2026-11-21. The cause is unknown.

## Files and steps

1. Coordinate the load experiment with the orchestrator before consuming the
   shared verify slot. In the pinned environment collect all node IDs from
   `tests/test_stage2_swarm.py`, shuffle them with Python's seeded `random`
   using at least three distinct seeds, and pass the complete shuffled list to
   `python3 -m pytest -q -n auto`; run with a separately supervised CPU load.
   Record the exact commands, seeds and order, worker/load settings, revision,
   dates, run/failure counts and the failing run's swarm stderr in this plan.
   Preserve subprocess output and temporary files on failure. Do not claim a
   pass proves the flake gone. If stderr is not exposed, instrument the test
   fixture to retain it without altering swarm behaviour.
2. Trace a reproduced failure to its actual cause; force that interleaving in
   `tests/test_stage2_swarm.py::test_free_storage_key_flake_forced_interleaving`
   using synchronization rather than timing. Record its failing result before
   the fix, then repair the demonstrated cause and record the passing result.
   Keep all assertions and six parametrized cases of
   `test_free_model_storage_keys_preserve_best_effort_completion` intact.
3. The expected implementation file is `tests/test_stage2_swarm.py` (test,
   fixture or stand-in). The demonstrated cause may instead require
   `tests/atomic_test_log.py`, `scripts/stage2_research_run.py`, or
   `scripts/stage2_research_dispatch.py`; change only the demonstrated fault
   at its existing boundary. If the evidence identifies another file or a held
   path, stop and return the evidence and proposed path to the orchestrator
   before extending this plan. No held path is assigned to the attempt; any
   needed held-path edit belongs to the orchestrator after an accepted attempt.
4. Update this `plan.md` with commands, evidence and time, and replace the
   not-yet-written ledger entry once its test exists. The runner manages
   `plans/changes/free-storage-keys-flake/findings.md` and the generated
   `plans/INDEX.md`. If no cause is found within two hours, add `Stopped without
   a cause` to the findings with the attempted conditions and measurements,
   return without a speculative fix or bead closure, and do not claim success.

## Criterion ledger

- 1: not a test — inspect recorded commands, full collection, seeds and concurrent load; an omitted condition refutes the attempt.
- 2: not a test — inspect the dated reproduction record and failing stderr; a missing field or failure output refutes it.
- 3: not yet written tests/test_stage2_swarm.py::test_free_storage_key_flake_forced_interleaving — the reproduced interleaving does not fail before the fix or fails afterward.
- 4: tests/test_stage2_swarm.py::test_free_model_storage_keys_preserve_best_effort_completion — an existing case fails; compare collection and assertions with the baseline for removals or weakening.
- 5: not a test — inspect the stop report and diff if the appetite expires; a speculative fix or missing measurements refutes it.

## Verification and boundaries

Run the existing six cases and the new deterministic regression after a fix:

```sh
python3 -m pytest -q tests/test_stage2_swarm.py::test_free_model_storage_keys_preserve_best_effort_completion tests/test_stage2_swarm.py::test_free_storage_key_flake_forced_interleaving
make verify
```

The archived research-swarm plan and its test-ledger rows stay untouched;
no retry, increased timeout, skip, policy change or unrelated optimisation.
The runner performs full verification and the commit; no success is claimed
when the reproduction stops without a cause.

## Time used

2026-11-21 17:40:37–17:43:19 UTC, 162 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
