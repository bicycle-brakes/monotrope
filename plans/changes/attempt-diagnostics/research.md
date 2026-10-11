---
title: "Research — attempt-diagnostics"
status: draft
implementation_status: none
date: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-11
supersedes: null
superseded_by: null
bead: coding-harness-cit
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, runner, implement, diagnostics]
---

# Attempt diagnostics — Research

Read on 2026-10-11 against `origin/main` at `a6b7150`. This change answers
bead coding-harness-cit: the implement verb of the stage-2 runner
(`scripts/stage2.py implement`) discards why a failed attempt failed.

## What happened

On 2026-10-11 the implement run for change criterion-test-ledger (bead
coding-harness-909) failed its post-run check twice on GLM 5.3 Flash and
passed on the third attempt, the Sonnet 5.5 fallback (commit `1d179c9` on
branch `feat/criterion-test-ledger`). Its `findings.md` holds three audit
lines; the only reasons recorded are "first Flash post-run check failed" and
"two Flash post-run checks failed". Nothing under `~/.local/state/coding-harness/`
was written by the run (looked at 2026-10-11).

Indirect evidence, measured by the orchestrating session during the run: the
worktree held `scripts/check_criterion_ledger.py` but no
`tests/test_check_criterion_ledger.py`; the ratchet in `tests/test_ci.py`
demands a test file per script, which alone turns `make verify` red. Which
attempt wrote which file cannot be told: the runner makes one checkpoint
commit after the passing attempt.

## What exists today

- `scripts/stage2.py`, `implement()` (around line 1522): runs up to three
  routes (Flash, Flash repair, Sonnet). After each attempt
  `verify_attempt()` returns a list of problems: preparation failures, a red
  `make verify` with the blocking gates and their last lines
  (`red_sections`, `TAIL_LINES`, `STDERR_LINES`), scrubbed of the key by
  `scrub()`, and a missing measured line under `## Time used` in `plan.md`.
- Those problems are appended to a local list `diagnostics` and passed into
  the next attempt's prompt through `implementation_prompt()` under
  "Earlier post-run diagnostics"; the list is not written anywhere.
- `begin_work_call()` writes the audit line per attempt into the phase's
  durable artefact (`findings.md` for implement).
- When all attempts fail, `implement()` raises `CallFailed("implementation
  post-run checks failed after the allowed attempts")` without the
  diagnostics.

## What is unclear

- Where in `findings.md` the diagnostics belong (under the attempt's audit
  line, or a section of their own) and how long they may be.
- Whether the per-attempt diff stat should be kept too, so it is visible
  which model wrote what.
- Whether the explore verb and the review loop have the same gap.
