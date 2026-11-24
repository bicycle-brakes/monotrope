---
title: "Spec — ladder-next-step"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-24
updated: 2026-11-24
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

At commit `8cfb9de8`, a run whose review stages are consumed refuses with the same message whether the last round's taken findings are repaired or still open; a session must inspect the record and apply the maintainer's rule by hand (`research.md`, "What exists today"). The workflow and reviewer prompts still describe this state as a stop for the maintainer, although the maintainer decided the next step on 2026-11-20 (`research.md`, "Doctrine texts carrying today's behavior"; `decisions.md` Q-1). On 2026-11-24 the maintainer chose a schema-validated JSON instruction beside the loop record so consumers can read machine state instead of parsing Markdown (`decisions.md` Q-6).

## Terms

**Consumed ladder:** the saved run has no unconsumed eligible stage, has at least one completed round since its last restart, and its last completed round cannot end the loop as a clean round. For this next-step rule, an unconsumed paid rung or Flash member is inadmissible when the current declaration fails its admission check, including expired, missing or malformed terms dates, a dated skip, exclusion, removal, or unread retention or training terms. An inadmissible rung counts as consumed. An unconsumed Flash stage counts as consumed only when none of its members is admissible or replaceable; a member is replaceable only by an unconsumed admissible rung outside that stage. If at least one member is admissible or replaceable, the stage remains eligible (`decisions.md` Q-4; phase-2a S-12 and S-13). A cut-diff round cannot end the loop as a clean round even when it has no accepted findings (`decisions.md` Q-5). A taken finding is repaired when its status is `fixed` with the evidence mark required by the existing row rules.

## Acceptance criteria

1. When a consumed ladder's last round has no unrepaired taken finding and the other applicable stops permit it, `review-loop` exits 0 with standard output exactly `next: review <change>` and a newline, using the actual change name.
   *Refuted by:* a refusal, another exit code, or any different, additional, missing or duplicated standard output.
2. When a consumed ladder's last round has a taken finding awaiting repair and the other applicable stops permit it, `review-loop` exits 0 with standard output exactly `next: repair <change>` and a newline, using the actual change name, including when that taken row has no `Broke a test` mark yet.
   *Refuted by:* a refusal for an unmarked taken row, another exit code, or any different, additional, missing or duplicated standard output.
3. When a consumed ladder names a next step, it starts neither a reviewer nor a repair and does not reset, release or advance the run.
   *Refuted by:* a model or repair call, a release, a fresh run, or changed loop history caused by requesting the next step; publishing the instruction in criterion 16 is allowed.
4. When a consumed ladder is reconstructed from released history, the next step reflects the last completed round of that same run.
   *Refuted by:* a released repaired round naming repair, a released unrepaired round naming review, or a new stage being admitted.
5. When a row has no decision, a fixed row lacks its evidence mark, or an origin, record-integrity, clean-round or repair-brake stop applies, the existing stop holds before a consumed-ladder next step is reported.
   *Refuted by:* a next line bypassing an undecided row, an unmarked fixed row, invalid origin or record, clean stop or repair brake.
6. When the declaration names paid models but the consumed snapshot has no paid stage, any exclusion reasons found from the current declaration are reported on standard error.
   *Refuted by:* omitting a currently applicable reason, placing it on standard output, or claiming a stale snapshot-time reason after the declaration changes.
7. When no round has completed in the current run, exhausting its stages exits 2 and reports to the maintainer without naming a next step.
   *Refuted by:* a zero-round outage exiting with a code other than 2, returning either `next:` instruction, or proceeding to phase 6.
8. When the doctrine describes a consumed ladder, `docs/WORKFLOW.md`, `prompts/04b-review-loop.md`, `prompts/02a-spec-review.md`, and `AGENTS.md` describe repair for open taken rows and review once repaired.
   *Refuted by:* any of these texts requiring a maintainer decision solely because a completed run's ladder is consumed, omitting either next step, or claiming that the loop always ends with a clean round, including in their phase tables and `review-loop` descriptions.
9. When `docs/WORKFLOW.md` describes the exit status of `review-loop`, it states that exit 0 can also mean a next step was named without writing a round.
   *Refuted by:* a statement that exit 0 always means a round was written.
10. When `prompts/06-review.md` describes the loop, it states that phase 6 can follow a consumed ladder after its last repair.
    *Refuted by:* saying the loop always runs until a clean round or omitting the consumed-ladder path.
11. When phase 6 follows a consumed ladder, the documented existing sequence requires a fresh full `make verify` and the independent reviewer's read of the whole diff before release.
    *Refuted by:* documentation permitting release without either the full verification or the independent whole-diff review, including when the loop diff was cut.
12. When every remaining unconsumed stage is ineligible under the current admission check, a completed run satisfies the stage-exhaustion part of the next-step rule.
    *Refuted by:* refusing solely because an inadmissible rung remains, including for expired or malformed terms, a dated skip, exclusion or removal, instead of applying the applicable next step or prior stop; or treating a run with an admissible unconsumed rung as exhausted.
