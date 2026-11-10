---
title: "Decisions — verify-cheap-first"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, make-verify, gates]
---

# verify-cheap-first — Decisions

Class: bounded (bead coding-harness-bxxt.1). One answered question is owed;
the maintainer answered it in the orchestrating conversation on 2026-11-10 by
dialog choice, after stating in the same dialog: "Ich brauche eine dauerhaft
Umsetzung die dann auch im Kit funktioniert" — a lasting implementation that
also works in the kit.

## Q-1 · Where the order of the gates is declared

asked: 2026-11-10
answer: Cost field — every gate of the one list declares its cost class (seconds or minutes) in a required field; the mechanism orders a local run itself, seconds gates first, then minutes gates, and ends the run at the first red blocking gate; the schema check refuses a list without the field; hosted CI keeps running every gate.
answered_by: maintainer
status: answered
context: |
  Topic: a lasting way to fix the order of the gates that also works in the kit.
  Intention: the full check should fail fast when a gate of seconds is red, in every repository that receives the workflow through the kit.
  Today: the gate list decisions/gates.yaml and the scripts ci_gates.py and verify_all.sh all travel with the kit (scripts/kit/manifest.yaml). The order follows only from the position in the list; the test gate runs first (81 % of a run) and a run does not stop at a failure. An expensive gate inserted higher up would undo the gain unseen.
  Repository change: a required cost field per gate; the mechanism sorts locally and stops at the first red blocking gate, naming the gates it did not run; the schema check refuses a list without the field.
  Architecture change: the schema of the gate list gets a new field (version 3). decisions/gates.yaml is a held file, so the change arrives as a decision pull request the maintainer merges.

In the context of the order in which a local full check runs its gates,
facing an order that follows only from the position in the gate list and
would silently decay in any repository of the kit, we decided that every gate
declares its cost class in a required field and that the mechanism sorts
seconds gates before minutes gates and stops at the first red blocking gate,
to achieve a fast failure that holds in every repository the kit reaches,
accepting that the change is larger than re-sorting the list — schema
version, every list entry, the generated CI file and the gate catalogue
change, and target repositories must add the field at their next kit update
— 2026-11-10

## Decided by the agent

[DETAIL] **The local run names the gates it did not run** after an early
stop, so nobody reads a short red run as a complete one. Reason: the bead
asks for it, and the repair diagnosis of the runner reads red sections only.

[DETAIL] **Report and advisory gates never stop a run**, wherever the sort
places them. Reason: that is their meaning today; only the order changes.

[DETAIL] **The held files are the orchestrator's step** (`decisions/gates.yaml`,
the regenerated `.github/workflows/ci.yml`); the implement attempt works
against synthetic gate lists in its tests. Reason: an attempt may not edit a
held path, and the change decision-statement-skeleton lost three attempts on
a ledger that named tests depending on one.
