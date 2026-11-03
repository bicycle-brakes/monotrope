---
title: "Spec — adr-0016-docs-check"
status: draft
implementation_status: done
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-v9xx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, adr]
class: bounded
appetite: 1
adr_files: [docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md]
---

# Spec — adr-0016-docs-check

ADR 0016 names the check the draft runner really runs (bead
`coding-harness-v9xx`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

Since the draft-gates-only change (bead `coding-harness-77qj`) the draft
runner checks a draft with `bash scripts/verify_all.sh --job docs`, but ADR
0016 decisions 2, 3 and 7 still say `make verify`. A reader of the record
expects a check the runner no longer runs.

## Acceptance criteria

1. ADR 0016 decisions 2, 3 and 7 name `bash scripts/verify_all.sh --job docs`
   for the draft and no longer `make verify`.
   *Refuted by:* one of the three still names `make verify` for the draft.
2. A dated note after the Decision section says the text was amended on
   2026-11-01 under bead `coding-harness-77qj`, with no behavior change, and
   that implement and repair keep the full `make verify`.
   *Refuted by:* the note is missing or claims a behavior change.

## Non-goals

- Any change to `scripts/stage2.py`, `docs/WORKFLOW.md` or the gates.
- The other mentions of `make verify` in ADR 0016 (context, consequences,
  validation), which describe the state when the record was accepted.

## Definition of Done

- The document check `bash scripts/verify_all.sh --job docs` is green.
- The decision pull request is open with the label `decision`; the maintainer
  merges it.

## Open decisions

None open; the five answers stand in `decisions.md`.
