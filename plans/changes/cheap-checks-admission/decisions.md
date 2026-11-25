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

## Details decided by the orchestrator

[DETAIL] **D-1 (spec review S-1, the kit probe is serial)**: the kit probe's pytest runs without `-n`, so it is one serial process and needs no worker cap; criterion 2 becomes a check that the probe stays serial (no `-n` in its pytest command), and the cap applies to the runner's cheap-check pytest only. Reason: measured in scripts/kit/probe.py 455-464; capping a serial run changes nothing (Q-1 stays: no lock change).

[DETAIL] **D-2 (S-2, where the worker number comes from)**: `cheap_checks` computes its worker number with the same function the targeted pytest uses (`targeted_pytest_env`), independent of what the caller's environment carries; the ENV_ALLOW gap for `PYTEST_XDIST_AUTO_NUM_WORKERS` stays with coding-harness-9bv1. Reason: no runner caller supplies the variable today, so a caller-supplied setting would never apply.

[DETAIL] **D-3 (S-3, both call sites)**: criterion 1 covers both `cheap_checks` call sites — the targeted check's body and the full-mode preparation. Reason: both start the same unthrottled pytest.

[DETAIL] **D-4 (S-4, scope of the policy)**: only pytest launches of the cheap checks get the cap; `run_gates`, its other gates and its other callers (the draft's and the hand-off's document checks) are unchanged. Reason: the other gates are not pytest and are not the load the bead names.

[DETAIL] **D-5 (spec review round 2 S-5, the setting stays local)**: placement A — the computed worker setting is applied only to the cheap pytest launch, inside `cheap_checks` (a copy of the environment), and never written back into the environment the caller passes on to later steps, gates or the full verify. Reason: D-4 limits the policy to the cheap pytest.

