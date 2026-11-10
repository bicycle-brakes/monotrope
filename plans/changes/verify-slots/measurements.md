# Measurements — verify-slots

The serial-versus-paired evidence for criterion 11 of `spec.md` (bead
coding-harness-u1ha). The trials run at one tested implementation commit,
after `make verify` is green on it, coordinated by the orchestrator in a
quiet window: no other full check runs beside them, no edit lands between
the runs, and the enclosing runner's own verification stays on normal
admission. Nothing below is a result until its numbers stand in it; a trial
without its recorded fields leaves the change's completion pending.

## Protocol

Both trials use a temporary shared state root through `XDG_STATE_HOME`, so
the trial children take their own admissions there; the inherited admission
markers (`HARNESS_VERIFY_LOCK_HELD`, `HARNESS_VERIFY_LOCK_TOKEN`,
`HARNESS_VERIFY_LOCK_SLOT`, `HARNESS_VERIFY_ADMISSION_ID`,
`HARNESS_VERIFY_ADMISSION_WAIT`) are cleared from the trial environment.
The live machine setting is never edited: the capacity is set only inside
the temporary root's `coding-harness/verify.slots`, by atomic replacement.

- Trial one (serial): capacity `1`; `make verify` twice, the second run
  starting after the first has exited.
- Trial two (paired): capacity `2`; `make verify` twice, both runs started
  together and joined together.

Each run's own records stay the ones the implementation writes
(`verify-duration.jsonl` in that state root); the trials reuse those
durations and never copy an ownership token into this file. Load is sampled
with `os.getloadavg()` every five seconds across each batch; the one-minute
series, its mean and its maximum are recorded, and a load that cannot be
read is recorded as explicitly not measured — the evidence stays
incomplete in that case.

Recorded per trial: date, commit, dirty state, Python version, worker
configuration (the `PYTEST_XDIST_AUTO_NUM_WORKERS` actually applied), memory
floor, hardware, background workload, each run's exit code, queue wait,
execution time and wall time, the batch elapsed time, and the load series.

## Trial one — serial, capacity one

Pending.

## Trial two — paired, capacity two

Pending.

## Reading

Pending both trials. Both outcomes are kept, including a slower paired
result; a failed run leaves the completion pending until rerun green.
