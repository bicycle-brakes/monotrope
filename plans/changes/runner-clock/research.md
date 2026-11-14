---
title: "Research — runner-clock"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-pph3
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-14", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# runner clock — Research

Stage-2 call, 2026-11-14: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1073 files, 4226 commits, 12 rules.

## Runner exploration — 2026-11-14

The exploration is done — everything below is repository fact with sources, ready to append to `plans/changes/runner-clock/research.md`.

---

## What exists today

**The runner's direct monotonic reads.** On this branch (`fix/runner-clock`), `scripts/stage2.py` calls `time.monotonic()` directly at six code sites: inside `remaining()` (`scripts/stage2.py:3100`, the round-budget helper that `launch()` consults at `scripts/stage2.py:1025`), inside `monotonic_now()` itself (`scripts/stage2.py:5361-5363`), and four times inside `_review_round()` (`scripts/stage2.py:10810`, `10822`, `10865`, `10888` — the round deadline and its three expiry re-checks). One docstring mention sits in `run_reviewer` (`scripts/stage2.py:3246`). No `time.time()`, `time.sleep()` or `time.perf_counter()` call exists in `scripts/stage2.py` (searched with pattern `time\.[a-z_]+\(` — only `monotonic` matched).

**A seam already exists but is bypassed.** `monotonic_now()` (`scripts/stage2.py:5361`) is documented as "a seam for tests", paired with `utc_now()` (`scripts/stage2.py:5356`). They are used by the attempt bookkeeping in `run_attempts` (`scripts/stage2.py:9353`, `9751`, `9879`) and `persist_time_entry` paths (`10255`, `10347`); the five other reads above do not go through them. Tests already patch both seams: the `FakeClock` class (`tests/test_stage2.py:11765-11788`, "readings that move only when a test moves them") monkeypatches `stage2.utc_now` and `stage2.monotonic_now`.

**The sibling modules already follow the choke-point pattern.** `scripts/verify_lock.py` — imported and run in-process by the runner (`scripts/stage2.py:205`) — has `_now()` and `_sleep()` ("the seam the tests inject fake time through" / "shorten through", `scripts/verify_lock.py:162-169`) and four direct reads in its signal-grace loop (`916-920`). `scripts/verify_duration.py` has `monotonic()` with the same seam docstring (`scripts/verify_duration.py:93-95`). Outside the runner family, `scripts/stage2_research_run.py` carries an injectable `CLOCK = time.monotonic` (`scripts/stage2_research_run.py:70`), `scripts/stage2_research_dispatch.py` takes a `clock: Callable[[], float] = time.monotonic` parameter (`:141`) and still sleeps/polls directly (`:300`, `:345`, `:347`); further direct reads live in `scripts/stage2_research_history.py:26`, `scripts/stage2_research_snapshot.py:36`, `scripts/research_capture.py:1111,1136`, `scripts/outcome_test.py:767-775`, `scripts/close_merged_beads.py:324-397`. Tests inject fakes through these seams today: `tests/test_verify_lock.py:382-383,522-541`, `tests/test_stage2_swarm.py:1831` (`CLOCK`), `tests/test_stage2_research_history.py:243`, `tests/test_close_merged_beads.py:748`.

**The two load-flaky tests.** `test_verification_admission_is_outside_execution_timeout` (`tests/test_stage2.py:2402-2433`, comment: "Criterion 4 of the machine lock") monkeypatches `VERIFY_SECONDS` to 2.0, starts a real admission holder (`_real_holder`, `tests/test_stage2.py:2365-2389` — a supervised `python -m scripts.verify_lock` child that really sleeps, default 30.0 s), waits a real second in its own body (`time.sleep(1.0)`, `:2419`) and runs a planted `make` stand-in that really sleeps 1.5 s (`:2416`). The second real-holder user is `test_local_checks_preserve_nested_admission` (`tests/test_stage2.py:2436-2480`, "Criterion 5 of the machine lock (the runner half)"). The planted stand-ins execute `time.sleep(step.get("sleep", 0))` in their own subprocess (`tests/test_stage2.py:304`; `pi_version_sleep`/`pi_refresh_sleep` at `:181`, `:206`), and the holder poll loop `_holder_acquired` reads `time.monotonic()` itself (`:2392-2399`). `launch()` bounds children through `subprocess.run` / `process.communicate(timeout=…)` (`scripts/stage2.py:1043`), whose waiting runs in the standard library.

**Recorded failure evidence.** The flaky test failed under load in an earlier review loop: `plans/changes/verify-cheap-first/findings.md:284-338` ("the admission wait consumed the step limit: … stopped by the runner's step limit after 0.0 minutes", pytest `-n auto`, xdist worker gw1, darwin, 21:51 min run); also `plans/changes/research-free-paid/findings.md:237-291` and `plans/changes/pi-no-compaction/findings.md:194`. `make verify` runs `python3 -m pytest tests/ -q -n auto` (`Makefile:22`), so the suite runs parallelised; a full run took 10–13 minutes with slot waits of 7–39 minutes that evening (`docs/journal/handover/2026-11-14-night-ten-lanes-parked.md`, "Not run after…").

**Existing source-guard precedent, no exemption list.** `test_stamp_tests_pin_the_date_they_compare` (`tests/test_stage2.py:1798-1829`) regex-extracts named function bodies from two test files and forbids `date.today(` — no exemption list, every named body must be found. This is the pattern of the completed change `midnight-stamp-test` (spec criterion 5, `plans/changes/midnight-stamp-test/spec.md:101-106`). It contrasts with the exemption-list guards that exist elsewhere: the shrink-only lists `OHNE_TEST`/`OHNE_MUTATIONSTEST` (`tests/test_ci.py:2912,3098`) and the leak check's `EXEMPT_DIRS` (`tests/test_leakcheck.py:442`).

