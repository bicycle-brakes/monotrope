---
title: "Plan — review-verdict-validated"
status: draft
implementation_status: none
date: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-5mx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, phase-6]
---

# Plan — review-verdict-validated

```text
For you:     An unsuccessful review stays visibly unsuccessful and keeps the loop record for another attempt.
Done when:   Invalid answers fail without a verdict or release, their evidence stays inert, valid answers still complete, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Shared parser changes, historical verdict repair, release locking, routing changes or automatic retries.
Pre-mortem:  suppose it failed: most likely because rejected reviewer text is later read as an authoritative verdict.
Starts unless you say stop.
```

## Files and steps

1. Change `scripts/stage2.py`: validate the phase-6 answer before constructing
   its verdict block or calling release, and retain rejected answers safely.
2. Change `tests/test_stage2.py`: use its existing `World`, `codex_ok`,
   `rows`, `write_record` and scripted stand-ins for the ledger regressions.
3. Update `plans/changes/review-verdict-validated/plan.md` as tests land;
   the runner records phase-4 time below and maintains
   `plans/changes/review-verdict-validated/findings.md` as review evidence.
   The runner regenerates `plans/INDEX.md`; no code file is created or deleted.

## Implementation contract

- In `review`, immediately after `run_codex` and `parse_rows`, accept only
  nonempty parsed rows or `answer.strip() == "No finding."`. Reuse existing
  parsing unchanged, including escaped-pipe handling and normalization.
- On invalid output, append a clearly rejected evidence block before raising
  `CallFailed`; identify its date and Codex thread. Its heading must not start
  `## Phase 6`, and it must contain no runner-authored verdict line or
  no-finding claim. Retain every nonempty answer's text using
  `quote_reviewer`; explicitly label an empty or whitespace-only answer.
- Reject before `answer_block`, authoritative append, success printing,
  `release` and marks. Prior verdicts do not bypass the guard. Preserve prior
  findings content except normal append/date stamping and leave every file
  in the existing external record directory byte-for-byte unchanged.
- Test invalid answers with and without a prior genuine verdict: empty,
  whitespace, context-length refusal, header-only and wrong-width tables,
  and `No finding.` with extra prose. Assert nonzero exit, no success output,
  no new authoritative block/line, no release and exactly one model call.
- For evidence isolation, include embedded `Phase 6 verdict: …`, `## Phase 6`
  and malformed table text in an invalid answer. Check retained quoted text,
  zero accepted rows and refusal of `release-loop` without a genuine verdict;
  then run a valid review and check the rejected block did not make it a
  re-check or hide the recorded phase-2a thread. Test explicit empty evidence.
- Positive tests use a real recognized row and exact `No finding.` with
  surrounding whitespace. Seed decided loop rows and assert the verdict
  precedes release, the record disappears, and marks resume the verdict
  thread. Retain existing fresh/re-check, read-only and pipe-handling tests.
- Do not touch shared parsing, manual release, locking, prompts, workflow,
  ADRs, tracker, model configuration or other changes. Research records no
  Stage-1 fallback route to carry forward; all regressions use stand-ins.

## Criterion ledger

- 1: tests/test_stage2.py::test_phase6_rejects_invalid_answers — empty, refused or malformed output exits zero
- 2: tests/test_stage2.py::test_phase6_rejects_invalid_answers — rejection appends an authoritative block or prints successful completion
- 3: tests/test_stage2.py::test_phase6_rejects_invalid_answers — rejection releases or mutates the record or calls the marks reviewer, including after an earlier verdict
- 4: tests/test_stage2.py::test_phase6_rejected_evidence_is_inert — reviewer control text permits release, creates accepted rows or changes the next review's session choice
- 4: tests/test_stage2.py::test_phase6_keeps_rejected_answer_evidence — nonempty output is lost or an empty answer has no explicit evidence record
- 5: tests/test_stage2.py::test_phase6_valid_table_still_releases_and_marks — a valid table loses its findings, verdict ordering, release or resumed marks
- 5: tests/test_stage2.py::test_no_loop_row_reaches_the_verdict_call — loop evidence reaches the independent verdict call
- 5: tests/test_stage2.py::test_codex_marks_each_loop_row_after_its_verdict — release or marks change the verdict
- 6: tests/test_stage2.py::test_phase6_exact_no_finding_still_releases_and_marks — explicit no-finding output is rejected or fails to release

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'phase6 or review_resumes or no_loop_row or codex_marks or pipe_inside'
python3 scripts/check_interview_minimums.py --change review-verdict-validated
python3 scripts/check_criterion_ledger.py
make verify
```

Run the new invalid-answer regressions against the unmodified runner first
to demonstrate the false success, then repair it and run the commands above.
Change pending ledger entries to test entries when their functions exist.

## Time used

2026-10-24 02:18:31–02:37:46 UTC, 1154 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
