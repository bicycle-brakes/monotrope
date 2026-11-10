---
title: "Plan — triage-verb"
status: draft
implementation_status: partial
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-o2s1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, triage]
---

# Plan — triage-verb

```text
For you:     Record a loop-row decision with one command that preserves the table and refuses an ordinary taken status for a test-only location.
Done when:   Command tests prove the right row changes, invalid requests and failed writes preserve the record, guard authority stays explicit, and make verify is green.
Appetite:    2 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Model judgment, batches, proof-mark entry, released or phase-6 rows, model routing changes.
Pre-mortem:  suppose it failed: most likely because a reason containing a pipe shifted the proof column.
Starts unless you say stop.
```

## Scope and prerequisites

Implements criteria 1–8 of `spec.md`. Baseline read: `ae3402c2`, 2026-11-07.
Class remains bounded; no design or ADR is due. `findings.md` contains only
the runner audit, no phase-2a rows. Phase 1 used Stage 2, route `flash`,
endpoint `glm-coding-plan`, model `glm-5.3-flash`; no Explore fallback is
recorded. `templates/plan.md` and `scripts/validate_change_artefacts.py` are
absent at this baseline; this plan follows `prompts/03-plan.md` and does not
claim their gate passed.

## Build sequence

1. Add the `triage` registration and two positional operands to `main`:
   `<row>=<status>` and `<reason>`. Reject them for other verbs. Split the
   assignment once; accept exactly `taken`, `rejected`, `taken — not a test`,
   `taken — guard test`, with a separate nonempty single-line reason. The
   caller quotes operands containing spaces. Example:
   `python3 scripts/stage2.py triage triage-verb 'L1-1=taken — not a test' 'The finding only strengthens a test.'`.
2. Dispatch before any model `preflight`/`begin_call`: validate the change
   with `folder_of`, then hold `holding_record` across read, validation and
   replacement. Use the existing worktree-keyed `read_record`; missing or
   unreadable records refuse. Use `_record_lines` and `record_rows` so quoted
   reviewer text never becomes a target. Require exactly one target row,
   exactly nine physical cells on editable rows, and no `fixed` target.
   Refuse damaged records rather than repairing them implicitly.
3. Recognise file locations in `Where`, stripping Markdown delimiters and
   line suffixes. Classify test-only only when at least one repository file
   path is present and all such paths are below `tests/`; mixed locations,
   test-related prose and production paths do not qualify. Refuse ordinary
   `taken` there with Q-1's exact corrective form. Preserve explicit guard
   handling through `guard_authorised`; a quoted-only guard reason refuses.
   Do not read arbitrary paths named by a reviewer.
4. Construct the canonical status, escape literal and already escaped pipes
   once using the runner's cell conventions, and splice only the target's
   Status span. Preserve every other byte, including spacing, quotations,
   proof marks and the final newline. Publish once with `replace_record`;
   report invalid input/lock as exit 2, I/O failure as exit 1, success as 0
   with row ID and status. Do not append an audit line or change git state.
5. Extend `tests/test_stage2.py` using its isolated `World`/record fixtures
   and real `main` dispatch. Exercise the faults in the ledger, including
   competing lock ownership and injected replacement failure. Spy on model
   launch, repository writes and commit helpers; assert triage works with a
   dirty tree and absent credentials. Test resulting records with existing
   `record_rows`, `repair_targets`, `undecided`, `accepted_row` and
   `clean_round`; preserve the existing requirement for proof marks before
   a next round/release. Verify the command as a prerequisite to repair,
   never manufacture marks merely to make a row decided.
6. Update the workflow and help; after the runner accepts the implementation,
   the orchestrator applies the held prompt edit below and checks its example.
   Remove ledger `not yet written` prefixes only once tests exist. Record
   phase-4 time below; the runner owns full verification and its checkpoint.

## Files and ownership

- `scripts/stage2.py` — implementation adds CLI parsing, local triage dispatch,
  strict validation and the Status-only atomic rewrite, reusing record helpers.
- `tests/test_stage2.py` — implementation adds the tests named in the ledger
  and extends help/verb checks where the existing suite enumerates verbs.
- `docs/WORKFLOW.md` — implementation documents local triage in phase 4b and
  its routing table as no model call, with syntax, limits and proof ownership.
- `prompts/04b-review-loop.md` — orchestrator bootstrap edit after the accepted
  attempt adds the command example, refusal rule and existing mark procedure;
  the implementation attempt must not edit this held path.
- `plans/changes/triage-verb/spec.md` — update implementation status without
  changing criteria or the maintainer's answer.
- `plans/changes/triage-verb/plan.md` — record actual time and ledger progress.
- `plans/changes/triage-verb/findings.md` — runner-owned audit/review evidence;
  preserve existing content and never prewrite a verdict.
- `plans/INDEX.md` — runner-owned regeneration after artifact header changes.

No deletions. Do not touch `decisions.md`, `research.md`, `AGENTS.md`,
`templates/findings.md`, `scripts/stage2_runs.py`, endpoint declarations,
gates, provenance, tracker, accepted ADRs, other changes or tool provisioning.
The status vocabulary, table schema, model routes and counters stay unchanged.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'triage or shifted_broke or pipe_in_a_status or damaged_loop_row or guard_answer_requires_explicit_row_authorisation'
.venv/bin/python3 -m pytest tests/test_stage2_runs.py -q
python3 scripts/check_interview_minimums.py --change triage-verb
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

Full verification belongs to the runner. After the orchestrator's prompt
edit, rerun the triage help/instruction tests. Use temporary state roots,
never the maintainer's real loop record, for tests.

## Criterion ledger

- 1: tests/test_stage2.py::test_triage_records_each_supported_decision_in_the_worktree_record — dispatch refuses a valid form or writes a sibling worktree's row
- 2: tests/test_stage2.py::test_triage_changes_only_the_target_status_and_escapes_pipes_once — another byte changes or a pipe moves the mark column
- 3: tests/test_stage2.py::test_triage_refuses_plain_taken_for_test_only_locations_with_a_correction — ordinary taken is written, the correction is absent, or explicit not-a-test is refused
- 4: tests/test_stage2.py::test_triage_invalid_requests_leave_the_record_unchanged — invalid syntax, damaged/missing records, duplicate/unknown IDs or fixed targets succeed or mutate state
- 5: tests/test_stage2.py::test_triage_holds_the_record_lock_and_replaces_atomically — a lock competitor writes or injected replacement failure loses the old record
- 6: tests/test_stage2.py::test_triage_is_local_and_does_not_write_proof_or_repository_state — credentials/clean-tree checks, a model call, commit or unrelated write occurs
- 7: tests/test_stage2.py::test_triage_preserves_guard_authority_and_existing_loop_rules — quoted guard text gains authority, explicit guard is rewritten or taken counts as clean
- 8: tests/test_stage2.py::test_triage_help_and_instructions_match_the_cli_and_proof_ownership — the example fails parsing or operative instructions omit the refusal/mark boundary

## Runner route — 2026-11-08

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-08 01:59:33–03:32:07 UTC, 5554 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-08 03:32:36–04:19:14 UTC, 2798 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-08 04:19:38–05:04:02 UTC, 2664 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · accepted · measured by the runner
2026-11-08 13:25:15–20:26:14 UTC, 25258 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-08 21:53:58–2026-11-09 00:28:38 UTC, 9280 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-09 06:35:04–10:18:02 UTC, 13377 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-10 01:21:36–02:40:47 UTC, 4750 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-10 09:26:24–09:56:11 UTC, 1787 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
2026-11-10 11:13:24–12:03:51 UTC, 3027 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner
