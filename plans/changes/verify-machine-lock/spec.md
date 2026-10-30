---
title: "Spec — verify-machine-lock"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-30
supersedes: null
superseded_by: null
bead: coding-harness-p6mu
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, verification]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — `verify-machine-lock`

The goal is to queue local verification for one user on one machine, checking
available memory before work starts, without spending a runner's checking
time limit on admission (bead `coding-harness-p6mu` — serialize verification).
Research: `research.md`. Decisions: `decisions.md`.

## Problem

- Concurrent full checks exhaust the machine's capacity: the three-lane
  trial recorded load above 100 and checks exceeding 30 minutes, versus
  11–12 minutes sequentially (research, origin handover dated 2026-10-28).
- Neither the shell entry nor the runner serializes verification. A lock
  scoped to a checkout would miss the competing worktrees (research,
  "What exists today"; confirmed at `8b1f2d98`, 2026-10-28).
- The runner currently counts all child-process time against its checking
  limit, and the suite starts copied runners inside full verification.
  Adding an unconditional blocking lock alone would introduce timeouts or
  self-deadlock (research, "Hard pins" and draft-time gaps).
- No admission memory check exists at those entries; the chosen floor is a
  starting policy, not a measurement of the earlier memory stop (decisions,
  "Memory floor", 2026-10-28).

## Terms

- **Protected work:** gate execution through `scripts/verify_all.sh`, runner
  post-run `make verify` in both `verify_attempt` and `verify_draft`, and
  existing runner pytest checks in `red_first` and `fixed_test_proof`, including
  the former's pytest import probe. Listings execute no protected work.
- **Admission:** queue waiting followed by the memory check while holding the
  exclusive lock, before protected work starts.
- **Shared state:** `${XDG_STATE_HOME:-~/.local/state}/coding-harness/`, shared
  by cooperating entries of the same user on this machine. The exclusive
  lock is `verify.lock`; neither repository nor worktree identifies it.
- **Nested work:** protected work descended from a lock holder, carrying
  `HARNESS_VERIFY_LOCK_HELD=<holder-pid>` and `HARNESS_VERIFY_LOCK_TOKEN=<token>`,
  the random token that admission published with its ownership. The token is
  the proof of belonging: the environment reaches every descendant, also across
  new sessions, nested runners and a dead holder, and no unrelated process
  knows it (maintainer, 2026-10-30).

## Acceptance criteria

1. When independent protected entries use the same shared state, at most one
   admission's protected work executes at a time across repositories and worktrees.
   *Refuted by:* overlapping gate/pytest intervals from independent admissions.

2. When several live entries wait, they are admitted in registration order
   without runner priority.
   *Refuted by:* a later registered waiter overtaking an earlier live waiter.

3. While an entry waits for another holder, it logs the wait immediately and
   at least every five minutes, identifying the holder's process id, command
   and start time whenever a holder exists.
   *Refuted by:* a silent wait, a missing five-minute update, or missing holder
   identity despite an active holder with published metadata.

4. When a runner check finally starts, its configured execution time limit
   is available in full regardless of time spent in admission.
   *Refuted by:* queue or memory waiting causing a short passing check to time
   out, or removal of the existing limit on a hung executing check.

5. When nested work inherits a valid held marker, it uses its ancestor's
   admission without another queue or memory wait.
   *Refuted by:* a nested copied runner deadlocking or rechecking memory; an
   absent, malformed, stale or unrelated marker bypassing admission.

6. When a protected invocation finishes, fails or is interrupted, remaining
   live waiters can proceed without manual stale-lock or dead-waiter cleanup.
   *Refuted by:* a dead holder/waiter blocking progress, or releasing ownership
   while its protected child workload still runs.

7. When a memory reading is available, admission uses macOS
   `memory_pressure`'s system-wide free percentage or Linux
   `MemAvailable / MemTotal * 100`, according to the host platform.
   *Refuted by:* substituting another macOS percentage, Linux `MemFree`, or
   accepting malformed/non-finite values as a usable reading.

8. While usable available-memory readings are below the configured floor,
   admission retains the lock and waits, logging and rechecking every 30 seconds.
   *Refuted by:* protected work starting on a below-floor reading or another
   admission entering while the first waits for memory.

9. If usable memory readings remain below the floor for 60 minutes from the
   first low reading, admission refuses without starting protected work and
   names the floor and last reading.
   *Refuted by:* a workload starting, an unbounded low-memory wait, or refusal
   without the two percentages; a qualifying reading before the deadline must
   instead allow work to start.

10. If memory cannot be measured, admission logs that fact and proceeds.
    *Refuted by:* an unavailable, failed, hung, unsupported or malformed probe
    hanging/refusing the run or being silently treated as a valid percentage.

