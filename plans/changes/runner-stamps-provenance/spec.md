---
title: "Spec — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, model: glm-5.3, version: "2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, provenance]
class: bounded
appetite: 3
adr_files: []
neighbours: [plans/changes/archive/2026-11-16-explore-provenance/spec.md, plans/specs/implementation-verification/spec.md]
---

# Spec — runner-stamps-provenance

The runner records the actual producer after explore, draft and repair, and rejects invalid producer headers in files touched by a run (bead `coding-harness-f9sv`). Research: `research.md`; decisions: `decisions.md`.

## Problem

- Draft artifacts receive headers from the model session; research publication is already stamped by the runner (`research.md`, “What exists today”, 2026-11-16).
- On 2026-11-16, 271 of 620 producer headers under `plans/` failed the census rule; a tree-wide check would also turn existing lanes red (`decisions.md`, Q-4). The existing stock is addressed separately.

## Terms

A **producer record** identifies the program, model and publication date of a model session in `produced_by`. A **touched file** is a file changed by the run and retained for its post-run checks; files restored by the runner are excluded.

## Acceptance criteria

1. When explore publishes research, the runner stamps a producer record with the actual program, model and publication date of that run.
   *Refuted by:* a GLM route recording `codex`, a different model or a date other than the publication day.
   *Basis:* `decisions.md#Q-4`.
2. When draft retains a model-written artifact with frontmatter, including a new ADR if present, the runner stamps a producer record with the actual program, model and publication date before its post-run checks, including an attempt that subsequently fails those checks.
   *Refuted by:* an affected artifact missing that record, or a GLM attempt recorded as `codex`, with a wrong model or date.
   *Basis:* `decisions.md#Q-4`.
3. When repair retains a model-written artifact with frontmatter, the runner stamps a producer record with the actual program, model and publication date before its post-run checks.
   *Refuted by:* an affected artifact missing that record, or its record naming a different program, model or publication day.
   *Basis:* `decisions.md#Q-4`.
4. When a runner verb checks its result, a failing producer header in a touched file makes its post-run check fail with a diagnostic identifying the file.
   *Refuted by:* a touched file with an invalid producer header accepted by its verb's post-run check.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-4`.
5. While the runner stamps an artifact, it preserves bytes outside the fields that stamping must change.
   *Refuted by:* changed prose, fences, plan card or unrelated frontmatter.
   *Basis:* `research.md`, “The runner already stamps provenance in these places”.
6. If an artifact cannot be stamped safely, the attempt fails with a diagnostic instead of publishing an invented or malformed header.
   *Refuted by:* accepting a header with ambiguous YAML anchors or undecodable bytes, or failing without identifying the artifact.
   *Basis:* `research.md`, “The runner already stamps provenance in these places”.

The exact treatment of existing producer records, the validation contract and approval state remains open below; criteria dependent on those answers are not final.

## Non-goals

- Migration of existing headers and a tree-wide check belong to the separate migration work (bead `coding-harness-2i7x`), per Q-4.
- No general side-route detector, enforcement of allowed provenance classes, change to the untouched new-change skeleton, or automated human approval.
- No change to the maintainer's answers in `decisions.md`, nor to the headerless loop record.

## Protected areas

Runner-held paths remain outside model attempts, including `provenance.yaml`, `decisions/gates.yaml`, `prompts/`, `templates/`, and `AGENTS.md`; no edit to them is planned. Existing unrelated artifacts and archived headers are not migrated.

## Definition of Done

- `make verify` green; the tests in the criterion ledger exercise the runner routes and their failure cases.
- The runner, its shared producer validation and their tests move in the same pull request; no special migration run is required.
- The protected areas and non-goals are checked against the pull request's file list.
- The pull request closes `coding-harness-f9sv` and its final commit carries `Closes-Bead: coding-harness-f9sv`.

## Open decisions

### [DECISION] Existing producer records (review finding F-2)

Topic: Frühere Angaben zur Urheberschaft eines Dokuments.
Intention: Ein erneuter Entwurf soll seine Herkunft nachvollziehbar festhalten.
Today: Die Forschungs-Veröffentlichung behält vorhandene Angaben und ergänzt den aktuellen Lauf; frühere Angaben können aber falsch sein.
Repository change: Der Runner übernimmt frühere Angaben oder ersetzt sie durch den aktuellen Lauf.
Architecture change: Der Runner bleibt die zentrale Schreibstelle; die gespeicherte Herkunft unterscheidet sich.

Goal in one sentence: Festlegen, welche Herkunft ein neu veröffentlichter Entwurf zeigt.
Options: 1. Frühere Angaben behalten und den aktuellen Lauf ergänzen — frühere Beiträge bleiben sichtbar, möglicherweise auch falsche Angaben. 2. Nur den aktuellen Lauf eintragen — seine Herkunft ist eindeutig, frühere Beiträge gehen verloren.
Recommendation: Option 1 — weil frühere Beiträge sonst nicht mehr erkennbar sind.
If you say "ok": Der Runner behält interpretierbare frühere Angaben und ergänzt den tatsächlichen aktuellen Lauf.
What is lost: Option 2 hätte eine ausschließlich auf den aktuellen Lauf begrenzte Herkunft gezeigt.
Downside you accept: Option 1 kann falsche frühere Angaben mitführen; Option 2 verliert die Herkunft früherer Beiträge.

Welche Option und den jeweils genannten Nachteil akzeptierst du?

### Further unresolved review ambiguities

- F-7: whether the per-run check validates only the producer record's shape or the full research publication metadata contract. No answer recorded.
- F-9: whether a new draft resets an existing human approval to pending or preserves it. No answer recorded.

[DETAIL] If a field must be inserted and no `tags` field exists, place it at the end of the frontmatter; this preserves unrelated bytes.

[DETAIL] The post-run check identifies the affected file: this makes a failure actionable without changing the intended scope.
