---
title: "Research — midnight-stamp-test"
status: draft
implementation_status: none
date: 2026-11-10
last_reviewed: 2026-11-10
updated: 2026-11-10
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.5
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3-flash, version: "2026-11-10"}
review: {status: pending, approved_by: null, approved_at: null}
class: bounded
tags: [research]
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
---

# midnight stamp test — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). The
intent below was written by the orchestrator (Claude Code) before the first
call; the runner exploration (GLM 5.3 Flash) follows it unchanged.

## Intent of the bead (written by the orchestrator before the first call)

Bead coding-harness-bxxt.5, class bounded, a bug.
`tests/test_stage2.py::test_every_write_to_findings_keeps_its_updated_stamp_current`
takes today's date once and compares it with the stamp the runner writes
later. A full check that crosses local midnight fails on it: on 2026-11-09 at
23:22 UTC (00:22 local time) a full check ended with 1 failed and 5349
passed, on `assert date(2026, 11, 10) == date(2026, 11, 9)`. One lost run
costs about 25 minutes of the one verify slot. Done when the test fixes the
clock it compares against, and a search has shown whether sibling tests take
the date the same way.

Questions for the exploration: how this test and the production code it
exercises read the date (`date.today()`, `datetime.now()`, a helper, a
timezone); which other tests under `tests/` compare a date taken in the test
with a date written by code under test, by file and test name; whether the
repository already has a way to fix the clock in tests (a fixture, a
monkeypatched helper, an environment variable) that such tests should use.

Stage-2 call, 2026-11-10: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1012 files, 3897 commits, 12 rules.

## Runner exploration — 2026-11-10

The exploration is complete. Here is the research, ready to append to `plans/changes/midnight-stamp-test/research.md`:

---

## What exists today

**The failing test.** `tests/test_stage2.py::test_every_write_to_findings_keeps_its_updated_stamp_current` (`tests/test_stage2.py:1733`, docstring "Repair round 1, F-7") reads the calendar date exactly once — `today = dt.date.today()` at `tests/test_stage2.py:1735` (`tests/test_stage2.py` imports `datetime as dt` at line 21). It then drives three runner verbs in sequence through the in-process fixture: `world.run("spec-review")` (line 1746), `world.run("review-loop")` (line 1750), `world.run("review")` (line 1756), where `World.run` (`tests/test_stage2.py:388`) calls `stage2.main()` directly. Each verb stamps `findings.md` with a freshly read date. Three assertions compare the written stamp against the captured variable (`updated_of(world.findings) == today`, lines 1747, 1751, 1757; `updated_of` at line 1729 wraps the pure parser `check_frontmatter_current.read_updated`), and two rewrites at lines 1749 and 1754 do `world.text().replace(f"updated: {today}", "updated: 2026-09-29", 1)` — a replace that silently no-ops when the stamp's day has moved on. The recorded failure `assert date(2026, 11, 10) == date(2026, 11, 9)` (bead intent, and the run of 2026-11-09 23:22 UTC) is the equality-assert shape: the test held 2026-11-09, the runner wrote 2026-11-10 after local midnight. The window is the whole test — three scripted runner verbs — which is why this test crosses midnight in practice while the pattern elsewhere stays unobserved.

**The production stamp path.** The stamp functions themselves take the date as a parameter and never read a clock: `check_frontmatter_current.stamped(text, today)` (`scripts/check_frontmatter_current.py:226`) and `check_frontmatter_current.stamp(path, today)` (`scripts/check_frontmatter_current.py:250`). The clock enters through the callers in `scripts/stage2.py`, which reads it inline at every stamp site, all as `dt.date.today()` under `import datetime as dt` (`scripts/stage2.py:157`): `append()` at line 1199 (the atomic append-and-stamp for findings call lines and audit lines), `stamp_updated()` at line 1234, the `review_audit_only` re-stamp comparison at line 3202, and `prepare_derived` at line 5387 (stamps every changed held document on the implement/verify path). `stamp_updated` is called from `fill_marks` (`scripts/stage2.py:3365`, call at 3378), `release` (3988 → 4014), `insert_before_time` (4928 → 4936 and 4941), `mark_repaired_findings` (7498 → 7524), `persist_time_entry` (8283 → 8324 and 8343) and `run_attempts` (8354 → 9010). A separate helper `stage2.today()` (`scripts/stage2.py:664`) reads `dt.date.today()` again for the `Stage-2 call, <date>:` audit text. The `world` fixture (`tests/test_stage2.py:650`) seeds the demo change with `provenance.yaml` holding `plans/` as `frontmatter: required` (line 671), so every one of these writes actually stamps. Outside the runner, the module's own CLI is the only other clock read in that file: `main()` passes `date.today(), datetime.now(UTC).date()` (`scripts/check_frontmatter_current.py:315`); the module binds `from datetime import … date` at import time (line 30). The repository's wider production convention is boundary-read, parameter-injected dates: `check_frontmatter_current.run(root, do_stamp, today, utc_today)` (`scripts/check_frontmatter_current.py:272`), `time_log(… today=today or date.today())` (`scripts/harness.py:490-501`), `today = args.today or date.today()` (`scripts/check_research_currency.py:326`).

