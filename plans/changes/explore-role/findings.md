---
title: "Findings — explore-role"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-e7m
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — explore-role

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: the
three new test cases failed before the edit. Six existing tests whose
stand-in answers named no path ("A sourced fact.", "a fact", …) now name
`src/app.py`; their assertions are unchanged.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- The path check resolves each candidate inside the worktree and ignores
  the root itself, `.` and `..`, so a path that climbs out does not count.
- The answer shown on standard error comes from `run_work_model`, which
  scrubs it like every relayed stream.
- Risk: research that cites only symbols and no path now fails. The
  phase prompt asks for source paths, so such an answer already misses
  the prompt's form.
