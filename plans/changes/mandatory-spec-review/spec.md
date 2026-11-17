---
title: "Spec — mandatory-spec-review"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-ttic
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-terra, 2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, spec-review, stage-2]
class: bounded
adr_files: []
---

# Spec — mandatory-spec-review

The spec review is required before the plan card for bounded, feature and architectural changes, and the implement runner refuses an unreviewed or ambiguous spec (bead coding-harness-ttic). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- The class table permits bounded changes to skip the spec review, and `AGENTS.md` calls phase 2a optional, although ADR 0016 requires it for changes routed through stage 2 (`research.md`, 2026-11-17).
- The implement runner does not refuse a missing review or an open ambiguity; review and redrafting currently depend on instructions rather than a runner precondition (`research.md`, 2026-11-17).
- Existing open changes may already have passed planning or implementation without a review; the maintainer needs a list to decide whether to catch up each one (`decisions.md`, Q-1, 2026-11-17).

## Acceptance criteria

1. When a bounded, feature or architectural change reaches its plan card, the workflow requires an Opus spec review first.
   *Refuted by:* The workflow permits such a card without that review.
2. When a spike reaches its plan card, the workflow does not require the new mandatory review.
   *Refuted by:* The new rule requires a spike to have the review.
3. When an implement call for a bounded, feature or architectural change lacks spec-review rows dated after the spec's last change, the runner refuses before starting an implementation model.
   *Refuted by:* An absent or older review reaches an implementation model.
4. When an implement call for a bounded, feature or architectural change has an open `[AMBIGUITY]` in its spec-review rows, the runner refuses before starting an implementation model.
   *Refuted by:* An open ambiguity reaches an implementation model.
5. When an implement call for a bounded, feature or architectural change has a current spec review and no open `[AMBIGUITY]`, the new review precondition permits it to proceed to the existing checks.
   *Refuted by:* The new precondition rejects that call.
6. When an implement call is for a spike, the new review precondition does not refuse it.
   *Refuted by:* An unreviewed spike is refused by the new precondition.
7. When a morning handover is prepared, it lists open changes without a spec review for the maintainer to decide individually whether to catch up the review.
   *Refuted by:* An open unreviewed change is omitted or the handover decides catch-up on the maintainer's behalf.
8. When this change takes effect, the new refusal applies to subsequent implement calls, including calls on previously implemented changes.
   *Refuted by:* A later implement call is exempted because the change was implemented before this change merged.

## Non-goals

- Retroactively undoing or automatically reviewing changes already implemented.
- A new runner verb, standalone gate, or ADR; changing the review model or the phase-6 review.
- Requiring a spec review for spikes under the new rule.

## Protected areas

Existing decision records and ADRs stay unchanged: the maintainer has already settled this change's scope without an ADR amendment.

## Definition of Done

- `make verify` green.
- Doctrine and runner behavior updated together: `AGENTS.md`, `docs/WORKFLOW.md`, `prompts/02a-spec-review.md`, `scripts/stage2.py`, and their applicable tests; morning handover instructions carry the inventory requirement.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead coding-harness-ttic, with `Closes-Bead: coding-harness-ttic` in its last commit.
- Special runs: none.

## Open decisions

- [DETAIL] A bounded change has no design phase or ADR draft; the class and the recorded decision already set that boundary.
- [DETAIL] A clean review must remain identifiable as a review even when it returns no finding rows; otherwise a successful clean review would be indistinguishable from no review. Its representation is an implementation detail.
