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

**Runner call:** one operating-system process executing the Stage-2 runner, including its concurrent work; a later process is a separate call.

**Distinct notice:** the complete notice text produced by the address assessment, including its model and path pair or wire API, independent of output prefix or stream.

## Acceptance criteria

1. When the same address notice occurs more than once during one runner call, the combined console output contains exactly one occurrence of that notice.
   *Refuted by:* a notice produced by discovery, probing, reporting or dispatch appears zero times or more than once on stdout and stderr combined.
2. When one runner call encounters distinct address notices, each distinct notice appears once in its console output.
   *Refuted by:* a different model, path pair, wire API, or notice kind is suppressed as a duplicate.
3. When a later runner call encounters a notice printed by an earlier call, that notice appears once in the later call's console output.
   *Refuted by:* a previous process prevents the later process from announcing the notice.
4. When concurrent work encounters the same notice during one runner call, the combined console output contains exactly one occurrence of that notice.
   *Refuted by:* simultaneous emitters print it twice or lose it altogether.
5. When a round record or report records an address notice, it retains each distinct notice once in that record even if that notice was already printed in the call.
   *Refuted by:* an earlier console announcement removes a notice from a later round record or report, or a record repeats the same notice.
6. When a research-seat or interactive-session audit records an address notice, it retains that notice even if it was already printed in the call.
   *Refuted by:* console deduplication removes the notice from either audit.
7. When an address notice is printed, its existing wording and the stream of its first occurrence are preserved.
   *Refuted by:* the first occurrence changes its notice text or moves from stdout to stderr or vice versa.
8. When an address assessment admits or refuses a destination, console deduplication leaves that result unchanged.
   *Refuted by:* suppressing a repeated notice changes admission, refusal or the checked destination.

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
