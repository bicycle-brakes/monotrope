---
title: "Plan — central-models"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-ylu
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, models, effort, routing, kit]
---

# Plan — central-models

```text
For you:     change workflow models and effort in one repository setting; the runner, agent definitions, routing tables, swarm selectors and session suggestion read that setting
Done when:   all 16 criteria have evidence in tests and ADR review, generated views match, the kit keeps approvals local, and make verify ends VERIFY GREEN
Appetite:    8 h of phase 4, repairs included; a stop, not an estimate
Not now:     new model approvals, changed model choices, swarm execution, shared values across repositories or a general harness extension
Pre-mortem:  suppose it failed: most likely because a launcher still reads an old global tuple after preflight validated the new selection
Starts unless you say stop.
```

Implements [spec.md](spec.md) and carries the necessary design below. Baseline:
`e048fa4`, branch `explore/central-models`, read 2026-10-14. Explore used the
runner's `flash` route, `glm-5.3-flash`; no Stage-1 Explore fallback is recorded
and none needs carrying forward. This draft runs no implementation or commit.

## Build order and selection contract

1. Add the strict shared reader and fixture tests; then migrate the live
   declaration without changing selections. No import-time configuration read.
2. Pass resolved selections through every runner launch, retry, audit and
   report. Dispatch by supported endpoint transport and role capabilities,
   never by equality with `CODEX` or `GLM`. Remove all six route constants.
3. Generate and check tables and native agent fields; convert prompts and
   repository instructions to role references. Declare the gate and regenerate
   CI. Preserve all ledger-referenced top-level test names.
4. Carry the complete routing bundle through the kit; prove target-local
   values with fixtures, then add the four ADR amendment notices and run verify.

Extend `model-endpoints.yaml` to version 2, preserving its permission fields.
Use the strict loader from `check_adr_answers.py`. New sections:
`models: {profile: {endpoint, model, display}}`,
`routes: {role: {model: profile, effort: value-or-null, fallback?: role, stage1?: role}}`,
`agents: {default: role, overrides: {name: role}}`,
`ladders: {name: [{model: profile, effort: value-or-null}]}` and
`session_default: role`. Ladder roles have `ladder` instead of `model`;
deterministic roles explicitly use `model: null`. Required `effort: null`
omits an override. Refuse duplicate keys, cycles, bad types/references,
undeclared models, absent clearance/residency and unsupported role/transport
or effort combinations; never supply a built-in model default.

The reader takes an explicit root or declaration text and returns immutable
`{role, endpoint, model, effort, display}` selections. Its read-only JSON CLI
accepts `--route NAME`, `--agent NAME`, `--ladder NAME`, `--session-default`.
There is no launch in a query. Load anew at each verb boundary, retain one
resolved snapshot within that invocation, and recheck permission/leaks before
every call. A removed clearance never advances to fallback.

Seed these selections, observed at the baseline; values in this table are
migration evidence, not future runtime inputs:

| Binding | Endpoint and model | Effort | Alternative binding |
|---|---|---|---|
| `explore`, `implement` | `glm-coding-plan` / `glm-5.3-flash` | `max` | explore Stage 1: `manual-explore`; implement fallback and Stage 1: `manual-implement` |
| `draft`, `repair`, `review` | `openai-codex` / `gpt-6.1-sol` | `max` per role | draft fallback: `draft-fallback`; repair fallback and Stage 1: `manual-implement` |
| `draft-fallback` | `glm-coding-plan` / `glm-5.3` | `max` | none |
| `spec-review`, `manual-draft` | `claude-code-plan` / `claude-opus-5-5` | `xhigh` | `draft.stage1` is manual guidance only |
| `manual-interview`, `manual-review` | `claude-code-plan` / `claude-opus-5-5` | `null` | none |
| `manual-explore`, `commit` | `claude-code-plan` / `claude-haiku-4-5` | `null` | none |
| `manual-implement` | `claude-code-plan` / `claude-sonnet-5-5` | `medium` | none |
| `agent-default` | `claude-code-plan` / `claude-sonnet-5` | `null` | optional per-agent override |
| `session-default` | `openai-codex` / `gpt-6.1-sol` | `null` | suggestion only |
| `review-loop`, `probe` | named ladder `review-loop` | each rung's value | none |
| `verify`, `release-loop` | explicit deterministic selection | `null` | none |

