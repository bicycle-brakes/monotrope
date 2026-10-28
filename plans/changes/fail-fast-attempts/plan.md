---
title: "Plan — fail-fast-attempts"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-5tyh
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: gpt-6.1-sol, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, verification]
---

# Plan — fail-fast-attempts

```text
For you:     Work attempts stop on cheap failures before full verification; restoring findings no longer discards otherwise valid work.
Done when:   Deterministic tests prove the early exits, required tests and safe findings restoration, and make verify is green.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     New routes, extra attempts, model command permissions, review/research swarms or a replacement for full verification.
Pre-mortem:  suppose it failed: most likely because test selection misses the test that would have refuted the attempt.
Starts unless you say stop.
```

Proposed implementation against `1cd54168`, inspected 2026-10-28. Class
`bounded`: no design or ADR. No `templates/plan.md` exists; this uses the
phase-3 prompt's form. Explore ran on Stage 2, GLM 5.3 Flash; no Stage-1
fallback was recorded to carry forward. No implementation is changed by
this draft.

## Files and steps

1. `prompts/04-implement.md` — the orchestrator applies this runner-held
   edit and checkpoints it before the guarded implement call: require ruff
   and the ledger's test ids, delegating execution to the runner on file-only
   routes, and name findings as runner-owned in the repair instructions.
   Do not let the work model edit this protected path or loosen
   `RUNNER_HELD`; the guarded implementation starts from that clean baseline.
2. `tests/test_stage2_fail_fast.py` (new) — reuse `World`, its synthetic
   process recorder and repair helpers from `tests/test_stage2.py`; add the
   ledger regressions below with explicit command order and planted faults.
   Cover implement/repair, retries and Stage-1 routes, new/modified/deleted
   files, a retained edit, aliased findings and absent tools. No live calls.
3. `scripts/stage2.py` — extend only work-attempt verification and prompt
   construction; update their module/function descriptions. Take explicit
   targets from `changed_paths` against HEAD (including untracked files),
   never from the bounded display-only attempt file list. Keep existing safe
   formatting first. Then run `.venv/bin/ruff check --force-exclude --no-cache`
   and `.venv/bin/ruff format --check --force-exclude --no-cache` on surviving,
   ordinary changed `.py` paths; skip aliases/hard links as existing format
   selection does and leave their final verdict to the unchanged gates.
   Pass paths as argv, never a shell command.
4. In `scripts/stage2.py`, select (amended 2026-10-28, `decisions.md#Q-3`):
   in each surviving changed `tests/**/test_*.py` file, the top-level
   `test_*` functions that are new or whose AST differs from HEAD's (a file
   absent at HEAD whole); the snapshotted plan's ledger ids as function ids,
   using `check_criterion_ledger.ledger_sections`/`parse_entry`, both test
   entry forms, ignoring fenced examples and `not a test`; and, on a retry,
   the `FAILED <node id>` lines pytest printed in the previous attempt of the
   same run. Parse files, never import them. No importer selection.
   Deduplicate and sort.
   A selection/read/parse failure is a diagnostic, never an empty green set.
   Run `.venv/bin/python3 -m pytest -q -n auto` with the explicit targets
   only (revised 2026-10-28, see "Plan revision" below).
5. In `scripts/stage2.py`, use `runner_env`, the original `tool_state`,
   `launch` and `TOOL_SECONDS` for each cheap command. Stop at the first red,
   launch error or timeout before derived preparation and `make verify`.
   Capture command identity, exit/timeout and both streams, passing the
   complete output through existing diagnostic protection before bounded
   reduction. Feed that single protected result into existing findings,
   retry and measured-time handling. Cheap green continues through ledger
   clearing, derived preparation, intent-to-add cleanup, full verification
   and existing answer checks. Keep `verify_draft` and attempt routes intact.
