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
For you:     Five focused reviewer trios replace repeated unfocused rounds; shadow mode reviews every lens twice before a bounded final review.
Done when:   All 20 criteria have evidence, the approved questions and central policy are wired through the runner and gates, and make verify passes.
Appetite:    12 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     A production threshold, the later calibration study, central configuration infrastructure or a dashboard.
Pre-mortem:  suppose it failed: most likely because duplicate reports were counted as different defects and distorted the calibration evidence.
Starts unless you say stop.
```

## Prerequisites and ownership

Phase 4 waits for the maintainer's question-list approval in the spec and
the central configuration work (`coding-harness-twvx`). Baseline `d23f416c`
has neither that central policy nor its contract in this tree. The proposed
integration is `model-endpoints.yaml:review_loop`; if the dependency chooses
another canonical path, reconcile this file list and adapter contract before
implementing. Do not create a parallel policy file or answer the open decision.
No phase-2a finding rows exist in the supplied `findings.md` on 2026-11-10.

The accepted implement attempt owns ordinary code/tests/docs only. Every held
path below belongs to the orchestrator as a bootstrap edit after the accepted
attempt; the attempt uses fixture policy inputs and never edits a held path.
The orchestrator records the actual question-list answer in this change's
`decisions.md`; it never creates an ADR answer from its own interpretation.

## Implementation steps

1. Create `scripts/stage2_review_policy.py` and `tests/test_stage2_review_policy.py`
   to adapt the dependency's single reader, reject invalid/duplicate/unknown
   fields and validate lens questions/approval, seat references/families, rounds,
   trigger/mode/threshold and phase-6 limit. Expose `--check` for CI. Proposed
   initial values: five spec lenses; each seated with DeepSeek Flash, MiMo Flash
   and Terra/medium as named in the spec; ordered rounds 1 and 2; shadow mode;
   provisional share comparison `> 0.5`; no live approval; two phase-6 reviews.
2. Create `scripts/stage2_review_lenses.py` and `tests/test_stage2_review_lenses.py`
   for versioned run/seat persistence, prompt construction, triage maps,
   overlap diagnostics, shadow/live selection, round-2 disposition, mechanism
   recurrence and phase-6 budget. Store raw answers plus sidecar metadata under
   the existing loop-record lock and release it into findings; preserve old
   table widths and dispatch legacy snapshots unchanged. Group only accepted
   identical defects by mechanism+trigger+invariant, retain all source rows,
   count each seat once per defect within its own lens, and never majority-vote.
3. Change `scripts/stage2.py` to route prepared new-policy loops through that
   component, call existing admission/leak/credential/read-only launch paths,
   and use an isolated official Codex loop call with configured Terra/medium.
   Extend `scripts/stage2_availability.py` for policy-bound reported preparation
   and complete trios. Change `tests/test_stage2.py` and
   `tests/test_stage2_availability.py` for actual command paths, receipts, fresh
   full verification, legacy runs and verdict-before-release. Missing seats,
   malformed/cut answers or input drift stop completion; resume only missing
   seats on the same revision. No quota fallback changes the three-seat design.
4. In those components, compute S=f1+f2+f3, share=f1/S, jackknife total=S+2*f1/3
   and Chao total=S+f1*f1/(2*f2); undefined denominators get reasons. Shadow
   always selects all lenses, including S=0; a future live policy requires the
   maintainer-approved threshold/comparison and selects undefined evidence for
   re-review. Round 2 uses the post-repair revision and frozen trios; required
   findings enter one final repair, style only accompanies it, outside-change
   follow-ups go to the orchestrator. Reserve substantive phase-6 launches
   before calling, count failed/unknown launches conservatively, and preserve
   the two-launch budget through release/restart; marking calls do not count.
5. Create `scripts/check_review_formalities.py` and
   `tests/test_check_review_formalities.py` for new/changed paths (committed,
   staged, unstaged and untracked against the established merge base; deletions
   skipped). Check headers/status, card against decisions/appetite and time
   ledger structure; use existing card parsing and runner time format rather
   than parallel grammars. Invoke Markdownlint on changed Markdown using safe
   path arguments. Old stock stays report-only for these new checks; broader
   existing blocking checks still run. Change `scripts/ci_gates.py` and
   `tests/test_ci.py` to wire both new CLI callers and changed-only blocking
   behavior consistently for local and hosted runs, including missing-tool
   failures and base resolution. Retain stock lint reporting.
6. Add the explicit local calibration-report CLI to `scripts/stage2_review_lenses.py`:
   export complete, triaged run observations, including zeros, seat unique
   yield, failures, tokens/unavailable reasons, durations and verify lock wait,
   idempotently by run ID to `docs/research/review-fewer-rounds-calibration.jsonl`.
   Create `docs/research/review-fewer-rounds-calibration.md` describing schema,
   export/summary commands, source commits and the 10–20-change comparison of
   would-stop lenses with actual round-2 MAJOR/BLOCKER yield. The JSONL is
   created by the first real export, never populated with invented samples.
   Its interfaces are `export --findings <repository-findings-path> --output
   docs/research/review-fewer-rounds-calibration.jsonl` and `summarize --input
   docs/research/review-fewer-rounds-calibration.jsonl`; reject outside/aliased
   inputs and outputs. Import only the released versioned observations, never
   reinterpret historical free/Flash/ladder rows as captures.
7. Orchestrator bootstrap after the accepted attempt: change `model-endpoints.yaml`
   with the dependency's canonical review section, the actual question approval
   reference and Terra loop admission; change `decisions/gates.yaml` to register
   the policy/formalities checks and changed-only Markdown blocking. Regenerate
   `.github/workflows/ci.yml` and `plans/INDEX.md` using the commands below.
   The attempt must not edit these held paths, even to fix its post-run gate.
8. Change `docs/WORKFLOW.md` and `docs/how-it-works.md` to explain configured
   trios, shadow evidence, final repair and bounded phase 6. Orchestrator bootstrap:
   change `AGENTS.md` for the new loop and style rule; change
   `prompts/04b-review-loop.md` and `prompts/06-review.md` for focused review,
   triage and budget, referring to configuration rather than duplicating policy
   literals. Preserve the one draft `docs/adr/0026-focused-review-with-a-shadow-period.md`
   and reconcile its number only if occupied before merge. Review current
   doctrine against spec criterion 20; historical ADRs stay untouched.

No other implementation paths are planned. The runner owns normal status,
ledger and evidence updates in this change's `spec.md`, `design.md`, `plan.md`
and `findings.md`; test entries change from `not yet written` when defined.
No new dependency or lockfile is planned. New modules have production callers,
the two gate CLIs have CI callers, and all have tests rather than exemptions.

## Criterion ledger

- 1: not yet written tests/test_stage2_review_policy.py::test_five_approved_scenario_lenses — missing lens or unapproved questions are admitted
- 2: not yet written tests/test_stage2_review_lenses.py::test_round_one_dispatches_fifteen_independent_seats — wrong count, shared answers or wrong Terra effort
- 3: not yet written tests/test_stage2_review_policy.py::test_self_family_is_excluded_only_when_sole_reviewer — sole self-review passes or diverse trio fails
- 4: not yet written tests/test_stage2_review_policy.py::test_policy_edits_drive_the_runner_without_code_defaults — runtime ignores changed configuration
- 5: not yet written tests/test_stage2_review_policy.py::test_invalid_policy_refuses_before_calls — malformed policy reaches a model
- 6: not yet written tests/test_stage2_review_lenses.py::test_resume_pins_policy_revision_and_completed_seats — configuration drift, release or retry replays a seat
- 7: not yet written tests/test_stage2_review_lenses.py::test_union_and_explicit_capture_groups_preserve_provenance — singleton lost, rejected vote counted or unrelated defects merged
- 8: not yet written tests/test_stage2_review_lenses.py::test_overlap_diagnostics_and_undefined_denominators — incorrect known capture matrix or invented zero-denominator value
- 9: not yet written tests/test_stage2_review_lenses.py::test_shadow_reviews_every_lens_again — zero or low-share lens omitted
- 10: not yet written tests/test_stage2_review_lenses.py::test_calibration_summary_keeps_zero_lenses_and_never_promotes — incomplete/duplicate samples or hidden would-stop misses
- 11: not yet written tests/test_stage2_review_lenses.py::test_live_selection_uses_only_the_approved_singleton_rule — estimator selection, wrong equality or skipped undefined evidence
- 12: not yet written tests/test_stage2_review_lenses.py::test_round_two_leads_to_one_final_repair_and_no_third_round — location-based deferral or unwanted third round
- 13: not yet written tests/test_stage2_review_lenses.py::test_minor_and_style_dispositions_do_not_drive_rounds — style-only repair or omitted required security repair
- 14: not yet written tests/test_check_review_formalities.py::test_changed_files_block_and_unchanged_stock_reports — changed metadata/card/time/lint passes or unchanged stock blocks
- 14: not yet written tests/test_ci.py::test_review_formalities_have_matching_local_and_hosted_callers — new gate absent, nonblocking or scoped differently in CI
- 15: not yet written tests/test_stage2_review_lenses.py::test_final_review_budget_survives_release_failure_and_restart — third substantive launch or missing stop proposal
- 16: not yet written tests/test_stage2_review_lenses.py::test_repeated_mechanism_requires_mechanism_repair — second same-kind finding gets another case repair
- 17: not yet written tests/test_stage2_review_lenses.py::test_incomplete_or_cut_lens_cannot_complete — missing, malformed or timed-out seat becomes a zero result
- 18: not yet written tests/test_stage2_review_lenses.py::test_observations_include_unique_yield_failures_tokens_and_lock_wait — invented tokens, lost failure or conflated wait time
- 19: not yet written tests/test_stage2.py::test_focused_calls_preserve_security_and_verdict_release_order — a mixed-endpoint seat bypasses leak/admission/isolation or releases before verdict
- 20: not a test — phase-6 review reads the named doctrine/prompt/ADR diff against the configured policy and spec; stale until-clean guidance or invented approval refutes it

## Verification

Tests must exercise production entry points with captured launches, synthetic
credentials and offline provider fixtures. Plant wrong grouping, missing
seats, duplicate YAML keys, changed receipts, interrupted launch reservations,
stale releases, S=0/f2=0, boundary shares and nonzero lint results. Positive
controls must demonstrate that legitimate review/read/check paths work.

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
baseline `d23f416c` (read 2026-11-10). Use the present registry/interview/ledger
checks; do not add the missing template/validator to this change. The runner
owns derived-file updates, verification and the single commit for this draft.

Draft checks on 2026-11-10, attempt 3 (route glm, after two failed Codex
attempts): the twelve answered records in `decisions.md` now carry their
dated decision statements in the repository's form, added without changing
any answer or its context, so `check_question_context.py` can read each
recording day — the one gate that blocked attempts 1 and 2. The gates were
read as code, not run: this session has no shell, and the runner's docs job
is the measurement. The statements restate the recorded answers in the
record form `plans/changes/loop-until-clean/decisions.md` established.

## Boundaries and route

Do not touch existing ADR bodies, decision/adoption answers, leak rules, data
permissions, provider transports, user configuration, research-swarm policy,
implement/repair routing or historical capture data. This plan authorizes no
live provider probes during drafting and no tracker write by an attempt.
If the twelve-hour appetite is spent, stop and report remaining criteria.

Carry-forward Explore fallback: on 2026-11-09, attempt 1 used Stage 1,
endpoint `claude-code-plan`, model `claude-haiku-5-5`; reason: the research
swarm returned report-format failures on its last two runs (research.md;
work item `coding-harness-1ga5`). The same file carries Opus 5.5 public-source
research dated 2026-11-09. No complete `research-swarm/v2` run is present;
`neighbours: []` makes no claim that adjacent loop specs do not exist.

## Time used
