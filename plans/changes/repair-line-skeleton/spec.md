---
title: "Spec — repair-line-skeleton"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-k93f
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, repair]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — repair-line-skeleton

The runner supplies each taken finding's fixed-line skeleton and accepts
independently valid completions despite another row's unreadable completion
(bead coding-harness-k93f — prefilled repair answer lines).
Research: `research.md`. Decisions: `decisions.md`.

## Problem

At `249840c7` (2026-10-31), the repair prompt lists findings but leaves the
model to compose every identifier, fixed marker and evidence kind. Research
records missing-line rejections across all three repair routes for run-report
on 2026-10-29 despite work on the requested repairs (`research.md`, “What
exists today”). Format mistakes spend attempts intended for repair work.

The answer checker discards every row's result when any row fails. The
writers also assume a complete result dictionary. Giving the model a
skeleton alone would therefore leave the answered requirement of independent
acceptance unmet. A partial checkpoint introduces another hazard: HEAD can
already contain an unresolved row's repair, invalidating its next red-first
comparison (`research.md`, “Draft gap checks — 2026-10-31”).

## Terms

- **Skeleton:** an exact taken identifier and fixed prefix, with one field
  to fill: `tests/<path>::<function>` for a code row or `<reason>` after
  `not a test — ` for a row taken as not a test.
- **Row failure:** a known row's missing, malformed, conflicting, unfilled
  or wrong-kind completion, or evidence that does not prove its repair.
- **Shared failure:** a failure of whole-attempt guards before acceptance,
  including an unknown claimed identifier, audit integrity, verification or
  checkpoint safety; proof-environment integrity failures belong here too.
- **Partial acceptance:** a verified batch checkpoints at least one proven
  row while leaving another taken; it does not assert that all rows are fixed.

## Acceptance criteria

1. When a repair prompt is built on either command-capable or file-only
   routes, it contains exactly one skeleton for each taken row selected from
   the active record, released blocks and phase-6 tables.
   *Refuted by:* a selected identifier is absent or repeated in the skeleton
   block, or a rejected or already fixed row receives a skeleton.

2. When a row's taken Status selects its evidence kind, its skeleton leaves
   only that kind's test reference or reason for the model to fill.
   *Refuted by:* a code row offers a not-a-test field, a not-a-test row offers
   a test field, or the runner presents the earlier taking reason as a
   completed repair reason.

3. When a model returns a completed copied line, the runner reads it in the
   existing fixed-status grammar.
   *Refuted by:* an existing valid full line stops working, identical claims
   conflict, explanatory prose becomes a fix, or distinct claims are silently
   resolved by choosing one.

4. When a batch has both a row failure and an independently valid repair,
   the failed row remains taken while the valid row is accepted.
   *Refuted by:* omission, malformed syntax, an unchanged placeholder,
   conflicting claims, a wrong kind or failed proof for one row prevents
   another proven row from receiving its canonical fixed Status and mark.

5. When a code completion is accepted, its named test proves the repair
   against that row's pre-repair baseline and repaired code under the existing
   red-first and fixed-code checks.
   *Refuted by:* a missing test, a baseline pass, an unrelated collection or
   fixture error, or a repaired-code failure earns a fixed Status or yes mark.

6. If a shared failure occurs, no row is accepted through the partial-result
   path.
   *Refuted by:* an unknown claimed identifier, red overall verification,
   altered audit, evidence-protection failure or rolled-back checkpoint
   nevertheless leaves a newly fixed row or proof mark.

7. When a partial acceptance checkpoints, the outcome identifies accepted
   and pending rows with the pending diagnostics and retains each pending
   row's original baseline for a subsequent repair call.
   *Refuted by:* the command reports complete success, pending rows disappear,
   a subsequent prompt demands an already fixed row again, or its pending
   proof compares against code committed by the partial acceptance.

8. When no row can be accepted, the existing repair retry ladder remains
   available with row diagnostics and protected answer evidence.
   *Refuted by:* a wholly malformed answer becomes a successful empty repair,
   loses its diagnostic/evidence locator, changes the route order or adds a call.

9. When repair instructions describe the answer contract, they explain
   field-only completion and the distinction between partial acceptance and
   shared failure.
   *Refuted by:* the shared runner prompt, implement prompt or workflow still
   says a bad known-row completion necessarily discards every valid repair.

## Non-goals

- No shortened answer language, positional matching, automatic kind changes,
  inferred test names, inferred reasons or repair of unreadable model output.
- No new model, attempt count, extra format-reminder call, review round,
  evidence standard or gate; no change to other verbs' answer contracts.
- No selective attribution or splitting of code edits by finding: the existing
  checkpoint contains the verified worktree; only proven rows are marked fixed.
- No design phase or ADR: this bounded change stays within the repair verb
  and its existing runner-owned findings and checkpoint boundaries.

## Protected areas

Endpoint declarations, gate configuration, ADRs, tracker data, permissions,
other change artifacts and foreign-call transport are outside this change.
The held `prompts/04-implement.md` edit belongs to the orchestrator, never
the guarded implementation attempt.

## Definition of Done

- `make verify` is green; row-isolation regressions demonstrate the refuting faults.
- Documents updated with code: `docs/WORKFLOW.md`, `prompts/04-implement.md`,
  this spec and `plan.md`; the runner maintains `findings.md` and `plans/INDEX.md`.
- The pull request's file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes coding-harness-k93f (prefilled repair answer lines)
  and its last commit carries `Closes-Bead: coding-harness-k93f`.
- Special runs: none; local model/process stand-ins suffice.

## Open decisions

None open. The reasoned interview skip and three recorded details in
`decisions.md` settle the scope; no maintainer answer is added here.

- [DETAIL] Use the existing complete-line grammar as a copy-and-fill form;
  the runner supplies identifiers and prefixes, avoiding a second wire format.
- [DETAIL] Keep `<reason>` unfilled even when the taking Status has a reason:
  taking a finding is not evidence that it has been repaired. Literal unfilled
  fields fail their row instead of serving as evidence.
- [DETAIL] A partial result checkpoints once and stops with a nonzero pending
  summary; a later repair selects the remaining rows. Zero accepted rows use
  the existing ladder. This keeps route counts and the checkpoint boundary
  intact without claiming the entire batch succeeded.
- [DETAIL] Pending rows retain their original baseline in runner bookkeeping
  in `findings.md`; later calls cannot substitute a HEAD that includes the
  unreported fix. Shared failures remain batch-wide because they cannot be
  safely attributed to one completion.
- [DETAIL] A loop-record write failure after a completed checkpoint keeps
  the existing recovery policy: report it for reconciliation without rewriting
  committed history. It is not permission to accept an unproved row.
- [DETAIL] Three hours of phase 4, repairs included, is the stop budget for
  prompt generation, independent proof handling and partial-checkpoint recovery;
  no input artifact sets an earlier appetite.
