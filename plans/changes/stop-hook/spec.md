---
title: "Spec — stop-hook"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-788
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, hooks, verification]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — `stop-hook`

A session with uncommitted Python changes gets a short, non-writing check at turn end; a red result blocks once, while a timeout warns and lets the turn end (bead `coding-harness-788`). Research: `research.md`. Maintainer answers: `decisions.md` Q-1 and Q-2 and the resolved phase-2a rows in `findings.md`.

## Problem

- The workflow promises a stop hook but the checked tree lacked it (research, checked 2026-11-03; notice based on `8ae99e50`). An agent can therefore hand back a red tree without this comfort check.
- The workflow notice and `README.md` name the hook as missing, and a test enforces that description (research, 2026-11-03). Delivery must update the description as well as the behavior.
- Full verification took about eleven minutes in CI on 2026-10-27 (research); the maintainer chose a bounded probe so a turn-end check stays useful.

## Terms

- **Changed Python path:** a `.py` path modified, added, deleted, renamed, staged or untracked relative to `HEAD`, including an index-only change. A rename includes both old and new paths.
- **Covering tests:** changed `tests/test_*.py` files run themselves. Other changed paths select test modules under `tests/` which mention the file path or filename, or import its module stem, including `import stem`, `import package.stem` and `from package.stem import ...`; match the last component on word boundaries. A deleted changed test is not passed to pytest as a file, but other tests referring to its path may be selected.
- **Probe:** read-only `ruff check` and `ruff format --check` on existing changed Python paths, then pytest with `-x` and per-test output on the nonempty covering set. A reported failed test is an observed red even before pytest exits. Deleted paths are skipped by ruff but still select covering tests. Pytest exit 5 (nothing collected) is green.
- **Block:** exit 2 with the reason on stderr. **Visible warning:** exit 0 with a JSON `systemMessage`.
- **Budget:** 60 seconds for the entire probe, overridable by a positive finite `HARNESS_STOP_HOOK_BUDGET` in seconds for testing. The override is read only when a probe is needed; an invalid value warns once per invocation.
- **Checkout:** the Git top level containing the Stop input `cwd`; if `cwd` is missing or outside a checkout, use `CLAUDE_PROJECT_DIR`.

## Acceptance criteria

1. When a normal Claude Code turn ends, `.claude/settings.json` invokes the executable `.claude/hooks/session-stop/check-tests-green.sh` as a Stop hook with a 90-second platform timeout.
   *Refuted by:* missing or non-executable hook, wrong command or timeout, or a changed existing SessionStart or permission setting.
2. When no Python path has changed, the hook ends the turn without starting ruff or pytest.
   *Refuted by:* a probe invocation or a blocked turn on a clean or Markdown-only tree.
3. When a Python path has changed and the probe succeeds, the hook ends the turn.
   *Refuted by:* no probe, a blocked green turn, or omission of a staged, unstaged, untracked, deleted, renamed or index-only Python path.
4. When an existing changed Python file has a lint or format finding, the hook blocks with exit 2 and names that file on stderr without modifying it.
   *Refuted by:* a lint or format finding passing, an incorrect exit or output stream, a missing file name, or a rewritten file.
5. When ruff finds red, pytest does not start and the hook blocks on that red even if later work would exceed the budget.
   *Refuted by:* pytest starting after ruff red, or a timeout replacing an already observed red with a pass.
6. When a covering test fails, the hook blocks with exit 2 and names both the changed Python path and the failing test on stderr.
   *Refuted by:* a failing selected test passing, or either path absent from stderr.
7. When a deleted Python path has covering tests, those tests run without passing the missing path to ruff.
   *Refuted by:* a deletion-only change being skipped, the missing path passed to ruff, or a failing test of the deleted path passing.
8. When a changed Python path has covering imports or path references, each matching test module is selected, including dotted imports and `from` imports.
   *Refuted by:* a matching test omitted or an unrelated stem selected solely by a substring match.
9. When the covering set is empty, the hook runs ruff on existing changed files without invoking bare pytest.
   *Refuted by:* pytest starting with no selected test path.
10. When pytest collects no tests and returns exit 5, the hook treats that result as green.
    *Refuted by:* exit 5 blocking a turn.
11. When the probe reaches its budget without a red result, the hook stops the probe process group and ends the turn with a visible warning that green was not confirmed.
    *Refuted by:* a timeout blocking, omitting the JSON warning, claiming green, or leaving a member of the probe process group running.
12. If a needed probe has an invalid budget override, the hook uses the 60-second default and warns once during that invocation, on stderr if the probe blocks and otherwise in the visible warning.
    *Refuted by:* an invalid value taking effect, a missing warning, an invalid override itself causing a block, or a red probe passing.
13. If Python, ruff or pytest cannot start, the hook blocks once with exit 2 and names `make venv && bash tools/pi/install.sh` on stderr as the fix.
    *Refuted by:* any missing dependency silently passing, a different exit, or an absent fix.
