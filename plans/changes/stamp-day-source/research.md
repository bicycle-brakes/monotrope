---
title: "Research — stamp-day-source"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5v6t
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-28", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# stamp day source — Research

## Topic (bead coding-harness-5v6t)

Class: bounded.

Measured 2026-11-09: the outcome-test round-5 repair committed 6bf5c6fc at 2026-11-09 01:30:27 +0100 with docs/WORKFLOW.md changed and its header still 'updated: 2026-11-08'. check_frontmatter_current.py takes 'the committer date (in the offset recorded in the commit) of the newest non-merge commit' (its docstring), i.e. 2026-11-09, so the gate went red; every later repair attempt of the change failed only on that gate (three attempts of F6-2..F6-4, about 3 h lost, attempt saved at refs/stage2/attempts/outcome-test/orchestrator-saved-20261109). The runner's stamp before its checkpoint evidently used a different day than the commit's recorded offset. Do: one day source for stamping and checking (the commit's own offset, or UTC on both sides), with a test that commits at 00:30 +0100.

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-28: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1325 files, 6161 commits, 12 rules.

## Runner exploration — 2026-11-28

The research for `stamp-day-source` is below, as prose ready to append to `plans/changes/stamp-day-source/research.md`. I used read-only tools only and changed no file.

## What exists today

**The check's day rule.** `scripts/check_frontmatter_current.py`, module docstring: a clean file's reference date is the committer date, in the offset recorded in the commit, of the newest non-merge commit that changed it. An untracked or modified file's reference date is "today". The module docstring also says that a shallow clone is refused, not guessed at. The history is read in one batched `git log` whose format string ends in `%cs` (`HISTORY_FORMAT`, `HISTORY_ARGS`). The day is then taken from `_History.dates` through `history_dates` and `reference_dates`. `%cs` is the committer's calendar date in the offset the commit records, so the check does not use UTC for committed files.

**The check's "today" inputs.** `findings(root, today, utc_today)` takes two dates. `today` is the reference for uncommitted files. `utc_today` is used only for the future bound: an `updated:` later than `utc_today + 1 day` is reported as `FUTURE`. `main()` passes `date.today()` (local) as `today` and `datetime.now(UTC).date()` as `utc_today`. So the check already uses two day sources in one run.

**The stamp's day rule.** `stamp(path, today)` and `stamped(text, today)` write `updated: <today.isoformat()>` by editing one line. The stamping callers pass `clock_now().local_date` (`scripts/stage2.py`, `prepare_derived` near line 8230, and `review_audit_only` near line 5000) or `dt.date.fromisoformat(today())` (`scripts/stage2.py`, near line 1734, where `today()` returns the local date string). The stamp helper `stamp_updated` (`scripts/stage2.py`, near line 1743) also uses `clock_now().local_date`. Every runner stamp therefore uses the local calendar date of the runner's process, read once in `clock_now()`.

**The runner's clock seam.** `scripts/stage2.py`, `ClockReading` and `clock_now()` (near line 760): one reading holds `monotonic`, `utc` (a `datetime` in UTC) and `local_date` (`dt.date.today()`). The docstring says stamps stay local dates, terms stay UTC dates, and durations stay monotonic differences.

**Existing test of the offset rule.** `tests/test_frontmatter_current.py::test_the_committers_own_offset_decides_the_day` commits `2026-09-20T23:30:00-05:00`, which is the 20th in the committer's offset and the 21st in UTC. It asserts that the 20th is the reference day, with `today` and `utc_today` both set to 2026-09-25. This test covers the check's use of the commit's offset. It does not cover a stamp taken on one side of midnight and a commit on the other.

**Prior midnight work.** `plans/changes/archive/2026-11-16-midnight-stamp-test/research.md` records a test in `tests/test_stage2.py` that takes `dt.date.today()` once and compares it with the stamp the runner writes later. It names a full check that ended at 00:22 local time on 2026-11-09 with one failure. The same research lists four sibling tests with the same shape: `test_preparation_stamps_only_changed_held_documents`, `test_filling_the_marks_keeps_the_updated_stamp_current`, `test_runner_detaches_matching_hardlinked_plan_before_stamp` and `test_the_release_reconcile_refreshes_the_findings_date`. That research also says no production or doctrine text found decides whether `updated:` uses the local or the UTC zone.

**The change's own record.** `plans/changes/stamp-day-source/research.md` cites the measurement from 2026-11-09. Commit `6bf5c6fc` at 01:30:27 +0100 changed `docs/WORKFLOW.md`, but its header still read `updated: 2026-11-08`. The gate then read the commit's day, 2026-11-09, as the reference, and failed. Three repair attempts (F6-2 to F6-4) failed only on that gate. `plans/changes/stamp-day-source/decisions.md` records the interview skip under the bounded standing grant, and says the source choice is a reversible `[DETAIL]` that the spec settles. The index row is `plans/INDEX.md`, line 776.

## Where it lives

- `scripts/check_frontmatter_current.py`: `reference_dates`, `findings`, `stamped`, `stamp`, `run`, `main`
- `scripts/stage2.py`: `ClockReading`, `clock_now`, `today`, `stamp_updated`, `prepare_derived`, `review_audit_only`, and the caller near line 1734
- `tests/test_frontmatter_current.py`: the offset test and the stamp tests
- `tests/test_stage2.py`: the sibling tests listed above, plus the midnight test from the archived change
- `plans/changes/archive/2026-11-16-midnight-stamp-test/`: prior research on the same day-boundary failure class

## What is unclear

- **The mechanism.** The read code shows that the runner stamps with its local date at the stamp's instant, and the check reads the commit's own date. These can differ when a stamp is written before midnight and the commit is made after it. The read code does not show whether the 2026-11-09 failure came from that gap or from another source. Checking that needs `git show 6bf5c6fc` (its committer line and offset) and the runner's stamp timestamp for that attempt. I could not run git in this phase.
- **Which zone the machine uses.** I did not read the machine's timezone setting. The 01:30 +0100 offset in the bead suggests Europe/Berlin, but I did not confirm it.
- **The sibling tests.** I read only their names and line ranges from the archived research, not their bodies. Whether each one reads `dt.date.today()` in a way that fails at midnight is not verified.
- **Whether `GIT_COMMITTER_DATE` is set by the runner.** I did not read the runner's commit path, so I cannot say whether the committed offset always equals the local offset.

## Which files a change would have to touch

- `scripts/check_frontmatter_current.py`: the day source of `reference_dates` and `findings`, and of `main`'s two arguments
- `scripts/stage2.py`: the stamp callers listed above, so that stamping and checking read the same day source
- `tests/test_frontmatter_current.py`: a test that commits at 00:30 +0100 and checks that the stamp and the check agree, as the bead asks
- `tests/test_stage2.py`: the sibling midnight tests, if the chosen source changes what they compare
