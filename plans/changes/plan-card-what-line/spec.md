---
title: "Spec — plan-card-what-line"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-kg8n
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-22", model: "glm-5.3"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, plan-card]
class: bounded
adr_files: []
---

# Spec — plan-card-what-line

Plan cards explain the change in plain words without requiring the spec (bead
`coding-harness-kg8n`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- The existing five card fields describe the delivery and its evidence, but
  do not require an explanation of the problem, an example and the change;
  on 2026-11-11 the maintainer had to ask at a plan card what the work does,
  and asked that every card carry it (research, "The decision this change
  carries", 2026-11-22).
- The draft check and the prompt-form test enforce the existing card's field
  order, so adding a field to the instruction alone would not protect it
  (research, "Who enforces the card today", 2026-11-22).

## Terms

- **Adoption day** — the day recorded for `plan-card-what-line` in
  `decisions/adoption.yaml`, read through `scripts/adoption.py`; it is this
  change's merge date.
- **Subject plan** — a plan whose spec date is later than the adoption day,
  the spec date read as criterion 8 says.
- **`What:` value** — the text after the `What:` label on its line, joined
  with any continuation lines indented under it inside the card block, line
  breaks folded to single spaces.
- **Sentence** — text that ends with a full stop, question mark or
  exclamation mark followed by a space or the end of the `What:` value.

## Acceptance criteria

1. When a plan card is drafted, its first field is `What:`, followed by the
   existing five fields in their existing order.
   *Refuted by:* The prompt's card puts `What:` elsewhere or moves an existing
   field.
2. When a plan card is drafted, the `What:` field explains in at most three
   short plain-language sentences the present problem with one concrete
   example, what changes, and the main risk.
   *Refuted by:* The instruction permits a card that omits the example, the
   change or the risk, or allows more than three sentences.
3. When the draft check reads a subject plan, it refuses a card that does not
   open with a non-blank `What:` value — missing, blank, or not the card
   block's first field.
   *Refuted by:* Such a card passes the draft check.
4. When a subject plan's `What:` value holds more than three sentences, the
   draft check refuses the card.
   *Refuted by:* A four-sentence `What:` passes the draft check.
5. When a subject plan's `What:` value repeats its `For you:` value apart
   from surrounding whitespace and letter case, the draft check refuses the
   card.
   *Refuted by:* Identical values, ignoring surrounding whitespace and letter
   case, pass the check.
6. When the draft check reads a plan whose spec date is on or before the
   adoption day, it applies the existing five-field check without requiring
   `What:`.
   *Refuted by:* An otherwise valid old card is refused for lacking `What:`.
7. If the spec date or the adoption day cannot be read, the draft check
   reports the fault as one more post-run problem of the attempt, retried and
   repaired as every draft problem is, instead of silently exempting the plan.
   *Refuted by:* A missing or malformed date lets a five-field card pass as
   old.
8. When the spec is committed at the attempt's base, the draft check reads
   the spec date from that committed spec; only when the base holds no spec
   does the drafted spec's own date decide.
   *Refuted by:* An attempt that rewrites the committed spec date to on or
   before the adoption day sees its five-field card pass as old.
9. When a card's `What:` line includes what `spec.md` names as a non-goal or
   no acceptance criterion covers, the existing widening rule requires the
   maintainer's approval before phase 4 starts, with the same wording as for
   `For you:` and `Done when:`.
   *Refuted by:* The prompt permits implementation without that approval.
10. When the run report reads a valid `Appetite:` from a card, it keeps that
    reading even when another card field, `What:` included, is defective.
    *Refuted by:* Adding or breaking `What:` makes the report lose a readable
    appetite.
11. When a plan card is shown, its existing contextual preface, unchanged-card
    presentation and veto remain in force.
    *Refuted by:* The prompt removes the preface, alters the card in
    presentation or makes ordinary implementation depend on an extra
    approval.

## Non-goals

- A full card redesign, tracked separately (bead `coding-harness-6xx`).
- Rewriting existing plans, changing the acceptance card, or changing the
  appetite parser and its stop semantics.
- Automated judgment of whether prose is meaningful, factually correct or
  semantically paraphrases another field; counting sentences is mechanical
  and in scope, judging content stays a review duty.

## Protected areas

Archived plans and the frozen historical prompt fixture
(`tests/fixtures/research_refs/plan-prompt-d862bc2.md`) remain unchanged as
records of what was in force at the time.

## Definition of Done

- `verify` green.
- Moved in the same pull request: `prompts/03-plan.md`, the draft check in
  `scripts/stage2.py`, the adoption record `decisions/adoption.yaml` and the
  tests of all three; no ADR or design is due for this bounded change.
- The protected areas remain untouched and the non-goals unbuilt, shown by
  the pull request's file list.
- Bead: the pull request closes `coding-harness-kg8n`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-kg8n`.
- Special runs: none.

## Open decisions

None open. The reversible details that make the recorded intent testable,
each with its reason; F-1 to F-6 name the spec-review rows in `findings.md`
whose triage decided them:

- [DETAIL] `What:` comes first and holds up to three sentences, as
  `decisions.md` records, so the explanation precedes the existing card
  fields.
- [DETAIL] `What:` may wrap onto continuation lines indented under it, and
  the check joins them into the `What:` value before judging, because three
  sentences rarely fit one line (F-1).
- [DETAIL] The draft check requires `What:` as the card block's first field,
  because the reader meets it first (F-2).
- [DETAIL] An unreadable spec date or adoption day is one more post-run
  problem of the draft attempt, retried as today, because it takes the same
  path as every draft check (F-3).
- [DETAIL] The draft check counts sentences — a sentence ends with a full
  stop, question or exclamation mark followed by a space or the end — and
  refuses more than three, because the criterion must be checkable on the
  card (F-4).
- [DETAIL] The widening rule covers `What:` with the existing "includes"
  wording and no new verb, because one rule serves all three lines (F-5).
- [DETAIL] The spec date is read from the committed spec at the attempt's
  base when one is committed there, because the judged attempt must not set
  its own rule (F-6); a fresh change, whose base holds no spec, is dated by
  the spec its attempt writes, there being no earlier record to defend.
- [DETAIL] The duplicate check compares values after trimming and
  case-folding; semantic repetition and the quality of the explanation stay a
  review duty because a string comparison cannot judge meaning.
- [DETAIL] The adoption day is recorded under the key `plan-card-what-line`
  in `decisions/adoption.yaml`, read through the existing
  `scripts/adoption.py`.
