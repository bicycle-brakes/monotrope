---
title: "Decisions — loop-record-other-worktree"
category: decisions
status: draft
implementation_status: none
date: 2026-11-18
created: 2026-11-18
last_reviewed: 2026-11-18
updated: 2026-11-18
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
  call it refuses: there is nothing to account for. Reason: audit lines carry
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
