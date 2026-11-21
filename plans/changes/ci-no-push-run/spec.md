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

1. When a repository declares that `main` moves through a merge queue, its
   generated hosted workflow has no push trigger.
   *Refuted by:* any push trigger remains in the generated workflow, or in this
   repository's committed workflow after its declaration is set.
   *Basis:* decisions.md#Q-1; findings.md F-7.

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
   rules, including first-parent measurement for a hosted push to `main`.
   *Refuted by:* local `main` does not use the first parent, a named branch
   does not use the merge base, a detached checkout at `origin/main` without
   a main-line event does not report not measured, or a detached hosted push
   with `GITHUB_EVENT_NAME=push` and `GITHUB_REF=refs/heads/main` does not
   use the first parent; a main ref without a push event must not select the
   hosted push rule.
   *Basis:* decisions.md#Q-1; research, "What exists today".

8. When the change is complete, `docs/WORKFLOW.md` and the `job:` header
   comment in `decisions/gates.yaml` describe verification on pull requests and
   merge groups and drift on schedule and manual dispatch.
   *Refuted by:* either description omits one of those retained events or
   claims or assumes that this workflow still runs on push.
   *Basis:* decisions.md#Q-1.

9. When the change is complete, the current workflow and interview-check
   descriptions identify the merge-group first-parent measurement and do not
   misdescribe detached merge-group candidates as using the merge base.
   *Refuted by:* `docs/WORKFLOW.md` omits the merge-group first-parent rule,
   or the gate's docstrings, generator comments or generated workflow
   describe the dropped push run as a current run of this workflow or imply
   that every detached checkout uses the merge base.
   *Basis:* decisions.md#Q-1; research, "What exists today".

10. When verification jobs are generated for a repository declaring a merge
    queue, neither event condition includes a push event.
    *Refuted by:* its gate job or `verify` summary still admits push.
    *Basis:* decisions.md#Q-1.

11. When interview-check fixture tests run inside a merge-group workflow,
    inherited GitHub event variables do not change the fixture's intended
    comparison base.
    *Refuted by:* a fixture expecting a branch merge base or an unmeasured
    detached tip instead uses the first parent because it inherited the
    enclosing run's event.
    *Basis:* decisions.md#Q-1; research, "What exists today".

12. When a repository does not declare that `main` moves through a merge
    queue, its generated workflow retains full verification on pushes to `main`.
    *Refuted by:* an absent or false declaration removes the `main` push
    trigger or either verification job excludes push.
    *Basis:* decisions.md#Q-1; findings.md F-7.

13. When the optional CI configuration is malformed or its queue declaration
    has a value other than a boolean, generation and schema validation reject it.
    *Refuted by:* a malformed CI mapping, quoted boolean, null, list or other
    non-boolean value selects a workflow instead of reporting an error.
    *Basis:* findings.md F-7.

## Non-goals

- Changing the gate set, interpreter matrix, live GitHub ruleset, merge
  procedure, or the merge queue's configuration.
- Adding a hosted post-merge run or full verification to manual dispatch.
- Automatically discovering or changing a repository’s merge-queue setting.
  A repository that declares a queue must update its declaration if that
  assumption ceases to hold. The maintainer accepted that no hosted run tests
  `main` after a merge if this repository’s queue is disabled without that
  update. The existing ruleset check also accepts strict up-to-date checks as an alternative, so
  it does not invariably report a disabled queue.
- Measuring external consumers of post-merge commit statuses; the research
  did not measure them.

## Protected areas

The live GitHub ruleset, merge procedure, gate definitions and
`docs/governance/gate-catalog.md` remain unchanged; the decision pull request
changes the declaration and the `job:` header comment in `decisions/gates.yaml`.

## Definition of Done

- `make verify` green after implementation and the held-path bootstrap edits.
- The generated `.github/workflows/ci.yml`, `decisions/gates.yaml` and
  `docs/WORKFLOW.md` move with the code in the same decision pull request.
- The pull request's file list shows the protected areas and non-goals intact.
- The pull request closes the redundant push-run bead (coding-harness-dmmy);
  its last commit carries `Closes-Bead: coding-harness-dmmy`.
- Special runs: none.

## Open decisions

None open.

- [DETAIL] The phase-4 appetite is two hours including repairs; it is a stop
  for this bounded change, not a delivery estimate.
- [DETAIL] The optional `ci.merge_queue` boolean in `decisions/gates.yaml` is
  `true` in this repository; absent or `false` retains the push run. The safe
  default preserves existing kit consumers, while invalid values fail closed.
- [DETAIL] Retain the hosted push-to-main signal alongside the merge-group
  signal because kit repositories without a queue retain a push trigger. A
  main ref without a push event is not that signal.
- [DETAIL] Isolate fixture subprocesses from inherited event variables and
  explicitly set them in event-specific tests, so the real candidate is
  measured without changing the fixture repositories' intended context.
