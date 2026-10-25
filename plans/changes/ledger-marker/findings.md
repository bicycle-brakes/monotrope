---
title: "Findings — ledger-marker"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-7g6h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — ledger-marker

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: both
new tests failed before the edit (no `clear_written`; the committed plan
kept the marker).

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- `clear_written` reads with the gate's own `read`, `ledger_sections` and
  `parse_entry`, so trailing whitespace, a byte-order mark and fences are
  handled as the gate handles them; it rewrites only the matched lines.
- The runner imports its own copy of the module, like
  `check_frontmatter_current`, never the attempt's.
- `repair` goes through `verify_attempt` too, so it clears markers as well.
