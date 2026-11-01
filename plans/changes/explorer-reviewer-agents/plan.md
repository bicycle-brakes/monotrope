---
title: "Plan — explorer-reviewer-agents"
status: draft
implementation_status: none
date: 2026-11-01
last_reviewed: 2026-11-01
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-9ll
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: gpt-6.1-sol, version: "2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, sub-agents]
---

# Plan — explorer-reviewer-agents

```text
For you:     Reusable read-only explorer and reviewer helpers use Haiku 5.5 and Opus 5.5 high.
Done when:   Definition tests and make verify pass, and fresh sessions confirm both selected models.
Appetite:    1 hour of phase 4 in total, repairs included; stop at the limit.
Not now:     The stop hook, artefact validator, model registry and Stage-2 routing changes.
Pre-mortem:  suppose it failed: most likely because Claude Code ignored the configured model.
Scope widens to workflow inventory and two additional kit exceptions; is that ok?
```

## Execution boundary

Blocked on the spec's open scope decision: the interview fixes models and
read-only operation, but its scope note permits only the pair and one test
module. The steps marked conditional below are proposals, not permission to
expand that scope. Record the maintainer's actual answer in `decisions.md`
before implementation; never supply an answer on their behalf. No design or
ADR is due for this bounded change. Explore used Stage 2, not a Stage-1 fallback.

## Files and steps

1. **Runner:** create `tests/test_explorer_reviewer_agents.py` with the ledger's
   static checks, parsing the two real files' YAML frontmatter. Assert names
   `explorer`/`reviewer`, nonempty English descriptions, exact model IDs,
   reviewer's `effort: high`, and exactly `Read`, `Grep`, `Glob` as tools.
   Missing files and unrestricted tool inheritance fail, never skip. Before
   bootstrap, the missing-file failure is expected, not completion.
   Check source-backed explorer findings and unknowns, spec-based reviewer
   findings and explicit prohibitions on repairs, commits, tracker writes
   and self-acceptance. Counter-check wrong-model, missing-effort, extra-tool
   and changed-role fixtures through the same assertion helpers.
2. **Orchestrator, after the accepted attempt:** create the held files
   `.claude/agents/explorer.md` and `.claude/agents/reviewer.md` in English,
   using Claude Code configuration frontmatter, not document metadata.
   Explorer: `model: claude-haiku-5-5`; map sources, report evidence and
   unknowns to the caller, and leave research-file and tracker writes to it.
   Reviewer: `model: claude-opus-5-5`, `effort: high`; compare supplied spec
   and implementation evidence in fresh context and return actionable
   findings, without repairs or self-acceptance. Both use
   `tools: Read, Grep, Glob`, follow repository instructions, and contain
   `## Evidence contract (RB-A1)` followed by the exact English paragraph
   from `docs/governance/regelwerk.md` §6; copy it, do not paraphrase it.
3. **Conditional runner maintenance, only after the scope answer:** update
   `docs/WORKFLOW.md` to move both helpers from absent to supplied and stamp
   the check's actual date and checked commit; update
   `tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands`
   to hold that inventory while retaining the validator and stop hook as gaps.
   Update `scripts/kit/probe.py` with the two measured endpoint-case IDs
   ending `[explorer.md-claude-haiku-5-5]` and
   `[reviewer.md-claude-opus-5-5]`, using the existing missing-full-suite reason;
   change its cap from 42 to 44 with the rationale that the kit carries
   definitions but no endpoint declaration. Do not suppress the repository's
   endpoint checks or fabricate an endpoint declaration in the kit.
   Bookkeeping may be prepared before bootstrap; only the orchestrator's
   combined tree can pass the complete kit check.
4. **Orchestrator:** record fresh-session observations in this change's
   `findings.md`: start Claude Code after installation, invoke each named
   helper from a parent using a different model, inspect the actual model
   through `/status` as the workflow requests, and record observable output,
   command/session, date and commit. If that surface cannot identify the
   child model, record not measured and stop completion; do not change pins.
5. **Orchestrator:** update this change's `plan.md` ledger from `not yet
   written` to test entries when functions exist, fill `## Time used`, and
   regenerate `plans/INDEX.md` with `python3 scripts/plans_registry.py --index`
   after metadata edits. The index is generated bookkeeping, not a new
   deliverable. No files are deleted; `spec.md`, `research.md` and
   `decisions.md` remain the basis, with only actual answers recorded.

## Verification

After bootstrap, run from the worktree with its locked environment selected:

```sh
.venv/bin/python3 -m pytest tests/test_explorer_reviewer_agents.py tests/test_regelwerk.py tests/test_model_endpoints.py tests/test_workflow_entry.py -q
make verify
```

Record the expected pre-bootstrap failure, targeted result, full verification
result and fresh-session evidence at their actual commits; the runner's
document check does not replace these checks.

Draft checks on 2026-11-01, working tree based on `544cb659`: the named
interview check, criterion ledger and question-context check passed; the
research-handoff check reports the legacy exemption (no swarm). Required
registry header fields, card order and empty time section were checked.
The artefact validator is absent. The full registry check was not run because
its tracker reader can leave this worktree; the generated index differs and
was left untouched under the draft's write limit. The open scope decision
means the spec gate is not complete. No implementation or runtime check ran.

## Criterion ledger

- 1: not yet written tests/test_explorer_reviewer_agents.py::test_explorer_pins_haiku — remove the definition or change its model
- 2: not yet written tests/test_explorer_reviewer_agents.py::test_reviewer_pins_opus_high — change the model or remove/change effort
- 3: not yet written tests/test_explorer_reviewer_agents.py::test_helpers_allow_read_tools_only — add a shell, writer, delegation or inherited tool set
- 4: not yet written tests/test_explorer_reviewer_agents.py::test_helpers_state_read_only_reporting_roles — remove the reporting role or authorize repairs
- 5: tests/test_regelwerk.py::test_rb_a1_clause_is_present_verbatim — modify the evidence paragraph
- 5: tests/test_regelwerk.py::test_agent_definitions_carry_no_instance_terms — introduce prohibited instance vocabulary
- 5: tests/test_model_endpoints.py::test_every_agent_model_resolves_to_a_declared_endpoint — pin an undeclared model
- 6: not a test — orchestrator records both fresh child-session model observations in findings.md against the checked commit; a mismatched or unobserved child model prevents completion

## Do not touch

No existing agent, endpoint declaration, normative evidence text, routing,
tracker, hook, validator, model registry, ADR, harness settings or gate-policy
changes. Conditional inventory/kit maintenance remains blocked on the scope
answer; held definitions are always the orchestrator's responsibility.

## Time used

## Scope answer — 2026-11-01

The maintainer answered the plan card's question on 2026-11-01 at about 08:55
UTC ("Ja"): step 3 runs — `docs/WORKFLOW.md` lists both helpers as supplied,
with its test, and `scripts/kit/probe.py` raises its cap from 42 to 44 with
the stated reason.
