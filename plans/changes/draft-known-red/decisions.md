---
title: "Decisions — draft-known-red"
category: decisions
status: draft
implementation_status: none
date: 2026-11-22
created: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-83e
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage2, draft]
---

# draft-known-red — Decisions

Class: feature (bead coding-harness-83e; the maintainer's answer B on 2026-11-22 amends ADR 0016, so the change carries an ADR addendum).

## What the research changed (orchestrator, 2026-11-22)

The bead (2026-10-17) wanted two things: (1) a draft that touches only plans and docs is judged by the gates its files can break, not by a known-red test suite; (2) a Sonnet fallback when GLM fails, since `--stage2-off` is refused for `draft`.

Part (1) is already in place: the draft runs only the document subset of the gate registry (`document_gates` in `scripts/stage2.py`, `docs/WORKFLOW.md` §4 "The draft"), and every draft record of 2026-11-21 says "document checks only, no tests ran". A known-red pytest can no longer fail a draft. Part (2) is still open: `scripts/stage2.py` refuses `--stage2-off` for every verb except explore, implement and repair, and the draft's route list ends at GLM 5.3.

## SKIP · interview

status: skipped
reason: The bead states what is wanted (a Sonnet fallback for the draft when GLM fails, and the draft judged by the gates its files can break); the first part is already merged, the second is a route addition in the existing Stage-1 pattern. The maintainer asked for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Scope narrows to the route.** Part (1) is recorded as already done, with the evidence above; this change adds no gate selection.
- **`--stage2-off [REASON]` is accepted for `draft`,** with the same record line and reason as explore, implement and repair; the model is Opus 5.5 at effort `xhigh` (Q-1, superseding the earlier Sonnet reading). Reason: one pattern for all writing verbs; the bead names the refusal as the gap.
- **The automatic fallback:** after the GLM 5.3 attempt fails (call failure or red document check), the draft does not fall through to Sonnet on its own; the runner's final message names `--stage2-off` as the next step. Reason: `docs/WORKFLOW.md` §3 says a failed model process stops instead of silently changing route, and the relaxation for writing attempts belongs to coding-harness-s9r / coding-harness-6ie, whose maintainer decision of 2026-10-16 is not yet implemented.
- **A failed draft keeps its work visible:** unchanged; the attempt refs under `refs/stage2/attempts/` already hold it, and the final message names them.

## Q-1 · The draft's Stage-1 route against ADR 0016 decision 9

asked: 2026-11-22
answer: B — amend ADR 0016: `--stage2-off` is accepted for `draft`, and the Stage-1 draft runs on Opus 5.5 at effort `xhigh`, as `docs/WORKFLOW.md` §3 assigns phases 2, 2b and 3 — not on Sonnet. The amendment is an ADR addendum to decision 9.
answered_by: maintainer
status: answered
context: |
  Topic: whether the draft gets a Stage-1 route, and on which model.
  Intention: spec-review round 1 found that accepted ADR 0016 (human-decided), decision 9, says "Where Stage 2 is off, Opus 5.5 drafts by hand as §3 says; draft has no Stage-1 route", while this change adds exactly that route (F-1), and that §3 gives phases 2, 2b and 3 to Opus at effort xhigh, not to Sonnet (F-2).
  Today: the draft's route list ends at GLM 5.3; --stage2-off is refused for draft; the orchestrator drafts by hand when every route fails.
  Repository change: Options: A close the bead as done (part 1 merged, part 2 conflicts with the ADR); B amend ADR 0016 and add a Stage-1 draft route on Opus xhigh; C keep the Sonnet route as drafted.
  Architecture change: ADR 0016 decision 9 amended by an addendum.

In the context of a draft whose every route failed, facing a hand draft or a runner route, we decided to amend ADR 0016 so that --stage2-off runs the draft on Opus 5.5 at effort xhigh, to achieve night runs that draft without the orchestrator's hand, accepting more load on the runner account's Opus limits and an ADR addendum. — 2026-11-22
