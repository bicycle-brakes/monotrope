---
title: "Plan — phase6-english"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-tscc
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, phase-6, language]
---

# Plan — phase6-english

```text
For you:     Phase-6 verdicts are requested in English and a detected German verdict gets one retry.
Done when:   The recorded German examples, retry and preservation regressions and make verify pass.
Appetite:    Three hours of phase 4 including repairs; stop at the limit.
Not now:     Translating historical findings, checking loop marks or detecting every language.
Pre-mortem:  suppose it failed: most likely because the heuristic mistakes code or an English finding for German.
Starts unless you say stop.
```

## Build sequence

1. In `scripts/stage2.py`, score the concatenated sixth Finding cells once per valid verdict using a documented fixed threshold of common German function words and words containing ä, ö, ü or ß among the remaining words. Exclude paired backticks, paired ASCII or German quotation marks, bare paths and identifiers (including snake_case, dotted and camelCase names); an empty score and `No finding.` are not German. Calibrate on the named historical whole-verdict fixtures and test mixed rows, exclusions and the English fixtures.
2. In `scripts/stage2.py`, after structural validation and before verdict or release, preserve the first German answer with the existing protected-answer evidence facility and put its retrievable path in the record line; ask once on its thread for the same findings again in English in the same table form. Retain the resumed thread's guard-evidence instructions. Use `begin_call` and `run_codex` for the retry, with audit label `review (language retry)`, and extend `review_audit_only` only for that label. If a valid replacement returns, record it unchanged, with a notice only if detected German; if its thread changed, record both and use the returned thread for verdict and marks. If a replacement is malformed, exits, times out or has no thread, record the original with a notice naming the failure and use its thread; a leak-check BLOCK instead stops without fallback or release. Keep rejected-evidence and no-release behavior for a malformed first answer, and preserve existing structural and guard-evidence validation for replacements.
3. In `tests/test_stage2.py`, add the runner and heuristic tests in the ledger using historical text as fixtures. Test the failure paths independently, including a leak-check block, changed thread, protected evidence and audit-only verification. Add a real `STAGE2_PLANT_FAULT` guard that bypasses detection or retry and demonstrate its planted red and clean green. The implementation attempt leaves the prompt test to the orchestrator: the runner requires every named ledger test to pass before accepting the attempt, while the held prompt changes only afterward.
4. In `docs/WORKFLOW.md`, document the phase-6 verdict language request, heuristic limit, retry, preservation and leak-block exception; distinguish the review loop's malformed-output retry.
5. **Orchestrator after the accepted attempt:** edit held `prompts/06-review.md` to add `Answer in English.`, and add a test of criterion 1 to `tests/test_stage2.py`, then replace the criterion 1 ledger entry with that test; run the targeted checks, then the full check before phase 6. The implementation attempt must not edit `prompts/` or any other runner-held path.

The implementation attempt changes only `scripts/stage2.py`, `tests/test_stage2.py`, and `docs/WORKFLOW.md`; the orchestrator edits `prompts/06-review.md` and the prompt test. Do not edit historic findings, other reviewer prompts, display translations, model endpoints or ADRs. No design or ADR is due for the bounded class.

Verification after the orchestrator's prompt edit:

```sh
python3 -m pytest -q tests/test_stage2.py
make verify
```

## Criterion ledger

- 1: not a test — orchestrator checks the assembled verdict prompt after the held prompt edit, then adds its test and replaces this entry; a test named before the edit would block the implementation attempt
- 2: not yet written tests/test_stage2.py::test_phase6_language_recognises_recorded_german_verdicts — a named German verdict is missed
- 3: not yet written tests/test_stage2.py::test_phase6_language_accepts_recorded_english_verdicts — a named English verdict is flagged
- 4: not yet written tests/test_stage2.py::test_phase6_language_excludes_quotes_code_paths_and_identifiers — excluded text affects the score
- 5: not yet written tests/test_stage2.py::test_phase6_german_verdict_retries_once_on_same_thread — the first answer is accepted, release precedes retry or retry is not resumed once
- 6: not yet written tests/test_stage2.py::test_phase6_language_retry_requests_same_findings_in_english — the reminder omits a required part
- 7: not yet written tests/test_stage2.py::test_phase6_valid_replacement_is_recorded_unchanged — the first or altered answer becomes the verdict
- 8: not yet written tests/test_stage2.py::test_phase6_second_german_verdict_is_kept_with_notice — the notice is absent or a third call occurs
- 9: not yet written tests/test_stage2.py::test_phase6_english_replacement_has_no_language_notice — a notice accompanies the English replacement
- 10: not yet written tests/test_stage2.py::test_phase6_first_answer_is_retained_as_protected_evidence — the named file is unavailable or the first answer is quoted
- 11: not yet written tests/test_stage2.py::test_phase6_retry_new_thread_is_recorded_and_used_for_marks — either thread is missing or the wrong thread is used
- 12: not yet written tests/test_stage2.py::test_phase6_failed_replacement_keeps_first_verdict_with_reason — a malformed, failed, timed-out or threadless retry loses the original or its notice
- 13: not yet written tests/test_stage2.py::test_phase6_retry_leak_block_stops_without_fallback — a blocked call records a verdict or releases rows
- 14: tests/test_stage2.py::test_phase6_keeps_rejected_answer_evidence — malformed first verdict loses its rejection record
- 15: tests/test_stage2.py::test_phase6_valid_table_still_releases_and_marks — a valid verdict fails the existing sequence
- 15: tests/test_stage2.py::test_phase6_exact_no_finding_still_releases_and_marks — no-finding changes the existing sequence
- 16: not yet written tests/test_stage2.py::test_phase6_language_retry_is_audited_and_leak_checked — the retry lacks its own check or audit label
- 17: not yet written tests/test_stage2.py::test_phase6_language_retry_audit_is_allowed_without_allowing_other_edits — the audit alone blocks verification or other changes pass

## Time used

2026-11-22 03:37:37–03:40:04 UTC, 147 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-22 03:44:37–03:47:53 UTC, 196 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
