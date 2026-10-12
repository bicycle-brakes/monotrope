---
title: "Decisions — adr-owning-change"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-afa
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, gates, adr]
---

# ADR owning change — Decisions

Phase 1a for bead coding-harness-afa, on 2026-10-12. The gate
interview-minimums infers an ADR's owning change from the diff; pull request
#126 carries an interim rule for that inference (a folder touched through
`plan.md` alone is no owner; beside other owners the ADR text decides). This
change replaces the inference with an explicit statement.

## Q-1 · Where the owning change is stated

asked: 2026-10-12
answer: A — the change claims the ADR files it creates or changes in its own spec header.
answered_by: maintainer
status: answered

In the context of an ADR edit that must be attributed to exactly one change
folder, facing that `owner:` in an ADR header already names a role and that
the answer-file format (schema_version 1) is frozen "not now", we decided that
a change names the ADR files it creates or changes in the header of its own
`spec.md`, to achieve an attribution that holds per edit — a later change that
amends an ADR claims that amendment itself — without touching the ADR or the
answer-file format, accepting that the claim lives in the change folder, not
in the ADR a reader opens. — 2026-10-12

## Q-2 · An ADR edit no change claims

asked: 2026-10-12
answer: A — the gate blocks and names the remedy; the inference from the diff goes, the interim rule of pull request #126 with it.
answered_by: maintainer
status: answered

In the context of a diff that changes a file under `docs/adr/` which no
change's spec header claims, facing the choice between one explicit rule and
the explicit rule beside the old inference, we decided that the gate reports a
finding that names the remedy (claim the file in the spec header of your
change) and no longer infers an owner from the diff, to achieve one rule
instead of two, accepting that even a typo fix in an ADR needs a change folder
with a spec — which the five-question duty for every ADR edit already asks
today. — 2026-10-12
