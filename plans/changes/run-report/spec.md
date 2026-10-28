---
title: "Spec — run-report"
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
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, run-report]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — run-report

Provide a local, read-only text report of active changes' recorded attempts,
time against appetite, and current process and memory figures (bead
`coding-harness-o2yc` — run report). Sources: `research.md` and `decisions.md`.

## Problem

- Attempt evidence and measured time are scattered between audit lines,
  plans and ephemeral console output; no existing report presents the
  running changes' time against their plan-card appetite (research,
  exploration of 2026-10-28 and gap check at `6daf7b17`).
- The existing post-hoc counter reports review and call counts, not current
  work or memory. The recorded brief asks for an early resource warning
  without changing runner behavior (decisions, interview skip of 2026-10-28).
- Historical plans contain unmeasured or narrative time entries; an absent
  measurement cannot safely mean zero (research, draft gap check).

## Terms

- **Appetite:** the positive phase-4 time budget in the opening plan card's
  `Appetite:` line, expressed in hours; the frontmatter is not its substitute.
- **Recorded time:** the sum of readable measured durations under
  `## Time used`, including accepted and rejected attempts and dated
  orchestrator records; it excludes live-process elapsed time.
- **Live figures:** a dated snapshot at report invocation, not continuous
  monitoring or a promise about a later start.

## Acceptance criteria

1. When `make report` runs without a change selection, it prints one block
   per active change folder in name order, followed by one live-figures block.
   *Refuted by:* an active folder is omitted, an archived folder is included,
   the ordering varies, or the live block is missing or repeated.

2. When `make report CHANGE=<name>` selects an active change, only that
   change and the live block are reported; an unavailable or invalid selection
   is identified without falling back to all changes.
   *Refuted by:* another change appears, a missing change looks empty and
   healthy, or a selection escapes the active-change directory.

3. When attempt records are readable, their report shows the recorded verb,
   attempt number, route, model and verdict wherever present, retaining calls
   from `findings.md` even when they have no measured completion.
   *Refuted by:* a rejected attempt disappears, a clean leak check becomes an
   accepted verdict, missing fields are invented, or a repeated attempt number
   in a later invocation overwrites an earlier attempt.

4. When a time section contains measured runner or dated orchestrator
   durations, its total counts each readable duration record once regardless
   of verdict, without adding call lines or live elapsed times to the sum.
   *Refuted by:* a fixture with 600 accepted, 900 rejected and 300 orchestrator
   seconds totals anything other than 1800 seconds, or a following section
   contributes time.

5. If a time record cannot be read as a measured duration, the report states
   `unread lines: N` and marks any readable subtotal as incomplete.
   *Refuted by:* prose supplies a guessed duration, an unread record silently
   vanishes, or an unreadable or missing section is presented as a measured zero.

6. When the opening card supplies a readable appetite, the report compares
   recorded time with that appetite in hours and warns at 50 percent or more.
   *Refuted by:* 1799 seconds warns against a one-hour appetite, 1800 does
   not, rejected time is excluded, or a contradictory frontmatter budget wins.

7. If the card's appetite is absent, unreadable or non-positive, the report
   says `appetite not read` without a fabricated ratio or threshold verdict.
   *Refuted by:* a missing card becomes a zero budget or a healthy percentage.

8. When the process table is readable, the live block shows matching runner
   invocations and verification processes using only process identifier,
   verb or verification label, change when known, and elapsed time.
   *Refuted by:* unrelated processes appear, a supported runner invocation is
   missed, or command arguments beyond those fields appear in the report.

9. When supported memory readings are available on macOS or Linux, the live
   block shows the available-memory percentage and compressed-memory share
   with its denominator or unit; an unavailable component says `not read`.
   *Refuted by:* compressed logical pages are presented as resident compressor
   usage, a missing compressed-memory source becomes zero, or a percentage
   lacks a defined physical-memory denominator.

10. When readable available memory is below 25 percent, the report warns
    against starting a step that runs verification, without starting or
    blocking that step itself.
    *Refuted by:* 24 percent produces no warning, 25 percent produces the
    below-floor warning, or the report starts, stops or locks verification.

11. If a file or system source is missing, malformed, inaccessible or times
    out, the report identifies that source as `not read`, continues with
    independent readable sources, and returns zero after printing its report.
    *Refuted by:* a failed process probe suppresses valid change totals, a
    missing memory tool hangs the report, or an exception traceback replaces
    a source-specific diagnostic.

12. While the report runs, it only reads local inputs and prints summary
    fields to standard output, without exposing prompt, answer or raw
    diagnostic text or changing repository, tracker or runner state.
    *Refuted by:* a sentinel in diagnostic prose or an unrelated process
    argument reaches output, an input changes, a model or network call runs,
    or reporting is added as a verification gate.

## Non-goals

- A dashboard, persistent report artifact, watch mode, archived-change report,
  token or cost accounting, or recovery of measurements never recorded.
- Automatic pre-step hooks, memory-based admission, verification locking,
  process termination, or changes to runner routing and time writers.
- Perfect interpretation of narrative time logs, inferred completion verdicts,
  or inferring a verification process's change from unrelated processes.
- Design and ADR documents: phase 2b does not run for this bounded change.

## Protected areas

`scripts/stage2.py`, `scripts/stage2_runs.py` and all other existing runner
modules remain unchanged: this adds a consumer of their formats.
`decisions/`, `docs/adr/`, `prompts/`, `templates/`, `AGENTS.md`, `.beads/`,
model configuration and other changes' artifacts are outside the scope.

## Definition of Done

- `make verify` green, including deterministic tests of these criteria.
- Documentation moved with code: `docs/WORKFLOW.md` describes invocation,
  thresholds, partial readings and the advisory boundary; this change's
  artifacts carry the implementation and review evidence.
- The PR file list respects the protected areas and non-goals; the runner
  regenerates `plans/INDEX.md` as derived metadata.
- The PR closes the run-report bead `coding-harness-o2yc`; its final commit
  carries `Closes-Bead: coding-harness-o2yc`.
- Special runs: no live model calls; report tests use injected system
  readings, with evidence and the tested commit recorded in the PR.

## Open decisions

None open. The following reversible details are chosen by the agent, with
their reasons, within the recorded brief:

- [DETAIL] Two hours of phase 4, including repairs, is the appetite: a stop
  for this bounded reader and its integration, not an estimate.
- [DETAIL] An incomplete time subtotal may still trigger the half-appetite
  warning when it already reaches the threshold; below it the report makes
  no claim that unrecorded work leaves budget available.
- [DETAIL] Use existing section/card checks and call-line constants, with
  report-local field extraction where no shared reader exists; the gap check
  shows that importing a complete duration or appetite parser is impossible.
- [DETAIL] Resource warnings are snapshots to read before a verify-bearing
  step, because an automatic pre-step interlock would change runner behavior
  beyond the read-only scope settled in `decisions.md`.
