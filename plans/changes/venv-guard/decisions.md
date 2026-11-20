---
title: "Decisions — venv-guard"
category: decisions
status: draft
implementation_status: none
date: 2026-11-17
created: 2026-11-17
last_reviewed: 2026-11-17
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-s55e
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-17", model: "Opus 5.5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, venv]
---

# venv-guard — Decisions

Class: bounded (bead coding-harness-s55e; one answered question is owed —
Q-1 below, answered by the maintainer on 2026-11-17 in the day session after
the night run 2026-11-16-a and recorded in the bead's notes).

## Q-1 · How the scripts find the checkout's own environment

asked: 2026-11-17
answer: "A mit den zwei Bedingungen. Es ist der kleinste Eingriff, repariert jeden Aufrufer auf einmal und gibt bei fehlender .venv eine klare Meldung. D ist ein guter Gedanke für später, falls die Rust-Werkzeuge konkret werden. Dann wäre es aber ein eigener Change mit eigener Entscheidung." — in English: option A with the two conditions; it is the smallest intervention, repairs every caller at once and gives a clear message when .venv is missing; option D (a language-neutral launcher) is a good thought for later, should the Rust tools become concrete, but then as a change and a decision of its own. Option A: one guard module at the start of each script; when the script does not run under the checkout's `.venv` and a `.venv` exists, it re-executes itself there; with no `.venv`, a clear "run make venv" message replaces the ModuleNotFoundError; callers keep `python3 scripts/...`. Condition 1: a test goes red when a script with a third-party import lacks the guard (house rule 9). Condition 2: kit fallback — in an instance repository without `.venv` the guard does nothing and the script runs as today.
answered_by: maintainer
status: answered
context: |
  Topic: the change venv-guard (bead coding-harness-s55e), scripts started with the system python3 fail because it lacks PyYAML.
  Intention: measured 2026-11-16 about 23:20 UTC in the night run 2026-11-16-a: the workflow-start skill runs exactly `python3 scripts/new_change.py <name> --bead <id>`, the system interpreter has no PyYAML, scripts/plans_registry.py fails with "No module named 'yaml'", and the skill forbids a retry, so no change folder can be opened through its one entry point; the stage-2 runner hit the same fault. It blocks the night-command lane (bead coding-harness-oswk).
  Today: every caller names bare `python3`; only `scripts/verify_all.sh` chooses the checkout's `.venv` interpreter itself. Measured 2026-11-17 on origin/main dfede341: 21 of 58 scripts import yaml; the third-party dependencies are PyYAML, Jinja2 and pydantic.
  Repository change: one guard module the affected scripts call first, a test that goes red when a script with a third-party import lacks it, and no change to any caller's command line.
  Architecture change: one choke point for the interpreter choice of the scripts; a language-neutral launcher (option D) stays out, for a later change of its own.

In the context of scripts that callers start with whatever `python3` is on
the path, facing a system interpreter without the locked third-party packages
and a skill that forbids a retry, we decided that one guard module at the
start of each script re-executes it under the checkout's `.venv` when one
exists and otherwise either names `make venv` or, in an instance repository
without `.venv`, does nothing, held by a test that goes red on a script with a
third-party import and no guard, to achieve one fix for every caller without
touching their command lines, accepting a re-exec at the start of those
scripts and a guard line in each of them — 2026-11-17

## Q-2 · Whether scripts/omnigent_policy.py carries the guard

asked: 2026-11-18
answer: "mache a und dann erstelle einen bead zu omnigenet" — in English: option A, apply the proposed hand finish (no guard in `scripts/omnigent_policy.py`, a declared exemption `NOT_GUARDED` for it in `tests/test_venv_guard.py`, `.venv` excluded from the trusted-registry mirror of `scripts/stage2.py`, `scripts/venv_guard.py` listed as a script without a CI caller), and create a follow-up bead for Omnigent.
answered_by: maintainer
status: answered
context: |
  Topic: the implement attempt of venv-guard (bead coding-harness-s55e) went red on 15 tests from three causes.
  Intention: the night run 2026-11-17-a parked the lane; the hand finish exceeded the night's hand-acceptance limit and relaxed criterion 5.
  Today: `scripts/omnigent_policy.py` runs under Omnigent's own Python as a hook; a guard there re-executes it into the checkout's `.venv` and breaks the hook. The trusted-registry mirror of `scripts/stage2.py` linked `.venv`, so a mirrored script restarted into the mirror's environment.
  Repository change: four files, about 15 lines (commit 45167828).
  Architecture change: one named exemption from criterion 5's automated check.

In the context of a hook script that must run under Omnigent's own
interpreter, facing a guard that would move it into the checkout's `.venv`,
we decided that `scripts/omnigent_policy.py` carries no guard and is named as
the one exemption in the guard test, to achieve a working Omnigent hook,
accepting that criterion 5's check skips that one file by name — 2026-11-18

## Q-3 · When the guard re-executes

asked: 2026-11-18
answer: "A + uv-Bead (Empfohlen)" — in English: the guard re-executes only when a required third-party dependency (PyYAML, Jinja2, pydantic) is not importable in the current interpreter, found without importing it; the marker, compared by value with the environment it names, only stops a loop; the `make venv` hint is installed in every framework checkout. A follow-up bead (coding-harness-b2mv) makes uv the one Python entry point for scripts, with the guard kept as the safety net.
answered_by: maintainer
status: answered
context: |
  Topic: review-loop round 2 of venv-guard, seven rows of one mechanism (L2-2, L2-3, L2-4, L2-8, L2-9, L2-14, L2-15).
  Intention: the re-exec marker the round-1 repair made presence-only is inherited by every child, so a guarded script of another worktree skips its guard and dies on PyYAML; this is the second finding of the marker mechanism, which ends case repair.
  Today: the guard re-executes whenever a usable `.venv` exists and the process is not in it; "usable" means only an executable file, so a broken `.venv` gets no hint; an explicit `$PYTHON` (verify_all.sh's documented escape) is overridden.
  Repository change: `scripts/venv_guard.py` and its tests; a follow-up bead for uv.
  Architecture change: the guard moves the process only when it must; the interpreter choice at the entry point is left to the uv bead.
  Options shown: A + uv bead (recommended); A without bead; switch to uv now (re-slice L6); B always enter the own checkout's `.venv` with a per-checkout marker. Asked first as A/B/C; the maintainer asked whether herdr, tmux, Orca or sandboxing solve it permanently — they do not choose the interpreter; uv at the entry point does.

In the context of a guard whose unconditional re-exec needs a marker that
children inherit, facing a second finding of that marker and an overridden
`$PYTHON`, we decided that the guard re-executes only when a required
dependency is missing from the current interpreter, keeps the marker only as
a loop stop compared by value, and shows the `make venv` hint in every
framework checkout, to achieve correct behaviour for children, other
worktrees and a chosen interpreter without per-case repairs, accepting that a
system interpreter which happens to carry the dependencies runs outside the
lock, as it did before this change — 2026-11-18

## Decided by the agent

[DETAIL] **The research did not read the bead.** The phase-1 exploration
(research.md, "What is unclear about it", item 1) could not hydrate the
tracker in the worktree, so its open questions 1 and 6 (scope and attachment
point of the guard) are answered by the bead text and Q-1 above: the guard
attaches at script start, not at verify time, build time or session start.
Reason: the bead (read 2026-11-17 from the main checkout with `tools/bd show
coding-harness-s55e`) names the failing callers and the maintainer chose A.

[DETAIL] **Condition 2 is read as: no `.venv` in the checkout → the guard
returns and the script continues under the current interpreter.** The
"run make venv" message applies when the script then fails on its
third-party import, which the guard may surface instead of the bare
ModuleNotFoundError. The exact split between "does nothing" and "clear
message" is left to the spec draft, which must keep both conditions true at
once; it is not a new decision because both behaviours were stated by the
maintainer. Reason: the two stated behaviours meet only at "no `.venv`", and
the kit fallback is the binding one there.

## Q-4 · The guard comes first

asked: 2026-11-19
answer: "A: Guard zuerst (Empf.)" — in English: the automated check of criterion 5 also requires that the guard import precedes every top-level statement with an effect in a guarded script under `scripts/`; the spec names the remaining case (a caller outside `scripts/` that acts before importing a guarded module) as a boundary.
answered_by: maintainer
status: answered
context: |
  Topic: phase-6 finding R2 of venv-guard, the third finding of the re-exec mechanism.
  Intention: a re-exec restarts the entry script, so an effect before the guarded import happens twice; Codex judged this not repairable in general, and a Sonnet heuristic failed ruff.
  Today: the guard runs at import time of a guarded module.
  Repository change: tests/test_venv_guard.py (the check of criterion 5) and a Boundary in spec.md.
  Architecture change: the guard is the first thing a guarded script does, enforced at the one check every script already passes.
  Options shown: A guard first (recommended); B heuristic that skips the re-exec after an effect; C name the limit and repair only R3.

In the context of a re-exec that repeats effects run before the guarded
import, facing a third finding of that mechanism, we decided that the check
of criterion 5 requires the guard before any top-level effect in guarded
scripts, to achieve a rule that turns red instead of a heuristic, accepting
that callers outside `scripts/` are named as a boundary — 2026-11-19
