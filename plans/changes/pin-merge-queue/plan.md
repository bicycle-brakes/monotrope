---
title: "Plan — pin-merge-queue"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-tsdr
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, merge-queue, repo-settings]
---

# Plan — pin-merge-queue

```text
For you:     The ruleset check accepts the merge queue for freshness only with the measured merge method and groups of one.
Done when:   Tests reject drift and missing fields, show unpinned values, preserve alternatives and bypass checks, and make verify passes.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Changing GitHub settings, merge procedures, other queue parameters or governance rules.
Pre-mortem:  suppose it failed: most likely because a later branch-rule payload omits a pinned field.
Starts unless you say stop.
```

## Build sequence

1. In `tests/test_repo_settings.py`, make `_queue_rule` match the active branch-rules payload measured on 2026-11-22 at 04:47 CET: `merge_method: MERGE`, `max_entries_to_build: 1`, `max_entries_to_merge: 1`, `min_entries_to_merge: 1`, `grouping_strategy: ALLGREEN`, `check_response_timeout_minutes: 60`, `min_entries_to_merge_wait_minutes: 0`, and its ruleset origin. The branch-rules response, not ruleset detail, supplies the pin; retain details for bypass checks.
2. Require exact string and integer types and values for the four pinned fields; `True` is not integer 1. Use only qualifying queues as freshness suppliers and as queue-derived bypass suppliers, retaining suppliers for all other rules. An invalid queue cannot negate a valid strict rule or another qualifying queue. If no alternative qualifies, diagnose every missing field (including a missing or non-object parameters value) with `not measured:` and diagnose wrong values or types with field, expected and found; do not give network/login advice for a missing field alone.
3. Display each observed queue's three unpinned parameters during the live writer-side check, marking absent fields explicitly, without adding findings or repeating the API read. Make the existing live test provide a reporting callback to `measure` and write through pytest's terminal reporter so the report is visible under the existing `-q -rs` invocation; the offline path can inject a callback for testing. Do not print on the offline suite's default path.
4. Add parametrised planted-fault tests for each field and type, missing parameters, invalid queues beside each valid alternative, multiple suppliers and bypass, and the reporting callback. Exercise `measure` with stubbed branch-rules and ruleset-detail answers as well as `ruleset_findings`; verify failures name the field and expected/found values and missing fields do not trigger misleading login advice.

## Files and limits

- `tests/test_repo_settings.py`: implement the pin, measured fixture, diagnostics and regressions.
- `plans/changes/pin-merge-queue/spec.md`, `plans/changes/pin-merge-queue/plan.md` and `plans/changes/pin-merge-queue/findings.md`: retain the specification and plan and record review and runner evidence as the change proceeds.
- `plans/INDEX.md`: regenerate the registry through `python3 scripts/plans_registry.py --index` when the orchestrator updates artifact headers or status.

No files are deleted. The bounded change needs no design or ADR. The gate configuration, governance, merge procedure, templates and GitHub settings are untouched; no held path is assigned to the implementation attempt.

## Verification

```sh
python3 -m pytest tests/test_repo_settings.py -q -rs
make verify
```

## Criterion ledger

- 1: tests/test_repo_settings.py::test_merge_queue_supplies_freshness — the measured valid queue is rejected with the strict flag off.
- 2: not yet written tests/test_repo_settings.py::test_queue_rejects_drifted_pinned_parameters — a wrong value or type for any pinned field supplies freshness.
- 3: not yet written tests/test_repo_settings.py::test_queue_reports_missing_pinned_parameters — a missing pinned field passes or lacks a named `not measured:` finding.
- 4: not yet written tests/test_repo_settings.py::test_queue_ignores_unpinned_parameters — a changed or absent unpinned field rejects an otherwise valid queue.
- 5: tests/test_repo_settings.py::test_todays_ruleset_holds — a valid strict-only ruleset is rejected.
- 6: tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass — a bypass or unreadable supplier passes.
- 6: tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements — a missing floor rule or unpinned check passes.
- 7: not yet written tests/test_repo_settings.py::test_queue_fixture_uses_measured_parameters — a measured field is missing or has the wrong value, or an old invented name remains.
- 8: not yet written tests/test_repo_settings.py::test_invalid_queue_does_not_supply_bypass_measurement — an otherwise non-supplying invalid queue causes a ruleset detail read or bypass finding.
- 9: not yet written tests/test_repo_settings.py::test_queue_drift_finding_names_expected_and_found — the drift finding omits the field or either value.
- 10: not yet written tests/test_repo_settings.py::test_strict_rule_survives_invalid_queue — a wrong or absent field makes valid strict freshness fail.
- 11: not yet written tests/test_repo_settings.py::test_valid_queue_survives_invalid_queue — a wrong or absent field makes another valid queue fail.
- 12: not yet written tests/test_repo_settings.py::test_live_queue_report_shows_unpinned_parameters — the live report omits a value or absent marker, or changes the findings.

## Time used

2026-11-22 03:41:49–03:44:25 UTC, 156 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-22 03:48:54–03:51:19 UTC, 145 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
