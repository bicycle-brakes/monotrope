---
title: "Plan — swarm-time-limits"
status: draft
implementation_status: none
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-ht1b
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, research-swarm, time-limits]
---

# Plan — swarm-time-limits

```text
For you:     Adjust research-swarm role and run limits in one checked-in file; finders start with 20 minutes and the run with 160.
Done when:   Configuration edits govern the next run, invalid settings refuse before research calls, deadline and reserve tests pass, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Other runner limits, live reload, routing, retries or admission changes.
Pre-mortem:  suppose it failed: most likely because one deadline or judge reserve still reads an old constant.
Starts unless you say stop.
```

Implements `spec.md` from baseline `0776b3a6`, inspected 2026-11-04. Bounded:
no design phase or ADR. No `templates/plan.md` exists; the card and ledger
follow `prompts/03-plan.md`. Explore ran through Stage 2, GLM 5.3 Flash via
`glm-coding-plan` on 2026-11-04; no Stage-1 fallback was recorded.

## Files and steps

1. Create `tests/test_stage2_research_limits.py` for the loader contract and
   checked-in starting values, and add the ledger's integration tests to
   `tests/test_stage2_swarm.py`; obtain red-first evidence before production
   edits. Use temporary roots, synthetic files, injected clocks and the
   existing stand-ins; no model endpoint or minute-long sleep. Demonstrate
   an assertion failure when the baseline ignores a planted finder/run
   configuration edit; an absent-loader import error is not that evidence.
2. Create `research-swarm-limits.yaml` with the following entire data schema,
   plus brief comments explaining minutes and validity:

   ```yaml
   run_minutes: 160
   role_minutes:
     finders: 20
     merge: 10
     sentence: 5
     topics: 10
     judge: 15
   ```

3. Create `scripts/stage2_research_limits.py`: a small reader taking the
   supplied repository root, using the existing PyYAML dependency with safe
   loading and duplicate-key rejection. Return validated instance-owned
   settings, or a dedicated error identifying the configuration path and
   failing field/reason. Enforce the exact schema, positive finite numeric
   values excluding bool/string, finite seconds conversion, roles <= run and
   judge < run. Handle read/decode/YAML/type/overflow errors as refusals,
   never defaults; valid fractional minutes must work. No module-global
   configuration cache or second source of default values.
4. Change `scripts/stage2_research_run.py`: load once at the beginning of
   `Run.open`, translating loader errors to `runner.Refused` before
   preflight, credentials, state-store setup or participant dispatch. Remove
   the old `MINUTES`/`RUN_MINUTES` value declarations. Use the instance's run
   value in `deadline`, role values in `run_stage`, and judge value in all
   four pre-judge reserve call sites (finders, merge, sentence, topics).
   Preserve `self.began`, monotonic timing and the judge's zero reserve;
   every resumed invocation constructs a new Run and reloads settings.
   Keep the existing snapshot, reuse and dispatcher interfaces unchanged.
5. Adapt `tests/test_stage2_swarm.py`: copy the new configuration into the
   shared `sworld` fixture before its initial commit. Replace hard-coded
   old-value assertions in `test_amended_graph_and_deadlines_bound_every_launch`
   with checks of the loaded configuration, preserving the invocation-budget
   and no-retry assertions. Derive clock jumps in the reserve and exhausted
   deadline tests from fixture settings rather than 140/151 minutes. Replace
   the two `MINUTES["topics"]` monkeypatches (partial-output/receipt tests)
   with temporary configuration edits before a run. Preserve their failure
   scenarios and the existing foreign-edit/reuse protections.
6. In the new tests, parameterize missing/unreadable files, bad UTF-8/YAML,
   non-mappings, missing/unknown/duplicate keys at both mapping levels,
   bool/string/null/container values, zero, negative, NaN/infinity, seconds
   overflow and impossible role/run relationships. Check refusal through
   real `explore` with a synthetic consumed receipt and an empty call log.
   Spy on real stage dispatch with distinct valid values to assert every
   role, shared deadline and reserve, including a free topic and judge;
   edit the file between stages to prove in-flight consistency. Exercise
   another root and another invocation to prove current settings are reread.
   For resume, retain an incomplete run and advance the injected clock
   beyond its old deadline: the next Run gets its full configured allowance
   while unchanged exact-binding reuse rules still apply.
7. Change `docs/WORKFLOW.md` to document the file, minute units, schema,
   refusal rules and next-invocation application; replace its 150-minute
   statement with the configured total, initially 160, and configured judge
   reserve, initially 15. Change `plans/changes/research-swarm/spec.md` only
   where its current deadline description states 150, finder 10, or a fixed
   judge reserve (criterion 19 and the deadline detail): identify the new
   source, finder 20/run 160, and configured judge reserve without weakening
   finite deadlines, required-first order or no retries. Historical decisions
   stay intact. Review both texts against the new configuration contract.
8. Update this `plan.md` to turn implemented ledger entries into test entries
   and record phase-4 evidence/time. The runner owns this change's
   `findings.md`, generated `plans/INDEX.md`, verification and commit. Two
   further files were not foreseen and the orchestrator accepted them by hand
   at `2a50c714` because the gates demanded them: `scripts/ci_gates.py` (a
   new `OHNE_AUFRUFER` entry declaring that `scripts/stage2_research_limits.py`
   has no caller outside its importer) and `scripts/kit/manifest.yaml` (a
   role rule for `research-swarm-limits.yaml`). No other implementation
   file is added, changed or deleted.

