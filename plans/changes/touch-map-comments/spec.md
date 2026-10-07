---
title: "Spec — touch-map-comments"
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
tags: [spec, touch-map]
class: bounded
appetite: 2
---

# Spec — touch-map-comments

The comment rule follows the two constructs that flipped files in F-10, and
keeps every accepted case. Inputs: [`research.md`](research.md).

## Acceptance criteria

1. A command substitution `$( … )` opens a quoting context of its own,
   inside double quotes too, and closes with its matching `)`.
   *Refuted by:* line 31 of portfolio's `format-code.sh`, verbatim,
   leaving the next line's comment as code.
2. In `$'…'` a backslash escapes the quote.
   *Refuted by:* `echo $'a\'b' # c` keeping `# c`.
3. In a YAML file an apostrophe between two letters is a letter.
   *Refuted by:* F-10's fixture losing `scripts/quoted_tool.py`.
4. Every case the existing tests accept stays: a multi-line quote's inner
   line and a heredoc body are code; the shell's own reading of a plain-text
   apostrophe stays a named limit.
   *Refuted by:* any existing `tests/test_touch_map.py` case red.
5. Measured over two heads: no link changes in coding-harness `b32f488`;
   in portfolio-agentic-engineering `20a279c` exactly the three false
   `format-code.sh` → `ruff.toml` links go.
   *Refuted by:* any other added or removed link.
