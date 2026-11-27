---
title: "Plan — research-seat-substitute"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-0ysc
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, research-swarm]
---

# Plan — research-seat-substitute

```text
For you:     A required research seat can recover from a model failure with one eligible substitute.
Done when:   Substitution, failure, history, resume and admission checks pass and make verify is green.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Finder limits, model policy changes and a promised completion-rate increase.
Pre-mortem:  suppose it failed: most likely because resume launches a second substitute for a completed seat.
Starts unless you say stop.
```

**Blocked before implementation:** the open decision in `spec.md` must be answered and incorporated, the spec review must settle its rows, and the existing ADR edit must meet the five-answer interview gate. The existing bounded skip does not supply those five answers. Do not manufacture answers or edit the ADR under an unclaimed path. This plan is provisional until those gates are met.

This bounded change has no design phase. Explore used the Stage-1 route with `claude-haiku-5-5`, because GLM via Z.ai had reached its weekly limit until 2026-11-29. No `templates/plan.md` exists at commit `3a5a1011`; this follows the phase-3 prompt.

## Files and steps

1. Change `scripts/stage2_availability.py` to retain ordered, class-admitted and actually probed reachable candidates in the frozen preparation receipt, without treating an unprobed model as reachable. Preserve uniqueness and existing chosen-seat rules.
2. Change `scripts/stage2_research_run.py` to dispatch at most one substitute for a failed required logical seat through the existing launch, admission, validation, time-limit and leak-check paths; carry the original failure and substitute identity through finder and topic results, including the resolved correction policy. Preserve successful results and judge inputs.
3. Change `scripts/stage2_research_store.py` and `scripts/stage2_research_history.py` as needed to persist and validate the original and substitute attempts and safely reuse them after interruption; keep the logical seat distinct from its attempts. Change `scripts/stage2_research_report.py` and `scripts/stage2_research_judge.py` as needed to expose the final logical outcome and history without counting attempts as additional seats.
4. Add `tests/test_stage2_research_substitute.py` covering the criterion ledger, concurrent failures, preparation reachability, correction ordering after the decision, exhaustion, interrupted resumes and the existing call and judge bounds. Update `tests/test_stage2_research_availability.py`, `tests/test_stage2_research_store.py`, `tests/test_stage2_research_history.py`, `tests/test_stage2_research_report.py`, `tests/test_stage2_research_judge.py` and `tests/test_stage2_swarm.py` where their frozen-selection or history expectations change.
5. The orchestrator edits held path `docs/adr/0020-phase-1-research-swarm.md` after the accepted implementation, once the required maintainer records exist, to reconcile substitution and call ceilings; it updates `docs/WORKFLOW.md` to match. Update this plan's ledger as tests land and record phase-4 time; the runner owns findings, index, full verification and commit.

## Criterion ledger

- 1: not yet written tests/test_stage2_research_substitute.py::test_only_one_substitute_per_failed_seat — a second substitute launches.
- 2: not yet written tests/test_stage2_research_substitute.py::test_eligible_substitute_is_dispatched — a qualifying failure remains untried with time and a candidate.
- 3: not yet written tests/test_stage2_research_substitute.py::test_substitute_is_next_reachable_admitted_for_trio — selection crosses a class or trio boundary or skips an earlier eligible candidate.
- 4: not yet written tests/test_stage2_research_substitute.py::test_valid_substitute_supplies_logical_result — the judge does not receive the valid result.
- 5: not yet written tests/test_stage2_research_substitute.py::test_failed_substitute_leaves_run_incomplete — the run completes with a failed required seat.
- 6: not yet written tests/test_stage2_research_substitute.py::test_history_records_substitute_and_failure_reason — either field is absent.
- 7: not yet written tests/test_stage2_research_substitute.py::test_resume_validates_substitute_before_reuse — resume accepts a mismatch or repeats a completed substitute.
- 8: not yet written tests/test_stage2_research_substitute.py::test_exhausted_candidates_or_deadline_stops_seat — the reason is missing or a forbidden call starts.
- 9: not yet written tests/test_stage2_research_substitute.py::test_substitute_respects_admission_and_leak_checks — a rejected call is sent.

## Verification and boundaries

```bash
.venv/bin/python -m pytest tests/test_stage2_research_substitute.py tests/test_stage2_research_availability.py tests/test_stage2_research_store.py tests/test_stage2_research_history.py tests/test_stage2_research_report.py tests/test_stage2_research_judge.py tests/test_stage2_swarm.py -q
python3 scripts/jobs.py start -- make verify
```

Do not change finder limits, model terms, customer material or admission policy. Do not launch implementation until the blocker above is resolved. The orchestrator owns held paths; no other files are planned.

## Time used

2026-11-27 23:01:37–23:04:15 UTC, 158 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
