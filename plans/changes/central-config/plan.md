---
title: "Plan — central-config"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-11
supersedes: null
superseded_by: null
bead: coding-harness-twvx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, configuration]
---

# Plan — central-config

```text
For you:     The existing writing-session limit has one source; prompts read it and a check keeps its displayed number current.
Done when:   Changed values reach the prompt, invalid data and drift fail checks, and make verify is green.
Appetite:    3 hours of phase 4 including repairs; stop when spent.
Not now:     Models, review rules, other limits and moving the three existing configuration files.
Pre-mortem:  suppose it failed: most likely because an old numeric statement is still treated as an independent source.
Starts unless you say stop.
```

Implements only the skeleton slice of `spec.md`, with the interfaces of
`design.md`; inspected baseline `7a027101`, 2026-11-10. No plan template exists
under `templates/`; this follows `prompts/03-plan.md` instead.

Explore fallback carried forward: Stage 1, endpoint `claude-code-plan`, model
`claude-haiku-5-5`, two explorations on 2026-11-10; reason: the research swarm's
reports failed their format check twice on 2026-11-09, as recorded in
`research.md`. There is no complete research-swarm/v2 handoff for this change.

## Files and steps

1. **Runner attempt — tests first.** Create `tests/test_harness_config.py`
   for strict loading, substitution and checker mutations in synthetic roots.
   Extend `tests/test_stage2.py` for the real implement prompt composition and
   pre-dispatch refusal, using stand-ins and the existing isolated fixtures.
   First demonstrate an assertion failure on a planted changed count reaching
   the prompt incorrectly; a missing-module error is not red-first evidence.
2. **Runner attempt — central contract.** Create `config/harness/lanes.yaml`
   with exactly `writing_sessions_per_repository: 2`, and
   `scripts/harness_config.py` with the sole schema and reader. Use existing
   PyYAML and Pydantic: strict frozen `LaneSettings` and `HarnessConfig`, extra
   fields forbidden, required positive integer with no default; safe UTF-8
   YAML parsing rejects duplicate/merge keys. Only `lanes.yaml` is a topic in
   this slice; reject other YAML topic files. `load(root)` returns an immutable
   snapshot and a dedicated error with path/key/reason for unusable inputs.
3. **Runner attempt — bindings.** In `scripts/harness_config.py`, add scalar
   lookup and literal substitution for `{{ harness.<dotted-key> }}`, rejecting
   unknown/malformed reserved tokens without executing template expressions.
   Store required binding paths/keys there, without numeric defaults. Create
   `scripts/check_harness_config.py` with `--root` and `--check`: validate data,
   require the registered marker/placeholder, compare prose values, and find
   numeric assignments to `writing_sessions_per_repository` or its uppercase
   spelling in live Python under `scripts/` and `tools/` (AST, including dict
   keys and annotated assignments). Exit 1 for drift, 3 for unreadable evidence;
   report path and binding. Tests/history are not duplicate-authority inputs.
4. **Runner attempt — runner integration.** Change `scripts/stage2.py` at
   `work_prompt`/its input-reading boundary to resolve the implement template
   before the normal `checked_prompt` call. Read configuration on demand when
   a reserved token occurs; prompts without migrated bindings retain their
   current behavior. Capture one immutable configuration per composition and
   include its bytes in the existing `inputs` snapshot/restoration mechanism.
   Translate loader/render errors into `Refused` before any model launch.
   Do not render arbitrary change inputs or model output. Recompose for the
   next call rather than keeping module-global configuration.
5. **Runner attempt — integration support.** Change `scripts/ci_gates.py`
   only to declare the imported `harness_config.py` helper in
   `OHNE_AUFRUFER` with its reader/renderer reason. Until the gate is registered,
   also declare `check_harness_config.py` there as the standalone checker
   awaiting held-path bootstrap; this temporary entry must be removed when
   its generated CI caller exists. The attempt's tests use
   synthetic prose/prompt files, since the real held inputs change only after
   acceptance. Leave real gate/kit assertions for the bootstrap step below;
   distinguish this interim result from the final repository check.
6. **Orchestrator bootstrap after the accepted attempt — held paths.** Change
   `prompts/04-implement.md` to state the session cap using the single reserved
   placeholder, with no enforcement promise. Change `AGENTS.md` only to wrap
   its existing default count with
   `<!-- harness-config: lanes.writing_sessions_per_repository -->2<!-- /harness-config -->`.
   Change `provenance.yaml` to classify `config/harness/` as editable values
   (`human-written`/`ai-drafted-reviewed`, no frontmatter); change
   `decisions/gates.yaml` to add blocking `harness-config` in the verify job,
   placement both, including the docs subset. Its command is
   `python3 scripts/check_harness_config.py --check`. Regenerate
   `.github/workflows/ci.yml` using
   `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`.
   Extend `tests/test_ci.py` at this bootstrap step for actual blocking gate
   presence, docs-subset membership and generated/local wiring; the new test
   must fail if the gate is removed or downgraded. The attempt is not asked
   to assert an unregistered gate on its own accepted tree.
   Remove the temporary checker entry from `scripts/ci_gates.py::OHNE_AUFRUFER`
   once generated CI calls it, retaining the imported reader's entry.
   Retain the already drafted `docs/adr/0026-one-central-harness-configuration.md`;
   any required ADR edit belongs to the orchestrator, never the implement attempt.
