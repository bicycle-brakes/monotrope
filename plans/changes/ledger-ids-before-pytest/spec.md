---
title: "Spec — ledger-ids-before-pytest"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.9
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, criterion-ledger]
class: bounded
appetite: 4
adr_files: []
---

# Spec — ledger-ids-before-pytest

The runner identifies missing criterion tests before pytest, permits a repair to address its own findings, and holds unwritten tests at phase 6 (bead `coding-harness-bxxt.9`). Research: `research.md`. Decision: `decisions.md#Q-1`.

## Problem

- At commit `5c7bce46` the runner passes ledger test references to pytest without checking whether they stand; a missing reference can stop collection of all selected tests (`research.md`, “What exists today”).
- On 2026-11-18 repairs failed on unrelated unwritten tests, with pytest reporting no tests ran without naming them; phase 6 had no checkpoint for that debt (`decisions.md#Q-1`).

## Terms

**Ledger test:** a test reference in either test form of the accepted plan's criterion ledger. **Standing:** the named file and top-level test function exist according to the runner's pre-launch check. **Attempt record:** the runner's persistent record of an implement or repair attempt.

## Acceptance criteria

1. When an implement or repair attempt selects tests, the runner checks every ledger test for existence before invoking pytest.
   *Refuted by:* a missing ledger test reaches pytest as a test ID.
2. When one or more ledger tests are missing, the attempt record names each missing test ID.
   *Refuted by:* a missing ID is absent from the record, including for an otherwise successful repair.
3. When missing ledger tests coexist with other selected targets, pytest runs the standing selected targets without the missing IDs.
   *Refuted by:* a missing ID prevents a standing selected test from running or is passed to pytest.
4. When no selected target stands, the runner skips pytest.
   *Refuted by:* pytest is launched with no standing target.
5. When an implement attempt has a missing ledger test, the attempt fails even if all standing selected tests pass.
   *Refuted by:* an implement attempt with a missing ledger test is accepted.
6. When a repair attempt has an unrelated missing ledger test, that missing test alone does not fail the attempt.
   *Refuted by:* an otherwise successful repair is rejected solely for an unrelated missing ledger test.
7. When a repair attempt addresses a finding, the finding's required proof remains the repair's obligation.
   *Refuted by:* a repair is accepted without the required proof of its finding.
8. When a selected standing test fails, the attempt fails even if missing ledger tests were also reported.
   *Refuted by:* a repair or implement attempt accepts a failing selected test.
9. When the current plan contains a ledger entry marked `not yet written`, phase 6 refuses before calling the reviewer and names each such entry and the next step.
   *Refuted by:* the reviewer starts, an entry is omitted, or the refusal omits how to proceed.
10. When the current plan has no `not yet written` ledger entry, this checkpoint does not refuse phase 6.
    *Refuted by:* a plan with only written tests and non-test entries is refused by this checkpoint.
11. If the runner cannot read or assess the ledger or selected test files, it reports the failure instead of treating the tests as absent or the checkpoint as clear.
    *Refuted by:* an unreadable or unparseable input yields a successful check or a missing-test-only diagnosis.

## Non-goals

- Changing criterion-ledger entry forms, the archive rule, or the runner's ledger clearing.
- Measuring pytest startup time, changing worker counts, or changing the scope of changed-test and retry selection.
- Relaxing phase-6 verification, review, or the existing proof required for repaired findings.

## Protected areas

The ledger gate and its governance remain unchanged: the new phase-6 checkpoint belongs to the runner, not a second ledger format or a change to archive policy. Held paths remain untouched by the implementation attempt.

## Definition of Done

- `make verify` green; focused checks exercise implement, repair and phase 6.
- `docs/WORKFLOW.md` describes the changed runner contract in the same pull request; no ADR is due.
- Protected areas and non-goals are checked against the pull request's file list.
- The pull request closes bead `coding-harness-bxxt.9`; its last commit carries `Closes-Bead: coding-harness-bxxt.9`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The phase-4 appetite is four hours including repairs: neither research nor the answered decision specifies one, and a finite stop makes the card actionable. [DETAIL] Existence means a readable file and a top-level function, matching the ledger's existing test form; collection and execution errors still belong to pytest.
