---
title: "Plan — handoff-new-feature"
status: draft
implementation_status: partial
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-in27
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, research-handoff, gate]
---

# Plan — handoff-new-feature

```text
For you:     New feature and architectural specs need complete research or a visible, reasoned maintainer exception.
Done when:   Gate tests prove the missing-run failure, dated legacy boundary and exception limits, and make verify is green.
Appetite:    2 hours of phase 4, including repairs; stop at the limit.
Not now:     Research execution, session handovers or decisions for other changes.
Pre-mortem:  suppose it failed: most likely because an exception returns before existing evidence checks run.
Starts unless you say stop.
```

## Files and steps

Route as run, 2026-11-04: the orchestrator launched stage-2 implement anyway
(two GLM 5.3 Flash and three Sonnet 5.5 attempts), made the adoption bootstrap
by hand after the first two, and accepted the last attempt by hand; review-loop
repairs go through the runner. The plan's original route read: the orchestrator
implements this repair manually. Do not launch stage-2 implement or repair: the human-decided adoption record is required for the
new checker to pass its own full verification, so an attempt cannot become
accepted before that bootstrap edit. No held edit is assigned to an attempt;
there is no accepted-attempt/bootstrap ordering to perform on this manual route.
No `templates/plan.md` exists; the phase-3 prompt supplies the plan form.

1. `tests/test_research_handoff.py`: add the ledger tests using the real
   `gate.main` and command-line entry point in temporary trees. Give fixtures
   their own adoption record; date old no-v2 fixtures explicitly, retaining
   their legacy assertion rather than removing coverage. Parameterize both
   swarm classes, both exempt classes, absent/plain/incomplete research,
   live/archive and named/all selection. First run the new-feature and
   invalid-exception cases red against the unchanged checker.
2. `scripts/check_research_handoff.py`: replace unconditional absent/no-v2
   returns with the spec-boundary applicability check. Reuse
   `adoption.adopted_on(root, "research-handoff")`; obtain the root from
   `run`, not a fixed global when `--root` is supplied. Use existing strict
   YAML parsing for `spec.md` and any `research.md` header. For no-v2 stock,
   start day on/before adoption permits missing historical class; otherwise
   require a valid spec class and agreement with any research class.
   `bounded`/`spike` need no adoption comparison when their class is known.
   Missing required metadata raises `CannotMeasure`; never fallback from an
   unreadable research date to a spec date or filesystem timestamp.
   Extend `QRecord`/`parse_decisions` for at most one
   `research_swarm_exception` mapping with exactly `granted` (boolean) and
   `reason` (text). Qualify grants only with the spec's human-answer/context
   requirements; blank reasons and false/missing grants do not qualify.
   For exceptions, validate answer and context as text before the existing
   parser can stringify values; booleans and collections cannot authorize a grant.
   Preserve duplicate-field/key detection, malformed-type errors and exit-3
   precedence. Keep parsing/validating runs before applying exceptions, and
   keep every complete run's inventory, answer, neighbour and basis checks.
   Apply the exception only to the missing-complete-run finding. With no
   spec, report pending instead of legacy for missing evidence; preserve
   malformed-evidence errors. Update the module's contract and output notes.
3. `decisions/adoption.yaml`: orchestrator-only bootstrap edit on this manual
   route, adding `research-handoff: 2026-10-26` under `adopted`; preserve
   existing dates. This is a human-decided path, so the final pull request
   uses the decision template, title `decide(research-handoff): require research
   for new feature specs`, and the `decision` label. The recorded interview
   authorizes the rule; merge gives it effect. Do not create an ADR answer.
   `tests/test_this_repository_adoption.py`: add the repository-specific date
   assertion named in the ledger; keep it separate from travelling fixtures.
4. `docs/WORKFLOW.md`: update only “The handoff is checked” with prospective
   applicability, start-day precedence, pending behavior, exception spelling
   and limits, output and exit codes. Run the regression suite and inspect
   the offline kit tests; its existing manifest already carries the checker,
   its tests, adoption reader and workflow, so no manifest edit is planned.
5. Update this change's `spec.md` implementation/review metadata, `plan.md`
   ledger and time below, and `findings.md` with revision-bound evidence;
   `research.md` changes only for further repository-backed gaps. Regenerate
   `plans/INDEX.md` with its command. No file is deleted.

## Verification

Run targeted red/green checks, then the complete verification after the
orchestrator's bootstrap. The last command is the phase-4 completion gate.

```sh
.venv/bin/python3 -m pytest -q tests/test_research_handoff.py tests/test_this_repository_adoption.py
.venv/bin/python3 -m pytest -q tests/test_kit.py
.venv/bin/python3 scripts/check_interview_minimums.py --change handoff-new-feature
.venv/bin/python3 scripts/check_research_handoff.py --change handoff-new-feature
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/plans_registry.py --index
make verify
```

