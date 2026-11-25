---
title: "Research — standin-call-counter"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.14
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-25", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
neighbours: []
---

# standin call counter — Research

## Topic (bead coding-harness-bxxt.14, copied by the orchestrator 2026-11-25)

Class: bounded.

Why: tests/test_stage2_swarm.py stand-in (297, 345) reads all records
through read_records (tests/atomic_test_log.py:106-125: flock plus
json.loads per line) only to count earlier calls with the same key; the log
grows with prompts, so cost grows quadratically per test. (The
test_stage2.py stand-in, 194-230, uses the records for step assignment, not
only counting.) What: a small per-key counter beside the log for the swarm
stand-in.

Checked 2026-11-24 at origin/main 18a13d3d by read-only subagents (session
claude-mp, night run 2026-11-24-a), from an external verify-speed analysis.



PARENT
↑ ○ coding-harness-bxxt: (EPIC) Verify speed and machine load P1

Stage-2 call, 2026-11-25: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu) · leak check clean over 1202 files, 5812 commits, 12 rules.

## Runner exploration — 2026-11-25

## What exists today

**The stand-in's read happens on every call, and only the swarm stand-in counts from it.** In the swarm stand-in template `STAND_IN` in `tests/test_stage2_swarm.py`, the module-level code does `previous = read_records(log)` (line 297) before anything else, with `log = here / "calls.jsonl"` (line 296). It then uses `previous` in exactly one place: `index = sum(1 for call in previous if call.get("key") == used)` (line 345), which selects the step for the call. The grep of the template body shows no other use of `previous`. This matches the bead's claim.

**Each record is the whole call, so the log grows with prompt size.** The record that the same template appends with `append_record(log, record)` (line 372) carries `stdin`, `system_prompt`, `prompt`, `env`, `home_listing` and `agent_settings` (record dict, lines 347–371). Every later call re-reads and `json.loads` all of those lines, so the read cost grows with the number of calls and with the size of each prompt.

**The helper's read is locked and whole-file.** `read_records` in `tests/atomic_test_log.py` (`read_records`, lines 106–125) opens the file, takes a shared `flock` through `_lock`, reads the full text, releases the lock, and returns `[json.loads(line) for line in text.splitlines()]`. A missing file returns `[]`. Nothing in it can be asked for a subset, a count or a tail.

**The append side is also whole-record.** `append_record` (lines 101–103) writes one JSON line under an exclusive lock, and `_declared` (lines 71–75) refuses any file name that is not in `STAND_IN_LOGS` (lines 44–51: `calls.jsonl`, `versions.jsonl`, `infrastructure.jsonl`, `local-pi.jsonl`, `path-pi.jsonl`, `npm-calls.jsonl`).

**The runtime guard covers only declared names.** `tests/stand_in_log_guard.py` refuses a raw `open`, `os.open` or `pathlib` read or write whose file name is in `STAND_IN_LOGS` (`check`, lines 93–110), outside the helper functions `_append_text` and `read_records`. Names outside the tuple pass the guard, and so does a call from the stand-in child processes, which run outside pytest (the module docstring says so).

**The other stand-in template uses the log for step assignment, not only for counting.** In `tests/test_stage2.py`, the stand-in reads `previous = read_records(log)` (line 194), slices it with `previous[scenario.get("_since", 0):]` (line 196), and then, for each call, loops over all prior records with the same name to assign step indices (the `assigned` loop, lines 216–225). `World.script` (lines 392–403) writes `_since` as `len(read_records(log))` at script time. The bead's note on this file is therefore accurate: a per-key count alone does not replace this use.

**Other readers of the same log.** `SwarmWorld.calls` (`tests/test_stage2_swarm.py`, line 478) and `World.calls` and `World.reviews` (`tests/test_stage2.py`, lines 405–411) read the full log on each call; `SwarmWorld.rewind` (line 493) deletes the file to start a fresh count. `tests/test_stage2_session.py`, `tests/test_stage2_research_availability.py` and `tests/test_pi_install.py` also embed the helper and append or read declared logs. I did not check whether any of them counts by key.

