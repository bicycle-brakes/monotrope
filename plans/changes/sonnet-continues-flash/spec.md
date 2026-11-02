---
title: "Spec — sonnet-continues-flash"
status: draft
implementation_status: none
date: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-6ie
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: gpt-6.1-sol, version: "2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, attempts]
class: bounded
appetite: 4
adr_files: [docs/adr/0024-implementation-attempts-continue-from-protected-partial-work.md]
neighbours: []
---

# Spec — sonnet-continues-flash

Implementation retries continue from protected partial work, including after
an aborted Flash call, instead of discarding it (bead `coding-harness-6ie` —
Sonnet continues Flash). Research: `research.md`. Decisions: `decisions.md`.
This is proposed behavior; no implementation is claimed.

## Problem

Evidence was checked at `baffe4a3` on 2026-11-02 against the exploration of
2026-10-31 (`research.md`, “What exists today” and “Where it lives”):

- `run_attempts` saves a failed call but restores the baseline and raises,
  preventing the later Flash repair or Sonnet route from finishing its work.
- A failed post-run check retains code in the same worktree, but the next
  prompt supplies diagnostics without the cumulative implementation diff.
  The interview rejects this unprotected continuation (Q-1).
- The implementation doctrine in `docs/WORKFLOW.md` says a failed process
  stops; changing it requires a visible amendment, not an undocumented retry.

The five answered records settle counting, abort-state continuation and
visibility. They do not extend this package to Codex repair calls, whose
separate stop rule is explicit in ADR 0017.

## Terms

**Abort:** an implementation model call reported as `CallFailed`, including
an error, timeout or empty answer; not an operator interrupt or safety refusal.
**Baseline:** the invocation's initial committed HEAD.
**Protected continuation:** a fresh attempt environment containing a copy of
the preceding attempt's permitted work, with runner inputs restored; not reuse
of that attempt's writable directory or model session.

## Acceptance criteria

1. When an implementation call aborts and another scheduled route remains,
   the runner advances exactly one position in Flash → Flash repair → Sonnet.
   *Refuted by:* stopping at the first ordinary call error, repeating a spent
   Flash position, skipping Flash repair or adding a fourth attempt.
   *Basis:* decisions.md#Q-2, decisions.md#Q-3.
2. When implementation advances after an abort or failed post-run check,
   the next attempt starts in a fresh environment copied from the preceding
   attempt's permitted state, including incomplete files.
   *Refuted by:* losing an earlier edit, creation or deletion, sharing writable
   file bytes with the previous attempt, or reusing its working directory.
   *Basis:* decisions.md#Q-1, decisions.md#Q-4.
3. When a continuation prompt is built, it identifies the cumulative changed
   paths and their diff against the invocation baseline and instructs the
   model to continue rather than redo the work.
   *Refuted by:* only diagnostics or only the last attempt's diff appearing,
   or a changed path silently omitted from the handoff.
   *Basis:* decisions.md#Q-1, decisions.md#Q-4.
4. When the preceding call aborted, the continuation prompt warns that files
   may be incomplete.
   *Refuted by:* the next route receiving an ordinary completed-work handoff
   after a timeout or error left a half-written file.
   *Basis:* decisions.md#Q-4.
5. Before each implementation call, every runner prompt input has its trusted
   baseline content plus only the runner's own accumulated records.
   *Refuted by:* a model's edited spec, plan, findings, decisions, design or
   phase prompt reaching the next call or replacing earlier runner evidence.
   *Basis:* decisions.md#Q-1.
6. When an implementation call aborts, its state is retained as recoverable
   attempt evidence before any continuation or disposal of its environment.
   *Refuted by:* the partial state existing only in a deleted scratch tree,
   or a failed save allowing continuation as though preservation succeeded.
   *Basis:* decisions.md#Q-4.
7. When an aborted implementation call causes a route transition, the reason
   and source and destination attempts are visible in runner output and plan.md.
   *Refuted by:* only findings.md recording the transition, a call error
   labelled a post-check failure, or a model's plan edit erasing the record.
   *Basis:* decisions.md#Q-2, decisions.md#Q-5.
