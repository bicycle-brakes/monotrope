---
title: "Decisions — isolated-attempts"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, isolation]
---

# Isolate each writing attempt — Decisions

Phase 1a for bead coding-harness-s9r, asked by the orchestrating Claude Code
session on 2026-10-14, each question with its context first (what it is
about, why, what happens today, what changes).

## Q-2 · Which runner verbs are isolated

asked: 2026-10-14
answer: the three automatic writing verbs (draft, implement, repair) and the interactive session verb as well.
answered_by: maintainer
status: answered

In the context of four verbs that let a model write — three automatic, one
interactive with the maintainer present — facing the choice between the
automatic three and all four, we decided on all four to achieve one boundary
for every model that writes, accepting a larger change and a less direct
interactive session. — 2026-10-14

## Q-3 · Whether reads are isolated too

asked: 2026-10-14
answer: yes — reads outside the change are confined as well, not only writes.
answered_by: maintainer
status: answered

In the context of Codex and the review models being able to read outside the
worktree (the residual risk ADR 0007 and ADR 0011 name), facing the choice
between confining writes only and confining reads too, we decided on reads
too to achieve that a model sees only what its call needs, accepting that
this practically requires operating-system isolation. — 2026-10-14
