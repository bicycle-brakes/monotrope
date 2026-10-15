---
title: "Decisions — sol-effort"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-14
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

## Q-3 · Whether the ADR amendments stay in this change (finding S-2)

asked: 2026-10-14
answer: the ADR amendments to ADR 0016 and ADR 0017 are taken out of this change; they follow in a change of their own once the three missing interview answers exist. This change keeps the runner, the active instructions and the tests.
answered_by: maintainer
status: answered

The phase 2a review found that editing a claimed ADR needs five interview
records and this change has two (`findings.md`, S-2). The orchestrating
session proposed on 2026-10-14: "die ADR-Änderungen aus #143 herausnehmen und
nach den drei fehlenden Interview-Antworten nachholen". The maintainer
answered "ja" the same day.

In the context of an ADR edit that the interview minimum blocks, facing the
choice between waiting for three more answers and splitting the ADR
amendments off, we decided to split them off to achieve that the runner stops
spending Sol at `max` now, accepting that ADR 0016 and ADR 0017 name `max`
until their amendment merges. — 2026-10-14

## Q-4 · Which texts change with the effort (finding S-1)

asked: 2026-10-14
answer: the effort of each Sol verb is set in one central place, where it can be changed once and simply; runner, instructions and tests take it from there instead of each repeating the value.
answered_by: maintainer
status: answered

The maintainer's words, 2026-10-14, asked whether only tables and Model lines
or also the prose of `docs/WORKFLOW.md` change: "ich brauche ein zentrale
stelle wo sich sowas parametrisiert und einmal einfach umstellen lässt". How
the instructions point to that place, and which file it is, is left to the
design.

In the context of the effort being written in the runner, four prompts, the
workflow tables and its prose, facing the choice between editing every
mention and one central parameter, we decided on one central parameter to
achieve that a later change of effort is one edit, accepting a larger change
now than renaming `max` where it stands. — 2026-10-14

## Q-5 · What the doctrine check counts (finding S-4)

asked: 2026-10-14
answer: only the effort attached to Sol counts; another model's effort in the same row, such as Sonnet 5.5 at `medium`, stays allowed.
answered_by: maintainer
status: answered

The maintainer chose the recommended option on 2026-10-14 ("Nur Sols
Aufwand").

In the context of rows that name Sol beside other models, facing the choice
between reading the effort per model and refusing any `max` or `medium` in a
Sol row, we decided to read the effort per model to achieve that correct rows
stay green and non-Sol text stays untouched, accepting a more involved check.
— 2026-10-14

## Q-6 · What the test of the resumed phase-6 call proves (finding S-3)

asked: 2026-10-14
answer: the test proves that the runner passes effort `high` on the resumed call's arguments; whether a thread first started at `max` then really works at `high` is not proven.
answered_by: maintainer
status: answered

The maintainer chose option A on 2026-10-14 ("A"), after the question was
explained: the first phase-6 review continues an earlier recorded Codex
thread of the same change (ADR 0016), which may have run at `max`.

In the context of a resumed Codex thread whose inner effort is not visible
from outside, facing the choice between an argument check offline and a live
paid call, we decided on the argument check to achieve a test that runs in
`make verify`, accepting that what Codex does inside a resumed thread stays
unproven. — 2026-10-14
