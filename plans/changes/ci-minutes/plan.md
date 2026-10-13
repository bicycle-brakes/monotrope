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
For you:     CI checks only Python 3.12 and runs only for pull requests (newest commit only) and for main; branch pushes without a pull request and the 3.11 leg no longer cost minutes.
Done when:   make verify is green with tests that pin push-only-on-main, PR-only cancelling and one declared interpreter floor, and the regenerated ci.yml passes the ci-drift gate.
Appetite:    2 hours of phase 4; a stop, not an estimate.
Not now:     self-hosted runner, regenerating the lock, tools/cloud-env (lakeswitch's 3.11, moves with lakeswitch-ai-6sj), path filters for text-only changes, a configurable branch name for kit repositories.
Pre-mortem:  suppose it failed: most likely because a test or doc that silently assumes two interpreters goes red only in the hosted run, not locally.
Starts unless you say stop.
```

> Amended 2026-10-13: maintainer decided 3.12 only. The first plan's
> per-event matrix expression is dropped; this plan replaces its steps and
> ledger (the first version is in git, commit `8df968d`).

Inputs: `spec.md` (criteria 1–8), `decisions.md` (the `[DETAIL]` choices and
the addendum). Explore route: written by the planning session itself, not by
the runner; Stage 2 is blocked for GLM (bead coding-harness-6th) — see
`research.md`, "Route of this exploration".

## Steps

1. `decisions/gates.yaml` — `tools.python: ["3.12"]`; the header comment
   says `job verify (per push to main / pull request)`.
2. `pyproject.toml` — `requires-python = ">=3.12"`. `ruff.toml` —
   `target-version = "py312"`.
3. `scripts/ci_gates.py` — add `MAIN_BRANCH = "main"` beside `MATRIX_JOB`;
   in `generate_ci`, `push:` gets `    branches: [main]` from the constant,
   and `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`.
   Triggers otherwise, the group, the matrix and every job unchanged.
4. `scripts/check_research_currency.py` — the comment above `_GLIMPSE` no
   longer says the repository is checked under 3.11; the attribute form
   stays (no code change).
5. Regenerate: `.venv/bin/python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`.
6. `tests/test_ci.py` — in `test_every_declared_interpreter_gets_a_leg`
   drop `len(declared) >= 2` and assert `"3.11" not in declared`; add the
   four tests named in the ledger. Sample lists elsewhere stay.
7. `docs/WORKFLOW.md` §3, "Verification runs through git and CI, not through
   the harness" — one sentence after the code block: CI runs on pull requests
   (superseded runs cancelled) and on `main`, under Python 3.12; a branch
   without a pull request gets no hosted run. Bump its `updated:`.
8. `plans/INDEX.md` — `.venv/bin/python3 scripts/plans_registry.py --index`.

## Not touched

`requirements-ci.txt` (valid for 3.12, `research.md` amendment);
`tools/cloud-env/`; `tests/test_repo_settings.py` and the ruleset;
`_merge_ref_findings` and the checkout steps; the gate list itself;
`AGENTS.md` (nothing there names 3.11 or the matrix; its text-only rule stays
true); `scripts/kit/manifest.yaml`; sample `3.11` lists in `tests/` and the
schema's error text.

## Verification

```bash
git add -A && make verify
```

## Criterion ledger

- 1: tests/test_ci.py::test_push_starts_the_workflow_only_on_main — a bare `push:`, or a filter on `pull_request`
- 2: tests/test_ci.py::test_every_declared_interpreter_gets_a_leg — 3.11 declared, or a matrix that ignores `tools.python`
- 3: tests/test_ci.py::test_one_version_is_the_interpreter_floor — `requires-python`, the ruff target and `tools.python[0]` disagree
- 4: tests/test_ci.py::test_only_pull_request_runs_cancel_superseded_runs — `cancel-in-progress` true or false for every event
- 4: tests/test_ci.py::test_concurrency_group_carries_the_event — the group loses the event
- 5: tests/test_ci.py::test_drift_job_runs_on_schedule_and_dispatch_only — the drift job on push or pull request
- 5: tests/test_ci.py::test_the_schedule_runs_only_the_drift_job — the matrix or summary job's `if` admits `schedule`
- 6: tests/test_ci.py::test_the_summary_check_passes_only_when_every_leg_passed — `verify` passes on a failed or cancelled leg
- 7: tests/test_gate_machinery.py::test_ci_drift_gate_goes_red_when_the_workflow_is_hand_edited — `check_ci` green on a hand edit
- 8: not a test — the phase-6 review reads the `decisions/gates.yaml` header comment, the `docs/WORKFLOW.md` sentence and the `scripts/check_research_currency.py` comment against criterion 8

## Runner route — 2026-10-13

Stage-1 route: implement · model claude-sonnet-5-5 · reason: Claude Code 2.1.296 refused glm-5.3(-flash) as an unrecognized model before any call (bead coding-harness-6th).

## Time used

2026-10-13 span not measured: this session has file tools only and no `date`, so no start or end was read; the runner's timestamps are the record.

2026-10-13 orchestrator repair after the failed attempt, not timed: renamed the floor test (its old name matched the mutation-test pattern by accident, `declared_once` holds `red_on`) and declared it in the kit probe (cap 36 -> 37).
