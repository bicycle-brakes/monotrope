---
title: "Research — explore-role"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-e7m
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, explore]
---

# explore-role — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `f8a6b33`
(2026-10-25).

## The finding

On 2026-10-20 (change `review-loop-row-ids`), `stage2.py explore <change>
--stage2-off "GLM unavailable …"` ran `claude-haiku-5-5`. The model
answered that it could not run phase 1 because "the Bash tool is disabled"
and that `stage2.py explore` had to be run through it: it took itself for
the orchestrator. The runner appended that answer to `research.md` as
research (bead coding-harness-e7m).

## What exists today

Read in `scripts/stage2.py` at `f8a6b33`:

- `explore` routes to Haiku 5.5 under `--stage2-off`, GLM 5.3 Flash
  otherwise; the call has read-only tools (Read, Grep, Glob).
- The runner's own prompt addition says to report repository facts with
  source paths; it does not say who the model is or which tools it has.
- Any non-empty answer is appended under `## Runner exploration`.

Constraints read in `provenance.yaml`: `prompts/` is `human-written`
only, so the phase prompt is not this change's to edit. The Haiku route
for `--stage2-off` stands in `AGENTS.md` and `docs/WORKFLOW.md` §3 as a
model assignment.

## Options

1. Route `--stage2-off` explore to Sonnet 5.5: changes a documented model
   assignment, the maintainer's call (beads coding-harness-ylu,
   coding-harness-f44 own phase routing).
2. State the model's role and its read-only tools in the runner's own
   prompt addition (the bead's alternative), and fail an answer that is
   no research instead of appending it.

Option 2 needs no routing decision and also guards the GLM route.

## Sources

- Bead coding-harness-e7m.
- `scripts/stage2.py` `explore`; `provenance.yaml` (`prompts/`).
