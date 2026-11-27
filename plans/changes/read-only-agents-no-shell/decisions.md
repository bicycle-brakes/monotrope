---
title: "Decisions — read-only-agents-no-shell"
category: decisions
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.22
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-opus-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, agents, ramp-valves]
---

# Decisions — read-only-agents-no-shell

Phase-1a record for `read-only-agents-no-shell` (bead `coding-harness-5ane.22`).

## SKIP · interview

status: skipped
reason: "Bounded enforcer whose content the maintainer set in the bead (2026-11-25, bead coding-harness-5ane.1) and run autonomously under the bounded standing grant (2026-11-25): one test, tests/test_agents.py::test_read_only_agents_have_no_bash, that holds on today's agent definitions and goes red on a planted read-only agent with a shell tool; then the ramp valve agents-tool-scopes is closed and rule RB-A2 raised as the bead names. Any edit of a human-decided file (docs/governance/regelwerk.md, if provenance.yaml marks it so) is prepared as text for the maintainer, not written. No product or architectural choice is open."
