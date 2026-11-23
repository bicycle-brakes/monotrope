---
title: "Spec — commit-hook-stamp"
status: draft
implementation_status: none
date: 2026-11-23
last_reviewed: 2026-11-23
updated: 2026-11-23
supersedes: null
superseded_by: null
bead: coding-harness-yv9i.2
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-23"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, commit-hook]
class: bounded
appetite: 3
adr_files: []
---

# Spec — commit-hook-stamp

A normal commit stamps its staged held documents without relying on a person remembering the date (bead `coding-harness-yv9i.2`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

On 2026-11-23, research found that the frontmatter currency gate reports stale `updated:` dates but the pre-commit hook does not stamp them; recorded midnight incidents left verification red and consumed work. The maintainer recorded a stale hand edit that cost three draft attempts (`decisions.md#Q-1`).

## Terms

**Held document:** a Markdown path for which the provenance map requires frontmatter. **Staged content:** the version Git will commit, which can differ from the working file.

## Acceptance criteria

1. When a normal Git commit runs the installed repository pre-commit hook, each staged, added or modified held document with stampable frontmatter is committed with `updated:` set to the local date at hook execution.
   *Refuted by:* a committed staged held document retains a stale or future date or lacks the stamp.
   *Basis:* `decisions.md#Q-1`.
2. When a held document is partially staged, stamping preserves all other staged content and does not add unstaged edits to the commit.
   *Refuted by:* an unstaged edit enters the commit or staged content other than the stamp changes.
   *Basis:* `decisions.md#Q-1`.
3. When the hook stamps staged content, it updates the working file to the same stamped content only if that file matched the staged content before stamping; otherwise it leaves the working file unchanged and reports that it was left unchanged.
   *Refuted by:* a matching working file retains the old stamp, or a different working file is changed or left unchanged without a notice.
   *Basis:* `decisions.md#Q-1`.
4. If a staged held document cannot safely be stamped, the hook refuses the commit and identifies the path and reason.
   *Refuted by:* a commit succeeds with malformed, duplicate or unreadable frontmatter, or the error does not identify the affected path and reason.
   *Basis:* `decisions.md#Q-1`.
5. When the repository pre-commit hook runs, its existing Beads tracker integration retains its existing execution and failure behavior.
   *Refuted by:* a tracker hook failure that previously stopped a commit is ignored, or the tracker hook is skipped.
   *Basis:* `decisions.md#Q-1`.
6. When a staged path is deleted or is not a held document, the stamping operation leaves it alone.
   *Refuted by:* a deletion is restored or a non-held staged path is changed.
   *Basis:* `decisions.md#Q-1`.
7. If the currency measurement refuses to run, the hook reports its reason on standard error and allows the commit without changing the index.
   *Refuted by:* a shallow checkout or an empty held set blocks the commit, changes the index, or produces no reason.
8. If stamping any staged document fails, the hook leaves the entire index as it was before the hook ran.
   *Refuted by:* an earlier document remains stamped in the index after a later document fails.
9. When the repository's Beads hooks are installed or reinstalled, the pre-commit hook invokes the stamping step.
   *Refuted by:* a fresh installation or a regenerated hook commits a staged stale held document without invoking the step.
10. When a staged date is later than tomorrow in UTC, the hook treats it as the currency gate's future finding.
    *Refuted by:* the hook uses a different future threshold than the gate.
    A date no later than tomorrow UTC is not future solely for being after the local date.
11. When a kit copy is assembled, it includes the staged-document stamping script.
    *Refuted by:* the kit manifest omits the script or the assembled kit lacks it.
12. When stamping produces a staged document, the hook checks the result against the applicable currency rules before allowing the commit.
    *Refuted by:* a failed post-stamp check permits the commit.
13. When a commit is aborted after stamping succeeded for a separate reason, the stamped index remains in place.
    *Refuted by:* a later commit-message abort rolls back the successful stamp.

## Non-goals

Changing the currency gate's CI policy, the meaning of `last_reviewed:`, other existing stamp writers, hook-bypassed Git commands, or the tracker hook's managed section is outside this change. Custom hook configurations and commits made with hooks explicitly disabled remain outside the hook's reach.

## Protected areas

The Beads managed hook section and tracker database are protected to preserve tracker integration and shared data. Customer instances are outside the framework boundary.

## Definition of Done

- `make verify` green and the temporary-repository commit tests pass.
- Updated hook, `scripts/hooks/stamp_staged.py`, `scripts/kit/manifest.yaml`, tests and workflow documentation move in the same pull request; no ADR is due.
- Protected areas and non-goals are checked against the pull request file list.
- The pull request closes `coding-harness-yv9i.2` and its last commit carries `Closes-Bead: coding-harness-yv9i.2`.
- Special runs: none.

## Open decisions

[DETAIL] Update a matching working file along with its staged version; leave a different working file alone and report it. This avoids a stale working copy after a fully staged commit while preserving partial staging. A hook deliberately disabled or replaced by a custom hook cannot run; the existing CI gate remains the backstop.

[DETAIL] A later abort does not roll back a successful stamp: the stamp remains correct and can be applied again without changing the result.

[DETAIL] Measurement refusal passes unchanged with a diagnostic, while a stamping failure leaves the index intact; this retains commit access where the existing gate cannot measure and avoids partial updates. A missing runtime is a hook execution failure, reported by the hook rather than treated as a measurement result.

[DETAIL] The future threshold follows the existing currency gate, and the kit carries the stamping script; these reuse existing definitions and distribution. The tracked `.beads/hooks/pre-commit` invokes `scripts/hooks/stamp_staged.py` outside the managed section so installation and regeneration retain the invocation.

[DECISION] Invalid date values (phase-2a finding S-1):

Topic: Ungültiger Datumswert in einem zum Commit vorgemerkten Dokument.
Intention: Der Commit-Hook soll vor dem Commit einen fehlenden oder veralteten Datumsstempel behandeln.
Today: Der vorhandene Stempelbefehl ersetzt auch einen ungültigen Datumswert; die bisherige Spec lässt offen, ob der Hook das ebenfalls tun darf.
Repository change: Die Spec legt fest, ob der Commit bei einem ungültigen Datumswert fortgesetzt oder angehalten wird.
Architecture change: Die bestehende Datumsprüfung bleibt die Grundlage; die Entscheidung bestimmt das Verhalten des neuen Commit-Hooks.

Goal in one sentence: Ein ungültiger Datumswert soll beim Commit eindeutig behandelt werden.
Options: A — automatisch auf das heutige Datum setzen und den Commit fortsetzen; B — den Commit mit einer Fehlermeldung anhalten.
Recommendation: A — weil der vorhandene Stempelbefehl ungültige Datumswerte bereits repariert.
If you say "ok": Der Hook ersetzt einen ungültigen Datumswert durch das lokale Datum; nicht als UTF-8 lesbare Dateien bleiben ein gesonderter Fehler.
What is lost: Option B würde eine manuelle Prüfung vor jeder Korrektur erzwingen.
Downside you accept: A — ein falscher Wert wird ohne manuelle Prüfung ersetzt; B — ein reparierbarer Wert unterbricht den Commit.

Welche dieser Folgen akzeptierst du: A oder B?

The other unresolved ambiguities S-2 through S-4 remain open in `findings.md`; their provisional agent decisions are not maintainer answers.
