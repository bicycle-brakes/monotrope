---
title: "Findings — export-import-closure"
category: findings
status: draft
implementation_status: none
date: 2026-11-28
created: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — export-import-closure

Stage-2 call, 2026-11-28: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1325 files, 6191 commits, 12 rules.

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6193 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:cae707a456f237848fb68e4c79b3b940496b009e4c2ce05999efdcbb7d6ba775

Spec review commit: cb02b7405b8865008bbc3bcffe98527482d3c67e

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | MAJOR | SPEC | base | spec.md § Terms "Local import"; acceptance criteria 3 and 4 | The spec does not say how the test resolves a static import name to "a Python module or package in the repository". It names no search roots and does not say which files count as in the repository. The carried files find their local modules only through runtime path edits. Line 36 of scripts/kit/probe.py adds scripts/ to the path before `import venv_guard` and `from _verdict import Verdict`, and the bead checks find `bead_render` only because scripts/ is their own directory. Reading 1: names are resolved against the importing file's directory or the repository root. Then `venv_guard` and `_verdict` resolve to nothing and are skipped as non-local, so dropping scripts/_verdict.py leaves the test green and criterion 3 misses a real case. Reading 2: "in the repository" means every file in the working tree on disk, not just tracked files. Then probe.py's `import yaml` resolves to the git-ignored .venv/lib/python3.12/site-packages/yaml/__init__.py, whose verdict is drop, so the test rejects the corrected manifest and criterion 4 goes red. The spec also does not say whether a non-standard-library name that resolves to nothing is ignored or is a failure. Nor does it say whether the carried Python files are listed from tracked files or from the disk. An implementer has to invent all of this. | Opus | in spec — local = tracked file or dir under the own dir, scripts/ or the repo top; [DETAIL] S-1, S-2 (bounded standing grant) | — |
| S-2 | MINOR | SPEC | base | spec.md § Terms "Carried" and "Local import"; acceptance criterion 3 | "Local import" includes packages, and criterion 3 requires that "the imported module or package is carried". But "Carried" is defined only for a single file. For `import pkg.sub` or `from pkg import sub`, the spec does not say which files must be carried: pkg/__init__.py alone, every parent `__init__.py` too, the submodule file `sub.py`, or every file under pkg/. No carried file imports a local package today, so the answer only decides how the fixtures behave, and an implementer would have to make it up. | Opus | in spec — every __init__.py on the path plus the submodule file; [DETAIL] S-1, S-2 | — |
