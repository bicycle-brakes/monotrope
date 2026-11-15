---
title: "Spec — flaky-swarm-leak-test"
status: draft
implementation_status: partial
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-15
supersedes: null
superseded_by: null
bead: coding-harness-yb1l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, tests, swarm, concurrency]
class: bounded
appetite: 3
adr_files: []
neighbours:
  - plans/changes/swarm-test-speed/spec.md
  - plans/changes/raising-fault-test/spec.md
---

# Spec — flaky-swarm-leak-test

Concurrent test-log access must preserve complete observations without weakening
the swarm's security refusal (bead coding-harness-yb1l — flaky swarm leak test).
Research: `research.md`. Maintainer answers: `decisions.md`.

## Problem

The research records two main-CI failures of the refused-run notice test,
reported in the 2026-11-12 night handover: its clean second run returned 2
instead of 0. These CI logs were not read directly. Its print observer parses
the call log while stand-in processes append large records; an incomplete
line can raise inside the gate and correctly trigger a fail-closed refusal.
That causal chain is inferred, not yet reproduced.

The maintainer chose a common test-log helper and a regression guard rather
than a one-test workaround. The draft inspection at `3950c853` accounts for
the interview's 17 opens: 15 data appends and two lock-only opens across five
test files; three data appends already have a local lock. Shared readers must
participate too: locking only writers still exposes partial records.

## Terms

**Atomic observation:** a reader sees a snapshot of complete appends; an
append in progress is either absent or complete, never a partial fragment.
**Test logs:** stand-in call, infrastructure, version, installer and receipt
logs in the five files inventoried in `research.md`, including their generic
scenario-driven text appends.
**Declared stand-in log:** a JSON test log whose file name the shared helper
declares (`STAND_IN_LOGS`); the helper's JSON functions serve no other name.
Append-mode opens elsewhere under `tests/` — production-lock probes, document
mutations, the admission-order probe of the verify lock (whose writers the
lock under test admits one at a time) — are not stand-in logs.
**Receipt log (`receipts.jsonl`):** a test log with a production writer, so
not a declared stand-in log (2026-11-14, loop row L2-6). The swarm stand-in
appends receipts through the helper's `text_append`, but the production tool
wrapper (`scripts/stage2_research_tools.mjs`, `appendFileSync`) writes the same
file and cannot take Python's `flock`; production reads it without the helper,
once the seat's process has ended (`scripts/stage2_research_run.py`). Its
protection therefore rests on each writer appending one small receipt line (a
bounded title and excerpt) in a single `O_APPEND` write and on that late read,
not on the helper's lock; the helper's lock only orders the stand-in's own
appends. Changing the production writer or reader is a non-goal of this
change. Within the suite the stand-in appends `receipts.jsonl` through
`text_append`, under the helper's lock (2026-11-14, loop rows L2-6 and L3-3;
phase-6 row F6-3); the file is not a declared stand-in log, so the guard does
not watch it, and the production writer stays outside the lock. A torn read
there is not expected: each seat has its own scratch directory with one stand-in writing its receipts, no test
under `tests/` reads that file itself (read 2026-11-14 at `88e28114`; the one
test that writes a `receipts.jsonl` by hand, in `tests/test_research_capture.py`,
does so after its child process has returned), and the only reader is the
production runner, which reads it after the seat's process has ended. A test
that read it while a stand-in may still write would reopen the gap.

## Acceptance criteria

1. When independent stand-in processes append to a test log while another process or the pytest observer reads it, every observation contains only complete appends.
   *Refuted by:* a forced mid-append read returns a fragment or raises a JSON parsing error for otherwise valid records.
   *Basis:* decisions.md#Q-1.
2. When concurrent writers finish successfully, the final test log contains every submitted record exactly once with its full payload.
   *Refuted by:* an identifier is missing or duplicated, or a large record's payload differs from the submitted value.
   *Basis:* decisions.md#Q-1.
3. If a test log already contains malformed JSON, the shared JSON reader reports the parse failure rather than hiding it.
   *Refuted by:* a malformed stored record is skipped, truncated, retried indefinitely or returned as an empty successful observation.
   *Basis:* decisions.md#Q-1.
