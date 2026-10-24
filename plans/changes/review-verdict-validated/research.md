---
title: "Research — review-verdict-validated"
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
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, runner, review, phase-6]
---

# review-verdict-validated — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session itself at `origin/main` `7586f1a7`
(2026-10-24): the scope is one reproduced finding, so no separate
exploration call was made.

## The finding

A runner audit at `378879a` (2026-10-21) reproduced, without model calls,
that an empty phase-6 answer, an answer saying the reviewer could not review
because of the context length, and a malformed findings table each ended
`stage2.py review` with exit code 0 and a completion note, and the external
loop record was deleted.

## What exists today

Read in `scripts/stage2.py` at `7586f1a7`, `review`:

- the Codex answer is parsed with `parse_rows`; whatever it holds is
  appended to `findings.md` as a `## Phase 6` block with a verdict line —
  there is no check that the answer is a findings table or an explicit
  no-finding verdict;
- `release` then moves the loop rows into `findings.md` (and deletes the
  external loop record), and a marks call follows;
- `answer_parts` already distinguishes a table, table lines that are not
  six-cell rows, and "no finding"; the review loop's own reviewers are
  refused on "malformed finding output: expected six-cell findings or
  exactly 'No finding.'" — the phase-6 verb has no such check.

## What the change has to do

The review verb validates the verdict before it writes anything that counts
as a verdict: valid is at least one six-cell row, or exactly the no-finding
statement the phase-6 prompt asks for. Otherwise it exits non-zero, writes
no `Phase 6 verdict` line, does not release or delete the loop record, and
keeps the raw answer as evidence where a later run cannot mistake it for a
verdict. Tests for the empty, the refused (context length) and the malformed
answer, plus a valid table and a valid no-finding verdict.

## Open questions

None for the maintainer: the bead's "Needed" line is the direction
(`decisions.md`, skip record).
