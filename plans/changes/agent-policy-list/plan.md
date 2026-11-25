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
For you: Claude Code, Codex and Antigravity consult the same permission rules, including unattended runs.
Done when: rule, adapter and drift tests pass and the one-time host check is documented.
Appetite: 8 hours for phase 4, including repairs; stop at the limit.
Not now: a general shell security boundary or the companion merge-queue script.
Pre-mortem: suppose it failed: most likely because a host cannot enforce the hook's decision.
Starts unless you say stop.
```

## Steps and files

1. Establish supported host versions, hook input and output, registration and timeout behavior from host documentation or controlled probes; document the one-time host check and any unsupported host in `plans/changes/agent-policy-list/findings.md`. Stop claiming support where denial on timeout cannot be established.
2. Add `scripts/agent_policy.py` as the shared check command: read `scripts/merge_guard.py` and `scripts/omnigent_policy.py` as the existing rule sources, give remaining rules one source, split the named shell operators, combine decisions by strength, and fail closed. Update those two existing scripts only as needed to expose their rules and preserve their present layer-two and merge behavior.
3. Add `scripts/agent_policy_hooks.py` with thin Claude Code, Codex and Antigravity adapters using the verified host protocols; translate ask to deny when unsupported or `HARNESS_UNATTENDED=1`, abstain only after a successful unmatched check, and report faults. Update `tools/claude-code/night.py` to set that variable for its launched process while retaining its overlay.
4. After the accepted attempt, the orchestrator alone generates `.claude/settings.json`, updates `.codex/hooks.json` preserving existing hooks, and creates `.agents/hooks.json`; held paths are never assigned to the implementation attempt. Generate Claude permissions without changing unrelated settings, and wire every relevant shell and MCP merge event supported by each host to the adapter. Document registration, launcher signal, limitations and the host check in `docs/WORKFLOW.md`.
5. Add `tests/test_agent_policy.py` for policy, adapters, failures and drift; update `tests/test_merge_guard.py`, `tests/test_omnigent_deny_layers.py`, and `tests/test_night_profile.py` where existing assertions need the shared reader. Update `Makefile` if needed to run the drift check during verification.
6. Run `make verify`. Do not edit user settings, customer instances, the companion enqueue script or ADRs. The orchestrator handles all held paths and their verification.

Explore fallback: Stage 1, Claude Haiku 5.5 (`claude-haiku-5-5`), because GLM through Z.ai was at its weekly limit until 2026-11-29 (research, 2026-11-25).

## Criterion ledger

- 1: not yet written tests/test_agent_policy.py::test_rule_sources_preserve_permissions — a rule is missing, duplicated or reclassified.
- 2: not yet written tests/test_agent_policy.py::test_render_preserves_unrelated_settings — an unrelated setting changes.
- 3: not yet written tests/test_agent_policy.py::test_adapters_match_shared_check — an adapter disagrees for shell or MCP merge input.
- 4: not yet written tests/test_agent_policy.py::test_compound_parts_use_strongest_decision — a covered part is ignored or a deny weakened.
- 5: not yet written tests/test_agent_policy.py::test_unattended_asks_are_denied — an adapter emits ask or abstain.
- 6: not yet written tests/test_agent_policy.py::test_unmatched_input_abstains — an unrelated input is blocked.
- 7: not yet written tests/test_agent_policy.py::test_generated_configuration_drift_fails — altered or missing generated content passes.
- 8: not yet written tests/test_agent_policy.py::test_layer_two_and_night_protection — a deny, layer-two ask or overlay conversion is lost.
- 9: not yet written tests/test_agent_policy.py::test_failures_deny_with_fault — malformed input, unreadable policy or exception passes or lacks a fault message.
- 10: not yet written tests/test_agent_policy.py::test_unrepresentable_ask_denies — a host without ask receives abstain.
- 11: not a test — the documented host check establishes timeout enforcement before support is claimed; a host that permits on timeout is marked unsupported.

## Time used

2026-11-25 14:47:26–14:49:01 UTC, 96 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 15:24:33–15:26:29 UTC, 116 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
