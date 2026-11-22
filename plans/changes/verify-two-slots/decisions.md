---
title: "Decisions — verify-two-slots"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-u1ha
owner: framework-architect
provenance: ai-drafted-reviewed
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verify-lock, make-verify]
---

# verify-two-slots — Decisions

Class: bounded (bead coding-harness-u1ha; re-slice of the earlier `feat/verify-slots` lane, maintainer 2026-11-18).

## Q-1 · Slice 1 scope for verify-two-slots

asked: 2026-11-21
answer: "Option A (Empfohlen): Minimaler Slice 1 — nur die 2 konfigurierbaren Slots (Default 2), Mehr-Halter-Status/Wartelog, Ein-Prozess-Boundary und 2-Slot-Messung (1,6x-Grenze); bestehende Worker-Berechnung bleibt unangetastet; Folge-Bead coding-harness-bxxt.11 fuer Worker-Anpassung angelegt."
answered_by: maintainer
status: answered
context: |
  Topic: scope of Slice 1 for coding-harness-u1ha (two verify slots, branch feat/verify-two-slots) after the earlier feat/verify-slots lane was stopped for re-slicing (2026-11-18).
  Intention: relieve the single-verify-slot bottleneck quickly with a small, clean slice instead of bundling unrelated worker-sizing and telemetry changes.
  Today: scripts/verify_lock.py admits one protected make verify run at a time via FIFO; full runs wait up to 77 minutes overnight.
  Repository change: scripts/verify_lock.py, scripts/verify_run.py, doctrine and tests — 2 configurable verify slots (HARNESS_VERIFY_SLOTS, default 2, later moving into central config coding-harness-twvx), multi-holder published state and wait log, one-admission-per-process Boundary, and paired 2-slot measurement against the confirmed 1.6x serial wall-time threshold.
  Architecture change: none — extends the existing flock/FIFO lock to 2 slots; per-slot pytest worker adjustment moves to coding-harness-bxxt.11, explicit admission handles stay in coding-harness-42em, and RAM-minimum recording stays out of Slice 1.
alternatives: |
  - Option A (chosen): minimal Slice 1 (2 configurable slots default 2, multi-holder status/wait log, one-admission-per-process Boundary, 2-slot 1.6x measurement); existing worker sizing untouched and split to coding-harness-bxxt.11.
  - Option B: also halve per-slot pytest workers inside Slice 1 (larger diff and review surface).

In the context of re-slicing coding-harness-u1ha after the earlier verify-slots
lane grew past its appetite, facing a single local verify slot that serializes
parallel lanes, we decided on minimal Slice 1 with 2 configurable verify slots
(HARNESS_VERIFY_SLOTS, default 2), multi-holder status and wait logs, a
one-admission-per-process Boundary, and a paired 2-slot measurement against the
1.6x serial threshold while keeping existing pytest worker sizing untouched
(split to coding-harness-bxxt.11), to achieve fast relief of the verify
bottleneck with a bounded diff, accepting that per-slot worker tuning follows
separately after the 2-slot measurement — 2026-11-21

## Interview minimum

Bounded class: one maintainer-answered question (Q-1). Prior settled constraints carried from the bead notes: default slot count is 2 (maintainer 2026-11-20), 1.6x threshold is scoped to two slots and 3x4 is not gated (maintainer 2026-11-17), and explicit admission handles belong to coding-harness-42em (maintainer 2026-11-11).
