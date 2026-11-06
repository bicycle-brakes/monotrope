---
title: "Decisions — verify-worker-count"
category: decisions
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-xay1
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, spike, verify]
---

# verify-worker-count — Decisions

Class: spike (bead coding-harness-xay1).

## SKIP · interview

status: skipped
reason: The maintainer chose this item on 2026-11-05 (change verify-duration, phase-6 row F6-2, option A), and the bead (coding-harness-xay1) fixes the subject the research could not read: subject (a) — make the actually started pytest-xdist worker count visible per run (read from the xdist session, or a baseline option that prints it), measure it on at least five runs, and add it to docs/research/2026-11-04-verify-duration-baseline.md as a dated addendum. The sizing trade-off (default 4 against -n auto) and the hosted runner are out of scope and stay as recorded in verify-worker-cap. No choice is left open before the measurement.
