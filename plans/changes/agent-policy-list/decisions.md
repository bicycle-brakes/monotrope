---
title: "Decisions — agent-policy-list"
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
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, permissions, antigravity, harness-neutral]
---

# agent-policy-list — Decisions

## SKIP · interview

status: skipped
reason: The maintainer decided the direction in the conversation of 2026-11-25 (session 9200c6b1): one policy list in the repository generates Claude Code's deny/ask rules and backs an Antigravity PreToolUse hook, ask becomes deny in an unattended run; asked 'Ok, leg los'. The bead (coding-harness-r7zc) states the scope; no open human intent question remains.

## Q-1 · Ambiguity S-1 (one list across harnesses)

asked: 2026-11-25
answer: "The list must work with all common harnesses. One harness-neutral check command reads every rule source; thin hooks for Claude Code, Codex and Antigravity call it, further harnesses later with the same command; the existing sources stay, ADR 0008 stays true."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-1 of agent-policy-list.
  Intention: one truth for every harness.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/agent-policy-list/spec.md in the final draft.
  Architecture change: none.

In the context of the rule sources for agent permissions, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting per-harness adapters to maintain. — 2026-11-25

## Q-2 · Ambiguity S-2 (compound command lines)

asked: 2026-11-25
answer: "Check every part of a compound line, split at shell operators."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-2 of agent-policy-list.
  Intention: close compound-line bypasses.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/agent-policy-list/spec.md in the final draft.
  Architecture change: none.

In the context of compound command lines, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting a small shell splitter. — 2026-11-25

## Q-3 · Ambiguity S-3 (what the tests prove)

asked: 2026-11-25
answer: "The tests prove the hook output for given input; the host's user settings are a named Boundary, with a one-time documented host check."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-3 of agent-policy-list.
  Intention: reproducible tests in CI.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/agent-policy-list/spec.md in the final draft.
  Architecture change: none.

In the context of testing host-installed hooks, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting that user-level settings stay outside the proof. — 2026-11-25

## Q-4 · Ambiguity S-4 (which tools the hook checks)

asked: 2026-11-25
answer: "Shell commands plus every MCP tool whose name ends in merge_pull_request; file writers stay a named Boundary."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-4 of agent-policy-list.
  Intention: cover the merge paths an agent can reach.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/agent-policy-list/spec.md in the final draft.
  Architecture change: none.

In the context of tool coverage of the hook, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting file-writing tools outside the hook. — 2026-11-25

## Q-5 · Ambiguity S-8 (MCP merge tool names)

asked: 2026-11-25
answer: "Every tool name ending in merge_pull_request, whatever the separator; each adapter normalises the host's name; the rule list stays unchanged."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-8 of agent-policy-list.
  Intention: cover MCP merges on every host.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/agent-policy-list/spec.md in the final draft.
  Architecture change: none.

In the context of MCP merge tools across hosts, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting name normalisation in each adapter. — 2026-11-25

## Q-6 · Ambiguity S-9 (quotes in compound lines)

asked: 2026-11-25
answer: "Split as the shell reads it; quoted operators do not split; the argument of bash -c, sh -c and zsh -c is checked as a command line of its own."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-9 of agent-policy-list.
  Intention: catch hidden merges without blocking harmless text.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/agent-policy-list/spec.md in the final draft.
  Architecture change: none.

In the context of compound command lines with quotes, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting a quote-aware splitter. — 2026-11-25

## Q-7 · Ambiguity S-10 (hook failure and support)

asked: 2026-11-25
answer: "A host counts as supported when it blocks on a hook failure or has a holding second layer; without one, a one-time documented host check."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-10 of agent-policy-list.
  Intention: an honest support claim per host.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/agent-policy-list/spec.md in the final draft.
  Architecture change: none.

In the context of hosts that continue after a hook failure, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting a host check outside CI. — 2026-11-25

## Q-8 · Gap S-11 (hosts without a verified pre-tool hook)

asked: 2026-11-25
answer: "Build adapters only for hosts with a verified pre-tool hook (Claude Code, Antigravity); Codex is listed as not supported with a follow-up bead; one table in the policy documentation names every host's state."
answered_by: maintainer
status: answered
context: |
  Topic: spec-review round 1 row S-11 of agent-policy-list.
  Intention: ship only what is proven.
  Today: the draft spec left two readings open.
  Repository change: plans/changes/agent-policy-list/spec.md in the final draft.
  Architecture change: none.

In the context of hosts whose hook surface is unverified, facing two readings that build differently, we decided as answered above, to achieve one testable reading for the final draft, accepting Codex outside this change. — 2026-11-25

## Details decided by the orchestrator (cross-lane, 2026-11-25)

[DETAIL] Companion change enqueue-pr (coding-harness-va1l, Q-8): the policy list holds one more rule, `python3 scripts/enqueue_pr.py * --maintainer*` (and the `.venv/bin/python` spelling) as ask; in an unattended run the ask becomes deny like every other ask, so only the maintainer can use the maintainer mode. The default call `scripts/enqueue_pr.py <number>` is allowed.

## Details decided by the orchestrator (spec-review round 1)

[DETAIL] Round-3 spec review (S-16..S-20) decided by the orchestrator under the maintainer's standing grant for bounded changes (2026-11-25: answer spec-review questions except BLOCKERs, recorded here). No further redraft: the spec stays as reviewed in round 3 so the review stays current; the implementer applies the S-16..S-20 statuses in findings.md as written.
