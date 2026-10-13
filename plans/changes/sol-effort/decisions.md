---
title: "Decisions — sol-effort"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-yzk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, codex, effort]
---

# Sol runs at an effort per verb — Decisions

Phase 1a for bead coding-harness-yzk, on 2026-10-13. Both questions were
answered by the maintainer in the conversation that day before this file was
written; it records those answers, it asked nothing new.

## Q-1 · Which effort each Sol verb gets

asked: 2026-10-13
answer: repair `medium`; draft (spec, design and plan) `high`; phase-6 review `high`. No Sol call keeps `max`.
answered_by: maintainer
status: answered

The maintainer's words, 2026-10-13: "Mache Sol nur mit hoch", then "Bitte
nutze für Korrektur mit Codex Sol mit Medium, für das Entwerfen der Spec Sol
mit high". The second sentence sets repair and draft; the first still covers
the review.

In the context of the Codex five-hour limit running out after about ten
max-effort Sol calls in one afternoon, facing the choice between `max` for
every verb and an effort per verb, we decided on medium for repairs and high
for drafts and reviews to achieve more Sol calls per five-hour window,
accepting that a repair or a review at a lower effort may miss what `max`
would have found. — 2026-10-13

## Q-2 · How the change is recorded

asked: 2026-10-13
answer: dated amendments to ADR 0016 (draft effort) and ADR 0017 (repair and review effort), no new ADR.
answered_by: maintainer
status: answered

The maintainer agreed to the night queue of 2026-10-13 with "Ja"; its item
for this bead read "recorded as a dated amendment to ADR 0016 and 0017, not
as a new ADR".

In the context of an effort that both ADRs name, facing the choice between a
new ADR and amendments, we decided on dated amendments to achieve that each
ADR still states its own route completely, accepting two ADR files touched by
one change. — 2026-10-13
