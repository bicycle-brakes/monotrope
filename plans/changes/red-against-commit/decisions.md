---
title: "Decisions — red-against-commit"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-qvf7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, repair, red-first, stage2-runner]
---

# red-against-commit — Decisions

Class: bounded (bead coding-harness-qvf7).

## The bead (read from the tracker by the orchestrator, 2026-11-21)

> Class: bounded (an extension of change guard-test, bead coding-harness-0ho, after it merges). Why: on 2026-11-01 (l7sc review rows) a fix already sat in a committed saved attempt, so no red baseline remained and the red-first proof had to be done by hand. The maintainer answered on 2026-11-01 ~15:15 UTC (answer C): yes, a row may name the commit before the fix as its 'red against' commit, and the runner proves red there. Kept out of guard-test so its merged draft (PR #281) is not redrafted.

The dependency is met: coding-harness-0ho is closed and guard-test is archived (`plans/changes/archive/2026-11-16-guard-test/`). "Free" in the bead's title is not the review loop's free swarm: it means a commit the row may name freely — the commit before the fix — instead of the run's HEAD.

## SKIP · interview

status: skipped
reason: The maintainer answered the one design question on 2026-11-01 (answer C, quoted in the bead): a row may name the commit before the fix as its 'red against' commit, and the runner proves red there. The maintainer asked for no question windows until the block on 2026-11-23 10:00. The rest are [DETAIL] items; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Where the commit is named:** in the row's fixed status, as an optional suffix of the test form: `fixed — tests/<path>::<function> — red against <sha>`. The `<sha>` must be an ancestor of HEAD on the change's branch (or a saved attempt ref of this change) and must not contain the fix. Reason: one place, next to the test it proves.
- **What the runner proves there:** it runs the named test against a temporary checkout of `<sha>` (a throwaway worktree, never the lane's tree) and requires it red with the test's actual outcome (assertion failure or pytest's failed outcome), then green on HEAD as today. Reason: the same red-first proof, only the baseline moves.
- **Refusals:** a `<sha>` that is not reachable from HEAD or a saved attempt ref, a test that is already green at `<sha>`, or a test file absent at `<sha>` refuses the fixed status with the reason; the row stays taken. Reason: a red proof must be real.
- **Scope: repair only,** where the bead's case occurred. Implement keeps today's baseline. Reason: the bead's case and the guard-test precedent.
- **No new evidence grammar in the criterion ledger.** Reason: guard-test's protected areas.
