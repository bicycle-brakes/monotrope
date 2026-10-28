---
title: "Plan — run-report"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-o2yc
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, run-report]
---

# Plan — run-report

```text
For you:     One local command shows recorded attempts, time against appetite, and live process and memory figures.
Done when:   Boundary and failure fixtures hold all twelve criteria, the report leaves its inputs unchanged, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Dashboards, automatic start guards, verification locks, runner changes or invented missing measurements.
Pre-mortem:  suppose it failed: most likely because unreadable time records silently become a reassuring zero.
Starts unless you say stop.
```

## Files and steps

1. Create `tests/test_run_report.py`: build temporary change folders and
   injected process/memory sources for the ledger cases; first demonstrate
   the missing report behavior, with no live models or resource-dependent assertions.
2. Create `scripts/run_report.py`: implement a read-only CLI with optional
   `--change NAME`, structured readers and a plain-text renderer as below.
3. Change `Makefile`: add `report` to `.PHONY` and help, passing optional
   `CHANGE` as quoted data through the environment, never as shell code.
4. Change `docs/WORKFLOW.md`: document `make report`, `make report CHANGE=name`,
   local CLI use, measured-subtotal limits and the two warning thresholds.
5. Update `plans/changes/run-report/plan.md` as tests land and measured phase-4
   time accrues; the runner maintains `plans/changes/run-report/findings.md`
   and regenerates `plans/INDEX.md` as derived metadata.

No existing file is deleted. Keep `spec.md` as the yardstick and
`decisions.md` unchanged. No design or ADR is due for class `bounded`.

## Implementation contract

- Default root is the script's repository root, not the caller's current
  directory. Enumerate immediate real directories under `plans/changes`,
  excluding `archive`; sort names and do not follow links outside the root.
  Validate `--change` as a single active-folder name. Unknown or invalid
  selections print a bounded diagnostic and the live block, with exit zero;
  normal argparse help/usage behavior need not masquerade as a report.
- Import `stage2.time_log`, `stage2.card_problem`, `stage2.CARD_LABELS`
  and `stage2_runs.CALL_LINE`/`CALL_PREFIXES`. Imports and readers must have
  no dispatch side effects. Do not duplicate their section or audit-line
  recognition expressions, modify the imported modules or call their CLIs.
- Extract the appetite from the opening card only. Accept positive decimal
  hours (`2 hours`, `2 h`) and hours plus minutes (`2 h 30 min`), allowing
  trailing explanatory text; reject competing budget values or missing units.
  Convert to seconds before comparing, with the inclusive 50 percent boundary.
- Parse canonical runner durations using their explicit seconds as authority,
  not wall-clock endpoint subtraction; tests build these with `time_entry`.
  Also accept dated orchestrator records with an explicit measured seconds
  field or an exact closed UTC range (same-day clock endpoints or ISO UTC
  endpoints with dates). Reject approximate, unmeasured, negative, ambiguous
  or malformed records instead of extracting arbitrary prose numbers.
  Prefer an explicit duration over endpoints within the same record.
- Count each nonblank unrecognised content line in the time section as
  `unread lines: N`, excluding Markdown heading/fence furniture. Keep readable
  sums visibly incomplete when any content is unread; a missing section or
  unreadable plan is `time not read`, not zero. An empty readable section is
  zero recorded seconds, never proof that no work occurred. Do not add audit
  calls or live elapsed times. Emit a UTC snapshot timestamp for the report.
- Render measured attempt rows in source order with verb, attempt, route,
  model and accepted/rejected. Read audit records from `findings.md`
  separately as calls with only their explicitly recorded metadata, using
  `not read` for absent fields and `verdict not recorded` when absent.
  Label these as evidence of calls, not extra measured attempts. Do not join
  on attempt number alone or treat leak-check success as completion.
- Read `ps -axo pid,etime,command` once with a finite timeout and no shell.
  Token-match actual `scripts/stage2.py` invocations (including options
  between verb and change), `make verify` and `scripts/verify_all.sh`;
  discard shell wrappers and unrelated commands containing those strings.
  Print only validated pid, elapsed time, known verb/verification label and
  change token. A verification change not carried in the command is `not read`.