`scripts/validate_change_artefacts.py` is absent at `a98c09c1`; do not claim
its gate ran. The current draft only checks available read-only gates; index
regeneration and full verification belong to the outer runner or phase 4.

## Criterion ledger

- 1: tests/test_research_handoff.py::test_new_swarm_class_without_complete_research_is_red — a spec with absent, plain or only incomplete research is exempted; replacing the applicability check with the old early return must turn this test red.
- 2: tests/test_research_handoff.py::test_legacy_exemption_uses_start_day — later spec/review dates or archiving lose the pre-adoption exemption; day-before/day-of/day-after fixtures expose the boundary.
- 2: tests/test_this_repository_adoption.py::test_this_repository_adopted_research_handoff_on_2026_10_26 — the repository's adoption date is absent or differs from the merge day.
- 3: tests/test_research_handoff.py::test_non_swarm_classes_are_exempt_by_class — either exempt class requires a swarm or is reported as legacy.
- 4: tests/test_research_handoff.py::test_only_a_reasoned_maintainer_exception_waives_missing_research — removing human authorization, actual answer, context, grant or reason still gives success; the valid grant omits its question or reason in output.
- 5: tests/test_research_handoff.py::test_ambiguous_applicability_or_exception_is_not_measured — missing/invalid adoption or start dates, invalid/conflicting classes, duplicate fields or multiple exception records pass or crash instead of exiting 3; a second finding must not mask exit 3.
- 6: tests/test_research_handoff.py::test_exception_never_hides_existing_research_failures — a granted exception suppresses malformed evidence, missing inventory/answers, bad neighbours or bad bases.
- 6: tests/test_research_handoff.py::test_only_complete_runs_supply_handoff_and_prior_obligations_survive — incomplete claims supply a basis or a rerun erases prior complete-run obligations.
- 7: tests/test_research_handoff.py::test_missing_research_before_spec_is_pending — no spec with absent/plain/incomplete research becomes a legacy exemption or a missing-run failure; malformed evidence exits 0.
- 7: tests/test_research_handoff.py::test_pending_handoff_is_green_only_before_spec — valid pending complete-run items block before spec or pass after spec.
- 8: tests/test_research_handoff.py::test_applicability_and_exceptions_hold_in_live_archive_and_cli — selection or archival skips the new check; temporary offline fixtures use external state.

## Boundaries and route

No edits to `scripts/stage2.py`, `scripts/research_handoff.py`, `scripts/adoption.py`,
`decisions/gates.yaml`, kit manifest, CI, prompts, templates, ADRs, harness
configuration, session-handover files or another change folder (one exception:
the orchestrator's Q-6 record in `plans/changes/go-access-point/decisions.md`,
`decisions.md#Q-2`).
Explore ran on 2026-11-04 through Stage 2, route flash, endpoint
`glm-coding-plan`, model `glm-5.3-flash`; no Stage-1 fallback is recorded.
No design or ADR draft is due for this bounded repair.

Known integration dependency at `a98c09c1` (2026-11-04): the feature for one
Go access point has start day 2026-10-31 and records a maintainer exception
in introductory prose, without the proposed structured field
(`plans/changes/go-access-point/decisions.md`). Under this rule the all-tree
gate will expose it. Report that failure to the orchestrator. Resolved on
2026-11-04: the maintainer confirmed the exception and the orchestrator
recorded it (`decisions.md#Q-2`); an attempt still never edits that change. Do not invent an answer,
edit that change, weaken applicability or call verification green while it
blocks. The same applies to any additional dependency found during phase 4.

The outer session shows the card unchanged before implementation. This
draft stops after writing and checking artifacts; it does not start phase 4.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash failed both attempts (ruff, then a test TypeError and a broken adoption test), 2026-11-04; continues from the kept attempt.

## Runner route — 2026-11-04

Stage-1 route: implement · model claude-sonnet-5-5 · reason: GLM 5.3 Flash failed both attempts, 2026-11-04; after the orchestrator's adoption bootstrap the full make verify is red because the checker reads older changes' prose decisions answers as YAML (adr-owning-change Q-5, attempt-diagnostics Q-1): an exempt or legacy change must not need a readable answer.

## Time used

2026-11-04 16:42:05–18:07:03 UTC, 5097 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 18:07:13–18:27:55 UTC, 1242 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-04 18:28:11–18:28:36 UTC, 25 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 18:30:01–18:30:48 UTC, 47 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 19:13:37–20:12:54 UTC, 3558 s — implement · attempt 1 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-04 22:38:43–2026-11-05 01:10:01 UTC, 9078 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · measured by the runner

## Appetite overrun — 2026-11-04

Phase 4 took 9,969 s (about 2.8 h) against the 2-hour appetite, largely verify-lock waits and failed attempts. The orchestrator reported it after review-loop round 1; the maintainer let the change run to its pull request without a limit (2026-11-04, ~22:36 UTC).
