---
title: "Spec — definitive-refusal"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-2ym2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, review-loop]
class: bounded
appetite: 1.5
adr_files: []
neighbours: []
---

# Spec — definitive-refusal

A paid review-loop rung refused with HTTP 403 or 410 retires automatically
and the loop continues with its next stage, with the refusal preserved as
evidence (bead coding-harness-2ym2). Research: `research.md`, especially
"Scope correction and repository gap check". Decision: `decisions.md#Q-1`.

## Problem

At commit `4a80673c` (2026-11-06), a failed paid single-model round raises
`CallFailed` without consuming its stage; only failed Flash members have
automatic replacement. A loop prepared before a model's deprecation therefore
keeps selecting that failed rung until the maintainer retires it manually
(`research.md`, scope correction; `scripts/stage2.py::_review_round`).

The interview records a night-run interruption on 2026-11-05 and authorizes
automatic retirement for HTTP 403 (access disabled) and 410 (deprecated),
while excluding transient errors (`decisions.md#Q-1`). The initial exploration
of permission brakes is superseded for scope by that answer.

## Terms

- **Paid rung:** a single-model ladder stage in the current run's saved
  snapshot; not the free or Flash swarm.
- **Definitive refusal:** explicit HTTP 403 or 410 evidence from a failed
  provider call, not a local preflight refusal or a reviewer's prose.
- **Retirement:** consuming a stage without claiming it completed a review.

## Acceptance criteria

1. When a paid rung's provider call fails with a definitive refusal, its
   retirement is durably recorded before any later stage starts.
   *Refuted by:* either status leaves the rung pending, or a later stage
   starts despite failure to persist its retirement.
   *Basis:* `decisions.md#Q-1`.
2. When a rung has been retired and time and admission permit another call,
   the same `review-loop` invocation attempts the next unconsumed stage in
   the saved order.
   *Refuted by:* another command is required, the retired rung is retried,
   the order changes, or a next call starts after the round deadline.
   *Basis:* `decisions.md#Q-1`.
3. When a rung is automatically retired, the persistent audit identifies the
   stage, model, HTTP status, provider diagnostic and automatic retirement
   reason as protected evidence.
   *Refuted by:* missing attribution or provider evidence, a credential in
   stderr or persisted text, or quoted provider text creating control rows,
   round headings or snapshot fields.
   *Basis:* `decisions.md#Q-1`.
4. If a paid rung fails without explicit HTTP 403/410 evidence from its
   failed provider call, it remains unretired by this change.
   *Refuted by:* retirement after HTTP 429, 5xx, timeout, launch failure,
   malformed answer, local admission refusal, or incidental 403/410 text
   in successful reviewer output or an unrelated error number.
   *Basis:* `decisions.md#Q-1`.
5. When retirement replaces a failed rung attempt, that attempt does not
   count as a completed or clean round.
   *Refuted by:* an invented finding, a new completed-round heading, a clean
   verdict for the failed call, or a gap in subsequent round numbering.
   *Basis:* `decisions.md#Q-1`.
6. When a loop resumes from its saved record or released snapshot, it retains
   the automatic retirement together with its previous review history.
   *Refuted by:* a retired model called again, erased or renumbered earlier
   rows, or lost retirement evidence after release and continuation.
   *Basis:* `decisions.md#Q-1`.
7. If definitive refusals retire every remaining stage without a usable
   review answer, the loop stops with a diagnostic that the saved ladder is
   exhausted.
   *Refuted by:* a clean-success exit, an unrecorded retirement, a repeated
   call to a retired stage, or substitution outside the saved run.
   *Basis:* `decisions.md#Q-1`.

## Non-goals

- General HTTP retry policy, retirement for other statuses, or automatic
  recovery from local admission, leak, credentials or configuration failures.
- Changing free-swarm skipping, Flash replacement, model selection,
  availability probing, manual retirement or explicit restart semantics.
- Permanent removal of models from configuration or other loop snapshots.
- Permission hooks, merge enforcement, session-stop hooks or new gates.
- Design phase 2b and an ADR: this is the interviewed `bounded` change and
  extends an existing runner transition without changing architecture.

## Protected areas

- `model-endpoints.yaml`, `decisions/`, `docs/adr/`, `provenance.yaml` and
  harness configuration: no changed admission policy or governance decision.
- `prompts/`, `templates/`, `AGENTS.md` and `README.md`: the change concerns
  the runner's failed-call handling, not its entry instructions.
- Existing rounds, findings and pinned stage membership: only the refused
  rung's consumption and its evidence may be added by retirement.

## Definition of Done

- `PYTHON=.venv/bin/python3 make verify` is green at the implementation head.
- Offline tests exercise the real failed-Pi-call path for both statuses,
  transient and misleading inputs, persistence failure, exhaustion and resume.
- `docs/WORKFLOW.md` documents automatic retirement and its narrow exception
  to all-failed attempts consuming no stage; this change's plan and findings
  carry verification evidence. No ADR or model declaration changes.
- The pull request's file list respects the protected areas and non-goals.
- The pull request closes the automatic paid-rung retirement task, and its
  last commit carries `Closes-Bead: coding-harness-2ym2`.
- Special live runs: none; the contract is verified with offline fixtures.

## Open decisions

None open.

- [DETAIL] Require explicit HTTP failure evidence on a nonzero Pi exit,
  classified before diagnostic truncation; never infer status from successful
  review text. This confines the interview's exception to provider failures.
- [DETAIL] Reuse the existing saved stage consumption and quoted retirement
  evidence, identifying the runner as actor rather than the maintainer.
  This preserves resume and release behavior without a new state format.
- [DETAIL] Share the round deadline across consecutive automatic retirements;
  a spent deadline stops before another call. Retirement must not buy more time.
- [DETAIL] Phase 4 has an appetite of 1.5 hours including repairs; stop there
  because this is one bounded failure transition with existing test fixtures.
