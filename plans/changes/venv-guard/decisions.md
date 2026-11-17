---
title: "Decisions — venv-guard"
category: decisions
status: draft
implementation_status: none
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-17
supersedes: null
superseded_by: null
bead: coding-harness-s55e
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, venv]
---

# venv-guard — Decisions

Class: bounded (bead coding-harness-s55e; one answered question is owed —
Q-1 below, answered by the maintainer on 2026-11-17 in the day session after
the night run 2026-11-16-a and recorded in the bead's notes).

## Q-1 · How the scripts find the checkout's own environment

asked: 2026-11-17
answer: "A mit den zwei Bedingungen. Es ist der kleinste Eingriff, repariert jeden Aufrufer auf einmal und gibt bei fehlender .venv eine klare Meldung. D ist ein guter Gedanke für später, falls die Rust-Werkzeuge konkret werden. Dann wäre es aber ein eigener Change mit eigener Entscheidung." — in English: option A with the two conditions; it is the smallest intervention, repairs every caller at once and gives a clear message when .venv is missing; option D (a language-neutral launcher) is a good thought for later, should the Rust tools become concrete, but then as a change and a decision of its own. Option A: one guard module at the start of each script; when the script does not run under the checkout's `.venv` and a `.venv` exists, it re-executes itself there; with no `.venv`, a clear "run make venv" message replaces the ModuleNotFoundError; callers keep `python3 scripts/...`. Condition 1: a test goes red when a script with a third-party import lacks the guard (house rule 9). Condition 2: kit fallback — in an instance repository without `.venv` the guard does nothing and the script runs as today.
answered_by: maintainer
status: answered
context: |
  Topic: the change venv-guard (bead coding-harness-s55e), scripts started with the system python3 fail because it lacks PyYAML.
  Intention: measured 2026-11-16 about 23:20 UTC in the night run 2026-11-16-a: the workflow-start skill runs exactly `python3 scripts/new_change.py <name> --bead <id>`, the system interpreter has no PyYAML, scripts/plans_registry.py fails with "No module named 'yaml'", and the skill forbids a retry, so no change folder can be opened through its one entry point; the stage-2 runner hit the same fault. It blocks the night-command lane (bead coding-harness-oswk).
  Today: every caller names bare `python3`; only `scripts/verify_all.sh` chooses the checkout's `.venv` interpreter itself. Measured 2026-11-17 on origin/main dfede341: 21 of 58 scripts import yaml; the third-party dependencies are PyYAML, Jinja2 and pydantic.
  Repository change: one guard module the affected scripts call first, a test that goes red when a script with a third-party import lacks it, and no change to any caller's command line.
  Architecture change: one choke point for the interpreter choice of the scripts; a language-neutral launcher (option D) stays out, for a later change of its own.

In the context of scripts that callers start with whatever `python3` is on
the path, facing a system interpreter without the locked third-party packages
and a skill that forbids a retry, we decided that one guard module at the
start of each script re-executes it under the checkout's `.venv` when one
exists and otherwise either names `make venv` or, in an instance repository
without `.venv`, does nothing, held by a test that goes red on a script with a
third-party import and no guard, to achieve one fix for every caller without
touching their command lines, accepting a re-exec at the start of those
scripts and a guard line in each of them — 2026-11-17

## Decided by the agent

[DETAIL] **The research did not read the bead.** The phase-1 exploration
(research.md, "What is unclear about it", item 1) could not hydrate the
tracker in the worktree, so its open questions 1 and 6 (scope and attachment
point of the guard) are answered by the bead text and Q-1 above: the guard
attaches at script start, not at verify time, build time or session start.
Reason: the bead (read 2026-11-17 from the main checkout with `tools/bd show
coding-harness-s55e`) names the failing callers and the maintainer chose A.

[DETAIL] **Condition 2 is read as: no `.venv` in the checkout → the guard
returns and the script continues under the current interpreter.** The
"run make venv" message applies when the script then fails on its
third-party import, which the guard may surface instead of the bare
ModuleNotFoundError. The exact split between "does nothing" and "clear
message" is left to the spec draft, which must keep both conditions true at
once; it is not a new decision because both behaviours were stated by the
maintainer. Reason: the two stated behaviours meet only at "no `.venv`", and
the kit fallback is the binding one there.
