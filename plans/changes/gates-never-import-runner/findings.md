---
title: "Findings — gates-never-import-runner"
category: findings
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7ayv
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — gates-never-import-runner

Stage-2 call, 2026-11-21: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1162 files, 5240 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1165 files, 5242 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-21

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `spec.md:38-39`, criterion 2 | [AMBIGUITY] "a nested import" can be read two ways. (a) An import statement below module top level, inside a function, `if` or `try` body. The check scripts already use this lazy form (`scripts/check_bead_export.py:57`, `scripts/check_dangling_bead_ids.py:70`). The checker then has to walk the whole syntax tree, and the fixture is a function-local `import stage2`. (b) A multi-name or dotted statement: `import os, stage2`, `import stage2.x`, `from scripts.stage2.x import y`. The checker then has to test every alias and the leading part of each module name, and the fixture is one of those statements. A checker that reads only module-level statements passes the (b) fixture. A checker that compares only the first alias's full module name passes the (a) fixture. Each misses the other reading's case and criterion 2 stays green. | Opus | open | — |
| F-2 | MAJOR | SPEC | base | `spec.md:41-42`, criterion 3; `spec.md:53` | [AMBIGUITY] "calls `importlib.import_module` with the literal" can be read two ways. (a) Only the call written as `importlib.import_module("stage2")` on the name `importlib`. Then `from importlib import import_module; import_module("stage2")`, `import importlib as il; il.import_module("stage2")` and `importlib.import_module(name="stage2")` are all accepted. The non-goal at line 53 ("dynamic import APIs beyond the literal `importlib.import_module` calls") would cover them. (b) Any call of that function with the literal, however the function was bound. Then each of those spellings refutes criterion 3. The two readings lead to different checkers and fixture sets. Criterion 2 settles that aliases count for import statements, but nothing settles it for this call. | Opus | open | — |
| F-3 | MAJOR | SPEC | base | `spec.md:44-45`, criterion 4; `spec.md:35-36`, criterion 1 | [AMBIGUITY] "a temporary matching script" handed to "the checker" can be read two ways. (a) The negative control goes through the same file collection criterion 1 uses: a `check_*.py` file that the `scripts/check_*.py` selection finds. That file is written either into the real `scripts/`, where it races with the criterion-1 scan in other `-n auto` workers and writes into the tree, or into a temporary root that the collector takes as a parameter. (b) The negative control passes the file or its source straight to the per-file predicate, and "matching" refers only to its name. Under (b), no test notices a collection that finds zero files, for example a root resolved from the working directory or a typo in the pattern. Criteria 1–5 then all stay green on every run. Only criterion 1's manual refutation, adding a real script, would show it. No criterion requires the scanned set to be non-empty or to contain today's twelve files. | Opus | open | — |
| F-4 | MINOR | SPEC | base | `spec.md:35-36`, criterion 1 | [AMBIGUITY] The criterion says "every current `scripts/check_*.py`", but its refutation talks about "a newly added matching script". (a) The twelve files present today, kept as a recorded list. The bead's "a ratchet, like RB-G4's mutation ratchet" (`decisions.md:26`) points this way, because this repository's ratchets are recorded lists (`OHNE_AUFRUFER`, the mutation ratchet). A new `check_*.py` is then either never scanned, so the refutation case stays green, or has to be added to the list first. (b) The pattern is evaluated on every run, so a new script is scanned straight away. The criterion's own sentence allows (a); only the refutation line rules it out. | Opus | open | — |
| F-5 | MINOR | SPEC | base | `spec.md:47-48`, criterion 5 | The refutation needs only "a fixture containing only such imports" and names no spelling for the `stage2_*` family, while criterion 2 names five spellings for the runner. Take a checker that matches on a prefix in one spelling only. It refuses `from scripts.stage2_availability import x` or `importlib.import_module("scripts.stage2_runs")`, yet stays green under a fixture that holds only `import stage2_availability`. The criterion cannot go red for a prefix fault in spellings its fixture leaves out. Which family spellings the fixture has to hold, including an `importlib.import_module` literal naming a family member, is left to the builder. | Opus | open | — |
