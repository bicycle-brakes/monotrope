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
   *Refuted by:* the both-slow case uses the real ten-second timer.
3. When the controlled deadline marker is written for the both-slow case, the current step has recorded starts for both held requests.
   *Refuted by:* the marker is written after the first current-step request starts but before the second starts, including when earlier steps recorded both starts.
4. When the catalog deadline test runs, it retains its existing overlap, timeout, selection, exit-code, request-count and guard assertions for the same scenarios.
   *Refuted by:* sequential reads, a retry, a wrong timeout or selection, or a lost existing assertion going undetected.
5. When the log-guard test runs, it executes all six outcomes in two nested pytest sessions per worker and drain pair, separating outcomes that fail on their own from those that do not.
   *Refuted by:* more than eight nested sessions for the matrix, a missing outcome, or a self-failing node in the session used to check the audit's exit status.
6. When each log-guard outcome runs for each worker and drain pair, its own node has the expected result and a raw-read violation attributed to that node.
   *Refuted by:* a wrong node result or one missing outcome violation being masked by another.
7. When a bundled log-guard session finishes, its exit status, violation header, raw-read text and pass count match its known mix of outcomes, and its clean test has the expected result.
   *Refuted by:* an incorrect session-wide check, a missing or failing clean node, or an audit that no longer sets the exit status passing unnoticed in the session without self-failing nodes.
8. When the pull request is prepared, it records one before and one after duration total per rewritten test function, summing all parametrized cases and phases, on the same machine with the same serial worker setting and identified base revision, together with the one-minute load average taken immediately before each measurement.
   *Refuted by:* a missing total, phase, case, load reading or base revision, a different machine or worker setting, or a before/after load difference greater than 1.0.

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

[DETAIL] With draining off, the pass outcome belongs with the error outcome in the self-failing session; otherwise it would mask a broken audit exit status. With draining on, pass belongs in the session without self-failing nodes.

None open.
