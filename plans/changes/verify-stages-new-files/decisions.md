---
title: "Decisions — verify-stages-new-files"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-fdz
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# verify-stages-new-files — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · Where the fix for untracked new files lives

context: |
  Topic: the runner's post-run make verify and gates that read the index.
  Intention: an attempt's new script was missing from the leerprobe
  gate's foreign repository, which failed a correct attempt
  (bead coding-harness-fdz).
  Today: make verify runs while the attempt's new files are untracked.
  Repository change: the runner adds them intent-to-add before make verify.
  Architecture change: none.
asked: 2026-10-16, conversation 2026-10-16 (interview, about 21:00)
answer: "candidate 1: the runner stages the attempt's new untracked, non-ignored files intent-to-add (git add -N) before make verify"
answered_by: maintainer
status: answered

The answer was given in the conversation on 2026-10-16 and recorded in the
bead's notes the same evening; this record copies it from there.

In the context of the runner's post-run verification, facing gates that
build their view from the index, we decided that the runner adds the
attempt's new, non-ignored files intent-to-add before make verify, to
achieve that every gate sees the files the attempt created, accepting that
the index holds path-only entries until the checkpoint stages the content.
— 2026-10-16
