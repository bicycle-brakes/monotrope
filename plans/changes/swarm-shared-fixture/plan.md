---
title: "Plan — swarm-shared-fixture"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-wnka
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, tests, swarm, performance]
---

# Plan — swarm-shared-fixture

```text
For you:     The five slowest research-swarm tests cost less in aggregate, with their existing assertions preserved.
Done when:   Individual profiles justify the edits, matched medians improve, coverage stays effective, and make verify is green.
Appetite:    3 hours of phase 4, measurement and repairs included; a stop, not an estimate.
Not now:     Shared fixture worlds, production changes, test consolidation or verification-gate changes.
Pre-mortem:  suppose it failed: most likely because a shortcut removes the production behaviour an assertion needs to exercise.
Starts unless you say stop.
```

Baseline inspected: `2c16bd4e992b2febf1c020e74f886976043c0dd4`, 2026-11-14.
Follow `spec.md` and the maintainer's measured-test-body re-scope. Bounded:
no design or ADR. No `templates/plan.md` exists; use the phase-3 prompt's form.
Explore: Stage 2, `glm-5.3-flash`, endpoint `glm-coding-plan`, 2026-11-13;
no Stage-1 fallback was recorded.

## Files and steps

1. Before executable edits, save the baseline collected node IDs for the
   swarm module and its two importing consumers to temporary files. Run the
   baseline command below with the machine's verification admission. Select
   the five slowest call-phase node IDs; break ties by node ID. Record the
   selection here, separately from setup and teardown durations. Historical
   names and the 2026-11-13 six-worker totals are context, not this baseline.
2. Measure each selected node alone three times without a profiler; then
   profile each once using the commands below. Record elapsed times, call
   counts and cumulative costs separately. Identify repeated work within
   test bodies, including declaration reads, leak-scan subprocesses and
   stand-in launches. Do not choose a cache or a mock from the old profile.
3. Change only `tests/test_stage2_swarm.py`: optimise the first measured
   repeated operation that can be shared or avoided without losing an
   existing fault detector. Keep the function-scoped `sworld`, test names,
   parameter cases, assertions and importable helpers compatible. Prefer
   reusing immutable test-input construction and repeated test-side report
   preparation; any reuse must be local to one test and keyed by every input
   it depends on. Never cache a final verdict or substitute an asserted
   production result. Keep real subprocesses, scans, clocks and fresh reads
   for cases whose assertions depend on them; use no autouse or global
   acceleration patch. Record the measured hotspot, exact edited functions,
   reuse lifetime and preserved fault path here before the edit is accepted.
   If the profile offers no safe test-only saving, stop with the evidence;
   do not implement a speculative optimisation or declare the change done.
4. Exercise each edited case and demonstrate that its original stated fault
   still makes an assertion fail, using temporary reversible mutations and
   recording the command and failure. If a reusable helper is introduced,
   add focused tests in the same module for changed inputs, mutation isolation
   and teardown; add their exact names to the ledger before acceptance.
   Run the module and both importing consumers together; also run edited
   nodes individually and in reverse order to expose leaked state.
5. Repeat three unprofiled individual runs per fixed target, using the same
   interpreter, dependencies, input and worker settings without competing
   verification. Record both revisions, dates, load conditions, raw results,
   each median and their sums here. If conditions drift, repeat both sides;
   an equal or slower after total is an unmet criterion, not a passing claim.
   Compare collected baseline node IDs and review assertions/production paths.
6. Update `plans/changes/swarm-shared-fixture/plan.md` with evidence, new test
   ledger entries when applicable and measured phase-4 time. The orchestrator
   maintains `plans/changes/swarm-shared-fixture/spec.md` status and the runner
   maintains `plans/changes/swarm-shared-fixture/findings.md`; neither invents
   evidence. The orchestrator regenerates `plans/INDEX.md` after the accepted
   attempt. No other file is created, changed or deleted by implementation;
   no held-path edit is assigned to the implementation attempt.

## Verification commands

Use the locked `.venv`; temporary logs/profiles are not committed. Set
`swarm_node` to each complete selected node ID and `swarm_profile` to a unique
temporary profile path before these per-node commands; retain their expanded
values in the evidence. Run both revisions with the same commands.

```sh
.venv/bin/python3 -m scripts.verify_lock -- .venv/bin/python3 -m pytest tests/test_stage2_swarm.py -q -p no:xdist --durations=0
/usr/bin/time -p .venv/bin/python3 -m scripts.verify_lock -- .venv/bin/python3 -m pytest "$swarm_node" -q -p no:xdist --durations=0
.venv/bin/python3 -m scripts.verify_lock -- .venv/bin/python3 -m cProfile -o "$swarm_profile" -m pytest "$swarm_node" -q -p no:xdist
.venv/bin/python3 -m scripts.verify_lock -- .venv/bin/python3 -m pytest tests/test_stage2_swarm.py tests/test_stage2_research_deep_review.py tests/test_stage2_terms_expiry.py -q -p no:xdist
.venv/bin/python3 scripts/check_interview_minimums.py --change swarm-shared-fixture
.venv/bin/python3 scripts/check_research_handoff.py --change swarm-shared-fixture
.venv/bin/python3 scripts/check_criterion_ledger.py
PYTEST_ADDOPTS=--durations=50 /usr/bin/time -p make verify
```

Use pytest's elapsed result for criterion 2; the outer time includes admission
wait and is recorded separately. Full verify is runner-owned. The advertised
`scripts/validate_change_artefacts.py` is absent at the inspected baseline and
cannot be reported green. Do not edit other tests, production, declarations,
gates, dependencies, held paths or neighbouring ledgers to obtain a pass.

## Criterion ledger

- 1: not a test — dated baseline selection and five individual profiles in this plan; refuted by a missing profile or an edit unrelated to its hotspot.
- 2: not a test — three successful unprofiled runs per target per revision, with matched conditions and a lower sum of medians; refuted by missing/mismatched runs or a non-decreasing sum.
- 3: not a test — before/after collected-node comparison and assertion/path review, plus a failing original fault for each edited case; refuted by a missing case, weaker assertion or a fault that now passes.
- 4: tests/test_stage2_swarm.py::test_a_leak_in_the_first_prompt_starts_no_model — a planted leak reaches a model.
- 4: tests/test_stage2_swarm.py::test_leak_block_cancels_queued_dispatch — queued work starts after a leak BLOCK.
- 4: tests/test_stage2_swarm.py::test_launch_record_keeps_individual_leak_check_before_launch — a launch lacks its own prior check.
- 4: tests/test_stage2_swarm.py::test_swarm_uses_only_the_injected_pi_wrapper — a launch bypasses the pinned stand-in.
- 4: tests/test_stage2_swarm.py::test_the_next_run_uses_its_own_frozen_free_selection — the next run inherits the old selection.
- 4: tests/test_stage2_terms_expiry.py::test_research_probes_and_dispatch_recheck_expiry — a launch ignores expiry, including expiry during scanning.
- 4: not a test — individual, combined and reverse-order edited-node runs plus review of reused mutable inputs; refuted by order-dependent state or a bypassed asserted boundary.
- 5: not a test — make verify and the implementation diff; refuted by a red run or an executable edit outside the one allowed test file.

## Time used
