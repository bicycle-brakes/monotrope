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
rule mechanically, accepting that the session still starts the named verb — 2026-11-20

## Q-2 · ADR 0021 decision 7 and the new next-step line

asked: 2026-11-20
answer: "Ergänzung zu ADR 0021 (Recommended)" — decision 7's "exhausting eligible stages with accepted findings also stops and reports to the maintainer" is amended by a decision pull request of its own: a consumed ladder whose taken rows are repaired goes to phase 6, one with open taken rows to the repair; the repair brake (two rounds of repair-caused findings) stays. This change merges after that amendment.
answered_by: maintainer
status: answered
context: |
  Topic: spec-review row S-4 of this change.
  Intention: ADR 0021 decision 7 and the behaviour of this change contradict each other; an agent may not edit an ADR.
  Today: the ADR is unchanged; AGENTS.md (PR #419) already states the new rule.
  Repository change: a decide(...) pull request amending ADR 0021, drafted by the orchestrator, merged by the maintainer.
  Architecture change: when the review loop escalates to the maintainer.

In the context of an ADR that still escalates every consumed ladder to the
maintainer, facing a runner that will name the next step instead, we decided
to amend ADR 0021 decision 7 in a decision pull request of its own and merge
this change after it, to achieve that ADR and code agree, accepting one more
pull request — 2026-11-20

## Q-3 · The AGENTS.md rule after the change

asked: 2026-11-20
answer: "Ja, im hwll-PR (Recommended)" — the AGENTS.md bullet "An exhausted review ladder goes to phase 6" is reworded in this change's pull request to: "when every stage of a `review-loop` run is consumed and the last round was not clean, the runner names the next step: `next: review <change>` once every taken row of that round is repaired, `next: repair <change>` before; phase 6 checks that last repair."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review row S-5 of this change.
  Intention: the rule must name the state the runner reports, not a refusal that no longer happens.
  Today: the bullet begins "when `review-loop` refuses because every stage … is consumed".
  Repository change: one bullet of AGENTS.md, in this change's pull request.
  Architecture change: none.

In the context of an AGENTS.md rule worded around a refusal, facing a runner
that will end with exit 0 and a next-step line, we decided to reword the rule
in this change's pull request, to achieve one statement in rule and runner,
accepting a held file in the change's diff — 2026-11-20

## Interview minimum

Bounded class: one question, answered (Q-1). The reading of "phase 6 checks
that last repair" is the existing phase-6 path (the full `make verify` before
the reviewer and the reviewer's whole-diff read); no extra check is added
([DETAIL], decided by the orchestrator: the rule's own text names no other
check).
