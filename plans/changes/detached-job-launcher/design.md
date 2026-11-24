---
title: "Design — detached-job-launcher"
category: design
created: 2026-11-24
status: draft
implementation_status: none
date: 2026-11-24
last_reviewed: 2026-11-24
updated: 2026-11-24
supersedes: null
superseded_by: null
bead: coding-harness-a6ns.1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-24"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [design, jobs, night-run]
---

# Design — detached-job-launcher

## Alternatives

- A tmux window per job with a durable record: observable across sessions, with tmux as a prerequisite.
- An independent process session: fewer dependencies, but live observation and lifetime management require separate facilities.

Chosen: tmux and durable records, as the maintainer chose in `decisions.md` Q-2 and Q-4; merge of the decision pull request gives it effect.

## Interfaces

- Caller → `scripts/jobs.py`: start accepts any argument vector and the caller environment, list reads records, stop identifies one job; arguments must retain their boundaries.
- Launcher → tmux: the dedicated `coding-harness` server starts detached if absent; one unique window hosts a wrapper and the command; the wrapper owns terminal result publication after the launcher exits.
- Wrapper → state store: a unique record and log persist under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/jobs/`; report reads them without writing lane state.
- Command → verification: verification enters the existing `verify_lock` path itself with all four inherited admission values cleared; the launcher neither pre-acquires nor bypasses the admission.
- Kit → destination: launcher and its imports travel as mechanisms; tmux remains a host prerequisite.

## Data model

One JSON record per generated job ID stores the argument vector, runner-verb classification, working directory, started command PID, wrapper PID, recorded process group, window identity, start time, end time, exit code or signal, and log path. The launcher creates it before launch; the wrapper atomically publishes completion. A missing completion is not proof of success: list reports `lost` when the wrapper PID is gone. Stop ends the command tree but spares the wrapper to record `signal 15` and exit. Finished records are kept 14 days; the default list shows running jobs and the last 24 hours, lost records remain visible until pruned 14 days after start, and `--all` shows all retained records. The log captures both output streams. Distinct IDs and atomic replacement prevent simultaneous jobs from overwriting one another.

## ADR draft

The proposed decision is `docs/adr/0026-detached-job-launcher.md`; its acceptance is the merge, not this draft.

## Architecture delta

```mermaid
flowchart LR
    person["Person: orchestrator"] --> launcher["Component: job launcher"]
    launcher --> tmux["Container: tmux job windows"]
    tmux --> runner["Component: stage-2 runner"]
    tmux --> records["Container: job records and logs"]
    report["Component: run report"] --> records
    runner --> admission["Component: verify admission"]
```

**Added**

- Launcher, per-job tmux window and durable job records and logs.

**Changed**

- The report also reads job state and deduplicates by started command PID; detached runner commands retain the existing verify admission.

**Removed**

- Only the restriction on detached runner jobs in the two earlier night-run non-goals, once the decision is merged.
