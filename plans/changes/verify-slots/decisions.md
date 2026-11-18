---
title: "Decisions — verify-slots"
category: decisions
status: draft
implementation_status: none
date: 2026-11-09
created: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-18
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

## Q-10 · Whether the 1.6x threshold gates the three-slot default (spec review row S2-1)

context: |
  Topic: criterion 11 cites decision Q-4 (every parallel run within 1.6 times a single run), while the 3 x 4 trial at e693604e measured 2.12 to 2.13 times.
  Intention: the phase-2a re-review of 2026-11-16 (row S2-1, BLOCKER, still open from row S-2) found two readings: Reading A, the ratio is a gate and the change cannot close at the shipped default; Reading B, the figures are recorded only.
  Today: the spec cites Q-4 in criterion 11's basis but its refutation has no ratio, and the non-goals exclude a new performance threshold.
  Repository change: the spec records the trial figures as evidence and states that Q-4's 1.6x applies to two slots only; a follow-up bead tunes the default slot count against the measured ratio.
  Architecture change: none.
  Recommendation: B, plus a follow-up bead; consequence: the change can close, parallel runs may stay slower than 1.6x until the follow-up.
asked: 2026-11-16, night run 2026-11-16-a, parked question
answer: "B" — record the figures, no gate on 3 x 4; the default slot count is tuned in a follow-up bead. Reasoning, verbatim: "Die Schwelle war für 2 Slots, nicht für 3 oder 4, das ergibt sich aus der Arithmetik." Decision Q-4 (1.6x) stands, scoped to two slots; the spec states that scope explicitly. (Maintainer, 2026-11-17, day session; recorded from the bead notes of coding-harness-u1ha.)
answered_by: maintainer
status: answered

In the context of criterion 11 and the 1.6x threshold of Q-4, facing a three-slot trial at 2.12 to 2.13 times a single run, we decided that the trial figures are recorded as evidence and do not gate completion, and that Q-4's 1.6x applies to two slots only, to achieve a change that can close at the shipped default, accepting that parallel runs may stay slower than 1.6x until a follow-up bead tunes the default slot count — 2026-11-17

## Q-11 · Which trial run closes criterion 11 (spec review row S2-2)

context: |
  Topic: whether the e693604e trial closes criterion 11 or the serial and three-at-once runs must be repeated on the merged head.
  Intention: row S2-2 (MAJOR, [AMBIGUITY]) asks it; Q-9 already answered which trial evidences completion.
  Today: Q-9 cites the 3 x 4 trial at e693604e; at that commit DEFAULT_SLOTS was 4, so the trial set three slots through the machine-local file.
  Repository change: the spec cites the e693604e trial as the completion evidence and says the configuration counts, not the layer that set it.
  Architecture change: none.
asked: 2026-11-17, settled by the orchestrating agent from Q-9 (night run 2026-11-17-a)
answer: "Reading A — the 3 x 4 trial at e693604e closes criterion 11, as Q-9 states; three slots of four workers set through the machine file is the configuration that ships, so it counts as operation at the default; no repeat on the merged head"
answered_by: agent
status: answered

In the context of criterion 11's completion evidence, facing a trial run at an earlier commit with the slot count set through the machine file, we decided that the e693604e 3 x 4 trial closes the criterion as Q-9 states, to achieve no second night-load trial against a spent appetite, accepting that the trial predates the Q-8 single-function worker derivation, which changes how the worker count is computed, not the four workers it computes on that machine — 2026-11-17

## Q-12 · Whose core reading counts (spec review rows S2-3, S2-4, S2-10)

context: |
  Topic: the over-cores warning and the worker formula name "the shell's reading, else Python's" and "logical cores", while Q-8 makes one Python function the only reader.
  Intention: rows S2-3 (MAJOR, [AMBIGUITY]), S2-4 (MAJOR, cannot go red) and S2-10 (MINOR, [AMBIGUITY]) follow from one gap, and phase-6 row F6-1 is the same mechanism.
  Today: verify_all.sh reads sysctl or nproc and passes the values to `verify_lock --settings`; the runner reads os.cpu_count; the warning text says "each run gets one worker" whatever the workers are.
  Repository change: only `read_settings` reads the machine; verify_all.sh passes no core or memory reading; the warning names the workers in force.
  Architecture change: none; this is Q-8 applied.
asked: 2026-11-17, settled by the orchestrating agent as [DETAIL] (night run 2026-11-17-a)
answer: "The Python reader alone reads the machine for every entry point (Reading B of S2-3): the cores are the CPUs this process may use — os.sched_getaffinity where the platform has it, else os.cpu_count; a cgroup CPU quota is not read. Refuting case: a Linux process whose affinity allows 6 of 24 CPUs, at three slots, gets 2 workers on the shell path and on the runner path alike. The oversubscription warning compares against that same reading and states the workers in force instead of the fixed 'each run gets one worker'."
answered_by: agent
status: answered

