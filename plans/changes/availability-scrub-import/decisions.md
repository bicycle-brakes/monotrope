---
title: "Decisions — availability-scrub-import"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-vg9.2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, stage2, imports]
---

# availability-scrub-import — Decisions

## SKIP · interview

status: skipped
reason: A behaviour-preserving fix with a stated remedy (bead coding-harness-vg9.2, filed at the maintainer's request on 2026-11-24 from a checked analysis): `read_intelligence` in scripts/stage2_availability.py stops importing `stage2` and uses the runner module its caller already holds, as the module's own docstring and the maintainer's decision s9r Q8 (the runner module travels as a parameter) prescribe; no design choice is left to the maintainer.

## Details decided by the orchestrator

[DETAIL] **D-1 (how scrub reaches read_intelligence)**: `read_intelligence` gains a keyword-only `runner` parameter and calls `runner.scrub`; `prepare_research` passes its own `runner`; the existing tests pass the `stage2` module they already import. Reason: the module's documented pattern (the runner travels as an argument), not a new callable parameter.

[DETAIL] **D-2 (the structural check)**: a test reads scripts/stage2_availability.py with `ast` and fails on any `import stage2` or `from stage2 import` anywhere in the module, function-local imports included. Reason: the function-local import is what the bead names; without a check it can come back.

[DETAIL] **D-3 (what stays)**: the error text stored in `reading["status"]` stays exactly as today, redacted by the same `scrub`; no other function changes. Reason: behaviour-preserving fix.
