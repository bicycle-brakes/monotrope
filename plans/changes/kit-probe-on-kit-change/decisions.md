---
title: "Decisions — kit-probe-on-kit-change"
category: decisions
status: draft
implementation_status: none
date: 2026-11-13
created: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-w2ay
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Fable 5.2, 2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, verify-speed, kit, gates]
---

# kit-probe-on-kit-change — Decisions

Class: bounded (bead coding-harness-w2ay).

## Q-1 · What counts as a changed kit file

asked: 2026-11-13
answer: "Aus dem Kit-Manifest (Empfohlen)" — the trigger is derived from the kit manifest: every file the manifest classifies as travelling, the manifest and the probe themselves, and every added or removed file.
answered_by: maintainer
status: answered
context: |
  Topic: the kit probe (`leerprobe`) costs 2 to 3 minutes of every local make verify (122 to 176 s measured on 2026-11-13) and shall run locally only when kit files changed; hosted CI keeps it always.
  Intention: the full check shall get under 10 minutes; the probe is about 20 % of it.
  Today: the probe runs in every local full check; "kit files changed" is defined nowhere.
  Repository change: one predicate that reads scripts/kit/manifest.yaml; no second path list.
  Architecture change: none; the manifest stays the one statement of what travels.

In the context of a probe that shall run only when the kit changed, facing a choice between a predicate derived from the manifest and a fixed path list, we decided for the manifest, to achieve one source that new kit files join by themselves, accepting that the predicate must read the manifest on every run. — 2026-11-13

## Q-2 · Which half of the probe is skipped

asked: 2026-11-13
answer: "Nur die teure Hälfte (Empfohlen)" — the classification check always runs, in seconds; only the test run in the empty repository is conditional.
answered_by: maintainer
status: answered
context: |
  Topic: the probe has a cheap half (every file is classified in the manifest) and an expensive half (the tests run in an empty repository).
  Intention: a new, unclassified file must show even when no kit file changed.
  Today: both halves live in one command.
  Repository change: the two halves become separately selectable; the cheap one runs always.
  Architecture change: none.

In the context of a probe with a cheap and an expensive half, facing a choice between skipping both and skipping only the expensive one, we decided to skip only the expensive half, to achieve that an unclassified file still blocks locally, accepting a split of the one command. — 2026-11-13

## Q-3 · Where the condition is declared

asked: 2026-11-13
answer: "Feld in der Prüfliste (Empfohlen)" — a new, general field in decisions/gates.yaml says that a gate runs locally only when given paths are affected; the runner holds no rule of its own.
answered_by: maintainer
status: answered
context: |
  Topic: the local runner holds no commands or rules of its own; it asks the one gate list.
  Intention: the condition travels in the kit and must not become a special case outside the list.
  Today: decisions/gates.yaml has no field for a conditional local run.
  Repository change: a schema change of the gate list (schema version, the field, its validation); other gates can use the field later.
  Architecture change: none; the one list stays the source.

In the context of a condition for one gate, facing a choice between a field in the one gate list and a rule in the runner script, we decided for the field, to achieve that the list stays the only place that says what runs, accepting a schema change. — 2026-11-13

## Q-4 · The skip before phase 6

asked: 2026-11-13
answer: "Ja, als erklärter Skip (Empfohlen)" — the probe may be skipped in the full local check before phase 6 as well, when no kit file is affected; the run says so explicitly and records it in the run log; hosted CI measures the probe on every pull request.
answered_by: maintainer
status: answered
context: |
  Topic: the workflow demands a fresh full local make verify as evidence before phase 6.
  Intention: most full local runs are exactly these, so the saving depends on this answer.
  Today: a skipped gate gets no timing event, so a skip is invisible in the run log.
  Repository change: a declared skip with its reason in the run output and the run log; docs/WORKFLOW.md says that the hosted run is the probe's measurement for such a head.
  Architecture change: none.

In the context of the full local check before phase 6, facing a choice between always running the probe there and a declared skip, we decided for the declared skip, to achieve the whole saving, accepting that for such a head the probe is measured by hosted CI and not locally. — 2026-11-13

## Decided by the agent

[DETAIL] **Without a base to compare against, the probe runs.** Reason: a fresh clone or a shallow checkout cannot answer what changed; guessing "nothing" would skip silently, so the predicate fails closed.
