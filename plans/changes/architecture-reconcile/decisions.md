---
title: "Decisions — architecture-reconcile"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-190
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# architecture-reconcile — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).

## SKIP · interview

status: skipped
reason: the bead (coding-harness-190) already states the form — a dated table under docs/research/, like the WORKFLOW.md reconciliation of coding-harness-i0l, per contract section of the target and per M-step of the plan, with the gap table re-measured — and the maintainer put this bead into lane D of the run plan of 2026-10-31 (conversation, about 15:10 UTC: "Gebe Spur d weitere beads die sie bearbeiten kann"). Every choice that would change a decision is kept out of scope below and goes to the maintainer as a finding.

## Details for the draft

[DETAIL] **A new dated document, no rewrite of the four architecture
documents.** Reason: the bead asks for a table under `docs/research/`; the
living target and plan are pinned by `scripts/check_decision_continuity.py`
and `tests/test_stage2.py` (`test_d13_is_amended_by_adr_0007`), so a rewrite
would change gated text without the maintainer's word. Research open point 4
(re-measure versus supersede) is answered by the bead: the table records the
state, superseding a document is the maintainer's call.

[DETAIL] **Contradictions become rows with a proposed remedy, not edits.**
Reason: the D-16 row (`model-routing.yaml`), the D-17 row (Apache-2.0 against
the PolyForm licence in `LICENSE` and `COMMERCIAL.md`) and the M0 rows against
ADR 0006 (research open point 5) each need either a banner, an
`AMENDMENT_ADRS` entry or an ADR; which one is a decision. The table names the
contradiction, its evidence and the candidate remedies.

[DETAIL] **The gap table is re-measured on the change's base commit.** Reason:
the gap analysis measured `eddfc0b` on 2026-09-17; the new table states its
own commit and date for every row, and a row that could not be measured says
"not read".

[DETAIL] **Tracker state is read through `scripts/bead_render.py`** for the
gap beads the analysis cites (research open point 2). Reason: the explorer ran
no commands; the drafter's table must state each bead's status with its date.

[DETAIL] **Text only.** Reason: no script, test, prompt or `decisions/` file
changes, so the local `make verify` is skipped and CI is the gate (AGENTS.md,
"A text-only change"). If the draft finds a needed script or test change, it
stops and records it as a finding instead.
