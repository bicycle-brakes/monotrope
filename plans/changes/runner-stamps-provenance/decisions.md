---
title: "Decisions — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: [{kind: llm-session, name: claude-code, model: claude-opus-5-5, version: "2026-11-16"}, {kind: llm-session, name: codex, version: "2026-11-20", model: "gpt-6.1-terra"}]
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# runner-stamps-provenance — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).
Exploration: `research.md` (GLM 5.3 Flash, 2026-11-16). The bead
(coding-harness-f9sv) states the problem and the four-part fix; the
answers below were given in conversation on 2026-11-16 and recorded in the
bead's notes the same day; this file copies them from there.

## Q-1 · How the rule "no hand-written provenance" is enforced

context: |
  Topic: artifact headers (`produced_by`) written by hand.
  Intention: 50 `research.md` headers on main (2026-11-16) carry a free-form
  `produced_by`; a lane went red on one. House rule 9 says a rule holds
  through a check that goes red.
  Today: models and sessions write the header by hand; only `findings.md`
  is stamped by `scripts/stage2.py`.
  Repository change: a red check per case (this header), or one general
  detector of side routes.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "pro Fall"
answered_by: maintainer
status: answered


In the context of hand-written artifact headers, facing a free-form `produced_by` that keeps failing the census rule, we decided to make the rule red per case at the header's own check, to achieve that this header can no longer be written wrongly, accepting that other hand-written fields need their own checks.
— 2026-11-16

## Q-2 · What happens to the existing free-form headers

context: |
  Topic: the 50 existing headers that fail the census rule.
  Intention: a stamping runner and a red check leave the old headers red
  or exempt.
  Today: archived changes carry most of them.
  Repository change: migrate all headers once, or exempt archived changes.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "migrieren"
answered_by: maintainer
status: answered


In the context of 50 existing free-form headers, facing a new red check, we decided to migrate every header once, archived ones included, to achieve one rule without exemptions, accepting a large one-time diff.
— 2026-11-16

## Q-3 · Order

context: |
  Topic: when this change runs.
  Intention: it removes the most frequent source of hand repairs.
  Today: queued behind other lanes.
  Repository change: none.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "ja" (to: start it as the next lane, before lane 10)
answered_by: maintainer
status: answered

In the context of the lane queue, facing the most frequent source of hand repairs, we decided to start this change as the next lane, before lane 10, to achieve fewer hand steps, accepting that lane 10 waits.
— 2026-11-16

## Q-4 · Scope: split the change

