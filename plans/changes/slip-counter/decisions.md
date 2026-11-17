---
title: "Decisions — slip-counter"
category: decisions
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5.2, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verify-speed, targeted-check, run-log]
---

# slip-counter — Decisions

Class: bounded (bead coding-harness-bxxt.7).

## Q-1 · Derive the count or write slip records

asked: 2026-11-13
answer: "Ableiten statt schreiben (Empfohlen)" — no slip record of its own is written; a reader computes the count from what the local run log holds anyway: a green targeted check followed by a red full run on the same tree.
answered_by: maintainer
status: answered
context: |
  Topic: the slip counter counts faults the targeted check lets through and only the full check finds; it was split out of the change targeted-check-more-verbs on 2026-11-13.
  Intention: in that change the runner wrote a record per slip, and this writing drew five findings in six phase-6 re-checks (duplicates, failed appends, lost records); the maintainer asked for the most long-term build.
  Today: no counter exists on origin/main; the local run log (scripts/verify_duration.py) records full runs.
  Repository change: a reader over the run log; the targeted check leaves its result in the same log so the reader can pair it with the full run; no slip writer.
  Architecture change: none; the run log stays the one local history.

In the context of a counter whose own records drew five findings, facing a choice between taking the removed code up again and deriving the count at read time, we decided to derive it, to achieve a counter without a writer that can fail, accepting that the targeted check must leave its result in the run log. — 2026-11-13

## Q-2 · Incomplete runs in the asked interval

asked: 2026-11-13
answer: "Zahl plus Lücken (Empfohlen)" — the reader names the counted slips and, beside them, how many runs were incomplete and not counted; it never reports a bare zero while incomplete runs exist. The spec states this as a Boundary.
answered_by: maintainer
status: answered
context: |
  Topic: the last finding on the old counter (F6-12) was a reported zero when a red full run had lost its end record.
  Intention: five case repairs did not close the mechanism, so the spec gets a Boundary for incomplete evidence instead of a sixth case.
  Today: an incomplete run is silently skipped.
  Repository change: the reader's output and exit state distinguish "counted" from "not countable"; the night handover names both numbers.
  Architecture change: none.

In the context of runs that end without an end record, facing a choice between no number at all and a count with the gaps named, we decided for the count with the number of incomplete runs beside it, to achieve a figure that stays usable after one crash, accepting that the reader of the handover must look at two numbers. — 2026-11-13

## Q-3 · The comparison tree leaves out the change's own bookkeeping

asked: 2026-11-15
answer: "yes, variant A" — the slip comparison leaves out the change's own plan.md and findings.md.
answered_by: maintainer
status: answered
context: |
  Topic: the slip counter counts a red full check that ran after a green targeted check on the same tree.
  Intention: the plan's prerequisite proof failed; with a whole-tree identity the counter reads zero on the real runner path.
  Today: between the two checks the runner's and phase 6's bookkeeping change two files of the change, `plans/changes/<change>/plan.md` (the time line) and `findings.md` (call records, committed rows, audit lines), so the tree ids never match.
  Repository change: for the comparison the runner forms a tree identity without exactly these two files of the change; the spec changes in its term "Checked tree", a named Boundary and one new test case.
  Architecture change: none; a reader without a writer, the run log stays the one local history.
  Question: May the spec state that the change's `plan.md` and `findings.md` are not part of the comparison tree for slips (variant A)?
  Recommendation: variant A; consequence: a change to those two files between the checks goes unseen, and a gate that reads them (for example the criterion ledger) could count one slip too many — a risk named in the spec.

In the context of a prerequisite proof that showed the runner's own bookkeeping moving the tree between a targeted check and the later full one, facing a choice between stopping the change and leaving the change's two bookkeeping files out of the comparison, we decided to leave them out, to achieve a counter that can pair real runs, accepting that an edit to those two files between the checks goes unseen. — 2026-11-15

## Q-4 · Narrow the slip-history reader instead of repairing its edge cases

