---
title: "Plan — night-machine-facts"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-yql7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, night-run, machine-facts]
---

# Plan — night-machine-facts

```text
For you:     A dated block shows free disk, swap, registered worktrees and running jobs before night lanes start.
Done when:   Fixture tests prove the readings and honest failures, night-start display is documented, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; stop at the limit.
Not now:     Resource gates, cleanup, scheduling, session hooks or changes to the existing run report.
Pre-mortem:  suppose it failed: most likely because an unreadable source looked like a safe zero.
Starts unless you say stop.
```

## Files and steps

1. Create `tests/test_machine_facts.py` with the ledger tests, injecting the
   clock, disk reader, command runner, platform and Linux proc-data path.
   Demonstrate red cases against the absent command before implementing it.
   Use fixed macOS/Linux readings, real temporary repository registrations
   where useful, and fake process tables; never probe live machine pressure
   in deterministic tests.
2. Create `scripts/machine_facts.py` with `main()` and a testable snapshot
   collector/renderer. Resolve the invoking worktree from the current working
   directory with read-only Git, not from the script's installation path;
   collect a fresh UTC start stamp and the four fields independently.
   Set `sys.dont_write_bytecode = True` before importing local helpers.
   Accept no new operational options or environment policy.
3. In that script, use `os.statvfs(worktree)` and `f_bavail * f_frsize` for
   user-available disk bytes; render the worktree-filesystem scope without
   printing an absolute path. Read macOS `sysctl -n vm.swapusage` or Linux
   `SwapTotal`/`SwapFree` from `/proc/meminfo`; normalize units to explicitly
   labelled GiB and show used/total, rejecting missing, negative,
   non-finite or inconsistent readings rather than inventing values.
4. Read `git -C <worktree> worktree list --porcelain -z`, count non-bare
   records including stale registrations, and never prune. Reuse
   `run_report.run_command` (two-second subprocess timeout),
   `run_report.parse_processes` and `run_report.active_changes` for one
   `ps -axo pid,etime,command` snapshot and known change names. Preserve
   readable process rows when change attribution is unavailable; when the
   shared runner definitions are unavailable, label runner recognition
   `not read` rather than claiming no runners. Rows carry only PID, elapsed
   time, verb and known change or `not read`; they count invocations, so a
   verify wrapper and child are not deduplicated into a logical job.
5. Complete the test matrix in `tests/test_machine_facts.py`: worktree vs home
   disk, macOS unit conversions, Linux arithmetic and zero swap, worktree
   paths with whitespace and stale/bare records, matching and false process
   matches, successive changed readings, independent source failures,
   timeouts and malformed values. Trap unexpected subprocesses and local
   writes, including bytecode; exercise the CLI with fake system commands
   in a temporary repository and compare its state before/after. Emit only
   bounded source/reason labels on failures, never raw command output.
6. Update `docs/orchestration.md` with a short night-start subsection:
   run `python3 scripts/machine_facts.py` from the worktree, show the dated
   block in the main conversation before starting lanes, and copy it into
   the night plan's “State at the start”. Explain scopes, `not read`, the
   absence of an admission verdict and optional fresh morning reruns;
   update the document's review/update dates without rewriting history.
   Register the script in `scripts/ci_gates.py` as an `OHNE_AUFRUFER` entry
   (reason: it reads the live host, which no CI checkout can stand in for);
   `tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason`
   requires it (maintainer answer Q-M1, bead coding-harness-8sxb).
7. Update `plans/changes/night-machine-facts/plan.md` as tests land (remove
   their `not yet written` markers) and record measured phase-4 time below;
   record revision-bound validation/review evidence in
   `plans/changes/night-machine-facts/findings.md`. Keep
   `plans/changes/night-machine-facts/spec.md` aligned only with accepted
   clarifications, not implementation shortcuts. The runner regenerates
   `plans/INDEX.md`; no files are deleted and no held paths need editing.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_machine_facts.py tests/test_run_report.py
PYTHON=.venv/bin/python3 make verify
```

The first command checks the new snapshot and the unchanged process-report
contract. The full gate run remains the runner's responsibility. Phase 6
also reads the usage paragraph and the implementation diff against the
spec's boundaries; fixtures cannot prove the orchestrator followed a manual
instruction on a particular night.

## Criterion ledger

- 1: tests/test_machine_facts.py::test_cli_prints_fresh_dated_machine_block — a field/stamp is absent or successive changed sources reuse stale values.
- 2: tests/test_machine_facts.py::test_disk_reports_worktree_available_space — the wrong filesystem, used bytes, unit or scope is reported.
- 3: tests/test_machine_facts.py::test_swap_reports_used_and_total_on_both_platforms — conversion or subtraction is wrong, or valid zero swap is unreadable.
- 4: tests/test_machine_facts.py::test_worktrees_count_registered_non_bare_entries — main, linked, stale, bare or whitespace-path fixtures give an incorrect count.
- 5: tests/test_machine_facts.py::test_jobs_use_existing_process_recognition — a real invocation is lost, a wrapper is counted, an attribution is guessed or raw arguments leak.
- 6: tests/test_machine_facts.py::test_sources_fail_independently_without_becoming_a_gate — failure/timeout becomes zero, suppresses another field, leaks raw diagnostics or yields a failing valid invocation.
- 7: tests/test_machine_facts.py::test_snapshot_is_local_and_read_only — a write, unexpected command, tracker/network access or state change occurs.
- 7: not a test — phase-6 diff review verifies no admission, mutation or network path was introduced beyond the instrumented command tests.
- 8: not a test — phase-6 review reads docs/orchestration.md for the exact command, display before lane startup, dated start-state recording and snapshot-only meaning; omission or a claimed gate refutes it.

## Boundaries and route

No edits to `scripts/run_report.py`, `tests/test_run_report.py`,
`scripts/stage2.py`, `scripts/verify_lock.py`, `scripts/verify_all.sh`,
`scripts/verify_duration.py`, `AGENTS.md`, `docs/WORKFLOW.md`, `Makefile`,
ADRs, prompts, templates, gate definitions, tracker data or harness
configuration. One exception to the gate-definition rule is required and
recorded: the `OHNE_AUFRUFER` entry for `scripts/machine_facts.py` in
`scripts/ci_gates.py`, forced by
`tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason`
(every new script needs a `ci.yml` step or a declared reason); it adds no
gate and changes no existing one. There is no held-path bootstrap edit for the orchestrator.
No design or ADR is due for this bounded change. Explore ran through Stage 2
on 2026-11-06, route flash, endpoint `glm-coding-plan`, model
`glm-5.3-flash`; no Stage-1 fallback is recorded. The interview was skipped
with the reason recorded in `decisions.md`; no maintainer answer is invented.

## Runner route — 2026-11-06

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-07

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-06 00:58:23–02:11:13 UTC, 4370 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-06 02:11:26–03:01:55 UTC, 3029 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-06 03:02:09–03:26:11 UTC, 1442 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-06 19:56:51–21:06:20 UTC, 4170 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-06 21:06:31–2026-11-07 00:52:51 UTC, 13579 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-07 00:53:03–01:41:18 UTC, 2895 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
