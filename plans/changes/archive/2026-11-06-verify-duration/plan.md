---
title: "Plan — verify-duration"
status: accepted
implementation_status: done
date: 2026-11-04
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-1um6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, measurement]
---

# Plan — verify-duration

```text
For you:     Every verification run shows gate durations and keeps local machine context for comparison.
Done when:   Tests pass, five full runs supply a baseline and slow-test evidence, and a measured warning-budget proposal is written.
Appetite:    4 hours of phase 4, repairs and baseline collection included; a stop, not an estimate.
Not now:     Speed optimisation, budget enforcement, hosted CI changes or model-attempt accounting.
Pre-mortem:  suppose it failed: most likely because runs under different machine conditions are treated as comparable.
Starts unless you say stop.
```

Baseline `4d57b1c0`, inspected 2026-11-04. Implements `spec.md` and the three
maintainer answers. Class `spike`: no design or ADR. No `templates/plan.md`
exists; this follows `prompts/03-plan.md`. Explore used Stage 2, GLM 5.3 Flash
through `glm-coding-plan`; no Stage-1 fallback is recorded.

## Files and steps

1. **Implementing attempt — tests first.** Create `tests/test_verify_duration.py`
   for controlled-clock arithmetic, history persistence, reader and failure cases.
   Extend `tests/test_ci.py`'s temporary runner trees to copy the new helper and
   exercise a synthetic multi-gate list (pass, advisory failure, blocking failure,
   later pass), docs/drift selection, list-only and inherited admission. Extend
   `tests/test_verify_lock.py` for admission measurement and inherited context.
   Demonstrate a missing-timing failure against the unchanged runner before repair;
   use isolated state and fake clocks/resources, never five real verifies in tests.
2. **Implementing attempt — admission context.** Change `scripts/verify_lock.py`
   to retain queue-plus-memory elapsed seconds and a non-secret admission UUID
   (never the ownership token) after
   `_memory_gate()` succeeds, exposing them through validated ownership metadata
   and the active admission. Both CLI supervision and `hold_admission`/`inherit_env`
   descendants must resolve the same context; keep the yielded descriptor API,
   token validation, FIFO, floor, cleanup and execution timeout boundaries intact.
   Read old/missing measurement fields as unknown; no Stage-2 edits or new
   admission policy. A nested run marks reuse rather than inventing a new wait.
3. **Implementing attempt — measurements and reader.** Create
   `scripts/verify_duration.py`, invoked as `python3 -m scripts.verify_duration`,
   with small clock/start/gate/end operations for the shell and a `report` reader.
   Use standard-library monotonic time for elapsed seconds and UTC for attribution.
   Append version-1 JSON lines to `verify-duration.jsonl` under
   `verify_lock.state_root()`: `run_start`, `gate`, `run_end` events with a fresh
   run UUID. Start records hold UTC start, repository root, commit, dirty flag,
   gate-file SHA-256, job, placement, free-memory percentage sampled at execution
   start, worker setting, admission identity/wait/reuse. Gate records hold run ID,
   gate ID, seconds, exit status and enforcement; end records hold execution
   seconds and final verdict. Null means unavailable, never zero by assumption.
   Protect complete append writes with a file lock; use private regular files,
   no-follow opens and reject aliased/nonregular destinations without writing
   through them. Keep records local, with no command output, credentials or upload.
   Reader command: `python3 -m scripts.verify_duration report --run <run-id>`;
   without `--run`, list run summaries. Diagnose malformed lines, preserve valid
   earlier records and label runs without a valid end incomplete; never repair
   or truncate history in the reader, or sum reused admission waits across runs.
4. **Implementing attempt — shell integration.** Change `scripts/verify_all.sh`
   after admission to create one run identity, before report and gate selection;
   invoke helper clock operations immediately around the existing `sh -c` gate
   command and capture its status before any timing operation. Preserve live
   gate output and existing verdict text, adding gate seconds and a final
   execution/wait summary. The admission supervisor's re-exec must not create
   a duplicate run. A killed run can leave a start without an end. Report/list
   failures must not acquire a successful completion. Persistence errors emit
   visible diagnostics and leave gate execution and enforcement intact. Keep
   Bash 3.2 compatibility and the one gate list; clock/storage helpers are not
   check commands. Replace implemented ledger markers in this `plan.md`.
5. **Implementing attempt — kit and integration.** Change
   `scripts/kit/manifest.yaml` to classify the new helper and
   `tests/test_verify_duration.py` as mechanism, beside the existing runner/lock
   entries; they are dependencies of the exported runner. Existing
   `tests/test_ci.py` and `tests/test_verify_lock.py` already travel. Run the
   targeted suite and `make verify`; no held paths need an orchestrator edit.
