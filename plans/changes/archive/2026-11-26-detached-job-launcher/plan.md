---
title: "Plan — detached-job-launcher"
status: accepted
implementation_status: done
date: 2026-11-24
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-a6ns.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, jobs, night-run]
---

# Plan — detached-job-launcher

```text
For you:     Runner jobs keep running after the session ends and remain visible with their outcome.
Done when:   Survival, stopping, reporting, shared verification admission and kit delivery are tested and make verify passes.
Appetite:    8 hours of phase 4 including repairs; stop at the limit.
Not now:     Automatic lane advancement, a new permissions policy, or removing the 30-minute wake.
Pre-mortem:  suppose it failed: most likely because the job tree survives a stop and retains a verification admission.
Starts unless you say stop.
```

## Files and sequence

1. Create `scripts/jobs.py` with `start`, `list`, and `stop`; use a unique job ID, preserve command argument boundaries and working directory, and check tmux before starting. Start a detached dedicated `tmux -L coding-harness` server if absent and one window per job with a wrapper independent of the launcher process. Pass the caller cwd and whole environment explicitly per job, clearing `HARNESS_VERIFY_LOCK_HELD`, `HARNESS_VERIFY_LOCK_TOKEN`, `HARNESS_VERIFY_ADMISSION_ID` and `HARNESS_VERIFY_ADMISSION_WAIT`; pass `VIRTUAL_ENV` and the caller PATH including its virtual-environment prefix. Classify as a runner verb when argv invokes scripts/stage2.py followed by a non-option word, without importing stage2. Store a schema-validated, atomically written JSON record including the two PIDs with process start times, process groups and stop request. Pass its path to the command via an environment variable. Wait at most 10 seconds for both PIDs; otherwise exit 1 with state failed to start. The wrapper captures both streams in the job log, waits for the actual command and atomically writes its end time and exit status. Place records and logs under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/jobs/`. A vanished wrapper without a completed record is lost and remains visible until pruning 14 days after start; the wrapper records an exit code or `signal N`. Write the stop request before signalling the selected command tree and recorded process groups, including separately sessioned descendants; after five seconds escalate surviving verified identities to SIGKILL; spare the wrapper to record `signal 15` regardless of exit status, and release admission without touching other jobs. Refuse stop on finished, lost or process-identity-mismatched jobs with exit 2; a reused PID counts as gone. Prune each log with its record; keep finished records 14 days from end and lost records 14 days from start; list running jobs, retained lost jobs and those finished within 24 hours by default, all retained records with `--all`. Refuse malformed records and failed starts clearly; concurrent jobs must not overwrite one another.
2. Use the existing verification entry point from the job itself, without holding an admission in the short-lived launcher or creating a second quota. Clear all four inherited admission values so every job obtains its own slot; model commands continue through `scripts/stage2.py`. Do not write lane or busy markers. `lanes.py advance` is future work and is not implemented here.
3. Change `scripts/stage2.py` to append every process group it starts in its own session, with process identity, to the supplied job record. Change `scripts/machine_facts.py` to include job records in its jobs field. Change `scripts/run_report.py` to read the same job records and show running jobs, deduplicate by started command PID against process recognition, show only the program name without arguments for non-runner jobs, and show an explicit unreadable or lost state on bad or incomplete data; retain its existing report and read-only behavior. Change `scripts/ci_gates.py` to declare the launcher caller, and `scripts/kit/manifest.yaml` to carry the launcher and every new dependency as a mechanism. Change `tests/test_jobs.py` (new) , `tests/test_run_report.py`, `tests/test_machine_facts.py`, and `tests/test_stage2.py` for the ledger, including isolated state and concurrent jobs. Change `tests/test_kit.py` if needed to prove the exported launcher runs with its imports. No file is deleted.
4. Orchestrator bootstrap after the accepted implementation attempt: update held `AGENTS.md` background-mode guidance to require the detached launcher for every runner verb and bare `make verify`, allow harness background mode for commands outside the runner, and retain the 30-minute wake until `lanes.py advance` lands. The orchestrator handles any necessary held-path edits and registry regeneration; the implementation attempt must not edit held paths. `docs/adr/0026-detached-job-launcher.md` is the proposed decision already drafted with this plan. Update `docs/WORKFLOW.md` night-run guidance to align with the decision, explain reading job completion, and retain wake and existing supervision; do not change the earlier historical artifacts.
5. Update the criterion ledger of this plan as tests are written and record phase-4 time under `## Time used`; the runner records findings. Run a real tmux smoke test in an isolated state directory: start a command from a short-lived parent, end that parent, observe the command still running, then observe its exact nonzero exit and log after completion. Record command, result and commit in the pull request; do not kill an unrelated tmux server.

Do not touch `scripts/verify_lock.py`, its quota or memory floor, `scripts/stage2.py` model routes (only process-group recording changes), lane files or busy markers. Do not add scheduling, automatic advancement or permissions policy. The central permissions change (bead coding-harness-a6ns.2) remains separate.

## Verification

