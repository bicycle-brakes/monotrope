---
title: "Spec — verify-cheap-first"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, model: gpt-6.1-sol, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, make-verify, gates]
class: bounded
appetite: 3
adr_files: []
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
---

# Spec — verify-cheap-first

Local verification derives a lasting cheap-first order from the one gate
list and stops at the first blocking failure, including in repositories
receiving the kit (bead coding-harness-bxxt.1). Research: `research.md`.
Maintainer decision: `decisions.md#Q-1`.

## Problem

- The research records 11 red full checks between 2026-11-04 and
  2026-11-09 whose test gate passed before a cheap gate failed: 3.3 hours
  of test execution preceded an already available failure. Its source is
  `docs/research/2026-11-09-make-verify-long-term.md`, measured through
  2026-11-09 21:42 UTC.
- At `a764f4c4` (2026-11-10), `scripts/ci_gates.py` returns declaration
  order, `scripts/verify_all.sh` runs pytest first and continues after a
  blocking failure, and schema version 2 has no cost field. Reordering the
  list alone would leave adopters able to undo the gain silently.
- The same reader, runner and gate list travel with the kit. The maintainer
  therefore chose a required cost classification and automatic local
  ordering, while retaining exhaustive hosted CI (`decisions.md#Q-1`).

## Terms

- **Cost class:** the declared scheduling category `seconds` or `minutes`,
  not a measured duration, deadline or runtime guarantee.
- **Selected gates:** executable gates remaining after job/subset,
  placement and action-equivalent filtering.
- **Local run:** the runner without `--ci`, for `verify`, `docs` or `drift`.

## Acceptance criteria

1. When a gate list is validated or consumed, schema version 3 requires
   every gate to declare `cost` as exactly `seconds` or `minutes`.
   *Refuted by:* a missing, null, non-string or unknown cost, including on
   an advisory, hosted-only or drift gate, or a version-2 list being accepted.
   *Basis:* decisions.md#Q-1.

2. When a local run selects gates, every selected `seconds` gate precedes
   every selected `minutes` gate, preserving declaration order within each
   class.
   *Refuted by:* an expensive gate placed first in the input executing
   before a selected seconds gate, ties changing order, or subset/placement
   membership changing because of sorting.
   *Basis:* decisions.md#Q-1.

3. When a local gate with `enforcement: block` exits nonzero, the run exits
   nonzero without executing any remaining selected gate.
   *Refuted by:* a planted failing `frontmatter-current` gate allowing the
   later `pytest` marker to be created, or the runner reporting green.
   *Basis:* decisions.md#Q-1.

4. When a local run stops on a blocking failure, its output identifies
   every remaining selected gate as not run because of that failure.
   *Refuted by:* an omitted remaining gate, an already executed or filtered
   gate labelled as skipped by the failure, or a skipped gate shown as green.
   *Basis:* decisions.md#Q-1; research.md, runner output consumers.

5. When all selected local gates succeed, the run executes each exactly
   once and reports `VERIFY GREEN`.
   *Refuted by:* an omitted or repeated selected gate, including a minutes
   gate, or a green verdict after gate-list generation failed or was empty.
   *Basis:* decisions.md#Q-1; research.md, intent of the bead.

6. When a report or advisory gate that runs fails, its failure remains
   visible without stopping the run or making the final verdict red by
   itself. A report or advisory gate that sorts behind the first blocking
   failure is not run and is named in the not-run summary like every other
   gate there.
   *Refuted by:* a later marker missing, a suppressed nonblocking failure,
   or a nonzero run exit when all blocking gates passed.
   *Basis:* decisions.md, agent-decided enforcement preservation.

7. When verification uses hosted CI or the runner's `--ci` mode, a
   blocking failure does not suppress any later selected gate.
   *Refuted by:* generated workflow steps losing `!cancelled()` or their
   enforcement semantics, matrix fail-fast becoming enabled, or a `--ci`
   run missing a later gate after a blocking failure.
   *Basis:* decisions.md#Q-1; research.md, exhaustive hosted CI.

8. When a local run stops early, the existing repair evidence parser
   extracts the failed gate's command and diagnostic as a blocking failure.
   *Refuted by:* changed start/end frames hiding the failure, or the skip
   summary being parsed as another gate's executed or failed section.
   *Basis:* research.md, red_sections and verify_evidence consumers.

