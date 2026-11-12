---
title: "Spec — no-work-done"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-te7q
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, acceptance]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — no-work-done

An implement or repair attempt cannot be accepted solely on the runner's
own bookkeeping (bead coding-harness-te7q). Inputs: `research.md` and the
maintainer's answered empty-diff decision (`decisions.md#Q-1`).

## Problem

On 2026-11-06, three implement attempts were reported as verified and
committed although they changed only runner bookkeeping; the heartbeat-night
handover records the failures and the parked work (`research.md`, "What
exists today"). At drafting input commit `ed78f742`, acceptance requires
green verification but no model-produced change: the runner's audit and
measured time supply enough bytes for a checkpoint. The existing per-call
change measurement feeds diagnostics, not the verdict (`research.md`,
"The measurement a work check would need already exists").

## Terms

- **Work:** a non-empty Git-visible change produced by this model call,
  after discounting runner-owned writes and model edits the runner discards
  from its own findings file and time-section body. Changes outside that
  bookkeeping, including document changes, count without a source whitelist.
- **Attempt baseline:** the state immediately before this model call,
  including earlier attempts' retained changes and runner records; an
  earlier attempt's work is not this attempt's work.

## Acceptance criteria

1. When an implement or repair attempt produces no work relative to its
   attempt baseline, the runner rejects it as `no work done`.
   *Refuted by:* a no-edit call, same-byte rewrite, findings-only edit or
   time-body-only edit is accepted after green verification.
   *Basis:* decisions.md#Q-1.
2. When an otherwise valid attempt produces work, the no-work check passes
   regardless of whether the changed file is code, documentation, the plan
   outside its time body, or absent from the plan's file list.
   *Refuted by:* the check rejects an addition, modification, deletion,
   binary change or file-mode change solely for its kind or unplanned path.
   *Basis:* decisions.md#Q-1.
3. When a no-work rejection has a remaining attempt in the existing route,
   the runner supplies its `no work done` diagnostic to that next attempt.
   *Refuted by:* it stops instead of taking the existing retry, adds a new
   attempt, or omits the reason from the retry prompt or findings record.
   *Basis:* decisions.md#Q-1; the existing post-run failure contract.
4. When all allowed attempts produce no work, the invocation ends in failure
   without a checkpoint commit or a `verified and committed` success report.
   *Refuted by:* an all-empty default or explicit Stage-2-off run exits
   successfully, advances HEAD, or reports acceptance.
   *Basis:* decisions.md#Q-1.
5. When a completed attempt is rejected for no work, its existing audit and
   single runner-measured rejected time entry remain available.
   *Refuted by:* the rejection loses or duplicates its audit/time record,
   logs it as accepted, or marks repair findings as fixed without a fix.
   *Basis:* decisions.md#Q-1; the existing audit and timing contract.
6. If the runner cannot measure whether the attempt produced work, that
   measurement failure prevents acceptance with its reason reported.
   *Refuted by:* an unreadable comparison is treated as evidence of work or
   becomes a successful checkpoint.
7. When an attempt produces work but another existing post-run check fails,
   that failure still prevents acceptance.
   *Refuted by:* a non-empty diff bypasses verification, repair-answer
   proofs, integrity checks or checkpoint restrictions.

## Non-goals

- Requiring every planned file to change, proving completeness or usefulness
  from a non-empty diff, or restricting work to code files.
- Changing providers, route order, attempt limits, review-loop selection,
  verification commands, repair proofs, time-record format or checkpoint mechanics.
- Extending the check to explore, draft, spec-review or phase-6 review.
- Phase 2b and an ADR: this bounded change adds an acceptance condition to
  the existing implement/repair loop without changing architecture.

## Protected areas

Tracker, ADRs, decisions, prompts, templates, model configuration, dependency
pins, agent settings and other changes' artifacts stay untouched; none is
needed for this runner-side condition. The existing living implementation
verification spec may be clarified alongside the workflow text.

## Definition of Done

- `make verify` is green, including the interview and criterion-ledger gates.
- Regression tests cover empty and real work, both verbs, retries, fallback,
  measurement failure and runner-owned records; a guard test plants a real
  bypass under `STAGE2_PLANT_FAULT=1` and fails on the resulting acceptance.
- Updated documents: `docs/WORKFLOW.md`,
  `plans/specs/implementation-verification/spec.md`, this change's ledger
  and runner-owned findings; the runner regenerates `plans/INDEX.md`.
- The pull request's file list respects protected areas and non-goals.
- The pull request closes the empty-attempt acceptance bug (bead
  coding-harness-te7q); its final commit carries
  `Closes-Bead: coding-harness-te7q`.
- Special runs: none; local model and verifier stand-ins suffice.

## Open decisions

None open; Q-1 is carried forward unchanged.

- [DETAIL] Use the individual call's baseline, because the existing
  measurement already distinguishes each model's work from earlier attempts.
- [DETAIL] Discount the discarded time body, but retain plan changes outside
  it, because the shared time writer restores that body from trusted input.
- [DETAIL] Set a three-hour phase-4 appetite, repairs included, as a stop for
  the shared check and its regression-fixture updates; none was stated in Q-1.

These reversible details are agent choices recorded with their reasons.
