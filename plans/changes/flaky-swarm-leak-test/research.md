---
title: "Research — flaky-swarm-leak-test"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-yb1l
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# flaky swarm leak test — Research

Phase 1 exploration follows; the repository inspection addendum below resolves
the append inventory without changing the maintainer's recorded answers.

Stage-2 call, 2026-11-13: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1042 files, 4091 commits, 12 rules.

## Runner exploration — 2026-11-13

The exploration is complete. Here is the research, ready to append to `plans/changes/flaky-swarm-leak-test/research.md`.

---

## Suggested header addition

```
neighbours:
  - plans/changes/swarm-test-speed/spec.md          (active, bounded, bead coding-harness-dca4 — same test suite; its protected areas name the same three scripts)
  - plans/changes/archive/2026-11-06-research-swarm/ (spec/plan/findings — introduced the flaky test as F-37, criterion 56; documents two sibling load flakes)
  - plans/changes/archive/2026-11-06-swarm-time-limits/ (dispatcher time limits, same subsystem)
  - plans/changes/raising-fault-test/               (planted-fault doctrine that governs how a repair to this test must be written)
```

## What exists today

**The subject of this change is one named flaky test.** `tests/test_stage2_swarm.py::test_a_refused_run_is_printed_before_any_model_call` (`tests/test_stage2_swarm.py:1467`) failed twice on main's push CI with `assert 2 == 0`: after #369 (run 43062892770, 2026-11-11 16:54 UTC) and after #367 (run 42914422313), green in between — as recorded in the night handover `docs/journal/handover/2026-11-12-night-ten-lanes.md` ("Validation" section), which also raised the bead coding-harness-yb1l to P1 ("the main-CI flake"). The bead was opened on 2026-10-29 as "a flaky swarm test; a CI rerun passed" (`docs/journal/handover/2026-10-29-three-lane-night.md`, "New tonight"), and a duplicate flake bead coding-harness-9pib was folded into it on the night of 2026-11-12 (same handover, "Tracker, carried out"). I could not read the bead records themselves (the Dolt tracker is not readable with this phase's tools) nor the GitHub run logs; both facts rest on the handover files.

**What the test does.** It plants the marker `LEAKMARK-123456` (constant `LEAK`, `tests/test_stage2_swarm.py:46`) into the working-tree copy of `research.md` and runs a swarm explore once, expecting exit 2 — the leak check refuses because the marker stands in an uncommitted edit (denylist rule `planted = LEAKMARK-[0-9]{6}`, constant `DENYLIST`, `tests/test_stage2_swarm.py:47`, env `LEAKCHECK_DENYLIST`, line 495). It then restores the seed `research.md`, deletes the stand-in call log, installs a `print` spy on `stage2_research_run` and runs the swarm a second time, expecting exit 0 (`tests/test_stage2_swarm.py:1470-1483`). The CI failure message `assert 2 == 0` is the second assertion: the second run exited 2.

**Exit 2 means a security refusal, and any gate exception is one.** In the dispatcher, a slot whose `gate()` raises any exception is converted fail-closed into a refused slot (`scripts/stage2_research_dispatch.py:223-226`, comment "fail closed: an unreadable gate is a refusal"); a refused slot sets the `security` event and stops the stage (`scripts/stage2_research_dispatch.py:227-231`), and `security` makes the stage exit code 2 (`scripts/stage2_research_dispatch.py:375-376`). The swarm runner turns that into `Stop("a declaration or leak check refused a call; every queued call was cancelled", 2)` (`scripts/stage2_research_run.py:899-900`). So run 2's exit 2 does not require a real leak — any exception inside `gate()` suffices.

**The gate's fallible step in this test is the spied print.** `gate()` calls `print(result.verdict.render())` after every slot's leak check (`scripts/stage2_research_run.py:504`). Under the spy, each such print first evaluates `len(sworld.calls())` (`tests/test_stage2_swarm.py:1479`), and `SwarmWorld.calls()` reads the stand-in log `calls.jsonl` from disk and `json.loads` every line (`tests/test_stage2_swarm.py:371-374`).

**The log is appended concurrently, without locking.** The stand-in script (`STAND_IN`, `tests/test_stage2_swarm.py:187-353`) appends one JSON record per call with a plain buffered text-mode write (`log.open("a")` + `handle.write(json.dumps(record) + "\\n")`, `tests/test_stage2_swarm.py:270-271`). Each record carries the full prompt, the full environment and the stdin text (fields `prompt`, `env`, `stdin`, `tests/test_stage2_swarm.py:245-269`), so lines are many kilobytes and a buffered append is not a single atomic write. Meanwhile the dispatcher runs up to `PER_PROVIDER_LIMIT = 4` worker threads per provider (`scripts/stage2_research_dispatch.py:23, 331-336`): the gates of queued slots (under `gate_lock`) overlap in time with the stand-in processes of already launched slots appending to the same file. The finder trio and most seats ride provider "go" (fixture seats `REPOSITORY_SEATS`/`ONLINE_SEATS`, `tests/test_stage2_swarm.py:76-85`; provider assignment `scripts/stage2_research_run.py:870`), so the overlap starts in the very first stage.

