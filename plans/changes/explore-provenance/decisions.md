---
title: "Decisions — explore-provenance"
category: decisions
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-06
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

## Q-2 · The whole metadata contract (loop rows L4-1, L5-2, L6-1, L6-4)

asked: 2026-11-06
answer: "Ganzen Kopf prüfen (Recommended)" — the census checks the whole research metadata contract (provenance, produced_by, pending review, dates) for every active model-written research file, and one script normalises every active research file once.
answered_by: maintainer
status: answered
context: |
  Topic: the change corrects research files written by a model whose header claims human authorship; a census test is to prevent it.
  Intention: the review loop found the same mechanism a third time (L4-1, L5-2, L6-1/L6-4); the rule ends case repair at the second finding of one mechanism.
  Today: the census checks only "human-written" and the empty skeleton, not the rest of the header.
  Repository change: one script normalises all active research files; the test checks the whole header.
  Architecture change: none.

In the context of a census that each round found one more gap in, facing a third finding of one mechanism, we decided to check the whole metadata contract and normalise every active research file once, to achieve a census that finds further gaps itself, accepting a change that touches research files of other changes. — 2026-11-06

## Q-3 · Spec and plan follow Q-2; producer knowledge is kept (loop rows L7-1 to L7-4)

asked: 2026-11-06
answer: "Spec anpassen, Wissen erhalten (Recommended)" — spec and plan are redrafted to cover Q-2's scope (the normalisation script and every active research file, no longer protected areas for this purpose); research written by several models keeps them as a list instead of collapsing them into one entry; then repair and review.
answered_by: maintainer
status: answered
context: |
  Topic: after Q-2 the repair built a script that normalises every active research file.
  Intention: round 7 reported a BLOCKER — about 40 research files of other lanes, protected by the spec, were changed, and the script is not in the plan; it also collapses several models (for example "GLM 5.3 Flash and Claude Haiku 5.5") into one entry, losing who wrote what.
  Today: spec and plan predate Q-2 and do not know the larger scope; the lane's appetite is already spent.
  Repository change: spec and plan redrafted; the script stays.
  Architecture change: none.

In the context of a repair that followed the maintainer's wider answer while spec and plan did not, facing a BLOCKER for touching protected files and a loss of producer knowledge, we decided to redraft spec and plan to Q-2's scope and keep every producing model as a list, to achieve a change that does what was decided without losing provenance, accepting about one to two hours beyond the spent appetite. — 2026-11-06
