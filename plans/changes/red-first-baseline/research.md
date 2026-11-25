---
title: "Research — red-first-baseline"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-7aso
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# red first baseline — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1148 files, 5012 commits, 12 rules.

## Runner exploration — 2026-11-21

Research complete. Here is the prose for `plans/changes/red-first-baseline/research.md`, ready to append below the existing Stage-2 call line.

---

## What exists today

**The change's bead and its two recorded incidents.** This change is bead `coding-harness-7aso` (frontmatter of this `research.md`; `plans/INDEX.md`, row for `changes/red-first-baseline/research.md`). The day handover of 2026-11-20 records the triggering fault: "The runner's red-first check misjudged two tests of finder-partial-report as green on the baseline; both were red by hand (bead coding-harness-7aso)" (`docs/journal/handover/2026-11-20-day-run.md`, "Findings and beads of the day"). The same day the maintainer confirmed a second, related case: "red-first impossibility confirmed plus bead (coding-harness-bf9m)" (`docs/journal/handover/2026-11-20-day-run.md`, "Decisions and preferences"). The earlier incident behind `bf9m` is recorded in the night handover: phase-6 rows R-1/R-2 of journal-citation-gate were "repaired by orchestrator hand acceptance: the runner's red-first check cannot work when the code under test lives in the test file; red-first checked by hand (both tests red on the old code)" (`docs/journal/handover/2026-11-20-night-run-2026-11-19-b.md`, "Needed from the maintainer" table, row journal-citation-gate; commit `94439546`).

**Where the red-first proof lives.** The baseline proof is `red_first(root, baseline, test, key, tools)` in `scripts/stage2.py` (`def red_first`, scripts/stage2.py). Its single call site is the repair verb's answer check: `check_repair_answer` in `scripts/stage2.py` calls `red_first(ctx.root, baseline, anchor, key, tools)` for every row answered `fixed — tests/…`; a grep over `scripts/` finds no other caller. The `baseline` string is `git rev-parse HEAD` captured in `repair` before the first model call (`def repair`, scripts/stage2.py). The fixed-code proof (`fixed_test_proof`) and the guard-test proof (`guard_test_proof`, two legs around `STAGE2_PLANT_FAULT`) share the helper `_attempt_tree_proof` in `scripts/stage2.py`; the repair answer check routes `fixed — guard test — …` rows to `guard_test_proof` instead of the baseline proof.

