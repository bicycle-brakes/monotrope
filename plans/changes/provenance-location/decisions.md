---
title: "Decisions — provenance-location"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-3ar.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, provenance, adr-answers]
---

# Provenance location — Decisions

Phase 1a for bead coding-harness-3ar.1 (package 1 of
`docs/research/2026-10-11-adr-answer-pin-plan.md`), on 2026-10-12.
`scripts/harness.py decide adr` reads the provenance map only at the
repository root (`PROVENANCE = "provenance.yaml"`); LakeSwitch keeps its map at
`decisions/provenance.yaml` (read on GitHub, 2026-10-12), so the command
refuses there.

## Q-1 · How the command finds the provenance map

asked: 2026-10-12
answer: A — a fixed search order: `provenance.yaml` at the root, else `decisions/provenance.yaml`; when both exist, the command refuses with a clear message.
answered_by: maintainer
status: answered

In the context of an instance that keeps its provenance map somewhere other
than the repository root, facing the choice between a fixed search order and a
path the instance configures, we decided on the fixed order — root first, then
`decisions/provenance.yaml`, a refusal when both exist — to achieve that
LakeSwitch works without a new setting and only the command and its tests
change, accepting that a third location would need a change to the order. —
2026-10-12

## Decisions taken by the agent

[DETAIL] Class `bounded`: one lookup in one command and its tests; one
answered question meets the minimum.

[DETAIL] Scope stays as the package names it: the lookup serves
`scripts/harness.py` (the one read site, `answering_role`) and its tests.
`scripts/check_adr_answers.py` never opens the map, so it does not change. The
other readers of the same file (`scripts/check_frontmatter_current.py`,
`scripts/ramp_valves.py`, `scripts/stage2.py` through the first) are left as
they are; whether they follow the same order is a later change, once an
instance needs one of them.

[DETAIL] The stale header comment of `provenance.yaml` (it names readers that
do not hold today) is not touched here: the file is `human-decided`, and an
edit would turn this change into a decision pull request for a comment.
