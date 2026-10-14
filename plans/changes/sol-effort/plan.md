---
title: "Plan — sol-effort"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-yzk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, codex, effort]
---

# Plan — sol-effort

```text
For you:     Sol drafts and reviews at high and repairs at medium.
Done when:   Argument checks, instructions and dated ADR amendments agree; make verify is green.
Appetite:    One hour for phase 4 including repairs; stop at the limit.
Not now:     Quota measurements, model or fallback changes, interactive effort defaults.
Pre-mortem:  suppose it failed: most likely because a retry inherits the other verb's effort.
Starts unless you say stop.
```

## Prerequisites

Before phase 4, the orchestrator completes phase 1a's five-answer requirement
for the two ADR edits; only Q-1 and Q-2 are recorded as of 2026-10-14.
It reads the whole draft, resolves any Opus phase-2a rows with a second draft
and shows this card unchanged. This call drafts only; the runner owns
verification and its single commit. No design or new ADR draft is due.
Prepare the worktree with `make venv` once before implementation verification.

## Build sequence

1. Keep one `CODEX` endpoint identity, with its shared default changed to
   `high`; add the per-verb mapping draft/review `high`, repair `medium`.
   Give `run_codex` a keyword-only effort override and pass the mapped value
   at draft's call, `run_attempts`' Codex call using its existing `verb`, and
   both review calls. Preserve `endpoint == CODEX` branches and Codex repair
   formatting; separate effort-bearing tuples would break those comparisons.
2. Extend existing argv regressions for both draft and repair attempts and
   all review session variants. Preserve historical test names, adapt local
   call stand-ins to the new keyword, and keep transport, safety and fallback
   assertions. In particular, draft's `codex-repair` retry stays `high`.
3. Update active instructions and add dated overrides to the two existing
   ADRs, citing the maintainer's 2026-10-13 answers and taking effect on merge.
   Keep their original decision bodies. Add doctrine regressions with planted
   wrong efforts, missing dates and missing overrides, then run verification.

## Files

- `scripts/stage2.py`: select Sol effort by caller verb without changing
  endpoints, retry labels or the existing invocation contract.
- `tests/test_stage2.py`: extend existing launch/routing regressions and add
  the two doctrine tests named in the ledger, preserving prior test names.
- `docs/WORKFLOW.md`: change Sol efforts in the section-3 runner notes and
  section-4 draft, design, plan, repair and review rows.
- `prompts/02-spec.md`: set the drafting Model line to `high`.
- `prompts/02b-design.md`: set the drafting Model line to `high`.
- `prompts/03-plan.md`: set the drafting Model line to `high`.
- `prompts/06-review.md`: set the phase-6 Model line to `high`.
- `docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md`: append a dated
  drafting-effort amendment and stamp `updated` on the edit day.
- `docs/adr/0017-codex-repairs-taken-findings.md`: append a dated repair/review
  effort amendment and stamp `updated` on the edit day.
- `plans/changes/sol-effort/research.md`: retain the current-tree evidence
  added during drafting, including the remaining interview prerequisite.
- `plans/changes/sol-effort/spec.md`: carry the acceptance contract created
  here and incorporate any subsequent phase-2a resolution.
- `plans/changes/sol-effort/plan.md`: carry this plan, resolve reviewed changes
  and record measured implementation/repair spans under `Time used`.
- `plans/changes/sol-effort/decisions.md`: only phase 1a may add real missing
  answers; the existing two answers are preserved by this draft.
- `plans/changes/sol-effort/findings.md`: the runner records attempts and
  reviews; resolve only open phase-2a rows during a later draft.
- `plans/INDEX.md`: the runner regenerates the derived index; do not hand-edit.

No deletions. Do not touch `scripts/stage2_session.py`, `model-endpoints.yaml`,
`AGENTS.md`, permissions, gates, provenance, answer files, other ADRs or
other change folders. No Stage-1 Explore route is recorded in the research.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py tests/test_stage2_runs.py tests/test_model_endpoints.py tests/test_stage2_session.py -q
python3 scripts/check_interview_minimums.py --change sol-effort
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

The requested `python3 scripts/validate_change_artefacts.py --check` cannot
run: that script is absent. Use the available gates and runner checks,
without creating a substitute validator or changing a gate. Once the doctrine
tests exist, replace their `not yet written` ledger entries with test entries.

## Criterion ledger

- 1: tests/test_stage2.py::test_a_draft_starts_codex_with_workspace_write_and_no_bypass — initial draft effort differs from high
- 1: tests/test_stage2.py::test_a_failed_first_draft_gets_one_codex_repair_with_its_diagnostics — extend to assert high on both calls; the retry incorrectly uses repair's medium
- 2: tests/test_stage2.py::test_repair_uses_codex_at_max_effort — retain the historical name and assert medium; the initial repair keeps max
- 2: tests/test_stage2.py::test_repair_retry_uses_fresh_codex_with_diagnostics — extend to assert medium on both calls; retry inherits high
- 3: tests/test_stage2.py::test_codex_is_pinned_on_first_and_resumed_calls — expect high; historical resume or mark call keeps max
- 3: tests/test_stage2.py::test_a_fresh_phase_6_session_says_so — extend fresh-call assertions; its effort is unpinned or wrong
- 3: tests/test_stage2.py::test_phase6_after_codex_repair_starts_a_fresh_read_only_session — extend to assert high; re-check inherits repair's medium
- 3: tests/test_stage2.py::test_the_loop_marks_after_a_recheck_resume_the_fresh_verdict_thread — extend both argv checks; resumed marks lose high
- 4: not yet written tests/test_stage2.py::test_sol_efforts_in_workflow_and_prompts_match_each_verb — plant a wrong effort at each active Sol instruction, including section-3 notes and section-4 repair; also update routing_problems and its existing planted needles
- 5: not yet written tests/test_stage2.py::test_sol_effort_amendments_state_the_dated_overrides — plant a missing/undated ADR 0016 amendment or wrong draft effort
- 6: not yet written tests/test_stage2.py::test_sol_effort_amendments_state_the_dated_overrides — plant a missing/undated ADR 0017 amendment or wrong repair/review effort
- 7: tests/test_stage2_session.py::test_codex_is_dispatched_interactively_with_its_exact_safety_flags — an added interactive effort override changes the exact argv

## Runner handoff — 2026-10-14

Draft baseline: `feat/sol-effort`, HEAD `9113a3d`; only the runner's findings
audit was dirty on entry. Intent remains repair medium, draft/review high,
dated amendments and no new ADR. No phase-2a rows were open. Implementation
is pending; the three missing phase-1a answers remain a prerequisite for ADR
edits. Live PR and tracker state were not read within this call's boundary.
The orchestrator owns tracker writes and the dated journal handover; this
call neither commits nor changes git state. Resume: complete phase 1a for
the claimed ADR amendments, then review the draft and show the card unchanged.

Draft evidence on 2026-10-14: the named interview check, criterion ledger,
frontmatter-current and header/claim checks passed; `git diff --check` passed.
The requested artefact validator exited 2 because its file is absent. Full
registry checking was not run because it reads the shared tracker outside
this worktree; index generation and `make verify` remain with the runner.

## Time used
