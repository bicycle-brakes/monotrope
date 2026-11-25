---
title: "Spec — cheap-checks-admission"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.13
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, workers]
class: bounded
adr_files: []
---

# Spec — cheap-checks-admission

The runner's cheap pytest uses the targeted pytest worker policy, while the targeted kit probe remains serial and outside verify admission (bead coding-harness-bxxt.13). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-25, research found that both runner paths launch cheap pytest with `-n auto` without the targeted pytest worker policy; this can overload a small machine outside admission.
- The first spec review found that the targeted kit probe already launches pytest without `-n`, so adding the worker environment alone would not bound its process count (`findings.md`, S-1, 2026-11-25).

## Acceptance criteria

1. When the targeted check preparation or full-mode preparation launches cheap-check pytest, the launch uses the existing targeted pytest worker policy for its environment and machine readings.
   *Refuted by:* either preparation launches pytest with a worker setting different from the targeted policy for the same inputs.
   *Basis:* `decisions.md#Q-1`, D-2, D-3.
2. When the targeted check selects the kit probe, the probe's pytest command remains serial, without an xdist `-n` option.
   *Refuted by:* the probe launches pytest with an `-n` option.
   *Basis:* `decisions.md#Q-1`, D-1.
3. When cheap-check pytest receives a nonempty worker setting in its input environment, the targeted policy preserves that setting.
   *Refuted by:* its launch replaces or removes the supplied setting.
   *Basis:* `decisions.md#Q-1`, D-2.
4. While the runner executes a targeted check, its cheap checks and selected kit probe remain outside verify admission and carry no admission ownership markers.
   *Refuted by:* either acquires admission or inherits its ownership markers.
   *Basis:* `decisions.md#Q-1`.
5. When cheap pytest or a selected kit probe fails, the existing blocking failure behavior remains in effect.
   *Refuted by:* a failing affected command is reported as a successful check.
   *Basis:* `decisions.md#Q-1`.
6. When cheap checks compute a pytest worker setting, they do not write it into the environment dictionary supplied by their caller.
   *Refuted by:* the computed setting is added to or changes that caller-supplied dictionary; a later step independently computing its own setting is not a leak.
   *Basis:* `decisions.md#Q-1`, D-5, D-6.

## Non-goals

- Changing the targeted check's lock rule, worker calculation, gate selection or full-verify admission policy.
- Changing `run_gates`, other gates or its other callers, or fixing worker settings lost at the foreign-model environment boundary.
- Parallelizing the kit probe or removing it from targeted checks.

## Protected areas

The gate declarations and kit probe implementation remain unchanged: the probe already runs serially.

## Definition of Done

- `make verify` green.
- Updated with the code: `docs/WORKFLOW.md` and the relevant tests; no ADR.
- Protected areas untouched and non-goals unbuilt, checked by tests and review of the pull request diff.
- Pull request closes bead coding-harness-bxxt.13; its last commit carries `Closes-Bead: coding-harness-bxxt.13`.
- Special runs: none.

## Open decisions

- [DETAIL] Use the existing targeted worker policy for cheap pytest only; the probe is already serial and the other gate launches are outside this change (decisions D-1–D-4).
- [DETAIL] Keep the computed setting local to that launch so later steps retain their own environment and worker policy (decision D-5).
- [DETAIL] Judge leakage by the caller-supplied dictionary; later subprocesses may compute their own setting (decision D-6).