**How the baseline checkout is built.** `red_first` creates a temporary directory `stage2-red-` and a private repository via `_private_repository(root, tree, baseline)` (`scripts/stage2.py`, `def _private_repository`): a `git clone --no-hardlinks` of the source, remote removed, every source ref preserved under its own name, HEAD detached at `baseline`. Then `shutil.rmtree(tree / "tests")` removes the baseline's tests and `git restore --source <worktree_tree(root)> --worktree -- tests` overlays the attempt's Git-visible `tests/` tree (`worktree_tree` in `scripts/stage2.py` writes the worktree's current tree through a temporary index, including untracked non-ignored and force-added ignored files). Only the pathspec `tests` is restored from the attempt; every other path in the private checkout is the baseline commit's bytes. The interpreter is the checkout's `.venv/bin/python3` when executable, else the running one (`red_first_python`, `scripts/stage2.py`), and a changed `.venv` tree refuses the proof up front (`tool_problem` guard at the top of `red_first`; rule R-21).

**How the outcome is judged.** Two admission-wrapped launches run under `verify_lock.hold_admission` with a 10-minute limit (`RED_FIRST_MINUTES`, `scripts/stage2.py`): first `python -c "import pytest"` (a startup failure must refuse, phase-6 F-1), then `python -m pytest -q -p no:cacheprovider -p stage2_red_probe <file>::<function>`. The runner-owned probe `RED_PROBE_SOURCE` (`scripts/stage2.py`, constants block near `RED_PROBE_NAME`) travels into the checkout as a plugin and writes a JSON record (schema 1, fresh token, selector, collection errors, selected node ids, per-phase outcomes with `assertion`/`pytest_failed`/`exception`/`expected` flags, session finish and exit status). The runner requires pytest exit exactly 1 ("pytest ended N on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome"), then `_red_record_fault` (`scripts/stage2.py`) validates the record: this invocation's token and selector, a finished failing session, no collection errors, a non-empty selection of the requested test only, at least one qualifying call failure (uncaught `AssertionError` or `pytest.fail.Exception` — DID-NOT-RAISE, DID-NOT-WARN, explicit `pytest.fail`, subclasses included), passing setup and teardown for every selected case, and no skip, xfail, XPASS or nonqualifying failure among them. Before/after snapshots of the private store's refs (`_ref_targets`, `_proof_ref_targets`, `_proof_reference_guard`) fail the proof if any ref changed, compared in `finally` before cleanup (`_remove_private`); nothing in the source repository is written (successor spec red-first-own-refs, criteria 1–9).

**Doctrine.** `docs/WORKFLOW.md` §"Repairing taken findings (repair)", paragraph "Red first:" — the runner proves each code repair by running the named test alone against the baseline's code; the guard-test exception paragraph (ADR 0023) follows it. `docs/testing.md` layer 2 ("Red first") states the same rule as the strategy that travels with the kit. `prompts/04-implement.md` tells the model a code row "needs a test that is red first — it fails on the baseline's code — and the runner runs that proof itself", and `prompts/04b-review-loop.md` step 1 has `triage` refuse a plain `taken` on a row whose finding touches only tests, naming the corrective guard form. ADR 0023 (`docs/adr/0023-guard-proof-for-test-only-repairs.md`) is the accepted decision for repairs that live only in test code; the gate `guard-test-environment` in `decisions/gates.yaml` refuses any verification run while `STAGE2_PLANT_FAULT` is present.

**The proof's amendment history (all archived, all implemented).**
- `plans/changes/archive/2026-11-06-red-first-install/spec.md` (bead `coding-harness-omp`, 2026-10-16): outcome classification introduced after a missing ignored Pi installation made a fixture error read as red; environment faults refuse.
- `plans/changes/archive/2026-11-06-red-first-pytest-failed/spec.md` (bead `coding-harness-a7m`, 2026-10-27): pytest's own `Failed` outcome counts as red; exit contract "exactly 1 (red side) or 0 (fixed side)"; missing-helper `NameError`/`ImportError`/`AttributeError` stays refused.
- `plans/changes/archive/2026-11-16-red-first-own-refs/spec.md` (bead `coding-harness-wkxm`, 2026-11-01): proofs moved into private repositories with their own ref stores; its Boundary states the tests-only carryover: ignored, untracked fixtures do not reach a proof, and a named test depending on them refuses.
- `plans/changes/archive/2026-11-16-guard-test/` (bead `coding-harness-0ho`, folding `coding-harness-y17`): the guard-test two-leg proof; `plans/changes/archive/2026-11-06-test-strength-rows/research.md` (bead `coding-harness-y17`) is the older strand about tests that already pass on baseline.
- The one living spec, `plans/specs/implementation-verification/spec.md`, holds verify preparation and slip counting; a grep for `red|baseline` finds no red-first clause in it — it is adjacent only through the shared admission machinery (`verify_lock.hold_admission`) that `red_first` uses.

**Existing evidence.** `tests/test_stage2.py` holds the red-first regression suite: `test_red_first_refuses_a_changed_venv` (O188-2), `test_a_named_test_that_is_not_red_first_fails_the_attempt` (criterion 18, asserts the exact "pytest ended 0 on the baseline's code" diagnostic), `test_a_red_first_interpreter_that_cannot_start_pytest_fails_the_attempt` (phase-6 F-1), `test_the_red_first_run_leaves_no_worktree_behind` (criterion 19), the ref-snapshot fault test (phase-6 F-7), and the classification block under the comment "The red-first outcome classification (bead coding-harness-omp)" (`test_red_first_accepts_only_clean_assertion_runs`, `test_red_first_accepts_pytest_failed_call_outcomes`, `test_red_first_refuses_a_missing_pi_install`, `test_red_first_refuses_setup_and_teardown_errors`, `test_red_first_refuses_non_assertion_call_failures`, and neighbours). The comment above `OTHER_TEST` in `tests/test_stage2.py` states the multi-round rule as a fact of the fixture design: "a repair run that stands on an earlier run's commit needs a fix the earlier commit does not carry, or the red-first proof finds its test green on the baseline."

## Where it lives

- Proof and classification: `scripts/stage2.py` — `red_first`, `_private_repository`, `worktree_tree`, `red_first_python`, `RED_PROBE_NAME`/`RED_PROBE_SOURCE`/`RED_FIRST_MINUTES`, `_red_record_fault`, `_ref_targets`/`_proof_ref_targets`/`_proof_reference_guard`, `_remove_private`, `guard_test_proof`/`fixed_test_proof`/`_attempt_tree_proof`/`GUARD_SOURCE_PROBE_SOURCE`.
- Caller and baseline capture: `check_repair_answer` and `repair` in `scripts/stage2.py`; the attempt loop `run_attempts` in `scripts/stage2.py` carries `baseline` through.
- Doctrine: `docs/WORKFLOW.md` (§"Repairing taken findings (repair)"), `docs/testing.md` (layers 2 and the "Reviews find, tests prove" section), `docs/adr/0023-guard-proof-for-test-only-repairs.md`, `prompts/04-implement.md`, `prompts/04b-review-loop.md`, `decisions/gates.yaml` (`guard-test-environment`).
- Evidence: `tests/test_stage2.py` blocks named above; `tests/test_run_report.py` pins the report wording "the orchestrator's red-first check of the eight retained repairs".
- Adjacent runner checks in the same family: `PYTEST` and `selected_tests` in `scripts/stage2.py` (the attempt's cheap pytest selection — bead `coding-harness-bxxt.9` territory: the runner hands pytest ledger ids including `not yet written` entries, and pytest-xdist ends exit 5 naming none, per the closed diagnosis bead `coding-harness-ogfn` in `docs/journal/handover/2026-11-20-day-run.md`).

## What is unclear about it

- **The `7aso` misjudgement's mechanism is not recorded anywhere in this worktree.** The two named tests, the repair round, the runner's exact diagnostic line and how the by-hand check was run live on the unmerged lane branch `fix/finder-partial-report` (branch/head recorded in `docs/journal/handover/2026-11-20-day-run.md`, lane table) and in bead `coding-harness-7aso`'s notes (Dolt tracker, transported via `refs/dolt/data`; no rendered copy is committed, and this phase reads no tracker). `Glob plans/changes/finder-partial-report/**` finds no files here. Without those, "misjudged as green on the baseline" cannot yet be attributed to a baseline-construction fault, an environment difference in the private checkout, or a correctly-green baseline that the by-hand check then contradicted.
- **Whether the `7aso` case is the confirmed impossibility class or a second mechanism.** The structural fact is that the private checkout takes only `tests/` from the attempt (`git restore --worktree -- tests`); any red that depends on attempt bytes outside `tests/` cannot show on that baseline. The `bf9m`/journal-citation-gate case ("the code under test lives in the test file") is the maintainer-confirmed instance of that class. Whether the two finder-partial-report tests belong to the same class — or ran green for a different reason, e.g. the baseline already containing an earlier round's fix for the same mechanism (each repair round checkpoints `fix(<change>): repair taken findings <IDs>`, `docs/WORKFLOW.md` §"Repairing taken findings") — is unread.
- **Exit-code contract divergence, doc vs code.** `docs/WORKFLOW.md` §"Repairing taken findings" says the runner "accepts a test only when pytest exits 1 or 2 there"; the code requires exactly exit 1 (`red_first`, exit check), and the successor spec `red-first-pytest-failed` defines "exit exactly 1 (red side)". The successor spec states it governs; whether the WORKFLOW sentence should be aligned is a question for the interview.
- **A stale-looking sentence in `docs/testing.md`** ("Reviews find, tests prove"): "Where a fix lives only in test code … Today the orchestrator then shows, by hand, a planted fault …; a runner form for it is open work." The runner form exists and is accepted (`guard_test_proof` in `scripts/stage2.py`, ADR 0023, `docs/WORKFLOW.md` guard-test paragraph). Whether that sentence means hand repairs by the orchestrator (where no runner runs) or is simply out of date is unresolved.
- **Not read:** bead notes for `coding-harness-7aso`, `coding-harness-bf9m`, `coding-harness-ogfn` (all tracker-only); the `fix/finder-partial-report` branch's `findings.md`/loop record; the saved attempt evidence of the refused repair under the worktree's own git directory (not located from this session); `git log` context of the incident commits.

## Which files a change would have to touch

- `scripts/stage2.py` — whatever the diagnosis names: most plausibly the baseline construction in `red_first`/`_private_repository`/the `tests` overlay, the exit/outcome contract in `red_first` + `_red_record_fault`, the baseline capture in `repair`, and the answer-check routing in `check_repair_answer` (baseline route vs guard-test route).
- `tests/test_stage2.py` — the red-first blocks listed under "Existing evidence"; any new rule needs its red-first regression with a planted fault, per `docs/testing.md` ("Each new test names its fault").
- `docs/WORKFLOW.md` §"Repairing taken findings (repair)" and `prompts/04-implement.md` / `prompts/04b-review-loop.md` — only if the red-first or guard-test wording changes; `docs/testing.md` layer 2 likewise.
- `plans/INDEX.md` is runner-rendered; no ADR file is known to be implicated from the facts read so far.

**Suggested `neighbours:` header** (specs already known to this exploration):

```
neighbours:
  - plans/changes/archive/2026-11-06-red-first-install/spec.md
  - plans/changes/archive/2026-11-06-red-first-pytest-failed/spec.md
  - plans/changes/archive/2026-11-16-red-first-own-refs/spec.md
  - plans/changes/archive/2026-11-16-guard-test/spec.md
  - plans/changes/archive/2026-11-06-test-strength-rows/research.md
  - plans/specs/implementation-verification/spec.md
```

Tracker-only neighbours, named for the interview, not the header: `coding-harness-7aso` (this change), `coding-harness-bf9m` (red-first impossibility, confirmed 2026-11-20), `coding-harness-yd8w`/`coding-harness-x9ed` (the two lanes whose incidents triggered them), `coding-harness-bxxt.9` and closed `coding-harness-ogfn` (the cheap-pytest selection family), `coding-harness-u1ha` (verify slots, shares the admission queue this proof waits in).
