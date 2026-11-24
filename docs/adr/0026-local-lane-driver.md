---
title: "ADR 0026 — A local driver starts recorded lane steps"
category: adr
status: draft
created: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, lanes]
---

# ADR 0026 — A local driver starts recorded lane steps

* Status: draft, not a recorded decision. The interview explicitly chose an amendment to ADR 0021 and no new ADR (advance-verb `decisions.md` Q-4); this separate draft is provided for the current draft instruction and does not change that answer.
* Review: maintainer · prepared by Codex; acceptance requires the maintainer's merge.
* Date: 2026-11-24 · takes effect only if accepted on merge.

## Context

Lanes waited for hand starts between 03:20 and 08:00 on 2026-11-24; the next-step producer names work without starting it (`plans/changes/advance-verb/decisions.md` Q-1 and Q-3). ADR 0021 governs the review ladder and its hand-back.

## Decision Drivers

* Continue authorized lane work while retaining the runner's safeguards and one next-step decider.

## Considered Options

* A separate local driver starts a recorded step; it adds an entry point and local state to maintain.
* A person starts each named step; this retains the current boundary but leaves lanes waiting.

## Decision

Proposed: a separate local driver may start only `repair`, `review`, `review-loop`, `release-loop`, `prepare-loop` and `implement` as runner child processes from a recorded instruction. Adding a verb requires a further amendment. The runner retains its checks, locks and stops. The existing recorded answer requires amending ADR 0021, not adding this ADR.

## Consequences

* The driver and its machine-local state require maintenance; the runner remains the next-step decider.

## Validation

* Driver tests cover allowed steps and child invocation; phase-6 review checks the decision text and retained stops.
