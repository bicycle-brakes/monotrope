---
title: "Research — verify-machine-lock"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-p6mu
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
---

# verify machine lock — Research

Stage-2 call, 2026-10-28: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 727 files, 2504 commits, 12 rules.

## Runner exploration — 2026-10-28

The exploration is complete. Here is the research, ready to append to `plans/changes/verify-machine-lock/research.md`.

---

## What exists today

**The bead and its evidence.** Bead `coding-harness-p6mu` — "one `make verify` at a time per machine. P1, queue 2" — was opened from the three-lane night trial (`docs/journal/handover/2026-10-28-three-lane-night.md`, "Open work" and "Decisions and preferences"). The trial's measurement: three full `make verify` runs at once on the 8-core machine drive the load average above 100 and past the runner's 30-minute step limit; one at a time, a run takes 11–12 minutes (same handover, "Where we are"). The maintainer's decision recorded there: "full verification must run one at a time (bead coding-harness-p6mu makes it a lock). Foreign-model calls may run beside it."

**The verify chain, and that no lock exists in it.** `make verify` runs `bash scripts/verify_all.sh` (`Makefile`, target `verify`). `verify_all.sh` is the local runner of the one gate list: it holds no commands of its own, asks `scripts/ci_gates.py`, and that reads `decisions/gates.yaml` (`scripts/verify_all.sh` header comment and gate loop; `decisions/gates.yaml` header, "THE ONE LIST"). The heavy gate is `pytest` — `python3 -m pytest tests/ -q -n auto` (gate id `pytest`, enforcement block, floor true, placement both) — where `-n auto` spreads the suite over all cores; three concurrent full runs are what produced the load spike. I searched `Makefile`, `scripts/verify_all.sh`, `scripts/ci_gates.py` and the gate list for any lock, flock or mkdir-guard around verification: **not there** — nothing today serialises `make verify`. The locks that do exist guard other things, per change or per record, never per machine.

**The runner's own verify path.** The stage-2 runner invokes verification too: `["make", "verify"]` with `timeout=VERIFY_SECONDS` and the limit "the runner's step limit after 30 minutes" (`scripts/stage2.py` `verify_attempt`, around lines 5020–5024, and a second call site at 7014–7015; `VERIFY_SECONDS = 30 * 60` at `scripts/stage2.py:3803`). `launch()` (`scripts/stage2.py:873`) runs it in a process group of its own and kills the whole group on timeout. An attempt's verify "runs from the attempt's own tree: its Makefile, `scripts/verify_all.sh`, `conftest.py` and tests" (`scripts/stage2.py:4696–4697`) — so any lock keyed to a checkout path would miss cross-worktree contention; a machine-keyed lock covers both entry paths because both go through `verify_all.sh`.

