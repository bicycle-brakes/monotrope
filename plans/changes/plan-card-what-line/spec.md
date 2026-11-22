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
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
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
  the maintainer had to ask what the work did (research and bead statement,
  2026-11-22).
- The draft check and the prompt-form test enforce the existing card's field
  order, so adding a field to the instruction alone would not protect it
  (research, 2026-11-22).

## Acceptance criteria

1. When a plan card is drafted, its first field is `What:`, followed by the
   existing five fields in their existing order.
   *Refuted by:* The prompt's card puts `What:` elsewhere or moves an existing field.
2. When a plan card is drafted, the `What:` field explains in at most three
   short plain-language sentences the present problem with one concrete
   example, what changes, and the main risk.
   *Refuted by:* The instruction permits a card that omits the example, the
   change or the risk, or allows more than three sentences.
3. When the draft check reads a plan whose spec date is later than this
   change's merge date, it refuses a missing or blank `What:` field.
   *Refuted by:* Such a plan passes the draft check with `What:` absent or empty.
4. When a subject plan's `What:` repeats its `For you:` value apart from
   surrounding whitespace and letter case, the draft check refuses the card.
   *Refuted by:* Identical values, ignoring surrounding whitespace and letter
   case, pass the check.
5. When the draft check reads a plan whose spec date is on or before this
   change's merge date, it applies the existing five-field check without
   requiring `What:`.
   *Refuted by:* An otherwise valid old card is refused for lacking `What:`.
6. If the spec date or the recorded merge date cannot be read, the draft
   check refuses the attempt instead of silently exempting it.
   *Refuted by:* A missing or malformed date lets a five-field card pass as old.
7. When a card's `What:` promises a non-goal or work uncovered by the spec's
   acceptance criteria, the existing widening rule requires the maintainer's
   approval before implementation.
   *Refuted by:* The prompt permits implementation without that approval.
8. When the run report reads a valid `Appetite:` from a card, it keeps that
   reading even if another card field is defective.
   *Refuted by:* Adding or breaking `What:` makes the report lose a readable appetite.
9. When a plan card is shown, its existing contextual preface, unchanged-card
   presentation and veto remain in force.
   *Refuted by:* The prompt removes the preface, alters the card in presentation
   or makes ordinary implementation depend on an extra approval.

## Non-goals

- A full card redesign, tracked separately (bead `coding-harness-6xx`).
- Rewriting existing plans, changing the acceptance card, or changing the
  appetite parser and its stop semantics.
- Automated judgment of whether prose is meaningful, factually correct or
  semantically paraphrases another field; review checks those qualities.

## Protected areas

Archived plans and the frozen historical prompt fixture remain unchanged as
records of what was in force at the time.

## Definition of Done

- `make verify` is green after the orchestrator's held-path edits.
- The prompt, draft check, adoption record and their tests move together in
  the pull request; no ADR or design is due for this bounded change.
- The protected areas remain untouched and the non-goals unbuilt, shown by
  the pull request's file list.
- The pull request closes `coding-harness-kg8n`; its last commit carries
  `Closes-Bead: coding-harness-kg8n`.
- Special runs: none.

## Open decisions

None open. The following reversible details make the recorded intent testable:

- [DETAIL] `What:` comes first and holds up to three sentences, as recorded in
  `decisions.md`, so the explanation precedes the existing card fields.
- [DETAIL] The mechanical duplicate check compares values after trimming and
  case-folding; semantic repetition and the quality of the explanation stay a
  review duty because a string comparison cannot judge meaning.
- [DETAIL] The widening rule also covers `What:`, because an extra promise in
  that field has the same scope consequence as one in `For you:`.
- [DETAIL] A missing or unreadable date refuses measurement, so an unknown
  cutoff cannot silently exempt a new plan.
