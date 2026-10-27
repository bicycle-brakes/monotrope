---
title: "Plan — ratchet-mutation-evidence"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-26
supersedes: null
superseded_by: null
bead: coding-harness-a05
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, mutation-coverage, ratchet]
---

# Plan — ratchet-mutation-evidence

```text
For you:     A file that only names a gate's script no longer empties the mutation ratchet.
Done when:   Both coverage checks share one rule that needs a mutation test reaching the script; ramp-valves has its seeded red run; make verify green.
Appetite:    1 hour of phase 4; stop at the limit.
Not now:     Fixtures and cross-file helpers; the plans-registry seeded red run; translating the section's German names.
Pre-mortem:  suppose it failed: most likely because a genuine evidence shape (alias, helper, path constant) was missed and a covered gate went red.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_ci.py`: extract today's mention rule into one predicate,
   `_evidence(script, sources)`, used by both
   `test_every_gate_step_has_a_mutation_test` and
   `test_the_mutation_ratchet_only_turns_one_way` (pure refactor, green).
2. `tests/test_ci.py`: add the tests of the ledger with synthetic test
   files; run them and keep the red output (criterion 1).
3. `tests/test_ci.py`: replace the mention rule by `_tests_reaching`, which
   reads a file's syntax tree once (`_parsed`, cached) and follows
   module-level helpers of the same file.
4. `tests/test_gate_machinery.py`: add the ramp-valves seeded red run after
   the coverage check names that gate.
5. Update this plan, `findings.md` and `plans/INDEX.md`
   (`plans_registry.py --index`), stamp `updated:`.

## Verification

```sh
.venv/bin/python3 -m pytest -q -p no:cacheprovider tests/test_ci.py tests/test_gate_machinery.py
PYTHON=$PWD/.venv/bin/python3 make verify
```

## Criterion ledger

- 1: tests/test_ci.py::test_a_bare_mention_of_a_gate_script_is_no_mutation_evidence — a mention or a `__file__` read counts as evidence.
- 2: tests/test_ci.py::test_a_mutation_test_that_reaches_the_gate_script_is_evidence — a genuine shape no longer counts.
- 3: tests/test_ci.py::test_every_gate_step_has_a_mutation_test — a covered gate loses its evidence under the shared rule.
- 3: tests/test_ci.py::test_the_mutation_ratchet_only_turns_one_way — an exempted gate counts as covered.
- 4: tests/test_gate_machinery.py::test_the_ramp_valve_gate_goes_red_when_a_valve_is_due — a due, open valve leaves the gate green.
- 5: not a test — the diff of `OHNE_MUTATIONSTEST` in `tests/test_ci.py` is empty, read in review.

## Route

Research, spec, plan, implementation and self-review by a Claude Code
sub-agent (Opus 5.5) in a cloud container on 2026-10-25, in the worktree
`.claude/worktrees/ratchet-mutation-evidence`, at the orchestrating
session's instruction. The review loop and the phase-6 Codex review are
still owed.

## Runner route — 2026-10-26

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Runner route — 2026-10-26

Stage-1 route: repair · model claude-sonnet-5-5 · reason: maintainer: Sonnet replaces Codex for two hours (2026-10-26).

## Runner route — 2026-10-26

Stage-1 route: repair · model claude-sonnet-5-5 · reason: maintainer: Sonnet replaces Codex for two hours (2026-10-26).

## Runner route — 2026-10-26

Stage-1 route: repair · model claude-sonnet-5-5 · reason: maintainer: Sonnet replaces Codex for two hours (2026-10-26).

## Runner route — 2026-10-26

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used
2026-10-25 17:00–17:40 UTC, about 40 min — research, spec, plan, implement and self-review · Claude Code sub-agent · model claude-opus-5-5 · accepted · estimated by the sub-agent from its own file times, not measured by the orchestrator
2026-10-26 02:14:54–02:26:04 UTC, 670 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-26 02:26:09–02:32:50 UTC, 401 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-26 02:32:55–02:39:21 UTC, 386 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-26 16:20:10–16:43:10 UTC, 1380 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-26 17:06:11–17:17:18 UTC, 667 s — repair · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-26 17:18:45–17:31:56 UTC, 791 s — repair · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-10-26 17:51:24–18:09:04 UTC, 1060 s — repair · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-26 18:09:33–18:19:06 UTC, 573 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-10-26 19:43:47–20:10:02 UTC, 1574 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-26 20:10:07–20:19:52 UTC, 585 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-10-26 20:19:58–20:29:48 UTC, 590 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
