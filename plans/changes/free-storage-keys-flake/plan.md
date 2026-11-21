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
Done when:   A matching forced regression fails before and passes after the fix, the repeated load protocol has no target failure, and make verify is green.
Appetite:    2 hours of phase 4 including repairs; one extension to 4 hours is allowed under the workflow.
Not now:     Retries, longer deadlines, skipped tests, unrelated swarm changes or speculative fixes.
Pre-mortem:  suppose it failed: most likely because the failing interleaving did not recur under the available load.
Starts unless you say stop.
```

Baseline `9491d2d3`, 2026-11-21. This bounded change has no design phase or
ADR. There is no `templates/plan.md` in this checkout. The cause is unknown;
25 serial repetitions and one random-order run passed at `ee349b78`.

## Files and steps

1. Coordinate the shared verify slot with the orchestrator. In the pinned
   environment run the exact CI command below at least five times in default
   order. Separately collect all IDs in `tests/test_stage2_swarm.py`, shuffle
   the complete list with at least three recorded Python random seeds, and run
   at least 20 repetitions with `python3 -m pytest -q -n auto` and those IDs.
   For every run supervise one busy process per logical CPU for its duration;
   stop and reap the load processes even on failure. Capture complete pytest
   output, swarm stderr and temporary files on failure. Use a temporary pytest
   reporting plugin, loaded through the environment without modifying the CI
   command or test order, to log each worker's ordered test IDs and resolved
   worker count; retain the failing worker's preceding IDs for serial replay
   with `-p no:xdist`. Record the exact plugin and load commands and verify the
   capture works before counting runs.
2. `plans/changes/free-storage-keys-flake/findings.md`: record dated revision,
   OS, Python, commands, seeds and full collection orders, worker counts, load,
   runs, target-case failure counts and each failing target's stderr and worker
   history; list other failing test IDs separately. Count only the six cases of
   `test_free_model_storage_keys_preserve_best_effort_completion` as target
   failures. A cause is found only if a load failure and the forced interleaving
   match, including stderr; code-reading alone is not reproduction.
3. `tests/test_stage2_swarm.py`: add
   `test_free_storage_key_flake_forced_interleaving` to force the demonstrated
   interleaving by synchronization, show it red before the fix and green after.
   Keep the whole existing parametrized function and each exercised scenario
   unchanged. Change shared helpers only at the proven cause and explain each
   change in `findings.md`.
4. If the demonstrated cause instead lies in `tests/atomic_test_log.py`,
   `scripts/stage2_research_run.py` or `scripts/stage2_research_dispatch.py`,
   change only the proven fault at its existing boundary. If another file or a
   held path is needed, stop and return evidence and proposed path to the
   orchestrator; any held-path edit is an orchestrator bootstrap edit after an
   accepted attempt. Do not add retries, extend any timeout or deadline, or
   weaken a protected policy. Rerun the identical load protocol after the fix.
5. `plans/changes/free-storage-keys-flake/plan.md`: replace the pending ledger
   entry when its regression exists and record phase-4 time. If no cause is
   found within the available appetite, record `Stopped without a cause` in
   `findings.md` with what was tried and measured; if a fix cannot fit the
   appetite or boundaries, record the cause and proposed remedy there instead.
   In either stop, return to the orchestrator without a speculative fix or bead
   closure. The workflow allows one extension from two to four hours.

## Criterion ledger

- 1: not a test — inspect file-run commands, collection, seeds and run counts; fewer than 20 runs or three orders refutes it.
- 2: not a test — inspect the five default-order CI command records; a missing or changed run refutes it.
- 3: not a test — inspect the load process records for each run; a gap or fewer processes than cores refutes it.
- 4: not a test — inspect the dated findings record and target-only counts; any missing field refutes it.
- 5: not a test — inspect each target failure's stderr and worker history; a missing item refutes it.
- 6: not a test — compare non-target failures in the output with findings; an omitted ID refutes it.
- 7: not yet written tests/test_stage2_swarm.py::test_free_storage_key_flake_forced_interleaving — the forced failure does not match the observed load failure and stderr.
- 8: not yet written tests/test_stage2_swarm.py::test_free_storage_key_flake_forced_interleaving — it passes before the fix or fails afterward.
- 9: tests/test_stage2_swarm.py::test_free_model_storage_keys_preserve_best_effort_completion — a case fails; compare the function and scenarios with the baseline for changes.
- 10: not a test — compare helper changes and their cause-based explanations in findings; an unexplained change refutes it.
- 11: not a test — compare post-fix load records to the original settings and counts; a missing run or target failure refutes it.
- 12: not a test — inspect the stop report and diff if no cause is found; missing evidence or a speculative fix refutes it.
- 13: not a test — inspect the stop report and diff if the remedy exceeds appetite or boundaries; a missing proposal or implemented prohibited remedy refutes it.

## Verification and boundaries

The CI reproduction command, in default order:

```sh
python3 -m pytest tests/ -q -n auto
```

After a fix, run the unchanged six cases and the forced regression, the same
load protocol, and the full verification:

```sh
python3 -m pytest -q tests/test_stage2_swarm.py::test_free_model_storage_keys_preserve_best_effort_completion tests/test_stage2_swarm.py::test_free_storage_key_flake_forced_interleaving
make verify
```

Do not touch the archived research-swarm plan or its ledger, admission and
leak-check policy, model declarations or verification gates. The runner manages
`plans/INDEX.md`, full verification and the commit.

## Time used

2026-11-21 17:40:37–17:43:19 UTC, 162 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 17:47:02–17:49:20 UTC, 139 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