context: |
  Topic: the size of this change.
  Intention: the first draft (2026-11-16) migrated "~50" headers and stamped
  after `draft` only. The bead (coding-harness-f9sv) asks for a stamp after
  explore, draft and repair, and for a post-run check of the files each run
  touched. A count with the census rule on origin/main (2026-11-16) found
  271 of 620 producer headers under plans/ failing, wrong program names
  (`Claude Code`, `glm`, `stage2`) included. The migration method was
  decided on 2026-11-07 in coding-harness-2i7x (producers read from each
  file's history, never collapsed).
  Today: one change holds stamp, check, migration and a tree-wide check.
  Repository change: this change keeps the stamp and the per-run check;
  the migration and the tree-wide check move to coding-harness-2i7x.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "teilen"
answered_by: maintainer
status: answered

In the context of a provenance change four times larger than first drafted,
facing open lanes that a tree-wide check would turn red, we decided to split it,
so that this change makes `scripts/stage2.py` stamp `produced_by` (program,
model, publication date) after explore, draft and repair, and makes every
verb's post-run check refuse a failing producer header in the files the run
touched; the migration and the tree-wide check go to coding-harness-2i7x, to
achieve that no new free-form header is written from now on, accepting that
existing ones stay until 2i7x lands.
— 2026-11-16

## Q-5 · Existing producer records on a new draft

context: |
  Topic: earlier records in a document's `produced_by` when the runner
  stamps a new draft.
  Intention: the spec review (findings F-2 and F-12) left the spec's open
  [DECISION] "Existing producer records" unanswered; the stamp cannot be
  built before it is answered.
  Today: the research publication keeps existing records and appends the
  current run; earlier records can be false.
  Repository change: the runner either keeps earlier records and adds the
  actual current run, or writes only the current run.
  Architecture change: none; the runner stays the one writer, only the
  stored provenance differs.
asked: 2026-11-16, conversation
answer: "Behalten und ergänzen (Empfohlen)"
answered_by: maintainer
status: answered

In the context of earlier producer records in a header the runner stamps,
facing records that may be false or unreadable, we decided to keep every
readable earlier record and add the record of the run that actually
produced the draft, and to make the check red on an unreadable earlier
record instead of guessing it, to achieve that earlier contributions stay
visible and producers are never collapsed, as decided on 2026-11-07 for
coding-harness-2i7x, accepting that a readable but wrong earlier record
stays until that migration corrects it.
— 2026-11-16

## Q-6 · Scope of the post-run check

context: |
  Topic: what the post-run check checks in the files a run touched.
  Intention: the spec review (finding F-7) found two readings, the record
  shape only or the full header contract of the full verify.
  Today: the full header contract is checked only by the full verify.
  Repository change: the post-run check applies either the record shape
  only or the same header contract as the full verify.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "Ganzer Kopf-Vertrag (Empfohlen)"
answered_by: maintainer
status: answered

In the context of the post-run check on the files a run touched, facing a
record-shape check that the full verify would still refuse later, we
decided that the post-run check applies the same header contract as the
full verify, only earlier and only to the touched files, to achieve that a
header the full verify refuses is refused at the run that wrote it,
accepting that a touched file fails for any header fault, not only for its
producer record.
— 2026-11-16

## Q-7 · Earlier producer records in the post-run check

context: |
  Topic: which producer records in a touched file the post-run check
  judges.
  Intention: the spec review (finding F-11) found two readings of AC 4:
  every record in a touched file's `produced_by`, or only the records this
  run wrote. Active lanes carry old readable records in a legacy form
  (for example `name: Claude Code` with the model in `version`).
  Today: the agent had decided (a [DETAIL] below) that an earlier readable
  record in a legacy form is reported, not refused.
  Repository change: the post-run check either stops the run on any
  producer-header fault in a touched file, earlier readable records
  included, or judges only the records this run wrote.
  Architecture change: none.
asked: 2026-11-16, conversation (spec review finding F-11)
answer: "Ja, jeder Fehler stoppt (Empfohlen)"
answered_by: maintainer
status: answered

In the context of the post-run check on the files a run touched, facing
earlier readable producer records in a legacy form, we decided that the
full header contract applies and any fault stops the run, earlier
readable producer records included, to achieve one contract with no
exemption at the run that touches the file, accepting that a run touching
a file with an old faulty record fails until that record is corrected.
— 2026-11-16

## Q-8 · Producer record of a swarm publication

context: |
  Topic: what the swarm explore route records in `produced_by`.
  Intention: the spec review (finding F-14) found the spec silent on it:
  several member models write the swarm's answer, while AC 1 asks for the
  actual program, model and publication date of the run.
  Today: the route publishes a publisher record
  (`stage2-research-swarm`, the publication day) with no model.
  Repository change: a swarm publication names each member model, keeps
  the publisher record without a model, or is exempt.
  Architecture change: none.
asked: 2026-11-16, conversation (spec review finding F-14)
answer: "Schwarm als Urheber (Empfohlen)"
answered_by: maintainer
status: answered

In the context of a research publication written by several member
models, facing a producer record that asks for one model, we decided that
a swarm publication names the swarm as its producer with the publication
day and no single model, to achieve a true record of who published,
accepting that the member models are not named in the header.
— 2026-11-16

## Q-9 · Park the change for the night or let the runner continue

context: |
  Topic: whether this change pauses for the night or the runner goes on
  with the spec.
  Intention: the spec review left 17 rows open (F-1 to F-17), among them
  the BLOCKER F-1; the maintainer had answered F-11 and F-14 (Q-7, Q-8),
  and F-12 and F-13 still need the maintainer.
  Today: the spec review's findings stand in `findings.md`; the answers
  so far are recorded in Q-7 and Q-8.
  Repository change: either the change is parked until the maintainer
  has answered F-12 and F-13, or the runner works the answered rows into
  the spec now and leaves F-12 and F-13 open.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "Weiterlaufen lassen"
answered_by: maintainer
status: answered

In the context of a spec review with 17 open rows, a BLOCKER among them,
facing two rows (F-12, F-13) that only the maintainer can answer, we
decided that the change is not parked and the runner works the answered
rows into the spec, while F-12 and F-13 stay open for the maintainer, to
achieve progress overnight on what is already settled, accepting that the
spec stays open on F-12 and F-13 until the maintainer answers them.
— 2026-11-16

## Q-10 · Which producer records count as earlier records

context: |
  Topic: the producer record a drafting or repairing session writes about
  itself into the header during the attempt.
  Intention: the spec review (finding F-12) found two readings of "earlier
  records" in Q-5: the records committed before the run, or everything in
  the header when the stamp runs, the session's own self-description
  included. This change's committed `spec.md` shows a false
  self-description (route codex accepted, header naming glm-5.3).
  Today: the spec's open [DECISION] "The current session's
  self-description" offers keeping that record or replacing it with the
  runner's measured record.
  Repository change: either the session's self-written record stays beside
  the runner's record, or only records committed before the run count as
  earlier records and the runner drops what the session wrote into the
  header during the attempt.
  Architecture change: none; the runner stays the one writer of the
  producer record.
asked: 2026-11-17, conversation (spec review finding F-12)
answer: "A"
answered_by: maintainer
status: answered

Recorded in the bead notes (coding-harness-f9sv) on 2026-11-17 as: "F-12:
only producer records committed before the run count as earlier records;
the runner drops whatever the session wrote into the header during the
attempt (answer A)."

In the context of a session that writes its own producer record into the
header during an attempt, facing self-descriptions that name the wrong
program or model, we decided that only producer records committed before
the run count as earlier records and the runner drops whatever the session
wrote into the header during the attempt, to achieve that the record of the
current run is the runner's measurement alone, accepting that a
self-written record is lost.
— 2026-11-17

## Q-11 · Which header fields stamping may change

context: |
  Topic: the header fields the runner's stamp changes on a draft or repair.
  Intention: the spec review (finding F-13) found that AC 5 names no
  closed list of fields the stamp changes, so "unrelated frontmatter" has
  no edge. A new ADR carries `provenance: human-decided`, and the research
  publication today rewrites `provenance`, `produced_by`, `review` and
  `updated` and removes skeleton notices.
  Today: the spec's open [DECISION] "Header fields changed by stamping"
  offers applying the research contract's field rewrites everywhere, or
  keeping `provenance` and resetting approval only on changed content.
  Repository change: a closed list of fields the stamp may change, with
  `provenance` never changed and `review` changed only through the redraft
  reset.
  Architecture change: none; the runner's write rights on the header are
  bounded by the list.
asked: 2026-11-17, conversation (spec review finding F-13)
answer: "A"
answered_by: maintainer
status: answered

Recorded in the bead notes (coding-harness-f9sv) on 2026-11-17 as: "F-13:
closed list — stamping never changes provenance; review only through the
AC 8 redraft reset; removal of skeleton notices declared; the exact field
list is [DETAIL] for the agent (answer A)."

In the context of a stamp that writes into draft and repair headers,
facing an open boundary that could overwrite a human-decided provenance or
an approval, we decided that the stamp works on a closed list of fields,
never changes `provenance`, changes `review` only through the redraft
reset of AC 8, and declares its removal of skeleton notices, with the exact
field list left to the agent as a [DETAIL], to achieve that a test can go
red at the list's edge, accepting that the header check must accept a
kept `provenance` on such documents.
— 2026-11-17

## Q-12 · The four rows of the redraft's spec review (F-18 to F-21)

context: |
  Topic: the four rows the phase-2a review of the redraft of 2026-11-17
  added (findings F-18, F-19, F-20 and F-21).
  Intention: each row left two readings of a criterion open; the night run
  2026-11-16-a parked the lane with one recommendation per row in the
  bead's notes.
  Today: F-18 asks which touched files the post-run check judges; F-19
  whether a readable earlier record keeps its bytes or is normalised; F-20
  where a redraft reset names the approver and whether repair resets too;
  F-21 what happens to an attempt whose changed files were not measured.
  Repository change: the post-run check judges only touched files whose
  header carries `produced_by`; earlier records keep their bytes; the
  approver reset is recorded in the attempt's block in `findings.md`, and
  repair resets like a redraft; an unmeasured draft attempt fails and the
  next route runs.
  Architecture change: none.
asked: 2026-11-17, conversation (spec review findings F-18 to F-21)
answer: "A"
answered_by: maintainer
status: answered

Recorded in the bead notes (coding-harness-f9sv) on 2026-11-17 as:
"F-18..F-21: all four night-run recommendations accepted as one batch
(answer A): F-18 only files whose header carries produced_by; F-19 earlier
records keep their bytes (drafts on a file with an old faulty record fail
until migration bead coding-harness-2i7x runs); F-20 approver reset
recorded in the attempt's findings.md block, repair resets too; F-21 an
unmeasured draft attempt fails and the next route runs."

In the context of four open readings in the redraft's criteria, facing
tests that could not be written against any of them, we decided that the
post-run check judges only touched files whose header carries
`produced_by`, that earlier records keep their bytes, that the approver
reset is recorded in the attempt's block in `findings.md` and repair
resets like a redraft, and that an unmeasured draft attempt fails and the
next route runs, to achieve one testable reading per criterion, accepting
that a draft or repair on a file with an old faulty record fails until
coding-harness-2i7x migrates it.
— 2026-11-17

## Decided by the agent

[DETAIL] **A redraft that changes a document's body resets a non-pending
`review` to pending and names whose approval was reset; stamping that
changes only the header leaves `review` as it is** (spec review finding
F-9). Reason: measured on 2026-11-16 at origin/main aed8eaf0, all 623
`review` headers under `plans/` are pending, so no approval is lost today;
an approval given to other content does not cover changed content, and
naming the reset keeps it visible to the maintainer.

### Historical agent decision — superseded by Q-7

[DETAIL] **The post-run check judges only the producer records this run
wrote, plus the well-formedness of the `produced_by` list; an earlier
record that fails the census rule is reported, not refused, until
coding-harness-2i7x migrates it** (spec review finding F-11). Reason: open
lanes carry such records today, and refusing them would turn those lanes
red, which the split in Q-4 set out to avoid. An earlier record that
cannot be read at all stays red, as Q-5 decided; this detail covers only
readable records in a legacy form.
Superseded on 2026-11-16 by the maintainer's answer in Q-7: any fault
stops the run, earlier readable records included.

## Q-13 · Which header rules the post-run check applies outside research.md

Superseded by the maintainer’s later answer in Q-18 on 2026-11-18: the shared check also judges provenance and review against the committed header.

asked: 2026-11-18, conversation (spec review finding F-22)
answer: "A" (the producer record only)
answered_by: maintainer
status: answered
context: |
  Topic: which header rules the post-run check applies to a touched file
  outside `research.md` whose header carries `produced_by` (a new ADR, a
  document under `docs/`, `spec.md`, `plan.md`).
  Intention: the spec review (finding F-22, a BLOCKER) found that AC 4
  cannot be built until this is settled; the research rules applied
  everywhere would fail every ADR draft, because documents under `docs/`
  carry `created:`, not `date:` (the reviewer reports all 25 files under
  `docs/adr/`, not re-measured).
  Today: the research rules apply only to active `research.md`; documents
  under `docs/` are checked only for key presence; `spec.md` and `plan.md`
  get no producer check.
  Repository change: A = one shared producer-record check (shape, known
  program, date) for every touched file with `produced_by`, the other
  header fields stay with each file's own gate; B = the full research
  rules everywhere, with exceptions; C = one full header contract per
  file type.
  Architecture change: none.
  Recommendation offered: A (catches the free-form `produced_by` fault;
  consequence: a wrong date, review or provenance in a non-research header
  is caught only by that file's own gate; Q-6 is narrowed for non-research
  files).

Recorded in the bead notes (coding-harness-f9sv) on 2026-11-18 as: "A — the
post-run check judges only the producer record (shape, known program, date)
of every touched file with produced_by outside research.md; other header
fields stay with each file's own gate. C goes to its own bead to be thought
through again." That bead is coding-harness-vkd0 (header contracts per file
type), out of scope here.

