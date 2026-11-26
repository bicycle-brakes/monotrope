---
title: "Plan — phase6-guard-evidence"
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
tags: [plan, phase-6, guard-evidence]
---

# Plan — phase6-guard-evidence

```text
For you:     Valid phase-6 guard evidence no longer discards a review over ordinary punctuation or test references.
Done when:   Accepted and malformed evidence cases pass regression tests and make verify is green.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Checking evidence coverage or changing guard-test doctrine and the Claude review path.
Pre-mortem:  suppose it failed: most likely because allowing punctuation also admits a reasonless no.
Starts unless you say stop.
```

## Build sequence

1. In `scripts/stage2.py`, extend the existing `GUARD_EVIDENCE_LINE` / `split_guard_evidence` choke point for the forms in the spec, preserving the requirement for a nonempty fault and a substantive reason after `no`; keep malformed lines in verdict text for rejection and preserve the original answer for recording. Retain existing accepted forms and do not introduce a second parsing path.
2. In `tests/test_stage2.py`, add the ledger tests with a matrix of punctuation and reference forms, including combinations; exercise both verdict types and the actual review recording path, and verify malformed lines cannot hide beside either verdict. Include the observed `yes.` regression and punctuation-only or whitespace-only purported reasons for `no`.
3. Update this plan's ledger markers when tests exist; the runner records findings and elapsed time and regenerates the plans index. No files are deleted and this bounded change requires neither design nor ADR.

## Files and limits

- `scripts/stage2.py`: widen the existing guard-evidence parser.
- `tests/test_stage2.py`: add acceptance, rejection and recording regressions.
- `plans/changes/phase6-guard-evidence/plan.md`: update ledger markers and record phase-4 time.
- `plans/changes/phase6-guard-evidence/findings.md` and `plans/INDEX.md`: runner records review evidence and regenerates the index.

Leave `prompts/06-review.md`, `templates/findings.md`, `docs/WORKFLOW.md`, the guard-proof mechanism and `docs/adr/0023-guard-proof-for-test-only-repairs.md` untouched; no held path needs an implementation edit.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'phase6_guard_evidence or phase6_refuses_malformed_guard_evidence'
make verify
```

Start the full verification detached with `python3 scripts/jobs.py start -- make verify`; inspect its exit before phase 6.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_phase6_guard_evidence_accepts_sentence_punctuation — a specified punctuated verdict is rejected.
- 2: not yet written tests/test_stage2.py::test_phase6_guard_evidence_accepts_test_reference_forms — a wrapped or parametrized reference is rejected.
- 3: not yet written tests/test_stage2.py::test_phase6_guard_evidence_records_new_forms — a valid review is rejected or its evidence or verdict is lost.
- 4: not yet written tests/test_stage2.py::test_phase6_guard_evidence_rejects_invalid_forms — malformed evidence passes beside a valid verdict.
- 5: tests/test_stage2.py::test_phase6_guard_evidence_survives_findings_and_no_finding_verdicts — evidence alone releases a verdict.
- 6: tests/test_stage2.py::test_phase6_guard_instructions_require_a_real_fault_and_block_empty_guards — previously accepted prose forms are rejected.
- 6: tests/test_stage2.py::test_phase6_guard_evidence_survives_findings_and_no_finding_verdicts — previously accepted bare yes is rejected.

## Explore fallback

On 2026-11-26 explore used the Stage-1 route, `claude-haiku-5-5`, because GLM through Z.ai had reached its weekly limit until 2026-11-29 (`research.md`).

## Time used

2026-11-26 22:12:51–22:15:01 UTC, 130 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
