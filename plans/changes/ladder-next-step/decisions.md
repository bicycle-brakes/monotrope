---
title: "Decisions — ladder-next-step"
category: decisions
status: draft
implementation_status: none
date: 2026-11-20
created: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-24
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

## Q-4 · Ambiguity S-8 (expired-terms stage in a consumed ladder)

asked: 2026-11-21
answer: "An unconsumed rung whose admission no longer holds (terms expired / valid_until passed) counts as consumed for the next-step rule, so the runner names the next step (next: review <change> or next: repair <change>) instead of launching a round that refuses. (Detail for Flash stage: if every member of an unconsumed stage is no longer admissible, the stage counts as consumed; if at least one member remains admissible or replaceable, the stage remains eligible.)"
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 2 ambiguity row S-8 of ladder-next-step.
  Intention: determine whether an unconsumed rung with expired data terms blocks the exhausted-ladder next-step rule.
  Today: `next_stage` still returns an unconsumed rung whose `valid_until` passed, and launching it refuses with `terms_problem` (exit 2).
  Repository change: `scripts/stage2.py` (`next_stage` / consumed-ladder check) and its spec/tests in `plans/changes/ladder-next-step/`.
  Architecture change: none — aligns eligibility with admission inside the consumed-ladder check.

In the context of a snapshot holding an unconsumed rung whose terms reading
has expired, facing a runner that would otherwise refuse at launch instead of
naming the next step, we decided that an expired rung counts as consumed for
the next-step rule (and a Flash stage counts as consumed when none of its
members remain admissible or replaceable), to achieve a clean transition to
repair or phase 6 without manual stage retirement, accepting that a stage with
expired terms is not retried automatically — 2026-11-21

## Q-5 · Ambiguity S-9 (cut-diff round in a consumed ladder)

asked: 2026-11-21
answer: "A round whose diff was cut is not clean for the next-step rule, even when zero findings were accepted; the next step follows the taken rows (next: repair <change> if any taken row is unrepaired, else next: review <change>)."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 2 ambiguity row S-9 of ladder-next-step.
  Intention: clarify whether a consumed ladder ending on a cut-diff round with no accepted findings counts as clean or emits `next:`.
  Today: `clean_round` returns true when zero rows were accepted, yet the clean-round stop does not fire on a cut diff, leaving today's refusal active.
  Repository change: `scripts/stage2.py`, `plans/changes/ladder-next-step/spec.md` Terms, and tests.
  Architecture change: none — keeps cut-diff rounds non-terminal so phase 6 reviews the whole diff.

In the context of a consumed ladder whose final round had a cut diff and no
accepted findings, facing a clean-round stop that already refuses to end the
loop on a cut diff, we decided that a cut-diff round is not clean for the
next-step rule and follows the taken rows (`next: repair` or `next: review`),
to achieve consistent handoff to phase 6 on the whole diff, accepting that
zero-finding cut rounds still trigger phase 6 — 2026-11-21

## Interview minimum

Bounded class: one question, answered (Q-1). The reading of "phase 6 checks
that last repair" is the existing phase-6 path (the full `make verify` before
the reviewer and the reviewer's whole-diff read); no extra check is added
([DETAIL], decided by the orchestrator: the rule's own text names no other
check).

## Q-6 · The next-step instruction as a JSON file

asked: 2026-11-24
answer: "B — besides the standard-output line, the runner writes the current next-step instruction as a JSON file beside the loop record, `$XDG_STATE_HOME/coding-harness/stage2/<change>@<digest>/next.json`, atomically (temporary file, then replace) and validated against a declared schema: schema version, change, verb (`review`, `repair` or `hand`), the row ids for `hand`, the producing verb and the UTC time it was written. It is never written into loop.md or any other Markdown file; consumers such as `scripts/lanes.py advance` (bead coding-harness-z40g) read only this file. Maintainer rule of 2026-11-24: code before prose; Markdown only where it cannot be avoided. Options put: keep the line in loop.md behind one reader function (recommended at the time); the JSON file now (chosen); wait for bead coding-harness-5ane.11."
answered_by: maintainer
status: answered
context: |
  Topic: where the next-step instruction is kept.
  Intention: make the instruction machine state instead of Markdown, following the state-first direction of bead coding-harness-5ane.11 (draft ADR in PR #445).
  Today: the instruction exists only as a standard-output line; advance-verb Q-11 had planned a line in loop.md.
  Repository change: review-loop (and the hand-step case of advance-verb Q-12) write next.json in the runner state directory; a schema file and its validator.
  Architecture change: a new machine-state file in the runner state directory; no ADR in this pull request.

In the context of the next-step instruction, facing Markdown parsed back as control state, we decided on a schema-validated JSON file beside the loop record, to achieve state that code reads without patterns, accepting a fourth spec review — 2026-11-24

## Q-7 · Fourth spec-review round

asked: 2026-11-24
answer: "authorized — the maintainer answered yes on 2026-11-24: one fourth spec-review round (Opus, phase 2a) of the draft c0c8ea95, because Q-6 changes the spec after the third round. Options put: a fourth review for both lanes (recommended); re-slice the JSON instruction into its own change."
answered_by: maintainer
status: answered
context: |
  Topic: whether the changed spec is reviewed again.
  Intention: the runner admits a spec change after round three only with this authorization.
  Today: AGENTS.md phase 2a ends spec review after round three.
  Repository change: none.
  Architecture change: none.

In the context of a spec changed after its third review, facing an unreviewed contract, we decided on one fourth spec review, to achieve a checked spec before phase 4, accepting one more Opus run — 2026-11-24
