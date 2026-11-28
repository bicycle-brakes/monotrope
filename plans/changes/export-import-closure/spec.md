---
title: "Spec — export-import-closure"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, export, imports]
class: bounded
appetite: 3
adr_files: []
---

# Spec — export-import-closure

The export carries the repository-local Python modules its carried scripts import, and a test prevents regressions (bead `coding-harness-5ane.7`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At commit `b03cf9c2`, the export manifest carries two bead checks but drops their shared `bead_render` module. Their function-level imports fail when the checks run. The reader in turn imports the dropped `render_beads_export` module; the research traced this cycle by reading the source on 2026-11-28.

## Terms

**Local import:** a statically written Python `import` or `from ... import` that resolves to a Python module or package in the repository, including imports inside functions; standard-library and third-party imports are outside this definition.

**Carried:** a file whose longest matching export-manifest prefix has the `carry` verdict.

## Acceptance criteria

1. When either carried bead check imports its local dependencies, the export includes `scripts/bead_render.py`.
   *Refuted by:* the manifest drops that reader while either check is carried.
2. When the carried reader imports its local renderer, the export includes `scripts/render_beads_export.py`.
   *Refuted by:* the manifest drops the renderer while the reader is carried.
3. When a carried Python file has a statically written local import, the closure test checks that the imported module or package is carried.
   *Refuted by:* a carried file imports a dropped local module, including inside a function, and the test passes.
4. When all local imports of carried Python files are carried, the closure test passes.
   *Refuted by:* the test rejects a closed fixture, including standard-library or third-party imports, or the corrected manifest.
5. When the closure test encounters a cycle of carried local imports, it terminates and accepts the cycle.
   *Refuted by:* the reader–renderer–check cycle makes the test fail or loop.

## Non-goals

- Installing or exporting the tracker executable, tracker data, or other non-Python runtime dependencies; static import closure does not establish that the checks can render tracker data in a target repository.
- Checking dynamic imports, external package installation, or all runtime paths.
- Changing the kit manifest or making tests travel with the export.

## Protected areas

The tracker database and customer instance are outside this change; neither is needed to check the export manifest.

## Definition of Done

- `make verify` green.
- Documents, models and ADRs moved with the code: none beyond this change's artifacts.
- The protected areas untouched and the non-goals unbuilt, shown by the pull request's file list.
- The pull request closes `coding-harness-5ane.7` (export import closure), and its last commit carries `Closes-Bead: coding-harness-5ane.7`.
- Special runs: none.

## Open decisions

None open. [DETAIL] Carry both existing modules instead of cutting their imports: this preserves the established reader and renderer and makes their transitive dependency visible. Count function-level static imports because the observed failure is inside `main()`; exclude dynamic imports and external executables because they require a different runtime-dependency contract.

[DETAIL] Spec-review S-1, S-2 (round 1, decided by the orchestrator under the bounded standing grant, 2026-11-28): S-1 — a static import name is local when a file `<root>/<name>.py` or a directory `<root>/<name>/` exists for a search root that is the carried file's own directory, `scripts/`, or the repository top (the roots the carried scripts reach through their runtime path edits, as `scripts/kit/probe.py:36` does); every other name is treated as standard library or third party and is not checked. "In the repository" means tracked by Git. S-2 — for `import pkg.sub` or `from pkg import sub`, the carried set must contain every `__init__.py` on the path from `pkg` down, and `pkg/sub.py` (or `pkg/sub/__init__.py`) when it exists; no other files under the package are required.

[DETAIL] Spec-review S-3, S-4 (round 2, orchestrator under the bounded standing grant, 2026-11-28): S-3 — the search roots are tried in the order the carried script's runtime path gives them: the file's own directory first, then `scripts/`, then the repository top; the first match is "the imported module" of criterion 3, and only that candidate must be carried. S-4 — relative imports (`ast.ImportFrom` with level > 0) resolve against the carried file's package directory (level 1 its own directory, each further level one directory up); `from . import x` names `x.py` or `x/` there, and criterion 3 applies to them.
