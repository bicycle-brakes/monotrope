---
title: "Spec — journal-citation-gate"
status: draft
implementation_status: none
date: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-19
supersedes: null
superseded_by: null
bead: coding-harness-x9ed
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-19"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, provenance]
class: bounded
appetite: 2
adr_files: []
---

# Spec — journal-citation-gate

The existing journal-date check distinguishes real undated citations from patterns and runner-written research records (bead coding-harness-x9ed). Research: `research.md`. Decision: `decisions.md`.

## Problem

On 2026-11-19 the existing tracked-Markdown check treats a glob and paths in runner-written research-swarm records as undated citations, although neither is a hand-written citation (decisions.md, Q-1). The research identifies `tests/test_provenance.py` as the existing enforcer and its current placeholder and date exemptions (research.md, 2026-11-19).

## Terms

**Runner envelope:** a `research-swarm/v2` run from its opening marker through the end of its closing marker, in an active or archived change's `research.md`. Its extents come from the existing research-handoff reader. All envelopes in that file are trusted only when `parse_text` reads the whole file without raising `CannotMeasure`; this is a parse-level verdict, not the later whole-change validation. The trusted extent includes prose outside record fences (Q-1; details S-8–S-10).

**Normalised target:** the captured target after repeatedly stripping trailing sentence punctuation (`.`, `:`, `!`, `?`, `'s`, `'`) and Markdown emphasis markers (`*`, `_`) in any order. All target conditions below use that result (details S-6–S-7).

## Acceptance criteria

1. When a tracked Markdown citation target contains `*` after normalisation, the journal-date check does not report it.
   *Refuted by:* `docs/journal/handover/*.md` is reported as undated.
   *Basis:* decisions.md#Q-1 and detail S-2.
2. When a citation occurs anywhere inside a trusted runner envelope, the journal-date check does not report it.
   *Refuted by:* an undated path in a record or in the envelope's audit prose is reported.
   *Basis:* decisions.md#Q-1 and detail S-5.
3. When a concrete journal citation outside a trusted runner envelope lacks an ISO date in its normalised target, the journal-date check reports it.
   *Refuted by:* an undated hand-written path before or after an envelope, or an emphasised undated path, passes.
   *Basis:* decisions.md#Q-1 and detail S-2.
4. When a normalised journal citation target has an ISO date, is empty, starts with `<`, or is exactly `…` or `...`, the journal-date check does not report it.
   *Refuted by:* a dated citation, directory mention, marker-only target, convention placeholder or elision is reported.
   *Basis:* research.md, existing exemptions; decisions.md#Q-1 and detail S-1.
5. When text is outside an active or archived change's `research.md`, or `parse_text` raises for the file, the journal-date check scans that text without envelope exemptions.
   *Refuted by:* a forged envelope in another file, a nested or unclosed envelope, or a mismatched manifest hides an undated concrete path; or a good envelope is exempt when another envelope in the same file makes parsing fail.
   *Basis:* decisions.md#Q-1 and details S-3 and S-4.

## Non-goals

- A new gate, gate-list changes, or changes to the journal immutability rule.
- Scanning non-Markdown files, changing the runner's output, or repairing other stale provenance references.

## Protected areas

Gate definitions, governance rules, runner code and journal records stay untouched. The existing research-handoff reader may expose spans without changing its parsing verdicts or messages (detail S-10).

## Definition of Done

- `make verify` green; no documents, models or ADRs need changes beyond this change folder.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes bead coding-harness-x9ed and its last commit carries `Closes-Bead: coding-harness-x9ed`.
- Special runs: none.

## Open decisions

[DETAIL] Normalise targets before all checks, so punctuation and emphasis cannot hide concrete citations. Trust whole envelopes only when the existing reader parses the entire change research file, and obtain their spans from that reader, so there is one definition of a runner record (decisions.md, details S-1–S-10).

[DETAIL] The phase-4 appetite is two hours including repairs; it is a stop for this bounded test change.
