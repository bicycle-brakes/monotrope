---
title: "Decisions — outcome-test"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-3nm5
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, measurement, outcome-test]
---

# outcome-test — Decisions

Class: bounded (bead coding-harness-3nm5).

## Q-1 · Questions, frequency and where results live

asked: 2026-11-06
answer: "8 Fragen, bei Bedarf (Recommended)" — eight questions; the test runs before every change to a handover convention or AGENTS.md and once now as a baseline; results go to one JSONL file under docs/research/, each record dated and bound to a commit.
answered_by: maintainer
status: answered
context: |
  Topic: a fresh, memory-free session answers fixed harness questions (for example who repairs taken findings, where run plans live); the expected answer is read from the repository at test time, never stored; this shows whether a change to the handover or AGENTS.md makes sessions answer better or worse.
  Intention: the lane is explored; size, frequency and storage are open.
  Today: the gates check artefacts, not whether a session knows the current rules.
  Repository change: a question file, a script and a result file.
  Architecture change: none.

In the context of gates that measure artefacts but not what a fresh session knows, facing the cost of nightly runs, we decided on eight questions run on demand before handover or AGENTS.md changes plus one baseline, results in one dated JSONL file under docs/research/, to achieve a measurement exactly where knowledge changes, accepting no trend line between such changes. — 2026-11-06

## Q-2 · What the fresh session may use

asked: 2026-11-08
answer: "Repo lesend erkunden (Recommended)" — option 1: a new Claude Code session gets its usual start context and may read the repository; the run records Claude Code, the model actually used, the start context and the permitted read access.
answered_by: maintainer
status: answered
context: |
  Topic: which fresh session the baseline measurement represents.
  Intention: the spec carried this as an open decision; review loop round 1 marked it twice as a BLOCKER, and the implementation already assumed option 1.
  Today: no measurement exists; different session kinds get different start contexts.
  Repository change: the answer goes into this record; the spec and docs/WORKFLOW.md name the choice.
  Architecture change: none.

In the context of a baseline that could measure either the normal working start or start-context knowledge alone, facing that choice before building, we decided to measure the normal working start with read access to the repository, to achieve a test of whether a new session finds the current rules in everyday work, accepting that it no longer shows what the start context alone already holds. — 2026-11-08

## Q-3 · What the repository history keeps when the session may read the repository

asked: 2026-11-08
answer: "Nur Punktzahl im Repo (Recommended)" — the history in the repository keeps date, commit, the four labels and a correct/incorrect mark per question, never the answer texts; the full submitted answers stay in a local file outside the repository. This narrows Q-1's history contents.
answered_by: maintainer
status: answered
context: |
  Topic: Q-1 placed the history, with submitted answers and verdicts, at docs/research/outcome-test-results.jsonl; Q-2 lets the answering session read the repository.
  Intention: review loop round 2 (row L2-2, MAJOR) showed that from the second run on a session could read earlier correct answers, silently polluting the comparison.
  Today: the history with answer texts lies in the readable repository.
  Repository change: the repository record drops answer texts; a local file outside the repository keeps them.
  Architecture change: none.

In the context of a test session that may read the repository, facing a history that would hand it earlier answers, we decided to keep only scores per question in the repository and the answer texts locally outside it, to achieve comparable runs without an answer key in reach, accepting a second, unversioned file for the full answers. — 2026-11-08
