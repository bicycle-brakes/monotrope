---
title: "Findings — ratchet-mutation-evidence"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
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
