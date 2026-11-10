---
title: "Plan — review-fewer-rounds"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-3rtn
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, review-loop]
---

# Plan — review-fewer-rounds

```text
For you:     Five focused lenses replace repeated unfocused rounds; small changes use five first-round calls, and shadow adds one free second round.
Done when:   All 24 criteria have evidence, the answered policy is wired through the runner and gates, and make verify passes.
Appetite:    12 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     A production trigger or threshold, the later calibration study, central configuration infrastructure or a dashboard.
Pre-mortem:  suppose it failed: most likely because duplicate reports were counted as different defects and distorted the calibration evidence.
Starts unless you say stop.
```

## Prerequisites and ownership

**Phase 4 is blocked**, independently of the card's veto: the central
configuration skeleton must merge first (central configuration work item
`coding-harness-twvx`, Q-4), and the maintainer must answer the spec's three
open decisions: initial questions, free second-round seating, and the
small-change live trigger. The orchestrator records the actual answers and
context in `decisions.md` and the bead; this draft records none.

At baseline `fe8a6329` on 2026-11-10 there is no central review-policy
contract. Proposed integration is `model-endpoints.yaml:review_loop`;
confirm the merged dependency's canonical path/reader/schema before phase 4
and reconcile this file list if different. No interim file or local schema
is implemented. Configuration holds both rounds independently, including
full/small seats and the final-review night exception. No phase-2a rows
exist in the supplied findings file; its runner diagnostics are preserved.

The accepted implement attempt owns ordinary code/tests/docs below. Held
paths belong exclusively to the orchestrator as bootstrap edits after the
accepted attempt: `model-endpoints.yaml`, `decisions/gates.yaml`,
`.github/workflows/ci.yml`, `AGENTS.md`, `prompts/04b-review-loop.md`,
`prompts/06-review.md` and the human-decided ADR prefix. The attempt uses
fixture configuration, never edits held paths or fabricates their approval.
The existing branch-local ADR draft is the one new ADR against main.

## Implementation steps and files

1. Create `scripts/stage2_review_policy.py` and
   `tests/test_stage2_review_policy.py`: adapt the dependency's single reader
   and validate five scenario lenses, initial approval/evidence, independently
   declared round rosters, full/small mode, endpoint/model/family/effort,
   round order/count, shadow/live trigger and ranges, and ordinary/night
   phase-6 budgets. Reject duplicate/unknown keys and missing intent answers
   before any call. Expose `--check` for CI. Initial full-change proposal:
   DeepSeek Flash, MiMo Flash and Terra/medium, as dated in the spec; small
   changes get one explicit other-family seat per lens. Do not infer round-2
   seats. Policy edits drive runtime without repeated constants.
2. Create `scripts/stage2_review_lenses.py` and
   `tests/test_stage2_review_lenses.py`: versioned run/seat persistence,
   round-1 prompt construction, free round-2 prompts, triage/capture mapping,
   diagnostics, round selection, disposition and phase-6 budget. Use the
   existing external loop-record lock and a versioned metadata block;
   preserve original six-cell rows and release evidence only after verdict.
   Snapshot policy, classification, implementation family and round revision.
   Persist successful answers as they arrive; resume only missing seats on
   that revision. Never share answers between independent reviewers.
3. Change `scripts/stage2.py` and `scripts/stage2_availability.py` to dispatch
   new-policy runs through those components using existing commands, reported
   policy-bound receipts, per-call admission/leak checks, isolated credentials,
   repository-pinned Pi and the official read-only Codex CLI. Extend
   `tests/test_stage2.py` and `tests/test_stage2_availability.py` at the actual
   command boundaries. Full round 1 has fifteen calls; bounded or text-only
   has five. At most one implementer-family reviewer per lens, never a sole
   self-family reviewer. Missing required seats wait with evidence retained;
   quota, malformed output or cut input never becomes a clean result.
