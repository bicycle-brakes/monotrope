---
title: "Plan — review-diff-4000"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-24
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
For you:     Every review-loop round can carry up to 4,000 lines of its selected diff before the shared bound cuts it.
Done when:   Boundary, free-stage and cut-record checks pass, the living documentation agrees, and make verify is green.
Appetite:    2 hours of phase 4, including repairs; stop at the limit.
Not now:     Multi-part review, diff ordering, and changes to the review deadline.
Pre-mortem:  suppose it failed: most likely because a cut diff was mistakenly treated as a clean round.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: add the ledger tests using the real limits, with 4,000 and 4,001 newline-counted selected lines through free, Flash and ladder prompts (inject the selected diff where free filtering cannot produce that size); check the cut record and run the new boundary tests against the old bound first. Build a free-diff fixture of several eligible files under 400 lines each that crosses the 2,000-line threshold on its last file without a free cut note; assert both the round prompt and `free_probe_prompt` carry it in full and the round has no shared-bound cut note. Exercise the real free per-file limit and total threshold, including the whole-file overshoot and omitted later files. For the probe, separately construct selected diffs above 2,000 lines with a per-file cut and with a total-threshold cut, then assert that each full selected diff reaches the probe and round prompt; confirm each free cut is recorded and cannot be clean.
2. `scripts/stage2.py`: change `REVIEW_DIFF_MAX_LINES` to 4,000, retaining the single shared path, newline counting, cut reporting, free filter and helpers, and compaction-off behavior. Correct comments or docstrings that imply all stages carry the same selected diff, without changing the helpers.
3. `docs/WORKFLOW.md` and `docs/how-it-works.md`: state the shared 4,000-line bound in each, correct the overview's 400-line per-file cut recording, and make any description of free total-threshold cuts consistent with cut-round behavior; state that Flash and ladder rounds receive the full change diff under that bound, keeping stage names intact.
4. `plans/changes/review-diff-4000/plan.md`: replace each `not yet written` ledger entry when its test exists and record phase-4 time in `## Time used`.
5. `plans/INDEX.md`: regenerate with `python3 scripts/plans_registry.py --index` if required after artifact header changes.

No held path is assigned to the implement attempt. Do not change ADRs, historical records, free filtering or its helpers and limits, splitting, the deadline, or model settings. Review the actual patch of `scripts/stage2.py` to verify those protected parts, not just the file list.

## Verification

```sh
python3 -m pytest -q tests/test_stage2.py -k 'review_diff_4000 or free_diff_actual_limits or free_diff_reports_its_own_cut or free_round_over_a_cut_file or cut_round_stays_cut_after_the_release'
make verify
```

## Criterion ledger

- 1: tests/test_stage2.py::test_review_diff_4000_line_boundary — a 4,000-line selected diff is cut or marked cut in a stage prompt.
- 2: tests/test_stage2.py::test_review_diff_4000_cut_prefix — a 4,001-line selected diff loses the wrong lines or lacks its marker.
- 3: tests/test_stage2.py::test_review_diff_4000_cut_record — a shared-bound cut is missing from the round record.
- 4: tests/test_stage2.py::test_review_diff_4000_free_overshoot_reaches_round_and_probe — an uncut free output above 2,000 lines is truncated or marked cut in the round or probe.
- 5: tests/test_stage2.py::test_free_diff_actual_limits — the real free per-file or total threshold behavior changes.
- 5: not a test — phase-6 review inspects the actual patch to verify the free filter and helpers are unchanged.
- 6: tests/test_stage2.py::test_a_free_round_over_a_cut_file_is_never_clean — a free per-file cut is not recorded or the round ends clean.
- 6: tests/test_stage2.py::test_a_cut_round_stays_cut_after_the_release — a shared-bound cut is accepted as clean after release.
- 7: not a test — phase-6 review checks both documents for their required statements and for incorrect bounds or cut-recording claims, including any claim about total-threshold cuts.
- 8: tests/test_stage2.py::test_review_diff_4000_probe_carries_free_cut_overshoots — the probe drops part of a selected diff above 2,000 lines with either a per-file cut or a total-threshold cut.
- 9: not a test — phase-6 review checks that the workflow describes the full change diff and shared bound for Flash and ladder rounds rather than the free stage's selected diff.

## Runner route — 2026-11-24

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash via Claude Code fails with unrecognized_model (bead coding-harness-b5pu; two failures on 2026-11-24); Sonnet as for detached-job-launcher (maintainer 2026-11-24).

## Time used

2026-11-21 01:49:28–01:52:18 UTC, 170 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 10:33:47–10:36:35 UTC, 168 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 10:51:52–10:53:51 UTC, 119 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-21 11:13:45–11:15:42 UTC, 117 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 21:02:11–21:26:23 UTC, 1451 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/stage2.py` is shared execution infrastructure · measured by the runner
