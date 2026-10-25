---
title: "Spec — tolerate-derived-leftovers"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-b5w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, runner]
class: bounded
appetite: 1
adr_files: []
---

# Spec — tolerate-derived-leftovers

The pre-existing-change check of `implement`, `draft` and `repair` lets a
run start on a failed run's tree when the only changes are the runner's own
derived writes (bead coding-harness-b5w). Research: `research.md`.
Decisions: `decisions.md`, Q-1.

## Terms

- **Derived leftover:** `plans/INDEX.md`; a file whose only difference
  from `HEAD` is one `updated:` line replaced by another; a `.pyc` file
  under a `__pycache__` directory.

## Acceptance criteria

1. After a failed `implement`, a second `implement` starts and passes when
   the worktree differs from `HEAD` only by derived leftovers.
   *Refuted by:* a refusal naming a derived leftover.
2. A content change beside derived leftovers is still refused, and the
   refusal names it but no derived leftover.
   *Refuted by:* a start, or a refusal that lists `plans/INDEX.md`.

## Non-goals

- Put derived writes back after a failed run (the bead's other route).
- Tolerate any other change.

## Definition of Done

- Tests red before the edit; `PYTHON=.venv/bin/python3 make verify` green
  except the gates this container cannot run.
- The last commit carries `Closes-Bead: coding-harness-b5w`.

## Open decisions

None open.

- [DETAIL] The three refusal blocks become one `refuse_preexisting`, so
  the verbs cannot drift apart.
- [DETAIL] `plans/INDEX.md` is tolerated whatever it holds: the next
  verify re-renders it from the tree, so no hand edit of it survives.
