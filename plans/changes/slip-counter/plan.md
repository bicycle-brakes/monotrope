---
title: "Plan — slip-counter"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verification, run-log]
---

# Plan — slip-counter

```text
For you:     Read observed slips and incomplete runs beside each other from the local verification history.
Done when:   Matching runs count once, missing evidence stays visible, the real runner pairing is proved, and make verify is green.
Appetite:    3 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Slip records, unique-defect counts, CI/nightly collection, test tiers or changes to verification policy.
Pre-mortem:  suppose it failed: most likely because the recorded targeted tree cannot be matched to the later full check.
Starts unless you say stop.
```

## Prerequisite and build sequence

1. Orchestrator: wait for the targeted-check expansion (bead coding-harness-0swp — targeted checks for more runner verbs) to merge, then sync this branch and read its actual logging interfaces. Do not port its removed counter. First prove the accepted targeted attempt and later phase-6 full check can record the same checked-tree identity despite commit, stamping and audit finalization. Reuse existing evidence where sufficient. If they cannot, stop and report the boundary; do not silently substitute commit/dirty identity or invent tree exclusions.
2. Attempt: add red-first tests in `tests/test_verify_duration.py` for pairing, duplicate/conflicting records, selection, incomplete evidence, read-only reporting and legacy compatibility. Extend `tests/test_stage2.py` with targeted/full instrumentation and a real finalization-path regression; mock expensive gate execution, not the production history writer, tree capture, finalization or reader. Use isolated state roots exclusively.
3. Attempt: extend `scripts/verify_duration.py` with ordinary targeted-run recording and a read-only `slips` subcommand; extend `scripts/stage2.py` only at the actual targeted execution and phase-6 full-verification boundaries to provide comparison context. Keep logging outside verdict logic and use the existing safe append/refusal mechanism; never write a slip result. The contracts below are the implementation details phase 4 needs.
4. Attempt: update `docs/WORKFLOW.md` with the observation definition and evidence boundary; update `docs/orchestration.md` so a handover reports both counts and partial status; update `plans/specs/implementation-verification/spec.md` with the local measurement contract. These document existing decisions without amending ADR 0025.
5. Attempt/runner: update `plans/changes/slip-counter/spec.md` and `plans/changes/slip-counter/plan.md` statuses only as work happens, clear ledger markers once tests exist, leave measured time to the runner in this plan, and retain runner evidence in `plans/changes/slip-counter/findings.md`. Runner regenerates `plans/INDEX.md` before verification. No deletions, new source files, manifest additions or held-path bootstrap edits are planned.

## Evidence and reader contracts

- Keep `verify-duration.jsonl` as the one local history. Use its existing `run_start`/`run_end` records with additive optional comparison fields, preserving version-1 duration readability. Each start has an independent run id, repository/worktree attribution, change, check kind (`targeted`, `full`, or `full-fallback`), checked-tree identity and configuration digest; unknowns are explicit. Existing legacy starts remain valid duration records. End records retain the actual green/red verdict and time. No counter, pairing receipt or consumed flag is stored.
- Supply full-run context through an explicitly runner-owned environment passed to `full_verify`; let `verify_duration.cmd_start` capture it at the shell's existing start call. No `verify_all.sh` edit is needed. Targeted starts precede execution after preparation; ends follow completion. Capture identity on both sides of execution, invalidating comparison evidence if inputs move. Red, interrupted, timed-out and failed-to-start targeted work must never emit targeted green. Fallback remains full, never a green targeted predecessor. Diagnostics from failed appends are visible and leave existing verification results unchanged.
- Use the dependency's verified checked-tree capture, or the existing `worktree_tree` content-tree capture where sufficient; compare contents and modes, not commit ids. Keep repository, change and configuration in the match key. A missing field never matches another missing field. Do not broaden the checked tree's equivalence to make the counter useful: a failure of the prerequisite stops implementation.
- `python3 -m scripts.verify_duration slips [--since UTC] [--until UTC] [--change NAME]` defaults to the current resolved repository/worktree and all recorded time. Require timezone-aware bounds, normalize to UTC, reject reversed intervals with exit 2. Select full-run counts and incomplete-run counts by start time in `[since, until)`; search the whole available history for an earlier matching targeted completion, including before `since`. Completion must precede full-run start; overlapping checks do not pair. Show the selected repository, change scope and bounds with the result.
- Validate/group records before pairing. Identical duplicate events collapse; contradictory starts/ends or a malformed attributable record invalidate that run once. Count each qualifying red full-run id once regardless of predecessor multiplicity. Known nonmatching trees/configurations are non-slips; missing comparison evidence makes an otherwise in-scope run not countable. Legacy full runs therefore contribute to incomplete/not-countable runs, never inferred slips. Ignore complete unrelated jobs and placements. Diagnose unknown kinds/versions instead of treating them as clean evidence.
- Print `slips: N; incomplete/not countable runs: M` together. Exit 0 means complete readable evidence, even when N is positive; exit 1 means partial/unavailable evidence, with usable counts retained when possible; exit 2 means invalid invocation or refused/unreadable storage. A missing history yields unavailable with no invented zero. Malformed unassignable rows get separate diagnostics and partial status, not invented run counts; conservatively retain such diagnostics when interval or repository attribution is impossible. Reading never appends, repairs or creates history. Preserve the existing `report` command's duration behavior.

