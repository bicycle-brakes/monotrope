---
title: "Interview preparation — artcraft-autocraft"
class: feature
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-68kr
owner: Data Architect
provenance: ai-drafted-reviewed
review: {status: pending, approved_by: null, approved_at: null}
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-26"}
tags: [decisions, interview]
---

# artcraft autocraft — Interview preparation

Phase 1a. Two complete research-swarm runs bind this change: `e7be7d272599ab4091231773cd532193` (short e7be7d27, 82 obligation items; its online topics are off-brief because research.md held no brief then) and `cfcbfc1afaed5cc8504b4b9d95cd7350` (short cfcbfc1a, 79 items, run with the Brief). The 161 items are sorted into seven questions; each question's record closes the items listed under it. The sorting was checked mechanically: every item is assigned exactly once.

## Q-1 · Class: keep feature, or re-declare spike or architectural?

research_items:
  - e7be7d272599ab4091231773cd532193/H-20
  - e7be7d272599ab4091231773cd532193/H-25
  - e7be7d272599ab4091231773cd532193/H-28
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-23
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-27
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-32
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-73
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-78

## Q-2 · Scope: which AutoCraft practices does this change build (failure-count breaker, per-step cost in the event log, human review by area), and which does it leave (multi-repository ingest, release jobs, post-training, Rust)?

research_items:
  - e7be7d272599ab4091231773cd532193/H-2
  - e7be7d272599ab4091231773cd532193/H-3
  - e7be7d272599ab4091231773cd532193/H-5
  - e7be7d272599ab4091231773cd532193/H-6
  - e7be7d272599ab4091231773cd532193/H-32
  - e7be7d272599ab4091231773cd532193/H-33
  - e7be7d272599ab4091231773cd532193/H-35
  - e7be7d272599ab4091231773cd532193/H-36
  - e7be7d272599ab4091231773cd532193/H-37
  - e7be7d272599ab4091231773cd532193/H-43
  - e7be7d272599ab4091231773cd532193/H-70
  - e7be7d272599ab4091231773cd532193/H-71
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-1
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-2
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-3
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-4
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-6
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-8
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-19
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-31
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-36
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-38
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-40
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-41
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-58
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-69
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-70
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-75
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-76

## Q-3 · Boards and dashboards: does the night-runs-stay-plain rule stand for every candidate drawn from the talk?

research_items:
  - e7be7d272599ab4091231773cd532193/H-4
  - e7be7d272599ab4091231773cd532193/H-34
  - e7be7d272599ab4091231773cd532193/H-39
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-5
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-7
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-26
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-30
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-34
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-35
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-39
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-42

## Q-4 · ADR: does this change claim an ADR, and if so which number?

research_items:
  - e7be7d272599ab4091231773cd532193/H-21
  - e7be7d272599ab4091231773cd532193/H-22
  - e7be7d272599ab4091231773cd532193/H-26
  - e7be7d272599ab4091231773cd532193/H-27
  - e7be7d272599ab4091231773cd532193/H-29
  - e7be7d272599ab4091231773cd532193/H-74
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-24
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-28
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-29
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-33

## Q-5 · Neighbours: which suggested neighbour specs does the spec header keep or drop?

research_items:
  - e7be7d272599ab4091231773cd532193/H-23
  - e7be7d272599ab4091231773cd532193/H-40
  - e7be7d272599ab4091231773cd532193/H-41
  - e7be7d272599ab4091231773cd532193/H-42
  - e7be7d272599ab4091231773cd532193/H-44
  - e7be7d272599ab4091231773cd532193/H-45
  - e7be7d272599ab4091231773cd532193/H-46
  - e7be7d272599ab4091231773cd532193/H-75
  - e7be7d272599ab4091231773cd532193/H-76
  - e7be7d272599ab4091231773cd532193/H-78
  - e7be7d272599ab4091231773cd532193/H-79
  - e7be7d272599ab4091231773cd532193/H-80
  - e7be7d272599ab4091231773cd532193/H-81
  - e7be7d272599ab4091231773cd532193/H-82
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-43
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-45
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-46
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-49

## Q-6 · Evidence: does the spec rest on run cfcbfc1a with its thin online evidence, with run e7be7d27 (off-brief) and the source note as they stand, without a further run?

research_items:
  - e7be7d272599ab4091231773cd532193/H-1
  - e7be7d272599ab4091231773cd532193/H-7
  - e7be7d272599ab4091231773cd532193/H-8
  - e7be7d272599ab4091231773cd532193/H-9
  - e7be7d272599ab4091231773cd532193/H-10
  - e7be7d272599ab4091231773cd532193/H-11
  - e7be7d272599ab4091231773cd532193/H-12
  - e7be7d272599ab4091231773cd532193/H-13
  - e7be7d272599ab4091231773cd532193/H-14
  - e7be7d272599ab4091231773cd532193/H-15
  - e7be7d272599ab4091231773cd532193/H-30
  - e7be7d272599ab4091231773cd532193/H-31
  - e7be7d272599ab4091231773cd532193/H-38
  - e7be7d272599ab4091231773cd532193/H-52
  - e7be7d272599ab4091231773cd532193/H-55
  - e7be7d272599ab4091231773cd532193/H-57
  - e7be7d272599ab4091231773cd532193/H-60
  - e7be7d272599ab4091231773cd532193/H-63
  - e7be7d272599ab4091231773cd532193/H-65
  - e7be7d272599ab4091231773cd532193/H-66
  - e7be7d272599ab4091231773cd532193/H-67
  - e7be7d272599ab4091231773cd532193/H-68
  - e7be7d272599ab4091231773cd532193/H-69
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-9
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-10
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-11
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-12
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-13
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-14
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-15
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-16
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-17
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-57
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-59
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-61
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-71
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-72
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-77

## Q-7 · Swarm machinery and repository housekeeping raised by the seats: out of scope here, handed to the tracker writer as separate proposals?

research_items:
  - e7be7d272599ab4091231773cd532193/H-16
  - e7be7d272599ab4091231773cd532193/H-17
  - e7be7d272599ab4091231773cd532193/H-18
  - e7be7d272599ab4091231773cd532193/H-19
  - e7be7d272599ab4091231773cd532193/H-24
  - e7be7d272599ab4091231773cd532193/H-47
  - e7be7d272599ab4091231773cd532193/H-48
  - e7be7d272599ab4091231773cd532193/H-49
  - e7be7d272599ab4091231773cd532193/H-50
  - e7be7d272599ab4091231773cd532193/H-51
  - e7be7d272599ab4091231773cd532193/H-53
  - e7be7d272599ab4091231773cd532193/H-54
  - e7be7d272599ab4091231773cd532193/H-56
  - e7be7d272599ab4091231773cd532193/H-58
  - e7be7d272599ab4091231773cd532193/H-59
  - e7be7d272599ab4091231773cd532193/H-61
  - e7be7d272599ab4091231773cd532193/H-62
  - e7be7d272599ab4091231773cd532193/H-64
  - e7be7d272599ab4091231773cd532193/H-72
  - e7be7d272599ab4091231773cd532193/H-73
  - e7be7d272599ab4091231773cd532193/H-77
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-18
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-20
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-21
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-22
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-25
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-37
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-44
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-47
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-48
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-50
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-51
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-52
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-53
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-54
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-55
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-56
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-60
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-62
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-63
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-64
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-65
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-66
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-67
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-68
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-74
  - cfcbfc1afaed5cc8504b4b9d95cd7350/H-79
