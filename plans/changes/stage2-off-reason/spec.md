---
title: "Spec — stage2-off-reason"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-73gi.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2]
class: bounded
appetite: 2
adr_files: []
---

# Spec — stage2-off-reason

The Stage-1 fallback requires the caller to supply a reason (bead `coding-harness-73gi.6`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-28, `research.md` found that `scripts/stage2.py` accepts a bare `--stage2-off`, substitutes a default reason, and needs a special guard when a change name is consumed as the optional value. Current instructions and the process report also describe or interpret the value as optional.

## Acceptance criteria

1. When `--stage2-off` is supplied without a value, the runner refuses with exit 2 before a model call.
   *Refuted by:* A bare flag starts a call or exits successfully.
2. When a caller supplies a reason and change for `explore`, `implement` or `repair`, the existing Stage-1 route receives the supplied reason.
   *Refuted by:* A supported invocation rejects or replaces its reason or chooses a different route.
3. When a Stage-1 call with a nonempty reason is recorded, the supplied reason remains in its existing phase artefact call record.
   *Refuted by:* The record omits, replaces or moves the reason.
4. When a caller supplies a change name as the flag's only value and no positional change, the runner refuses before a model call.
   *Refuted by:* The invocation launches a call without a change.
5. When `--stage2-off` has a value on an unsupported verb, the runner refuses with exit 2 before a model call.
   *Refuted by:* An unsupported verb is accepted or starts a call.
6. When the process report reads a valid invocation with a supplied reason, it identifies the positional change even if the reason equals a known change name.
   *Refuted by:* The report names the reason as the change or fails to identify the actual change.
7. When current runner instructions show the fallback invocation, they require a reason value.
   *Refuted by:* A current instruction presents a bare flag or an optional reason as a valid invocation.

## Non-goals

- Change fallback models, routing, leak checks, or the location of the call record.
- Rewrite historical ADRs, archived changes or handovers, or reconstruct obsolete bare-flag process invocations.
- Add a design phase or ADR for this bounded change.

## Protected areas

Historical records remain unchanged; their wording describes the behavior at their recorded time.

## Definition of Done

- `make verify` green.
- Update `docs/WORKFLOW.md`, `prompts/01-explore.md`, `prompts/04-implement.md` and `AGENTS.md` with the code in the same pull request; no ADR changes.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes bead `coding-harness-73gi.6` and its last commit carries `Closes-Bead: coding-harness-73gi.6`.
- Special runs: none.

## Open decisions

- [DETAIL] Interpret a reason as the value accepted by the existing argument parser, without adding a new nonempty-content validation rule; the requested change makes the value mandatory but does not redefine its contents.
- [DETAIL] Interpret process reports using the new mandatory-value syntax; old bare-flag invocations are ambiguous and are outside this bounded fix.
- [DETAIL] Keep historical ADRs as historical records; update the current instructions so the executable contract is clear.

None open.
