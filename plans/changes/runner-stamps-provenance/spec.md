---
title: "Spec — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-17
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

A **producer record** identifies a producing program and publication date in `produced_by`; a model is optional in the existing contract but is required for a new single-model run record. A **touched file** is a file changed by a run and retained for its post-run checks; files restored by the runner are excluded.

## Acceptance criteria

1. When a single-model explore publishes research, the runner stamps a producer record with the actual program, model and publication date of that run; a swarm publication instead names the swarm as producer, the bound publication day and no single model.
   *Refuted by:* a GLM route recording `codex`, a different model or a date other than the publication day.
   *Basis:* `decisions.md#Q-4`, `decisions.md#Q-8`.
2. When a draft attempt changes and retains a model-written artifact with frontmatter, including a new ADR if present, the runner stamps a producer record with the actual program, model and publication date before its post-run checks, including an attempt that subsequently fails those checks.
   *Refuted by:* an affected artifact missing that record, or a GLM attempt recorded as `codex`, with a wrong model or date.
   *Basis:* `decisions.md#Q-4`.
3. When a repair attempt changes and retains a model-written artifact with frontmatter, the runner stamps a producer record with the actual program, model and publication date before its post-run checks.
   *Refuted by:* an affected artifact missing that record, or its record naming a different program, model or publication day.
   *Basis:* `decisions.md#Q-4`.
4. When a runner verb checks its result, a touched file that fails the full research publication header contract, including any earlier producer record, makes its post-run check fail with a diagnostic identifying the file.
   *Refuted by:* a touched file with an invalid producer, provenance, review or date accepted by its verb's post-run check.
   *Basis:* `decisions.md#Q-1`, `decisions.md#Q-4`, `decisions.md#Q-6`, `decisions.md#Q-7`.
5. While the runner stamps a draft or repair artifact, it preserves bytes outside `produced_by`, `updated` and a `review` reset required by criterion 8.
   *Refuted by:* changed prose, fences, plan card, `provenance` or unrelated frontmatter; in particular a draft ADR loses its `human-decided` provenance.
   *Basis:* `research.md`, “The runner already stamps provenance in these places”.
6. If an artifact cannot be stamped safely, the attempt fails with a diagnostic instead of publishing an invented or malformed header.
   *Refuted by:* accepting a header with any YAML anchor or alias, undecodable bytes, a non-mapping header or an unreadable earlier producer, or failing without identifying the artifact.
   *Basis:* `research.md`, “The runner already stamps provenance in these places”.

7. When an artifact is stamped, every readable earlier producer record remains and the record of the run that actually contributed is added.
   *Refuted by:* losing a readable earlier record or attributing an unchanged file to a later attempt.
   *Basis:* `decisions.md#Q-5`.
8. When a redraft changes an approved document's body, its approval is reset to pending and the reset identifies the approver.
   *Refuted by:* retaining approval for changed body content or omitting whose approval was reset.
   *Basis:* `decisions.md`, “Decided by the agent”.
9. When stamping changes only the header of an approved document, its approval remains unchanged.
   *Refuted by:* resetting an approval solely because of a header stamp.
   *Basis:* `decisions.md`, “Decided by the agent”.
10. If an attempt's changed files cannot be measured, the runner refuses to attribute its producer to an unmeasured file and reports the failure.
    *Refuted by:* stamping an unchanged file with that attempt's producer or accepting an unmeasured attempt without a diagnostic.
    *Basis:* `decisions.md#Q-5`.

Criteria 2, 4, 5, 6 and 7 are provisional where the unanswered decisions below affect them. The explore publication's existing removal of generated skeleton notices is outside criterion 5.

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

[DETAIL] Insert a missing field at the end of frontmatter when `tags` is absent; this preserves unrelated bytes. Refuse all YAML anchors and aliases, not just ambiguous ones, because their shared source spans make safe edits uncertain. A resumed swarm retains its frozen preparation day, because its publication bytes are bound to the resume snapshot.

### [DECISION] The current session's self-description (review finding F-12)

