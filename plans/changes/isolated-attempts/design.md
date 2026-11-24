---
title: "Design — isolated-attempts"
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

# Design — isolated-attempts

## Alternatives

- Linked detached worktrees: cheap local attempts, with shared Git state and explicit protection of lane inputs and tools.
- Containers: stronger isolation of network and foreign reads, but a heavier runtime and macOS setup.

Chosen: worktrees, as the maintainer decided in Q-1 and Q-10; containers remain a later layer.

## Interfaces

The runner passes its module and attempt context to `scripts/stage2_attempts.py`; its command-line entry offers other harnesses lifecycle operations only; each harness owns model execution and its policies. The lifecycle returns an accepted result or a recorded failed state to the lane; the runner alone applies a checkpoint after verifying the lane HEAD.

## Data model

Attempt worktrees live under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/attempts/`, named with invocation and attempt identity, with a process-id lock for orphan pruning. Failed states are Git refs under `refs/stage2/attempts/<change>/`; post-merge cleanup owns deletion. The lane's Python environment and Pi are permission-protected and both checksummed before and after each attempt; tampering is detected rather than prevented. A mismatch rebuilds Python and reinstalls Pi, and an ineffective restoration stops the run. Findings record route switches and reasons.

## ADR draft

The existing proposed decision is `docs/adr/0026-isolated-attempts.md`; it partially supersedes ADR 0017 decision 2 upon merge. Its text must be aligned with decisions Q-17 through Q-21 by the orchestrator before the decision pull request.

## Architecture delta

```mermaid
flowchart LR
  user["Person: maintainer or harness"] --> runner["Component: stage-2 runner"]
  user --> attempts["Component: attempt lifecycle"]
  runner --> attempts
  attempts --> worktree["Component: detached attempt worktree"]
  attempts --> refs["Component: attempt refs"]
  attempts --> lane["Component: lane checkpoint"]
```

**Added**
- A protected, reusable attempt lifecycle and its direct entry; detached worktrees and retained refs.

**Changed**
- Implement, repair, draft and phase-6 review use the lifecycle; repair is isolated first, the others only after the qualifying night. Spec-review and review-loop remain outside.
- Post-merge cleanup removes the merged change's refs.

**Removed**
- Separate attempt paths for the covered verbs; unconditional stop on a writing call failure.
