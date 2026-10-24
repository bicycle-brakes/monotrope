---
title: "Research — venv-pycache"
status: draft
implementation_status: none
date: 2026-10-24
last_reviewed: 2026-10-24
updated: 2026-10-24
supersedes: null
superseded_by: null
bead: coding-harness-q94b
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, runner, venv, tool-integrity]
---

# venv-pycache — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session itself at `origin/main` `7586f1a`
(2026-10-24): the scope is one measured failure, so no separate exploration
call was made.

## The failure

Measured three times on 2026-10-23/24 (repair of `runner-time-line-exits`,
pull request #225; repair of `loop-state-block`, pull request #229): every
attempt of a `stage2.py repair` run was refused with "`.venv/lib/python3.12/site-packages/xdist/__pycache__/__init__.cpython-312-pytest-8.3.4.pyc`
is not what the runner saw before the call, and a tool the attempt wrote is
not run". The first attempt ran pytest, which wrote xdist's
assertion-rewritten bytecode into the venv; the later attempts changed no
file but tripped on the same path. Resetting the tree and rerunning passed,
because the `.pyc` then stood in the baseline.

## What exists today

Read in `scripts/stage2.py` at `7586f1a`:

- `tool_state` digests every file and symlink under the worktree's `.venv/`
  before the model runs (R-21): `.venv/` is gitignored, so this digest is the
  only thing that shows an overwritten tool, a planted `*.pth` or a replaced
  package.
- `tool_problem` compares a fresh digest with the one taken before the call
  and names the first differing path; any difference refuses the attempt.

## What the change has to do

After the call, before the comparison, the runner deletes files under a
`__pycache__` directory inside `.venv/` that are new or changed against the
pre-call digest (Python rebuilds them from source); every other change inside
the venv is still refused (`decisions.md`, Q-1). A `.pyc` is executable code,
so leaving it out of the digest would be a hole; deleting it cannot inject
code. Tests: a changed and a new `.pyc` under `__pycache__` are deleted and
the attempt passes the check; a changed `.py`, a `.pth`, and a `.pyc`
outside `__pycache__` are still refused; a `__pycache__` that is a symlink is
not followed.

## Open questions

None for the maintainer: the direction is decided (`decisions.md`, Q-1).

## Draft-time repository checks — 2026-10-24

Read at input commit `4dc80fa`:

- `tool_problem` is the shared guard for `verify_attempt`, `format_step`,
  `red_first`, `fixed_test_proof` and `verify_draft`. The checks compare both
  additions and missing baseline entries, so deleting a changed baseline
  cache needs explicit bookkeeping of the runner's own deletion.
- `run_attempts` shares one `tools` dictionary across attempts rather than
  taking a new baseline after rejection; its comment requires this to avoid
  trusting a replaced tool. Cleanup must preserve that protection while
  allowing repeated checks after its own deletions.
- Existing tests in `tests/test_stage2.py` cover source/package, `.pth`,
  executable and symlink tampering; they are regression constraints, not
  candidates for replacement by cache tests.
- `templates/spec.md` exists; no plan template or
  `scripts/validate_change_artefacts.py` exists in this tree. The available
  interview and criterion-ledger gates can check the draft; the runner owns
  index generation and full verification.
