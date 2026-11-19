---
title: "Decisions — slip-counter"
category: decisions
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-19
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

## Q-7 · "Targeted check" means the runner's targeted repair check in this change

asked: 2026-11-18
answer: "C: A jetzt, B als nächster Change" — A now, B as the next change: this change counts only the runner's targeted repair check (A); the follow-up change (bead coding-harness-l0g6) extends it right after to every green partial check (B) through the same step.
answered_by: maintainer
status: answered
context: |
  Topic: the slip definition pairs a green "targeted check" with a later red full run; phase-2a row S-11 found the term undefined, and the phase-6 re-check of 2026-11-18 (codex 01a1ec2b, row R-3) raised it as a BLOCKER.
  Intention: on 2026-11-18 the maintainer re-cut the lane: the spec is cleaned with all open phase-2a rows decided in one sitting, then the lane restarts from the cleaned spec.
  Today: only the runner's targeted repair check records slip evidence; a green cheap check of an implement or draft attempt followed by a red full verify counts as no slip.
  Options: A — only the runner's targeted repair check; B — every partial check by which an attempt called its work green; C — A in this change, B in the next change.
  Repository change: A — a spec Term only, no code; B — more runner paths record evidence, one more repair round and tests; C — A here, B in the follow-up change through the same step.
  Architecture change: none under A.
  Question: does "targeted check" mean only the runner's targeted check (A) or every partial check an attempt called green (B)?
  Recommendation: A, with B as a follow-up bead.

In the context of a slip definition whose term "targeted check" was undefined and raised as a BLOCKER by a phase-6 re-check, facing a choice between counting only the runner's targeted repair check and instrumenting every runner path where an attempt calls its work green, we decided to count only the runner's targeted repair check in this change and to extend the count to every green partial check in the follow-up change (bead coding-harness-l0g6) through the same step, to achieve a defined term without a further repair round in this change, accepting that until the follow-up merges a green partial check of an implement or draft attempt followed by a red full verify counts as no slip. — 2026-11-18

## Q-8 · A targeted green pairs only with the first full run after it

asked: 2026-11-18
answer: "C" — a targeted green pairs only with the first full run of the same identity after it; any later check of that identity ends the pairing, so each wrong green counts once; in addition the pattern "full green, then full red" on the same identity is counted separately as a flaky-test signal.
answered_by: maintainer
status: answered
context: |
  Topic: which runs of one identity may answer a green targeted check and form a slip (phase-2a row S-3).
  Intention: the re-cut of 2026-11-18 decides all open phase-2a rows in one sitting.
  Today: the spec says "an earlier completed green targeted check" and does not say whether other runs of the same identity in between matter. For the histories targeted green, full red, full red / targeted green, targeted red, full red / targeted green, full green, full red, row S-3's reading A (any earlier green targeted check qualifies) gives 2, 1 and 1 slips, its reading B (only the first full run after a targeted green answers it, any later check ends the pairing) gives 1, 0 and 0.
  Options: row S-3 states readings A and B; the bead notes record the chosen option C and no wording of the others.
  Repository change: the spec's pairing rule follows C; the report also counts "full green, then full red" on one identity as a separate flaky-test signal.
  Architecture change: not recorded with the question in the bead notes.

In the context of a pairing rule that gave different slip counts for one history under two readings, facing a choice of which runs of one identity may answer a green targeted check, we decided that a targeted green pairs only with the first full run of the same identity after it, that any later check of that identity ends the pairing, and that "full green, then full red" on one identity is counted separately as a flaky-test signal, to achieve a count in which each wrong green counts once, accepting that a red full run after an intermediate check of the same identity is not counted as a slip. — 2026-11-18

## Q-9 · Legacy and change-less runs are outside the population

