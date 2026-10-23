---
title: "Plan — runner-time-line-exits"
status: draft
implementation_status: none
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-9wp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, time-accounting]
---

# Plan — runner-time-line-exits

```text
For you:     Completed attempts keep their measured time even when a post-call check stops the run.
Done when:   Every post-call exit has regression evidence, each completed attempt retains exactly one time entry, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Failed-call timing, routing changes, verification retries or new checkpoint and recovery policies.
Pre-mortem:  suppose it failed: most likely because an early exception bypasses the shared completion boundary.
Starts unless you say stop.
```

## Files and steps

1. Change `scripts/stage2.py`: route completed `run_attempts` post-call paths
   through one time-finalization boundary, retaining existing refusal, restore
   and checkpoint behavior.
2. Change `tests/test_stage2.py`: add the exit regressions below using the
   existing `World`, `FakeClock`, `runner_entries` and scripted stand-ins.
3. Update `plans/changes/runner-time-line-exits/plan.md`: convert pending ledger
   entries as tests land; the runner appends measured phase-4 time below.
   The runner maintains `plans/changes/runner-time-line-exits/findings.md`
   and regenerates `plans/INDEX.md`; no implementation file is created or deleted.

## Implementation contract

- Keep preflight and failed-call handling outside completed-attempt logging.
  Mark completion only after a successful return (and the existing nonempty
  Codex-answer check); begin clocks at their existing pre-invocation point.
- Enclose all subsequent processing through the verdict in one finalization
  boundary, including HEAD checks, both scans, verification, answer checks and
  diagnostic protection. Default to rejected until those checks accept it.
  Use one writer for both normal and exceptional departures; remove the old
  inline writer so a late refusal cannot produce a duplicate.
- End the UTC and monotonic span after the last check that ran, before time
  persistence, retry restoration and checkpointing. Retain `time_entry` fields
  and `with_time_entry` section handling; logging runs no verification itself.
- Reuse the existing safe destination recovery and `restore_work_input` for
  missing parents and aliases, without reading or writing through aliases.
  Exceptional rejections can use the trusted pre-call plan plus their entry;
  never restore credential-bearing model bytes. Preserve previous time records,
  route blocks, date stamping and the baseline-plus-entry retry snapshot.
- Propagate the original refusal/failure after logging; never retry or
  checkpoint from the finalizer, reset HEAD, or turn a refusal into success.
  If logging itself fails, fail closed with both its error and the original
  failure as the cause. The accepted/rejected label remains a pre-checkpoint
  verdict; checkpoint failures must not trigger a second entry.
- Add one regression per exceptional exit, parameterizing implement and repair
  where applicable. Assert persisted entry/count, rejection, controlled duration,
  call count and absence of checkpoint; credential cases also assert scrubbing.
  Cover early refusals with deleted/rewritten plans and parent/file aliases.
  For HEAD checks use in-memory seams, preserving moved history. Plant a
  refusal in diagnostic protection too, to prove the boundary is structural.
- Keep existing test names and all prior time, route, restore and safety
  coverage. Do not touch prompts, workflow, ADRs, tracker, model configuration,
  other change artifacts or unrelated runner verbs.

## Criterion ledger

- 1: tests/test_stage2.py::test_runner_logs_first_postcall_credential_refusal — the first scan raises before the entry
- 1: tests/test_stage2.py::test_runner_logs_verify_refusal — verify_attempt raises Refused before the entry
- 1: tests/test_stage2.py::test_runner_time_includes_postgate_credential_rejection — the late scan omits or duplicates the rejected entry
- 1: tests/test_stage2.py::test_runner_logs_unstartable_verify_once — cannot_start omits or duplicates the entry
- 1: tests/test_stage2.py::test_runner_logs_completed_call_head_failure — unreadable or moved HEAD skips logging
- 1: tests/test_stage2.py::test_runner_logs_postcall_diagnostic_refusal — diagnostic protection raises outside the boundary
- 1: tests/test_stage2.py::test_runner_logs_each_completed_attempt_once — normal verdicts omit or duplicate an entry
- 2: tests/test_stage2.py::test_runner_logging_preserves_terminal_refusals — logging masks refusal, starts fallback/checkpoint or leaves a leaked key
- 3: tests/test_stage2.py::test_runner_early_rejection_span_reaches_refusing_check — endpoint precedes refusal or its identity/result is wrong
- 3: tests/test_stage2.py::test_runner_time_entry_identifies_attempt_and_midnight_span — fields or monotonic duration change
- 3: tests/test_stage2.py::test_runner_span_includes_model_and_postchecks — checkpoint time enters the span
- 4: tests/test_stage2.py::test_runner_keeps_rejected_time_across_input_restore — retry loses earlier time
- 4: tests/test_stage2.py::test_runner_preserves_precall_time_on_final_verdict — model-rewritten time replaces trusted records
- 4: tests/test_stage2.py::test_runner_time_insert_preserves_section_boundaries — entry lands outside its section
- 5: tests/test_stage2.py::test_runner_early_refusal_recovers_time_destination_safely — early refusal loses recoverable time or writes through an alias
- 5: tests/test_stage2.py::test_runner_time_write_failure_keeps_original_cause — write failure masks refusal or permits fallback/checkpoint
- 6: tests/test_stage2.py::test_runner_does_not_log_uncompleted_calls — failed/empty call or preflight rejection acquires a completed entry

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q
.venv/bin/python3 scripts/check_interview_minimums.py --change runner-time-line-exits
.venv/bin/python3 scripts/check_criterion_ledger.py
PYTHON=$PWD/.venv/bin/python3 make verify
```

Demonstrate the new early-exit tests red against the input runner, then green
after repair; use fake clocks and local stand-ins, no sleeps or live providers.
The runner owns index regeneration, full verification and the one commit.
The requested change-artefact validator and a plan template are absent at input
commit `2b16cb4`; use the existing gates and this phase-3 prompt's form.

## Explore route

Research was written by the orchestrating Claude Code Opus 5.5 session on
2026-10-23 at `8acaa8b` from an already reproduced finding; no separate
exploration call or Stage-1 fallback was recorded.

## Runner route — 2026-10-23

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-23 08:50:03–09:28:11 UTC, 2288 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-23 09:28:17–10:03:53 UTC, 2137 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-23 10:03:59–10:10:09 UTC, 370 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
