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

1. When the paid ladder declaration is read, both qwen4-max and hy4 are listed in `opencode-go.modelle`.
   *Refuted by:* either id is absent.
2. If a model's terms reading is missing, ambiguous or non-compliant, its wire API is unmapped, or its reachability probe fails, that id has a dated skip with the actual reason.
   *Refuted by:* an affected id has no skip date or a missing or inaccurate reason.
3. When an id is not skipped, its terms record contains a dated, sourced retention reading and records training as `Not used`, with expiry under the existing terms policy; retention above zero days is permitted.
   *Refuted by:* a missing, unsupported or expired reading, or training other than `Not used`.
4. When an id is not skipped, its positive requests-per-five-hours value and dated source match the public Go request table.
   *Refuted by:* the value, source or date is missing, invalid or differs from the recorded evidence.
5. When an id is not skipped, a fresh availability preparation finds its catalog definition and its reachability probe succeeds under the existing address policy.
   *Refuted by:* the definition is absent or the probe is refused or fails.
6. When a public table row cannot be unambiguously matched to the exact id, that row is treated as missing for that id.
   *Refuted by:* a single ambiguous Hy4 row is attributed to `hy4` or `hy4-preview` without evidence distinguishing them.
7. When terms or request values are read for either id, dated evidence preserves the relevant source rows and their attribution to the exact id for later review.
   *Refuted by:* a reviewer cannot compare a declared value or a skip for a missing or ambiguous row with the recorded reading.
8. When an id has a dated skip, it is ineligible for paid review and research calls under the existing terms policy.
   *Refuted by:* a skipped id passes the terms check for either use.

## Non-goals

- Do not admit longcat-2.0; the maintainer excluded it because of its recent performance (decisions.md Q-2).
- Do not admit contributor models; their separate trial requires its own decision (decisions.md Q-3).
- Do not change runner behavior, the existing hy4-preview admission, free-model policy or ADRs.
- Eligible terms records also make the ids research candidates under existing rules; this consequence is in scope, without changing research selection.

## Protected areas

Runner code, existing model declarations and data policies remain unchanged except for the two new admissions; these are outside the agreed bounded scope.

## Definition of Done

- `make verify` green; the public source readings and fresh availability preparation results, including skips, are recorded with dates and the tested commit in the pull request.
- `model-endpoints.yaml` moves with this change; no ADR is changed.
- The pull request file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes work item coding-harness-x0ph and its last commit carries `Closes-Bead: coding-harness-x0ph`.

## Open decisions

[DETAIL] A one-hour phase-4 appetite is chosen for this bounded declaration change; it is a stop, not an estimate. Source values are deliberately left to the dated reading rather than guessed. Eligible admissions become research candidates because the existing shared terms policy applies; skipped ids fail that same policy. The redundant ordering criterion was removed because the unchanged runner computes order from the recorded values.
