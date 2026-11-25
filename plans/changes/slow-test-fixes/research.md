---
title: "Research — slow-test-fixes"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.16
owner: Data Architect
provenance: human-written
tags: [research]
class: bounded
neighbours: []
---

# slow test fixes — Research

## Topic (bead coding-harness-bxxt.16, copied by the orchestrator 2026-11-25)

Class: bounded.

Why/What, each read at 18a13d3d: (1) tests/test_pi_contract.py:1268-1275
makes 14 real Pi calls, 5 identical baseline repeats -> drop the repeats.
(2) tests/test_stage2_research_catalog.py:936-938 waits a real
deadlineMs=10000 although held_collect (264-274) exists -> use it; the file
also has 66 cold node spawns via collect (185-261). (3)
tests/test_stage2_swarm.py:2489 finder sleep 5 -> a file barrier. (4)
tests/test_atomic_test_log.py:1087-1155 runs 24 nested pytest subprocesses,
12 with -n 2 -> bundle outcomes per (workers, drain). Related: coding-
harness-dca4, coding-harness-76sf, coding-harness-wnka.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp, night run 2026-11-24-a), from an external verify-speed analysis.



PARENT
↑ ○ coding-harness-bxxt: (EPIC) Verify speed and machine load P1

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
