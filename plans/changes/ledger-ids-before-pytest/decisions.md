---
title: "Decisions — ledger-ids-before-pytest"
category: decisions
status: draft
implementation_status: none
date: 2026-11-20
created: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.9
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, cheap-checks, criterion-ledger]
---

# ledger-ids-before-pytest — Decisions

Class: bounded (bead coding-harness-bxxt.9; one answered question is owed —
Q-1 below, answered by the maintainer in the conversation of 2026-11-20).

## Q-1 · Who owes the ledger tests still marked `not yet written`

asked: 2026-11-20
answer: "Ein Prüfpunkt vor Phase 6 (Recommended)" — (1) before pytest the runner checks every selected ledger id, names each missing one and still runs the tests that stand; (2) an `implement` attempt owes every ledger test, as today; a `repair` attempt owes only the tests of its findings, and unwritten ledger tests are named in its record without failing it; (3) `review` (phase 6) refuses while any ledger entry is still `not yet written`, naming the entries and the next step.
answered_by: maintainer
status: answered
context: |
  Topic: the runner's cheap check after an implement or repair attempt (bead coding-harness-bxxt.9, diagnosed by bead coding-harness-ogfn).
  Intention: on 2026-11-18 two repair attempts of lane verify-slots failed with pytest exit 5 'no tests ran' because ten ledger tests of a redrafted plan were not yet written; under -n auto pytest-xdist names none of them, and a repair of one finding had to write tests unrelated to it.
  Today: implement and repair both owe every ledger test still marked `not yet written`; the runner hands the ids to pytest unchecked and reports only 'exited 5'; the ledger gate (scripts/check_criterion_ledger.py) accepts unwritten entries while a change is live and refuses them only once the change is archived; phase 6 does not look at them.
  Repository change: scripts/stage2.py (test selection, cheap check, phase-6 admission) and tests.
  Architecture change: the debt of unwritten ledger tests gets one check point, the entry to phase 6, instead of falling on whichever attempt runs next.
alternatives: |
  - One check point before phase 6 (chosen): the debt cannot slip through and shows at one fixed place.
  - Implement owes, repair does not, no new check point: less code, but unwritten tests can reach the pull request and show only at archiving.
  - Only name the missing ids: failures become readable, but repairs keep failing on unrelated scope.

In the context of ledger tests a redrafted plan marks `not yet written`,
facing repair attempts that failed unnamed on tests unrelated to their
findings, we decided that the runner names missing ids before pytest and
runs the rest, that implement owes every ledger test while repair owes only
its findings' tests, and that phase 6 refuses while a ledger entry is still
unwritten, to achieve one place where that debt is collected, accepting a
new refusal at the phase-6 entry — 2026-11-20

## Q-2 · Recut after the third spec-review round

asked: 2026-11-20
answer: "Neu schneiden (Recommended)" — this change builds parts 1 and 2 of Q-1 only: the runner names every selected ledger id that does not stand before pytest and still runs the rest; an implement attempt owes every ledger test, a repair attempt only its findings' tests. Part 3, the phase-6 check point for entries still marked `not yet written`, becomes bead coding-harness-bxxt.10 with its own interview. The final draft after round three gets no new review.
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 3 of this change, row S-16 (BLOCKER).
  Intention: part 3 did not settle in three rounds: after a phase-6 refusal no route writes the debt row, and five further rows concern its form, status and edge cases.
  Today: without part 3 an unwritten ledger test shows only when the change is archived; the criterion-ledger gate turns it red there.
  Repository change: scripts/stage2.py without the phase-6 check point.
  Architecture change: none in this change; the debt route is decided in bead coding-harness-bxxt.10.
alternatives: |
  - Recut (chosen): the bug that lets repairs fail unnamed goes quickly.
  - A fourth round with a new debt route: one change, more scope and an undecided route.
  - Send the lane back to implement: no new route, but whether implement may rerun after acceptance is unchecked.

In the context of a phase-6 check point that three spec-review rounds left
without a route for its debt rows, facing a BLOCKER in the last allowed
round, we decided to build only the naming of missing ledger ids and the
narrower repair duty here and to move the check point to bead
coding-harness-bxxt.10, to achieve a quick fix of unnamed repair failures,
accepting that unwritten ledger tests show only at archiving until then — 2026-11-20
