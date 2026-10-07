---
title: "Plan — touch-map-comments"
status: draft
implementation_status: partial
date: 2026-10-08
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-cff
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, touch-map]
---

# Plan — touch-map-comments

```text
For you:     The touch map in a pull request shows fewer false or missing links from shell quotes.
Done when:   Five criteria hold, make verify is green, reviewed code is in a PR.
Appetite:    2 hours; a stop, not an estimate.
Not now:     A shell parser, backticks, <<$end, plain-text apostrophes in shell scripts.
Pre-mortem:  suppose it failed: most likely because a new rule cut a name a real script reads.
```

## Decided in phase 3

- [DETAIL] A context stack for `$( … )`, `$'…'` as its own quote, and a
  YAML-only word-apostrophe rule, instead of the bead's three options: each
  of those breaks F-7's accepted multi-line-quote rule (research).
- [DETAIL] Implemented by the orchestrating session (Claude Code with
  Anthropic, Opus 5.5): a new change folder trips the derived-file gap a
  file-tool worker cannot clear (bead coding-harness-mfv).

## Steps

1. `scripts/touch_map.py`: `_scan` carries a state stack; `_strip_comments`
   and `read_code` pass the YAML flag.
2. `tests/test_touch_map.py`: the verbatim line, ANSI and arithmetic cases,
   F-10's YAML fixture; planted faults per rule.
3. Measure links at both heads before and after.

## Time used

2026-10-08 23:31–23:36 UTC, 5 min by the orchestrator's clock (worktree
created to `make verify` green): code, tests, measurement (226 → 226;
251 → 248, the three false links), four planted faults each turned a test
red. The clock readings are the shell's `date -u` before and after.
