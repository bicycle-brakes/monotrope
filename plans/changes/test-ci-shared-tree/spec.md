---
title: "Spec — test-ci-shared-tree"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.12
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, tests, xdist]
class: bounded
appetite: 1
adr_files: []
neighbours: []
---

# Spec — test-ci-shared-tree

The orphan-script control test runs in isolation without weakening the real script inventory checks (bead `coding-harness-bxxt.12` — isolate the shared-tree test). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-25, research found that the orphan-shell-script control test creates a file in the checkout's `scripts/` directory while other parallel tests enumerate it. Those tests can see the temporary orphan, and the kit probe can cache untracked files during that window (`research.md`, second runner exploration; confirmed in `tests/test_ci.py` at commit `790bf418`).

## Acceptance criteria

1. When the orphan-shell-script control test runs, it creates its orphan only in a temporary tree outside the repository checkout.
   *Refuted by:* The test creates its orphan inside the checkout, even if it later removes it.
2. When the control test runs, the same script glob and orphan classification used by the real inventory checks report its actual temporary `.sh` file as an orphan.
   *Refuted by:* Omitting `.sh` from the glob or treating the uncalled file as called leaves the control test green.
3. When the real inventory checks enumerate scripts, they continue to inspect the checkout's `scripts/` directory by default.
   *Refuted by:* A real script under that directory is omitted or a temporary tree replaces the default inventory.

## Non-goals

- Changing pytest scheduling to work stealing or parallelising the kit probe; the dependent work addresses those separately.
- Changing script inventory policy, CI configuration, or kit-probe behaviour.

## Protected areas

Production scripts, CI configuration and tracker data remain untouched: the change isolates a test, not the checks' policy or execution.

## Definition of Done

- `make verify` green.
- Documents, models and ADRs moved in the same pull request: none beyond this change's phase artifacts.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead `coding-harness-bxxt.12` — isolate the shared-tree test — and its last commit carries `Closes-Bead: coding-harness-bxxt.12`.
- Special runs: none.

## Open decisions

None open. [DETAIL] Keep the existing control-test name so the kit probe's dated reference stays accurate; one hour is the phase-4 stop because this is a focused test-only correction.
