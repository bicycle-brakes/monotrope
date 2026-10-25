---
title: "Decisions — review-row-closing-pipe"
status: draft
implementation_status: partial
date: 2026-10-25
last_reviewed: 2026-10-25
updated: 2026-10-25
supersedes: null
superseded_by: null
bead: coding-harness-2i9j
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# review-row-closing-pipe — Decisions

Class: bounded (one counted interview record owed; Q-1 below).

## Q-1 · What the runner does with finding lines that lack a closing pipe

context: |
  Topic: how the review loop reads reviewer answers.
  Intention: five valid-looking finding lines without a closing pipe
  failed three free members and left no trace of two paid answers
  (bead coding-harness-2i9j).
  Today: a line without a closing pipe is no row; a malformed answer fails
  its member with a message that names no line, and the raw answer is lost
  when no round is written.
  Repository change: the answer parser accepts that one row shape; the
  failure message names the first unrecognised line; the raw answer is kept.
  Architecture change: none.
asked: 2026-10-22, conversation 2026-10-22
answer: "(1) on a malformed answer, the credential-scrubbed raw answer goes into the loop record next to the failure line; (2) the error message names the first unrecognised line; (3) a line that starts with '|', has exactly six cells and a severity (BLOCKER, MAJOR, MINOR) in cell 2 counts as a row without a closing pipe - the six-cell rule stays strict otherwise (F-ids alone, prose without a table stay errors); (4) red-first test with exactly these five lines"
answered_by: maintainer
status: answered

The answer was given in the conversation on 2026-10-22 and copied into the
bead's description the same day; this record copies it from there.

In the context of reading reviewer answers, facing valid finding lines that
only lack their closing pipe, we decided that such a line counts as a row
when it has exactly six cells and a severity in cell 2, and that a malformed
answer is kept and its first unrecognised line named, to achieve that a
formatting slip neither fails a member nor erases its answer, accepting a
second, narrow row shape in the answer parser. — 2026-10-22
