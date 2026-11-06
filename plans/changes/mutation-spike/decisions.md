---
title: "Decisions — mutation-spike"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-bvy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, spike, mutation-testing]
---

# mutation-spike — Decisions

Class: spike (bead coding-harness-bvy).

## SKIP · interview

status: skipped
reason: The bead (coding-harness-bvy) fixes the three spike topics: the tool (a mutation tool such as mutmut, installed locally for the measurement, not added to the lock), the targets (scripts/check_research_handoff.py and scripts/stage2_availability.py, both densely tested) and the output (mutation score, surviving mutants by kind and run time, dated and bound to a commit, under docs/research/), with the explicit limit that nothing is added to make verify before the maintainer decides on the result. No open choice remains for the maintainer before the measurement.
