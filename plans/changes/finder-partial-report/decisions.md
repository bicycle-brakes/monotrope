---
title: "Decisions — finder-partial-report"
category: decisions
status: draft
implementation_status: none
date: 2026-11-19
created: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-19
supersedes: null
superseded_by: null
bead: coding-harness-yd8w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm]
---

# finder-partial-report — Decisions

Class: bounded (bead coding-harness-yd8w; one answered question is owed —
Q-1 below, answered by the maintainer on 2026-11-19 in the conversation and
recorded in the bead's notes).

## Q-1 · What happens to a finder answer with malformed entries

asked: 2026-11-19
answer: "A: Retry + Rest behalten (Empf.)" — in English: the finder seat is asked once more with the exact validation error; if its second answer still fails, the runner keeps the valid locator entries, records the dropped ones as a gap in the run record, and the run continues; the requirement that every locator names a path and an exact symbol or section stays.
answered_by: maintainer
status: answered
context: |
  Topic: bead coding-harness-yd8w, the finder step of the research swarm.
  Intention: the trust-pyramid-swarm run could not run; finder seat 3 failed twice in two changes.
  Today: run 2277a0ed's finder answer from claude-haiku-5-5 was valid JSON with the four lists and 102 entries; 36 named a whole file without a reference. scripts/stage2_research_map.py validate_locator_report raises on the first such entry, scripts/stage2_research_run.py stage_finders voids the whole answer, and require_ok stops the run before any topic.
  Repository change: scripts/stage2_research_map.py, scripts/stage2_research_run.py and their tests.
  Architecture change: the finder step recovers before it refuses (the maintainer's rule of 2026-11-15: rules must reduce aborts).
  Options shown: A retry once, then keep the valid entries (recommended); B admit whole-file locators with a marker; C make seat 3 selectable on the command line; D rerun unchanged with Haiku.

In the context of a finder step that voids a whole answer for one malformed
entry, facing two aborted research runs, we decided to ask the seat once more
with the exact error and then keep the valid entries and record the rest as a
gap, to achieve a run that a form error no longer stops, accepting a map built
from fewer locators when a seat answers badly twice — 2026-11-19
