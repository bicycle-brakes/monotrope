---
title: "Findings — availability-scrub-import"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-vg9.2
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — availability-scrub-import

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5784 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/availability-scrub-import/plan.md` +54 -0
> - `plans/changes/availability-scrub-import/spec.md` +60 -0
>
> Diagnostics:
> ```text
> - Runner verification scope: document checks only, no tests ran; result: red; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: ` [… 45 characters left out …]
> - `plan.md` does not open with the plan card (For you:, Done when:, Appetite:, Not now:, Pre-mortem:)
> ```

Stage-2 call, 2026-11-25: draft · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason the first draft attempt failed · leak check clean over 1206 files, 5784 commits, 12 rules.

> Attempt 2 (codex-repair): the runner put back what a draft may not change:
> - `plans/INDEX.md`

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5785 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:fa67c0a0b4bf7950fac6f343c7fdfa855258588368d2f795b20b2d7f31cf95a5

Spec review commit: 8fbce0c1be51ef75d643ad3ca7f9ee3e225fce52

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MINOR | SPEC | base | spec.md, acceptance criterion 2, *Refuted by* | The refutation counts any "credential fragment" in the reading as a failure, but sets no minimum length. The existing redaction (`scrub`, `scripts/stage2.py:882`) replaces only the whole key and fragments of 8 or more characters, and `tests/test_stage2.py:4199` asserts that a 7-character fragment stays. The criterion also requires the change to keep that existing redaction behaviour. Taken literally, the refuting case is already met today: a key fragment of 1 to 7 characters (for example a single letter of the key inside "not read: …") appears in the status, so the criterion is red before anything changes, and fixing that would mean redesigning the redactor, which is a non-goal. The refuting input needs a lower bound, such as the existing test's fragments of 8 to 15 characters at offsets 0, 5 and 9, before this criterion can tell a regression apart from today's behaviour. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-4 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5786 commits, 12 rules.
