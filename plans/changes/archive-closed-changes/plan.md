---
title: "Plan — archive-closed-changes"
category: plan
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-cqun
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, archive, plans-registry]
---

# Plan — archive-closed-changes

```text
For you:     completed changes leave the active list through make archive, once for the backlog and then after each merge.
Done when:   the measured closed-folder backlog is archived, the index matches, and make verify plus the recorded application evidence hold.
Appetite:    3 hours of phase 4 including repairs; stop at the limit.
Not now:     tracker closure, unrelated drift repair, historical link repair or startup/CI automation.
Pre-mortem:  suppose it failed: most likely because a folder's completion was inferred from its headers instead of its bead state.
Starts unless you say stop.
```

Implements `spec.md`, criteria 1–10; bounded, no design or ADR due.
Explore used Stage 2, GLM 5.3 Flash, on 2026-11-06; no Stage-1 fallback.

## Files and steps

1. **Implementation attempt — create `scripts/archive_closed_changes.py`.**
   Resolve the checkout from the script, including worktrees; expose reporting
   by default and `--write` only. Read state solely through
   `bead_render.render_pfad()` and validate with `check_bead_export.run()`;
   additionally reject duplicate IDs. Capture `date.today()` once. Enumerate
   immediate active folders in stable order, excluding `archive`; use the
   registry's artifact selection, require all artifact beads to agree, and
   select only exact `closed`. Report open, unknown, empty and mixed-bead
   folders with reasons. No tracker or Git writes, shell interpolation, fetch,
   subprocess closure, or selection by `implementation_status`.
   Report every prospective source/destination file by repository-relative
   path, including companions, so the application has an exact manifest.
2. **Implementation attempt — complete the same script's write path.**
   Preflight the complete eligible batch: readable uniquely keyed YAML
   mappings with required registry fields, valid original values/dates,
   writable destinations with no collision, and no symlink traversal in
   scanned source/destination boundaries or moved members. Reject malformed
   evidence without rewriting it. Build replacement headers in memory,
   editing/inserting only `status`, `implementation_status`, `updated` and
   `last_reviewed`; preserve every other value and the body bytes. Move each
   whole folder with filesystem operations, retaining companion bytes, then
   obtain the index from `plans_registry.render_index()` and replace it only
   when changed. Do not duplicate the index format or change the registry.
   On I/O failure stop, return nonzero and list completed/unfinished moves;
   never overwrite an existing destination or claim all-or-nothing recovery.
   Repeats see no active source and do not restamp historical files.
3. **Implementation attempt — change `Makefile` and `scripts/ci_gates.py`.**
   Add `archive` to `.PHONY`, its recipe and help. Follow `close-merged`'s
   checkout anchoring and raw command-line argument validation: only empty
   `ARGS` or literal `ARGS=--write`, transported as data, are accepted;
   environment arguments cannot silently opt into writing. Declare the new
   local command in `OHNE_AUFRUFER` with its Make/procedure caller and tests;
   no new gate or CI mutation.
4. **Implementation attempt — create `tests/test_archive_closed_changes.py`.**
   Use temporary fixture trees, controlled dates and mocked tracker-access
   boundaries; never the real tracker. Cover mixed header completion states,
   all skip reasons, non-Markdown companions, nested artifacts, header/body
   preservation, dry-run byte equality, duplicate/broken/empty renders,
   conflicting destinations, malformed headers, symlinks, repeat runs and
   injected move/index failures. Exercise CLI and Make argv handling with a
   recording fake. In fixtures reuse the real registry generator/checker
   with patched root constants and the real criterion-ledger checker to
   prove that moving does not exempt an invalid post-cutoff ledger.
5. **Orchestrator after the accepted attempt — change held
   `prompts/07-commit.md`.** After confirmed `MERGED` and
   `make close-merged ARGS=--write`, instruct the responsible session to run
   `make archive`, inspect its manifest and run `make archive ARGS=--write`
   in its own up-to-date cleanup worktree. Carry resulting changes through
   ordinary verification and a reviewed PR; never modify another session's
   checkout, automatically commit/push, or bypass the maintainer's merge.
   **Change `tests/test_archive_closed_changes.py`** in this bootstrap step
   to add `test_post_merge_procedure_orders_archive_after_closure`; the
   accepted attempt must neither edit the held prompt nor depend on its
   future wording for a green check.
6. **Orchestrator — apply once to the backlog.** Before moving, run the report
   and record its date, base commit, tracker-render source, each bead's state
   and every source/destination filename in
   `plans/changes/archive-closed-changes/findings.md`. These named files,
   measured at application time, are the exact operational move set; the
   research examples are not a whitelist. If the manifest changes, replace
   the proposed move inventory before writing. Run the write command and
   record its actual result and before/after registry output. Do not repair
   historical bodies/ledgers to manufacture a pass: surface any gate blocker.
   This operational batch is the orchestrator's work after acceptance, never
   the implementation attempt's live test. No current eligibility measurement
   was available during drafting; a named application inventory is still owed.
