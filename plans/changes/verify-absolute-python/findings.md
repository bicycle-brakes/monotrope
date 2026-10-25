---
title: "Findings — verify-absolute-python"
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
tags: [findings]
---

# Findings — verify-absolute-python

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: both
cases of the new test failed before the edit (the gate saw
`.venv/bin/python3`). After the edit, `PYTHON=.venv/bin/python3 make
verify` shows `leerprobe` green, where it was red on the same tree before.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- A bare name such as `python3` has no `/` and stays a PATH lookup; an
  absolute path is unchanged; an unset `PYTHON` takes the existing search.
- Calling `scripts/kit/probe.py` directly with a relative `PYTHON` still
  hands that path to the foreign repository; only runs through
  `verify_all.sh` are fixed. The non-goal keeps the probe unchanged.

## Pre-review by an Opus 5.5 subagent, 2026-10-25

At the maintainer's request, a read-only Opus 5.5 subagent reviewed this
change before the phase-6 Codex review, which this container cannot reach.
It stands in for nothing: phase 6 is still owed. It found no blocker and
two minor rows, both reproduced and both fixed by the orchestrating session.

- **P237-1 (MINOR), fixed.** `scripts/verify_all.sh` pasted the now absolute
  `$PYTHON` unquoted into a gate command for `sh -c`. Under a directory with
  a space, a gate starting with `python3` failed, where the relative path
  had worked. The path is now single-quoted, with a quote inside it escaped.
  Test: `tests/test_ci.py::test_a_python_path_with_a_space_still_starts_the_gate`,
  red before the fix.
- **P237-2 (MINOR), fixed.** Criterion 2 cited only the unset case. The new
  `tests/test_ci.py::test_an_absolute_or_bare_python_reaches_the_gate_unchanged`
  pins the absolute and bare-name cases; it passed before and after, as
  criterion 2 expects. The ledger names both new tests.
- Not now: the runner echoes the literal word `lauf_cmd` instead of the
  command (`── [<gate>] $ lauf_cmd`). Present on `main` before this change.
