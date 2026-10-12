---
title: "Decisions — stage2-format"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-52r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, stage2, formatting]
---

# Stage-2 runner formats the attempt — Decisions

Phase 1a for bead coding-harness-52r, on 2026-10-12. The work models have no
command tool, so every attempt in change stage2-repair failed `make verify` on
ruff's gates alone; the runner is to correct that itself before `make verify`.

## Q-1 · What the runner corrects before `make verify`

asked: 2026-10-12
answer: A — `ruff format` and `ruff check --fix` with ruff's safe fixes only, never `--unsafe-fixes`.
answered_by: maintainer
status: answered

In the context of attempts that fail only on the `ruff-format` and
`ruff-check` gates, facing the choice between formatting plus safe fixes,
formatting alone, and every fix including the unsafe ones, we decided on
formatting plus safe fixes to achieve that both gates seen failing in
change stage2-repair are caught by the runner, accepting that a lint finding
without a safe fix still fails the attempt. — 2026-10-12
