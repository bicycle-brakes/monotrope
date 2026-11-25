---
title: "Research — worktree-setup-hook"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-wg4z
owner: Data Architect
provenance: human-written
tags: [research]
class: bounded
neighbours: []
---

# worktree setup hook — Research

## Topic (bead coding-harness-wg4z)

Class: bounded. 2026-11-25: a new lane worktree lacked .venv and the pinned Pi; scripts/new_change.py failed with 'No module named yaml' and the rule lived only in tracker memory new-worktree-needs-pi (2026-11-22: about 110 tests fail without Pi). Extend the versioned hook .beads/hooks/post-checkout (core.hooksPath), outside the managed beads section: when git runs it for a new worktree (previous HEAD is the null SHA, branch checkout flag 1), run make venv and bash tools/pi/install.sh in that worktree, then a short check (the venv imports yaml, tools/pi/pi --version matches the pin); on failure print a loud message naming the step, without failing the checkout. HARNESS_NO_LANE_SETUP=1 skips it. The runner adds no worktrees itself (measured: no 'worktree add' in scripts/). Harness-neutral: Claude Code, Codex and Antigravity get set-up worktrees. Then retire memory new-worktree-needs-pi in favour of the hook.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
