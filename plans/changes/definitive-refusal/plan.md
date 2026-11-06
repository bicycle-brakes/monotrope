---
title: "Plan — definitive-refusal"
status: draft
implementation_status: none
date: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-2ym2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, review-loop]
---

# Plan — definitive-refusal

```text
For you:     A paid review rung refused with HTTP 403 or 410 retires itself so the loop can continue without manual retirement.
Done when:   Offline tests prove retirement, audit, continuation and unchanged transient failures, and make verify is green.
Appetite:    1.5 hours of phase 4 including repairs; stop at the limit.
Not now:     Other HTTP statuses, free or Flash policy changes, model declarations or permission hooks.
Pre-mortem:  suppose it failed: most likely because an incidental status number was mistaken for a definitive provider refusal.
Starts unless you say stop.
```

## Files and steps

1. `tests/test_stage2.py`: write the ledger's new tests first using `World`,
   scripted nonzero Pi exits and saved `loop_state` fixtures; use two or more
   rungs to observe order, consecutive retirement and exhaustion. Exercise
   explicit HTTP error forms, not just constructed exception messages.
2. `scripts/stage2.py`: carry explicit HTTP 403/410 evidence from a failed
   `run_reviewer` call in a distinct `CallFailed` subtype or structured field,
   before `fail` truncates the diagnostic. Recognize explicit provider HTTP
   error/status forms (including `HTTP 403` and `HTTP 410`), never arbitrary
   number substrings; successful output still passes through normal answer validation.
   Keep provider diagnostics bounded, scrub every secret before printing or
   storage, and quote them with `quote_reviewer` so they cannot become control text.
3. `scripts/stage2.py`: for a single paid rung only, persist a `Stage failed`
   block naming automatic retirement and update just that stage's consumption
   via the existing atomic `write_round`. Continue in `review_loop` from the
   updated record/state, retaining one deadline across retired rungs and using
   fresh record text for numbering. Preserve existing leak and admission checks
   before each next launch; stop on persistence failure, exhausted time or ladder.
   Do not route this through the command that attributes retirement to the maintainer.
4. `scripts/stage2.py`: keep failed-call audit accounting truthful: a retirement
   is not a round, no-round markers must not claim its stage was unconsumed,
   and audit calls must remain accounted for if continuation fails or no rung
   remains. Preserve the snapshot and quoted retirement through normal release.
5. `docs/WORKFLOW.md`: document the automatic paid-rung exception beside manual
   retirement and all-failed round semantics, including transient errors and
   the no-round audit wording. Existing policy and other failure paths stay.
6. `plans/changes/definitive-refusal/plan.md`: clear ledger markers once tests
   exist and record measured phase-4 time; `plans/changes/definitive-refusal/findings.md`:
   retain the runner's audit and record test evidence and review results.
   `plans/INDEX.md`: regenerate through `python3 scripts/plans_registry.py --index`.

No implementation files are created or deleted; the named tests are additions
to the existing suite. No held path needs editing; any later necessary held-path
bootstrap edit belongs to the orchestrator after the accepted attempt.

## Verification

```sh
.venv/bin/python3 -m pytest -q tests/test_stage2.py -k 'definitive or retirement or failed_flash_member or spent_ladder or expired_round or each_call_runs_its_own_leak_check'
python3 scripts/check_interview_minimums.py --change definitive-refusal
python3 scripts/check_criterion_ledger.py
PYTHON=.venv/bin/python3 make verify
```

For each new regression, first demonstrate its specified fault on the pre-fix
runner or an isolated fault injection, then its passing result. Use no live
provider calls. Also cover a refusal followed by a transient failure and a
deadline expiring after persisted retirement: only confirmed retirements remain.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_definitive_paid_refusal_retires_the_rung — parameterized 403/410 leaves the rung pending.
- 1: not yet written tests/test_stage2.py::test_definitive_retirement_write_failure_starts_no_next_stage — failed atomic persistence is followed by another model call.
- 2: not yet written tests/test_stage2.py::test_definitive_retirement_continues_in_saved_order — continuation needs another command, changes order or repeats a rung.
- 2: not yet written tests/test_stage2.py::test_definitive_retirement_does_not_extend_the_deadline — the next rung starts after expiry.
- 3: not yet written tests/test_stage2.py::test_definitive_retirement_preserves_protected_provider_evidence — status or diagnostic is lost, a secret escapes, or quoted text becomes control state.
- 4: not yet written tests/test_stage2.py::test_only_definitive_paid_provider_failures_retire — transient, local, malformed, successful-output or incidental-number cases consume a stage.
- 5: not yet written tests/test_stage2.py::test_definitive_retirement_is_not_a_completed_round — retirement creates a round, clean result or numbering gap.
- 6: not yet written tests/test_stage2.py::test_definitive_retirement_survives_resume_and_release — a retired stage repeats or prior history or evidence changes across release and continuation.
- 7: not yet written tests/test_stage2.py::test_definitive_retirements_exhaust_the_saved_ladder — exhaustion loses retirement, returns clean or calls an unsaved model.

## Boundaries and route

Do not touch the spec's protected areas or broaden free/Flash handling. Existing
manual retirement and general `CallFailed` behavior remain regression checks.
No design or ADR is due for the interviewed `bounded` class. Exploration ran
through Stage 2, GLM 5.3 Flash, on 2026-11-06; no Stage-1 fallback was recorded.
The requested aggregate artifact validator and plan template are absent in
this tree; use the available interview/ledger gates and the runner's document
checks without creating substitutes or weakening requirements.

## Time used
