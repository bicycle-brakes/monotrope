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

1. When the process-creation failures' cause is established, a controlled regression for each recorded worker parametrization, SIGINT (run 44591912821) and SIGTERM (PR #418), reproduces the cause against the faulty pre-fix production code or test helper and records the ordering and baseline failure of each case.
   *Refuted by:* either case lacks its own controlled pre-fix failure, does not establish the relevant ordering, or fails for an unrelated reason.
2. When cancellation arrives while a timed launch is creating a child on the main thread or a worker, cancellation stops the child and reaps its leader before the launch returns or raises, before the child's natural exit or the launch's timeout, and, for a worker, within two seconds after `Popen` returns once the run is cancelled.
   *Refuted by:* for SIGINT or SIGTERM on either thread, the child survives cancellation, exits naturally or times out, is unreaped when its launch finishes, or, on a worker, is still running or unreaped two seconds after `Popen` returns after cancellation; the worker is joined before its verdict.
3. When cancellation stops the runner, a timed launch attempted afterwards starts no program.
   *Refuted by:* a late launch creates its marker or child after cancellation.
4. When an interrupted timed launch has a running descendant in its process group, cancellation stops that descendant and reaps the group leader.
   *Refuted by:* the descendant remains live or the leader remains unreaped after the interrupted launch finishes.
5. When the sibling main-thread interrupt failures are investigated, the relationship of each recorded failure to the established cause is recorded with evidence.
   *Refuted by:* the Terminated failure on PR #404 or the KeyboardInterrupt failure on PR #419 is assumed to share the cause without evidence, or a recorded sibling failure is omitted.
6. When the verification runner's process-creation path is assessed for the established race, the result records why that path is affected or not affected and an affected path is protected and regression-tested.
   *Refuted by:* the assessment omits its actual calling thread and cancellation behavior, or an affected path can leave a gate process alive without a failing regression.
7. When the existing process-creation signal test and any sibling case explained by the same cause complete, their verdicts depend on observed process state and controlled ordering rather than timing workarounds.
   *Refuted by:* the existing flaky test remains uncontrolled, a passing result requires a longer watchdog, an added timing delay or a retry, or succeeds through the child's natural exit.
8. If a sibling failure has a different established cause, a `Follow-up for the orchestrator` section in the change's `findings.md` attempt record names the cause, evidence and test IDs.
   *Refuted by:* an evidenced different cause has no such handoff or lacks any of those details.
9. If the cause cannot be established and reproduced within the two-hour appetite, the attempt stops without committing a speculative fix or test change and records the interleavings tried, the result of each, and what was not tried under `Stopped without a cause` in the `findings.md` attempt record for the orchestrator.
   *Refuted by:* the attempt continues past the limit, commits a speculative change, or omits the named section or any of its three contents.
10. If the established cause is solely in the test's cleanup or liveness verdict, the evidence records why production cleanup is safe for the observed ordering.
    *Refuted by:* the test alone is changed without evidence of production cleanup and reaping for that ordering.

## Non-goals

- A retry decorator, CI-level retry, wider watchdog or sleep as a remedy.
- Fixing an unrelated cause of the sibling failure in this change; an evidenced separate cause goes to its own follow-up.
- General process supervision redesign, unrelated verification races, and changes to CI configuration.

## Protected areas

Tracker and held paths are owned by the orchestrator; the implementation attempt must not edit them. Unrelated signal handlers and other test families stay unchanged except where necessary to preserve the specified cancellation behavior.

## Definition of Done

- For a completed fix, the controlled pre-fix failure and post-fix result, cause, sibling assessment and verification-runner assessment are recorded in the pull request with the tested commits. If the cause is not established and reproduced by the appetite limit, criterion 9 governs the stopped attempt instead.
- If the cause is established and reproduced but the fix is unfinished at the appetite limit, the attempt stops and the findings attempt record gives the evidence, work completed and remaining, without committing an unverified fix.
- `make verify` green; no ADR or external document changes are required.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes bead coding-harness-oag7 and its last commit carries `Closes-Bead: coding-harness-oag7`.

## Open decisions

[DETAIL] The phase-4 appetite is two hours including repairs; this bounds the investigation and implementation without prescribing the cause.

[DETAIL] The reproduction must control the ordering while keeping an independent release path for any thread blocked by the signal handler; this prevents the test barrier itself from deadlocking the run.

[DETAIL] The cancellation guarantee is per launch call, not the return of the runner's main function; joining the worker before judging its child measures that contract.

[DETAIL] Worker cancellation has a two-second bound after `Popen` returns once cancellation has occurred; this distinguishes cancellation cleanup from a later natural exit or launch timeout (phase-2a finding S-7).

[DETAIL] If the appetite expires after reproduction but before a finished fix, the attempt reports its evidence and remaining work without committing an unverified fix; this makes the stop reviewable without treating a reproduced cause as an absent one.
