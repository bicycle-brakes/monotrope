---
title: "Research — read-only-agents-no-shell"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.22
owner: Data Architect
provenance: human-written
tags: [research]
---

# read only agents no shell — Research

## Topic (bead coding-harness-5ane.22)

Class: bounded. Ramp valve `agents-tool-scopes` (`scripts/ramp_valves.py`),
rule RB-A2 in `docs/governance/regelwerk.md`; maintainer 2026-11-25 (bead
`coding-harness-5ane.1`): build the enforcer in the 72-hour run; the valve was
re-dated to 2026-12-31 meanwhile. Write
`tests/test_agents.py::test_read_only_agents_have_no_bash` so that it holds
today and fails on a planted fault; then the valve is due and the rule is
raised in the rule set
(`tests/test_ramp_valves.py::test_no_valve_is_due_and_still_open`).

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).
