---
title: "Spec — loop-record-other-worktree"
status: draft
implementation_status: none
date: 2026-11-18
last_reviewed: 2026-11-18
updated: 2026-11-18
supersedes: null
superseded_by: null
bead: coding-harness-e82i
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, review-loop]
class: bounded
appetite: 6
adr_files: []
---

# Spec — loop-record-other-worktree

A maintainer can explicitly supersede a review-loop record left in another worktree and start a fresh run without losing its history (bead coding-harness-e82i). Research: `research.md`. Decision: `decisions.md#Q-1`.

## Problem

On 2026-11-18 research found that a record is keyed by the resolved worktree path, so continuing a change in another worktree leaves its prior record invisible; the missing-record refusal names another state directory but not another worktree. The 2026-11-17-a night run parked a lane on this refusal; its findings held audit calls but no released rounds, so the existing restart could not account for them (`research.md`, incident and recovery paths).

## Terms

**Record key:** the change name and digest identifying one worktree's state directory. **Supersede:** archive the selected old loop record and account for it before a fresh run.

## Acceptance criteria

1. When any no-record refusal for the loop, restart, stage retirement, preparation or triage finds active loop records for the same change under other worktree keys in the current state directory, it names each such key.
   *Refuted by:* a matching key is omitted, or another change's key or an archive is named.
2. When the maintainer runs `release-loop <change> --restart --supersedes <key> --reason <text>` for eligible other-worktree records, repeating `--supersedes <key>` for every active other key, the runner writes one `Loop restarted: <date> after round <N> — ...` accounting line to the current findings naming each key, each record’s round-number range and archive path, the count of all pending review-loop audit calls since the last release or restart, and the reason; N is the highest superseded round.
   *Refuted by:* the line is absent, duplicated, or misstates any of those facts.
3. When supersession succeeds, each selected loop record is preserved unchanged under `<state>/coding-harness/stage2-superseded/<change>@<digest>@<UTC timestamp>/`, without overwriting a prior archive, and is no longer active at its old key.
   *Refuted by:* its contents are lost or altered, or the old key can continue that record.
4. When supersession succeeds, the next review loop starts fresh and its round numbers do not reuse numbers from the superseded record or existing findings.
   *Refuted by:* the old snapshot or consumed stages are reused, or a prior round number recurs.
5. If the requested key is invalid, belongs to another change or the current worktree, is missing without an unfinished archived supersession or unreadable, not all active other keys are named, no audit call is pending, the current worktree has an active record, the reason is blank, or the flags are incompatible, supersession refuses without changing findings or any record.
   *Refuted by:* an invalid request succeeds or changes findings or record state.
6. While either worktree's loop record is in use, supersession does not alter it or its findings.
   *Refuted by:* a competing run and supersession can both change either protected record or findings.
7. If supersession is interrupted or an archive or write fails, retry safely completes without losing records or duplicating accounting, including by recognizing records already archived before accounting.
   *Refuted by:* a fault leaves the record irretrievable, a restart line while its record remains active at the old key, or duplicate accounting on retry.
8. When a loop record is superseded, research state, research receipts and probe audits beside it remain at their original key unchanged.
   *Refuted by:* any such item moves, disappears or changes.
9. While no explicit supersession command is issued, each worktree's loop record remains private and existing release, restart and stage-retirement behavior remains in force.
   *Refuted by:* an ordinary operation adopts, changes or removes another worktree's record, or an existing restart or release regression fails.
10. When release is requested after supersession but before a new round, it refuses without writing findings.
    *Refuted by:* release writes a “loop did not run” line or otherwise changes findings.
11. When a superseded run is restarted, release requires a new phase-6 verdict after the restart line.
    *Refuted by:* a verdict preceding supersession releases the new run.
12. When the workflow describes a missing record, it explains the explicit supersession command and its effect on history and a fresh run.
    *Refuted by:* the workflow omits the command or promises recovery of the old run as the new run.

## Non-goals

- Automatically adopt another worktree's state or change the worktree-based key.
- Recover a record that is actually lost or stored in another state directory.
- Change research state, availability receipt binding, phase-6 verdict rules or the model ladder.
- Amend an architecture decision record.

## Protected areas

Other changes' records and worktrees, and the research state associated with either key, remain untouched.

## Definition of Done

- `make verify` green.
- Update `docs/WORKFLOW.md` with the command in the same pull request; no ADR changes.
- Protected areas untouched and non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes coding-harness-e82i and its last commit carries `Closes-Bead: coding-harness-e82i`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The accepted details S-1 through S-7 are recorded in `decisions.md`; they make the agreed restart measurable. A six-hour phase-4 appetite is a reversible stop for this bounded change; it includes repair rounds and leaves the agreed scope unchanged.
