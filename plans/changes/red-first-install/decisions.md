---
title: "Decisions — red-first-install"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-omp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# red-first-install — Decisions

## SKIP · interview

status: skipped
reason: A bounded fix whose requirement the bead already states (coding-harness-omp: the baseline check must see the pinned install, or count only an assertion failure as red, with a test that a missing install is not red). The maintainer pre-approved the merge of this bead's pull request on 2026-10-16 under two conditions (no open BLOCKER after the phase-6 Opus review, green CI). What stays open is the choice between the two directions the bead names, decided below as a detail with its reason.

## Details the orchestrating session decides

These are `[DETAIL]` items (the agent decides and writes its reason down);
none of them changes a decision of record.

1. **Count only an assertion failure as red.** `red_first` counts an outcome
   as red only when pytest ends with a failed assertion (the test's own
   failure), and exit 1 from a setup error, a fixture error or a missing
   install is not red. Reason: copying or linking the pinned install into the
   scratch checkout would hide a dependency the baseline check should not
   need, and it would also couple the scratch to `node_modules` of the main
   worktree. Classifying the outcome keeps the check honest about what it
   proves. The other direction (provision the pinned install) stays open
   as a later change if the classification proves too narrow.
2. **Setup failures refuse instead of passing.** An outcome that is neither a
   test failure nor a pass ends the repair as "red first could not be
   established", naming the cause, so a repair cannot pass the check on
   an environment fault. Reason: the bead asks that a missing install is not
   read as red; refusing is the fail-closed side of the same rule.
3. **Coordinate with the guard-test change.** `explore/guard-test` (bead
   coding-harness-0ho) also changes the red-first path. The implementation
   lands after or rebases onto that change; the phase-4 notes name the shared
   function. Reason: both edit `red_first` in `scripts/stage2.py`.
4. **The test follows the existing pattern.** A test with a planted failing
   fixture (an interpreter that cannot import pytest, and a fixture error in
   the baseline run) asserts the outcome is refused, not red, using the
   existing `red_first` tests as the model. Reason: the research names these
   tests as the established shape.
