---
title: "Decisions — research-free-paid"
category: decisions
status: draft
implementation_status: none
date: 2026-11-05
created: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-wb40
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, research-swarm, free-selection]
---

# research-free-paid — Decisions

Class: bounded (bead coding-harness-wb40).

## Interview — reasoned skip

The one decision this repair needs is already the maintainer's: in change pi-catalog-move (`plans/changes/pi-catalog-move/decisions.md`, Q-2, 2026-11-04) the maintainer left the choice to the recommendation that a paid admission wins in code — an id the `opencode-go` entry declares in `modelle` is never selected by the free rule, whatever its suffix — and that change's plan step 4a named both the review loop and the research swarm. The merged repair (PR #335) covered the review loop only; with Pi 1.5.0, `prepare-explore` refuses on `beam-free` (reproduced 2026-11-05). This change applies the same answer to the research swarm's free selection; no new question arises, so the interview is skipped with this reason.
