---
title: "Decisions — handoff-new-feature"
category: decisions
status: draft
implementation_status: none
date: 2026-11-04
created: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-in27
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-handoff, gate]
---

# handoff-new-feature — Decisions

Class: bounded (bead coding-harness-in27).

## Q-1 · How strict the gate is for a new change without a swarm run

asked: 2026-11-04
answer: "A: rot, mit benannter Ausnahme (Recommended)" — a feature or architectural change created after the research swarm's merge needs a complete swarm run, otherwise `research-handoff` is red; changes created before that stay exempt; an exception the maintainer grants in the change's interview, recorded with its reason, lets the change pass and is named in the gate's output.
answered_by: maintainer
status: answered
context: |
  Topic: the research-handoff gate reads a new feature change without swarm evidence as "exempt - legacy" (bead coding-harness-in27).
  Intention: the maintainer asked on 2026-11-04 how to be sure the swarm's results take effect; this gap lets a change skip the swarm unseen.
  Today: "legacy" is meant for changes from before the swarm; the boundary is not drawn by the change's creation date.
  Repository change: the gate turns red for a new feature/architectural change without a swarm run, unless an interview-granted exception is recorded.
  Architecture change: a stricter blocking gate.

In the context of a research-handoff gate that lets a new feature change without a swarm run pass as legacy, facing the maintainer's wish for certainty that research takes effect, we decided to make such a change red unless an interview-granted exception is recorded, to achieve a gate that cannot be skipped unseen, accepting one more interview answer where a change deliberately skips the swarm. — 2026-11-04

## Q-2 · The exposed go-access-point exception

asked: 2026-11-04
answer: "A: ja, nachtragen (Recommended)" — the maintainer confirmed the exception of 2026-10-31 for go-access-point and had the orchestrator record it in that change's decisions.md in the structured form, as Q-6.
answered_by: maintainer
status: answered
context: |
  Topic: the stricter gate named go-access-point, a feature change from 2026-10-31 explored without the research swarm, whose decisions.md states the maintainer's exception only in prose.
  Intention: the plan reported this dependency and left its normalisation as separate work; the full make verify stayed red on it.
  Today: the exception reads "by the maintainer's exception of 2026-10-31" at the head of that file.
  Repository change: one structured record (Q-6) in plans/changes/go-access-point/decisions.md, written by the orchestrator; this change's spec and plan name that one edit outside its folder.
  Architecture change: none.

In the context of a stricter gate that exposed a feature change whose swarm exception existed only in prose, facing a red verification that the plan forbade waiving silently, we decided that the orchestrator records the maintainer-confirmed exception in that change's decisions.md, to achieve a visible, structured grant and a green gate, accepting one edit outside this change's folder. — 2026-11-04