In the context of the core reading behind the worker count and the oversubscription warning, facing a shell reading and a Python reading that disagree under a CPU restriction, we decided that the one Python reader takes the process's CPU affinity for every entry point and that the warning names the workers in force, to achieve the single derivation Q-8 asked for and a criterion with a stated expected value, accepting that a cgroup CPU quota without an affinity mask is not seen — 2026-11-17

## Q-13 · What an unusable settings file does outside an admission (spec review rows S2-5, S2-8)

context: |
  Topic: an invalid `workers_per_run`, a malformed verify.toml, a leftover verify.slots, or a present file that sets no key, met by the runner's targeted pytest or a nested verify_all.sh.
  Intention: rows S2-5 (MAJOR, missing) and S2-8 (MINOR, [AMBIGUITY]) ask whether these paths refuse, fall back, or reuse an ancestor's values, and whether an empty file is valid.
  Today: the reader refuses any present content that is not one non-empty `[verify]` table with valid keys; the targeted pytest fails its launch with that diagnostic; the shell exits 2.
  Repository change: the spec states that every entry point refuses with the same diagnostic, for either key, and that only absence of the file means the repository default.
  Architecture change: none.
asked: 2026-11-17, settled by the orchestrating agent as [DETAIL] (night run 2026-11-17-a)
answer: "Every entry point — admission, nested verify_all.sh, the runner's targeted and cheap pytest — refuses with the reader's diagnostic naming the file, for an unusable `slots` or `workers_per_run` alike; no fallback, no reuse of an ancestor's values. A present file that sets no key (zero bytes, comments only, a bare `[verify]`) refuses too; only an absent file means the repository default."
answered_by: agent
status: answered

In the context of an unusable machine settings file, facing entry points outside an admission that could fall back silently, we decided that every entry point refuses with the one reader's diagnostic and that a present file must set at least one key, to achieve the one declared, validated value of Q-2 with no silent change of meaning, accepting that a broken file stops runner repairs on the machine until it is fixed or removed — 2026-11-17

## Q-14 · Free memory in the verify history (spec review row S2-6)

context: |
  Topic: Q-7 keeps a real-operation window only if free memory never falls below 25 percent, but the history records only end load and peak pytest memory.
  Intention: row S2-6 (MAJOR, missing) shows the windows cannot apply their own condition from the records.
  Today: the run's five-second sampler records the peak summed pytest resident memory; `read_available_memory` already reads the system-wide free percentage for the admission's memory check.
  Repository change: the same sampler also keeps the lowest free-memory percentage of the run, recorded in the end record; unknown when never readable.
  Architecture change: none.
asked: 2026-11-17, settled by the orchestrating agent as [DETAIL] (night run 2026-11-17-a)
answer: "The five-second sampler also records the run's minimum available-memory percentage through `read_available_memory`, in the end record beside the peak, unknown when no sample could be read. The non-goal 'continuous memory monitoring' means no monitoring that gates or acts during the run; a recorded minimum acts on nothing."
answered_by: agent
status: answered

In the context of the free-memory condition of Q-7, facing records that hold no free-memory figure, we decided that the existing sampler also records the run's minimum free-memory percentage, to achieve windows that can apply their own condition from the history, accepting one more field per end record and one more reading per sample — 2026-11-17

## Q-15 · Which runner pytest launches take the shared workers (spec review row S2-7)

context: |
  Topic: the runner starts pytest twice outside the admission: the targeted check after a repair, and an attempt's cheap tests with xdist `-n auto`.
  Intention: row S2-7 (MAJOR, [AMBIGUITY]) asks whether only the targeted check asks `read_settings`.
  Today: only the targeted check asks the reader; the cheap tests run with xdist auto, every logical core, beside up to three admitted runs.
  Repository change: the cheap tests take their workers from `read_settings` and log the `[verify-settings]` line, as the targeted check does.
  Architecture change: none.
asked: 2026-11-17, settled by the orchestrating agent from Q-6 and Q-8 (night run 2026-11-17-a)
answer: "Reading B — every xdist launch of the runner takes its workers from `read_settings` and logs `[verify-settings]`; Q-6 names the runner as a user of the one reading function and Q-8 says one function computes the workers for every caller (house rule 9, one choke point)."
answered_by: agent
status: answered

In the context of the runner's pytest launches outside the admission, facing cheap tests that size themselves to every core beside the admitted runs, we decided that every runner xdist launch takes its workers from the one reader, to achieve one worker rule on the machine as Q-6 and Q-8 ask, accepting that an attempt's cheap tests run with fewer workers than before — 2026-11-17

## Q-16 · The remaining reading details (spec review rows S2-9, S2-11 to S2-16)

context: |
  Topic: seven minor holes of the re-review: the memory bound, a raised capacity, legacy-holder logs, ADR 0025's sentence, the load average, partial samples, and when the reader runs.
  Intention: rows S2-9, S2-11, S2-12, S2-13, S2-14, S2-15 and S2-16 (MINOR) each leave a reading open; each is revisable and the implementation already takes one side.
  Today: the code takes physical memory, re-reads capacity every 0.25-second poll, names the compatibility lock's published holder, records all three load averages, keeps the maximum of readable samples, and reads settings after the reservation in verify_all.sh.
  Repository change: the spec states these readings; no protected file changes.
  Architecture change: none.
