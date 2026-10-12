---
title: "Research — stage2-repair"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-g2f
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, review-loop, repair]
---

# Stage-2 repair verb — Research

Phase 1 for bead coding-harness-g2f, read against `origin/main` on
2026-10-12. Today the review findings the orchestrator takes — loop rows of
phase 4b marked `taken`, and open phase-6 findings — are repaired by a Claude
Sonnet sub-agent, which costs Claude tokens. The bead asks for a runner verb
(for example `python3 scripts/stage2.py repair <change>`) that hands those
rows to GLM 5.3 (not Flash; maintainer, 2026-10-12) with the same guards as
`implement`: the leak check before the call, `make verify` after the attempt,
one repair attempt and a Stage-1 fallback, a failing test per row, and one
checkpoint commit. The flow is: the reviewer reports, the orchestrator
decides, GLM repairs, the reviewer re-checks. Non-goal: a reviewer (Codex,
the review-loop ladder) never repairs its own findings — it would judge its
own fix, and reviewers stay read-only (ADR 0007, ADR 0011).

## Questions for the exploration

1. How `implement` in `scripts/stage2.py` is built end to end: preflight,
   the prompt it assembles, the write permission it gives the model, the
   attempt and repair sequence (route `flash-repair`, the Sonnet fallback),
   the `make verify` run, the time-log check and the checkpoint commit — and
   which parts a second verb could reuse as they are.
2. Where the rows to repair live and in which form: the loop record
   (`~/.local/state/coding-harness/stage2/<change>/loop.md`, its Status and
   "Broke a test" columns), the phase-6 table in `findings.md`, and
   `release-loop`; how a taken row and an open finding are recognised today,
   and which code parses those tables.
3. Which models and endpoints `model-endpoints.yaml` and `stage2.py` declare
   (GLM 5.3, GLM 5.3 Flash, Sonnet, Haiku), how a verb picks one, and what
   the review-loop ladder and the phase-6 review read afterwards — so a
   re-check after a repair works with what exists.
4. Which documents name the repair step today (`docs/WORKFLOW.md` phase 4b
   and 6, `prompts/04-implement.md`, `AGENTS.md`, ADR 0007, ADR 0011), and
   which tests pin `implement` and the loop (`tests/` for `stage2`).
