---
title: "Findings — admit-qwen4-hy4"
category: findings
status: draft
implementation_status: none
date: 2026-11-16
created: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-x0ph
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — admit-qwen4-hy4

Stage-2 call, 2026-11-16: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1101 files, 4484 commits, 12 rules.

Stage-2 call, 2026-11-16: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1104 files, 4486 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-16

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | `plans/changes/admit-qwen4-hy4/spec.md:33-40` (AC2–AC5); `plans/changes/admit-qwen4-hy4/decisions.md` Q-1 | [AMBIGUITY] The spec doesn't say what happens when the dated reading or the probe goes against one of the two ids. Examples: the Go page shows training other than `Not used`, it has no privacy or request row for the id, the id sits on an unmapped wire API, or its probe fails. Reading A, all or nothing: AC4 and AC5 have no condition, so the change cannot finish. The implementer stops, and the maintainer decides Q-1 again for that id. Reading B, the house precedent: declare the id in `modelle` with a dated skip (`uebersprungen`/`grund`), as `gpt-6-luna`, `claude-haiku-5-5` and `gemini-4-argon` are declared. `test_every_new_paid_model_carries_its_terms_reading` accepts this. AC1 ("declared members") stays green, and AC2/AC3, which start "When either model is admitted", are trivially true for a skipped id. Only AC4/AC5 go red. Reading A ships nothing, or ships one id after a new decision. Reading B ships a declared model that is never selected. A third path, shipping the other id alone, is not ruled out either. | Opus | open | — |
| F-2 | MAJOR | SPEC | base | `plans/changes/admit-qwen4-hy4/spec.md:33-34` (AC2) | [AMBIGUITY] It is unclear which retention value admits a model. AC2 fixes training at `Not used` but asks only for "a dated public-source reading of retention". Its refutation, "non-compliant terms field", doesn't name the rule the field must comply with. Reading A, the machine rule (`terms_problem`, `scripts/stage2.py:2047`): any non-empty `aufbewahrung` admits, so "30 days" or "Not ZDR" passes and the implementer admits the id. Reading B, the maintainer's recorded practice: the `opencode-go` `bemerkung` says "the maintainer admitted all five on 2026-10-17, the 30-day ones included". So retention above 0 days needs its own word from the maintainer, and Q-1's "ja" came before either id's terms were read. Under A a 30-day id ships. Under B the build stops for a question. | Opus | open | — |
| F-3 | MINOR | SPEC | base | `plans/changes/admit-qwen4-hy4/spec.md:33-36`; `plans/changes/admit-qwen4-hy4/spec.md:46`; `plans/changes/admit-qwen4-hy4/research.md` §3 first GAP | The spec doesn't say how a row of the Go page's privacy table or estimated-requests table is matched to the id `hy4` rather than to the admitted `hy4-preview` (or to `qwen4-max`). The tables list display names (e.g. 'MiMo-V2.6-Pro \| Not used \| 0 days'). research.md left open whether `hy4` is a new model or a rename of `hy4-preview`, and the spec keeps `hy4-preview`'s record (1350 requests, read 2026-11-14) unchanged. If the page shows a single Hy4 row, the implementer must decide alone whether it belongs to `hy4`, to `hy4-preview` or to both. AC2/AC3 then pass on a reading that may describe the other model. | Opus | open | — |
| F-4 | MINOR | SPEC | base | `plans/changes/admit-qwen4-hy4/spec.md:33-36` (AC2, AC3) | AC2 and AC3 can only go red against the live Go page, and only on the day it is read. Their refutation, "differs from the source", names no stored evidence that a later check could compare against. The spec requires neither the quoted table row (some existing records carry one, e.g. `mimo-v2.6-pro`'s `quelle`) nor a capture of the page. Once the page changes, a later check (the review loop, phase 6) cannot tell a wrong value from a page update. An unchanged wrong value can no longer be shown at all. The only refuting case is a recorded `anfragen_5h`, retention or training value that differs from the table row on the reading day itself. | Opus | open | — |
| F-5 | MINOR | SPEC | base | `plans/changes/admit-qwen4-hy4/spec.md:39-40` (AC5) | The clause "ordered contrary to that rule" cannot go red within this change. `ordered_models()`/`ladder()` (`scripts/stage2.py:2293`, `scripts/stage2.py:2342`) compute each position from `anfragen_5h`, the declared order of `modelle` does not count, and runner code is a non-goal. So no edit inside the scope can produce a wrong order. The only other refuting case, "absent from the eligible ladder", is already covered by AC1–AC3 (missing id, failed terms, missing value). AC5 has no refuting state of its own. | Opus | open | — |
| F-6 | MINOR | SPEC | base | `plans/changes/admit-qwen4-hy4/spec.md:44-50` (Non-goals, Protected areas); `plans/changes/admit-qwen4-hy4/research.md` §3 last DETAIL | The spec scopes the change to the paid review ladder. But the `modelle_terms` records that AC2/AC3 require also admit both ids to the research swarm. `prepare_research` takes every `modelle_terms` key without the `-free` suffix as a candidate (`scripts/stage2_availability.py:1174`) and fills open Go seats cheapest first, so a high `anfragen_5h` puts either id into research seats. The non-goals ("Do not change runner behavior") and the protected areas neither accept nor rule out this effect. Keeping the ids out of research would need an `ausgeschlossen` entry, which the protected areas forbid. research.md asked "ladder or research-only" as a question for the maintainer, and decisions.md answers only for the ladder. So phase 6 cannot tell whether the changed research-seat selection is in scope or a breach of a non-goal. | Opus | open | — |
