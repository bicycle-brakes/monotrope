---
title: "Plan — haiku-5-5"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-eao
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, models, haiku]
---

# Plan — haiku-5-5

```text
For you:     The current workflow selects Haiku 5.5 wherever it pins a Haiku version.
Done when:   The runner selects claude-haiku-5-5, declarations and instructions agree, and make verify including the kit probe is green.
Appetite:    1 hour of phase 4, including repairs; stop at the limit.
Not now:     Centralizing model names, rewriting dated records, changing unversioned aliases or checking provider availability.
Pre-mortem:  suppose it failed: most likely because the kit probe still expects the old parameterized case name.
Starts unless you say stop.
```

## Changes

- `tests/test_stage2.py`: first retarget the existing Stage-1 explore assertion and the explore-prompt expectation with its two matching fault examples to 5.5; assert the new audit line's model too, retaining the no-GLM-key and reason checks, and leave unrelated wrong-model fixtures intact.
- `scripts/stage2.py`: change `HAIKU` to `("claude-code-plan", "claude-haiku-5-5", None)` and update the module's versioned fallback description; other routes and behavior stay fixed.
- `model-endpoints.yaml`: replace the old Haiku id in both `anthropic-api` and `claude-code-plan`, preserving every other field and model id.
- `AGENTS.md`: replace Haiku 4.5 in the Stage-2 fallback paragraph.
- `docs/WORKFLOW.md`: replace the two §3 routing-table names and the three §4 fallback references, preserving unversioned alias guidance.
- `prompts/01-explore.md`: replace the Haiku fallback version in the Model paragraph.
- `prompts/07-commit.md`: replace the Haiku version in the Model paragraph.
- `scripts/kit/probe.py`: rename only the `REIST_NICHT` key ending `[07-commit.md-Haiku 4.5]` to `[07-commit.md-Haiku 5.5]`, keeping its reason, entry count and `DECKEL` unchanged.
- `plans/changes/haiku-5-5/plan.md`: record measured phase-4 time below; the runner owns route records, audit and check evidence in `plans/changes/haiku-5-5/findings.md`, metadata stamps and regeneration of `plans/INDEX.md`.

## Verification

Run `.venv/bin/python3 -m pytest -q tests/test_stage2.py::test_explore_stage2_off_uses_haiku_without_reading_the_glm_key tests/test_stage2.py::test_the_explore_prompt_names_the_live_flash_command_and_haiku_fallback` before production edits (red) and after them (green), then `.venv/bin/python3 -m pytest -q tests/test_model_endpoints.py tests/test_kit.py` and `make verify`; the last includes `python3 scripts/kit/probe.py --strict`.
Review the diff against all protected areas and confirm both declaration replacements and every operative prose reference; do not replace old names across the whole tree. Explore used Stage 2, `glm-coding-plan` / `glm-5.3-flash`, on 2026-10-14; no Stage-1 fallback record needs carrying forward.
The prompt's `python3 scripts/validate_change_artefacts.py --check` cannot run at drafting baseline `6c66c49`: that script is absent; do not add it in this change.

## Criterion ledger

- 1: tests/test_stage2.py::test_explore_stage2_off_uses_haiku_without_reading_the_glm_key — the command or new audit line names the old model; this existing test gains the audit assertion.
- 2: tests/test_model_endpoints.py::test_every_model_in_the_routing_table_resolves — the new table model has no declared endpoint.
- 2: not a test — phase-6 diff review checks both Anthropic lists; either retaining 4.5 or lacking 5.5 fails, even if the other list resolves the model.
- 3: tests/test_stage2.py::test_the_explore_prompt_names_the_live_flash_command_and_haiku_fallback — the explore prompt retains 4.5.
- 3: tests/test_model_endpoints.py::test_every_model_in_a_phase_prompt_resolves — the commit prompt retains a model removed from the declaration.
- 3: tests/test_model_endpoints.py::test_every_model_in_the_routing_table_resolves — a routing row retains a model removed from the declaration.
- 3: not a test — phase-6 review reads the remaining prose in AGENTS.md, WORKFLOW.md and the runner docstrings; any operative 4.5 instruction fails.
- 4: tests/test_kit.py::test_the_exemption_list_only_shrinks — the exception count or cap increases.
- 4: not a test — `python3 scripts/kit/probe.py --strict` fails on the stale 4.5 key or an unexplained 5.5 case.

## Time used
