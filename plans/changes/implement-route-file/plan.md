---
title: "Plan — implement-route-file"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-08
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-9ycy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, implement, routing]
---

# Plan — `implement-route-file`

```text
For you:     One central file selects the implementer, initially GLM 5.3, and records your instruction behind each switch.
Done when:   File-driven routing, preserved safeguards and matching operational instructions pass make verify.
Appetite:    3 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     ADR edits, new endpoints, other runner verbs, different retry limits or a general routing engine.
Pre-mortem:  suppose it failed: most likely because a current operational instruction still selects a different implementer.
Starts unless you say stop.
```

Implements [spec.md](spec.md); no design phase for this bounded change.
The maintainer's Q-2 in `decisions.md` leaves all ADRs untouched and assigns
ADR 0007's pointer amendment to a separate PR with its own interview. This
plan replaces the earlier draft's ADR-edit prerequisite, not an interview rule.

## Steps and ownership

1. **Worker — `scripts/stage2.py`:** add a side-effect-free reader for
   `implement-route.yaml`, using the existing duplicate-rejecting safe YAML
   loader (`check_adr_answers.strict_load`). Schema: `schema_version: 1`,
   `changes: [record, ...]`; each record has `date`, `stated_words`, `reason`,
   `primary`, `fallback`; each selection has `endpoint`, `model`, `effort`.
   Require exact keys, integer version (not boolean), a nonempty history,
   valid nondecreasing ISO dates, nonblank text, and effort in `low`, `medium`,
   `high`, `max`. The last record supplies the active selection. Primary
   accepts `glm-coding-plan` or `claude-code-plan`; fallback accepts only
   `claude-code-plan`. Both use existing Claude Code file-tool transports.
   Reject missing/unreadable files, invalid encoding, malformed YAML,
   duplicate keys, invalid history or unsupported selections with `Refused`
   naming the file, before secrets or calls; never default to constants.
2. **Worker — `scripts/stage2.py`:** read once before implement preflight;
   build primary, fresh primary retry, fallback from that snapshot, or fallback
   alone for explicit `--stage2-off`. Read `GLM_KEY` only for a selected GLM
   transport; preserve scrubbing and a clean native environment. Use labels
   `configured`, `configured-repair`, `stage-1` and model-neutral reasons.
   Keep post-check-only retries, call-failure stops, per-call declaration and
   leak checks, preparation, full verification, timing and checkpoints.
   Add `implement-route.yaml` to `RUNNER_HELD`, using its case-insensitive
   prefix guard for implement and repair; do not redirect any other verb.
3. **Worker — `tests/test_stage2.py`:** seed route files in temporary worlds;
   adapt primary/label assertions without removing functions used by other
   ledgers. Add the tests below: multiple valid history entries; file-only
   model/effort switches on both transports; invalid schema/history/files;
   credentials; each rung's admission and leak refusal; retries and call
   failures; snapshot tampering; held route edits in implement and repair.
   Include a configured native primary with no GLM secret read and a changed
   native fallback with Stage 2 off. Keep existing rollback and preparation
   cases. Candidate-text doctrine checks can run before bootstrap; leave the
   real repository instruction assertions at baseline until bootstrap.
4. **Worker — `tests/test_stage2_runs.py`:** add mixed historical Flash and
   configured-label coverage using actual generated audit/time records,
   checking recorded endpoint/model as well as report counting. Leave the
   historical foreign-route probes unchanged: their tuple already includes
   `stage2.GLM`, and the existing record grammar accepts the new labels.