- macOS: read `memory_pressure`'s free percentage and `vm_stat`'s page size
  and pages occupied by the compressor, not pages stored. Use a bounded
  `sysctl -n hw.memsize` read for the physical-byte denominator of compressor
  share. Linux: read `/proc/meminfo`, using MemAvailable/MemTotal and the
  optional resident `Zswap` field/MemTotal for compressed share, labelled as
  zswap; do not substitute SwapFree or uncompressed Zswapped bytes. Missing
  fields stay `not read`. Validate ranges, units and positive denominators.
- Use independent source reads, at most two seconds per system command;
  catch missing commands, timeout, nonzero exit, decode errors and malformed
  values. A source failure cannot erase other sources; never echo raw input,
  exception text containing it, process arguments or subprocess stderr.
- Warn at recorded time >= half the appetite, including a partial sum already
  above it; with partial time below it state the comparison is incomplete.
  Warn before starting a verify-bearing step when available memory <25 percent.
  These are advice on the snapshot; do not install hooks or claim a later
  step was inspected. The 25 percent constant is local until separate
  verification-resource work lands (bead `coding-harness-p6mu`).
- Run no network, tracker, model, Git mutation or state-writing command.
  Prevent bytecode writes by setting `sys.dont_write_bytecode` before local
  imports. Test file bytes and directory entries before/after execution;
  inject failures and sentinel prompt/answer/command text to test output
  allow-listing. Keep report execution outside `make verify`'s gate list;
  its unit tests run in the normal suite.

## Criterion ledger

- 1: not yet written tests/test_run_report.py::test_default_lists_active_changes_then_live — an archive appears or a plan-less active folder disappears
- 2: not yet written tests/test_run_report.py::test_selection_is_confined_and_never_falls_back — traversal, shell syntax or a missing name selects other inputs
- 3: not yet written tests/test_run_report.py::test_attempts_and_unfinished_calls_keep_recorded_metadata — repeated attempt numbers overwrite history or clean calls acquire an accepted verdict
- 4: not yet written tests/test_run_report.py::test_measured_durations_sum_without_audit_or_live_double_counting — accepted, rejected or exact orchestrator seconds are omitted or counted twice
- 5: not yet written tests/test_run_report.py::test_unread_time_is_visible_and_totals_are_partial — malformed or approximate records supply a guessed duration or a false complete total
- 6: not yet written tests/test_run_report.py::test_card_appetite_warns_at_half_including_rejected_time — the boundary, unit conversion or card authority is wrong
- 7: not yet written tests/test_run_report.py::test_unread_appetite_never_becomes_zero — absent, conflicting or non-positive card values yield a ratio
- 8: not yet written tests/test_run_report.py::test_process_filter_emits_only_permitted_fields — options hide a runner, substring matches add unrelated processes or extra arguments leak
- 9: not yet written tests/test_run_report.py::test_memory_sources_preserve_units_and_unknowns — page size, resident compressor usage, zswap units or physical denominator is wrong
- 10: not yet written tests/test_run_report.py::test_low_memory_warning_is_advisory_and_strictly_below_floor — 24 percent fails to warn, 25 warns or a verification command launches
- 11: not yet written tests/test_run_report.py::test_source_failures_are_independent_bounded_and_exit_zero — timeout or unreadable input crashes, hangs or suppresses valid output
- 12: not yet written tests/test_run_report.py::test_report_is_read_only_local_and_does_not_echo_prose — sentinels leak, filesystem entries change or forbidden commands run
- 12: not yet written tests/test_run_report.py::test_make_report_passes_change_as_data_and_is_not_a_gate — make interpolation executes selection text or reporting enters verification

## Verification

```sh
.venv/bin/python -m pytest tests/test_run_report.py -q
python3 scripts/check_interview_minimums.py --change run-report
python3 scripts/check_criterion_ledger.py
make verify
```

Use injected command output and temporary files for both operating systems;
no real process listing, memory pressure or sleeps are needed for tests.
The runner owns full verification, index generation and the commit.
`scripts/validate_change_artefacts.py` is absent at input `6daf7b17`;
do not claim it passed or introduce it here.

## Explore route

Research records Stage-2 explore on route `flash`, endpoint
`glm-coding-plan`, model `glm-5.3-flash`, on 2026-10-28. No Stage-1 fallback
is recorded. The stopped low-memory attempt is evidence, not a fallback.

## Time used
