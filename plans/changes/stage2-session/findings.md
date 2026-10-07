---
title: "Findings — stage2-session"
category: findings
status: draft
implementation_status: none
date: 2026-10-07
created: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-amp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — stage2-session

Stage-2 call, 2026-10-07: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 270 files, 607 commits, 12 rules.

## Phase 2a — Codex, 2026-10-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `spec.md:44–51,74–85,113–117`; `research.md:58–61` | [GAP] No accepted OpenCode model or provider/model mapping is identified. Research reports no OpenCode declaration; undeclared transports must be refused, and new endpoint approvals are excluded. Only PR #89 is a prerequisite. Implementing the OpenCode path therefore requires an unstated declaration dependency or an invented supported-model contract; no permitted positive OpenCode invocation is specified. | Codex | in spec — Supported models and prerequisites: existing Codex positive path; OpenCode Go activation depends on the separately approved declaration, with fixture-only positive tests until then | — |
| F-2 | MAJOR | SPEC | base | `spec.md:37–38,66–77` | [AMBIGUITY] Consider Terminal accepting the command while its shell cannot find the CLI. Reading “Dispatch” as terminal acceptance produces success and a successful-dispatch audit. Reading AC8’s missing-executable refutation as requiring executable startup produces failure and a failed-dispatch audit. The spec gives these different outcomes for the same launch state without defining which boundary determines success. | Codex | open | — |
| F-3 | MAJOR | SPEC | base | `spec.md:44–47` | [GAP] The association between a change and its dedicated worktree is undefined. Two attached, non-main linked worktrees can contain the same tracked change directory, so resolving that directory within the current root does not identify which worktree belongs to the change. For an invocation from the other change’s worktree, the implementer must invent the association that determines acceptance or refusal. | Codex | in spec — Supported models and prerequisites fixes the canonical main-checkout/.claude/worktrees/change association and attached-branch requirement | — |

Reviewer session: codex 01a116cd-d624-7ee0-9e14-3db0027c8eff
