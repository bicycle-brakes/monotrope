---
title: "Decisions — index-merge-regenerates"
status: draft
implementation_status: partial
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-njtm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# index-merge-regenerates — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; Q-1
below). One package of three beads: regenerate `plans/INDEX.md` instead of
merging it (beads coding-harness-njtm, coding-harness-hfsz) and the daily
pull-request sync (bead coding-harness-eq6y).

## Q-1 · What the package covers and what the sync may do

context: |
  Topic: four remedies for pull requests that could no longer merge main
  (five night-plan pull requests on 2026-10-27, bead coding-harness-s05q).
  Intention: settle which remedies travel together and whether the sync
  only warns or also merges.
  Today: plans/INDEX.md is generated but committed and conflicts on almost
  every merge; the daily sync in docs/WORKFLOW.md §3 is doctrine with no
  script behind it (research.md, "The merge practice, as recorded").
  Repository change: a merge rule that regenerates the index, and a sync
  step runnable by day and in the night run.
  Architecture change: none.
  Question: one package or separate, and does the sync merge?
asked: 2026-10-27, the directing conversation and pull request #260
answer: "one package led by coding-harness-hfsz (one pull request)"; the
  sync "does not only warn. Where git merge-tree shows a clean merge it
  merges origin/main into the PR branch and pushes; where it conflicts it
  reports the PR and files; it also lists PRs open longer than five working
  days for the maintainer. A runner-held file or a decision PR is reported,
  not merged into."
answered_by: maintainer
status: answered

In the context of pull requests that drift from main until they cannot
merge, facing separate fixes or one package, and a warning-only or a
merging sync, we decided on one package whose sync merges clean pull
requests, reports conflicts and lists old ones, to achieve that a conflict
is resolved while it is small, accepting that the sync pushes to pull
request branches and must leave decision and runner-held work alone.
— 2026-10-27

## Details the orchestrating session decides

These are `[DETAIL]` items, recorded on 2026-10-28; none changes a decision
of record.

1. **The mechanism is the drafter's, within three limits.** A merge driver,
   a post-merge regeneration or an explicit step in the sync and merge
   helpers are all open. Limits: the committed index must equal what
   `scripts/plans_registry.py --index` renders from the merged tree (not
   from either side alone); the `plans-registry` gate stays the backstop and
   is not weakened; a conflict in any other file still stops the merge.
   Reason: the index renders from every artefact's frontmatter, which is
   only final after the other files are merged; a per-file driver may run
   before that.
2. **Merges made on GitHub's servers are out of scope.** A custom merge
   driver does not run in GitHub's "Update branch" or merge button. The
   package covers local merges (the sync step, the phase-6 helper, agents'
   hand merges); the spec names the server-side gap as a limit. Reason:
   GitHub offers no hook for it; the registry gate still catches a stale
   index there.
3. **`make index` is not added here.** The check's remedy line ("Fix: make
   index") named a target that did not exist when the research ran
   (research.md, "The named remedy does not exist in this tree"); PR #267
   (merge `a6ddd9d1`, 2026-10-28) added it before this change's
   implementation. This change only keeps it pinned by a test. (Amended
   2026-10-28 after the merge; the earlier text planned to add it.)
4. **The sync never pushes into work in progress.** Besides decision pull
   requests and runner-held branches, it skips a branch that a local
   worktree has checked out with uncommitted or unpushed commits, and
   reports it. Reason: a push there would make the worktree diverge from
   its remote.
5. **The sync runs on request only.** It is a script the night run and a
   day session call; no scheduled job is added. Reason: the bead names the
   night-run skill and "runnable by day"; a scheduled job writing to pull
   request branches would need a decision of its own.
