---
title: "Research — touch-map-comments"
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
tags: [research, touch-map]
---

# Research — touch-map-comments

Phase 1 for bead coding-harness-cff, read on 2026-10-08 at `origin/main`
`b32f488`.

`scripts/touch_map.py` strips comments from shell, Makefile and YAML text
(`_scan`, `_strip_comments`) and carries an open quote across lines, so a
quote it misreads flips the rest of the file (touch-map finding F-10, a named
limit; the maintainer asked for a sturdier rule in this bead).

The measured cases of F-10 have two causes:

1. **A quote nested in a command substitution** — line 31 of each of the
   three copies of `format-code.sh` in portfolio-agentic-engineering
   (`20a279c`): `FILE_PATH="$(echo "$INPUT" | grep … '"file_path"…' | sed
   's/…"\(.*\)"$/\1/')"`. The shell nests quotes inside `$( … )`; the
   scanner does not, ends the line inside a single quote and reads the
   comment of line 40 as code: three false `reads` links to `ruff.toml`.
2. **An apostrophe inside a word in YAML** (`- name: Don't skip`): in YAML
   it is a letter, the scanner opens a quote; F-10's own fixture loses a
   link to a name inside a later real quote.

The bead's options: resetting the quote at each line would break F-7's
accepted rule that the inner line of a multi-line quote is code (test
`test_a_name_the_shell_reads_is_not_cut`); counting only names outside a
comment on both readings would lose those links too.

Measured before the change (links of `touch_map.links`):
coding-harness `b32f488` 226, portfolio-agentic-engineering `20a279c` 251.