**House lock precedents to reuse.** Three `fcntl.flock` sites exist. `holding_record(change, root)` (`scripts/stage2.py:3006–3026`): advisory `flock(LOCK_EX | LOCK_NB)` on a file beside the record, refuses with `Refused("another run holds the loop record …; one runner at a time")`, and "a descriptor dies with its process — so a crashed run leaves no lock behind to break the next". `Store.acquire_lock/release_lock/locked` (`scripts/stage2_research_store.py:186–211`): `os.open(..., O_RDWR|O_CREAT|O_NOFOLLOW, 0o600)` plus `flock(LOCK_EX | LOCK_NB)` → `StoreLocked`, "the operating system drops the lock when the holder dies". `scripts/stage2_availability.py:229–235` takes a blocking `flock(LOCK_EX)` on a `<path>.lock` file and releases it in a `finally`. Machine-local state lives outside the repository under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/stage2/…` (`docs/WORKFLOW.md:1296`, `scripts/stage2.py:122`, `scripts/stage2_research_store.py:65`) — the established place a machine-scoped verify lock would live. An older, different pattern is the `mkdir`-based lock with staleness cleanup in `tools/claude-code/statusline.sh:69–74`; flock needs no such staleness handling.

**Hard pins a change must design around.**
- `test_runner_holds_no_command_list_of_its_own` (`tests/test_ci.py:1002–1014`): `verify_all.sh` must reference no `scripts/<name>.py` except `ci_gates.py` (pinned negatively by regex over the script text). A Python lock helper called by a `scripts/….py` path from `verify_all.sh` would trip this pin.
- The runner-copy tests (`_runner_tree`/`_run_runner`, `tests/test_ci.py:1031–1187`): the suite copies `verify_all.sh` into throwaway trees and starts it several times, under `pytest -n auto` — including *inside* an outer `make verify`. A machine-wide lock taken unconditionally in `verify_all.sh` would make these tests contend with each other and self-deadlock against the outer verify that holds the lock (non-blocking: the suite goes red; blocking: it hangs toward the step limit). A declared opt-out or scoped key is therefore required, not optional polish.
- Environment-dependent behaviour is declared, never silent, in this repo: `placement: writer` gates run only on the writer machine, `leakcheck` "never in CI" (`Makefile:30–33`), and the gate schema comment says "A declared skip is a statement, not silence" (`decisions/gates.yaml`). Hosted CI runs the same verify job, so the lock needs a declared CI/no-op path.
- `scripts/verify_all.sh` is a kit file, role `mechanismus` (`scripts/kit/manifest.yaml:82–84`); a behaviour addition does not invalidate its reason line ("holds no commands, asks ci_gates.py") as long as the pin above holds.

## Where it lives

Everything named above: `Makefile` (target `verify`, lines 18–19; target `test`, 21–22), `scripts/verify_all.sh` (the whole runner, no lock today), `decisions/gates.yaml` (gate `pytest`, the `-n auto` suite), `scripts/stage2.py` (`VERIFY_SECONDS` 3803, verify calls 5020/7014, `holding_record` 3006, `launch` 873), `scripts/stage2_research_store.py` (store lock 186–211), `scripts/stage2_availability.py` (blocking lock 229–235), `tests/test_ci.py` (pins at 442–468, 1002–1014; runner-copy tests 1031–1187), and the origin handover `docs/journal/handover/2026-10-28-three-lane-night.md`.

## What is unclear about it

These are the open questions for the interview (research-handoff):

1. **Refuse or wait.** Does a second `make verify` fail fast naming the holder (the `holding_record` pattern, `LOCK_NB` + `Refused`), or block until the lock frees (the `stage2_availability.py` pattern)? The handover decision says "one at a time" but not which failure mode. A blocking lock interacts with the runner's 30-minute step limit (`scripts/stage2.py:3803`). `[DECISION]`
2. **Lock location and key.** Under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/` (survives reboots, matches the loop-record precedent) or `$TMPDIR` (per-boot); and what identifies "one at a time" — the machine, or this repository across all its worktrees. No artifact I read states either. `[DECISION]` or `[DETAIL]`
3. **The test/CI opt-out.** Name and semantics of the declared opt-out (env variable) that keeps `tests/test_ci.py`'s runner-copy runs and the hosted CI out of the machine lock. Not stated anywhere yet; required by the self-deadlock fact above. `[DETAIL]`
4. **Scope: `make test` too?** The bead and handover say `make verify` / "full verification"; `make test` (`Makefile:21–22`) drives the same `-n auto` load by hand. Whether it is covered is undecided. `[DECISION]`
5. **Not read:** live pull-request state, the tracker entry `coding-harness-p6mu` itself (a tracker read needs the Dolt hydration; my tools are read-only file access), and `tools/bd` metadata. The bead's description as quoted here comes from the handover, not from the tracker. What the tracker adds (dependencies, "Needed" line) is an open question for the runner.

## Which files a change would have to touch

`scripts/verify_all.sh` (take the lock around the gate loop — covers both the developer's `make verify` and the runner's calls, including attempts verifying from another tree); `tests/test_ci.py` (new lock regressions; opt-out wiring for the runner-copy tests; the negative pin at 1002–1014 constrains how the lock is invoked); possibly a small helper script whose name and call spelling must respect that pin; `Makefile` only if `make test` is covered (the W-6 pin, `tests/test_ci.py:442–468`, compares Makefile tab lines against gate commands); `docs/WORKFLOW.md` §"Verification runs through git and CI" (line 441 ff.) and/or the `make help` text for the declared behaviour. `decisions/gates.yaml` does not change — the lock wraps the run, it is not a measured gate.

## Neighbours

- `plans/changes/review-release-lock/spec.md` — active change; the loop-record lock (R-14, bead coding-harness-1wo, PR #190) and its refusal semantics, the closest precedent.
- `plans/changes/research-swarm/spec.md` — the runner change whose `design.md` (line 474) specifies the state-store flock.
- `plans/specs/implementation-verification/spec.md` — living spec; pins the ordering "stamping precedes index rendering, which precedes make verify on every attempt", i.e. where verification sits in the attempt pipeline.

## Draft-time repository gaps resolved — 2026-10-28

Read against `8b1f2d98` in this worktree:

- [GAP] There is no separate general cheap-pytest preflight in `scripts/stage2.py` at this commit. The existing selected-test executions are `red_first` and `fixed_test_proof`; the former also starts an interpreter import probe. The plan guards these existing local pytest executions and adds no new checking stage. Both `verify_attempt` and `verify_draft` launch `make verify` through `launch(timeout=VERIFY_SECONDS)`; admission must precede that timed launch.
- [GAP] `templates/plan.md` and `scripts/validate_change_artefacts.py` do not exist in this tree. The plan therefore follows `prompts/03-plan.md`; available checks are the interview, criterion-ledger and registry checks. The missing validator cannot supply evidence of a passing gate.
- [DETAIL] FIFO means order of registration with the shared queue, not process creation time. An explicit live-waiter order is needed alongside the exclusive file lock to make the decision's first-come-first-served promise testable.
- Not read: live pull-request state, live session registry and tracker contents. Those sources are outside the draft's permitted file-reading boundary; the handover describes earlier parallel lanes, not current ownership of this checkout. This draft writes no tracker state.
