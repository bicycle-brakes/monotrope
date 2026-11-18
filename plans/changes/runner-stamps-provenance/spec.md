---
title: "Spec — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-18
updated: 2026-11-18
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

A **producer record** identifies a producing program and an ISO publication date in `produced_by`; the existing contract permits an absent model, while a new single-model run record requires one. A **touched file** is a file changed by a run and retained for its post-run checks; files restored by the runner are excluded. The **committed baseline** is the header committed before the run, not a session-written header. A swarm’s publication day is the preparation day frozen in its resume binding. A **valid retained approval** is a committed `approved` review with a nonempty approver and an ISO approval date, unchanged by the session; the runner does not grant approvals.

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
4. When any file-writing runner verb completes, including future verbs, one shared post-run check rejects each touched file carrying `produced_by` if its applicable contract fails, identifying the file; for research the existing research publication contract applies, adapted to preserve the committed provenance class and valid retained approval, and for other files only the producer records' shape, known program and ISO date are checked, including every earlier record.
   *Refuted by:* explore or spec-review bypassing the check; an invalid earlier producer being accepted; a file without `produced_by` being rejected by this check; or a valid retained approval or committed provenance class being refused.
   *Basis:* `decisions.md#Q-6`, `decisions.md#Q-7`, `decisions.md#Q-12`, `decisions.md#Q-13`, `decisions.md#Q-14`, `decisions.md#Q-17`.

5. While the runner stamps a draft or repair artifact, it preserves bytes outside `produced_by`, `updated` and a `review` reset required by criterion 8.
   *Refuted by:* changed prose, fences, plan card, `provenance` or unrelated frontmatter; in particular a draft ADR loses its `human-decided` provenance.
   *Basis:* `decisions.md#Q-11`.
6. If an artifact cannot be stamped safely, the attempt fails with a diagnostic instead of publishing an invented or malformed header.
   *Refuted by:* accepting a header with any YAML anchor or alias, undecodable bytes, a non-mapping header duplicate `produced_by` keys, or an unreadable earlier producer, or failing without identifying the artifact.
   *Basis:* `research.md`, “The runner already stamps provenance in these places”.

7. When explore, draft or repair stamps an artifact, readable producer records committed before the run remain byte-for-byte, session-written self-descriptions are discarded, and each measured contributing attempt is recorded only for files that attempt changed.
   *Refuted by:* normalising an earlier record, retaining a self-written record, or attributing an unchanged file to a later attempt.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-10`, `decisions.md#Q-12`, `decisions.md#Q-15`.
8. When a draft or repair changes an approved document outside `produced_by` and `updated`, the committed approval is reset to pending with null approver and date and an attempt block in `findings.md` identifies the former approver, including for an accepted or earlier failed attempt.
   *Refuted by:* approval surviving a changed title, appetite or body, or a missing reset notice for a failed or accepted attempt.
   *Basis:* `decisions.md#Q-11`, `decisions.md#Q-12`, `decisions.md#Q-14`, `decisions.md#Q-16`.
9. When a draft or repair changes an approved document only in `produced_by` or `updated`, its committed approval remains unchanged.
   *Refuted by:* resetting approval solely for those fields.
   *Basis:* `decisions.md#Q-14`, `decisions.md#Q-16`.
10. If a draft or repair attempt's changed files cannot be measured, the attempt fails with a diagnostic and the next available route runs.
    *Refuted by:* accepting an unmeasured attempt or skipping an available next route.
    *Basis:* `decisions.md#Q-12`.
11. When a model-written file is new, it has `ai-drafted-reviewed` provenance and a pending review, except that a new ADR may have `human-decided` provenance but must still have a pending review.
    *Refuted by:* a new file carrying an approval written by the session, or a new ADR being refused solely for `human-decided` provenance.
    *Basis:* `decisions.md#Q-14`.
12. When a previously committed model-written file is stamped, its provenance class and any retained approval are measured against the committed baseline, and a session-written approval is refused.
    *Refuted by:* accepting an approval invented by the session or rejecting an unchanged committed approval solely for being approved.
    *Basis:* `decisions.md#Q-11`, `decisions.md#Q-14`.

The explore publication continues to remove generated skeleton notices; criterion 5 applies to draft and repair, not that removal.

## Non-goals

- Migration of existing headers and a tree-wide check belong to the separate migration work (bead `coding-harness-2i7x`), per Q-4; that migration is the next change after this one, per Q-15.
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

[DETAIL] Insert a missing field at the end of frontmatter when `tags` is absent; this preserves unrelated bytes. Refuse all YAML anchors and aliases because safe source-span edits cannot be guaranteed. A resumed swarm retains its frozen preparation day so its publication binding remains stable.

[DETAIL] A retained approval needs a nonempty approver and ISO approval date, without introducing role membership or date-range rules; this makes the committed approval checkable without inventing an authorization policy. Do not append an identical measured producer record twice; the existing record already represents that producer and day. If a block mapping cannot be converted into a sequence while preserving the earlier record's bytes, refuse safely with the file named, rather than silently rewriting history. Fail an unmeasured repair attempt and continue to the next available route, as for draft, because its contributions cannot be attributed reliably.