7. **Orchestrator — finish evidence.** Update
   `plans/changes/archive-closed-changes/plan.md` with measured phase-4 time
   and implemented ledger entries, retain review/application evidence in
   `plans/changes/archive-closed-changes/findings.md`, and regenerate
   `plans/INDEX.md` through its existing generator after artifact edits.
   Verify the combined diff after bootstrap and backlog application. Report
   remaining unrelated strict drift separately; it is outside this repair.

**Dependent consumers (recorded 2026-11-07).** Moving the backlog relocates
specs that real-repository tests read by path. Those tests follow the move to
the dated archive copy (`tests/test_stage2.py`, the paid-terms doctrine test;
`tests/test_research_handoff.py`, the framework research contract) instead of
skipping; no other test or script edit belongs to this change.

## Not touched

No existing script or test deletion, new ADR/design/gate, tracker write,
startup-hook change, gate exemption or living-spec promotion. Leave
`scripts/plans_registry.py`, `scripts/bead_render.py`,
`scripts/close_merged_beads.py`, all archive-sensitive checkers,
`tools/claude-code/hooks/beads-start.sh`, `tools/bd`, `docs/WORKFLOW.md`,
`plans/_README.md`, `plans/specs/`, pre-existing archived folders,
`decisions/`, `provenance.yaml`, routing, kit manifests, `.github/`,
`.claude/`, `.codex/`, `.agents/`, `.pi/`, `.mcp.json`, `CLAUDE.md`,
`AGENTS.md`, `README.md` and `templates/` unchanged. The only held edit is
the orchestrator's post-merge prompt step above.

## Verification

Targeted tests after implementation; include the prompt test only after the
orchestrator bootstrap. Run the combined tree through the full check:

```bash
python3 -m pytest tests/test_archive_closed_changes.py tests/test_ci.py -q
python3 scripts/check_interview_minimums.py --change archive-closed-changes
python3 scripts/check_research_handoff.py --change archive-closed-changes
python3 scripts/check_criterion_ledger.py
make verify
```

Operational evidence commands (orchestrator only, with its tracker access):

```bash
python3 scripts/plans_registry.py --check --strict
make archive
make archive ARGS=--write
python3 scripts/plans_registry.py --check --strict
make index
make verify
```

The first strict run may be red because it measures the backlog; record both
outputs and distinguish closed-active coupling from unrelated drift. Require
no eligible closed folder left active after application, not an invented
promise that archiving clears every kind of strict drift.
`scripts/validate_change_artefacts.py --check` cannot run: the file is absent
at draft base `8be8751e` (2026-11-06). Do not build it here or claim a pass.

## Criterion ledger

- 1: tests/test_archive_closed_changes.py::test_only_closed_single_bead_folders_are_selected — an eligible folder is omitted or an open, unknown, mixed, empty, archived or living folder is selected without the required skip report.
- 2: tests/test_archive_closed_changes.py::test_default_cli_and_make_are_read_only — reporting changes any file, calls a tracker writer or invokes a mutating Git command.
- 3: tests/test_archive_closed_changes.py::test_write_moves_complete_folder_on_captured_day — a source remains, a companion/body changes, or the date/name differs.
- 4: tests/test_archive_closed_changes.py::test_only_lifecycle_header_fields_change — any required field is wrong or an unrelated field/body changes.
- 5: tests/test_archive_closed_changes.py::test_index_matches_registry_after_archive — generated rows differ or registry closed-active coupling remains for the moved fixtures.
- 5: tests/test_archive_closed_changes.py::test_archiving_does_not_exempt_criterion_ledger — a deliberately invalid post-cutoff ledger stops failing solely because it moved.
- 6: tests/test_archive_closed_changes.py::test_preflight_failure_leaves_entire_batch_unchanged — broken render, duplicate IDs, malformed header, collision or symlink allows a mutation.
- 7: tests/test_archive_closed_changes.py::test_write_failure_reports_partial_work — injected move/index failure returns success, overwrites evidence or hides completed/unfinished work.
- 8: tests/test_archive_closed_changes.py::test_successful_repeat_is_byte_identical — rerunning restamps history, creates another copy or rewrites an unchanged index.
- 9: tests/test_archive_closed_changes.py::test_post_merge_procedure_orders_archive_after_closure — the procedure omits or misorders the write command, or tells a session to mutate another checkout; orchestrator adds after bootstrap.
- 10: not a test — the orchestrator's dated manifest, application transcript and before/after registry output in findings.md and the PR identify every moved file and show no eligible closed folder left active; any omission or unsupported all-drift-green claim refutes it.

## Runner route — 2026-11-07

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-11-06 16:19:48–17:39:17 UTC, 4768 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-06 17:39:27–18:21:25 UTC, 2518 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · accepted · measured by the runner
2026-11-07 09:11:25–10:22:14 UTC, 4249 s — repair · attempt 1 · route codex · model gpt-6.1-sol · rejected · measured by the runner
2026-11-07 10:22:26–11:05:06 UTC, 2560 s — repair · attempt 2 · route codex-repair · model gpt-6.1-sol · rejected · measured by the runner
2026-11-07 11:05:21–12:59:21 UTC, 6839 s — repair · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-07 13:28:08–14:07:02 UTC, 2333 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-07 14:49:40–16:43:38 UTC, 6838 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-07 18:38:38–19:24:10 UTC, 2731 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
