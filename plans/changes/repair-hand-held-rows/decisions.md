---
title: "Decisions — repair-hand-held-rows"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-0zhf
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, repair, stage2-runner]
---

# repair-hand-held-rows — Decisions

Class: bounded (bead coding-harness-0zhf; maintainer decision 2026-11-21: "file as P1 bounded").

## SKIP · interview

status: skipped
reason: The maintainer fixed the shape when filing the bead on 2026-11-21 (morning handover of night run 2026-11-20-a, "Needed from the maintainer" item 6(b), and the bead description): "Before a repair attempt, the runner classifies each taken row by the paths its Where names (RUNNER_HELD / uncommittable), repairs only the rows it can commit, and names the held rows as an orchestrator hand step in its answer and findings record." The evidence is the three full restores of that night (findings-per-model F6-1 on AGENTS.md, mandatory-spec-review L5-4 on model-endpoints.yaml, ledger-ids-before-pytest L2-1 on prompts/04-implement.md). On 2026-11-21 the maintainer also asked for no question windows during the following four hours of the day run. No choice is left for the interview; the open points the explore named are [DETAIL] items below, decided by the orchestrator with their reasons, and the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Scope: the repair verb only.** `implement` and `draft` share `checkpoint()`/`uncommittable()`, but the bead names "a repair attempt" and all three restores were repairs. Reason: smallest slice that removes the measured cost; the other verbs keep today's behavior.
- **Classification source: the existing pair `_held_prefixes`/`uncommittable` (`scripts/stage2.py`), applied to the paths a taken row's `Where` cell names.** No second list. Reason: one path, one rule (the classification the checkpoint already enforces after the attempt now runs before it).
- **Batch split.** Committable taken rows are repaired in the attempt; held rows are not sent to the model at all. If every taken row is held, the verb makes no model call and exits 0 with the hand-step listing (an intended outcome, not a refusal; corrected after spec-review S-4). Reason: the bead's "repairs only the rows it can commit".
- **A row whose `Where` names no readable path stays with the model,** as today. Reason: only a named held path is evidence the attempt would be restored.
- **Hand-step record.** The runner names each held row (id, held path, the reason "runner-held path") in its answer and appends the same listing to `findings.md` once, before the attempt loop (spec-review S-3); it does not change the row's Status. Reason: the Status and the `Broke a test` mark stay the orchestrator's marks (`docs/WORKFLOW.md`, repair section). The orchestrator books a held row after its hand edit in one of the valid forms (spec-review S-14): when no test fits (text and config files) it retakes the row as `taken — not a test` and books `fixed — not a test — orchestrator hand edit <sha>`; otherwise it books a `fixed — tests/<path>::<function>` form.
- **The checkpoint stays as the safety net.** A model that still writes a held path is restored exactly as today. Reason: the pre-classification can miss a path a row's `Where` does not name.
