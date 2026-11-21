---
title: "Plan — review-diff-4000"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, review-loop, diff-bound]
---

# Plan — review-diff-4000

```text
For you:     Paid reviewers can receive up to 4,000 lines of a change diff before it is cut.
Done when:   Boundary and cut-record tests pass, the free limits remain covered, and make verify is green.
Appetite:    2 hours of phase 4, including repairs; stop at the limit.
Not now:     Multi-part review, diff ordering, and changes to the review deadline.
Pre-mortem:  suppose it failed: most likely because a cut diff was mistakenly treated as a clean round.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: add the ledger's boundary and paid-prompt tests, asserting actual 4,000/4,001-line behavior without monkeypatching the bound, including the full 4,000-line paid prompt; add a free-limit test using the actual 400/2,000 limits and enough files to cross the total. Retain the existing free-cut and cut-release regressions. Make the new paid-bound tests fail against the old bound first.
2. `scripts/stage2.py`: set `REVIEW_DIFF_MAX_LINES` to 4,000; keep newline counting, cut reporting, free limits and the compaction-off explanation intact.
3. `docs/WORKFLOW.md` and `docs/how-it-works.md`: update the overall limit and explicitly distinguish the free total and per-file limits.
4. `plans/changes/review-diff-4000/plan.md`: replace each `not yet written` ledger entry with its test entry when that test exists; record phase-4 time in `## Time used`.
5. `plans/INDEX.md`: regenerate with `python3 scripts/plans_registry.py --index` after the change artifacts are in place.

No held path is edited by the implement attempt. Do not change ADRs, historic records, free filtering, splitting, the deadline or model settings.

## Verification

```sh
python3 -m pytest -q tests/test_stage2.py -k 'paid_review_diff_4000 or free_diff_actual_limits or free_diff_reports_its_own_cut or cut_round_stays_cut_after_the_release'
make verify
```

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_paid_review_diff_4000_line_boundary — a 4,000-line paid diff is cut or marked cut.
- 2: not yet written tests/test_stage2.py::test_paid_review_diff_4000_cut_reaches_prompt_and_record — a 4,001-line paid diff lacks the correct prefix, marker or record note.
- 3: tests/test_stage2.py::test_free_diff_reports_its_own_cut — either free limit stops cutting and reporting its cut.
- 3: not yet written tests/test_stage2.py::test_free_diff_actual_limits — the real per-file or total free limit differs from 400 or 2,000 lines or fails to cut.
- 4: tests/test_stage2.py::test_a_cut_round_stays_cut_after_the_release — a cut round is accepted as clean after release.
- 5: not a test — phase-6 review compares both living documents' overall and free limits with the spec.

## Time used

2026-11-21 01:49:28–01:52:18 UTC, 170 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
