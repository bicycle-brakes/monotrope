---
title: "Research — standin-call-counter"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.14
owner: Data Architect
provenance: human-written
tags: [research]
class: bounded
neighbours: []
---

# standin call counter — Research

## Topic (bead coding-harness-bxxt.14, copied by the orchestrator 2026-11-25)

Class: bounded.

Why: tests/test_stage2_swarm.py stand-in (297, 345) reads all records
through read_records (tests/atomic_test_log.py:106-125: flock plus
json.loads per line) only to count earlier calls with the same key; the log
grows with prompts, so cost grows quadratically per test. (The
test_stage2.py stand-in, 194-230, uses the records for step assignment, not
only counting.) What: a small per-key counter beside the log for the swarm
stand-in.

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
