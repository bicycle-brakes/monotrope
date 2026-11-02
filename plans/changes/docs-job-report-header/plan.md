---
title: "Plan — docs-job-report-header"
status: draft
implementation_status: none
date: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-ooj5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification]
---

# Plan — docs-job-report-header

```text
For you:     The verification header names the selected document subset and its gate count consistently with the run.
Done when:   Runner tests prove the selected name, counts, existing report fields and gate verdicts, and make verify is green.
Appetite:    1 hour of phase 4, repairs included; stop at the limit.
Not now:     Gate membership, report schema, hosted CI, worker sizing or the make report snapshot.
Pre-mortem:  suppose it failed: most likely because tests exercise the report producer without running the caller that omits the job.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_ci.py`: use the existing copied-runner helpers to add the two
   ledger tests. Run the real shell runner and gate reader with default,
   explicit verify, docs and drift selections. Seed unequal membership counts
   and marker commands; parse the initial JSON with `JSONDecoder.raw_decode`
   so later gate output is not treated as JSON. First demonstrate that docs
   and drift fail against the unchanged runner.
2. `scripts/verify_all.sh`: change only the report invocation to
   `"$PYTHON" scripts/ci_gates.py --report --job "$JOB" || exit 2`.
3. `tests/test_ci.py`: assert the exact existing report key set, selected
   membership count, global total and gate-file byte digest. Include a
   selected hosted-only gate so membership differs from locally executed
   commands. Keep git identity deterministic inside the temporary tree by
   supplying a local fake git returning known HEAD/base values, then failing
   it to check nulls; never depend on the developer's refs. Check executed
   markers and block/report/advisory failures, including a later passing gate.
4. `plans/changes/docs-job-report-header/plan.md`: clear not-yet-written
   ledger markers as tests land and record phase-4 time below.
   `plans/changes/docs-job-report-header/findings.md`: record dated revision-bound
   regression and review evidence. `plans/INDEX.md`: the runner regenerates
   the index during preparation. No file is deleted; no held path needs editing.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_ci.py
PYTHON=.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_ci.py::test_runner_report_matches_selected_job — docs or drift reports verify, or default/explicit verify reports another name.
- 2: tests/test_ci.py::test_runner_report_matches_selected_job — selected/global counts are confused or placement removes a gate from the membership count.
- 3: tests/test_ci.py::test_runner_report_matches_selected_job — keys, known git values, unavailable-reference nulls or the configuration byte digest change.
- 4: tests/test_ci.py::test_runner_report_keeps_gate_verdict — unselected gates run, later gates are skipped, or block/report/advisory failures give the wrong exit code.

## Boundaries and route

Do not edit `scripts/ci_gates.py`, `decisions/gates.yaml`, `.github/`,
`Makefile`, `scripts/stage2.py`, `scripts/verify_lock.py`,
`scripts/run_report.py`, `docs/WORKFLOW.md`, ADRs, prompts, templates or
harness configuration. Preserve admission, worker sizing and report-failure
exit 2. No design or ADR is due for this bounded change. Explore ran through
Stage 2 on 2026-11-02, route flash, endpoint `glm-coding-plan`, model
`glm-5.3-flash`; no Stage-1 fallback is recorded.

## Time used

2026-11-02 09:27:18–10:12:26 UTC, 2708 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
