---
title: "Decisions — template-bundle"
status: draft
implementation_status: none
date: 2026-10-01
last_reviewed: 2026-10-01
updated: 2026-10-01
supersedes: null
superseded_by: null
bead: coding-harness-9qo
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-01"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# template-bundle — Decisions

**Provisional answers, chosen by the agent, awaiting the maintainer.** The
maintainer is away until Sunday 2026-10-04 and asked on 2026-09-30 that the
session work off as much of the plan as possible meanwhile. The phase 1a
interview could not be held. The orchestrating session took each
recommendation of `research.md` ("Open points for the phase 1a interview")
as a provisional answer. Nothing here takes effect before the maintainer
merges the pull request (house rule 8); the pull request lists every answer
for confirmation, and any answer the maintainer changes is reworked before
the merge.

## Provisional answers

1. **Q1 — scope: (b), the contract core.** A spec template, a findings
   template and a decision-record (MADR) template; the plan-marking template
   is retired, not moved (open PR #60 retires plan marking); the two dead
   template links are repaired. The design phase 2b, ROADMAP, arc42 and
   LikeC4 go to the not-now list, each with the trigger that brings it back.
   The tracker writer re-scopes bead coding-harness-9qo and opens one bead
   for the not-now parts.
2. **Q2 — findings table: (b), the practised table** (`ID | Severity |
   Dimension | Origin | Where | Finding | Status`), plus the stage-2 columns
   as defined once PR #60 is merged, named as such. Bead coding-harness-4me
   may later add its machine-readable list on top.
3. **Q3 — protected areas and failure mode: (b), mapped onto what specs
   have.** The failure mode is each criterion's "Refuted by" line; the
   template has a short "Protected areas" list that the Definition of Done
   points to, and no separate failure-mode section.
4. **Q4 — LikeC4 and D-15: (a), D-15 stays and LikeC4 is deferred.**
   Amending D-15 to match LakeSwitch's D-58 would be its own decision PR
   with an ADR, not a side effect of this change.
5. **Q5 — design phase duty: not asked**, because Q1 put the design phase
   on the not-now list.

## Details the orchestrator adds

- The spec template's size field is called **appetite**, the same word the
  parallel change `adhd-frame` (bead coding-harness-q24) uses in the phase
  prompts, so the two do not name one concept twice.
- The spec template follows the criterion form that open PR #60 adds to
  `prompts/02-spec.md` (one condition per criterion, When / While / If)
  only as a recommendation, because #60 is not merged.
