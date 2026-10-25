---
title: "Findings — dirty-index"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-0c8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — dirty-index

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25 (conversation):
Codex, GLM and OpenCode Go are unreachable there, so `stage2.py implement`
could not run. Red first: the four new test cases failed before the
production edit (`changed_paths` returned an empty set; `implement`
exited 0 and committed over the staged content); criterion 4's test passed
before and after, as a guard.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review; the review
loop and the phase-6 Codex review are still owed.

- Callers with `against=base` (the whole-change listing in the commit guard)
  now also list paths whose index differs from `base`; every such path
  already differs in the working tree or will be committed, so the listing
  gains no false entry in the runner's own flow.
- After the checkpoint's `git add -A`, index and working tree agree, so the
  post-commit cleanliness proof is unchanged.
