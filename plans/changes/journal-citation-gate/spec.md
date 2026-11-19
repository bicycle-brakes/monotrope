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

**Runner record:** a fenced `research-swarm/v2` record inside a matching runner-written run envelope. The exemption trusts its contents, as the maintainer accepted in Q-1.

## Acceptance criteria

1. When a tracked Markdown citation target contains `*`, the journal-date check does not report it.
   *Refuted by:* `docs/journal/handover/*.md` is reported as undated.
   *Basis:* decisions.md#Q-1.
2. When a citation occurs inside a runner record, the journal-date check does not report it.
   *Refuted by:* an undated path within a fenced record in a matching run envelope is reported.
   *Basis:* decisions.md#Q-1.
3. When a concrete journal citation outside a runner record lacks an ISO date in its target, the journal-date check reports it.
   *Refuted by:* an undated hand-written path before or after a runner record passes.
   *Basis:* decisions.md#Q-1.
4. When a journal citation target has an ISO date, is empty, or starts with `<`, the journal-date check does not report it.
   *Refuted by:* a dated citation, directory mention, or convention placeholder is reported.
   *Basis:* research.md, existing exemptions; decisions.md#Q-1.
5. When a runner record is unclosed or outside a matching run envelope, the journal-date check does not exempt its contents as a runner record.
   *Refuted by:* an undated concrete path hidden by an incomplete or standalone record is missed.
   *Basis:* decisions.md#Q-1.

## Non-goals

- A new gate, gate-list changes, or changes to the journal immutability rule.
- Scanning non-Markdown files, changing the runner's output, or repairing other stale provenance references.

## Protected areas

Gate definitions, governance rules, runner code and journal records stay untouched: the decision confines this change to the existing check and its tests.

## Definition of Done

- `make verify` green; no documents, models or ADRs need changes beyond this change folder.
- Protected areas untouched and non-goals unbuilt, shown by the pull request file list.
- The pull request closes bead coding-harness-x9ed and its last commit carries `Closes-Bead: coding-harness-x9ed`.
- Special runs: none.

## Open decisions

[DETAIL] Exempt only complete fenced records inside complete matching run envelopes; malformed or standalone markers do not establish runner authorship. This preserves the check outside the trusted record while accommodating the recorded runner format.

[DETAIL] The phase-4 appetite is two hours including repairs; it is a stop for this bounded test change.
