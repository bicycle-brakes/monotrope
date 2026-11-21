---
title: "Decisions — contract-real-pi-data"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-z4oo
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, pi, contract-tests]
---

# contract-real-pi-data — Decisions

Class: bounded (bead coding-harness-z4oo).

## The bead (read from the tracker by the orchestrator, 2026-11-21)

> Why: two findings of one mechanism on 2026-11-01. (1) bead coding-harness-xul8: the neutral-path extension was tested against a hand-made prompt; the pinned Pi 1.2.0 hands before_agent_start an already rendered prompt, so the live run failed closed. (2) bead coding-harness-4tr4, review row L7-1: the session lookup was tested against a synthetic catalog with bare keys; the pinned catalog (tools/pi/.../pi-ai/dist/providers/data/opencode-go.json) keys every model with 'chat:', so every real Go session would refuse. AGENTS.md: a second finding of one mechanism ends case repair. What: every test that stands in for a Pi file format or hook payload also runs once against the pinned installation's real file or a real rendering (skipped with a reason when Pi is not installed), so a format drift goes red in make verify.

The explore ran with `--stage2-off` (Sonnet) because GLM 5.3 Flash refused twice with `unrecognized_model` (bead coding-harness-b5pu).

## SKIP · interview

status: skipped
reason: The bead fixes the mechanism, the two cases and the remedy; the maintainer asked for no question windows until the block on 2026-11-23 10:00. The explore's open points are [DETAIL] items below; the maintainer's veto on the Plan Card stays.

## [DETAIL] items decided by the orchestrator

- **Scope: an inventory first.** The spec lists every test that builds a stand-in for a Pi file format or hook payload (catalog JSON, `models.json`, the `before_agent_start` prompt, session records), with file and test name; each gets one twin that reads the pinned installation's real file or a real rendering produced by the pinned Pi. Reason: the bead's "every test", made checkable.
- **The first twin is the session lookup** (the neutral-path extension of the first recorded finding does not exist on main, so its twin belongs to the change that lands it — spec-review SR-4):  the session lookup against the shipped `opencode-go.json` with its `chat:` keys. Reason: the two recorded findings.
- **Pi not installed:** the twin fails with the install hint, as ADR 0019 item 4 requires (corrected after spec-review SR-1; the bead said skip, the accepted ADR wins). CI installs the pinned Pi.
- **No live network call, no paid model:** a real rendering means running the pinned Pi's own code offline (or reading its shipped files), never an API call. Reason: contract tests stay hermetic.
- **ADR 0019 and `tools/pi/install.sh` stay unchanged.** Reason: the remedy is tests, not a decision change.
