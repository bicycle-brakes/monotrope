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
Pre-mortem:  suppose it failed: most likely because a job outlives its launcher but loses its outcome or verification admission.
Starts unless you say stop.
```

## Files and sequence

1. Create `scripts/jobs.py` with `start`, `list`, and `stop`; use a unique job ID, preserve command argument boundaries and working directory, and check tmux before starting. Start one tmux window per job with a wrapper independent of the launcher process. The wrapper captures both streams in the job log, waits for the actual command and atomically writes its end time and exit status. Place records and logs under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/jobs/`. A disappeared window without a completed record is unknown, never successful. Stop identifies one recorded window and does not act on a reused or unrelated window; publish a stopped or unknown outcome without fabricating an exit code. Refuse malformed records and failed starts clearly; concurrent jobs must not overwrite one another.
2. Use the existing verification entry point from the job itself, without holding an admission in the short-lived launcher or creating a second quota. Preserve the inherited environment needed by the runner and its existing policy; model commands continue through `scripts/stage2.py`. Do not write lane or busy markers. `lanes.py advance` is future work and is not implemented here.
3. Change `scripts/run_report.py` to read the same job records and show running jobs, including an explicit unreadable or unknown state on bad or incomplete data; retain its existing report and read-only behavior. Change `scripts/ci_gates.py` to declare the launcher caller, and `scripts/kit/manifest.yaml` to carry the launcher and every new dependency as a mechanism. Change `tests/test_jobs.py` (new) and `tests/test_run_report.py` for the ledger, including isolated state and concurrent jobs. Change `tests/test_kit.py` if needed to prove the exported launcher runs with its imports. No file is deleted.
4. Orchestrator bootstrap after the accepted implementation attempt: update held `AGENTS.md` background-mode guidance to name the detached launcher and retain the 30-minute wake until `lanes.py advance` lands. The orchestrator handles any necessary held-path edits and registry regeneration; the implementation attempt must not edit held paths. `docs/adr/0026-detached-job-launcher.md` is the proposed decision already drafted with this plan. Update `docs/WORKFLOW.md` night-run guidance to align with the decision while retaining wake and existing supervision; do not change the earlier historical artifacts.
5. Update `plans/changes/detached-job-launcher/plan.md` ledger entries as tests are written and record phase-4 time in `## Time used`; the runner records findings. Run a real tmux smoke test in an isolated state directory: start a command from a short-lived parent, end that parent, observe the command still running, then observe its exact nonzero exit and log after completion. Record command, result and commit in the pull request; do not kill an unrelated tmux server.

Do not touch `scripts/verify_lock.py`, its quota or memory floor, `scripts/stage2.py` model routes, lane files or busy markers. Do not add scheduling, automatic advancement or permissions policy. The central permissions change (bead coding-harness-a6ns.2) remains separate.

## Verification

```sh
.venv/bin/python -m pytest -q tests/test_jobs.py tests/test_run_report.py tests/test_kit.py
python3 scripts/check_interview_minimums.py --change detached-job-launcher
python3 scripts/check_research_handoff.py --change detached-job-launcher
python3 scripts/plans_registry.py --check
make verify
```

## Criterion ledger

- 1: not yet written tests/test_jobs.py::test_job_survives_launcher_exit — ending the launching process kills the job or windows are shared
- 2: not yet written tests/test_jobs.py::test_missing_tmux_refuses_start — a command runs without tmux or no useful diagnostic appears
- 3: not yet written tests/test_jobs.py::test_stop_targets_only_selected_job — another job stops or the selected job survives
- 4: not yet written tests/test_jobs.py::test_start_record_contains_command_window_time_and_log — a required field or location is wrong
- 5: not yet written tests/test_jobs.py::test_completion_retains_real_exit_status — the final status or end time is lost or wrong
- 6: not yet written tests/test_jobs.py::test_list_reports_running_job — a running job is absent or misclassified
- 7: not yet written tests/test_run_report.py::test_report_includes_running_detached_job — report omits the running record
- 8: not yet written tests/test_jobs.py::test_detached_verify_obeys_shared_admission — detached verification bypasses the shared limit or floor
- 9: not yet written tests/test_jobs.py::test_runner_command_keeps_stage2_entry — the launcher changes or bypasses the runner command
- 10: not yet written tests/test_kit.py::test_detached_launcher_travels_with_dependencies — installed kit lacks launcher or imports
- 11: not yet written tests/test_jobs.py::test_ci_declares_launcher_caller — the caller registry lacks the launcher
- 12: not yet written tests/test_jobs.py::test_launcher_does_not_write_lane_markers — launcher alters a lane or busy marker
- 13: not a test — phase-6 review checks the proposed ADR explicitly supersedes both headless-job non-goals
- 14: not a test — phase-6 review checks both updated guidance and ADR retain the 30-minute wake until advance lands
- 15: not a test — phase-6 review checks the held background guidance names detached launching and the interim wake

## Time used

2026-11-24 13:29:42–13:33:56 UTC, 254 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
