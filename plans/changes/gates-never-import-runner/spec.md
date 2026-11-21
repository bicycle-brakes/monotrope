---
title: "Spec — gates-never-import-runner"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-7ayv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, gates, imports]
class: bounded
appetite: 1
adr_files: []
---

# Spec — gates-never-import-runner

Keep the existing gate-to-runner import boundary from regressing (bead coding-harness-7ayv). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-21 the research found no `scripts/check_*.py` importing `stage2`, but no check held that property. The runner can write the worktree, call models, read credentials and take verification admission; importing it into a read-only gate risks making its verdict depend on machine state. `research_census.py` already imports the runner but lies outside the named gate-script set.

## Terms

**Runner:** `scripts/stage2.py`, importable as `stage2` or `scripts.stage2`.

## Acceptance criteria

1. When the existing pytest gate runs, it checks every current `scripts/check_*.py` for imports of the runner.
   *Refuted by:* A newly added matching script containing `import stage2` leaves the pytest gate green.

2. When a checked script contains `import stage2`, `import scripts.stage2`, `from stage2 import …`, `from scripts import stage2`, or `from scripts.stage2 import …`, the check fails.
   *Refuted by:* Any one of those import forms, including an aliased or nested import, is accepted.

3. When a checked script calls `importlib.import_module` with the literal `stage2` or `scripts.stage2`, the check fails.
   *Refuted by:* Either literal call is accepted.

4. When the checker is given a temporary matching script that imports `stage2`, its negative control demonstrates that the checker rejects it.
   *Refuted by:* The negative control passes while the checker accepts that script.

5. When a checked script imports unrelated modules, including the `stage2_*` family, the check accepts those imports.
   *Refuted by:* A fixture containing only such imports is rejected.

## Non-goals

- Changing the runner, the `stage2_*` family, or `scripts/research_census.py`; the census is a known neighbour outside the named subject set.
- Restricting imports in `tests/`, indirect dependencies, computed module names, or dynamic import APIs beyond the literal `importlib.import_module` calls stated above. The check is a static source boundary, not a proof of runtime isolation.
- Adding a new gate-list entry, governance rule row or valve.

## Protected areas

The gate list and its generated views remain untouched: the existing pytest gate carries the check. Other scripts and tests retain their existing imports.

## Definition of Done

- `make verify` green.
- Documents, models and ADRs moved with the code: none beyond these change artifacts.
- The protected areas untouched and the non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead `coding-harness-7ayv` and its last commit carries `Closes-Bead: coding-harness-7ayv`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The one-hour phase-4 appetite is a stop suited to this bounded test-only change; the recorded import spellings and scope follow `decisions.md`.
