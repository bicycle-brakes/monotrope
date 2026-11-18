---
title: "Plan — slip-counter"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-18
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, run-log]
---

# Plan — slip-counter

```text
For you:     Read slips, flaky-test signals, incomplete runs and runs outside the count from the local verification history.
Done when:   Immediate matching runs count correctly, gaps and excluded runs stay visible, the real runner pairing is proved, and make verify is green.
Appetite:    6 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Slip records, unique-defect counts, CI/nightly collection, test tiers or changes to verification policy.
Pre-mortem:  suppose it failed: most likely because the recorded targeted tree cannot be matched to the later full check.
Starts unless you say stop.
```

## Build sequence

1. Attempt: update `scripts/verify_duration.py` to derive the counts and diagnose
   uncertainty under the contracts below. Update `scripts/stage2.py` only where
   the targeted repair and named full runs record comparison evidence.
2. Attempt: update `tests/test_verify_duration.py` for immediate succession,
   pair validity, scopes, outside counts and old-reader compatibility; update
   `tests/test_stage2.py` and `tests/test_ci.py` for the real runner evidence
   path. Use isolated state roots and the production writer and reader.
3. Attempt: update `docs/WORKFLOW.md`, `docs/orchestration.md` and
   `plans/specs/implementation-verification/spec.md` to describe the counts and
   boundaries. Update this change's `spec.md`, `plan.md` and `findings.md` as
   the workflow requires. The runner regenerates `plans/INDEX.md` after header edits.
4. Orchestrator: assign any newly needed held-path edit as a bootstrap edit
   after an accepted attempt; no such edit is currently planned. Do not alter
   `scripts/verify_all.sh`, admission, check selection or `scripts/stage2_runs.py`.

## Evidence and reader contracts

- Keep the existing version-1 run history with additive optional comparison
  fields; prove older duration readers accept the added fields. Capture the
  resolved common Git directory, change, check kind, checked tree and SHA-256
  of `decisions/gates.yaml` at start, plus actual outcome and completion time.
  Targeted repair checks capture their tree at both ends; the full run captures
  it only at start, as the spec's Boundary states. The runner passes the named
  change to the existing full-start path; a successful normal run with available
  context must not substitute unknowns. Never write a slip or signal record.
- Group identical events and validate every in-scope run once. Order completed
  checks by UTC completion with strict earlier-than; equal timestamps cannot
  establish succession. For each identity, any intervening completed check ends
  the previous opportunity. A red full run immediately following a green
  targeted repair check counts once; full green immediately followed by full
  red counts once as a separate signal. Search history before the lower bound
  for predecessors; select counted runs by their own start time.
- Apply the spec's potential-pair rule before declaring a non-slip: compatible
  known fields and possible order leave candidates even when evidence is
  incomplete. Mark each selected affected run incomplete once; incompatible
  known fields cannot pair, and ambiguity does not pick an arbitrary candidate.
  Diagnose unassignable evidence separately and mark the report partial. Treat a
  start without an end as incomplete, including an active run.
- The reader `python3 -m scripts.verify_duration slips [--since UTC] [--until UTC] [--change NAME]`
  defaults to the current shared Git repository and all time. Bounds are aware
  UTC instants, lower inclusive and upper exclusive; reject reversed bounds.
  Show scope, slips, incomplete runs, flaky-test signals and an outside-count
  line for attributable legacy or change-less full runs. Recognizable legacy runs without scope evidence appear separately as
  unattributed outside runs and do not make the slip measurement partial. A missing history or
  empty selection is not a measured zero. Exit 0 for complete evidence, 1 for
  partial or unavailable evidence, 2 for invalid arguments or refused storage.
  Read without changing history; append failures never change a check verdict.
