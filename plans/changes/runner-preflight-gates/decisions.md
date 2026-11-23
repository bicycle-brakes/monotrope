---
title: "Decisions — runner-preflight-gates"
category: decisions
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, runner-preflight]
---

# runner-preflight-gates — Decisions

Class: bounded (bead coding-harness-yv9i.3).

## Q-1 · Build this layer now, as its own bounded change

asked: 2026-11-23
answer: 'A — two small bounded P1 beads beside coding-harness-7ftj (maintainer, 2026-11-23, dialog in session c820a13d); this one: before the first model call of draft, implement and repair the runner runs the fast document gates on the starting tree and refuses with the gate's fix command, spending no call.'
answered_by: maintainer
status: answered
context: |
  Topic: preventing the failure of 2026-11-23, when an orchestrator hand edit of plans/changes/isolated-attempts/decisions.md left updated: stale and a draft spent three model attempts on a starting tree no draft may change.
  Intention: the fault should not depend on the orchestrator's care.
  Today: the runner runs the document gates only after a model attempt; a red starting tree fails every attempt.
  Repository change: a preflight step in scripts/stage2.py before the first model call; tests with a fake model that records calls.
  Architecture change: none.

In the context of a stale document date that cost three model attempts, facing a choice between two bounded layers, one note in bead coding-harness-7ftj, or the hook layer alone, we decided on two bounded P1 changes, of which this is one, to achieve a fix that holds for every harness and saves model calls, accepting two small changes instead of one larger feature — 2026-11-23

## Provisional agent decisions on the spec review (2026-11-23, night run 2026-11-23-a)

Decided by the orchestrator by its recommendation, marked provisional; the plan card lists them for the maintainer.

- [DETAIL] **S-1 (provisional agent decision):** Reading B — the preflight refuses only for a blocking document gate whose failing file the attempt may not change (decisions.md, research.md, files outside the change folder, as the runner's draft_keep/held rules define); a gate the attempt can fix does not refuse.
- [DETAIL] **S-2 (provisional agent decision):** drop 'non-admitted' from the criterion; the selection is every gate with subsets [docs] that ci_gates.declared_cheap admits, and the criterion is refuted by a gate in that set that does not run.

- [DETAIL] **R-1 (provisional agent decision, night run 2026-11-23-a):** Reading B, as S-1 decided: the preflight refuses only for a red blocking document gate whose failing file the verb may not write (decisions.md, research.md and paths outside the change folder under the runner's keep/held rules); a fault the verb or the runner's own `prepare_derived` fixes (this change's findings.md, plans/INDEX.md) does not refuse. AC 2 and its refutation are rewritten to that reading; the spec's [DECISION] block is removed.
