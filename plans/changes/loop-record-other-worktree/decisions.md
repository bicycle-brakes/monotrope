---
title: "Decisions — loop-record-other-worktree"
category: decisions
status: draft
implementation_status: none
date: 2026-11-18
created: 2026-11-18
last_reviewed: 2026-11-18
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-e82i
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, review-loop, stage2]
---

# loop-record-other-worktree — Decisions

Class: bounded (bead coding-harness-e82i; one answered question is owed —
Q-1 below, answered by the maintainer on 2026-11-18 in the day session after
the night run 2026-11-17-a).

## Q-1 · What the runner does when a change continues in a new worktree

asked: 2026-11-18
answer: "A: Ablösen per Befehl" — in English: option A, supersede by command. The refusal names records of the same change found under other keys. A new form `release-loop <change> --restart --supersedes <key> --reason <text>` lets the runner itself write one accounting line into findings.md (the superseded record's key, its rounds and the audit calls it accounts for) and move the old record into an archive beside the state directory; the next `review-loop` starts a fresh run. Accepted downside as shown with the option: exactly one command may read another worktree's key of the same change and mark it superseded; everywhere else each worktree's record stays private (R-2).
answered_by: maintainer
status: answered
context: |
  Topic: the review-loop record of a change that continues in a new worktree (bead coding-harness-e82i).
  Intention: lane L4 (bead coding-harness-xul8, change pi-neutral-paths) is blocked: its second attempt runs in worktree pi-neutral-paths-v2, while the first attempt's loop record (rounds 1 to 3, never released) sits under the key of the old worktree pi-neutral-paths. Every re-sliced lane (L1, L2 of the same night) can hit the same trap.
  Today: the record key is the change name plus the first eight hex digits of the sha256 of the worktree path (record_key in scripts/stage2.py), so each worktree's record is private (R-2 of the 2026-10-20 runner review). No verb looks across keys. findings.md of the new worktree carries the old attempt's seven review-loop audit lines but none of its rounds, so review-loop, release-loop and `release-loop --restart` refuse, and the refusal only says the record may sit "under another state directory". docs/WORKFLOW.md asks the maintainer to reconcile by hand but names no form; every line the runner accepts is runner output and would state something false here.
  Repository change: scripts/stage2.py (the refusal names other keys of the same change; release-loop gains the supersede form), tests, docs/WORKFLOW.md §4 (loop record).
  Architecture change: one command may read another worktree's record key of the same change and mark it superseded; the privacy of each worktree's record stays otherwise.
  Options shown: A supersede by command (recommended); B only name the other records in the refusal (L4 stays blocked); C key by change and branch instead of worktree path (changes R-2 isolation and the key in three places); D like A but the old record stays in place, only marked (the old worktree could later continue its loop by mistake).

In the context of a change whose review loop continues in a new worktree
while the old worktree's record stays under its own key, facing a refusal
that no honest hand line can pass and a doctrine that names no form for the
maintainer's reconciliation, we decided that the runner names records of the
same change under other keys and supersedes one through
`release-loop --restart --supersedes <key> --reason <text>`, writing the
accounting line itself and archiving the old record, to achieve a restart
that the runner records truthfully and that no other worktree can continue by
mistake, accepting that exactly one command reads across worktree keys of the
same change. — 2026-11-18

## Q-2 · How the review loop ends after round 6

asked: 2026-11-19
answer: "A: Reparieren + ersetzt" — in English: case repair ends; the orchestrator takes L6-2, L6-3, L6-5 and L6-6 and aligns criterion 2's text with S-14 (L6-1); for L6-4 the superseded worktree's `release-loop` recognises the archive by the accounting line and writes "superseded by <key>" instead of a false line. Then one more round and phase 6.
answered_by: maintainer
status: answered
context: |
  Topic: review-loop round 6 of this change opened the supersession mechanism a fourth time.
  Intention: the night rule ends case repair at a further finding of one mechanism; the maintainer decides how the change finishes.
  Today: six rounds ran; all taken rows of rounds 1-3 are repaired; round 6 raised L6-1 (criterion 2's wording disagrees with S-14), L6-2 (a partially moved record is finalised incomplete on retry), L6-3 (other worktrees' records read outside their lock), L6-4 (the superseded worktree has no honest release), L6-5 and L6-6 (refusal-text gaps).
  Repository change: scripts/stage2.py (supersession, release-loop), docs/WORKFLOW.md, spec criterion 2, tests; one more round, then phase 6.
  Architecture change: release-loop knows a superseded state.
  Options shown: A repair and add the superseded release (recommended); B ship L6-3 and L6-4 as named limits with a follow-up bead; C re-slice supersession into its own change.

In the context of a supersession mechanism that a fourth review round still
found incomplete, facing a superseded worktree that can only write a false
release line, we decided to repair the round-6 rows and give release-loop a
"superseded by <key>" outcome, to achieve an honest record on both
worktrees, accepting one or two more loop rounds — 2026-11-19

## Agent decisions on the phase-2a rows S-1..S-7 — 2026-11-18

`[DETAIL]` decisions, taken by the orchestrating session (Opus 5.5) and shown
to the maintainer as one list, who accepted them as proposed on 2026-11-18
("A: So übernehmen"). Each is freely revisable before implementation.

- **S-1, where the archive lives.** In a tree of its own beside `stage2/`:
  `<state>/coding-harness/stage2-superseded/<change>@<digest>@<UTC timestamp>/`.
  The scan for other keys of the same change never meets it, and a second
  supersession of the same key never overwrites the first archive. The
  accounting line names the archive path. Reason: the key namespace stays
  exactly what criterion 1's scan reads.
- **S-2, which audit calls the line accounts for.** Every review-loop audit
  line pending since the last release or restart, the set
  `lost_record_refusal` counts. When the scan finds more than one other key
  of the change, the supersession must name all of them in one call
  (`--supersedes` repeatable) or it refuses and names them. With no pending
  call it refuses: there is nothing to account for (superseded by S-15). Reason: audit lines carry
  no key, so any attribution to one record would be a guess.
- **S-3, the kind of line.** A restart under the ADR 0021 restart amendment:
  `Loop restarted: <date> after round <N> — superseded record <key> (rounds
  <a>–<b>, archived at <path>), audit calls <M> — <reason>`, with N the
  highest round number in the superseded record(s). Every existing restart
  reader then applies: the verdict floor, the stop floor, `restarted_fresh`
  and the already-restarted refusal. Reason: the existing rule "a restarted
  run is released only after a new phase-6 verdict" keeps holding without a
  second line kind.
- **S-4, an interrupted supersession.** Archive first, then write the line.
  A retry that finds the key absent at its old place, present in the archive
  and no accounting line for it writes the line only and completes. A false
  completed restart is the observable state "the line stands in findings.md
  while the record is still active at its old key"; this order never
  produces it. Reason: the only half-done state allowed is one the retry
  recognises from the archive alone.
- **S-5, which refusals name other keys.** Every no-record refusal —
  `lost_record_refusal`, `restart_loop`'s missing-record refusal and
  triage's no-record refusal — names records of the same change under other
  keys, through one shared helper. Reason: the incident's own path was
  `release-loop --restart`.
- **S-6, "its rounds".** The round number range, e.g. "rounds 1–3"; the
  restart's N is the highest of them, so the next round continues after it
  and no row id repeats. The audit calls are given as a count.
- **S-7, release after a supersession with no new round.** `release-loop`
  refuses and writes nothing ("no round ran since the supersession; run
  review-loop first"). Reason: the old "the loop did not run" line would be
  false here.

## Agent decisions on the second phase-2a rows S-8..S-13 — 2026-11-18

`[DETAIL]` decisions by the orchestrating session (Opus 5.5), shown to the
maintainer as one list and accepted as proposed on 2026-11-18 ("A: So
übernehmen"). Each is freely revisable before implementation.

- **S-8, round numbers and stops after a supersession.** The run after a
  restart numbers its rounds from the restart floor: round number = N (the
  restart line's round) + rounds run since the restart + 1, for every later
  round and after the run's own release too. The stops (clean stop, repair
  brake) count only rounds after the floor, so a clean round N+1 stops the
  loop. Reason: otherwise the clean stop does not fire and a paid stage runs
  for nothing.
- **S-9, an unfinished supersession.** One supersession moves all of its keys
  into one archive directory, first under a staging name, with a manifest
  listing the keys and the key of the worktree that supersedes them; the
  staging directory is renamed into place, then the line is written. A retry
  completes only an archive whose manifest names its own worktree key and the
  same key set; any other archive is not "unfinished" for it. Reason: no
  worktree completes another's supersession, and no key is dropped from an
  interrupted multi-key supersession.
- **S-10, a plain restart while other-worktree records are active.**
  `release-loop --restart --reason` without `--supersedes` refuses while a
  record of the same change is active under another key, names the keys and
  points to `--supersedes`. Reason: otherwise the fresh run repeats the old
  record's round numbers.
- **S-11, which releases criterion 10 covers.** Only releases after a
  supersession restart with no round after it refuse; the runner recognises
  that restart by the fixed clause "superseded record" in its own line form,
  through one pattern. A plain restart keeps today's release behaviour.
  Reason: criterion 9 keeps plain restarts unchanged.
- **S-12, what the archive takes.** Everything a release would delete from
  the key directory — `loop.md` and the prepare-loop receipt
  `availability.json` included; research state, research receipts and probe
  audits stay in place (criterion 8). Reason: the new run must not consume
  the old worktree's receipt.
- **S-13, how the line writes the archive path.** In the form
  `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2-superseded/<dir>`,
  as docs/WORKFLOW.md writes record paths; a retry matches a line to its
  archive by `<dir>`. Reason: no home directory in a committed file, and the
  leak check stays quiet.

## Agent decisions on the third phase-2a rows S-14..S-18 — 2026-11-18

Third and last spec-review round (maintainer rule of 2026-11-18: triage each
round, at most three rounds). `[DETAIL]` decisions by the orchestrating
session (Opus 5.5), shown as one list and accepted as proposed ("A: So
übernehmen"). No fourth review runs; the final draft works these in.

- **S-14, N of a later plain restart.** N is the highest round number ever
  given in this change's loop, across a supersession (the restart floor and
  every numbered round after it), never a count. Reason: no round number is
  given twice and no restart line misstates its round.
- **S-15, no way out.** `--supersedes` is allowed with no pending audit call
  when the named key holds an active record of the change; the line then says
  "audit calls 0". Reason: the maintainer can always restart without deleting
  a record directory by hand.
- **S-16, which keys are "other worktree keys".** Only digests of this
  repository's worktrees as `git worktree list` reports them; a record of
  another repository with a change of the same name is never named, refused
  on or archived. A worktree still listed by git remains discoverable even if its directory
  is gone; once pruned from git metadata, its record is not seen — a named limit. Reason: no command may touch another repository's state.
- **S-17, archive layout for several keys.**
  `<change>@<digest of the superseding worktree>@<UTC timestamp>/<key>/…`,
  one subdirectory per superseded key, with the manifest at the top; the
  accounting line lists each key with its round range and archive
  subdirectory. Reason: two `loop.md` files cannot collide, and every key
  stays findable.
- **S-18, an interrupted supersession whose key set changed before the
  retry.** Not recoverable by a verb in this change: a named limit in
  plan.md; follow-up bead coding-harness-0aht adds a verb to abandon or roll back such a
  supersession. Reason: rare, and a further verb would grow this change again.
