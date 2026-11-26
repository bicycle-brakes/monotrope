---
title: "Spec — phase6-guard-evidence"
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, phase-6, guard-evidence]
class: bounded
appetite: 2
adr_files: []
---

# Spec — phase6-guard-evidence

Valid guard evidence accompanies a Codex phase-6 verdict without causing its rejection (bead `coding-harness-mwzv.6` — phase-6 guard-evidence parsing). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-26, inspection of three recorded rejected reviews showed that valid finding rows followed by guard evidence ending in `yes.` were rejected as malformed; the parser also rejects normal punctuation before a reason, backtick-wrapped test references and parametrized test IDs (`research.md`, orchestrator verification, at commit `94d03e0d`).

## Acceptance criteria

1. When valid guard evidence ends in `yes.` or uses `yes. <text>`, `no. <reason>` or `no — <reason>`, a phase-6 answer with a valid verdict accepts it.
   *Refuted by:* Any of those forms causes a valid verdict to be rejected.
   *Basis:* `decisions.md#Q-1`.
2. When valid guard evidence uses a backtick-wrapped test reference or a parametrized test ID, a phase-6 answer with a valid verdict accepts it.
   *Refuted by:* A valid verdict with either reference form is rejected.
   *Basis:* `decisions.md#Q-1`.
3. When a valid phase-6 answer contains guard evidence beside six-cell finding rows or `No finding.`, the recorded answer retains the evidence and its verdict.
   *Refuted by:* Either verdict form is rejected or the recorded answer loses the evidence or verdict.
   *Basis:* `decisions.md#Q-1`.
4. When a guard-evidence line has a missing fault, a prefix only, a verdict other than `yes` or `no`, or `no` or `no.` without a reason, the phase-6 answer is rejected even beside a valid verdict.
   *Refuted by:* Any such malformed line is accepted beside a finding or `No finding.`.
   *Basis:* `decisions.md#Q-1`.
5. When guard evidence appears without a phase-6 verdict, the answer is rejected.
   *Refuted by:* Evidence alone releases a verdict.
   *Basis:* `decisions.md#Q-1`.
6. When guard evidence uses an already accepted form, the phase-6 answer continues to accept it beside a valid verdict.
   *Refuted by:* A previously valid bare `yes`, or a `yes` or reasoned `no` with comma, semicolon or colon and prose, is rejected.
   *Basis:* `decisions.md#Q-1`; `research.md`, runner exploration.

## Non-goals

- Checking whether every changed guard test has evidence, or whether a named test exists or changed.
- Changing the Claude review path, guard-test proof, phase-6 verdict grammar or the guard-test doctrine.

## Protected areas

`docs/adr/0023-guard-proof-for-test-only-repairs.md` and the review instructions outside the existing parser stay untouched: the agreed change is a bounded parser correction, not a doctrine change.

## Definition of Done

- `make verify` green; regression tests exercise the accepted and rejected forms.
- Documents, models and ADRs moved with the code: none beyond this change's artifacts.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes `coding-harness-mwzv.6` — phase-6 guard-evidence parsing — and its last commit carries `Closes-Bead: coding-harness-mwzv.6`.
- Special runs: none.

## Open decisions

[DETAIL] The phase-4 appetite is two hours including repairs: this bounded parser correction has a small, locally testable surface, and the limit can be revised without changing the agreed behavior. None open.