Topic: Eine Herkunftsangabe, die das gerade laufende Modell selbst in den Kopf schreibt.
Intention: Frühere Beiträge sollen sichtbar bleiben und die Herkunft des aktuellen Laufs soll stimmen.
Today: Modelle können ihren eigenen Namen falsch oder als Platzhalter eintragen.
Repository change: Der Runner behält diese Angabe als früheren Eintrag oder ersetzt sie durch seine gemessene Angabe.
Architecture change: Der Runner bleibt die zentrale Schreibstelle; die gespeicherten Einträge unterscheiden sich.

Goal in one sentence: Festlegen, ob eine selbst geschriebene Angabe des aktuellen Laufs erhalten bleibt.
Options: 1. Als früheren Eintrag behalten — keine lesbare Angabe geht verloren, aber eine falsche Angabe bleibt sichtbar. 2. Durch die gemessene Angabe ersetzen — die aktuelle Herkunft ist eindeutig, aber ein selbst geschriebener Eintrag geht verloren.
Recommendation: Option 2 — weil die Angabe denselben aktuellen Lauf beschreibt und dessen Herkunft sonst widersprüchlich bleiben kann.
If you say "ok": Der Runner ersetzt die selbst geschriebene Angabe des aktuellen Laufs durch den gemessenen Eintrag und behält lesbare Angaben aus dem Stand vor dem Lauf.
What is lost: Option 1 hätte auch den selbst geschriebenen Eintrag bewahrt.
Downside you accept: Option 1 kann falsche aktuelle Angaben behalten; Option 2 entfernt einen selbst geschriebenen Eintrag.

Welche Option und den jeweils genannten Nachteil akzeptierst du?

### [DECISION] Header fields changed by stamping (review finding F-13)

Topic: Änderungen am Dokumentkopf durch den Herkunftsstempel.
Intention: Der Stempel soll Herkunft richtig festhalten und bestehende Entscheidungen und Freigaben schützen.
Today: Die Forschungs-Veröffentlichung ändert Herkunftsklasse, Urheber, Prüfstatus und Änderungsdatum und entfernt Vorlagenhinweise; eine Architekturentscheidung trägt die Herkunftsklasse `human-decided`.
Repository change: Der Runner ändert entweder diese Kopfwerte auch bei Entwurf und Reparatur oder erhält Herkunftsklasse und Freigabe dort nach einer gesonderten Regel.
Architecture change: Der Runner bleibt die zentrale Schreibstelle; der Umfang seiner Schreibrechte am Dokumentkopf unterscheidet sich.

Goal in one sentence: Festlegen, welche Angaben der Stempel bei Entwurf und Reparatur ändern darf.
Options: 1. Herkunftsklasse und Prüfstatus wie bei Forschungs-Veröffentlichungen ersetzen — ein einheitlicher Vertrag, aber eine Architekturentscheidung verliert ihre vorgesehene Klasse und Freigaben werden zurückgesetzt. 2. Herkunftsklasse erhalten und Freigaben nur bei geändertem Inhalt zurücksetzen — menschliche Entscheidungen bleiben erkennbar, aber die Prüfung braucht eine passende Regel für solche Dokumente.
Recommendation: Option 2 — weil Architekturentscheidungen ihre menschlich entschiedene Herkunft behalten sollen.
If you say "ok": Der Stempel erhält die Herkunftsklasse, ergänzt den Urheber, aktualisiert das Änderungsdatum und setzt eine Freigabe nur bei geändertem Inhalt zurück; die Prüfung berücksichtigt diese Fälle.
What is lost: Option 1 hätte für alle Dokumentarten denselben Forschungs-Kopfvertrag angewendet.
Downside you accept: Option 1 kann die Herkunftsklasse menschlicher Entscheidungen und bestehende Freigaben überschreiben; Option 2 benötigt eine dokumentartgerechte Prüfung und weicht damit vom unveränderten Forschungs-Kopfvertrag ab.

Welche Option und den jeweils genannten Nachteil akzeptierst du?

### Further review ambiguities awaiting a maintainer answer

F-9, F-10, F-15, F-16 and F-17 remain open in `findings.md`. The criteria and agent details above are provisional where they address those rows. F-13 also remains open as asked above: applying the research contract's `ai-drafted-reviewed` and pending-review requirements to an ADR or a previously approved header conflicts with preserving those values. The maintainer's answer and any resulting spec changes must precede implementation.
