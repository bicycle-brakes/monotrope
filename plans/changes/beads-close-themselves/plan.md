---
title: "Plan — beads-close-themselves"
status: draft
implementation_status: partial
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-l1if
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, beads, reconciliation]
---

# Plan — beads-close-themselves

```text
For you:     merged completion trailers close their beads at the next eligible session start or own merge.
Done when:   make verify is green and isolated tests prove merged-only closure, safe repeats, writer eligibility and visible failures.
Appetite:    3 hours of phase 4 including repairs; a stop, not an estimate.
Not now:     CI closure, merge automation, new writer locking, other harness adapters or instance rollout.
Pre-mortem:  suppose it failed: most likely because the start hook writes before checking another session's ownership.
Starts unless you say stop.
```

Implements `spec.md`, criteria 1–12; bounded, no design or ADR due.
Explore used Stage 2, GLM 5.3 Flash, on 2026-10-31; no Stage-1 fallback.

## Steps

1. **Implementation attempt — create `scripts/close_merged_beads.py`.**
   CLI: reporting by default, writing only with `--write`; resolve the checkout
   and pinned `tools/bd` from the repository, including linked worktrees.
   Fetch `origin` main into `origin/main` with a bounded timeout, refuse shallow
   or unreadable history, pin the fetched SHA, traverse all its reachable
   commits (not first-parent or HEAD), parse trailers through Git, and deduplicate
   exact `Closes-Bead` entries deterministically newest-first. Accept one
   identifier per trailer, never shell text, lists or a free-form message match.
   Get state solely through `bead_render.render_pfad()` and validate the complete
   JSONL render; reject preset `BEAD_RENDER` for writes before rendering.
   Preflight failures return nonzero before any closure. Unknown identifiers
   and malformed declarations are reported, never created or guessed.
   Close each eligible id once through argv calls to
   `tools/bd close <id> --reason=<commit and explicit PR reference>`; never use
   `--force`, reassign, or alter already closed beads. Continue independent
   candidates after a refusal and preserve an overall failure result.
   Every eligible write run ends with `tools/bd dolt push`, including a no-op
   retry after a prior publication failure; report local versus published
   results distinctly. No cursor, committed export, PR API or automatic git push.
2. **Implementation attempt — change `Makefile`.** Add `close-merged` to
   `.PHONY`, its recipe and help, invoking the new script; allow only the empty
   argument or `ARGS=--write`, pass validated arguments as data, and refuse
   other values without executing them. Reporting mode never mutates the tracker.
3. **Implementation attempt — create
   `tools/claude-code/hooks/beads-start.sh`.** Consume SessionStart JSON once;
   identify the session and checkout; use the existing `hooks/session-scan.sh`
   to recognise live `clash` and `sibling` sessions, not unrelated repositories.
   Verify that the registry/scan is readable before trusting its empty result;
   missing identity or unavailable scan cannot mean sole writer. Skip writes
   for child runs (`CLAUDE_RECAP_CHILD`), compaction and uncertain eligibility.
   When eligible, run `python3 scripts/close_merged_beads.py --write` synchronously
   before pinned `tools/bd prime --hook-json`. Preserve valid prime hook JSON;
   add failure/skip context in German without mixing plain stdout into JSON,
   and still emit prime context after reconciliation failure. Use bounded
   subprocess timeouts; timeout/failure is visible, never a successful no-op.
   Invoke this repository hook directly; do not add it to the global installer.
4. **Implementation attempt — create `tests/test_close_merged_beads.py` and
   `tests/test_beads_start.py`.** Use disposable Git origins, real merge-parent
   history and a fake pinned-wrapper/render boundary; never use this repository's
   tracker or network. Test the CLI/Make target with recording fakes for close
   and push; test two runs, interrupted publication, duplicate trailers,
   unmerged local history, invalid values, unreadable/pre-set renders and wrapper
   refusals. For startup, use fake HOME/session registries and process/Git
   fixtures, checking event order, sibling worktrees, unrelated/dead sessions,
   child/compact inputs, eligibility failure and valid prime JSON after failure.
   These tests exercise the hook directly, so they do not depend on held wiring.
5. **Orchestrator after the accepted attempt — change held
   `.claude/settings.json`.** Replace only its direct prime SessionStart command
   with `bash "$CLAUDE_PROJECT_DIR/tools/claude-code/hooks/beads-start.sh"`, with
   an explicit timeout covering the bounded reconciliation and prime calls.
   Keep all merge ask/deny rules and other hooks. **Change
   `tests/test_omnigent_deny_layers.py`** in this same bootstrap step: update its
   exact hook-command expectation and add the ledger wiring test; keep the
   preservation/idempotence tests for the policy writer. The attempt must not
   edit `.claude/` or make its green tests depend on this later settings edit.
