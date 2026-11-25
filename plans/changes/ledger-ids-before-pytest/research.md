---
title: "Research — ledger-ids-before-pytest"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-20", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# ledger ids before pytest — Research

Stage-2 call, 2026-11-20: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1145 files, 4931 commits, 12 rules.

## Runner exploration — 2026-11-20

The exploration is complete. Here is the research, as prose ready to append to `plans/changes/ledger-ids-before-pytest/research.md`.

---

## What exists today

The "ledger" of this repository is the **criterion ledger**: a `plan.md` section `## Criterion ledger` with one line per acceptance criterion, in one of three entry forms — `- <n>: tests/<file>::<function> …`, `- <n>: not yet written tests/<file>::<function> …`, `- <n>: not a test — …` (regexes `TEST`, `NOT_YET`, `NOT_A_TEST`, `scripts/check_criterion_ledger.py:65-70`, `parse_entry` at `scripts/check_criterion_ledger.py:152`). The gate `criterion-ledger` holds it (`scripts/check_criterion_ledger.py`, ADR `decisions/adr/0013-every-criterion-names-its-proof.md`; `docs/governance/gate-catalog.md`, row `criterion-ledger`). "Ledger ids" are the test references the ledger carries, read as `tests/x.py::test_y` ids by the stage-2 runner's `_ledger_test_refs` (`scripts/stage2.py:6578`).

