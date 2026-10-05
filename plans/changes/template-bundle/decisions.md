---
title: "Decisions — template-bundle"
status: draft
implementation_status: none
date: 2026-09-30
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-9qo
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-30"}
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

## Addendum 2026-10-05: the maintainer's answers

The maintainer went through the provisional answers one at a time in the
Claude Code session on 2026-10-05:

1. **Q1 — scope: changed to (c), the contract core plus the design phase
   2b.** The three templates stay; the design phase (a prompt
   `prompts/02b-design.md` and a `design.md` template) is added to this
   change. ROADMAP and arc42 stay on the not-now list.
2. **Q2 — findings table: (b) confirmed**, the practised table.
3. **Q3 — protected areas and failure mode: (b) confirmed**, mapped onto
   existing spec parts.
4. **Q4 — LikeC4 and D-15: open.** The maintainer asked for a check whether
   LikeC4 makes sense before deciding; a research note is being written
   (`docs/research/2026-10-05-likec4.md`, branch `docs/research-likec4`).
   The design template's "model-as-code delta" section follows that answer.
5. **Q5 — design-phase duty: (a), D-14 as decided.** Mandatory for
   `architectural`, a one-sentence reason in `spec.md` when a `feature`
   skips it, absent for `bounded` and `spike`; stated in the workflow and
   not checked until the validator (bead coding-harness-jc3) lands. D-14 is
   unchanged, so no ADR is needed for it.

Still to answer before phase 7: Q4, the class (`feature`, as the spec
review found) and the ADR question for this change.

## Addendum 2026-10-05 (later): LikeC4, ROADMAP and arc42 after the research

The maintainer asked for a check of LikeC4, ROADMAP and arc42 and answered
after reading its result (`docs/research/2026-10-05-likec4-roadmap-arc42.md`,
PR #69), one question at a time:

6. **Q4 — LikeC4: amend D-15 and O-3 by an ADR toward Mermaid.** In its own
   decision PR (ADR 0009): an architecture delta lives in `design.md` as a
   Mermaid diagram plus lists of what is added, changed or removed; LikeC4
   stays the upgrade path with the research's revisit triggers. This
   change's `design.md` template uses that form and names ADR 0009; the
   ADR merges first.
7. **ROADMAP: try the file first.** A `ROADMAP.md` in Coding Harness with at
   most three "Now" themes, checked at every hand-over; a kit template only
   after it stays true through two hand-overs. That is its own change, not
   part of this one.
8. **arc42: a skeleton now, in this change.** The research recommended "not
   now"; the maintainer chose the skeleton. arc42 is licensed CC BY-SA 4.0
   and the kit Apache-2.0, so the skeleton is written in this repository's
   own words with arc42's section structure, attributes arc42 and links its
   template instead of copying its text; the licence point is checked and
   recorded, not assumed.

Scope of this change from now on: the three templates, the design phase 2b
(prompt and `design.md` template) and an arc42 skeleton.
9. **arc42 licence: the skeleton carries CC BY-SA 4.0** (maintainer,
   2026-10-05, option 1 of the spec's open question). arc42's licence covers
   its structure and headings, so an own-words skeleton is still an
   adaptation. `templates/arc42.md` states CC BY-SA 4.0 visibly and credits
   arc42; it is the one exception in a kit meant to be Apache-2.0 (bead
   coding-harness-lir). This is an assessment, not legal advice; both
   repositories are private, so nothing is shared today.
