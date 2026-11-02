---
title: "Plan — sonnet-continues-flash"
status: draft
implementation_status: none
date: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
supersedes: null
superseded_by: null
bead: coding-harness-6ie
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: gpt-6.1-sol, version: "2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, attempts]
---

# Plan — sonnet-continues-flash

```text
For you:     After a Flash abort, the next implementation route continues from a protected copy of the partial work and reports why it switched.
Done when:   Deterministic tests prove copied continuation, preserved inputs and visible transitions; make verify is green.
Appetite:    4 hours of phase 4, repairs included; stop with saved evidence when exhausted.
Not now:     Repair fallback, container deployment, new models, extra attempts or broader model permissions.
Pre-mortem:  suppose it failed: most likely because recovery restores the baseline before preserving the partial work.
Starts unless you say stop.
```

Proposed against `baffe4a3`, inspected 2026-11-02; class `bounded`, so no
design.md. Follow spec.md and the five recorded answers. No templates/plan.md
exists at this baseline; this follows prompts/03-plan.md. Explore used Stage 2,
GLM 5.3 Flash on 2026-10-31; no Stage-1 fallback is recorded to carry forward.

## Files and steps

1. `tests/test_stage2_continuation.py` (new) — reuse `World` from
   `tests/test_stage2.py` for the ledger tests below. Exercise real local
   attempt-copy creation and recovery with synthetic model processes; no
   paid calls. Prove cumulative edits, additions, deletions, binary files,
   half-written files, mixed abort/check failures and two consecutive aborts.
2. `scripts/stage2.py` — add an implement-only continuation policy to
   `run_attempts`; default it off for repair. Keep Flash, Flash repair, Sonnet,
   their efforts and the single Stage-1 route. Classify `CallFailed` from the
   model-call boundary only as an abort; never catch verifier, checkpoint,
   snapshot or recovery failures as model availability failures. Each ordinary
   abort consumes its scheduled slot, even if no files changed.
3. In `scripts/stage2.py`, run each implementation model in a fresh private
   local checkout with independent writable files and Git metadata, seeded
   from the initial committed baseline plus the preceding permitted work.
   Use runner-owned temporary storage, not a model-selected path, and fresh
   model processes; do not reuse or resume a prior session. Build the copy
   without hard-linking workspace files or following model-created aliases.
   Provision its own required tools with the existing worktree setup contract
   (`make venv`, pinned Pi install) and validate them before calls; do not
   copy or share mutable model-modified tools. The canonical checkout stays
   runner-owned and its initial HEAD and index are checked before promotion.
4. In `scripts/stage2.py`, keep the invocation's trusted input snapshot from
   committed Git: spec, plan, optional decisions/design, phase prompt, rules
   and every other prompt-builder input. Before each call overlay only the
   runner's audit, diagnostics, route and time records; never accept the
   candidate's version of those records. Findings remains runner-owned and
   retains its normal audit/verification role. Initialize the next checkout
   from permitted implementation changes, restoring these inputs separately.
5. In `scripts/stage2.py`, build a cumulative baseline-to-candidate handoff
   with path status and diff, not just the last attempt's changes; explicitly
   say continue rather than redo and warn of incomplete files after an abort.
   Include deletions and untracked non-ignored additions. For binary or large
   content, name every changed path and supply a runner-owned diff artifact
   inside the next checkout with an explicit reference; never silently truncate
   the handoff. Treat it as untrusted evidence, scan/protect it like existing
   diagnostics, and leak-check the exact next prompt and candidate tree.
6. In `scripts/stage2.py`, reuse `save_attempt` semantics with a unique
   invocation/attempt identity to retain an aborted candidate before disposing
   of its environment or starting the next call. Preserve cumulative permitted
   bytes; scrub credentials first and stop on exposure under existing policy.
   On save/copy/restore failure stop with the retained location, no next model
   call and no cleanup of the sole surviving copy. Exhaustion exits 1 with
   recoverable last work and unchanged canonical branch HEAD. A normal abort
   does not run verification on unfinished files or fabricate a completed-call
   duration; existing completed-call time accounting stays intact.
7. In `scripts/stage2.py`, print each abort transition and insert a runner-owned
   record before `## Time used` in plan.md: source/destination attempt, route,
   model, abort reason and recovery reference. Do this for Flash → Flash repair
   too, not just Sonnet. Restore these records across subsequent failures.
   Do not create review findings for route transitions; ordinary call audits
   may still appear in findings.md. Keep post-check diagnostics and causes
   distinct from abort diagnostics in mixed failure sequences.
8. In `scripts/stage2.py`, run existing cheap and full checks on each completed
   candidate under trusted runner/tool controls, retaining findings restoration
   and held-path checks. Promote only an accepted cumulative candidate into the
   canonical checkout with safe create/change/delete handling, recheck the
   canonical state and complete the existing checkpoint contract once. A moved
   HEAD, external alias, tool mutation or refused promotion stops without
   fallback; retain evidence and never overwrite concurrent canonical work.
9. `tests/test_stage2.py` — update only implement assertions that require
   failed-call rollback/stop, including the failed/empty-call, baseline restore,
   restored-file message and saved-attempt tests. Preserve their names for
   existing ledgers; replace obsolete expected behavior with abort continuation
   and preservation assertions. Adapt the synthetic process recorder to record
   private checkout cwd and inspect cumulative candidate bytes; keep real Git
   operations and do not globally bypass checks. Retain credential and ignored
   tracked-file preservation assertions and every repair-specific expectation.
