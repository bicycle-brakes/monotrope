---
title: "Decisions — verify-tmp-cleanup"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, make-verify]
---

# verify-tmp-cleanup — Decisions

Class: bounded (bead coding-harness-bxxt.3; one answered question or a
reasoned skip is owed — a skip below, written during the night run of
2026-11-10 and to be confirmed by the maintainer at the plan card).

## SKIP · interview

status: skipped
reason: A bounded fix whose intent the bead states in full — each run of the full check uses a base temporary folder of its own and removes it when it ends, green or red, also after an interrupt, and a red run keeps it only on request (bead coding-harness-bxxt.3, created on the maintainer's request of 2026-11-09 after the data volume ran full). What remains is mechanics, decided below with reasons; the plan card goes to the maintainer before anything is built.

## Decided by the agent

[DETAIL] **The gate command line stays as it is.** The folder is set through
the environment of the run, not by an option in `decisions/gates.yaml`.
Reason: the gate list is a held file and its command is pinned byte for byte
against the Makefile; the exploration found that pytest takes its temporary
root from the environment.

[DETAIL] **The removal sits where end-of-run work is already guaranteed**: the
supervised entry of the verify lock, which runs on a normal end, a red gate,
a cancel and a trapped signal. Reason: it is the one place in the tree that
provably runs in all four cases; a supervisor killed hard is outside it, as
its own boundary already states, and a later run removes what such a run
left behind.

[DETAIL] **"On request" is one environment variable set by the caller** for a
red run whose folder should stay; nothing is kept by default. Reason: the
bead asks for the request to be explicit, and a default that keeps red runs
is how the volume filled.

[DETAIL] **Scope is the runs that go through `scripts/verify_all.sh`** (the
full check and its job subsets). The runner's own targeted and cheap test
runs are named in the spec as covered or as a stated limit, whichever the
draft finds they share with that entry. Reason: the bead names the full
check; widening silently would be scope the maintainer has not seen.

[DETAIL] **No free-disk check is added here.** Reason: that is its own bead
(coding-harness-87b0).
