---
title: "Decisions — drift-lane-branches"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-l54q
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, plans-registry, ci, drift]
---

# drift-lane-branches — Decisions

Class: bounded (bead coding-harness-l54q).

## Correction to the explore

The explore could not read the bead from the tracker and read the folder name as "lane branches drift behind `origin/main`". That is not this change. The bead (created 2026-11-21 at the maintainer's request from the read-only CI research swarm of that day) says:

> Why: the scheduled drift job failed on all 8 nights 2026-11-13..20, each time on the check 'bead is in_progress but has no artefact under plans/changes/' (plans_registry.py, the coupling block), with 10 to 17 beads per run. On 2026-11-21, 24 beads were in_progress; the lane beads among them (for example coding-harness-e82i, coding-harness-ttic, coding-harness-mwzv.4) have their change folder only on their unmerged branch, because the lane model opens the folder in the lane's worktree. The job reads main, so every running lane is reported as drift. An always-red job hides a real case. Some in_progress beads may also be stale claims with no branch at all; that is the real drift the check is meant to find.
>
> What: the check accepts an in_progress bead whose change folder exists on a pushed branch (origin/<branch> refs, read in the drift job after a full fetch), and still reports a bead with no folder on main or on any pushed branch. Then release or close the stale claims the narrowed check still lists (tracker writer's work, not part of the code change).
>
> Done when: a test pins both sides (folder only on a pushed branch: not drift; no folder anywhere: drift), and the drift job is green on a night with only running lanes.

The explore's facts about `scripts/plans_registry.py`, `scripts/_verdict.py`, `scripts/ci_gates.py` and the drift job stay useful; its open questions 1–3 and 5 concern a different topic and are closed by this record.

## SKIP · interview

status: skipped
reason: The bead description above fixes the problem, the remedy and the done condition; the maintainer approved creating it on 2026-11-21 (chat, answer 8: "ja, als P2") and asked for no question windows until the block on 2026-11-23 10:00. No choice is left for the interview; the details are [DETAIL] items below, and the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Where the change lands: the reverse-coupling block of `scripts/plans_registry.py`** (the `in_progress` beads without artefact). A bead counts as having an artefact when a file under `plans/changes/` on the checked tree names it in its `bead:` header, as today, or when such a file exists on any remote-tracking branch `refs/remotes/origin/*`. Reason: the bead's "What"; one place, no second check.
- **How the branches are read.** One bounded read per run: list the remote-tracking refs, let `git grep` per ref narrow the candidate files under `plans/changes/`, then read each candidate with `git show` and apply the checked-tree interpretation (spec-review S-8); never a checkout. Reason: the job must stay cheap and must not change the tree it checks.
- **What the verdict says.** A bead whose folder exists only on a branch is not DRIFT; the INFO summary line names how many running beads were found on branches (and the first few branch names). A bead with no folder on the tree or any remote branch stays DRIFT with today's message. Reason: keeps the real case visible and explains a green run.
- **No remote refs present.** When the checkout has no remote-tracking refs at all, the check behaves exactly as today and says so in an INFO line. Reason: local runs and shallow clones must not change meaning silently.
- **The drift job fetches the branches.** The generator `scripts/ci_gates.py` adds a step to the drift job that fetches `+refs/heads/*:refs/remotes/origin/*` before the strict check; `.github/workflows/ci.yml` is regenerated, never hand-edited (the `ci-drift` gate). Reason: the job's default checkout holds only the triggering ref.
- **Stale claims are tracker work, not code.** Releasing or closing in_progress beads the narrowed check still lists is done by the tracker writer after the merge and is not part of the diff. Reason: the bead says so.
- **Tests.** Both sides pinned in `tests/test_plans_registry.py` (or the file that holds the coupling tests): folder only on a remote-tracking branch is not DRIFT; no folder anywhere is DRIFT; no remote refs keeps today's behaviour. Plus the generator test that the drift job fetches branches. Reason: the bead's done condition.
