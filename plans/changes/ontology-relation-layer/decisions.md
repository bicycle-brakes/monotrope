---
title: "Decisions — ontology-relation-layer"
class: architectural
status: draft
implementation_status: none
date: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-19
supersedes: null
superseded_by: null
bead: coding-harness-kpo7
owner: Data Architect
provenance: ai-drafted-reviewed
review: {status: pending, approved_by: null, approved_at: null}
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-19"}
tags: [decisions, interview]
---

# ontology relation layer — Decisions

Class: architectural (bead coding-harness-kpo7, the ontology relation layer
epic). Phase 1a, held with the maintainer in the conversation on 2026-11-19,
in German. The questions are the twelve prepared in `interview-prep.md`
(Q1–Q12). Together they close the 104 obligation items `H-1` … `H-104` of the
research swarm's complete run `bb903f1132e2711d2a789c03072d2793` (short:
bb903f11) in `research.md`. Each record links the items it closes in
`research_items`, exactly as the prep assigns them.

Interview minimum: an architectural change that claims its own ADR owes five
counted records (`scripts/check_interview_minimums.py`); Q-8 below decides one
new ADR. Twelve are recorded.

What follows from the answers for the order of work: the spec waits for the
one front-matter module (bead coding-harness-rg8i, Q-3) and for the
policy-engine spike (bead coding-harness-uvau, Q-9), which blocks this
change's spec.

## Q-1 · Which is the declaration of record: the YAML files or the models?

asked: 2026-11-19
answer: "A: YAML bleibt" — the YAML files (`decisions/gates.yaml`, `provenance.yaml`) and `plans_registry.REQUIRED` stay the declaration of record; the typed models read them at every run and copy no value; existing validators and their pinned messages stay; the two extra field lists are left to the front-matter bead (coding-harness-rg8i).
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-4
  - bb903f1132e2711d2a789c03072d2793/H-5
  - bb903f1132e2711d2a789c03072d2793/H-9
  - bb903f1132e2711d2a789c03072d2793/H-19
  - bb903f1132e2711d2a789c03072d2793/H-20
  - bb903f1132e2711d2a789c03072d2793/H-42
  - bb903f1132e2711d2a789c03072d2793/H-52
  - bb903f1132e2711d2a789c03072d2793/H-57
  - bb903f1132e2711d2a789c03072d2793/H-65
  - bb903f1132e2711d2a789c03072d2793/H-76
  - bb903f1132e2711d2a789c03072d2793/H-79
context: |
  Topic: where the one truth about gates, provenance classes and required header fields lives once typed models exist.
  Intention: every later choice (validators, rendering, kit) depends on it, and the research swarm raised it eleven times.
  Today: decisions/gates.yaml (human-decided) and provenance.yaml declare the closed vocabularies. plans_registry.REQUIRED (scripts/plans_registry.py:39) declares the required plan-header fields. Two more field lists exist (new_change._known_field_values, check_docs.PFlicht). ci_gates.validate_schema checks the gate file with messages that tests pin. No Python model exists.
  Repository change: one new module of Pydantic models that read the two YAML files and REQUIRED at every run. Existing validators and their messages stay.
  Architecture change: a typed reading layer between the declaration files and the gates; no new declaration.
  Options shown: A — the YAML files and REQUIRED stay the record, the models read them at every run and copy no value (recommended); B — the models become the record and the YAML is generated from them; C — models beside the YAML with their own copied values, which house rule 9 forbids.
  Explained on request before the answer: the maintainer asked what the difference between the YAML files and the models is, then which answer follows "code before prose". The answer given: house rule 9 (one entry point and one writer per action) is met by A and by B alike, because the YAML is data that code reads, not prose; A keeps the decisions in a language-neutral file, which suits the long-term direction towards Rust.

In the context of typed models for gates, provenance classes and required
header fields, facing the choice between the human-decided YAML files and the
models as the one declaration, we decided that the YAML files and
`plans_registry.REQUIRED` stay the declaration of record and the models only
read them at every run, to achieve types without moving the human-decided
record or any pinned message, accepting that the two other required-field
lists wait for the front-matter bead — 2026-11-19

## Q-2 · Who owns the Rule: this change or the rule registry?

