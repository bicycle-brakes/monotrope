---
title: "ADR 0024 — Implementation attempts continue from protected partial work"
category: adr
status: accepted
created: 2026-11-02
last_reviewed: 2026-11-02
updated: 2026-11-02
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: gpt-6.1-sol, version: "2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, implementation, attempts]
---

# ADR 0024 — Implementation attempts continue from protected partial work

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open
  is proposed, closed is rejected. Adds the implementation-attempt policy
  under ADR 0007's implementation routing; supersedes no ADR and amends no
  D- or O-number. ADR 0017's repair stop rule is unchanged.
* Review: the maintainer's direction recorded in Q-1 and Q-2 of
  `plans/changes/sonnet-continues-flash/decisions.md` (2026-10-16), and Q-3
  through Q-5 (2026-10-31), copied by the orchestrator on 2026-11-02.
  Acceptance is the merge commit; no approval or ADR answer is recorded here.
  Decider: maintainer · prepared by Codex.
* Date: 2026-11-02 · takes effect on merge.

## Context

At `baffe4a3`, inspected 2026-11-02, `scripts/stage2.py` runs implementation
on Flash, then Flash repair, then Sonnet after failed post-run checks. A
model-call error saves the attempt but restores the baseline and stops.
`docs/WORKFLOW.md` says a failed model process stops instead of silently
changing route (`research.md`, exploration of 2026-10-31).

The maintainer chose continuation from protected partial work, counted aborts
and visible route changes. The later visibility answer replaces an earlier
reference to findings.md with runner output and plan.md (Q-5). The separate
repair policy explicitly stops on a failed Codex call (ADR 0017, decision 2);
this package does not amend it.

## Decision Drivers

* Retain work even when an interrupted provider leaves incomplete files.
* Bound attempts to the existing implementation ladder.
* Protect runner inputs and make a budget-changing route transition visible.
* Retain credential, verification, recovery and checkpoint guards.

## Considered Options

* **Continue from a protected copy, visibly** — preserves partial work and
  trusted inputs; owes a fresh environment and an explicit handoff (chosen).
* **Restart from baseline** — gives a clean retry but discards useful work;
  rejected in Q-1.
* **Continue in the same writable worktree** — avoids copying but retains the
  input-damage risk; rejected in Q-1.
* **Stop without reverting after a call error** — retains work but needs a
  manual restart; rejected in Q-2.

## Decision

Chosen option: "Continue from a protected copy, visibly", because it lets the
remaining implementation routes finish partial work without trusting the
previous attempt's edits to runner inputs.

1. A failed implementation model call, including a timeout, consumes one
   scheduled attempt and advances to the next existing route. There is no
   additional retry: Flash, Flash repair, Sonnet. With Stage 2 explicitly off,
   implementation still has just one Sonnet attempt.
2. After a failed call or post-run check, the next implementation attempt
   receives a copy of the preceding permitted work in a fresh environment.
   Its prompt lists cumulative changed paths and the baseline diff, says to
   continue rather than redo, and warns of incomplete files after an abort.
   Runner inputs are restored from committed trusted content before each
   call, retaining the runner's own accumulated records.
3. An aborted state is saved as recoverable attempt evidence. A route change
   caused by that abort shows its reason in runner output and plan.md;
   findings.md is not the route-change record. Its ordinary call audits and
   post-check evidence remain valid runner records.
4. Credential scrubbing, declaration/leak checks, held-path protection,
   tool integrity, unchanged HEAD and safe recovery remain prerequisites.
   A refusal, failed preservation or unsafe promotion stops, rather than
   being treated as a provider error. No failed attempt is accepted without
   the existing checks; exhaustion retains recoverable work and exits red.
5. This qualifies only the implementation part of the workflow's failed
   model-process stop sentence. Draft, repair, explore and review retain
   their own rules. It chooses no container technology and claims no new
   operating-system confinement.

## Consequences

* A provider failure can spend the next already scheduled route's budget,
  visibly, without another manual invocation.
* Later attempts must inspect incomplete work instead of assuming a clean
  baseline; copying and evidence retention add storage and recovery work.
* The shared design is carried into the fresh-copy handoff of this bounded
  package (bead `coding-harness-6ie` — Sonnet continues Flash). Broader
  writing-attempt isolation remains separate (bead `coding-harness-s9r` —
  isolate writing attempts); existing failed-work retention is reused (bead
  `coding-harness-znc` — preserve failed attempts).

## Validation

* The change's criterion ledger maps counted aborts, cumulative copies,
  trusted input restoration, warning, retention, transitions, exhaustion,
  checkpointing and safety stops to deterministic tests.
* Phase 6 checks the workflow against this policy and verifies that repair's
  ADR 0017 rule was not silently widened.
* `make verify` and the decision PR are required before delivery. This file
  is a proposal, not evidence of implementation or of a completed merge.
