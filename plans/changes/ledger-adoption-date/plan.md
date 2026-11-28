---
title: "Plan — ledger-adoption-date"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-64fa
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, gates]
---

# Plan — ledger-adoption-date

```text
For you:     The criterion ledger gate follows the adoption date recorded for each repository.
Done when:   Boundary and unreadable-record tests pass and make verify is green.
Appetite:    2 hours for implementation and repairs; stop at the limit.
Not now:     Changing adoption dates, other gates or historical ADR decisions.
Pre-mortem:  suppose it failed: most likely because a test still relies on the old hard-coded date.
Starts unless you say stop.
```

## Steps

1. Change `scripts/check_criterion_ledger.py`: load `criterion-ledger` through `adoption.adopted_on(root, ...)` once per run, pass the date to archive measurement and summary, and map `NotRecorded` to not measured with its remedy and exit 3. Preserve the existing strict plan-header rules, live-plan and archived-ledger behavior; remove the constant and stale docstring wording.
2. Change `tests/test_check_criterion_ledger.py`: give isolated trees a valid adoption record; update the existing boundary and summary tests, and add tests for a different configured date, the 2026-10-28/29 boundary, and missing, unreadable, malformed, absent, quoted and impossible records. Check the diagnostic and exit 3, including when no plans exist. Update the workflow-row assertion to the recorded-date rule. Leave independent reader fixtures in `tests/test_adoption.py` intact.
3. Change `docs/WORKFLOW.md`: describe the repository's adoption record as the boundary and retain the decision pull request requirement for changing it. Leave `decisions/adoption.yaml`, `docs/adr/0013-every-criterion-names-its-proof.md`, `docs/adr/0014-a-change-claims-its-adr-files.md`, gate configuration, the kit manifest and other gates untouched. No held path needs an implementation edit and no file is deleted.
4. Update `plans/changes/ledger-adoption-date/plan.md` ledger entries when new tests exist. The orchestrator records review evidence in `plans/changes/ledger-adoption-date/findings.md` and states the widened 2026-10-11 through 2026-10-28 exemption in the pull request. Run the checks below; stop when the appetite is used.

Explore fallback: Stage 1 via `claude-code-plan`, model `claude-haiku-5-5`, because GLM through Z.ai had reached its weekly limit until 2026-11-29 (research, 2026-11-28).

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_check_criterion_ledger.py tests/test_adoption.py
python3 scripts/jobs.py start -- make verify
```

Check the detached verification job's exit with `python3 scripts/jobs.py list` before phase 6.

## Criterion ledger

- 1: not yet written tests/test_check_criterion_ledger.py::test_recorded_adoption_date_controls_exemption — changing the record does not move the boundary or the adoption day is exempt.
- 2: tests/test_check_criterion_ledger.py::test_an_archived_plan_without_a_ledger_is_exempt_only_by_an_earlier_plain_date — a valid earlier date is held.
- 3: tests/test_check_criterion_ledger.py::test_an_archived_plan_without_a_ledger_is_exempt_only_by_an_earlier_plain_date — a malformed header date is exempt.
- 4: tests/test_check_criterion_ledger.py::test_every_live_plan_is_held_whatever_its_date_and_class — a live plan before adoption is exempt.
- 5: tests/test_check_criterion_ledger.py::test_an_archived_ledger_is_held_whatever_its_date — an old ledger naming a missing test passes.
- 6: not yet written tests/test_check_criterion_ledger.py::test_unusable_adoption_record_is_not_measured — an unusable record passes or lacks the remedy or exit 3.
- 7: not yet written tests/test_check_criterion_ledger.py::test_summary_names_recorded_adoption_date — the summary reports a different date.
- 8: tests/test_check_criterion_ledger.py::test_the_workflow_names_the_gate_and_its_exemption — the row fails to name the adoption record.
- 8: tests/test_check_criterion_ledger.py::test_the_workflow_row_makes_moving_the_cutoff_a_governance_act — the row omits the decision requirement.

## Time used

2026-11-28 14:14:52–14:16:56 UTC, 124 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
