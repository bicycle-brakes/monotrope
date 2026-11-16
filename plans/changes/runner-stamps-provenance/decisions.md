---
title: "Decisions — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: claude-opus-5-5, version: "2026-11-16"}
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

## Decided by the agent

[DETAIL] **A redraft that changes a document's body resets a non-pending
`review` to pending and names whose approval was reset; stamping that
changes only the header leaves `review` as it is** (spec review finding
F-9). Reason: measured on 2026-11-16 at origin/main aed8eaf0, all 623
`review` headers under `plans/` are pending, so no approval is lost today;
an approval given to other content does not cover changed content, and
naming the reset keeps it visible to the maintainer.

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
