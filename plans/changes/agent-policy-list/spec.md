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

One harness-neutral policy check supplies consistent decisions to Claude Code and Antigravity (bead coding-harness-r7zc). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `e68a00e6`, Claude Code's permissions are split between generated Omnigent rules and hand-maintained command rules; the repository has no Antigravity permission hook. The research did not verify Antigravity's hook protocol or user settings. Claude Code's unattended overlay converts asks to denies, but no equivalent Antigravity path was found.

## Acceptance criteria

1. When the policy check reads rules, it uses the existing merge and Omnigent sources and one source for each remaining rule, preserving the Claude Code deny and ask rules at commit `937cdec8` and adding the maintainer-mode enqueue rules recorded in `decisions.md`.
   *Refuted by:* a missing, extra, duplicated or reclassified rule.
2. When Claude Code permissions are generated, unrelated settings and hooks remain unchanged.
   *Refuted by:* a changed SessionStart hook or unrelated setting.
3. When a Claude Code or Antigravity adapter receives a shell command or an MCP tool name ending in `merge_pull_request`, it returns the shared check's decision.
   *Refuted by:* an adapter disagrees for a covered input.
4. When an MCP tool name ends in `merge_pull_request`, regardless of separator, its adapter normalises it to the existing merge ask rule.
   *Refuted by:* `github.merge_pull_request` or `github_merge_pull_request` abstains.
5. When a shell line contains unquoted `&&`, `||`, `;` or `|`, the check evaluates every part and applies the strongest decision: deny, then ask, then abstain.
   *Refuted by:* `cd /repo && gh pr merge 54` abstains or a deny is weakened by another part.
6. When an operator occurs inside shell quotes, it does not split the enclosing line.
   *Refuted by:* `git commit -m "docs; git push origin main later"` is treated as a push.
7. When `bash -c`, `sh -c` or `zsh -c` receives a command string, the check evaluates that string as a command line.
   *Refuted by:* `bash -c "cd /repo && gh pr merge 54"` abstains.
8. When `HARNESS_UNATTENDED` is nonempty and differs from `0`, each adapter converts ask to deny.
   *Refuted by:* an ask remains ask for `1` or `true`.
9. When `HARNESS_UNATTENDED` is unset, empty or `0`, the adapter treats the run as attended.
   *Refuted by:* an ask becomes deny solely due to one of these values.
10. When Claude Code's night launcher starts its child, it sets `HARNESS_UNATTENDED=1`.
    *Refuted by:* the child environment lacks that value.
11. When the repository's Antigravity unattended launcher starts the run, it sets `HARNESS_UNATTENDED=1` for its child.
    *Refuted by:* the child environment lacks that value.
12. When an input matches no rule and the check succeeds, the adapter abstains.
    *Refuted by:* a successful check blocks an unrelated command.
13. When generated permissions or either generated hook registration's command, matcher or timeout differs from its policy-module source, repository verification fails.
    *Refuted by:* an altered or missing rule, command, matcher or timeout passes the drift check.
14. When policy output is regenerated, Omnigent's layer-two deny and ask policies and Claude Code's unattended overlay retain their protection.
    *Refuted by:* a denial, the `sys_advise_models` layer-two ask, or an overlay conversion is lost or weakened.
15. If policy reading, input parsing or adapter execution fails while the adapter can respond, it denies and identifies the fault.
    *Refuted by:* malformed input, unreadable policy or a caught exception produces abstain or an unexplained denial.
16. If a host cannot express ask, its adapter returns deny for an ask decision.
    *Refuted by:* an ask produces abstention on that host.
17. When policy documentation declares a host supported, a documented host check establishes that timeout and abnormal hook exit are blocked by the host or a holding second layer.
    *Refuted by:* support is claimed without that evidence or a covered action passes either failure.
18. When policy documentation lists host support, it identifies Codex as unsupported and names a follow-up bead for its missing verified pre-tool hook.
    *Refuted by:* Codex is presented as supported or the follow-up is absent.

## Non-goals

- A general shell security boundary, general shell syntax beyond the named operators, quoting and named shell `-c` forms, or alternate spellings beyond the existing rules.
- The companion merge-queue enqueue script or a change to maintainer merge authority.
- Changing user-level settings, covering file-writing tools, or building a Codex adapter without a verified pre-tool hook.

## Boundary

Tests establish check and adapter output for supplied input, not effective host behavior after user-level settings. File-writing tools are outside these hooks. The pull request documents a one-time host check with host versions, registration, unattended mode, timeout and abnormal exit, including whether any second layer holds the covered actions. Support is not claimed without that evidence. Reinstalling Claude Code's launcher into user configuration is the maintainer's step.

## Protected areas

Customer instances and user-level configuration are outside this change. Existing unrelated settings and Omnigent layer-two protections remain intact.

## Definition of Done

- `make verify` green; host check and its limits recorded in the pull request.
- Policy documentation and generated configurations move with the code; no ADR changes.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes `coding-harness-r7zc` and its last commit carries `Closes-Bead: coding-harness-r7zc`.

## Open decisions

[DETAIL] Eight hours is a revisable stop. Empty `HARNESS_UNATTENDED` is treated as unset; a nonempty value other than `0` fails toward deny. The repository supplies an Antigravity unattended launcher so the signal has a named owner. The generator owns both registrations so their command, matcher and timeout can be checked for drift. These choices make the recorded decisions testable without changing their intent.
