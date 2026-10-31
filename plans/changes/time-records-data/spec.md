---
title: "Spec — time-records-data"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-v6vk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-31"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, time-accounting]
class: bounded
appetite: 3
adr_files: []
neighbours: []
---

# Spec — time-records-data

Runner attempts and orchestrator spans use one writer for fixed-format time
records in the plan, so the report counts both without interpreting prose
(bead `coding-harness-v6vk` — shared time-record writer). Sources:
`research.md` and `decisions.md`, especially the reasoned interview skip and
its three drafting details.

## Problem

As inspected on 2026-10-31 in `research.md`, “What exists today”, the runner
writes a fixed line through `time_entry()` and `persist_time_entry()`, while
interactive sessions follow a prose-writing instruction in
`prompts/04-implement.md`. The report accepts only the runner grammar.
The run-report plan contains measured orchestrator spans that consequently
remain unread; its repeated parsing findings led to the maintainer's
2026-10-29 decision to stop interpreting free text. Widening the reader with
more prose patterns would reproduce that failure. The interview skip settles
the remedy: one writer and one fixed format, retaining old prose as history.

## Terms

- **Record:** a UTC span, explicit elapsed whole seconds, activity, positive
  attempt number, route, model and accepted/rejected outcome, in the existing
  runner line format ending `measured by the runner`.
- **Orchestrator span:** a measured, non-overlapping period of work logged by
  the interactive session, outside time already logged by the runner.
- **Shared writer:** the command's implementation, also callable in-process
  by the runner; it records observed measurements, never estimates them.

## Acceptance criteria

1. When the orchestrator submits a complete measured span through
   `python3 scripts/harness.py time-log`, exactly one record is appended to
   the selected change's plan.
   *Refuted by:* a successful invocation writes no record, writes duplicates,
   or requires manual editing to produce a report-readable line.

2. When either caller records a span, the shared writer emits the existing
   runner format with the supplied activity, attempt, route, model and outcome.
   *Refuted by:* callers use separate formatters, an existing runner record
   changes bytes for identical inputs, metadata is lost, or a midnight span
   omits its end date.

3. When a record is written, its elapsed seconds are the explicitly measured
   duration supplied by the caller, independently of the UTC endpoints.
   *Refuted by:* the writer estimates duration, subtracts endpoints instead,
   or replaces a controlled monotonic duration with wall-clock arithmetic.

4. If the command receives invalid record fields or an unsafe, missing or
   unreadable plan destination, it refuses without altering the destination.
   *Refuted by:* missing fields, invalid timestamps, negative/noninteger
   seconds, nonpositive attempts, an unknown outcome, delimiter/newline
   injection, a path outside the active change, an alias, invalid UTF-8 or
   a missing time heading causes a write or a successful exit.

5. When a record is appended, existing time content retains its order within
   `## Time used`, and following sections retain their content.
   *Refuted by:* earlier runner entries or old prose disappear, a new record
   lands after a following level-two heading, or unrelated plan text changes
   other than the existing `updated:` date stamp.

6. When a completed runner attempt exits its post-call processing, its
   existing exactly-once measurement and recovery contract still holds through
   the shared writer, including its explicit unwritten stop when restoration
   safety refuses the destination.
   *Refuted by:* an accepted or rejected completion loses or duplicates an
   entry, retry loses a prior record, model-written time survives restoration,
   an alias target is written, or logging changes a refusal into fallback or
   checkpoint success; a restoration-safety refusal itself is not a missing
   entry defect.

7. When the report reads records produced by either caller, it counts their
   explicit seconds through the shared format definition.
   *Refuted by:* a command-produced record is unread, an equivalent runner
   record yields different seconds, or the reader maintains a separate grammar
   that disagrees with the writer.

8. While old prose or malformed records remain in the time section, the
   report preserves its unread-count and incomplete-subtotal behavior.
   *Refuted by:* historical prose is rewritten, estimated seconds enter the
   subtotal, unread content silently disappears, or an unreadable section is
   reported as zero measured time.

9. When an interactive session follows the implementation instructions, it
   records measured spans through the command with the same fixed format.
   *Refuted by:* the instructions still require hand-written duration lines,
   request guessed measurements, or direct a model running under Stage 2 to
   add a second entry for an attempt the runner measures.

## Non-goals

- No sidecar, database, JSON store, migration or rewriting of historical lines.
- No expansion of prose parsing, new report gate, appetite enforcement or
  changes to appetite-extension and stop decisions; those notes remain prose.
- No extra time accounting for draft, explore, failed model invocations or
  overlapping orchestration while the runner already measures the work.
- No change to routing, model calls, verification, checkpoint policy or safe
  restoration rules; no concurrent-writer locking service.
- No design document: phase 2b does not run for a bounded change. No ADR.

## Protected areas

`decisions/`, `provenance.yaml`, `model-endpoints.yaml`, `docs/adr/`,
`AGENTS.md`, `README.md`, `templates/`, harness configuration directories and
other change folders remain untouched: this is a writer consolidation, not a
change to governance or historical acceptance criteria. The sole planned held
path is `prompts/04-implement.md`, edited by the orchestrator after the
accepted implementation attempt. `plans/INDEX.md` remains runner-generated.

## Definition of Done

- `make verify` green after the orchestrator's instruction update, with the
  runner recovery regressions and command/report integration tests passing.
- Documentation moved together: `docs/WORKFLOW.md` and
  `prompts/04-implement.md`; this change's spec and plan track the final work.
- Protected areas and non-goals respected by the pull request file list.
- The pull request closes the shared-time-writer bead `coding-harness-v6vk`;
  its final commit carries `Closes-Bead: coding-harness-v6vk`.
- Special runs: deterministic temporary-plan tests only; no live model calls
  needed to prove this change. Evidence in the pull request names its commit.

## Open decisions

None open. The interview skip settles the direction and compatibility policy.

- [DETAIL] Preserve the literal marker `measured by the runner` for both
  entry points because the agreed format is the existing runner format. Here
  it identifies the shared machine writer; route `orchestrator` identifies
  interactive input, whose measured clock readings remain the caller's duty.
- [DETAIL] Require all existing metadata at the command boundary rather than
  inventing it: an orchestrator uses the activity's span number as `attempt`,
  route `orchestrator`, its actual model and the activity's actual outcome.
  These are time records, not additional model-call evidence in findings.
- [DETAIL] Use a three-hour phase-4 appetite, repairs included, because the
  bounded consolidation crosses the command, runner recovery and report.
- [DETAIL] Reject malformed input before writing and share the parser and
  insertion function; this prevents a second writer/reader grammar drifting.
