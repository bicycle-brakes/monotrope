---
title: "Research — triage-where-cell"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-3ha6
owner: Data Architect
provenance: human-written
tags: [research]
---

# triage where cell — Research

## Topic (bead coding-harness-3ha6)

Class: bounded. Follow-up of change triage-verb (bead coding-harness-o2s1): review-loop round 4 rows L4-1 (MAJOR: a Where location without a slash — bare file name or file::test — is classified like any path, so a test-only row is still refused), L4-2 and L4-5 (read Where through ROW_COLUMNS; a slash token counts only when it names a tracked path), L4-3, L4-4 and L4-6 (prompt and help wording; prompts/04b-review-loop.md is a held path the orchestrator edits). The round-4 repair failed because the model edited the held prompt; appetite spent. Maintainer 2026-11-09: phase 6 now, round-4 rows as follow-up bead.

Further evidence (orchestrator, 2026-11-28): two review-loop rows of 2026-11-27/28 could not be triaged or repaired without a hand edit of the reviewer's record: `enqueue-pr-rulesets` L1-1 has `Where` = `scripts/enqueue_pr.py:runner_state_line` (a symbol after the colon, refused as 'unrecognised Where location') and Origin `Implementation`; `bead-topic-in-research` L1-1 has Origin `implementation` (repair refuses: 'selected repair rows carry an invalid Origin'). The runner then asks the orchestrator to correct the cells by hand; an unattended session's permission layer blocks that hand edit, so both lanes stop. Whether this change should also let `triage` set the Origin cell and accept a `path symbol` Where is for the spec to settle within the bead's scope.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