In the context of the post-run check on touched files outside
`research.md`, facing research header rules that would fail every new ADR
and a full verify that checks no producer field in `spec.md` or `plan.md`,
we decided that the post-run check judges only the producer record (shape,
known program, date) of every touched file outside `research.md` whose
header carries `produced_by`, while every other header field stays with
that file's own gate, narrowing Q-6 for non-research files, to achieve that
the free-form `produced_by` fault is caught on every file a run touches,
accepting that a wrong date, review or provenance in a non-research header
is caught only by that file's own gate until coding-harness-vkd0 settles
per-type contracts.
— 2026-11-18

## Q-14 · What preserved provenance and retained approval are measured against

asked: 2026-11-18, conversation (spec review finding F-23)
answer: "A" (the header committed before the run)
answered_by: maintainer
status: answered
context: |
  Topic: what "the preserved provenance class" and "a valid retained
  approval" in AC 4 (and "an approved document" in AC 8) are measured
  against.
  Intention: the spec review (finding F-23) found two readings; under one
  of them a drafting session could write an approval of its own work into
  a new file and the check would accept it.
  Today: the spec does not say; the leaning in the bead notes was the
  header committed before the run, with an exception for a new ADR.
  Repository change: A = the header committed before the run, with an
  exception for a new ADR; B = the state after the stamp; C = A without
  the ADR exception.
  Architecture change: none.

