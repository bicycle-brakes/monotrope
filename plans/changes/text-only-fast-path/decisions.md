---
title: "Decisions — text-only-fast-path"
category: decisions
status: draft
implementation_status: none
date: 2026-11-21
created: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-is4h
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-21"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, spike, ci, fast-path]
---

# text-only-fast-path — Decisions

Class: spike (bead coding-harness-is4h).

## Correction to the explore

The explore could not read the bead and read the topic as the *local* `make verify` exception. This spike is about the **hosted CI** fast path. The bead says: "Why: maintainer, 2026-11-18, while choosing the fast CI path for handover-only PRs (answer A): 'lege einen bead an, dass c geprüft werden soll' — option C was the same fast path for every text-only PR, matching the local rule that text-only changes skip make verify. What: list which gates read documentation content (glossary, links, ADR index, question-context, workflow docs, prompt tests) and which would miss a fault if a text-only PR skipped the full verify; measure the CI time text-only PRs spent since 2026-11-01; recommend with alternatives. Builds on the handover-only fast path." Its notes (CI research swarm, 2026-11-21) add: 13 of 26 failed CI runs in 2026-11-12..21 were text-only PRs, every one failed in a cheap process gate, never in pytest; so the fast path must keep every process gate and the tracker hydration, and only pytest and leerprobe are candidates to skip; skip them with an `if:` inside the verify job, never a workflow path filter (a required check would stay Pending and block the merge queue); exclude `prompts/`, `decisions/` and every Markdown file a test reads.

The explore's map of the local paths stays useful as background; its open questions on the local runner are outside this spike.

## SKIP · interview

status: skipped
reason: A spike owes its learning goal, time budget and expected outcome. The bead states the learning goal and the expected outcome (the gate list, the measured CI time since 2026-11-01, a recommendation with alternatives); the maintainer asked for no question windows until the block on 2026-11-23 10:00; the time budget is set below as a [DETAIL]. The recommendation itself goes to the maintainer — the spike decides nothing about CI.

## [DETAIL] items decided by the orchestrator

- **Time budget: two hours.** Stop at the limit and report what was measured.
- **Output: one research note** under `docs/research/2026-11-2x-text-only-fast-path.md` with (1) the gate list — for every gate in `decisions/gates.yaml`, whether it reads Markdown content and which Markdown files tests read (found by searching `tests/` for the paths they open); (2) the measured hosted CI minutes of text-only pull requests merged since 2026-11-01 (`gh run list` / `gh pr list`, text-only = no changed path outside Markdown, and no path under `scripts/`, `tests/`, `prompts/`, `decisions/` or `.github/`); (3) a recommendation with at least two alternatives and their risk. No change to `scripts/ci_gates.py`, `.github/workflows/ci.yml` or `decisions/gates.yaml`.
- **Definition of text-only for the measurement:** the bead's — Markdown outside `scripts/`, `tests/`, `prompts/`, `decisions/` — plus the swarm's exclusion of every Markdown file a test reads. Reason: the note must say which set it measured.