## Criterion ledger

- 1: tests/test_stage2_research_limits.py::test_checked_in_limits_have_decided_values — a configured role/run value or minute conversion differs from the interview.
- 2: tests/test_stage2_swarm.py::test_research_limits_are_captured_once_per_invocation — a mid-run edit changes that run or the next invocation ignores it.
- 2: tests/test_stage2_research_limits.py::test_each_root_reads_its_current_limits — another root or a prior read supplies stale values after a valid edit.
- 3: tests/test_stage2_research_limits.py::test_limits_reject_unusable_documents — missing, unreadable, malformed, ambiguous or incomplete data produces usable settings.
- 3: tests/test_stage2_research_limits.py::test_limits_reject_implausible_values — non-numeric, non-positive, non-finite, overflowing or impossible budgets are accepted.
- 3: tests/test_stage2_swarm.py::test_invalid_limits_refuse_before_research_launch — explore launches a participant, exits other than 2, or omits the path and reason.
- 4: tests/test_stage2_research_limits.py::test_valid_limits_accept_fractional_minutes — valid fractional minutes are refused or converted incorrectly.
- 4: tests/test_stage2_swarm.py::test_configured_limits_reach_every_research_stage — any dispatched role uses a constant, wrong role or wrong units.
- 5: tests/test_stage2_swarm.py::test_configured_run_limit_controls_deadline — stages receive different deadlines or retain 150 minutes instead of the configured monotonic total.
- 5: tests/test_stage2_swarm.py::test_resumed_run_uses_a_fresh_configured_deadline — the resumed invocation inherits the old spent deadline or loses its configured allowance.
- 5: tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent — an exhausted run starts a participant or omits not-started outcomes.
- 6: tests/test_stage2_swarm.py::test_research_judge_reserve_uses_configured_limit — a pre-judge stage reserves another value or the judge reserves its allowance twice.
- 6: tests/test_stage2_research_dispatch.py::test_child_allowance_is_lesser_of_role_and_remaining_before_reserve — a child receives more than its role or unreserved remainder.
- 6: tests/test_stage2_research_dispatch.py::test_no_launch_inside_reserve_and_free_not_started_is_not_incomplete — a slot launches inside the reserve or a missing free slot incorrectly fails the run.
- 6: tests/test_stage2_swarm.py::test_required_slots_precede_free_and_reserve_judge_time — required topics consume the reserved time or unlaunched slots lose their outcomes.

## Verification and boundaries

The orchestrator ensures the pinned environment and Pi prerequisites are
installed before phase 4. Run the focused checks verbatim, then the runner's
full gate:

```bash
.venv/bin/python -m pytest -q tests/test_stage2_research_limits.py tests/test_stage2_swarm.py tests/test_stage2_research_dispatch.py tests/test_stage2_research_deep_review.py
make verify
```

Do not edit `scripts/stage2.py`, `scripts/stage2_availability.py`,
`scripts/stage2_research_dispatch.py`, `model-endpoints.yaml`, gate declarations,
provenance, held prompts/templates/instructions, ADRs or dependency files.
No held-path bootstrap edit is needed. The two documentation edits are ordinary
allowed paths, not orchestrator-held configuration. Stop at the two-hour
appetite with unmet criteria recorded; never weaken a criterion to pass.
`scripts/validate_change_artefacts.py` is absent at the inspected baseline:
it cannot be reported green. The runner handles index generation and
tracker-dependent gates, which this draft does not mutate.

## Verification record

Attempts 1 to 3 ended red (ruff, a pytest cheap check, then three gate tests:
`test_every_tracked_file_has_a_role`, `test_the_role_check_goes_red_when_a_rule_is_removed`
and `test_every_script_has_a_caller_or_a_declared_reason`). The orchestrator
fixed those by hand in the two files named in step 8 and recorded a full
`make verify` green on `2a50c714` (2026-11-04). Later repair rounds (review
rows L1-1 to L1-11) edit docs, the limits loader, the run's constructor and
tests; their gate is the runner's own `make verify` after the repair.

Review loop, 2026-11-04/05 (the rows live outside the repository until the
phase-6 verdict, then in `findings.md`): round 1 eleven rows, repaired and
accepted by hand (2e2ba948); round 2 four rows, L2-4 repaired by the runner
(63a53261); round 3 four rows, three repaired and accepted by hand after the
midnight date-stamp rollover (7aac74ea); round 4 three rows. Each hand
acceptance followed a full `make verify` and is named in its commit.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-04

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-11-04

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-04 11:36:56–12:18:41 UTC, 2504 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 12:18:50–12:28:23 UTC, 573 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 12:28:32–12:48:37 UTC, 1205 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 14:00:20–14:30:02 UTC, 1781 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-04 14:30:10–14:51:48 UTC, 1298 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-04 14:51:57–15:15:13 UTC, 1396 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 16:14:37–16:43:11 UTC, 1714 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-04 17:12:32–18:29:38 UTC, 4625 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-04 18:29:51–18:51:48 UTC, 1316 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-04 18:51:59–22:00:40 UTC, 11320 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
