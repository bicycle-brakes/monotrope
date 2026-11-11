---
title: "Plan — verify-tmp-cleanup"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-11
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, temporary-files]
---

# Plan — verify-tmp-cleanup

```text
For you:     Full checks remove their pytest temporary areas after success, failure or interruption; failed runs can be kept explicitly, and later runs reclaim orphans.
Done when:   Isolated process tests prove placement, cleanup, retention and orphan recovery without removing active or unrelated data, and make verify is green.
Appetite:    4 hours of phase 4, repairs included; stop at the limit.
Not now:     Standalone targeted tests, historical pytest leftovers, free-disk admission or cleanup of unrelated temporary files.
Pre-mortem:  suppose it failed: most likely because a nested check was mistaken for the owner of its ancestor's temporary area.
Starts unless you say stop.
```

## Files and steps

1. Extend `tests/test_verify_lock.py` and `tests/test_ci.py` with the ledger
   tests before implementation; demonstrate missing placement/cleanup in
   isolated fixtures, not against the machine's real temporary or lock state.
   Extend existing copied-runner helpers in `tests/test_ci.py` to clear
   inherited temporary-scope markers and set fixture-only temporary parents.
2. Extend `scripts/verify_lock.py` with opt-in `--tmp-scope` supervision and
   a read-only `--tmp-held` query, leaving ordinary admission-only callers
   unchanged. A scope belongs to one supervised runner, not one admission:
   inherited admission still gets a fresh scope without another queue or
   memory wait. The query accepts only the immediate child of the live scope
   supervisor, backed by its ownership record and lease; the query checks its
   calling shell's identity, not the short-lived query process. A copied
   environment in a deeper child must not bypass its own scope.
3. In `scripts/verify_all.sh`, after `--list` handling and before the existing
   admission-context logic, query `--tmp-held`; if false, exec the existing
   module with `--tmp-scope -- bash` and the original script/arguments.
   Its direct child passes the scope query and the existing admission query,
   avoiding re-exec recursion. Preserve the supervisor-parent relation used
   by `duration_admission_context`, the gate loop and worker sizing; do not
   add gate commands or a directly invoked helper script.
4. Keep the lifecycle implementation inside `scripts/verify_lock.py`: resolve
   the temporary parent from `PYTEST_DEBUG_TEMPROOT` or `tempfile.gettempdir()`;
   create a user-owned mode-0700 managed container and unique run directories.
   Serialize publication/sweeping with a short registry flock, separate from
   admission. Publish a versioned ownership record with directory identity,
   supervisor/child identity, protected process group and retention state.
   Carry a validated container locator with the scope environment so a nested
   run allocates a sibling area under the original container, rather than
   treating its inherited pytest root as a new caller-selected parent. Hold a
   per-area flock, passed to the protected child alongside any admission fd;
   a killed supervisor alone must never make a live child's area an orphan.
5. Give the child `PYTEST_DEBUG_TEMPROOT=<run-area>` without rewriting
   `TMPDIR` or appending one shared `--basetemp` to `PYTEST_ADDOPTS`: each
   pytest session chooses its own numbered root inside the area, including
   xdist workers and the kit probe. Preserve unrelated options. Parse inherited
   `PYTEST_ADDOPTS` with pytest-compatible shell splitting and refuse both
   `--basetemp PATH` and `--basetemp=PATH` (including accepted abbreviations)
   before gates; malformed option quoting also refuses with a diagnostic.
6. Finalize the scope in `supervise()` after `_stop_child` and
   `end_lingering_group`, before releasing admission. Keep signal deferral
   around launch/publication and ignore repeated trapped signals throughout
   finalization. Snapshot `HARNESS_VERIFY_KEEP_TMP=1` in the ownership record
   before launch so recovery can preserve evidence even after SIGKILL; if an
   orphan's outcome is unknown, conservatively honor that request. With a
   known unsuccessful status and the request, mark retained and print the
   absolute inspection path; otherwise remove
   only the owned area. Always restore handlers and release admission/leases,
   including setup, spawn, sweep and removal errors; preserve existing failed
   or signal statuses and return 2 for a cleanup failure after success.
7. At scope startup sweep only recognizable, unretained managed areas in the
   same container, under the registry flock. Acquire their lease without
   waiting and establish that the recorded protected group is gone before
   deleting; a busy lease or live group means skip. Validate ownership and
   directory identity without following symlinks, including the container,
   metadata and lease files; never delete a metadata-supplied arbitrary path.
   Use descriptor-relative/no-follow operations and symlink-safe tree removal.
   Report unreadable, unsafe or undeletable candidates and fail closed rather
   than guessing; never sweep the caller's parent or legacy pytest roots.
8. Finish the process matrix in the two test files: successive and nested
   scopes, valid inherited admission, real serial pytest plus `-n 2`, all
   four signals, remaining grandchildren, interrupted retention, successful
   retention override, non-1 values, killed supervisor with a surviving child,
   later orphan recovery, retained-area persistence, symlink substitutions,
   unrelated sentinels and injected allocation/spawn/removal failures.
   Record probe paths outside the area being removed. Bound every wait, reap
   every child and use fixture-local state/temporary parents, with memory
   floor zero. Reuse existing admission, duration and worker tests as regressions.
