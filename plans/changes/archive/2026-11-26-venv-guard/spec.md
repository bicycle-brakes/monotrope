---
title: "Spec — venv-guard"
status: accepted
implementation_status: done
date: 2026-11-17
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-s55e
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-17"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, venv]
class: bounded
appetite: 2
adr_files: []
---

# Spec — venv-guard

Scripts started with the caller's Python use the checkout's environment when available, while kit instances retain their existing fallback (bead coding-harness-s55e). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-16 the workflow-start command failed when the system Python lacked PyYAML: `new_change.py` imports `plans_registry.py`, which imports that dependency before the command can run. The local verify runner chooses a suitable interpreter, but direct script callers do not (`research.md`, “Choosing the interpreter at verify time”; `decisions.md`, Q-1).

## Acceptance criteria

1. When a script reaches a third-party dependency that the current interpreter lacks and the checkout has a usable `.venv` interpreter, its invocation runs under that checkout's interpreter, retaining its arguments, working directory, output and exit status; an interpreter that already carries the dependencies continues (decisions.md Q-3).
   *Refuted by:* A system-Python invocation fails on a dependency or changes its observable invocation behavior despite a usable checkout environment.
2. When the invocation already runs under that checkout's interpreter, it continues without repeated re-execution.
   *Refuted by:* An invocation loops or starts a replacement process unnecessarily.
3. When the framework checkout has no usable `.venv` and a required third-party import is missing, the failure tells the caller to run `make venv`.
   *Refuted by:* The caller sees only a missing-module traceback or a misleading success.
4. When a kit instance has no `.venv`, the guard leaves its existing interpreter and dependency behavior unchanged.
   *Refuted by:* The guard exits, re-executes or changes the instance's missing-dependency diagnostic.
5. When a script in `scripts/` gains a direct third-party import without the guard before that import, an automated check fails.
   *Refuted by:* An unguarded new or reordered PyYAML, Jinja2 or pydantic import passes the check.
6. When a guarded module is imported by another script, the original invocation is preserved through any interpreter change.
   *Refuted by:* The imported module replaces the caller as the entry point or loses its arguments.
7. When the kit exports a script requiring the guard, the exported kit also contains the guard.
   *Refuted by:* An exported guarded script cannot load its guard in a clean kit instance.

## Non-goals

- A language-neutral launcher, changing callers' command lines, or changing the verify runner's interpreter-selection contract.
- Installing or repairing environments automatically, changing the dependency lock, or modifying cloud setup.
- Guarding non-Python tools; a language-neutral launcher returns as a separate change if Rust tools make it necessary.

## Boundaries

A restart replays the whole entry script, so the automated check of criterion 5 also requires the guard import to precede every top-level statement with an effect in a guarded script under `scripts/` (decisions.md, Q-4). A caller outside `scripts/` that prints or acts before importing a guarded module is outside that check: its earlier effect repeats once when the guard restarts it. The check is static and reads top-level statements only: a guard imported lazily inside a function, and an assignment without a call (to a name, a subscript or an attribute) before the guard, are outside it; such a state change also repeats once on a restart (phase-6 R8, R9, 2026-11-19). The Omnigent policy script is exempt from the guard because it also runs under Omnigent’s own Python. The trusted registry mirror excludes `.venv` to prevent execution through an attempt-controlled interpreter (decisions.md, Q-2).

## Protected areas

Do not change the dependency lock, CI interpreter declaration, generated CI workflow, or another change's artifacts: the decision concerns direct script startup.

## Definition of Done

- `make verify` green.
- The kit manifest accompanies the guard; no ADR or other documentation change is required.
- The protected areas untouched and the non-goals unbuilt, shown by the pull request's file list.
- The pull request closes bead `coding-harness-s55e` and its last commit carries `Closes-Bead: coding-harness-s55e`.
- Special runs: none.

## Open decisions

[DETAIL] A framework checkout is distinguished by the project and lock files that the kit does not carry; this keeps the missing-environment hint local while preserving the stated kit fallback. A broken or absent environment is unusable; the hint is emitted only for a missing third-party dependency, so unrelated import errors remain visible. These reversible choices reconcile both conditions in Q-1 without inventing a maintainer answer.
