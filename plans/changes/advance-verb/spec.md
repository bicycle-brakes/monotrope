---
title: "Spec — advance-verb"
status: draft
implementation_status: none
date: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-z40g
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, lanes]
class: architectural
appetite: 8
adr_files: [docs/adr/0021-review-swarms-until-clean.md]
neighbours: [plans/changes/adr-0021-consumed-ladder/spec.md, plans/changes/harness-decide-adr/spec.md]
---

# Spec — `advance-verb`

A local lane driver starts the runner's named next step within a bounded call (bead coding-harness-z40g). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-24 lanes waited for a hand start between 03:20 and 08:00 (`decisions.md` Q-1). At research baseline 17d1e15f20c9, the runner refused an exhausted ladder rather than starting the next step; the planned `ladder-next-step` change owns the next-step output (`research.md`, complete run bf9a45e85a44e4a95f12a03ccafaf5a1, reconciliation). The existing night-run lanes file has no parser (`decisions.md` Q-6).

## Acceptance criteria

1. When `python3 scripts/lanes.py advance` runs, it reads `${XDG_STATE_HOME:-~/.local/state}/coding-harness/lanes.yaml`, whose local entries name a change and its worktree, in file order.
   *Refuted by:* The file entries are read in a different order or an entry is not read.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-9`, `decisions.md#Q-11`.
2. When a change argument is supplied, only its listed lane is considered.
   *Refuted by:* Another or unlisted change runs.
   *Basis:* `decisions.md#Q-6`.
3. If the lanes file is unreadable, malformed, contains duplicate changes, or the requested change is unlisted, the call is refused before starting a step.
   *Refuted by:* Any step starts or the call is not refused.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-11`, `decisions.md#Q-15`.
4. When a lane is considered, its runner record is selected using that lane’s worktree and each step runs using that worktree’s own `scripts/stage2.py`.
   *Refuted by:* A record or execution belongs to another checkout.
   *Basis:* `decisions.md#Q-11`.
5. When a lane has multiple recorded `next:` lines, the latest line governs under the grammar supplied by ladder-next-step.
   *Refuted by:* An earlier line overrides the latest.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-11`.
6. If an existing latest instruction is unreadable, malformed, names another change or names a disallowed verb, the lane stops without starting that instruction.
   *Refuted by:* The driver guesses or starts the instruction.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-10`, `decisions.md#Q-11`.
7. When a valid allowed instruction is read, the driver starts the exact verb and change as a separate `python3 scripts/stage2.py` child process.
   *Refuted by:* A different step runs or the runner is called in-process.
   *Basis:* `decisions.md#Q-2`, `decisions.md#Q-10`.
8. While the central allow list has its initial values, only `repair`, `review`, `review-loop`, `release-loop`, `prepare-loop` and `implement` are allowed.
   *Refuted by:* A listed verb is refused as disallowed or another verb is accepted.
   *Basis:* `decisions.md#Q-10`.
9. While the central counted list has its initial values, `implement`, `repair` and `review` count as verify-bearing steps.
   *Refuted by:* One of these is not counted or an unlisted verb is counted.
   *Basis:* `decisions.md#Q-10`.
10. When a lane reaches the centrally configured per-lane limit of verify-bearing steps, it starts no further step of any kind in that call and is treated as advanced without a park mark.
   *Refuted by:* The lane starts any step after reaching its limit or receives a park mark for reaching it.
   *Basis:* `decisions.md#Q-9`, `decisions.md#Q-10`.
11. When the limit is not configured, it defaults to two per lane.
   *Refuted by:* The default differs from two.
   *Basis:* `decisions.md#Q-10`.
12. If the configured limit is not an integer from one through five, the call is refused before any step starts.
   *Refuted by:* An invalid value is accepted or a step starts.
   *Basis:* `decisions.md#Q-10`.
13. When a step exits 1 or the latest instruction is `next: hand <change> <rows>`, that lane stops even if the preceding repair exited successfully.
   *Refuted by:* A subsequent step starts in the stopped lane.
   *Basis:* `decisions.md#Q-9`, `decisions.md#Q-12`.
14. When a lane stops, the driver records a park mark with its reason in the lanes file and does not run it again until the orchestrator clears the mark.
   *Refuted by:* A later call retries a parked lane without clearing it or the reason is missing.
   *Basis:* `decisions.md#Q-12`.
15. When a lane stops, the driver proceeds to the next listed lane sequentially.
   *Refuted by:* A stop aborts the remaining lanes or lanes overlap.
   *Basis:* `decisions.md#Q-9`.
