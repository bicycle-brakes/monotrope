---
title: "Plan — review-fewer-rounds"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-24
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
For you:     Focused reviews use two models per lens and fewer follow-up rounds.
Done when:   Each spec criterion has fault-sensitive evidence and make verify passes.
Appetite:    12 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     A live threshold, the later calibration study, central configuration infrastructure or a dashboard.
Pre-mortem:  suppose it failed: most likely because defect groups distort the calibration evidence.
Starts unless you say stop.
```

**Prerequisite:** The maintainer's answer Q-31 changes the spec after the
third spec-review round. Before phase 4, obtain a recorded authorization for
a fourth spec-review round or re-slice the change; do not invent that answer.
The orchestrator must reconcile the existing branch-local ADR 0027 with the
spec before the decision PR is complete. The central configuration skeleton is
not a prerequisite (Q-16). Reuse the per-model accepted-share measure of the
findings-per-model change (`coding-harness-qut1`); if absent at phase 4, first
reconcile that dependency with the orchestrator rather than add a second
authoritative calculation.

The maintainer confirmed the review readings in Q-32–Q-36; Q-31 replaces the
provisional S2-12 with one additional re-check per newly chosen mechanism
repair and a single night exception. Their detailed behavior is in the spec.

## Implementation and ownership

The accepted implement attempt owns ordinary code, tests and unheld docs;
the orchestrator alone edits all held paths listed in the phase-3 prompt,
including `model-endpoints.yaml`, `decisions/gates.yaml`, `.github/`,
`AGENTS.md`, `prompts/` and the human-decided `docs/adr/` prefix. The attempt
uses fixtures for those files and never edits them. Existing runner commands
remain the only action entry points; legacy snapshots retain frozen settings under the two-round house rule.

1. Create `scripts/stage2_review_policy.py` and
   `tests/test_stage2_review_policy.py`: validate one central declaration,
   model-family mapping including implementers, exact initial Q-13 questions and
   sourced additions, per-lens and free-round substitutes, seat date and citation, live references,
   configurable lenses/seats/rounds/cap/early-end/limits, independent round-2
   roster, shadow/live mode and resolvable calibration approval. Verify an
   edited setting changes actual scheduling. Unknown keys, duplicates,
   missing evidence and invalid family or endpoint references refuse.
2. Create `scripts/stage2_review_lenses.py` and
   `tests/test_stage2_review_lenses.py`: persist frozen policy, revision,
   availability receipts (including a fresh one at free-round start), seeded draws,
   independent seat results,
   complete chunk coverage, per-physical-call self-checks, failures and declared
   substitutions; retain non-admitted rows outside union triage with source row IDs and the spec's semantic grouping contract.
   Compute the per-seat-count diagnostics in the spec, including two-seat
   `S=f1+f2`, jackknife `S+f1/2` and Chao where defined; never apply a
   three-seat estimate to two seats. Preserve zero and unknown explicitly. Measure accepted share by
   model and lens, challenger comparisons since the fixed-seat date using deduplicated
   released findings, accepted/triaged rows and sample counts,
   token/time availability and verify
   execution and lock wait separately. Persist phase-6 launch reservations,
   night evidence, mechanism links and maintainer authorizations.
3. Change `scripts/stage2.py`, `scripts/stage2_availability.py`,
   `tests/test_stage2.py` and `tests/test_stage2_availability.py`: use the
   existing preparation/launch/resume and security paths. Initially every
   full or bounded lens has fixed DeepSeek Flash plus a seeded random eligible
   reachable challenger; expired terms are reported and seat 1 falls back to an
   eligible per-lens substitute; text-only skips the loop. At most one implementer
   family sits on a lens; substitutes are distinct and eligible. Resume
   successful seats without replay and complete oversized input by checked
   chunks; retry once, then substitute in order or redraw an eligible
   challenger from the substitute list. Persist a waiting state and report a
   five-hour stop. Shadow runs the free round unless the accepted first-round
   rows are nonempty, all MINOR and all required repairs are complete;
   bounded changes skip it. Initial free seats are three seeded, independently
   drawn distinct families excluding the OpenAI family and Codex endpoint.
   One-seat observations have no share or positive trigger; a family-ineligible
   sole fixed seat uses an eligible different-family substitute or waits. Collect one final
   repair, then fresh phase 6 with the configured budget and exceptions; a night exception can add one re-check
   beyond a zero ordinary budget; each new explicit maintainer choice permits
   exactly one re-check of that repair, without replaying any authorization.
4. Create `scripts/check_review_formalities.py` and
   `tests/test_check_review_formalities.py`; change `scripts/ci_gates.py`
   and `tests/test_ci.py`: gate new formalities and Markdownlint on lines
   written against `git merge-base HEAD origin/main` after fetch locally and
   the merge base of HEAD and the PR base commit in CI, keeping existing
   blocking gates. Reuse existing card and time checks. Missing tools/base
   fail; semantic card-scope equivalence gets a follow-up, not a false claim
   of automated proof. Resolve the review-formalities coverage in the spec.
5. Create `docs/research/review-fewer-rounds-calibration.md` for the export
   contract and use `scripts/stage2_review_lenses.py` for idempotent export
   to `docs/research/review-fewer-rounds-calibration.jsonl` (created by the
   first actual export, no invented samples) and summary. Record round-2
   provenance as pre-existing, repair-introduced or unknown; compare the
   singleton candidate with estimator sensitivity analyses and identify
   would-stop MAJOR/BLOCKER misses. Count only eligible complete full changes;
   report bounded, zero and incomplete cases separately. The maintainer owns
   any later live decision.
6. Orchestrator bootstrap: edit `model-endpoints.yaml` to hold the policy and
   exact Q-13 questions with source references; edit `decisions/gates.yaml`
   to register the new checks; regenerate `.github/workflows/ci.yml` and
   `plans/INDEX.md` with the repository generators. Amend `AGENTS.md`,
   `prompts/04b-review-loop.md`, `prompts/06-review.md`, and the existing
   `docs/adr/0027-focused-review-with-a-shadow-period.md` to match the
   spec and actual settings. Create the uncovered semantic-card follow-up
   bead under the repository's single-writer rule and name it in the PR.
7. Change `docs/WORKFLOW.md` and `docs/how-it-works.md` to describe the
   new policy and weekly ISO-week collection of clear style and maintainability
   rows, with source IDs and one clean-up bead/PR. The orchestrator performs
   tracker writes; reviewers and foreign repairs do not. Update this change's
   `spec.md`, `design.md`, `plan.md`, `findings.md` and `decisions.md` only
   as their respective workflow steps require. Implement the closed-week
   deferred-row report in `scripts/stage2_review_lenses.py`; the orchestrator
   uses its IDs for tracker updates, never the reviewer or repair model.

## Criterion ledger

- 1: not yet written tests/test_stage2_review_policy.py::test_initial_and_added_questions_have_sources — an unapproved initial list or unsourced addition is admitted
- 2: not yet written tests/test_stage2_review_lenses.py::test_two_seeded_independent_seats_for_full_and_bounded — wrong roster, unrecorded draw or shared answers passes
- 3: not yet written tests/test_stage2_review_policy.py::test_family_limit_and_unknown_family — two self-family seats or unknown family passes
- 4: not yet written tests/test_stage2_review_policy.py::test_changed_configuration_drives_scheduling — changing a policy value does not affect runtime
- 5: not yet written tests/test_stage2_review_policy.py::test_invalid_policy_blocks_before_calls — bad keys, references or live approval reach a call
- 6: not yet written tests/test_stage2_review_lenses.py::test_resume_pins_snapshot_and_completed_seats — policy drift or restart replays a successful seat
- 7: not yet written tests/test_stage2_review_lenses.py::test_union_triage_preserves_rows_and_group_ids — a raw, non-admitted or triaged row or its provenance disappears
- 8: not yet written tests/test_stage2_review_lenses.py::test_two_seat_overlap_diagnostics — incorrect f1/f2 or undefined ratio is reported as valid
- 9: not yet written tests/test_stage2_review_lenses.py::test_shadow_round_and_repaired_minor_early_end — signal alone skips a required round or repaired minors run one
- 10: not yet written tests/test_stage2_review_lenses.py::test_calibration_counts_only_complete_full_changes — duplicate, early-ended or bounded change enters the ten
- 11: not yet written tests/test_stage2_review_lenses.py::test_live_trigger_and_undefined_share — undefined share triggers or a bounded change gets a second round
- 12: not yet written tests/test_stage2_review_lenses.py::test_round_two_one_final_repair — a required repair is deferred or another loop round runs
- 13: not yet written tests/test_stage2_review_lenses.py::test_minor_dispositions — a logic defect is left or maintainability alone causes repair
- 14: not yet written tests/test_check_review_formalities.py::test_markdown_errors_only_on_written_lines_block — legacy line blocks or changed line passes
- 14: not yet written tests/test_ci.py::test_formality_gate_uses_same_merge_base_locally_and_in_ci — hosted and local callers differ
- 15: not yet written tests/test_stage2_review_lenses.py::test_review_budget_night_and_maintainer_authorization — an unauthorized call or replay is permitted, a second night exception runs, or a newly chosen repair is denied its check
- 16: not yet written tests/test_stage2_review_lenses.py::test_linked_phase_six_findings_require_mechanism_instruction — linked rows yield a case-only repair prompt
- 17: not yet written tests/test_stage2_review_lenses.py::test_substitution_and_complete_chunk_coverage — a failed seat is counted clean or an ineligible replacement runs
- 18: not yet written tests/test_stage2_review_lenses.py::test_model_lens_shares_and_measurement_provenance — failed calls or challenger comparison disappear
- 19: not yet written tests/test_stage2.py::test_focused_calls_keep_admission_and_leak_checks — a launch bypasses an existing boundary
- 20: not a test — phase-6 review compares the named doctrine and ADR with the spec and configuration; stale guidance refutes it
- 21: not yet written tests/test_stage2_review_lenses.py::test_weekly_cleanup_report_identifies_uncollected_rows — omitted outstanding or included fixed rows refute it
- 22: not a test — phase-6 review compares Q-1 formalities with the inventory, gate contracts and follow-up bead; a missing check or follow-up refutes it
- 23: not yet written tests/test_stage2_review_policy.py::test_addition_source_and_frozen_runs — unsourced additions or changes to a frozen run pass
- 24: not yet written tests/test_stage2_review_policy.py::test_interim_policy_single_source — a second authoritative policy or mandatory skeleton is accepted
- 25: not yet written tests/test_stage2_review_lenses.py::test_free_round_initial_mixed_family_roster — wrong roster or shared outputs passes
- 26: not yet written tests/test_stage2_review_lenses.py::test_bounded_change_skips_free_round — a bounded change receives a second loop round
- 27: not yet written tests/test_stage2_review_lenses.py::test_findings_require_file_and_line — a locationless row enters triage or disappears from the report
- 28: not yet written tests/test_stage2_review_lenses.py::test_cap_exempts_major_and_blocker — an excess MINOR passes or an excess MAJOR is dropped
- 29: not yet written tests/test_stage2_review_lenses.py::test_prompt_requires_self_check — a physical call omits the evidence self-check
- 30: not yet written tests/test_stage2_review_lenses.py::test_text_only_skips_loop — a text-only change calls a loop reviewer

## Verification

Run offline fault cases at real scheduling and gate boundaries, including
substitution, unavailable pools, chunk coverage, recorded seeds, zero overlap,
failed budget reservations, repair-origin uncertainty and both review
exceptions. After the orchestrator bootstrap, from the worktree root:

```sh
.venv/bin/python3 -m pytest tests/test_stage2_review_policy.py tests/test_stage2_review_lenses.py tests/test_check_review_formalities.py tests/test_stage2.py tests/test_stage2_availability.py tests/test_ci.py -q
.venv/bin/python3 scripts/stage2_review_policy.py --check
.venv/bin/python3 scripts/check_review_formalities.py
.venv/bin/python3 scripts/check_interview_minimums.py --change review-fewer-rounds
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/plans_registry.py --check
make verify
```

The runner owns full verification and the one commit. No paid live model call
is required as an implementation test. The current checkout has no
`templates/plan.md` or `scripts/validate_change_artefacts.py` (checked
2026-11-23); use the prompt's card/ledger/time form and existing gates.

## Boundaries and route

Do not edit existing ADR bodies other than the branch-local draft, admission
rules, credentials, provider transports, research-swarm routing, user
configuration or historical run records. Twelve hours is a stop.

Explore fallback: 2026-11-09 attempt 1 used Stage 1, endpoint
`claude-code-plan`, model `claude-haiku-5-5`, because the research swarm's
last two runs had report-format failures (research.md; follow-up
`coding-harness-1ga5`). No complete `research-swarm/v2` run is recorded.

## Time used

2026-11-23 15:45:43–15:48:34 UTC, 171 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-23 16:03:56–16:10:02 UTC, 365 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-23 16:17:24–16:21:50 UTC, 266 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-23 16:29:48–16:33:17 UTC, 210 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-24 13:38:31–13:41:22 UTC, 171 s — draft · attempt 1 · route codex · model gpt-6.1-terra · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