9. When an early-stopped run has working duration storage, its history
   contains measurements only for gates actually executed and ends red.
   *Refuted by:* a duration event for a skipped gate, a green or absent
   run-end record, or measurement-storage failure changing gate enforcement.
   *Basis:* research.md, duration history; decisions.md#Q-1.

10. When the repository's gate list and catalogue are inspected, every
    gate exposes its declared cost, with pytest and the kit probe classified
    as `minutes` and the remaining current gates as `seconds`.
    *Refuted by:* absent or contradictory catalogue costs, pytest or the
    kit probe classified as seconds, or an obsolete claim that pytest must
    run first locally.
    *Basis:* research.md, duration baseline of 2026-11-05;
    decisions.md#Q-1.

11. When the kit transfers its gate list and verification mechanism to
    another repository, that recipient derives the same cheap-first local
    order and stops at the first blocking failure.
    *Refuted by:* a missing transferred dependency, order depending on this
    repository's gate identifiers, or an adopter executing a minutes marker
    after a planted seconds-gate failure.
    *Basis:* decisions.md#Q-1.

## Non-goals

- Speeding up successful gates, reducing test coverage, selecting gates
  from changed files, caching results or promising a total runtime target.
- Changing admission locks, worker sizing, duration storage schema,
  targeted repair scheduling, hosted CI coverage or enforcement levels.
- Automatic cost estimation, additional cost classes or sorting by live
  timings. Future reclassification remains an explicit gate-list edit.
- Migrating sibling repositories or reading or modifying a user-level stop
  hook. Such a hook was not read in this worktree; compatibility beyond the
  repository's output consumers is outside this change.
- Design phase 2b and an ADR draft: this change retains class `bounded`,
  for which the design phase does not run; the held gate-list edit still
  makes the implementation a decision pull request.

## Protected areas

- No edits to gate commands, membership, enforcement or placement; only
  schema version, cost declarations and the obsolete pytest-order reason
  change in the gate list.
- No edits to other changes, existing ADRs, model configuration, tracker,
  admission or duration helpers, workflow prompts, or kit classification.
- One exception (maintainer, 2026-11-11, decisions Q-2): a text elsewhere
  that the early stop makes false is corrected in the same change — the
  local-run line of `prompts/05-verify.md` and the `run_targeted`
  docstring in `scripts/stage2.py`. Text only; no behaviour of the runner
  or the targeted check changes.
- Held paths are never edited by the implementation attempt; the
  orchestrator owns `decisions/gates.yaml` and `.github/workflows/ci.yml`.

## Definition of Done

- `make verify` is green after the orchestrator's schema activation and
  held-file bootstrap, with the planted cheap-failure and all-green proofs.
- `docs/governance/gate-catalog.md` and `.github/workflows/ci.yml` match
  their generators; the gate-list schema and tests migrate together.
- The pull request file list shows the protected scope and non-goals held.
- The decision pull request names and closes the cheap-first verification
  bead, and its last commit carries `Closes-Bead: coding-harness-bxxt.1`.
- Special evidence in the pull request: synthetic local failure, green,
  nonblocking and CI-mode runs, parser/history checks, and transferred-kit
  smoke run, each bound to the tested commit.

## Open decisions

None open. The maintainer's answered cost-field choice is not reopened.

[DETAIL] Use the field `cost` with values `seconds` and `minutes`, and a
stable two-class ordering of selected local gates; ties retain declaration
order because the decision supplies no finer ranking. Sort nonblocking
gates too, preserving their enforcement rather than inventing a third class.

[DETAIL] Keep declaration order for hosted CI and `--ci`; preserve `gates()`
as the declaration-order inventory and derive local scheduling in its one
reader. Reason: local scheduling must not reorder other consumers silently.

[DETAIL] Skipped gates get a summary outside the existing gate-frame format
and no fabricated timing events. Reason: existing diagnostics and measured
history must describe executed commands only.

[DETAIL] A temporary v2 path may keep the implementation attempt testable
against the untouched held list; the orchestrator removes it when activating
schema 3, before final verification. Reason: the accepted attempt precedes
the held-file bootstrap; accepting v2 in the delivered result is forbidden.

[DETAIL] Limit phase 4 to three hours including repairs. Reason: this is a
bounded schema/runner change; reaching the stop calls for reassessment rather
than absorbing the other verification-speed work.
