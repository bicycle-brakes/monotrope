---
title: "Research — enqueue-pr"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-va1l
owner: Data Architect
provenance: human-written
tags: [research]
class: bounded
neighbours: []
---

# enqueue pr — Research

## Topic (bead coding-harness-va1l)

Class: bounded. Maintainer grant 2026-11-25 (AGENTS.md, PR #459): the orchestrator admits a pull request to the merge queue itself once phase 6 is clean, make verify is green on its head and its last commit carries Closes-Bead. Today the grant is prose and gh pr merge stays 'ask' in .claude/settings.json and in Antigravity, so an unattended run cannot use it. Build scripts/enqueue_pr.py <number>: refuse unless (1) the PR targets main and is open, (2) the change's newest phase-6 table in plans/changes/<change>/findings.md has no open row (or reports no finding), (3) every required check on the PR head is SUCCESS, (4) the head commit carries a Closes-Bead trailer naming an existing bead; then run gh pr merge <number> --merge (admission to the merge queue only, never --admin, never a direct merge). Every refusal names the failing condition. Harness-neutral: Claude Code, Codex and Antigravity allow only this script; a direct gh pr merge stays ask (deny at night). Needed before the 72-hour Antigravity run.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
