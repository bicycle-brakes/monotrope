---
title: "Decisions — verify-slots"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-15
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

In the context of the machine-wide verify lock, which admits one full check at
a time, facing repair lanes that waited one to five hours each at the lock
while one check of about 25 minutes ran, we decided that two full checks may
run at the same time on the machine, to achieve a shorter wait, accepting that
two checks side by side each run slower and that the effect must be measured
before the change counts as done — 2026-11-09

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

In the context of the slot count of the verify lock, facing a value that the
machine and later measurements may change, we decided that the count lives in
one central, easily changed place with the default 2 and that no constant
repeats it, to achieve a change of the count without a code change, accepting
that the central harness configuration is its own change (bead
coding-harness-twvx) and the value moves there later — 2026-11-09

Evidence to keep in view (bead coding-harness-p6mu): three concurrent full
checks once drove the load above 100 and each check past 30 minutes, against
11–12 minutes run one after the other. Two slots must be measured (wall time
and load) before the change counts as done.

## Q-3 · Under which load the paired trial runs

asked: 2026-11-14
answer: the paired trial runs under the night load — the other lanes keep working — not on an idle machine. (Relayed in English by the orchestrator; the German original was not passed to the recording session.)
answered_by: maintainer
status: answered
context: |
  Topic: the trial of two simultaneous full checks that criterion 11 requires.
  Intention: measure the slots the way they will be used, beside running lanes.
  Today: the plan asked for a quiet window with no other full check beside the trials.
  Repository change: measurements.md records the background workload as the night load and its sampled load.
  Architecture change: none.

In the context of the paired trial of criterion 11, facing a plan that asked
for a quiet window while the night lanes kept the machine busy, we decided
that the trial runs under the night load, to achieve a measurement of the
slots as they are used, accepting that the figures carry the noise of the
other lanes and are not a clean-room benchmark — 2026-11-14

## Q-4 · When the paired trial counts as a success

asked: 2026-11-14
answer: both paired runs finish within 1.6 times the time of a single run, and no test turns red or flaky because of the parallelism; below that the lane stops and reports. (Relayed in English by the orchestrator.)
answered_by: maintainer
status: answered
context: |
  Topic: the pass mark of the paired trial.
  Intention: a stop the maintainer can see before more time goes into the change.
  Today: the spec promised no threshold; the trials only reported evidence.
  Repository change: measurements.md reads the paired trial against this threshold.
  Architecture change: none.

In the context of the paired trial, facing a spec that set no threshold, we
decided that both runs must finish within 1.6 times a single run with no test
red or flaky because of the parallelism, to achieve a clear go or stop,
accepting that a red test whose cause is content, not parallelism, does not
count against the threshold — 2026-11-14

## Q-5 · When the new slot count takes effect

asked: 2026-11-14
answer: after the merge the configured slot count holds at once; jobs already running finish on the old lock. (Relayed in English by the orchestrator.)
answered_by: maintainer
status: answered
context: |
  Topic: the rollout of the slot count on the shared machine.
  Intention: no drain window and no interrupted lane at the merge.
  Today: older checkouts take the compatibility lock exclusively (spec, "Open decisions", second detail).
  Repository change: none beyond the documented rollout; running jobs are not touched.
  Architecture change: none.

In the context of the merge of this change, facing lanes that still run on
the single-slot lock, we decided that the configured slot count holds at once
and running jobs finish on the old lock, to achieve the gain without a drain
window, accepting that new admissions wait until the old exclusive holders
are gone — 2026-11-14

## Q-6 · How the slot count and the workers per run are set

asked: 2026-11-15
answer: the number of slots and the number of pytest workers per run are set centrally and easily, in layers — a validated default in the repository (workers = logical cores / slots, floored, at least 1, still bounded by memory at 2 GiB per worker across all slots); one machine-local file that may override both values; ONE reading function used by verify_lock, verify_all.sh and the runner; every run logs the values in force and where they came from. The keys move unchanged into the central configuration later (bead coding-harness-twvx). The repository default of this change is 4 slots, so 3 workers on 12 logical cores. (Relayed in English by the orchestrator.)
answered_by: maintainer
status: answered
context: |
  Topic: where the slot count and the pytest worker count live, and who reads them.
  Intention: change both without a code change, see in every run which values were used.
  Today: the slot count sits in a bare `verify.slots` file (default 2); the worker count follows a half-the-cores rule copied into `verify_all.sh` and `scripts/stage2.py`, and the runner's environment allow-list drops a caller's worker variable.
  Repository change: `read_settings` in `scripts/verify_lock.py` is the one reader; `verify.toml` in the shared state root replaces `verify.slots`; the shell runner and the runner ask the reader; the history records the values, their sources, the end load and the pytest peak memory.
  Architecture change: none; the central configuration stays its own change (bead coding-harness-twvx).

In the context of the slot count and the pytest workers per run, facing a
worker rule copied in two places and a slot file that knew nothing of the
workers, we decided on layered settings — a validated repository default,
one machine-local override file, one reading function for every caller, and
a log of the values and their sources in every run — to achieve one central,
easily changed place for both values, accepting that the bare `verify.slots`
file of the first implementation is replaced, not kept — 2026-11-15

## Q-7 · How the slot configuration is measured in real operation

asked: 2026-11-15
answer: three windows in this order — two days with 4 slots x 3 workers, then two days with 3 slots x 4 workers, then two days with 2 slots x 6 workers. The winner is the shorter mean time from queueing to result, on the conditions that no additional test turns red or flaky and free memory never falls below 25 %. A kit rule follows in its own bead if the result holds. (Relayed in English by the orchestrator; first stated with the first two windows, the third window added by the maintainer on the same day.)
answered_by: maintainer
status: answered
context: |
  Topic: which slot and worker combination the machine keeps.
  Intention: decide on real operation, not on one night's trial.
  Today: the trials of 2026-11-14 measured 2 x 6 and 4 x 3 once each, under the night load (measurements.md).
  Repository change: the repository default starts the first window (4 slots); each later window is set in the machine-local file; the verify history records the values per run.
  Architecture change: none; a kit rule would be its own bead.

In the context of choosing the slot and worker combination, facing one
night's trial that measured two of the candidates once each, we decided to
measure three windows of two days each in real operation (4 x 3, then 3 x 4,
then 2 x 6) and keep the one with the shorter mean time from queueing to
result, provided no additional test turns red or flaky and free memory never
falls below 25 percent, to achieve a choice that rests on daily use,
accepting six days before the setting is final and a kit rule only in its
own bead — 2026-11-15
