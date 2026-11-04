---
title: "Decisions — explore-provenance"
category: decisions
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, explore, provenance]
---

# explore-provenance — Decisions

Class: bounded (bead coding-harness-g19n).

## Q-1 · How far the change goes

asked: 2026-11-04
answer: "B: Runner plus Altbestand" — the runner sets research.md to `provenance: ai-drafted-reviewed` with `produced_by` and `review` and drops the skeleton note after every explore (Flash and research swarm), proved by a test; and every open research.md that still carries the skeleton's `human-written` provenance after a model filled it is corrected in the same change.
answered_by: maintainer
status: answered
context: |
  Topic: every Flash explore leaves research.md with provenance human-written and the "empty until it has run" note (bead coding-harness-g19n); the earlier fix (bead coding-harness-er46, closed) does not hold on main d167b0e6.
  Intention: on 2026-11-04 this cost a review-loop row and a repair in two changes (raising-fault-test, swarm-time-limits).
  Today: the explore verb appends the model's answer under the skeleton and leaves the header as it was.
  Repository change: the explore verb rewrites the header and drops the note; open research.md files are corrected once.
  Architecture change: none.

In the context of explores that leave research.md marked as human-written, facing a review-loop row and a repair per change for it, we decided to fix the explore verb and correct every open research.md at once, to achieve truthful provenance without later loop rows, accepting a diff that touches change folders other lanes own. — 2026-11-04