9. Document the retention command and boundary in the module/script usage
   comments in `scripts/verify_lock.py` and `scripts/verify_all.sh`:
   `HARNESS_VERIFY_KEEP_TMP=1 PYTHON=.venv/bin/python3 make verify`;
   only unsuccessful runs retain, and retained areas need manual removal.
   Update `plans/changes/verify-tmp-cleanup/plan.md` ledger markers as tests
   land and record measured implementation time below; add revision-bound
   validation/review evidence to `plans/changes/verify-tmp-cleanup/findings.md`.
   `plans/changes/verify-tmp-cleanup/spec.md` is the yardstick, changed only
   for accepted clarifications. The runner regenerates `plans/INDEX.md`.
   No file is deleted; no new source module or held-path bootstrap edit is needed.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_verify_lock.py tests/test_ci.py tests/test_verify_duration.py
PYTHON=.venv/bin/python3 make verify
```

Use minimal pytest probe suites to verify actual paths and worker placement;
do not run the full repository suite inside the new process tests. The runner
owns full verification and the commit. Phase 6 checks the unchanged gate
commands and the stated detached-descendant boundary against the diff.

## Criterion ledger

- 1: tests/test_ci.py::test_verify_runs_have_distinct_nested_temp_areas — a nested runner shares or deletes its parent's area, or re-enters recursively.
- 2: tests/test_ci.py::test_verify_pytest_sessions_and_workers_use_run_area — real serial/xdist probes or a second pytest session escape the area or erase an active session.
- 3: tests/test_ci.py::test_verify_temp_cleanup_preserves_exit_status — green/red normal exits leave payloads or return a different original status.
- 4: tests/test_verify_lock.py::test_temp_scope_signals_clean_after_process_group — any trapped signal deletes before group cleanup, leaves payloads or loses 128-plus-signal status.
- 5: tests/test_verify_lock.py::test_failed_temp_scope_retention_is_explicit_and_reported — failed/interrupted requested evidence disappears, lacks a path or is removed by the next run; other values retain unexpectedly.
- 6: tests/test_verify_lock.py::test_successful_temp_scope_never_retains — a successful requested run leaves its payload.
- 7: tests/test_verify_lock.py::test_temp_scope_recovers_orphans_after_protected_work_ends — the next start deletes a surviving child's area or leaves a reclaimable SIGKILL orphan.
- 8: tests/test_verify_lock.py::test_temp_scope_cleanup_preserves_unrelated_paths — siblings, parent/default-root sentinels or substituted symlink targets change.
- 9: tests/test_verify_lock.py::test_temp_scope_storage_failures_are_visible_and_unsuccessful — injected setup/spawn/sweep/removal failures start unsafe work, leak admission, go silent or return success.
- 10: tests/test_ci.py::test_runner_holds_no_command_list_of_its_own — lifecycle wiring adds a second gate-command source.
- 10: tests/test_ci.py::test_the_makefile_runs_what_the_one_list_runs — the gate recipe and Makefile cease to match.
- 10: tests/test_ci.py::test_temp_scope_preserves_runner_entry_contracts — list enters admission/allocates, jobs or --ci bypass scopes, inherited admission requeues, or worker/duration context changes.
- 11: tests/test_ci.py::test_verify_rejects_external_basetemp_options — accepted basetemp spellings escape containment, or unrelated addopts are lost.

## Boundaries and route

Do not edit `decisions/gates.yaml`, `Makefile`, `pyproject.toml`,
`scripts/stage2.py`, `scripts/kit/probe.py`, `scripts/verify_duration.py`,
`tests/test_stage2.py`, `tests/test_verify_duration.py`,
`tests/test_repo_settings.py`, kit manifests, governance, ADRs, prompts,
templates or harness configuration. The existing exported module carries the
new lifecycle; adding a helper would need kit/fixture propagation and is out
of this plan. No held path is assigned to the implement attempt.

Class remains bounded; no design or ADR is due. Explore used Stage 2 on
2026-11-10, route flash, endpoint `glm-coding-plan`, model `glm-5.3-flash`;
no Stage-1 fallback is recorded. The interview has a reasoned skip in
`decisions.md`, still awaiting the maintainer's confirmation in the
orchestrating session; this draft supplies no answer. No phase-2a rows were
present in `findings.md` at drafting. There is no `templates/plan.md` in
this checkout, so this plan follows `prompts/03-plan.md` and the existing
change-plan form. `scripts/validate_change_artefacts.py` is also absent;
use the existing interview, criterion-ledger and research-handoff gates,
with the runner responsible for index regeneration and the full document job.

## Runner route — 2026-11-12

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-11 22:24:30–23:22:10 UTC, 3459 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-11 23:22:37–23:26:39 UTC, 241 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-11 23:26:50–23:27:40 UTC, 50 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