4. When any inventoried stand-in data append or corresponding concurrent log read executes, it uses the shared helper while preserving the existing record contents and missing-log-as-empty behavior: only `FileNotFoundError` for a missing file or directory yields an empty snapshot. Other I/O errors propagate, including `NotADirectoryError` when a parent component is a regular file.
   *Refuted by:* any of the 15 data appends of the five-file stand-in inventory bypasses the helper, a reader can race an append, a missing log or its missing directory fails, or a scenario text append gains or loses bytes.
   *Basis:* decisions.md#Q-1.
5. When a test reads, writes or opens a declared stand-in log without the shared helper, the test fails with a clear error: in the pytest process the runtime check refuses every `open`, `io.open`, `os.open` and `pathlib.Path` `open`, `read_text`, `read_bytes`, `write_text` or `write_bytes` of a declared log outside the helper's locked read and append, however the path was bound, and fails the test even when the code under test swallows the refusal or makes the access in another thread. The static guard additionally reads every module under `tests/`, including executable stand-in source strings, as a cheap advisory and identifies the source location of what it can follow.
   *Refuted by:* a planted raw read or append of a declared log in the pytest process completes or leaves its test green - including both forms of phase-6 row F6-8 (a log reached through a comprehension's first iterable or a parameter default) and a refusal swallowed in the test body or in a thread -, the helper's locked read or append is refused on the main thread or in an observer thread, an operation on a file that is not a declared log is refused or flagged, or either check needs an exemption list to pass the repository (the one marked planted-fault test is not such a list; [DETAIL] under Open decisions).
   *Basis:* decisions.md#Q-2; decisions.md#Q-3; decisions.md#Q-5; decisions.md, "Guard design after the review loop".
6. When a leak refuses a swarm run and its inputs are then restored, the refused run is announced before any model call in the next successful run.
   *Refuted by:* the leaking run starts a model call or returns success, the clean run returns 2, or its first refused-run notice is absent or observes a nonzero call count.
   *Basis:* decisions.md#Q-1.
7. When the repair is submitted for review, its proof is the forced mid-append race failing before the fix and passing after it, ten of ten runs on each side with the same workload, and the evidence states openly that the natural CI failure was not reproduced locally (60 of 60 loaded refused-run checks passed on the pre-fix tree `079e0aac`).
   *Refuted by:* only green reruns are shown, the two sides run different workloads without explanation, an after-run fails, commands, commits, repetition counts or diagnostics are missing, or the evidence presents the loaded refused-run checks as a before/after signal or the natural CI failure as reproduced or explained.
   *Basis:* decisions.md#Q-1; decisions.md#Q-4.

## Non-goals

- Production runner, dispatcher, leak-check or admission changes; no exception
  suppression, retries or relaxed assertions to make the flake disappear.
- Faster swarms, changed scheduling, new dependencies or workflow changes.
- A transactional allocation of scenario steps, crash recovery for a killed
  writer, or atomic reads by production readers of arbitrary fixture text.
- A claim that the historical CI failures are conclusively explained without
  their diagnostics; local reproduction proves the mechanism it exercises.
- Design phase 2b and an ADR draft: this bounded test-only repair requires neither.

## Boundary

The guard knows stand-in logs by declaration only (decisions.md#Q-3, loop
row L2-1). It fails on a raw read, write or open of a file whose name is one
of the helper's declared names (`STAND_IN_LOGS`); a test that introduces a
log under a new name and appends to it concurrently without the helper is
not seen, and the torn-read flake could return through that name. The
helper refuses an undeclared name in its JSON functions, so a log that uses
the helper is always one the guard watches; the gap is the log that never
uses it. The maintainer chose to ship with this boundary stated; the
contract that closes it is tracked separately (bead coding-harness-6zpj).
Paths that never carry a declared name stay outside both checks. Arbitrary
obfuscation and raw OS calls stay outside the static guard ([DETAIL] under
Open decisions). So does a path produced by a call outside the static
guard's known path-building set (`Path`, `PurePath`, `str`, `join`,
`joinpath`, `resolve` and the like): an ordinary helper function or string
method that returns a declared name hides it from the static guard just as
obfuscation does, and a raw `open`, `read_text` or `write_text` on its result
passes it (2026-11-14, loop row L3-2). In the pytest process the runtime
check below refuses both.

