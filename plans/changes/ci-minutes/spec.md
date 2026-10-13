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
push without a pull request starts nothing, a pull request runs only for its
newest commit, and every run checks one interpreter, Python 3.12 (bead
coding-harness-cac). Research: `research.md`. Decisions: `decisions.md`.

> Amended 2026-10-13: maintainer decided 3.12 only. The per-event matrix of
> the first draft (pull requests on 3.12, `main` on 3.11 and 3.12) is
> replaced by one interpreter everywhere (`decisions.md`, addendum).
> Criteria 2, 3 and 8, the non-goals and the Definition of Done carry the
> marker where they changed; criteria 1 and 4–7 stand as first written.

## Problem

- GitHub stopped starting jobs on 2026-10-13 (failed payment or spending
  limit). Over the last 100 runs, measured by the maintainer on 2026-10-13,
  61 successful runs came from `push` and 8 from `pull_request`, about 3.5
  minutes each, on two legs (bead coding-harness-cac).
- Every push to every branch starts the workflow, and a push to a branch with
  an open pull request starts it twice: `generate_ci` in
  `scripts/ci_gates.py` writes a bare `push:` and a bare `pull_request:`
  (`research.md`, "What exists today", read at `14f6e1a`).
- Every run runs both interpreters, 3.11 and 3.12: the matrix is the
  literal `tools.python` list for every event (same source). (amended
  2026-10-13: maintainer decided 3.12 only — lakeswitch-ai enforces 3.12 as
  well, so a 3.11 leg checks an interpreter no repository of the maintainer
  targets.)
- A newer push to a pull request never cancels the older run:
  `cancel-in-progress: false` for every event (same source).

## Acceptance criteria

1. When the generator writes the workflow, its `push` trigger carries exactly
   the branch filter `branches: [main]`, and its `pull_request` trigger stays
   without any filter.
   *Refuted by:* a bare `push:`, a push filter naming another branch or a path,
   or a `branches`, `paths` or `types` key on `pull_request`.
2. (amended 2026-10-13: maintainer decided 3.12 only) When the workflow runs
   on `push` or `pull_request`, the matrix job has exactly the legs
   `tools.python` declares, and `tools.python` declares no 3.11.
   *Refuted by:* a 3.11 leg, a declared 3.11, or a matrix that does not follow
   a changed `tools.python`.
3. (amended 2026-10-13: maintainer decided 3.12 only) When the repository
   states its oldest supported interpreter, `pyproject.toml`
   (`requires-python`), `ruff.toml` (`target-version`) and the first entry
   of `tools.python` name the same version.
   *Refuted by:* `requires-python = ">=3.11"`, `target-version = "py311"`, or
   any of the three disagreeing with the others.
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
8. (amended 2026-10-13: maintainer decided 3.12 only) When a reader looks up
   which event runs what, `decisions/gates.yaml` (its header comment) and
   `docs/WORKFLOW.md` §3 ("Verification runs through git and CI, not through
   the harness") say: a push runs CI only on `main`, a pull request cancels
   its superseded runs, the schedule runs only the drift gates; and no
   document or comment of this repository outside sample data and history
   says the repository is checked under 3.11.
   *Refuted by:* a comment still saying "per push/PR", or the comment in
   `scripts/check_research_currency.py` still saying the repository "is
   checked under 3.11 too".

## Non-goals

- A self-hosted runner (rejected by the maintainer on 2026-10-13).
- More gate legs on the nightly schedule (moot since the amendment of
  2026-10-13: one interpreter).
- A new key or schema version in `decisions/gates.yaml`.
- (amended 2026-10-13: maintainer decided 3.12 only) Regenerating
  `requirements-ci.txt`: it carries no interpreter marker and already
  installs on 3.12 (`research.md`, amendment).
- (amended 2026-10-13) In `tools/cloud-env/`, lakeswitch-ai's interpreter
  (3.11), which moves with lakeswitch-ai-6sj. This repository's own `.venv`
  there is built with 3.12, the floor (round 1, L1-1).
- (amended 2026-10-13) Sample interpreter lists in tests and in the schema's
  error text: 3.11 there is data, not a claim about this repository.
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
- `requirements-ci.txt`: not regenerated (amended 2026-10-13).

## Definition of Done

- `verify` green.
- Moved in the same pull request: `.github/workflows/ci.yml` (regenerated),
  `decisions/gates.yaml` (`tools.python` and its comments),
  `pyproject.toml` (`requires-python`), `ruff.toml` (`target-version`), the
  comment in `scripts/check_research_currency.py`, `docs/WORKFLOW.md` (one
  sentence). (amended 2026-10-13: maintainer decided 3.12 only)
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes coding-harness-cac, and its last commit
  carries the trailer `Closes-Bead: coding-harness-cac`
  (`prompts/07-commit.md`).
- Special runs: the first hosted run on the pull request shows one leg
  (3.12), and so does the push run after the merge (amended 2026-10-13) —
  its link in the bead's closing note, or "not observed" if GitHub still
  starts no jobs.

## Open decisions

None open. The measures were the maintainer's (2026-10-13), the one
interpreter included (amended 2026-10-13: maintainer decided 3.12 only); the
remaining points are `[DETAIL]` decisions with their reasons in
`decisions.md`, addendum.
