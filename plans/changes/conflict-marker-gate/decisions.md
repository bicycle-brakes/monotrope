---
title: "Decisions — conflict-marker-gate"
category: decisions
status: draft
implementation_status: none
date: 2026-11-05
created: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-i76l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, gate, merge]
---

# conflict-marker-gate — Decisions

Class: bounded (bead coding-harness-i76l).

## SKIP · interview

status: skipped
reason: The maintainer answered "Ja" on 2026-11-05 to this item as the orchestrator proposed it: a blocking gate that fails on merge-conflict markers in tracked text files (`git diff --check` and a scan for lines that start with `<<<<<<<`, `=======` or `>>>>>>>`, fixtures excepted by name), and a small helper for merging main into a change branch that stops with the conflicted paths instead of continuing. Trigger the same day: a merge of origin/main into spike/verify-duration conflicted on docs/WORKFLOW.md and the next command committed and pushed the markers (31d35400). The scope is settled; any further choice (for example which paths count as fixtures) is a [DETAIL] the draft decides with its reason.

## Q-2 · What git diff --check compares

asked: 2026-11-23
answer: A — `git diff --check` covers only the branch's committed changes against `origin/main` (`origin/main...HEAD`), not the working tree; the conflict-marker scan stays over all tracked text files.
answered_by: maintainer
status: answered
context: |
  Topic: the scope of the whitespace and error check inside the conflict-marker gate.
  Intention: on 2026-11-22/23 six implement attempts failed; Sonnet's attempt 3 was nearly done, and adding the missing gate declaration by hand showed that criterion 4's check over staged and unstaged changes goes red inside every runner attempt, because the runner writes quoted diagnostics with trailing whitespace into findings.md before its post-run checks.
  Today: the spec's criterion 4 runs git diff --check over staged and unstaged changes.
  Repository change: Options: A only the branch's committed changes against origin/main; B the working tree without findings.md; C the runner strips trailing whitespace from quoted diagnostics.
  Architecture change: none.

In the context of a gate that runs inside runner attempts, facing a check over the working tree that the runner's own records turn red, we decided to check only the branch's committed changes against origin/main, to achieve a gate that judges what is pushed and merged, accepting that whitespace faults in uncommitted work show only after the commit. — 2026-11-23
