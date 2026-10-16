---
title: "Spec — repair-scope"
status: draft
implementation_status: none
date: 2026-10-16
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-t83
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, repair]
class: bounded
appetite: 2
adr_files: []
---

# Spec — repair-scope

Repair and implement attempts leave changes only in their permitted areas;
the runner restores and names forbidden changes before verification (bead
`coding-harness-t83` — bound the repair attempt's writes). Sources:
[`research.md`](research.md) and [`decisions.md`](decisions.md).

## Problem

- A repair wrote its own handover, removed manually afterwards; the incident
  is recorded in the research seed dated 2026-10-16, not independently
  re-verified there.
- At `9943a25`, `run_attempts` verifies successful model calls without a
  path-scope check, and `checkpoint` stages the whole tree. Both `repair`
  and `implement` can therefore commit unrelated files. Research section
  "What exists today" identifies the shared gap and the draft's existing
  restoration mechanism.
- The embedded repository rules require handovers, while the repair and
  implement contracts give no exception for runner calls. The research
  identifies both handover references in `prompts/04-implement.md`.

## Terms

- **Denied areas:** `docs/journal/**`, `.beads/**`, `.claude/**`,
  `decisions/**`, `docs/adr/**`, root `AGENTS.md`, every folder under
  `plans/changes/` other than this invocation's change folder, and that
  change's own `decisions.md`.
- **Measured paths:** tracked changes, including staged changes and
  deletions, and untracked non-ignored files, as seen by the existing
  `changed_paths` reader. Restoration returns tracked paths to the run's
  baseline commit and removes new untracked paths.

## Acceptance criteria

1. When an implement or repair prompt is assembled for any supported route,
   it explicitly forbids writes in every denied area and assigns handovers
   to the orchestrating session, overriding the embedded handover instruction
   for this call.
   *Refuted by:* a generated prompt omits a denied area or leaves this call
   responsible for a handover.
2. When a successful model call leaves measured paths changed in denied
   areas, those paths are restored before derived-file preparation,
   formatting or `make verify` starts.
   *Refuted by:* verification observes a forbidden addition, modification,
   staged edit or deletion, or a forbidden path reaches the checkpoint.
3. When post-run checks fail and another attempt follows, the same scope
   restoration applies independently to each attempt.
   *Refuted by:* a retry sees a predecessor's forbidden edit or a later
   attempt's forbidden change survives because cleanup ran only once.
4. When the runner restores forbidden paths, `findings.md` records every
   restored path in full with its attempt number and route, whether the
   attempt passes or fails its post-run checks.
   *Refuted by:* a restored path is absent, truncated, attributed to another
   attempt, or lost when failed repair findings are restored.
5. When scope restoration runs, permitted model changes remain available to
   the existing checks and checkpoint, alongside the runner's legitimate
   derived-file, route, time-log and finding-status writes.
   *Refuted by:* a permitted code, test, doctrine or own-change edit is
   discarded by cleanup, or a runner-owned write disappears from the result.
6. When the workflow and implementation instructions describe runner work
   calls, they state the shared denied areas, restoration before verification,
   and the orchestrating session's ownership of handovers consistently.
   *Refuted by:* the workflow promises unrestricted repair commits or an
   implementation instruction assigns the worker a handover file.

## Non-goals

- An allow list for legitimate code, tests or doctrine changes; a refusal
  merely because restoration was needed; changes to draft or explore scope.
- New sandbox guarantees for ignored files, external paths or the git
  directory: the residual risks accepted in ADR 0016 and retained in ADR 0017
  remain. Existing credential scans and failed-call ignored-file cleanup stay.
- Changes to model routing, retry limits, moved-HEAD stops, failed-process
  rollback, review ownership or repair answer validation.
- Phase 2b and an ADR draft: this is the recorded `bounded` correction.

## Protected areas

`AGENTS.md`, `decisions/**`, `docs/adr/**`, `.beads/**`, `.claude/**`,
`docs/journal/**` and other change folders stay untouched: the correction
enforces existing worker ownership without changing governance or task state.

## Definition of Done

- The criterion-ledger tests and `make verify` pass.
- `scripts/stage2.py`, `tests/test_stage2.py`, `prompts/04-implement.md` and
  `docs/WORKFLOW.md` agree; the runner refreshes `plans/INDEX.md` and stamps
  changed held documents. No architecture model or ADR changes.
- The pull request's file list respects the protected areas and non-goals.
- The orchestrator closes the write-scope work item in the pull request and
  uses `Closes-Bead: coding-harness-t83` in its last commit.
- Special runs: none; verification uses stand-ins, with no live model call.

## Open decisions

None open. The four recorded details in `decisions.md` stand: restore rather
than refuse, use the denied areas, guard both verbs, and clarify the prompts
without editing `AGENTS.md`.

- `[DETAIL]` The scope check measures what the existing draft restoration can
  measure; its ignored-file and git-directory limits remain explicit rather
  than implying a new sandbox guarantee.
- `[DETAIL]` Phase 4 has a two-hour appetite, repairs included: this bounds
  the shared-loop correction and its regressions; no earlier appetite is
  recorded in the inputs.