Recorded in the bead notes (coding-harness-f9sv) on 2026-11-18 as:
"provenance class and approval are measured against the header committed
before the run; a new file must carry ai-drafted-reviewed with a pending
review; exception: a new ADR may carry human-decided as provenance (decided
by PR) but never an approval; an approval written by the session is
refused."

In the context of a post-run check that must tell a preserved provenance
class and a retained approval from ones a session wrote, facing a session
that could otherwise approve its own new file, we decided that both are
measured against the header committed before the run, that a new file must
carry `ai-drafted-reviewed` with a pending review, that a new ADR may carry
`human-decided` as provenance (decided by its pull request) but never an
approval, and that an approval written by the session is refused, to
achieve that no model approves its own work, accepting one named exception
for new ADRs.
— 2026-11-18

## Q-15 · Whether AC 7 covers the explore stamp

asked: 2026-11-18, conversation (spec review finding F-26)
answer: "C" (A, explore too, and bring the migration forward)
answered_by: maintainer
status: answered
context: |
  Topic: whether criterion 7 (earlier producer records keep their bytes)
  holds for the explore stamp too.
  Intention: the spec review (finding F-26) found AC 5 limited to draft
  and repair while AC 7 is not; today the explore publication re-renders
  every earlier record, which is a per-file migration without history,
  and the non-goals give migration to coding-harness-2i7x.
  Today: `research_publication()` in `scripts/stage2.py` normalises earlier
  records when explore publishes.
  Repository change: A = AC 7 holds for explore too; B = draft and repair
  only; C = A, and the migration coding-harness-2i7x is brought forward.
  Architecture change: none.

