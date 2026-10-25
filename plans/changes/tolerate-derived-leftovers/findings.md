---
title: "Findings — tolerate-derived-leftovers"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-b5w
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — tolerate-derived-leftovers

## Implementation, 2026-10-25

Implemented by hand by the orchestrating Claude Code session in a cloud
container, at the maintainer's instruction of 2026-10-25. Red first: both
new tests failed before the edit.

## Self-review, 2026-10-25

Read by the implementing session, so it is no independent review.

- A content edit that also changes the `updated:` line has more than one
  changed line, so it is not a stamp-only diff and stays refused.
- A tolerated leftover is not in the restore's `keep` set: a failed
  attempt puts it back to the baseline with the rest, and a passing one
  commits it re-stamped and re-rendered.
- `clear_derived_leftovers` in the tests is now redundant for the index;
  it is left as it is, outside this change.

## Independent runner review, 2026-10-25

An Opus sub-agent of the orchestrating session reviewed the runner with all
open pull requests merged (read-only, in a separate context). Its row for
this change:

| ID | Severity | Finding | Status |
|---|---|---|---|
| R-3 | MINOR | `derived_leftover` dropped diff lines starting `---`/`+++` as file headers, so a removed Markdown rule (`---`) or an added line starting `++` hid a content edit beside an `updated:` change; criterion 2 was broken (reproduced). | fixed — tests/test_stage2.py::test_a_content_edit_behind_dash_lines_is_no_derived_leftover |

The check now compares the `HEAD` version and the working file with their
first `updated:` line masked; a symlink, a non-file, undecodable bytes or
identical bytes are no stamp-only change.