10. `docs/WORKFLOW.md` — update the implementation process-stop sentence and
    its phase-4 description to name counted aborts, copied cumulative work,
    restored inputs, output/plan transitions and the safety exceptions; cite
    ADR 0024. Leave the draft and repair rules explicitly distinct.
11. `docs/adr/0024-implementation-attempts-continue-from-protected-partial-work.md`
    — the sole new ADR is drafted with this package. It is runner-held:
    the orchestrator owns any subsequent correction as a bootstrap edit after
    an accepted implementation attempt; the work model must not edit it or
    any other held path. Publish the final package as a decision PR with the
    decision template and label; acceptance is the maintainer's merge.
12. `plans/changes/sonnet-continues-flash/plan.md` — remove `not yet written`
    as ledger tests land; runner appends actual time and route records.
    `plans/changes/sonnet-continues-flash/findings.md` — runner-owned audit
    and later review evidence. `plans/INDEX.md` — runner-regenerated registry.
    `plans/changes/sonnet-continues-flash/spec.md` — drafted yardstick, unchanged
    by implementation. No repository file is deleted.

## Verification

Demonstrate new behavioral tests red against baseline code, then green; test
copy failure, evidence-write failure and an unsafe destination as well as the
happy route. Assert different directories and independent writable bytes,
not just different model process ids. Assert cumulative content in the final
checkpoint, branch commit count, retained recovery bytes and exact route
sequence. Synthetic credentials must never enter prompts or saved diffs.
The orchestrator ensures the worktree's venv and pinned Pi setup exist once
before full verification; the implementation owns equivalent candidate setup.

```sh
.venv/bin/python3 -m ruff check scripts/stage2.py tests/test_stage2.py tests/test_stage2_continuation.py
.venv/bin/python3 -m ruff format --check scripts/stage2.py tests/test_stage2.py tests/test_stage2_continuation.py
.venv/bin/python3 -m pytest -q -n auto tests/test_stage2_continuation.py tests/test_stage2.py tests/test_stage2_fail_fast.py
.venv/bin/python3 scripts/check_interview_minimums.py --change sonnet-continues-flash
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/check_research_handoff.py
make verify
```

`scripts/validate_change_artefacts.py` is absent at this baseline; its named
`--check` cannot be claimed green. The draft runner owns derived generation,
tracker-backed registry checks, `make verify` and the commit. This drafting
call runs only the available artifact checks and makes no git mutation.

Draft validation on 2026-11-02: the interview-minimums and criterion-ledger
checks passed; research-handoff passed with this non-swarm change exempt.
Full verification and the registry refresh remain with the runner.

## Criterion ledger

- 1: not yet written tests/test_stage2_continuation.py::test_implement_aborts_consume_exactly_the_scheduled_slots — an abort stops early, skips a position or starts an extra call
- 2: not yet written tests/test_stage2_continuation.py::test_continuation_copies_cumulative_partial_work_to_a_fresh_environment — additions/deletions disappear or writable files/working directories are reused
- 3: not yet written tests/test_stage2_continuation.py::test_continuation_prompt_carries_the_cumulative_diff — an earlier change or binary/large-file reference disappears from the handoff
- 4: not yet written tests/test_stage2_continuation.py::test_abort_handoff_warns_of_incomplete_files — an aborted half-written file is handed off without the warning
- 5: not yet written tests/test_stage2_continuation.py::test_each_implementation_attempt_restores_trusted_inputs — forged inputs or erased runner records reach the next call
- 6: not yet written tests/test_stage2_continuation.py::test_abort_is_saved_before_continuation_or_cleanup — save failure proceeds or cleanup deletes the only recoverable partial state
- 7: not yet written tests/test_stage2_continuation.py::test_abort_transitions_survive_in_output_and_plan — a transition is missing, mislabeled or recorded only in findings
- 8: not yet written tests/test_stage2_continuation.py::test_exhausted_implementation_keeps_recoverable_work_without_a_checkpoint — the runner reports success, commits failure or loses the last state
- 9: not yet written tests/test_stage2_continuation.py::test_accepted_continuation_commits_cumulative_verified_work_once — verification is skipped, accepted work disappears or more than one branch checkpoint appears
- 10: not yet written tests/test_stage2_continuation.py::test_implementation_safety_refusals_never_continue — secret-bearing evidence escapes or a guard failure reaches a later call/promotion
- 11: tests/test_stage2.py::test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason — the explicit Stage-1 route gains attempts or loses its reason
- 12: not yet written tests/test_stage2_continuation.py::test_continuation_policy_does_not_change_other_verbs — repair gains call-error fallback or draft loses its existing one
- 13: not a test — phase-6 review compares docs/WORKFLOW.md and ADR 0024 to spec criteria 1–12; stale unconditional stop wording or a repair-policy amendment refutes it

## Not touched

No existing ADR edits, new endpoint declarations, tracker writes, prompts/,
templates/, AGENTS.md, provenance.yaml, decisions/gates.yaml, model-endpoints.yaml,
harness configuration or CI changes. No containers, operating-system sandbox,
repair/draft isolation rollout or closure of the broader isolation bead.
The copy boundary protects attempt state; it is not proof of restricted host
reads. Research and maintainer answers remain inputs. There is no design.md
for this class and no ADR answer is recorded.

## Time used
