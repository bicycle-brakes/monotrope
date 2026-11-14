---
title: "Decisions — verify-cheap-first"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-11
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

## Q-2 · Whether the change may correct texts the early stop makes false

asked: 2026-11-11
answer: Widen the scope — plan and spec allow correcting false texts about `make verify` without any behaviour change in the runner.
answered_by: maintainer
status: answered
context: |
  Topic: the change edits two files its own plan excludes.
  Intention: review round 3 (row L3-1) found that the change edits the `run_targeted` docstring in scripts/stage2.py and the local-run line of prompts/05-verify.md, both out of the plan's scope; round 2 had shown that both would state something false after the change.
  Today: two text-only edits outside the planned scope, on the branch.
  Repository change: plan and spec name the two text corrections as an allowed consequence, or the two edits are withdrawn into a follow-up bead.
  Architecture change: none.

In the context of a change whose early stop makes two texts outside its
scope false, facing a plan that forbids editing scripts/stage2.py and
workflow prompts, we decided that the change corrects those two texts by
text only, to achieve that no false statement about `make verify` is
merged, accepting that the scope grows after the fact by two files, one of
them held — 2026-11-11

## Decided by the agent

[DETAIL] **The local run names the gates it did not run** after an early
stop, so nobody reads a short red run as a complete one. Reason: the bead
asks for it, and the repair diagnosis of the runner reads red sections only.

[DETAIL] **Report and advisory gates never stop a run**, wherever the sort
places them. Reason: that is their meaning today. Corrected 2026-11-11 (loop
row L3-2): one that sorts behind the first blocking failure is not run and is
named in the not-run summary; the stop is the maintainer's decision Q-1, so
order is not the only change.

[DETAIL] **The held files are the orchestrator's step** (`decisions/gates.yaml`,
the regenerated `.github/workflows/ci.yml`); the implement attempt works
against synthetic gate lists in its tests. Reason: an attempt may not edit a
held path, and the change decision-statement-skeleton lost three attempts on
a ledger that named tests depending on one.
