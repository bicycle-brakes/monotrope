---
title: "Spec — agent-policy-list"
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
tags: [spec, permissions]
class: bounded
appetite: 8
adr_files: []
neighbours: []
---

# Spec — agent-policy-list

One harness-neutral policy check supplies consistent decisions to Claude Code, Codex and Antigravity (bead coding-harness-r7zc). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `e68a00e6`, Claude Code's permissions are split between generated Omnigent rules and hand-maintained command rules; the repository has no Antigravity permission hook. The research did not verify Antigravity's hook protocol or user settings. Claude Code's unattended overlay converts asks to denies, but no equivalent Antigravity path was found.

## Acceptance criteria

1. When the policy check reads rules, it uses the existing merge and Omnigent sources and a single source for each remaining rule, preserving the Claude Code deny and ask rules at commit `937cdec8`.
   *Refuted by:* a missing, extra or reclassified rule or an independently maintained duplicate.
2. When Claude Code permissions are generated, unrelated settings and hooks remain unchanged.
   *Refuted by:* a changed SessionStart hook or unrelated setting.
3. When any of the three harness adapters receives a shell command or an MCP tool name ending in `merge_pull_request`, it returns the shared check's decision for that input.
   *Refuted by:* an adapter returns a different decision for a covered input.
4. When a shell line contains parts separated by `&&`, `||`, `;` or `|`, the check evaluates every part and applies the strongest decision to the whole line, with deny stronger than ask and ask stronger than abstain.
   *Refuted by:* `cd /repo && gh pr merge 54` or `git add . && git push origin main` abstains, or a deny is weakened by another part.
5. When `HARNESS_UNATTENDED=1`, an ask decision becomes deny in each adapter.
   *Refuted by:* a covered ask produces ask or abstain in unattended mode.
6. When an input matches no rule and the check succeeds, the adapter abstains.
   *Refuted by:* a successful check blocks an unrelated command.
7. When generated permissions or hook registration drift from their sources, repository verification fails.
   *Refuted by:* a changed or missing generated rule or hook registration passes the drift check.
8. When policy output is regenerated, the existing Omnigent layer-two deny and ask policies and Claude Code's unattended ask-to-deny overlay retain their protection.
   *Refuted by:* a denial, the `sys_advise_models` layer-two ask, or an overlay conversion is lost or weakened.
9. If policy reading, input parsing or adapter execution fails, the adapter denies and identifies the fault.
   *Refuted by:* malformed input, unreadable policy or an exception produces abstain or an unexplained denial.
10. If a host cannot express ask, its adapter returns deny for an ask decision.
    *Refuted by:* a host without ask support receives an abstention for an ask rule.
11. If a host cannot enforce denial on hook timeout, the integration is not declared supported.
    *Refuted by:* support is claimed although a timed-out hook can permit a covered action.

## Non-goals

- A general shell security boundary, shell syntax beyond the named operators, or alternate spellings beyond the existing rules.
- The companion merge-queue enqueue script or a change to maintainer merge authority.
- Changing user-level settings or covering file-writing tools.

## Boundary

Tests establish check and adapter output for supplied input, not effective host behavior after user-level settings. File-writing tools are outside these hooks. A one-time host check on the maintainer's machine is documented in the pull request with host versions, registration, unattended mode and timeout behavior; if host behavior cannot be established, support is not claimed.

## Protected areas

Customer instances and user-level configuration are outside this change. Existing unrelated settings and Omnigent layer-two protections remain intact.

## Definition of Done

- `make verify` green; host check and its limits recorded in the pull request.
- Policy documentation and generated configurations move with the code; no ADR changes.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes `coding-harness-r7zc` and its last commit carries `Closes-Bead: coding-harness-r7zc`.

## Open decisions

[DETAIL] The eight-hour appetite is a revisable stop. The launcher sets `HARNESS_UNATTENDED=1`; absence means attended. Deny is used when ask cannot be represented, and failures deny, because silently allowing an unchecked action would lose the brake. Host timeout enforcement must be verified rather than assumed.
