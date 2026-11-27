---
title: "Research — read-only-agents-no-shell"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.22
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# read only agents no shell — Research

## Topic (bead coding-harness-5ane.22)

Class: bounded. Ramp valve `agents-tool-scopes` (`scripts/ramp_valves.py`),
rule RB-A2 in `docs/governance/regelwerk.md`; maintainer 2026-11-25 (bead
`coding-harness-5ane.1`): build the enforcer in the 72-hour run; the valve was
re-dated to 2026-12-31 meanwhile. Write
`tests/test_agents.py::test_read_only_agents_have_no_bash` so that it holds
today and fails on a planted fault; then the valve is due and the rule is
raised in the rule set
(`tests/test_ramp_valves.py::test_no_valve_is_due_and_still_open`).

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1320 files, 6152 commits, 12 rules.

## Runner exploration — 2026-11-28

# Research: read-only-agents-no-shell (phase 1 output, for appending to `research.md`)

Nothing was written to any file. Everything below comes from read-only searches and reads of the worktree.

## What exists today

**The open valve.** `scripts/ramp_valves.py`, `REGEL_VENTILE["agents-tool-scopes"]`, names the rule RB-A2 ("read-only agents carry no shell, executors declare their scope"). Its enforcer is `tests/test_agents.py::test_read_only_agents_have_no_bash`, with deadline `2026-12-31`. The comment above the entry records the re-dating from 2026-11-30 by the maintainer on 2026-11-25 (bead `coding-harness-5ane.1`). `_enforcer_exists()` in the same file decides "due" by a text search for `^def test_read_only_agents_have_no_bash\(` in that path. It does not import the module.

**The rule.** `docs/governance/regelwerk.md`, row `RB-A2`: "Read-only-Agents führen kein `Bash`, `Write` oder `Edit`; wer eine Shell hat, deklariert ihren Umfang; `permissions.deny` enthält mindestens Prod-Deploy, `bundle destroy`, Force-Push und `rm -rf`". Level `2`, enforcer `Ramp:agents-tool-scopes`. `docs/research/2026-09-16-review-corpus-vs-running-workflow.md` (the row on approval boundaries) names the same four deny entries and says path rules do not catch `Bash` writes (WORKFLOW §3).

**The test file does not exist.** `tests/test_agents.py` is not present (Glob `tests/test_agents*.py` returned nothing). An archived triage note, `plans/changes/archive/2026-09-20-2ee-triage/research.md`, cites a `tests/test_agents.py (bash-scope)` for RB-A2. That reference is historical; the file is not in the tree now.

**Existing read-only enforcement for two agents.** `tests/test_explorer_reviewer_agents.py`:
- `READ_TOOLS = ("Read", "Grep", "Glob")`.
- `_assert_tools()` requires the `tools:` field to name exactly those three, and accepts a comma-string or a list.
- `ACTIONS` lists the prohibited actions for the two helpers: repairs, commits, tracker writes, accepting one's own work, and writes for the explorer.
- Test functions: `test_helpers_allow_read_tools_only`, `test_helpers_state_read_only_reporting_roles`.
- It covers only `.claude/agents/explorer.md` and `.claude/agents/reviewer.md`, not the other agents in the directory.

**The agent definitions.** `.claude/agents/` holds nine `*.md` files. Each has a `tools:` line, and the `tools:` values, from the frontmatter, are:

| File | `tools:` | Language of text |
|---|---|---|
| `explorer.md` | Read, Grep, Glob | English |
| `reviewer.md` | Read, Grep, Glob | English |
| `consistency-auditor.md` | Read, Grep, Glob | German |
| `migration-supervisor.md` | Read, Grep, Glob | German |
| `preconditions-gate-runner.md` | Read, Grep, Glob | German (description: "liest und berichtet nur") |
| `entity-deployer.md` | Read, Bash, Grep, Glob | German |
| `code-generation-orchestrator.md` | Read, Write, Edit, Grep, Glob, Bash | German |
| `entity-builder.md` | Read, Write, Edit, Grep, Glob, Bash | German |
| `reconciliation-orchestrator.md` | Read, Write, Grep, Glob, Bash | German |

Source: the `tools:` and `description:` lines of each file, read by Grep.

**Consequence for "holds today".** Among the agents that carry no `Write`, `Edit` or `Bash` (`explorer`, `reviewer`, `consistency-auditor`, `migration-supervisor`, `preconditions-gate-runner`), none has `Bash`. So the planned test holds on the current tree under any reading of "read-only" that uses the tool list or the two English helpers. Only `entity-deployer` has `Bash` without `Write`; whether it is "read-only" decides whether it fails the test.

**Other relevant tests.**
- `tests/test_regelwerk.py::test_rb_a1_clause_is_present_verbatim` compares the RB-A1 clause in every `.claude/agents/*.md` with `regelwerk.md` section 6.
- `tests/test_regelwerk.py::test_agent_definitions_carry_no_instance_terms` scans every `.claude/agents/*.md` for instance terms (house rule 6).
- `tests/test_model_endpoints.py::agent_modelle()` reads `^model:` from every agent file.