8. If every scheduled implementation attempt fails, the invocation exits
   unsuccessfully with its last permitted partial state recoverable and no
   implementation checkpoint on the branch.
   *Refuted by:* baseline rollback destroying the sole copy, a success exit,
   or a failed attempt being committed as accepted work.
   *Basis:* decisions.md#Q-2, decisions.md#Q-3, decisions.md#Q-4.
9. When a later implementation attempt passes the existing acceptance checks,
   its checkpoint contains the cumulative accepted work.
   *Refuted by:* a commit without full verification, loss of a preceding
   attempt's accepted edit, or multiple implementation checkpoints for one run.
   *Basis:* decisions.md#Q-1, decisions.md#Q-2.
10. If an existing credential, declaration, leak, tool-integrity, HEAD or
    recovery-safety guard refuses an implementation attempt, no later route starts.
    *Refuted by:* catching a refusal as an ordinary abort, sending a secret in
    a new diff, bypassing a held-path check or writing after a no-write refusal.
    *Basis:* decisions.md#Q-2 concerns call errors; research.md, existing guards.
11. When implement uses an explicit Stage-1 route, it retains the single
    Sonnet attempt and records the supplied reason.
    *Refuted by:* adding Flash calls or retrying the sole Sonnet call after failure.
    *Basis:* research.md, “The implement attempt ladder”.
12. When draft, repair, explore or a review runs, its existing call-failure
    routing is unchanged by this implementation-only policy.
    *Refuted by:* a failed Codex repair automatically reaching another route
    contrary to ADR 0017, or draft losing its existing fallback.
    *Basis:* research.md, “What is unclear”; decisions.md#Q-3 identifies Flash.
13. When the implementation policy is delivered, its workflow description
    and proposed ADR state the visible abort continuation and its boundaries.
    *Refuted by:* the implementation doctrine still claiming every failed
    model process stops, or an amendment claiming repair fallback was approved.
    *Basis:* decisions.md#Q-2, decisions.md#Q-5.

## Non-goals

- Changing repair's ADR 0017 stop rule, draft, explore, reviews, route counts,
  models, credentials or model tool permissions.
- Selecting or deploying containers or host-level confinement. The shared
  design's broader isolation work remains with bead `coding-harness-s9r` —
  isolate writing attempts; this package owes the fresh-copy handoff itself
  and does not claim that bead is closed. Existing attempt preservation from
  bead `coding-harness-znc` — retain failed work — is reused, not replaced.
- Automatic recovery after an operator interrupt, safety refusal, failed
  snapshot or failed promotion; diagnostics retain the recovery location.
- A design.md: phase 2b does not run for this bounded class. The ADR below
  records the expressly requested doctrine amendment, without reclassifying it.

## Protected areas

- Runner-held paths, endpoint declarations, shared tracker data, hooks and
  model permissions retain their existing protection; attempts cannot edit them.
- Existing ADRs remain historical; only the claimed new ADR is proposed.
- Credential scrubbing and refusal rules take precedence over copying partial
  work; “nothing reverted” never authorizes retaining or forwarding a secret.
- Other changes' criteria, interview answers and status are not rewritten.

## Definition of Done

- `make verify` green; deterministic continuation regressions shown red on
  baseline code and green after implementation, without live model calls.
- Moved with the code: `docs/WORKFLOW.md`, the claimed ADR 0024, and this
  change's spec, plan and runner findings; `plans/INDEX.md` regenerated.
- Protected areas untouched except the new ADR applied by the orchestrator;
  PR diff contains no non-goals.
- The decision PR names bead `coding-harness-6ie` — Sonnet continues Flash;
  closure follows delivery, not this draft, with its `Closes-Bead` trailer.
- Special live runs: none required; stand-ins verify the observable contract.

## Open decisions

None open. Q-1 through Q-5 are maintainer answers, not newly inferred answers.

[DETAIL] Scope is implement only: research names the Flash ladder and an
explicitly different repair decision; shared code receives an opt-in policy.
[DETAIL] Fresh local attempt copies implement the handoff, without claiming
OS isolation; container selection belongs to the neighbouring isolation work.
[DETAIL] Four hours of phase 4, repairs included, is the proposed stop because
this package crosses recovery boundaries; stop with evidence if it is exhausted.
[DETAIL] ADR 0024 is a new standalone addendum rather than an edit of historical
ADRs; the explicit drafting instruction supersedes the stale note in decisions.md
that agents cannot write the proposed ADR file. No ADR answer is recorded.
