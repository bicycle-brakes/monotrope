---
title: "Decisions — runner-time-line-exits"
status: draft
implementation_status: none
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-9wp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# runner-time-line-exits — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · Where the runner writes the time line when an attempt leaves early

context: |
  Topic: the time line the runner writes under `## Time used` in plan.md for
  each implement or repair attempt (row F-6 of pull request #216).
  Intention: the phase-6 re-check of #216 found that an attempt refused by
  the first post-call credential scan leaves without its time line.
  Today: the entry is computed late in the attempt loop; exits before that
  point skip it.
  Repository change: every post-call exit passes through one place that
  writes the entry; one test per exit.
  Architecture change: none.
asked: 2026-10-22, conversation 2026-10-22 (joint window, night-run plan item 2)
answer: "write the time line in one place every post-call exit passes through; a test per exit; the immediate stop without fallback stays"
answered_by: maintainer
status: answered

In the context of the runner's measured time line, facing post-call exits
that leave before the entry is written, we decided that one place every
post-call exit passes through writes the entry, with one test per exit, to
achieve that every completed attempt carries its measurement, accepting that
a refused attempt writes plan.md once more before it stops. The immediate
stop without fallback on a credential leak stays. — 2026-10-22
