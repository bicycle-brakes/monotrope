---
title: "Plan — verify-tmp-cleanup"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-12
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3, version: "2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, temporary-files]
---

# Plan — verify-tmp-cleanup

```text
For you:     Full checks clear their temporary test folders; the next check clears leftovers from a hard kill, and failed checks can be kept explicitly.
Done when:   Isolated tests prove normal, interrupted and hard-kill cleanup, retention and protection of live or unrelated folders; make verify is green.
Appetite:    4 hours of phase 4, repairs included; stop at the limit.
Not now:     Standalone targeted tests, old default pytest folders, a free-disk floor or changes to verify_lock.py.
Pre-mortem:  suppose it failed: most likely because cleanup ran before the admission re-exec and tracked the wrong process.
Starts unless you say stop.
```

## Files and steps

1. In `tests/test_ci.py`, adapt the existing run-area tests to observe
   `PYTEST_DEBUG_TEMPROOT` and numeric shell-pid areas; make `_runner_env`
   create a fixture-only `TMPDIR`. Add the ledger's runner-level interruption,
   retention, orphan, safety and failure tests. Keep existing admission,
   worker, duration, interpreter and gate-command regressions.
2. In `scripts/verify_all.sh`, remove the old `--tmp-held`/`--tmp-scope`
   re-exec, which currently aborts even the document job before gates.
   After ordinary admission has been acquired or inherited, before
   duration/report/gates, add the small lifecycle block Q-1 chose (roughly
   twenty lines for allocation/sweep/traps, not a new framework): create the
   private absolute `${TMPDIR:-/tmp}/coding-harness-verify-${UID}` parent;
   inspect only numeric, non-symlink child directories; remove dead-pid areas
   using `kill -0` liveness, skipping live or uncertain ones; create `$$`
   exclusively and export it as `PYTEST_DEBUG_TEMPROOT`. Nested runs thus use
   sibling areas. Reject unsafe parents and existing own-pid areas.
3. In that script, one EXIT handler captures `$?`, removes the owned area,
   or renames it to `kept-<pid>` for an unsuccessful explicitly requested run
   and prints its absolute path. INT/TERM/HUP/QUIT handlers exit 128+signal
   through EXIT; cleanup must not run twice. Diagnose setup/removal failures,
   preserve existing failure statuses and turn otherwise successful removal
   failures into exit 2. Keep existing process-group supervision unchanged.
   Refuse conflicting inherited basetemp options, including pytest-accepted
   abbreviations, before gates; preserve other options. Use a short inline
   interpreter check for shell-compatible option splitting, not a new module.
   Keep the retention command in the script's usage comments.
4. In `tests/test_verify_lock.py`, remove only the rejected attempt's
   temporary-scope-specific block and its exclusive helpers; its replacement
   proofs exercise the actual runner in `tests/test_ci.py`. Preserve every
   admission/process-group test. Do not edit `scripts/verify_lock.py` or fix
   its generator/context-manager defect or now-unused temporary-scope API;
   deleting those obsolete tests reflects
   Q-1's replaced architecture, not a waiver of runner behavior.
5. In `plans/changes/verify-tmp-cleanup/plan.md`, clear ledger markers as tests
   land and record measured phase-4 time below; append revision-bound evidence
   to `plans/changes/verify-tmp-cleanup/findings.md`. No source file is created
   or deleted. The runner owns `plans/INDEX.md` regeneration and the commit.

