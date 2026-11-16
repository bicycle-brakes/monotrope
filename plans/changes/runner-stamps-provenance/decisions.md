---
title: "Decisions — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: claude-opus-5-5, version: "2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# runner-stamps-provenance — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).
Exploration: `research.md` (GLM 5.3 Flash, 2026-11-16). The bead
(coding-harness-f9sv) states the problem and the four-part fix; the
answers below were given in conversation on 2026-11-16 and recorded in the
bead's notes the same day; this file copies them from there.

## Q-1 · How the rule "no hand-written provenance" is enforced

context: |
  Topic: artifact headers (`produced_by`) written by hand.
  Intention: 50 `research.md` headers on main (2026-11-16) carry a free-form
  `produced_by`; a lane went red on one. House rule 9 says a rule holds
  through a check that goes red.
  Today: models and sessions write the header by hand; only `findings.md`
  is stamped by `scripts/stage2.py`.
  Repository change: a red check per case (this header), or one general
  detector of side routes.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "pro Fall"
answered_by: maintainer
status: answered


In the context of hand-written artifact headers, facing a free-form `produced_by` that keeps failing the census rule, we decided to make the rule red per case at the header's own check, to achieve that this header can no longer be written wrongly, accepting that other hand-written fields need their own checks.
— 2026-11-16

## Q-2 · What happens to the existing free-form headers

context: |
  Topic: the 50 existing headers that fail the census rule.
  Intention: a stamping runner and a red check leave the old headers red
  or exempt.
  Today: archived changes carry most of them.
  Repository change: migrate all headers once, or exempt archived changes.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "migrieren"
answered_by: maintainer
status: answered


In the context of 50 existing free-form headers, facing a new red check, we decided to migrate every header once, archived ones included, to achieve one rule without exemptions, accepting a large one-time diff.
— 2026-11-16

## Q-3 · Order

context: |
  Topic: when this change runs.
  Intention: it removes the most frequent source of hand repairs.
  Today: queued behind other lanes.
  Repository change: none.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "ja" (to: start it as the next lane, before lane 10)
answered_by: maintainer
status: answered

In the context of the lane queue, facing the most frequent source of hand repairs, we decided to start this change as the next lane, before lane 10, to achieve fewer hand steps, accepting that lane 10 waits.
— 2026-11-16
