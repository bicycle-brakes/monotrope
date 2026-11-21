---
title: "Spec — free-storage-keys-flake"
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
tags: [spec, flaky-test, research-swarm]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — free-storage-keys-flake

Find and fix the demonstrated cause of the intermittent free-model storage-key
test failure without weakening its coverage (bead coding-harness-068l —
reproduce and fix the free storage keys flake). Research: `research.md`;
decisions: `decisions.md`.

## Problem

- On 2026-11-08, the merge queue reported exit 1 for the case with a long model
  name and no scripted failure; another pull request passed on the same base
  shortly afterward (`decisions.md`, base `8f740e13`).
- On 2026-11-21 at `ee349b78`, 25 serial repetitions of all six cases and one
  random-order run passed; the cause and a local reproduction remain unknown
  (`decisions.md`, first measurement; `research.md`, What is unclear).

## Terms

**Scenario:** a case’s declared model, fault override, scripted steps and expected
outcomes; shared helper implementation is not part of the scenario.

## Acceptance criteria

1. When reproduction is attempted, exactly 20 non-overlapping runs of the complete swarm test
   file use `-n auto` across the default collection order, its reverse and one
   seeded shuffle, recorded with the seed.
   *Refuted by:* a different run count, overlapping runs, a missing order or seed,
   a partial file, or a worker setting other than `-n auto`.
2. When reproduction is attempted, the exact CI command `python3 -m pytest tests/ -q -n auto` runs exactly five times in default order, without overlapping other protocol runs,
   with reporting-only additions that include a JUnit XML report.
   *Refuted by:* a different run count, changed command flags or order, an
   overlap, a scheduling change, or a missing JUnit XML report.
3. While each reproduction run executes, one CPU-busy process per CPU core runs alongside it.
   *Refuted by:* fewer busy processes or a run with a gap in that load.
4. When an attempt ends, dated evidence in `findings.md` records revision, OS,
   Python version, commands, load, orders, resolved worker counts, run counts,
   and counts of failures among the six cases of the target test, plus each load
   process’s start and end times and its liveness at each run’s end.
   *Refuted by:* any missing field or a failure count including another test.
5. When a target case fails, the evidence includes its swarm stderr, its worker
   and the ordered test IDs that worker ran before it.
   *Refuted by:* a target failure without stderr or a replayable worker history.
6. When another test fails under load, the evidence lists its test ID separately.
   *Refuted by:* an unlisted non-target failure or its inclusion in the target failure count.
7. If a cause is found, a regression forces the interleaving that produced a
   target failure under load and matches its captured failure: the same exception
   type, failing assertion line and runner stderr lines after normalising temporary
   paths, run IDs and timestamps.
   *Refuted by:* a cause inferred from reading alone, or a difference in any
   of those fields after normalisation.
8. If a cause is found, its forced regression fails before the fix and passes after it.
   *Refuted by:* a passing pre-fix run or a failing post-fix run.
9. When the test runs after a fix, its entire existing test function and the
   scenario exercised by each of its six cases remain unchanged.
   *Refuted by:* a changed setup or assertion, renamed case, changed scenario,
   added skip or expected-failure marker, or failed case.
10. If shared test helpers change, the evidence explains how the demonstrated cause requires each change.
    *Refuted by:* a helper change without a cause-based explanation.
11. When a fix is made, the same load protocol runs again with the same settings, including reporting,
    orders and counts, with no target-case failure.
    *Refuted by:* a missing or different run, or any target-case failure after the fix.
12. If no cause is found within the available implementation appetite, the attempt stops without a speculative fix and records what was tried and measured under `Stopped without a cause` in `findings.md`.
    *Refuted by:* an unproven fix or a stop without the stated evidence.
13. If a demonstrated fix exceeds the available appetite or would touch a protected area or non-goal, the attempt stops and records the cause and proposed remedy in `findings.md` for the orchestrator.
    *Refuted by:* implementing that remedy or stopping without the cause and proposal.

## Non-goals

- Any retry or longer timeout or deadline as a remedy, in tests or production;
  remove a demonstrated race instead.
- Changing admission, storage-key contracts or unrelated swarm behaviour;
  broader suite or fixture optimisation is separate.
- Renaming the existing test or changing its archived criterion-ledger rows.

## Protected areas

- `plans/changes/archive/2026-11-06-research-swarm/plan.md`: its existing test
  name and ledger rows stay intact.
- Admission and leak-check policy, model declarations and verification gates:
  the failure does not establish a reason to weaken them.

## Definition of Done

- The cause is reproduced under load; the matching forced regression is red
  before the fix and green after it; the full load protocol then has no target
  failure, the six cases pass and `make verify` is green.
- The pull request includes the evidence and commands in `findings.md` and
  checks protected areas and non-goals against its file list.
- The pull request closes bead coding-harness-068l — reproduce and fix the free
  storage keys flake — with `Closes-Bead: coding-harness-068l` on its last commit.
- A stop is reported to the orchestrator without claiming completion or closing
  the bead, including when a fix cannot fit the available appetite or boundaries.

## Open decisions

None open.

- [DETAIL] The phase-4 appetite is two hours including repairs; the session may
  extend it once to four hours under the workflow, then stops. Wall time spent
  running the load protocol counts; this keeps the investigation bounded.
- [DETAIL] The load protocol uses exactly 20 file runs, three orders, five CI
  command runs and one busy process per core to make its conditions measurable.
  Higher load is an additional exploratory run, not a protocol reproduction.
- [DETAIL] A temporary collection hook supplies the three orders without a new
  dependency; a temporary reporting plugin captures worker histories alongside
  JUnit XML because the XML alone is not assumed to establish execution order.
- [DETAIL] The research is a single-explorer report, not a completed research
  swarm, so its suggested neighbours are not a swarm handoff.
