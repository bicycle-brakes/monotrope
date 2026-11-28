---
title: "Spec — verify-lock-handle"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-42em
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verify-lock]
class: bounded
appetite: 4
adr_files: []
---

# Spec — verify-lock-handle

Independent verification admissions have explicit owners, so two admissions in one process cannot confuse their children or records (bead `coding-harness-42em`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `03298ec1`, `scripts/verify_lock.py` refuses a second independent admission while the first is held or acquiring: its single process-global admission would otherwise be overwritten. Child markers and measurement context read that global admission, and publishing uses a process-id-based temporary name. The research records these paths and the predecessor's temporary single-admission boundary (2026-11-28).

## Terms

**Admission:** permission to run protected verification work, including its locks, slot, ownership token and measured context. A nested entry reuses a validated ancestor's admission.

## Acceptance criteria

1. When an independent admission is held, `hold_admission` yields its admission handle containing its lock ownership, slot and token.
   *Refuted by:* The caller receives only descriptors or cannot identify the owned slot and token.
2. When two independent admissions in one process are eligible for the two available slots, both can be held concurrently with distinct ownership and holder records.
   *Refuted by:* The second is refused solely because of the process, blocks despite available capacity, or either admission overwrites the other's record.
3. When a child is launched for an admission, its inherited descriptors, ownership marker and measurement context identify that admission alone.
   *Refuted by:* A child receives another concurrent admission's descriptor, token, slot record or measurement identity.
4. When one of two concurrent admissions ends or fails to enter, the other retains its own ownership and remains usable until its own release.
   *Refuted by:* Releasing or failing one closes, removes or invalidates the other's lock, marker or holder record.
5. When an admission publishes a holder record, its temporary publication name is specific to its token.
   *Refuted by:* Two admissions with the same process ID select the same temporary publication name.
6. When a valid descendant enters nested verification, it reuses its validated ancestor's admission without acquiring another slot.
   *Refuted by:* A valid descendant queues for another slot or a stale or forged marker is accepted.
7. While admissions contend, existing capacity, queue, memory-floor, exclusive-mode and descendant-survival protections continue to apply across processes and within one process.
   *Refuted by:* Protected work exceeds the configured capacity, bypasses the queue or memory floor, overlaps exclusive mode, or releases a surviving child's lock prematurely.
8. When no owned admission is supplied for a child, only a validated inherited admission can supply its ownership marker, and unrelated or foreign calls receive no owned admission marker.
   *Refuted by:* An unrelated child inherits an arbitrary concurrent admission or a foreign-model environment receives its token.

## Non-goals

Changing slot counts, queue fairness, memory-floor policy, foreign-model allowlists, or the on-disk holder record format is outside this change. Queue record naming is unchanged; the token-specific name concerns temporary holder publication.

## Protected areas

Archived change artifacts are historical evidence and stay unchanged. Tracker data and model configuration are outside this change.

## Definition of Done

- `make verify` green.
- `docs/WORKFLOW.md` and `docs/how-it-works.md` describe the resulting admission behavior in the same pull request.
- Protected areas remain untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead `coding-harness-42em` and its last commit carries `Closes-Bead: coding-harness-42em`.
- Special runs: none.

## Open decisions

- [DETAIL] A nested entry may use a distinct no-owned-handle representation: it already has a validated ancestor and must not claim fresh descriptors. This preserves existing nesting without inventing ownership.
- [DETAIL] Four hours is the phase-4 appetite, including repairs; it is a reversible planning limit and no earlier appetite is recorded.
