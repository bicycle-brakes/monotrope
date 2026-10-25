---
title: "Spec — ledger-marker"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-7g6h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, criterion-ledger]
class: bounded
appetite: 1
adr_files: []
---

# Spec — ledger-marker

Before its own `make verify`, the stage-2 runner removes `not yet written`
from every ledger entry whose named test exists, so a correct attempt no
longer fails on a stale marker (bead coding-harness-7g6h). Research:
`research.md`. Decisions: `decisions.md`, Q-1.

## Acceptance criteria

1. `check_criterion_ledger.clear_written(root, plan)` removes the marker
   from each ledger entry whose test file defines the named function, and
   returns those criterion numbers.
   *Refuted by:* a remaining marker on an existing test, or a missing number.
2. An entry whose file or function is missing keeps its marker, and an
   entry inside a fence is never changed; a second pass changes nothing.
   *Refuted by:* any such line changed.
3. `implement` and `repair` clear the markers before `make verify`, so the
   committed plan carries the cleared entries.
   *Refuted by:* a committed plan with the marker on a test the attempt wrote.
4. The runner refuses a plan reached through an alias (a symbolic link at
   it or in its parent folders, or a hard link) before it clears anything,
   so no file outside the worktree is written. Added after runner review
   R-1 and pre-review row P239-3, 2026-10-25.
   *Refuted by:* a changed file outside the worktree.

## Non-goals

- Add a marker for a missing test, or change any other ledger form.
- Change the criterion-ledger gate's findings.

## Definition of Done

- Tests red before the edit; `PYTHON=.venv/bin/python3 make verify` green
  except the gates this container cannot run.
- The last commit carries `Closes-Bead: coding-harness-7g6h`.

## Open decisions

None open.

- [DETAIL] The function lives in the gate's module and reuses its
  parsing, so the runner and the gate read entries the same way.
- [DETAIL] It runs in `verify_attempt`, before `prepare_derived`, so the
  date stamp sees the plan as changed.
