---
title: "Plan — export-import-closure"
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
tags: [plan, export, imports]
---

# Plan — export-import-closure

```text
For you:     Exported Python checks carry their local import dependencies, and a test catches future omissions.
Done when:   The corrected manifest and planted missing-module cases pass the closure checks and make verify.
Appetite:    3 hours for phase 4, including repairs; stop at the limit.
Not now:     Tracker installation, dynamic imports and other runtime dependencies.
Pre-mortem:  suppose it failed: most likely because the test overlooks imports inside functions.
Starts unless you say stop.
```

## Approach and files

- `scripts/export/manifest.yaml` — add `carry` rules for `scripts/bead_render.py` and `scripts/render_beads_export.py`; retain longest-prefix verdicts.
- `tests/test_export_import_closure.py` — add the closure test and focused fixtures. Enumerate tracked Python files with a `carry` verdict, parse all static imports including nested ones, resolve repository-local modules and packages against the importing directory and `scripts/`, and check every resolved local file's manifest verdict. Use the repository's actual manifest and tracked files for the integration case; use isolated fixture trees and manifests for planted faults, external imports and cycles. Report importer and missing module. Do not import the files or execute their bodies.
- `plans/changes/export-import-closure/spec.md` and `plans/changes/export-import-closure/plan.md` — keep these artifacts aligned with implementation if review requires it; the orchestrator owns any held-path edits.

The `bounded` class has no design phase or ADR. Do not change `scripts/kit/manifest.yaml`, the tracker, exported runtime installation, or dynamic-import behavior.

Explore fallback: stage 1, Claude Haiku 5.5 via `claude-code-plan`, because GLM through Z.ai had reached its weekly limit until 2026-11-29 (research, 2026-11-28).

## Criterion ledger

- 1: not yet written tests/test_export_import_closure.py::test_bead_reader_is_carried — the reader is dropped while a check is carried.
- 2: not yet written tests/test_export_import_closure.py::test_bead_renderer_is_carried — the renderer is dropped while the reader is carried.
- 3: not yet written tests/test_export_import_closure.py::test_missing_local_import_fails — a dropped local module, including a function-level import, is missed.
- 4: not yet written tests/test_export_import_closure.py::test_closed_export_passes — a closed fixture or the actual corrected manifest is rejected, including for external imports.
- 5: not yet written tests/test_export_import_closure.py::test_carried_import_cycle_passes — a carried cycle fails or does not terminate.

## Verification

Targeted: `python3 -m pytest tests/test_export_import_closure.py tests/test_kit.py tests/test_lock.py tests/test_venv_guard.py -q`

Full verification, started detached: `python3 scripts/jobs.py start -- make verify`

## Time used

2026-11-28 04:25:34–04:27:27 UTC, 112 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
