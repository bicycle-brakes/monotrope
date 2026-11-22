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

Class: bounded (bead coding-harness-83e proposed `feature` on 2026-10-27, "to confirm"; after the research below only the route part is left, which is bounded).

## What the research changed (orchestrator, 2026-11-22)

The bead (2026-10-17) wanted two things: (1) a draft that touches only plans and docs is judged by the gates its files can break, not by a known-red test suite; (2) a Sonnet fallback when GLM fails, since `--stage2-off` is refused for `draft`.

Part (1) is already in place: the draft runs only the document subset of the gate registry (`document_gates` in `scripts/stage2.py`, `docs/WORKFLOW.md` §4 "The draft"), and every draft record of 2026-11-21 says "document checks only, no tests ran". A known-red pytest can no longer fail a draft. Part (2) is still open: `scripts/stage2.py` refuses `--stage2-off` for every verb except explore, implement and repair, and the draft's route list ends at GLM 5.3.

## SKIP · interview

status: skipped
reason: The bead states what is wanted (a Sonnet fallback for the draft when GLM fails, and the draft judged by the gates its files can break); the first part is already merged, the second is a route addition in the existing Stage-1 pattern. The maintainer asked for no question windows until the block on 2026-11-23 10:00. The details are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Scope narrows to the route.** Part (1) is recorded as already done, with the evidence above; this change adds no gate selection.
- **`--stage2-off [REASON]` is accepted for `draft`,** with the same Stage-1 route, record line and reason as explore, implement and repair. Reason: one pattern for all writing verbs; the bead names the refusal as the gap.
- **The automatic fallback:** after the GLM 5.3 attempt fails (call failure or red document check), the draft does not fall through to Sonnet on its own; the runner's final message names `--stage2-off` as the next step. Reason: `docs/WORKFLOW.md` §3 says a failed model process stops instead of silently changing route, and the relaxation for writing attempts belongs to coding-harness-s9r / coding-harness-6ie, whose maintainer decision of 2026-10-16 is not yet implemented.
- **A failed draft keeps its work visible:** unchanged; the attempt refs under `refs/stage2/attempts/` already hold it, and the final message names them.
