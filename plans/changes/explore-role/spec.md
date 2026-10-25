---
title: "Spec — explore-role"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-e7m
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, explore]
class: bounded
appetite: 1
adr_files: []
---

# Spec — explore-role

The explorer is told who it is and which tools it has, and an answer that
names no file of the repository fails instead of being appended as research
(bead coding-harness-e7m). Research: `research.md`.

## Acceptance criteria

1. Every exploration prompt, on the GLM and the `--stage2-off` route,
   carries the runner's statement of the explorer's role and its read-only
   tools (`EXPLORER_ROLE`).
   *Refuted by:* a prompt without it.
2. An answer that names no existing file or directory inside the worktree
   exits 1, appends nothing to `research.md` beyond the call record, and
   shows the answer's last 40 lines on standard error.
   *Refuted by:* an appended `## Runner exploration` block, or no answer shown.
3. An answer that names a repository file is appended as before.
   *Refuted by:* a refused answer with a path (existing explore tests).

## Non-goals

- Change which model `--stage2-off` uses (option 1 in research).
- Edit `prompts/01-explore.md` (human-written).

## Known limits

The check is a heuristic, not proof that research was done.

- A refusal that names a repository file which also appears in the phase
  prompt or in `AGENTS.md` (for example `scripts/stage2.py`,
  `docs/WORKFLOW.md`, `AGENTS.md`) still passes. Real research legitimately
  cites these files, so the check does not exclude them.
- "Exists" means exists in the worktree: ignored files count, and no git
  call is made. Only a path under `.git` is never counted.
- A bare word counts only if it is an entry directly at the root of the
  worktree (`Makefile`); a path may be absolute if it lies inside the
  worktree, and `\` is read as `/`.

## Definition of Done

- Tests red before the edit; `PYTHON=.venv/bin/python3 make verify` green
  except the gates this container cannot run.
- The last commit carries `Closes-Bead: coding-harness-e7m`.

## Open decisions

None open.

- [DETAIL] "Names a repository file" is the measurable form of "holds
  research": the prompt asks for facts with source paths, and the
  2026-10-20 refusal named only `stage2.py`, which does not exist at the
  worktree root.
