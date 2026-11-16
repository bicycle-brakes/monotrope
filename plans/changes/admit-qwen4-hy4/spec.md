---
title: "Spec — admit-qwen4-hy4"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-x0ph
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-16", model: gpt-6.1-terra}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, model-terms, opencode-go]
class: bounded
appetite: 1
adr_files: []
---

# Spec — admit-qwen4-hy4

Admit qwen4-max and hy4 to the OpenCode Go paid review ladder with read terms and verified reachability (work item coding-harness-x0ph). Research: `research.md`; decisions: `decisions.md`.

## Problem

The catalog refresh of 2026-11-16 found qwen4-max and hy4, but neither is declared for the paid ladder; the runner therefore cannot select them as paid review models (`decisions.md` Q-1; `research.md`, sections 1 and 3). The public terms for these ids were not read in the research, so their retention, training and request values cannot be assumed (`research.md`, section 3).

## Acceptance criteria

1. When the paid ladder is read, qwen4-max and hy4 are both declared members.
   *Refuted by:* either id is absent from `opencode-go.modelle`.
2. When either model is admitted, its terms record contains a dated public-source reading of retention and training, with training recorded as `Not used`, and an expiry derived under the existing terms policy.
   *Refuted by:* a missing, unsupported, expired or non-compliant terms field for either id.
3. When either model is admitted, its positive requests-per-five-hours value and dated source reading match the public Go request table.
   *Refuted by:* either value or its source and reading date is missing or differs from the source.
4. When a fresh availability preparation runs, each model has a refreshed catalog definition and a successful reachability probe under the existing address policy.
   *Refuted by:* either model is absent, unprobeable, rejected by the address policy or fails its probe.
5. When the paid ladder is ordered, both models take their positions under the existing requests-per-five-hours ordering rule.
   *Refuted by:* either model is absent from the eligible ladder or ordered contrary to that rule.

## Non-goals

- Do not admit longcat-2.0; the maintainer excluded it because of its recent performance (decisions.md Q-2).
- Do not admit contributor models; their separate trial requires its own decision (decisions.md Q-3).
- Do not change runner behavior, the existing hy4-preview admission, free-model policy or ADRs.

## Protected areas

Runner code, existing model declarations and data policies remain unchanged except for the two new admissions; these are outside the agreed bounded scope.

## Definition of Done

- `make verify` green; the public source readings and successful fresh availability preparation are recorded with dates and the tested commit in the pull request.
- `model-endpoints.yaml` moves with this change; no ADR is changed.
- The pull request file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes work item coding-harness-x0ph and its last commit carries `Closes-Bead: coding-harness-x0ph`.

## Open decisions

[DETAIL] A one-hour phase-4 appetite is chosen for this bounded declaration change; it is a stop, not an estimate. Source values are deliberately left to the dated reading rather than guessed.
