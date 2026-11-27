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

1. When valid guard evidence uses case-insensitive `yes` (`(?i:yes)`) — bare, with optional trailing `.` or `!`, or followed by whitespace or optional separator punctuation `[,;:.!—–-]` (with optional spaces before dashes `—`, `–`, `-`) plus mandatory whitespace and prose (e.g. `yes.`, `yes!`, `yes. <text>`, `yes — <text>`, `Yes.`) — or case-insensitive `no` (`(?i:no)`) followed by whitespace or optional separator punctuation `[,;:.!—–-]` (with optional spaces before dashes) plus mandatory whitespace and a non-empty reason containing at least one word character (`\w`) (e.g. `no. <reason>`, `no! <reason>`, `no — <reason>`, `no – <reason>`, `no - <reason>`, `No, <reason>`), a phase-6 answer with a valid verdict accepts it.
   *Refuted by:* Any of those verdict forms causes a valid verdict to be rejected.
   *Basis:* `decisions.md#Q-1`.
2. When valid guard evidence wraps the full test node ID (with or without parametrized suffix: `` `tests/<path>.py::test_<name>` `` or `` `tests/<path>.py::test_<name>[<id>]` ``) or the file path alone (`` `tests/<path>.py`::test_<name> `` or `` `tests/<path>.py`::test_<name>[<id>] ``) in paired backticks, or carries an unquoted non-empty parametrized test suffix `\[[^\]]+\]` (e.g. `[case-1]`, `[a b]`, `[1.5-x/y]`), a phase-6 answer with a valid verdict accepts it; empty `[]`, unpaired backticks (e.g. `` `tests/x.py::test_y ``), and a parametrized suffix split outside a backticked node ID (`` `tests/x.py::test_y`[case] ``) are rejected.
   *Refuted by:* A valid verdict with paired backtick-wrapped node ID/path (including combined backticks + `[<id>]`) or non-empty `[...]` suffix is rejected, or empty `[]`, an unpaired backtick, or `` `tests/x.py::test_y`[case] `` is accepted.
   *Basis:* `decisions.md#Q-1`.
3. When a valid phase-6 answer contains guard evidence beside six-cell finding rows or `No finding.`, the recorded answer retains the evidence and its verdict.
   *Refuted by:* Either verdict form is rejected or the recorded answer loses the evidence or verdict.
   *Basis:* `decisions.md#Q-1`.
4. When a `Guard evidence:` line has a blank/missing fault (`fault:` followed by no non-whitespace text before ` — catches without switch:`), a prefix only (`Guard evidence: ...`), wrong case on the inner fixed labels (`FAULT:`, `CATCHES WITHOUT SWITCH:` — case-insensitivity applies only to `yes`/`no`), a verdict word other than `(?i:yes|no)` (e.g. `maybe`, `yes-ish`, `no-op`, or unspaced `yes—text`), unlisted verdict punctuation (e.g. `yes?`, `yes…`), or a `no` without a substantive reason (bare `no`, `no.`, `no!`, or punctuation-only tail such as `no —`, `no -`, `no .` with no `\w` character), the phase-6 answer is rejected even beside a valid verdict; a wrong-case prefix (`guard evidence:`) is rejected beside `No finding.` (and never matched by `GUARD_EVIDENCE_LINE`), while `phase6_rows`'s existing `Guard evidence:` prefix filter stays unchanged; a single non-whitespace character fault (e.g. `fault: x`) counts as non-empty so verdict-refusal tests test the verdict rule itself.
   *Refuted by:* Any such malformed `Guard evidence:` line is accepted beside a finding or `No finding.`, a wrong-case `guard evidence:` line is accepted by `GUARD_EVIDENCE_LINE` or beside `No finding.`, or a single-character fault fails the fault check instead of the verdict check.
   *Basis:* `decisions.md#Q-1`.
5. When guard evidence appears without a phase-6 verdict, the answer is rejected.
   *Refuted by:* Evidence alone releases a verdict.
   *Basis:* `decisions.md#Q-1`.
6. When guard evidence uses any valid form already accepted today (excluding punctuation-only non-reasons like `no —` or `no .` that AC4 rejects), the phase-6 answer continues to accept it beside a valid verdict.
   *Refuted by:* A previously valid bare `yes`, a space-separated `yes <text>` or `no <reason>` (with word-character reason text) without punctuation, or a `yes` or reasoned `no` with comma, semicolon or colon and prose/reason is rejected.
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

[DETAIL] Spec-review S-7, S-8, S-9 & S-10 (round 2): Adopt uniform separator set `[,;:.!—–-]` (with optional spaces around dashes) for both `yes` and `no` (S-7, Reading B); require at least one `\w` character in a `no` reason so punctuation-only tails like `no —`, `no -`, `no .` are refused and excluded from AC6 (S-8, Reading B); restrict case-insensitivity strictly to `(?i:yes|no)` and explicitly refuse wrong-case labels, unlisted verdict punctuation (`yes?`, `yes…`), and unpaired backticks (S-9); allow combined backticks + parametrized suffix inside the backticked node ID or after a backticked file path, refusing split `` `node`[id] `` (S-10) (all decided under bounded standing grant).

[DETAIL] Spec-review S-11 & S-12 (round 3 final draft): S-11 Reading B — keep `phase6_rows`'s existing `Guard evidence:` prefix filter untouched (within parser scope); `GUARD_EVIDENCE_LINE` refuses wrong-case prefix `guard evidence:` (rejecting it beside `No finding.`) and refuses wrong-case inner labels (`FAULT:`, `CATCHES WITHOUT SWITCH:`) beside both verdicts. S-12 Reading A — whitespace after any separator punctuation is mandatory, so unspaced `yes—text`, `yes-ish`, and `no-op` are rejected (decided under bounded standing grant; final draft after round 3 needs no fourth review).
