---
title: "Spec — phase6-guard-evidence"
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-27
updated: 2026-11-27
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

1. When valid guard evidence uses case-insensitive `yes` (bare, with optional trailing `.`/`!`, or followed by optional punctuation `[,;:.!—–-]` and whitespace plus prose, e.g. `yes.`, `yes. <text>`, `yes — <text>`, `Yes.`) or case-insensitive `no` followed by optional punctuation `[,;:.—–-]` and whitespace plus a non-empty reason (e.g. `no. <reason>`, `no — <reason>`, `no – <reason>`, `no - <reason>`, `No, <reason>`), a phase-6 answer with a valid verdict accepts it.
   *Refuted by:* Any of those verdict forms causes a valid verdict to be rejected.
   *Basis:* `decisions.md#Q-1`.
2. When valid guard evidence wraps the full test node ID or file path in backticks (`` `tests/<path>.py::test_<name>` `` or `` `tests/<path>.py`::test_<name> ``) or carries a non-empty parametrized test suffix `\[[^\]]+\]` (e.g. `[case-1]`, `[a b]`, `[1.5-x/y]`, rejecting empty `[]`), a phase-6 answer with a valid verdict accepts it.
   *Refuted by:* A valid verdict with backtick-wrapped node ID/path or non-empty parametrized `[...]` suffix is rejected, or an empty `[]` suffix is accepted.
   *Basis:* `decisions.md#Q-1`.
3. When a valid phase-6 answer contains guard evidence beside six-cell finding rows or `No finding.`, the recorded answer retains the evidence and its verdict.
   *Refuted by:* Either verdict form is rejected or the recorded answer loses the evidence or verdict.
   *Basis:* `decisions.md#Q-1`.
4. When a guard-evidence line has a blank/missing fault (`fault:` followed by no non-whitespace text before ` — catches without switch:`), a prefix only (`Guard evidence: ...`), a verdict word other than case-insensitive `yes`/`no` (e.g. `maybe`), or bare `no`/`no.`/`no!` without a non-empty reason, the phase-6 answer is rejected even beside a valid verdict; a single non-whitespace character fault (e.g. `fault: x`) counts as non-empty so verdict-refusal tests test the verdict rule itself.
   *Refuted by:* Any such malformed line is accepted beside a finding or `No finding.`, or a single-character fault fails the fault check instead of the verdict check.
   *Basis:* `decisions.md#Q-1`.
5. When guard evidence appears without a phase-6 verdict, the answer is rejected.
   *Refuted by:* Evidence alone releases a verdict.
   *Basis:* `decisions.md#Q-1`.
6. When guard evidence uses any form already accepted today, the phase-6 answer continues to accept it beside a valid verdict.
   *Refuted by:* A previously valid bare `yes`, a space-separated `yes <text>` or `no <reason>` without punctuation, or a `yes` or reasoned `no` with comma, semicolon or colon and prose is rejected.
   *Basis:* `decisions.md#Q-1`; `research.md`, runner exploration.

## Non-goals

- Checking whether every changed guard test has evidence, or whether a named test exists or changed.
- Changing the Claude review path, guard-test proof, phase-6 verdict grammar, `PHASE6_GUARD_EVIDENCE` / `PHASE6_ANSWER_FORMAT` prompt constants, or the guard-test doctrine.
- Accepting bold `**Guard evidence:**` labels or whole-line backtick-wrapped guard lines.

## Protected areas

`docs/adr/0023-guard-proof-for-test-only-repairs.md` and all prompt/review instructions (`PHASE6_GUARD_EVIDENCE`, `PHASE6_ANSWER_FORMAT`, `prompts/06-review.md`) stay untouched: the agreed change edits only the parser (`GUARD_EVIDENCE_LINE` / `split_guard_evidence`) in `scripts/stage2.py` and its tests in `tests/test_stage2.py`.

## Definition of Done

- `make verify` green; regression tests in `tests/test_stage2.py` exercise every accepted and rejected form (including the three real 2026-11-25 rejected `yes.` outputs and multi-character faults in verdict-rejection fixtures).
- Documents, models and ADRs moved with the code: none beyond this change's artifacts.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list and diff.
- The pull request closes `coding-harness-mwzv.6` — phase-6 guard-evidence parsing — and its last commit carries `Closes-Bead: coding-harness-mwzv.6`.
- Special runs: none.

## Open decisions

None open.

[DETAIL] The phase-4 appetite is two hours including repairs: this bounded parser correction has a small, locally testable surface, and the limit can be revised without changing the agreed behavior.

[DETAIL] Spec-review S-1 (verdict punctuation & case): Adopt Reading B with an explicit closed grammar (AC1) — case-insensitive `yes`/`no`, trailing `.`/`!` on `yes`, and optional separator punctuation `[,;:.!—–-]` before prose/reason (`yes` prose optional; `no` reason mandatory).

[DETAIL] Spec-review S-2 (Markdown wrapping): Adopt Reading A (AC2 & Non-goals) — allow optional backticks around the test node ID or file path only; do not accept bold labels or whole-line backtick wrapping.

[DETAIL] Spec-review S-3 (prompt constants): Adopt Reading A (Protected areas & Non-goals) — leave `PHASE6_GUARD_EVIDENCE` and `PHASE6_ANSWER_FORMAT` untouched; change only the parser regex/helper and tests.

[DETAIL] Spec-review S-4, S-5 & S-6 (fault length, parametrized IDs, space-only forms): A non-empty fault requires at least one non-whitespace character (`\S.*?`), and verdict-refusal tests use realistic multi-character faults (AC4); parametrized suffixes match `\[[^\]]+\]` rejecting empty `[]` (AC2); AC6 explicitly refutes regressions on space-only `yes <text>` and `no <reason>` (all decided under bounded standing grant).
