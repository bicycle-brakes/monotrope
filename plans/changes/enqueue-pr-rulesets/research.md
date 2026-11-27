---
title: "Research — enqueue-pr-rulesets"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-3wtk
owner: Data Architect
provenance: human-written
tags: [research]
---

# enqueue pr rulesets — Research

## Topic (bead coding-harness-3wtk)

Class: bounded. Observed 2026-11-27 (main `f4352686`) on PR #477:
`scripts/enqueue_pr.py <n>` refuses every pull request for two reasons in the
script itself.

1. `checks: the required checks of main could not be read: gh api
   repos/bicycle-brakes/monotrope/branches/main/protection/required_status_checks
   failed: gh: Branch not protected (HTTP 404)`. `repos/.../branches/main`
   reports `protected: true` because ruleset `24528176` ("main") is active,
   while classic branch protection does not exist; the script (around line
   383) tolerates only a 404 containing "Required status checks not enabled".
2. `phase-6: an unrecognised table line in the released block: Loop state:
   {...}`. `scripts/stage2.py:505-507` writes `Loop state: ` (`STATE_KEY`) as
   the released loop block's own line after `release-loop`, but the block
   parser of `enqueue_pr.py` (around lines 585-590) rejects it.

Effect: no pull request can enter the merge queue through the one allowed
route (AGENTS.md rule 8). What: treat the 404 "Branch not protected" answer as
no classic protection and rely on the ruleset rules already read; accept
exactly the runner's `Loop state: ` line in a released block; keep every other
failure unreadable (fail closed). Acceptance: tests with a fake `gh` answering
`protected: true` plus that 404 admit on green ruleset checks; other 404/403
texts still refuse; a released block with the runner's `Loop state:` line
parses, a different unknown line still refuses. This change edits
`enqueue_pr.py` itself, so the maintainer merges it (bootstrap exception).

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
