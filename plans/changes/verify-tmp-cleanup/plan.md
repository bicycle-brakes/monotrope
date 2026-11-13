---
title: "Plan — verify-tmp-cleanup"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-12
updated: 2026-11-13
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
Appetite:    6 hours of phase 4, repairs included; stop at the limit (raised from 4 by the maintainer on 2026-11-12, decisions.md#Q-3).
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

- 1: tests/test_ci.py::test_verify_runner_owns_distinct_pid_areas — nested runs share an area, lose PID naming or delete their parent's area.
- 2: tests/test_ci.py::test_verify_runner_contains_pytest_sessions_and_workers — serial/xdist or second-session paths escape or erase another session.
- 3: tests/test_ci.py::test_verify_runner_cleans_normal_exit — green/red exits leave payloads or successful cleanup changes the verdict.
- 4: tests/test_ci.py::test_verify_runner_cleans_on_interrupt — handled signals leave payloads or lose the public supervisor's signal status.
- 5: tests/test_ci.py::test_verify_runner_retains_only_on_explicit_request — requested failed/interrupted evidence disappears, lacks a path or is swept later; another value retains.
- 6: tests/test_ci.py::test_verify_runner_cleans_normal_exit — successful requested retention leaves payloads.
- 7: tests/test_ci.py::test_verify_runner_reclaims_dead_pid_areas — a killed/reaped runner's area survives the next start or a live PID's area disappears.
- 8: tests/test_ci.py::test_verify_runner_preserves_unrelated_paths — caller/default-root sentinels, unrelated entries or symlink targets change.
- 9: tests/test_ci.py::test_verify_runner_reports_temp_storage_failures — setup failure starts gates or cleanup failure is silent/green.
- 10: tests/test_ci.py::test_runner_holds_no_command_list_of_its_own — lifecycle wiring creates another gate-command source.
- 10: tests/test_ci.py::test_the_makefile_runs_what_the_one_list_runs — the gate command and Makefile recipe drift.
- 10: tests/test_ci.py::test_verify_runner_preserves_entry_contracts — list allocates/admit work, job/CI selection changes, nested admission requeues or worker/duration ownership changes.
- 11: tests/test_ci.py::test_verify_runner_refuses_conflicting_pytest_options — basetemp escapes, malformed quoting passes or unrelated options are lost.
- 12: tests/test_stage2.py::test_shorten_git_error_keeps_the_first_line_whole_after_a_long_path — a long path or a leading warning line pushes git's reason out of the diagnostic.

## Correction for the fourth run — 2026-11-12 (decisions.md#Q-2) — superseded

Superseded by the next section (decisions.md#Q-3): keeping the start and the
end did not carry; do not implement this section.


The third attempt left three red tests, all cases of
`tests/test_stage2.py::test_failed_intent_cleanup_rejects_the_attempt_with_a_diagnostic`
with `index.lock`. Cause: `scripts/stage2.py` cuts a git error to its first
200 characters in two places (`git {verb} failed: …`), and the run area makes
the temporary path long enough that the reason at the end of git's message is
cut off. Keep the attempt's `scripts/verify_all.sh` and `tests/test_ci.py` as
they are and add only this:

1. In `scripts/stage2.py`, one small helper shortens a git error by keeping
   its start and its end with a marker between them (same total bound as
   today, about 200 characters); both `git … failed:` sites use it. No other
   line of `scripts/stage2.py` changes.
2. In `tests/test_stage2.py`, one test for the helper, red first: a message
   whose reason follows a path longer than the bound still shows the reason
   and the start. The three red cases pass unchanged; do not weaken them.

## Correction of the correction — 2026-11-12 (decisions.md#Q-3)

Keeping the start and the end of git's message did not carry: git states the
reason in its first line, behind the long path, and adds a hint paragraph
after it, so the middle with the reason was cut again. The helper now keeps
git's first non-empty line whole (first bounded at 1,000 characters; the
bound was removed by loop row L3-2 of 2026-11-13) and drops the
hint. Done by the orchestrator by hand and accepted on the maintainer's answer.

## Boundaries and route

`scripts/stage2.py` and `tests/test_stage2.py` may be edited only as the
correction above states.


Do not edit `scripts/verify_lock.py`, `tests/test_verify_lock.py`,
`decisions/gates.yaml`, `Makefile`, `pyproject.toml`,
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
`findings.md` and counts against the six-hour appetite, not a fresh budget.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at
`a320748b`; use the phase-3 form and existing artifact gates. The orchestrator
owns index regeneration and tracker-backed registry/full verification.

## Runner route — 2026-11-12

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-12

Stage-1 route: implement · model claude-sonnet-5-5 · reason: three attempts rejected; the fourth run starts from the kept third attempt with the plan correction Q-2.

## Runner route — 2026-11-13

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-12 13:48:41–15:35:51 UTC, 6429 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-12 15:36:03–16:04:37 UTC, 1714 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-12 16:04:51–16:39:14 UTC, 2063 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-12 18:16:39–19:18:51 UTC, 3732 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-12 20:41:13–20:45:01 UTC, 228 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-12 21:14:35–22:22:10 UTC, 4054 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-13 06:00:29–06:47:23 UTC, 2814 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-13 06:47:44–08:27:27 UTC, 5982 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-13 08:27:40–09:42:34 UTC, 4494 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