The stage-2 runner runs **cheap checks before anything expensive**: in full mode, format → cheap checks → ledger clearing → derived preparation → the admitted `make verify` (`verify_attempt`'s `prepare()`, `scripts/stage2.py:7493-7523`; the admission is taken only around the protected gates — `bead coding-harness-bxxt.6` is cited in that block). In targeted mode the same preparation runs outside the admission (`_targeted_body`, `scripts/stage2.py:7302`). `cheap_checks` is ruff lint, ruff format check, then **pytest over the selected tests** with the fixed argv `PYTEST = (".venv/bin/python3", "-m", "pytest", "-q", "-n", "auto")` (`scripts/stage2.py:4829`), bounded by `TOOL_SECONDS = 5 * 60` (`scripts/stage2.py:4915`); a red cheap command ends the attempt before `make verify`.

`selected_tests` (`scripts/stage2.py:6655`) builds the pytest targets from three sources: new-or-changed test functions in changed `tests/**/test_*.py` files (a new file whole, `_changed_test_ids` at `scripts/stage2.py:6639`), **the accepted plan's ledger test refs in both forms — written and `not yet written` — with no existence check** (`targets.update(_ledger_test_refs(plan))`, `scripts/stage2.py:6678`), and, on a retry, the failed ids of the attempt before. The retry ids **are** pre-checked against the tree: a failed id whose test no longer stands is dropped (`_top_level_names` + `_id_stands`, `scripts/stage2.py:6610-6636`; pinned by tests for rows L1-12, L5-2, F6-2, F6-3 in `tests/test_stage2_fail_fast.py:488,554,674,694`). Ledger ids deliberately get **no** such pre-check: a ledger test that the tree lacks stays a target, so that pytest itself names the missing id — "pytest then fails the attempt with the missing id named, which is the attempt's own gap" (`selected_tests` docstring, `scripts/stage2.py:6664-6665`; pinned by `test_a_ledger_test_missing_from_a_new_file_is_still_selected`, row L3-1, `tests/test_stage2_fail_fast.py:538`, which asserts the missing id remains in the pytest argv). The repository records the cost of that choice: a stale id makes pytest refuse the **whole** cheap run with `not found` before any test runs (row F6-2 wording, `tests/test_stage2_fail_fast.py:674-676`; the same protection for retry ids exists precisely because pytest refuses the run on an id it no longer collects — comments at `scripts/stage2.py:6684-6691`). When the target set is empty, the pytest step is skipped entirely (`cheap_checks`, `scripts/stage2.py:6743-6744`).

Two prompt constants carry the ledger ids to the model as a must-run list: `must_run_refs` (`scripts/stage2.py:6770`) renders them from the **accepted plan's snapshot bytes**, and `MUST_RUN_DELEGATED` / `MUST_RUN_COMMANDS` (`scripts/stage2.py:6786-6812`) are inserted into the implement prompt (~`scripts/stage2.py:9098-9101`) and the repair prompt (~`scripts/stage2.py:10716-10719`). `MUST_RUN_DELEGATED` tells the model: "a missing ledger test fails the attempt before post-run verification."

The **ledger clearing** is separate and runs *after* the cheap checks: `clear_written` (`scripts/check_criterion_ledger.py:198`) removes a `not yet written` marker when the named test exists, and the runner captures the exact rewrites in `capture_ledger_clearing` / `LedgerClearing` (`scripts/stage2.py:5766-5828`) so the work check can discount them. The gate itself does no clearing ("its ledger clearing is a runner function, not the gate", `plans/changes/verify-cheap-before-admission/seconds-gate-audit.md`, row `criterion-ledger`).

This change is a child of the verify-speed epic: bead `coding-harness-bxxt` is "Verify speed and machine load" (`docs/journal/handover/2026-11-02-five-lane-night.md`, lane table; `docs/journal/handover/2026-11-02-tracker-cleanup-and-evaluations.md`, P2 row 8). Sibling children reached in the tree: bxxt.1 `verify-cheap-first` ("planted cheap failures stop before pytest", archived plan), bxxt.2 verify-result-reuse, bxxt.3 verify-tmp-cleanup, bxxt.5 midnight-stamp-test, bxxt.6 `verify-cheap-before-admission` (cheap gates outside the admission, live), bxxt.7 `slip-counter` (merged as PR #421). bxxt.9 is this change, opened 2026-11-20 (commit `87eefee8`, `plans/INDEX.md` row `changes/ledger-ids-before-pytest/research.md`). The nearest measured pytest-cost fact in the tree: the **targeted** pytest step alone measured 8.5–10.5 minutes on 2026-11-12/13, past the old tool limit (`coding-harness-dq4u` note at `scripts/stage2.py:4915-4918`); no measurement of the cheap selected pytest startup cost exists in the tree (not found, not measured — different statements: the second holds).

## Where it lives

- Selection: `scripts/stage2.py` — `selected_tests` (`:6655`), `_ledger_test_refs` (`:6578`), `_changed_test_ids` (`:6639`), `_top_level_names`/`_id_stands` (`:6610`, `:6630`), `failed_test_ids`/`FAILED_LINE` (`:6563`, `:6560`), `cheap_checks` (`:6708`), `PYTEST` (`:4829`), `_cheap_evidence` with `TAIL_LINES = 80` / `STDERR_LINES = 40` (`:6494`, `:6035-6041`).
- Preparation order: `verify_attempt.prepare()` (`scripts/stage2.py:7493`), `_targeted_body` (`:7302`), `full_verify` (`:7255`).
- Ledger clearing and its discount: `check_criterion_ledger.clear_written` (`scripts/check_criterion_ledger.py:198`), `LedgerClearing`/`capture_ledger_clearing`/`_undo_ledger_clearing` (`scripts/stage2.py:5766-5940`).
- Prompts: `must_run_refs`, `MUST_RUN_DELEGATED`, `MUST_RUN_COMMANDS` (`scripts/stage2.py:6770-6812`); insertion at the implement and repair prompt builds (`~:9100`, `~:10718`).
- Pinned behaviors: `tests/test_stage2_fail_fast.py` — Ledger 3 argv assertion (`:120`), L3-1 (`:538`), L1-12 (`:488`), L5-2 (`:554`), L6-1 (`:618`), L7-2 (`:640`), F6-2 (`:674`), F6-3 (`:694`), L4-3/L5-1/L8-1 (`:657`); prompts pinned by `test_prompts_require_ledger_tests_with_file_only_delegation` (Ledger 7, `:293`).
- Origin of the current semantics: the archived change `plans/changes/archive/2026-11-06-fail-fast-attempts/spec.md`, term "Selected tests" (amended 2026-10-28, `decisions.md#Q-3`), bead `coding-harness-5tyh`; the ledger gate itself: `plans/changes/archive/2026-11-06-criterion-test-ledger/` (ADR 0013); the marker clearing: `plans/changes/archive/2026-11-06-ledger-marker/` (bead `coding-harness-7g6h`).

## What is unclear about it

- The problem statement of bead `coding-harness-bxxt.9` could **not be read**: the tracker is the Dolt database under `.beads/` and its readers run through `scripts/bead_render.py`, which a read-only explorer cannot run; no rendered copy is committed (house rules). The change title, the epic, and the code positions above are the only in-tree signals of intent.
- "Ledger ids before pytest" has two compatible readings in the code: (a) the ledger ids are the one target group handed to pytest **without** a pre-launch existence check (retry ids have one; L3-1 pins that the missing id must stay a target so pytest names it), and (b) it could concern the *order* of ledger handling relative to the cheap pytest. Which one the bead means is an interview question, not a fact.
- The current behavior wastes one pytest process (with `-n auto` worker startup) whenever a ledger id does not stand, because pytest errors at collection before running any selected test; no measurement of that startup cost exists in the repository (not found in tree).
- Whether a runner-side pre-check may keep the L3-1 contract ("pytest names the missing id") by producing the missing-id diagnostic itself, or must change that contract, is undecided; the L3-1 test and the `selected_tests` docstring pin the current wording.
- Whether `not yet written` rows and written rows should be treated differently in any pre-check is not stated anywhere in the tree; `must_run_refs` lists them as-is and `MUST_RUN_DELEGATED` says the attempt must write them.

## Which files a change would have to touch

- `scripts/stage2.py` — `selected_tests` and `_ledger_test_refs` (any pre-check or reordering), `cheap_checks` (diagnostic path before the pytest launch), possibly `MUST_RUN_DELEGATED`/`MUST_RUN_COMMANDS` and the two prompt insertion sites if the must-run wording changes; the `capture_ledger_clearing` blocks only if preparation order changes.
- `tests/test_stage2_fail_fast.py` — the argv-pinning Ledger 3 test, the L3-1 test, and the retry-id tests around them; red-first for every changed behavior is the house rule.
- `plans/changes/ledger-ids-before-pytest/spec.md` and `plan.md` — to be written; the frontmatter provenance note in the current `research.md` skeleton applies to whoever fills it.
- `docs/WORKFLOW.md` (§ around line 1119-1175, runner ledger clearing and must-runs) — only if semantics or wording change.
- `scripts/check_criterion_ledger.py` — not expected to change: the entry forms already cover both test forms, and the gate does no clearing (`seconds-gate-audit.md`, row `criterion-ledger`).

## Research questions (for the interview, gate `research-handoff`)

1. What exactly does bead `coding-harness-bxxt.9` state as the problem and appetite (unread, tracker-only)?
2. Should the runner detect ledger ids that do not stand **before** launching pytest, reporting the missing ledger test as the attempt's own bounded diagnostic — and does that replace or preserve the L3-1 contract that pytest names the missing id?
3. Should written ledger rows and `not yet written` rows be distinguished in such a pre-check?
4. Is a measurement of the wasted cheap-pytest startup wanted as evidence (red-first test, or a recorded timing)?

## Neighbours (for the `neighbours:` header)

`plans/changes/verify-cheap-before-admission/spec.md` (bxxt.6, moved the cheap checks outside the admission) · `plans/changes/slip-counter/spec.md` (bxxt.7) · `plans/changes/swarm-test-speed/spec.md` · `plans/changes/review-loop-deep-a/spec.md` · `plans/changes/stage2-session/spec.md` · `plans/changes/archive/2026-11-06-fail-fast-attempts/` (spec + decisions Q-3: the selected-tests semantics) · `plans/changes/archive/2026-11-06-criterion-test-ledger/` (ADR 0013) · `plans/changes/archive/2026-11-06-ledger-marker/` (the runner's marker clearing) · `plans/changes/archive/2026-11-16-verify-cheap-first/` (cheap failures stop before pytest) · `plans/changes/archive/2026-11-16-verify-tmp-cleanup/` (bxxt.3).
