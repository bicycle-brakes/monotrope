---
title: "Findings — read-only-agents-no-shell"
category: findings
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.22
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — read-only-agents-no-shell

Stage-2 call, 2026-11-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1320 files, 6153 commits, 12 rules.

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1323 files, 6154 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:4611e555a9f25fcf0aeb9ce77db2345ebdf9a3edf328b7bdb89a8eaf13913b41

Spec review commit: 22b3446b990e91dc6457488ff2f0fe68e25e8115

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | Protected areas; Definition of Done; `scripts/ramp_valves.py` `REGEL_VENTILE["agents-tool-scopes"]` | The spec does not say what happens to the valve entry. Once the test exists, `_enforcer_exists` makes the valve due. `python3 scripts/ramp_valves.py` (the `ramp-valves` gate in verify) then exits 1 as long as the entry stays in `REGEL_VENTILE`. If the rule row stops naming `Ramp:agents-tool-scopes` while the entry stays, `tests/test_regelwerk.py::test_every_named_ramp_exists_and_no_valve_is_orphaned` fails. So "make verify green" needs a change to `scripts/ramp_valves.py`: remove the entry, point it at a different enforcer, re-date it, or add a new valve with a name and deadline for the shell-scope and deny clauses. The spec names none of these and does not list the file, so the implementer would pick one silently, including a deadline that only the maintainer has set so far. The research relies on `tests/test_ramp_valves.py::test_no_valve_is_due_and_still_open`, which does not exist in the tree. | Opus | open | — |
| F-2 | [AMBIGUITY] | SPEC | base | AC 1–3; Terms | "Valid tool list" has two readings. (a) Denylist: any list without the names Bash, Write and Edit passes, as AC 1 is worded. Then `MultiEdit`, `NotebookEdit`, `Task`, an `mcp__*` tool, or a scoped `Bash(git status:*)` under exact-name matching all pass next to Read, Grep and Glob. (b) Allowlist: exactly Read, Grep and Glob, as `_assert_tools` in `tests/test_explorer_reviewer_agents.py` requires and AC 3's fixture suggests. Then any added tool fails, harmless or not. "Malformed" is not defined either (empty value, `[]`, lowercase `bash`, YAML list vs comma string), so AC 2's refutation case cannot be built without choosing one. | Opus | open | — |
| F-3 | [AMBIGUITY] | SPEC | base | AC 4; DoD "Special runs"; Protected areas | Where the planted shell lives has two readings. (a) A branch commit adds `Bash` to a real `.claude/agents/<name>.md`, the red run is shown, and a later commit reverts it. "The same enforcer" and "with its commit in the pull request body" point this way. But it edits agent definitions, which Protected areas says are not changed, and that edit stays in the PR history even though the net file list is clean. (b) The mutation is a fixture inside the test, a temporary copy of an identified agent with `Bash` added, run through a helper the named test also calls. No agent file is touched. But then "its commit" is just the test commit, and "the same enforcer" means a shared helper, not `test_read_only_agents_have_no_bash` itself, which reads only the live directory. | Opus | open | — |
| F-4 | [AMBIGUITY] | SPEC | base | Open decisions, Option 1; Protected areas ("exact proposed change") | It is unclear what "Teilprüfung ausweisen" changes in the rule row, which has one level and one enforcer cell. (a) RB-A2 goes to level 4, names the test and carries a written "partial" note. The shell-scope and deny clauses then sit at level 4 with no enforcer, which `tests/test_regelwerk.py` cannot detect and which contradicts "ohne mehr Schutz zu behaupten". (b) RB-A2 stays at level 2 and names the test plus a new dated `Ramp:` for the remaining clauses. That needs the new valve from F-1. (c) RB-A2 is split into two rows, with the remaining clauses under a new ID; family numbering must stay gap-free. A maintainer who answers "ok" does not know which of these diffs they are approving. | Opus | open | — |
| F-5 | [AMBIGUITY] | SPEC | base | DoD bullets 1, 3 and 4 | Where the maintainer's edit of `docs/governance/regelwerk.md` lands has two readings. (a) In this PR: the file list then contains the protected file, so bullet 3 ("as shown by the pull request file list") cannot show it untouched. The commit carrying `Closes-Bead` must then come after the maintainer's commit, or be that commit. (b) In a separate PR: whichever merges first is red. A rule at level 4 naming a missing test fails `test_rules_at_level_three_or_higher_name_an_existing_enforcer`, and a test landing first turns the ramp-valves gate red. | Opus | open | — |
| F-6 | MAJOR | SPEC | base | DoD; Open decisions, Option 2 | Under Option 2 the DoD cannot be met as written. The DoD requires verify green and closing bead `coding-harness-5ane.22` with no condition attached. Option 2 leaves RB-A2 at its current level and says completion is delayed. With the test merged and the rule not raised, the ramp-valves gate stays red (F-1). The spec does not say whether, under Option 2, this PR still ships the test, re-dates or re-points the valve, or leaves the bead open. | Opus | open | — |
| F-7 | MAJOR | SPEC | base | AC 5 | AC 5 cannot be checked in the delivered tree. For verify to be green, the `agents-tool-scopes` entry must leave `REGEL_VENTILE` or change (F-1). Once it is removed, there is no valve predicate left to read. If it is pointed at an enforcer for the remaining clauses (F-4 b), the predicate is false while the named test exists, so the refutation case happens by design. The criterion can only go red on an intermediate commit, and the spec does not name that commit. | Opus | open | — |
| F-8 | MINOR | SPEC | base | Terms; AC 2 | The spec does not cover a missing or renamed file in the fixed baseline. If `.claude/agents/migration-supervisor.md` is deleted or renamed, the enforcer could fail (file not found), or it could skip the file and pass with only four agents checked. AC 2 covers a missing tool list, not a missing definition, and no refutation case asserts that all five files were found and checked. | Opus | open | — |
