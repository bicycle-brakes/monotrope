---
title: "Decisions — verify-machine-lock"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-p6mu
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# verify-machine-lock — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).

## SKIP · interview

status: skipped
reason: the bead (coding-harness-p6mu) carries the maintainer's direction of 2026-10-28 and answers the research's three decision questions. A second run waits in a queue and is not refused ("so concurrent lanes queue instead of overlapping"). The wait does not count against the runner's step limit and is logged. The scope is make verify through scripts/verify_all.sh, the runner's post-run make verify and its cheap pytest check. A memory floor makes a run wait instead of starting. Foreign-model calls stay parallel. The maintainer said "sowas wie eben darf nicht mehr passieren" (a memory stop must not happen again) and put the change first in the night plan of 2026-10-28/29. What is left is the agent's to decide, below. No answer is needed at night.

## Decided by the agent

[DETAIL] **A second run waits; it is never refused** (research question 1).
The bead asks for a queue. The wait is logged when it starts and again every
five minutes. It names the holder: process id, the command, and since when.
Reason: a refusal would push the queueing back onto the orchestrator, which
is the manual rule this change replaces.

[DETAIL] **One lock per user per machine, in the state directory**
(research question 2). The lock is `${XDG_STATE_HOME:-~/.local/state}/coding-harness/verify.lock`,
taken with an exclusive `fcntl.flock`. The kernel releases it when the
holder exits, even on a kill, so a stale lock cannot block the queue. It is
keyed by the machine, not the repository: the memory it protects is the
machine's, and every worktree shares it. The precedent is the loop record
under the same directory. Reason: `$TMPDIR` would also work, but one
directory for all runner state is easier to find.

[DETAIL] **Nested runs pass through the lock instead of waiting for
themselves** (research question 3). The holder exports
`HARNESS_VERIFY_LOCK_HELD=<pid>` to its children. A verify-bearing entry
that sees the variable runs without taking the lock. This covers the
runner's own `make verify` and the test suite's runner-copy runs inside a
held verify. The hosted CI runs one job per machine and needs no opt-out.
The variable has one meaning, held by an ancestor, and turns nothing off.
Reason: an opt-out flag could be set by mistake and silently drop the
protection. The held marker only ever covers a run that already sits inside
a held lock.

[DETAIL] **`make test` by hand is not covered** (research question 4). The
bead names three entries, so this change wraps those three. A hand run of
`make test` is the orchestrator's own act, and it stays under the night
rule. It can join later with one line. Reason: keep the change to the named
scope.

[DETAIL] **Memory floor: wait at 25 % free, bounded at 60 minutes.** After
taking the lock and before starting, the run reads available memory. On
macOS that is `memory_pressure`'s "System-wide memory free percentage". On
Linux it is `MemAvailable / MemTotal` from `/proc/meminfo`. Below the floor
the run waits and re-reads every 30 seconds, logged. If memory has not
recovered after 60 minutes, the run is refused with the floor and the last
reading named. It never starts below the floor. A reading that cannot be
taken is logged and does not block, so a machine without either source keeps
working. The floor and the bound are constants declared in one place.
`HARNESS_VERIFY_MEMORY_FLOOR` overrides the floor for a measurement. Reason:
the maintainer ruled out a memory stop. Waiting for a bounded time and then
refusing honours that rule, and an unbounded wait would hang a night run
without a word. The 25 % is a starting value: 50 % free was read
on 2026-10-28 at about 21:30 UTC; a reading during the memory stop was not
taken. The
run report (coding-harness-o2yc) will show whether the value holds.

[DETAIL] **First come, first served; no priority for runner attempts.** The
bead's note of 2026-10-28 gave a runner attempt's verify priority, because
the step limit could kill it while it waited. This change takes the wait out
of the step limit, so priority is no longer needed for correctness. A plain
queue is simpler to test. Reason: the stated risk is gone without a second
mechanism.

[DETAIL] **Foreign-model calls are untouched.** Only the three local entries
take the lock (bead, point c).
