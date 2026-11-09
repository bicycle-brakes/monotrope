---
title: "Spec — adr-repair-check"
status: draft
implementation_status: none
date: 2026-11-08
last_reviewed: 2026-11-08
updated: 2026-11-08
supersedes: null
superseded_by: null
bead: coding-harness-firy
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, adr, repair, verification]
class: architectural
appetite: 1
change: adr-repair-check
adr_question: {proposed: "yes", reason: "The runner's check after a repair changes, which ADR 0021 decision 6 states."}
adr_files: [docs/adr/0025-targeted-check-after-repair.md]
---

# Spec — adr-repair-check

The goal in one sentence: ADR 0021 decision 6 states the verification rule
that pull request #343 (bead coding-harness-gxwg) enforces, so a reader of
the ADR meets the current gate.

## Scope

ADR 0025 amends ADR 0021 decision 6. It records the maintainer's answers of
2026-11-08 (`decisions.md`, Q-1 to Q-5) and nothing else. No code changes;
the runner behaviour lands with pull request #343.

## Acceptance criteria

1. ADR 0025 states the targeted check after a runner repair as decided.
   *Basis:* decisions.md#Q-1
2. ADR 0025 states when the full `make verify` runs instead.
   *Basis:* decisions.md#Q-2
3. ADR 0025 requires one fresh green full `make verify` on the reviewed head
   before phase 6, with audit lines in `findings.md` exempt.
   *Basis:* decisions.md#Q-3
4. ADR 0025 names the measurement over five changes or two weeks and its
   report to the maintainer.
   *Basis:* decisions.md#Q-4
5. ADR 0025 holds from its merge and names the testing-strategy spike as the
   place that may amend it.
   *Basis:* decisions.md#Q-5

## Definition of Done

- The decision pull request carries ADR 0025 and this change folder.
- The gates `interview-minimums` and `question-context` are green.
- The maintainer merges it together with or right after pull request #343.
