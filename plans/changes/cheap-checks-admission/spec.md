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

The runner's cheap tests and the kit probe in a targeted check use the targeted pytest worker policy while remaining outside the verify admission (bead coding-harness-bxxt.13). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-25, research found that the runner's cheap pytest uses `-n auto` without the targeted check's worker policy, and the targeted kit probe runs through a gate without that policy. Both run outside admission and can add unbounded load on a small machine. The maintainer chose the worker cap rather than changing the lock rule (`decisions.md#Q-1`).

## Acceptance criteria

1. When either runner path launches the cheap-check pytest, its worker environment follows the existing targeted pytest policy.
   *Refuted by:* either path launches pytest with a different worker environment for the same input and machine readings.
   *Basis:* `decisions.md#Q-1`.
2. When a targeted check runs the kit probe, the pytest process started by the probe receives the existing targeted pytest worker policy.
   *Refuted by:* the probe's pytest receives a different worker environment for the same input and machine readings.
   *Basis:* `decisions.md#Q-1`.
3. When the caller supplies a nonempty worker setting, both affected pytest processes retain that setting as the targeted pytest does.
   *Refuted by:* either process receives a replacement value.
   *Basis:* `decisions.md#Q-1`.
4. While the runner executes a targeted check, the cheap checks and selected kit probe remain outside verify admission and carry no admission ownership markers.
   *Refuted by:* either acquires admission or inherits its ownership markers.
   *Basis:* `decisions.md#Q-1`.
5. When cheap tests or a selected kit probe fail, the existing blocking failure behavior remains in effect.
   *Refuted by:* a failing affected command is reported as a successful check.
   *Basis:* `decisions.md#Q-1`.

## Non-goals

- Changing the targeted check's lock rule, worker calculation or full-verify admission policy.
- Removing the kit probe from targeted checks, changing gate selection, or fixing worker settings lost at the foreign-model environment boundary.

## Protected areas

The gate declarations and kit probe implementation remain unchanged: the existing gate and inherited environment carry the selected policy.

## Definition of Done

- `make verify` green.
- Updated with the code: `docs/WORKFLOW.md` and the relevant tests; no ADR.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- Pull request closes bead coding-harness-bxxt.13; its last commit carries `Closes-Bead: coding-harness-bxxt.13`.
- Special runs: none.

## Open decisions

- [DETAIL] Apply the existing worker policy at the affected subprocess boundaries: it is reversible and keeps the existing calculation authoritative.
