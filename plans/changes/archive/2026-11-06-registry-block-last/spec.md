---
title: "Spec — registry-block-last"
status: accepted
implementation_status: done
date: 2026-11-03
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-2g7y
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification, stage-2]
class: bounded
appetite: 1
adr_files: []
---

# Spec — registry-block-last

A gate report's blocking reason reaches a reader that keeps only its tail
(bead `coding-harness-2g7y`). Research: `research.md`. Decisions:
`decisions.md`.

## Problem

The stage-2 runner hands a repairing model the tail of each red gate.
`plans-registry` prints its BLOCK lines first and hundreds of DRIFT lines
after them, so the model never learns why the gate blocked; seven attempts
in three changes failed that way (`research.md`).

## Acceptance criteria

1. When a report holds BLOCK findings and at least one finding of another
   level, its last lines repeat every BLOCK message under a heading that
   says so.
   *Refuted by:* a report with one block and 300 drift findings whose last
   two lines do not name the block.
2. When a report holds only BLOCK findings, or none, its text is unchanged.
   *Refuted by:* the repeat heading in a block-only report, or any change to
   the "OK — no deviation." text.

## Non-goals

- Changing `scripts/stage2.py`'s tail rule, gate exit codes, finding levels
  or the order of the sections.
- Reducing the DRIFT noise itself (bead `coding-harness-cqun`).

## Definition of Done

- `make verify` green; phase 6 has no open BLOCKER.
- The pull request touches `scripts/_verdict.py`, `tests/test_gate_machinery.py`
  and this folder; its last commit carries `Closes-Bead: coding-harness-2g7y`.

## Open decisions

None open.
