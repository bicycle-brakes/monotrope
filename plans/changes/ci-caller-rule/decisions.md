---
title: "Decisions — ci-caller-rule"
category: decisions
status: draft
implementation_status: none
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-8sxb
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage-2, implement, ci]
---

# ci-caller-rule — Decisions

Class: bounded (bead coding-harness-8sxb).

## Q-1 · Where the CI-caller rule is taught and checked

asked: 2026-11-06
answer: "Anleitung + Runner (Recommended)" — the implement prompt states the rule in English (every script under scripts/ needs a CI step or a declared reason in ci_gates.OHNE_AUFRUFER), and when an attempt adds a file under scripts/ the runner adds the caller test to its cheap checks, so the attempt fails in seconds and the retry prompt carries the failure. No German enters an artefact; the rename of OHNE_AUFRUFER stays with bead coding-harness-yim (maintainer, morning question Q-M1, 2026-11-06).
answered_by: maintainer
status: answered
context: |
  Topic: implement attempts that add a script fail late, after a full make verify, on tests/test_ci.py's caller rule; two lanes hit it (conflict-marker-gate, and on 2026-11-07 the outcome-test full verify).
  Intention: make the failure early and cheap so a retry can fix it.
  Today: the rule lives only in the test; the implement prompt does not mention it.
  Repository change: one sentence in the implement prompt and one cheap check in the runner, with tests.
  Architecture change: none; the cheap-check mechanism of bead coding-harness-5tyh is reused.

In the context of attempts that fail late on an unstated caller rule, facing a choice between the prompt alone, the runner alone or both, we decided on both — the prompt states the rule and the runner checks it early when a script is added — to achieve a failure in seconds with its fix in the retry prompt, accepting one more cheap check. — 2026-11-07
