---
title: "Decisions — explorer-reviewer-agents"
category: decisions
status: draft
implementation_status: none
date: 2026-11-01
created: 2026-11-01
last_reviewed: 2026-11-01
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-9ll
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# explorer-reviewer-agents — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; one
below).

## Q-1 · Which models the two sub-agents pin

asked: 2026-11-01
context: |
  Topic: the two sub-agent files .claude/agents/explorer.md and reviewer.md that docs/WORKFLOW.md names and the tree lacks (bead coding-harness-9ll).
  Intention: the exploration is done; only the maintainer can say which model each file pins, and the draft cannot start without it.
  Today: phase 1 runs through the runner (GLM Flash or the research swarm), phase 6 through a fresh Codex. The sub-agents are the Claude Code path when stage 2 is off (--stage2-off); AGENTS.md names Haiku 5.5 or Sonnet 5.5 for that case, and for the review the maintainer set Opus 5.5 high as the Codex fallback on 2026-10-14.
  Repository change: two new files under .claude/agents/ and a test that reads them; the stop hook is bead coding-harness-788, the validator bead coding-harness-jc3.
  Architecture change: none; the files state what WORKFLOW already says.
  Question: which models should the two sub-agents pin? Options: Haiku 5.5 for explorer and Opus 5.5 high for reviewer (recommended) / Sonnet 5.5 and Opus 5.5 high / wait for the model registry (bead coding-harness-wq1m).
answer: "Haiku + Opus high" — explorer.md pins Claude Haiku 5.5, reviewer.md pins Claude Opus 5.5 with effort high; both read-only.
answered_by: maintainer
status: answered

In the context of two sub-agent files the workflow names for the Claude Code
path when stage 2 is off, facing a choice between the fallback models AGENTS.md
already names and waiting for a central model registry, we decided that the
explorer pins Claude Haiku 5.5 and the reviewer pins Claude Opus 5.5 at effort
high, both read-only, to achieve files that match the routes already decided,
accepting that the registry (bead coding-harness-wq1m) will later take these
choices over. — 2026-11-01

## Details for the draft

[DETAIL] **Only the two agent files and a test that reads them.** Reason: the
stop hook is bead coding-harness-788 and the validator bead coding-harness-jc3;
the explore's open point on scope is answered by the bead's title.

[DETAIL] **`.claude/` is held from runner attempts** (`RUNNER_HELD` in
`scripts/stage2.py`). Reason: the attempt writes the test and the plan; the
orchestrator writes the two agent files after the accepted attempt, as with
the held settings of coding-harness-l1if.

[DETAIL] **The `model:` field's effect in this Claude Code version is checked
once by hand** and recorded in findings.md. Reason: WORKFLOW §3 "Check after
setup" asks for it; no record was found in the tree.