Recorded in the bead notes (coding-harness-f9sv) on 2026-11-18 as:
"criterion 7 holds for explore too - research_publication stops normalising
earlier records and keeps their bytes (tests in
tests/test_explore_provenance.py change); the migration coding-harness-2i7x
runs as the next change right after this one."

In the context of the explore publication that re-renders earlier producer
records, facing a per-file migration without history that the non-goals
give to coding-harness-2i7x, we decided that criterion 7 holds for explore
too, so `research_publication` stops normalising earlier records and keeps
their bytes, and that the migration coding-harness-2i7x runs as the next
change right after this one, to achieve one rule for every stamp and no
migration outside its own change, accepting that the tests in
`tests/test_explore_provenance.py` that expect normalisation change and
that old faulty records stay until 2i7x lands.
— 2026-11-18

## Q-16 · What counts as a change to an approved document

asked: 2026-11-18, conversation (spec review finding F-30)
answer: "B" (any change outside produced_by and updated)
answered_by: maintainer
status: answered
context: |
  Topic: which change to an approved document resets its approval (AC 8,
  AC 9).
  Intention: the spec review (finding F-30) found that AC 9's condition
  holds for every stamp read literally, and that "body" has two readings.
  Today: the spec speaks of a change to the "body" and leaves the header
  fields open.
  Repository change (the readings in finding F-30): A = the body is the
  text after the closing `---`, so a session that changes only `title`,
  `class`, `appetite` or `adr_files` keeps the approval; B = any change the
  session makes outside `produced_by` and `updated` resets the approval.
  Architecture change: none.