**Limits the runner carries.** `REVIEWER_MINUTES = 45` (`scripts/stage2.py:275`), `VERIFY_SECONDS = 45 * 60` (`:4800`), `TARGETED_PYTEST_SECONDS = VERIFY_SECONDS` (`:4803`), applied at three launch sites (`:6953` `full_verify`, `:7205` draft documents, `:6923` targeted pytest), `GIT_SECONDS = 2 * 60` (`:4804`), `KILL_DRAIN_SECONDS = 5` (`:926`). `scripts/time_records.py` reads no clock at all — it parses and formats handed-in values (searched; only `parse_stamp`/`format_entry` string work).

## Where it lives

Runner clock reads: `scripts/stage2.py` (six sites above). Runner satellite seams: `scripts/verify_lock.py:162-169`, `scripts/verify_duration.py:93-95`. Flaky tests and their helpers: `tests/test_stage2.py:2365-2480`. Fake-clock precedent: `tests/test_stage2.py:11765-11788`. Source-guard precedent: `tests/test_stage2.py:1798-1829`. Failure records: `plans/changes/verify-cheap-first/findings.md:284`, `plans/changes/research-free-paid/findings.md:237`, `plans/changes/pi-no-compaction/findings.md:194`. Interview decision: `plans/changes/runner-clock/decisions.md` Q-1 (class bounded, bead coding-harness-pph3). The change folder rows already stand in `plans/INDEX.md:566-567`.

## What is unclear about it

1. **Site count.** The decision context says "7 call sites … on origin/main" (`plans/changes/runner-clock/decisions.md:33`); this branch shows six code sites plus one docstring mention. I did not diff against origin/main — the exact origin count is an open question, not a guess.
2. **The second test's name.** `test_before_admission_execution_budget_is_shared_and_wait_free` matches no test in `tests/` (searched by name fragment `wait_free`/`budget|admission|timeout` — not found). The nearest real candidates are the two `_real_holder` users, `tests/test_stage2.py:2402` and `:2436`; the "30-second limit" matches `_real_holder`'s default `seconds: float = 30.0` (`:2365`). Which test the answer named is unsettled.
3. **Scope of "the runner"** for the source test: `scripts/stage2.py` alone, or also `scripts/verify_lock.py` (run in-process by the runner, own seams) and the other `stage2_*`/`verify_*` scripts with their own direct reads? The decision says "one choke point for time in the runner" without naming files.
4. **Scope of "time read".** The decision names `time.monotonic, time.time, time.sleep, time.perf_counter`; `scripts/stage2.py` additionally reads the wall clock via `dt.date.today()` / `dt.datetime.now(dt.UTC)` at ten sites (`:675, :1209, :1578, :1981, :2785, :3627, :5177, :5358` inside `utc_now, :6029, :9275`). In or out of the guard?
5. **Fake clock versus real subprocess waits.** The flaky tests' waits live in child processes (planted stand-ins `tests/test_stage2.py:304`, holder child `:2382`) and in stdlib `communicate(timeout=…)` (`scripts/stage2.py:1043`); today's `FakeClock` only moves the runner's own seam reads. How an injected clock governs those real waits is stated as intent (`decisions.md:27`) but unresolved in the tree.
6. **"Every other runner test with small real-time limits."** The real-wait population beyond the two flaky tests includes `tests/test_stage2.py:6761` (`time.sleep(30)` child under a short launch timeout), `:22048/:22073` (`time.sleep(5)` in signal stand-ins), `:22166` (`time.sleep(2.5)` slow reviewer), `:24782-24796` (heartbeat child ≈3 s), poll loops at `:22016, :22035, :22055, :22080, :25156, :25231`. Which of these the change converts is unstated.
7. **Header gap.** The `research.md` skeleton carries no `neighbours:` key; the required header must be added by the runner (only the runner writes the file).

**Neighbours for the header:** `plans/changes/archive/2026-11-06-verify-machine-lock/spec.md` (archived — its criteria 4 and 5 are exactly the two flaky tests, plan card 4 names the test, `plan.md:114`) · `plans/changes/verify-step-limit/spec.md` (draft, `implementation_status: partial` — owns the 45-minute `VERIFY_SECONDS`; its criterion 4 is the admission-wait-exclusion property, its plan ledger maps card 4 to the flaky test, `plan.md:66`) · `plans/changes/midnight-stamp-test/spec.md` (draft, done — the pinned-clock-in-tests precedent and the guard test) · `plans/changes/time-records-data/spec.md` (draft — the shared time-record writer and the `utc_now`/`monotonic_now` seams; its spec guards monotonic-vs-wall arithmetic, `spec.md:69`) · `plans/specs/implementation-verification/spec.md` (living spec — "keep the existing limits", do not weaken `make verify`).

## Which files a change would have to touch

- `scripts/stage2.py` — route the five bypassing reads (`remaining`, `_review_round` ×4) through the existing `monotonic_now` seam or a replacement choke point; the wall-clock sites stay unless unclear-point 4 says otherwise.
- `tests/test_stage2.py` — the timing tests at `:2402` and `:2436`, the other real-wait tests per unclear-point 6, a new source guard test beside the precedent at `:1798`, and `FakeClock` (`:11765`) as the injection mechanism.
- No change required in `scripts/time_records.py` (clock-free today). Changes in `scripts/verify_lock.py` or the other scripts depend on unclear-point 3.
- Nothing in `plans/INDEX.md` — the folder rows already stand (`plans/INDEX.md:566-567`).