asked: 2026-11-18
answer: "B" — legacy version-1 records and full runs without a change name are outside the population and not gaps; the report names their count in a line "outside the count", so a complete report is reachable.
answered_by: maintainer
status: answered
context: |
  Topic: whether legacy version-1 records and full runs with no change name (for example a hand-run `make verify`) belong to the population the slip reader counts (phase-2a row S-4).
  Intention: the re-cut of 2026-11-18 decides all open phase-2a rows in one sitting.
  Today: the spec does not say; under reading A each such run is incomplete once, so with the default selection every real history reports them as incomplete and the report can never exit as a complete measurement; under reading B they are outside the slip population, neither enters the incomplete count, and a complete report is reachable.
  Options: A — they are in-scope runs without comparison evidence, each incomplete once; B — they are outside the population.
  Repository change: under B the reader leaves them out of both counts and the report names their number on a line "outside the count".
  Architecture change: not recorded with the question in the bead notes.

In the context of records that by construction carry no comparison identity, facing a choice between counting them as incomplete and leaving them outside the population, we decided to leave legacy version-1 records and change-less full runs outside the population and name their number on a line "outside the count", to achieve a report that can exit as a complete measurement on a real history, accepting that a fault in a legacy or change-less run is never counted as a slip. — 2026-11-18

## Q-10 · A slip is decided on the pair's evidence

asked: 2026-11-18
answer: "B" — when either side of a pair is incomplete, both count as incomplete; the slip is decided on the pair.
answered_by: maintainer
status: answered
context: |
  Topic: whether "complete comparison evidence" (decision Q-4) means each run's own evidence or the evidence of the pair (phase-2a row S-10).
  Intention: the re-cut of 2026-11-18 decides all open phase-2a rows in one sitting.
  Today: case of row S-10 — a red full run with complete evidence whose only same-identity green targeted predecessor is itself incomplete (conflicting duplicate completions, or a tree that moved during the check); under reading A the full run is a counted non-slip and only the targeted run is incomplete (incomplete = 1); under reading B whether the full run is a slip cannot be decided from complete evidence, so it is incomplete too (incomplete = 2).
  Options: A — per-run evidence; B — per-pair evidence.
  Repository change: under B the reader moves both sides of a pair to the incomplete count when either side is incomplete.
  Architecture change: not recorded with the question in the bead notes.

In the context of a pair whose targeted side has incomplete evidence while its full side is complete, facing a choice between judging each run's own evidence and judging the pair, we decided that when either side of a pair is incomplete both count as incomplete, to achieve a slip that is decided only on evidence complete for both runs, accepting that one incomplete targeted run moves a complete full run into the incomplete count. — 2026-11-18

## Appetite for the restarted lane

The maintainer's appetite for the restarted lane is 6 hours of phase 4, repairs included — stated to the orchestrating session on 2026-11-18 and relayed to this lane's session; not read in the bead notes. It replaces the 3 hours of the first draft (bead notes, 2026-11-13).

## Decided by the agent

[DETAIL] **The implementation starts after the targeted-check change (bead coding-harness-0swp) is merged.** Reason: this change reads what that one writes; spec and plan are drafted before, on the branch state of origin/main.

## Agent decisions on the second phase-2a rows S-12..S-20 — 2026-11-18

Second spec-review round (maintainer rule of 2026-11-18: triage each round,
at most three rounds). Decisions by the orchestrating session (Opus 5.5),
shown to the maintainer as one list with one principle and accepted as
proposed ("A: Grundsatz + so übernehmen").

**Principle.** A slip or non-slip is decided only on complete, unambiguous
evidence; otherwise the runs concerned are `incomplete`. It follows from the
maintainer's answers on S-10 (B, the pair decides) and, in the sibling change
findings-per-model, F-8 (B, gaps are shown, never hidden).

- **S-12, an end record with no start.** Before the first version-2 record in
  the history it is a legacy record, reported on the line "outside the
  count"; after it, the end is damaged evidence and the report is partial.
- **S-13, an invalid check between a targeted green and a full red.** The
  pairing cannot be decided; every run concerned is incomplete (principle).
- **S-14, a predecessor whose tree moved during its check.** Both sides are
  incomplete, as the context of the S-10 answer names (principle).
- **S-15, the targeted check's end reading.** A criterion requires a targeted
  check to record its checked tree at start and end, with the refuting case:
  a targeted green whose tree changes between start and end, followed by a
  red full run of the start tree, counts one slip (the mechanism of R-2).
