---
title: "Spec — verify-stages-new-files"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-fdz
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, verify]
class: bounded
appetite: 1
adr_files: []
---

# Spec — verify-stages-new-files

Before its post-run `make verify`, the runner adds every untracked,
non-ignored file intent-to-add, so a gate that reads `git ls-files` sees
the files the attempt created (bead coding-harness-fdz). Research:
`research.md`. Decisions: `decisions.md`, Q-1.

## Acceptance criteria

1. When `implement` or `repair` launches `make verify`, `git ls-files`
   lists every new, non-ignored file the attempt created.
   *Refuted by:* a new file missing from `git ls-files` at that moment.
2. The checkpoint commit still holds the new file's content.
   *Refuted by:* the file missing from the commit.
3. No intent-to-add entry outlives `make verify`; the caller's index is left as it was.
   *Refuted by:* an intent-to-add entry or a changed staged state after the attempt.

## Non-goals

- Stage content before the checkpoint, or stage ignored files.
- Change the probe or the draft verb's verification.

## Definition of Done

- A test red before the edit; `PYTHON=.venv/bin/python3 make verify` green
  except the gates this container cannot run.
- The last commit carries `Closes-Bead: coding-harness-fdz`.

## Open decisions

None open.

- [DETAIL] Only `verify_attempt` (implement and repair): drafts write
  plans and docs, which no index-reading gate collects as code.
