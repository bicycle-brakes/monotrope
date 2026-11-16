---
title: "Decisions — omnigent-test-not-blocking"
category: decisions
status: draft
implementation_status: none
date: 2026-11-12
created: 2026-11-12
last_reviewed: 2026-11-12
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-i9df
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, omnigent, make-verify, tests]
---

# omnigent-test-not-blocking — Decisions

Class: bounded (bead coding-harness-i9df).

## Q-1 · What "not blocking" means

asked: 2026-11-12
answer: "A: Nur der Abgleich meldet (Recommended)" — only the test that reads the Omnigent installed on the machine stops blocking: it runs when Omnigent is installed or updated (tools/omnigent/install.sh) and reports new tools there; the other tests (the list against the rendered rule files) stay blocking.
answered_by: maintainer
status: answered
context: |
  Topic: the change omnigent-test-not-blocking (bead coding-harness-i9df): a local Omnigent update must not turn every check run red.
  Intention: the exploration is done; the draft needs one answer (class bounded).
  Today: 38 Omnigent tests block in make verify. Nearly all check only that the rule files match the list in the repository (local and stable). One compares the list with the Omnigent installed on the machine; it went red on 2026-11-12 after an update to 0.21.0. The maintainer does not use Omnigent yet.
  Repository change: one test and possibly the install script.
  Architecture change: none.

In the context of a test that reads a tool installed outside the repository,
facing an update that turned every local check red without a code change,
we decided that only the comparison with the installed Omnigent stops blocking
and runs where Omnigent is installed or updated,
to achieve check runs that change only with the repository,
accepting that a new Omnigent tool is reported at install time rather than by
every check run — 2026-11-12
