---
title: "Decisions — verify-slots"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verify-lock, make-verify]
---

# verify-slots — Decisions

Class: bounded (bead coding-harness-u1ha).

## Q-1 · How many full checks may run at once

asked: 2026-11-09
answer: "Ich erlaube 2 parallel make verify" — two full checks (`make verify`) may run at the same time on the machine.
answered_by: maintainer
status: answered
context: |
  Topic: the machine-wide verify lock (scripts/verify_lock.py) admits one full check at a time; on 2026-11-09 five repair lanes waited one to five hours each at the lock while one check of about 25 minutes ran.
  Intention: shorten the wait without overloading the machine.
  Today: one exclusive work lock, FIFO admission, a free-memory check before work starts.
  Repository change: the lock admits N holders at once, FIFO kept, the memory check per admission.
  Architecture change: none.

## Q-2 · Where the number lives

asked: 2026-11-09
answer: "Das muss auch zentral leicht änderbar sein in Zukunft" — the slot count is a value that is easy to change in one central place (default 2), later inside the central harness configuration (bead coding-harness-twvx); no constant repeats it.
answered_by: maintainer
status: answered
context: |
  Topic: the slot count needs a home.
  Intention: change it without a code change when the machine or the measurements say so.
  Today: no setting exists; one slot is built into the lock.
  Repository change: one declared value read by the lock, validated; documentation names it.
  Architecture change: none; the central configuration file is its own change (bead coding-harness-twvx).

Evidence to keep in view (bead coding-harness-p6mu): three concurrent full
checks once drove the load above 100 and each check past 30 minutes, against
11–12 minutes run one after the other. Two slots must be measured (wall time
and load) before the change counts as done.
