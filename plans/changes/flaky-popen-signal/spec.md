---
title: "Spec — flaky-popen-signal"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-oag7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, signals, stage2-runner]
class: bounded
appetite: 2
adr_files: []
---

# Spec — flaky-popen-signal

Cancellation during process creation leaves no launched child behind and its regression test gives a deterministic verdict (bead coding-harness-oag7). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-19 and 2026-11-20, the process-creation signal test reported a surviving child in Linux CI while a worker was creating it; the 2026-11-19 log said one registered group was killed. A sibling interrupt test also reported a surviving descendant (decisions.md, CI and tracker evidence read 2026-11-21). The worker can be inside process creation before the child is registered when the main thread receives cancellation; the research identifies this window but does not establish the cause of the observed failures (research.md, 2026-11-21).

## Acceptance criteria

1. When the reported failure's cause is established, a controlled regression reproduces that cause against the pre-fix code and records the observed interleaving and baseline failure.
   *Refuted by:* the test merely sends a signal without establishing the relevant ordering, or its recorded pre-fix result passes or fails for an unrelated reason.
2. When cancellation arrives while a timed launch is creating a child on the main thread or a worker, the launched child is stopped and its leader reaped before that launch returns or raises.
   *Refuted by:* a forced interruption leaves the child running or unreaped after the launch finishes, for SIGINT or SIGTERM on either thread.
3. When cancellation stops the runner, a timed launch attempted afterwards starts no program.
   *Refuted by:* a late launch creates its marker or child after cancellation.
4. When an interrupted timed launch has a running descendant in its process group, cancellation stops that descendant and reaps the group leader.
   *Refuted by:* the descendant remains live or the leader remains unreaped after the interrupted launch finishes.
5. When the sibling main-thread interrupt failure is investigated, its relationship to the established cause is recorded with evidence and, if it has a different cause, a separate follow-up is handed to the orchestrator.
   *Refuted by:* the sibling failure is assumed to share the cause without evidence, or an evidenced different cause is left without a follow-up handoff.
6. When the verification runner's process-creation path is assessed for the established race, the result records why that path is affected or not affected and an affected path is protected and regression-tested.
   *Refuted by:* the assessment omits its actual calling thread and cancellation behavior, or an affected path can leave a gate process alive without a failing regression.
7. When the deterministic signal tests complete, their verdicts depend on observed process state and synchronization rather than increased watchdogs, sleeps or retries to conceal the failure.
   *Refuted by:* a passing result requires a longer watchdog, an added timing delay or a retry, or succeeds through the child's natural exit.

## Non-goals

- A retry decorator, CI-level retry, wider watchdog or sleep as a remedy.
- Fixing an unrelated cause of the sibling failure in this change; an evidenced separate cause goes to its own follow-up.
- General process supervision redesign, unrelated verification races, and changes to CI configuration.

## Protected areas

Tracker and held paths are owned by the orchestrator; the implementation attempt must not edit them. Unrelated signal handlers and other test families stay unchanged except where necessary to preserve the specified cancellation behavior.

## Definition of Done

- The controlled pre-fix failure and post-fix result, cause, sibling assessment and verification-runner assessment are recorded in the pull request with the tested commits.
- `make verify` green; no ADR or external document changes are required.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes bead coding-harness-oag7 and its last commit carries `Closes-Bead: coding-harness-oag7`.

## Open decisions

[DETAIL] The phase-4 appetite is two hours including repairs; this bounds the investigation and implementation without prescribing the cause.

[DETAIL] The reproduction must control the ordering while keeping an independent release path for any thread blocked by the signal handler; this prevents the test barrier itself from deadlocking the run.
