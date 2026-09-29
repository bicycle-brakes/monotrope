---
title: "Decisions — reproducible bead export"
category: decisions
created: 2026-09-21
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-21"
review:
  status: pending
  approved_by: null
  approved_at: null
status: accepted
implementation_status: done
date: 2026-09-21
last_reviewed: 2026-09-21
updated: 2026-09-29
bead: coding-harness-1jg.1
---

# Decisions — reproducible bead export

Phase 1a. The interview took place in the session of 2026-09-21; the
maintainer's answers are recorded here.

1. **Three stages, in this order** — answered "do it": (1) the renderer omits
   machine-local fields; (2) the gate file declares where a gate can measure
   and `export-identity` becomes a writer-side gate; (3) target: no committed
   export, hosted CI and local runs render fresh from Dolt. Stages 2 and 3 are
   their own changes (`coding-harness-1jg.2`, `coding-harness-1jg.3`).
2. **Local CI is a complement, not a replacement** for the hosted run; it
   arrives with the Omnigent proof of concept, not in this change.
3. **This change is stage 1 only.**

No `[DECISION]` is open for stage 1. Stage 3 will need the maintainer's
amendment of D-4 and of lakeswitch D-09/D-31; that question belongs to its own
change and is not asked here.