5. **Orchestrator bootstrap after the accepted attempt — `implement-route.yaml`
   (new, held by step 2):** add the initial complete record with date
   `"2026-11-06"`, primary
   `{endpoint: glm-coding-plan, model: glm-5.3, effort: max}`, fallback
   `{endpoint: claude-code-plan, model: claude-sonnet-5-5, effort: medium}`.
   Copy Q-1's exact maintainer words (`agent auf mein wort, aber es muss eine
   zentrales artifact dafür geben`); the reason distinguishes this edit
   authority from the GLM 5.3 switch stated in that record's context. Comments
   require future changes to append dated complete records with stated words
   and reason, through ordinary PRs on the maintainer's instruction. Do not
   invent an earlier history or a quotation of the contextual model switch.
6. **Orchestrator bootstrap — `AGENTS.md`, `prompts/04-implement.md`,
   `model-endpoints.yaml` (held):** replace operative primary selections with
   the file pointer and update rule; preserve Flash's Explore role, other
   verbs, fallback behavior, file-tool contract and endpoint admission.
   **`docs/WORKFLOW.md`:** update every current implement-selection passage
   and any model-selecting table entry to the file pointer, retaining retry
   limits and Stage-2-off behavior. Explain the temporary ADR 0007 discrepancy
   and separate follow-up without changing an ADR. **`tests/test_stage2.py`:**
   the orchestrator updates real instruction-text expectations alongside these
   bootstrap edits, retaining test names cited by other ledgers.
7. **Worker — `plans/specs/implementation-verification/spec.md`:** replace
   obsolete Flash-specific current implementation wording with configured
   primary wording; preserve all attempt counts, preparation order and guards.
   **`plans/changes/implement-route-file/plan.md`:** remove each ledger's
   `not yet written` marker when its test exists; keep `## Time used` for
   runner-measured phase-4 entries. **Runner/orchestrator —
   `plans/changes/implement-route-file/findings.md`:** retain audit and review
   evidence. **Runner — `plans/INDEX.md`:** regenerate derived metadata.
   No files are deleted.

The worker is not asked to edit any held path, including the new route file.
Its tests use fixture routes and candidate texts, so its check does not depend
on the later bootstrap. After bootstrap the orchestrator validates the real
file with the same reader, checks the four real instruction surfaces, and
reruns verification; worker acceptance alone does not complete the change.

## Do not touch

All `docs/adr/` files, `provenance.yaml`, `decisions/gates.yaml`, permission
settings, tracker state, endpoint admissions and every other verb's routing
stay untouched. No changes to `scripts/time_records.py`, `scripts/run_report.py`
or `scripts/stage2_runs.py`: existing labels and declared foreign routes suffice.
No retry-policy or failed-edit-continuation change is bundled; the older
measurement's sequencing recommendation concerned a different ladder.
Explore succeeded through Flash, so there is no Stage-1 Explore fallback to
carry forward. This runner draft writes planning artifacts only; the
orchestrator presents the card and starts phase 4 without another approval.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py tests/test_stage2_runs.py tests/test_model_endpoints.py -q
python3 scripts/check_interview_minimums.py --change implement-route-file
python3 scripts/check_research_handoff.py --change implement-route-file
python3 scripts/check_criterion_ledger.py
make verify
```

These are phase-4 checks, after worker edits and again after bootstrap.
The requested `python3 scripts/validate_change_artefacts.py --check` does not
exist at drafting base `924729ad` (2026-11-08); do not claim it passed.
The runner prepares derived files and runs its document check for this draft.
There is no ADR-edit interview prerequisite in this slice: Q-2 explicitly
splits that work, and both recorded answers remain untouched.

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
- 10: not a test — orchestrator/phase-6 review checks all four real instruction surfaces against the tested text contract; an obsolete current instruction refutes it
- 11: not yet written tests/test_stage2.py::test_implement_route_does_not_select_other_verbs — a route-only edit changes another verb's dispatch
- 12: tests/test_stage2.py::test_first_implement_refreshes_derived_files_without_a_model_repair — a good first attempt needs a retry for generated metadata
- 12: tests/test_stage2.py::test_implement_and_repair_keep_full_verify_after_docs_draft — full verification is weakened
- 12: tests/test_stage2.py::test_a_leak_between_work_attempts_stops_before_fallback — a refusal reaches a later call

## Time used
