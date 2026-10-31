---
title: "Plan — time-records-data"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-v6vk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, time-accounting]
---

# Plan — time-records-data

```text
For you:     Runner and orchestrator time reaches the report through one fixed-format writer.
Done when:   Both callers produce counted records, old prose stays visibly unread, runner recovery tests pass, and make verify is green.
Appetite:    3 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Historical migration, a separate time store, prose parsing or appetite-policy changes.
Pre-mortem:  suppose it failed: most likely because consolidation bypasses the runner's safe recovery path.
Starts unless you say stop.
```

## Files and steps

1. Create `scripts/time_records.py`: own the record type, fixed formatter,
   parser, section extraction and insertion, and common write operation;
   preserve runner bytes and explicit seconds, including midnight formatting.
   A write accepts trusted prior section text and a persistence callback so
   runner recovery can keep its existing safe restore without duplicating
   record construction or insertion. Keep this module independent of stage2.
2. Change `scripts/harness.py`: add `time-log` and dispatch it before the ADR
   branch, without reading provenance, asking questions, writing an answer
   commit message or requiring git. Accept a positional active-change name,
   `--start` and `--end` UTC timestamps (`YYYY-MM-DDTHH:MM:SSZ`), `--seconds`
   nonnegative integer, `--verb`, `--attempt` positive integer, `--route`,
   `--model`, `--result accepted|rejected`, and existing-style `--root`.
   Require all fields; reject blank, control-character or `·`-bearing text,
   invalid dates and end-before-start, but do not derive duration from dates.
   Resolve only `plans/changes/<single-name>/plan.md`; reject traversal,
   archive selection, symlinked parents/file and hard-linked plans before
   reading or writing. Require readable UTF-8 and one time heading; validate
   everything before the shared write, publish safely, stamp `updated:`,
   print the resulting line, return 0; refusal/write failure returns 2 with
   bounded context. No partial overwrite on a failed publication.
3. Change `scripts/stage2.py`: preserve public helper signatures and Refused
   behavior as thin adapters to the shared module; keep clocks, successful-call
   boundary, persistence/recovery policy and retry snapshots where they are.
   Route normal, retry and exceptional time persistence through the common
   writer with the existing safe-restore callback; do not start a CLI subprocess.
4. Change `scripts/run_report.py`: replace the local runner regex with the
   shared parser, preserving TimeRecord-facing behavior, optional bullet
   handling, attempt display, unread counts, totals and appetite warnings.
   Keep the existing stage2 time-section adapter and unrelated readers intact.
5. Create `tests/test_time_records.py` for the shared format, validation and
   section boundaries; create `tests/test_harness_time_log.py` for CLI
   round-trips, refusal without writes and path/publication failures; change
   `tests/test_stage2.py` to prove the shared writer is used without losing
   existing completion/recovery guarantees; change `tests/test_run_report.py`
   to consume command output alongside runner records and unread prose.
6. Change `docs/WORKFLOW.md`: document the shared writer, retained marker,
   explicit measured seconds, `route orchestrator`, and no overlapping spans;
   retain the report's snapshot-only and unread-source contract.
   Change `scripts/ci_gates.py` to declare the new module as a tested library,
   not a gate, and update the harness entry's description; change
   `scripts/kit/manifest.yaml` to classify the shared module and its two new
   test files as `mechanismus`, because the existing harness command travels
   in the kit probe and must retain its import dependency. Keep the module
   and CLI tests independent of the non-travelling stage2/run-report modules.
7. **Orchestrator bootstrap after the accepted attempt:** change only the
   relevant text in held `prompts/04-implement.md` to replace manual span
   insertion with the command below, retaining clock readings, counted breaks,
   appetite notes and the prohibition on model-written Stage-2 time entries.
   The implement/repair attempt must not edit this path. Adjust the existing
   doctrine test in `tests/test_stage2.py` in that same bootstrap step, then
   run the targeted checks and `make verify` again.
8. Change `plans/changes/time-records-data/plan.md` as tests land: remove
   `not yet written` from their ledger entries and let the runner record time.
   The runner manages `plans/changes/time-records-data/findings.md` and
   regenerates `plans/INDEX.md`; no hand edits or file deletions are planned.

