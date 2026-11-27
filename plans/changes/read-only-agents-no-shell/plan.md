---
title: "Plan — read-only-agents-no-shell"
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
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, agents, ramp-valves]
---

# Plan — read-only-agents-no-shell

```text
For you:     The five identified read-only agents are checked for shell and writing tools.
Done when:   The real definitions pass, planted faults fail, and make verify is green after the governance decision.
Appetite:    2 hours of phase 4, repairs included — stop at the limit.
Not now:     Executor scopes, deny-list enforcement and automatic classification of new roles.
Pre-mortem:  suppose it failed: most likely because the rule claims more coverage than the test supplies.
Starts unless you say stop.
```

## Files and sequence

1. Resolve the open governance decision in `spec.md` before implementation; do not represent the full rule as enforced by a partial test. The orchestrator obtains and records the maintainer's answer under the repository protocol.
2. Create `tests/test_agents.py`: parse YAML frontmatter for the five named definitions in `spec.md`, accepting comma-separated strings and lists, and reject missing, malformed, inherited or forbidden tool lists. Add valid and mutated fixture counter-checks that use the same assertion as the real definitions. Do not infer read-only status from absence of forbidden tools: that would make a planted shell disappear from the checked set.
3. For `docs/governance/regelwerk.md`, prepare exact proposed text reflecting the decision and the partial coverage; this human-decided file is for the maintainer to edit, never the stage-2 attempt. The orchestrator coordinates any authorized bootstrap edit after the accepted attempt. Do not claim the other RB-A2 obligations are tested. `scripts/ramp_valves.py` is unchanged: its existing predicate finds the named top-level test. No files are deleted.
4. Update `plans/changes/read-only-agents-no-shell/plan.md` ledger entries when tests exist. The runner maintains `plans/changes/read-only-agents-no-shell/findings.md` and the generated `plans/INDEX.md`; record measured time below.

Do not touch agent definitions, permissions, generated settings, the valve implementation, or other rules. The governance decision may require a separately scoped change; do not silently widen this one.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_agents.py tests/test_ramp_valves.py tests/test_regelwerk.py
make verify
```

Record the failure on a planted Bash mutation and the passing unmodified run. Run `make verify` through `python3 scripts/jobs.py start -- make verify`; it cannot be green until the governance issue is resolved.

## Criterion ledger

- 1: not yet written tests/test_agents.py::test_read_only_agents_have_no_bash — an identified agent with Bash, Write or Edit passes.
- 2: not yet written tests/test_agents.py::test_missing_or_invalid_tool_list_is_rejected — absent or malformed tools pass.
- 3: not yet written tests/test_agents.py::test_valid_read_only_fixture_passes — a valid fixture fails.
- 4: not yet written tests/test_agents.py::test_planted_shell_is_rejected — the Bash mutation passes the same assertion used on real agents.
- 5: not yet written tests/test_agents.py::test_agent_scope_valve_becomes_due — the existing valve predicate stays false when the named test exists.

## Runner route — 2026-11-28

Stage-1 route: explore · model claude-haiku-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Time used

2026-11-27 23:12:10–23:14:22 UTC, 132 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