Shared model profiles centralize identifiers; effort stays per binding.
Phases 2, 2b and 3 reference `draft`/`manual-draft`. `research-recheck` keeps
an explicit job-configured reference, with no invented fixed choice. Initialize
`review-loop` to the current Go order: `deepseek-v4.1-flash`,
`mimo-v2.6-flash`, `mimo-v2.6-pro`, each effort `max`. Initialize
`research-swarm` and `review-swarm` to empty lists and refuse execution
selection until their own changes supply approved members. Do not derive
ladder order from the endpoint approval list.

Keep primary/primary/fallback attempts and their existing failure triggers;
only bindings are data. Client capabilities stay explicit: current Codex and
Claude writing paths, existing read-only review paths and Pi loop/session
paths. `run_codex`, `run_work_model` and `run_reviewer` receive a selection;
prompt format and tool permissions follow the transport and role. Keep the
first phase-6 review's existing historical Codex phase-2a resume rule when its
selected client supports that recorded thread; otherwise start a fresh
read-only context. Re-checks remain fresh, and loop marks resume only the
current verdict's thread. Preserve repair/re-check freshness even when two
roles choose the same model; no repair thread becomes a review thread.

Session suggestions produce the exact model-id form and optional `--effort`
argument for the existing explicit `session --model` launch. Add session-only
`--effort`; when absent, preserve today's client default. Pass Codex effort
as its reasoning configuration and Pi effort as thinking; apply the same
capability validation. The suggestion does not remove the explicit-model
requirement or change approval, worktree or policy checks.

The renderer owns marked `central-models:manual` and `central-models:stage2`
table blocks and only native agents' marked `model`/optional `effort` fields.
Leave tools, descriptions, frontmatter outside those fields and bodies intact.
Every prompt identifies its role(s), with explicit deterministic, ladder and
job-configured exceptions. `--write` is idempotent; `--check` detects missing
or doubled markers, missing agents/prompts and drift without writing. Exit 1
means invalid configuration/drift, exit 3 means not measurable. Wire that
check as the block gate `model-routes` in the existing verify job, placement
`both`; derive CI through `scripts/ci_gates.py`.

The kit template has the same role and effort defaults, unset model profiles,
empty endpoint approvals and explicit unconfigured ladders. Do not copy local
`model-endpoints.yaml` values into a target. Carry the runner's import closure,
prompts and generator inputs through explicit export rules, plus fixture tests
in the mechanism manifest. Missing target selections refuse until configured;
fixture-backed portable tests pass without approving production providers.
Replace model-dependent probe node IDs with stable IDs, retaining measured
reasons for inventory-only cases; never increase the exception cap to hide a
failure. Do not change the probe's tracked-file collection policy.

## Files

- `model-endpoints.yaml` — add profiles, roles, agent bindings, independent
  ladders and session default; replace current routing claims in remarks with
  role references, preserving provider facts and permissions.
- `scripts/model_routes.py` — create the strict root/text reader, validation,
  typed selections and the non-launching JSON selection CLI.
- `scripts/render_model_routes.py` — create deterministic generation and its
  read-only drift/reference check.
- `scripts/stage2.py` — remove selection constants and pass per-verb selections
  through preflight, all attempts, launchers, audit, loop/probe and session.
- `scripts/stage2_session.py` — share declaration/transport validation and
  carry optional explicit effort without weakening session guards.
- `scripts/stage2_runs.py` — resolve selections from `Source` at the requested
  revision; remove constant imports and retain historical counting.
- `tests/test_model_routes.py`, `tests/test_render_model_routes.py` — create
  the positive and planted-fault tests named in the ledger.
- `tests/test_stage2.py` — extend fixtures with central settings and test
  argv against changed bindings, keeping existing contract tests and names.
- `tests/test_stage2_session.py`, `tests/test_stage2_runs.py` — cover central
  suggestions, explicit effort, revisions and historical audit counts.
- `tests/test_model_endpoints.py` — replace guessed live display resolution
  with declared profiles/roles and stable parametrization IDs; preserve
  permission/terms assertions and ledger-referenced functions.
- `tests/test_templates.py` — resolve the design prompt's role when comparing
  it with the generated phase-2b row; keep the existing test's name and purpose.
- `tests/test_kit.py` — prove complete portable dependencies, unconfigured
  template refusal and two repositories with independent permitted bindings.
- `scripts/kit/manifest.yaml`, `scripts/export/manifest.yaml` — classify and
  carry the routing bundle and its import closure, leaving live values local.
- `scripts/kit/probe.py` — update affected stable node IDs and measured
  inventory reasons only; no cap increase or collection-policy change.
- `templates/model-endpoints.yaml` — create the role/effort template with
  unset models and no target permissions.
