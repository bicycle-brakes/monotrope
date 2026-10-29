---
title: "Decisions — workflow-promises"
status: draft
implementation_status: partial
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-i0l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# workflow-promises — Decisions

Class: bounded (one counted interview record or a reasoned skip owed). One
package led by coding-harness-i0l with coding-harness-690, coding-harness-72w
and coding-harness-7bw (maintainer, 2026-10-27: one pull request).

## SKIP · interview

status: skipped
reason: Each piece is a file or target `docs/WORKFLOW.md` already promises and describes; the beads state what "done" means (a gate catalog kept in step with `decisions/gates.yaml` by a test, a `/workflow-start` command that runs `scripts/new_change.py` with the bead link, `make change` and `make index` delegating to the scripts and listed by `make help`). What remains is mechanics, decided below with reasons.

## Decided by the agent

[DETAIL] **The stop hook is split out.** The stop hook (coding-harness-788,
`.claude/hooks/session-stop/check-tests-green.sh`) fires at the end of every
turn, and the full `make verify` takes about eleven minutes (CI, 2026-10-27).
Which check it runs, and how long it may hold a turn, changes how every
session in this repository feels; that is the maintainer's to decide, so it
goes to the daily decision block and stays out of this pull request.

[DETAIL] **The audit lead is answered by the research.** coding-harness-i0l
asks for a read-only comparison of WORKFLOW.md with the tree; the runner
exploration in `research.md` (2026-10-27) is that comparison. This change
builds the three bounded pieces and updates the "Not all of it is here yet"
list in `docs/WORKFLOW.md` for what it adds.

[DETAIL] **The gate catalog is derived, not hand-kept.** A test reads
`decisions/gates.yaml` and fails when a gate is missing from
`docs/governance/gate-catalog.md` or the catalog names one that is not
declared, so the two cannot drift.
