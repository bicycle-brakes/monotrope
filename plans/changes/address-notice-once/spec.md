---
title: "Spec — address-notice-once"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-zywb
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2-runner, output]
class: bounded
appetite: 4
adr_files: []
---

# Spec — address-notice-once

Each distinct address notice is printed once per runner call while its durable evidence remains available (bead `coding-harness-zywb`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- On 2026-11-21 the research traced notices through discovery, probes, overlays and dispatch, each of which can announce the same address drift again. An archived round shows eighteen model-specific notices repeated in the next round (`research.md`, “Every emission site” and “The measured volume”).
- The tracker record read on 2026-11-21 reports about 70 lines for 18 models in one preparation call, and a later run repeated an unrecorded-wire-api notice within a call (`decisions.md`, “The bead”).

## Terms

**Runner call:** one invocation of the Stage-2 runner entry point, including its availability and research work and concurrent workers. A later invocation is a separate call, even in the same process. Direct function calls outside an entry retain their current printing behavior.

**Distinct notice:** the complete notice text produced by the address assessment, including its model and path pair or wire API, independent of output prefix or stream.

**Encountered:** an existing console print site would print the notice during the call, including a notice held for a preparation report. Assessment alone does not make a notice encountered.

## Acceptance criteria

1. When the same address notice occurs more than once during one runner call, the combined console output contains exactly one occurrence of that notice.
   *Refuted by:* discovery, probing, reporting or dispatch produces a notice that appears zero times or more than once on stdout and stderr combined.
2. When one runner call encounters distinct address notices, each distinct notice appears once in its console output.
   *Refuted by:* a different model, path pair, wire API, or notice kind is suppressed as a duplicate.
3. When a later runner call encounters a notice printed by an earlier call, that notice appears once in the later call's console output, including when both calls run in the same process.
   *Refuted by:* the first invocation prevents a second invocation from announcing the notice.
4. When concurrent work encounters the same notice during one runner call, the combined console output contains exactly one occurrence of that notice.
   *Refuted by:* simultaneous emitters print it twice or lose it altogether.
5. When a round record or report records an address notice, it retains the notice exactly once in each existing notice section that recorded it before this change, independently of console announcements.
   *Refuted by:* a notice is lost from its section after an earlier announcement, or repeated within that section. The same notice under both existing `Notice:` and `Address notice:` spellings is not a repetition within a section.
6. When a research-seat or interactive-session audit records an address notice, it retains that notice even if it was already printed in the call.
   *Refuted by:* console deduplication removes the notice from either audit.
7. When an address notice is printed outside a preparation report, its existing wording and the stream of its first occurrence are preserved.
   *Refuted by:* the first printed occurrence changes its notice text or moves between stdout and stderr.
8. When an address assessment admits or refuses a destination, console deduplication leaves that result unchanged.
   *Refuted by:* suppressing a repeated notice changes admission, refusal or the checked destination.
9. When a preparation call prints an availability report containing an address notice, the report retains that notice once and earlier console announcements of the same notice are suppressed.
   *Refuted by:* a report omits or repeats a notice it would have recorded, or the same notice also appears earlier in that call's console output.
10. When a probe or measured-model installation records an address notice in its launch audit, the audit retains it independently of console deduplication.
    *Refuted by:* a previously announced notice is missing from the probe audit or installation audit lines.
11. When a notice is emitted by a direct function call outside a runner entry, it prints as before without inheriting another call's suppression.
    *Refuted by:* two independent direct calls that previously printed the same notice no longer both print it.
12. When an assessment produces a notice that no existing console print site would print during the call, that assessment does not cause a console notice.
    *Refuted by:* a refused session binding or an early research-preparation failure prints a notice that previously existed only in audit or selection state.
13. When preparation ends before printing its report, each held notice is printed once using the wording and stream of its first existing console print site.
    *Refuted by:* a notice held from free discovery is lost, repeated, or flushed to stdout instead of its original stderr on an early refusal.

## Non-goals

- Deduplicating terms warnings, changing notice wording or unifying stdout and stderr.
- Combining different models into one drift summary or deduplicating across runner processes.
- Changing the existing `Notice:` and `Address notice:` record spellings, address policy or endpoint declarations.

## Protected areas

`model-endpoints.yaml` and `docs/adr/0024-one-access-policy-for-opencode-go.md` retain the existing address policy and evidence obligation. Other held paths are outside the implementation attempt.

## Definition of Done

- `make verify` green.
- Documents, models and ADRs moved with code: none beyond this change's artifacts.
- Protected areas untouched and non-goals unbuilt, shown by the pull request's file list.
- The pull request closes the output-deduplication work item (bead `coding-harness-zywb`); its last commit carries `Closes-Bead: coding-harness-zywb`.
- Special runs: none.

## Open decisions

None open. [DETAIL] The four-hour phase-4 appetite is a stop including repairs; it keeps this bounded change time-limited. The deduplication scope, evidence and exclusions are recorded with reasons in `decisions.md`.

[DETAIL] A runner call is an entry invocation, not a whole process: embedded invocations need independent output. A direct call outside an entry keeps its existing behavior. When a preparation report is printed, its existing stdout line takes precedence over earlier matching announcements, preserving the report and showing one copy. When preparation exits before the report, only held notices from existing console print sites are flushed, using their first site's wording and stream; an assessment alone does not create a console line. Probe and installation audit lines remain evidence. The two existing round-record spellings are separate sections, each deduplicated independently; this preserves both sources (phase-2a findings S-1 through S-6).