```sh
.venv/bin/python -m pytest -q tests/test_jobs.py tests/test_run_report.py tests/test_machine_facts.py tests/test_stage2.py tests/test_kit.py
python3 scripts/check_interview_minimums.py --change detached-job-launcher
python3 scripts/check_research_handoff.py --change detached-job-launcher
python3 scripts/plans_registry.py --check
python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: tests/test_jobs.py::test_job_survives_launcher_exit — ending the launching process kills the job or windows are shared
- 2: tests/test_jobs.py::test_missing_tmux_refuses_start — a command runs without tmux or no useful diagnostic appears
- 3: tests/test_jobs.py::test_stop_targets_only_selected_job — a separately sessioned descendant or its admission survives, the wrapper fails to record signal 15, or another job stops
- 4: tests/test_jobs.py::test_start_record_contains_command_window_time_and_log — a required PID, process group, other field or location is wrong
- 5: tests/test_jobs.py::test_completion_retains_real_exit_status — exit code, signal, end time or 14-day retention is wrong
- 6: tests/test_jobs.py::test_list_reports_running_job — running, retained lost, recent or all retained jobs are missing or an older finished job appears by default
- 7: tests/test_run_report.py::test_report_includes_running_detached_job — report omits the record or counts its process twice
- 8: tests/test_jobs.py::test_detached_verify_obeys_shared_admission — a job inherits a held admission or bypasses the shared limit or floor
- 10: tests/test_kit.py::test_detached_launcher_travels_with_dependencies — installed kit lacks launcher or imports
- 11: tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason — the launcher has neither a caller nor a declared reason
- 12: tests/test_jobs.py::test_launcher_does_not_write_lane_markers — launcher alters a lane or busy marker
- 13: not a test — phase-6 review checks the proposed ADR quotes all three exact non-goals and exempts only detached runner verbs and make verify jobs
- 14: not a test — phase-6 review checks both updated guidance and ADR retain the 30-minute wake until advance lands
- 15: not a test — phase-6 review checks the updated guidance requires the launcher for all runner verbs and bare make verify, permits background commands outside the runner and retains the wake

- 16: tests/test_jobs.py::test_caller_environment_and_admission_are_passed_safely — server environment replaces caller values or any of the four admission values is inherited
- 17: tests/test_jobs.py::test_missing_process_is_lost — a vanished wrapper is shown as running or successful, or lost retention is wrong
- 18: tests/test_jobs.py::test_start_creates_detached_server — an outside-tmux caller cannot start a job

- 19: tests/test_jobs.py::test_records_are_schema_validated_and_atomic — invalid or partial JSON becomes visible
- 20: tests/test_stage2.py::test_job_records_separate_process_groups — a separately sessioned group is absent
- 21: tests/test_jobs.py::test_stop_refuses_finished_lost_and_reused_pids — stop signals an unrelated process or does not exit 2
- 22: tests/test_jobs.py::test_stop_request_precedes_signal — signalling occurs before the request is recorded
- 23: tests/test_run_report.py::test_detached_non_runner_hides_arguments — a command argument appears in the report
- 24: tests/test_jobs.py::test_start_waits_for_both_pids — success precedes PID publication or waits over 10 seconds
- 25: tests/test_jobs.py::test_failed_start_has_terminal_state — missing PIDs do not yield exit 1 and failed-to-start state
- 26: tests/test_jobs.py::test_log_captures_streams_and_is_pruned — a stream is missing or the log outlives its record
- 27: tests/test_machine_facts.py::test_jobs_field_includes_detached_records — a record-only job is omitted

## Runner route — 2026-11-24

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash via Claude Code fails with unrecognized_model in two attempts on 2026-11-24 (bead coding-harness-b5pu); maintainer chose Sonnet.

## Runner route — 2026-11-24

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-25

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-25

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-24 13:29:42–13:33:56 UTC, 254 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 13:56:31–13:59:55 UTC, 204 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 15:12:09–15:15:04 UTC, 175 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 16:03:53–16:06:53 UTC, 180 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 19:12:34–19:51:49 UTC, 2355 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `scripts/ci_gates.py` is shared execution infrastructure · measured by the runner
2026-11-24 20:05:04–20:13:00 UTC, 476 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_jobs.py`, `tests/test_kit.py`, `tests/test_machine_facts.py`, `tests/test_run_report.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-24 20:38:18–20:40:27 UTC, 128 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-24 20:40:38–20:41:54 UTC, 77 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-24 20:42:06–20:43:15 UTC, 69 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-25 07:43:18–07:46:46 UTC, 209 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-25 07:47:25–07:50:36 UTC, 191 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-25 07:50:51–07:52:48 UTC, 117 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-25 12:11:47–12:17:42 UTC, 355 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-25 12:17:57–12:19:37 UTC, 101 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · rejected · measured by the runner
2026-11-25 12:19:52–12:25:44 UTC, 352 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-25 13:19:52–13:23:13 UTC, 201 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_jobs.py`, `tests/test_kit.py`, `tests/test_machine_facts.py`, `tests/test_run_report.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-25 13:41:59–13:55:21 UTC, 801 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_jobs.py`, `tests/test_kit.py`, `tests/test_machine_facts.py`, `tests/test_run_report.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-25 14:14:52–14:27:49 UTC, 777 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_jobs.py`, `tests/test_kit.py`, `tests/test_machine_facts.py`, `tests/test_run_report.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
