---
title: "Research — codex-drafts"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-rhq
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, codex, spec, plan]
---

# Codex drafts spec and plan — Research

Phase 1 for bead coding-harness-rhq, read against `origin/main` on
2026-10-12. Candidate 2 of the research of bead coding-harness-nsm
(`plans/changes/codex-takeover/research.md`): phases 2 (Spec), 2b (Design)
and 3 (Plan) are drafted by Codex instead of Opus 5.5, to save Claude tokens.
So that Codex does not review what it drafted, a Claude model becomes the
stage-2 reviewer of the spec (phase 2a). The maintainer has answered the
first interview question already (2026-10-12, recorded on the bead): a Claude
model takes over phase 2a only; Codex stays the phase-6 code reviewer, since
the code comes from GLM and Codex reviews nothing of its own there.

## Questions for the exploration

1. How `scripts/stage2.py` calls Codex today (`run_codex`, `spec-review`,
   `review`, the `session` verb of ADR 0012): which tools and sandbox it
   grants, whether any call can write files, how the 2a session is recorded
   and resumed in phase 6, and which tests pin that.
2. How phases 2, 2b and 3 run today: the `spec-planner` agent definition
   (`.claude/agents/`), `prompts/02-spec.md`, `prompts/02b-design.md`,
   `prompts/03-plan.md`, their `Model` lines, the validators and gates a
   draft must pass, and the ADR-answer step (`scripts/harness.py decide adr`)
   that runs inside phase 2.
3. Where the routing of phases to models is written: `docs/WORKFLOW.md`
   sections 3 and 4, `model-endpoints.yaml`, ADR 0007, ADR 0011, ADR 0012,
   and `AGENTS.md`; which tests pin the routing text.
4. What a Claude reviewer for phase 2a would need: how `spec-review` builds
   its prompt and writes its rows, what `prompts/02a-spec-review.md` (or its
   equivalent) asks, and how an orchestrator could check a Codex draft before
   the review (the gates in `make verify` that read `spec.md`, `design.md`
   and `plan.md`).