The static guard follows a log's path through every way Python binds a name -
assignment with one or several targets, tuple and list unpacking paired
element by element, starred, annotated and augmented assignment, the walrus,
`for` and comprehension targets, `with … as`, and parameter defaults - and
every such binding shadows an enclosing one, with lexical scoping for
functions and comprehensions (2026-11-15, findings F6-4, F6-5, F6-6) - with one
known miss: it resolves a comprehension's first iterable and a parameter
default in the inner scope, where Python evaluates them in the enclosing one,
so `[log.read_text() for log in [log]]` and `def reader(log=log)` lose the
log (phase-6 row F6-8). The static guard is not extended for that: the
runtime check closes it. What a static reading cannot follow stays outside
it, and the static guard errs in a known direction for each (2026-11-15):

- Containers and unpacking that cannot be paired: unpacking a variable or a
  call result (`a, b = pair`) and looping over anything but a literal give
  the whole value to every target, so a document that shares a container
  with a log is flagged as a log - the guard errs towards a finding.
- Attributes: a path stored as `self.log = …` or on any object is not
  followed, so a raw read through the attribute passes.
- Calls: a log passed as an argument is unseen inside the callee, whose
  parameter shadows any enclosing binding (finding F6-5), and a function's
  return value is not a path (loop row L3-2) - both pass.
- Order: a name bound to a log anywhere in a scope is a log in the whole
  scope, so a name rebound from a log to a document is still flagged.
- `global` and `nonlocal` keep the enclosing binding, but what a function
  binds through them does not reach the enclosing scope; a class body's
  bindings count as its enclosing scope's.
- The destination of `read_text`, `read_bytes`, `write_text` and
  `write_bytes` is their receiver, or their first argument when called on a
  path class (`Path.read_text(path)`) or as a bare function; any `open` is
  judged by its receiver, first argument and `file=` (finding F6-7).

