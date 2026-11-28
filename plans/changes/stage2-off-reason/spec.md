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
4. When a caller supplies a change name as the flag's only value and no positional change, the runner refuses with exit 2 before a model call because the positional change is missing. The after-the-fact guard in `scripts/stage2.py` and its test `test_a_change_name_after_the_stage2_off_flag_is_named_as_eaten` are removed; the refusal comes from the missing change alone (S-2).
   *Refuted by:* The invocation launches a call without a change, or the old guard or its test is still present.
5. When `--stage2-off` has a value on an unsupported verb, the runner refuses with exit 2 before a model call.
   *Refuted by:* An unsupported verb is accepted or starts a call.
6. When the process report reads a valid invocation with a supplied reason, it never names the reason as the change. It identifies the positional change when the reason is one whitespace-free argument or the change precedes the flag; for a multi-word reason placed before the change, which `ps` output cannot split, it reports the change as unknown (S-1). Detached job records carry the original argument array, so a job record's change is always identified exactly, whatever the reason (S-5).
   *Refuted by:* The report names the reason as the change; fails to identify the change in one of the two identifiable cases or in a job record; or, for an unsplittable `ps` line, names any change instead of unknown (S-7).
7. When current runner instructions show the fallback invocation, they require a reason value. Current runner instructions are `docs/WORKFLOW.md`, `prompts/01-explore.md`, `prompts/04-implement.md`, `README.md`, the module docstring and `--help` text of `scripts/stage2.py`, and the runtime next-step messages of `scripts/stage2.py` (for example "rerun the verb or add --stage2-off", which becomes "… add --stage2-off <reason>") (S-3, S-4).
   *Refuted by:* One of these presents a bare flag or an optional reason as a valid invocation.

## Non-goals

- Change fallback models, routing, leak checks, or the location of the call record.
- Rewrite historical ADRs, archived changes or handovers, or reconstruct obsolete bare-flag process invocations.
- Add a design phase or ADR for this bounded change.

## Protected areas

Historical records remain unchanged; their wording describes the behavior at their recorded time.

## Definition of Done

- `make verify` green.
- Update `docs/WORKFLOW.md`, `prompts/01-explore.md`, `prompts/04-implement.md` and `README.md` with the code in the same pull request; `AGENTS.md` is human-written, so its wording is proposed to the maintainer in the pull request body, not edited; the doctrine test `flash_runner_doctrine_problems` requires the new literal `--stage2-off <REASON>` in `docs/WORKFLOW.md`, `prompts/01-explore.md` and `prompts/04-implement.md`, and accepts the old or the new literal in `AGENTS.md` until the maintainer applies the proposed wording (S-6); no ADR changes.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes bead `coding-harness-73gi.6` and its last commit carries `Closes-Bead: coding-harness-73gi.6`.
- Special runs: none.

## Open decisions

- [DETAIL] Interpret a reason as the value accepted by the existing argument parser, without adding a new nonempty-content validation rule; the requested change makes the value mandatory but does not redefine its contents.
- [DETAIL] Interpret process reports using the new mandatory-value syntax; old bare-flag invocations are ambiguous and are outside this bounded fix.
- [DETAIL] Keep historical ADRs as historical records; update the current instructions so the executable contract is clear.

None open.
