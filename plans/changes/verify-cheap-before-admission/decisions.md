---
title: "Decisions — verify-cheap-before-admission"
category: decisions
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5.2, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verify, admission, gates, kit]
---

# verify-cheap-before-admission — Decisions

Class: bounded (bead coding-harness-bxxt.6).

## Q-1 · Which gates need the verify slot

asked: 2026-11-13
answer: "Slot nur für schwere Prüfungen (Empfohlen)" — the admission belongs to the gate, not to the whole run: a gate declared cost `minutes` needs the slot, a gate declared cost `seconds` never does; a seconds gate that writes shared state can be marked explicitly as needing the slot. The maintainer had asked for the most long-term solution before choosing.
answered_by: maintainer
status: answered
context: |
  Topic: `make verify` takes the admission to the one verify slot for the whole run and orders the gates cheap-first only afterwards.
  Intention: on 2026-11-13 a lane waited 710 s for the slot and then failed in seconds on a ruff row a merge of origin/main had caused.
  Today: 22 of 24 gates in decisions/gates.yaml are declared cost `seconds`; all of them wait behind the lock that protects CPU and memory for the two `minutes` gates.
  Repository change: scripts/verify_all.sh requests admission only for the gates that need it, derived from the cost class of the one gate list, with an explicit exception mark; the files travel in the kit.
  Architecture change: none; the one gate list stays the source, and the rule also holds with two slots.

In the context of a full check whose cheap gates wait behind the machine-wide lock, facing a choice between all seconds gates before admission derived from the cost class, an explicit field on every gate, and ruff alone, we decided that only the heavy gates take the slot, derived from the cost class with one explicit exception mark, to achieve that a cheap fault never costs the wait and a new gate is placed correctly by its cost, accepting that the spec must find any seconds gate that writes shared state. — 2026-11-13

## Q-2 · The seconds gates after admission

asked: 2026-11-13
answer: "Ergebnis übernehmen (Empfohlen)" — the result of the seconds gates counts when the tree is unchanged; when the tree changed during the wait they run again.
answered_by: maintainer
status: answered
context: |
  Topic: the seconds gates ran green before admission, then the run waits for the slot.
  Intention: decide whether the time in the slot is spent on them a second time.
  Today: every gate runs once, inside the lock.
  Repository change: the run keeps the pre-admission result and compares the tree before it relies on it.
  Architecture change: none.

In the context of seconds gates that ran before admission, facing a choice between reusing their result and running them again inside the slot, we decided to reuse the result for an unchanged tree, to achieve the shortest time in the slot, accepting a tree comparison after the wait. — 2026-11-13

## Q-3 · A red seconds gate

asked: 2026-11-13
answer: "Alle roten melden (Empfohlen)" — all seconds gates run through and every red one is reported at once; the run then ends without requesting admission.
answered_by: maintainer
status: answered
context: |
  Topic: a seconds gate is red before admission.
  Intention: one repair should be able to mend everything the cheap gates see.
  Today: the cheap-first order stops at the first red blocking gate (bead coding-harness-bxxt.1).
  Repository change: before admission the seconds gates all run; the report names every red one.
  Architecture change: none.

In the context of a red seconds gate before admission, facing a choice between stopping at the first red gate and running all seconds gates, we decided to run them all and report every red one, to achieve one repair per run instead of one per gate, accepting a few seconds more and a longer message. — 2026-11-13

## Q-4 · A check right after a merge of origin/main

asked: 2026-11-13
answer: "Nein, eine Stelle reicht (Empfohlen)" — no second mechanism after a merge of origin/main into a lane branch; the gates before admission are the one place.
answered_by: maintainer
status: answered
context: |
  Topic: the ruff row of 2026-11-13 came from a merge of origin/main after which nothing was checked.
  Intention: decide whether the merge path gets a check of its own.
  Today: no check runs after such a merge.
  Repository change: none beyond Q-1.
  Architecture change: none.

In the context of a fault that entered through an unchecked merge, facing a choice between a check after every merge and the one place before admission, we decided for the one place, to achieve one mechanism that covers merges, hand edits and runner attempts alike, accepting that the fault shows at the next start of the full check and not at the merge. — 2026-11-13

## Q-5 · A switch in kit repositories

asked: 2026-11-13
answer: "Kein Schalter (Empfohlen)" — the behaviour holds everywhere the kit carries the full check; no configuration value turns it off.
answered_by: maintainer
status: answered
context: |
  Topic: scripts/verify_all.sh, scripts/verify_lock.py and decisions/gates.yaml travel in the kit to the sibling repositories.
  Intention: the maintainer asked on 2026-11-13 that the kit carries the change.
  Today: the kit carries the full check as it is, with the lock around the whole run.
  Repository change: none beyond Q-1; no switch is added.
  Architecture change: none.

In the context of a change that travels in the kit, facing a choice between one behaviour everywhere and a configuration value per repository, we decided against a switch, to achieve one variant to test and explain, accepting that a repository cannot return to the old behaviour on its own. — 2026-11-13
