---
title: "Decisions — no-work-ledger-marker"
category: decisions
status: draft
implementation_status: none
date: 2026-11-10
created: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-twbl
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, no-work-check]
---

# no-work-ledger-marker — Decisions

Class: bounded (bead coding-harness-twbl; one answered question or a reasoned
skip is owed — a skip below, written during the night run of 2026-11-10 and
to be confirmed by the maintainer at the plan card).

## SKIP · interview

status: skipped
reason: A bounded bug fix whose intent the bead states in full and whose direction the maintainer set on 2026-11-09 when the finding was made a follow-up ("PR now, MAJOR as follow-up bead") — the runner's own clearing of a ledger marker is discounted before the no-work check decides whether an attempt did work (bead coding-harness-twbl, finding F-1 of the change no-work-done). What remains is mechanics, decided below with reasons; the plan card goes to the maintainer before anything is built.

## Decided by the agent

[DETAIL] **The discount compares content, not paths**: a plan whose only
surviving change, beside the discounts that exist, is a `not yet written`
marker the runner's own clearing removed is no work. Reason: the gap is that
the candidate filter looks at paths only, so a ledger edit by the runner on a
candidate path counts for the model.

[DETAIL] **Only the clearing the runner itself performs is discounted.** A
ledger line the model rewrote in any other way stays work. Reason: the check
must not start to hide real edits of the plan.

[DETAIL] **The four discounts that exist stay as they are** (findings file
and plan index, stamp-only edits, the plan's time section, the candidate
filter). Reason: they are pinned by tests and were reviewed with the change
no-work-done; this change adds one case and reorders nothing.

[DETAIL] **The reproduction of finding F-1 becomes the red-first test**: a
rejected attempt leaves a new test, the retry restores the marker,
verification clears it, and the retry is rejected as no work done. Reason:
it is the measured case, reproduced in memory by the phase-6 reviewer.