16. When the call reports a stop, it writes the reason to standard error.
   *Refuted by:* Standard error lacks the reason.
   *Basis:* `decisions.md#Q-12`, `decisions.md#Q-16`.
17. When every selected lane advances or has nothing to do, the call exits 0; if any lane stops it exits 1; if the call is refused it exits 2.
   *Refuted by:* An outcome has a different exit code.
   *Basis:* `decisions.md#Q-12`.
18. When the driver writes state, its own code writes no document lifecycle field, including `status`, `implementation_status` or `updated`.
   *Refuted by:* The driver itself changes such a field.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-12`.
19. When locally invoked, the driver ignores lanes and steps obtained from remote labels, comments, branch names or fetched files.
   *Refuted by:* Remote data selects a lane or step.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-12`.
20. When the decision pull request is merged, ADR 0021 permits the separate driver to start `repair`, `review`, `review-loop`, `release-loop`, `prepare-loop` and `implement` while retaining the runner’s existing stops.
   *Refuted by:* The ADR omits a named verb, permits an additional verb without a further amendment, or weakens a stop.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-4`, `decisions.md#Q-10`.

21. When a lane has no loop record or no `next:` line, it has nothing to do and receives no park mark.
   *Refuted by:* The lane is parked or reported as a stop solely for the missing record or line.
   *Basis:* `decisions.md#Q-13`.
22. When a started instruction remains the latest instruction after a successful step, the lane ends for this call without repeating it.
   *Refuted by:* The same instruction starts again in that call.
   *Basis:* `decisions.md#Q-13`.
23. When a lane is already parked, the driver skips it as having nothing to do and repeats its reason on standard error.
   *Refuted by:* The lane runs, counts as a new stop, or its reason is absent from standard error.
   *Basis:* `decisions.md#Q-13`.
24. When a runner step exits 2, its lane ends for this call without a park mark.
   *Refuted by:* The driver retries it in the call or parks the lane for that refusal.
   *Basis:* `decisions.md#Q-14`.
25. When advance works on a lane, it holds that lane's lock for the duration.
   *Refuted by:* Two advance calls work on the same lane simultaneously.
   *Basis:* `decisions.md#Q-14`.
26. When advance writes the lanes file, it holds a file lock.
   *Refuted by:* Concurrent writes lose a park mark or corrupt the file.
   *Basis:* `decisions.md#Q-14`.
27. If a selected lane's worktree path does not exist or is not a worktree of this repository, only that lane is parked.
   *Refuted by:* The lane runs, is not parked, or the invalid path alone refuses the whole call.
   *Basis:* `decisions.md#Q-15`.
28. If either central verb list is absent, malformed, includes an unknown runner verb, or the counted list is not a subset of the allow list, the call is refused before a step starts.
   *Refuted by:* An invalid list is accepted or any step starts.
   *Basis:* `decisions.md#Q-15`.
29. When the night routine is followed, it calls `scripts/lanes.py advance` using one machine-local lanes file shared by concurrent runs under the specified locks.
   *Refuted by:* The routine prescribes the old per-run lanes file or hand-starts the next lane step.
   *Basis:* `decisions.md#Q-11`, `decisions.md#Q-14`, `decisions.md#Q-16`.

## Non-goals

The `ladder-next-step` change (bead coding-harness-hwll) supplies the recorded instruction and its grammar before implementation here. This driver neither derives the next step nor adds a runner verb, workflow phase, external trigger, independent push, or lifecycle-field writer. Parallel lanes belong to the detached job launcher (bead coding-harness-a6ns.1). The thirteen-verb prose and its pinned tests stay unchanged.

## Protected areas

The runner's verb registries and stops remain intact. Held paths are edited only by the orchestrator after the accepted implementation attempt.

## Definition of Done

- `make verify` green after the dependency lands.
- The decision pull request includes the night routine in `docs/WORKFLOW.md` and the ADR 0021 amendment and names bead coding-harness-z40g; its last commit carries `Closes-Bead: coding-harness-z40g`.
- The protected areas and non-goals are checked against the pull request file list.
- Special runs: none.

## Open decisions

[DETAIL] The eight-hour phase-4 appetite is a stop, chosen because no appetite was recorded. Duplicate or malformed lane entries refuse the call before any step, avoiding partial action on ambiguous configuration. The central configuration and lane format are specified in the plan; they are revisable implementation details.
