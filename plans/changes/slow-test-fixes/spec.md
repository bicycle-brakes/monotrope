---
title: "Spec — slow-test-fixes"
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
tags: [spec, tests, speed]
class: bounded
adr_files: []
---

# Spec — slow-test-fixes

Three test changes reduce avoidable work while preserving their existing checks (bead `coding-harness-bxxt.16`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- At `449f1872`, the real-Pi isolation test makes 14 calls, including five repeated baseline configurations; its MCP control has a distinct baseline (`research.md`, Pi contract).
- At `449f1872`, the catalog test waits for a real ten-second deadline even though an event-controlled deadline helper exists (`research.md`, catalog deadline).
- At `449f1872`, the log-guard test starts 24 nested pytest runs for six outcomes across two worker and two drain settings (`research.md`, nested pytest subprocesses).
- The cited costs are source counts, not measurements of these three tests; matched duration evidence is needed (`research.md`, what is unclear).

## Acceptance criteria

1. When the real-Pi isolation test runs, it removes the five repeated baseline calls while retaining the untrusted baseline, both distinct trusted baselines, and each of the six omitted-flag positive controls with their existing assertions.
   *Refuted by:* a repeated ordinary baseline, a missing MCP baseline or positive control, or a lost assertion.
2. When both catalog sources are held past the shared deadline, the catalog test fires the existing controlled deadline rather than waiting ten seconds of wall time.
   *Refuted by:* the both-slow case uses the real ten-second timer or does not hold both requests until the deadline.
3. When the catalog deadline test runs, it retains its existing overlap, timeout, selection, exit-code, request-count and guard assertions for the same scenarios.
   *Refuted by:* sequential reads, a retry, a wrong timeout or selection, or a lost existing assertion going undetected.
4. When the log-guard test runs, it executes all six outcomes in one nested pytest run per worker and drain pair.
   *Refuted by:* more than four nested runs for the matrix or any missing outcome in a pair.
5. When each log-guard outcome runs for each worker and drain pair, the existing return-code, violation-report, raw-read and clean-test assertions remain independently attributable to that outcome.
   *Refuted by:* a missing violation for one outcome being masked by another, or a lost existing assertion.
6. When the pull request is prepared, it records before and after durations of each rewritten test on the same machine, using the base test file for the before measurement.
   *Refuted by:* any missing test duration, unmatched machine or an unidentified base revision.

## Non-goals

- The finder sleep belongs to the neighbouring swarm-test-speed change; catalog-wide process batching and other test speed work are excluded.
- Production behaviour, dependencies, verification gates and CI configuration do not change.

## Protected areas

The finder test in `tests/test_stage2_swarm.py` is reserved for the neighbouring change to avoid overlapping work.

## Definition of Done

- `make verify` green; the pull request records the matched duration evidence.
- Documents, models and ADRs moved with the code: none beyond this change's artefacts.
- Protected areas and non-goals remain untouched, as shown by the pull request's file list.
- The pull request closes `coding-harness-bxxt.16` and its last commit carries `Closes-Bead: coding-harness-bxxt.16`.
- Special runs: the before and after measurements, with their revisions in the pull request.

## Open decisions

[DETAIL] Use the existing event-controlled deadline for both held sources; it exercises the existing abort path without a wall-clock wait. The measurement compares reported pytest durations without a fixed speed threshold because no matched baseline exists yet.

None open.