- **S-16, where targeted-check records go.** Into a history file of their
  own beside `verify-duration.jsonl`; version-1 readers never see them and
  the full-run minutes stay clean.
- **S-17, a byte-identical duplicated end record.** It collapses into one
  record (an append retry, not a conflict).
- **S-18, equal completion timestamps.** No order is established; both runs
  are incomplete (principle).
- **S-19, one interrupted run.** Any incomplete run makes the measurement
  not complete: the report says so and exits non-zero.
- **S-20, the flaky signal beside an incomplete run.** The slip status of a
  run whose predecessor is a full run stays decided (it is not a slip); the
  flaky signal is counted as "undecided" on its own line.

## Agent decisions on the third phase-2a rows S-21..S-27 — 2026-11-18

Third and last spec-review round (maintainer rule of 2026-11-18: triage each
round, at most three rounds). `[DETAIL]` decisions by the orchestrating
session (Opus 5.5), applying the principle of the second round, shown to the
maintainer as one list and accepted as proposed ("A: So übernehmen"). No
fourth review runs; the final draft works these in.

- **S-21, one of the two history files missing.** The targeted-check history
  is created at the first record the version-2 runner writes. Once the
  duration history holds a version-2 record, a missing targeted-check history
  is missing history: the report is unavailable and exits non-complete. A
  missing duration history with a present targeted-check history is missing
  history as well. Reason: a removed file must never yield a complete zero
  (Q-2).
- **S-22, a full run with no end between a targeted green and a full red.**
  Its completion is unknown, so it may intervene: the targeted green, the
  run without an end and the full red are all incomplete — also while that
  run is still going (principle).
- **S-23, an end with no start between the pair.** A full-run end with no
  start whose completion lies between the targeted green's completion and the
  full red's completion may belong to a run of the pair's identity: both
  sides of the pair are incomplete and the report is partial (principle).
- **S-24, which reports such an end makes partial.** Only the selections it
  could belong to: a report whose lower bound lies after the end's completion
  is not made partial by it; every repository counts as possible, since the
  end names none. Named limit in plan.md: a report without bounds stays
  partial once one such end exists, and a damaged line with no timestamp
  makes every report partial; `--since` is the remedy.
- **S-25, what "legacy" means.** A record format, not a position: a
  well-formed version-1 start and end pair is a recognisable legacy run
  wherever it stands in the history, reported on the line "outside the
  count", and the report can still be complete. Reason: a worktree not yet
  rebased must not make every report partial.
- **S-26, AC 12 against the Boundary.** The Boundary governs: when a full
  run of uncertain tree or uncertain order sits between a targeted green and
  a full red, all three runs are incomplete and no flaky line is printed; AC
  12 and AC 13 are aligned to this, for all three cases the row names
  (principle).
- **S-27, a moved targeted check.** Its identity covers its start tree and
  its end tree; a full run on either is a possible match, and the runs
  concerned are incomplete (principle).

## Agent decisions on review-loop round 11 — 2026-11-19

The maintainer was asked whether legacy and change-less full runs appear on
the outside line under `--change NAME` and answered that this cannot be
judged from the maintainer's seat (2026-11-19), so the orchestrator decides
it as a detail with reasons.

[DETAIL] **L11-2 (the outside line under `--change`)**: under `--change
NAME` the outside line still counts legacy and change-less full runs of the
repository in the interval, labelled "not change-scoped"; the spec Boundary
sentence ("only where … requested change scope can be established") is
aligned with it. Reason: a filtered report must not hide what it could not
measure (S-4 B, a complete report names what lies outside), and the taken
rows L7-1 and L10-2 already build on it; the label keeps the reader from
taking those runs for this change's.

[DETAIL] **L11-1 (the targeted history on a machine without a repair)**:
the version-2 full-run writer creates the empty targeted history, so a
missing history means a removed file, as the Boundary and the reader
contract promise. Reason: the alternative, rewriting the promise, would make
"unavailable" the normal state of every machine that has not repaired yet.

[DETAIL] **L11-3 (interval of the unattributed count)** and **L11-4 (the
handover paragraph names the repair-only source)**: taken as reported.
Reason: AC 8 and decisions Q-7 already say so; the code and the lane-facing
document lag behind.
