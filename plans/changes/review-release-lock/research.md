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

## Draft-stage repository checks — 2026-10-24

Read at `4e18b97d`: `main` dispatches `review` through the unlocked fallback,
while `prepare-loop`, `review-loop` and `release-loop` hold `holding_record`.
Wrapping the review dispatch therefore covers its first `read_record`,
verdict call and append, `release`, and loop marks without nesting locks in
`release`. The lock file is outside the directory that `release` removes.

The local `World` fixture and Codex stand-ins in `tests/test_stage2.py`
exercise `main` without real model calls. Existing regressions cover verdict
and marks ordering, a failed marks call, and undecided-row refusal. The
contention test in `tests/test_stage2_availability.py` covers the three other
record verbs but not `review`; the new tests can reuse its real-lock pattern.

`templates/spec.md` exists; no plan template exists under `templates/` at
this commit, so the plan follows `prompts/03-plan.md` and the adjacent
runner plans. `scripts/validate_change_artefacts.py` named in the prompts
does not exist at this commit; interview and criterion-ledger checks exist.
Session-registry files and live pull-request state were not read: they
require access outside this runner's permitted worktree and git directory.
