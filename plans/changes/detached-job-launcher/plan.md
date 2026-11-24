---
title: "Plan — detached-job-launcher"
status: draft
implementation_status: none
date: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
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

1. Create `scripts/jobs.py` with `start`, `list`, and `stop`; use a unique job ID, preserve command argument boundaries and working directory, and check tmux before starting. Start a detached dedicated `tmux -L coding-harness` server if absent and one window per job with a wrapper independent of the launcher process. Pass the caller cwd, PATH, virtual environment, XDG_STATE_HOME and HARNESS_VERIFY_* explicitly, clearing `HARNESS_VERIFY_LOCK_HELD`, `HARNESS_VERIFY_LOCK_TOKEN`, `HARNESS_VERIFY_ADMISSION_ID` and `HARNESS_VERIFY_ADMISSION_WAIT`; pass `VIRTUAL_ENV` and the caller PATH including its virtual-environment prefix. Record whether the command is a runner verb and its started command PID, wrapper PID and recorded process group. The wrapper captures both streams in the job log, waits for the actual command and atomically writes its end time and exit status. Place records and logs under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/jobs/`. A vanished wrapper without a completed record is lost and remains visible until pruning 14 days after start; the wrapper records an exit code or `signal N`. Stop the selected command tree including separately sessioned descendants, spare the wrapper to record `signal 15` and exit, and release its verify admission without touching other jobs. Keep finished records 14 days; list running jobs, retained lost jobs and those finished within 24 hours by default, all retained records with `--all`. Refuse malformed records and failed starts clearly; concurrent jobs must not overwrite one another.
2. Use the existing verification entry point from the job itself, without holding an admission in the short-lived launcher or creating a second quota. Clear all four inherited admission values so every job obtains its own slot; model commands continue through `scripts/stage2.py`. Do not write lane or busy markers. `lanes.py advance` is future work and is not implemented here.
3. Change `scripts/run_report.py` to read the same job records and show running jobs, deduplicate by started command PID against process recognition, and show an explicit unreadable or lost state on bad or incomplete data; retain its existing report and read-only behavior. Change `scripts/ci_gates.py` to declare the launcher caller, and `scripts/kit/manifest.yaml` to carry the launcher and every new dependency as a mechanism. Change `tests/test_jobs.py` (new) and `tests/test_run_report.py` for the ledger, including isolated state and concurrent jobs. Change `tests/test_kit.py` if needed to prove the exported launcher runs with its imports. No file is deleted.
4. Orchestrator bootstrap after the accepted implementation attempt: update held `AGENTS.md` background-mode guidance to require the detached launcher for every runner verb running full `make verify` and bare `make verify`, allow harness background mode for short commands, and retain the 30-minute wake until `lanes.py advance` lands. The orchestrator handles any necessary held-path edits and registry regeneration; the implementation attempt must not edit held paths. `docs/adr/0026-detached-job-launcher.md` is the proposed decision already drafted with this plan. Update `docs/WORKFLOW.md` night-run guidance to align with the decision, explain reading job completion, and retain wake and existing supervision; do not change the earlier historical artifacts.
5. Update `plans/changes/detached-job-launcher/plan.md` ledger entries as tests are written and record phase-4 time in `## Time used`; the runner records findings. Run a real tmux smoke test in an isolated state directory: start a command from a short-lived parent, end that parent, observe the command still running, then observe its exact nonzero exit and log after completion. Record command, result and commit in the pull request; do not kill an unrelated tmux server.

Do not touch `scripts/verify_lock.py`, its quota or memory floor, `scripts/stage2.py` model routes, lane files or busy markers. Do not add scheduling, automatic advancement or permissions policy. The central permissions change (bead coding-harness-a6ns.2) remains separate.

## Verification

```sh
.venv/bin/python -m pytest -q tests/test_jobs.py tests/test_run_report.py tests/test_kit.py
python3 scripts/check_interview_minimums.py --change detached-job-launcher
python3 scripts/check_research_handoff.py --change detached-job-launcher
python3 scripts/plans_registry.py --check
python3 scripts/check_criterion_ledger.py
make verify
```

## Criterion ledger

- 1: not yet written tests/test_jobs.py::test_job_survives_launcher_exit — ending the launching process kills the job or windows are shared
- 2: not yet written tests/test_jobs.py::test_missing_tmux_refuses_start — a command runs without tmux or no useful diagnostic appears
- 3: not yet written tests/test_jobs.py::test_stop_targets_only_selected_job — a separately sessioned descendant or its admission survives, the wrapper fails to record signal 15, or another job stops
- 4: not yet written tests/test_jobs.py::test_start_record_contains_command_window_time_and_log — a required PID, process group, other field or location is wrong
- 5: not yet written tests/test_jobs.py::test_completion_retains_real_exit_status — exit code, signal, end time or 14-day retention is wrong
- 6: not yet written tests/test_jobs.py::test_list_reports_running_job — running, retained lost, recent or all retained jobs are missing or an older finished job appears by default
- 7: not yet written tests/test_run_report.py::test_report_includes_running_detached_job — report omits the record or counts its process twice
- 8: not yet written tests/test_jobs.py::test_detached_verify_obeys_shared_admission — a job inherits a held admission or bypasses the shared limit or floor
- 10: not yet written tests/test_kit.py::test_detached_launcher_travels_with_dependencies — installed kit lacks launcher or imports
- 11: tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason — the launcher has neither a caller nor a declared reason
- 12: not yet written tests/test_jobs.py::test_launcher_does_not_write_lane_markers — launcher alters a lane or busy marker
- 13: not a test — phase-6 review checks the proposed ADR quotes both exact non-goals and exempts detached runner jobs alone
- 14: not a test — phase-6 review checks both updated guidance and ADR retain the 30-minute wake until advance lands
- 15: not a test — phase-6 review checks the updated guidance requires the launcher for full verification runner verbs, also requires it for bare make verify, permits short background commands and retains the wake

- 16: not yet written tests/test_jobs.py::test_caller_environment_and_admission_are_passed_safely — server environment replaces caller values or any of the four admission values is inherited
- 17: not yet written tests/test_jobs.py::test_missing_process_is_lost — a vanished wrapper is shown as running or successful, or lost retention is wrong
- 18: not yet written tests/test_jobs.py::test_start_creates_detached_server — an outside-tmux caller cannot start a job

## Time used

2026-11-24 13:29:42–13:33:56 UTC, 254 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 13:56:31–13:59:55 UTC, 204 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 15:12:09–15:15:04 UTC, 175 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
