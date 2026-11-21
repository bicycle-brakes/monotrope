---
title: "Spec — ladder-next-step"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-21
updated: 2026-11-21
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

**Consumed ladder:** the saved run has no unconsumed eligible stage, has at least one completed round since its last restart, and its last completed round was not clean. A taken finding is repaired when its status is `fixed` with the evidence mark required by the existing row rules.

## Acceptance criteria

1. When a consumed ladder's last round has no unrepaired taken finding and the other applicable stops permit it, `review-loop` exits 0 with standard output exactly `next: review <change>` and a newline, using the actual change name.
   *Refuted by:* a refusal, another exit code, or any different, additional, missing or duplicated standard output.
2. When a consumed ladder's last round has a taken finding awaiting repair and the other applicable stops permit it, `review-loop` exits 0 with standard output exactly `next: repair <change>` and a newline, using the actual change name, including when that taken row has no `Broke a test` mark yet.
   *Refuted by:* a refusal for an unmarked taken row, another exit code, or any different, additional, missing or duplicated standard output.
3. When a consumed ladder names a next step, it starts neither a reviewer nor a repair and does not reset, release or advance the run.
   *Refuted by:* a model or repair call, a release, a fresh run, or changed run history caused by requesting the next step.
4. When a consumed ladder is reconstructed from released history, the next step reflects the last completed round of that same run.
   *Refuted by:* a released repaired round naming repair, a released unrepaired round naming review, or a new stage being admitted.
5. When a row has no decision, a fixed row lacks its evidence mark, or an origin, record-integrity, clean-round or repair-brake stop applies, the existing stop holds before a consumed-ladder next step is reported.
   *Refuted by:* a next line bypassing an undecided row, an unmarked fixed row, invalid origin or record, clean stop or repair brake.
6. When the declaration names paid models but the consumed snapshot has no paid stage, any exclusion reasons found from the current declaration are reported on standard error.
   *Refuted by:* omitting a currently applicable reason, placing it on standard output, or claiming a stale snapshot-time reason after the declaration changes.
7. When no round has completed in the current run, exhausting its stages stops and reports to the maintainer without naming a next step.
   *Refuted by:* a zero-round outage returning either `next:` instruction or proceeding to phase 6.
8. When the doctrine describes a consumed ladder, `docs/WORKFLOW.md`, `prompts/04b-review-loop.md`, and the exhausted-ladder rule in `AGENTS.md` describe repair for open taken rows and review once repaired.
   *Refuted by:* any of these texts requiring a maintainer decision solely because a completed run's ladder is consumed, or omitting either next step.
9. When `docs/WORKFLOW.md` describes the exit status of `review-loop`, it states that exit 0 can also mean a next step was named without writing a round.
   *Refuted by:* a statement that exit 0 always means a round was written.
10. When `prompts/06-review.md` describes the loop, it states that phase 6 can follow a consumed ladder after its last repair.
    *Refuted by:* saying the loop always runs until a clean round or omitting the consumed-ladder path.
11. When phase 6 follows a consumed ladder, the documented existing sequence requires a fresh full `make verify` and the independent reviewer's read of the whole diff before release.
    *Refuted by:* documentation permitting release without either the full verification or the independent whole-diff review, including when the loop diff was cut.

## Non-goals

Starting the named verb automatically; changing the review ladder, its membership, restart authority, repair brake or clean-stop exit; adding a separate phase-6 check or changing the existing full verification and whole-diff review; resetting a run's history; changing the night-run wake or other consumers.

## Protected areas

Model declarations and terms, ADRs, tracker data and availability policy are outside this change. The held `AGENTS.md` and prompt files are changed by the orchestrator, not the stage-2 implementation attempt.

## Definition of Done

- `make verify` green.
- `docs/WORKFLOW.md`, `prompts/04b-review-loop.md`, `prompts/06-review.md` and `AGENTS.md` move with the code; no ADR changes in this pull request. The consumed-ladder amendment of ADR 0021 is already in this worktree (commit `4755e255`); this change merges after that decision pull request (`decisions.md` Q-2).
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes `coding-harness-hwll` and its last commit carries `Closes-Bead: coding-harness-hwll`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The existing full verification and whole-diff review constitute the phase-6 check of the last repair; no additional reviewer task is implied (`decisions.md`, interview minimum). [DETAIL] The next-step line is the entire standard output and diagnostics go to standard error, so a caller can read it without parsing other messages (phase-2a S-2). [DETAIL] Exclusion diagnostics retain the existing all-paid-stages-excluded case and use current declaration reasons, avoiding a new snapshot contract (phase-2a S-3). [DETAIL] The phase-4 appetite is four hours including repairs: this bounded change alters an existing stop and its tests, and the limit provides a concrete stop for the implementer.
