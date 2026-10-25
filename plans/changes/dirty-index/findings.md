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

## Pre-review by an Opus 5.5 subagent, 2026-10-25

At the maintainer's request, a read-only Opus 5.5 subagent reviewed this
change before the phase-6 Codex review, which this container cannot reach.
Phase 6 is still owed. It found no blocker and one minor row, reproduced
and fixed by the orchestrating session.

- **P234-1 (MINOR), fixed.** `tests/test_stage2.py::test_changed_paths_lists_each_kind_once`,
  cited for criterion 4, could not fail: `changed_paths` returns a set, so
  "listed twice" holds by construction, and its only tracked path was also
  staged, so dropping the working-tree query left it green. It now changes a
  second tracked file in the working tree only and asserts the exact set.
  With the working-tree query replaced by an empty list, it fails.

## Review loop skipped, 2026-10-25

The review loop (phase 4b) did not run on this change. The maintainer
answered on 2026-10-25 (night-run plan, `docs/research/2026-10-25-night-run-plan.md`,
answer 1) that the small cloud-session fixes get phase 6 only tonight,
because each had the Opus 5.5 pre-review recorded above. Phase 6 follows in
a fresh Codex session.

Stage-2 call, 2026-10-25: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 552 files, 2089 commits, 12 rules.

## Phase 6 — Codex, 2026-10-25

Codex reported no finding.

The answer was not only six-cell rows; what is not one is kept below as it came.

No finding.

Phase 6 verdict: codex 01a174a8-d9aa-75c1-a1a6-728a5456059e, 2026-10-25
Reviewer session: codex 01a174a8-d9aa-75c1-a1a6-728a5456059e — a fresh session reviewed: no phase-2a session was recorded

Loop rows: none — the loop did not run for this change.
