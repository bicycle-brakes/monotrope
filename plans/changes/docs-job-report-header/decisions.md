---
title: "Decisions — docs-job-report-header"
category: decisions
status: draft
implementation_status: none
date: 2026-11-02
created: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-ooj5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# docs-job-report-header — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; a skip
below).

## SKIP · interview

status: skipped
reason: A bounded bug fix whose one intent question the bead already answers — its title says the report step is forwarded the job "so its header names the document subset" (bead coding-harness-ooj5, filed 2026-10-31 from review-loop row L7-2 of bead coding-harness-77qj); the run plan of 2026-10-31 planned it for building, not for an interview. What remains is mechanics, decided below with reasons.

## Decided by the agent

[DETAIL] **A `--job docs` run's header names the subset and the subset's gate
count** (11 at origin/main 156aae08), not the verify job's 21. Reason: the
bead's title; the header should say what the run measured.

[DETAIL] **`verify_all.sh` forwards `--job "$JOB"` to the `--report` call.**
Reason: the explore found this the single caller (`scripts/verify_all.sh`,
the `--report` call) and `in_job` in `scripts/ci_gates.py` already answers
subset membership.

[DETAIL] **The JSON report keeps its field names**; `gates_job` holds the
subset's count under `--job docs`, and `gates_total` stays job-independent.
Reason: no reader outside the code documents the fields (the explore's search
over `docs/` found none), so keeping the names breaks nothing; a new field
would need a reader first.

[DETAIL] **A test pins the header for both jobs.** Reason: the report fields
are unpinned today (the explore found no `gates_job` assertion), which is how
the asymmetry went unnoticed.

[DETAIL] **The German `report()` docstring stays as it is.** Reason: house
rule 1 translates German in pull requests of its own (bead
coding-harness-yim), never in passing.
