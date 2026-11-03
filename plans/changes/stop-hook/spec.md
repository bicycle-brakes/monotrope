---
title: "Spec — stop-hook"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-788
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3, version: "2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, hooks, verification]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — `stop-hook`

The goal in one sentence: a turn of a session in this repository ends only
after a quick probe — ruff and the tests covering the changed Python files,
at most 60 seconds — has run, and blocks only on a red result (bead
`coding-harness-788`). Research: `research.md`. Decisions: `decisions.md`
(Q-1, the probe and its budget; Q-2, the timeout).

## Problem

- The doctrine names the hook and the tree lacks it. Four sites promise it
  (`prompts/05-verify.md` gate line; `docs/WORKFLOW.md` §2 phase table and
  the verdicts paragraph, §3 map row "Stop hook"; `AGENTS.md` phase table),
  and the missing-pieces notice of `docs/WORKFLOW.md`, checked 2026-11-01
  against `8ae99e50`, lists `.claude/hooks/session-stop/check-tests-green.sh`
  as not in this repository (research, "What exists today"; Glob over
  `.claude/**`, 2026-11-03: no `hooks/` directory).
- `README.md`'s "Not built yet" section (2026-11-03, `6de1d036`) still
  promises "a stop hook that blocks a session end on a red tree", and the
  ratchet `tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands`
  holds the hook in the notice's *absent* half — a delivered hook would leave
  both lying (research, "A test ratchet holds the hook absent").
- What the hook would do was undecided until 2026-10-28: the
  `workflow-promises` change split it out precisely because "which check it
  runs, and how long it may hold a turn, changes how every session in this
  repository feels" (`plans/changes/workflow-promises/decisions.md`,
  `[DETAIL] The stop hook is split out`). The maintainer has since answered:
  a quick probe — ruff plus the changed files' tests, only when Python is
  changed and uncommitted, at most 60 s, blocking on red (decisions.md Q-1);
  a timeout ends the turn with a warning that nothing was confirmed green
  (decisions.md Q-2). Nothing in the tree implements either answer.
- Without the hook, an agent can hand back a red tree and only the hosted
  `verify` job catches it — the comfort layer the doctrine assigns to phase 5
  is absent (`docs/WORKFLOW.md` §2, verdicts paragraph; `docs/testing.md`,
  "Where tests run", read 2026-11-03).

## Terms

- **Changed Python file:** a path ending `.py` that differs from `HEAD` —
  modified, staged, renamed or untracked. Nothing else triggers the probe.
- **Probe:** ruff (check and format) on the changed Python files, plus
  pytest on their covering tests; one run, started only when a changed
  Python file exists.
- **Covering tests:** a changed file under `tests/` that matches `test_*.py`
  runs itself; for every other changed Python file, the test modules under
  `tests/` that name it — by its file name or by importing its module stem.
  A changed file no test module names contributes no test run (an accepted
  limit of the comfort layer, not a gap in enforcement).
- **Budget:** 60 seconds wall clock from the probe's start, overridable for
  tests through `HARNESS_STOP_HOOK_BUDGET`.
- **Blocks:** the hook ends nonzero with the red file named, the documented
  way a Stop hook holds a session open with its reason
  (`plans/changes/handover-at-95/research.md`, hook mechanics, read
  2026-10-14). **Warns:** the hook ends the turn and prints a warning.

## Acceptance criteria

1. When a turn ends in a checkout of this repository, the committed hook
   `.claude/hooks/session-stop/check-tests-green.sh` — executable — is
   started through a `Stop` entry in `.claude/settings.json` beside the
   existing `SessionStart` entry.
   *Refuted by:* a checkout whose settings carry no `Stop` entry, whose
   entry names a path that does not exist, or whose script is not
   executable.
2. When no changed Python file exists, the hook ends the turn without
   starting ruff or pytest.
   *Refuted by:* any ruff or pytest process started on such a tree, or a
   blocked turn.
3. When a changed Python file exists, the hook runs the probe, and a green
   probe ends the turn.
   *Refuted by:* a green tree blocked, or changed Python without a probe.
4. When the probe finds red — a ruff finding on a changed file, or a failing
   covering test — the hook blocks the turn end and names a red file.
   *Refuted by:* a red tree ending the turn, or a block that names no file.
5. While the probe runs longer than the budget, the hook stops it — leaving
   no probe process running — ends the turn, and warns that no green was
   confirmed.
   *Refuted by:* a timeout blocking the turn, an ended turn without the
   warning, or an orphaned probe still running after the hook returned.
6. When the hook is delivered, the `docs/WORKFLOW.md` missing-pieces notice
   lists it as supplied at a re-check dated to this change's baseline
   commit, and keeps `scripts/validate_change_artefacts.py` listed as
   absent.
   *Refuted by:* the hook still on the absent half, a re-check without its
   date or commit, or the validator disappearing from the absent half.
7. When the hook is delivered, `README.md`'s "Not built yet" section no
   longer names a stop hook.
   *Refuted by:* the promise of a stop hook that blocks a session end
   reappearing in that section.
8. If the probe's commands cannot start — no usable Python interpreter — the
   hook ends the turn with a warning instead of blocking.
   *Refuted by:* a missing interpreter blocking the turn, or the failure
   passing silently.

