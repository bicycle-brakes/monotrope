---
title: "Measurements — verify-slots"
status: draft
implementation_status: partial
date: 2026-11-10
last_reviewed: 2026-11-15
updated: 2026-11-15
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: [{kind: llm-session, name: claude-code, version: "Sonnet 5.5, 2026-11-10"}, {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-15"}]
review: {status: pending, approved_by: null, approved_at: null}
tags: [measurements, verification]
---

# Measurements — verify-slots

The trial evidence for criterion 11 of `spec.md` (bead coding-harness-u1ha;
review round 4, row L4-1). All runs of 2026-11-14 ran on one Mac mini (Apple
M-series, 12 logical cores, 24 GiB), **under the night load**: the other
lanes of night run 2026-11-14-a kept working beside them, as the maintainer
decided (`decisions.md#Q-3`). The raw files are machine-local, under
`~/.local/state/coding-harness/night/2026-11-14-a/` (`worker-curve/`,
`paired-trial/`, `quad-trial/`: `summary.txt`, `load*.csv`, `verify-*.log`);
every figure below was read from them on 2026-11-15.

**What these figures are, and are not** (review round 5, row L5-2). The
serial figures are the worker curve on `main` at `1d4419d1`; the paired
(2 x 6) and quad (4 x 3) figures come from the branch at `8ad6b533`. All six
trial runs on the branch exited red for the content reason below, and no
trial ran at capacity one on the branch. No figure here is a comparison on
the same implementation: each ratio below sets a branch run beside a `main`
run of another revision, under a night load that differed between them.
Criterion 11 is therefore not met by this file yet; the trials on the
repaired head (last section) are owed.

**Measured** means read from those files. **Derived** means computed here
from measured figures; the derivation is shown. Execution seconds are the
runner's own `execution …s · admission wait …s` line (the admission wait is
not part of them); pytest seconds are pytest's own closing line.

## How this deviates from the protocol of 2026-11-10

The protocol drafted on 2026-11-10 asked for a quiet window, a temporary
state root and a serial trial at capacity one. What ran instead:

- **Night load, not a quiet window** (`decisions.md#Q-3`). Other lanes' full
  checks and runner calls ran beside the trials.
- **The serial comparison is the worker curve on `main`** (`1d4419d1`): one
  run at a time, seven worker counts, not two runs at capacity one on the
  branch. The single run with six workers is the baseline of the paired
  trial, the single run with three workers the baseline of the quad trial.
- **Shared admission.** The trial runs waited at the live machine lock for
  the other lanes' checks (737 s and 1,237 s, the holders named in the logs);
  whether a temporary state root was used is not read in the files.
- **Load sampling** came from the orchestrator's sampler every five seconds
  (`utc,load1,cpu_busy_pct,pytest_procs,pytest_rss_mib,mem_free_pct`). For the
  worker curve the `load-n*.csv` files hold only their header line: the load
  of the single runs is **not measured**.

## Single runs by worker count — `main` 1d4419d1, measured

| Workers (`PYTEST_XDIST_AUTO_NUM_WORKERS`) | Start (UTC) | Exit | Admission wait s | Execution s | pytest s | Tests |
|---|---|---|---|---|---|---|
| 1 | 20:27:34 | 0 | 0.0 | 2,599 | 2,441 | 5985 passed, 17 skipped |
| 2 | 20:03:04 | 0 | 0.0 | 1,469 | 1,302 | 5985 passed, 17 skipped |
| 3 | 19:44:36 | 0 | 2.1 | 1,106 | 934 | 5985 passed, 17 skipped |
| 4 | 19:29:00 | 0 | 1.8 | 934 | 777 | 5985 passed, 17 skipped |
| 5 | 19:15:55 | 0 | 5.9 | 779 | 615 | 5985 passed, 17 skipped |
| 6 | 19:03:26 | 0 | 0.3 | 748 | 575 | 5985 passed, 17 skipped |
| 12 | 18:46:30 | 0 | 422.0 | 594 | 433 | 5985 passed, 17 skipped |

The figures the orchestrator passed on (1,108, 937 and 785 s for three, four
and five workers) are the wall times including the short admission waits;
the table keeps the runner's execution seconds.

**Derived — the worker curve.** pytest seconds fit T(n) ≈ 251 s + 2,190 s / n
(through n = 1 and n = 12; it predicts 981 s for three workers against the
measured 934 s, and 616 s for six against 575 s). About 250 s of every run do
not shrink with more workers.

## Paired trial — two slots x six workers, branch 8ad6b533, measured

Batch start 2026-11-14T21:32:13Z, end 21:58:38Z; both runs admitted
together after 737–738 s of waiting behind another lane's `make verify`.

| Run | Exit | Admission wait s | Execution s | pytest s | Tests |
|---|---|---|---|---|---|
| 1 | 2 (red) | 737.6 | 847 | 793 | 2 failed, 6000 passed, 17 skipped |
| 2 | 2 (red) | 737.4 | 814 | 787 | 2 failed, 6000 passed, 17 skipped |

Load (sampler, 207 rows from 21:42:00Z; the protected window from the
admission at about 21:44:30Z to the end holds 168): one-minute load mean
16.7, maximum 25.7 in the protected window (14.6 over all rows); CPU busy
mean 37 %, maximum 59 %; summed pytest RSS peak 4,064 MiB (about 4.0 GiB);
free memory never below 62 %. Memory floor 25 %; the admission read 73 %
free.

## Quad trial — four slots x three workers, branch 8ad6b533, measured

Batch start 2026-11-14T21:59:21Z, end 22:45:20Z; all four admitted together
after 1,237 s of waiting behind other lanes' work (a runner review, then a
`make verify`).

