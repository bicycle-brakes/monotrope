---
title: "Spec — runner-preflight-gates"
status: draft
implementation_status: none
date: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, verification]
class: bounded
adr_files: []
---

# Spec — runner-preflight-gates

Before a draft, implementation or repair model starts, document gates check the starting tree so a fault the attempt cannot fix does not consume model calls (bead `coding-harness-yv9i.3`). Research: `research.md`. Decision: `decisions.md`.

## Problem

On 2026-11-23 a stale document date in an orchestrator's edit caused a draft to spend three attempts on a starting-tree fault outside the draft's writable scope (`decisions.md`, Q-1). At commit `90ce2ed4`, research identifies document checks after attempts, alongside existing per-call admission and leak checks; those checks do not prevent that waste (`research.md`, Runner exploration).

## Acceptance criteria

1. When draft, implement or repair is about to make its first model call, the locally runnable, non-admitted document gates selected from the existing gate registry run on the starting tree.
   *Refuted by:* Any of the three verbs calls a model without running that selected set, or uses a separate hand-maintained gate list.
   *Basis:* `decisions.md#Q-1`.
2. When a blocking document gate fails on the starting tree, the run stops before any model call or fallback call.
   *Refuted by:* A fake model records a call after a blocking gate exits nonzero.
   *Basis:* `decisions.md#Q-1`.
3. When a blocking gate reports a fix command, the refusal shows that command to the operator.
   *Refuted by:* A stale document date causes refusal without `python3 scripts/check_frontmatter_current.py --stamp`.
   *Basis:* `decisions.md#Q-1`.
4. When gate selection or a blocking gate cannot complete, the run refuses before any model call and identifies the failure.
   *Refuted by:* An unavailable interpreter, launch failure, timeout or invalid gate selection is treated as green or calls a model.
   *Basis:* `decisions.md#Q-1`.
5. When all blocking starting-tree document gates pass, the existing route proceeds to its ordinary model-call admission.
   *Refuted by:* A green starting tree stops a valid draft, implement or repair before its normal call.
   *Basis:* `decisions.md#Q-1`.
6. While the starting-tree check runs, it preserves the tree and does not create or modify draft artifacts or automatically apply a fix.
   *Refuted by:* The check stamps a document or writes a spec, plan or index before the model call.
   *Basis:* `decisions.md#Q-1`.
7. When a nonblocking document gate reports a finding, the starting-tree check preserves its existing report-only enforcement.
   *Refuted by:* A report-only gate prevents a model call solely because it reports a finding.
   *Basis:* `decisions.md#Q-1`.

## Non-goals

Changing gate definitions or enforcement, automatically fixing documents, checking availability receipts, changing model routing, replacing per-call leak checks or post-attempt verification, and running full `make verify` as the preflight are outside this change.

## Protected areas

The gate registry and endpoint declarations remain unchanged: the existing registry is the source of the checks. Runner-held paths remain under the existing ownership rules.

## Definition of Done

- `make verify` green; the targeted regressions exercise all three verbs without live model calls.
- Documents moved with code: this spec, `plan.md` and `findings.md`; no ADR is changed.
- The pull request's file list shows protected areas untouched and non-goals unbuilt.
- The pull request closes bead `coding-harness-yv9i.3` and its last commit carries `Closes-Bead: coding-harness-yv9i.3`.
- Special runs: none.

## Open decisions

[DETAIL] Use the existing document-gate selection and enforcement for the starting check, including its report-only gates; this keeps the reversible selection aligned with the established document check. A draft's own missing ADR answer retains the existing document-check tolerance, because the maintainer alone can supply it. No maintainer decision is open.
