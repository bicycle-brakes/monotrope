---
title: "Spec — ci-minutes"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-cac
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, ci, github-actions]
class: bounded
appetite: 2
---

# Spec — `ci-minutes`

After this change the hosted CI runs only where its result is used: a branch
push without a pull request starts nothing, a pull request runs one
interpreter and only for its newest commit, and `main` keeps the full check
(bead coding-harness-cac). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- GitHub stopped starting jobs on 2026-10-13 (failed payment or spending
  limit). Over the last 100 runs, measured by the maintainer on 2026-10-13,
  61 successful runs came from `push` and 8 from `pull_request`, about 3.5
  minutes each, on two legs (bead coding-harness-cac).
- Every push to every branch starts the workflow, and a push to a branch with
  an open pull request starts it twice: `generate_ci` in
  `scripts/ci_gates.py` writes a bare `push:` and a bare `pull_request:`
  (`research.md`, "What exists today", read at `14f6e1a`).
- Every pull-request run runs both interpreters, 3.11 and 3.12: the matrix is
  the literal `tools.python` list for every event (same source).
- A newer push to a pull request never cancels the older run:
  `cancel-in-progress: false` for every event (same source).

## Acceptance criteria

1. When the generator writes the workflow, its `push` trigger carries exactly
   the branch filter `branches: [main]`, and its `pull_request` trigger stays
   without any filter.
   *Refuted by:* a bare `push:`, a push filter naming another branch or a path,
   or a `branches`, `paths` or `types` key on `pull_request`.
2. When the workflow runs on `pull_request`, the matrix job resolves to
   exactly one leg, the last interpreter `tools.python` declares.
   *Refuted by:* two legs on a pull request, or a leg other than the last
   declared interpreter, also after `tools.python` changes.
3. When the workflow runs on `push`, the matrix job resolves to every
   interpreter `tools.python` declares, in the declared order.
   *Refuted by:* one leg on a push to `main`, or a list that does not follow a
   changed `tools.python`.
4. If a newer `pull_request` run of the same pull request starts, the older
   run is cancelled; a `push` run is never cancelled. The concurrency group
   still carries the event name and the ref.
   *Refuted by:* `cancel-in-progress` true on `push`, false on
   `pull_request`, or a group without `github.event_name` or `github.ref`.
5. While the run is a `schedule` or `workflow_dispatch` run, only the `drift`
   job runs, on the last declared interpreter, as before this change.
   *Refuted by:* the matrix job or the summary job running on the schedule.
6. When the workflow runs on `push` or `pull_request`, the required check
   `verify` still needs the matrix job and passes only when every leg of that
   run passed.
   *Refuted by:* `verify` passing with a failed, cancelled or skipped leg.
7. When the change is merged, the committed `.github/workflows/ci.yml` is
   byte-identical to `python3 scripts/ci_gates.py --generate-ci`.
   *Refuted by:* the `ci-drift` gate red.
8. When a reader looks up which event runs what, `decisions/gates.yaml` (its
   header and `tools` comments) and `docs/WORKFLOW.md` §3 ("Verification runs
   through git and CI, not through the harness") say: push to `main` runs
   every interpreter, a pull request runs the last one and cancels its
   superseded runs, the schedule runs only the drift gates.
   *Refuted by:* a comment still saying "per push/PR" or "once per entry"
   without the pull-request exception.

## Non-goals

- A self-hosted runner (rejected by the maintainer on 2026-10-13).
- More gate legs on the nightly schedule (`decisions.md`, the schedule
  stays as it is).
- A new key or schema version in `decisions/gates.yaml`.
- A configurable default-branch name for repositories that take the kit;
  it comes back when a kit repository's default branch is not `main`.
- Path filters that skip CI for text-only pull requests: the pull request
  stays the gate of a text-only change (`AGENTS.md`).
- Changing the ruleset on `main` or its required check.

## Protected areas

- `tests/test_repo_settings.py` and the ruleset: the required check `verify`
  is unchanged.
- The `pull_request` trigger's checkout of the merge ref (RB-G7,
  `_merge_ref_findings` in `tests/test_ci.py`): untouched.
- The gate list in `decisions/gates.yaml`: no gate added, removed or moved.

## Definition of Done

- `verify` green.
- Moved in the same pull request: `.github/workflows/ci.yml` (regenerated),
  `decisions/gates.yaml` (comments only), `docs/WORKFLOW.md` (one sentence).
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes coding-harness-cac, and its last commit
  carries the trailer `Closes-Bead: coding-harness-cac`
  (`prompts/07-commit.md`).
- Special runs: the first hosted run on the pull request shows one leg
  (3.12), and the push run after the merge shows two — its link in the bead's
  closing note, or "not observed" if GitHub still starts no jobs.

## Open decisions

None open. The three measures were the maintainer's (2026-10-13); the
remaining points are `[DETAIL]` decisions with their reasons in
`decisions.md` — notably that the nightly schedule stays unchanged, because it
runs no gate legs today and every merge to `main` already runs both.
