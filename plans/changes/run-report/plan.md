---
title: "Plan — run-report"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-29
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
Appetite:    3 hours 45 minutes of phase 4, repairs included; a stop, not an estimate.
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
- Import `stage2.time_log`, `stage2.CARD_LABELS`
  and `stage2_runs.CALL_LINE`/`CALL_PREFIXES`. Imports and readers must have
  no dispatch side effects. Do not duplicate their section or audit-line
  recognition expressions, modify the imported modules or call their CLIs.
- Extract the appetite from the opening card only. Accept positive decimal
  hours (`2 hours`, `2 h`) and hours plus minutes (`2 h 30 min`), allowing
  trailing explanatory text; reject competing budget values or missing units.
  Convert to seconds before comparing, with the inclusive 50 percent boundary.
- Parse canonical runner durations using their explicit seconds as authority,
  not wall-clock endpoint subtraction; tests build these with `time_entry`.
  Only the runner's own fixed format counts (maintainer, 2026-10-29, a
  structural cut after five loop rows on orchestrator prose records):
  every other line, dated orchestrator records included, is unread and
  never yields a number.
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

- 1: tests/test_run_report.py::test_default_lists_active_changes_then_live — an archive appears or a plan-less active folder disappears
- 2: tests/test_run_report.py::test_selection_is_confined_and_never_falls_back — traversal, shell syntax or a missing name selects other inputs
- 3: tests/test_run_report.py::test_attempts_and_unfinished_calls_keep_recorded_metadata — repeated attempt numbers overwrite history or clean calls acquire an accepted verdict
- 4: tests/test_run_report.py::test_measured_durations_sum_without_audit_or_live_double_counting — accepted or rejected runner seconds are omitted or counted twice, or an orchestrator record is counted
- 5: tests/test_run_report.py::test_unread_time_is_visible_and_totals_are_partial — malformed or approximate records supply a guessed duration or a false complete total
- 6: tests/test_run_report.py::test_card_appetite_warns_at_half_including_rejected_time — the boundary, unit conversion or card authority is wrong
- 7: tests/test_run_report.py::test_unread_appetite_never_becomes_zero — absent, conflicting or non-positive card values yield a ratio
- 8: tests/test_run_report.py::test_process_filter_emits_only_permitted_fields — options hide a runner, substring matches add unrelated processes or extra arguments leak
- 9: tests/test_run_report.py::test_memory_sources_preserve_units_and_unknowns — page size, resident compressor usage, zswap units or physical denominator is wrong
- 10: tests/test_run_report.py::test_low_memory_warning_is_advisory_and_strictly_below_floor — 24 percent fails to warn, 25 warns or a verification command launches
- 11: tests/test_run_report.py::test_source_failures_are_independent_bounded_and_exit_zero — timeout or unreadable input crashes, hangs or suppresses valid output
- 12: tests/test_run_report.py::test_report_is_read_only_local_and_does_not_echo_prose — sentinels leak, filesystem entries change or forbidden commands run
- 12: tests/test_run_report.py::test_make_report_passes_change_as_data_and_is_not_a_gate — make interpolation executes selection text or reporting enters verification

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

## Runner route — 2026-10-29

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-10-28 22:41:23–23:33:17 UTC, 3114 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-28 23:33:23–23:49:18 UTC, 955 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
2026-10-29 00:23:13–00:36:13 UTC, 780 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-29 00:36:20–00:48:46 UTC, 746 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-29 00:48:52–01:00:59 UTC, 727 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-29 01:01:00–01:02:44 UTC, 104 s — review loop round 1 · the orchestrator's red-first check of the eight retained repairs (L1-6 rejected) · measured with `date -u`
2026-10-29 01:44:14–01:44:32 UTC, 18 s — review loop round 2 · row L2-1 repaired by the orchestrator · measured with `date -u`
2026-10-29 07:28:59–07:42:12 UTC, 793 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-29 08:22:18–08:35:31 UTC, 793 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-29 13:10:44–13:23:53 UTC, 790 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-29 14:22:01–14:36:00 UTC, 840 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner

## Appetite stop — 2026-10-29

At 01:51 UTC, after review round 3 took three rows (L3-1, L3-2, L3-3, each a
code repair with a red-first test). The measured spans under Time used sum to
6444 s, 1.79 h of the 2-hour appetite. The first repair run's two failed Codex
calls left no measured entry, so the real use is higher. Three repairs and a
full `make verify` do not fit in the rest.

Answer (orchestrator, night rule of 2026-10-28/29, which allows cut, park or
drop but never continue): **park**. Proposed for the maintainer: a new
appetite of 45 minutes for the three taken rows. Then the loop runs to its
end, followed by phase 6. The report already works for its main purpose:
attempts, time against appetite and the half-way warning, measured on this
change on 2026-10-28.

## Resumed — 2026-10-29

The maintainer granted a new appetite of 45 minutes for the three taken rows
(2026-10-29). The repair took them in one Codex attempt (`f3a49d2e`, 793 s,
red-first tests for each row, `make verify` green inside the runner).

Review round 4, 07:42:39–07:42:49 UTC: refused by OpenCode Go with
`GoUsageLimitError` (HTTP 429, "Go usage limit exceeded") on the round's
first member, `hy3`; no round was written and no stage was consumed. Not
retried. The loop therefore did not reach a clean round on this stand; the
change goes to phase 6 with that gap named, and the next round runs when the
Go limit has reset.

Appetite raised on the card (loop row L6-3, 2026-10-29): the maintainer
granted 45 minutes (morning), 30 minutes (about 10:40 UTC) and 30 minutes
(about 13:50 UTC, for the strict time-record grammar of L5-1) on top of the
original 2 hours; the card now states the total, 3 hours 45 minutes.
