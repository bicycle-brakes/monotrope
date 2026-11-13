---
title: "Decisions — origin-check-across-blocks"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-13
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

## Q-1 · Which row is current for a finding id

asked: 2026-11-11
answer: Option D, stated by the maintainer on 2026-11-12 about 07:30 UTC (recorded in the notes of bead coding-harness-3h96; it supersedes answer A of 2026-11-11) — one resolver function in scripts/stage2.py decides which row is current for a finding id (the latest in its block); the Origin check and the repair-target selection both ask only that function; repeated ids across tables are a finding's history, not an error; ids must be unique only within one table.
answered_by: maintainer
status: answered
context: |
  Topic: a phase-6 re-check may repeat a finding id that an earlier table already holds, and two code paths each decided on their own which row counts.
  Intention: a repair attempt was parked on 2026-11-11 because the uniqueness rule for finding ids was undecided; the maintainer asked for the most lasting solution.
  Today: the Origin check and the repair-target selection resolve rows separately, so one can validate a row the other does not repair.
  Repository change: one resolver in scripts/stage2.py that both callers ask; the duplicate-id refusal is scoped to one table; the saved tests follow.
  Architecture change: none; one choke point replaces two readings of the same tables.

In the context of finding ids that repeat across phase-6 tables, facing a choice between uniqueness per block kind, uniqueness across everything with renumbering, the old back-computation, and one resolver, we decided for one resolver that names the current row of an id, to achieve that the Origin check and the repair selection can never disagree, accepting that a repeated id across tables is read as history and no longer refused. — 2026-11-12

## Q-2 · Ending the review loop after round 9

asked: 2026-11-13
answer: "ja" — after the repair of the three rows of round 9 the change goes straight to phase 6, without a tenth loop round; the pull request names it.
answered_by: maintainer
status: answered
context: |
  Topic: the review loop of this change has run nine rounds with 35 rows and no clean round.
  Intention: round 9 brought three documentation rows and none on the behaviour of the code; the appetite of one hour is long spent.
  Today: the rule is rounds until a clean one, each followed by a repair with a full check.
  Repository change: none in code; the pull request states that the loop ended after round 9.
  Architecture change: none.

In the context of a loop that finds something new in every round, facing a choice between a tenth round and phase 6, we decided to go to phase 6 after this repair, to achieve an end to the change, accepting that a further loop round might have found what phase 6 misses. — 2026-11-13