4. In the new lens component, merge reports by union; explicit triage groups
   a defect only by the same faulty mechanism, trigger and intended invariant.
   Keep every source row, including incidental outside-lens BLOCKERs; count
   one capture per reporting seat in its own lens. For three seats compute
   S=f1+f2+f3, share=f1/S, jackknife total=S+2*f1/3 and Chao total=S+f1*f1/(2*f2).
   Undefined denominators carry reasons; one-seat small changes have no
   three-seat estimator. Shadow always runs one whole-diff free second round
   on the repaired revision, never five focused re-reviews. Future approved
   live mode ORs per-lens signals into that one round, using the recorded
   comparison winner/threshold and the separately answered small-change rule.
   Round-2 required repairs form one final batch, without a third loop round;
   outside-change follow-ups go to the orchestrator. Clear style rides along
   only when repair is already required; taste remains a named PR limit.
5. Reserve substantive phase-6 calls persistently before launch in the lens
   component and enforce them at `scripts/stage2.py`'s review entry point.
   Default policy: initial review plus one re-check; stop with unresolved rows
   and a named-limit/mechanism-repair/stop proposal. Only a recorded night run
   with all open findings in one repaired mechanism may spend one extra
   re-check; reserve that exception once, with repair commit and row evidence.
   No fourth call; failed/unknown launches do not silently refund a slot.
   Release/restart must preserve counts; marking an existing verdict is not
   another review. Repeat-mechanism findings require a mechanism repair.
6. Create `scripts/check_review_formalities.py` and
   `tests/test_check_review_formalities.py`; change `scripts/ci_gates.py` and
   `tests/test_ci.py` for matching local/hosted callers. Select eligible
   committed/staged/unstaged/untracked changed paths against the established
   merge base, skip deletions, and use safe path arguments for Markdownlint.
   Reuse `stage2.card_problem` and the runner's time-entry grammar. Check
   header/status, card placement/appetite and time structure mechanically;
   do not claim semantic card-scope equivalence. New checks block changed
   paths; unchanged stock reports only; existing blocking gates stay intact.
   Missing linter/base/tool is not a passing check. Expose one gate CLI.
7. Add local `export` and `summarize` subcommands to
   `scripts/stage2_review_lenses.py` and create
   `docs/research/review-fewer-rounds-calibration.md` for schema and usage.
   The first real export creates
   `docs/research/review-fewer-rounds-calibration.jsonl`; no invented samples.
   Use repository-confined explicit inputs/outputs, atomic replacement by run
   ID and no duplicate samples. Store raw provenance, small/full mode, round-1
   captures (including zeros), round-2 new accepted defects and primary lens,
   unique seat yield, failed calls, tokens or unavailable reason, elapsed call
   time, verify execution and lock wait separately. Free-round reviewers are
   not per-lens captures. At ten complete changes report would-stop misses,
   compare share and diagnostic candidates once and hand off clear/unclear
   evidence for the calibration decision; never auto-select a winner.
   Commands: `export --findings <repository-findings-path> --output
   docs/research/review-fewer-rounds-calibration.jsonl` and `summarize --input
   docs/research/review-fewer-rounds-calibration.jsonl`.
8. Orchestrator bootstrap: change `model-endpoints.yaml` at the dependency's
   canonical section with actual intent answers, approval reference and Terra
   loop admission. Change `decisions/gates.yaml` to register policy and
   changed-path formality/lint checks; regenerate `.github/workflows/ci.yml`
   and `plans/INDEX.md` with the commands below. Extend the spec's formality
   inventory if another gap appears. Create a follow-up bead for uncovered
   semantic card-scope comparison, recording title/ID in the inventory and PR;
   an accepted attempt never writes the tracker or these held files.
