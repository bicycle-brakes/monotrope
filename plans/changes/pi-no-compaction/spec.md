---
title: "Spec — pi-no-compaction"
status: draft
implementation_status: partial
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, runner, pi]
class: bounded
appetite: 1
adr_files: []
neighbours: []
---

# Spec — pi-no-compaction

The runner disables automatic context summarisation in every Pi settings file
it already writes, so a context overflow fails the member instead of allowing
a review based on a summary (bead coding-harness-mwzv.2 — disable Pi compaction).
Research: `research.md`. Scope: `decisions.md`, reasoned interview skip.

## Problem

At baseline `8a7ada25`, read 2026-11-06, the runner writes only
`{"retry": {"enabled": false}}` into its scratch Pi settings. Pi enables
automatic compaction by default. The five writes are the catalog refresh,
its listing copy, review members, research members and availability probes
(`research.md`, “Where the runner writes Pi settings files today”).

The measurement on 2026-11-03 found that Pi 1.2.0 with compaction enabled
summarises and retries after a provider context overflow; disabled compaction
instead yields one request and a text-mode failure which the runner refuses.
The worktree pins Pi 1.5.0, whose installed source still gates compaction on
the same setting, but its overflow behaviour has not been re-measured
(`research.md`, “The measurement behind the change” and “What is unclear
about it”; `docs/research/2026-11-03-pi-context-overflow.md`).

## Terms

**Compaction:** Pi's automatic shortening of conversation history, including
threshold checks and provider-overflow recovery; manual `/compact` is separate.

**Runner settings:** the scratch agent-directory `settings.json` files the
runner already creates or copies, not a user's or project's Pi configuration.

## Acceptance criteria

1. When the runner creates or copies a Pi settings file for catalog refresh,
   catalog listing, review members, research members or availability probes,
   its parsed content is `{"retry": {"enabled": false}, "compaction": {"enabled": false}}`.
   *Refuted by:* any of these five paths omits compaction, enables either
   retry or compaction, or uses a non-boolean value.

2. When the pinned Pi 1.5.0 receives a provider context-overflow error during
   a runner review call, the member fails through the existing `CallFailed`
   path after the rejected request, without a summary request or recovery retry.
   *Refuted by:* a second provider request, a successful or empty accepted
   answer, a zero text-mode process exit, or failure to raise `CallFailed`.

## Non-goals

- Changing `REVIEW_DIFF_MAX_LINES = 2000`, existing splitting/cut handling,
  or deriving limits from model context windows; the bound remains a cost
  and attention limit.
- Changing text output mode, retries, model admission, routing, failure kinds
  or review-loop completion rules.
- Configuring interactive Terminal sessions that currently write no settings
  file, user-home settings or project `.pi/settings.json`.
- Paid-provider measurements, exhaustive provider error compatibility, or a
  separate measurement of threshold compaction and overflow from tool reads.
- Moving the Pi pin, changing general catalog contracts, or changing doctrine.

This bounded change has no design phase or ADR draft: it changes existing
per-call settings and verifies their runtime effect without changing boundaries.

## Protected areas

- `scripts/stage2_session.py` and personal settings: the interactive route
  creates no settings file and is outside the recorded scope.
- `tools/pi/package.json`, `tools/pi/package-lock.json`, the wrapper and
  installer: the already pinned runtime is the subject of the re-check.
- Governance, ADRs, prompts, templates, agent configuration and CI: no policy
  or architecture change is required.

## Definition of Done

- `make verify` passes, including the settings assertions and real-Pi offline
  overflow contract; evidence names its tested commit and installed version.
- The comment above `REVIEW_DIFF_MAX_LINES` explains the retained bound as a
  cost/attention limit without claiming that runner compaction is still enabled.
- No other document, model declaration or ADR needs to move with the code.
- The pull request's file list shows the protected areas untouched and the
  non-goals unbuilt.
- The pull request closes the Pi-compaction work item and its last commit
  carries `Closes-Bead: coding-harness-mwzv.2`.
- Special runs: the offline Pi 1.5.0 overflow contract, with its tested commit
  in the pull request body; no live model call is required.

## Open decisions

None open.

- [DETAIL] Include discovery and its listing copy even though they run no
  agent turn: this keeps every existing runner-written settings file identical.
- [DETAIL] Re-check overflow through the existing loopback contract harness
  and synthetic credentials: this exercises the installed runtime without
  provider cost or transmitting repository content.
- [DETAIL] Update the nearby bound comment because its present explanation
  would otherwise contradict the disabled setting; retain historical research.
- [DETAIL] Use a one-hour phase-4 appetite, repairs included, because this is
  a local settings change with existing test seams; stop and return evidence
  if the runtime contract requires a broader repair.