Recorded in the bead notes (coding-harness-f9sv) on 2026-11-18 as: "every
change the session makes to an approved document outside produced_by and
updated (body or any other header field, e.g. appetite, class, adr_files)
resets the approval to pending."

In the context of an approved document a session changes, facing a "body"
whose edge leaves header fields such as `appetite` or `class` open, we
decided that every change the session makes to an approved document
outside `produced_by` and `updated`, in the body or in any other header
field, resets the approval to pending, to achieve that an approval never
covers content it did not see, accepting that a header-only edit such as
an `appetite` change also needs a fresh approval.
— 2026-11-18

## Q-17 · Which verbs the post-run check covers

asked: 2026-11-18, conversation (spec review finding F-31)
answer: "C" (one shared check point after every verb that writes files)
answered_by: maintainer
status: answered
context: |
  Topic: which runner verbs run the post-run header check of AC 4.
  Intention: the spec review (finding F-31) found that `explore()` and
  `spec_review()` in `scripts/stage2.py` write files without a post-run
  check, so the explore stamp would never be judged.
  Today: only draft, implement and repair check their result.
  Repository change (the readings in finding F-31): A = only the verbs
  that already check their result get the producer check; B = Q-4's
  "every verb's post-run check", so explore, spec-review and every other
  verb gain one. The bead notes record the answer C, not the wording of
  the option as offered.
  Architecture change: one shared post-run check point in
  `scripts/stage2.py` (as the answer records it).

Recorded in the bead notes (coding-harness-f9sv) on 2026-11-18 as: "one
shared post-run check point in scripts/stage2.py runs after every verb that
writes files (explore, draft, spec-review, implement, repair, ...), new
verbs included automatically; explore and spec-review may fail on a faulty
header from now on."

In the context of runner verbs that write files with and without a
post-run check, facing an explore stamp that no check would judge, we
decided that one shared post-run check point in `scripts/stage2.py` runs
after every verb that writes files (explore, draft, spec-review, implement,
repair and any other), new verbs included automatically, to achieve one
choke point that no writing verb reaches around, accepting that explore and
spec-review may fail on a faulty header from now on.
— 2026-11-18

## Q-18 · Who stops a model from approving its own new non-research file

asked: 2026-11-18
answer: "D: Prüfpunkt + Klasse und Freigabe" — in English: option D, the check point plus class and approval. The shared post-run check point judges, for every touched file, the producer record and in addition `provenance` and `review` against the header committed before the run; all other header fields stay with each file's own gate. A self-approval makes the attempt red, implement included.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a row F-32 — a drafting session writes `provenance: human-written` and `review: {status: approved, approved_by: "@MPAdesso", ...}` into a new spec.md; nothing named refuses it.
  Intention: two earlier answers pulled apart here: Q-13 (F-22 A) limits the shared check outside research to the producer record; Q-14 (F-23 A) measures class and approval against the header committed before the run and refuses a session-written approval.
  Today: no check reads class or review of a non-research file after a run, so the self-approval would be committed.
  Repository change: a rule in the shared post-run check point (Q-17) plus tests.
  Architecture change: none.
  Options shown: D check point judges producer record plus provenance and review against the committed header, other fields stay with each file's gate (recommended); A the whole header against the committed state (contradicts Q-13, touches every file on implement); C only draft and repair refuse at stamp time (new Markdown files from implement stay unchecked); B research only (a self-approved spec.md is committed, contradicting Q-14).

In the context of a shared post-run check point that Q-13 limited to the
producer record outside research, facing Q-14's rule that no session-written
approval may stand, we decided that the check point judges the producer
record and in addition provenance and review of every touched file against
the header committed before the run, to achieve that no model can approve its
own work in any file, accepting that implement attempts too go red on a
self-approval while every other header field stays with each file's own
gate. — 2026-11-18

## Agent decisions on the third phase-2a rows F-33..F-38 — 2026-11-18

Third and last spec-review round (maintainer rule of 2026-11-18: triage each
round, at most three rounds). `[DETAIL]` decisions by the orchestrating
session (Opus 5.5), each derived from Q-14, Q-16, Q-17 and Q-18, shown as one
list and accepted as proposed ("A: So übernehmen"). No fourth review runs;
the final draft works these in.

