---
title: "Decisions — codex-agents-writer"
category: decisions
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-xrcd
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, codex, agents, regelwerk]
---

# codex-agents-writer — Decisions

Class: bounded (bead coding-harness-xrcd). The interview ran in the conversation on 2026-11-22.

## Q-1 · What to do with the untracked .codex/agents/ definitions

asked: 2026-11-22
answer: C — commit the Codex TOML agent definitions now, together with the Regelwerk enforcer's TOML branch. Read by the orchestrator on 2026-11-23: the "TOML branch" is code, not a git branch — `docs/governance/regelwerk.md` (RB-A1 change note) says that when the Codex definitions under `.codex/agents/*.toml` land, the clause enforcer `tests/test_regelwerk.py::test_rb_a1_clause_is_present_verbatim` must grow a TOML reader, because the definitions embed the clause in `developer_instructions` and the current paragraph parser reads Markdown only; that extension belongs to the change that commits them.
answered_by: maintainer
status: answered
context: |
  Topic: the untracked .codex/agents/ folder that appears in lane worktrees.
  Intention: on 2026-11-18 an untracked copy of the main checkout's .codex/agents/ appeared in two lane worktrees and the runner refused to start there; the writer is outside the repositories (no script in coding-harness, portfolio-agentic-engineering or lakeswitch-ai references it).
  Today: the main checkout holds nine untracked TOML definitions whose text matches the tracked .claude/agents/*.md; stray copies are moved to the scratchpad by hand.
  Repository change: Options: A add .codex/agents/ to the shared local .git/info/exclude and keep looking for the writer; B keep moving stray copies by hand; C commit the TOML definitions now with the Regelwerk enforcer's TOML branch.
  Architecture change: the nine Codex agent definitions become tracked files held by the RB-A1 clause enforcer.

In the context of untracked Codex agent definitions that stop runner calls when copied into lanes, facing a local exclude, hand clean-up or committing them, we decided to commit them together with a TOML reader in the RB-A1 enforcer, to achieve wanted, checked files instead of strays, accepting a second format the enforcer must read. — 2026-11-22
