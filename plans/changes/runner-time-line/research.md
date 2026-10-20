---
title: "Research — runner-time-line"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-9wp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# runner time line — Research

Phase 1 by the orchestrator (Opus 5.5), read at `origin/main` `94ae6cc`; the
runner's explore route is not used because with `--stage2-off` it answers with
no research (bead coding-harness-e7m).

## The problem, measured

In the research-swarm change (PR #158), phase-6 rounds 10 and 11 on
2026-10-20, all six runner repair attempts were rejected although their code
was correct: each repair was later booked by hand after a red-first check and
a green full `make verify`. Every attempt failed on one or both of two causes:

1. `plan.md did not add a measured line below ## Time used` — all six.
2. A wall-clock test that lost its bound under load (load average 13 to 22) —
   four of six. Those tests exist only on the research-swarm branch; they are
   repaired there (bead coding-harness-9wp, part 2), not in this change.

## Where the time line is demanded today

- `verify_attempt` (`scripts/stage2.py:3035`) compares the time section with
  the pre-call `baseline_time` and fails the attempt when no line was added
  (`:3069–3075`). It is called from the shared attempt loop (`:3804`), which
  serves `implement` and `repair`.
- The prompts ask the model for the line: `REPAIR_FORMAT` (`:252`), the
  implement prompt (`:3646`), and the file-tools repair variant.
- `time_log` (`:2572`) and `insert_before_time` (`:2584`) keep the section
  and the stage-1 route block apart, so a route block cannot satisfy the check.
- `prompts/04-implement.md:33–45` defines the line's form:
  `<date> <start>–<end>, <span>[, break counted]`, read from `date`, never
  estimated. `docs/WORKFLOW.md:748` says the runner checks for it.
- `:3879` and `:4260` require the heading before a model call; that stays.

## Why the model cannot meet the demand

The Flash and Sonnet routes have no shell, so they cannot read `date`
(their own entries say "Span not measured: this session had no command tool").
Codex has a shell but did not write the line in any of four attempts. The
runner itself knows each attempt's start (before the call) and end (after
`make verify`), so it can measure what the prompt forbids the model to guess.

## What the change touches

- `verify_attempt` / the attempt loop: measure start and end with the
  runner's clock; on a passing attempt write one line under `## Time used`
  in the prompt's form, naming verb, attempt, route and model and
  "measured by the runner"; drop the added-line check.
- The three prompt sentences that ask the model for the line.
- `docs/WORKFLOW.md:748` and `prompts/04-implement.md` wording for runner
  attempts (an interactive session still writes its own line).
- `tests/test_stage2.py`: about 26 places name the time section; the tests
  that assert the refusal become tests that assert the runner's line.

## Questions

- `[DECISION]` answered (maintainer, 2026-10-20, Q-1 in `decisions.md`):
  the runner writes the line; no retry of red tests in the runner.
- `[DETAIL]` Whether a failed attempt also gets a line: yes — time spent on a
  rejected attempt counts against the appetite as well; it lands in the same
  section, marked "rejected".
