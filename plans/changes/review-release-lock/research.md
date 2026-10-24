---
title: "Research — review-release-lock"
status: draft
implementation_status: none
date: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-751
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, runner, review, record-lock]
---

# review-release-lock — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session itself at `origin/main` `7586f1a7`
(2026-10-24): the scope is one reproduced finding, so no separate
exploration call was made.

## The finding

A runner audit at `378879a` (2026-10-21) reproduced, without model calls,
that with the loop-record lock held, `release-loop` refused correctly while
`stage2.py review` still moved and deleted the same record.

## What exists today

Read in `scripts/stage2.py` at `7586f1a7`:

- `holding_record(change, root)` is the record lock (R-14, bead
  coding-harness-1wo, pull request #190): an advisory `flock` on a file
  beside the record, refusing with "another run holds the loop record" when
  it is taken; `prepare-loop`, `review-loop`, `release-loop` and the
  repair's record rewrite hold it.
- `review` reads the record, checks for undecided rows, runs the phase-6
  call, appends the verdict and then calls `release(root, change)` without
  holding the lock; `release` appends the loop rows to `findings.md` and
  removes the record's directory.

## What the change has to do

`review` takes the same lock before it reads the record and holds it through
`release()`, so a concurrent run either refuses review before any call or
waits for nothing; the record and `findings.md` stay unchanged when review
refuses. Where exactly the lock starts (before the reviewer call, or only
around the release) is for the spec to settle: holding it across a long
Codex call blocks other verbs for that time, taking it late lets the record
change between the undecided-row check and the release. A test holds the lock
and expects review to refuse and keep the record.

## Open questions

None for the maintainer: the bead's "Needed" line is the direction
(`decisions.md`, skip record).