asked: 2026-11-16
answer: "Eingrenzen (Empfohlen)" — the slip-history reader counts only runs with complete comparison evidence; every other run appears once as incomplete; the remaining edge cases become named Boundaries in the spec.
answered_by: maintainer
status: answered
context: |
  Topic: the slip-history reader in scripts/verify_duration.py pairs a green targeted check with a later red full run on the same tree and counts the pair as a slip.
  Intention: the phase-6 re-check of 2026-11-16 (codex 01a1e510) found P6-5 (a targeted check that finishes after the full run started is not counted) and P6-6 (a run with an unknown tree, change or gate configuration is reported as countable evidence); the round before found P6-3 and P6-4; all four are the same mechanism, edge cases of the reader, so case repair ends.
  Today: the reader tries to classify every run, and each repaired edge case is followed by the next one.
  Repository change: the reader counts only runs with complete comparison evidence; every other run is reported once in the incomplete count; the spec names the remaining edge cases as Boundaries.
  Architecture change: none; a reader without a writer, the run log stays the one local history.
  Question: narrow the reader to runs with complete comparison evidence and name the rest as Boundaries, or keep repairing case by case?
  Recommendation: narrow; consequence: some real slips with incomplete evidence show up only in the incomplete count, not as slips.

In the context of a slip-history reader whose edge cases drew two findings in each of two phase-6 re-checks from one mechanism, facing a choice between repairing a fifth case and narrowing what the reader counts, we decided to count only runs with complete comparison evidence, report every other run once as incomplete and name the remaining edge cases as Boundaries, to achieve a reader whose count rests on evidence it can check, accepting that a slip with incomplete evidence appears only in the incomplete count. — 2026-11-16

## Q-5 · What "repository" means for pairing and selection

asked: 2026-11-17
answer: "B" — 'repository' means the shared git repository (common git dir), not the single worktree; pairs form across worktrees and any checkout reports all lanes.
answered_by: maintainer
status: answered
context: |
  Topic: the slip reader pairs a green targeted check with a red full run of the same repository, change, tree and gate configuration, and selects runs by repository.
  Intention: the phase-6 re-check of 2026-11-17 (codex 01a1e69e, row R-1) raised the open phase-2a row S-1 as a BLOCKER: the spec never says what "repository" is.
  Today: the reader compares the recorded checkout path; a green targeted check in a lane worktree and a red full run of the same tree in another checkout never pair, and the default report from the main checkout shows no lane runs.
  Repository change: the spec defines "Repository" as the shared Git repository (common git directory); the runner records it and the reader pairs and selects by it; one spec line plus a test.
  Architecture change: none; the run log stays the one local history.
  Question: is "repository" the single worktree path (A) or the shared git repository, the common git dir (B)?
  Recommendation: B, because lanes run in worktrees of one repository and slips cross them; consequence: one spec line plus a test.

In the context of lanes that run in worktrees of one repository and write one shared run history, facing a choice between the worktree path and the shared Git repository as the repository identity, we decided for the shared Git repository, to achieve pairs across worktrees and a report from any checkout that covers every lane, accepting that a report no longer separates the lanes of one repository. — 2026-11-17

## Q-6 · One validity check for every run instead of a third case repair

asked: 2026-11-17
answer: "A" — third row of one mechanism (P6-2, P6-6, R-2), so one validity check that every run, green or red, passes before it counts, plus a Boundary for what it cannot see; capped at one repair round, then phase 6 (the lane is past its appetite).
answered_by: maintainer
status: answered
context: |
  Topic: the slip reader decides per run whether its evidence is complete enough to count.
  Intention: the phase-6 re-check of 2026-11-17 (codex 01a1e69e, row R-2) found a red targeted check whose tree moved during the run counted as complete; after P6-2 and P6-6 this is the third row of one mechanism (when evidence is incomplete), so case repair stops by the house rule.
  Today: the reader checks evidence in several branches per kind and verdict; the tree-stability check applies only to a green targeted check.
  Repository change: one validity check at a single choke point that every run passes before it may count, green or red, targeted or full; a run that fails it is incomplete once; the spec names a Boundary for what that check cannot see.
  Architecture change: none; a reader without a writer.
  Question: one validity check at a single choke point plus a Boundary (A), or another case repair?
  Recommendation: A; consequence: one more repair round.

In the context of three phase-6 rows of one mechanism about incomplete evidence, facing a choice between a further case repair and one validity check every run passes, we decided for the one validity check plus a Boundary for what it cannot see, capped at one repair round before phase 6, to achieve a reader with one place that decides whether a run may count, accepting that whatever the check cannot see stays a named limit. — 2026-11-17

## Decided by the agent

[DETAIL] **The implementation starts after the targeted-check change (bead coding-harness-0swp) is merged.** Reason: this change reads what that one writes; spec and plan are drafted before, on the branch state of origin/main.
