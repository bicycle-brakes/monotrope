---
title: "Spec — worktree-setup-hook-race"
status: draft
implementation_status: none
date: 2026-11-27
last_reviewed: 2026-11-27
updated: 2026-11-27
supersedes: null
superseded_by: null
bead: coding-harness-1ba3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-27"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, worktree, tests]
class: bounded
appetite: 2
adr_files: []
---

# Spec — worktree-setup-hook-race

A trusted new worktree gets its setup budget after the trust check, and the two budget tests distinguish the outcomes they claim to exercise (bead `coding-harness-1ba3`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- At commit `4d46d54a`, the deadline is set before the trust check; whole-second arithmetic can exhaust a one-second budget before `make venv` starts (`research.md`, 2026-11-27).
- At that commit, the not-started test accepts a timeout instead of proving its named path, and the timeout test also accepts a not-started message (`research.md`, 2026-11-27). The reported CI failure itself is not available in the tree.

## Acceptance criteria

1. When a trusted automatic setup starts, time spent checking trust does not consume the setup-step budget, and once `_ls_trusted` succeeds the shared `_ls_step` preamble starts step 1 (`make venv`, when `_ls_prev` is empty) with `_ls_left="$_ls_limit"` directly without a second `date +%s` subtraction before step 1 (keeping `_ls_deadline` set after `_ls_trusted` for step 2+ and leaving the no-Perl post-wait watchdog branch untouched per Non-goals).
   *Refuted by:* Invoking the hook directly (`lane.new_worktree_hook`, avoiding Git's `--exec-path` `PATH` prepend) with `PATH`-injected `git`, `date`, and `perl` shims where (a) `git` advances the controlled clock during `_ls_trusted` (either past the budget or by `limit - 1` seconds) and either `make venv` or `bash tools/pi/install.sh` (with zero controlled time spent in `make venv`) is reported as not started or receives a `perl` alarm argument below `_ls_limit`, OR (b) under `HARNESS_LANE_SETUP_TIMEOUT=1`, a `date` shim that increments by 1 second on each `date +%s` call causes `make venv` to be reported as not started or to receive a `perl` alarm below `1`.
2. On the Perl timeout path, when a completed `make venv` (exiting 0) consumes the setup budget, the next step is reported as not started and names `make venv` as the step that used it.
   *Refuted by:* The next step runs, or its failure line lacks either the not-started report or the name `make venv` as the preceding step.
3. When `make venv` exceeds the setup budget, the failure reports that `make venv` timed out at the configured limit.
   *Refuted by:* The test accepts a not-started report, a missing timeout or an incorrect limit.
4. When the setup budget expires, later setup steps do not run.
   *Refuted by:* An install, import or version check is recorded after the budget is spent.
5. While setup runs, the managed Beads integration block remains unchanged.
   *Refuted by:* Its contents differ from the block on `origin/main`.

## Non-goals

Sub-second clock dependencies, changes to trust policy, the managed Beads integration, changes to the no-Perl shell watchdog branch, adding a new test-only clock hook point inside `.beads/hooks/post-checkout`, and a general redesign of timeout enforcement are outside this change.

## Protected areas

The Beads-managed block in `.beads/hooks/post-checkout` is managed externally and must remain untouched.

## Definition of Done

- `make verify` green; the targeted hook tests pass.
- Documents changed with the code: this spec and `plan.md`; no models or ADRs.
- The protected Beads block matches `origin/main` (Criterion 5) and non-goals are unbuilt, shown by the pull request diff.
- The pull request closes the work item for the hook timeout race (bead `coding-harness-1ba3`), and its last commit carries `Closes-Bead: coding-harness-1ba3`.
- Special runs: none.

## Open decisions

[DETAIL] Use `PATH`-injected `git`/`date` shims (no hook-internal clock seam) so the controlled clock advances specifically inside `_ls_trusted` for Criterion 1 and inside `make venv` for Criterion 2's spent-budget path, and use a two-second budget for Criterion 3's real timeout test; these revisable test choices make the distinct paths observable without depending on a wall-clock boundary.

[DETAIL] Spec-review F-1..F-5 (round 1): F-1 Reading A — Criterion 2 covers the Perl path only, leaving the no-Perl shell watchdog untouched (Non-goals); F-2 — controlled clock uses `PATH` `git`/`date` shims advancing inside `_ls_trusted` (no new hook seam); F-3 Reading B — compute `_ls_deadline` after `_ls_trusted` and start step 1 (`make venv`) with the full `_ls_limit` directly so a second boundary before step 1 never prevents `make venv` from starting; F-4 — Criterion 1 refutes both full-budget and partial (`limit - 1`) trust-check advances; F-5 — DoD checks protected block via Criterion 5 diff against `origin/main` rather than PR file list (all decided under bounded standing grant).

[DETAIL] Spec-review F-6..F-8 (round 2): F-6 Reading A — Criterion 1's full-limit step-1 start applies to the Perl path while the no-Perl post-wait watchdog stays untouched (moving `_ls_deadline` after `_ls_trusted` still keeps trust time out of both paths); F-7 — Criterion 1 uses a `PATH`-injected `perl` wrapper recording the alarm argument passed to `make venv` so partial (`limit - 1`) advances are detected deterministically without wall-clock sleeps; F-8 — Criterion 1 invokes the hook directly (`lane.new_worktree_hook`) so Git's `--exec-path` prepend does not shadow the `PATH` `git` shim (all decided under bounded standing grant).

[DETAIL] Spec-review F-9..F-11 (round 3 final draft): F-9 — Criterion 1 refutes trust-check budget consumption on step 2 (`bash tools/pi/install.sh`) as well as step 1 when `make venv` spends zero controlled time; F-10 — Criterion 1 also refutes a second `date +%s` subtraction before step 1 using an auto-incrementing `date` shim under `HARNESS_LANE_SETUP_TIMEOUT=1`; F-11 Reading A — the full-limit step-1 assignment (`_ls_left="$_ls_limit"` when `_ls_prev` is empty) lives in the shared `_ls_step` preamble before the Perl/no-Perl split while the no-Perl post-wait watchdog branch stays untouched (decided under bounded standing grant; final draft after round 3 needs no fourth review).
