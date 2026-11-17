---
title: "Spec — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3, version: "2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, provenance]
class: bounded
appetite: 3
adr_files: []
neighbours: [plans/changes/archive/2026-11-16-explore-provenance/spec.md, plans/specs/implementation-verification/spec.md]
---

# Spec — runner-stamps-provenance

The runner records the actual producer after explore, draft and repair, and rejects invalid producer headers in files touched by a run (bead `coding-harness-f9sv`). Research: `research.md`; decisions: `decisions.md`.

## Problem

- Draft artifacts receive headers from the model session; research publication is already stamped by the runner (`research.md`, “What exists today”, 2026-11-16).
- On 2026-11-16, 271 of 620 producer headers under `plans/` failed the census rule; a tree-wide check would also turn existing lanes red (`decisions.md`, Q-4). The existing stock is addressed separately.

## Terms

A **producer record** identifies a producing program and publication date in `produced_by`; a model is optional in the existing contract but is required for a new single-model run record. A **touched file** is a file changed by a run and retained for its post-run checks; files restored by the runner are excluded.

## Acceptance criteria

1. When a single-model explore publishes research, the runner stamps a producer record with the actual program, model and publication date of that run; a swarm publication instead names the swarm as producer, the bound publication day and no single model.
   *Refuted by:* a GLM route recording `codex`, a different model or a date other than the publication day.
   *Basis:* `decisions.md#Q-4`, `decisions.md#Q-8`.
2. When a draft attempt changes and retains a model-written artifact with frontmatter, including a new ADR if present, the runner stamps a producer record with the actual program, model and publication date before its post-run checks, including an attempt that subsequently fails those checks.
   *Refuted by:* an affected artifact missing that record, or a GLM attempt recorded as `codex`, with a wrong model or date.
   *Basis:* `decisions.md#Q-4`.
3. When a repair attempt changes and retains a model-written artifact with frontmatter, the runner stamps a producer record with the actual program, model and publication date before its post-run checks.
   *Refuted by:* an affected artifact missing that record, or its record naming a different program, model or publication day.
   *Basis:* `decisions.md#Q-4`.
4. When a runner verb checks its result, a touched file whose frontmatter carries `produced_by` fails the publication header contract, including any earlier producer record, the post-run check fails with a diagnostic identifying the file; the check accepts the preserved provenance class and a valid retained approval.
   *Refuted by:* a touched producer-bearing file with an invalid producer or date is accepted, or a file without `produced_by` is rejected by this check.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-4`, `decisions.md#Q-6`, `decisions.md#Q-7`, `decisions.md#Q-11`, `decisions.md#Q-12`.
5. While the runner stamps a draft or repair artifact, it preserves bytes outside `produced_by`, `updated` and a `review` reset required by criterion 8.
   *Refuted by:* changed prose, fences, plan card, `provenance` or unrelated frontmatter; in particular a draft ADR loses its `human-decided` provenance.
   *Basis:* `decisions.md#Q-11`.
6. If an artifact cannot be stamped safely, the attempt fails with a diagnostic instead of publishing an invented or malformed header.
   *Refuted by:* accepting a header with any YAML anchor or alias, undecodable bytes, a non-mapping header or an unreadable earlier producer, or failing without identifying the artifact.
   *Basis:* `research.md`, “The runner already stamps provenance in these places”.

7. When an artifact is stamped, readable producer records committed before the run remain byte-for-byte, session-written self-descriptions from the attempt are discarded, and the measured contributor record is added.
   *Refuted by:* normalising an earlier record, retaining a self-written record, or attributing an unchanged file to a later attempt.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-10`, `decisions.md#Q-12`.
8. When a draft or repair changes an approved document's body, its approval is reset to pending with null approver and date, and the attempt block in `findings.md` identifies the former approver.
   *Refuted by:* retaining approval for changed body content or omitting whose approval was reset.
   *Basis:* `decisions.md#Q-11`, `decisions.md#Q-12`.
9. When stamping changes only the header of an approved document, its approval remains unchanged.
   *Refuted by:* resetting an approval solely because of a header stamp.
   *Basis:* `decisions.md`, “Decided by the agent”.
10. If a draft attempt's changed files cannot be measured, the attempt fails with a diagnostic and the next available route runs.
    *Refuted by:* accepting the unmeasured draft attempt or failing to continue to the next available route.
    *Basis:* `decisions.md#Q-12`.

The explore publication continues to remove generated skeleton notices; criterion 5 applies to draft and repair, not that removal.

## Non-goals

- Migration of existing headers and a tree-wide check belong to the separate migration work (bead `coding-harness-2i7x`), per Q-4.
- No general side-route detector, enforcement of allowed provenance classes, change to the untouched new-change skeleton, or automated human approval.
- No change to the maintainer's answers in `decisions.md`, nor to the headerless loop record.

## Protected areas

Runner-held paths remain outside model attempts, including `provenance.yaml`, `decisions/gates.yaml`, `prompts/`, `templates/`, and `AGENTS.md`; no edit to them is planned. Existing unrelated artifacts and archived headers are not migrated.

## Definition of Done

- `make verify` green; the tests in the criterion ledger exercise the runner routes and their failure cases.
- The runner, its shared producer validation and their tests move in the same pull request; no special migration run is required.
- The protected areas and non-goals are checked against the pull request's file list.
- The pull request closes `coding-harness-f9sv` and its final commit carries `Closes-Bead: coding-harness-f9sv`.

## Open decisions

[DETAIL] Insert a missing field at the end of frontmatter when `tags` is absent; this preserves unrelated bytes. Refuse all YAML anchors and aliases, not just ambiguous ones, because their shared source spans make safe edits uncertain. A resumed swarm retains its frozen preparation day, because its publication bytes are bound to the resume snapshot.

The remaining review ambiguities F-10 (attribution across attempts), F-15 (whether a model is required for every producer), F-16 (publication day on swarm resume), and F-17 (unsafe YAML headers) remain open in `findings.md`. Their provisional wording above does not constitute a maintainer answer; reconcile them before implementation. F-9 is settled by Q-11 and Q-12.
