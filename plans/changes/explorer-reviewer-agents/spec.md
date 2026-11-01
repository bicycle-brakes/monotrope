---
title: "Spec — explorer-reviewer-agents"
status: draft
implementation_status: none
date: 2026-11-01
last_reviewed: 2026-11-01
updated: 2026-11-01
supersedes: null
superseded_by: null
bead: coding-harness-9ll
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: gpt-6.1-sol, version: "2026-11-01"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, sub-agents]
class: bounded
appetite: 1
adr_files: []
neighbours: []
---

# Spec — explorer-reviewer-agents

Provide the two read-only Claude Code helpers already promised by the workflow,
with the maintainer's chosen models (bead coding-harness-9ll — supply explorer
and reviewer definitions). Research: `research.md`. Decisions: `decisions.md`.

## Problem

- At `544cb659` on 2026-11-01, neither promised agent definition exists;
  `docs/WORKFLOW.md` §3 promises both as read-only helpers with pinned models
  (`research.md`, "What exists today"). Ad hoc helpers have no shared role
  definition to reuse.
- The workflow's setup check leaves actual model selection unmeasured;
  a definition alone does not prove that Claude Code uses its model
  (`research.md`, "What is unclear"). The maintainer has now chosen Haiku 5.5
  for exploration and Opus 5.5 at high effort for review (`decisions.md#Q-1`).
- Adding the definitions also adds endpoint-test cases to the exported kit;
  its endpoint declaration does not travel, and its exception cap has no room
  for the additional cases. This conflicts with the recorded three-file scope
  (`research.md`, "Draft follow-up — 2026-11-01").

## Acceptance criteria

1. When Claude Code reads the repository's explorer definition, the configuration selects Claude Haiku 5.5.
   *Refuted by:* a missing definition or a model setting other than `claude-haiku-5-5`.
   *Basis:* `decisions.md#Q-1`.

2. When Claude Code reads the repository's reviewer definition, the configuration selects Claude Opus 5.5 at high effort.
   *Refuted by:* a missing definition, a model setting other than `claude-opus-5-5`, or an absent or different effort setting.
   *Basis:* `decisions.md#Q-1`.

3. While either helper operates, its configured tool allowlist contains only repository reading and search tools.
   *Refuted by:* any tool beyond `Read`, `Grep` and `Glob`, including a shell, a writer, delegation or unrestricted inherited tools.
   *Basis:* `decisions.md#Q-1`; `research.md`, workflow sub-agent promise.

4. When either definition is read, its instructions state the corresponding read-only reporting role.
   *Refuted by:* an explorer that lacks source-backed findings and explicit unknowns, a reviewer that lacks findings against the supplied spec and evidence, or either role authorizing repairs, commits, tracker writes or acceptance of its own work.
   *Basis:* `research.md`, runner exploration role and evidence governance.

5. When the repository's agent-governance checks inspect the new definitions, both satisfy the existing evidence, endpoint and instance-neutrality rules.
   *Refuted by:* a changed or missing verbatim evidence-contract paragraph, an undeclared model, or instance terminology rejected by the existing tests.
   *Basis:* `research.md`, governance of new agent definitions.

6. When each helper is invoked in a fresh Claude Code session, observed model selection matches its definition.
   *Refuted by:* the explorer running on the parent model instead of Haiku 5.5, the reviewer running on another model, or a missing observation for either invocation.
   *Basis:* `decisions.md`, "Details for the draft"; `research.md`, setup check.

## Non-goals

- The missing stop hook, artefact validator, central model registry and changes
  to Stage-2 routing rules; these remain separate work.
- Editing or translating the seven existing agent definitions, or changing
  the normative evidence contract or model declarations.
- Granting either helper write, execution or orchestration powers.
- Design phase 2b and an ADR: this remains a bounded delivery of existing
  workflow promises, with no architecture change.

## Protected areas

The runner never edits `.claude/`; the orchestrator installs the two new
definitions after the accepted attempt. All other files there stay untouched.
`AGENTS.md`, `model-endpoints.yaml`, `provenance.yaml`, `decisions/gates.yaml`,
`docs/governance/regelwerk.md`, existing ADRs and the tracker remain unchanged.
The workflow notice, its test and kit bookkeeping remain outside the recorded
scope until the open scope decision is answered; no gate is bypassed meanwhile.

## Definition of Done

- `make verify` is green after the orchestrator installs the held definitions;
  an accepted runner attempt containing tests alone is not completion.
- Both fresh-session model observations, their commands and checked commit
  are recorded in `findings.md`; an unavailable observation is not a pass.
- No companion model or ADR file changes. Any inventory and kit maintenance
  first requires the scope decision below and is listed in the pull request.
- The pull request's file list respects protected areas and non-goals.
- The pull request closes the work item for the two helpers and its last
  commit carries `Closes-Bead: coding-harness-9ll`.

## Open decisions

The model choice in `decisions.md#Q-1` is settled and is not asked again.
The following scope conflict remains open; no maintainer answer is inferred.

### [DECISION] Complete delivery versus the recorded file limit

Topic: Zwei nur lesende Helfer für Recherche und Prüfung ausliefern.
Intention: Der Entwurf muss den festgehaltenen Umfang mit der bestehenden vollständigen Prüfung vereinbaren.
Today: Die Helfer fehlen. Festgehalten sind nur zwei Agentendateien und ein Testmodul. Neue Agenten erzeugen zusätzliche Prüffälle im übertragbaren Workflow-Kit; dessen Ausnahmeliste ist am 01.11.2026 bei Commit `544cb659` mit 42 von 42 Einträgen ausgeschöpft. Der Workflow führt die Helfer noch als damals fehlend auf.
Repository change: Zusätzlich zu den drei Lieferdateien würden der Workflow-Hinweis, sein vorhandener Test und die Kit-Ausnahmeliste samt sichtbarer Obergrenze nachgeführt.
Architecture change: Keine; Modelle, Leserechte und Phasen bleiben wie entschieden. Es ändern sich nur die ausgelieferten Definitionen und ihre Bestandsprüfung.

Goal in one sentence: Die beiden Helfer mit ehrlicher Dokumentation und vollständig bestandenen Prüfungen ausliefern.
Options:
1. Vollständig ausliefern: Die notwendigen Begleitänderungen gehören dazu; zwei zusätzliche Kit-Ausnahmen machen sichtbar, dass die Modellzuordnung im Ziel-Repository eine eigene Endpunktdeklaration braucht.
2. Beim engen Dateiumfang bleiben: Die Installation wartet auf eine gesonderte Änderung für diese Begleitpflege; bis dahin werden die Helfer nicht als fertig gemeldet.
Recommendation: Option 1 — sie liefert die bereits gewünschten Helfer zusammen mit den bestehenden Nachweisen aus.
If you say "ok": Die beiden Helfer und das neue Testmodul werden gebaut; `docs/WORKFLOW.md`, `tests/test_workflow_entry.py` und `scripts/kit/probe.py` werden im selben Änderungspaket nachgeführt, mit zwei zusätzlichen benannten Ausnahmen und einer Obergrenze von 44.
What is lost: Die Beschränkung dieses Änderungspakets auf genau drei Lieferdateien.

Darf dieses Änderungspaket die notwendige Begleitpflege einschließen?

[DETAIL] The phase-4 appetite is one hour including repairs, chosen as a stop
for this small definition-and-test delivery; exceeding it returns to the
orchestrator. Test names, ordering and English role wording are reversible
implementation details. A static allowlist check proves the configuration,
not runtime sandbox enforcement.