**One production site shares the hazard's shape.** `review_audit_only` (`scripts/stage2.py:3184-3205`) validates an append by re-stamping the before-bytes with `dt.date.today()` at check time (line 3202) and comparing against the after-bytes. An append stamped immediately before local midnight and checked immediately after would mismatch and be refused as not audit-only. The window is seconds within one verb, not minutes; no incident is recorded for it. The only occurrence of this test's id in an archived findings list is `plans/changes/archive/2026-11-06-loop-until-clean/findings.md:112`, where dozens of unrelated tests failed in the same run — that record does not date the midnight cause to that incident.

**Sibling tests that compare a test-taken date with a runner-written stamp** (the bead's second question), by file and test name:

- `tests/test_stage2.py::test_first_implement_refreshes_derived_files_without_a_model_repair` (line 1921) and `::test_each_retry_prepares_before_verify_and_keeps_real_failure_diagnostics` (line 1958), through the helper `checking_derived_make` (lines 1906-1918): the planted make stand-in is a *subprocess* whose inline script asserts `"updated: " + datetime.date.today().isoformat()` in `plan.md` (line 1913) that `prepare_derived` stamped in-process moments earlier. Window: the gap between stamp write and subprocess read. An in-process clock patch cannot reach the subprocess, and a frozen constant date would newly clash with the subprocess's live date.
- `tests/test_stage2.py::test_preparation_stamps_only_changed_held_documents` (lines 1931-1955): `stage2.verify_attempt(...)` stamps `held`, then the assert builds `f"updated: {dt.date.today()}"` evaluated after the call (line 1950). Window: one verify_attempt with a planted make.
- `tests/test_stage2.py::test_filling_the_marks_keeps_the_updated_stamp_current` (lines 5766-5776): direct `stage2.fill_marks(...)`, then `updated_of(...) == dt.date.today()` evaluated after (line 5775). Window: one function call.
- `tests/test_stage2.py::test_runner_detaches_matching_hardlinked_plan_before_stamp` (lines 11856-11887, parametrized `retry` False/True): `stage2.persist_time_entry(...)` stamps the plan, then `f"updated: {dt.date.today().isoformat()}"` is asserted (line 11884). Window: one function call.
- `tests/test_stage2.py::test_the_release_reconcile_refreshes_the_findings_date` (lines 21246-21259): `world.run("release-loop")` stamps, then `f"updated: {stage2.dt.date.today().isoformat()}\n"` (line 21256). Window: one scripted verb.
- `tests/test_stage2.py::test_review_accepts_runner_audit_date_stamp` (lines 24730-24764, five cases): takes `yesterday` from `dt.date.today()` (line 24736), commits it, then `stage2.append(...)` stamps with its own write-time read (line 24744); the asserts at 24750 and 24752 re-read via `stage2.today()` at assert time; the accepted cases then run `world.run("review")` (line 24762), whose acceptance path is `review_audit_only` with its own now-based re-stamp (scripts/stage2.py:3202). Two windows: append→assert and append→review-check.
- `tests/test_workflow_entry.py::test_new_change_creates_the_folder_and_a_current_index` (lines 87-95): `new_change.main` writes the scaffold's `updated:` (`scripts/new_change.py:254`, `heute = dt.date.today().isoformat()`); the assert at line 95 reads `date.today()` after the write. Window: one file write.

**Dates taken in tests that are not this class** (checked so the sibling list stays honest): `tests/test_archive_closed_changes.py::test_index_matches_registry_after_archive` (lines 425-453) builds a relative fixture date `(dt.date.today() - dt.timedelta(days=2))` (line 432) for a staleness measure whose threshold is ~90 days (`scripts/plans_registry.py` computes the age at lines 87-90; the in-test comment at lines 429-431 explains the choice) — midnight moves the age 2→3, far below the threshold. `tests/test_feedback_channel.py:502` compares configured skip deadlines against `date.today()` with `<=` — midnight only tightens it. `tests/test_frontmatter_current.py` injects constant dates (`TODAY` at line 107; `cfc.stamp(path, TODAY)` at lines 383, 429-431, 480). `tests/test_harness_decide_adr.py:330` (`today=TODAY`) and `tests/test_run_report.py:792` (`today=datetime(2026, 10, 31).date()`) inject fixed parameters. None of these compares a captured date against a later runner-written one.

**Clock-fixing devices the repository already has** (the bead's third question): three, none of which the stamp path currently uses. First, named seams in `scripts/stage2.py` with pinning precedent: `terms_today()` (lines 1630-1637, docstring "a seam for tests", judged in UTC), pinned via `monkeypatch.setattr(stage2, "terms_today", lambda: dt.date(…))` in `tests/test_stage2_terms_expiry.py` (lines 115, 138, 174); `utc_now()` and `monotonic_now()` (lines 4882-4889, both docstringed "a seam for tests"), pinned by the `FakeClock` helper (`tests/test_stage2.py:10514-10537`, used at lines 10545 through 12093) and by direct `monkeypatch.setattr(stage2.time, "monotonic", …)` (lines 8000, 8086). Second, module-attribute patching: `monkeypatch.setattr(stage2.dt, "date", LocalDateAhead)` and `…stage2.dt, "datetime", FrozenDateTime` (`tests/test_stage2_terms_expiry.py:159-160`), after `monkeypatch.undo()` at line 158 with the comment "Lift the constant seam first, or the fakes below are never read and a local-date implementation would pass" (lines 156-157). Because `scripts/stage2.py:157` and `tests/test_stage2.py:21` are both `import datetime as dt`, both names resolve attributes on the same shared `datetime` module object at call time, so such a patch is visible to every `dt.date.today()` in the runner — including all four stamp sites — and to the test's own reads alike; it does not reach `check_frontmatter_current`'s import-bound `date` (line 30) or its CLI clock (line 315), which no test under `tests/` exercises. Third, `FakeClock` itself, scoped to the measured-span seams. Not there: no `tests/conftest.py` exists (Glob found none), `freeze_time`/`freezegun` appear nowhere under `tests/`, and no environment-variable clock override exists anywhere in `scripts/` (searched `environ` against `TODAY|DATE|CLOCK|NOW`). Not found, and not searched beyond the above: any convention statement about the stamp's timezone in `docs/WORKFLOW.md` — the gate's own docstring ties the reference date to the committer date "in the offset recorded in the commit" (`scripts/check_frontmatter_current.py:9-12`), and every stamp read in the path is local-zone (`dt.date.today()`); `terms_today` is the only UTC date in the runner.

## What is unclear

- Whether `checking_derived_make`'s subprocess assertion (`tests/test_stage2.py:1913`) can be covered by an in-process fix at all: it compares across a process boundary, and a pinned constant date would newly break it unless the pin carries the live date. The bead's intent ("a search has shown whether sibling tests take the date the same way") is answered with this list; what the fix does about the subprocess case is a decision, not stated anywhere in the repository.
- Whether the stamp date must stay local-zone or is allowed to be UTC: no production or doctrine text found that decides the zone for `updated:`; the only UTC-date statement found is terms expiry (`scripts/stage2.py:1630-1637`).
- Whether the `review_audit_only` now-based re-stamp (`scripts/stage2.py:3202`) counts as in scope: its window is seconds and no incident is recorded; it shares the shape, not the exposure.

## Which files a change would have to touch

The failing test and all six in-class siblings live in `tests/test_stage2.py` (lines 1733-1758, 1906-1918 with 1921 and 1958, 1950, 5775, 11884, 21256, 24736-24764); one sibling lives in `tests/test_workflow_entry.py` (line 95). The existing patch precedent for the whole `datetime` module lives in `tests/test_stage2_terms_expiry.py` (lines 146-162) and would be the place a shared helper is extracted from, if one is extracted. Production code (`scripts/stage2.py`, `scripts/check_frontmatter_current.py`) is untouched by the bead's stated done-condition — "the test fixes the clock it compares against" (bead intent, `plans/changes/midnight-stamp-test/research.md`); the four inline `dt.date.today()` stamp sites (1199, 1234, 3202, 5387) become relevant only if a named seam is chosen instead, which is a `[DECISION]` for the maintainer, not a fact this exploration states.

---

**Where we are / Next step / Needed from you** — per the phase gate `research-handoff`: the research answers all three questions from the bead's intent (how the test and the stamp path read the date; the sibling list by file and test name; the three existing clock-pinning devices). One open decision for the interview: whether the fix pins the clock test-side only (the bead's wording) or introduces a named seam in `scripts/stage2.py` like `terms_today`; the subprocess-based assertion at `tests/test_stage2.py:1913` needs a position either way.