asked: 2026-11-19
answer: "A: Aufteilen" — split ownership: the rule registry epic (coding-harness-73gi) owns the rule list and its enforcement states (its YAML once built, until then the enforcer column of `docs/governance/regelwerk.md`); this change owns the typed `Rule` reading and the "rule loses its last gate" check; `decisions/gates.yaml` gains no field.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-3
  - bb903f1132e2711d2a789c03072d2793/H-37
  - bb903f1132e2711d2a789c03072d2793/H-38
  - bb903f1132e2711d2a789c03072d2793/H-46
  - bb903f1132e2711d2a789c03072d2793/H-71
  - bb903f1132e2711d2a789c03072d2793/H-73
  - bb903f1132e2711d2a789c03072d2793/H-99
  - bb903f1132e2711d2a789c03072d2793/H-101
context: |
  Topic: the entity "rule" and the edge "a rule is protected by a gate".
  Intention: this change's main acceptance, "red when a rule loses its last gate", needs a list of rules. The rule registry epic (bead coding-harness-73gi) builds exactly that list.
  Today: docs/governance/regelwerk.md holds 33 rules (count from bead coding-harness-73gi, 2026-11-18), each with an enforcer that tests/test_regelwerk.py checks exists. The nine house rules and the operating rules of docs/WORKFLOW.md are outside it. All seats agree that no check reads a rule-to-gate edge from decisions/gates.yaml.
  Repository change: a typed Rule reading and a "last gate" check that reads the registry. gates.yaml gains no field.
  Architecture change: the registry becomes the source of the protects edge; the relation layer only reads it.
  Options shown: A — split: the registry owns the rule list, this change owns the typed reading and the check, no gates.yaml schema change (recommended); B — this change owns list and model and the registry consumes them, so the two scopes collide; C — the registry owns everything and this change drops Rule, losing its clearest measurable acceptance.

In the context of a "last gate" check that needs a list of rules, facing a
rule registry epic that builds that list, we decided to split ownership so
that the registry owns the rule list and this change owns the typed `Rule`
reading and the check, to achieve one owner per declaration with the check
still landing in this change, accepting that the check covers the rulebook's
rules now and the house rules only once the registry lands — 2026-11-19

## Q-3 · Does this change wait for the one front-matter module?

