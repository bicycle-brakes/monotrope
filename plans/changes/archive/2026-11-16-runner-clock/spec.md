---
title: "Spec — runner-clock"
status: accepted
implementation_status: done
date: 2026-11-14
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-pph3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, runner, clock, flaky-tests]
class: bounded
appetite: 4
adr_files: []
neighbours: []
---

# Spec — runner-clock

Make the runner's timing tests independent of machine load through one
injectable clock boundary, without weakening execution limits or process
cleanup (bead coding-harness-pph3 — runner clock and load-flaky tests).
Research: [research.md](research.md). Decision: [decisions.md](decisions.md#q-1--how-the-load-flaky-timing-tests-become-robust).

## Problem

At `9140bfb6` on 2026-11-14, the runner has a test seam for monotonic
time, but its remaining-budget helper and review-round expiry checks bypass
it. A fake clock therefore cannot control the whole timing policy
(research, “What exists today” and “Where it lives”).

The verification-admission test combines a two-second execution allowance,
one second of queueing and a child sleeping for 1.5 seconds. Under parallel
load, scheduling consumes that margin and produces a timeout despite a
correct admission boundary. Research cites failures in the verification-order,
research-routing and compaction review records, dated 2026-11-14.

Other tests use real short deadlines, child sleeps and elapsed-time assertions
for reviewer expiry, discovery and cleanup. Moving only runner clock reads
cannot accelerate a child's sleep or the standard library's process wait
(research, “What is unclear about it”, items 5–6). The tests must control both
the policy clock and the outcome of the process wait where timing is simulated.

## Terms

- **Runner:** `scripts/stage2.py`; imported components retain their own clock boundaries.
- **Clock boundary:** the single function through which this module obtains
  current monotonic time, UTC wall time and local calendar dates.
- **Timing test:** a runner test whose verdict depends on a short real-time
  allowance, an elapsed-duration comparison or sleeping to cross a deadline.
  A bounded wait used only to stop a stuck integration test is a watchdog,
  not evidence that a timing policy is correct.

## Acceptance criteria

1. When runner code obtains the current time or date, it does so through one
   replaceable clock function.
   *Refuted by:* a current monotonic, wall-clock or calendar-date read in
   `scripts/stage2.py` outside that function, including a read through an alias.
   *Basis:* decisions.md#Q-1; research, existing seams and direct reads.

2. If a direct clock read or sleep is introduced outside the clock boundary
   in the runner, a test fails without adding an exemption for that site: the
   runtime check of the test session when runner code makes the read, and the
   source test as a cheap advisory reading of the module.
   *Refuted by:* accepting `time.monotonic`, `time.time`, `time.sleep`,
   `time.perf_counter`, their nanosecond variants, other current-time APIs
   (including CPU clocks and no-argument local/UTC time conversion),
   `date.today` or `datetime.now`/`utcnow`/`today` outside the boundary,
   including imported aliases;
   or requiring a list of permitted caller functions or source lines;
   or a read the runner makes at run time or at import, through any alias,
   default argument, `__call__` or partial application, that leaves the test
   session green.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2; research, source-guard precedent.

3. While verification waits for admission, advancing the injected clock by
   more than the execution allowance leaves that allowance available in full
   when execution begins.
   *Refuted by:* a simulated timely check failing because it queued, or a
   simulated over-budget check succeeding; both outcomes must be checked
   without real sleeping or a real queue holder.
   *Basis:* decisions.md#Q-1; research, verification-admission failure.

4. When any runner timing test exercises a deadline or duration policy, its
   result is determined by an injected clock and controlled wait outcomes.
   *Refuted by:* a test still requiring a child to finish within a small
   real-time margin, a real sleep to expire a budget, a duration comparison
   against the machine clock, or a fake that passes without checking the
   production path's supplied timeout/deadline.
   *Basis:* decisions.md#Q-1; research, timing-test population and subprocess boundary.

5. When the clock is injected or uses its production implementation, existing
   timing meanings remain unchanged: durations use monotonic differences,
   terms use UTC dates, and document stamps use local dates.
   *Refuted by:* a wall-clock jump changing a measured duration, a timezone
   boundary making terms use the local date or stamps use the UTC date, or
   an existing independently pinned date/time seam ceasing to work.
   *Basis:* decisions.md#Q-1; research, paired clock seams and wall-clock sites.

6. When a launched program exceeds its allowance or the runner is interrupted,
   the existing bounded cleanup and diagnostic behavior remains effective.
   *Refuted by:* a changed production limit, a surviving process group after
   cleanup, an unbounded drain of escaped descendants, lost timeout diagnostics,
   or replacing all operating-system cleanup evidence with simulated processes.
   *Basis:* decisions.md#Q-1; research, existing execution and drain limits.

## Non-goals

- Increasing timeouts, serializing the suite, reducing parallel workers or
  replacing a failing assertion with a larger timing margin.
- A repository-wide clock framework, a new runtime setting, changing how
  the standard library measures subprocess timeouts, or virtualizing an
  actual operating-system scheduler.
- Changes to the time-record schema, admission protocol, model selection,
  terms policy or the verification workload.
- A design document or ADR: the class is `bounded`, and this refactor adds
  an injection boundary inside an existing component.

## Protected areas

- `scripts/verify_lock.py`, `scripts/verify_duration.py`, `scripts/time_records.py`
  and `scripts/stage2_research_*.py` — independent components, outside this
  runner-module refactor; their production clocks and protocols stay intact.
- `tests/test_verify_lock.py` — real admission integration evidence stays intact.
- Held configuration, governance and harness paths, including `AGENTS.md`,
  `provenance.yaml`, `decisions/`, `model-endpoints.yaml`, `prompts/`,
  `templates/` and the harness dot-directories — no policy change is required.

## Boundary

Maintainer, 2026-11-15 (decisions.md Q-2), after the phase-6 review found two
more shapes the source guard accepts (`time.monotonic.__call__()` and a
default argument that reads the clock at import, rows F6-1 and F6-2): case
repair of the static guard stops, and the runtime check is the closing
mechanism of criterion 2. When the test session starts, before any test
module imports the runner, it wraps every clock-reading `time` function on
the `time` module and the clock-reading class methods of `datetime.date` and
`datetime.datetime` in the types' own dictionaries, the same sets the source
guard bans (`sleep` and the CPU clocks included). Every alias, `from … import`,
default argument, `__call__`, `getattr` or partial application the runner
builds therefore reaches a wrapper, at import as at call time. The wrapper
judges the Python frame that called it: a frame compiled from
`scripts/stage2.py` outside the one module-level `clock_now` is recorded and
refused, and an autouse fixture fails the test on any new record, so a read
the runner swallows still fails. The standard library, test code and other
modules read freely. A clock callable the runner holds instead of reading by
attribute - an original bound before the wrappers, or a wrapper that a
dataclass default factory or a thread target would call later from a frame
not the runner's - is found by a scan of the module's globals, its functions'
defaults, keyword defaults and closures, and its classes' attributes and
dataclass fields; the session refuses to start if the runner was imported
first. A conversion called with a `None`
instant held in a variable is now caught. The source guard and the
paragraphs below stay as a cheap advisory reading; a runtime finding no
longer calls for a new static case.

What the runtime check cannot see: a line no test executes (the source guard
still reads those); a clock callable the runner passes as an argument at run
time without holding it, such as `threading.Thread(target=time.sleep)`, since
the call then comes from the library's frame; code run through `eval` or
`exec` under another filename; a child process, which does not load the test
session; and the window in which a test itself replaces a wrapper, as a fake
clock does. The check relies on CPython: it writes the `datetime` types'
dictionaries through `gc` and `ctypes`, and the session refuses to start if
that does not take effect.

Orchestrator, 2026-11-15, after the third finding of the source-guard
completeness mechanism in review-loop round 1 (an annotated alias, the raw
POSIX clocks and a star import passing the guard): the guard of criterion 2
reads the runner module's syntax tree and is structural, not a list of
spellings. It resolves every binding the module gives the `time` and
`datetime` modules or a chain rooted in them (`import`, `from … import`
including a star import, plain, multiple-target, positional tuple and
annotated assignment, and the walrus), bans a declared complete set of
clock-reading `time` functions and `datetime`/`date` methods wherever they
are named, not only where they are called, forbids the two modules to be
named on their own outside an attribute access, and exempts exactly one
function object, the single module-level `clock_now` definition; a second
definition or binding of that name is itself a violation.

Orchestrator, 2026-11-15, after a fourth finding of the same mechanism in
review-loop round 2 (the banned set's completeness unchecked): "complete" is
measured, not declared. A test classifies every public callable of the
installed `time` module and every public class method of the `datetime`
classes as a clock read, a no-argument conversion or a non-reading callable,
so a clock function a new interpreter adds fails the suite until it is
classified.

Orchestrator, 2026-11-15, after a fifth finding of the same mechanism in
review-loop round 3 (a conversion's instant judged by argument count alone):
a no-argument conversion counts as given its instant only when that instant
is passed as plain positional arguments. A starred or double-starred argument
can expand to nothing and a literal `None` asks for the current time, so the
guard reports both; a keyword is never the instant, since the conversions take
none. A variable that holds `None` only at run time is not visible to a static
reading and stays outside this guard.

What a static reading of one module cannot see is outside this guard: a
clock reached through `importlib`, `__import__` or `sys.modules`; a
`datetime` or `date` class handed into a function as an argument and called
there; clock reads inside another module the runner imports (those keep
their own boundaries, see Protected areas); a clock read through a module
other than `time` and `datetime`, such as the elapsed time of `os.times()`
(the runner calls none on 2026-11-15); and waits measured inside the
standard library, such as a subprocess timeout. On 2026-11-15 the runner's
uses of `importlib` and `sys.modules` load a probe file and hand on the
runner module itself, not a clock module. A reviewer reading a new such
path reports it; the guard does not claim to catch it.

## Definition of Done

- The runner's full `make verify` is green at the reviewed commit.
- Moved in the same pull request: this spec and `plan.md`, with implementation
  status, criterion-ledger progress and measured phase-4 time; no ADR or other
  policy document changes.
- The source guard is proven red by representative bypasses and green on the
  clock boundary; timing tests pass under serial and parallel execution.
- The pull request's file list preserves the protected areas and non-goals.
- The pull request closes the runner-clock work item; its final commit carries
  `Closes-Bead: coding-harness-pph3`.

## Open decisions

None open. The maintainer's answer in Q-1 is unchanged; Q-2 (2026-11-15)
makes the runtime check the closing mechanism of criterion 2.

- [DETAIL] Guard the runner module, including its wall-clock/date reads;
  independent imported components are outside this bounded change. This
  follows the decision's named module and avoids introducing a shared service.
- [DETAIL] Preserve the existing `utc_now`, `monotonic_now`, `today` and
  `terms_today` seams as adapters, so existing callers and date pins keep
  their meaning while the raw reads have one boundary.
- [DETAIL] Use four hours of phase 4, repairs included, as a stop: the
  interview states no appetite, and the test-boundary work is bounded here.
- [DETAIL] The second test name in Q-1,
  `test_before_admission_execution_budget_is_shared_and_wait_free`, is absent
  from this worktree at `9140bfb6` (2026-11-14). It is not silently renamed
  to the nested-admission test. Criterion 4 covers the entire present timing
  class; the plan records the missing name for reconciliation if that test
  arrives before merge, without adding a new budget policy.