**The resulting chain — stated as a mechanism, not as a proven reproduction.** A stand-in appending while a gate's spy reads can leave a torn last line; `json.loads` raises `JSONDecodeError`; the exception escapes the spy into `gate()`; the dispatcher's fail-closed rule refuses the slot; the stage exits 2. No reproduction was run in this phase (read-only). This is the only nondeterministic exit-2 source found on the spied path; the remaining gate inputs of run 2 are deterministic (below).

**The same torn-read hazard has a second symptom that does not match the CI signature.** The stand-in itself reads the whole log at start (`previous = [json.loads(line) …]`, `tests/test_stage2_swarm.py:203`); a torn line there crashes the stand-in, whose exit code makes the slot outcome "failed" and the stage exit 1 — visible as a different failure than `assert 2 == 0`.

**Two further exit-2 paths under load, unquantified.** `leakcheck._git` catches `OSError` from spawning git and returns a refusal verdict ("git cannot be started", `scripts/leakcheck.py:252-253`), which blocks the gate → exit 2; and the dispatcher's final guard marks a slot whose worker died as failed and sets `security` (`scripts/stage2_research_dispatch.py:352-357`). Whether either has ever fired here is unknown.

**Ruled out (checked, not there).** The terms path cannot refuse this fixture: the fixture seats get synthetic records from `admissible_terms` with `valid_until: "2099-01-01"` (`tests/terms_fixtures.py:33-41`) and `gelesen: "2026-10-25"` overridden per seat (`tests/test_stage2_swarm.py:444-450`), and the production rule `terms_problem` checks only structure plus `valid_until < terms_today()` — it has no age rule on `gelesen` (`scripts/stage2.py:1656-1686`). The leak scan of run 2 has clean inputs: the marker exists only in run 1's uncommitted working-tree edit and is restored before run 2; it is never committed (`w.commit()` runs only in the fixture, `tests/test_stage2_swarm.py:504`), and the leak check's scanned set — change-folder files, tracked plus untracked files, `git diff --cached`, `git log --branches --remotes --cc -p`, prompt texts (`scripts/leakcheck.py:311-419`) — therefore holds no marker in run 2. The research store lives outside the scanned root (`research_dir` under `XDG_STATE_HOME`, `scripts/stage2_research_store.py:59-68`; placement refused inside git-visible directories, `scripts/stage2_research_store.py:152-159`).

**The suite has a documented history of load-timing flakes, with two precedent repairs.** The research-swarm plan's round 6 records, next to F-37 itself, two flaky tests repaired by widening margins or replacing timers with a file handshake: `test_catalog_shared_deadline_keeps_asymmetric_failure_rules` (0.5 s margin under parallel load → 3 s delay, 5 s deadline) and `test_terminal_record_survives_sigkill_after_the_outcome` (timer → waits for a file the test writes) (`plans/changes/archive/2026-11-06-research-swarm/plan.md:2322-2323`). The whole suite runs under pytest-xdist, `python3 -m pytest tests/ -q -n auto` (`Makefile:22`), and the swarm suite dominates its cost: 35 of the 60 slowest calls, 438 s, in `tests/test_stage2_swarm.py` (measurement of 2026-11-12 01:08–01:34 UTC, `docs/journal/handover/2026-11-12-night-ten-lanes.md`, "Validation"). In that measurement the full suite was green except one unrelated `test_machine_facts` failure — so the flake did not fire on 2026-11-12 locally.

**Doctrine constraints a repair sits under.** Every new test names its fault in the docstring ("Planted fault: …") and a test that has never been red measures nothing (`docs/testing.md:45-46`); this test carries that form (`tests/test_stage2_swarm.py:1468-1469`, "Criterion 56 (phase-6 F-37). Planted fault: …"). The test itself was introduced red-first in the research-swarm change (`plans/changes/archive/2026-11-06-research-swarm/plan.md:2321`).

## Where it lives

