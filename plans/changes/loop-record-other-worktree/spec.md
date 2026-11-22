---
title: "Spec — loop-record-other-worktree"
status: draft
implementation_status: none
date: 2026-11-18
last_reviewed: 2026-11-18
updated: 2026-11-21
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

**Record key:** the change name and digest identifying one worktree's state directory. **Supersede:** archive the selected old loop record and account for it before a fresh run. **Other worktree keys:** keys derived from the currently listed worktrees of this repository; worktrees no longer listed by git and other repositories are excluded. A worktree still listed by git remains eligible even if its directory is gone.

## Acceptance criteria

1. When any no-record refusal for the loop, restart, stage retirement, preparation or triage finds active loop records for the same change under other worktree keys in the current state directory, it names each such key.
   *Refuted by:* a matching key is omitted, or another change's key or an archive is named.
2. When the maintainer runs `release-loop <change> --restart --supersedes <key> --reason <text>` for eligible other-worktree records, repeating `--supersedes <key>` for every active other key, the runner writes one `Loop restarted: <date> after round <N> — ...` accounting line to the current findings naming each key, each record’s round-number range and archive subdirectory expressed as `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2-superseded/<change>@<superseding-digest>@<UTC timestamp>/<key>`, the count of all pending review-loop audit calls since the last release or restart, and the reason; N is the highest round ever assigned, including superseded rounds, released rounds, the current round count and the previous restart floor.
   *Refuted by:* the line is absent, duplicated, or misstates any of those facts.
3. When supersession succeeds, all selected records and the other non-research entries that release would delete, including `availability.json`, are preserved unchanged in one unique archive directory under `<state>/coding-harness/stage2-superseded/`, and are no longer active at their old keys.
   *Refuted by:* its contents are lost or altered, or the old key can continue that record.
4. When supersession succeeds, the next review loop starts fresh and each subsequent round, including after release, is numbered N plus the number of rounds run since the restart plus one.
   *Refuted by:* the old snapshot or consumed stages are reused, or a round is misnumbered or a prior round number recurs.
5. If the requested key is invalid, belongs to another change or the current worktree, is missing without an unfinished archived supersession or unreadable, the complete active and unfinished key set is not named, the current worktree has an active record, the reason is blank, or the flags are incompatible, supersession refuses without changing findings or any record.
   *Refuted by:* an invalid request succeeds or changes findings or record state.
6. While either worktree's loop record is in use, supersession does not alter it or its findings.
   *Refuted by:* a competing run and supersession can both change either protected record or findings.
7. If supersession is interrupted or an archive or write fails and its key set and readability remain unchanged, retry safely completes without losing records or duplicating accounting, using a staged archive with a manifest of the complete key set and the superseding worktree key, finalized before accounting; retry completes only the same key set started by that worktree.
   *Refuted by:* a fault leaves the record irretrievable, a restart line while its record remains active at the old key, duplicate accounting on retry, an omitted key after a partial move, or one worktree completing another worktree’s archive.
8. When a loop record is superseded, research state, research receipts and probe audits beside it remain at their original key unchanged.
   *Refuted by:* any such item moves, disappears or changes.
9. While no explicit supersession command is issued, each worktree's loop record remains private and existing release, restart and stage-retirement behavior remains in force except for the plain restart refusal in criterion 13.
   *Refuted by:* an ordinary operation adopts, changes or removes another worktree's record, or an existing restart or release regression fails.
10. When release is requested after a supersession restart but before a new round, it exits unsuccessfully without writing findings; a plain restart retains its existing release behavior.
    *Refuted by:* release exits successfully, writes a “loop did not run” line, or otherwise changes findings.
11. When a superseded run is restarted, release requires a new phase-6 verdict after the restart line.
    *Refuted by:* a verdict preceding supersession releases the new run.
12. When the workflow describes a missing record, it explains the explicit supersession command and its effect on history and a fresh run.
    *Refuted by:* the workflow omits the command or promises recovery of the old run as the new run.

13. When a plain restart is requested while another worktree has an active record for the same change, it refuses, names those keys and points to `--supersedes`.
    *Refuted by:* the restart succeeds or omits a key or the supersession option.
14. When a clean round runs after a supersession restart, the clean stop prevents the next stage from running.
    *Refuted by:* a paid stage runs after a clean fresh round.
15. When the repair brake applies to rounds after a supersession restart, it stops the loop using only rounds after the restart floor.
    *Refuted by:* the brake ignores an applicable fresh round or counts an earlier round.
16. When a supersession archive is retried, its accounting line is matched to the archive by its directory name.
    *Refuted by:* a retry matches a different archive or duplicates the line.
17. When a later plain restart follows supersession, its restart floor is the highest round number ever assigned, including clean rounds without findings and the previous restart floor.
    *Refuted by:* the line understates that number or a later round repeats a number.
18. When the named eligible active records have no pending audit calls, supersession is allowed and the accounting line reports zero calls.
    *Refuted by:* the command refuses solely for the lack of calls or reports a nonzero count.
19. Supersession, its retry and release of a change's loop records run under one repository-wide lock per change in the state directory, held from reading the active and unfinished key set until the accounting line is written; a second worktree that asks while the lock is held refuses, naming the holder, and changes no record or findings.
    *Refuted by:* two worktrees interleave supersession, retry or release of the same change (rows P6-1, P6-2), or the waiting one changes a record.
    *Basis:* maintainer decision 2026-11-20 (option A: one choke point closes concurrent supersession instead of case repair).

## Non-goals

- Automatically adopt another worktree's state or change the worktree-based key.
- Recover a record that is actually lost or stored in another state directory.
- Change research state, availability receipt binding, phase-6 verdict rules or the model ladder.
- Amend an architecture decision record.
- Recover or abandon an interrupted supersession whose key set changes or whose remaining record becomes unreadable; the follow-up is coding-harness-0aht (abandon or roll back an interrupted supersession).
- Discover records of worktrees no longer listed by git or of other repositories.

## Boundary

An interrupted multi-step supersession is outside this change. If a supersession stops between its steps — an archive finalised before its accounting line is written, or a `loop.md` moved into staging that then becomes unreadable — a later request is not guaranteed to refuse without changing records (phase-6 re-check rows P6-1 and P6-2, 2026-11-21). These are the third and fourth findings of one crash-window mechanism after N6-1 and N6-2; closing it needs one journal of the supersession steps that a retry replays or refuses on, which is bead coding-harness-bw73.3.

## Protected areas

Other changes' records and worktrees, and the research state associated with either key, remain untouched.

## Definition of Done

- `make verify` green.
- Update `docs/WORKFLOW.md` with the command in the same pull request; no ADR changes.
- Protected areas untouched and non-goals unbuilt, as shown by the pull request's file list.
- The pull request closes coding-harness-e82i and its last commit carries `Closes-Bead: coding-harness-e82i`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The accepted details S-1 through S-18 are recorded in `decisions.md`; they make the agreed restart measurable. A six-hour phase-4 appetite is a reversible stop for this bounded change; it includes repair rounds and leaves the agreed scope unchanged.
