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

[DETAIL] **D-4 (spec review F-1, fragment length)**: criterion 2's refutation counts the whole key or a fragment of 8 or more characters, the threshold `scrub` already applies (`scripts/stage2.py` `scrub`; `tests/test_stage2.py` keeps a 7-character fragment); shorter fragments are outside the criterion. Reason: the change keeps the existing redaction and must not demand more than it.

[DETAIL] **D-5 (spec review F-2, which fragment)**: reading (a) — the criterion concerns the credential text the exception carried: neither the whole key nor any run of eight or more of its characters that the exception message contained may survive into the reading; the test injects such a fragment and checks it is replaced. Reason: `scrub` redacts what it is given; the reading cannot contain credential text the exception never carried.

[DETAIL] **D-6 (spec review F-3, the substituted redactor)**: reading (a) — the test passes a stand-in runner object (not the module importable as `stage2`) whose `scrub` returns a sentinel, and asserts the reading carries the sentinel, so a reader that ignores its `runner` and imports `stage2` goes red. Reason: only that construction catches the defect the Problem names.

