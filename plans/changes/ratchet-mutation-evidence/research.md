---
title: "Research — ratchet-mutation-evidence"
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
tags: [research, mutation-coverage, ratchet]
---

# ratchet-mutation-evidence — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by a Claude Code sub-agent at `origin/main` `f8a6b33`
(2026-10-25), for bead coding-harness-a05.

## How the ratchet decides coverage today

Two tests in `tests/test_ci.py` (section "Mutation coverage (RB-G4)") judge
whether a gate has mutation evidence — a test that turns the gate red when
what it protects against is broken:

- `test_every_gate_step_has_a_mutation_test` fails for a gate with no
  evidence and no entry in the exemption list `OHNE_MUTATIONSTEST`.
- `test_the_mutation_ratchet_only_turns_one_way` fails for an exemption whose
  gate already has evidence ("long since covered, but still in the ratchet").

Both take the gate's subject from `_pruefling` (the script under `scripts/`
its command runs, or a `tests/` file it runs). Mutation-named tests are found
by the regular expression `MUTATIONS_NAMEN` over the raw file text
(`goes_red`, `refuses`, `is_caught`, `notices` and similar name parts).

The decision itself is one line in each test, not shared:

- **coverage**, for a script: any test file that contains the script's file
  name anywhere and matches `MUTATIONS_NAMEN` anywhere counts. For a
  `tests/` subject the file itself must hold a mutation-named test — a
  stricter rule added on 2026-09-08 after `test_workflow_entry.py` became
  the "evidence" for the ruleset gate by naming the path in a list.
- **ratchet**: the mention rule for every subject, without the `tests/`
  exception.

So a file that names `plans_registry.py` in a comparison and holds an
unrelated `..._goes_red_...` test is evidence for the plans-registry gate.
The bead's case: on 2026-10-20 a call-site test in `tests/test_stage2.py`
(PR #188) named the renderer's file to identify a command, and the ratchet
called both plans-registry exemptions stale. The maintainer had the line
reworded (option A, 2026-10-21; it now reads
`Path(plans_registry.__file__).name`) and asked for the stricter rule here
(option B).

The mention rule also misses in the other direction: a file that imports a
gate's module and calls it, but never spells the `.py` file name, is not
evidence. Today's genuine evidence for, for example, `check_docs.py` counts
only because the same file names the path elsewhere.

## The current ratchet, run 2026-10-25 at `f8a6b33`

`pytest tests/test_ci.py -k mutation`: 3 passed. The exemption list holds
seven gates: `pytest`, `ruff-check`, `ruff-format`, `markdownlint`,
`lychee`, `plans-registry`, `plans-registry-strict`.

## Which gates rest on bare mentions

Measured by listing, per gate, the test files the mention rule accepts, then
reading the mutation-named tests there for whether they call into, import or
run the script:

| Gate | Script | Accepted today | Genuine evidence |
|---|---|---|---|
| leerprobe | `probe.py` | `test_kit.py`, `test_stage2.py` | `test_kit.py` (calls `probe.*`); `test_stage2.py` only mentions |
| docs-links | `check_docs.py` | `test_gate_machinery.py` | yes, `check_docs.main` |
| frontmatter-current | `check_frontmatter_current.py` | `test_frontmatter_current.py`, `test_research_currency.py` | yes, through the alias `cfc` and `SCRIPT` in helpers |
| bead-export | `check_bead_export.py` | `test_gate_machinery.py` | yes |
| dangling-beads | `check_dangling_bead_ids.py` | `test_gate_machinery.py`, `test_workflow_entry.py` | yes, in `test_gate_machinery.py` |
| decision-continuity | `check_decision_continuity.py` | `test_gate_machinery.py` | yes |
| adr-answers | `check_adr_answers.py` | `test_check_adr_answers.py`, `test_harness_decide_adr.py` | yes, through `_run` and the alias `cag` |
| interview-minimums | `check_interview_minimums.py` | `test_adoption.py`, `test_check_interview_minimums.py` | yes, in the latter |
| question-context | `check_question_context.py` | `test_check_question_context.py` | yes |
| criterion-ledger | `check_criterion_ledger.py` | `test_check_criterion_ledger.py` | yes, through `_run` |
| gate-schema, ci-drift | `ci_gates.py` | `test_gate_machinery.py` | yes, `ci_gates.*` |
| **ramp-valves** | `ramp_valves.py` | `test_gate_machinery.py`, `test_regelwerk.py` | **none** |
| research-currency | `check_research_currency.py` | `test_research_currency.py` | yes |
| ruleset | `tests/test_repo_settings.py` | the file itself | yes |

`ramp-valves` is the one gate whose evidence is only mentions:
`test_gate_machinery.py` runs `scripts/ramp_valves.py` in a test that
asserts it is green today (`test_the_ramp_valve_check_runs_green_here`, not
mutation-named), beside mutation tests for other gates;
`test_regelwerk.py` imports `valves` from it, but its mutation-named tests
seed faults into the rule set, not into the valve script.

`plans-registry` and `plans-registry-strict` have no evidence under either
rule: `tests/test_stage2.py` imports `plans_registry` but only reads its
`__file__`; `tests/test_bead_render.py` calls it in tests that are not
mutation-named; `tests/test_gate_machinery.py` runs it green.

## What genuine evidence looks like

Every genuine case above has one of five shapes, in the mutation-named test
or in a module-level helper of the same file that it calls:

1. a call into the imported module (`import check_docs` …
   `check_docs.main(...)`), at module level or inside the test;
2. the same through an alias (`import check_adr_answers as cag`);
3. a name imported from the module (`from ramp_valves import valves`);
4. a module-level path constant (`SCRIPT = REPO_ROOT / "scripts" / "x.py"`)
   handed to `subprocess.run` in a helper;
5. a command list with the script path (`[sys.executable, "scripts/x.py"]`).

None of them goes through a pytest fixture or a helper in another file.

## Options

1. Keep the mention rule and add the PR #188 shape to a deny list — stays a
   mention rule.
2. Read each test file's syntax tree and count a mutation-named test only
   when it reaches the script in one of the five shapes, directly or through
   helpers of the same file; one predicate for both checks.
3. Run each mutation test against a mutated script (real mutation testing) —
   far beyond a bounded change.

Option 2 is what the bead describes ("imports or runs the script and the
mutation-named test … names the script in its body").
