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

One repository policy supplies Claude Code's permissions and the command decisions for Antigravity (bead coding-harness-r7zc). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `e68a00e6`, Claude Code's permissions are split between generated Omnigent rules and hand-maintained command rules; Antigravity has no repository hook to apply the command rules. The research did not verify Antigravity's hook protocol or its user settings. Unattended Claude Code runs already convert asks to denies, but the research found no equivalent Antigravity path.

## Acceptance criteria

1. When the policy is rendered, Claude Code's deny and ask rules match the existing rules at commit `937cdec8` and have one authoritative source.
   *Refuted by:* a missing, extra or differently classified rule, or an independently maintained duplicate.
2. When permissions are rendered, unrelated settings and hooks remain unchanged.
   *Refuted by:* a changed SessionStart hook or unrelated setting.
3. When Antigravity invokes `run_command`, the hook returns the policy's deny or ask decision for each command covered by the existing Claude Code command rules.
   *Refuted by:* a covered command receives a weaker or different decision.
4. When Antigravity runs unattended, every command that the policy asks about is denied.
   *Refuted by:* an ask-covered command can proceed or waits for approval.
5. When a command matches no command rule, the Antigravity hook leaves the decision to the host.
   *Refuted by:* an unrelated command is denied or requires approval by this hook.
6. When generated settings or hook configuration drift from the policy, the repository verification fails.
   *Refuted by:* changing or removing a generated rule or hook configuration leaves verification green.
7. When the policy is regenerated, the existing Omnigent layer-two policy and Claude Code unattended overlay retain their present protection.
   *Refuted by:* an Omnigent denial or an unattended ask-to-deny conversion is lost.

## Non-goals

- A general shell security boundary or coverage of alternate spellings beyond the existing command rules; these rules remain brakes.
- Implementing the companion merge-queue enqueue script or changing the maintainer's merge authority.
- Applying Claude-only tool and file rules to Antigravity tools it does not expose, or changing user-level settings.

## Protected areas

Customer instances and user-level configuration are outside this change. Existing non-permission settings and the Omnigent layer-two protections remain intact.

## Definition of Done

- `make verify` green; the Antigravity hook protocol and both interactive and unattended behavior verified against the installed supported host, with the version and result recorded in the pull request.
- The policy documentation and generated configurations move with the code; no ADR changes.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes `coding-harness-r7zc` and its last commit carries `Closes-Bead: coding-harness-r7zc`.

## Open decisions

[DETAIL] An eight-hour implementation appetite provides a bounded stop; it is a revisable planning limit, not an estimate. The host's hook schema and unattended signal must be established from the supported host before implementation; do not invent either.
