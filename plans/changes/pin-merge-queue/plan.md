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
Done when:   Tests reject drift and missing fields, preserve the strict alternative and bypass checks, and make verify passes.
Appetite:    Two hours of phase 4 including repairs; stop at the limit.
Not now:     Changing GitHub settings, merge procedures, other queue parameters or governance rules.
Pre-mortem:  suppose it failed: most likely because the live branch-rule payload differs from the measured ruleset detail.
Starts unless you say stop.
```

## Build sequence

1. In `tests/test_repo_settings.py`, replace the queue fixture's unmeasured names with `merge_method: MERGE`, `max_entries_to_build: 1`, `max_entries_to_merge: 1` and `min_entries_to_merge: 1`, preserving the measured optional fields. The measurement in `decisions.md` is from ruleset detail, not the branch-rules endpoint: check which endpoint supplies these fields before relying on the fixture; if the branch rule omits them, use the already-read supplying ruleset detail and fail closed when it cannot supply them. Do not change live settings.
2. Make the queue freshness predicate require all four values with exact types (a boolean is not an integer for this purpose). Keep the strict up-to-date alternative and the existing supplier bypass measurement; do not let a malformed queue hide another qualifying queue or a valid strict rule. If no freshness alternative qualifies, report missing field names, including for missing or non-object `parameters`.
3. Add parametrised planted-fault tests covering each pinned field independently, wrong types and absent fields, a measured valid queue, unpinned-parameter changes, multiple queues, strict-only fallback, and supplier bypass and floor failures. Exercise the full `measure` path with stubbed API answers as well as the predicate so a mismatch between endpoint shapes cannot silently pass; retain the existing offline tests.

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
- 3: not yet written tests/test_repo_settings.py::test_queue_reports_missing_pinned_parameters — an absent field passes or its name is not reported.
- 4: not yet written tests/test_repo_settings.py::test_queue_ignores_unpinned_parameters — a changed or absent unpinned field rejects an otherwise valid queue.
- 5: tests/test_repo_settings.py::test_todays_ruleset_holds — a valid strict-only ruleset is rejected.
- 6: tests/test_repo_settings.py::test_queue_supplier_is_measured_without_bypass — a bypass or unreadable supplier passes.
- 6: tests/test_repo_settings.py::test_queue_preserves_the_other_ruleset_requirements — a missing floor rule or unpinned check passes.
- 7: not yet written tests/test_repo_settings.py::test_queue_fixture_uses_measured_parameters — a measured field is missing or has the wrong value, or an old invented name remains.

## Time used

2026-11-22 03:41:49–03:44:25 UTC, 156 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
