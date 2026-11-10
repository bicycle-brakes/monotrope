---
title: "ADR 0027 — Focused first reviews calibrate one free second round in shadow"
category: adr
status: accepted
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, review-loop, calibration]
---

# ADR 0027 — Focused first reviews calibrate one free second round in shadow

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, open is proposed and closed is rejected. Amends ADR 0021's
  stage order and clean-round end condition and ADR 0017's review-loop bound;
  supersedes no ADR. Amends no D- or O-number.
* Review: direction stated by the maintainer on 2026-11-07 through 2026-11-10
  (`plans/changes/review-fewer-rounds/decisions.md`, Q-1 through Q-12).
  The first question list, free second-round seating and small-change live
  trigger still await answers; no answer is inferred here. Decider:
  maintainer; prepared by Codex. Acceptance is the merge commit, recorded
  nowhere else; the header's review remains pending.
* Date: 2026-11-10; takes effect on merge.

## Context

The current loop sends unfocused reviewers through a free swarm, a Flash
swarm and a paid ladder until clean. Repository observations in this
change's research (2026-11-08: 63 changes, 1,205 rows) show typically 4–8
rounds; successive repairs introduce more defects. Formalities occupied
26% of 296 rows in 14 records measured 2026-11-07 (Q-1).

The public evidence synthesised on 2026-11-09 is mixed on focused reading
and warns that capture-recapture with three correlated reviewers can
underestimate remaining defects. No validated stopping threshold was found.
Q-11 starts with accepted singleton share as the shadow signal and compares
it once with the logged estimators after shadow. Q-12 calls for assessment at
ten completed changes, ending shadow when the evidence is clear and asking
the maintainer otherwise. The winning trigger and threshold are not decided
by this draft.

## Decision Drivers

- Find different defect classes in parallel and preserve singleton reports.
- Replace repeated repair/review cycles with a bounded, observable experiment.
- Keep model choice, rounds and limits centrally editable and validated.
- Let the maintainer approve check questions and the later live threshold.
- Retain admission, leak checks, isolation and independent final review.

## Considered Options

- **Continue until clean through the ladder:** preserves current behavior
  but continues successive cycles without measuring missing coverage.
- **Gate immediately on a capture-recapture estimate:** reduces calls but
  treats an uncalibrated, biased estimate as a stopping guarantee.
- **Focused first reviews with a free shadow second round:** increases parallel calls while
  collecting the observations needed before selective re-review is enabled.

## Decision

Chosen option: "Focused first reviews with a free shadow second round", because it follows
the maintainer's answered experiment and avoids inventing its threshold.

1. Five lenses cover spec/scope, hostile input/failure, state/retry/abort,
   tests as evidence and maintainability. Each uses concrete approved check
   questions, not role-play. Formalities become deterministic checks.
2. Each lens has three distinct models: best measured precision, a cheap
   different-lineage model, and Codex `gpt-6.1-terra` at effort `medium`.
   A bounded or text-only change instead has one reviewer per lens. Sole
   self-family review is excluded; parallel lenses permit at most one
   implementer-family member. Missing required seats may wait, never silently
   fabricate overlap.
3. Merge by union and triage before counting. Preserve raw reports and an
   explicit same-defect grouping; only accepted distinct defects are captures.
   Log singleton share, jackknife and Chao; initially the estimators are
   diagnostic only. A small change has no three-reviewer estimator.
4. In shadow, every change gets one free second round over the whole diff,
   including when round 1 found nothing. Its seating remains open. In live
   mode at least one per-lens trigger schedules that one round, never a lens
   subset. Assess at ten completed changes; compare share and the recorded
   estimators once against round-2 misses. The recorded calibration decision
   sets the better trigger and threshold, ending shadow if evidence is clear;
   otherwise ask the maintainer. No agent invents a production rule or the
   small-change trigger.
5. The initial central policy has two loop rounds. Round-2 MAJOR/BLOCKERs
   in this change enter one last repair regardless of location; only defects
   in code outside the change may become follow-up work. Tests/security/false
   statements are repaired; clear style fixes accompany a necessary repair
   but never cause one. Matters of taste become named PR limits. The
   orchestrator collects outstanding clear style rows weekly in one clean-up
   bead and its own repair PR.
6. Phase 6 permits the first review and one re-check. At the limit, stop and
   report with a proposal for a named limit, a mechanism repair or stop.
   Repeated findings of one mechanism require a mechanism repair. Only at
   night, when all open findings share one mechanism and it was repaired,
   one second re-check is permitted; no further re-check follows.
7. One central validated declaration owns lenses, seating, round order/count,
   trigger/mode/threshold and final-review limit. It depends on the central
   configuration work (`coding-harness-twvx`); implementation waits for its
   merged skeleton, with no interim settings source. Existing snapshots retain their semantics; fresh runs pin the new
   policy. New/changed files block on new lint/formality checks, stock reports
   only; existing blocking gates retain their contracts. The spec inventories
   every formality and its gate; uncovered ones get follow-up beads.
8. The maintainer approves the first scenario-question list. Only a phase-6
   finding not covered by that list warrants an addition; it applies at once
   and is shown with its evidence in the pull request.

## Consequences

- Fifteen calls in full-change round 1, or five for small changes, replace
  the current first swarm. Second-round call count remains undecided. Quota and
  wall time must be measured; this ADR claims no measured cost saving.
- Missing reviewers cannot silently turn the three-seat experiment into a
  two-seat one. Incomplete/cut input pauses completion with its evidence kept.
- Calibration owes accepted-defect identities, overlap, unique yield, call
  tokens/time and verification/lock-wait evidence; unavailable values say so.
- Check-question approval and the configuration dependency block rollout.
  Free-round seating and small-change trigger answers also block rollout.
  The live winner and threshold belong to the later calibration decision.
- Current doctrine and prompts change together; historical ADRs remain intact.

## Validation

- The change's criterion ledger names fault-sensitive tests for configuration,
  seating, triage, shadow selection, persistence, gates and review limits.
- `make verify` and the decision PR's review hold implementation and current
  documentation to `plans/changes/review-fewer-rounds/spec.md`.
- Subsequent calibration reports compare candidate stopping signals with
  actual round-2 accepted MAJOR/BLOCKER yield at ten completed changes,
  separating small/full changes and reporting unclear evidence honestly.
