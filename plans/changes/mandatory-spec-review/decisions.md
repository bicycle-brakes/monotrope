---
title: "Decisions — mandatory-spec-review"
category: decisions
status: draft
implementation_status: none
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-18
supersedes: null
superseded_by: null
bead: coding-harness-ttic
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, spec-review, stage-2, runner]
---

# mandatory-spec-review — Decisions

Class: bounded (bead coding-harness-ttic: doctrine plus one runner check).

The intent itself is settled and not asked again: the maintainer answered
"jaja" on 2026-11-16 to making the Opus spec review (phase 2a) mandatory
before a plan card for the classes `bounded`, `feature` and `architectural`,
with `spike` exempt (bead description). ADR 0016 point 5 already decides that
Opus 5.5 reviews the spec for every change stage 2 routes; this change aligns
the doctrine and the runner with it, no ADR change (bead notes, 2026-11-16).

## Q-1 · Which changes the new refusal reaches

asked: 2026-11-17
answer: "C" — the refusal applies to implement calls from the merge of this change on; changes already implemented stay untouched (a later implement call needs the review). In addition the morning handover lists open changes without a spec review, and the maintainer decides per change whether one is caught up (xul8 already planned).
answered_by: maintainer
status: answered
context: |
  Topic: the runner will refuse `stage2.py implement` while a change's spec has no spec-review rows dated after the spec's last change, or has open [AMBIGUITY] rows (bead coding-harness-ttic).
  Intention: decided before the night run 2026-11-17-a so the lane can build without waiting; open changes already exist that were planned or implemented without a spec review, so the reach of the refusal has to be fixed first.
  Today: phase 2a is called optional in AGENTS.md and docs/WORKFLOW.md; nothing in the runner checks for spec-review rows, so implement runs whether or not a review was held; two plan cards were shown unreviewed on 2026-11-16.
  Repository change: the doctrine marks phase 2a mandatory for bounded, feature and architectural changes; the runner's implement verb refuses without a current spec review; the morning handover lists open changes that have none.
  Architecture change: none; one more precondition in an existing runner verb, no new verb, gate or ADR.

In the context of making the phase-2a spec review mandatory before implement, facing open changes that were planned or implemented without one, we decided that the runner's refusal applies to every implement call from the merge of this change on, leaves already implemented changes untouched, and that the morning handover lists open changes without a spec review for the maintainer to decide per change, to achieve that no new implementation starts from an unreviewed spec without retroactively blocking finished work, accepting that changes implemented before the merge stay unreviewed until the maintainer chooses to catch one up. — 2026-11-17

*Note (2026-11-17, recording agent): the answer is taken verbatim from the
bead notes of coding-harness-ttic ("2026-11-17 interview (night prep, answer
C)"). The exact wording of the question shown before the night run was not
recorded there; the context above is restated from the bead description and
notes, not invented beyond them.*

## Q-2 · Which spec change makes a spec review stale (row S-1)

