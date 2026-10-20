---
title: "Plan — runner-precheck"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-csm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, verification]
---

# Plan — runner-precheck

```text
For you:     Failed implement and repair attempts stop before full verification when their cheap checks are red, and retries see the first failing assertions.
Done when:   The nine criteria have passing regression proofs and make verify is green; a passing pre-check alone never permits a commit.
Appetite:    2 hours of phase 4 including repairs; stop at the limit.
Not now:     Automatic time entries, test retries, provider routing, model permissions or replacement of full verification.
Pre-mortem:  suppose it failed: most likely because the new assertion evidence is truncated again on its way into the retry prompt.
Starts unless you say stop.
```

## Scope and prerequisites

Build `spec.md` criteria 1–9, class bounded; no design or ADR is due.
Repository facts were read at `52e440d` on 2026-10-20. No phase-2a rows are
open in the current `findings.md`. This call drafts only; the orchestrator
shows the card unchanged before phase 4 and owns the runner's commit.

Explore was performed by the Opus 5.5 orchestrator on 2026-10-20 because
`explore --stage2-off` currently produces no research (coding-harness-e7m —
empty fallback exploration). Research records no executed Stage-1 fallback
or fallback model; do not invent one. During the temporary Z.ai outage use
the active Sol 6.1 implementation session, as the repository instructs.

## Build sequence

1. In `verify_attempt`, keep derived-file preparation first, then evaluate
   the existing `time_log`/Counter difference against the pre-call plan.
   Preserve the baseline rule excluding moved old lines; return its failure
   before starting format, targeted pytest or full verification.
2. Keep `format_step` and its audit list. Add a strict, non-mutating ruff
   check of `format_targets` after safe fixes/formatting, using `.venv/bin/ruff`
   and the existing exclusion/no-cache options. No targets means no ruff.
   Missing/unlaunchable ruff or nonzero check returns bounded scrubbed
   diagnostics; do not infer success from the formatting note.
3. Import the ledger gate's readers; require exactly one section and use
   `parse_entry` with its continuation rules, rejecting malformed rows.
   Select only kind `test`, deduplicate in ledger order, and validate resolved
   test paths stay under the worktree's `tests/`. Do not import test modules
   while reading the ledger. Empty selections proceed directly to `make verify`.
4. Launch `[red_first_python(root), '-m', 'pytest', '-q', '--tb=long',
   '--color=no', '-p', 'no:cacheprovider', *selectors]` once, serially with
   a 600-second timeout, worktree cwd, empty stdin and the same `foreign_env`
   used for verification. Pass arguments as a list, never through a shell.
   Any nonzero exit or `CallFailed` becomes an attempt problem, naming the
   step/selectors, without starting `make verify`; reuse existing retries.
5. Add a shared pytest failure-block extractor for targeted output and
   `verify_evidence`. Retain the first three blocks in printed order, including
   parameterized headings, assertion lines and multiline explanations; cap
   at 60 lines per block and 180 total, labels and omission markers included.
   Scrub first; cap lines at 500 characters with a suffix marker. If a block
   is over budget retain its heading and assertion-bearing context before
   surrounding source; explicitly mark omitted middle content. Preserve
   existing red-gate/stdout-fallback/stderr tails after the assertion section.
   No recognized block means the existing bounded fallback, never green.
   Exercise the final quoted findings and next prompt, not just the extractor.
6. After green pre-checks run the existing `make verify` exactly as before.
   Keep checkpoint, credential scans, repair red-first and retry counts intact.
   Draft uses `verify_draft`, not `verify_attempt`: only shared diagnostic
   enrichment affects it. Update obsolete formatter-verdict expectations in
   existing tests, retaining top-level names referenced by historical ledgers
   and documenting why their expected outcome changes under this spec.

## Files and limits

- `scripts/stage2.py`: implement pre-check ordering and shared bounded assertion evidence; update its affected docstrings.
- `tests/test_stage2.py`: add the ledger's regressions using the existing world/stand-ins and isolated real pytest cases; adjust old early-abort expectations without renaming referenced tests.
- `plans/changes/runner-precheck/spec.md`: create the contract and update implementation metadata during phase 4.
- `plans/changes/runner-precheck/plan.md`: create this plan; replace ledger promise markers as tests land and record measured phase-4 time.
- `plans/changes/runner-precheck/research.md`: append the draft-time repository corrections; retain prior evidence.
- `plans/changes/runner-precheck/findings.md`: preserve the audit line; the runner appends execution and review evidence.
- `plans/INDEX.md`: the runner regenerates the derived registry; this draft does not edit it.

No deletion. Leave `decisions.md`, the ledger gate, gate definitions, prompts,
model declarations, leak rules, red-first classifier and other changes intact.
Hosted PR state and live parallel-session ownership were not read; coordinate
ownership before implementation or tracker writes. This draft writes no tracker.

## Verification

In the implementation worktree run `make venv` once if not already prepared,
then run these commands verbatim:

```sh
.venv/bin/python3 -m pytest tests/test_stage2.py -q
python3 scripts/check_interview_minimums.py --change runner-precheck
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at
`52e440d`: this plan follows the phase-3 prompt and existing plan form.
Do not create either missing file or claim the requested validator passed.
The runner owns index preparation, full verification and the single commit.
No live provider call or external service is needed for the regression proofs.

Draft validation on 2026-10-20 at `52e440d` plus these artifacts: the interview
gate and criterion-ledger gate passed. Direct structural checks passed for
required metadata, bounded class, plan card and empty time section.
`plans_registry.py --check` was not run in this draft; its tracker coupling
and regenerated-index check, and the full `make verify`, remain runner-owned.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_precheck_rejects_missing_time_before_verify — absent, unchanged or moved old time lines still launch make.
- 2: not yet written tests/test_stage2.py::test_precheck_requires_clean_post_format_ruff — unresolved syntax/lint or an unavailable ruff reaches pytest/make; safe fixes wrongly fail.
- 3: not yet written tests/test_stage2.py::test_precheck_selects_only_distinct_concrete_ledger_tests — duplicate, promised, fenced or unrelated selectors run, or an empty selection runs all tests.
- 4: not yet written tests/test_stage2.py::test_precheck_refuses_unreadable_or_unsafe_ledgers — malformed/missing/duplicate sections or escaping paths reach pytest/make.
- 5: not yet written tests/test_stage2.py::test_precheck_pytest_failure_skips_full_verify — exits 1–5, launch failure or timeout still start full verification.
- 6: not yet written tests/test_stage2.py::test_precheck_green_still_requires_full_verify_before_checkpoint — green targeted tests plus red full verification commit, or retry handling is bypassed.
- 7: not yet written tests/test_stage2.py::test_first_assertion_blocks_survive_long_verify_output — early multiline assertion evidence disappears from targeted/full-run retries despite fitting the budget.
- 8: not yet written tests/test_stage2.py::test_precheck_evidence_is_scrubbed_bounded_and_persisted — secret-bearing/oversized evidence escapes limits or silently loses content in prompts/findings.
- 9: not yet written tests/test_stage2.py::test_precheck_preserves_environment_and_draft_boundary — subprocesses inherit credentials, model tool permissions widen or draft requires measured implementation time.

## Time used