Use real copied runners with stub gates and minimal serial/repeated/`-n 2`
pytest probes. Record paths outside the area being removed. For SIGKILL,
record the admitted shell pid, kill it, wait until it is gone and the existing
supervisor has ended its group, then start a successor at the same parent;
keep another real process alive as a sweep sentinel. Bound waits and reap
children in `finally`. Stub failing filesystem commands for error cases;
never sweep machine-global test data. Confirm useful failures before the fix.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_ci.py tests/test_verify_lock.py tests/test_verify_duration.py
PYTHON=.venv/bin/python3 make verify
```

Draft blocker at `2fd91ebc`: `bash scripts/verify_all.sh --job docs` aborts
in `_TempScope.start` with `TypeError: 'generator' object does not support
the context manager protocol`. Direct document checks measure this draft,
but cannot replace the runner's required post-check. Steps 2–4 remove the
obsolete caller and replace its tests; no gate bypass or module edit is
authorized. The orchestrator must resolve this draft/implementation ordering
before retrying the same post-check; this draft leaves it visibly blocked.

## Criterion ledger

- 1: tests/test_ci.py::test_verify_runs_have_distinct_nested_temp_areas — nested runs share or remove an ancestor's area.
- 2: tests/test_ci.py::test_verify_pytest_sessions_and_workers_use_run_area — serial/repeated/parallel pytest escapes the run area.
- 3: tests/test_ci.py::test_verify_temp_cleanup_preserves_exit_status — green/red exits leave files or change their status.
- 4: not yet written tests/test_ci.py::test_verify_runner_signal_cleanup — an interrupted real runner leaves its area or loses 128-plus-signal status.
- 5: not yet written tests/test_ci.py::test_verify_runner_failed_retention — failure/interrupt evidence has no path or the successor sweep deletes it; non-1 values retain.
- 6: not yet written tests/test_ci.py::test_verify_runner_success_never_retains — a successful requested run leaves files.
- 7: not yet written tests/test_ci.py::test_verify_runner_reclaims_dead_pid_areas — a successor leaves a killed runner's area or deletes a live-pid sentinel.
- 8: not yet written tests/test_ci.py::test_verify_runner_preserves_unrelated_paths — parent/default-root sentinels, nonnumeric entries or symlink targets change.
- 9: not yet written tests/test_ci.py::test_verify_runner_temp_failures — setup failure starts gates, cleanup errors are silent, or cleanup masks failure.
- 10: tests/test_ci.py::test_runner_holds_no_command_list_of_its_own — lifecycle wiring introduces another gate list.
- 10: tests/test_ci.py::test_the_makefile_runs_what_the_one_list_runs — gate and Makefile commands diverge.
- 10: tests/test_ci.py::test_temp_scope_preserves_runner_entry_contracts — list allocates, subsets/CI bypass cleanup, nested admission requeues or duration ownership changes.
- 10: not a test — phase-6 diff review confirms scripts/verify_lock.py and all other protected paths unchanged from the implementation baseline.
- 11: tests/test_ci.py::test_verify_rejects_external_basetemp_options — a basetemp spelling escapes without refusal.
- 11: tests/test_ci.py::test_verify_keeps_unrelated_and_refuses_malformed_addopts — unrelated options change or malformed quoting starts gates.

## Limits and route

Leave `scripts/verify_lock.py`, `decisions/gates.yaml`, `Makefile`,
`pyproject.toml`, `scripts/stage2.py`, `scripts/kit/probe.py`,
`scripts/verify_duration.py`, other tests and all held paths unchanged;
no orchestrator bootstrap edit is needed. The class remains bounded, so no
`design.md` or ADR is due. Q-1 of 2026-11-12 replaces the old plan.

Explore used Stage 2 on 2026-11-10: route flash, endpoint `glm-coding-plan`,
model `glm-5.3-flash`; no Explore fallback was recorded. The previous
implementation's Sonnet fallback was not an Explore route. Rejected attempts
and their measured time remain in `findings.md`; the time section below is
empty for execution of this revised plan. The prior 3750 seconds count
against the same four-hour limit; 2 h 57 min 30 s remain before new
implementation work. No open phase-2a rows were found.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent;
this plan follows the phase-3 prompt and existing form. Use the available
interview, ledger, research-handoff and frontmatter gates for this draft;
the runner owns full verification and registry/index checks.

## Time used
