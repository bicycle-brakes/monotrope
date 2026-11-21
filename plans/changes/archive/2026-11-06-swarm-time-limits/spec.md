---
title: "Spec — swarm-time-limits"
status: accepted
implementation_status: done
date: 2026-11-04
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-ht1b
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, research-swarm, time-limits]
class: bounded
appetite: 2
adr_files: []
---

# Spec — swarm-time-limits

The maintainer can adjust the research swarm's role and whole-run time limits
in one checked-in configuration without changing runner code (bead
`coding-harness-ht1b`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

At baseline `0776b3a6`, inspected 2026-11-04, the research runner fixes five
role allowances in `MINUTES` and the whole-run allowance in `RUN_MINUTES`
(`scripts/stage2_research_run.py`). Changing these values requires editing
code, tests and doctrine. The exploration describes their monotonic deadlines,
the dispatcher's remaining-time clamp and the reserved judge allowance
(`research.md`, "What exists today", item 2).

The interview records finder failures at the existing 600-second limit on
2026-11-04. The maintainer chose a 20-minute finder allowance and a 160-minute
run allowance, and limited this change to the research swarm
(`decisions.md#Q-1`, `decisions.md#Q-2`). Other runner limits are separate work.

## Terms

- **Role limit:** the maximum executing time for one finder, map merge,
  public-topic author, topic researcher or judge, before remaining-time clamping.
- **Run limit:** one monotonic allowance shared by the stages of one research
  invocation; a resumed invocation gets a fresh allowance.
- **Judge reserve:** time within that run allowance withheld from earlier
  stages so the final reconciliation can run; it equals the judge role limit.

## Acceptance criteria

1. When the checked-in configuration is used, its six limits in minutes are
   finders 20, merge 10, sentence 5, topics 10, judge 15 and run 160.
   *Refuted by:* a missing limit, another initial value or a value interpreted
   in another unit.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-2`, and "Decided by the agent".

2. When a fresh or resumed research invocation starts, it captures that
   worktree's current valid configuration once for its duration.
   *Refuted by:* a valid configuration-only edit is ignored on the next
   invocation, a different worktree's values leak into it, or an edit during
   execution changes an already-running invocation's allowances.
   *Basis:* `decisions.md#Q-1`; the capture boundary is the reversible detail
   recorded below.

3. If the configuration is unreadable or invalid, the research invocation
   refuses with exit 2, naming the file and fault, before any research
   participant starts.
   *Refuted by:* a missing file, invalid UTF-8/YAML, ambiguous or incomplete
   schema, or implausible limit starts a participant, causes an uncaught
   exception, or silently substitutes a default.
   *Basis:* `decisions.md#Q-1` requires a strict loader that refuses missing or
   implausible values; the precise validation contract is recorded below.

4. When a research participant is dispatched, its role allowance is the
   corresponding configured number of minutes converted to seconds.
   *Refuted by:* any finder, merge, sentence, repository/free topic researcher
   or judge retains a hard-coded allowance or receives another role's value.
   *Basis:* `decisions.md#Q-1`.

5. When a research invocation starts, its whole-run deadline is its monotonic
   start plus the configured run allowance.
   *Refuted by:* the deadline still uses 150 minutes, uses wall time, resets
   between stages, or carries the previous invocation's spent deadline into
   a resumed run.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-2`; existing run semantics are
   described in `research.md`, "What exists today", item 2.

6. While a research invocation runs, its existing remaining-time enforcement
   reserves the configured judge allowance for every pre-judge stage.
   *Refuted by:* a pre-judge stage uses the former fixed reserve after a judge
   configuration edit, a child receives more than the lesser of its role
   allowance and remaining unreserved time, a stage launches after that time
   is spent, or the judge reserves its own allowance a second time.
   *Basis:* `decisions.md#Q-1`; `research.md`, "What exists today", item 2.

## Non-goals

- Other runner time limits: review rounds, single-model work calls,
  preparation/freezing, probes, catalogs, verification, tools, Git and process
  drain grace periods. Their configuration follows in the separately opened
  work item for other runner limits (bead `coding-harness-phop`).
- New command-line overrides, environment overrides, live reload, automatic
  run-budget growth or fallback values when configuration is unusable.
- Changes to model selection, availability receipts, provider concurrency,
  dispatch order, retry policy, reuse eligibility, report schemas, leak checks
  or cancellation and process-group cleanup.
- A design phase or ADR: this is the interview's bounded configuration
  extraction, so phase 2b does not run and no ADR file is touched.

## Protected areas

`scripts/stage2.py`, `scripts/stage2_availability.py`,
`scripts/stage2_research_dispatch.py` and `model-endpoints.yaml` retain their
existing behavior and contents: this change consumes the dispatcher's existing
interface and adds no admission or routing policy. Gate declarations,
provenance rules, prompts, templates, agent instructions and ADRs are outside
the implementation. Historical decision records are not rewritten.

## Definition of Done

- `make verify` is green; the changed configuration behavior has meaningful
  red-first evidence and the criterion ledger names its checks.
- The same pull request adds `research-swarm-limits.yaml`, its strict loader
  and tests, and updates `docs/WORKFLOW.md` plus the current deadline wording
  in `plans/changes/research-swarm/spec.md` to identify the configuration and
  its units. The latter retains its dispatch, reserve and no-retry guarantees;
  its fixed judge wording becomes the configured judge allowance, initially 15.
- The pull request's file list shows protected areas untouched and non-goals
  unbuilt. The runner generates `plans/INDEX.md` after artifact changes.
- The pull request closes the research-swarm limit configuration work item
  (bead `coding-harness-ht1b`), with `Closes-Bead: coding-harness-ht1b` on its
  closing commit; this draft does not close it.
- No live model call or long-running timeout demonstration is required;
  temporary configurations, injected monotonic clocks and stand-ins hold the
  criteria.

## Open decisions

None open. The following are agent-decided, reversible implementation details;
they make the strict configuration contract explicit without another interview.

- [DETAIL] Use `research-swarm-limits.yaml` at the worktree root, with exactly
  `run_minutes` and `role_minutes`; the latter has exactly `finders`, `merge`,
  `sentence`, `topics`, `judge`. Explicit units and separate storage avoid
  changing the held endpoint declaration for an unrelated timing setting.
- [DETAIL] Require mappings with unique known keys and all six values present;
  each value must be a positive finite integer or float, excluding booleans
  and numeric strings, whose seconds conversion remains finite. Each role
  must be no greater than the run, and the judge must be strictly smaller
  than the run. These relationships reject unusable budgets without imposing
  an arbitrary maximum or requiring enough time for every queued slot.
- [DETAIL] Read once at the start of each invocation and use instance-owned
  settings. This prevents cross-worktree cache leakage and mixed allowances;
  the existing frozen-input drift check remains in force for mid-run edits.
- [DETAIL] Allow two hours for phase 4 including repairs, as a stop rather
  than an estimate; the change is limited to extraction, wiring, tests and
  the directly affected documentation.
