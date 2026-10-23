---
title: "Research — loop-state-block"
status: draft
implementation_status: none
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-i70
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, runner, review-loop, loop-state]
---

# loop-state-block — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session itself at `origin/main` `7586f1a`
(2026-10-23): the scope is one reproduced finding, so no separate
exploration call was made.

## The finding

A runner audit at `378879a` (2026-10-21) reproduced, without model calls,
that free text a phase-6 reviewer adds is stored unfiltered and later parsed
as the runner's loop state: a forged `Loop state: {...}` line in a verdict
made the loop start a never-discovered free model without a catalog query.

## What exists today

Read in `scripts/stage2.py` at `7586f1a`:

- `STATE_LINE` matches `^Loop state: (\{.*\})` anywhere in a text
  (multiline).
- `write_round` and `write_state` replace the **first** match in
  `loop.md` and otherwise insert the line before the first round heading.
- `read_state` reads the record line by line and skips reviewer lines
  (`_record_lines`); without a record it takes the block of the last
  release in `findings.md`, cuts it at `Kept from the loop record:` and
  takes the first `STATE_LINE.search` match in the rest.
- Whether a phase-6 verdict, or any other text a model wrote, can stand
  inside that release block, or before the runner's own line, so that a
  forged line wins, was not traced to the end by this session; the spec
  settles it from the code, together with the release (`release-loop`) and
  the review verb's verdict writing.

## What the change has to do

The runner writes its loop state into a clearly marked block of its own and
reads state only from there; reviewer text is never parsed as state, whatever
it contains (`decisions.md`, Q-1). A test plants a forged state line in a
phase-6 verdict and in a loop-round answer and shows the runner's own state
wins or the run refuses.

## Open questions

None for the maintainer: the direction is decided (`decisions.md`, Q-1).
