---
title: "Decisions — leak-diff-tests-exemption"
category: decisions
status: draft
implementation_status: none
date: 2026-11-23
created: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-juu
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, leak-check, security]
---

# leak-diff-tests-exemption — Decisions

Class: feature (bead coding-harness-juu; it changes what the leak check lets through to a foreign model, a security policy change). The maintainer answered three questions in the 15:00 block of 2026-11-01 (quoted in the bead's notes) and a fourth in the conversation on 2026-11-22; Q-4 widens Q-2.

## Q-1 · Does the tests/ exemption reach the diff inside a prompt

asked: 2026-11-01
answer: yes: diff hunks under tests/ in a prompt get the same exemption as the file - only the secret rules lapse, only for those hunks; the rest of the prompt and every other rule stay fully checked.
answered_by: maintainer
status: answered
context: |
  Topic: the secret rules over a diff sent as prompt text.
  Intention: the review loop sends the change's diff as prompt text, so a fake key-shaped literal a new test assigns blocks the call (seen 2026-10-16 on coding-harness-omp, rule secret:generic-api-key-assignment).
  Today: scripts/leakcheck.py skips the secret rules for files under tests/, but scans a prompt text whole.
  Repository change: Options: exempt the tests/ hunks of the diff on the file's terms; keep scanning the whole prompt; drop the secret rules for prompts.
  Architecture change: none (ADR 0007 boundary unchanged in kind).

In the context of diffs sent to foreign models, facing a blocked review for a fake test key or a widened exemption, we decided that tests/ hunks get the file's exemption for the secret rules only, to achieve reviews that are not blocked by test fixtures, accepting that a real secret committed under tests/ could reach a reviewer. — 2026-11-01

## Q-2 · Which diff lines are exempt

asked: 2026-11-01
answer: only added (+) lines in tests/ are exempt; context and removed lines stay checked.
answered_by: maintainer
status: answered
context: |
  Topic: which lines of a tests/ hunk the exemption covers.
  Intention: keep the exemption as narrow as the bead needs.
  Today: no exemption in prompts.
  Repository change: Options: added lines only; added and context lines; the whole hunk.
  Architecture change: none.

In the context of the exempt hunks, facing added lines only or wider, we decided on added lines only, to achieve the narrowest exemption, accepting that context lines still block. — 2026-11-01 (widened by Q-4)

## Q-3 · How a use of the exemption is recorded

asked: 2026-11-01
answer: every use is recorded as a line in the findings.md call record with the count of exempt lines, never their content.
answered_by: maintainer
status: answered
context: |
  Topic: visibility of the exemption.
  Intention: the maintainer sees when the exemption worked.
  Today: the call record names the leak check result only.
  Repository change: Options: a count in the call record; the lines themselves; nothing.
  Architecture change: none.

In the context of an exemption on a security check, facing silence or a record, we decided to record each use with its count, never the content, to achieve a visible exemption without copying the exempt text, accepting one more record line per call. — 2026-11-01

## Q-4 · Context lines of tests/ files

asked: 2026-11-22
answer: A — the exemption also covers unchanged context lines of files under tests/ (they are already committed and passed as test files); removed (-) lines stay fully checked; everything else of Q-1 to Q-3 stands.
answered_by: maintainer
status: answered
context: |
  Topic: context lines in the diff of a tests/ file.
  Intention: on 2026-11-21 an already committed fixture line (TEST_TOKEN in tests/test_verify_lock.py) entered the review-loop prompt as diff context and blocked prepare-loop; the orchestrator moved a helper to get past it (06c6414b, verify-two-slots). Second occurrence after 2026-10-16.
  Today: Q-2 keeps context lines checked.
  Repository change: Options: A context lines of tests/ files exempt, removed lines checked; B keep Q-2 (added lines only); C the whole tests/ hunk exempt, removed lines included.
  Architecture change: none.

In the context of committed test fixtures shown as diff context, facing repeated blocked reviews or a wider exemption, we decided to exempt context lines of tests/ files too while removed lines stay checked, to achieve reviews that pass over already committed fixtures, accepting that a committed test file's content reaches a reviewer that could read the file anyway. — 2026-11-22