asked: 2026-11-19
answer: "A: rg8i zuerst" — the front-matter bead (coding-harness-rg8i, one front-matter module and a gate that finds a script's own header parser) ships first; this change builds its typed header model on that one module and adds no reader of its own.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-6
  - bb903f1132e2711d2a789c03072d2793/H-8
  - bb903f1132e2711d2a789c03072d2793/H-21
  - bb903f1132e2711d2a789c03072d2793/H-77
  - bb903f1132e2711d2a789c03072d2793/H-78
  - bb903f1132e2711d2a789c03072d2793/H-84
context: |
  Topic: reading YAML headers.
  Intention: a typed header model needs one reader. Bead coding-harness-rg8i (one front-matter module, and a gate that finds a script's own header parser) plans exactly that.
  Today: at least seven scripts read headers themselves (bead coding-harness-rg8i). They disagree on BOM and CRLF, on duplicate keys and on "no header" against "malformed header". That bead's notes of 2026-11-19 already hold these four items (H-21, H-77, H-78, H-84).
  Repository change: none in this change; the front-matter bead ships first.
  Architecture change: none from this question; it sets the order of two changes.
  Options shown: A — the front-matter bead first, this change builds on its module (recommended); B — this change absorbs the front-matter bead, one much larger change mixing two scopes; C — the model gets its own reader now, an eighth private parser against house rule 9.

In the context of seven scripts that each read headers their own way, facing
a typed header model that needs exactly one reader, we decided that the
front-matter bead ships first and this change builds on its module, to
achieve one header reader without a second route, accepting that the relation
layer starts later — 2026-11-19

## Q-4 · A new gate, or absorb the four existing checks?

asked: 2026-11-19
answer: "A: Neues Gate" — one new gate with its own id; the four existing checks (dangling bead ids, decision continuity, research handoff, frontmatter current) stay unchanged and may delegate later in changes of their own; a disagreement between a parser and the shared model is exit 3 ("not measured"), never a pass or a rule finding.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-14
  - bb903f1132e2711d2a789c03072d2793/H-25
  - bb903f1132e2711d2a789c03072d2793/H-43
  - bb903f1132e2711d2a789c03072d2793/H-69
  - bb903f1132e2711d2a789c03072d2793/H-72
  - bb903f1132e2711d2a789c03072d2793/H-80
  - bb903f1132e2711d2a789c03072d2793/H-83
  - bb903f1132e2711d2a789c03072d2793/H-86
  - bb903f1132e2711d2a789c03072d2793/H-87
  - bb903f1132e2711d2a789c03072d2793/H-88
  - bb903f1132e2711d2a789c03072d2793/H-90
context: |
  Topic: where the one reasoner over typed edges sits among the gates.
  Intention: absorbing the four checks moves their findings texts, exit codes and callers. The swarm asked about it eleven times.
  Today: 24 gates in decisions/gates.yaml (research.md, fd2b8701, 2026-11-18). The four checks (check_dangling_bead_ids.py, check_decision_continuity.py, check_research_handoff.py, check_frontmatter_current.py) each parse on their own and exit 3 when they cannot measure. Their callers: gates.yaml, the generated ci.yml, verify_all.sh, stage2.py and prompts.
  Repository change: one new gate id (a decision PR, house rule 8), its seeded red-run test, and the projection module. The four checks stay untouched.
  Architecture change: a new gate that reads an in-memory projection rebuilt on every run, so it cannot go stale.
  Options shown: A — one new gate with its own id, the four checks stay, parser/model disagreement is exit 3 (recommended); B — absorb the four now, moving findings texts, pinned tests and every caller in one change; C — like A, but the new gate starts as report and blocks after a dated valve.

In the context of one reasoner over typed edges beside four checks that each
parse on their own, facing findings texts, exit codes and callers that tests
pin, we decided on one new gate with its own id while the four checks stay
untouched, with a parser and model disagreement reported as exit 3, to
achieve the smallest blast radius and folding in existing routes only by
changes of their own, accepting that two readers coexist until those
follow-ups — 2026-11-19

## Q-5 · Is Pydantic the basis, and how far do earlier refusals reach?

asked: 2026-11-19
answer: "A: Ja, Pydantic" — both recorded refusals (verify-tmp-cleanup Q-6, decision-statement-skeleton's [DETAIL]) are scoped to their own problem and do not bind this change; Pydantic is the basis of the typed models.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-2
  - bb903f1132e2711d2a789c03072d2793/H-7
  - bb903f1132e2711d2a789c03072d2793/H-41
  - bb903f1132e2711d2a789c03072d2793/H-47
  - bb903f1132e2711d2a789c03072d2793/H-53
  - bb903f1132e2711d2a789c03072d2793/H-56
  - bb903f1132e2711d2a789c03072d2793/H-98
context: |
  Topic: the library behind the typed models.
  Intention: two archived changes declined Pydantic and Jinja2. The swarm asks whether those answers bind this change.
  Today: pyproject.toml pins pydantic 2.13.5 and Jinja2 3.1.6, and no script imports either (grep, 2026-11-18). verify-tmp-cleanup's record Q-6 says "Pydantic or Jinja do not help: only pytest knows what it makes of its option sources". decision-statement-skeleton's [DETAIL] says "a second record representation is unnecessary for this refusal".
  Repository change: the first import pydantic under scripts/.
  Architecture change: none beyond Q1.
  Options shown: A — both refusals are per problem, Pydantic is the basis (recommended); B — a standing preference against the libraries, standard-library dataclasses and hand checks; C — decide after a short spike that builds one model both ways.

In the context of typed models over the repository's declaration files,
facing two archived answers that declined Pydantic and Jinja2 for other
problems, we decided that those refusals are per problem and that Pydantic is
the basis of the models, to achieve typed reading with the library the
repository already pins, accepting the first `import pydantic` under
`scripts/` — 2026-11-19

## Q-6 · Render headers with Jinja2, or validate and write through one function?

asked: 2026-11-19
answer: "C: Alles als .md.j2" — every artefact, kit templates included, is rendered as a `.md.j2` Jinja2 template; `provenance.yaml`'s `frontmatter: none` for `templates/` changes through a decision PR; bead coding-harness-kpo7.2 (one Jinja2 template for every artefact header) is re-scoped to this.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-22
  - bb903f1132e2711d2a789c03072d2793/H-31
  - bb903f1132e2711d2a789c03072d2793/H-66
  - bb903f1132e2711d2a789c03072d2793/H-70
context: |
  Topic: who writes artefact headers.
  Intention: bead coding-harness-kpo7.2 (one Jinja2 template for every artefact header) proposes a renderer. House rule 9 asks for one writer per action.
  Today: new_change._frontmatter_template() (scripts/new_change.py:80) writes new headers as an f-string. check_frontmatter_current.stamp rewrites updated:, and archive_closed_changes rewrites four lifecycle fields. No file under templates/ carries a Jinja2 marker, and provenance.yaml declares frontmatter: none for them.
  Repository change (for the recommended A): one header writer function (in the front-matter module) that every writer site calls; every header validated against the model.
  Architecture change (for A): none beyond Q1 and Q3.
  Options shown: A — validate every header against the model, every header write through one writer function, no Jinja2 in this change (recommended); B — one Jinja2 template renders new headers (the bead as written), so stamping and archiving stay separate writers; C — render every artefact, kit templates included, as .md.j2; provenance.yaml's frontmatter: none for templates/ changes (a file the runner holds) and the template tests grow; the largest change.

In the context of three header writers today and a bead that proposes one
Jinja2 template, facing house rule 9's one writer per action, we decided to
render every artefact, kit templates included, as a `.md.j2` Jinja2 template
and to change `provenance.yaml`'s `frontmatter: none` for `templates/` through
a decision PR, to achieve one rendering route for every artefact, accepting
the largest of the three options, a decision PR on a runner-held file, growing
template tests and the re-scope of bead coding-harness-kpo7.2 — 2026-11-19

## Q-7 · Which relations enter the closed vocabulary, and where is it declared?

asked: 2026-11-19
answer: "C: Spec entscheidet" — the spec decides the first closed relation vocabulary as a [DETAIL], with its reason in the spec; it is not settled in this interview.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-48
  - bb903f1132e2711d2a789c03072d2793/H-51
  - bb903f1132e2711d2a789c03072d2793/H-58
  - bb903f1132e2711d2a789c03072d2793/H-64
  - bb903f1132e2711d2a789c03072d2793/H-89
context: |
  Topic: the list of named relations the layer knows.
  Intention: a vocabulary that grows on demand is not a vocabulary (research.md, "What is unclear").
  Today: research.md proposes eight: protects, answers, claims, derives-from, supersedes, belongs-to, blocks, cites. The archived change adr-owning-change already enforces adr_files as the claim of ADR files. It left two points open by decision: no check that a claimed file exists, and archived changes claim nothing.
  Repository change (for the recommended A): three relations in a human-decided file; the models read them.
  Architecture change (for A): a closed list that only a decision PR extends.
  Options shown: A — start with three relations that have a record or a measured gap (protects, claims derived from adr_files and a plan's bead:, answers), declared in a human-decided file (recommended); B — all eight now, some without a check; C — leave the set to the spec as a detail, so the spec's author decides a vocabulary that is meant to be human-decided.

In the context of eight proposed relations for a closed vocabulary, facing
relations that differ in whether a record or a gate reads them, we decided
that the spec decides the first closed relation vocabulary as a detail with
its reason, to achieve a set chosen with the spec's full view of the gates,
accepting that the spec's author, not this interview, sets a vocabulary meant
to be closed, and that the maintainer sees it at spec review and at merge
— 2026-11-19

## Q-8 · Class, ADR and kit

asked: 2026-11-19
answer: "A: Neues ADR" — the class stays `architectural`; one new ADR of its own is drafted in phase 2b (design), its number set at merge; the ADR states that ADR 0009 governs architecture models, not a typed schema over repository files; the kit ships the module and each instance declares its own vocabularies.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-26
  - bb903f1132e2711d2a789c03072d2793/H-27
  - bb903f1132e2711d2a789c03072d2793/H-29
  - bb903f1132e2711d2a789c03072d2793/H-30
  - bb903f1132e2711d2a789c03072d2793/H-33
  - bb903f1132e2711d2a789c03072d2793/H-39
  - bb903f1132e2711d2a789c03072d2793/H-40
  - bb903f1132e2711d2a789c03072d2793/H-44
  - bb903f1132e2711d2a789c03072d2793/H-97
context: |
  Topic: the change's class, the ADR it owes, and what the kit carries.
  Intention: the class sets the phases and the interview minimum; the ADR number is contested.
  Today: the class is declared architectural. docs/WORKFLOW.md says an architectural change "carries its ADR already" (line 433) and asks for "an ADR draft" in design.md (phase 2b, line 86). ADR 0009 keeps "an Architectural change requires an ADR in the same pull request". Its bullet "No model as code in the kit now" names LikeC4, a model/ scaffold, the likec4 gates and Node.js. origin/main f31d216e ends at ADR 0025. Numbers 0026 and 0027 are drafted on the branches feat/central-config and feat/review-fewer-rounds (no pull request found, 2026-11-19).
  Repository change: one ADR file, claimed under adr_files in the spec header.
  Architecture change: recorded in that ADR. The kit carries the module as mechanism, and each instance declares its own vocabularies.
  Options shown: A — keep architectural, one new ADR drafted in phase 2b, its number set at merge (0028 the next unused on 2026-11-19) (recommended); B — reclassify as feature, no ADR; C — architectural, but amend ADR 0009 instead of a new ADR.

In the context of a change that adds a subsystem every later gate may read,
facing a contested ADR number and an ADR 0009 that speaks about architecture
models, we decided to keep the class `architectural` with one new ADR drafted
in phase 2b and numbered at merge, the kit shipping the module while each
instance declares its own vocabularies, to achieve a recorded architecture
decision that does not mix with ADR 0009, accepting five owed interview
records and an ADR in the same pull request — 2026-11-19

## Q-9 · External standards and online evidence

asked: 2026-11-19
answer: "C: Engine prüfen" — first evaluate a policy engine (OPA, CUE or CEL) in a research-swarm spike; the orchestrator created the spike as bead coding-harness-uvau, which blocks this change's spec.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-10
  - bb903f1132e2711d2a789c03072d2793/H-11
  - bb903f1132e2711d2a789c03072d2793/H-12
  - bb903f1132e2711d2a789c03072d2793/H-13
  - bb903f1132e2711d2a789c03072d2793/H-16
  - bb903f1132e2711d2a789c03072d2793/H-17
  - bb903f1132e2711d2a789c03072d2793/H-18
  - bb903f1132e2711d2a789c03072d2793/H-91
  - bb903f1132e2711d2a789c03072d2793/H-94
  - bb903f1132e2711d2a789c03072d2793/H-95
  - bb903f1132e2711d2a789c03072d2793/H-102
context: |
  Topic: whether an outside format or engine should carry the model, and what the online topics prove.
  Intention: eleven items from the online topics 9–11 ask for a reference tool or an evidence standard.
  Today: the reconciliation finds no retrieved tool shown to be a typed relation layer shared by repository gates. dependency-cruiser is adjacent. The failure records show parser divergence, but none of them in gate checkers. Several excerpts held only titles and boilerplate. research.md rules out RDF, OWL and YAML-LD, and requires that a gate run with pip only.
  Repository change (for the recommended A): none.
  Architecture change (for A): none.
  Options shown: A — an internal vocabulary (YAML plus Pydantic), outside tools as background only (recommended); B — like A, plus a published JSON Schema export; C — first evaluate a policy engine (OPA, CUE or CEL) through a research-swarm spike, a delay and possibly a runtime that pip alone does not provide (not checked).

In the context of a typed relation layer that outside policy engines might
carry, facing online evidence that neither shows nor rules out such an engine
for repository gates, we decided to evaluate a policy engine (OPA, CUE or CEL)
first in a research-swarm spike (bead coding-harness-uvau) before the spec, to
achieve a measured answer instead of an assumed one, accepting the delay of
one spike and a possible runtime beyond pip — 2026-11-19

## Q-10 · Which neighbours enter the spec header?

asked: 2026-11-19
answer: "A: Alle sechs" — the spec header keeps all six neighbours (the two given and the four confirmed, including the two that contradict the premise), drops address-drift-warning, and adds none.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-49
  - bb903f1132e2711d2a789c03072d2793/H-50
  - bb903f1132e2711d2a789c03072d2793/H-103
  - bb903f1132e2711d2a789c03072d2793/H-104
research_neighbours: {keep: [plans/changes/archive/2026-09-29-frontmatter-current/spec.md, plans/changes/archive/2026-11-06-provenance-location/spec.md, plans/changes/archive/2026-11-06-adr-owning-change/spec.md, plans/changes/archive/2026-11-16-decision-statement-skeleton/spec.md, plans/changes/archive/2026-11-16-explore-provenance/spec.md, plans/changes/archive/2026-11-16-verify-tmp-cleanup/spec.md], drop: [plans/changes/archive/2026-11-16-address-drift-warning/spec.md], add: []}
context: |
  Topic: the neighbours: list of the future spec.md.
  Intention: the research-handoff gate holds the spec header to the run's neighbour records. A contradicting neighbour needs a keep or drop from the maintainer.
  Today: run bb903f11 lists two given paths (frontmatter-current, provenance-location) and four confirmed ones (adr-owning-change, decision-statement-skeleton, explore-provenance, verify-tmp-cleanup). It rejected address-drift-warning, because all three seats judged it unrelated. Two confirmed neighbours contradict the premise: their Pydantic and Jinja2 refusals (see Q5).
  Repository change: six paths in the spec header.
  Architecture change: none.
  Options shown: A — keep all six, drop address-drift-warning, so the spec has to answer the two contradicting neighbours (recommended); B — keep the four related ones, drop the two that contradict.

In the context of a spec header that the research-handoff gate holds to the
run's neighbour records, facing two confirmed neighbours that contradict the
premise and one suggested neighbour that all seats judged unrelated, we
decided to keep all six given and confirmed neighbours and drop
address-drift-warning, to achieve a spec that must answer the recorded
counter-positions, accepting a longer header — 2026-11-19

## Q-11 · Who wrote research.md, and what does its header say?

asked: 2026-11-19
answer: "A: Absatz korrigieren" — the stale body paragraph of `research.md` that says `produced_by` is absent is corrected now; the header stays as the runner wrote it; the hand-written part gets its producer once bead coding-harness-uo6s (no honest producer name for an OpenCode session) gives OpenCode a name.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-28
  - bb903f1132e2711d2a789c03072d2793/H-45
  - bb903f1132e2711d2a789c03072d2793/H-54
  - bb903f1132e2711d2a789c03072d2793/H-62
  - bb903f1132e2711d2a789c03072d2793/H-100
context: |
  Topic: the provenance of this change's own research artefact.
  Intention: review finding R-3 on PR #411 (noted on the epic coding-harness-kpo7) found header and body contradicting each other. The swarm found it again.
  Today (read at 92f3b2fa): the header carries two produced_by entries stage2-research-swarm (versions 2026-11-18 and 2026-11-19). The body (lines 83–88) still says produced_by "is deliberately absent". The hand-written part came from an OpenCode session that RESEARCH_PROGRAMS cannot name (bead coding-harness-uo6s). ai-drafted-reviewed with review.status: pending is the usual pairing in change artefacts (for example, verify-tmp-cleanup's decisions.md).
  Repository change: one corrected paragraph in research.md.
  Architecture change: none.
  Options shown: A — correct the stale body paragraph now, leave the header as the runner wrote it (recommended); B — also remove the 2026-11-18 swarm entry by hand, a side route under house rule 9; C — change nothing until bead coding-harness-uo6s lands.

In the context of a research artefact whose body denies the producer entries
its header carries, facing a hand-written part whose harness the closed
program vocabulary cannot name, we decided to correct the stale body
paragraph now and leave the runner-written header unchanged, to achieve a
true statement without hand-editing runner output, accepting that the
hand-written part has no producer entry until bead coding-harness-uo6s lands
— 2026-11-19

## Q-12 · Accept the sort of the remaining 23 items, and which beads to create

asked: 2026-11-19
answer: "Wie empfohlen" — as recommended: the sort of the 23 items is accepted; B-1, B-2 and B-5 are created as beads, B-3 is added as a note to bead coding-harness-hg6w, B-4 is declined. The orchestrator created B-1 as bead coding-harness-iheo, B-2 as bead coding-harness-z976 and B-5 as bead coding-harness-ddt2, and wrote B-3 as a note on coding-harness-hg6w.
answered_by: maintainer
status: answered
research_items:
  - bb903f1132e2711d2a789c03072d2793/H-1
  - bb903f1132e2711d2a789c03072d2793/H-15
  - bb903f1132e2711d2a789c03072d2793/H-23
  - bb903f1132e2711d2a789c03072d2793/H-24
  - bb903f1132e2711d2a789c03072d2793/H-32
  - bb903f1132e2711d2a789c03072d2793/H-34
  - bb903f1132e2711d2a789c03072d2793/H-35
  - bb903f1132e2711d2a789c03072d2793/H-36
  - bb903f1132e2711d2a789c03072d2793/H-55
  - bb903f1132e2711d2a789c03072d2793/H-59
  - bb903f1132e2711d2a789c03072d2793/H-60
  - bb903f1132e2711d2a789c03072d2793/H-61
  - bb903f1132e2711d2a789c03072d2793/H-63
  - bb903f1132e2711d2a789c03072d2793/H-67
  - bb903f1132e2711d2a789c03072d2793/H-68
  - bb903f1132e2711d2a789c03072d2793/H-74
  - bb903f1132e2711d2a789c03072d2793/H-75
  - bb903f1132e2711d2a789c03072d2793/H-81
  - bb903f1132e2711d2a789c03072d2793/H-82
  - bb903f1132e2711d2a789c03072d2793/H-85
  - bb903f1132e2711d2a789c03072d2793/H-92
  - bb903f1132e2711d2a789c03072d2793/H-93
  - bb903f1132e2711d2a789c03072d2793/H-96
context: |
  Topic: items that are not decisions for this change.
  Intention: close them in one answer, and create only the beads the maintainer accepts. Today's gate needs an answered record even for a duplicate.
  Today: this question holds 9 duplicates, 11 settled items and 3 bead proposals. The other four duplicates (H-21, H-77, H-78, H-84) sit in Q3, and the other four settled items in Q2 (H-99, H-101), Q4 (H-88) and Q11 (H-28).
  Duplicates shown: H-1 and H-85 to coding-harness-dwsk (one declaration for the research program vocabulary), H-85 also coding-harness-uo6s; H-61 to coding-harness-uo6s (no honest producer name for an OpenCode session); H-24 to coding-harness-c20s (gate-catalog.md calls ci_gates.py the one reader); H-34 to coding-harness-hg6w (AGENTS.md 1a table names no architectural minimum); H-63 to coding-harness-oqv7 (stage2-session spec still names gpt-6.1-sol); H-67 to coding-harness-glqo (a timed-out seat voids the run), ADR 0020's rule that only a complete run counts stands; H-75 to coding-harness-36z (D-60 write guard); H-92 to coding-harness-dd3v (template header test covers 5 of 10 templates).
  Settled shown: H-23, H-36, H-55 — a new gate is a decision PR (house rule 8); H-32 — the prep sorts research.md's open items; H-35, H-74, H-81 — run bb903f11 is complete; H-59 — the seat amendment of ADR 0020 is on origin/main; H-60 — the 40-minute finder limit is held in research-swarm-limits.yaml by decision PR #414 (open on 2026-11-19); H-68 — a new gate needs a seeded control test (tests/test_ci.py:3845); H-82 — the leak check's limits and the accepted consequence stand in docs/WORKFLOW.md.
  Bead proposals shown: B-1 (bounded) provenance.yaml's reader note is wrong, from H-96; B-2 (bounded) a stale comment above stage2.RUNNER_HELD, found while checking H-23; B-3 docs/WORKFLOW.md says when an architectural change writes its ADR in two ways, as a note on coding-harness-hg6w, from H-27; B-4 (bounded) online failure-record topics should cite dated primary records, from H-15, recommended decline; B-5 (bounded) the mutation-exemption ratchet does not ratchet, from H-93.
  Repository change: none in this change. Accepted beads are created by the session that writes the tracker, as discovered-from the epic coding-harness-kpo7.
  Architecture change: none.
  Options shown: A — accept the sort, create B-1, B-2 and B-5, add B-3 as a note to coding-harness-hg6w, decline B-4 (recommended); B — accept the sort, create no bead; C — accept the sort and choose the proposals one by one.

In the context of 23 inventory items that are duplicates, settled facts or
bead proposals, facing a gate that closes every item only through an answered
record, we decided to accept the sort as recommended, with beads for B-1, B-2
and B-5, B-3 as a note on bead coding-harness-hg6w and B-4 declined, to
achieve closed items and tracked follow-up work outside this change,
accepting that no gate of this change rests on dated online incident records
— 2026-11-19
