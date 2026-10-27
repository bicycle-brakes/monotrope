---
title: "Spec — terms-test-fixtures"
status: draft
implementation_status: none
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-hxkw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, tests, model-terms]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — terms-test-fixtures

Synthetic model terms stay compatible across suites, and the process-kill
regression retains its evidence under parallel test load (shared fixtures,
bead `coding-harness-hxkw`; load-sensitive test, bead `coding-harness-jik`).
Research: `research.md`. Scope and agent decisions: `decisions.md`.

## Problem

- Independent admissible terms builders drift when admission rules change:
  adding mandatory expiry left 55 research-availability tests failing after
  a merge on 2026-10-27. The incident and six construction sites are recorded
  in `research.md`, "What exists today" and "Draft-time gap checks".
- A process-kill regression historically passed alone but timed out under
  full verification load (`decisions.md`, reasoned interview skip). At
  `e4f84f04`, its buffered-marker regression already exists, but readiness
  still depends on pipe-line deadlines; current load failure is unmeasured
  (`research.md`, "Draft-time gap checks", inspected 2026-10-27).

## Terms

- **Admissible baseline:** synthetic terms that pass the unchanged production
  admission check before a test deliberately removes or replaces a field.
- **Launch record:** a persisted audit of an attempted launch; it does not
  certify that the child has started.

## Acceptance criteria

1. When any of the six suites identified in research constructs an admissible
   baseline, its required admission fields come from one shared test builder.
   *Refuted by:* an independent normal-record builder remains in any of those
   suites, so a required field still needs multiple baseline edits.
2. When the shared builder's default record is checked by the production
   `terms_problem` function, it is admitted without borrowing live terms.
   *Refuted by:* a missing required field causes refusal, or renewing the
   repository's real terms changes the synthetic baseline.
3. When a test customizes a builder result, subsequent builder results retain
   their defaults independently.
   *Refuted by:* a removed field, override or skip marker leaks to another call.
4. When existing tests deliberately invalidate a terms record, they continue
   to exercise their intended admission boundary after consolidation.
   *Refuted by:* defaults repair the invalid field, or refusal for a different
   missing field masks the tested reading, retention, training, cost or expiry
   boundary; fixed-date tests must keep controlling the terms clock.
5. When the process-kill regression kills its driver after the first terminal
   result and second launch audit are durable, the first result remains
   readable and the second slot remains interrupted without a result.
   *Refuted by:* the first outcome/report disappears, or the second slot is
   absent from interrupted slots or appears as a completed result.
6. While full verification runs with its normal parallelism, the process-kill
   regression passes in three consecutive complete runs.
   *Refuted by:* any run times out, skips the regression or fails its assertions.

## Non-goals

Production admission policy, real model terms or renewals, model routing,
research scheduling, persistent-store behavior, runner gates and retry
budgets, general fixture/world consolidation, other timing tests, and a new
fixture-scanning gate. A bounded change has no phase-2b design or ADR draft.

## Protected areas

- `scripts/`, `model-endpoints.yaml`, `decisions/`, `docs/adr/`,
  `docs/WORKFLOW.md`, `AGENTS.md`, `Makefile` and `pyproject.toml`: preserve
  production behavior, governance, and the normal parallel verification run.
- Other changes and the living implementation-verification spec: their
  contracts remain unchanged; derived index refresh belongs to the runner.

## Definition of Done

- `make verify` green in three consecutive full runs, with command, baseline
  or implementation commit, date, outcome and run duration in `findings.md`.
- Documents moved with the tests: this change's `research.md`, `spec.md`,
  `decisions.md`, `plan.md` and `findings.md`; no architecture/model documents.
- The PR file list demonstrates protected areas untouched and non-goals unbuilt.
- The PR closes the shared-fixture task (`coding-harness-hxkw`) and identifies
  the load-sensitive test task (`coding-harness-jik`); the last commit carries
  `Closes-Bead: coding-harness-hxkw`. Tracker updates belong to the orchestrator.
- Special run: repeat the existing full verification command, not a serial
  substitute; a test-only runner refusal is reported rather than bypassed.

## Open decisions

None open. The reasoned interview skip and agent decisions in `decisions.md`
settle the scope; no maintainer answer is invented here.

- [DETAIL] Use synthetic far-future expiry for ordinary baselines and explicit
  overrides for boundary tests, keeping tests independent of live renewal.
- [DETAIL] Preserve explicit missing-cost cases: cost is optional metadata,
  not an implicit default of the shared admissible record.
- [DETAIL] The appetite is two hours of phase 4 including repairs; three full
  runs are the finite load-evidence threshold, not a promise of zero future flakes.

These reversible details are chosen by the agent to bound implementation
and make the evidence reproducible.