**The runtime check closes what the static reading cannot follow**
(decisions.md#Q-5, 2026-11-15; phase-6 row F6-8). It judges the file name at
the moment of access, not the source text, so every miss listed above for the
static guard - attributes, call arguments and results, obfuscation, row
F6-8's two forms - is refused when it runs in the pytest process. The static
guard stays as a cheap advisory and is no longer extended case by case. The
runtime check (`tests/stand_in_log_guard.py`, installed by `tests/conftest.py`)
has its own limits:

- Process: it covers the pytest process, each xdist worker, from the import
  of `tests/conftest.py` on. The stand-in child processes and the
  forced-split writer run outside it; their sources stay under the static
  advisory, and the stand-ins use the embedded helper.
- Entry points: `builtins.open`, `io.open`, `os.open` and the five
  `pathlib.Path` methods. Lower layers - `io.FileIO`, `_io.open`, a shell
  command such as `cat` in a subprocess - pass.
- Names: declared names only, as above (bead coding-harness-6zpj). An integer
  file descriptor carries no name and passes. Removal and existence checks
  are not access: removal is the suites' clear.
- Helper: an access passes when the helper's `read_records` or its locked
  append (`_append_text`) is on the call stack; a test that calls the private
  `_append_text` directly passes as well.

Platform: the helper takes its lock with `fcntl.flock` and imports `fcntl`
unconditionally, so it runs on POSIX systems only — macOS locally and Linux
on CI. Windows is not supported: there every test module that imports the
helper fails at import (2026-11-14, loop row L3-4).

## Protected areas

`scripts/`, `tools/`, `tests/terms_fixtures.py`, production configuration,
`prompts/`, `templates/`, governance files and other change folders stay
untouched: the test mechanism is the repair boundary. The neighbouring
swarm-test-speed change's protected production call and scan paths stay intact.

## Definition of Done

- Targeted checks and runner-owned `make verify` are green.
- The shared helper, its tests, the runtime check (`tests/stand_in_log_guard.py`,
  `tests/conftest.py`), the five migrated test files and this change's
  research/spec/plan move together; no model, ADR or external document changes.
- The pull request's file list demonstrates the protected areas and non-goals.
- The final implementation commit carries `Closes-Bead: coding-harness-yb1l`;
  the orchestrator owns tracker and pull-request work.
- Red/green concurrency evidence and repeated loaded runs name their date,
  measured commit, exact command and outcomes in `plan.md` and the PR body.
- After the merge (a follow-up, not a merge gate): for two weeks the
  orchestrator counts failures of the swarm tests (`tests/test_stage2_swarm.py`)
  on main's CI and reports them to the maintainer (decisions.md#Q-4).

## Open decisions

None open. The two answers of 2026-11-13 remain unchanged; the maintainer's
third answer (decisions.md#Q-3, 2026-11-14) states the guard's name boundary,
the fourth (decisions.md#Q-4, 2026-11-14) restates criterion 7 and adds
the after-merge measurement, and the fifth (decisions.md#Q-5, 2026-11-15)
makes the runtime check the choke point and keeps the static guard as an
advisory.

- [DETAIL] The appetite is three hours of phase 4 including repairs, a stop
  chosen because neither answer states a budget and this is a bounded repair.
- [DETAIL] The 17-site inventory retains its two lock-only operations as
  explicit classifications; only its 15 data appends require migration. This
  follows the inspected operations without calling a lock probe a log write.
- [DETAIL] Missing logs remain empty snapshots; actual I/O and parsing errors
  propagate. This preserves fixture behavior and keeps the observer honest.
- [DETAIL] (2026-11-14, replacing the exemption-list guard.) The guard
  identifies stand-in logs by the helper's declaration and has no exemption
  list: it fails on `open`, `read_text`, `read_bytes`, `write_text` or
  `write_bytes` of a path that carries a declared name, directly, through a
  variable or through an environment key, in Python and embedded Python
  stand-ins. A path that never carries a declared name, arbitrary
  obfuscation and raw OS calls are outside this bounded static guard's claim
  (decisions.md, "Guard design after the review loop").
- [DETAIL] (2026-11-14.) The lock is the data file's own `flock`, waited for
  at most 60 s before `TimeoutError`: one identity for every spelling of a
  file, no lock file in a fixture repository, and a wedged writer fails a
  reader loudly instead of hanging it.
- [DETAIL] (2026-11-14, loop row L2-2.) The suites clear a declared log by
  removing the file, and the helper offers no locked clear. Because the lock
  is the file's own, a removal splits it: a writer of the cleared run still
  holding the old file's lock finishes its record on the removed file, while
  the next run's writers and readers lock the new file. That split is the
  clear's purpose: the late record must not reach the next run, and the next
  run must not wait on the old writer. A clear that empties the file in place
  under the lock would do both wrong (it waits for the old writer, which then
  appends into the next run's log); a lock taken only around the removal adds
  no guarantee, since the removed file's content is discarded anyway. So
  removal stays the clear, and the guard does not count it as raw access
  (`test_a_cleared_log_starts_fresh_under_a_late_writer`, red on an in-place
  clear with a `TimeoutError`, green on removal).
- [DETAIL] (2026-11-15, decisions.md#Q-5.) A test that must perform the
  unlocked access itself to prove the race test rejects it carries the
  marker `raw_stand_in_log_access(reason=...)`, which suspends the runtime
  check for that one test; a marker without a reason is a usage error. Today
  one test carries it (`test_race_rejects_a_delayed_unlocked_observer`).
  Reason: the planted fault must run for real, and a visible per-test marker
  with its reason is the honest form; reaching the file through an unwrapped
  lower layer instead would hide the bypass.
- [DETAIL] (2026-11-15.) The runtime check raises at the access and also
  records it; a test that passed with a recorded access fails at the end of
  its call phase. Reason: the swarm gates turn an exception into a refusal by
  design, so a raised error alone could vanish, as the original flake did.
- [DETAIL] Deterministic handshakes plus repeated concurrent runs establish
  the regression evidence; sleep-only timing would recreate the same flake.
