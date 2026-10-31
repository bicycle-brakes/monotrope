---
title: "Spec — repair-targeted-check"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-gxwg
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, repair, verification]
class: bounded
appetite: 3
adr_files: []
---

# Spec — repair-targeted-check

Runner repairs pass targeted post-run checks, followed by full verification
before phase 6 (bead `coding-harness-gxwg` — shorten runner repair cycles).
Research: `research.md`. Authority and scope: `decisions.md`, including its
reasoned interview skip and three draft details.
This remains a proposed, unimplemented change against `9eae5d26`
(2026-10-31); the earlier draft's failed check is not implementation evidence.

## Problem

- Every runner repair currently pays for full `make verify`, even for a
  narrow edit: `run_attempts()` always calls the full `verify_attempt()`.
  The exploration of 2026-10-31 cites a measured 12–13-minute full check on
  2026-10-30 and the maintainer's targeted-check rule for hand repairs.
- The interview extends that rule to runner repairs, while the workflow
  still says runner repairs retain full verification. Existing cheap checks
  select tests from edits and the criterion ledger, rather than all linked
  test files. The touch map reads committed objects and misses new links in
  uncommitted repairs (`research.md`, exploration and draft gap checks).
- Phase 6 currently starts without independently enforcing full verification
  on the current head. Replacing repair verification alone would leave that
  final safety boundary unenforced (`research.md`, draft gap checks at
  baseline `9eae5d26`, 2026-10-31).

## Terms

**Touched paths:** the repair's changes against its starting head, including
index-only changes, working-tree edits, untracked files and both names of a
rename; retained edits from earlier attempts remain in scope.

**Linked tests:** test files linked directly to touched paths by the touch
map's existing naming/import rules, using working-tree content and baseline
links for removed paths. These are heuristic links, not complete dependency
analysis.

**Targeted check:** touched and linked test files, existing accepted-ledger
and retry test selections, lint and format checks of touched Python files,
and the existing local gates applicable to the touched file kinds.

## Acceptance criteria

1. When a runner repair has determinable targeted coverage, its post-run
   verification uses the targeted check instead of full `make verify`.
   *Refuted by:* a narrow, covered Python repair invoking full verification.

2. When a targeted repair is checked, every surviving touched test file and
   every surviving linked test file is executed in full from current content.
   *Refuted by:* an unchanged linked test's failing sibling being omitted,
   an untracked or index-only touch being missed, a removed path losing its
   baseline-linked tests, or a retry losing an earlier retained edit.

3. When a repair touches surviving Python files, read-only ruff lint and
   format checks cover those files after the runner's existing formatting.
   *Refuted by:* accepting a touched file with a remaining lint or format
   fault because it was outside the check's targets.

4. When targeted verification runs, it measures the existing locally
   runnable gates applicable to the touched file kinds with their declared
   enforcement unchanged.
   *Refuted by:* omitting the document gates after derived plan/index edits,
   omitting a changed gate's own check, or treating an unmeasured blocking
   gate as passing.

5. If a repair touches `prompts/` or its targeted coverage cannot be
   determined safely, full `make verify` is required for that attempt.
   *Refuted by:* targeted acceptance of a prompt edit, an unclassified input,
   an unreadable link inventory or production code with no linked test.

6. When targeted post-run commands execute, they run outside the
   machine-wide verify admission.
   *Refuted by:* a targeted command acquiring or claiming inherited ownership
   of that admission; full fallback and phase-6 checks still owe admission.

7. If a required targeted command fails, cannot start or exceeds its time
   bound, the repair cannot checkpoint or mark its findings fixed.
   *Refuted by:* a checkpoint or fixed row despite that failure, or an
   unbounded/unprotected diagnostic reaching the existing retry flow.

8. When repair uses targeted verification, the existing preparation,
   accepted-ledger/retry selections, fixed-line validation and red-first
   proof remain prerequisites for its checkpoint.
   *Refuted by:* a missing derived refresh, a planted ledger-selected failure
   being skipped, acceptance of an invalid fixed answer, or a proof failure
   becoming a fixed row merely because targeted commands passed.

9. When phase 6 is requested, the runner obtains a fresh green full
   `make verify` for the current head before starting the reviewer.
   *Refuted by:* a reviewer call after a red, unstartable or timed-out full
   check, after the checked head or substantive tree changed, or using only
   an earlier repair's green result.

10. When implement or draft runs, its existing verification scope and
    admission behavior remain unchanged.
    *Refuted by:* implement checkpointing after targeted checks alone, or
    draft losing its existing document/full verification choice.

11. When a repair's verification finishes, its runner-owned evidence names
    the verification mode, selected checks and result without presenting
    targeted success as full verification.
    *Refuted by:* a successful repair checkpoint with no such evidence, an
    unreported fallback reason, or targeted output claiming full green.

## Non-goals

- No new gate, gate-schema change, CI reduction, model route, retry count,
  review approval or automatic pull-request publication.
- No automated hand-repair command, new loop status or verification receipt.
  The orchestrator still owns hand-repair row bookkeeping and a full check
  on the final head before a pull request leaves draft.
- No complete dependency graph, transitive test analysis or change to the
  committed-object touch-map CLI; conservative full fallback covers inputs
  outside the targeted selector's supported kinds.
- No redesign of machine admission or of the existing admitted red-first
  proofs. Only targeted post-run verification bypasses that admission.
- No design phase or ADR: the recorded bounded class changes the runner's
  existing post-run choice, using existing checks and the phase-6 boundary.

## Protected areas

- `decisions/gates.yaml`, `.github/`, `provenance.yaml`, model configuration
  and tracker data: their definitions and authority remain unchanged.
- Held instructions are edited only by the orchestrator after the accepted
  implementation attempt; this draft changes no held path.
- Other changes' historical artifacts and ledgers retain their evidence;
  the repair-only exception is documented in the current workflow instead.

## Definition of Done

- The criterion tests and full `make verify` pass on the implementation head.
- The same pull request aligns `docs/WORKFLOW.md`, `AGENTS.md`,
  `prompts/04-implement.md` and `prompts/04b-review-loop.md` with targeted
  runner repairs and full verification before phase 6; no ADR is touched.
- The pull request's file list respects the protected areas and non-goals.
- The pull request closes the runner-targeted-check work item, and its last
  commit carries `Closes-Bead: coding-harness-gxwg`.
- Special runs: none; offline command-capture tests establish selection and
  ordering without starting foreign models or repeatedly running full verify.

## Open decisions

None open. The following reversible details are chosen explicitly for this
change; none records a maintainer answer.

- [DETAIL] Set the phase-4 appetite to three hours including repair rounds,
  as a stop rather than a duration prediction, for the selector and boundary
  regressions within this bounded change.
- [DETAIL] Full phase-6 verification runs synchronously on every `review`,
  including a re-check, rather than trusting a saved receipt; this needs no
  new durable state and always checks the head being reviewed.
- [DETAIL] Reuse existing link rules with a working-tree adapter; use
  baseline links for removals and fall back to full verification for unsafe
  or unsupported selection. This avoids promising complete dependency
  discovery while keeping new and deleted repair inputs visible.
- [DETAIL] Select existing gates by identifier and file kind, obtaining
  commands and enforcement from the one gate list. Conservatively include
  the document subset for runner metadata changes rather than inventing a
  second command list or weakening any gate.
