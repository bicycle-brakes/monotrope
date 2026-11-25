---
title: "Findings — test-ci-shared-tree"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.12
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — test-ci-shared-tree

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5751 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5752 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:3a05bca3b4859876c1aa85ea06e95dc90c775df50756e0e5a08b20fcaaf3a571

Spec review commit: 20f05467788bb5582608925fb82dd1558e29a4b2

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md, criterion 2 ("the same script glob") | Reading A: the control test calls the real `_scripts()` (e.g. aimed at the temporary tree through a parameter) and `_heimatlose_namen()`. Then dropping `*.sh` from `_scripts()` at `tests/test_ci.py:3534` turns the control test red. Reading B: the test repeats the glob pattern (`*.py` plus `*.sh`, minus `test_*`) over its temporary tree. Then dropping `*.sh` from `_scripts()` leaves the control test green while the real checks lose sight of `.sh` scripts again. The "Refuted by" line ("Omitting `.sh` from the glob") does not say which glob it means. Reading B defeats the purpose stated in the test's own docstring (`tests/test_ci.py:3606-3612`: prove that `_scripts()` sees a `.sh` file). | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-4 (2026-11-25) | — |
| S-2 | [AMBIGUITY] | SPEC | base | spec.md, criterion 3, "Refuted by" | "A real script under that directory is omitted". Reading A: omitted compared with today's set, which is the top-level `*.py` and `*.sh` files in `scripts/` that do not start with `test_`. The criterion holds on today's code and pins only the default root. Reading B: any script anywhere below `scripts/`. `scripts/kit/probe.py` is already left out by the non-recursive glob (`tests/test_ci.py:3534`), so the criterion is red before any change. Making it green would need a recursive glob, which changes the inventory policy (a non-goal) and would make the caller check report `probe.py`. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-5 (2026-11-25) | — |
| S-3 | MAJOR | SPEC | base | spec.md, criterion 1 | The refuting state is easy to build: keep the write to `REPO_ROOT / "scripts"` at `tests/test_ci.py:3619`. But nothing turns red in that state. The control test passes wherever its file lies, and the inventory tests pass when the tests run one at a time. The spec names nothing that checks where the file is written, so the criterion ledger would have to name a test invented while building. The obvious candidate, the control test asserting on its own path, only checks itself. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-6 (2026-11-25) | — |
| S-4 | MAJOR | SPEC | base | spec.md, criterion 3 | Refuting state: `_scripts()` defaults to an empty or temporary tree, or its callers at `tests/test_ci.py:3568` and `:3729` pass one. Then `test_every_script_has_a_caller_or_a_declared_reason` and `test_every_script_has_a_test_or_a_declared_reason` both pass on an empty list, because neither checks that the list has entries. No other test catches it. The spec's purpose is "without weakening the real script inventory checks", and nothing that could go red guards that part. The spec names no such check. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-7 (2026-11-25) | — |
| S-5 | MINOR | SPEC | base | spec.md, Problem and criteria 1–2 ("the orphan-shell-script control test") | The spec never gives the test's id. In `tests/test_ci.py`, `test_an_orphan_shell_script_gets_flagged` (docstring: "The control test to finding 11") fits the phrase as well as `test_the_glob_itself_finds_a_real_orphan_shell_script` (docstring: "The second half of the control test"). The first already meets criterion 1, because it writes no file. Only the Problem's "creates a file" and the indirect reference to the kit probe's comment point to the second; the id itself appears only in research.md. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-8 (2026-11-25) | — |
| S-6 | MINOR | SPEC | base | spec.md, criterion 2; decisions.md D-1 | The spec does not say what the orphan classification reads in the isolated case. Today the test passes the real `ci.yml`, `verify_all.sh` and `OHNE_AUFRUFER` (`tests/test_ci.py:3622-3626`). D-1 says the temporary tree holds "the files the orphan check reads", which suggests copies. Blank inputs, as in `test_an_orphan_shell_script_gets_flagged`, would also meet criterion 2. Each choice checks against a different set of callers (the real ones, copies, or none), and the implementer has to pick one without guidance. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-9 (2026-11-25) | — |
