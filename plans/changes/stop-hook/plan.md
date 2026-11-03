---
title: "Plan — stop-hook"
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
tags: [plan, hooks, verification]
---

# Plan — stop-hook

```text
For you:     A session end runs a quick probe — ruff and the changed files' tests, at most 60 s — only when Python changed, and blocks only on red.
Done when:   The hook's tests, the flipped notice ratchet and make verify are green, and a live session shows both the block and the pass.
Appetite:    2 hours of phase 4 in total, repairs included; stop at the limit.
Not now:     Full make verify in the hook, gate-list or kit-travel changes, any other hook event.
Pre-mortem:  suppose it failed: most likely because a wide change made the probe time out at every turn end and the warning became noise.
Starts unless you say stop.
```

## Execution boundary

No design phase and no ADR draft: the class is `bounded` (D-14), the
architecture unchanged. The hook script, the settings wiring and the README
row sit on held paths (`.claude/`, `README.md`) — a stage-2 attempt never
writes them; the orchestrator adds them after the accepted attempt, and the
tests below are expected to be red until then, not completion. Explore ran
through Stage 2 (flash, `glm-5.3-flash`), and this draft through Stage 2
(`glm-5.3` after two failed Codex attempts); no Stage-1 fallback to carry
forward.

## Files and steps

1. **Runner:** create `tests/test_stop_hook.py` with the ledger's seven new
   tests. Every case builds its own git repository under `tmp_path`, puts a
   controlled `python3` first on `PATH` that logs each invocation (the
   pattern of `tests/test_workflow_entry.py::_controlled_python`), and runs
   the committed hook by absolute path. Fixtures: a clean tree or a `.md`
   edit only (2); a module with its passing test and a `ruff.toml`-clean
   file (3); a repo with a failing test and one with a ruff violation (4);
   `HARNESS_STOP_HOOK_BUDGET=1` and a test sleeping past it that writes a
   marker file only at its end — the marker must never appear (5); the
   notice and README text of this repository (1, 7); a `PATH` without any
   `python3` and no `.venv` (8). Criterion 1's test also asserts the script
   is executable.
2. **Runner:** edit `tests/test_workflow_entry.py` — in
   `test_workflow_notice_records_supplied_commands`, move
   `.claude/hooks/session-stop/check-tests-green.sh` from the absent half to
   the supplied half, keep `scripts/validate_change_artefacts.py` absent, and
   keep the both-lists exclusivity assertions.
3. **Runner:** edit `docs/WORKFLOW.md` — the missing-pieces notice moves the
   hook to the supplied half with a fresh check date and the delivery
   commit; the comfort-layer paragraph after the verify-lock section gains
   one sentence recording the decided probe (ruff and the changed files'
   tests, 60 s; a timeout ends the turn with a warning that nothing was
   confirmed green; maintainer 2026-10-28 and 2026-11-03).
4. **Orchestrator, after the accepted attempt:** create
   `.claude/hooks/session-stop/check-tests-green.sh`, executable, bash,
   implementing the spec's Terms and recorded details: find the root with
   `git rev-parse --show-toplevel`; collect changed Python files against
   `HEAD` (modified, staged, renamed, untracked); exit 0 at once when there
   are none; run `ruff check` and `ruff format --check` on them and pytest
   on their covering tests under one budget (60 s, `HARNESS_STOP_HOOK_BUDGET`
   override), children killed as a process group on timeout; exit 2 naming a
   red file on red, exit 0 with a warning on timeout or when no interpreter
   (`.venv/bin/python3`, then `PATH` `python3`) can start the probe.
5. **Orchestrator:** edit `.claude/settings.json` — add a `Stop` entry
   beside `SessionStart`, `"matcher": ""`, one command hook pointing at
   `"$CLAUDE_PROJECT_DIR"/.claude/hooks/session-stop/check-tests-green.sh`;
   the `permissions` lists and the `SessionStart` entry stay byte for byte.
6. **Orchestrator:** edit `README.md` — "Not built yet" drops the stop-hook
   promise and keeps the artefact validator.
7. **Orchestrator:** record the live-session observation of the Definition
   of Done in this change's `findings.md` (turn ends on green, planted red
   test blocks with the file named), update this plan's ledger from `not
   yet written` where the runner has not, fill `## Time used`, and
   regenerate `plans/INDEX.md` with `python3 scripts/plans_registry.py
   --index`. No files are deleted.

## Verification

Run from the worktree after step 4 (before it, the missing hook is the
expected red of step 1):

```sh
.venv/bin/python3 -m pytest tests/test_stop_hook.py tests/test_workflow_entry.py tests/test_omnigent_deny_layers.py tests/test_merge_guard.py -q
make verify
```

The settings-pinning suites run alongside because step 5 edits the file they
hold. No manifest, probe or gate file changes: both new files fall under
`bestand` catch-alls (`tests/`, `.claude/`), so the kit probe never sees
them and its cap stays at 44.

## Criterion ledger

- 1: not yet written tests/test_stop_hook.py::test_settings_wire_the_stop_hook — the Stop entry is removed, points nowhere, or the script lost its executable bit
- 2: not yet written tests/test_stop_hook.py::test_unchanged_tree_starts_no_probe — the hook starts ruff or pytest on an unchanged tree, or exits nonzero
- 3: not yet written tests/test_stop_hook.py::test_green_probe_ends_the_turn — a green probe exits nonzero or the invocation log stays empty
- 4: not yet written tests/test_stop_hook.py::test_red_probe_blocks_and_names_the_file — a red probe exits 0, or blocks without naming a file
- 5: not yet written tests/test_stop_hook.py::test_timeout_ends_the_turn_with_a_warning — the timeout exits 2, warns nothing, or the killed probe still writes its end marker
- 6: tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands — the hook sits on the absent half, or the re-check carries no date or commit
- 7: not yet written tests/test_stop_hook.py::test_readme_not_built_yet_names_no_stop_hook — the stop-hook promise reappears in the not-built list
- 8: not yet written tests/test_stop_hook.py::test_a_probe_that_cannot_start_warns_and_passes — a missing interpreter blocks the turn, or the failure passes silently

## Do not touch

`decisions/gates.yaml`, `scripts/verify_all.sh`, `scripts/ci_gates.py`, the
`Makefile`, `.github/` — the hook is comfort, never a gate.
`tools/claude-code/` — user-level tooling, a different layer.
`prompts/05-verify.md` and `docs/testing.md` — their statements stay true
as written. `provenance.yaml` and `scripts/kit/manifest.yaml` — unmapped is
INFO, unclassified-kit is not the case here, and both stay held. The
`SessionStart` entry and the `permissions` lists of `.claude/settings.json`.
`scripts/kit/probe.py` — no `REIST_NICHT` entry, no cap raise.

## Time used
