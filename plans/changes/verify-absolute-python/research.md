---
title: "Research — verify-absolute-python"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-4x2c
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, verify, leerprobe]
---

# verify-absolute-python — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md),
written by the orchestrating session at `origin/main` `f8a6b33`
(2026-10-25).

## The finding

Locally, `make verify` was red on the `leerprobe` gate with two cases,
`tests.test_ci::test_runner_reports_what_it_cannot_run` and
`tests.test_ci::test_the_runner_still_admits_what_it_cannot_do_at_all`,
while hosted CI was green (bead coding-harness-4x2c, measured 2026-10-22/23).

## Cause, measured 2026-10-25 in a cloud container

`python3 scripts/kit/probe.py` on the same commit:

| `PYTHON` in the environment | leerprobe |
|---|---|
| unset | green |
| `.venv/bin/python3` (relative) | red, exactly the two cases |
| absolute path to the same interpreter | green |

Both cases run `bash scripts/verify_all.sh --list` with the inherited
environment. The probe runs the suite in a throw-away foreign repository
that has no `.venv`. `verify_all.sh` takes `$PYTHON` as given and exports
it ("the gates' own children find it in the environment"), so the
relative path names nothing there, and the runner fails. Hosted CI sets no
relative `PYTHON`, so it stays green. The repository's own definition of
done asks for `PYTHON=.venv/bin/python3 make verify`, which is why every
local run of that form was red.

Earlier guesses, now refuted: the gate is not red because of uncommitted
files. It was red on a clean, committed tree with a relative `PYTHON`, and
green on an uncommitted tree without one.

## Options

1. `verify_all.sh` exports a relative `$PYTHON` as an absolute path, read
   against the caller's directory before it changes to the repository root.
2. The probe drops `PYTHON` from the foreign run's environment.
3. Name the difference in `docs/WORKFLOW.md` (the bead's fallback).

Option 1 fixes the cause for every child of every gate, not just the
probe's, and keeps the caller's choice of interpreter.