## Limits and route

No edits to admission, `scripts/verify_lock.py`, `scripts/verify_all.sh`,
`scripts/stage2_runs.py`, check selection, retry/timeout policy, CI, gates,
prompts, templates, endpoint configuration, tracker or other change folders.
Any newly necessary held-path edit goes to the orchestrator after the accepted
attempt, never to implement/repair. No design or ADR is due for class `bounded`.
Phase 1 used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash`; no Stage-1 fallback is recorded. The research's unread class
and scope are settled by decisions.md's class declaration and two answers.
At `8807a2b8` (2026-11-13), no plan template or change-artefact validator exists;
report that limit rather than claim that gate green. Findings contain only a
draft-call record, no phase-2a rows. Live PR and current parallel-session state
were not read within the runner's worktree-only boundary.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_verify_duration.py -q
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'slip or targeted or review_requires_fresh_full_verification_before_model_call'
.venv/bin/python3 -m ruff check scripts/verify_duration.py scripts/stage2.py tests/test_verify_duration.py tests/test_stage2.py
.venv/bin/python3 -m ruff format --check scripts/verify_duration.py scripts/stage2.py tests/test_verify_duration.py tests/test_stage2.py
python3 scripts/check_interview_minimums.py --change slip-counter
python3 scripts/check_research_handoff.py --change slip-counter
python3 scripts/check_criterion_ledger.py
make verify
```

These are phase-4 commands, not claims of execution during drafting. The
runner owns full verification and the commit; edits to `scripts/stage2.py`
retain full verification under the current hot-file rule. Demonstrate the
matching count and lost-end boundary with planted fixtures before and after
the fix; no real machine history or deliberately failing full suite is needed.

## Criterion ledger

- 1: not yet written tests/test_verify_duration.py::test_slips_count_each_matching_red_full_run_once — a qualifying run disappears or duplicate predecessors/events multiply it
- 2: not yet written tests/test_verify_duration.py::test_slips_require_complete_matching_predecessor — mismatched identity, order, kind or verdict produces a slip
- 3: not yet written tests/test_stage2.py::test_slip_history_captures_targeted_and_full_evidence — the real runner path fails to yield comparable evidence or writes a slip record
- 3: not yet written tests/test_stage2.py::test_slip_history_never_records_unfinished_targeted_green — interruption, launch failure, timeout or changing inputs leaves green comparable evidence
- 4: not yet written tests/test_verify_duration.py::test_slips_show_incomplete_runs_beside_count — a lost end, conflicting duplicate or missing comparison field vanishes instead of appearing once as not countable
- 5: not yet written tests/test_verify_duration.py::test_slips_select_interval_repository_and_change — interval endpoints or scope leak, or a pre-interval predecessor is lost
- 6: not yet written tests/test_verify_duration.py::test_slips_distinguish_complete_partial_and_unavailable_history — incomplete, corrupt, unsupported or missing history exits as complete or discards valid observations
- 7: not yet written tests/test_verify_duration.py::test_slips_are_read_only_and_preserve_duration_history — repeated reads mutate history or legacy duration reporting breaks
- 7: not yet written tests/test_stage2.py::test_slip_measurement_failure_preserves_verification_result — failed history writes change gate verdicts or disappear without a diagnostic
- 7: tests/test_verify_duration.py::test_reader_refuses_substituted_history — a symlink or nonregular history is followed
- 7: tests/test_verify_duration.py::test_writer_refuses_hard_linked_history — measurement writes through an aliased history

## Time used
