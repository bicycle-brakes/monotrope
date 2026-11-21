---
title: "Decisions — ci-no-push-run"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-dmmy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, ci, merge-queue]
---

# ci-no-push-run — Decisions

Class: bounded (bead coding-harness-dmmy).

The bead (created 2026-11-21 from the read-only CI research swarm, maintainer approval "ja, als P2"): every merged pull request runs the full verify three times — on the pull request, in the merge group and on the push to main (median about 25 min each; 200 runs, 2026-11-12..21). Main moves only through the merge queue (rule RB-G7; ruleset without bypass, rule RB-M6), so the push run re-tests a commit the merge group has just tested. First check, done by the orchestrator on 2026-11-21: `gh run list` shows the push run of merge commit `f30418ad` and the merge-group run of `f30418ad` on the same commit.

## Q-1 · Drop the push-to-main CI run, and where interview-minimums measures the landed main line

asked: 2026-11-21
answer: "A (meine Empfehlung): Entscheidungs-PR. Der Lauf beim Push fällt weg, der Kommentar wird angepasst, und der Lauf in der Merge-Queue übernimmt die Messung von interview-minimums, denn sein Commit ist genau der, der auf main landet."
answered_by: maintainer
status: answered
context: |
  Topic: dropping the full verify run on push to main (bead coding-harness-dmmy, branch fix/ci-no-push-run).
  Intention: save about 25 minutes of hosted CI time per merge; the merge-group run already tests the exact commit that lands.
  Today: every merge runs the full verify on the pull request, in the merge group and on the push to main; decisions/gates.yaml (human-decided) says in its header comment 'per push to main / pull request'; scripts/check_interview_minimums.py takes its first-parent main-line base only when GITHUB_REF is refs/heads/main, that is only in the push run.
  Repository change: the CI generator scripts/ci_gates.py drops the push trigger, .github/workflows/ci.yml is regenerated, tests/test_ci.py follows, the gates.yaml header comment is updated, and check_interview_minimums.py takes the main-line base in the merge-group run.
  Architecture change: the CI trigger set loses push to main; pull_request, merge_group, schedule and workflow_dispatch stay.
alternatives: |
  - A (chosen): decision pull request; the push run goes, the comment is updated, the merge-group run takes the interview-minimums main-line measurement because its commit is the one that lands on main.
  - B: keep the push run but run only the interview-minimums gate there.
  - C: leave everything as it is.

In the context of a merge queue that already tests the exact commit that lands
on main, facing a third full verify run per merge on the push to main, we
decided to drop the push run, update the human-decided gates.yaml comment in a
decision pull request, and move the interview-minimums main-line measurement to
the merge-group run, to achieve about 25 minutes less hosted CI time per merge,
accepting that no hosted run tests main after the merge if the merge queue is
ever switched off (the ruleset gate reports a switched-off queue on the next
local make verify) — 2026-11-21

## [DETAIL] items decided by the orchestrator

- **This is a decision pull request** (title `decide(ci-no-push-run): …` or the `decision` label), because it edits `decisions/gates.yaml`; the orchestrator does not merge it — the maintainer does. Reason: the human-decided file.
- **The merge-group run's main-line base** is the first parent of the merge-group commit, the same rule the push run used for `refs/heads/main`; the gate recognises the merge-group event (`GITHUB_EVENT_NAME == merge_group`) instead of the ref. Reason: the merge-group commit is the commit that lands.
- **Kept triggers:** pull_request, merge_group, schedule, workflow_dispatch. Reason: the bead.
- **Risk named in the spec:** with the merge queue switched off, RB-G7 falls back to the up-to-date requirement and no run tests main after a merge; the ruleset gate already reports a switched-off queue. Reason: the bead asks for it.
