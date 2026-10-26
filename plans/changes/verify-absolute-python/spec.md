---
title: "Spec — verify-absolute-python"
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
tags: [spec, verify, leerprobe]
class: bounded
appetite: 0.5
adr_files: []
---

# Spec — verify-absolute-python

`PYTHON=.venv/bin/python3 make verify` is green locally where hosted CI is
green: the runner hands every gate's children an absolute interpreter path
(bead coding-harness-4x2c). Research: `research.md`.

## Acceptance criteria

1. A relative `$PYTHON` containing `/` reaches the gates as the absolute
   path it names from the caller's directory, also when the caller stands
   outside the repository root.
   *Refuted by:* a gate that sees a relative path, or one resolved against
   the repository root instead of the caller's directory.
2. An unset, absolute or bare-name `$PYTHON` behaves as before.
   *Refuted by:* a changed interpreter choice in the existing runner tests.

## Non-goals

- Change the interpreter search when `$PYTHON` is unset.
- Change the probe or the two `test_ci` cases.

## Definition of Done

- Regression test red before the edit; `PYTHON=.venv/bin/python3 make verify`
  shows `leerprobe` green.
- The last commit carries `Closes-Bead: coding-harness-4x2c`.

## Open decisions

None open.

- [DETAIL] Resolve in `verify_all.sh` before its `cd` (research,
  option 1): the fix reaches every child of every gate.
