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
For you: Claude Code and Antigravity consult the same permission rules, including unattended runs.
Done when: rule, adapter, launcher and drift tests pass and the one-time host check is documented.
Appetite: 8 hours for phase 4, including repairs; stop at the limit.
Not now: a general shell security boundary, a Codex adapter or the companion merge-queue script.
Pre-mortem: suppose it failed: most likely because a host cannot enforce the hook's decision.
Starts unless you say stop.
```

## Steps and files

1. Establish host versions, pre-tool input and output, registration and failure behavior from host documentation and controlled probes. `docs/WORKFLOW.md` records a host support table, the one-time checks for timeout and abnormal exit (including any holding second layer), user-settings boundary, launcher and reinstall instructions; the orchestrator creates the Codex follow-up bead and names it there. Do not claim support without evidence.
2. Add `scripts/agent_policy.py`: read `scripts/merge_guard.py` and `scripts/omnigent_policy.py` as existing sources; own the remaining rules including both Python spellings of enqueue maintainer mode; normalise MCP merge names, split unquoted shell operators, recursively check the command strings of bash, sh and zsh `-c`, and combine decisions by strength. Update those two source scripts only as needed, preserving their existing behavior.
3. Add `scripts/agent_policy_hooks.py` for thin Claude Code and Antigravity adapters using verified host protocols. Fail closed with a fault when able to respond, convert asks when unattended or unsupported by the host, and abstain for successful unmatched inputs. Update `tools/claude-code/night.py` to set `HARNESS_UNATTENDED=1` for its child; add `tools/antigravity/night.py` as the unattended launcher setting the same child environment.
4. The policy module generates Claude permissions and both hook registrations, including command, matcher and timeout; its drift check compares those fields and the permissions. After the accepted attempt, the orchestrator alone generates `.claude/settings.json` and `.agents/hooks.json`, preserving unrelated settings. Do not create a Codex hook. The orchestrator alone edits the held `docs/WORKFLOW.md` if its provenance requires it.
5. Add `tests/test_agent_policy.py` for the shared rules, both adapters, quoting, nested shell commands, environment values, failures, registration and drift. Update `tests/test_merge_guard.py`, `tests/test_omnigent_deny_layers.py` and `tests/test_night_profile.py` as needed; add launcher coverage there or in the new test. Update `Makefile` if needed to include the drift check in verification.
6. Run `make verify`. Do not edit user settings, customer instances, `.codex/hooks.json`, the companion enqueue script or ADRs. Held paths are exclusively the orchestrator's bootstrap edits after the accepted attempt.

Explore fallback: Stage 1, Claude Haiku 5.5 (`claude-haiku-5-5`), because GLM through Z.ai was at its weekly limit until 2026-11-29 (research, 2026-11-25).

## Criterion ledger

- 1: not yet written tests/test_agent_policy.py::test_rule_sources_preserve_permissions — a rule is missing, duplicated or reclassified.
- 2: not yet written tests/test_agent_policy.py::test_render_preserves_unrelated_settings — an unrelated setting changes.
- 3: not yet written tests/test_agent_policy.py::test_adapters_match_shared_check — an adapter disagrees for shell or MCP input.
- 4: not yet written tests/test_agent_policy.py::test_mcp_merge_names_normalised — an alternative separator abstains.
- 5: not yet written tests/test_agent_policy.py::test_compound_parts_use_strongest_decision — a covered part is ignored or deny weakened.
- 6: not yet written tests/test_agent_policy.py::test_quoted_operators_do_not_split — quoted text is treated as a command.
- 7: not yet written tests/test_agent_policy.py::test_shell_c_command_is_checked — a nested merge abstains.
- 8: not yet written tests/test_agent_policy.py::test_unattended_asks_are_denied — an unattended ask is not denied.
- 9: not yet written tests/test_agent_policy.py::test_attended_environment — unset, empty or zero alone causes denial.
- 10: not yet written tests/test_agent_policy.py::test_claude_night_child_environment — the child lacks the signal.
- 11: not yet written tests/test_agent_policy.py::test_antigravity_night_child_environment — the child lacks the signal.
- 12: not yet written tests/test_agent_policy.py::test_unmatched_input_abstains — an unrelated input is blocked.
- 13: not yet written tests/test_agent_policy.py::test_generated_configuration_drift_fails — altered rules or registration fields pass.
- 14: not yet written tests/test_agent_policy.py::test_layer_two_and_night_protection — a deny, layer-two ask or overlay conversion is lost.
- 15: not yet written tests/test_agent_policy.py::test_failures_deny_with_fault — a caught fault passes or lacks a message.
- 16: not yet written tests/test_agent_policy.py::test_unrepresentable_ask_denies — a host without ask receives abstain.
- 17: not a test — the documented host check proves timeout and abnormal-exit protection or marks the host unsupported; a passing action or missing evidence refutes support.
- 18: not a test — phase-6 review checks the support table names Codex unsupported and its follow-up bead; a missing state or bead refutes it.

## Time used

2026-11-25 14:47:26–14:49:01 UTC, 96 s — draft · attempt 2 · route codex-repair · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 15:24:33–15:26:29 UTC, 116 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 16:01:10–16:03:29 UTC, 139 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
