---
title: "Spec — mandatory-spec-review"
status: draft
implementation_status: none
date: 2026-11-17
last_reviewed: 2026-11-18
updated: 2026-11-18
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

A current spec review precedes the plan card for bounded, feature and architectural changes, and implementation refuses an unreviewed spec (bead coding-harness-ttic). Research: `research.md`; decisions: `decisions.md`.

## Problem

- The class table permits bounded changes to skip review and the entry table calls it optional, despite the existing review policy (`research.md`, 2026-11-17).
- The implement runner checks neither review currency nor open ambiguity, and the existing day-only review heading cannot distinguish same-day edits (`research.md`, 2026-11-17; `decisions.md`, Q-3, 2026-11-18).
- Open changes may already be planned or implemented without review, so the maintainer needs an inventory for individual catch-up decisions (`decisions.md`, Q-1 and Q-8, 2026-11-18).

## Terms

**Qualifying review:** a runner-written Opus 5.5 block or declared fallback block with readable rows, including an identifiable clean result; failed calls, unreadable answers, Codex blocks and hand-written reviews do not qualify.

**Open ambiguity:** in the newest current qualifying block, a row whose Severity or Finding cell begins `[AMBIGUITY]` and whose Status begins `open`; an answer alone does not close the row.

## Acceptance criteria

1. The workflow requires a current spec review before the plan card for bounded, feature and architectural changes.
   *Refuted by:* The workflow text permits a card before that review.
2. The workflow exempts spikes from this mandatory review.
   *Refuted by:* The workflow text requires the review for a spike.
3. When a review produces rows requiring a spec edit, the workflow repeats draft and review until a clean review reads the revised spec.
   *Refuted by:* The workflow permits the card after the edit without another review.
4. When implement reads a missing, invalid or disagreeing class, it refuses before starting a model and tells the operator to add or repair class declarations.
   *Refuted by:* An unknown class reaches a model or the remedy is missing.
5. When implement is called for a spike, the new review precondition permits it to reach the existing checks.
   *Refuted by:* The new precondition refuses an unreviewed spike.
6. When implement is called for a bounded, feature or architectural change without a current readable qualifying review, it refuses before starting a model.
   *Refuted by:* A missing, stale, unreadable, hand-written or Codex review admits a model.
7. When implement is called with a current readable qualifying review whose newest current block has an open ambiguity, it refuses before starting a model and names the row.
   *Refuted by:* The model starts or the refusal omits the row.
8. When implement is called with a current readable qualifying review and no open ambiguity in its newest current block, the new precondition permits the existing checks.
   *Refuted by:* The new precondition refuses the call.
9. When implement is called with --stage2-off, the same class and review preconditions apply.
   *Refuted by:* The flag bypasses either precondition.
10. When a new spec review succeeds, its runner-written block records the SHA-256 fingerprint of the spec bytes read by the reviewer.
   *Refuted by:* The block lacks the fingerprint or identifies different bytes.
11. When spec bytes differ from the fingerprint of a review, including uncommitted edits, that review is stale.
   *Refuted by:* A changed spec is accepted as current.
12. When a legacy qualifying block lacks a fingerprint, its currency is compared by day against the spec change, including uncommitted changes.
   *Refuted by:* The legacy block is treated as a fingerprinted review or an uncommitted change is ignored.
13. When Opus is unreachable, the spec-review verb retries once after a pause before using its centrally declared DeepSeek fallback through Pi.
   *Refuted by:* Fallback runs before the retry or a different unconfigured route is used.
14. When the fallback reviews a spec, the existing foreign-call leak check runs before the call.
   *Refuted by:* A blocked leak check still permits the fallback call.
15. When a fallback review succeeds, its runner-written block identifies it as fallback.
   *Refuted by:* A fallback block is indistinguishable from an Opus block.
16. When the morning inventory is generated, it lists non-archived bounded, feature, architectural and classless changes that fail the same review check as implement, including implemented changes.
   *Refuted by:* A qualifying refused change is missing or an exempt spike is listed as refused.
17. When the morning inventory finds a fallback review, it identifies the change for an Opus re-check by day.
   *Refuted by:* A fallback review is omitted from the re-check list.
18. When a later implement call targets a previously implemented change, the same precondition applies.
   *Refuted by:* Earlier implementation exempts the later call.

## Non-goals

- Undoing prior implementation or automatically deciding which reviews to catch up.
- Applying the shared currency component to review-loop rounds or phase 6; that follows separately (bead coding-harness-4amm).
- A new runner verb, standalone gate, ADR amendment or mandatory review for spikes.

## Protected areas

Existing ADRs and decision records remain unchanged because the maintainer settled the scope without an ADR amendment.

## Definition of Done

- `make verify` green.
- Doctrine, runner, tests and morning inventory instructions move together as named in `plan.md`.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes bead coding-harness-ttic, with `Closes-Bead: coding-harness-ttic` in its last commit.
- Special runs: none.

## Open decisions

- [DETAIL] A legacy date-only review is current when its day is on or after the last committed spec-change day and the spec has no uncommitted edits; same-day committed changes remain indistinguishable, the limit accepted in Q-3.
- [DETAIL] The retry pause is 30 seconds; it is a revisable operational delay and avoids an immediate duplicate call.
- [DETAIL] The initial centrally configured fallback is `deepseek-v4.1-flash` on OpenCode Go, an already declared DeepSeek model; the configuration can be changed in one value.
