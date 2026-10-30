---
title: "Decisions — run-report"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-28
supersedes: null
superseded_by: null
bead: coding-harness-o2yc
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# run-report — Decisions

Class: bounded (one counted interview record or a reasoned skip owed).

## SKIP · interview

status: skipped
reason: the explorer could not read the bead (coding-harness-o2yc), but the orchestrator read it on 2026-10-28, and its description states the change. It adds a new read-only scripts/run_report.py and a make report target. Both read what already exists: the runner's measured time lines and the plan card's appetite in each plans/changes/<name>/plan.md, the Stage-2 call lines in findings.md, and the live process table. The report prints, per change, the attempts with route, model and verdict, and the time used against the appetite. It warns at half the appetite or more. It is local only and shows figures only, never prompt or answer text, and it does not touch scripts/stage2.py. The bead's note adds available memory and the compressor share, plus a warning before a verify-bearing step would start below the floor. The maintainer approved this step on 2026-10-28 ("schnell", as its own change). What is left is the agent's to decide, below.

## Decided by the agent

[DETAIL] **Read the runner's own formats through its own code, read-only.**
The report imports the parsers that `scripts/stage2.py` and
`scripts/stage2_runs.py` already use (`time_log`, the call-line pattern,
the plan card reader) and does not copy their regular expressions. It writes
nothing and changes neither module. Reason: one parser per format, so the
report cannot drift from what the runner writes. `scripts/stage2_runs.py`
sets the precedent.

[DETAIL] **The card's `Appetite:` line is the appetite.** It is read in
hours. A card without a readable appetite prints "appetite not read",
never zero. Time used is the sum of the measured spans under
`## Time used`, the runner's lines and the orchestrator's dated lines alike.
A line the parser cannot read is counted as "unread lines: N". Reason: the
card is the one place a raised appetite is written (fail-fast-attempts did
exactly that on 2026-10-28).

[DETAIL] **Scope: the active change folders.** By default the report covers
every `plans/changes/<name>/` that is not archived; `make report
CHANGE=<name>` narrows it to one. Reason: the archive is history, and the
report exists for the running night.

[DETAIL] **The live part reads the process table and memory, both bounded.**
Processes come from `ps -axo pid,etime,command`, filtered to
`scripts/stage2.py <verb> <change>`, `make verify` and
`scripts/verify_all.sh`. Only the pid, the verb, the change and the elapsed
time are printed, never the rest of a command line. Memory comes from
`memory_pressure` (free percentage) and `vm_stat` (compressor pages) on
macOS, and from `/proc/meminfo` on Linux. A source that cannot be read
prints "not read". The warning floor is 25 % free, the value
coding-harness-p6mu declares. Until that change lands, the report declares
the same constant itself. Reason: the bead's note asks for it, and a missing
source must not look like a healthy reading.

[DETAIL] **Plain text on stdout, exit 0.** One block per change, then the
live block. The report never fails a gate and is not part of `make verify`.
Reason: figures for the orchestrator and the maintainer. No dashboard until
the simple form has held two weeks (maintainer, 2026-10-12).
