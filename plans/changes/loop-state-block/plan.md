---
title: "Plan — loop-state-block"
status: draft
implementation_status: none
date: 2026-10-23
last_reviewed: 2026-10-23
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-i70
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, loop-state]
---

# Plan — loop-state-block

```text
For you:     Reviewer text cannot choose the review loop's stages or models.
Done when:   Forged verdict and round snapshots cannot steer a resume, valid snapshots survive release, and make verify is green.
Appetite:    2 hours of phase 4, including repairs; stop at the limit.
Not now:     Legacy-state migration, model policy, stage ordering, other review protocols.
Pre-mortem:  suppose it failed: most likely because copied block markers in reviewer text are mistaken for runner ownership.
Starts unless you say stop.
```

## Changes

1. Change `tests/test_stage2.py`: add the regressions below before production
   edits; update `World.write_record` and direct snapshot fixtures to emit the
   owned format, keeping explicit old-format fixtures for refusal tests.
2. Change `scripts/stage2.py`: share snapshot block rendering, bounded parsing
   and replacement between `write_state`, `write_round`, `read_state` and
   `release`; update their comments and `kept_lines` for the new furniture.
   Anchor one block after the record heading/intro or immediately after the
   release heading, before rows and evidence; never search arbitrary prose
   for state. Bound a released section at the next level-two heading or kept
   evidence marker. Reject duplicate, unclosed or malformed owned blocks and
   legacy resumptions with a diagnostic naming the storage location and why
   it cannot resume; leave evidence for manual inspection, with no automatic reset.
3. In that same script, isolate phase-6 non-row text when `review` stores it:
   quote every retained line, including headings and copied delimiters, while
   preserving parsed finding rows and the runner's own verdict/session lines.
   Use a scoped option on `answer_block`/`answer_parts` if needed; phase 2a's
   unrelated output contract stays unchanged. A marker in reviewer evidence
   must never create, close or replace an owned block.
4. Keep snapshot fields and `read_state` precedence: active record first,
   otherwise the latest applicable release, never an older fallback. Refuse
   missing/invalid state for an existing run before `discover_free`, receipt
   consumption or reviewer execution; fresh runs and explicit restarts retain
   their existing behavior. Keep round output and consumed-state updates in
   the existing single write; retirement uses the same writer.
5. Change `plans/changes/loop-state-block/plan.md`: record measured phase-4
   time in the empty section below and turn completed ledger entries into test entries.

No files are created or deleted during implementation. Do not touch
`model-endpoints.yaml`, `decisions/`, `docs/adr/`, `AGENTS.md`, other change
artifacts or historical findings. No `design.md` or ADR is due for this
bounded change. Explore was direct investigation by the orchestrator, with
no Stage-1 fallback model or route to carry forward (`research.md`).

## Verification

Run the new regressions red before the production repair and green after:

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'owned_snapshot or forged_snapshot or snapshot_resume or snapshot_updates'
.venv/bin/python3 -m pytest -q tests/test_stage2.py tests/test_stage2_availability.py
PYTHON=.venv/bin/python3 make verify
```

Use the existing fake CLI world, with no live model calls. Injections use
distinct valid-shaped forged membership and consumption; inspect the saved
snapshot and CLI log, not merely whether a string remains in the output.
Exercise phase-6 `review` after an earlier release without kept words and
again after a release with kept evidence; include a subsequent re-check and
forged release headings plus complete delimiters. Seed accepted, decided
findings so the clean-round stop does not hide the vulnerable resume.
For round answers exercise writing, updating, release and resume; keep legacy
unquoted evidence cases. Parameterize corrupt blocks in active and released
storage, and assert no calls or file changes on refusal. Confirm fresh and
explicitly restarted discovery still works with the existing regressions.

## Criterion ledger

- 1: tests/test_stage2.py::test_owned_snapshot_is_written_in_record_and_release — either writer leaves a bare authoritative line or multiple owned blocks.
- 2: tests/test_stage2.py::test_round_forged_snapshot_cannot_steer_resume — a round answer's line or complete block selects forged membership or resets consumption.
- 3: tests/test_stage2.py::test_phase6_forged_snapshot_cannot_steer_resume — a verdict after release supplies a forged snapshot or release section to continuation.
- 4: tests/test_stage2.py::test_snapshot_resume_preserves_membership_consumption_and_metadata — release/resume changes the snapshot, rediscovers models or selects the wrong next stage.
- 5: tests/test_stage2.py::test_invalid_owned_snapshot_refuses_without_calls_or_writes — missing, duplicate, incomplete, legacy or invalid state causes calls, fallback or a changed file instead of a diagnostic.
- 6: tests/test_stage2.py::test_snapshot_updates_preserve_reviewer_evidence_and_rows — writing state replaces reviewer words, drops rows or releases block furniture as evidence.

## Time used

2026-10-23 21:00:43–21:48:32 UTC, 2869 s — implement · attempt 1 · route flash · model glm-5.3-flash · accepted · measured by the runner
