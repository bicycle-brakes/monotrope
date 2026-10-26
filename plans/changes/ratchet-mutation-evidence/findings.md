---
title: "Findings — ratchet-mutation-evidence"
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
tags: [findings]
---

# Findings — ratchet-mutation-evidence

## Implementation, 2026-10-25

Implemented by a Claude Code sub-agent (Opus 5.5) in a cloud container, at
the orchestrating session's instruction, on a tree branched from
`origin/main` `f8a6b33`.

**Red first.** Step 1 moved today's mention rule unchanged into
`_evidence`; the three mutation-coverage tests stayed green. The new tests
of step 2, run against that rule
(`pytest -k "bare_mention or reaches_the_gate_script or mutation"`):
6 failed, 4 passed.

- Both cases of `test_a_bare_mention_of_a_gate_script_is_no_mutation_evidence`
  failed: "a mention in another test counted as mutation evidence" and
  "a call site that only identifies the script counted as mutation
  evidence" (criterion 1).
- `test_the_mutation_ratchet_only_turns_one_way` failed with "long since
  covered, but still in the ratchet: ['plans-registry',
  'plans-registry-strict']" — the new test data in `tests/test_ci.py` named
  `plans_registry.py` beside mutation-named tests, which reproduced the
  bead's case on the live tree.
- Three cases of `test_a_mutation_test_that_reaches_the_gate_script_is_evidence`
  failed too (a call into the module, an alias, a name imported from it):
  the mention rule also misses genuine evidence that never spells the `.py`
  name. The two path shapes passed.

**After step 3** (`_tests_reaching`): all new tests green, the ratchet green,
and `test_every_gate_step_has_a_mutation_test` red with exactly one gate,
"ramp-valves → ramp_valves.py" — the one gate whose evidence was only
mentions (`research.md`). **After step 4** (the seeded ramp-valves run):
`tests/test_ci.py` and `tests/test_gate_machinery.py` green, 114 passed,
2 skipped. Per gate the shared rule now names the reaching tests; the
exemption list is unchanged at seven entries.

Cost: the coverage test parses every test file that names a gate's module
once (cached), about 1 s on this container, where the text search took
0.04 s.

**`PYTHON=$PWD/.venv/bin/python3 make verify`, 2026-10-25:** red on two
blocking gates, both for this container only. `pytest`: 1 failed, 2505
passed, 30 skipped, 16 errors — the failure is
`test_an_unreadable_target_is_named_by_its_repository_path` (the container
runs as root) and the errors are `tests/test_pi_contract.py` (no pinned Pi);
none touches this change. `ruleset`: needs network and a `gh` login.
`leerprobe` and every other blocking gate green; `docs-links` and
`markdownlint` red as report-only gates, as on `main`.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- The reading is syntactic: a test that copies a script by a path built
  with `/` (as the stage-2 tests plant the renderer) would reach it in this
  sense without running it. No mutation-named test does so on
  `f8a6b33`; a later one would make an exemption look stale, and the
  ratchet's message names the gate.
- A local variable that shares the alias of an imported gate module is read
  as the module (scope is not tracked).
- Fixtures, `conftest.py` and helpers in another file are not followed
  (non-goal); evidence that lives only there would go unseen and turn the
  coverage check red, not green.
- `MUTATIONS_NAMEN` still matches raw text for a `tests/` subject (the
  ruleset gate), as before.
- New identifiers are English; the section's German names stay (D-4).

## Review loop skipped, 2026-10-25

The review loop (phase 4b) did not run on this change. The maintainer
answered on 2026-10-25 (night-run plan, `docs/research/2026-10-25-night-run-plan.md`,
answer 1) that the small cloud-session fixes get phase 6 only tonight,
because each had the Opus 5.5 pre-review recorded above. Phase 6 follows in
a fresh Codex session.

Stage-2 call, 2026-10-26: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 593 files, 2190 commits, 12 rules.

## Phase 6 — Codex, 2026-10-26

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| R6-1 | MAJOR | SPEC | implementation | tests/test_ci.py:2010–2015 | A mutation-named test containing only `assert command[0].endswith("plans_registry.py")` is returned as evidence for the registry script. Every call argument is treated as a script path, including strings used solely to compare commands. This reproduces the false evidence the change must reject and can force removal of an exemption without a reaching test. [Acceptance criterion 1] | Codex | taken — test: tests/test_ci.py::test_a_string_comparison_is_no_gate_evidence — a mutation-named test that only compares command[0] with the script name is credited as reaching it (orchestrator, 2026-10-26) | — |
| R6-2 | MAJOR | SPEC | implementation | tests/test_ci.py:2083–2089 | Helper references count as helper calls. With `_run()` calling `plans_registry.main()`, a mutation-named test containing only `assert callable(_run)` is returned as registry evidence although it never invokes `_run` or the gate. Reachability must follow invocations; merely referencing a callable cannot establish execution. [Acceptance criterion 1] | Codex | taken — test: tests/test_ci.py::test_a_helper_reference_is_no_helper_call — a mutation-named test that only references a helper calling the gate is credited as reaching it (orchestrator, 2026-10-26) | — |
| R6-3 | MAJOR | MAINT | implementation | tests/test_ci.py:2027–2031 | Imports inside unrelated functions become bindings for every test in the file. Reproduced with `from plans_registry import main` inside a normal test and a separate mutation-named test calling its own `main` fixture: `_evidence` credits the registry script although the mutation test never imports or calls it. Preserve import scope when resolving names so unrelated tests cannot supply false gate coverage. | Codex | taken — test: tests/test_ci.py::test_an_import_in_another_test_binds_nothing_here — an import inside an unrelated test function credits a separate mutation-named test (orchestrator, 2026-10-26) | — |

Phase 6 verdict: codex 01a175fa-3ebc-7151-80c0-fd1cdb4f6b43, 2026-10-26
Reviewer session: codex 01a175fa-3ebc-7151-80c0-fd1cdb4f6b43 — a fresh session reviewed: no phase-2a session was recorded

Loop rows: none — the loop did not run for this change.

Stage-2 call, 2026-10-26: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 593 files, 2192 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_ci.py` +105 -24
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - R6-1: tests/test_ci.py::test_a_string_comparison_is_no_gate_evidence: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - R6-2: tests/test_ci.py::test_a_helper_reference_is_no_helper_call: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> - R6-3: tests/test_ci.py::test_an_import_in_another_test_binds_nothing_here: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure
> ```

Stage-2 call, 2026-10-26: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-sol · reason first Codex post-run check failed · leak check clean over 593 files, 2192 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - R6-1: no fixed line
> - R6-2: no fixed line
> - R6-3: no fixed line
> ```

Stage-2 call, 2026-10-26: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 593 files, 2192 commits, 12 rules.

> Attempt 3 (stage-1) failed its post-run checks.
>
> Files the attempt changed: none.
>
> Diagnostics:
> ```text
> - Runner format before `make verify`: ruff changed no file.
> - R6-1: several fixed lines
> - R6-2: several fixed lines
> - R6-3: several fixed lines
> ```
