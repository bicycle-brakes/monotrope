---
title: "Spec — no-work-ledger-marker"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-11
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-twbl
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, no-work-check]
class: bounded
appetite: 2
adr_files: []
neighbours: [plans/changes/no-work-done/spec.md]
---

# Spec — no-work-ledger-marker

The runner's own removal of a pending-test marker cannot qualify an implement
or repair attempt as model work (bead coding-harness-twbl). Inputs:
`research.md` and `decisions.md`; the bounded interview has a reasoned skip,
not an invented maintainer answer.

## Problem

At input commit `c54bbdd5` (2026-11-10), the work check admits candidate paths
changed during the model call but measures their final content after
verification. A rejected attempt can leave a test while retry restoration
brings back its plan's `not yet written` marker. A retry changing only the
discarded time body makes the plan a candidate; verification then clears that
marker, and the runner counts its own ledger edit as model work. Research
records the reproduction from the earlier change's phase-6 finding F-1
("What exists today", "The mechanism, restated against the current code").

The existing contract already excludes earlier attempts' retained work and
accepts genuine plan edits; discounting the entire plan or every ledger
change would break it (the neighbouring no-work-done spec, criteria 1–2;
`decisions.md`, "Decided by the agent").

## Terms

- **Work:** surviving Git-visible change produced by this model call,
  measured against its own pre-call state after the existing bookkeeping,
  stamp, time-body, index and formatter discounts.
- **Runner clearing:** removal of `not yet written` from a criterion-ledger
  entry by the runner's actual verification step because its named test
  exists; a model's own removal is not runner clearing.

## Acceptance criteria

1. When an implement or repair attempt leaves only runner clearing beside
   the existing discounted changes, it is rejected as `no work done` against
   that attempt's pre-call state.
   *Refuted by:* a failed attempt leaves a test, retry restoration returns
   its marker, and a time-body-only retry is accepted after verification
   clears the marker, including when several entries are cleared.
2. When an otherwise valid attempt leaves genuine model work beside runner
   clearing, the no-work check still passes.
   *Refuted by:* surviving plan prose, a changed ledger test reference or
   explanation, a model-removed marker that the runner did not clear, or
   another file's substantive change is hidden by the new discount.
3. When verification finds a pending ledger entry's named test, the existing
   clearing behavior remains effective before stamping and verification.
   *Refuted by:* full or targeted verification stops clearing eligible
   entries, clears missing-test or fenced entries, or runs stamping or the
   verifier before clearing.
4. When a marker-only attempt is rejected, it follows the existing no-work
   rejection flow.
   *Refuted by:* its diagnostic does not reach the next allowed attempt,
   its rejected audit or single measured time entry is lost or duplicated,
   a repair row is marked fixed, or exhaustion checkpoints or reports success.
5. If the runner cannot measure the clearing discount reliably, that failure
   prevents acceptance with a reported reason.
   *Refuted by:* unreadable clearing evidence or a failed comparison is
   treated as work and allows a successful checkpoint.

## Non-goals

- Changing route order, attempt limits, verification selection, retry
  restoration, time records, ledger syntax or what constitutes an existing
  test.
- Broadly ignoring ledger text, the whole plan, or model-written marker
  removals; extending the work check to other verbs.
- Redesigning the existing findings, index, stamp or time-body discounts.
- Phase 2b and an ADR: this bounded fix corrects attribution within the
  existing acceptance check without changing architecture.

## Protected areas

Other changes' artifacts, including no-work-done, remain accepted history.
The ledger gate (`scripts/check_criterion_ledger.py`) and the living
implementation-verification spec retain their existing contracts. Tracker,
ADRs, decisions, prompts, templates, model configuration, dependency pins and
agent settings need no implementation edits.

## Definition of Done

- `make verify` is green, with the retry reproduction first demonstrated red
  on the input runner and then green with the fix, using local stand-ins.
- Updated documents: `docs/WORKFLOW.md` names runner clearing among the work
  discounts; this change's plan tracks its tests. The runner maintains this
  change's findings and regenerates `plans/INDEX.md`.
- The pull request's file list respects the protected areas and non-goals.
- The pull request closes the ledger-attribution bug (bead
  coding-harness-twbl); its final commit carries
  `Closes-Bead: coding-harness-twbl`.
- Special runs: none; no live provider call is needed for regression tests.

## Open decisions

None open. The reasoned interview skip remains as recorded in `decisions.md`.

- [DETAIL] Attribute only the actual clearing performed in this attempt,
  rather than masking every removable marker; this preserves model edits
  with the same textual result and follows the recorded agent decisions.
- [DETAIL] Set a two-hour phase-4 appetite, repairs included, as a stop for
  the shared runner fix and its regressions; the input records no appetite.

These reversible choices are made by the agent and recorded with reasons.
