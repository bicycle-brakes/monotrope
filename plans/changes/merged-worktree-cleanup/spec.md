---
title: "Spec — merged-worktree-cleanup"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, worktrees]
class: bounded
adr_files: []
---

# Spec — merged-worktree-cleanup

Provide an explicit way to retire finished, safe-to-remove worktrees and their local branches (bead coding-harness-bxxt.4 — merged worktree cleanup). Research: `research.md`. Decisions: `decisions.md`; review dispositions: `findings.md`, phase 2a.

## Problem

- Worktree removal after merge is a manual rule; neither the session guard nor the post-merge cleanup sequence carries it out (`research.md`, 2026-11-22).
- The 2026-11-21 machine snapshot recorded 117 registered worktrees; the work item records disk pressure from accumulated worktrees on 2026-11-09 (`research.md`, `decisions.md`).

## Terms

**Merged pull request:** a merged pull request in the origin repository whose head branch name and head commit exactly match the local branch and its current tip, and whose tip is an ancestor of freshly fetched `origin/main`.

**Pushed:** the local tip equals or is an ancestor of its fresh `origin/<branch>` remote-tracking tip; if that branch ref is absent after a successful pruning fetch, a matching merged pull request proves the local tip landed. An upstream of `origin/main` is not the branch's own remote ref. A configured branch-specific upstream that cannot be resolved is not evidence of a push; the gone-ref case still requires the matching merged pull request.

**Clean:** no staged, unstaged, or untracked non-ignored changes, and no merge, rebase or cherry-pick in progress.

**In use:** a process belonging to the invoking user has its working directory in the worktree or below it, or a lane busy marker records that worktree path. Every report header states that processes owned by other users are outside this check.

**Safety checks:** a fresh pruning fetch and readable origin/main; registered worktree and nesting inspection; branch attachment and protection; merged pull request and ancestry; pushed state; cleanliness and operation state; lock; invoking-user process working directories; and lane busy markers. A command error or unreadable answer is a failed check; a successfully determined disqualifying state is a keep reason, not a failure. Global checks run first; for each registration the applicable checks run until a keep reason is established, with nested registrations identified before evaluating candidates. A missing prunable directory is assessed as a registration, not as a present worktree.

**Busy marker:** every `busy/*` marker under every run directory in `${XDG_STATE_HOME:-~/.local/state}/coding-harness/night/` is read; a recorded worktree path equal to the candidate path marks it in use. A marker that cannot be read or whose worktree path cannot be determined fails the check. An absent night-state directory means there are no markers.

**Nested:** a registered worktree whose directory lies inside another registered worktree, and a registered worktree containing another, are both kept while that nesting exists.

**Eligible:** a registered, present worktree with an attached branch other than `main`, a matching merged pull request, clean and pushed, not in use, locked or nested, neither the main checkout nor the invoking worktree, and with every safety check completed successfully. These conditions are sufficient as well as necessary.

## Acceptance criteria

1. When `make prune-worktrees` runs with successful checks, it reports every eligible worktree as a removal candidate without removing worktrees, registrations or local branches.
   *Refuted by:* an eligible worktree is omitted, or preview removes any of those objects.
2. When a present registered worktree is ineligible, the report names it as kept and gives an accurate reason corresponding to an observed check outcome.
   *Refuted by:* a detached, unmerged, dirty, in-use, locked, protected or otherwise ineligible worktree is omitted, has a missing or incorrect reason, or is a candidate.
3. When the matching merged pull request is absent or its head branch or head commit differs from the local branch or tip, the worktree is kept.
   *Refuted by:* a fresh worktree whose tip is on `origin/main`, or a worktree with a mismatched pull request, is a candidate.
4. When the local tip is not an ancestor of freshly fetched `origin/main`, the worktree is kept.
   *Refuted by:* an unmerged tip is a candidate.
5. When a fresh `origin/<branch>` ref exists, the worktree is kept unless the local tip equals or is an ancestor of that ref.
   *Refuted by:* an ahead or divergent local tip is a candidate.
6. When a fresh `origin/<branch>` ref is absent, a matching merged pull request is required as evidence that the local tip landed.
   *Refuted by:* a worktree with a missing remote branch and no matching merged pull request is reported as a candidate, omitted, or reported with an incorrect reason.
7. When a worktree contains staged, unstaged or untracked non-ignored changes, it is kept.
   *Refuted by:* any of these changes is removed or the worktree is a candidate.
8. When a merge, rebase or cherry-pick is in progress in a worktree, it is kept.
   *Refuted by:* any such worktree is a candidate or removed.
9. When a worktree is in use or locked, it is kept.
   *Refuted by:* a worktree with a process working directory inside it, a lane busy marker, or a Git lock is a candidate or removed.
10. When the main checkout, the invoking worktree or a worktree on local `main` is encountered, it is kept.
    *Refuted by:* any of these is a candidate or removed.
