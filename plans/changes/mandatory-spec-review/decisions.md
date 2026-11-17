---
title: "Decisions — mandatory-spec-review"
category: decisions
status: draft
implementation_status: none
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-ttic
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, spec-review, stage-2, runner]
---

# mandatory-spec-review — Decisions

Class: bounded (bead coding-harness-ttic: doctrine plus one runner check).

The intent itself is settled and not asked again: the maintainer answered
"jaja" on 2026-11-16 to making the Opus spec review (phase 2a) mandatory
before a plan card for the classes `bounded`, `feature` and `architectural`,
with `spike` exempt (bead description). ADR 0016 point 5 already decides that
Opus 5.5 reviews the spec for every change stage 2 routes; this change aligns
the doctrine and the runner with it, no ADR change (bead notes, 2026-11-16).

## Q-1 · Which changes the new refusal reaches

asked: 2026-11-17
answer: "C" — the refusal applies to implement calls from the merge of this change on; changes already implemented stay untouched (a later implement call needs the review). In addition the morning handover lists open changes without a spec review, and the maintainer decides per change whether one is caught up (xul8 already planned).
answered_by: maintainer
status: answered
context: |
  Topic: the runner will refuse `stage2.py implement` while a change's spec has no spec-review rows dated after the spec's last change, or has open [AMBIGUITY] rows (bead coding-harness-ttic).
  Intention: decided before the night run 2026-11-17-a so the lane can build without waiting; open changes already exist that were planned or implemented without a spec review, so the reach of the refusal has to be fixed first.
  Today: phase 2a is called optional in AGENTS.md and docs/WORKFLOW.md; nothing in the runner checks for spec-review rows, so implement runs whether or not a review was held; two plan cards were shown unreviewed on 2026-11-16.
  Repository change: the doctrine marks phase 2a mandatory for bounded, feature and architectural changes; the runner's implement verb refuses without a current spec review; the morning handover lists open changes that have none.
  Architecture change: none; one more precondition in an existing runner verb, no new verb, gate or ADR.

In the context of making the phase-2a spec review mandatory before implement, facing open changes that were planned or implemented without one, we decided that the runner's refusal applies to every implement call from the merge of this change on, leaves already implemented changes untouched, and that the morning handover lists open changes without a spec review for the maintainer to decide per change, to achieve that no new implementation starts from an unreviewed spec without retroactively blocking finished work, accepting that changes implemented before the merge stay unreviewed until the maintainer chooses to catch one up. — 2026-11-17

*Note (2026-11-17, recording agent): the answer is taken verbatim from the
bead notes of coding-harness-ttic ("2026-11-17 interview (night prep, answer
C)"). The exact wording of the question shown before the night run was not
recorded there; the context above is restated from the bead description and
notes, not invented beyond them.*
