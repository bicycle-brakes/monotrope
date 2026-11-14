---
title: "Spec — swarm-shared-fixture"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-wnka
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, tests, swarm, performance]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — swarm-shared-fixture

Reduce measured research-swarm test-body cost without losing behavioural
coverage (bead coding-harness-wnka — speed up the slowest swarm tests).
Research: `research.md`; the maintainer's re-scope: `decisions.md#Q-1`.

## Problem

- The research records eleven research-swarm cases among the twelve slowest
  tests in the baseline dated 2026-11-04; repeated full runs inside individual
  tests amplify per-slot work (`research.md`, "What exists today").
- The original shared-world proposal targets little of the measured cost:
  fixture setup took 23 s and test bodies 768 s summed on 2026-11-13, using
  six workers on the Mac mini (`decisions.md#Q-1`). These are aggregate
  phase durations, not elapsed suite time.
- The earlier profile attributed time to declaration reads and leak checks,
  but declaration parsing has since been cached; it cannot establish the
  current bottleneck (`research.md`, "Where the time goes"). The maintainer
  therefore requires individual measurement of the five slowest tests before
  choosing an optimisation (`decisions.md#Q-1`, recorded 2026-11-13).

## Terms

**Target set:** five collected pytest node IDs with the highest baseline
call-phase durations in `tests/test_stage2_swarm.py`, selected before edits
and kept fixed for the comparison, including any parameter suffixes.
**Preserved coverage:** the same pre-existing collected cases, behavioural
assertions and exercised production paths that detect each case's stated fault.

## Acceptance criteria

1. When a test is first optimised, the target set already has individual
   timing and profiling evidence identifying the repeated work the edit addresses.
   *Refuted by:* fewer than five individually measured targets, a changed
   target set after edits, or an edit without an observed hotspot.
   *Basis:* `decisions.md#Q-1`; `research.md`, "Where the time goes".

2. When the fixed target set is measured before and after under matched
   isolated conditions, the sum of its five per-target median elapsed times
   is lower after the change.
   *Refuted by:* an equal or larger sum, fewer than three successful
   unprofiled runs per target per revision, or unmatched interpreter,
   dependencies, worker settings, inputs or competing verification load.
   *Basis:* `decisions.md#Q-1` — measured savings rather than an assumed gain.

3. When the revised suite is compared with its baseline, all pre-existing
   test names, collected cases and behavioural assertions remain effective.
   *Refuted by:* deletion, renaming, fewer cases, added skips/xfails, a
   weakened assertion, or a replacement that makes a previously detected
   fault pass by supplying the expected result itself.
   *Basis:* `decisions.md#Q-1` — no test loses an assertion.

4. While tests run individually or together, any reused test data remains
   isolated from another test's mutations and the real admission, leak,
   expiry, launch and timing boundaries remain exercised where asserted.
   *Refuted by:* order-dependent results, leaked mutable state, a blanket
   clean verdict, stale input after a test edit, or bypass of a boundary
   needed to detect an existing planted fault.
   *Basis:* `decisions.md#Q-1`; `research.md`, fixture injection contract and
   per-slot production costs.

5. When the implementation is verified, the existing verification command
   passes with executable changes confined to the research-swarm test file.
   *Refuted by:* a failing `make verify`, a production/dependency/gate change,
   or an executable edit outside `tests/test_stage2_swarm.py`.
   *Basis:* `decisions.md#Q-1` — only test files change; production untouched.

## Non-goals

- A shared fixture world, broader fixture scope, `conftest.py`, cross-suite
  consolidation or edits to the sibling single-explorer world.
- Production speedups, cached admission or leak verdicts, replacing real
  boundary checks with unconditional success, or reducing tested scenarios.
- Changing verification parallelism, gates, dependencies, model declarations
  or test tiers; repairing the independent concurrent test-log mechanism.
- A guaranteed percentage saving or a full verification run below ten
  minutes: that is the broader goal, not a demonstrated outcome of this change.
- Design phase 2b and an ADR: the class is `bounded` and architecture stays
  unchanged. If profiling requires production work, stop and return the
  evidence to the orchestrator instead of extending this change.

## Protected areas

- `scripts/`, `Makefile`, `decisions/`, `docs/adr/`, `model-endpoints.yaml`,
  `research-swarm-limits.yaml`, `pyproject.toml`, `requirements-ci.txt`,
  `.github/`, `prompts/` and `templates/`: runtime behaviour and workflow
  contracts are outside this test-only scope.
- All other test files, shared fixture modules and neighbouring change
  ledgers: keep their contracts and imports intact.
- Remaining held paths, including `provenance.yaml`, `AGENTS.md`, `.claude/`,
  `.codex/`, `.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md`, `README.md` and
  `.beads/`: no implementation edit is needed there.

## Definition of Done

- `make verify` green in the pinned environment, with the existing gates.
- Dated selection, profiles, raw paired timings, medians, revision IDs,
  environment and coverage checks recorded in this change's `plan.md`.
- The diff preserves protected areas and implements no non-goal.
- Documents moving with the tests: this change's `spec.md`, `plan.md` and
  runner-managed `findings.md`; no living spec, model file or ADR changes.
- The runner regenerates `plans/INDEX.md`; the PR names bead
  coding-harness-wnka — speed up the slowest swarm tests — and its final
  commit carries `Closes-Bead: coding-harness-wnka`.
- Special runs: the fixed-target comparisons and full verification, each
  identified by date and revision in the PR body.

## Open decisions

None open; the maintainer's re-scope is already answered.

- [DETAIL] Use a three-hour phase-4 appetite including measurement and repairs
  as a stop, because the work is restricted to one measured test hotspot.
- [DETAIL] Compare the sum of five medians from three runs each, without an
  invented percentage target; report individual changes as well so a slower
  target cannot disappear behind the total.
- [DETAIL] Restrict executable edits to the existing swarm test module, keeping
  names and cross-imports stable; select the mechanism only after profiling.
- [DETAIL] Keep `neighbours: []`: Explore used the single-model Flash route,
  not a complete research-swarm/v2 handoff. Its suggested neighbours describe
  context rather than confirmed handoff obligations.
