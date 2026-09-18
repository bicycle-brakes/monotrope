---
title: "CrewAI as a possible coding-harness runtime component"
category: research
status: proposed
created: 2026-09-18
last_reviewed: 2026-09-18
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: codex-sol
  version: "2026-09-18"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [crewai, orchestration, runtime, evaluation]
---

# CrewAI assessment for the coding harness

**Recommendation: defer CrewAI as coordinator.** The proposed target assigns dispatch and observation to Omnigent, work status to Beads, evidence to Git, and final merge to a human. CrewAI can express agent tasks and event-driven flows, but making it the coordinator would reopen the confirmed Omnigent direction and add a second runtime before the M0 proof of concept. A narrower Flow or checkpoint adapter is worth evaluating only when a measured M0 gap calls for it. This is a design assessment, not a failed CrewAI pilot. ([Target state](../architecture/2026-09-17-omnigent-first-target.md), [implementation plan](../architecture/2026-09-17-implementation-plan.md), [CrewAI introduction](https://docs.crewai.com/v1.15.22/en/introduction))

## Scope and checked source

Checked on **18 September 2026**: the upstream `crewAIInc/crewAI` repository, published docs for version **1.15.22**, and the GitHub [1.15.22 release](https://github.com/crewAIInc/crewAI/releases/tag/1.15.22), shown as released on 16 September 2026. The [repository license](https://github.com/crewAIInc/crewAI/blob/main/LICENSE) uses the MIT grant; the [package manifest](https://github.com/crewAIInc/crewAI/blob/main/lib/crewai/pyproject.toml) declares Python `>=3.10,<3.14`. The recent release supports an active-maintenance assessment, but neither release cadence nor documentation proves operational fitness. Main-branch source can change; an experiment must pin its exact release and dependencies.

This review read documentation and repository pages. It did **not** install CrewAI, execute external project code, connect a model, test a sandbox, or use a hosted account. Source-linked capabilities below are documented capabilities; harness-specific controls remain unverified until a pilot.

## Product boundary

The open-source framework supplies [Crews for agent collaboration and Flows for event-driven control](https://docs.crewai.com/v1.15.22/en/introduction). Flow state can persist to local SQLite by default, resume or fork from a state ID, and use a custom persistence implementation. A requested state ID that is missing can fall back silently, so a harness adapter must explicitly reject a missing checkpoint before resuming. ([Flow persistence](https://docs.crewai.com/v1.15.22/en/concepts/flows))

The framework also documents [human-feedback pause and resume](https://docs.crewai.com/v1.15.22/en/learn/human-feedback-in-flows) and [checkpointing for Crew, Flow, and Agent](https://docs.crewai.com/v1.15.22/en/concepts/checkpointing). Automatic checkpoint writes are best-effort: a failed write is logged while the run continues. JSON and SQLite checkpoint providers are local storage options. Those mechanisms are useful execution aids, but do not themselves make a durable Git/Beads handover or prove recovery after host loss.

[CrewAI AMP](https://docs.crewai.com/enterprise/introduction) is a separate managed platform offering deployment, API access, monitoring, and scaling. Credit those capabilities only to a separately selected hosted product. The OSS license does not cover model usage costs or imply hosted service access.

## Fit against the proposed contracts

| Target contract | CrewAI fit and gap |
|---|---|
| Seven-phase change contract | A Flow can sequence stages and branch on outcomes. It has no native coding-harness `spec.md`, `plan.md`, `findings.md`, phase gates, class rules, or canonical verifier. Retain Git artifacts and the single manifest as authority. ([Flows](https://docs.crewai.com/v1.15.22/en/concepts/flows)) |
| Two isolated coding workers | Crews and tasks support agent collaboration and asynchronous work. That is not evidence of separate worktrees, branch ownership, restricted shells and descendants, safe shared Git resources, or candidate assembly. W0 isolation and M0 probes remain necessary. ([Tasks](https://docs.crewai.com/v1.15.22/en/concepts/tasks), [crews](https://docs.crewai.com/v1.15.22/en/concepts/crews)) |
| One Beads writer | Flow persistence stores execution state. It does not establish the target's `tools/bd` use, exclusive writer lock, Dolt transport, run/attempt fencing, or stale-result rejection. An adapter may read Beads snapshots; the authorized coordinator alone updates Beads. ([Flow persistence](https://docs.crewai.com/v1.15.22/en/concepts/flows), [target ownership contract](../architecture/2026-09-17-omnigent-first-target.md)) |
| Human decisions and merge | OSS feedback can pause and resume; its guide calls for an idempotent callback handler. Harness decision records, approval identity, timeout, and human merge still require explicit controls. ([Human feedback](https://docs.crewai.com/v1.15.22/en/learn/human-feedback-in-flows)) |
| Run-wide cost and cancellation | Agents expose `max_iter`, `max_rpm`, `max_execution_time`, and `max_retry_limit`. These are per-agent settings, not a verified total-spend ledger including coordinator, reviewer, workers, retries, and in-flight calls. Process-group termination and quarantining late children need an external supervisor. ([Agents](https://docs.crewai.com/v1.15.22/en/concepts/agents), [target limits](../architecture/2026-09-17-omnigent-first-target.md)) |
| Reproducible evidence and recovery | Checkpoints can resume completed tasks, but automatic persistence can fail without stopping the run. They do not bind gate verdicts to base/candidate SHAs, invalidate a verdict after candidate changes, or provide full Beads restore. Git commits, run records, verifier reports, and a fresh-context packet remain required. ([Checkpointing](https://docs.crewai.com/v1.15.22/en/concepts/checkpointing)) |
| Model and tool boundary | Agent settings include a model, a separate function-calling model, delegation, optional code execution, and context summarization. Every possible model call, tool, log, and telemetry route needs a declared endpoint and safe-fixture probe; settings alone do not prove confinement. ([Agents](https://docs.crewai.com/v1.15.22/en/concepts/agents)) |

## Bounded follow-up

Keep CrewAI outside the M0 critical path. If Omnigent's pinned OSS release cannot provide a required Flow-like primitive, write an ADR for the specific missing function and test CrewAI **inside a disposable synthetic repository**, with its own tracker and no customer content. The experiment should prove all of the following against the same serial/Omnigent fixtures:

1. A pinned version runs under declared model endpoints with verified telemetry and egress; no undeclared model fallback or tool call occurs.
2. Two task attempts retain distinct IDs, worktrees, branches and scopes. A late result and a second tracker writer fail closed.
3. Aggregate budget counts coordinator, workers, reviewer, nested retries and in-flight exposure. Cancellation stops or quarantines descendants; a retry cannot reset the run ledger.
4. Missing/corrupt Flow state and failed automatic checkpoint writes are detected by the adapter. Restart reconstructs the task, SHAs, protected paths, decisions and remaining budget from durable harness evidence.
5. Candidate changes invalidate prior verification and review. Only the human merges the reviewed candidate after current CI evidence.

Compare acceptance success, escaped defects, wall time, total model cost, human minutes and recovery with the existing M0 baseline. Adopt an adapter only if it improves a named outcome without weakening a target control. Otherwise retain the Omnigent-first topology and ordinary-session fallback. ([M0 acceptance and abort criteria](../architecture/2026-09-17-implementation-plan.md))

The unresolved facts are operational: isolation of shells and shared Git state, actual cost accounting across nested calls, cancellation semantics, telemetry egress, and recovery after a failed write or host loss. None was tested in this source review.
