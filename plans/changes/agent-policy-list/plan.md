---
title: "Plan — agent-policy-list"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-r7zc
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, permissions]
---

# Plan — agent-policy-list

```text
For you: Claude Code and Antigravity use the same command policy, including unattended runs.
Done when: drift and behavior tests pass and the installed Antigravity hook is verified.
Appetite: 8 hours for phase 4, including repairs; stop at the limit.
Not now: a general shell security boundary or the companion merge-queue script.
Pre-mortem: suppose it failed: most likely because Antigravity's actual hook protocol differs from the assumed interface.
Starts unless you say stop.
```

## Steps and files

1. Establish the installed Antigravity version, hook input/output schema, registration and unattended signal from its supported documentation or a controlled local probe; record evidence in `plans/changes/agent-policy-list/findings.md`. If these cannot be established, stop rather than claim host enforcement.
2. Implement the single source and command matcher in new `scripts/agent_policy.py`; preserve the exact current rule set and use the existing merge matching semantics. Update `scripts/omnigent_policy.py` and `scripts/merge_guard.py` to consume that source without a second writer or independently maintained permissions list; keep Omnigent's layer-two generation and existing merge samples.
3. Add `scripts/antigravity_policy_hook.py` to translate the verified host input and output to policy decisions, including the verified unattended signal. Unmatched commands abstain; malformed host input must not silently authorize a covered call.
4. The orchestrator generates `.claude/settings.json` and `.agents/hooks.json` after the accepted implementation attempt; these held paths never go to the implementer. Preserve existing unrelated settings. Add policy operation and host-mode instructions in `docs/WORKFLOW.md`.
5. Add `tests/test_agent_policy.py` for generation, command decisions, drift and hook protocol; update `tests/test_merge_guard.py`, `tests/test_omnigent_deny_layers.py`, and `tests/test_night_profile.py` for the single source and preserved protections. Wire drift checking into `Makefile` if not already collected by verification. Confirm the actual installed host invokes the hook in both modes; record version, commands and results in `findings.md`.
6. Run `make verify` and resolve failures; the orchestrator handles held files and their checks. Do not edit user settings, the companion enqueue script, ADRs or customer instances.

Explore fallback: Stage 1, Claude Haiku 5.5 (`claude-haiku-5-5`), because GLM through Z.ai was at its weekly limit until 2026-11-29 (research, 2026-11-25).

## Criterion ledger

- 1: not yet written tests/test_agent_policy.py::test_existing_rules_have_one_source — a rule is missing, added or classified differently.
- 2: not yet written tests/test_agent_policy.py::test_render_preserves_unrelated_settings — a hook or unrelated setting changes.
- 3: not yet written tests/test_agent_policy.py::test_hook_matches_command_policy — a covered command gets the wrong decision.
- 4: not yet written tests/test_agent_policy.py::test_unattended_asks_are_denied — an ask remains interactive or permits execution.
- 5: not yet written tests/test_agent_policy.py::test_unmatched_command_abstains — an unrelated command is blocked.
- 6: not yet written tests/test_agent_policy.py::test_generated_configuration_drift_fails — altered or missing generated content passes.
- 7: not yet written tests/test_agent_policy.py::test_existing_layer_two_and_night_protection — regeneration loses a protection.

## Time used

2026-11-25 14:47:26–14:49:01 UTC, 96 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
