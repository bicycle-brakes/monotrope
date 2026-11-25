---
title: "Spec — availability scrub import"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-vg9.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, availability]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — availability scrub import

The availability reader uses the runner it was given to redact errors, without importing a second runner (bead coding-harness-vg9.2). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At the worktree examined on 2026-11-25, `scripts/stage2_availability.py` imports `scrub` from `stage2` inside the intelligence-reading exception path, although the caller already holds the runner. When the runner is executed as `__main__`, importing it by name can load a second module, so that path can miss a patched or moved redactor. The module has no structural test preventing that import from returning (`research.md`, runner exploration).

## Acceptance criteria

1. When an intelligence fetch or response raises an exception, the status uses the redactor on the runner supplied by the caller.
   *Refuted by:* a substituted runner redactor is not called or its result is absent from the status.
2. When an intelligence fetch or response raises an exception containing credential material, the returned reading keeps the existing redaction and `not read` status behavior.
   *Refuted by:* a credential fragment appears in the reading, or the error is propagated instead of returning a `not read` reading.
3. While the availability module is loaded or executed, its source contains no `import stage2` or `from stage2 import` statement at any nesting depth.
   *Refuted by:* either form appears at module level or inside a function.
4. When intelligence data is read successfully, matching scores and per-model reasons retain their existing behavior.
   *Refuted by:* the existing matching or unmatched-model checks produce a different result.

## Non-goals

- Moving or redesigning the redactor, creating a shared secrets module, or refactoring the runner.
- Changing intelligence selection, reporting, or other availability functions beyond passing the runner to the reader.

## Protected areas

`scripts/stage2.py` and the shared-secrets question remain outside this change; the parent runner refactor owns that decision.

## Definition of Done

- `make verify` green.
- Documents, models and ADRs moved with the code: none beyond this change's artifacts.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead coding-harness-vg9.2 and its last commit carries `Closes-Bead: coding-harness-vg9.2`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The reader takes a keyword-only runner and the import guard inspects Python syntax, as recorded in `decisions.md`; these follow the existing runner-passing pattern and catch function-local imports.
