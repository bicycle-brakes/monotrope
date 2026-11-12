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
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, temporary-files]
---

# Plan — verify-tmp-cleanup

```text
For you:     Full checks remove their own pytest folders; failed runs can be kept explicitly, and the next run removes dead-process leftovers.
Done when:   Isolated tests prove placement, exit/interrupt cleanup, retention and next-start recovery; make verify is green.
Appetite:    4 hours of phase 4, repairs included; stop at the limit.
Not now:     Standalone targeted tests, historical leftovers, free-disk admission or supervisor changes.
Pre-mortem:  suppose it failed: most likely because a nested run deleted its parent's folder.
Starts unless you say stop.
```

## Files and steps

1. In `tests/test_ci.py`, add the runner tests in the ledger using the existing
   copied-runner helpers; prove missing behavior red before implementation.
   Isolate the temporary parent, admission state and home in fixtures; clear
   inherited run-area markers while preserving valid admission in nested probes;
   use a zero memory floor so probes never depend on machine pressure.
2. In `scripts/verify_all.sh`, add the small runner-owned lifecycle chosen by
   Q-1, after `--list` and admission re-exec, before reports/gates. Use the
   executing shell's `$$` as its area name. Keep the existing admission entry
   unchanged; never add `--tmp-scope`, `--tmp-held` or a helper module. Aim for
   about twenty core lifecycle lines, with only the validation needed by the
   criteria, rather than rebuilding the rejected supervisor architecture.
3. Use an absolute private per-user managed parent under the caller's original
   `PYTEST_DEBUG_TEMPROOT` or platform temporary parent. Carry this original
   managed-parent locator through nested runner environments; each run still
   allocates its own PID area using exclusive creation. Export only its own
   area as `PYTEST_DEBUG_TEMPROOT`; leave `TMPDIR`, gate commands and unrelated
   `PYTEST_ADDOPTS` unchanged. Reject malformed shell quoting and explicit
   basetemp spellings (both value forms and pytest-accepted abbreviations)
   before gates. Use the selected interpreter for parsing if needed, inline
   in this script rather than through a new module/dependency.
4. At startup inspect only numeric direct-child directories of that private
   parent, skip retained entries and live PIDs, and remove dead-PID entries.
   Skip non-managed names; refuse unsafe ownership/type or symlink substitutions
   with a path/reason. Never follow a symlink, sweep the caller's parent or
   infer liveness from age. Fail before gates if safe setup/sweeping fails.
5. Install EXIT and INT/TERM/HUP/QUIT cleanup without changing the supervisor.
   Preserve the original status; on cleanup failure report path/reason and
   retain nonzero statuses, or return 2 after otherwise successful work.
   Mark an explicit keep request and report its absolute path before gates
   so a hard kill cannot lose either the request or its inspection location;
   successful runs remove their area anyway. Failed/interrupted requested
   runs report the absolute retained path. Keep cleanup idempotent across
   signal and EXIT handling, including early report/gate-list errors.
6. Complete the probes: nested runners, two real pytest sessions, xdist `-n 2`,
   green/red exits, all four handled signals, explicit/non-1 retention values,
   subsequent sweeps and a killed/reaped runner followed by another start.
   Cover the public supervisor entry and valid inherited admission; do not
   require descendant leases or deletion after process-group teardown.
   Check live sibling/symlink/unrelated sentinels and injected storage failures.
   Keep probe outputs outside the deleted area; bound waits and reap children.
7. Document retention and the PID-only hard-kill boundary in usage comments
   of `scripts/verify_all.sh`. In `plans/changes/verify-tmp-cleanup/plan.md`,
   replace ledger markers as tests land and record measured time below; add
   revision-bound results to `plans/changes/verify-tmp-cleanup/findings.md`.
   `plans/changes/verify-tmp-cleanup/spec.md` remains the yardstick. No source
   file is added or deleted. The orchestrator regenerates `plans/INDEX.md`;
   no held-path implementation or bootstrap edit is needed.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_ci.py tests/test_verify_lock.py tests/test_verify_duration.py
PYTHON=.venv/bin/python3 make verify
```

Use minimal pytest probes, not recursive full suites. The runner owns full
verification and the commit. Review the diff to ensure `scripts/verify_lock.py`
and its tests are unchanged and the only lifecycle owner is the shell runner.

## Criterion ledger

- 1: not yet written tests/test_ci.py::test_verify_runner_owns_distinct_pid_areas — nested runs share an area, lose PID naming or delete their parent's area.
- 2: not yet written tests/test_ci.py::test_verify_runner_contains_pytest_sessions_and_workers — serial/xdist or second-session paths escape or erase another session.
- 3: not yet written tests/test_ci.py::test_verify_runner_cleans_normal_exit — green/red exits leave payloads or successful cleanup changes the verdict.
- 4: not yet written tests/test_ci.py::test_verify_runner_cleans_on_interrupt — handled signals leave payloads or lose the public supervisor's signal status.
- 5: not yet written tests/test_ci.py::test_verify_runner_retains_only_on_explicit_request — requested failed/interrupted evidence disappears, lacks a path or is swept later; another value retains.
- 6: not yet written tests/test_ci.py::test_verify_runner_cleans_normal_exit — successful requested retention leaves payloads.
- 7: not yet written tests/test_ci.py::test_verify_runner_reclaims_dead_pid_areas — a killed/reaped runner's area survives the next start or a live PID's area disappears.
- 8: not yet written tests/test_ci.py::test_verify_runner_preserves_unrelated_paths — caller/default-root sentinels, unrelated entries or symlink targets change.
- 9: not yet written tests/test_ci.py::test_verify_runner_reports_temp_storage_failures — setup failure starts gates or cleanup failure is silent/green.
- 10: tests/test_ci.py::test_runner_holds_no_command_list_of_its_own — lifecycle wiring creates another gate-command source.
- 10: tests/test_ci.py::test_the_makefile_runs_what_the_one_list_runs — the gate command and Makefile recipe drift.
- 10: not yet written tests/test_ci.py::test_verify_runner_preserves_entry_contracts — list allocates/admit work, job/CI selection changes, nested admission requeues or worker/duration ownership changes.
- 11: not yet written tests/test_ci.py::test_verify_runner_refuses_conflicting_pytest_options — basetemp escapes, malformed quoting passes or unrelated options are lost.

## Boundaries and route

Do not edit `scripts/verify_lock.py`, `tests/test_verify_lock.py`,
`decisions/gates.yaml`, `Makefile`, `pyproject.toml`, `scripts/stage2.py`,
`scripts/kit/probe.py`, `scripts/verify_duration.py`, `tests/test_verify_duration.py`,
kit manifests, governance, ADRs, prompts, templates or harness configuration.
The PID-only rule can reclaim a dead runner's area despite surviving children;
PID reuse may defer recovery. No lease registry or descendant guarantee is added.

Class remains bounded: no design or ADR is due. The answered Q-1 of 2026-11-12
supersedes the old interview skip and supervisor plan. No open phase-2a rows
were found. Explore used Stage 2 on 2026-11-10, route flash, endpoint
`glm-coding-plan`, model `glm-5.3-flash`; no Explore fallback is recorded.
The historical implement fallback was Stage 1, model `claude-sonnet-5-5`,
because two Flash post-run checks failed; its rejected time remains in
`findings.md` and counts against the four-hour appetite, not a fresh budget.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at
`a320748b`; use the phase-3 form and existing artifact gates. The orchestrator
owns index regeneration and tracker-backed registry/full verification.

## Time used
