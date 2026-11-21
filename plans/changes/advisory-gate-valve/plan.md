---
title: "Plan — advisory-gate-valve"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-73gi.4
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, gates, valves]
---

# Plan — advisory-gate-valve

```text
For you:     Every non-blocking gate has a dated review point and a tracking item; an expired date is visible without blocking verification.
Done when:   Schema tests reject missing or malformed valves and numeric counts, report expiry without failing, and make verify is green.
Appetite:    4 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Automatically changing enforcement, blocking on expiry, or repairing the documentation corpus.
Pre-mortem:  suppose it failed: most likely because a gate receives a tracking item that does not actually own its review.
Starts unless you say stop.
```

## Build sequence and files

1. **Attempt — schema and output.** Change `scripts/ci_gates.py`: validate each non-blocking valve mapping, its real ISO calendar date and repository bead identifier (`coding-harness-` followed by an alphanumeric item and optional dot-separated numeric child levels), and count-free reasons; retain the valve in normalized gate records. Expose expired valves as diagnostics in `--check-schema` without adding them to schema errors, using the current date and treating `until` as inclusive. Keep other commands' formats, gate scheduling and generated workflow behavior intact, and retain the validated snapshot when reporting without rereading a vanished file. Increase the declared schema version consistently in the reader and gate file for the new required field.
2. **Attempt — evidence.** Change `tests/test_gate_machinery.py` with isolated fixtures for both enforcement levels, missing and wrong types, impossible dates, malformed bead identifiers, numeric counts, identifiers and ISO dates in reasons, expiry versus today and future, and ordinary blocking gates. Exercise `--check-schema` output and exit status, not only a helper; seed faults so each new rejection or missing warning turns a test red. Adjust the affected non-blocking fixture in that file to satisfy the new schema.
3. **Attempt — compatibility.** Change `tests/test_ci.py`, `tests/test_verify_cheap_first.py`, `tests/test_verify_before_admission.py` and `tests/test_stage2.py` to migrate schema-version literals and affected synthetic non-blocking gate fixtures; preserve their original fault assertions and retain the existing hosted and local non-blocking behavior tests. Change `tests/test_gate_catalog.py` to retain the catalog's independent comparison, fixtures and documentation checks.
4. **Orchestrator bootstrap after the accepted attempt — held path.** Change `decisions/gates.yaml`: update the schema comment and version; give `docs-links`, `markdownlint`, `lychee` and `research-currency` valves with proposed `until: "2026-12-19"`, remove counts from their reasons without altering their meaning or translating unrelated German, and retain `coding-harness-bt8` for `docs-links`. Identify an evidenced tracking item for each remaining gate; do not fabricate one or claim a planned flip for a deliberately permanent report. If an appropriate item cannot be established, hand that gap to the tracker-owning orchestrator before finalizing the decision pull request. Dates and any governance changes remain proposals for the maintainer's merge.
5. **Attempt and orchestrator — catalog.** Change `docs/governance/gate-catalog.md` to explain both valve fields and the warning-only expired date. After the held gate-file edit the orchestrator regenerates its marked inventory using `python3 scripts/ci_gates.py --catalog`. The existing generated workflow `.github/workflows/ci.yml` is held: the orchestrator regenerates it only if `python3 scripts/ci_gates.py --generate-ci` differs, never by hand. The runner regenerates `plans/INDEX.md` from the change headers; never hand-edit it.

Do not edit `scripts/verify_run.py`, `scripts/ramp_valves.py`, `scripts/_verdict.py`, tracker data or unrelated governance text. A `bounded` change has no design phase or ADR. The pre-existing Stage-2 explore used GLM 5.3 Flash; it was not a Stage-1 fallback.

## Verification

Before the held-path edit, use isolated schema fixtures for the attempt's targeted tests: the checked-in gate list cannot pass the new schema until that edit. After the orchestrator's held-path edit, run:

```sh
python3 scripts/ci_gates.py --check-schema
python3 -m pytest tests/test_gate_machinery.py tests/test_gate_catalog.py tests/test_ci.py tests/test_verify_cheap_first.py tests/test_verify_before_admission.py tests/test_stage2.py -q
make verify
```

## Criterion ledger

- 1: not yet written tests/test_gate_machinery.py::test_nonblocking_gate_requires_valve_mapping — a missing or non-mapping valve passes.
- 2: not yet written tests/test_gate_machinery.py::test_nonblocking_valve_requires_calendar_date — a missing, malformed or impossible date passes.
- 3: not yet written tests/test_gate_machinery.py::test_nonblocking_valve_requires_bead_id — an empty or malformed identifier passes.
- 4: not yet written tests/test_gate_machinery.py::test_nonblocking_reason_rejects_numeric_counts — a numeric count passes, or a bead identifier or ISO date is mistaken for one.
- 5: not yet written tests/test_gate_machinery.py::test_expired_valve_is_reported_without_failing_schema — expiry is silent, incomplete or exits nonzero.
- 6: not yet written tests/test_gate_machinery.py::test_current_and_future_valves_pass — a valid current or future valve is rejected.
- 7: not yet written tests/test_gate_machinery.py::test_blocking_gate_needs_no_valve — a valid blocking gate without a valve is rejected.
- 8: not yet written tests/test_gate_machinery.py::test_declared_nonblocking_gates_have_valves — a declared non-blocking gate lacks a valid valve or carries a count, or the docs-links item is lost.
- 9: not yet written tests/test_gate_catalog.py::test_valve_documentation_describes_warning_only_expiry — either schema or catalog omits a field or describes expiry as blocking.
- 10: tests/test_ci.py::test_no_blocking_gate_step_carries_continue_on_error — hosted enforcement flags drift.
- 10: not yet written tests/test_gate_machinery.py::test_valve_metadata_preserves_nonblocking_execution — local or hosted report/advisory failures become blocking.

## Time used

2026-11-21 22:44:12–22:47:33 UTC, 201 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