6. In `scripts/stage2.py`, restore findings after existing HEAD checks,
   credential scanning and model-only file measurement, before formatting,
   cheap/full verification or answer checks can read model-written state.
   Reuse the whole-batch `preflight_recovery` and `restore_work_input`;
   restore the complete pre-call snapshot, not parsed rows. Remove the
   edit-as-failure behavior while retaining audit/body validation against
   the restored snapshot. Include a restore note in rejected-attempt
   bookkeeping, or a quoted restore-only notice under the current audit
   for a passing attempt: never label the latter failed. Repair still
   validates fixed lines and red-first evidence before the runner alone
   marks statuses. Preserve original evidence capture and stop ordering.
7. In `scripts/stage2.py`, derive the must-run references for
   `implementation_prompt` and `repair_prompt` from the original accepted
   plan snapshot, preserving that list on retries. Command-capable Codex
   must run ruff and the named tests before handback; file-only Flash and
   Sonnet explicitly delegate to the same runner cheap checks. Include
   not-yet-written ledger refs without claiming they already exist.
8. `tests/test_stage2.py` — extend the stand-ins/fixture with controlled
   local ruff and pytest execution and adapt command-order assertions.
   Update regressions demanding rejection solely for ruff/findings edits,
   including `test_a_ruff_failure_leaves_the_verdict_to_make_verify`,
   `test_implement_cannot_write_findings`, frontmatter forgery and earlier
   repair-evidence deletion cases. Keep their test names for existing
   ledgers, explain the new restoring/early-exit contract, and retain forged
   state, credential, alias and evidence assertions. Do not mock cheap
   checks globally away to make the older suite green.
9. `docs/WORKFLOW.md` — update the routing/verification and repair prose:
   safe formatting, cheap checks, red short-circuit, full-green requirement,
   ledger must-runs/delegation and restore notices; retain existing ladders.
10. `plans/changes/fail-fast-attempts/plan.md` — clear `not yet written` as
    tests land; let the runner append measured phase-4 spans below.
    `plans/changes/fail-fast-attempts/findings.md` — runner-only audit,
    restoration and review evidence. `plans/INDEX.md` — runner-regenerated
    index. No file is deleted.

## Verification

The orchestrator ensures `make venv` and `bash tools/pi/install.sh` have
completed once in this worktree before full verification. Demonstrate new
behavioral tests red against the baseline implementation, then green;
restore baseline faults after each proof. Selection tests include imports
with aliases, a deleted script's importer, ledger/file overlap, missing
ledger tests, and zero targets. Restoration tests include forged statuses,
erased earlier audit/diagnostics, deletion, a leaf alias and a refusing
parent; no external target may be written. Diagnostic tests use synthetic
credentials and controlled timeouts, not real provider calls.

