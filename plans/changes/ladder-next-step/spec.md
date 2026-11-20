---
title: "Spec — ladder-next-step"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-hwll
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, review-loop]
class: bounded
appetite: 4
adr_files: []
---

# Spec — ladder-next-step

A consumed review ladder names the next action without stopping a lane for a new decision (bead `coding-harness-hwll`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `8cfb9de8`, a run whose review stages are consumed refuses with the same message whether the last round's taken findings are repaired or still open; a session must inspect the record and apply the maintainer's rule by hand (`research.md`, "What exists today"). The workflow and reviewer prompts still describe this state as a stop for the maintainer, although the maintainer decided the next step on 2026-11-20 (`research.md`, "Doctrine texts carrying today's behavior"; `decisions.md` Q-1).

## Terms

**Consumed ladder:** the saved run has no unconsumed stage and its last completed round was not clean. A taken finding is repaired when its status is `fixed` with the evidence mark required by the existing row rules.

## Acceptance criteria

1. When a consumed ladder's last round has no unrepaired taken finding and the existing prior stops permit it, `review-loop` exits 0 and prints exactly one line `next: review <change>`, with the actual change name.
   *Refuted by:* a refusal, another exit code, a missing, duplicated or incorrectly named next line, or a repair instruction in this state.
2. When a consumed ladder's last round has an unrepaired taken finding and the existing prior stops permit it, `review-loop` exits 0 and prints exactly one line `next: repair <change>`, with the actual change name.
   *Refuted by:* a refusal, another exit code, a missing, duplicated or incorrectly named next line, or a review instruction in this state.
3. When a consumed ladder names a next step, it starts neither a reviewer nor a repair and does not reset, release or advance the run.
   *Refuted by:* a model or repair call, a release, a fresh run, or changed run history caused by requesting the next step.
4. When a consumed ladder is reconstructed from released history, the next step reflects the last completed round of that same run.
   *Refuted by:* a released repaired round naming repair, a released unrepaired round naming review, or a new stage being admitted.
5. When existing row, origin, record-integrity, clean-round or repair-brake stops apply, they retain their existing outcome before any consumed-ladder next step is reported.
   *Refuted by:* a next line bypassing an undecided or evidence-incomplete row, invalid origin, invalid record, clean stop or repair brake.
6. When declared paid models were excluded from a consumed snapshot, the result retains the reasons for their exclusion.
   *Refuted by:* a consumed result that drops the previously reported exclusion reasons.
7. When the ladder is consumed, the workflow and the phase-4b and phase-6 prompts describe the next repair or review and the existing full verification and independent phase-6 review before release.
   *Refuted by:* any of these texts still directing the session to stop for the maintainer solely because the ladder is consumed, or omitting the applicable verification and review sequence.

## Non-goals

Starting the named verb automatically; changing the review ladder, its membership, restart authority, repair brake or clean-stop exit; adding a separate phase-6 check or changing the existing full verification and whole-diff review; resetting a run's history; changing the night-run wake or other consumers.

## Protected areas

`AGENTS.md` already carries the decision and is not changed by this lane. Model declarations and terms, ADRs, tracker data and availability policy are outside this change.

## Definition of Done

- `make verify` green.
- `docs/WORKFLOW.md`, `prompts/04b-review-loop.md` and `prompts/06-review.md` move with the code; no ADR changes.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes `coding-harness-hwll` and its last commit carries `Closes-Bead: coding-harness-hwll`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The existing full verification and whole-diff review constitute the phase-6 check of the last repair; no additional check is implied by the recorded rule (`decisions.md`, interview minimum). [DETAIL] The phase-4 appetite is four hours including repairs: this bounded change alters an existing stop and its tests, and the limit provides a concrete stop for the implementer.
