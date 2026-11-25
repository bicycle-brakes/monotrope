---
title: "Plan — worktree-setup-hook"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-wg4z
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, worktree, setup]
---

# Plan — worktree-setup-hook

```text
For you:     A new worktree sets up its Python environment and pinned Pi automatically when the checkout hook is enabled.
Done when:   Hook regressions, a real new-worktree smoke test and make verify pass.
Appetite:    Three hours of phase 4 including repairs; stop at the limit.
Not now:     Installing or configuring Git hooks, or setting up existing worktrees.
Pre-mortem:  suppose it failed: most likely because Git invokes a shared hook from a different checkout.
Starts unless you say stop.
```

## Build sequence

1. The stage-2 attempt creates `tests/test_worktree_setup_hook.py` using isolated temporary repositories and stub commands, with a fixture hook until the held hook is edited; it covers every ledger case without downloads. The tests must exercise the actual versioned hook once the orchestrator applies it.
2. After the accepted attempt, the orchestrator edits the held `.beads/hooks/post-checkout` outside the Beads-managed block. Detect the all-zero previous object ID and flag `1`, honour the exact opt-out, and run both setup commands and both checks from Git's new-worktree root. Run synchronously above the managed block with an overall `HARNESS_LANE_SETUP_TIMEOUT` limit (default 600 seconds); on expiry stop setup and report the step and limit. Write command and check output to `lane-setup.log` in the new worktree Git directory; emit one start and one result line, plus `LANE SETUP FAILED:` with step and log path for each failure. Continue after ordinary step failures, preserve the Beads invocation and exit status, and never propagate setup failures. Compare Pi output to the exact package pin; retain no shared working-directory assumptions.
3. The orchestrator edits held `AGENTS.md` to describe the hook and manual fallback; update `docs/WORKFLOW.md` §3 to match. Neither should promise setup when hooks are disabled or not installed. The local `core.hooksPath` was an absolute path to the main checkout on 2026-11-25, so a new worktree can invoke that shared copy; test this layout and state that the updated hook must be present at the configured path.
4. Run the tests against the actual hook and run a real temporary `git worktree add` smoke test with the updated hook at its configured path, confirming YAML and the exact Pi version; report the commit and result. The pull request records that after merge the tracker owner rewrites `new-worktree-needs-pi` to point to the hook, respecting the one-writer rule.
5. Update `plans/changes/worktree-setup-hook/plan.md` ledger markers as tests are written; the runner owns `findings.md`, time evidence and the plans index. No files are deleted; this bounded change has no design or ADR.

## Files and limits

- `.beads/hooks/post-checkout`: orchestrator adds setup outside the managed block; held from the attempt.
- `tests/test_worktree_setup_hook.py`: attempt creates isolated behavior and integration regressions.
- `AGENTS.md`: orchestrator updates setup guidance; held from the attempt.
- `docs/WORKFLOW.md`: update worktree guidance and manual fallback.
- `plans/changes/worktree-setup-hook/plan.md`: replace ledger markers as tests land; runner records elapsed time.
- `plans/changes/worktree-setup-hook/findings.md` and `plans/INDEX.md`: runner records evidence and regenerates the index.

Leave other hooks, Git configuration, dependency pins and historical handovers untouched. The tracker memory is a tracker operation, not a committed file.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_worktree_setup_hook.py
make verify
```

## Criterion ledger

- 1: tests/test_worktree_setup_hook.py::test_new_worktree_runs_venv_in_worktree — setup is omitted or uses the shared hook's directory.
- 2: tests/test_worktree_setup_hook.py::test_new_worktree_runs_pi_install_in_worktree — Pi installation is omitted or uses the wrong directory.
- 3: tests/test_worktree_setup_hook.py::test_yaml_check_reports_failure — a failed import is accepted.
- 4: tests/test_worktree_setup_hook.py::test_pi_version_check_reports_failure — a missing, failed or mismatched version is accepted.
- 5: tests/test_worktree_setup_hook.py::test_each_setup_failure_names_step — a failed step is silent or unnamed.
- 6: tests/test_worktree_setup_hook.py::test_setup_failure_does_not_fail_checkout — setup failure makes the hook fail.
- 7: tests/test_worktree_setup_hook.py::test_opt_out_skips_setup — an opted-out invocation runs setup or checks.
- 8: tests/test_worktree_setup_hook.py::test_other_checkouts_skip_setup — a normal checkout runs setup or checks.
- 9: tests/test_worktree_setup_hook.py::test_beads_integration_is_preserved — arguments or exit status change.
- 10: tests/test_worktree_setup_hook.py::test_setup_finishes_before_worktree_add_returns — Git returns before setup finishes.
- 11: tests/test_worktree_setup_hook.py::test_setup_timeout_stops_and_reports_step_and_limit — a stalled step continues or its report omits the limit.
- 12: tests/test_worktree_setup_hook.py::test_setup_precedes_failing_beads — failing Beads prevents setup.
- 13: tests/test_worktree_setup_hook.py::test_setup_output_uses_worktree_git_log — output reaches the caller or the log is elsewhere.
- 14: tests/test_worktree_setup_hook.py::test_setup_emits_start_and_result — either status line is missing or duplicated.
- 15: tests/test_worktree_setup_hook.py::test_only_one_opts_out — an unset or non-1 value skips setup.

## Explore fallback

On 2026-11-25 explore used the Stage-1 route, `claude-haiku-5-5`, because GLM through Z.ai had reached its weekly limit until 2026-11-29.

## Runner route — 2026-11-25

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM through Z.ai at its weekly limit until 2026-11-29.

## Time used

2026-11-25 14:46:40–14:48:55 UTC, 135 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 15:24:33–15:26:20 UTC, 107 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-25 15:52:40–16:01:28 UTC, 528 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · accepted · targeted verification, not the full `make verify`; result: green; test files `tests/test_worktree_setup_hook.py`; extra ruff targets none beyond the cheap checks; gates `leerprobe` (block), `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); reported without blocking: `docs-links` exited 1, `markdownlint` exited 1; a fresh full `make verify` is still required before phase 6 · measured by the runner
