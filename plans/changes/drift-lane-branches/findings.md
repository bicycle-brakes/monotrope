---
title: "Findings — drift-lane-branches"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-l54q
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — drift-lane-branches

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1150 files, 5132 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1153 files, 5138 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | spec.md AC 7; `scripts/ci_gates.py` `_schritt` (line 649) | [AMBIGUITY] Every generated gate step carries `if: ${{ !cancelled() }}`, so by default a failed fetch step is followed by the strict check anyway. After `actions/checkout`, `refs/remotes/origin/main` already exists, so neither AC 4 (no refs → INFO) nor AC 6 (enumeration/read failure → BLOCK) notices that only one branch was fetched. AC 7 can then be met in two ways. (a) The strict step is skipped or held back on the fetch outcome: that night's other registry findings (forward coupling, staleness, built-not-archived) go unmeasured, and the job is red only through the fetch step. (b) The fetch failure is handed to the registry check, which BLOCKs and still reports its other findings. The spec names neither and does not say whether the job must end red. | Opus | open | — |
| S-2 | MAJOR | SPEC | base | spec.md AC 6 (vs AC 5/7, which are scoped to the drift job); `decisions/gates.yaml` `plans-registry`; `.github/workflows/ci.yml:31` | [AMBIGUITY] The same `check()` also runs as the non-strict PR gate `plans-registry` (verify job, enforcement block, needs_tracker) on every pull_request, push and merge_group. That job checks out with `fetch-depth: 0`, so it sees every origin branch. It also runs in local `make verify`. Reading (a): the branch search always runs inside `check()`, so a git failure BLOCKs every unrelated PR and every local verify. That includes runs where all running beads already have a checked-tree artefact, or the tracker is unmeasurable. Reading (b): the search runs only under `--strict`/the drift job, or only when some running bead lacks a checked-tree artefact. In that case a failure never reaches the PR gate. | Opus | open | — |
| S-3 | MAJOR | SPEC | base | spec.md AC 4 vs AC 6 | [AMBIGUITY] What counts as a "failure" is undefined. (i) A root that is not a git repository, or a machine without a git binary (the fixture-REPO seam in `plans_registry.py`, an exported tarball): reading (a) is "no origin remote-tracking branches" → checked-tree behaviour plus INFO (AC 4); reading (b) is failed enumeration → BLOCK (AC 6). (ii) A `plans/changes/` file on a branch whose frontmatter does not parse: reading (a) ignores it as not an artefact; reading (b) BLOCKs, as on the checked tree, or as "reading a branch fails". Under the BLOCK readings, one malformed draft on any lane branch turns the gate red. | Opus | open | — |
| S-4 | MAJOR | SPEC | base | spec.md AC 5; decisions.md "The drift job fetches the branches"; `scripts/ci_gates.py` `generate_ci` (lines 845–858) | Hole: the generator builds drift-job steps only from gates.yaml rows plus fixed preconditions (checkout, toolchain, tracker hydration triggered by `needs_tracker`). The spec does not say where the fetch is declared: a new gate field like `needs_tracker`/`needs_history` (gates.yaml schema, `validate_schema`, local runner) or hard-coded in `generate_ci`. It is also silent on the local run of `plans-registry-strict` (`placement: both`). Without a fetch there, the check searches stale or never-fetched local remote-tracking refs and reports the result as complete, which is exactly what AC 6/7 forbid in CI. | Opus | open | — |
| S-5 | MAJOR | SPEC | base | spec.md Definition of Done items 1 and 4; Non-goals item 3 | [AMBIGUITY] The pull request closes `coding-harness-l54q` at merge. Scheduled runs happen only on main after the merge, and a night "with only running-lane claims" also needs the stale-claim cleanup, which is a non-goal done after the merge. Reading (a): done = merged, and the live run is recorded later in a follow-up whatever it shows. Reading (b): the bead's own done condition ("the drift job is green on a night with only running lanes") must be seen before the bead counts as closed. "Demonstrates the live outcome" also leaves the outcome open. It could mean a green job, or only that no bead with a pushed-branch artefact appears among the DRIFT lines while the job stays red for other drift (Non-goals item 3). | Opus | open | — |
| S-6 | MINOR | SPEC | base | spec.md AC 2/3; `scripts/plans_registry.py:428` | Hole: the spec is silent on today's INFO line "N running beads checked, M without artefact". M could still count branch-only beads (checked tree only) or count only beads with no artefact anywhere. Tests that pin this line would differ. | Opus | open | — |
| S-7 | MINOR | SPEC | base | spec.md AC 3; Open decisions [DETAIL] 2 | AC 3 cannot go red on its bound: "bounded sample" has no number and no order, so printing every branch name passes. The spec also leaves open which name is shown for a bead found on several branches. It does not say whether `origin/HEAD` (a symref) or `origin/main` count as branches for the count and the examples. On a run dispatched from another ref, `origin/main`'s artefacts are not checked-tree matches. | Opus | open | — |
| S-8 | MINOR | SPEC | base | spec.md Terms "Branch artefact"; decisions.md "How the branches are read" | [AMBIGUITY] The spec defines a branch artefact by the checked-tree interpretation: a frontmatter block from line 1, parsed as YAML, read through its `bead` value, `_*.md` excluded, `archive/` included. decisions.md names a `git grep` for `bead:` lines instead. The two readings disagree on a `bead:` line in a file body or code fence, on a quoted or aliased value, on unparseable frontmatter, and on `_`-prefixed files. In each case the same bead is either satisfied or reported as drift. | Opus | open | — |