9. Change `docs/WORKFLOW.md` and `docs/how-it-works.md` for focused full/small
   round 1, free round 2, ten-change calibration and bounded phase 6.
   Orchestrator bootstrap changes `AGENTS.md`, `prompts/04b-review-loop.md`
   and `prompts/06-review.md` to the same policy, including immediate disclosed
   question additions only for uncovered phase-6 findings. Revise the one
   draft `docs/adr/0027-focused-review-with-a-shadow-period.md` consistently;
   it amends ADR 0021/0017 without modifying their historical bodies.
   `docs/WORKFLOW.md` also gives the orchestrator the weekly procedure:
   collect outstanding clear style rows into one clean-up bead and its own
   repair PR, with source row IDs and collection week to prevent duplicates.
   No new scheduling service or automated tracker writer is built.

No other implementation paths are planned. The runner owns status/evidence
updates in this change's `spec.md`, `design.md`, `plan.md` and `findings.md`;
the orchestrator records actual answers in `decisions.md`. Convert ledger
entries when tests are defined. No dependency/lockfile changes are planned.
All new code modules have production callers, and both gate CLIs have CI
callers and fault-sensitive tests.

## Criterion ledger

- 1: not yet written tests/test_stage2_review_policy.py::test_five_approved_scenario_lenses — missing lens or unapproved initial questions reach a model
- 2: not yet written tests/test_stage2_review_lenses.py::test_full_and_small_round_one_dispatch — wrong 15/5 count, shared answers or wrong Terra effort
- 3: not yet written tests/test_stage2_review_policy.py::test_implementer_family_per_lens_limit — sole self-review or two self-family members pass
- 4: not yet written tests/test_stage2_review_policy.py::test_policy_edits_drive_the_runner_without_code_defaults — configuration edits do not change actual scheduling
- 5: not yet written tests/test_stage2_review_policy.py::test_invalid_policy_refuses_before_calls — malformed, duplicate or unknown fields reach a model
- 6: not yet written tests/test_stage2_review_lenses.py::test_resume_pins_policy_revision_and_completed_seats — drift or release replays completed seats
- 7: not yet written tests/test_stage2_review_lenses.py::test_union_and_explicit_capture_groups_preserve_provenance — singletons disappear or unrelated defects merge
- 8: not yet written tests/test_stage2_review_lenses.py::test_overlap_diagnostics_by_seat_count — wrong capture matrix or fabricated one-seat estimate
- 9: not yet written tests/test_stage2_review_lenses.py::test_shadow_runs_one_free_second_round — zero findings skip it or lens prompts constrain it
- 10: not yet written tests/test_stage2_review_lenses.py::test_ten_change_comparison_preserves_misses_and_needs_decision — duplicates/zeros distort sample or report promotes itself
- 11: not yet written tests/test_stage2_review_lenses.py::test_live_trigger_ors_into_one_free_round — multiple rounds, selected lenses, wrong comparison or an invented small-change rule
- 12: not yet written tests/test_stage2_review_lenses.py::test_round_two_leads_to_one_final_repair_and_no_third_round — location-based deferral or third full round
- 13: not yet written tests/test_stage2_review_lenses.py::test_minor_and_style_dispositions_do_not_drive_rounds — style-only repair or unrepaired required MINOR
- 14: not yet written tests/test_check_review_formalities.py::test_changed_files_block_and_unchanged_stock_reports — invalid changed metadata/card/time/lint passes or old stock blocks
- 14: not yet written tests/test_ci.py::test_review_formalities_have_matching_local_and_hosted_callers — new gate absent or scoped differently in CI
- 15: not yet written tests/test_stage2_review_lenses.py::test_review_budget_with_one_mechanism_night_exception — ordinary third, unjustified night third or any fourth launch
- 15: not yet written tests/test_stage2_review_lenses.py::test_final_review_budget_survives_release_failure_and_restart — failed/lost/released state refunds a reservation
- 16: not yet written tests/test_stage2_review_lenses.py::test_repeated_mechanism_requires_mechanism_repair — another case-only repair is admitted
- 17: not yet written tests/test_stage2_review_lenses.py::test_incomplete_or_cut_seats_cannot_complete — failure becomes zero/clean evidence
- 18: not yet written tests/test_stage2_review_lenses.py::test_observations_include_unique_yield_failures_tokens_and_lock_wait — invented tokens, omitted failure or conflated time
- 19: not yet written tests/test_stage2.py::test_focused_calls_preserve_security_and_verdict_release_order — launch bypasses admission/isolation or release precedes verdict
- 20: not a test — phase-6 review compares the named current doctrine and ADR diff with the spec/configuration; stale lens-round-2 or until-clean guidance refutes it
- 21: not a test — weekly orchestrator review links outstanding clear style source rows to that week's clean-up bead and own PR; discarded rows or a source-change style round refute it
- 22: not a test — phase-6 review checks every inventory row against its actual gate and uncovered follow-up bead; unsupported gate claims or a missing follow-up refute it
- 23: not yet written tests/test_stage2_review_policy.py::test_question_additions_require_uncovered_phase_six_evidence — unapproved first list or unexplained later addition is used
- 23: not a test — phase-6 review checks that every immediate addition and its source finding are disclosed in the PR; an omitted addition refutes it
- 24: not a test — orchestrator checks the central-skeleton merge commit before phase 4 and the PR file list for interim settings; pre-merge implementation or an interim policy refutes it

