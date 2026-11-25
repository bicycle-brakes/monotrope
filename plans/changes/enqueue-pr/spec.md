---
title: "Spec — enqueue-pr"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-va1l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, merge-queue]
class: bounded
adr_files: []
---

# Spec — enqueue-pr

A single guarded command admits an eligible pull request to the merge queue (bead `coding-harness-va1l`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-25 the research found that direct merge commands require approval, so an unattended orchestrator cannot use the stated queue-admission grant. No existing script checks the pull request, phase-6 review, required checks and closure trailer together. The grant cited in the research was not present in the checked-out `AGENTS.md`; its exact wording was not read. Existing instructions require an exact head and a maintainer request for merging.

## Terms

**Head:** the pull request's current commit. **Admission:** placing that head in an enabled merge queue; admission is not proof of a merge.

## Acceptance criteria

1. When invoked with a pull request number whose request is open and targets `main`, whose newest phase-6 review has no open finding or explicitly reports no findings, whose required checks on its head all succeeded, and whose head commit has a `Closes-Bead` trailer naming an existing bead, the command admits that head to the enabled merge queue.
   *Refuted by:* an eligible request is refused or its verified head is not queued.
2. When the request is closed or targets a branch other than `main`, admission is refused.
   *Refuted by:* either request reaches the admission command.
3. When the newest phase-6 review has an open row, admission is refused.
   *Refuted by:* a request with an open row reaches the admission command.
4. When any required check on the head is missing, pending, failed or not successful, admission is refused.
   *Refuted by:* a request with any such check reaches the admission command.
5. When the head commit lacks a `Closes-Bead` trailer naming an existing bead, admission is refused.
   *Refuted by:* a missing, malformed or unknown declaration reaches the admission command.
6. When any prerequisite, its association with the request and its head, or the enabled queue cannot be established, admission is refused.
   *Refuted by:* missing, ambiguous, stale or unreadable evidence reaches the admission command.
7. When the head changes after verification, the previously verified head is not admitted as the new head.
   *Refuted by:* a changed head enters the queue using the earlier evidence.
8. When admission is attempted, it uses the verified head and cannot bypass the queue or invoke administrative merge.
   *Refuted by:* a direct merge, administrative option or unpinned admission is issued.
9. When admission is refused, the command identifies the failed condition.
   *Refuted by:* a refusal leaves the operator unable to identify the failed prerequisite.
10. When admission succeeds, the result reports queued rather than merged.
    *Refuted by:* queue admission is reported as a completed merge.
11. While using Claude Code, Codex or Antigravity, the guarded command is the permitted unattended admission path and direct merge commands retain their approval or night-time denial.
    *Refuted by:* the guarded command is unavailable unattended or a direct merge becomes unattended in any of those environments.

## Non-goals

- Merging without an enabled queue, administrative bypass, closing beads, or treating queue admission as a completed merge.
- Changing required checks or review standards, or creating a second merge entry point.

## Protected areas

Tracker data and other changes' findings are read-only; their writers retain ownership.

## Definition of Done

- `make verify` green; all criteria demonstrated by the criterion ledger.
- The command, tests, applicable permission policy and merge procedure move together; no ADR is proposed.
- The pull request closes bead `coding-harness-va1l` and its last commit carries `Closes-Bead: coding-harness-va1l`.
- Special runs: none.

## Open decisions

[DETAIL] Fail closed when evidence cannot be associated unambiguously with the current head: this preserves the stated conditions without assuming an unknown state is safe.

[DECISION]

Thema: Aufnahme von Entscheidungs-Pull-Requests in die Merge-Warteschlange.
Absicht: Die neue Freigabe soll unbeaufsichtigtes Einreihen ermöglichen, ohne ungeklärte Architekturentscheidungen vorwegzunehmen.
Heute: Die Repository-Regel sagt, dass eine Entscheidung durch den Merge ihres Pull Requests durch dich wirksam wird; der genaue Wortlaut der angeführten neuen Freigabe wurde nicht gelesen.
Repository-Änderung: Das Skript muss entscheiden, ob es solche Pull Requests annimmt oder zurückweist.
Architekturänderung: Der bestehende Entscheidungsprozess bleibt bestehen; betroffen ist, wer das Einreihen auslösen darf.

Ziel in einem Satz: Klären, ob die unbeaufsichtigte Freigabe auch Pull Requests mit Architekturentscheidungen umfasst.
Option 1 — Entscheidungs-Pull-Requests zurückweisen: Du reihst diese weiterhin selbst ein; Nachteil: sie können den unbeaufsichtigten Ablauf anhalten.
Option 2 — Auch Entscheidungs-Pull-Requests einreihen: Sie laufen unter denselben Prüfungen automatisch weiter; Nachteil: eine Entscheidung kann ohne deine erneute Einzelaufforderung wirksam werden.
Empfehlung: Option 1, weil der gelesene Stand keine ausdrückliche Ausnahme für Entscheidungs-Pull-Requests belegt.
Wenn du „ok“ sagst: Das Skript weist Entscheidungs-Pull-Requests zurück und nennt den Grund.
Was verloren geht: Option 2 würde auch diese Pull Requests unbeaufsichtigt weiterbringen.
Akzeptierter Nachteil: Bei Option 1 ist ein manueller Schritt nötig; bei Option 2 entfällt die erneute Einzelaufforderung vor dem Wirksamwerden.

Welche Option und welchen zugehörigen Nachteil akzeptierst du?
