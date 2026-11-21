---
title: "Spec — red-first-baseline"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7aso
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, red-first]
class: bounded
appetite: 4
adr_files: []
---

# Spec — red-first-baseline

A repair's baseline proof reports the named test's actual qualifying outcome on baseline code (bead coding-harness-7aso). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-20, the runner reported two finder-partial-report repair tests green on baseline although the hand check found them red (`research.md`, “What exists today”). The recorded refusal for round 3 names `test_finder_deep_envelope_is_invalid_without_crashing` and exit 0 (commit `ca493614`); the hand repair reports its new tests red against the old scripts (commit `5121a00c`). The cause is not yet established. Separately, the workflow says exit 1 or 2 while the implemented and governing red-first contract requires exit exactly 1 (`research.md`, “What is unclear about it”; `decisions.md`, D-1).

## Acceptance criteria

1. When the recorded finder-partial-report round-3 refusal is reproduced using its baseline and attempted test, the regression demonstrates the mismatch before the fix and the baseline proof accepts the qualifying red after the fix.
   *Refuted by:* The pre-fix regression does not demonstrate the reported mismatch, or the fixed proof still reports exit 0 for the qualifying red run.
2. When the named test actually passes on the baseline, the baseline proof refuses it as not red first.
   *Refuted by:* A passing baseline test is accepted as proof of a repair.
3. When the named test fails for an environment, collection, setup, teardown, or nonqualifying call error instead of a qualifying assertion or pytest failure, the baseline proof refuses it.
   *Refuted by:* A missing dependency, collection failure, fixture error or unrelated exception is accepted as a qualifying red.
4. When the baseline proof runs, it uses baseline production code and the attempt's Git-visible tests without changing the source repository's refs, index or worktree.
   *Refuted by:* Attempt production bytes reach the proof, attempt tests are omitted, or the proof changes the source repository.
5. When a reader consults the workflow's red-first exit contract, it states that a qualifying baseline run requires pytest exit exactly 1.
   *Refuted by:* The workflow permits exit 2 or omits the exit-1 requirement.

## Non-goals

- Changing the tests-only baseline rule for code under test that lives in the test file (bead coding-harness-bf9m); that separate investigation can bring it back.
- Changing guard-test routing, the qualifying-failure definition, dependency provisioning, or the fixed-code proof.
- Treating a hand check as sufficient proof without reproducing the discrepancy in the runner.

## Protected areas

Other change folders, accepted ADRs and tracker data are outside this bounded repair; the existing private proof repository and ref safeguards remain in force.

## Definition of Done

- `make verify` green.
- `docs/WORKFLOW.md` accompanies the correction; no ADR or model change.
- The protected areas untouched and the non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead `coding-harness-7aso` and its last commit carries `Closes-Bead: coding-harness-7aso`.
- The pull request records the pre-fix reproduction and post-fix result with the tested commits.

## Open decisions

[DETAIL] This is `bounded`: the recorded task restores the existing proof contract and its interview was skipped for that reason. The four-hour phase-4 appetite is a reversible stop for reproducing and repairing the reported fault; stop and report if evidence or scope exceeds it.