## Command and measurement contract

The runner keeps using monotonic elapsed seconds and UTC endpoints. An
interactive session reads its clock at span boundaries and supplies the
observed elapsed whole seconds; the writer never estimates them. For example,
with measured readings substituted for these demonstration values:

```sh
python3 scripts/harness.py time-log time-records-data --start 2026-10-31T10:00:00Z --end 2026-10-31T10:01:00Z --seconds 60 --verb implement --attempt 1 --route orchestrator --model gpt-6.1-sol --result accepted
```

This emits the existing runner line with `route orchestrator`; the final
marker names the common machine writer, not an extra model invocation.
The attempt field numbers that activity's spans; outcome names the actual
activity result. Do not log the same interval again while a runner measures
it. Stop/extension prose remains unread and unchanged. No Stage-1 exploration
fallback needs carrying forward: research records a successful Flash route.

## Criterion ledger

- 1: not yet written tests/test_harness_time_log.py::test_time_log_appends_one_counted_record — success with zero or duplicate appended records
- 2: not yet written tests/test_time_records.py::test_shared_format_preserves_runner_bytes_and_midnight — changed metadata, suffix or end date
- 3: not yet written tests/test_time_records.py::test_explicit_seconds_are_authoritative — wall-clock subtraction replaces the supplied seconds
- 3: tests/test_stage2.py::test_runner_time_entry_identifies_attempt_and_midnight_span — runner clocks or explicit duration change
- 4: not yet written tests/test_harness_time_log.py::test_invalid_input_and_unsafe_destination_leave_bytes_unchanged — invalid fields or an unsafe destination receive a write
- 4: not yet written tests/test_harness_time_log.py::test_publication_failure_preserves_plan — failure truncates the plan or returns success
- 5: not yet written tests/test_time_records.py::test_shared_append_preserves_section_content — old prose disappears or a following section is changed
- 6: not yet written tests/test_stage2.py::test_runner_time_persistence_uses_shared_writer — runner bypasses the common write service
- 6: tests/test_stage2.py::test_runner_preserves_precall_time_on_final_verdict — model time replaces trusted history or completion duplicates a record
- 6: tests/test_stage2.py::test_runner_early_refusal_recovers_time_destination_safely — recovery writes an alias target or loses a rejection
- 6: tests/test_stage2.py::test_runner_time_write_failure_keeps_original_cause — failed logging hides the original failure or permits progress
- 7: not yet written tests/test_run_report.py::test_report_counts_shared_cli_and_runner_records — the command's line is unread or counted with different seconds
- 8: tests/test_run_report.py::test_time_records_require_whitelisted_measurement_forms — prose contributes seconds or unread visibility disappears
- 9: not a test — phase-6 review checks the orchestrator's prompt update against criterion 9; manual insertion, guessed time or duplicate Stage-2 logging refutes it

## Verification

Run format/ruff checks on changed Python files and the ledger tests first;
exercise accepted, rejected, retry and early-refusal runner paths using the
existing deterministic World/FakeClock fixtures. Parameterize invalid fields,
midnight/zero-second spans, missing heading, following section, unreadable
plan and alias destinations. Prove public CLI dispatch leaves ADR behavior
unchanged. Verification commands, verbatim:

```sh
.venv/bin/python -m pytest tests/test_time_records.py tests/test_harness_time_log.py tests/test_harness_decide_adr.py tests/test_run_report.py tests/test_stage2.py
.venv/bin/python -m pytest tests/test_ci.py tests/test_kit.py
python3 scripts/check_interview_minimums.py --change time-records-data
python3 scripts/check_criterion_ledger.py
make verify
```

The prompt names `scripts/validate_change_artefacts.py --check`, but that
script is absent at draft baseline `275efefd` (2026-10-31); do not create a
substitute gate. The runner owns complete verification and the draft commit.

## Do not touch

No historical plans/specs, ADRs, new gates, endpoint/routing settings,
`decisions/`, provenance map, configuration directories, `AGENTS.md`,
`README.md`, `templates/`, `scripts/stage2_runs.py`, Makefile recipe or
appetite semantics. Keep recovery, credential checks and checkpoint order;
record insertion is shared, recovery policy stays runner-owned.

## Time used