```sh
.venv/bin/python3 -m ruff check scripts/stage2.py tests/test_stage2.py tests/test_stage2_fail_fast.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py tests/test_stage2.py tests/test_stage2_fail_fast.py
.venv/bin/python3 -m pytest -q tests/test_stage2_fail_fast.py tests/test_stage2.py
.venv/bin/python3 scripts/check_interview_minimums.py --change fail-fast-attempts
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

`scripts/validate_change_artefacts.py` is absent at the inspected baseline;
do not claim its `--check` passed or add it here. The draft runner owns full
verification, derived preparation, tracker-backed registry checking and
the commit. This drafting call does not run `make verify` or change git.

Draft checks on 2026-10-28: `check_interview_minimums.py --change
fail-fast-attempts` and `check_criterion_ledger.py` passed;
`check_research_handoff.py` passed with this non-swarm change exempt.
The tracker-backed registry and full verification remain for the runner.

## Criterion ledger

- 1: tests/test_stage2_fail_fast.py::test_red_ruff_skips_full_verification — lint or format red still starts make or accepts the attempt
- 2: tests/test_stage2_fail_fast.py::test_red_selected_pytest_skips_full_verification — a failing or uncollectable selected test still starts make
- 3: tests/test_stage2_fail_fast.py::test_cheap_test_selection_matches_changed_importers_and_ledger — a changed/retained file, direct importer or ledger id is omitted, duplicated or replaced by broad discovery
- 4: tests/test_stage2_fail_fast.py::test_empty_targets_skip_their_command — a zero-target check starts ruff/pytest or rejects a valid text-only attempt
- 5: tests/test_stage2_fail_fast.py::test_cheap_green_still_requires_full_verification — cheap green checkpoints without make or despite its red result
- 6: tests/test_stage2_fail_fast.py::test_cheap_failures_reach_findings_and_next_route_safely — original failure evidence is lost, a credential escapes, a rejected span disappears or the ladder changes
- 7: tests/test_stage2_fail_fast.py::test_prompts_require_ledger_tests_with_file_only_delegation — a ledger reference or must-run is missing, retries reread edited inputs or model tools broaden
- 8: tests/test_stage2_fail_fast.py::test_findings_edits_are_restored_without_spending_an_attempt — forged state reaches checks, good code is lost or an otherwise valid attempt is retried
- 8: tests/test_stage2_fail_fast.py::test_findings_restore_preserves_recovery_and_repair_guards — restoration writes through an alias or bypasses fixed-line/red-first validation
- 9: tests/test_stage2_fail_fast.py::test_findings_restore_notice_matches_the_verdict — restore evidence disappears, overwrites history or calls an accepted attempt failed
- 10: tests/test_stage2_fail_fast.py::test_unstartable_or_timed_out_cheap_checks_never_pass — missing/non-executable tools or a timeout reach full verification as green

## Not touched

No changes to `verify_draft`, review/research swarms, foreign-call transport,
route counts or models, model tool permissions, protected-path lists,
recovery containment, dependencies, gate configuration, lint rules, ADRs or
maintainer answers. Research and decisions are inputs after this draft;
spec criteria are not rewritten during implementation. No live benchmark,
tracker write, commit or push belongs to this drafting call.

## Runner route — 2026-10-28

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-10-28

Stage-1 route: implement · model claude-sonnet-5-5 · reason: three attempts rejected; six pre-existing tests left red; Sonnet came closest in attempt 3; 1.6 h of the 5.5 h appetite left.

## Plan revision — 2026-10-28

`[DETAIL]`, decided by the orchestrating session. Step 4 ran the selected
tests serially. Measured on 2026-10-28: implement attempt 1 of the Sonnet
route (18:34–18:41 UTC) was refused because the runner's own cheap pytest
check over the selected targets, which included the whole of
`tests/test_stage2.py` (1230 tests), "did not finish: .venv/bin/python3 was
stopped by the runner's tool limit after 5 minutes". The cheap check now
runs with `-n auto`, the same parallelism the `pytest` gate uses
(`decisions/gates.yaml`), and keeps `TOOL_SECONDS` unchanged. The runner
judges an attempt with the worktree's own `scripts/stage2.py`
(`REPO_ROOT` from the file path), so the change's cheap checks already ran
on itself; that is how the gap showed.

## Runner route — 2026-10-28

Stage-1 route: implement · model claude-sonnet-5-5 · reason: four attempts rejected; the cheap check now runs in parallel (84c1bfab); six pre-existing tests and the pinned cheap-check command left; about 1.4 h of the 5.5 h appetite left.

## Time used

2026-10-28 14:11:49–16:24:46 UTC, 7977 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-10-28 16:25:26–17:54:28 UTC, 5342 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-10-28 17:54:35–18:08:41 UTC, 845 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner

Appetite stop at 14164 s of 4 h (2026-10-28 18:2x UTC, three implement attempts rejected; the last left 6 red pre-existing tests that plan step 8 says to adapt). Answer: continue — the maintainer named a new appetite of 5.5 hours in total (conversation, 2026-10-28). It replaces the card's Appetite line.
2026-10-28 18:34:10–18:41:17 UTC, 426 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-10-28 18:43:53–18:52:11 UTC, 498 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