- Phase 1 used Stage 2, route `flash`, model `glm-5.3-flash`; no Stage-1
  Explore fallback was recorded. The later implementation fallback was Sonnet
  5.5 after two Flash post-run failures (2026-11-14). No design or ADR is due
  for the bounded class. The targeted-check scope is repair only in this change;
  broader partial checks are follow-up work (bead coding-harness-l0g6).

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_verify_duration.py -q
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'slip or targeted or review_requires_fresh_full_verification_before_model_call'
.venv/bin/python3 -m ruff check scripts/verify_duration.py scripts/stage2.py tests/test_verify_duration.py tests/test_stage2.py
.venv/bin/python3 -m ruff format --check scripts/verify_duration.py scripts/stage2.py tests/test_verify_duration.py tests/test_stage2.py
python3 scripts/check_interview_minimums.py --change slip-counter
python3 scripts/check_research_handoff.py --change slip-counter
python3 scripts/check_criterion_ledger.py
make verify
```

These are phase-4 commands, not claims of execution during drafting. The
runner owns full verification and the commit; edits to `scripts/stage2.py`
retain full verification under the current hot-file rule. Demonstrate the
matching count and lost-end boundary with planted fixtures before and after
the fix; no real machine history or deliberately failing full suite is needed.

## Criterion ledger

- 1: tests/test_verify_duration.py::test_slips_pair_overlapping_checks_by_completion — an overlapping qualifying pair disappears
- 1: not yet written tests/test_verify_duration.py::test_slips_count_only_immediate_successor — a repeated red full run counts twice
- 2: not yet written tests/test_verify_duration.py::test_slips_intervening_check_ends_pairing — an intervening same-identity check leaves the prior green eligible
- 3: not yet written tests/test_verify_duration.py::test_slips_report_consecutive_full_flaky_signal — a full green then full red lacks its separate signal
- 4: tests/test_stage2.py::test_slip_history_captures_targeted_and_full_evidence — targeted repair evidence is missing or incomparable
- 4: tests/test_stage2.py::test_slip_history_never_records_unfinished_targeted_green — a failed or unstable check records a comparable green
- 5: tests/test_stage2.py::test_slip_history_captures_targeted_and_full_evidence — a named full run loses available comparison context
- 6: tests/test_verify_duration.py::test_slips_show_incomplete_runs_beside_count — interrupted or conflicting evidence disappears or counts twice
- 6: tests/test_verify_duration.py::test_slips_reject_unstable_red_targeted_run — an unstable red check counts as valid
- 7: not yet written tests/test_verify_duration.py::test_slips_incomplete_candidate_marks_both_sides — a complete full run with an incomplete possible predecessor is a non-slip
- 8: tests/test_verify_duration.py::test_slips_select_interval_repository_and_change — selection leaks or a predecessor before the interval is lost
- 9: not yet written tests/test_verify_duration.py::test_slips_report_legacy_and_changeless_outside_count — an excluded run becomes incomplete or vanishes from the outside line
- 10: tests/test_verify_duration.py::test_slips_distinguish_complete_partial_and_unavailable_history — damaged or missing history appears complete
- 11: tests/test_verify_duration.py::test_slips_are_read_only_and_preserve_duration_history — reading mutates history or legacy durations fail
- 11: tests/test_stage2.py::test_slip_measurement_failure_preserves_verification_result — an append failure changes the verdict
- 11: not yet written tests/test_verify_duration.py::test_old_duration_reader_accepts_additive_version_one_fields — an older reader rejects new records

## Time used

2026-11-14 17:00:12–17:56:17 UTC, 3365 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-14 17:56:26–18:24:20 UTC, 1674 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-14 18:24:27–18:25:36 UTC, 69 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-15 14:23:20–15:31:37 UTC, 4097 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_verify_cheap_first.py`, `tests/test_verify_duration.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-15 18:37:59–20:52:43 UTC, 8084 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_verify_cheap_first.py`, `tests/test_verify_duration.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-16 16:35:53–16:37:34 UTC, 100 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 16:49:00–16:50:04 UTC, 64 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-16 16:50:35–17:05:39 UTC, 904 s — repair · attempt 1 · route codex · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_verify_cheap_first.py`, `tests/test_verify_duration.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-17 22:24:45–22:35:27 UTC, 642 s — repair · attempt 1 · route codex · model gpt-6.1-terra · rejected · measured by the runner
2026-11-17 22:35:37–22:50:18 UTC, 881 s — repair · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_verify_cheap_first.py`, `tests/test_verify_duration.py`; extra ruff targets none beyond the cheap checks; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
2026-11-18 12:49:17–12:52:26 UTC, 189 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