- Test and fixture: `tests/test_stage2_swarm.py` — test `test_a_refused_run_is_printed_before_any_model_call` (line 1467), spy (1476-1486), `SwarmWorld.calls` (371-374), `SwarmWorld` fixture and env (`LEAKCHECK_DENYLIST`, narrowed `PATH`, `CC_SECRETS`, 420-514), stand-in template `STAND_IN` (187-353; append 270-271, pre-read 203), markers `OKEY`/`GKEY`/`LEAK`/`DENYLIST` (44-47), `manifest_of` (1347-1350, reads the manifest block appended to `research.md`).
- Production refusal path: `scripts/stage2_research_dispatch.py` — gate exception → refusal (223-231), security → exit 2 (375-376), final guard (352-357), per-provider concurrency (23, 331-336).
- Production gate: `scripts/stage2_research_run.py` — gate's leak check and print (500-517), refused-run notice before any model call (402-405, the behaviour under test), stage Stop with code 2 (899-900), run end and exit codes (1438-1497).
- Leak check: `scripts/leakcheck.py` — scanned set (291-419), git helper with OSError → refusal (244-256).
- Terms: `scripts/stage2.py` `terms_problem` (1656-1686); fixture builder `tests/terms_fixtures.py` (17-41).
- Evidence trail: `docs/journal/handover/2026-11-12-night-ten-lanes.md` and `docs/journal/handover/2026-10-29-three-lane-night.md`; `plans/changes/archive/2026-11-06-research-swarm/plan.md` (round 6).

## What is unclear about it

- No reproduction exists in the repository: the torn-read mechanism is inferred from the code, not demonstrated; the actual stderr/stdout of CI runs 42914422313 and 43062892770 (which would name the refused slot and its `{"error": "JSONDecodeError: …"}` gate record) was not read — it lives in GitHub, outside this phase's reach. [GAP]
- Whether the CI failures show the `JSONDecodeError`-in-spy path or one of the other exit-2 paths (`_git` spawn failure, lost worker) is open; the refusal record of the failing slot would tell them apart.
- The bead records coding-harness-yb1l and -9pib (dates of earlier occurrences, whether the 2026-10-29 flake was this same test) sit in the Dolt tracker and were not read.
- The intended split of responsibility — is a test-fixture race (unlocked log append, spied disk read) in scope for a production-script change, or must the production fail-closed rule stay untouched and only the fixture gain synchronisation — is a design question no artifact answers today. The swarm-test-speed spec protects exactly these scripts: `scripts/stage2_research_run.py`, `scripts/stage2_research_dispatch.py`, `scripts/leakcheck.py` ("the call-boundary and scan behaviour stays intact", `plans/changes/swarm-test-speed/spec.md:118-119`).
- How often the flake fires locally is unmeasured: the 2026-11-12 full run passed; no repetition protocol for this test exists in the tree (the research-swarm precedents used "three times in a row alone", `plans/changes/archive/2026-11-06-research-swarm/plan.md:2311`).

## Which files a change would have to touch

- `tests/test_stage2_swarm.py` — the flaky test, the spy, `SwarmWorld.calls`, and the `STAND_IN` template (its unlocked append at 270-271 and its own pre-read at 203 are the two concurrent readers/writers of `calls.jsonl`).
- `scripts/stage2_research_dispatch.py` and `scripts/stage2_research_run.py` — only if the production side of the refusal rule or the gate's print call site were to move; both files are named protected areas of the active swarm-test-speed change.
- No change to `scripts/leakcheck.py`, `scripts/stage2.py` or `tests/terms_fixtures.py` is implied by any fact found; those paths were ruled out above.

## Draft inspection addendum — 2026-11-13

At `3950c853`, the 17 append-mode opens counted in the interview comprise:

| File | Data appends | Lock-only opens |
|---|---|---|
| `tests/test_stage2.py` | lines 190, 196, 242, 298, 319 | 137 (`calls.lock` acquisition), 484 (`holds_record_lock`, a production-lock probe) |
| `tests/test_stage2_swarm.py` | lines 206, 270, 275, 282 | none |
| `tests/test_pi_install.py` | lines 101, 158, 183 | none |
| `tests/test_stage2_session.py` | lines 82, 87 | none |
| `tests/test_stage2_research_availability.py` | line 72 | none |

Thus 15 sites append data; three already take the local `locked(False)`
lock in `test_stage2.py`. The two lock-only opens do not append log records.
The scenario-driven arbitrary-text appends in stage2 and swarm are included;
they must preserve their exact text. Top-level document mutations elsewhere
in `test_stage2.py` are not concurrent stand-in logs. This is a repository
fact resolving an inventory gap, not a replacement interview answer.

Readers also require migration: `World.calls`, `World.script`, `World.versions`,
`SwarmWorld.calls`, the session fixture's `World.calls`, the Pi fixture's three log readers,
the stand-ins' startup reads, and direct reads of these logs in the five files.
The existing `test_a_stand_in_contacts_nothing` parses the rendered stand-in's
imports; a shared helper must keep that transitive standard-library-only
boundary. Embedded source is feasible without changing the runner's scrubbed
environment or exposing helper files inside its scanned fixture repository.

The torn-read explanation remains a hypothesis: this draft ran no reproduction
and read no CI logs. The interview answers settle the repair boundary and the
guard; no remaining intent decision is needed. No complete `research-swarm/v2`
record is present. `templates/plan.md` and
`scripts/validate_change_artefacts.py` do not exist at this commit; the plan uses
the phase-3 prompt's form and the available individual gates.
