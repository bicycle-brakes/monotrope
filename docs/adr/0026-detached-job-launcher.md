---
title: "ADR 0026 — Host detached runner jobs in tmux"
category: adr
status: accepted
created: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, night-run, jobs]
---

# ADR 0026 — Host detached runner jobs in tmux

* Status: accepted by the merge of the pull request carrying this file; until then it is proposed. Supersedes the headless-job non-goals of the night-heartbeat and night-stall-guard changes; amends no numbered D- or O-decision and supersedes no ADR.
* Review: maintainer chose the direction on 2026-11-24 (`decisions.md` Q-1–Q-7) · Decider: maintainer · prepared by Codex.
* Date: 2026-11-24 · takes effect on merge.

## Context

Research on 2026-11-23 found that runner child groups are tied to their launching session and the report does not prove job survival (`plans/changes/detached-job-launcher/research.md`, run 28bf813a). Earlier night-run changes excluded headless jobs; the interview on 2026-11-24 chose a different boundary.

## Decision Drivers

* Jobs survive session exit and can be observed live.
* Verification retains one machine-wide admission and job outcomes remain visible.
* The launcher can travel with the kit across harnesses.

## Considered Options

* A separate tmux window per job and durable records: live observation and survival require tmux.
* A separate process session: fewer prerequisites, but live observation needs another mechanism.
* A launchd job: host-specific service supervision with additional platform coupling.

## Decision

Chosen option: a separate tmux window per job with durable records, because it provides survival and live observation across harnesses. `scripts/jobs.py` starts, lists and stops jobs; model calls remain routed through `scripts/stage2.py`. Verification uses the existing admission. Job records live beside runner state and the report reads them. The launcher does not write lane or busy markers. The existing 30-minute wake remains until `lanes.py advance` lands. The two earlier changes' exclusions of headless jobs no longer apply; their other provisions remain.

## Consequences

* tmux is a prerequisite and missing tmux is reported before launch.
* A durable record and log must outlive the window and correctly represent unknown outcomes.
* Detached jobs may wait for the shared verification admission.

## Validation

* The change's tests exercise session exit, status, stopping, reporting and shared verification admission; `make verify` runs before phase 6.
* A real tmux run and review of the updated night-run guidance confirm the decision before merge.
