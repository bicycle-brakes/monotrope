---
title: "Findings — review-mixed-malformed-row"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-vque
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — review-mixed-malformed-row

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: the
three cases of criterion 1 failed before the edit (the round was written
with the malformed line only quoted); criterion 2's guard passed before
and after. All 908 runner tests pass except the root-only one.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- A line with more than six cells and a severity is widened into a row by
  `parse_rows`, so it never reaches `finding_shaped` as leftover text.
- The header line `| ID | Severity | … |` has no severity in cell 2 and is
  furniture anyway; it does not refuse.