**Existing history.** The locked helper was introduced by change `flaky-swarm-leak-test` (`plans/changes/flaky-swarm-leak-test/spec.md`, `plan.md`, `decisions.md`). Its decisions record the choice of one declared-log tuple and a runtime guard, not a per-key structure. The timing research for the same test file is `plans/changes/swarm-test-speed/research.md`. Its orchestrator addenda put the swarm file as the largest per-test cost (about 615 s of the top 50 durations, measured 2026-10-28 at `dbef390f`) and name the per-slot declaration re-read and leak check as the dominant costs in production code (`scripts/stage2_research_run.py`, `Run.gate`). That report measured the production path; it did not measure the stand-in's log read.

**Not found.** No per-key counter, sidecar file or count helper exists in `tests/`, `scripts/` or `plans/changes/` (grep for `counter` in `tests/*.py` finds only unrelated test names). No file under `plans/changes/standin-call-counter/` besides `research.md` exists; the spec, decisions and plan are not written. No measurement of the stand-in's own log-read cost is recorded in the repository.

## Where it lives

- `tests/test_stage2_swarm.py`: `STAND_IN` template (lines 277–379, read at 297, counted at 345, appended at 372); `SwarmWorld.calls`, `SwarmWorld.rewind`.
- `tests/test_stage2.py`: the second stand-in (`read_records` at 194, `_since` at 196, assignment loop at 216–230); `World.script`, `World.calls`, `World.reviews`.
- `tests/atomic_test_log.py`: `STAND_IN_LOGS`, `_declared`, `append_record`, `read_records`, `_lock`, `embedded_source`.
- `tests/stand_in_log_guard.py`: `check`, `install`, `suspend`.
- `tests/test_atomic_test_log.py`: the tests that pin the helper, the guard and the stand-in templates (I read only its opening 80 lines).

## What is unclear

- **The bead's own text.** The topic copied into `research.md` by the orchestrator is the only source I have for the bead's scope. I cannot read the tracker (`.beads/` is a Dolt database and needs `tools/bd show`, which the explorer does not run).
- **Whether a second file is a declared log.** `_declared` and the guard only handle names in `STAND_IN_LOGS`. Whether a counter file under a new name would need its own declaration, and whether any test pins the exact tuple, is not read; `tests/test_atomic_test_log.py` past line 80 was not read.
- **Whether a counter has to be locked.** Stand-in children run in parallel (the swarm runs up to the provider limit at once), so a counter updated by read-modify-write without a lock would race. What guarantee the bead wants (exact counts or only a lower bound) is not stated in the repository.
- **Whether the count must match the log exactly.** The key count in line 345 counts records written before this call. Whether a separate counter would also have to reproduce the `repeat_last` fallback, the `kind` and `name` filters that the test files apply, or the `rewind` reset, is not established.
- **The cost figure.** The bead cites an external verify-speed analysis (checked 2026-11-24 at `18a13d3d`). The repository has no measurement of how much of the test time the log read takes, so the size of the gain is not known here.
- **Scope of `test_stage2.py`.** Whether the second stand-in's assignment loop is in or out of scope is a question the bead leaves open.

## Which files a change would have to touch

- For the swarm stand-in's count alone: `tests/test_stage2_swarm.py` (the `STAND_IN` template, line 296–297 and 345) and, for the locking, `tests/atomic_test_log.py` (a new helper beside `read_records`, or a declared name).
- If a new file name is used: `tests/atomic_test_log.py` (`STAND_IN_LOGS`) and possibly `tests/test_atomic_test_log.py` (the pinned tests).
- If the guard must also cover the counter: `tests/stand_in_log_guard.py`.
- If the test-side readers are changed too: `SwarmWorld.calls` and `SwarmWorld.rewind` in `tests/test_stage2_swarm.py`, and the teardown of `calls.jsonl` in `tests/test_stage2.py` and `tests/test_stage2_session.py`.
- Not touched by the bead: `tests/test_stage2.py`'s assignment logic, unless its second stand-in is in scope.