asked: 2026-11-18
answer: "A" — every change to the spec after the review makes the review stale; the chain becomes draft -> review -> second draft -> re-review until a review is clean (at least one more Opus call).
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a row S-1 (the Opus spec review's finding that the spec does not say which spec change makes a review stale). The documented chain rewrites spec.md in a second draft after the review, to work the review's rows in.
  Intention: the implement refusal compares the review with "the spec's last change"; the night run 2026-11-17-a parked this lane at the phase-2a gate until the seven open rows were answered.
  Today: implement reads no spec review at all; the second draft follows the review and the plan card follows the second draft, with no second review.
  Repository change: option A, any spec change after the review makes it stale, so the chain gains a re-review after the second draft (one more Opus call); option B, a redraft that only works the 2a rows in does not count, which needs a rule telling such a redraft apart from any other edit, and the spec gives none.
  Architecture change: none; the draft chain in docs/WORKFLOW.md and prompts/02-spec.md gains a step, no new verb, gate or ADR.

In the context of making the phase-2a spec review a precondition of implement, facing a draft chain that rewrites the spec after its review, we decided that every change to spec.md after a review makes that review stale, so the chain runs draft, review, second draft and re-review until a review is clean, to achieve that implement only ever starts from a spec a review has read as it stands, accepting at least one more Opus call per change whose first review had rows. — 2026-11-18

## Q-3 · How the runner decides a review is still current (row S-2)

asked: 2026-11-18
answer: "A" — a shared runner building block: one writer of a fingerprint of the reviewed object (for phase 2a the sha256 of spec.md as read, written into the 2a block), one check "is this review still current?", a legacy reader comparing by day for blocks without a fingerprint; uncommitted spec edits count as a change. Review-loop rounds and the phase-6 verdict follow in bead coding-harness-4amm.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a row S-2 (the spec does not say where the spec's change time comes from or how it is compared with the review). The 2a block heading carries only a day.
  Intention: the refusal must decide whether a review read the current spec; a same-day redraft cannot be told apart by days, and the review loop (phase 4b) and the phase-6 verdict share the same gap.
  Today: the 2a heading is "## Phase 2a — Opus 5.5, <date>"; the spec's own updated: header is a day written by the author; nothing compares the two.
  Repository change: recommended first, a UTC time in the review heading compared with the last commit touching spec.md, uncommitted spec edits refused, date-only blocks compared by day; after the comparison with the review loop and phase 6, option A, a shared runner building block that writes a fingerprint (sha256) of the reviewed object into the block and one check that compares it, with the by-day reader for old blocks.
  Architecture change: one new shared building block in the runner (one writer of the fingerprint, one currency check), used here for phase 2a and later by the loop rounds and phase 6 (bead coding-harness-4amm); no new verb, gate or ADR.

In the context of the implement refusal needing to know whether a spec review read the current spec, facing day-only review headings and the same gap in the review loop and phase 6, we decided on one shared runner building block that writes the sha256 of spec.md as read into the 2a block and one check that tells whether the review is still current, with a by-day legacy reader for blocks without a fingerprint and uncommitted spec edits counting as a change, to achieve one writer and one check that the loop rounds and phase 6 can reuse, accepting that old blocks are compared only by day and that the loop and phase-6 users are built in a later change (bead coding-harness-4amm). — 2026-11-18

## Q-4 · Which records count as a spec review (row S-3)

asked: 2026-11-18
answer: "A" — only runner-written "## Phase 2a — Opus 5.5" blocks count (and, per Q-6, the declared fallback reviewer's blocks); a block whose answer was not readable as rows does not count (fail closed); Codex and hand-held reviews do not count.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a row S-3 (which records count as a spec review). Findings files hold runner blocks "## Phase 2a — Opus 5.5", older Codex blocks "## Phase 2a — Codex" and hand-written SPEC rows under other headings after a skipped phase 2a.
  Intention: the refusal must recognise a review; counting any "## Phase 2a" block would let a Codex review admit implement although the doctrine requires Opus.
  Today: implement reads no review; the runner records a 2a answer that was not six-cell rows as such, so an [AMBIGUITY] in it stands in no row.
  Repository change: recommended option A, only runner blocks headed "Opus 5.5" count and an unreadable answer fails closed; the other reading counts any "## Phase 2a" block.
  Architecture change: none; the refusal reads the runner's own blocks only.

In the context of the implement refusal recognising a spec review, facing three kinds of 2a records of differing trust in existing findings files, we decided that only runner-written Opus 5.5 blocks, and the declared fallback reviewer's blocks, count, that a block whose answer was not readable as rows does not count, and that Codex and hand-held reviews do not count, to achieve that implement is admitted only by a review the runner itself recorded in rows it can read, accepting that changes reviewed by Codex or by hand need a new runner review before a later implement call. — 2026-11-18

## Q-5 · What makes an ambiguity row open (row S-4)

asked: 2026-11-18
answer: "A" — only the newest current block is read; a row is open when its Severity or Finding cell begins [AMBIGUITY] and its Status begins "open"; an answered but unmoved row refuses, and the refusal names it.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a row S-4 (what makes an [AMBIGUITY] row open, which cell carries the marker, and whether every 2a block or only the latest is read).
  Intention: the refusal must find open ambiguities without matching a finding that only quotes the phrase "no open [AMBIGUITY]", and without an old block's row refusing after a later clean review.
  Today: the runner writes Status "open" on every row; an answered row may move to "in spec", "rejected — …", "resolved <date> by <source>" or "answered", or stay unmoved.
  Repository change: recommended option A, only the latest block is read and a row is open when Severity or Finding begins [AMBIGUITY] and Status begins "open"; the other reading treats a row as open while no answer is recorded and ignores the Status cell.
  Architecture change: none; one reading rule inside the new precondition.

In the context of the implement refusal deciding whether a spec review leaves an ambiguity open, facing free-text severity cells, rows that quote the gate phrase and several 2a blocks per change, we decided to read only the newest current block and to treat a row as open when its Severity or Finding cell begins [AMBIGUITY] and its Status begins "open", so that an answered but unmoved row refuses and the refusal names it, to achieve a check that reads one cell pair in one block and points at the exact row to move, accepting that an answer recorded in decisions.md does not count until its row's Status is moved. — 2026-11-18

## Q-6 · The duty under --stage2-off and when Opus is unreachable (row S-5)

asked: 2026-11-18
answer: "Pflicht und Ersatzprüfer DeepSeek via Pi, aber das muss zentral und einfach umzustellen sein" (English: "mandatory, and DeepSeek via Pi as the fallback reviewer, but it has to be central and easy to switch") — the duty applies everywhere, --stage2-off included; when Opus is unreachable: one retry after a pause, then a declared fallback reviewer, a DeepSeek model through Pi (OpenCode Go, with the stage-2 leak check as for every foreign call), runs through the same spec-review verb, named in one central configuration entry so a switch is one value; the block is marked as fallback, the morning handover lists it, and Opus re-checks it by day.
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a row S-5 (whether "implement --stage2-off [REASON]" is subject to the new precondition). That route keeps stage 1, spec-review has no stage-1 route, and night runs may meet an unreachable Opus.
  Intention: exempting the route would let any change reach implement unreviewed just by adding the flag; applying it without a fallback would block every bounded, feature or architectural change while Opus cannot be reached.
  Today: the stage-1 route skips class derivation; spec-review runs only on Opus 5.5 and has no fallback.
  Repository change: recommended option A, the check applies on --stage2-off too; the other reading lets the stage-1 route skip the check. After a discussion of night runs the maintainer chose the duty everywhere plus a declared fallback reviewer in the same spec-review verb.
  Architecture change: the spec-review verb gains one declared fallback reviewer (a DeepSeek model through Pi on OpenCode Go), named in one central configuration entry (ties to beads coding-harness-twvx and coding-harness-wq1m); no new verb, gate or ADR.

In the context of making the phase-2a spec review a precondition of every implement call, facing a stage-1 route that has no spec-review and night runs that may meet an unreachable Opus, we decided that the duty applies everywhere, --stage2-off included, and that spec-review retries Opus once after a pause and then runs a declared fallback reviewer, a DeepSeek model through Pi with the stage-2 leak check, named in one central configuration entry so that a switch is one value, its block marked as fallback, listed in the morning handover and re-checked by Opus by day, to achieve that no change implements unreviewed and that a night run is not stopped by an unreachable Opus, accepting a foreign fallback model whose data terms are due for re-reading before 2026-11-30 (bead coding-harness-hw7w) and one more Opus review by day for every fallback block. — 2026-11-18

## Q-7 · How implement learns the class (row S-6)

asked: 2026-11-18
answer: "A" — implement uses the shared class reader of explore (declared_class: research.md and spec.md); a missing, invalid or disagreeing class refuses with the remedy "add class:".
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a row S-6 (a hole: the spec does not say how implement learns the class that decides whether the duty applies; spikes are exempt).
  Intention: failing open would exempt a change with no class header as if it were a spike; failing closed needs a clear remedy, since previously implemented changes are the most likely to lack a header.
  Today: implement reads no class; only explore runs declared_class, which reads research.md and spec.md and refuses when no class is stated.
  Repository change: recommended option A, implement reads the class through the explore class reader, and a missing or invalid class is refused with the remedy "add class:".
  Architecture change: none; implement reuses the existing class reader, no second reader.

In the context of implement deciding whether the spec-review duty applies, facing a verb that reads no class today and older changes without a class header, we decided that implement uses the shared class reader of explore over research.md and spec.md and refuses a missing, invalid or disagreeing class with the remedy "add class:", to achieve one class reader for every verb and no silent exemption of an unclassified change, accepting that a change without a class header must have one added before it can implement. — 2026-11-18

## Q-8 · Which changes the morning handover lists (row S-7)

asked: 2026-11-18
answer: "C" — the morning handover lists every non-archived change of class bounded, feature or architectural, or without a class, that has no current review free of open ambiguity (the same check as implement), including changes already implemented but not archived; fallback (DeepSeek) reviews are listed with "Opus re-checks".
answered_by: maintainer
status: answered
context: |
  Topic: phase-2a row S-7 (which changes the morning handover lists as lacking a spec review, per Q-1).
  Intention: the maintainer decides per change whether a review is caught up; the list has to match what implement would refuse, so a stale review is not first learnt of from a refusal.
  Today: no handover lists spec-review status; "without a spec review" could mean no 2a block at all or no current, ambiguity-free review.
  Repository change: recommended, the handover lists open non-archived bounded, feature, architectural and classless changes without a current review; the maintainer chose C, which uses the same check as implement, includes changes already implemented but not archived, and lists fallback reviews as "Opus re-checks".
  Architecture change: none; the handover reuses the implement check.

In the context of the morning handover listing changes that lack a spec review, facing open, implemented-but-unarchived and fallback-reviewed changes, we decided that the handover lists every non-archived change of class bounded, feature or architectural or without a class that has no current review free of open ambiguity by the same check as implement, implemented but unarchived changes included, and lists fallback reviews with "Opus re-checks", to achieve that the maintainer sees exactly what implement would refuse and what still needs an Opus review, accepting a longer morning list. — 2026-11-18

*Note (2026-11-18, recording agent): the answers to Q-2..Q-8 are taken from
the bead notes of coding-harness-ttic ("2026-11-18 maintainer answers"); the
only verbatim wording recorded there is the one quoted in Q-6. The options
as shown were not recorded beyond the recommendation package of 2026-11-18
00:15Z and the readings in findings.md rows S-1..S-7; the contexts above are
restated from those, not invented beyond them. Option letters other than
those named are not recorded.*
