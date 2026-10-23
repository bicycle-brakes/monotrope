---
title: "Research — runner-time-line-exits"
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
tags: [research, stage2, runner, time-line]
---

# runner-time-line-exits — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session itself at `origin/main` `8acaa8b`
(2026-10-23): the scope is one finding already reproduced by a reviewer, so
no separate exploration call was made.

## What exists today

The merged change `runner-time-line` (pull request #216, merged at
`aed2999`) makes `scripts/stage2.py` measure each implement and repair
attempt and write its line under `## Time used` in `plan.md` itself
(`time_entry`, `with_time_entry`). Its last phase-6 re-check (Codex,
2026-10-22, `plans/changes/runner-time-line/findings.md`) left one MAJOR row
open:

- **F-6** — when a successful model call leaves the GLM credential in a
  changed file, the first post-call credential scan
  (`remove_changed_credential`, right after the model call in the attempt
  loop) removes it and raises `Refused` before the time entry is computed.
  This completed, rejected attempt gets no runner entry; an in-memory run
  confirmed zero calls to `time_entry` (acceptance criterion 2 of that
  change).

## Where the attempt loop leaves after the call

Read in `scripts/stage2.py` at `8acaa8b` (the attempt loop around the
`time_entry` call):

1. the first credential scan after the call raises `Refused` (F-6, no entry);
2. `verify_attempt` raising `Refused` re-raises before the entry;
3. the credential scan after `make verify` records the problem and raises
   after the entry is written (already logged);
4. `cannot_start` (`make verify` could not be started) raises after the
   entry (already logged);
5. a failed model call (`CallFailed` before the post-call section) — the
   model did not complete; whether it owes an entry is for the spec to state.

## What the change has to do

Write the time line in one place that every post-call exit passes through,
so no completed attempt leaves without its entry, and keep the immediate stop
without fallback on a credential leak. One test per exit.

## Open questions

None for the maintainer: the direction is decided (`decisions.md`, Q-1).
