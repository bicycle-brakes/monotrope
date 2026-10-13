---
title: "Plan — ci-minutes"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-cac
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, ci, github-actions]
---

# Plan — ci-minutes

```text
For you:     CI runs only for pull requests (3.12 only, newest commit only) and for main (3.11 and 3.12); branch pushes without a pull request no longer cost minutes.
Done when:   make verify is green with tests that pin the three measures, and the regenerated ci.yml passes the ci-drift gate.
Appetite:    2 hours of phase 4; a stop, not an estimate.
Not now:     self-hosted runner, more legs at night, path filters for text-only changes, a configurable branch name for kit repositories.
Pre-mortem:  suppose it failed: most likely because GitHub does not evaluate the per-event matrix expression as the tests assume, and the first pull-request run shows no legs or both.
Starts unless you say stop.
```

Inputs: `spec.md` (criteria 1–8), `decisions.md` (the `[DETAIL]` choices).
Explore route: written by the planning session itself, not by the runner;
Stage 2 is blocked for GLM (bead coding-harness-6th) — see `research.md`,
"Route of this exploration".

## Steps

1. `scripts/ci_gates.py` — add a constant `MAIN_BRANCH = "main"` beside
   `MATRIX_JOB`. In `generate_ci`:
   - `on:` becomes `push:` with `    branches: [main]` (from the constant);
     `pull_request:`, `schedule` and `workflow_dispatch:` unchanged.
   - `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`; the
     group line unchanged.
   - the matrix line becomes
     `python: ${{ github.event_name == 'pull_request' && fromJSON('["<last>"]') || fromJSON('[<all>]') }}`,
     `<all>` the quoted declared list as today, `<last>` = `versionen[-1]`.
     Update the comment above it and the `_summary_job` docstring where they
     say "one leg per declared interpreter".
2. Regenerate: `.venv/bin/python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`.
3. `tests/test_ci.py`:
   - replace `_matrix(job)` with `_legs(job, event)`: assert the matrix has
     only `python`, match its value against exactly the expression form
     above (one regex, `fromJSON('…')` twice), `json.loads` both lists and
     return the one for `event`. Any other form fails the test.
   - `test_every_declared_interpreter_gets_a_leg`: push legs == declared;
     pull-request legs == `[declared[-1]]`; with `interpreters()` patched to
     three versions, push legs are the three and pull-request legs `["3.13"]`.
   - `test_every_job_sets_a_declared_interpreter_before_installing`: use the
     union of both events' legs.
   - add the four tests named in the ledger below.
4. `decisions/gates.yaml` — comments only: `job verify (per push to main / PR)`;
   the `tools` comment says push to `main` runs every entry, a pull request
   the last, the drift job the last.
5. `docs/WORKFLOW.md` §3, "Verification runs through git and CI, not through
   the harness" — one sentence after the code block: which event runs what,
   and that a branch without a pull request gets no hosted run. Bump its
   `updated:`.
6. `plans/INDEX.md` — `.venv/bin/python3 scripts/plans_registry.py --index`.

## Not touched

`tests/test_repo_settings.py` and the ruleset; `_merge_ref_findings` and the
checkout steps; the gate list itself; `AGENTS.md` (its text-only rule stays
true: the pull request is the gate); `scripts/kit/manifest.yaml` (the pair
already travels).

## Verification

```bash
git add -A && make verify
```

## Criterion ledger

- 1: not yet written tests/test_ci.py::test_push_starts_the_workflow_only_on_main — a bare `push:`, or a filter on `pull_request`
- 2: tests/test_ci.py::test_every_declared_interpreter_gets_a_leg — two legs on `pull_request`, or not the last declared one
- 2: not yet written tests/test_ci.py::test_a_pull_request_runs_only_the_last_interpreter — the generator emits a literal list
- 3: tests/test_ci.py::test_every_declared_interpreter_gets_a_leg — one leg on `push`, or a list that ignores a changed `tools.python`
- 4: not yet written tests/test_ci.py::test_only_pull_request_runs_cancel_superseded_runs — `cancel-in-progress` true or false for every event
- 4: tests/test_ci.py::test_concurrency_group_carries_the_event — the group loses the event
- 5: tests/test_ci.py::test_drift_job_runs_on_schedule_and_dispatch_only — the drift job on push or pull request
- 5: not yet written tests/test_ci.py::test_the_schedule_runs_only_the_drift_job — the matrix or summary job's `if` admits `schedule`
- 6: tests/test_ci.py::test_the_summary_check_passes_only_when_every_leg_passed — `verify` passes on a failed or cancelled leg
- 7: tests/test_gate_machinery.py::test_ci_drift_gate_goes_red_when_the_workflow_is_hand_edited — `check_ci` green on a hand edit
- 8: not a test — the phase-6 review reads the two `decisions/gates.yaml` comments and the `docs/WORKFLOW.md` sentence against criterion 8

## Time used
