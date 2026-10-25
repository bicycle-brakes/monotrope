---
title: "Spec — repair-restore-status"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-rcyf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, repair]
class: bounded
appetite: 1
adr_files: []
---

# Spec — repair-restore-status

A repair attempt that the commit guard refuses leaves `findings.md` as it
stood before the attempt, so no row stays `fixed` by a test the restore
removed (bead coding-harness-rcyf). Research: `research.md`.

## Acceptance criteria

1. When `checkpoint` refuses a passing attempt (a path a stage-2 run does
   not commit, or an unreadable map), `findings.md` is put back to its
   pre-call snapshot before the failure is raised; the taken rows read
   `taken` again.
   *Refuted by:* a row whose Status names a fix after the refusal, or
   phase-6 or released rows that differ from before the attempt.
2. The refused attempt's work is still undone (existing behaviour).
   *Refuted by:* the attempt's test file surviving the refusal.

## Non-goals

- Refuse a row up front because its fix may lie in a human-written path
  (research, option 3).
- Change the commit guard or what it keeps.

## Definition of Done

- A test red before the edit; `PYTHON=.venv/bin/python3 make verify`
  green except the gates this container cannot run.
- The last commit carries `Closes-Bead: coding-harness-rcyf`.

## Open decisions

None open.

- [DETAIL] Restore the whole pre-call snapshot (research, option 1), the
  same step every other failure path in `run_attempts` already takes.