| Run | Exit | Admission wait s | Execution s | pytest s | Tests |
|---|---|---|---|---|---|
| 1 | 2 (red) | 1,236.8 | 1,523 | 1,425 | 2 failed, 6000 passed, 17 skipped |
| 2 | 2 (red) | 1,236.5 | 1,523 | 1,446 | 2 failed, 6000 passed, 17 skipped |
| 3 | 2 (red) | 1,236.6 | 1,523 | 1,428 | 2 failed, 6000 passed, 17 skipped |
| 4 | 2 (red) | 1,236.6 | 1,477 | 1,417 | 2 failed, 6000 passed, 17 skipped |

Load (547 rows over the whole batch, 301 in the protected window from about
22:19:58Z): one-minute load mean 14.3, maximum 20.2 in the protected window
(10.7 over all rows); CPU busy mean 34 %, maximum 62 %; summed pytest RSS
peak 5,028 MiB (about 4.9 GiB); free memory never below 61 %.

## The red tests

The same two tests failed in all six trial runs and in no single run:
`tests/test_explore_provenance.py::test_active_census_is_enabled` and
`::test_active_model_research_has_no_false_human_provenance`. Both read the
header of this change's own `research.md`, which pull request 388 (merged
into the branch at `27aef082`) made untruthful by its new census rule — a
content failure, not one of parallelism. No other test failed, and no test
changed its result between runs, so no flakiness from the parallelism was
observed. The header is corrected through the runner's publication function
in `327e51d7`; with it both tests pass.

## Reading — derived

Against the maintainer's threshold (`decisions.md#Q-4`: both runs within
1.6 times a single run, no test red or flaky because of the parallelism) —
read across revisions, red branch runs beside green `main` runs, so an
orientation, not the comparison criterion 11 asks for:

- **Paired, 2 x 6 against the single six-worker run** (execution 748 s):
  814 s and 847 s, **1.09x and 1.13x**; by pytest seconds 787 and 793
  against 575, 1.37x and 1.38x. Below 1.6 on either measure, across
  revisions.
- **Quad, 4 x 3 against the single three-worker run** (execution 1,106 s):
  1,477–1,523 s, **1.34x–1.38x**; by pytest seconds 1,417–1,446 against
  934, **1.52x–1.55x**. Below 1.6 across revisions, but slower than the fit
  predicts: four three-worker runs use the 12 cores once, so the fit expects
  each about as fast as one three-worker run alone. The cause of this
  slowdown is **not read**; memory is not it by the sampled free memory
  (never below 61 %), the night load beside it and shared disk or the
  constant 250 s part are candidates nobody measured.

Throughput, derived from the slowest run of each batch (a batch finishes
when its last run does):

| Configuration | Runs per hour | Mean time to result for four queued runs |
|---|---|---|
| 1 x 6 (serial) | 3,600 / 748 = 4.8 | (748 + 1,496 + 2,244 + 2,992) / 4 ≈ 1,870 s |
| 1 x 12 (serial) | 3,600 / 594 = 6.1 | (594 + 1,188 + 1,782 + 2,376) / 4 ≈ 1,485 s |
| 2 x 6 | 2 x 3,600 / 847 = 8.5 | (847 + 847 + 1,694 + 1,694) / 4 ≈ 1,270 s |
| 4 x 3 | 4 x 3,600 / 1,523 = 9.5 | 1,523 s (all four at once) |

So 4 x 3 completes the most runs per hour, while 2 x 6 returns the first
results sooner and has the shorter mean time to result for four queued
runs. One night's single batch cannot separate them reliably: the
maintainer decided to measure in real operation (`decisions.md#Q-7`) —
two days each of 4 x 3, then 3 x 4, then 2 x 6, the winner the shorter mean
time from queueing to result, provided no additional test turns red or flaky
and free memory never falls below 25 %. The repository default of four slots
(three workers on this machine) starts the first window; the verify history
now records slots, workers, their sources, the end load and the pytest peak
memory of every full check the shell runner (`scripts/verify_all.sh`) runs,
which those windows read. The runner's targeted pytest logs its values and
their sources but writes no history record.

What is still missing for criterion 11 as the spec words it: no trial ran
at capacity one on the branch itself (the worker curve on `main` stands in
for it), and the six trial runs are red for the content reason above, so no
green paired run is recorded yet.

## Trials on the repaired head — owed, not yet run

Empty on purpose. The orchestrator runs these trials on the repaired head
and fills the rows; until then nothing in this section is measured. Each
trial records the tested commit, and a batch row per run.

| Trial | Commit | Run | Wall s | pytest s | Peak pytest RSS MiB | Load (1-min mean / max) | Free memory min % | Verdict |
|---|---|---|---|---|---|---|---|---|
| Serial, capacity one | | | | | | | | |
| Paired, 2 x 6 | | | | | | | | |
| Quad, 4 x 3 | | | | | | | | |
