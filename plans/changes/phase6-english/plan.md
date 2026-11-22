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

1. In `scripts/stage2.py`, assess only parsed finding cells of a structurally valid phase-6 verdict with a standard-library heuristic: remove Markdown code spans, paths and identifiers, then use a fixed, documented threshold over German function words and words containing ä, ö, ü or ß. Calibrate the threshold with the actual historical German and English findings in the tests; do not classify the exact `No finding.` verdict as German. This is an approximation, not a promise to detect every language.
2. In `scripts/stage2.py`, after structural validation and before appending or releasing, retry a detected German verdict once by resuming the returned Codex thread with an English reminder and the phase-6 answer format. Use the ordinary `begin_call` and `run_codex` path so the leak check and audit apply; validate the replacement structurally before using it. Keep its reviewer text through the existing answer-rendering path, add a clear notice within the verdict block only if it too is detected as German, and use the replacement thread for the verdict and marks. A malformed verdict at either position keeps the existing rejected-evidence and no-release path; a failed or blocked retry must not release or record an authoritative verdict.
3. In `tests/test_stage2.py`, add the ledger regressions below using historical finding text copied as test data, including English and German examples, code/path/identifier exclusions, an exact no-finding response, same-thread retry, malformed replacement, audit and blocked leak check. Include a real `STAGE2_PLANT_FAULT` guard that bypasses the new detection or retry behavior and prove that the normal test catches the fault; keep the existing phase-6 ordering, thread and guard-evidence tests green.
4. In `docs/WORKFLOW.md`, document the phase-6 language request, heuristic limit, one retry and notice; keep the distinction from the review loop's malformed-output retry explicit.
5. **Orchestrator, after the accepted implementation attempt:** add `Answer in English.` to `prompts/06-review.md`; this is a runner-held path, so the implement attempt must not edit it. Run the targeted prompt and runner tests after this hand edit, then the full check before phase 6.

The implementation attempt may create or edit only `scripts/stage2.py`, `tests/test_stage2.py`, and `docs/WORKFLOW.md`; the orchestrator edits `prompts/06-review.md`. The spec and plan in this change folder describe the work. Do not edit historic findings, other review prompts, runner display translations, endpoints or ADRs.

Verification after the orchestrator's prompt edit:

```sh
python3 -m pytest -q tests/test_stage2.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_phase6_verdict_prompt_requests_english — the actual verdict prompt omits the instruction
- 2: not yet written tests/test_stage2.py::test_phase6_language_heuristic_recognises_recorded_german — a recorded German verdict is missed
- 3: not yet written tests/test_stage2.py::test_phase6_language_heuristic_ignores_code_paths_and_identifiers — German tokens in code trigger an English finding
- 4: not yet written tests/test_stage2.py::test_phase6_german_verdict_retries_once_on_same_thread — the first answer is accepted, the thread changes or retry count exceeds one
- 5: not yet written tests/test_stage2.py::test_phase6_second_german_verdict_is_kept_with_notice — the replacement is changed, lost or unmarked, or a third call occurs
- 6: not yet written tests/test_stage2.py::test_phase6_english_replacement_is_kept_without_notice — the first verdict or a false notice is recorded
- 7: not yet written tests/test_stage2.py::test_phase6_malformed_replacement_does_not_release — malformed replacement becomes authoritative or releases rows
- 7: tests/test_stage2.py::test_phase6_keeps_rejected_answer_evidence — malformed first verdict loses its rejection record
- 8: tests/test_stage2.py::test_phase6_valid_table_still_releases_and_marks — a valid verdict fails the existing sequence
- 8: tests/test_stage2.py::test_phase6_exact_no_finding_still_releases_and_marks — no-finding changes the existing sequence
- 9: not yet written tests/test_stage2.py::test_phase6_language_retry_runs_leak_check_and_is_audited — the retry bypasses a refusal or leaves no call record

## Time used

2026-11-22 03:37:37–03:40:04 UTC, 147 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
