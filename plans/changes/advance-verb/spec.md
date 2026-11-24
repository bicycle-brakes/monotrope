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

1. When invoked as `python3 scripts/lanes.py advance`, the driver reads its locally defined lanes file and considers its listed lanes.
   *Refuted by:* a valid listed lane is ignored or a lane absent from the file is started.
   *Basis:* `decisions.md#Q-2`, `decisions.md#Q-6`.
2. When a change argument is supplied, the driver considers only that listed change.
   *Refuted by:* another lane starts, or an unlisted target starts.
   *Basis:* `decisions.md#Q-6`.
3. When the runner's local record provides a valid `next: <verb> <change>` instruction, the driver starts that exact step through `scripts/stage2.py`.
   *Refuted by:* a different step starts, or a valid instruction is merely printed.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-2`, `decisions.md#Q-3`.
4. If the next instruction is missing, malformed, ambiguous, names another change, or is not a supported runner step, the driver stops that lane with a reason and starts no step from it.
   *Refuted by:* a guessed or mismatched step starts, or the stop has no reason.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-6`.
5. When a call reaches its centrally configured maximum of verify-bearing steps, it starts no further verify-bearing step; the default maximum is two.
   *Refuted by:* three such steps start under the default, or a configured lower bound is exceeded.
   *Basis:* `decisions.md#Q-7`.
6. If a step fails or leaves an open hand step, including a successful repair with held rows, the driver stops that lane and reports the reason.
   *Refuted by:* a subsequent step starts for that lane or no reason is reported.
   *Basis:* `decisions.md#Q-7`.
7. When the driver runs, it writes no document lifecycle field.
   *Refuted by:* the driver changes `status` or `implementation_status` in a document.
   *Basis:* `decisions.md#Q-5`.
8. When external state changes, it cannot trigger a step through the driver.
   *Refuted by:* a webhook, label, comment or branch name starts a step without local invocation and input.
   *Basis:* `decisions.md#Q-6`.
9. When the decision pull request is merged, ADR 0021 permits the separate driver to start the runner's named next step while preserving the runner's other stops.
   *Refuted by:* the ADR still forbids that driver action or weakens an existing stop.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-4`.

## Non-goals

Implementing the producer of `next:` belongs to `ladder-next-step` (bead coding-harness-hwll), which must land first. The driver is not a new workflow phase or stage-2 runner verb; it does not derive the next step, write lifecycle fields, push independently, or use external triggers. The thirteen-verb prose and its pinned tests stay unchanged.

## Protected areas

The runner's verb registries and existing stop rules remain intact; only the runner's established entry point starts model work. Held paths are edited by the orchestrator, not a stage-2 implement attempt.

## Definition of Done

- `make verify` green after the dependency lands.
- The decision pull request includes the ADR 0021 amendment and names bead coding-harness-z40g; its last commit carries `Closes-Bead: coding-harness-z40g`.
- The protected areas and non-goals are checked against the pull request file list.
- Special runs: none.

## Open decisions

[DETAIL] An eight-hour phase-4 appetite is a stop for this plan, chosen because no appetite was recorded. A missing or invalid instruction stops rather than inferring state, preserving the single decider.
