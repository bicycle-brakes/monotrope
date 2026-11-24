---
title: "Design — isolated-writing-attempts"
category: design
created: 2026-11-24
status: draft
implementation_status: none
date: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [design, stage-2, attempts]
---

# Design — isolated-writing-attempts

## Alternatives

- Detached linked worktrees isolate changes cheaply but share Git and tool state, requiring checks and recovery.
- Containers also restrict network and foreign reads but add a heavier runtime and macOS setup.

Chosen: detached worktrees, as decided in Q-1 and Q-10; containers remain a later layer.

## Interfaces

The stage-2 runner passes its module and an attempt-specific context to the shared lifecycle. The lifecycle returns a checkpoint or failed state; the runner owns model policy, leak checks and records. No new public CLI is included.

## Data model

Worktrees reside beneath `${XDG_STATE_HOME:-~/.local/state}/coding-harness/attempts/`, with invocation and attempt identities. Code writes and validates JSON schemas for attempt records, process locks and the saved-state index; invalid state is not trusted. Failed states remain under `refs/stage2/attempts/<change>/`. Linked Python and Pi environments are checksummed; changes reject the attempt and trigger recovery. Lane records are exempt from the lane snapshot and are committed with the landing or by the orchestrator.

## ADR draft

`docs/adr/0026-isolated-writing-attempts.md` proposes the writing-only decision and partially supersedes ADR 0017 decision 2.

## Architecture delta

```mermaid
flowchart LR
  maintainer["Person: maintainer"] --> runner["Component: stage-2 runner"]
  runner --> lifecycle["Component: attempt lifecycle"]
  lifecycle --> attempt["Component: detached attempt worktree"]
  lifecycle --> state["Component: validated JSON state and attempt refs"]
  lifecycle --> lane["Component: lane checkpoint"]
```

**Added**

- A shared lifecycle, attempt worktrees and validated state.

**Changed**

- Writing verbs use one lifecycle; repair is isolated first, then draft and implement.
- Failed writing calls may continue through declared fallback routes.

**Removed**

- Separate model-attempt paths for the writing verbs.
