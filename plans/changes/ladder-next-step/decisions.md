---
title: "Decisions — ladder-next-step"
category: decisions
status: draft
implementation_status: none
date: 2026-11-20
created: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-hwll
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, review-loop, stage-2]
---

# ladder-next-step — Decisions

Class: bounded (bead coding-harness-hwll; one answered question is owed — Q-1
below, answered by the maintainer in the conversation of 2026-11-20).

## Q-1 · How the runner carries the rule "an exhausted ladder goes to phase 6"

asked: 2026-11-20
answer: "Ja" — to the orchestrator's proposal, after the maintainer asked for the smartest solution: at an exhausted ladder `review-loop` ends as a normal result (exit 0), not a refusal, and prints one fixed line, `next: review <change>` when every taken row of the last round is fixed and `next: repair <change>` while a taken row is open; `review-loop` does not start phase 6 itself.
answered_by: maintainer
status: answered
context: |
  Topic: the AGENTS.md rule "An exhausted review ladder goes to phase 6" (maintainer, 2026-11-20, PR #419), carried by the runner (bead coding-harness-hwll).
  Intention: house rule 9 — a rule takes hold through code, not prose. On 2026-11-19/20 the refusal of an exhausted ladder stopped the slip-counter and findings-per-model lanes until the orchestrator applied the rule by hand.
  Today: when every stage of a run is consumed and the last round was not clean, `review-loop` refuses and says the loop stops and reports to the maintainer.
  Repository change: `scripts/stage2.py` (the exhausted-ladder branch of `review-loop`) and its tests; the doctrine sentence in `docs/WORKFLOW.md` if it names the refusal.
  Architecture change: none — no new route; the runner names the next verb, the session runs it.
alternatives: |
  - Name the next step (chosen): small; each verb still does one thing.
  - review-loop starts phase 6 itself: no hand step, but one verb would run two phases including the full make verify on the one verify slot, and abort and resume get harder.
  - Later, the rule stays prose: a session that never read AGENTS.md stops at an exhausted ladder.

In the context of review-loop runs whose ladder is consumed before a clean
round, facing lanes that stopped overnight because the refusal named no next
step, we decided that review-loop ends with exit 0 and one fixed `next:` line
naming `review` or `repair` for the change, and does not start phase 6
itself, to achieve that any session — and the night-run wake — follows the
rule mechanically, accepting that the session still starts the named verb.

## Interview minimum

Bounded class: one question, answered (Q-1). The reading of "phase 6 checks
that last repair" is the existing phase-6 path (the full `make verify` before
the reviewer and the reviewer's whole-diff read); no extra check is added
([DETAIL], decided by the orchestrator: the rule's own text names no other
check).