**The deny list.** `.claude/settings.json`, `permissions.deny`, contains only `mcp__omnigent__*` entries and `Edit(//**/.omnigent/config.yaml)`. A search for `rm -rf`, `push --force`, `bundle destroy` and `deploy` found nothing in that file. `permissions.ask` has `Bash(git push *main*)`, among others. The second clause of RB-A2 therefore has no enforcer anywhere in the tests read so far.

**Where settings are written.** `docs/WORKFLOW.md`, around the lines naming `scripts/agent_policy.py write`, says that command renders `.claude/settings.json` and `.agents/hooks.json`. The same section says each tool that writes, runs, spawns or changes state is denied by name, with the list kept in `scripts/omnigent_policy.py`. So the settings file is generated; a hand edit would be a side route under house rule 9.

## Where it lives

- Valve and due-logic: `scripts/ramp_valves.py` (`REGEL_VENTILE`, `_enforcer_exists`, `_regel_ventil`).
- Rule row: `docs/governance/regelwerk.md`, table of RB rules.
- Helper contract: `tests/test_explorer_reviewer_agents.py`.
- Agent definitions: `.claude/agents/*.md`.
- Deny and ask lists: `.claude/settings.json`, rendered by `scripts/agent_policy.py` (per WORKFLOW).
- Change folder: `plans/changes/read-only-agents-no-shell/` (`research.md`, `decisions.md`).

## What is unclear

1. **What "read-only agent" means.** No field in the frontmatter marks an agent as read-only. Three readings are possible: (a) by tool list, no `Write`, `Edit` or `Bash`; (b) by description ("liest und berichtet nur"); (c) by name, the two helpers. Under (a) the set is five agents; under (b) and (c) it is two or three. Under (a) `entity-deployer` is not read-only, so it may keep `Bash`. The test's definition decides this, and nothing in the repository states it.
2. **The second clause of RB-A2 has no test.** The valve's enforcer name covers only "no Bash". The rule also requires that a shell-holding agent declares its scope (no field for that exists in the frontmatter) and that `permissions.deny` carries four named patterns (none present in `.claude/settings.json`). Whether the change must cover this clause, or the valve is closed on the first clause only, is not stated in the valve or the rule.
3. **Which "Bash" check.** The tool-list check can only see the `tools:` declaration. Whether a Bash capability is inherited when `tools:` is absent is covered for the two helpers by `_assert_tools`; the other seven agents all declare `tools:`, but no test asserts that for them.
4. **Language and house rule 6.** Seven of the nine agent definitions are in German. Whether they are part of this repository's kit or a leftover from elsewhere was not established (see the references below). The instance-term test already scans them.
5. **Provenance of this file.** `research.md` frontmatter says `provenance: human-written`. Its own banner says a language-model fill sets `ai-drafted-reviewed`, `produced_by:` and `review:`. This is an action for whoever writes the file, not a research finding.

## Which files a change would have to touch

- `tests/test_agents.py` (new): `test_read_only_agents_have_no_bash`, which parses each `.claude/agents/*.md` frontmatter the way `tests/test_explorer_reviewer_agents.py` does, and fails on a planted read-only agent with `Bash`. It must also include a counter-check fixture, as the existing helper test does.
- `docs/governance/regelwerk.md`: the RB-A2 row, level `2` to `4`, enforcer column changed to the test path. Per `tests/test_regelwerk.py`, a level-4 rule needs a real enforcer. This is a human-decided file if `provenance.yaml` marks it so (the decisions file says the maintainer decides that; not checked here).
- `scripts/ramp_valves.py`: nothing changes in code. The valve becomes due by the new test's existence, and `tests/test_ramp_valves.py::test_no_valve_is_due_and_still_open` then demands the rule be raised.
- `scripts/agent_policy.py` and `scripts/omnigent_policy.py` (only if the deny clause is taken): the deny list is generated from there, not edited by hand in `.claude/settings.json`.
- `plans/changes/read-only-agents-no-shell/research.md` and `decisions.md`: the phase-1 result and provenance header.

## Not read in this pass (so not reported as checked)

- `tests/test_ramp_valves.py` (the test named in the change's topic) — its exact assertions are not confirmed here.
- `tests/test_regelwerk.py` parser `_regeln` — the level and enforcer format were inferred from the mutation tests, not from the parser.
- `scripts/agent_policy.py`, `scripts/omnigent_policy.py`, `tests/test_hook_behaviour.py`.
- `scripts/kit/probe.py`, which names two of the German agent files (found by search, not opened).
- The bodies of the seven German agent definitions beyond their frontmatter.
- Whether the German agent files are tracked in git: no git command was run.
