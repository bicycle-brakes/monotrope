---
title: "Spec — ci-no-push-run"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-dmmy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, ci, merge-queue]
class: bounded
appetite: 2
adr_files: []
---

# Spec — ci-no-push-run

The hosted checks run before a queued merge without repeating the full run on
the subsequent push to `main` (bead coding-harness-dmmy — remove the redundant
push run). Inputs: [research](research.md) and [decisions](decisions.md).

## Problem

- As recorded on 2026-11-21, the workflow starts full verification on the
  pull request, merge group and push to `main`; a sample of 200 runs from
  2026-11-12 through 2026-11-21 had a median of about 25 minutes per run
  (decisions, introduction). The push repeats a merge-group check: the
  recorded example used the same commit for both events (decisions, Q-1).
- The interview minimums check uses the first parent for a hosted `main`
  push but the merge base for a merge group (research, "What exists today",
  2026-11-21). Removing the push without transferring that measurement would
  remove the hosted first-parent check of the landed change.

## Terms

**Merge group:** the queue's merge candidate on which GitHub requests checks.
**First parent:** the candidate commit's `HEAD^`, the comparison base used for
the main-line landfall.

## Acceptance criteria

1. When a commit is pushed, the generated hosted workflow has no push trigger.
   *Refuted by:* a push trigger remains, including a filtered or empty one.
   *Basis:* decisions.md#Q-1.

2. When a pull request or a merge group requests checks, the hosted workflow
   runs the existing full verification on that event's candidate.
   *Refuted by:* either trigger, the gate job, or candidate checkout is missing
   or excludes that event.
   *Basis:* decisions.md#Q-1.

3. When a pull-request or merge-group gate job fails, is cancelled or is
   skipped, its required `verify` summary cannot report success.
   *Refuted by:* a non-successful gate job produces a successful summary, or
   the summary is absent on either event; a successful gate job must pass.
   *Basis:* decisions.md#Q-1.

4. When the scheduled or manually dispatched workflow runs, it runs only the
   existing drift job.
   *Refuted by:* either event is absent or starts a full verification job, or
   the drift job no longer runs on either event.
   *Basis:* decisions.md#Q-1.

5. When a newer pull-request run supersedes an older run of the same pull
   request, the older run is cancelled.
   *Refuted by:* superseded pull-request runs remain active or the grouping
   separates runs of the same pull request.
   *Basis:* decisions.md#Q-1; research, "What exists today".

6. When the interview minimums check runs on a merge-group candidate, it
   compares the candidate with its first parent.
   *Refuted by:* a merge-group run uses the merge base or another commit as
   its base, including on a detached checkout.
   *Basis:* decisions.md#Q-1.

7. When the interview minimums check runs outside a merge-group event, it
   retains the existing local main, named-branch and detached-checkout base
   rules, except that a `GITHUB_REF` pointing to `main` alone no longer
   identifies a hosted main-line run.
   *Refuted by:* local `main` does not use the first parent, a named branch
   does not use the merge base, or a detached checkout at `origin/main`
   silently passes instead of reporting not measured without a merge-group
   event.
   *Basis:* decisions.md#Q-1; research, "What exists today".

8. When the change is complete, the current workflow description and gate
   catalog comment describe the retained events and the merge-group
   first-parent measurement.
   *Refuted by:* `docs/WORKFLOW.md` or the `decisions/gates.yaml` header
   still claims that a push starts verification, or the workflow describes
   the former hosted push as the first-parent run.
   *Basis:* decisions.md#Q-1.

## Non-goals

- Changing the gate set, interpreter matrix, live GitHub ruleset, merge
  procedure, or the merge queue's configuration.
- Adding a hosted post-merge run or full verification to manual dispatch.
- Guaranteeing coverage when the merge queue is disabled. The maintainer
  accepted that no hosted run then tests `main` after a merge. The existing
  ruleset check also accepts strict up-to-date checks as an alternative, so
  it does not invariably report a disabled queue.
- Measuring external consumers of post-merge commit statuses; the research
  did not measure them.

## Protected areas

The live GitHub ruleset and merge procedure remain unchanged; the decision
pull request changes the gate catalog's comment, not its gate definitions.

## Definition of Done

- `make verify` green after implementation and the held-path bootstrap edits.
- The generated `.github/workflows/ci.yml`, `decisions/gates.yaml` and
  `docs/WORKFLOW.md` move with the code in the same decision pull request.
- The pull request's file list shows the protected areas and non-goals intact.
- The pull request closes the redundant push-run bead (coding-harness-dmmy);
  its last commit carries `Closes-Bead: coding-harness-dmmy`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The phase-4 appetite is two hours including repairs; it
is a stop for this bounded change, not a delivery estimate.
