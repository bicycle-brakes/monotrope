---
title: "Decisions — review-loop-deep-a"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: to be filed
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# review-loop-deep-a — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).

The maintainer asked on 2026-10-25, in the conversation of the orchestrating
session, for every defect of the deep review of the review loop (part A,
DL-A-1 to DL-A-10) to be repaired (Q-10, the one counted record). The
direction of each fix (Q-1 to Q-9) is the orchestrating agent's, taken from
the review's smallest fixes and relayed to this session; those records are
agent answers and are not counted. Q-1 (DL-A-8) was put to the maintainer as
"runner or doctrine"; the maintainer answered "repair all of it", and the
agent chose that the code follows the doctrine. The research (`research.md`)
holds each finding.

## Q-1 · Whether the runner enforces "repair before the next round"

context: |
  Topic: the review loop's next round after a taken row (DL-A-8).
  Intention: the deep review found that ADR 0021 decision 6 ("decides and
  repairs before another review") is stated, not enforced; a test relies on
  the gap.
  Today: only an undecided row holds the next round; a taken row nobody
  repaired admits the next paid round on the unrepaired diff.
  Repository change: review-loop refuses while a taken row of the run is
  not repaired; the test that relied on the gap changes.
  Architecture change: none; the code follows the doctrine.
asked: 2026-10-25, decided by the orchestrating agent (relayed)
answer: "code follows doctrine: the runner refuses the next round while a taken row is not repaired; adapt test_round_three_starts_only_after_a_taken_row and every test that relies on the old behaviour"
answered_by: agent
status: answered

In the context of the review loop admitting a new round over taken rows
nobody repaired, facing the choice between enforcing ADR 0021 decision 6 in
the runner and rewording the doctrine, we decided that the runner refuses the
next round while a taken row is not repaired, to achieve that every paid
round reviews a repaired diff, accepting that tests which seeded taken rows
before a round change with it. — 2026-10-25

## Q-2 · Which phase-6 verdict a release needs

context: |
  Topic: the verdict check of release-loop (DL-A-7).
  Intention: after a restart or a continued run, rows are released on the
  old verdict, against the ADR 0021 restart amendment.
  Today: any verdict line anywhere in findings.md admits a release.
  Repository change: a release needs a verdict line that stands after the
  last release block and after the last restart line.
  Architecture change: none.
asked: 2026-10-25, decided by the orchestrating agent (relayed)
answer: "release requires a phase-6 verdict line after both the last release and the last restart"
answered_by: agent
status: answered

In the context of release-loop accepting an old verdict for new rows, facing
the choice between any verdict and a verdict after the last release and
restart, we decided on the latter, to achieve that every run's rows pass a
phase-6 verdict of their own, accepting that a continued run needs a new
verdict line before its release. — 2026-10-25

## Q-3 · How release survives a crash between append and delete

context: |
  Topic: release idempotence (DL-A-3).
  Intention: a crash after the append and before the record is deleted
  releases the same rows twice and makes a phantom clean round.
  Today: the second release-loop appends a second block.
  Repository change: release is idempotent; the mechanism is the agent's
  choice, reasoned in the plan.
  Architecture change: none.
asked: 2026-10-25, decided by the orchestrating agent (relayed)
answer: "make release idempotent — a record digest line or a tombstone rename, the implementer's choice, reasoned in the plan"
answered_by: agent
status: answered

In the context of a release that a crash can repeat, facing the choice
between a record digest line and a tombstone rename, we decided to make
release idempotent and left the mechanism to the plan, to achieve that a
repeated release-loop never appends the same rows twice, accepting one more
runner line in the released block. — 2026-10-25

## Q-4 · How findings.md is protected from the implementing model

context: |
  Topic: loop state forged through implement (DL-A-2).
  Intention: the implementing model can write a release block or a restart
  line into findings.md and the runner commits it.
  Today: implement passes no findings snapshot or body check; the loop's
  stops run before the snapshot is read.
  Repository change: findings.md's body is immutable across implement
  attempts (repair's check reused), and review-loop reads its snapshot
  before the stops.
  Architecture change: none.
asked: 2026-10-25, decided by the orchestrating agent (relayed)
answer: "findings.md body immutable across implement attempts, reusing repair's check, and read_state before the stops in review_loop"
answered_by: agent
status: answered

In the context of the implementing model being able to forge loop state,
facing the choice between protecting findings.md and hardening the loop's
reading of it, we decided on both, to achieve that neither a forged block
is committed nor a block without the runner's snapshot ends the loop,
accepting that an implement attempt which edits findings.md fails. —
2026-10-25

## Q-5 · How the record is written

context: |
  Topic: atomic record writes (DL-A-4).
  Intention: a write that fails midway loses rows of the only copy and can
  keep a consumed stage without its round.
  Today: Path.write_text truncates, then writes.
  Repository change: a temporary file in the record's directory, then
  os.replace.
  Architecture change: none.
asked: 2026-10-25, decided by the orchestrating agent (relayed)
answer: "temp file + os.replace for record writes"
answered_by: agent
status: answered

In the context of a loop record that a failed write can truncate, facing the
choice between writing in place and replacing atomically, we decided on a
temporary file and os.replace, to achieve that a record is either the old
or the new one, accepting one more file operation per write. — 2026-10-25

## Q-6 · How repair and release share the record

context: |
  Topic: the record lock during repair (DL-A-5).
  Intention: a release during a repair silently drops the fixed status.
  Today: repair takes the lock only to mark the record after the commit,
  and a missing record is skipped silently.
  Repository change: repair holds the record lock for its whole run, and a
  record gone at marking time raises, naming the ids.
  Architecture change: none.
asked: 2026-10-25, decided by the orchestrating agent (relayed)
answer: "hold the record lock for the whole repair; raise naming the ids if the record vanished"
answered_by: agent
status: answered

In the context of a repair whose record a release can remove, facing the
choice between the lock for the whole repair and a check at marking time,
we decided on both, to achieve that a committed fix is always booked or
named, accepting that review-loop, release-loop and review wait for a
running repair. — 2026-10-25

## Q-7 · What a lost record stops

context: |
  Topic: release and review-loop without a record (DL-A-6).
  Intention: a record under another state directory is released as "the
  loop did not run" and the next run replays the consumed free stage.
  Today: no record means no loop.
  Repository change: release-loop and a fresh review-loop refuse when
  review-loop audit lines stand but no record and no release, naming the
  expected record path.
  Architecture change: none.
asked: 2026-10-25, decided by the orchestrating agent (relayed)
answer: "refuse release and a fresh loop when audit lines exist but no record or release, naming the expected record path"
answered_by: agent
status: answered

In the context of a loop record that is missing while findings.md shows the
loop ran, facing the choice between treating it as no loop and refusing, we
decided to refuse and name the expected record path, to achieve that a lost
record never replays a consumed stage, accepting that a record lost for
good needs the maintainer. — 2026-10-25

## Q-8 · How a cut free diff reaches the round

context: |
  Topic: the free round's cut (DL-A-1).
  Intention: a free diff cut per file or in total is not recorded as cut,
  so a clean answer ends the loop.
  Today: only bounded_review_diff's cut reaches the round.
  Repository change: free_diff reports its cut and review_loop merges it
  into the round's cut note.
  Architecture change: none.
asked: 2026-10-25, decided by the orchestrating agent (relayed)
answer: "free_diff reports its cut; review_loop merges it into cut_note"
answered_by: agent
status: answered

In the context of a free round over a diff cut by free_diff's own bounds,
facing the choice between recording that cut and leaving the marker in the
prompt alone, we decided to record it, to achieve that a cut free round
never counts as clean, accepting another round when a large file is in the
change. — 2026-10-25

## Q-9 · The two NITs

context: |
  Topic: the change-name check and dead helpers (DL-A-9, DL-A-10).
  Intention: the lock is taken before the change name is checked, and
  three helpers are no longer used by the runner.
  Today: an escaping name leaves a lock file outside the state base;
  mark_consumed, taken_in_round and released_rows stay in the module.
  Repository change: the name is validated before the lock; the dead
  helpers are deleted after a grep over scripts/ and tests/.
  Architecture change: none.
asked: 2026-10-25, decided by the orchestrating agent (relayed)
answer: "validate the change name before taking the lock; delete the dead helpers, checking with grep across scripts/ and tests/ first"
answered_by: agent
status: answered

In the context of two small defects of the runner, facing the choice
between fixing them now and leaving them, we decided to fix them in this
change, to achieve that a bad name writes nothing and no unused two-write
path stays callable, accepting that tests of the deleted helpers move to
the runner's live functions. — 2026-10-25

## Q-10 · Whether every defect of the deep review part A is repaired

context: |
  Topic: the deep review of the review loop, part A (DL-A-1 to DL-A-10).
  Intention: decide whether the six reproduced defects, the doctrine gap
  DL-A-8 and the NITs are repaired now or left as findings.
  Today: the review reported them with reproductions; nothing was changed.
  Repository change: one branch repairs all ten in scripts/stage2.py and its
  tests.
  Architecture change: none; the code follows ADR 0021.
asked: 2026-10-25, conversation
answer: "repariere das alles" (repair all of it — stated in German, translated by the agent), given beside the list DL-A-1 to DL-A-10
answered_by: maintainer
status: answered

In the context of a deep review that reproduced ten defects and gaps in the
review loop's control and state, facing the choice between repairing them now
and leaving them as findings, we decided to repair all ten on one branch, to
achieve a loop whose stops and releases cannot be forged, lost or misread,
accepting that about forty loop tests change their seeding with it. — 2026-10-25
