---
title: "Plan — mutation-spike"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-bvy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, spike, mutation-testing]
---

# Plan — mutation-spike

```text
For you:     A dated measurement shows which generated faults the existing tests detect in two scripts.
Done when:   Both targets have recorded outcomes, reproducible counts, survivor kinds and runtime, with incomplete coverage explicit.
Appetite:    2 hours of phase 4, including setup and reporting; a stop, not an estimate.
Not now:     Test repairs, dependency-lock changes, recurring runs or a new verification gate.
Pre-mortem:  suppose it failed: most likely because mutation execution consumes the budget before both targets are measured.
Starts unless you say stop.
```

Baseline for drafting: `90ce5bff`, inspected 2026-11-06. Class `spike`: no
design or ADR. There is no plan template under `templates/`; this follows
`prompts/03-plan.md`. Explore used Stage 2, GLM 5.3 Flash through
`glm-coding-plan`; no Stage-1 fallback is recorded. The interview skip fixes
both targets and leaves existing verification unchanged.

## Files and steps

1. **Implementing attempt — prepare and baseline.** Start the phase-4 clock
   before setup. Make a disposable snapshot of one recorded source commit
   with `git archive`; never mutate this worktree or share writable source
   links. Install mutmut and the repository's test dependencies in a separate
   scratch environment using Python 3.12 or newer, recording exact versions.
   Keep temporary configuration, caches and logs outside the submitted tree.
   Read the installed tool's help to configure mutation of only the two target
   paths, one target per run. The test commands below use the scratch Python
   on PATH, from the snapshot root. Record collection counts, exit codes and
   elapsed times on unmutated source; diagnose setup failure without repairing
   source/tests, and report a blocked measurement if the baseline cannot pass.
2. **Implementing attempt — measure.** Use `tests/test_research_handoff.py`
   for `scripts/check_research_handoff.py`; use
   `tests/test_stage2_availability.py` and
   `tests/test_stage2_research_availability.py` for
   `scripts/stage2_availability.py`. Keep imported fixture/helper modules
   available, including `tests/test_stage2.py`, without selecting its full suite.
   Mutants must reach subprocess imports as well as direct imports; confirm
   the tool executes the mutated copy and retain an example mutation and result.
   Record exact tool/configuration commands, operators, selection rules and
   timeout. Pilot each target before spending the remaining time on further
   mutants; label selected functions/lines and generated/evaluated totals if
   sampling is necessary. Reserve the final 20 minutes for analysis and the
   note. Stop workers at the budget, preserving partial counts. Tool startup,
   collection and infrastructure failures are not kills; no baseline means no
   valid score. Run only fixture-based tests, never live model probes.
3. **Implementing attempt — analyse and report.** Create
   `docs/research/2026-11-06-mutation-testing-baseline.md` with normal research
   frontmatter. Include source commit/date, Python/tool/dependency versions,
   exact setup and execution commands, temporary configuration, test selection,
   machine context, per-target baseline/mutation times and total time. Give
   generated/evaluated counts and all outcome buckets; state the score formula
   and exclusions, and use “not measured” when a valid denominator is absent.
   Group survivors by mutation kind with counts and representative locations
   or IDs; if not all are inspected, count and label the remainder unreviewed.
   Separate missing assertions, suspected equivalents and tool limitations.
   Recommend a next step based on this selection alone; include reproduction
   instructions and relevant evidence excerpts so temporary logs are not the
   sole source of a claimed result. Do not repair findings in this spike.
4. **Implementing attempt — finish evidence.** Add measured time under
   `## Time used` in this `plan.md`; do not change acceptance criteria to match
   an incomplete run. Review the note against the ledger and run the whitespace
   check below. No source or test files are changed, and no files are deleted.
   The runner owns its commit and required verification; the orchestrator owns
   `plans/INDEX.md` regeneration after accepted artifacts and any tracker/PR
   bookkeeping. No held-path bootstrap edit is required for the measurement.

## Verification

Run these baseline commands in the disposable snapshot, with its scratch
environment active; configure the mutation runner to use the matching command:

```bash
python -m pytest tests/test_research_handoff.py -q
python -m pytest tests/test_stage2_availability.py tests/test_stage2_research_availability.py -q
```

In the change worktree, after writing the note:

```bash
git diff --check
```

This text-only deliverable uses CI as its gate. The one-off measurement and
evidence review hold the criteria; existing functional tests alone cannot prove
that a reported score or timing is true. No new tests mirror the report.

## Criterion ledger

- 1: not a test — phase-6 review reads the dated note for both target paths and completion states; an omitted target or concealed interruption refutes it.
- 2: not a test — reproduce the recorded setup from the named commit; missing versions, commands, scope or configuration refute it.
- 3: not a test — retained baseline output shows the selected unmutated tests passing for each scored target; a missing or red baseline refutes it.
- 4: not a test — reconcile tool outcomes and recompute each score from the note's counts and exclusions; a mismatched denominator or error counted as a kill refutes it.
- 5: not a test — reconcile survivor-kind counts with tool results and inspect representative mutants; missing kinds, lost survivors or unstated equivalence exclusions refute it.
- 6: not a test — compare recorded start/end and elapsed measurements with the note and Time used; missing runtime or interruption status refutes it.
- 7: not a test — measured total phase-4 time and stop evidence stay within two hours; overrunning or presenting unmeasured coverage as measured refutes it.
- 8: not a test — phase-6 review compares recommendations with measured scope and the PR file list; an unqualified generalisation or adopted gate refutes it.

## Not touched

Both target scripts, `scripts/research_handoff.py`, all tests, the dependency
declarations and lock, `Makefile`, `decisions/gates.yaml`, `.github/`,
`model-endpoints.yaml`, `AGENTS.md`, prompts, templates, governance and ADRs.
Temporary tool configuration is never a repository configuration change.
Tracker changes and the pull request belong to the orchestrator, not this attempt.

## Time used

2026-11-06 01:49:06–02:34:03 UTC, 2697 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
