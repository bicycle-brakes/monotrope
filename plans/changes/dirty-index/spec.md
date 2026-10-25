---
title: "Spec — dirty-index"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-0c8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, dirty-tree]
class: bounded
appetite: 1
adr_files: []
---

# Spec — dirty-index

The runner sees a change that exists only in the index, so its
pre-existing-change check refuses it and no checkpoint commit can overwrite
staged content (bead coding-harness-0c8). Research: `research.md`.
Decisions: `decisions.md`.

## Problem

`changed_paths` compares the working tree with `HEAD` and lists untracked
files. A path staged with other content and then put back in the working
tree differs from `HEAD` only in the index, so `implement`, `draft` and
`repair` start, and the checkpoint's `git add -A` replaces the staged
content (reproduced at `378879a`, 2026-10-21).

## Terms

- **Index-only change:** a tracked path whose index entry differs from the
  commit compared against while its working file does not.

## Acceptance criteria

1. `changed_paths` lists a path whose only difference from the compared
   commit is in the index.
   *Refuted by:* an index-only change missing from the result.
2. `implement`, `draft` and `repair` refuse an index-only change outside the
   change's `findings.md` with the existing pre-existing-change diagnostic,
   naming the path, before any model call.
   *Refuted by:* a model call, another exit or a diagnostic that does not
   name the path.
3. After that refusal the index and the working tree are unchanged.
   *Refuted by:* a changed staged blob or working file.
4. Paths changed in the working tree and untracked files are still listed
   exactly once each.
   *Refuted by:* a missing or duplicated entry.

## Non-goals

- Change what the checkpoint commits or which paths an attempt may commit
  (coding-harness-wqw, coding-harness-qr03).
- Tolerate staged changes, or stage or unstage anything for the operator.

## Protected areas

Model endpoints, credentials, leak-check rules, governance decisions and
ADRs stay unchanged: the fix widens one git query.

## Definition of Done

- Regression tests for criteria 1 to 4, red before the production edit.
- `PYTHON=.venv/bin/python3 make verify` green except the gates this
  container cannot run (named in the pull request).
- The pull request closes the bead; its last commit carries
  `Closes-Bead: coding-harness-0c8`.
- Special runs: none; tests use local stand-ins without model calls.

## Open decisions

None open.

- [DETAIL] Widen `changed_paths` instead of adding a check to the three
  verbs: every caller asks which paths differ from a commit, and an
  index-only difference is one (research, option 1).
- [DETAIL] Appetite one hour of phase 4: one git query and its tests.
