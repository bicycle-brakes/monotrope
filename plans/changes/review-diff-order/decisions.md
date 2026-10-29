---
title: "Decisions — review-diff-order"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-ut8q
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview]
---

# review-diff-order — Decisions

Class: bounded (one counted interview record or a reasoned skip owed; one
answered below). Reason for the class: the change alters which files of the
change diff a paid review-loop round receives and in which order, inside
`scripts/stage2.py`, its tests, `docs/WORKFLOW.md` §4 and the reviewer
prompt. ADR 0021 states what a free round receives (implementation source
and test hunks only) but no rule on the paid round's diff composition or
order (read 2026-10-29), so no ADR text has to change. Should the draft find
a sentence of ADR 0021 that the change contradicts, the class becomes
`architectural` and the ADR change goes as a decision pull request of its own.

## Q-1 · Which remedy for the cut review diff

context: |
  Topic: what a paid review-loop round sees when the change diff exceeds the
  2000-line bound.
  Intention: on 2026-10-28/29 no round of three changes saw a test file,
  because Git's path order puts docs/ and plans/ (with the growing
  findings.md) before scripts/ and tests/.
  Today: the diff goes to the reviewer in path order and is cut at 2000 lines.
  Repository change: the review-loop diff leaves out findings.md and
  plans/INDEX.md and orders code and tests before prose.
  Architecture change: none in ADR 0021's text; the loop's input changes.
  Question: which of the three options of the research note is taken?
asked: 2026-10-29, the directing conversation (through the orchestrator)
answer: one change — drop findings.md and plans/INDEX.md from the review-loop diff and put code and tests first
answered_by: maintainer
status: answered

In the context of review rounds whose 2000-line diff never reached the tests,
facing three options (leave the loop's own record out, order code and tests
first, split the diff across reviewers), we decided on the first two as one
change, to achieve rounds that see code and tests first, accepting that a
change still larger than the bound stays cut at its prose end and cannot end
the loop cleanly. — 2026-10-29

## Details for the draft

[DETAIL] **The free stage stays as it is.** `free_diff` already passes only
`scripts/` and `tests/` source; ordering and exclusion concern the paid
round's `change_diff`. Reason: the measured problem exists only there
(research, "How the diff is built today").

[DETAIL] **The cut-round rule stays.** A round over a diff that is still cut
after the new order is still not clean. Reason: the maintainer's decision
names no change to it, and splitting is not part of this change.
