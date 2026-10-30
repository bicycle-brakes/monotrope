---
title: "Spec — merge-queue"
status: draft
implementation_status: none
date: 2026-10-30
last_reviewed: 2026-10-30
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-eh42
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-30"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, merge-queue, github-actions, decision-pr]
class: bounded
appetite: 2
adr_files: []
neighbours:
  - plans/changes/archive/2026-10-08-rb-g7-merge-freshness/spec.md
  - plans/changes/index-merge-regenerates/spec.md
  - plans/changes/harness-decide-adr/spec.md
  - plans/changes/ci-minutes/spec.md
  - plans/changes/hermes-runner/spec.md
---

# Spec — merge-queue

GitHub's hosted merge queue checks the merge result against current `main`
without requiring a fresh pull-request head after each preceding merge
(bead coding-harness-eh42 — replace repeated branch updates with queued merges).
Inputs: [research](research.md) and [decisions](decisions.md).

## Problem

- A merge advances `main` and leaves other pull requests behind; updating
  their branches changes the heads against which auto-merge was armed.
  The research's orchestrator addendum records this on 2026-10-27/28 and
  repeated updates during eight sequential merges on 2026-10-30.
- The generated workflow accepts no `merge_group` event, and both its gate
  job and required summary check exclude that event. Enabling the queue
  alone would leave its required check absent (research, "What exists today";
  draft addendum measured at `bdfbe53f`, 2026-10-30).
- The local ruleset check and current merge instructions recognise only
  branch freshness. They would reject or work around the chosen queue
  (research, "The ruleset floor test" and orchestrator addendum).

## Terms

**Merge group:** GitHub's temporary merge candidate, incorporating the
current target branch, on which the queue requests checks.

**Freshness requirement:** the merge result must be tested; supplied either
by an active merge queue or by required checks with the strict up-to-date flag.

## Acceptance criteria

1. When active default-branch rules supply either a merge queue or the
   existing strict up-to-date requirement, the local ruleset check accepts
   the freshness requirement.
   *Refuted by:* otherwise valid rules fail solely because they use the queue,
   or the existing strict configuration stops passing during the transition.

2. When neither freshness alternative is present, the local ruleset check
   reports a finding identifying the missing protection.
   *Refuted by:* neither alternative is present and the check passes; a false,
   absent, null or string strict flag without a queue counts as missing.

3. When a ruleset supplies the merge-queue alternative, its bypass list is
   subject to the same fail-closed measurement as every existing supplier.
   *Refuted by:* a queue-only supplier has bypass actors or an unreadable or
   missing bypass list or detail, yet measurement passes, including when it
   is separate from the ruleset supplying required checks.

4. While the merge queue supplies freshness, every other existing ruleset
   floor requirement remains enforced.
   *Refuted by:* the queue makes a missing pull-request requirement, missing
   or unpinned `verify`, force pushes, deletions, a supplier bypass or a
   failed measurement acceptable.

5. When GitHub requests merge-group checks, the generated hosted workflow
   runs the existing verification gates on that group's merge candidate.
   *Refuted by:* no applicable trigger exists, the gate job excludes the
   event, or checkout/tests use a pull-request head or another ref instead.

6. When verification of a merge group fails, is cancelled or is skipped,
   the required `verify` summary check cannot report success.
   *Refuted by:* the summary is skipped on that event or passes for any gate
   result other than success; a successful group must still pass normally.

7. When the queue is active, the current governance, hosting template and
   merge procedure consistently describe queue admission without a
   preparatory branch update, preserving the maintainer's merge authority
   and the exact-head check.
   *Refuted by:* a current instruction requires `update-branch` for queue
   admission, permits an unrequested decision merge or bypass, drops
   `--match-head-commit`, or describes enqueueing as a completed merge.

8. While the decision pull request is unmerged, the live ruleset remains
   unchanged by this change.
   *Refuted by:* the queue or strict flag is changed before the maintainer
   merges the decision pull request.

9. When the approved switch is applied after that merge, the live default
   branch uses a merge-commit queue with build and merge groups of one.
   *Refuted by:* the queue is absent, a group can contain multiple pull
   requests, a different merge method is configured, or required `verify`
   does not run successfully on an actual merge-group candidate.

## Non-goals

- A repository-local queue, scheduler or new merge service.
- New permission to merge, unattended decision merges, admin bypass or
  changes to merge-command guards.
- Changes to the sync helper, auto-merge arming policy, nightly scheduling,
  interpreter matrix, CI cost policy or tracker closure machinery.
- Reconfiguring other repositories or changing architecture decisions.
  This bounded change has no design phase or ADR draft.

## Protected areas

`scripts/pr_sync.py` and `tests/test_pr_sync.py` belong to the neighbouring
sync change. Merge guards, `decisions/gates.yaml`, endpoint configuration,
tracker data and existing ADRs keep their contracts. Runner-held paths
needed for criterion 7 and the generated workflow are orchestrator-owned
bootstrap edits after the accepted implementation attempt.

## Definition of Done

- `make verify` is green after code, tests and orchestrator edits land together.
- The same decision pull request updates `docs/governance/regelwerk.md`,
  `docs/governance/quality-gates.md`, `docs/WORKFLOW.md`,
  `prompts/07-commit.md`, `templates/repo-settings.md` and the generated
  `.github/workflows/ci.yml`; no ADR is due.
- Its file list respects the protected areas and non-goals.
- The orchestrator records the post-merge ruleset readback and a hosted
  merge-group run with its commit; local fixtures alone do not establish
  live activation. Task closure follows that evidence, not queue admission.
- The pull request names bead coding-harness-eh42 — the merge-queue switch;
  the final completion commit carries its `Closes-Bead` trailer.

## Open decisions

None open. The maintainer's prior approval and reasoned interview skip are
recorded in `decisions.md`; merging the decision pull request confirms the rule change.

- [DETAIL] The phase-4 appetite is two hours including repairs, a stop rather
  than an estimate; no earlier appetite is stated in the inputs.
- [DETAIL] Keep the legacy freshness alternative for a safe transition and
  for kit repositories without a queue; disable its strict flag here only
  after activating the queue, avoiding the repeated-update requirement.
- [DETAIL] Synchronise the current quality-gates explanation as well as the
  rulebook; it explicitly describes the branch-update procedure being replaced.
- [DETAIL] Leave queue timeout and other unrelated hosting options at the
  host's existing/default values; only singleton groups and merge commits
  are selected, as `decisions.md` already specifies.
