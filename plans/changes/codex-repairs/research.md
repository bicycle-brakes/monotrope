---
title: "Research — codex-repairs"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-0ga
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair, codex]
---

# Codex repairs the taken review findings — Research

Phase 1 for bead coding-harness-0ga, read against `origin/main` at `3199a28`
on 2026-10-13.

## The request

The maintainer, 2026-10-13, in the conversation: "Bitte lasse zukünftig das
Implementieren der Fixes der Fehler aus dem Review Sol machen" — in future,
let Sol (Codex, model `gpt-6.1-sol`) implement the fixes of the review
findings. A second remark the same day: the Z.ai budget was exhausted mainly
by GLM 5.3 (not Flash), the model ADR 0015 routes the repairs to.

## Where it stands

- ADR 0015 (`docs/adr/0015-glm-5-3-repairs-taken-findings.md`) routes
  `python3 scripts/stage2.py repair <change>` to GLM 5.3: a first attempt, one
  GLM 5.3 repair attempt with the first one's diagnostics, then a Sonnet 5.5
  stage-1 fallback (`scripts/stage2.py`, `repair`).
- ADR 0016 has Codex draft spec, design and plan (`draft <change>`), so the
  runner already starts Codex for work that writes files.
- Codex (`gpt-6.1-sol`) is the phase-6 reviewer (`review <change>`).
- The research of the repair verb (`plans/changes/stage2-repair/research.md`)
  named as a non-goal: a reviewer never repairs its own findings, because it
  would then judge its own work in the next review.

## Questions this change has to answer

- [DECISION] Phase-6 findings come from Codex. If Codex repairs them, the
  re-review judges its own repair. Is that accepted, or does the re-review
  then run in a fresh Codex session, or on another model?
- [DECISION] Does Codex repair both the loop rows (4b, found by the OpenCode
  Go ladder) and the phase-6 findings?
- [DECISION] What is the fallback when the Codex attempts fail — GLM 5.3,
  Sonnet 5.5, or straight to the maintainer?
- [GAP] How the runner starts Codex for a writing task today (the `draft`
  route), its sandbox, its time limit and how its answer is checked.
- [GAP] What in the repair verb is GLM-specific (credential scrubbing,
  `glm_env`, the post-run checks) and what carries over unchanged.