7. **Orchestrator bootstrap — packaging and explanation.** Change
   `scripts/kit/manifest.yaml` to classify `config/harness/`,
   `scripts/harness_config.py`, `scripts/check_harness_config.py` and
   `tests/test_harness_config.py` as mechanism; extend `tests/test_kit.py` here
   to hold those actual classifications. Change
   `scripts/export/manifest.yaml` to carry the configuration and two modules
   with exported instructions, so their checked source is present. Change
   `docs/WORKFLOW.md` with a brief central-configuration subsection covering
   the current owned setting, validation, placeholder/marker syntax, drift
   boundary and ordered migrations; do not replace model or other limit prose.
8. **Runner/orchestrator bookkeeping and final checks.** Update this
   `plans/changes/central-config/plan.md` ledger when tests exist and let the
   runner fill `## Time used`. The runner owns
   `plans/changes/central-config/findings.md`, generated `plans/INDEX.md`,
   verification and its checkpoint commit. After bootstrap edits, the
   orchestrator runs the final checks and opens a decision pull request using
   `.github/PULL_REQUEST_TEMPLATE/decision.md`; it names the central-config
   parent (bead coding-harness-twvx), without closing it. Keep code/wiring PRs
   below about 800 lines; if needed land this ADR/draft separately, then the
   executable skeleton. Stop at the three-hour appetite instead of starting
   models/routes. No other path is created, changed or deleted in this slice.

## Verification

On a fresh worktree first run `make venv` and `bash tools/pi/install.sh`.
The runner's interim attempt precedes held-path bootstrap; the orchestrator
must distinguish its result from final acceptance and rerun after bootstrap.

```bash
.venv/bin/python -m pytest -q tests/test_harness_config.py tests/test_stage2.py tests/test_ci.py tests/test_kit.py
.venv/bin/python scripts/check_harness_config.py --check
.venv/bin/python scripts/ci_gates.py --check-ci
.venv/bin/python scripts/check_interview_minimums.py --change central-config
.venv/bin/python scripts/check_research_handoff.py --change central-config
.venv/bin/python scripts/check_criterion_ledger.py
make verify
```

Mutations use temporary roots and stand-in dispatch only. Include the actual
checker subprocess against missing files, bad types, unknown topics, deleted
markers, changed prose, literalized placeholders and named constant copies;
assert nonzero exit and the diagnostic. Never edit real policy during a test.

## Criterion ledger

- 1: tests/test_harness_config.py::test_initial_session_limit_has_one_authority — missing source, a different initial count or a live duplicate is accepted.
- 2: tests/test_harness_config.py::test_one_schema_rejects_unknown_topics_keys_and_bad_counts — an extra topic/key or bool/string/non-positive count is accepted.
- 3: tests/test_harness_config.py::test_unusable_config_has_path_and_reason_without_defaults — malformed, missing, unreadable, duplicate-key or merge-key input yields usable settings.
- 3: tests/test_stage2.py::test_invalid_central_config_refuses_before_implement_dispatch — the stand-in is called or the error lacks the configuration path.
- 4: tests/test_harness_config.py::test_prompt_render_uses_one_snapshot_and_refreshes_next_time — an intervening edit changes the captured view or the next render stays stale.
- 4: tests/test_harness_config.py::test_unknown_or_malformed_reserved_placeholder_refuses — an unresolved reserved token survives or an expression executes.
- 5: tests/test_stage2.py::test_implement_prompt_uses_central_session_limit_before_leakcheck — a changed count is ignored or the exact resolved outgoing text is not checked.
- 5: tests/test_stage2.py::test_attempt_snapshot_restores_central_prompt_inputs — an attempt changes its own configuration input without restoration.
- 6: tests/test_harness_config.py::test_checker_rejects_stale_missing_or_unknown_prose_bindings — changed prose or a deleted/invalid required marker passes the real checker.
- 7: tests/test_harness_config.py::test_checker_rejects_named_duplicates_and_literalized_prompt — a canonical/uppercase numeric assignment or lost registered placeholder passes.
- 8: tests/test_ci.py::test_central_config_gate_blocks_locally_and_in_generated_ci — invalid configuration can bypass one verification path.
- 9: not a test — phase-6 review compares the final path list and ADR/design sequence with Q-4/Q-5; moving an old declaration or claiming all migrations done refutes it.

## Not touched

`model-endpoints.yaml`, `research-swarm-limits.yaml`, existing ADRs, decision
answers, endpoint/leak policies, review-loop rules, verify-lock behavior,
metrics and other consumers stay as they are. The gate list is extended at
its existing path, never moved or unreserved. Later slices need their own
reader inventories, file lists, criteria and plan cards; they are not phase-4
instructions in this plan. The tracker stays with the orchestrating session.

## Runner route — 2026-11-10

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-10

Stage-1 route: implement · model claude-sonnet-5-5 · reason: three attempts failed on 2026-11-10; one more attempt from the kept tree on the maintainer's instruction to give every lane a task.

## Time used

2026-11-10 13:25:37–15:43:33 UTC, 8275 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-10 15:44:14–17:43:30 UTC, 7156 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-10 17:43:45–19:03:53 UTC, 4807 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-10 22:06:47–2026-11-11 00:37:19 UTC, 9031 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
