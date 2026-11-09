---
title: "Decisions — status-fields-restore"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-ljmi
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, runner, repair]
---

# status-fields-restore — Decisions

Class: bounded (bead coding-harness-ljmi).

## SKIP · interview

status: skipped
reason: The maintainer decided the guarantee on 2026-11-03 (bead coding-harness-mwzv.1, recorded in bead coding-harness-ljmi): after every repair attempt the runner puts back the frontmatter fields `status` and `implementation_status` of the change's spec.md, design.md and plan.md and names that in its report; a sentence in the repair prompt says so; tests cover it; a finding that needs a status change is taken by the orchestrator by hand, not given to a model. Nothing is left for the maintainer to choose; the remaining details are [DETAIL] items the draft decides with its reasons.

## Q-1 · Who owns the header when a protected value changes

asked: 2026-11-08
answer: "Kopf gehört dem Runner (Recommended)" — the header belongs to the runner: when an attempt changes a protected lifecycle value, the whole header returns to its snapshot and the attempt's other header edits are discarded; derived header fields are the runner's to write (bead coding-harness-7ftj). The spec's criterion 3 is amended; no code change.
answered_by: maintainer
status: answered
context: |
  Topic: the phase-6 re-check of 2026-11-08 found R9 (BLOCKER, DIVERGENT): restoring the whole header also discards an attempt's edit of an unrelated field such as last_reviewed, while criterion 3 promised to keep it.
  Intention: end the series of YAML edge cases in this change without new code.
  Today: the runner restores the whole header from snapshot bytes when a protected value changes (repair of R6-R8).
  Repository change: criterion 3 of the spec states that the header belongs to the runner; docs/WORKFLOW.md already describes this behaviour.
  Architecture change: the header of spec, design and plan becomes runner-owned, in line with coding-harness-7ftj (formalities by the runner).

In the context of a whole-header restore that discards unrelated header edits, facing a choice between runner-owned headers and a field-level round-trip restore, we decided that the header belongs to the runner, to achieve a restore without edge cases and in line with formalities written by the runner, accepting that a model's header edit is lost whenever it also changes a protected value. — 2026-11-08