6. **Orchestrator after the accepted attempt — change held
   `prompts/07-commit.md`.** Keep the trailer as the only completion declaration;
   replace the absent CI-reporting promise with the implemented local command,
   session-start recovery and writer restriction. Add reconciliation after
   `gh pr view` confirms `MERGED`, never merely after queue admission; retain
   maintainer authority, exact-head protection and every queue/strict alternative.
   **Change `tools/claude-code/README.md`** to document the repository-local
   hook, conservative writer check, order before prime and failure/retry command;
   explain that it is not part of the user-level installed hook set.
7. **Orchestrator — update `plans/changes/beads-close-themselves/plan.md`** with
   measured phase-4 time and convert each implemented ledger entry from
   `not yet written` to its test form; retain implementation/review evidence in
   `plans/changes/beads-close-themselves/findings.md`. **Regenerate
   `plans/INDEX.md`** with `python3 scripts/plans_registry.py --index`, then
   verify the combined tree after the held-file bootstrap edits.

## Not touched

No deletions. No design file, ADR, new gate or workflow. Leave `tools/bd`,
`tools/claude-code/install.sh`, global settings/hooks, `scripts/plans_registry.py`,
`decisions/gates.yaml`, `.github/`, `scripts/ci_gates.py`, `scripts/stage2.py`,
`AGENTS.md`, `templates/`, endpoint settings, `.codex/`, `.agents/` and the
kit/export manifests unchanged. Existing catch-all manifest classifications
apply; no portability/rollout claim is made. No tracker writes during drafting,
implementation tests or review; operational closure belongs to the tracker writer.
The ordinary artefact/archive lifecycle remains a separate phase-7 duty.

## Verification

Run the targeted tests after implementation and again after the orchestrator
adds wiring, then the full gate on the combined tree:

```bash
python3 -m pytest tests/test_close_merged_beads.py tests/test_beads_start.py tests/test_session_scan.py tests/test_omnigent_deny_layers.py tests/test_merge_guard.py -q
python3 scripts/check_interview_minimums.py --change beads-close-themselves
python3 scripts/check_research_handoff.py --change beads-close-themselves
python3 scripts/check_criterion_ledger.py
make verify
```

The prompt names `scripts/validate_change_artefacts.py --check`, but that file
is absent at base `9b9e9116` (2026-10-31); do not invent a pass or build it here.
The runner owns draft verification and the commit. A live `--write` run is not
part of testing and must not be used merely to obtain evidence.

## Criterion ledger

- 1: tests/test_close_merged_beads.py::test_all_merged_declarations_are_closed — a merged side-parent declaration is missed or local HEAD controls eligibility.
- 2: tests/test_close_merged_beads.py::test_only_valid_merged_trailers_close — prose, an unmerged commit or a malformed value closes a bead.
- 3: tests/test_close_merged_beads.py::test_duplicate_and_closed_beads_are_not_rewritten — repeats trigger another close or overwrite a reason.
- 4: tests/test_close_merged_beads.py::test_reasons_identify_commit_and_explicit_pr — the declaring SHA or explicit PR is lost or an unrelated number becomes a PR.
- 5: tests/test_close_merged_beads.py::test_reporting_and_make_default_do_not_write — default CLI/Make invocation calls close or push.
- 6: tests/test_close_merged_beads.py::test_unreadable_preflight_never_closes — stale ref, shallow history, failed fetch or invalid/preset write render permits a closure.
- 7: tests/test_close_merged_beads.py::test_unknown_and_refused_closures_are_reported_without_force — refusal is hidden or ownership bypassed while valid items are lost.
- 8: tests/test_close_merged_beads.py::test_partial_and_retried_runs_publish — a partial batch or already-closed rerun omits dolt push.
- 9: tests/test_close_merged_beads.py::test_failed_publication_is_not_success — failed push exits zero or claims remote publication.
- 10: tests/test_beads_start.py::test_reconcile_finishes_before_prime — prime runs first or a failure loses prime context and its diagnostic.
- 10: tests/test_omnigent_deny_layers.py::test_start_hook_wires_reconciliation_before_prime — repository settings retain the old direct prime entry; orchestrator writes this after the accepted attempt.
- 11: tests/test_beads_start.py::test_secondary_or_uncertain_start_never_writes — a live same-repository session, child or unreadable scan permits writing.
- 12: not a test — phase-6 review reads prompts/07-commit.md against criterion 12; missing writer restriction or reconciliation before MERGED confirmation refutes it.

## Runner route — 2026-10-31

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-31 09:39:20–10:37:10 UTC, 3470 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-31 10:37:16–11:13:02 UTC, 2146 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-31 11:13:08–11:26:44 UTC, 815 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-10-31 12:28:48–12:45:39 UTC, 1011 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-10-31 12:45:45–12:59:20 UTC, 815 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · accepted · measured by the runner