13. While an unconsumed Flash stage has an admissible or replaceable member, the next-step rule does not treat that stage as consumed.
    *Refuted by:* a `next:` instruction when even one member is admissible or replaceable; or failure to apply the next-step rule when neither a Flash member nor an unconsumed replacement rung is admissible and no other eligible stage remains.
14. When a consumed ladder's last round had a cut diff and no accepted findings, the next-step rule names review if the other applicable stops permit it.
    *Refuted by:* a clean stop or refusal instead of `next: review <change>` for a cut round with no rows or only rejected rows.

15. When the next-step rule passes over unconsumed models because their admission fails, it names each passed-over model and its admission failure reason on standard error.
    *Refuted by:* omitting any passed-over model or its reason, or writing a diagnostic to standard output.

16. When `review-loop` names a next step, it publishes a schema-validated `next.json` beside that run's loop record with the same change and verb as its standard-output line.
    *Refuted by:* a missing or invalid file, a file in another run's state directory, or a change or verb that differs from the printed instruction.
17. When a next-step record is validated, the declared schema requires schema version 1, the change name, a verb from `review`, `repair`, or `hand`, row identifiers for `hand`, the producing verb, and the UTC writing time.
    *Refuted by:* accepting a missing or malformed required field, an unsupported version or verb, or a `hand` instruction without row identifiers; or rejecting a valid record for any of the three verbs.
18. When `review-loop` publishes a next-step record, the producing verb is `review-loop`, the timestamp is the UTC time of publication, and the row identifiers are empty for `review` and `repair`.
    *Refuted by:* a wrong producer, a non-UTC or stale timestamp, or row identifiers on a review or repair instruction.
19. When a next-step record is published, it is written to a temporary file in the same directory and atomically replaces `next.json` only after schema validation.
    *Refuted by:* direct truncation or partial visibility, publication of an invalid record, or a failed replacement leaving partial JSON at the destination.
20. If validation or publication of the instruction fails, `review-loop` reports the failure and does not exit 0 or print a `next:` instruction.
    *Refuted by:* a successful exit or next-step line when validation or replacement fails, or a failure with no diagnostic.
21. When `review-loop` starts processing a run, it invalidates that run's previous next-step instruction before reporting a new outcome.
    *Refuted by:* a prior instruction remaining readable as current after that invocation refuses, writes a round, or reaches a clean stop.
22. When the next-step instruction is persisted, it is not written to `loop.md` or any other Markdown file.
    *Refuted by:* any Markdown file gaining the instruction as machine state.

## Non-goals

Starting the named verb automatically; changing the review ladder, its membership, restart authority, repair brake or clean-stop exit; adding a separate phase-6 check or changing the existing full verification and whole-diff review; resetting a run's history; changing the night-run wake or other consumers; implementing the `hand` producer in the separate advance-verb change.

## Protected areas

Model declarations and terms, ADRs, tracker data and availability policy are outside this change. The held `AGENTS.md` and prompt files are changed by the orchestrator, not the stage-2 implementation attempt.

## Definition of Done

- `make verify` green.
- The next-step schema and validator, `docs/WORKFLOW.md`, `prompts/04b-review-loop.md`, `prompts/02a-spec-review.md`, `prompts/06-review.md` and `AGENTS.md` move with the code; no ADR changes in this pull request. The consumed-ladder amendment of ADR 0021 is already in this worktree (commit `4755e255`); this change merges after that decision pull request (`decisions.md` Q-2).
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes `coding-harness-hwll` and its last commit carries `Closes-Bead: coding-harness-hwll`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The existing full verification and whole-diff review constitute the phase-6 check of the last repair; no additional reviewer task is implied (`decisions.md`, interview minimum). [DETAIL] The next-step line is the entire standard output and diagnostics go to standard error, so a caller can read it without parsing other messages (phase-2a S-2). [DETAIL] Exclusion diagnostics retain the existing all-paid-stages-excluded case and use current declaration reasons, avoiding a new snapshot contract (phase-2a S-3). [DETAIL] The phase-4 appetite is four hours including repairs: this bounded change alters an existing stop and its tests, and the limit provides a concrete stop for the implementer.

[DETAIL] Apply the same current admission check to rungs and Flash members, and count only an admissible unconsumed rung as a replacement, so ineligible models cannot keep a spent run blocked (phase-2a S-12 and S-13). [DETAIL] Name each passed-over model and reason on standard error to preserve the reason for its exclusion while keeping standard output machine-readable (phase-2a S-14). [DETAIL] Align the spec-review prompt as well, so it describes both terminal paths consistently (phase-2a S-15).

[DETAIL] Schema version 1 uses an empty row list for `review` and `repair` and a nonempty list for `hand`; the common shape lets the later hand producer use the same validator. A new invocation removes its prior instruction before computing its outcome so a refused or advanced run does not retain an obsolete instruction. The separate advance-verb change owns the `hand` producer; this change supplies its schema and validator (`decisions.md` Q-6).
