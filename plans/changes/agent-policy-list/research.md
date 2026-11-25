---
title: "Research — agent-policy-list"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-r7zc
owner: Data Architect
provenance: human-written
tags: [research]
class: bounded
neighbours: []
---

# agent policy list — Research

## Topic (bead coding-harness-r7zc)

Class: bounded. Measured 2026-11-25: the repository's layer-1 deny/ask rules (push to main, merges through gh pr merge and the GitHub API, codex, gh alias set, Omnigent tools) live only in .claude/settings.json; Antigravity (agy 1.5.14) does not read them, and its user settings carry a hand-maintained, different list. Omnigent is not involved (agy has no Omnigent MCP server). Build one source list in the repository (pattern of scripts/omnigent_policy.py) that (1) generates the permissions block of .claude/settings.json and (2) backs an Antigravity PreToolUse hook (.agents/hooks.json, matcher run_command) that answers deny or ask for the same commands, with ask turned into deny in an unattended run (as tools/claude-code/night.py does); a drift gate holds the generated files to the list. The enqueue script of the companion bead is the only allowed merge path. Needed before the 72-hour Antigravity run.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
