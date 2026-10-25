---
title: "Spec — interview-fenced-examples"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-k2r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, gate, interview-minimums]
class: bounded
appetite: 0.5
adr_files: []
---

# Spec — interview-fenced-examples

The interview-minimums gate reads no record or skip inside a fenced code
block, as the question-context gate already does (bead coding-harness-k2r).

## Acceptance criteria

1. A `## Q-n` record or a `## SKIP · interview` block inside a backtick or
   tilde fence (also a longer fence with an info string) is not counted.
   *Refuted by:* a fenced block in the parsed records or skips.
2. A record after a closed fence is counted with its fields.
   *Refuted by:* a missing record or field.

## Non-goals

- Share one fence helper across gate scripts (each travels alone in the kit).

## Definition of Done

- Tests red before the edit; the gate stays green on the repository.
- The last commit carries `Closes-Bead: coding-harness-k2r`.

## Open decisions

None open.

- [DETAIL] Blank fenced lines before the split instead of cutting them, so
  nothing else in the parser changes.
