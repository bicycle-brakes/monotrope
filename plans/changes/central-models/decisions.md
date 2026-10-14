---
title: "Decisions — central-models"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ylu
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, models, effort, routing]
---

# One central place for models and effort — Decisions

Phase 1a for bead coding-harness-ylu, asked by the orchestrating Claude Code
session on 2026-10-14, each question with its context first. The request,
the maintainer the same day: "insgesamt muss es einfacher werden, dass die
Modelle, die im Workflow genutzt werden, und deren Effort-Level geändert
werden".

## Q-1 · Where the one setting lives

asked: 2026-10-14
answer: in `model-endpoints.yaml`, in a new routes section — phase or verb to model, effort and fallback; the runner reads it and its route constants go.
answered_by: maintainer
status: answered

In the context of providers declared in `model-endpoints.yaml` and routes
written as constants in `scripts/stage2.py` and again in docs and prompts,
facing the choice between that file and a file of its own, we decided on
`model-endpoints.yaml` to achieve one file for who may see what and who does
what, accepting a larger file. — 2026-10-14

## Q-2 · How documents show the models

asked: 2026-10-14
answer: the model tables in `docs/WORKFLOW.md` are generated from the setting by a script and a gate checks they match; each prompt names only its route.
answered_by: maintainer
status: answered

In the context of model names and efforts repeated in tables and prompt
headers, facing the choice between a generated table with references and
references only, we decided on a generated table to achieve readable values
that cannot drift, accepting a generator and a gate. — 2026-10-14

## Q-3 · What a model change goes through

asked: 2026-10-14
answer: ADRs decide roles, not models; which model fills a role stands only in the setting, so a model or effort change is a one-line pull request the maintainer merges.
answered_by: maintainer
status: answered

In the context of ADRs that name concrete models, so that every change needs
an ADR amendment and five interview answers, facing the choice between roles
in ADRs and a decision pull request per change, we decided on roles to
achieve one-line changes, accepting an amendment of the ADRs that name models
today (at least 0007, 0011, 0016, 0017). — 2026-10-14

## Q-4 · What the setting steers

asked: 2026-10-14
answer: the runner's verbs, the models of Claude Code sub-agents, the ladders of the research swarm and the review swarm, and the default model proposed for an interactive session.
answered_by: maintainer
status: answered

In the context of models chosen by the runner, by a memory rule for
sub-agents, by swarm ladders and by hand in a session, facing the choice of
scope, we decided on all four to achieve one place for every model choice,
accepting that sub-agent and session defaults need a reader in each harness.
— 2026-10-14

## Q-5 · How the setting travels to other repositories

asked: 2026-10-14
answer: the form travels, the values stay per repository — the kit brings the format, the runner, the table generator and a template with defaults; each repository sets its own models and data clearances.
answered_by: maintainer
status: answered

In the context of a kit for other repositories and the vision of an extension
for many harnesses (bead coding-harness-25h), facing the choice between per
repository values and shared values, we decided on per repository values to
achieve that a repository with customer data never inherits a model it may
not use, accepting that a model change is made in each repository. —
2026-10-14
