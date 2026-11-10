---
title: "Decisions — origin-check-across-blocks"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-3h96
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, repair, origin]
---

# origin-check-across-blocks — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a skip
below).

## SKIP · interview

status: skipped
reason: A bounded bug fix whose intent and fix the bead already state — an older phase-6 row with an invalid Origin escapes validation once a newer phase-6 block exists, and the fix is to validate the outstanding repair targets across phase-6 blocks before any effect (bead coding-harness-3h96, class bounded). The maintainer decided on 2026-11-09 that this finding of the origin-cell review becomes a follow-up of its own. The exploration found one place for the check that contradicts no pinned test, so no choice is left for the maintainer.

## Decided by the agent

[DETAIL] **The check sits on the repair path, over the rows repair has
selected.** Reason: `repair_targets` already reads every phase-6 block and
`repair` is its only caller (research.md); validating exactly those rows
closes the gap where a model is called on a row with invalid provenance.

[DETAIL] **`origin_refusal` keeps its newest-block reading for review,
release and review-loop.** Reason: the narrow reading is the repair of a
BLOCKER of the origin-cell change — decided rows released before the check
existed must not hold the verbs — and two tests pin it
(`test_legacy_released_origin_does_not_hold_verbs`,
`test_origin_release_controls_keep_distinct_validation_scopes`).

[DETAIL] **The refusal comes before any effect**: before the model call and
before any write to `findings.md` or the loop record, and it names the row
and the block it stands in. Reason: the bead asks for "before any effect",
and the existing Origin refusals name row and place.

[DETAIL] **The wording in `docs/WORKFLOW.md` moves only as far as the
guarantee moves**: the repair section says that repair refuses a selected
row of any phase-6 table whose Origin is invalid. Reason: a test pins
phrases of the Origin paragraph
(`test_origin_workflow_assigns_provenance_to_the_orchestrator`).
