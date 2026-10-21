---
title: "Plan — runner-time-line"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-22
supersedes: null
superseded_by: null
bead: coding-harness-9wp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, time-accounting]
---

# Plan — runner-time-line

```text
For you:     Correct runner attempts no longer fail because the model omitted a measured time line.
Done when:   Completed attempts retain runner-measured spans, rejected retries keep their time, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Research-swarm timing tests, retries of red tests, model routing or process-failure rollback changes.
Pre-mortem:  suppose it failed: most likely because input restoration discards the rejected attempt's new time entry.
Starts unless you say stop.
```

## Files and steps

1. Change `scripts/stage2.py`: measure each completed `run_attempts` call,
   append its runner-owned entry, preserve it across restoration, and remove
   the model-added-line comparison from `verify_attempt` and runner prompts.
2. Change `tests/test_stage2.py`: replace obsolete missing-line assertions with
   automatic logging assertions, add the deterministic tests below and their
   planted faults, and retain all unrelated refusal and routing coverage.
3. Change `prompts/04-implement.md`: distinguish runner-owned attempt time
   from interactive sessions' own clock readings and time records.
4. Change `docs/WORKFLOW.md`: replace the added-line check description with
   runner-owned measurement, including rejected completed attempts.
5. Update `plans/changes/runner-time-line/plan.md`: turn ledger entries into
   written tests as they land and record measured phase-4 spans below.
   The runner maintains `plans/changes/runner-time-line/findings.md` for audit
   and review evidence and regenerates `plans/INDEX.md` as a derived file.

No implementation file is created or deleted; `spec.md` is the yardstick.
No `design.md` or ADR is due for the bounded class.

## Implementation contract

- Keep the initial `time_log(ctx.plan)` preflight for implement and repair.
  Remove only the added-line postcondition; retain post-call unreadable or
  missing-section diagnostics and every other verification failure.
- Read UTC wall time and a monotonic clock immediately around the model call
  plus post-run preparation, formatting, `make verify` and answer checks.
  End before checkpointing or the next attempt; use the monotonic difference
  for the span, never a model answer or a guessed duration. If preparation or
  verification cannot run, end at that rejection, without inventing a run.
- Append after the verdict, before a successful checkpoint or final failed
  exit: `<UTC date> <start>–<end>, <seconds> s — <verb> · attempt <n> · route
  <route> · model <id> · <accepted|rejected> · measured by the runner`.
  Include the end date when it differs. The final entry therefore includes
  verification time without running verification again just to log it.
- Use the existing time-section boundary, inserting before the next level-two
  heading. Preserve older records and route blocks; stamp `updated` using
  the existing helper. A write failure cannot produce a success or checkpoint.
- Restore rejected inputs as before, but carry the new trusted runner entry
  into the restored plan before the retry starts. Preserve pre-call time
  records even if the model rewrites them; do not restore the rejected
  model's other plan edits. Retain the missing-heading rejection even if
  restoring the baseline plan makes logging possible. A final rejected
  completed attempt must retain its measurement too; if its plan is missing
  or unreadable, restore the pre-call plan for logging after preserving the
  rejection diagnostic, without changing that verdict.
- Keep existing model-process failure, credential-refusal and moved-HEAD
  paths intact; these do not produce completed-attempt measurements.
- Update implementation prompt text, `REPAIR_FORMAT` and
  `REPAIR_FORMAT_FILE_TOOLS` to name runner ownership. Keep Codex command
  permission and file-only routes' command prohibition accurate.
- Use fake wall and monotonic readings, scripted model and verifier stand-ins,
  and planted wrong placements or removed logging; no sleeps or time bounds.
  Exercise implement, Codex repair/retry, Sonnet fallback, all-red exhaustion,
  deleted headings, following sections and a midnight crossing. Keep existing
  top-level test names, including obsolete historical names, so archived
  criterion ledgers remain valid; replace their time-line assertions only.

## Criterion ledger

- 1: tests/test_stage2.py::test_runner_accepts_attempt_without_model_time_entry — restoring the old added-line check rejects the otherwise green attempt
- 2: tests/test_stage2.py::test_runner_logs_each_completed_attempt_once — suppressing or duplicating a runner entry breaks the count for accepted and rejected attempts
- 3: tests/test_stage2.py::test_runner_span_includes_model_and_postchecks — ending before preparation or verification changes the controlled elapsed span
- 4: tests/test_stage2.py::test_runner_time_entry_identifies_attempt_and_midnight_span — omitting a field or using wall-clock subtraction instead of the controlled monotonic span fails
- 5: tests/test_stage2.py::test_runner_keeps_rejected_time_across_input_restore — restoring the old plan loses a rejected entry, including before a passing retry
- 6: tests/test_stage2.py::test_runner_time_insert_preserves_section_boundaries — appending at EOF or overwriting an older record breaks the expected section contents
- 7: tests/test_stage2.py::test_runner_time_doctrine_preserves_interactive_measurement — planting a model-owned runner instruction or removing the interactive clock rule fails
- 8: tests/test_stage2.py::test_implement_requires_spec_plan_time_heading_and_no_preexisting_work — a missing heading reaches a model
- 8: tests/test_stage2.py::test_repair_requires_a_clean_tree_a_spec_and_a_plan_with_its_time_heading — repair bypasses its initial heading guard
- 8: tests/test_stage2.py::test_runner_time_logging_does_not_retry_red_verification — rechecking red without another model call or checkpointing it fails

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change runner-time-line
python3 scripts/check_criterion_ledger.py
make verify
```

The runner owns full verification and checkpointing. Do not call a live model
for tests. `scripts/validate_change_artefacts.py` is absent at input commit
`8e7f2cf`; use the existing interview, ledger and registry gates, without
claiming the absent validator passed.

## Explore route and implementation availability

Explore was written by the orchestrator, Claude Code Opus 5.5 on 2026-10-20,
against `origin/main` at `94ae6cc`. No runner Stage-1 fallback was used:
research records that `explore --stage2-off` returned no research. Do not
invent a fallback measurement or route. Through 2026-10-21 12:34 UTC, the
maintainer's override uses the active Sol 6.1 session for implementation
because Z.ai GLM is unavailable and the Claude budget is exhausted.

## Runner route — 2026-10-20

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM model name refused by Claude Code (bead coding-harness-6th); Codex paused by the maintainer.

## Time used

2026-10-20 span not measured by this session (Sonnet 5.5, Stage-1 route, file tools only): it has no command tool, so `date` could not be read at start or end and no span is estimated; the runner's own entry for this attempt follows, and the orchestrator supplies any further measurement before the appetite is compared.

### Orchestrator — night run, 2026-10-22

Measured with `date -u`. Merged `origin/main` (127 commits; three conflicts
in `docs/WORKFLOW.md`, `scripts/stage2.py` and `tests/test_stage2.py`) and
finished the inherited Sonnet attempt by hand: 21 tests that used a missing
time line as their planted failure now plant a red `make verify`, and the
input-restore tests compare the plan without the runner's own time lines
(criterion 5). Red first: the nine runner-time tests fail against
`origin/main`'s runner, prompt and doctrine. Full `make verify` GREEN
2026-10-21T23:17:34Z to 23:22:16Z: 2383 passed, 16 skipped. Span counted:
2026-10-21T23:06:00Z (merge) to 23:23:00Z, about 17 min; the inherited
attempt's span stays not measured, as recorded above.
