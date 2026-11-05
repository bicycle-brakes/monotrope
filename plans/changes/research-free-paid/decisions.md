---
title: "Decisions — research-free-paid"
category: decisions
status: draft
implementation_status: none
date: 2026-11-05
created: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-wb40
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm, free-selection]
---

# research-free-paid — Decisions

Class: feature (bead coding-harness-wb40; reclassified from bounded on 2026-11-05 when the maintainer chose one central free selection). Three interview answers below.

## Q-1 · Patch the research swarm's selection, or one central free selection

asked: 2026-11-05
answer: "A: eine zentrale Auswahl (Recommended)" — one function selects the free models (free rule, exclusions, a paid admission wins, the address check), and both the review loop and the research swarm call it; a test proves both select the same members for the same catalog.
answered_by: maintainer
status: answered
context: |
  Topic: two separate code paths select free models — the review loop (select_free and free_drops in scripts/stage2.py) and the research swarm (select_research_catalog in scripts/stage2_swarm.py).
  Intention: after PR #335 (Pi 1.5.0) the research swarm selects beam-free, admitted as paid, and prepare-explore refuses; the pi-catalog-move repair covered only the review loop although its plan named both (reproduced 2026-11-05).
  Today: every future rule for free models must be kept in two places.
  Repository change: one shared free-selection function used by both paths.
  Architecture change: one central place for the free selection, like go-access-point for the Go address.

In the context of two code paths that each select free models, facing a paid-admission rule that reached only one of them and a research swarm that no longer starts, we decided on one central free selection used by both, to achieve one place for every free-model rule, accepting a larger change while the swarm stays blocked. — 2026-11-05

## Q-2 · Phase 1 without the research swarm

asked: 2026-11-05
answer: "Was ist die nachhaltig Lösung, ich will sowas nicht anpassen müssen ständig" — the maintainer asked for the sustainable solution; the follow-up question Q-3 answered it, granting this one exception together with a contract test that prevents the next one.
answered_by: maintainer
status: answered
research_swarm_exception: {granted: true, reason: "the research swarm is blocked by exactly the fault this change repairs (2026-11-05)"}
context: |
  Topic: this feature change would explore through the research swarm (ADR 0020), but the swarm refuses because of the fault this change repairs.
  Intention: the research-handoff gate (bead coding-harness-in27, not yet merged) requires a granted exception for a feature change without a complete swarm run.
  Today: GLM 5.3 Flash's exploration exists (2026-11-05); go-access-point had the same situation on 2026-10-31.
  Repository change: the Flash research stands as phase 1.
  Architecture change: none.

In the context of a research swarm blocked by the fault this change repairs, facing a feature change that cannot research itself through the swarm, we decided to accept the Flash exploration once, to achieve the repair without a detour, accepting phase-1 research without the swarm's independent maps. — 2026-11-05

## Q-3 · The sustainable solution

asked: 2026-11-05
answer: "A: Ausnahme + zentral + Vertragstest (Recommended)" — one exception now (Q-2); the central free selection (Q-1); and a contract test that prepares both the review loop and the research swarm offline against the pinned Pi's shipped catalog, without a model call, so any Pi or catalog move that breaks either preparation turns red before its merge.
answered_by: maintainer
status: answered
context: |
  Topic: the Pi move to 1.5.0 broke the research swarm and no test noticed before the merge; the Pi contract tests cover only the review loop.
  Intention: the maintainer does not want such adjustments again and again.
  Today: a Pi or catalog move that breaks the swarm preparation is found only in operation, then needs an exception and hand work.
  Repository change: a contract test beside the Pi contract test that runs both preparations against the pinned Pi's catalog offline.
  Architecture change: a new contract test as part of this change.

In the context of a Pi move that broke the research swarm unseen, facing repeated exceptions and hand work after each such move, we decided to add an offline contract test over both preparations to this change, to achieve a red signal before the merge of any move that breaks them, accepting a larger change and a test tied to the pinned Pi's catalog. — 2026-11-05
