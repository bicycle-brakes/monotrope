---
title: "Plan — implement-route-file"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-9ycy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, implement, routing]
---

# Plan — `implement-route-file`

```text
For you:     One central file selects the implementer, initially GLM 5.3, and records your instruction behind each switch.
Done when:   File-driven routing, preserved safeguards and matching instructions pass make verify after the ADR-edit interview prerequisite is met.
Appetite:    3 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     New endpoints, other runner verbs, different retry limits or a general routing engine.
Pre-mortem:  suppose it failed: most likely because a current instruction still selects a different implementer.
Starts unless you say stop.
```

Implements [spec.md](spec.md); no design phase for this bounded change.
The orchestrator must return the five-answer ADR-edit prerequisite to phase
1a before its ADR bootstrap edit: one answer stands at `ff012eba`, 2026-11-06.
Do not ask an implementing model to fill that gap or weaken the gate.

## Steps and ownership

1. **Worker — `scripts/stage2.py`:** add a strict, side-effect-free route
   reader using the repository's duplicate-key-rejecting YAML loader.
   Schema: `schema_version: 1`, `changes: [record, ...]`; each record has
   `date`, `stated_words`, `reason`, `primary` and `fallback`; each selection
   has `endpoint`, `model`, `effort`. Require exactly these keys, a nonempty
   sequence, valid nondecreasing ISO dates, nonblank text, and effort in
   `low`, `medium`, `high`, `max`. The last record alone selects the current
   route. Primary accepts only `glm-coding-plan` or `claude-code-plan`;
   fallback accepts only `claude-code-plan`, using existing file-tool work
   transports. Reject unsupported versions, wrong types, duplicate keys and
   unreadable files as `Refused` naming `implement-route.yaml`, before any
   secret read; endpoint/model admission remains the existing per-call check.
2. **Worker — `scripts/stage2.py`:** read once before `implement` preflight,
   use the primary tuple twice then the fallback tuple, and use fallback alone
   for explicit Stage 2 off. Read `GLM_KEY` only when a selected attempt needs
   the GLM transport; preserve scrubbing and the native fallback's clean
   environment. Use labels `configured`, `configured-repair`, `stage-1` and
   model-neutral diagnostic reasons. Keep fresh retry, post-check-only
   transitions, `run_attempts` protections, preparation and verification;
   do not route other verbs through this reader. Add `implement-route.yaml`
   to `RUNNER_HELD`, covering implement and repair through the existing
   case-insensitive prefix guard. No implementing attempt writes the file.
3. **Worker — `tests/test_stage2.py`:** seed valid route files in temporary
   worlds, adapt initial-model and label assertions, preserve existing test
   function names cited by other ledgers, and add the ledger's tests below.
   Vary valid configured models/efforts on both supported transports;
   parameterize malformed history, schema, missing file and duplicate-key
   cases. Test declaration/leak refusal on each rung, credential isolation,
   attempt-time configuration tampering and the held-path guard on both
   implement and repair. Retain current call-failure and rollback tests.
   Add a doctrine test taking candidate texts so its planted stale-model and
   missing-link faults can be checked before bootstrap; keep existing
   repository-reading doctrine assertions at baseline until bootstrap.
4. **Worker — `tests/test_stage2_runs.py`:** add mixed old/new audit and time
   label coverage using the existing parsers; keep historical foreign-route
   declaration probes unchanged. GLM 5.3 is already in their `FOREIGN_ROUTES`
   via `stage2.GLM`; no report implementation change is needed.
