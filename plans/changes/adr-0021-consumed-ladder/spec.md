---
title: "Spec — adr-0021-consumed-ladder"
status: accepted
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-hwll
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: antigravity, version: "2026-11-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, adr, review-loop]
class: bounded
appetite: 1
adr_files: [docs/adr/0021-review-swarms-until-clean.md]
---

# Spec — adr-0021-consumed-ladder

Decision record amendment for ADR 0021 decision 7 (`docs/adr/0021-review-swarms-until-clean.md`), establishing the consumed-ladder next-step rule prior to its runner implementation in `ladder-next-step` (bead `coding-harness-hwll`). Decisions: `decisions.md`.

## Problem

ADR 0021 decision 7 currently escalates every consumed review ladder to the maintainer, whereas `AGENTS.md` (PR #419) and the planned runner change `ladder-next-step` (bead `coding-harness-hwll`) direct a consumed ladder to `next: repair <change>` or `next: review <change>`.

## Acceptance criteria

1. `docs/adr/0021-review-swarms-until-clean.md` carries the consumed-ladder amendment stating that a consumed ladder with at least one completed review round names `next: repair <change>` while a taken row is open and `next: review <change>` once every taken row is fixed, including when the loop diff was cut at the line bound.
   *Refuted by:* ADR 0021 omitting the amendment or failing to state the one-round floor and cut-diff rule.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-2`, `decisions.md#Q-4`, `decisions.md#Q-5`.
2. When zero review rounds completed in the run, ADR 0021 keeps the escalation stop to the maintainer; the repair brake and every other stop remain unchanged.
   *Refuted by:* ADR 0021 allowing a zero-round outage to advance to phase 6 or weakening the repair brake.
   *Basis:* `decisions.md#Q-2`, `decisions.md#Q-4`.

## Non-goals

Implementing the runner behavior or rewording `AGENTS.md`; both belong to `ladder-next-step` (bead `coding-harness-hwll`), which merges after this decision pull request. Design phase 2b does not run for this bounded ADR amendment.

## Protected areas

Runner code, tests, model declarations and other ADRs stay untouched.

## Definition of Done

- `docs/adr/0021-review-swarms-until-clean.md` updated and claimed under `adr_files`.
- Five maintainer-answered interview records in `decisions.md` (`Q-1` through `Q-5`).
- CI green on PR #422; merged by the maintainer as a `decision` pull request.

## Open decisions

None open.
