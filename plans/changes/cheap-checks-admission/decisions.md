---
title: "Decisions — cheap-checks-admission"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.13
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verify, load]
---

# cheap-checks-admission — Decisions

## Q-1 · Lock or worker cap for the runner's cheap checks and the targeted kit probe

asked: 2026-11-25
answer: "A — the targeted check keeps running outside the verify lock (the standing rule of 2026-10-30, bead coding-harness-24ag, is unchanged); the runner's cheap checks and the pytest the kit probe starts in a targeted run get the same worker cap the targeted pytest gets (targeted_pytest_env). Options put: A worker cap, lock rule unchanged (recommended); B the targeted run's kit probe under the verify lock (amends 24ag); C no kit probe in targeted runs, left to the full make verify before phase 6 (overlaps coding-harness-w2ay)."
answered_by: maintainer
status: answered
context: |
  Topic: how the runner's cheap checks and the targeted run's kit probe are bounded.
  Intention: stop unthrottled pytest -n auto runs outside the admission from loading an 8 GB machine.
  Today: cheap_checks runs pytest -n auto with no worker cap outside the admission (scripts/stage2.py 8599-8606), and a targeted run whose touched paths appear or vanish adds leerprobe (~200 s) through run_gates, also outside the admission.
  Repository change: scripts/stage2.py (cheap checks and the targeted kit probe get the targeted worker cap), its tests, docs/WORKFLOW.md where it describes the targeted check.
  Architecture change: none; the lock rule of 24ag stays.

In the context of runner checks that run outside the verify lock by design, facing unbounded pytest workers on an 8 GB machine, we decided to keep them outside the lock and cap their workers like the targeted pytest, to achieve lower machine load without changing the lock rule, accepting that a capped kit probe may take longer. — 2026-11-25
