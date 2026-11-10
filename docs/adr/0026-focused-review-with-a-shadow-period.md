---
title: "ADR 0026 — Focused review trios calibrate a bounded second round in shadow"
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

# ADR 0026 — Focused review trios calibrate a bounded second round in shadow

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, open is proposed and closed is rejected. Amends ADR 0021's
  stage order and clean-round end condition and ADR 0017's review-loop bound;
  supersedes no ADR. Amends no D- or O-number.
* Review: direction stated by the maintainer on 2026-11-07 through 2026-11-09
  (`plans/changes/review-fewer-rounds/decisions.md`, Q-1 through Q-12).
  The concrete question list still awaits approval under Q-10. Decider:
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
Q-11 chooses accepted singleton share rather than an estimator as the future
signal; Q-12 requires observing both rounds for 10–20 changes first.

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
- **Focused trios with two shadow rounds:** increases parallel calls while
  collecting the observations needed before selective re-review is enabled.

## Decision

Chosen option: "Focused trios with two shadow rounds", because it follows
the maintainer's answered experiment and avoids inventing its threshold.

1. Five lenses cover spec/scope, hostile input/failure, state/retry/abort,
   tests as evidence and maintainability. Each uses concrete approved check
   questions, not role-play. Formalities become deterministic checks.
2. Each lens has three distinct models: best measured precision, a cheap
   different-lineage model, and Codex `gpt-6.1-terra` at effort `medium`.
   Sole self-family review is excluded; diverse parallel review may include it.
3. Merge by union and triage before counting. Preserve raw reports and an
   explicit same-defect grouping; only accepted distinct defects are captures.
   Log singleton share, jackknife and Chao; estimators never gate a round.
4. In shadow, all five lenses run again, even with no accepted first-round
   finding. After 10–20 complete shadow changes the maintainer sets the
   live singleton-share threshold using observed second-round misses.
   No automatic promotion and no agent-selected production threshold.
5. The initial central policy has two loop rounds. Round-2 MAJOR/BLOCKERs
   in this change enter one last repair regardless of location; only defects
   in code outside the change may become follow-up work. Tests/security/false
   statements are repaired; clear style fixes accompany a necessary repair
   but never cause one. Matters of taste become named PR limits.
6. Phase 6 permits the first review and one re-check. At the limit, stop and
   report with a proposal for a named limit, a mechanism repair or stop.
   Repeated findings of one mechanism require a mechanism repair; they do
   not grant another review call.
7. One central validated declaration owns lenses, seating, round order/count,
   trigger/mode/threshold and final-review limit. It depends on the central
   configuration work (`coding-harness-twvx`); there is no parallel settings
   source. Existing snapshots retain their semantics; fresh runs pin the new
   policy. New/changed files block on lint/formalities, stock reports only.

## Consequences

- Fifteen calls per full round replace the current first swarm. Quota and
  wall time must be measured; this ADR claims no measured cost saving.
- Missing reviewers cannot silently turn the three-seat experiment into a
  two-seat one. Incomplete/cut input pauses completion with its evidence kept.
- Calibration owes accepted-defect identities, overlap, unique yield, call
  tokens/time and verification/lock-wait evidence; unavailable values say so.
- Check-question approval and the configuration dependency block rollout.
  Live threshold approval belongs to the later calibration decision.
- Current doctrine and prompts change together; historical ADRs remain intact.

## Validation

- The change's criterion ledger names fault-sensitive tests for configuration,
  seating, triage, shadow selection, persistence, gates and review limits.
- `make verify` and the decision PR's review hold implementation and current
  documentation to `plans/changes/review-fewer-rounds/spec.md`.
- Subsequent calibration reports compare candidate stopping signals with
  actual round-2 accepted MAJOR/BLOCKER yield on 10–20 completed changes.
