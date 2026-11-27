---
title: "Spec — read-only-agents-no-shell"
status: draft
implementation_status: none
date: 2026-11-28
last_reviewed: 2026-11-28
updated: 2026-11-28
supersedes: null
superseded_by: null
bead: coding-harness-5ane.22
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, agents, ramp-valves]
class: bounded
appetite: 2
adr_files: []
---

# Spec — read-only-agents-no-shell

The five currently identified read-only agents retain an explicit tool list without shell or writing tools, with a test that detects a planted shell (bead `coding-harness-5ane.22`). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- At commit `59ae5778`, the named enforcer for the agent tool-scope ramp valve does not exist; the existing helper test covers only explorer and reviewer (`research.md`, What exists today).
- At the same commit, rule RB-A2 also requires shell scope declarations and four deny categories, which the proposed shell test alone cannot establish (`research.md`, The rule and The deny list).

## Terms

**Identified read-only agents:** explorer, reviewer, consistency-auditor, migration-supervisor and preconditions-gate-runner, the five agents whose current tool lists contain no Bash, Write or Edit (`research.md`, The agent definitions). This fixed baseline does not classify new roles automatically.

## Acceptance criteria

1. When the enforcer checks each identified read-only agent, its declared tool list excludes Bash, Write and Edit.
   *Refuted by:* One identified agent has one of those tools and the enforcer passes.
2. If an identified read-only agent has no explicit or valid tool list, the enforcer fails.
   *Refuted by:* A missing or malformed list passes and may inherit tools.
3. When a valid read-only definition is checked, the enforcer accepts it.
   *Refuted by:* A valid fixture using Read, Grep and Glob fails.
4. When a shell is planted in an identified read-only agent's tool list, the same enforcer fails.
   *Refuted by:* The planted Bash mutation passes.
5. When the named enforcer is present, the agent tool-scope ramp valve becomes due.
   *Refuted by:* The valve predicate remains false with the named top-level test present.

## Non-goals

Changing executor tool scopes or permissions, enforcing shell-scope declarations or the four deny categories, and automatically classifying future agent roles are outside this bounded change. Their inclusion depends on the decision below or a separate change. A bounded change has no design phase.

## Protected areas

`docs/governance/regelwerk.md` is human-decided: prepare an exact proposed change for the maintainer, without writing the file. Agent definitions, permission policies and generated settings are not changed.

## Definition of Done

- `make verify` green after the governance decision and any authorized maintainer edit.
- The proposed governance text and the test accompany the pull request; no ADR is changed.
- Protected areas remain untouched by the implementation attempt and non-goals remain unbuilt, as shown by the pull request file list.
- The pull request closes bead `coding-harness-5ane.22` and its last commit carries `Closes-Bead: coding-harness-5ane.22`.
- Special runs: a planted shell mutation is shown to fail, with its commit in the pull request body.

## Open decisions

[DETAIL] The current five roles are named explicitly because their role descriptions do not provide a reliable machine-readable classification; the baseline makes mutation checks non-circular and does not silently claim coverage of future roles.

[DECISION]

Thema: Aussagekraft der Regel für Agentenwerkzeuge.
Absicht: Der neue Test soll das offene Prüfventil schließen, ohne mehr Schutz zu behaupten, als er nachweist.
Heute: Die Regel verlangt zusätzlich begrenzte Shell-Nutzung und vier Verbote; der vorgesehene Test prüft diese nicht. Die Regeldatei darf nur der Maintainer ändern.
Repository-Änderung: Der Test macht das Ventil fällig; die Regeldatei muss danach passend geändert werden, damit die Gesamtprüfung besteht.
Architektur-Änderung: Die bestehenden Berechtigungen bleiben unverändert; zusätzliche Durchsetzung wäre eine eigene Änderung.

Ziel in einem Satz: Die Regel soll den tatsächlich nachgewiesenen Schutz korrekt ausweisen.
Option 1 — Teilprüfung ausweisen: Die Shell-Prüfung wird als Teilprüfung gekennzeichnet und die übrigen Anforderungen bleiben offen. Nachteil: Die vollständige Regel ist noch nicht durchgesetzt.
Option 2 — Vollständige Durchsetzung abwarten: Die Regel wird erst nach separater Prüfung aller Anforderungen hochgestuft. Nachteil: Der Abschluss dieses Arbeitsauftrags verzögert sich.
Empfehlung: Option 1, weil sie den nachgewiesenen Fortschritt sichtbar macht, ohne die übrigen Anforderungen als geprüft darzustellen.
Wenn du „ok“ sagst: Ein genauer Vorschlag für die Kennzeichnung als Teilprüfung wird vorbereitet; die übrigen Anforderungen bleiben offen.
Was verloren geht: Option 2 würde die Hochstufung erst bei vollständig nachgewiesener Durchsetzung erlauben.
Akzeptierter Nachteil: Bei Option 1 bleibt die vollständige Durchsetzung offen; bei Option 2 verzögert sich der Abschluss.

Welchen Nachteil akzeptierst du: Option 1 oder Option 2?
