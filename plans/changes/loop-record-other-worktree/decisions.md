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