## Verification

Use actual scheduling/admission/check entry points with captured launches and
offline synthetic credentials/providers. Test boundary shares, S=0/f2=0,
one-seat data, duplicate YAML keys, input drift, truncated output, interrupted
budget reservations and the positive/negative night exception. Include valid
read/check controls. No paid live probes are required for this change.

After prerequisites and orchestrator bootstrap, from this worktree root:

```sh
make venv
bash tools/pi/install.sh
.venv/bin/python3 -m pytest tests/test_stage2_review_policy.py tests/test_stage2_review_lenses.py tests/test_check_review_formalities.py tests/test_stage2.py tests/test_stage2_availability.py tests/test_ci.py -q
.venv/bin/python3 scripts/stage2_review_policy.py --check
.venv/bin/python3 scripts/check_review_formalities.py
.venv/bin/python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml
.venv/bin/python3 scripts/plans_registry.py --index
.venv/bin/python3 scripts/check_interview_minimums.py --change review-fewer-rounds
.venv/bin/python3 scripts/check_question_context.py
.venv/bin/python3 scripts/check_research_handoff.py --change review-fewer-rounds
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/plans_registry.py --check
make verify
git diff --check
```

`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at
`fe8a6329`, read 2026-11-10. Keep the prompt's card/ledger/time form and use
the present registry/interview/ledger checks; do not add the missing files.
The runner owns derived-file updates, full verification and the one commit.

## Draft validation — 2026-11-10

Measured on this draft over baseline `fe8a6329`: interview minimums,
question-context and criterion-ledger commands above exit 0. The scoped
research-handoff command exits 0 with the explicit legacy/no-v2 exemption;
it does not certify a swarm. `git diff --check` passes.

The complete registry gate is not run here: no tracker render confined to
this worktree was supplied, and this attempt may not read outside the tree.
The runner must measure registry coupling and `make verify` with its actual
tracker context. The absent change-artefact validator cannot be measured.
Open decisions remain open regardless of these structural check results.

## Boundaries and route

Do not touch existing ADR bodies, decision/adoption answers, leak rules,
data permissions, provider transports, user configuration, research-swarm
policy, implement/repair routing or historical capture data. Stop at the
12-hour appetite and report remaining criteria.

Carry-forward Explore fallback: 2026-11-09 attempt 1 used Stage 1, endpoint
`claude-code-plan`, model `claude-haiku-5-5`; reason: the research swarm's
last two runs returned report-format failures (research.md; research-report
repair work item `coding-harness-1ga5`). The file also holds Opus 5.5
public-source research dated 2026-11-09. No complete `research-swarm/v2`
run is recorded; `neighbours: []` does not assert no adjacent specs exist.

## Time used
