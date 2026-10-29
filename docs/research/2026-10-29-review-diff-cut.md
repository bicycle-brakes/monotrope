---
title: "Review loop — what the reviewers see when the diff is cut"
category: research
created: 2026-10-29
updated: 2026-10-29
last_reviewed: 2026-10-29
owner: framework-architect
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-ut8q
tags: [review-loop, stage-2, diff-bound, adr-0021, spike]
---

# Review loop — what the reviewers see when the diff is cut

**Result: the 2000-line cut does not drop the end of the change at random. It
drops the tests.** `change_diff` hands Git's diff over in path order, so the
change's own workflow files come first: `docs/`, `plans/` with the growing
`findings.md`, then `prompts/` and `scripts/`, and `tests/` last. On the three
changes reviewed in the night of 2026-10-28/29, that order filled more than
half the 2000 lines before any code. No reviewer in any round saw a line of
the changes' test files. This extends bead coding-harness-ut8q (a diff over
the bound can never end the loop cleanly) with what the cut does to the
rounds that do run.

## What was measured

On 2026-10-29 the change diff was measured per file against the merge base
with `origin/main`, at the heads named below. Files are listed in the order
the reviewer receives them, with the running line count. The bound is
`REVIEW_DIFF_MAX_LINES = 2000` (`scripts/stage2.py`).

| Change, head | Before the code (docs, plans, prompts) | `findings.md` alone | Last file seen in full | Not seen at all |
| --- | --- | --- | --- | --- |
| `fail-fast-attempts`, `78676b5e`, 3371 lines | 1445 | 582 | `prompts/04-implement.md` | the last 58 lines of `scripts/stage2.py`; `tests/test_stage2.py` (698); `tests/test_stage2_fail_fast.py` (615) |
| `index-merge-regenerates`, `60cd44f2`, 3209 lines | 1095 | 450 | `scripts/ci_gates.py` | the last 145 lines of `scripts/pr_sync.py`; the kit template (35); `tests/test_pr_sync.py` (1029) |
| `run-report`, `358472d8`, 2284 lines | 888 | 253 | `scripts/run_report.py` | the last 284 lines of `tests/test_run_report.py` |

The loop records of the night show 12 rounds over a cut diff, at 2000 of
2265 to 3361 lines. The `fail-fast-attempts` loop wrote eight rounds (a ninth
failed at the provider's usage limit), and each diff note said "cut". Its diff grew from 3000 to 3361 lines as repairs landed.

## What it explains

- **Findings about text, not code.** Many rows of the night addressed the
  change's own plan, spec and decisions, which reviewers saw first and in
  full. Examples: a stale appetite in three places (rows L1-5, L1-13, L1-17),
  a duplicate ledger number (L4-1, L6-2).
- **Repeated findings.** `findings.md` carries every earlier round's rows. A
  reviewer reads its predecessors' findings as part of the change and raises
  them again. One example is the ledger-number row, rejected twice with the
  same reason.
- **Test-strength findings are impossible.** No round could judge whether
  the new tests test what they claim, because no round saw them.
- **Real code defects were still found.** All of them sat in the first 2000
  lines. On `fail-fast-attempts`, rows L3-1, L5-2, L5-3, L6-1 and L7-2 were
  in the part of `scripts/stage2.py` that was seen.

## Options for the follow-up change

These touch ADR 0021, so the choice is the maintainer's. Three were seen,
and they combine:

1. **Leave the loop's own record out of the diff.** `findings.md` is the
   review's output, not the change. `plans/INDEX.md` is generated. On the
   three changes this frees 270 to 600 lines. It is cheap and keeps every
   other file.
2. **Order code and tests before prose.** Put `scripts/` and `tests/` first,
   then `prompts/`, `docs/` and `plans/`. A cut then drops prose, which phase
   6 and the spec review also read.
3. **Split a large change across reviewers instead of cutting it.** Each
   member of a round gets a disjoint part, files whole, and a round is clean
   only when every part came back clean. This addresses the bead's
   original point, a loop that can never end cleanly, without raising the
   bound past what Pi carries uncompacted.

Option 1 alone would have kept the `run-report` diff under the bound. With
2284 − 253 − 16 = 2015 lines it misses by 15; with `research.md` (113) out as
well, it is under. For the other two changes, the tests would have reached
the reviewers only with options 2 or 3.

## Not measured

- Whether reviewers' finding quality changes when they see the tests. That
  needs a run with the new order.
- The review loop's free stage uses its own per-file and total bounds
  (`FREE_DIFF_MAX_LINES`, `FREE_DIFF_MAX_TOTAL`). Tonight no free model was
  reachable, so that path did not run.