- `scripts/ci_gates.py` — classify the shared library in `OHNE_AUFRUFER` and
  any portable helper lacking a direct gate caller, with specific reasons.
- `decisions/gates.yaml`, `.github/workflows/ci.yml` — declare the routing
  block gate and regenerate the workflow from the gate list.
- `provenance.yaml` — declare the configuration's existing human-written or
  AI-drafted provenance and generated table/agent fields, without making
  routine compatible selection changes an ADR decision.
- `docs/WORKFLOW.md` — generate both tables and express other live routing
  prose through roles, including how to regenerate and restart native agents.
- `AGENTS.md` — replace model assignments with role references and the
  selection/regeneration commands used before a new agent session.
- `prompts/01-explore.md`, `prompts/01a-interview.md`,
  `prompts/02-spec.md`, `prompts/02a-spec-review.md`,
  `prompts/02b-design.md`, `prompts/03-plan.md`,
  `prompts/04-implement.md`, `prompts/04b-review-loop.md`,
  `prompts/05-verify.md`, `prompts/06-review.md`,
  `prompts/07-commit.md`, `prompts/research-recheck.md` — use validated role
  references instead of live model/effort assignments throughout each prompt.
- `.claude/agents/code-generation-orchestrator.md`,
  `.claude/agents/consistency-auditor.md`, `.claude/agents/entity-builder.md`,
  `.claude/agents/entity-deployer.md`, `.claude/agents/migration-supervisor.md`,
  `.claude/agents/preconditions-gate-runner.md`,
  `.claude/agents/reconciliation-orchestrator.md` — generate selection fields.
- `docs/adr/0018-models-fill-configured-workflow-roles.md` — the one new ADR;
  keep its review pending until the decision PR's merge.
- `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`,
  `docs/adr/0011-stage-2-reviews-through-opencode-go.md`,
  `docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md`,
  `docs/adr/0017-codex-repairs-taken-findings.md` — add dated notices that
  concrete selections are historical and current assignments follow roles;
  preserve the original decision text and non-selection contracts.
- `plans/changes/central-models/spec.md`,
  `plans/changes/central-models/design.md`,
  `plans/changes/central-models/plan.md`,
  `plans/changes/central-models/findings.md`,
  `plans/changes/central-models/research.md` — maintain implementation status,
  test ledger, measured phase-4 time, gap findings and review evidence; do not
  rewrite interview answers or the explorer's returned text.
- `plans/INDEX.md` — runner-regenerated registry after artifact updates.

No files are deleted. Leave enforcement settings, the leak checker, Pi session
policy, user installation, other repositories, past change artifacts and the
decision-continuity map untouched. Do not translate unrelated existing text.

## Verification

Run `make venv` once in a new implementation worktree. Commands, verbatim:

```sh
.venv/bin/python -m pytest tests/test_model_routes.py tests/test_render_model_routes.py tests/test_stage2.py tests/test_stage2_session.py tests/test_stage2_runs.py tests/test_model_endpoints.py tests/test_templates.py tests/test_kit.py -q
python3 scripts/render_model_routes.py --write
python3 scripts/render_model_routes.py --check
python3 scripts/ci_gates.py --generate-ci
python3 scripts/plans_registry.py --index
python3 scripts/check_interview_minimums.py --change central-models
python3 scripts/check_criterion_ledger.py
make verify
```