6. **Orchestrator — measured baseline after the runner's accepted commit.**
   On one clean committed instrumentation revision, run
   `PYTEST_ADDOPTS=--durations=30 make verify`
   at least five times serially through ordinary machine admission. Keep the
   same job, placement, gate configuration and worker setting; retain stdout
   locally for each run's 30 slowest pytest durations and actual started-worker
   count. No lock bypass or foreign model call. After collection, create
   `docs/research/2026-11-04-verify-duration-baseline.md` with normal research
   frontmatter and actual measurement dates. Record run IDs, revision, exact
   command, UTC dates, execution and per-gate seconds, outcome, admission wait,
   memory, configured/actual workers and slow-test evidence in the note. Identify
   excluded failed/incomplete/dirty runs; they do not count towards five. Show
   range and median, dominant gates and slow tests, and derive a warning-budget
   proposal with a reasoned margin and machine-load limitations. Make no
   speedup claim or timeout change. Stop at the appetite with missing evidence
   explicit rather than completing the spike by assertion. Keep implementation
   status partial until this evidence and proposal are delivered.

## Verification

```bash
python3 -m pytest tests/test_verify_duration.py tests/test_verify_lock.py tests/test_ci.py -q -n auto
make verify
PYTEST_ADDOPTS=--durations=30 make verify
```

The last command is the baseline command, repeated at least five times by the
orchestrator after the accepted implementation commit. The runner commits;
the implementing attempt must not commit. Regeneration of `plans/INDEX.md`
belongs to the runner, outside this draft's writable scope. No files are deleted.

## Criterion ledger

- 1: tests/test_ci.py::test_runner_reports_each_gate_duration_and_raw_result — advisory failure has no time or is reported passed.
- 2: tests/test_verify_duration.py::test_monotonic_execution_excludes_admission_wait — a clock jump or queued delay changes execution seconds.
- 3: tests/test_verify_duration.py::test_history_appends_distinct_runs_and_marks_incomplete — a later or nested run overwrites earlier evidence or missing end becomes complete.
- 3: tests/test_ci.py::test_runner_list_does_not_record_or_duplicate_runs — listing or admission re-exec creates an extra run.
- 4: tests/test_verify_duration.py::test_records_bind_results_to_revision_and_configuration — dirty state, job, placement, gate hash or exit status is lost.
- 5: tests/test_verify_duration.py::test_machine_context_preserves_unknowns_and_worker_override — unknown memory becomes zero or worker override is guessed away.
- 5: tests/test_verify_lock.py::test_admission_measurement_survives_cli_and_inherited_context — memory wait is omitted or inherited context loses its identity.
- 6: tests/test_verify_duration.py::test_reader_selects_runs_and_diagnoses_truncated_history — truncated history crashes or fabricates successful completion.
- 7: tests/test_ci.py::test_duration_storage_failure_warns_without_changing_verdict — failed append hides a warning or changes gate execution/result.
- 7: tests/test_verify_duration.py::test_history_rejects_substituted_destinations — writing through a symlink changes its target.
- 8: tests/test_ci.py::test_timing_preserves_job_selection_enforcement_and_nested_admission — selection, later gate execution, worker forwarding or inherited lock behavior changes.
- 9: not a test — phase-6 review checks the research note against five persisted complete green same-revision runs and retained pytest evidence; fewer runs, mixed configuration or missing slow-test data refutes it.
- 10: not a test — phase-6 review checks the proposed threshold's calculation against measured execution durations and confirms the PR changes no budget, timeout or gate; an unsupported or enforced threshold refutes it.

## Not touched

`decisions/gates.yaml`, `scripts/ci_gates.py`, `.github/`, `scripts/stage2.py`,
`scripts/time_records.py`, `scripts/run_report.py`, `scripts/harness.py`,
`pyproject.toml` and its lock, governance, prompts and templates stay unchanged.
The temporary pytest option obtains slow-test evidence without editing the
authoritative gate command. Raw history and console logs stay outside Git.

## Runner route — 2026-11-04 (superseded by the following route)

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two GLM 5.3 Flash attempts failed their post-run checks on 2026-11-04 (tests red).

## Time used

2026-11-04 11:40:16–12:48:35 UTC, 4098 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 12:48:43–12:51:47 UTC, 183 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 12:51:55–12:52:33 UTC, 38 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 12:54:08–13:34:48 UTC, 2441 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-04 15:30:16–17:29:26 UTC, 7149 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-04 17:29:42–23:47:36 UTC, 22672 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 07:40:42–09:20:48 UTC, 6006 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-05 10:12:10–11:00:44 UTC, 2914 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
