---
title: "Decisions — archive-closed-changes"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-cqun
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, plans-registry, archive, drift]
---

# archive-closed-changes — Decisions

Class: bounded (bead coding-harness-cqun).

## Q-1 · Tool or one-off cleanup

asked: 2026-11-06
answer: "Werkzeug + einmal anwenden (Recommended)" — a new `make archive` moves every change folder whose bead is closed to `plans/changes/archive/<date>-<name>/`, updates the moved files' headers and regenerates the index; it is applied once to the whole backlog and runs from then on after every merge, next to `make close-merged`.
answered_by: maintainer
status: answered
context: |
  Topic: finished changes are archived — the folder moves from plans/changes/<name>/ to plans/changes/archive/<date>-<name>/, headers are updated, the index is regenerated.
  Intention: 332 drift lines have kept the nightly CI red since 2026-09-30.
  Today: no tool archives; the 19 archived folders were moved by hand; the plans-registry gate reports the backlog but nothing clears it, so it grows with every merge (2026-11-03: 261 lines, 2026-11-06: 367).
  Repository change: a new script, a make target and tests.
  Architecture change: none — the gates already read archived folders.

In the context of a drift backlog that only a nightly gate reports and nothing clears, facing a backlog that grows with every merge, we decided to build an archive verb and apply it once to the whole backlog, to achieve a green nightly run that stays green, accepting a new script, a make target and its tests. — 2026-11-06

## Details decided by the orchestrator

- [DETAIL] The archive folder's date prefix is the day the archiving runs. Reason: no rule text defines it (research.md, "What is unclear"); the 19 existing folders are dated after their last review, which matches the archiving day; a closing date is not reliably readable for old beads.
- [DETAIL] Archiving sets `status: accepted` and `implementation_status: done` on every moved artifact, and stamps `updated:` and `last_reviewed:` with the archiving day. Reason: the whole archived stock carries `accepted`/`done`; the plans-registry coupling requires `done` under the archive; `check_frontmatter_current.py` requires `updated:` to follow the moving commit.
- [DETAIL] The tool reads bead state only through `scripts/bead_render.py` (house rule 2) and archives only folders whose bead is closed; a folder whose bead is open or missing from the render is reported, never moved. Running beads without a folder on `main` (lanes on unmerged branches) are out of scope.
- [DETAIL] Default is a report; `ARGS=--write` moves, like `make close-merged`.
