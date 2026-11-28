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

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6195 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:7bfe08065b38a84fb70e35a45343a61db4bd2f2faa48a40a0778115da4b7c04b

Spec review commit: 122923f550eb5ef2d6927eb59d8778051b01bceb

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-3 | MINOR | SPEC | base | spec.md § Open decisions, [DETAIL] S-1 (resolution rule); acceptance criteria 3 and 4 | The S-1 rule says a name is local when a matching file or directory exists under any of three search roots: the file's own directory, `scripts/`, or the repository top. It gives no order for those roots. It also does not say which candidate criterion 3 means by "the imported module" when the name exists under more than one root. Take `scripts/kit/x.py` (carried) and `scripts/x.py` (dropped), both imported as `x` from `scripts/kit/probe.py`. If every candidate must be carried, the test rejects the fixture, even though the export runs: the dropped file is absent there and the import falls back to the carried one. If only the first candidate counts, the result depends on an order the spec does not give. The listed order puts the own directory first, so the test accepts the fixture. Python's real order for probe.py is the other way round: line 36 inserts `scripts/` ahead of `scripts/kit/`, so the dropped file comes first and the test rejects. No such collision exists today (`scripts/kit/` holds only probe.py), so the choice only decides how fixtures behave. But whoever writes the resolver loop has to invent it. | Opus | in spec — root order own dir, scripts/, repo top, first match counts; [DETAIL] S-3, S-4 | — |
| S-4 | MINOR | SPEC | base | spec.md § Terms "Local import"; § Open decisions, [DETAIL] S-1; acceptance criterion 3 | The S-1 rule resolves "a static import name" against three search roots. That covers `import x` and `from x import y`. It does not cover relative imports like `from . import x` or `from .x import y` (an `ast.ImportFrom` with level > 0, where the module name may be absent). The Terms definition still counts them as local imports, since they can only resolve inside the repository, so criterion 3 applies to them. If the walker skips them, a carried file with `from . import dropped` passes, which is exactly what criterion 3's own refutation describes. If it resolves them, it needs a base directory and a package rule that the spec does not give. No carried file uses a relative import today, so this only decides how fixtures behave. But the walker has to do something with these nodes, and the spec is silent on what. | Opus | in spec — relative imports resolve against the package directory; [DETAIL] S-3, S-4 | — |

Stage-2 call, 2026-11-28: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1328 files, 6199 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-28

Spec fingerprint: sha256:40383623af1d8f6fd012e3c0f8c15509e8131a79442140b02b11268d7a474f57

Spec review commit: baf93671a3acea6a99c1dd73e7b8c9e78df37d91

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-5 | MINOR | SPEC | base | spec.md § Open decisions, [DETAIL] S-1, S-2; acceptance criteria 3 and 4 | S-1 makes a name local when any tracked directory `<root>/<name>/` exists, whether or not it has an `__init__.py`. S-2 then says what must be carried only through the `__init__.py` files on the path, plus `pkg/sub.py` for a submodule. For a directory without an `__init__.py` (a namespace package, or a directory with no Python in it), a plain `import name` therefore leaves nothing to check. Take a carried `scripts/kit/probe.py` that contains `import export`. `scripts/export/` is tracked, holds only `manifest.yaml`, and has the `drop` verdict. Read literally, S-2 lets the test pass. But the import fails in the export, because the directory is not there. That is the state criterion 3's refutation describes. The other reading requires `name/__init__.py` to be in the carried set. Then the test rejects a namespace directory even when every file in it is carried, and criterion 4 goes red. The spec does not say which reading applies or what "carried" means for a directory. It also does not say which candidate is the first match under S-3 when `<root>/x.py` and `<root>/x/` both exist under the same root. Python takes a regular package before a module and a module before a namespace directory. No carried file imports a directory today, so this only decides how fixtures behave, but the resolver has to do something here. | Opus | open | — |
