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