- **F-33, the explore stamp and class/approval.** A downgrade is allowed, an
  upgrade never: explore sets `provenance: ai-drafted-reviewed` and a pending
  review as today, so a `human-written` skeleton becomes `ai-drafted-reviewed`
  and an approved `research.md` loses its approval when explore appends to it.
  Reason: a model may never create an approval nor keep one over content it
  changed (Q-14, Q-16).
- **F-34, the census in make verify.** The post-run check point and the
  research census use one shared function; for research its contract stays
  as today (a file with a model record is `ai-drafted-reviewed` and pending).
  Reason: one rule, and no run passes that the next full verify refuses (Q-6).
- **F-35, converting a block mapping.** The compact sequence form
  (`produced_by:` followed by `- kind: …` with the later record lines
  unchanged) counts as keeping the earlier record's bytes; a block mapping is
  always converted, never refused. Reason: otherwise every repair touching one
  of 112 files fails on every route.
- **F-36, what a rejection does.** explore and spec-review check the content
  before writing it. A fault in the model's output fails the attempt and the
  next route runs; a fault in a committed earlier record stops the verb with a
  message naming the migration coding-harness-2i7x, without spending a further
  paid route. Reason: no paid attempt on a fault no model can fix.
- **F-37, what counts as research.** Active `plans/changes/<name>/research.md`
  only, the census scope; `archive/` and `docs/research/` get the producer-
  record check alone. Reason: `docs/research/` uses another header form.
- **F-38, what is model-written.** Any file with frontmatter the attempt
  changed gets a producer record appended; its class stays protected by Q-18.
  Whether a model may edit a `human-decided` file at all is governed by
  `decisions/provenance.yaml`, not by this change. Reason: an honest trace of
  who touched a file.

## Q-19 · Raise appetite, field-level header check, and active-change migration with gate

asked: 2026-11-20, conversation (review-loop round 9, finding L9-1)
answer: "Option 2 — extend appetite beyond 12 h as needed, make the runner's header check field-level, migrate legacy producer records of active changes once, and add a gate keeping active changes in the new form"
answered_by: maintainer
status: answered
context: |
  Topic: review-loop round 9 finding L9-1 (runner `updated:` stamps and untouched legacy headers triggering false committed-record faults on active changes) and the change's appetite budget.
  Intention: round 9 showed that whole-header judgement blocks runner appends (`spec-review`, `review-loop`, `release-loop`) on active changes still carrying legacy `produced_by` headers until the separate migration lands; the change had already reached its prior 10 h / 12 h appetite.
  Today: the post-run and pre-publication checks judge whole headers via set inclusion against committed faults, 21 active change artifacts in this checkout still carry legacy `produced_by` headers, and no blocking gate prevents new legacy producer records in active changes.
  Repository change: extend appetite to 16 h (as needed to finish cleanly); make the runner's header check field-level so untouched committed legacy fields never trigger false stops while changed/introduced faults are always refused as output faults; migrate the 21 legacy producer records of active changes under `plans/changes/` (outside `archive/`) once; wire the shared producer-record check into the `plans-registry` blocking gate for active changes (keeping `decisions/gates.yaml` untouched and archived headers under `coding-harness-2i7x`).
  Architecture change: the producer-record contract lives once in `scripts/plans_registry.py` (re-exported by `scripts/research_census.py` and consumed by `scripts/stage2.py`), and `scripts/stage2.py` classifies header problems field-by-field.

In the context of round-9 finding L9-1 where untouched legacy producer headers blocked runner housekeeping writes and the change approached its appetite limit, facing the choice between deferring the fix or finishing the root mechanism here, we decided to raise the appetite (beyond 12 h as needed, set to 16 h), make the runner's header check field-level, migrate the legacy producer records of active changes under `plans/changes/` once, and enforce the shared producer-record contract on active changes through the `plans-registry` gate, to achieve that untouched legacy headers never cause false stops and active changes stay cleanly in the new producer form without touching `decisions/gates.yaml`, accepting a larger one-time diff over active change headers while archived headers remain under `coding-harness-2i7x`.
— 2026-11-20
