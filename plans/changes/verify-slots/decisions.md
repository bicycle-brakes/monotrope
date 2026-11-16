---
title: "Decisions — verify-slots"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-16
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
superseded_by: Q-6 — the count of two is replaced by four slots (2026-11-15)
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

Superseded in its count by Q-6 (recorded 2026-11-15, review round 5, row
L5-4): the shipped default is four slots, not two. The answer above stays
as the maintainer gave it. The statement behind Q-6, verbatim, made by the
maintainer in the conversation on 2026-11-14: "stelle auf 4 slots mit 3 workern um, messe das, und mache daraus wenn gut irgendwann eine kit regel, messen auch die ram auslastung".

## Q-2 · Where the number lives

asked: 2026-11-09
answer: "Das muss auch zentral leicht änderbar sein in Zukunft" — the slot count is a value that is easy to change in one central place (default 2), later inside the central harness configuration (bead coding-harness-twvx); no constant repeats it.
answered_by: maintainer
status: answered
superseded_by: Q-6 — the default 2 and the bare slot file are replaced by four slots in layered settings (2026-11-15)
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

Superseded in its default by Q-6 (recorded 2026-11-15, review round 5, row
L5-4): the default is four slots, and the one central place is the layered
settings of Q-6; that the count is easy to change centrally still holds. The
answer above stays as the maintainer gave it; the statement behind Q-6 is
quoted under Q-1.

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
supersedes: Q-1 (the count of two) and Q-2 (the default 2); the maintainer's statement of 2026-11-14 is quoted under Q-1
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

## Q-7 addendum · The default after the trials at the repaired head

asked: 2026-11-16
answer: "3 mal 4" — the repository default is 3 slots x 4 workers. (Maintainer, 2026-11-16, in the conversation; relayed verbatim by the orchestrator.)
answered_by: maintainer
status: answered
context: |
  Topic: which slot and worker combination the repository default sets at the merge.
  Intention: the trials at e693604e (measurements.md, "Trials on the repaired head") measured all three candidates on the same commit.
  Today: 2 x 6 met Q-4 (1.53 x, 1.55 x the serial run); 3 x 4 missed it (2.12 x to 2.13 x); 4 x 3 missed it (about 3.2 x). Derived mean time to result for four queued runs: 2 x 6 about 1,950 s, 3 x 4 at least about 2,011 s, one slot about 2,104 s, 4 x 3 about 2,652 s. The orchestrator recommended 2 x 6.
  Repository change: DEFAULT_SLOTS goes from 4 to 3 (the worker count derives to 4 on a 12-core machine); the slot count stays configurable in the machine-local file.
  Architecture change: none.

The maintainer chose 3 x 4 knowing that it misses Q-4 in the trial; the
real-operation measurement of Q-7 continues from this default.

## Q-8 · One function computes slots and workers for every caller

asked: 2026-11-16
answer: "jaja" (to: one function computes slots x workers; verify_all.sh reads its answer instead of computing nproc itself) — the worker count is derived in exactly one place. (Maintainer, 2026-11-16, in the conversation; relayed verbatim by the orchestrator.)
answered_by: maintainer
status: answered
context: |
  Topic: where the pytest worker count per run is derived.
  Intention: the phase-6 re-check of 2026-11-16 (codex 01a1e52e) found F6-1 (under a CPU restriction the shell reads the allowed CPUs with nproc, the Python runners read all cores, and the two select different worker counts); the round before found F6-2 (the worker value reported differs from the one that runs); both are the same mechanism, the worker count derived in more than one place, so case repair ends.
  Today: verify_all.sh computes the worker count from nproc itself, while scripts/verify_lock.py and scripts/stage2.py compute it from all cores.
  Repository change: one function computes slots x workers; verify_all.sh reads its answer instead of computing nproc itself; the runner and verify_lock use the same function.
  Architecture change: none; the one reading function of Q-6 becomes the one computing function as well.
  Question: one choke point computes slots x workers and the shell reads its answer, or keep repairing case by case?
  Recommendation: one choke point; consequence: verify_all.sh depends on the Python function for its worker count.

In the context of the pytest worker count, facing two findings in two
phase-6 re-checks from one mechanism, a worker count derived separately in
the shell and in the Python runners, we decided that one function computes
slots and workers and that verify_all.sh reads its answer instead of
computing nproc itself, to achieve one worker count for every entry point,
accepting that the shell runner depends on the Python function for its
worker count — 2026-11-16

## Q-9 · Which trial evidences completion

context: |
  Topic: the completion trial named in spec.md.
  Intention: the spec still asked for a two-slot paired trial, written before
  the maintainer chose three slots of four workers as the default (Q-7).
  Today: trials of 2x6, 3x4 and 4x3 are recorded at commit e693604e
  (3x4: three simultaneous full runs at 2.12x one run's duration).
  Repository change: the completion criterion in spec.md and plan.md.
  Architecture change: none.
asked: 2026-11-16, conversation
answer: "3 gleichzeitig, 3×4 (Empfohlen)"
answered_by: maintainer
status: answered

In the context of the completion evidence for simultaneous verify runs, facing a criterion written before the three-slot default, we decided that three simultaneous full runs under the shipped default of three slots and four workers evidence completion, citing the 3x4 trial recorded at commit e693604e, to achieve that the trial measures exactly the configuration that ships, accepting that no two-run paired trial is required.
— 2026-11-16