11. When `make prune-worktrees ARGS=--write` runs after successful checks, it repeats the safety checks immediately before removing each still-eligible worktree without force, then freshly fetches and checks the branch tip against `origin/main` before attempting non-forcing local branch deletion from the main checkout.
    *Refuted by:* a changed candidate is removed, force is used, or branch deletion is attempted without that fresh ancestry check, before removal or from a different checkout.
12. When a missing-directory registration is prunable, preview reports it separately and only the explicit-write form may prune it using Git's worktree prune operation.
    *Refuted by:* it is omitted, preview prunes it, or the write form removes its branch as a consequence of pruning the registration.
13. When the fresh fetch or a safety check fails, the command reports the failure and exits nonzero in both modes.
    *Refuted by:* the failure is silent or the command exits successfully.
14. When the initial fetch or any initial safety check fails, the write form makes no removals.
    *Refuted by:* a worktree, registration or branch is removed despite an initial check failure.
15. When a repeated safety check fails during a write run, the command stops further removals and reports any earlier changes.
    *Refuted by:* removal continues after that failure or an earlier removal is omitted from the report.
16. When worktree removal or local branch deletion fails, the command reports the failure and partial result, continues with other candidates, and exits nonzero.
    *Refuted by:* a refusal stops other candidates, exits successfully, or hides a removed worktree whose branch remains.
17. When the handover routine is followed, it directs the session to run preview, read its output, and then run the explicit-write form.
    *Refuted by:* either command or the intervening review is absent from the handover instructions.
18. When the command is invoked, no remote branch is deleted.
    *Refuted by:* a remote branch is deleted; pruning stale local remote-tracking refs is allowed.
19. When a command-line `ARGS` other than empty or exactly `--write` is supplied to the Make target, the target rejects it without removing a worktree, registration or branch.
    *Refuted by:* another argument is accepted or causes a removal.
20. When the kit is exported to a new repository, it does not include this cleanup command.
    *Refuted by:* the new cleanup script is included in the kit manifest or export.
21. When a registered worktree contains another registered worktree or lies inside one, it is kept and reported as nested.
    *Refuted by:* either nested worktree is a candidate or its nesting is not reported.
22. When a candidate passes a repeated check but is no longer eligible, it is kept with its new accurate reason without making the exit status nonzero on that account.
    *Refuted by:* the candidate is removed, its new reason is absent or wrong, or that changed state alone causes a nonzero exit.
23. When an environment-only `ARGS` is present, the Make target ignores it and runs preview successfully if all checks succeed.
    *Refuted by:* an environment-only `ARGS=--write` selects write mode, or an environment-only invalid value is rejected.
24. When a busy marker cannot be read or its worktree path cannot be determined, the check fails.
    *Refuted by:* the command succeeds or a write run removes any candidate after an initial unreadable or unidentifiable marker.
25. When a safety check returns a disqualifying state without error, the worktree is kept for that reason without treating the state itself as a check failure.
    *Refuted by:* a cleanly detected dirty, locked or nested worktree alone causes a nonzero exit or is not reported with its actual reason.
26. When a report is produced, its header states that processes owned by other users are outside the in-use check.
    *Refuted by:* a report, including one with no in-use worktrees, omits that limit from its header.

## Non-goals

- Scheduled cleanup, age thresholds, worktree-count gates, and remote branch deletion.
- Cleaning dirty trees, rewriting history, or changing review-loop record discovery and supersession.
- Shipping this repository's lane housekeeping in the kit; a later change may reconsider portability.

## Protected areas

- The main checkout, the invoking worktree, `main`, worktrees in use and worktrees lacking safe evidence: they may contain ongoing work.
- Remote branches: only stale local remote-tracking refs may be pruned by the fetch.

## Definition of Done

- `make verify` green after implementation and orchestrator edits.
- `docs/WORKFLOW.md` and `tools/claude-code/skills/handover/SKILL.md` updated in the same pull request; no ADR.
- Protected areas preserved and non-goals unbuilt, checked against the pull request and tests.
- The pull request closes the merged worktree cleanup bead (`coding-harness-bxxt.4`), with `Closes-Bead: coding-harness-bxxt.4` in its last commit.
- The handover-convention pre-change measurement and skill installation are recorded with their relevant commits.

## Open decisions

None open. [DETAIL] The phase-2a dispositions in `findings.md` settle the merged-PR proof, use checks, stale registrations, failure handling, handover sequence and kit scope. Their reason is to avoid mistaking a branch based on main or missing evidence for a finished lane. Checks stop for a registration once a keep reason is known because further inspection cannot make it eligible; global evidence and nesting are still checked first. A pruning fetch may update local remote-tracking refs during preview.

**Boundary:** The final safety checks and Git removal are not atomic against other processes. A process or marker can appear between them; Git's non-forcing removal is a final guard, not a lock on other writers. The busy-marker convention does not guarantee a worktree path in every marker; such a marker blocks cleanup until it can be identified. Git's registration pruning also changes the set of worktrees through which existing review-loop records are discovered; it does not change the discovery mechanism.
