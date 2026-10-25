---
title: "Research — review-row-closing-pipe"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-2i9j
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, review-loop, parser]
---

# review-row-closing-pipe — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session on `fix/review-loop-row-ids`
(`415a795`, pull request #235, 2026-10-25). This change builds on that
branch because both touch the same answer handling in `run_swarm` and
`review_loop`.

## The finding

Measured 2026-10-22 on the loop record of `readme-review-2` (pull request
#219 test run; the record lives in the maintainer's local state directory
and is not in this repository): three free members wrote five finding lines
F-1 to F-5, each with a leading pipe and six cells but no closing pipe.
`split_row` requires both a leading and a closing pipe, so `parse_rows`
found no row and `run_swarm` failed each member with "malformed finding
output: expected six-cell findings or exactly 'No finding.'". Two paid
stages failed with the same message, and their raw answers were not
recorded, so their cause is unread (bead coding-harness-2i9j).

## What exists today

Read in `scripts/stage2.py` at `415a795`:

- `split_row(line)` returns the cells of a line that starts and ends with
  `|`, else `None`. It serves every table in the runner (loop records,
  `findings.md`, answers).
- `parse_rows(answer)` keeps six-cell lines as rows and widens a longer
  line whose second cell is a severity; everything else stays text.
- `run_swarm` raises `MalformedTable` (since #235) for an answer with table
  lines but no row, and a generic `CallFailed` for any other answer that is
  neither rows nor exactly `No finding.`. The generic message names no line.
- `review_loop` writes "<member> failed: <error>" into the round for a
  failed member of a written round; a refused attempt (all members failed,
  or #235's malformed-table refusal) writes no record (ADR 0021,
  decision 6), so the raw answer exists nowhere afterwards.
- `review` (phase 6) already keeps a rejected answer as a quoted block in
  `findings.md` (`rejected_review_block`), outside the authoritative
  records.

## Sources

- Bead coding-harness-2i9j and the maintainer's decision recorded there.
- `scripts/stage2.py` at `415a795`: `split_row`, `parse_rows`,
  `run_swarm`, `review_loop`, `rejected_review_block`, `quote_reviewer`.
