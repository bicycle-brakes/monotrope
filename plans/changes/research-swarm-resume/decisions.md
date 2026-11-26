---
title: "Decisions — research-swarm-resume"
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-f6qj
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: antigravity, version: "Gemini 4 Neon High, 2026-11-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm, resume]
---

# research-swarm-resume — Decisions

Phase-1a direction recorded from the maintainer's explicit requirement (2026-11-25, bead `coding-harness-f6qj` and handover PR #464).

## Q-1 · Scope of the repository-topic resume fix

asked: 2026-11-25
answer: "Fix why repository topic slots (topics 1–8) get a different prompt hash between consecutive runs with an unchanged selection and tree (while finders, merge, sentence and online topics 9–11 reuse cleanly), making repository topic prompts depend only on the frozen inputs so an aborted research swarm reuses every finished repository topic slot and only re-runs failed slots."
answered_by: maintainer
status: answered
context: |
  Topic: repository topic prompt stability across resumed research-swarm runs (bead coding-harness-f6qj, class bounded).
  Intention: stop recomputing all 24 repository topic slots whenever a single seat fails or times out (measured on artcraft-autocraft runs 3–4 and pi-work-route runs 1–3; raised to P1 by the maintainer on 2026-11-25 for the 72-hour run).
  Today: Store.resume_source and plan_reuse reuse finders, merge, sentence and online topics 9–11, but every repository topic slot 1–8 appears in not_reused with reason 'prompt' on a resumed run with the identical selection and tree.
  Repository change: identify the non-frozen input entering repository topic prompts in scripts/stage2_research_run.py / stage2_research_prompts.py (or related swarm modules), make repository topic prompts depend strictly on frozen inputs (no per-run id, timestamp, non-frozen research.md growth or changing commit count), and add a regression test running a swarm twice with one failed repository topic slot in run 1 and asserting every other repository topic slot is reused in run 2.
  Architecture change: none (bounded bug fix preserving the existing frozen-binding resume contract in docs/WORKFLOW.md Q-13).

In the context of resumed research-swarm runs recomputing all 24 repository topic slots due to prompt-hash drift, facing repeated full-swarm restarts on any single transient seat failure, we decided to eliminate non-frozen inputs from repository topic prompts and pin reuse with a two-run regression test, to achieve true slot-level resume on repository topics, accepting no relaxation of the frozen-binding or prompt-hash integrity checks. — 2026-11-26
