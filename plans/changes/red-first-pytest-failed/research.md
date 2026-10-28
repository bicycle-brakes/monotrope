---
title: "Research — red-first-pytest-failed"
status: draft
implementation_status: partial
date: 2026-10-27
last_reviewed: 2026-10-27
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-a7m
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "2026-10-27"}
review: {status: pending, approved_by: null, approved_at: null}
neighbours:
  - plans/changes/red-first-install/spec.md
  - plans/changes/review-loop-deep-b/spec.md
  - plans/changes/stage2-repair/spec.md
  - plans/changes/repair-fixed-lines/spec.md
  - plans/changes/repair-fixed-line-format/spec.md
tags: [research]
---

# red first pytest failed — Research

Stage-2 call, 2026-10-27: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 704 files, 2375 commits, 12 rules.

## Runner exploration — 2026-10-27

## What exists today

**The rule and where it is stated.** A repair row answered `fixed — tests/<file>::<test>` needs a test that is red first — it fails on the baseline's code — and the runner runs that proof itself (`prompts/04-implement.md`, the section on fixed lines, around the sentence "A code row needs a test that is red first"). The `Broke a test` column of a stage-2 `findings.md` excludes the finding's own new test, because "the evidence rule expects it to be red first" (`docs/WORKFLOW.md`, "Two columns for every stage-2 change"). The proof lives entirely in `scripts/stage2.py`: `check_repair_answer` calls `red_first(ctx.root, baseline, anchor, key, tools)` for every fixed code row, then `fixed_test_proof` on the same anchor, and marks the row `yes — <anchor>` only when both return `None` (`scripts/stage2.py`, function `check_repair_answer`, the call site of `red_first`; the mark comment cites R-24, the maintainer's answer C in the night interview of 2026-10-20).

**The proof, end to end (current behavior, after red-first-install merged as PR #155).** `red_first` (`scripts/stage2.py`, function `red_first`) builds a detached scratch worktree at the baseline in a `stage2-red-` temp directory, copies the attempt's whole `tests/` over it (ignoring `__pycache__` and `.pytest_cache`), writes the runner-owned probe into the scratch root as `stage2_red_probe.py` (`RED_PROBE_NAME`, `RED_PROBE_SOURCE`), pre-checks that the interpreter can `import pytest`, then runs exactly the named selector with `python -m pytest -q -p no:cacheprovider -p stage2_red_probe <file>::<function>` under `RED_FIRST_MINUTES = 10`. The interpreter comes from `red_first_python` (the checkout's `.venv/bin/python3` when executable, else `sys.executable`); the child environment goes through `foreign_env`'s allow-list. A ref snapshot (`_ref_targets`) before and after fails the proof on any difference, and cleanup removes the worktree before pruning.

**What the classifier demands today.** The run must exit **exactly 1** ("red first needs exit 1 with an assertion failure", the `done.returncode != 1` branch of `red_first` — exit 2 for an interrupt refuses, as the `interrupted` parameter of `test_red_first_refuses_non_proving_pytest_outcomes` pins). Exit 1 alone proves nothing: the probe record must then pass `_red_record_fault` (`scripts/stage2.py`), which demands schema 1, this selector, this run's fresh token, a finished session, a failing-run exit status, no collection errors, at least one selected case, every node id the selector or one of its parameterized cases, passing setup and passing teardown for every selected case (checked before the call phases, so a missing dependency's fixture error names the setup, not the call — the comment cites bead coding-harness-omp), no xfail/XPASS/skip markers, and — the heart for this change — every failed call must carry `assertion: true`; otherwise it refuses with "the call of `<nodeid>` failed with `<type>`, not an AssertionError". A fully green record refuses with "no selected call failed by assertion". Parameterized named tests may mix passing cases with assertion-failing ones (criterion 1 of the red-first-install spec, tested by `test_red_first_accepts_only_clean_assertion_runs`), but any `Failed`-failing case among them refuses like any other non-assertion failure.

**What the probe records.** Per phase: node id, phase name, final outcome, `assertion` (a bool, set only when `report.failed and isinstance(raised, AssertionError)`), `exception` (the **type name only** — `type(raised).__name__`, no message), and `expected` (xfail mark, `wasxfail`, or `skipped_by_mark`) (`RED_PROBE_SOURCE`, the `pytest_runtest_makereport` hookwrapper). Consequence recorded as fact: a `pytest.raises` "DID NOT RAISE" failure and an explicit `pytest.fail("…")` in the test body are indistinguishable in the record — both show `outcome: "failed"`, `exception: "Failed"`, `assertion: false` (`Failed` is the name of `pytest.fail.Exception`; the test file's own comment at the `Failed` case of `test_red_first_refuses_non_assertion_call_failures` states this naming). `fixed_test_proof` shares the same probe source and the same `_red_record_fault` with `passing=True`; on that path every call must pass, so the `assertion` flag is never read there — but the probe source and the classifier are shared seams between both proofs.

**The contract of record.** The red-first contract is the spec of the predecessor change: `plans/changes/red-first-install/spec.md` (bead coding-harness-omp) defines the term **Assertion failure** ("an uncaught `AssertionError` … during the test body's call phase") and its criterion 4 refuses any other exception, explicitly listing "a call to `pytest.fail` in the test body" as a case that must stay refused. Its `decisions.md` records the fail-closed classification as a `[DETAIL]` ("Count only an assertion failure as red") and names the coordination duty with the guard-test change on the shared `red_first` function. Its `plan.md` repeats: land after, or rebase onto, the guard-test change.

**The recorded cost of the fail-closed rule — the reason this change exists.**

- Phase-6 F-2 of red-first-install (`plans/changes/red-first-install/findings.md`, reviewer Opus 5.5, 2026-10-16): two legitimate red-first forms refuse on every attempt — a test written `with pytest.raises(ValueError): …` whose baseline does not raise (pytest reports "DID NOT RAISE" through its `Failed` exception, refusal reads "failed with Failed, not an AssertionError"), and a test that calls a helper the repair adds (fails with `AttributeError` on the baseline). Both are fail-closed, so no false proof results, but the repair verb ends such a repair as failed after all attempts. The orchestrator rejected F-2 for that change and raised the question to the maintainer as bead coding-harness-a7m (the orchestrator's decision note and the row's Status in the same file).
- Real occurrences on 2026-10-27: phase 6 of review-loop-deep-b, rows F6-7 and F6-8 (`plans/changes/review-loop-deep-b/findings.md`). The runner rejected both Codex repairs "only because its red-first check needs an AssertionError", citing coding-harness-a7m in both status cells. Both named tests — `test_catalog_allowlist_fails_closed_when_pi_rejects_the_overlay` and `test_a_signal_during_process_creation_leaves_no_child`, both in `tests/test_stage2.py` — drive the behavior under test through `pytest.raises(stage2.Refused/CallFailed, match=…)`, so on the baseline the context manager itself raises `Failed` ("DID NOT RAISE"). The orchestrator fell back to hand measurement (tests red without the change, green with it, then `make verify`), and per the same rows `make verify` hit the 30-minute step limit during the retries. Both rows are recorded fixed and the change merged as PR #250.
- Scale, measured textually in this worktree with Grep (method stated; no pytest run): `pytest.raises` occurs 157 times across 25 files under `tests/` — the count includes planted test source inside string literals in `tests/test_stage2.py`, which alone holds 45 occurrences — and `def test_` definitions number about 2140 across 57 files at column 0 or one indent. The reviewer's earlier, differently measured figure was "23 `pytest.raises` uses among 1165 test functions" at `fb4e403` on 2026-10-16 (F-2's evidence cell). The repair verb names tests in `tests/test_stage2.py` most often; both real refusals did.

**Adjacent strands.** The test-strength strand (bead coding-harness-y17, research only at `plans/changes/test-strength-rows/research.md`): rows whose tests are green on the baseline by construction have no red-first form at all and are re-taken by hand as `not a test`. The guard-test strand (bead coding-harness-0ho, branch `explore/guard-test`) owns "the test-only guard exception" policy — which repair rows owe baseline proof, a declared non-goal of red-first-install; the 2026-10-27 handover (`docs/journal/handover/2026-10-27-night-run.md`) lists 0ho as not started. The 2026-10-17 handover lists the a7m question among the open morning items.

## Where it lives

- `scripts/stage2.py` — `RED_FIRST_MINUTES`; `RED_PROBE_NAME` and `RED_PROBE_SOURCE` (the probe, including the `assertion` and `exception` fields); `red_first_python`; `_ref_targets`; `_red_report_bytes`; `_red_own_selector`; `_red_record_fault` (the classifier, including the failed-call branch that demands an `AssertionError`); `fixed_test_proof` (the passing-side proof sharing both probe and classifier); `red_first` (the proof itself, whose docstring states the rule); the `check_repair_answer` call site.
- `tests/test_stage2.py` — the red-first classification cluster under the comment heading "The red-first outcome classification (bead coding-harness-omp)": `test_red_first_accepts_only_clean_assertion_runs`, `test_red_first_refuses_a_missing_pi_install`, `test_red_first_refuses_setup_and_teardown_errors`, `test_red_first_refuses_non_assertion_call_failures` (RuntimeError / ImportError / Failed), `test_red_first_refuses_non_proving_pytest_outcomes` (ten parameterized cases), `test_red_first_refuses_missing_or_invalid_evidence`, `test_red_first_refuses_a_timed_out_run`, `test_repair_refuses_environment_only_red_first_evidence`, `test_red_first_scrubs_outcome_diagnostics`; plus the older cluster `test_red_first_refuses_a_changed_venv`, `test_a_named_test_that_is_not_red_first_fails_the_attempt`, `test_a_red_first_interpreter_that_cannot_start_pytest_fails_the_attempt`, `test_the_red_first_run_leaves_no_worktree_behind`, and the failed-`worktree remove` test beside it.
- `plans/changes/red-first-install/spec.md`, `decisions.md`, `plan.md`, `findings.md`, `research.md` — the contract of record and its history (F-2 with the two refused forms and the ad-hoc measurements).
- `plans/changes/review-loop-deep-b/findings.md` — F6-7 and F6-8, the two real runner rejections citing coding-harness-a7m.
- `prompts/04-implement.md` and `docs/WORKFLOW.md` — the doctrine wording quoted above.
- `docs/journal/handover/2026-10-17-night-run-sixth.md`, `2026-10-27-night-run.md` — the question's open status; 0ho's unstarted state.

## What is unclear

1. The exact text of bead coding-harness-a7m is not read: the tracker is the Dolt database under `.beads/`, which my read-only file tools cannot open, and no rendered copy is committed (repository house rule 2). Everything known about the question comes from F-2's row and evidence cell and from the F6-7/F6-8 status notes.
2. The maintainer's intended scope is nowhere recorded in this tree: whether acceptance should cover only pytest's own `Failed` verdict (DID NOT RAISE, and possibly explicit `pytest.fail`), or all ordinary call-phase exceptions (including the missing-helper `AttributeError`/`NameError` case F-2 names as its second example). The change name says "pytest failed"; the F-2 text names both forms. Not found in the tree — an open question for the interview, not a guess.
3. Whether red-first-install's criterion 4 refusal of an explicit body `pytest.fail` should stand while a `pytest.raises` DID-NOT-RAISE is accepted cannot be decided from the record as it exists: the probe stores the exception type name only, no message, so the two are indistinguishable today. Recorded as fact; the policy itself is a decision.
4. What the guard-test branch (`explore/guard-test`, bead 0ho) changes inside `red_first` is unreadable from this worktree; only the coordination duty is on record. The branch was not read — not "the branch contains nothing".
5. My `pytest.raises` and test-function counts are textual (they include planted string sources; the function count covers two indentation depths). A count of live uses inside test bodies was not measured.
6. No artifact in this worktree records a maintainer answer to a7m; the change folder was opened 2026-10-27 (commit 119420a9 on `fix/red-first-pytest-failed`) with an empty research skeleton, which is consistent with the question being moved into a change but records no decision.

## Files a change would have to touch

- `scripts/stage2.py` — the probe's `assertion`/`exception` fields in `RED_PROBE_SOURCE` (if the evidence must distinguish failure shapes, the record would have to hold more than the type name) and/or the failed-call branch of `_red_record_fault` (the acceptance rule); the docstrings of `red_first` and `fixed_test_proof` that state the rule; the refusal message text that tests pin. `fixed_test_proof` shares both seams, so any probe or classifier edit touches it.
- `tests/test_stage2.py` — `test_red_first_refuses_non_assertion_call_failures` (its `Failed` case asserts today's refusal and would change meaning), the plants beside it (`MISSING_PI_TEST` keeps a fixture-level `pytest.fail`, which fails the setup phase and is refused by the setup check regardless of any call-phase rule), and new cases for whichever failure shape becomes acceptable, on the established `repair_world`/`red_first_planted` pattern.
- `plans/changes/red-first-install/spec.md` — its term "Assertion failure" and criterion 4 are the contract a change would amend; how the amendment relates to that living spec is a workflow question for the spec phase, stated here only as the point of contact.
- `prompts/04-implement.md` / `docs/WORKFLOW.md` — only if the doctrine wording ("fails on the baseline's code") needs to name the accepted evidence classes; the current wording is generic and may stand unchanged.