11. When no override is provided, the floor is 25 percent, with equality
    sufficient for admission.
    *Refuted by:* a usable reading below 25 starting work, or exactly 25 waiting.

12. When `HARNESS_VERIFY_MEMORY_FLOOR` supplies a finite percentage in
    `[0, 100]`, admission uses that value; an invalid override refuses explicitly.
    *Refuted by:* ignoring a valid override or silently accepting an invalid one.

13. When protected work completes, the wrapper preserves its existing success
    or failure verdict and gate selection, including hosted CI.
    *Refuted by:* turning a failed check green, changing placement/enforcement,
    adding a second command list, or disabling admission merely because CI is set.

14. If shared locking or queue state cannot be used safely, the entry refuses
    with a diagnostic before protected work starts.
    *Refuted by:* falling through unlocked after a state-directory, lock or
    queue error, or following a substituted state file to overwrite another file.

## Boundary

Decided by the maintainer on 2026-10-30 after repeated phase-6 rows on one
mechanism (protected descendants outliving the admission). The admission
protects the machine's load, not data: an overlap of two checks costs time,
never correctness.

- Covered: normal exit, failure, cancellation and trapped signals (SIGINT,
  SIGTERM, SIGHUP, SIGQUIT) end the protected command's process group before
  release; a grandchild left in that group after the command exits is ended
  before release, by the supervisor and by the runner's timed launches. A trapped
  signal that arrives while the protected command is being started is held back
  until the command is registered for cleanup, in the supervisor as in the runner
  (phase-6 row F6-9).
- Accepted limit, signal timing (maintainer, 2026-10-30): after that deferral, a
  further finding about the moment a signal arrives is an accepted limit, not a
  finding: the lock protects the machine's load, never data.
- Accepted limit: when an intermediate process is killed hard (SIGKILL) while
  its own descendants run in another process group or session, those
  descendants can outlive the admission and briefly overlap a successor. Their
  time is bounded by the runner's step limits. A review row that describes
  only this case is an accepted limit, not a finding.
- A process container that would close the limit (cgroups, job objects) is out
  of scope until the run report measures such overlaps in practice.

## Non-goals

- Serializing hand-run `make test`, all Python processes, different users,
  different machines, or entries deliberately configured with different state roots.
- Limiting foreign-model calls, changing model availability, or holding this
  lock around an entire attempt or review round.
- Introducing a new cheap-pytest stage, changing pytest worker counts, gate
  commands, placement or enforcement, or changing configured execution limits.
- Guaranteeing memory safety after admission: the floor is a pre-start check,
  not continuous monitoring, memory reservation or a promise against every OOM.
- Priority scheduling, a public bypass flag, or CI-specific disabling.
- Architecture policy changes or ADR files. Phase 2b does not run for a bounded change.

## Protected areas

- `decisions/gates.yaml`, generated CI and `Makefile`: the existing gate list,
  placement and direct `make test` contract remain authoritative.
- Model routing, endpoint configuration and foreign-call lifecycle: independent
  network work must remain parallel.
- Existing interview records and unrelated changes: no new maintainer answer
  or change to their scope is implied.

## Definition of Done

- Targeted subprocess and runner regressions pass; `make verify` is green.
- Updated together: `docs/WORKFLOW.md`, the kit manifest, this plan's criterion
  ledger/time record and runner-derived `plans/INDEX.md`; no ADR changes.
- Protected areas remain untouched and non-goals unbuilt, shown by the PR file list.
- The PR closes the verification-serialization work item
  (`coding-harness-p6mu`); the last commit carries `Closes-Bead: coding-harness-p6mu`.
- Special runs: a synthetic three-entry contention/crash test, isolated from
  the real machine lock, with the checked commit recorded in the PR; no live
  low-memory stress run is required.

## Open decisions

None open. Existing direction and agent details stand in `decisions.md`.

- [DETAIL] FIFO is registration order; process creation time is not reliably
  observable across independently started entries. A bare exclusion lock is
  insufficient evidence of ordered admission.
- [DETAIL] The phase-4 appetite is three hours including repairs, chosen as
  a stop because no earlier appetite is stated for this change.
- [DETAIL] Override validation, bounded memory-probe execution and rejection
  of unusable lock state make failures explicit rather than silently removing
  protection; they do not change the recorded unknown-memory policy.
- [DETAIL] A held marker represents a live ancestor's ownership, not a generic
  opt-out. Invalid markers use ordinary admission; valid markers and the
  shared state root must survive local runner/test environment construction.
- [DETAIL] No research-swarm run exists for this bounded change, so claim
  handoff lines are not required. `neighbours: []` makes no swarm claim.
