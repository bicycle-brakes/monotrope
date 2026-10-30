---
title: "Plan — guard-test"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-0ho
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, repair, guard-test]
---

# Plan — guard-test

```text
For you:     Test-only repairs can prove a real planted fault without forcing changes into correct production code.
Done when:   Authorised guard repairs prove planted red and clean green, ordinary proof stays strict, every new guard test gets phase-6 fault evidence, and verification rejects a set planting switch.
Appetite:    3 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Guard proof for initial implementation or criterion ledgers, automatic fault judgment, model routing changes, historical test conversion.
Pre-mortem:  suppose it failed: most likely because the clean proof inherited the planting switch.
Starts unless you say stop.
```

## Scope and prerequisites

Implements criteria 1–12 of `spec.md` using `design.md`. Baseline: `9987eaca`,
read 2026-10-29. No phase-2a rows stand in `findings.md`; preserve its audit.
Feature classification and the five maintainer answers stand unchanged.
Phase 1 used Stage 2, route `flash`, endpoint `glm-coding-plan`, model
`glm-5.3-flash` on 2026-10-15; no Stage-1 fallback is recorded.
`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent;
this plan uses the phase-3 prompt's form and does not claim that validator green.

Before an implementation checkpoint, the coordinating session must carry
the protected wording updates below outside model attempts, the maintainer
must supply the already-decided gate definition, and the feature's formal
ADR answer must be recorded only from a stated maintainer answer. Do not
invent that answer or weaken checkpoint guards to include protected edits.
If those inputs are unavailable, report the dependency and stop at that boundary.

## Build sequence

1. Extend `fixed_status`, repair instructions and `check_repair_answer`
   with the guard form, reusing existing test-path/function checks. Keep
   duplicate/unknown-id and conflicting-fixed-line checks before proof.
   Require the row's explicit unquoted `taken — guard test — <reason>`
   with a nonempty reason; inspect only the named function's source for
   `STAGE2_PLANT_FAULT`, not another function in the file. Preserve ordinary
   and text-form authorisation; an authorised guard row answered as an
   ordinary test still owes ordinary baseline proof.
2. Factor the existing `fixed_test_proof` execution into a shared
   attempt-tree helper with a default clean mode and an explicit planted
   mode. Keep the public clean call compatible. Planted mode alone adds
   `STAGE2_PLANT_FAULT=1` after environment filtering and uses
   `_red_record_fault(..., passing=False)` plus exit 1; clean mode omits the
   switch and requires exit 0 and `passing=True`. Use independent reports
   and tokens, preserve tool checks and tree/ref snapshots, timeouts and
   scrubbing on both legs. Guard dispatch runs planted then clean on the
   attempt, never baseline `red_first`; ordinary dispatch stays unchanged.
3. Only after all evidence succeeds, return canonical guard statuses and
   `yes — guard test — <test>` marks through existing bookkeeping. Cover
   private, released and phase-6 rows; a failure anywhere returns no fixes
   or successful marks and preserves existing failed-attempt restoration.
4. Add a phase-6-only answer format allowing `Guard evidence: <test> —
   fault: <description> — catches without switch: <yes|no and reason>`.
   Separate these lines before checking the existing verdict grammar;
   require findings or `No finding.`, preserve evidence verbatim in its
   verdict block, reject evidence alone or unrelated malformed answers.
   Keep loop/2a formats and verdict-before-loop-release ordering. The review
   prompt requires every added/changed guard test to be found from source
   and diff, one semantic line each, and a BLOCKER for a bare conditional
   failure. No private loop rows enter that inspection.
5. Add the presence gate and its seeded-red test; have the maintainer add
   a `guard-test-environment` entry with command
   `python3 scripts/check_guard_test_environment.py`, job `verify`,
   enforcement `block`, floor `false`, placement `both`, and a reason
   explaining repeatable guard proofs must not count as green verification.
   The coordinating session regenerates CI with the command below and
   applies the doctrine/status updates, retaining planting branches.
6. Exercise new tests against their named planted faults, measure red then
   restored green, run verification and record commit-bound results. Remove
   `not yet written` ledger prefixes only when the functions exist. Phase 6
   must inspect each new guard test's real fault; stand-in reviewer tests
   prove transport/instructions, not the quality of a live review.

## Files and ownership

- `scripts/stage2.py` — guard parsing/dispatch, shared proof execution,
  guard marks, `RECORD_INTRO` and phase-6 answer handling.
- `tests/test_stage2.py` — the new tests named in the ledger, using
  `repair_world`, `repair_step`, `script_repair` and real probe executions;
  retain existing test names and extend existing status-vocabulary checks.
- `scripts/check_guard_test_environment.py` — new small presence check,
  reporting the variable's name only, never the environment or its value.
- `tests/test_ci.py` — subprocess gate cases (absent, `1`, empty, `0`),
  a recognised `*_goes_red_when_*` seeded control and blocking local/CI wiring.
- `docs/WORKFLOW.md` — coordinating session adds the authorised guard
  exception, two-run contract, mandatory semantic review, statuses and mark;
  keeps ordinary red-first and repair-only scope explicit.
- `prompts/04-implement.md` — coordinating session aligns the repair paragraph
  with the authorised exception; initial implementation evidence is unchanged.
- `prompts/04b-review-loop.md` — coordinating session adds guard triage/status
  and mark wording, including the reason and both proof legs.
- `prompts/06-review.md` — coordinating session adds mandatory per-test fault
  evidence and the BLOCKER rule, consistently with the runner's format.
- `templates/findings.md` — coordinating session adds guard taken/fixed forms
  and the distinct proof mark without new columns.
- `decisions/gates.yaml` — maintainer adds the presence gate described above;
  this path remains forbidden to the implementation model.
- `.github/workflows/ci.yml` — coordinating session regenerates from gates;
  never hand-edit the generated workflow.
- `docs/adr/0023-guard-proof-for-test-only-repairs.md` — proposed guard-only
  addendum to ADR 0017, carried in the decision PR without rewriting ADR 0017.
- `plans/changes/guard-test/spec.md`, `plans/changes/guard-test/design.md`,
  `plans/changes/guard-test/plan.md` — update implementation status; the plan
  also carries actual time and ledger progress without changing criteria.
- `plans/changes/guard-test/findings.md` — runner-owned audit and review
  evidence; preserve existing lines and never prewrite a reviewer verdict.
- `plans/changes/guard-test/research.md` — append dated, source-backed gap
  checks when implementation discovers facts the current research lacks.
- `plans/INDEX.md` — runner-owned regeneration for the new artifacts.

No deletions. Do not touch other change folders, accepted ADR bodies,
`scripts/check_criterion_ledger.py`, `AGENTS.md`, `provenance.yaml`, model
endpoints, tool provisioning, retries, probe schema or tracker state.
`decisions.md` changes only for an actual new maintainer answer, none needed
for the settled guard behaviour. The formal ADR answer file is not an
implementation output; only the authorised answer-recording step may create it.

## Verification

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q -k 'guard or red_first or fixed_code or repair_marks_no_proof or passing_repair'
.venv/bin/python3 -m pytest tests/test_ci.py -q
.venv/bin/python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml
.venv/bin/python3 scripts/ci_gates.py --check-ci
.venv/bin/python3 scripts/check_interview_minimums.py --change guard-test
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

CI generation is a coordinated protected-file step, not a model-attempt
command. Run normal verification with the switch absent; gate tests set it
only in isolated child environments. Full verification belongs to the runner.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_guard_answer_accepts_the_named_test_form — the canonical guard answer is rejected
- 2: not yet written tests/test_stage2.py::test_guard_answer_requires_explicit_row_authorisation — an unmarked, text, quoted or reasonless row runs guard proof
- 3: not yet written tests/test_stage2.py::test_guard_proof_uses_attempt_code_and_planted_switch — correct baseline code is used or the planted run is green
- 4: not yet written tests/test_stage2.py::test_guard_proof_requires_clean_green_without_the_switch — a dirty clean leg receives a proof mark
- 5: not yet written tests/test_stage2.py::test_guard_proof_preserves_outcome_and_execution_guards — invalid evidence, setup/crash/skip, tool/tree/ref mutation or timeout passes either leg
- 5: not yet written tests/test_stage2.py::test_guard_proof_scrubs_failure_diagnostics — a proof refusal exposes the test secret
- 6: not yet written tests/test_stage2.py::test_guard_switch_must_appear_in_the_named_test — another function's switch reference is accepted
- 7: not yet written tests/test_stage2.py::test_guard_repairs_write_statuses_and_marks_only_after_complete_proof — a failed leg writes a mark or a successful repair loses its guard form in any row location
- 8: tests/test_stage2.py::test_a_named_test_that_is_not_red_first_fails_the_attempt — an ordinary green-baseline test passes
- 8: tests/test_stage2.py::test_a_text_row_taken_as_not_a_test_is_repaired_and_its_status_written — an authorised text repair is refused
- 8: not yet written tests/test_stage2.py::test_guard_form_keeps_other_repair_forms_and_environments_strict — ordinary/text authorisation changes or a caller switch reaches an ordinary proof
- 9: not yet written tests/test_stage2.py::test_phase6_guard_evidence_survives_findings_and_no_finding_verdicts — evidence is lost/refused, evidence alone becomes a verdict, or unrelated malformed prose passes
- 9: not yet written tests/test_stage2.py::test_phase6_guard_instructions_cover_every_changed_test_without_loop_rows — the prompt allows sampling or exposes loop rows before verdict
- 10: not yet written tests/test_stage2.py::test_phase6_guard_instructions_require_a_real_fault_and_block_empty_guards — the prompt omits mandatory semantic evidence or the conditional-failure BLOCKER
- 10: not a test — phase 6 reads every added/changed guard test and records its real fault; accepting a conditional failure without a real fault refutes this criterion
- 11: not yet written tests/test_ci.py::test_guard_environment_gate_goes_red_when_the_switch_is_present — any present value exits 0, an absent value fails, or either verification path omits the blocking gate
- 12: not yet written tests/test_stage2.py::test_guard_doctrine_keeps_repeatable_repair_only_proofs — planting branches are removed or operative status/proof instructions contradict the repair-only contract
- 12: not yet written tests/test_stage2.py::test_guard_repairs_preserve_the_planting_branch_for_replay — a successful repair removes its branch or its retained test cannot repeat the two-run proof
- 12: not yet written tests/test_stage2.py::test_guard_status_does_not_extend_the_criterion_ledger — a guard repair status parses as a ledger entry

## Time used
