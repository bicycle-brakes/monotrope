---
title: "Decisions — status-fields-restore"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
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