14. When a Stop call has `stop_hook_active` true after a block, the hook passes with a visible warning instead of blocking again.
    *Refuted by:* a repeated block, a repeated probe, or an invisible warning.
15. When the stage-2 runner starts a Claude Code work session or a research-swarm role, that session skips the stop hook.
    *Refuted by:* either launch site omitting the marker, a marked session probing or blocking, or an ordinary session skipping merely because the runner exists.
16. When the hook is delivered, the workflow notice lists it as supplied and identifies a dated commit that actually contains the hook, while retaining the validator in the absent list.
    *Refuted by:* the hook listed as absent, a missing or incorrect delivery commit or date, or the validator removed from the absent list.
17. When the hook is delivered, the workflow's comfort paragraph states the Python-change trigger, ruff and covering tests, 60-second budget, red block and timeout warning.
    *Refuted by:* any of those facts missing or contradicted in the paragraph.
18. When the hook is delivered, the `README.md` not-built list no longer names a stop hook.
    *Refuted by:* the stop-hook promise still appearing in that list.
19. When pytest reports a failing test before the budget expires, the hook blocks on that failure even if pytest is then stopped at the budget.
    *Refuted by:* a test reporting failure before a later stall yields a timeout pass, or the block omits the changed path or failing test.
20. When the Stop input `cwd` is inside a checkout, the hook inspects that checkout rather than the project directory.
    *Refuted by:* a changed Python path in a nested worktree being missed because only the project checkout was inspected.
21. When the Stop input `cwd` is missing or outside a checkout, the hook inspects `CLAUDE_PROJECT_DIR`.
    *Refuted by:* a changed Python path in that fallback checkout being missed.
22. When the hook is delivered, the phase table, verdicts paragraph and map in `docs/WORKFLOW.md`, the phase table in `AGENTS.md`, the gate line in `prompts/05-verify.md`, and the stop-hook row in `docs/testing.md` describe its limited probe and do not promise that every red tree blocks.
    *Refuted by:* any of these sites still claiming that all red trees block or describing the hook as the phase-5 enforcement gate.

## Non-goals

- Making the hook an enforcement gate, running full `make verify` inside it, or acquiring its machine admission lock; CI remains enforcement.
- Wiring other hook events, changing SessionStart or permissions, or changing user-level `tools/claude-code/` tooling.
- Kit travel, provenance classification changes, caching, metrics, or new reporting. The kit's separate decision on `.claude/` remains outstanding.
- Changing the meaning or enforcement of phase 5 beyond correcting descriptions of the hook.

## Protected areas

`decisions/gates.yaml`, `scripts/verify_all.sh`, `scripts/ci_gates.py`, `Makefile`, `.github/`, `provenance.yaml`, `scripts/kit/manifest.yaml`, `tools/claude-code/`, prompts other than `prompts/05-verify.md`, `templates/`, `model-endpoints.yaml`, and the tracker remain untouched. Only the Stop entry changes in `.claude/settings.json`.

## Definition of Done

- `make verify` green at the implementation commit; the hook and settings, runner session markers, tests, workflow notice and descriptions, `AGENTS.md`, `prompts/05-verify.md`, `docs/testing.md`, README and plan index move in the same pull request; no ADR.
- A live Claude Code session observation in `findings.md`, with date and commit, shows a green pass, a red block naming the files, and a visible timeout warning.
- Protected areas and non-goals remain untouched; the pull request closes `coding-harness-788` and the last commit carries `Closes-Bead: coding-harness-788`.

## Open decisions

None open. The phase-2a answers in `findings.md` settle their respective cases.

- [DETAIL] Use the worktree's `.venv/bin/python3` if usable, otherwise `python3` on `PATH`, with `python -m ruff` and `python -m pytest`; one environment exposes missing dependencies consistently.
- [DETAIL] Read Stop input JSON for `stop_hook_active` and use a runner-owned environment marker for runner sessions; this distinguishes the two exceptions without suppressing ordinary sessions.
- [DETAIL] Kill the probe process group at timeout; the test override makes this observable without waiting a minute. Format checks do not write because the maintainer chose reporting only.
- **Boundary:** Descendants that a test starts in a separate session can survive the group cleanup; tracking and terminating them is outside this change.
- [DETAIL] Per-test pytest output exposes a failure before a timeout, and `-x` avoids continuing after a failure; this carries the maintainer’s existing red-result decision into pytest.
- [DETAIL] Correct the phase-5 description in `prompts/05-verify.md` and the hook row in `docs/testing.md` along with the other doctrine sites; their present red-tree claims conflict with the decided limited probe.
- [DETAIL] `neighbours: []` records the legacy non-swarm exploration; the four research neighbours are reading, not swarm claims. Bounded changes have no design phase or ADR draft.