The focused tests use client stand-ins: change a permitted model and effort,
assert actual argv, reorder permission lists independently of ladders, compare
two roots in one process and report a committed historical revision after a
working selection edit. Run generator tests against temporary copies, planting
stale fields and missing markers; assert exit code, diagnostic and no writes.
Keep full existing safety tests. No credentials or live provider probe is used.
The PR names the implementation commit and these commands as the special runs.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_changed_role_model_reaches_the_actual_client — preflight accepts the edit but argv still names the old model
- 1: not yet written tests/test_model_routes.py::test_two_roots_resolve_independent_selections_in_one_process — a module cache returns the first root's binding
- 2: not yet written tests/test_stage2.py::test_role_effort_reaches_each_supported_client — Codex, Claude or Pi receives a literal or another role's effort
- 3: not yet written tests/test_stage2.py::test_configured_primary_retry_fallback_and_stage1_bindings — a retry or explicit Stage-1 call ignores its binding
- 4: not yet written tests/test_model_routes.py::test_disallowed_or_incompatible_selection_is_refused — an undeclared model or incompatible transport/effort resolves
- 4: not yet written tests/test_stage2.py::test_invalid_selection_starts_no_client_or_fallback — a refusal invokes a client or advances the chain
- 5: not yet written tests/test_model_routes.py::test_malformed_ambiguous_or_incomplete_settings_report_the_fault — missing input, duplicate key, cycle or bad type defaults or raises unhandled
- 6: not yet written tests/test_render_model_routes.py::test_agent_model_and_effort_are_generated_without_job_changes — selection fields stay stale or tools/body change
- 7: not yet written tests/test_model_routes.py::test_named_ladders_are_independent_of_permission_order — endpoint-list order controls a ladder or distinct ladders are conflated
- 7: not yet written tests/test_stage2.py::test_loop_and_probe_use_configured_rung_selections — the second rung or probe uses a hardcoded model or effort
- 8: not yet written tests/test_model_routes.py::test_unconfigured_swarm_refuses_and_configured_members_resolve — an empty swarm invents members or a configured swarm cannot be selected
- 9: not yet written tests/test_stage2_session.py::test_session_suggestion_changes_without_launch_or_override — querying dispatches Terminal or overrides an explicit model
- 9: not yet written tests/test_stage2_session.py::test_explicit_session_effort_reaches_the_client — a suggested effort is dropped from the launch
- 10: not yet written tests/test_render_model_routes.py::test_both_tables_follow_changed_selections_idempotently — a table stays stale, a second write differs or outside prose changes
- 11: not yet written tests/test_render_model_routes.py::test_all_live_prompt_and_instruction_routes_resolve — a concrete independent assignment or unknown/missing reference passes
- 12: not yet written tests/test_render_model_routes.py::test_check_refuses_drift_and_missing_markers_without_writing — stale fields or missing markers exit zero or repair themselves
- 12: not yet written tests/test_render_model_routes.py::test_routing_gate_is_on_local_and_hosted_verify_paths — declaration or generated CI omits the check
- 13: not a test — phase-6 review compares ADR 0018 and the four amendment notices to Q-3; red if any effective contract still fixes a concrete selection or requires an ADR solely for a binding change
- 14: not yet written tests/test_kit.py::test_routing_bundle_is_complete_and_target_selections_stay_local — a dependency is absent or source permissions/bindings are inherited
- 15: not yet written tests/test_stage2_runs.py::test_revision_routes_ignore_working_settings_and_keep_old_counts — old-revision clearance follows today's config or old audit lines vanish
- 16: tests/test_stage2.py::test_a_leak_between_work_attempts_stops_before_fallback — leak refusal starts another attempt
- 16: tests/test_stage2.py::test_two_failed_postchecks_route_once_to_sonnet — the existing post-check chain changes (the historical test name stays)
- 16: tests/test_stage2_session.py::test_codex_is_dispatched_interactively_with_its_exact_safety_flags — session approval or sandbox flags weaken
- 16: tests/test_stage2.py::test_the_first_phase6_review_still_resumes_the_recorded_2a_session — centralization accidentally removes the existing first-review resume rule
- 16: tests/test_stage2.py::test_phase6_after_codex_repair_starts_a_fresh_read_only_session — a re-check resumes a repair or historical reviewer thread
- 16: not yet written tests/test_stage2.py::test_role_migration_keeps_review_freshness_permissions_and_round_limits — a same-model repair resumes a reviewer, review gains writes or a fourth/ungated third round starts

## Draft verification and resumption

The worktree has no `scripts/validate_change_artefacts.py` and no plan template;
the plan follows `prompts/03-plan.md` directly. The interview and criterion
ledger checks can run without the external tracker. Full registry/verify
measurement belongs to the runner: it regenerates `plans/INDEX.md` and renders
the tracker outside this draft's permitted read scope. Do not invent a render,
an ADR answer or another class to conceal a red or unmeasured gate.

Measured on 2026-10-14 at `e048fa4` plus these uncommitted draft artifacts:
`python3 scripts/check_interview_minimums.py --change central-models`,
`python3 scripts/check_criterion_ledger.py`,
`python3 scripts/check_frontmatter_current.py` and `git diff --check` passed.
Required metadata, the opening card and empty time section were also checked.
`python3 scripts/validate_change_artefacts.py --check` exited 2 because the
script is absent. The raw `python3 scripts/check_docs.py` exited 1 with 90
findings in existing documentation and none on the new ADR; its declared
`docs-links` gate is report-only. The registry index needs runner regeneration;
full registry and `make verify` have not been measured by this draft.

Resume with the runner's post-draft verification, then the independent spec
review if the orchestrator holds one; incorporate its rows before phase 4.
The plan card is for the orchestrator to show unchanged. No new approval is
needed for a card within these criteria, appetite and non-goals.

## Time used
