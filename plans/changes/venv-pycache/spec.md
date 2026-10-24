---
title: "Spec — venv-pycache"
status: draft
implementation_status: partial
date: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-q94b
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, tool-integrity]
class: bounded
appetite: 2
adr_files: []
---

# Spec — venv-pycache

The runner deletes new or changed cache files in its virtual environment
before using its tools, while retaining refusal of every other environment
change (bead coding-harness-q94b). Inputs: `research.md` and the maintainer's
answered cache-handling decision in `decisions.md` (Q-1).

## Problem

Three repair attempts measured on 2026-10-23/24 were refused after pytest
wrote xdist assertion-rewritten bytecode under `.venv/`; later attempts
inherited the same refusal even without another write (`research.md`,
"The failure"). At input commit `4dc80fa`, `tool_problem` compares every
file digest and symlink target against the pre-call snapshot. A cache write
therefore looks like a replaced tool, although deleting that cache would
let Python rebuild it without retaining attempt-written executable bytes.

## Terms

- **Cache file:** a regular file of any suffix beneath a directory component
  named exactly `__pycache__`, within this worktree's `.venv/`, reached
  without following a symlink. The `.venv/` root and all intervening
  directories must be real directories.
- **Baseline:** the environment's file digests and symlink targets captured
  before the first model call, shared by the run's checks and attempts.

## Acceptance criteria

1. When a post-call tool-integrity check finds a new cache file, it deletes
   that file before any runner-owned tool executes and accepts the otherwise
   unchanged environment.
   *Refuted by:* the file survives, a tool runs before deletion, or the cache
   addition alone refuses the check.
2. When a post-call tool-integrity check finds a cache file whose bytes differ
   from the baseline, it deletes that file before any runner-owned tool
   executes and accepts the otherwise unchanged environment.
   *Refuted by:* the changed bytes survive, a tool runs before deletion, or
   the resulting absence of the baseline file refuses the check.
3. When a cache file still matches the baseline, the check preserves it.
   *Refuted by:* unchanged cache bytes are removed or rewritten.
4. When checks or later attempts reuse the run's baseline after successful
   cleanup, the runner continues accepting its own deletions and removes
   newly generated cache bytes again before using its tools.
   *Refuted by:* a subsequent check refuses an earlier cleanup, or accepts a
   recreated cache file without deleting it.
5. When the environment has any difference other than a new or changed cache
   file successfully deleted by the runner, the check refuses it with a
   differing path named before any runner-owned tool executes.
   *Refuted by:* a changed source, added `.pth`, bytecode outside
   `__pycache__`, replaced executable, changed symlink, or model-deleted
   baseline file is accepted, including alongside removable cache files.
6. When a cache-looking path contains a symlink, cleanup leaves its target
   untouched and any changed symlink remains subject to integrity refusal.
   *Refuted by:* cleanup traverses a linked `.venv/`, parent directory or
   `__pycache__`, unlinks through it, or exempts a changed file symlink.
7. If an eligible cache file cannot be inspected or deleted, the check
   refuses with the affected path named before any runner-owned tool executes.
   *Refuted by:* an unreadable or undeletable changed cache is accepted or a
   runner-owned tool starts after that cleanup failure.

## Non-goals

- Ignoring cache files in the initial digest, trusting newly written cache
  bytes, or rebuilding the environment or its packages.
- Deleting unchanged caches, cleaning caches outside `.venv/`, or accepting
  other tool changes; cache directory removal is unnecessary.
- Changing model routing, retries, credential handling, timing, checkpoint
  policy, dependency pins or verification commands.
- Design phase 2b and an architecture decision record: this is the existing
  bounded cache-handling repair, with no architectural change.

## Protected areas

The tracker, `docs/adr/`, `decisions/`, prompts, workflow, kit and dependency
files remain untouched: none is needed to implement the answered decision.
Other changes' artifacts and files reached through symlinks are out of scope.

## Definition of Done

- `make verify` is green, including the criterion ledger and interview check.
- Regression tests prove cleanup, continued refusal, safe boundaries and
  repeated checks; the phase-6 review checks the ordering before tool use.
- Updated documents: this change's `plan.md` ledger and runner-maintained
  `findings.md`; the runner regenerates `plans/INDEX.md`. No ADR or model file.
- The pull request's file list respects protected areas and non-goals.
- The pull request closes the cache-integrity repair (bead
  coding-harness-q94b); its last commit carries
  `Closes-Bead: coding-harness-q94b`.
- Special runs: none; local fixtures need no provider call.

## Open decisions

None open. The maintainer's answer is unchanged.

- [DETAIL] Apply the answer to regular cache files of any suffix, rather
  than only `.pyc`, because Q-1 says files under `__pycache__`; symlinks stay
  integrity-protected so cleanup cannot reach another location.
- [DETAIL] Account only for successful runner deletions across checks; never
  refresh the whole baseline, because that could trust a modified package.
- [DETAIL] Use a two-hour phase-4 appetite, repairs included, as a stop for
  this bounded repair; no appetite was stated in the interview.

These reversible implementation details are agent choices with their reasons
recorded here; they do not add a maintainer answer.