## Non-goals

- Making the hook a gate: no entry in `decisions/gates.yaml`, no change to
  `scripts/verify_all.sh`, `scripts/ci_gates.py`, the `Makefile` or
  `.github/workflows/ci.yml`. The hook can be skipped; the hosted `verify`
  job stays the only enforcement (`docs/testing.md`, "The stop hook can be
  skipped").
- Running the full `make verify` (about eleven minutes, CI 2026-10-27), or
  consulting the machine admission lock: the probe is ruff plus targeted
  pytest, and a queueing hook would hold every turn end
  (`plans/changes/research-swarm/decisions.md`, S-12).
- Wiring any other hook event, changing the `SessionStart` entry or the
  `permissions` lists of `.claude/settings.json`, or touching the
  user-level tooling under `tools/claude-code/` — a different layer.
- Travelling with the kit: the hook, its wiring and its tests stay
  `bestand` pending the kit specification's open decision D3; no
  `scripts/kit/manifest.yaml` entry, no probe-cap raise, no `REIST_NICHT`
  entry.
- Mapping `.claude/hooks/` in `provenance.yaml`: an unmapped path reports
  INFO only (`scripts/` likewise carries no entry); growing the map is its
  own classification work.
- Changing `docs/testing.md` or `prompts/05-verify.md`: both already state
  the trigger and the role correctly (research, "Which files a change would
  have to touch").
- Caching, metrics or reporting of hook runs; sub-second precision on the
  budget.

## Protected areas

- `decisions/gates.yaml` and every runner of the one gate list
  (`scripts/ci_gates.py`, `scripts/verify_all.sh`, `Makefile`,
  `.github/workflows/ci.yml`): the comfort/enforcement split stays.
- The existing `SessionStart` entry and the `permissions.ask`/`deny` lists
  of `.claude/settings.json`, held by `tests/test_omnigent_deny_layers.py`,
  `tests/test_merge_guard.py` and `tests/test_stage2.py`: only the `Stop`
  entry is added.
- `tools/claude-code/` (user-level display tooling), `prompts/`,
  `templates/`, `AGENTS.md`, `model-endpoints.yaml`, `scripts/stage2.py`,
  the tracker: no edit of this change touches them.

## Definition of Done

- `verify` green at the implementation commit.
- Moved in the same pull request: `.claude/hooks/session-stop/check-tests-green.sh`
  (new) and the `Stop` entry in `.claude/settings.json`; `tests/test_stop_hook.py`
  (new) and the flipped ratchet in `tests/test_workflow_entry.py`;
  `docs/WORKFLOW.md` (notice and the comfort paragraph's probe sentence);
  `README.md` ("Not built yet"); the regenerated `plans/INDEX.md`; no ADR.
- The protected areas untouched and the non-goals unbuilt, shown by the pull
  request's file list.
- Bead: the pull request closes `coding-harness-788`, and its last commit
  carries the trailer `Closes-Bead: coding-harness-788`
  (`prompts/07-commit.md`).
- Special runs: one live Claude Code session observation, recorded in this
  change's `findings.md` with commit and date — a turn ends on a green
  probe, and a planted red test blocks a turn end with the file named.

## Open decisions

None open. The maintainer's two answers stand in `decisions.md` (Q-1, Q-2);
the reversible details below are decided by the agent, with their reasons.

- [DETAIL] Exit vocabulary: exit 0 and silent when nothing triggers or the
  probe is green; exit 2 with the red file named when the probe is red; exit
  0 with a warning on a timeout or a probe that cannot start. Exit 2 with
  the reason is the documented blocking form of a Stop hook, and Q-2's
  "never hold a session without a red result" fixes the other two.
- [DETAIL] Interpreter: the checkout's `.venv/bin/python3` when it is
  usable, otherwise the `python3` on `PATH` — the selection rule of
  `scripts/verify_all.sh`, so the probe sees the locked environment.
- [DETAIL] Covering-test mapping: a changed `tests/test_*.py` runs itself;
  for every other changed Python file, a test module counts as covering when
  its text names the file (`<stem>.py`) or imports the stem
  (`import <stem>`, word-bounded). Name-stem equality alone fails in this
  repository (`scripts/ci_gates.py` is tested by `tests/test_ci.py`,
  `scripts/kit/probe.py` by `tests/test_kit.py`); the text match catches
  both, and over-inclusion errs toward safety inside the budget.
- [DETAIL] One budget over the whole probe, children killed as a process
  group on timeout; `HARNESS_STOP_HOOK_BUDGET` (seconds) exists so a test
  can exercise the timeout in roughly one second.
- [DETAIL] The hook reads no stdin JSON (nothing in it is needed) and finds
  the repository root with `git rev-parse --show-toplevel` from its working
  directory, which holds in worktrees.
- [DETAIL] No design phase and no ADR draft: the class is `bounded`
  (`prompts/02b-design.md`, decision D-14) and the architecture is
  unchanged — the doctrine already names the file, the wiring point and the
  role.
- [DETAIL] `neighbours: []`: this change explored through the flash route,
  not a research swarm, so the gate `research-handoff` reports the legacy
  exemption and the header claims nothing; the four sibling specs the
  research names stay reading, not claims.