asked: 2026-11-17, settled by the orchestrating agent as [DETAIL] (night run 2026-11-17-a)
answer: "S2-9: the memory bound is total physical memory (2 GiB per worker across all slots); a cgroup limit is not read; 'at least one' wins over a bound of zero. S2-11: a raised capacity is taken by the first waiter at its next queue poll (0.25 s). S2-12: while an older checkout holds verify.lock exclusively, the waiting logs name the compatibility lock's published holder, or say none is published. S2-13: an ADR's context is dated rationale, not current policy; criterion 11's current-policy documents are the three the Definition of Done names, and ADR 0025 stays untouched (protected). S2-14: the end record holds the 1-, 5- and 15-minute load averages. S2-15: the peak is the maximum of the readable samples, unknown only when none was read (a run that ends before its first sample included). S2-16: an admitted run reads its settings after its reservation; the runner's targeted and cheap pytest read them at launch."
answered_by: agent
status: answered

In the context of seven minor readings the spec leaves open, facing an implementation that already takes one side of each, we decided to state those sides in the spec, to achieve criteria that can go red without a new mechanism, accepting that a missed sample can understate the peak and that ADR 0025 keeps its dated sentence until a decision pull request amends it — 2026-11-17

## Q-17 · Nesting across versions during the rollout (spec review row S3-1)

context: |
  Topic: a protected check nested inside an admission of the other version — the updated one or an older single-slot checkout.
  Intention: row S3-1 (MAJOR, missing) shows the spec does not say which markers count as validated across versions, and that an older verify_all.sh under an updated admission would wait forever for the compatibility lock its own ancestor holds shared.
  Today: the updated reader already honours an older checkout's marker (no slot marker, the compatibility lock held exclusively, verify.holder.json naming the marker's process and token) and nests under it; the older code cannot be changed by this change; the runner and the `make verify` it starts always come from the same checkout, the worktree it runs in.
  Repository change: the spec states both directions: an updated check nests under a valid older marker; an older check under an updated admission is a rollout limit, not built for.
  Architecture change: none.
asked: 2026-11-18, settled by the orchestrating agent as [DETAIL] (night run 2026-11-17-a)
answer: "An updated check validates an older checkout's marker by the legacy shape it already reads and nests under it, consuming no slot. An older check started under an updated admission cannot validate the slot marker and waits for the compatibility lock its ancestor holds shared; this is a stated rollout limit, not built for: it needs a process of the updated version to start an older checkout's verification, which the documented path never does (the runner starts `make verify` in its own checkout), and it ends when the older branch merges origin/main. No holder record is published for the older version, so criterion 9's one-record-per-holder rule stands."
answered_by: agent
status: answered

In the context of nesting across versions during the rollout of Q-5, facing an older check that cannot read the updated marker, we decided that the updated check nests under a valid older marker and that the opposite direction is a stated rollout limit, to achieve no second holder record and no change to old code, accepting that an older checkout's verification started by hand inside an updated admission waits until that admission ends — 2026-11-18

## Q-18 · Three minor holes of the second re-review (spec review rows S3-2, S3-3, S3-4)

context: |
  Topic: a refutation case for a raised slot count, the worker count when a machine reading fails, and what "substituted" and "cannot be safely read" mean for verify.toml.
  Intention: rows S3-2 (MINOR, cannot go red), S3-3 (MINOR, missing) and S3-4 (MINOR, [AMBIGUITY]) each leave one reading open; each is revisable and the code already takes one side.
  Today: `derived_workers` drops a bound whose reading fails and leaves xdist's own auto when neither reading exists, naming "no machine reading" as the source; `_read_settings_file` opens without following symlinks, refuses a non-regular file and refuses content beyond 65,536 bytes.
  Repository change: the spec states these readings and adds a refuting case above the default.
  Architecture change: none.
asked: 2026-11-18, settled by the orchestrating agent as [DETAIL] (night run 2026-11-17-a)
answer: "S3-2: criterion 2 adds the refuting case `slots = 4` with four or more independent checks contending, where the fourth does not start. S3-3: a failed reading drops only its own bound; with neither reading, xdist's own auto applies, as the earlier worker-cap rule did (bead coding-harness-l7sc), and the `[verify-settings]` line names 'no machine reading' as the workers' source. S3-4: Reading B — a symlinked or non-regular verify.toml refuses, and so does content beyond 65,536 bytes; nothing is parsed from a prefix."
answered_by: agent
status: answered

In the context of three minor readings the second re-review left open, facing code that already takes one side of each, we decided to state those sides and add the missing refuting case, to achieve criteria that can go red, accepting that a machine with no core or memory reading runs xdist's own auto beside the admitted runs — 2026-11-18