5. **Orchestrator bootstrap after the accepted attempt — `implement-route.yaml`
   (new):** write the initial schema record dated `2026-11-06`, primary
   `{endpoint: glm-coding-plan, model: glm-5.3, effort: max}`, fallback
   `{endpoint: claude-code-plan, model: claude-sonnet-5-5, effort: medium}`.
   Copy Q-1's exact maintainer words (`agent auf mein wort, aber es muss eine
   zentrales artifact dafür geben`), with a reason distinguishing its update
   authority from the GLM 5.3 switch stated in that record's context.
   Document that future changes append complete instruction-backed records
   and use ordinary PRs, never fabricate another quote or old history.
6. **Orchestrator bootstrap — `AGENTS.md`, `prompts/04-implement.md`,
   `model-endpoints.yaml`:** replace current primary-selection statements
   with the central file's authority and update rule; preserve explore's
   Flash route, the file-tool contract, fallback operation and endpoint
   admissions. These are held files, never worker edits. The orchestrator
   updates the corresponding real-text expectations in `tests/test_stage2.py`
   together with these edits, after the accepted worker attempt.
7. **Orchestrator bootstrap — `docs/WORKFLOW.md`:** replace all current
   implementation-selection prose and phase-table entries with the route-file
   reference, retaining the existing retry ceiling and Stage-2-off behavior.
   **`docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`:** after the interview
   prerequisite, amend only operative implementer-selection statements to
   defer to the file and its ordinary-PR update rule under Q-1; preserve
   historical decisions, explore routing and disclosure boundaries with a
   dated amendment note. No new ADR, ADR answer or decision-PR conversion.
   **`plans/specs/implementation-verification/spec.md`:** replace current
   Flash-only implementation wording with configured-primary wording,
   retaining its initial/retry/fallback counts, preparation order and guards.
8. **Worker — `plans/changes/implement-route-file/plan.md`:** remove each
   `not yet written` marker once its test exists; leave runner-measured
   phase-4 entries to the runner. **Runner/orchestrator —
   `plans/changes/implement-route-file/findings.md`:** retain audit, checks and
   review evidence. **Runner — `plans/INDEX.md`:** regenerate derived metadata.
   No files are deleted. The orchestrator reruns verification after bootstrap.

The worker's suite uses fixture route files and candidate doctrine texts;
no test requires the new repository-root file before bootstrap. After
bootstrap, the orchestrator runs the same reader on the real route file,
checks the real doctrine against criterion 10, and runs full verification.

## Do not touch

Keep endpoint admissions, `provenance.yaml`, `decisions/gates.yaml`, permission
settings, other ADRs, tracker state and every other verb's routes unchanged.
No edits to `scripts/time_records.py`, `scripts/run_report.py` or
`scripts/stage2_runs.py`: their route grammar and existing model declarations
already cover this change. No failed-edit-continuation change is bundled;
the old measurement's sequencing recommendation concerned a different ladder.
The research records a successful Flash Explore, so no Stage-1 fallback is
carried forward. Drafting does not start implementation or make commits.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py tests/test_stage2_runs.py tests/test_model_endpoints.py -q
python3 scripts/check_interview_minimums.py --change implement-route-file
python3 scripts/check_criterion_ledger.py
make verify
```

The requested `python3 scripts/validate_change_artefacts.py --check` is not
available in this tree; do not claim it passed. The runner prepares derived
files and runs its document check for this draft. Once the ADR diff exists,
the interview gate requires five answered records; the current one is not
enough, even though it passes the bounded-only check before that edit.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_implement_uses_the_last_configured_primary — a constant or earlier history entry wins
- 2: not yet written tests/test_stage2.py::test_implement_switches_by_route_file_only — changing the file fails to change the supported transport, model or effort
- 3: not a test — PR review compares retained history and exact words with Q-1 and the cited conversation; erased entries or invented words refute it
- 4: not yet written tests/test_stage2.py::test_bad_implement_route_refuses_before_secrets_or_calls — a malformed file is silently defaulted, crashes or starts work
- 5: not yet written tests/test_stage2.py::test_configured_implement_keeps_three_postcheck_attempts — a wrong retry, call-failure fallback or fourth attempt
- 6: tests/test_stage2.py::test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason — a primary call, GLM secret read or lost reason; adapt to configured fallback
- 7: not yet written tests/test_stage2.py::test_configured_implement_checks_each_attempt_admission_and_leaks — any rung calls despite refusal or advances after a leak
- 8: not yet written tests/test_stage2_runs.py::test_configured_implement_records_mix_with_historical_flash — actual-model evidence is wrong or either generation stops counting
- 9: not yet written tests/test_stage2.py::test_implement_freezes_route_and_holds_route_edits — tampering redirects a retry or survives a worker checkpoint
- 10: not yet written tests/test_stage2.py::test_implement_doctrine_uses_the_central_route_authority — candidate current instructions retain a competing primary or omit the update rule
- 10: not a test — orchestrator/phase-6 review checks all five real bootstrap surfaces against the tested text contract; an obsolete current instruction refutes it
- 11: not yet written tests/test_stage2.py::test_implement_route_does_not_select_other_verbs — a route-only edit changes another verb's dispatch
- 12: tests/test_stage2.py::test_first_implement_refreshes_derived_files_without_a_model_repair — a good first attempt needs a retry for generated metadata
- 12: tests/test_stage2.py::test_implement_and_repair_keep_full_verify_after_docs_draft — full verification is weakened
- 12: tests/test_stage2.py::test_a_leak_between_work_attempts_stops_before_fallback — a refusal reaches a later call

## Time used
