---
title: "Interview preparation — ontology-relation-layer"
class: architectural
status: draft
implementation_status: none
date: 2026-11-19
last_reviewed: 2026-11-19
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-kpo7
owner: Data Architect
provenance: ai-drafted-reviewed
review: {status: pending, approved_by: null, approved_at: null}
neighbours:
  - plans/changes/archive/2026-09-29-frontmatter-current/spec.md
  - plans/changes/archive/2026-11-06-provenance-location/spec.md
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-19", model: "Opus 5.5"}
tags: [interview]
---

# ontology relation layer — Interview preparation

This page prepares phase 1a (the interview) for the change. It sorts each of
the 104 obligation items (`H-1` … `H-104`) of the research swarm's run
`bb903f1132e2711d2a789c03072d2793` (short: bb903f11) and groups them into
twelve questions for the maintainer. It answers nothing. Answers go into
`decisions.md` as interview records, as `prompts/01a-interview.md` describes.

**Cut-offs.** Inventory as committed at `92f3b2fa` (2026-11-19). Code and
documents read at that commit and at `origin/main` `f31d216e`. Tracker read on
2026-11-19 through `tools/bd` (279 open beads, read only). The research-handoff
gate reports at `92f3b2fa`: 4 runs in `research.md`, 1 complete, 104 items
pending.

**Not present.** `decisions.md` and `spec.md` do not exist in the change
folder at `92f3b2fa`, so nothing here is checked against them.

## How the sorting works

Bead `coding-harness-orbx` (research swarm results propose beads in the
interview) asks for every item to be sorted into a decision, a bead proposal
or a duplicate. This page adds two more kinds, so that nothing is forced into
the wrong one:

- **decision** — the maintainer decides it for this change.
- **bead proposal** — real work outside this change that no bead covers yet.
  Checked against the code and the tracker before it is offered.
- **duplicate** — an open bead already covers it.
- **settled** — a merged rule, a recorded decision or a measured fact already
  answers it. The source is named.
- **not here** — work for another repository. No item of this run is of this
  kind.

**One limit of today's gate.** The research-handoff gate
(`scripts/check_research_handoff.py`) closes an item only through a
maintainer-answered interview record that lists it in `research_items`. A
duplicate or a settled item is no exception. So every item, of any kind, sits
in exactly one of the twelve questions below. Question 12 collects 23 items that
are duplicates, settled facts or bead proposals, so one answer can close them;
the other items of those kinds sit next to the decision they belong to. Bead
`coding-harness-orbx` would change that rule; until it lands, this is the
route.

## Counts per kind

At `92f3b2fa`, 2026-11-19, over the 104 items of run bb903f11:

| Kind | Items |
| --- | --- |
| decision | 73 |
| settled | 15 |
| duplicate | 13 |
| bead proposal | 3 |
| not here | 0 |

The 73 decisions condense into eleven questions (Q1–Q11), because the swarm
asked most of them several times in different words. For example, four items
(H-3, H-37, H-38, H-46) ask who owns the `Rule` model. The bead proposals grow
to five (B-1 to B-5) in Question 12: two more come from facts checked while
sorting (B-2 from H-23, B-3 from H-27).

## The inventory

The last column names the question that closes the item. Bead ids appear with
a short title; the full titles are in the tracker.

<!-- markdownlint-disable MD013 MD060 -->

| H | Summary | Kind | Existing bead | Recommendation | Q |
|---|---|---|---|---|---|
| H-1 | The research program set is declared twice (`stage2.RESEARCH_PROGRAMS`, `research_census.PROGRAMS`). | duplicate | `coding-harness-dwsk` (one declaration for the research program vocabulary) | Leave it to that bead; it is outside this change. | Q12 |
| H-2 | Do the pinned, unused Pydantic and Jinja2 become the basis of the layer? | decision | `coding-harness-kpo7.1` (relations as Pydantic models), `coding-harness-kpo7.2` (one Jinja2 header template) | Pydantic yes (Q5), Jinja2 decided separately (Q6): the two libraries answer different needs. | Q5 |
| H-3 | Who owns the `Rule` model: this change or the rule registry? | decision | `coding-harness-73gi` (rule registry epic) | Split: the registry owns the rule list, this change owns the typed reading and the edge check (Q2). | Q2 |
| H-4 | Does a typed header model replace `plans_registry.REQUIRED` or derive from it? | decision | `coding-harness-kpo7.1` | Derive: `REQUIRED` stays the declaration of record, so archiving, PR sync and the scaffold keep working (Q1). | Q1 |
| H-5 | Does a `Gate` model replace `ci_gates.validate_schema` and its pinned messages? | decision | `coding-harness-kpo7.1` | Stand behind it first; replacing the validator is its own change (Q1). | Q1 |
| H-6 | Build the model on `check_frontmatter_current`'s reader functions or on a new reader? | decision | `coding-harness-rg8i` (one front-matter module) | Neither: build on the one module that bead creates (Q3). | Q3 |
| H-7 | Is the earlier answer "Pydantic or Jinja do not help" (verify-tmp-cleanup Q-6) a standing preference? | decision | — | Read it as scoped to pytest option parsing, which its own text names (Q5). | Q5 |
| H-8 | Are the private frontmatter parsers folded in here or in the front-matter bead? | decision | `coding-harness-rg8i` | In that bead, before this change, so no second route appears (Q3). | Q3 |
| H-9 | If a `Gate` model replaced the validator, which outputs regenerate and do pinned messages stay? | decision | `coding-harness-kpo7.1` | Moot under the recommended answer to Q1: nothing regenerates, messages stay. | Q1 |
| H-10 | Which public implementation is the reference for a typed relation model read by gates? | decision | — | None: no retrieved source shows one; treat the online results as background (Q9). | Q9 |
| H-11 | Which of CEL, OPA or CUE encodes gate rules best? | decision | — | None in this change; a gate must run with pip only (research.md, "Where it must not go") (Q9). | Q9 |
| H-12 | What evidence would make an online tool relevant to the gate design? | decision | — | A source showing the tool used as a shared model behind repository gates; none was retrieved (Q9). | Q9 |
| H-13 | Express the shared model in an external declarative format or keep it internal? | decision | — | Internal vocabulary; an export format only when a consumer exists (Q9). | Q9 |
| H-14 | When a gate's own parser and the shared model disagree, which one decides? | decision | `coding-harness-kpo7.3` (one reasoner over typed edges) | The disagreement is "not measured" (exit 3), never a pass or a rule finding (Q4). | Q4 |
| H-15 | Should the online failure topic cite dated primary records (CVE JSON) instead of prose advisories? | bead proposal | new proposal B-4 | Decline: no gate of this change rests on online incidents. | Q12 |
| H-16 | Does the online "divergent parser" vulnerability class justify one shared typed model? | decision | — | Only as background; the case rests on the repository's own measurements (Q9). | Q9 |
| H-17 | Should gate input be constrained through one typed model because of deserialization attacks? | decision | — | Background only; the readers already use safe YAML loading, keep it (Q9). | Q9 |
| H-18 | Justify the layer by the catalogue pattern, or wait for dated incident citations? | decision | — | Neither: justify by the internal measurements in research.md (Q9). | Q9 |
| H-19 | Who owns `REQUIRED` (name, type, test patch point) once a header model exists? | decision | `coding-harness-kpo7.1` | `plans_registry` keeps it unchanged; the model reads it (Q1). | Q1 |
| H-20 | Is the `Gate` model what `ci_gates.gates()` returns, or a separate module beside it? | decision | `coding-harness-kpo7.1` | Separate typed reading; `gates()` keeps its output for stage2.py and the tests (Q1). | Q1 |
| H-21 | Header reader: tolerant of BOM/CRLF, or strict `---\n`? | duplicate | `coding-harness-rg8i` (notes of 2026-11-19 already hold it) | That bead settles it in its one module. | Q3 |
| H-22 | Which header writers does a single renderer absorb (scaffold, stamp, stage2, archive)? | decision | `coding-harness-kpo7.2` | One header writer function; every writer site calls it (Q6). | Q6 |
| H-23 | Who edits `decisions/gates.yaml` to add a gate? | settled | `coding-harness-wqw` (closed; gave gates.yaml its class) | A decision PR (house rule 8): `provenance.yaml` maps the file to human-decided since 9446abe5, and the runner holds it. | Q12 |
| H-24 | Does this change correct the gate-catalog reader statement? | duplicate | `coding-harness-c20s` (gate-catalog.md calls ci_gates.py the one reader) | Leave it to that bead. | Q12 |
| H-25 | If the four checks were absorbed, which caller surfaces keep their contracts? | decision | `coding-harness-kpo7.3` | All of them: the four checks stay unchanged in this change (Q4). | Q4 |
| H-26 | Is `architectural` the right class? | decision | — | Keep it: the change adds a subsystem and owes an ADR (Q8). | Q8 |
| H-27 | Which ADR does the change owe, given two differently worded rules? | decision | `coding-harness-hg6w` (1a table names no architectural minimum) | One new ADR in the same PR, as ADR 0009 keeps for architectural changes (Q8). | Q8 |
| H-28 | Is `ai-drafted-reviewed` with review pending an honest research header? | settled | — | Yes: `review.status: pending` records the owed acceptance, the repository-wide convention (Q11). | Q11 |
| H-29 | Does the ADR take number 0026? | decision | — | No: 0026 and 0027 are used on open branches; the number is set at merge (Q8). | Q8 |
| H-30 | `architectural` or `feature`? | decision | — | Same as H-26 (Q8). | Q8 |
| H-31 | House rule 9 against a hand-edited header beside a renderer and a second declaration as models. | decision | — | One writer function and models that read the YAML, so no second declaration (Q1, Q6). | Q6 |
| H-32 | Which of research.md's open items are maintainer decisions? | settled | `coding-harness-orbx` (swarm results propose beads in the interview) | This file sorts them; the questions below are the decisions. | Q12 |
| H-33 | Which ADRs does the change create or amend, claimed under `adr_files`? | decision | — | One new ADR, claimed in the spec header; ADR 0009 not amended (Q8). | Q8 |
| H-34 | AGENTS.md's 1a table names no `architectural` minimum. | duplicate | `coding-harness-hg6w` | Leave it to that bead (proposed AGENTS.md text already in it). | Q12 |
| H-35 | How is the ADR 0020 handoff met after three incomplete runs? | settled | — | Run bb903f11 is complete (gate output 2026-11-19: 4 runs, 1 complete). | Q12 |
| H-36 | A new gate means a decision PR; how is `schema_version` handled? | settled | — | Decision PR by house rule 8; a new key's schema bump is a spec detail. | Q12 |
| H-37 | Rule model ownership (same as H-3). | decision | `coding-harness-73gi` | As H-3 (Q2). | Q2 |
| H-38 | Rule model ownership (same as H-3). | decision | `coding-harness-73gi` | As H-3 (Q2). | Q2 |
| H-39 | Does ADR 0009's "no model as code in the kit now" cover a typed relation layer? | decision | — | No: its bullet names LikeC4, a `model/` scaffold and Node.js; the new ADR says so (Q8). | Q8 |
| H-40 | Which lists does the kit ship, and which does each instance declare? | decision | `coding-harness-04fj` (kit, instances and LakeSwitch alignment) | Kit ships the module; each instance declares its own vocabularies (Q8). | Q8 |
| H-41 | Does Q-6's "Pydantic and Jinja do not help" extend to header modelling? | decision | — | As H-7 (Q5). | Q5 |
| H-42 | Declaration of record: the YAML files or the models? | decision | `coding-harness-kpo7.1` | The YAML files; the models are their typed reading (Q1). | Q1 |
| H-43 | Is a gate added, absorbed or retired inside this change at all? | decision | `coding-harness-kpo7.3` | Added: one new gate; nothing absorbed or retired (Q4). | Q4 |
| H-44 | ADR 0009 coverage (same as H-39). | decision | — | As H-39 (Q8). | Q8 |
| H-45 | research.md's body says `produced_by` is absent; its header carries it. | decision | `coding-harness-uo6s` (no honest producer name for OpenCode) | Correct the stale body paragraph in this change (Q11). | Q11 |
| H-46 | Rule model ownership (same as H-3). | decision | `coding-harness-73gi` | As H-3 (Q2). | Q2 |
| H-47 | Does decision-statement-skeleton's refusal of Pydantic/Jinja2 bind this change? | decision | — | No: its [DETAIL] reasons about one refusal check only (Q5). | Q5 |
| H-48 | Does the layer own the ADR-to-owning-change edge? | decision | — | It reads it; `adr_files` stays the declaration (Q7). | Q7 |
| H-49 | Should address-drift-warning stay a neighbour? | decision | — | Drop: all three seats judged it unrelated and the runner rejected it (Q10). | Q10 |
| H-50 | Should the suggested neighbours enter the spec header? | decision | — | Keep the six given or confirmed paths (Q10). | Q10 |
| H-51 | Does a `claims` relation replace `adr_files`, derive from it, or leave it? | decision | — | Derive from it; `adr_files` stays the record (Q7). | Q7 |
| H-52 | Does this change take over frontmatter-current's excluded shared schema and `allowed:` validator? | decision | — | No; those stay with the front-matter bead and the provenance owner (Q1). | Q1 |
| H-53 | Are the recorded Pydantic/Jinja2 refusals general or per problem? | decision | — | Per problem (Q5). | Q5 |
| H-54 | explore-provenance's producer contract against research.md's body. | decision | `coding-harness-uo6s` | The contract wins; the body is corrected (Q11). | Q11 |
| H-55 | Does a new gate need a decision PR and an `adoption.yaml` entry first? | settled | — | Yes by house rule 8 (both files human-decided); order is set in the plan. | Q12 |
| H-56 | Do the two recorded Pydantic/Jinja2 judgements bind this layer? | decision | — | As H-53 (Q5). | Q5 |
| H-57 | Does the spec supersede frontmatter-current's non-goal, and which of its criteria stay? | decision | — | No supersession; all its criteria stay because `updated:` keeps its one owner (Q1). | Q1 |
| H-58 | Do adr-owning-change's non-goals stay when `claims` is typed? | decision | — | They stay (Q7). | Q7 |
| H-59 | Which seat description of the research swarm is in force? | settled | — | The seat amendment (c53d40f5, 25531756) is on origin/main; AGENTS.md and WORKFLOW.md describe seats. | Q12 |
| H-60 | Is 40 minutes the governed finder limit, and where is it held? | settled | `coding-harness-n76m` (finder limit follows repository size) | Held in `research-swarm-limits.yaml` (`finders: 40`) by decision PR #414, open on 2026-11-19. | Q12 |
| H-61 | Should `RESEARCH_PROGRAMS` admit another harness name? | duplicate | `coding-harness-uo6s` | Leave it to that bead. | Q12 |
| H-62 | Which producer record is authoritative for this research artefact? | decision | `coding-harness-uo6s` | The swarm record for the swarm sections; the hand part waits for that bead (Q11). | Q11 |
| H-63 | stage2-session spec still names gpt-6.1-sol as the usable path. | duplicate | `coding-harness-oqv7` (stage2-session spec names gpt-6.1-sol) | Leave it to that bead. | Q12 |
| H-64 | Must the `Gate`/`Rule` declaration live in a human-decided file? | decision | — | Yes: the relation vocabulary goes in a human-decided file (Q7). | Q7 |
| H-65 | How do volatile facts in the models stay current? | decision | — | The models copy no values; they read the YAML at every run (Q1). | Q1 |
| H-66 | Does the single renderer/validator satisfy the sharpened house rule 9? | decision | — | Only with one writer function that every site calls (Q6). | Q6 |
| H-67 | Should hand-accepted failed swarm runs count for the handoff gate? | duplicate | `coding-harness-glqo` (a timed-out seat voids the run) | ADR 0020 stands; the root fix is replacing a timed-out seat. | Q12 |
| H-68 | A new gate: seeded red test or mutation exemption entry? | settled | — | Seeded test: `tests/test_ci.py:3845` says a new gate needs one, not an entry. | Q12 |
| H-69 | Own gate id, or folded into an existing gate? | decision | `coding-harness-kpo7.3` | Own id (Q4). | Q4 |
| H-70 | Does Jinja2 render artefacts or only validate; do templates gain markers? | decision | `coding-harness-kpo7.2` | Neither in this change; templates keep `frontmatter: none` (Q6). | Q6 |
| H-71 | Rule-to-gate edge in `gates.yaml` or in the rulebook's enforcer column? | decision | `coding-harness-73gi` | In the rule registry; no `gates.yaml` schema change (Q2). | Q2 |
| H-72 | Which checks are absorbed, and must their findings text stay exact? | decision | `coding-harness-kpo7.3` | None absorbed; texts stay byte for byte (Q4). | Q4 |
| H-73 | How does the "rule loses its last gate" acceptance relate to the rule registry? | decision | `coding-harness-73gi` | The check reads the registry's rule list (Q2). | Q2 |
| H-74 | After an incomplete swarm run: rerun, resume or proceed? | settled | — | A complete run exists (bb903f11). | Q12 |
| H-75 | Should the one-writer tracker rule become a checked gate here? | duplicate | `coding-harness-36z` (D-60 write guard) | Leave it to that bead. | Q12 |
| H-76 | Which required-field list wins: `REQUIRED`, `_known_field_values` or `check_docs.PFlicht`? | decision | `coding-harness-rg8i`, `coding-harness-vkd0` (header contracts per file type) | `REQUIRED` for plan artefacts; folding the other two belongs to the front-matter bead (Q1). | Q1 |
| H-77 | Header tolerance (same as H-21). | duplicate | `coding-harness-rg8i` | That bead settles it. | Q3 |
| H-78 | Duplicate keys in one header: error or last wins? | duplicate | `coding-harness-rg8i` (notes of 2026-11-19) | That bead settles it. | Q3 |
| H-79 | `Gate` model and validator; does a relation field bump `schema_version`? | decision | `coding-harness-kpo7.1` | No new field in `gates.yaml` (Q2, Q1). | Q1 |
| H-80 | When the new gate cannot measure, exit 3 and stop the local run? | decision | `coding-harness-kpo7.3` | Yes, like the four existing checks; CI still runs every gate (Q4). | Q4 |
| H-81 | May spec.md be written while only incomplete runs exist? | settled | — | A complete run exists (bb903f11). | Q12 |
| H-82 | Must the leak check's stated scope gaps close first? | settled | `coding-harness-juu`, `coding-harness-159n` (leak check) | No: the limits and the 2026-10-07 decision stand in docs/WORKFLOW.md (lines 1294-1303). | Q12 |
| H-83 | Do absorbed checks keep their distinct exit-3 meaning? | decision | `coding-harness-kpo7.3` | Nothing is absorbed, so yes (Q4). | Q4 |
| H-84 | `parse_frontmatter` returns None for both "no header" and "malformed". | duplicate | `coding-harness-rg8i` (notes of 2026-11-19) | That bead settles it. | Q3 |
| H-85 | Is `RESEARCH_PROGRAMS` a deliberate closed boundary or an oversight? | duplicate | `coding-harness-uo6s`, `coding-harness-dwsk` | Leave it to those beads. | Q12 |
| H-86 | Is the shared model mandatory for every gate, or opt-in? | decision | `coding-harness-kpo7.3` | Opt-in: only the new gate uses it now (Q4). | Q4 |
| H-87 | Is the ripple cost of one shared model acceptable against parser drift? | decision | — | Yes at this size, because only one gate depends on it at first (Q4). | Q4 |
| H-88 | What happens when the shared model is stale? | settled | — | Cannot happen by design: rebuilt in memory on every run (research.md, architecture point 3). | Q4 |
| H-89 | Which information must the shared model carry, and which stays parser-specific? | decision | — | Only the relations of the closed vocabulary (Q7). | Q7 |
| H-90 | Must every gate consume the shared model? | decision | `coding-harness-kpo7.3` | No (Q4). | Q4 |
| H-91 | Code-as-data query model (CodeQL, Joern) or typed-document schema? | decision | — | Typed-document schema; the substrate is Markdown plus YAML (Q9). | Q9 |
| H-92 | The template header test covers 5 of 10 templates. | duplicate | `coding-harness-dd3v` (template header test covers 5 of 10) | Leave it to that bead. | Q12 |
| H-93 | Can a new gate still enter the mutation exemption list (cap 12, seven entries)? | bead proposal | new proposal B-5 | Accept: the cap should equal today's count, as its docstring promises. | Q12 |
| H-94 | Seats disagree whether OPA is a mature candidate. | decision | — | Moot: no external engine (Q9). | Q9 |
| H-95 | Seats disagree whether public failure records back the premise. | decision | — | They neither back nor refute it (Q9). | Q9 |
| H-96 | `provenance.yaml` names its readers wrongly ("two scripts", "nothing reads `allowed:`"). | bead proposal | new proposal B-1 (related `coding-harness-c20s`) | Accept: a bounded correction outside this change. | Q12 |
| H-97 | Is 0026 the next free ADR number? | decision | — | No, see H-29 (Q8). | Q8 |
| H-98 | Seats disagree how far Q-6 reaches. | decision | — | As H-7 (Q5). | Q5 |
| H-99 | Does any test assert a relation between artefacts? | settled | — | All seats agree the rule-to-gate edge is unchecked; that is the gap this change closes (Q2). | Q2 |
| H-100 | Seats disagree what the research header holds. | decision | `coding-harness-2i7x` (normalise research-file headers) | Read at 92f3b2fa: two `stage2-research-swarm` entries (2026-11-18, 2026-11-19); fix per Q11. | Q11 |
| H-101 | Is deleting a gate entry unguarded? | settled | — | All seats agree the rule-to-gate link is unchecked; the deletion itself needs a decision PR (Q2). | Q2 |
| H-102 | Seats disagree whether OPA treats input typing as optional. | decision | — | Moot: no external engine (Q9). | Q9 |
| H-103 | Neighbour decision-statement-skeleton contradicts the premise (its Pydantic/Jinja2 refusal). | decision | — | Keep it as a neighbour; the spec must answer it (Q10). | Q10 |
| H-104 | Neighbour verify-tmp-cleanup contradicts the premise (its Q-6). | decision | — | Keep it as a neighbour; the spec must answer it (Q10). | Q10 |

<!-- markdownlint-enable MD013 MD060 -->

## Questions for the maintainer

Twelve questions, the most important first. Each one closes the items it
names. A change of class `architectural` that claims its own ADR owes at least
five answered records (`scripts/check_interview_minimums.py`). Twelve meet that
floor, and the research-handoff gate needs all twelve.

### Q1 · Which is the declaration of record: the YAML files or the models?

Closes: H-4, H-5, H-9, H-19, H-20, H-42, H-52, H-57, H-65, H-76, H-79.

- **Topic:** where the one truth about gates, provenance classes and required
  header fields lives once typed models exist.
- **Intention:** every later choice (validators, rendering, kit) depends on
  it, and the swarm raised it eleven times.
- **Today:** `decisions/gates.yaml` (human-decided) and `provenance.yaml`
  declare the closed vocabularies. `plans_registry.REQUIRED`
  (`scripts/plans_registry.py:39`) declares the required plan-header fields.
  Two more field lists exist (`new_change._known_field_values`,
  `check_docs.PFlicht`). `ci_gates.validate_schema` checks the gate file with
  messages that tests pin. No Python model exists.
- **Repository change:** one new module of Pydantic models that read the two
  YAML files and `REQUIRED` at every run. Existing validators and their
  messages stay.
- **Architecture change:** a typed reading layer between the declaration files
  and the gates; no new declaration.

Options:

- **A — the YAML files and `REQUIRED` stay the record; the models read them at
  every run and copy no value.** Nothing regenerates and no pinned message
  moves. The two extra field lists are left to the front-matter bead
  (`coding-harness-rg8i`).
- **B — the models become the record; the YAML is generated from them.** The
  human-decided gate file becomes a rendering. The catalog, `ci.yml` and the
  drift tests regenerate, and the decision-PR route for gates needs a new
  object.
- **C — models beside the YAML, with their own copied values.** Two
  declarations of the same facts, which house rule 9 forbids.

Recommendation: **A**, because it adds types without moving the human-decided
record or any pinned message.

Which file is the declaration of record for these facts?

### Q2 · Who owns the `Rule`: this change or the rule registry?

Closes: H-3, H-37, H-38, H-46, H-71, H-73, H-99, H-101.

- **Topic:** the entity "rule" and the edge "a rule is protected by a gate".
- **Intention:** this change's main acceptance, "red when a rule loses its
  last gate", needs a list of rules. The rule registry epic
  (`coding-harness-73gi`) builds exactly that list.
- **Today:** `docs/governance/regelwerk.md` holds 33 rules (count from bead
  `coding-harness-73gi`, 2026-11-18), each with an enforcer that
  `tests/test_regelwerk.py` checks exists. The nine house rules and the
  operating rules of `docs/WORKFLOW.md` are outside it. All seats agree that no
  check reads a rule-to-gate edge from `decisions/gates.yaml`.
- **Repository change (A):** a typed `Rule` reading and a "last gate" check
  that reads the registry. `gates.yaml` gains no field.
- **Architecture change (A):** the registry becomes the source of the
  `protects` edge; the relation layer only reads it.

Options:

- **A — split.** The registry epic owns the rule list and its enforcement
  states (its YAML once built, until then the enforcer column of
  `regelwerk.md`). This change owns the typed reading and the check. No
  schema change to `gates.yaml`. The check covers the rulebook's rules now and
  the house rules once the registry lands.
- **B — this change owns list and model; the registry consumes them.** This
  change grows into the registry's scope (a third enforcement state, its ADR)
  and the two collide.
- **C — the registry owns everything; this change drops `Rule`.** The change
  loses its clearest measurable acceptance.

Recommendation: **A**, because each declaration keeps one owner and the check
still lands in this change.

Who owns the rule list and who owns the typed `Rule` reading?

### Q3 · Does this change wait for the one front-matter module?

Closes: H-6, H-8, H-21, H-77, H-78, H-84.

- **Topic:** reading YAML headers.
- **Intention:** a typed header model needs one reader. Bead
  `coding-harness-rg8i` (one front-matter module, and a gate that finds a
  script's own header parser) plans exactly that.
- **Today:** at least seven scripts read headers themselves (bead
  `coding-harness-rg8i`). They disagree on BOM and CRLF, on duplicate keys and
  on "no header" against "malformed header". That bead's notes of 2026-11-19
  already hold these four items (H-21, H-77, H-78, H-84).
- **Repository change (A):** none in this change; the front-matter bead ships
  first.
- **Architecture change:** none from this question; it sets the order of two
  changes.

Options:

- **A — the front-matter bead first; this change builds on its module.** The
  relation layer starts later but meets one reader.
- **B — this change absorbs the front-matter bead.** One much larger change
  that mixes two beads' scopes and their reviews.
- **C — the model gets its own reader now.** An eighth private parser, the
  opposite of the goal (house rule 9).

Recommendation: **A**, because it is the only order without a second reader.

Should the front-matter module be built before this change?

### Q4 · A new gate, or absorb the four existing checks?

Closes: H-14, H-25, H-43, H-69, H-72, H-80, H-83, H-86, H-87, H-88, H-90.

- **Topic:** where the one reasoner over typed edges sits among the gates.
- **Intention:** absorbing the four checks moves their findings texts, exit
  codes and callers. The swarm asked about it eleven times.
- **Today:** 24 gates in `decisions/gates.yaml` (research.md, `fd2b8701`,
  2026-11-18). The four checks (`check_dangling_bead_ids.py`,
  `check_decision_continuity.py`, `check_research_handoff.py`,
  `check_frontmatter_current.py`) each parse on their own and exit 3 when they
  cannot measure. Their callers: `gates.yaml`, the generated `ci.yml`,
  `verify_all.sh`, `stage2.py` and prompts.
- **Repository change (A):** one new gate id (a decision PR, house rule 8),
  its seeded red-run test, and the projection module. The four checks stay
  untouched.
- **Architecture change (A):** a new gate that reads an in-memory projection
  rebuilt on every run, so it cannot go stale.

Options:

- **A — one new gate with its own id; the four checks stay.** Each check may
  delegate later, in a change of its own. A disagreement between a parser and
  the model is exit 3 ("not measured"), never a pass or a rule finding. The
  smallest blast radius; two readers coexist until those follow-ups.
- **B — absorb the four now.** Findings texts, the tests that pin them, and
  every caller move in one change. The review gets much harder.
- **C — like A, but the new gate starts as `report` and blocks after a dated
  valve.** A softer start; a report gate needs a dated valve (bead
  `coding-harness-73gi.4`).

Recommendation: **A**, because house rule 9 folds an existing route in by its
own change, never in passing.

Should the reasoner be one new gate beside the four existing checks?

### Q5 · Is Pydantic the basis, and how far do earlier refusals reach?

Closes: H-2, H-7, H-41, H-47, H-53, H-56, H-98.

- **Topic:** the library behind the typed models.
- **Intention:** two archived changes declined Pydantic and Jinja2. The swarm
  asks whether those answers bind this change.
- **Today:** `pyproject.toml` pins pydantic 2.13.5 and Jinja2 3.1.6, and no
  script imports either (grep, 2026-11-18). verify-tmp-cleanup's record Q-6
  says "Pydantic or Jinja do not help: only pytest knows what it makes of its
  option sources". decision-statement-skeleton's `[DETAIL]` says "a second
  record representation is unnecessary for this refusal".
- **Repository change (A):** the first `import pydantic` under `scripts/`.
- **Architecture change (A):** none beyond Q1.

Options:

- **A — both refusals are per problem; Pydantic is the basis.** Both texts
  name their own problem, so neither binds a header and relation model.
- **B — a standing preference against the libraries: standard-library
  dataclasses and hand checks.** No new import and more hand code; the pinned
  pair stays unused and could be removed.
- **C — decide after a short spike** that builds one model both ways. Costs
  a delay of one spike.

Recommendation: **A**, because the recorded reasons are scoped to pytest
options and to one refusal check.

Is Pydantic the basis of the models?

### Q6 · Render headers with Jinja2, or validate and write through one function?

Closes: H-22, H-31, H-66, H-70.

- **Topic:** who writes artefact headers.
- **Intention:** bead `coding-harness-kpo7.2` (one Jinja2 template for every
  artefact header) proposes a renderer. House rule 9 asks for one writer per
  action.
- **Today:** `new_change._frontmatter_template()` (`scripts/new_change.py:80`)
  writes new headers as an f-string. `check_frontmatter_current.stamp`
  rewrites `updated:`, and `archive_closed_changes` rewrites four lifecycle
  fields. No file under `templates/` carries a Jinja2 marker, and
  `provenance.yaml` declares `frontmatter: none` for them.
- **Repository change (A):** one header writer function (in the front-matter
  module) that every writer site calls; every header validated against the
  model.
- **Architecture change (A):** none beyond Q1 and Q3.

Options:

- **A — validate every header against the model; every header write goes
  through one writer function; no Jinja2 in this change.** One writer per
  action. A YAML header is data, so it is serialised from the model, not
  templated as text. Bead `coding-harness-kpo7.2` is re-scoped or closed.
- **B — one Jinja2 template renders new headers (the bead as written).** Jinja2
  gets a use, but stamping and archiving stay separate writers, so three
  remain.
- **C — render every artefact, kit templates included, as `.md.j2`.**
  `provenance.yaml`'s `frontmatter: none` for `templates/` changes (a file the
  runner holds) and the template tests grow. The largest change.

Recommendation: **A**, because it removes writers instead of adding a fourth
representation of the header.

How should headers be written?

### Q7 · Which relations enter the closed vocabulary, and where is it declared?

Closes: H-48, H-51, H-58, H-64, H-89.

- **Topic:** the list of named relations the layer knows.
- **Intention:** a vocabulary that grows on demand is not a vocabulary
  (research.md, "What is unclear").
- **Today:** research.md proposes eight: `protects`, `answers`, `claims`,
  `derives-from`, `supersedes`, `belongs-to`, `blocks`, `cites`. The archived
  change adr-owning-change already enforces `adr_files` as the claim of ADR
  files. It left two points open by decision: no check that a claimed file
  exists, and archived changes claim nothing.
- **Repository change (A):** three relations in a human-decided file; the
  models read them.
- **Architecture change (A):** a closed list that only a decision PR extends.

Options:

- **A — start with three relations that have a record or a measured gap:**
  `protects` (rule to gate), `claims` (derived from `adr_files` and a plan's
  `bead:`) and `answers` (interview record to question). Declared in a
  human-decided file; more only by decision. adr-owning-change's open points
  stay open.
- **B — all eight now.** Some relations would have no check yet; the
  vocabulary is larger than any gate needs.
- **C — leave the set to the spec as a detail.** The spec's author would
  decide a vocabulary that is meant to be human-decided.

Recommendation: **A**, because each relation then has a gate that reads it.

Which relations enter the first closed vocabulary?

### Q8 · Class, ADR and kit

Closes: H-26, H-27, H-29, H-30, H-33, H-39, H-40, H-44, H-97.

- **Topic:** the change's class, the ADR it owes, and what the kit carries.
- **Intention:** the class sets the phases and the interview minimum; the ADR
  number is contested.
- **Today:** the class is declared `architectural`. `docs/WORKFLOW.md` says an
  architectural change "carries its ADR already" (line 433) and asks for "an
  ADR draft" in `design.md` (phase 2b, line 86). ADR 0009 keeps "an
  Architectural change requires an ADR in the same pull request". Its bullet
  "No model as code in the kit now" names LikeC4, a `model/` scaffold, the
  `likec4` gates and Node.js. `origin/main` `f31d216e` ends at ADR 0025.
  Numbers 0026 and 0027 are drafted on the branches `feat/central-config` and
  `feat/review-fewer-rounds` (no pull request found, 2026-11-19).
- **Repository change (A):** one ADR file, claimed under `adr_files` in the
  spec header.
- **Architecture change (A):** recorded in that ADR. The kit carries the
  module as mechanism, and each instance declares its own vocabularies.

Options:

- **A — keep `architectural`; one new ADR, drafted in phase 2b, its number set
  at merge (0028 is the next unused on 2026-11-19).** The ADR states that ADR
  0009 governs architecture models, not a typed schema over repository files.
  The kit ships the module, and each instance declares its own lists.
- **B — reclassify as `feature`; no ADR.** A new layer behind the gates
  without an ADR; phase 2b becomes optional.
- **C — `architectural`, but amend ADR 0009 instead of a new ADR.** This mixes
  a decision about architecture pictures with one about a gate layer.

Recommendation: **A**, because the change adds a subsystem that every later
gate may read.

Is the class `architectural`, with one new ADR of its own?

### Q9 · External standards and online evidence

Closes: H-10, H-11, H-12, H-13, H-16, H-17, H-18, H-91, H-94, H-95, H-102.

- **Topic:** whether an outside format or engine should carry the model, and
  what the online topics prove.
- **Intention:** eleven items from the online topics 9–11 ask for a
  reference tool or an evidence standard.
- **Today:** the reconciliation finds no retrieved tool shown to be a typed
  relation layer shared by repository gates. dependency-cruiser is adjacent.
  The failure records show parser divergence, but none of them in gate
  checkers. Several excerpts held only titles and boilerplate. research.md
  rules out RDF, OWL and YAML-LD, and requires that a gate run with `pip` only.
- **Repository change (A):** none.
- **Architecture change (A):** none.

Options:

- **A — an internal vocabulary (YAML plus Pydantic); outside tools are
  background only.** The case rests on internal measurements: the unchecked
  rule-to-gate edge and the private parsers.
- **B — like A, plus a published JSON Schema export** so that third-party tools
  can read the model. A second artefact to keep in step, with no consumer
  named.
- **C — first evaluate a policy engine (OPA, CUE or CEL) through a
  research-swarm spike.** A delay, and possibly a runtime that `pip` alone
  does not provide (not checked here).

Recommendation: **A**, because nothing retrieved shows an outside tool doing
this job for repository gates.

Should the model stay an internal vocabulary, with outside tools as background?

### Q10 · Which neighbours enter the spec header?

Closes: H-49, H-50, H-103, H-104.

- **Topic:** the `neighbours:` list of the future `spec.md`.
- **Intention:** the research-handoff gate holds the spec header to the run's
  neighbour records. A contradicting neighbour needs a `keep` or `drop` from
  the maintainer.
- **Today:** run bb903f11 lists two given paths (frontmatter-current,
  provenance-location) and four confirmed ones (adr-owning-change,
  decision-statement-skeleton, explore-provenance, verify-tmp-cleanup). It
  rejected address-drift-warning, because all three seats judged it unrelated.
  Two confirmed neighbours contradict the premise: their Pydantic and Jinja2
  refusals (see Q5).
- **Repository change (A):** six paths in the spec header.
- **Architecture change:** none.

Options:

- **A — keep all six, drop address-drift-warning.** The two contradicting
  neighbours stay, so the spec has to answer them.
- **B — keep the four related ones, drop the two that contradict.** A shorter
  header, but the spec could ignore the recorded counter-positions.

Recommendation: **A**. The record would carry
`research_neighbours: {keep: [the six paths], drop:
[plans/changes/archive/2026-11-16-address-drift-warning/spec.md], add: []}`.

Should the spec header list all six neighbours?

### Q11 · Who wrote research.md, and what does its header say?

Closes: H-28, H-45, H-54, H-62, H-100.

- **Topic:** the provenance of this change's own research artefact.
- **Intention:** review finding R-3 on PR #411 (noted on the epic
  `coding-harness-kpo7`) found header and body contradicting each other. The
  swarm found it again.
- **Today (read at `92f3b2fa`):** the header carries two `produced_by` entries
  `stage2-research-swarm` (versions 2026-11-18 and 2026-11-19). The body
  (lines 83–88) still says `produced_by` "is deliberately absent". The
  hand-written part came from an OpenCode session that `RESEARCH_PROGRAMS`
  cannot name (bead `coding-harness-uo6s`). `ai-drafted-reviewed` with
  `review.status: pending` is the usual pairing in change artefacts (for
  example, verify-tmp-cleanup's `decisions.md`).
- **Repository change (A):** one corrected paragraph in research.md.
- **Architecture change:** none.

Options:

- **A — correct the stale body paragraph now; leave the header as the runner
  wrote it.** The hand-written part gets its producer once bead
  `coding-harness-uo6s` gives OpenCode a name.
- **B — also remove the 2026-11-18 swarm entry by hand.** Hand-editing a field
  the runner wrote is a side route (house rule 9).
- **C — change nothing until bead `coding-harness-uo6s` lands.** The
  contradiction stays visible for every reviewer until then.

Recommendation: **A**, because it fixes the false sentence without hand-editing
runner output.

Should the stale provenance paragraph in research.md be corrected now?

### Q12 · Accept the sort of the remaining 23 items, and which beads to create

Closes: H-1, H-15, H-23, H-24, H-32, H-34, H-35, H-36, H-55, H-59, H-60, H-61,
H-63, H-67, H-68, H-74, H-75, H-81, H-82, H-85, H-92, H-93, H-96.

- **Topic:** items that are not decisions for this change.
- **Intention:** close them in one answer, and create only the beads you
  accept. Today's gate needs an answered record even for a duplicate (see
  "One limit of today's gate").
- **Today:** this question holds 9 duplicates, 11 settled items and 3 bead
  proposals. The other four duplicates (H-21, H-77, H-78, H-84) sit in Q3, and
  the other four settled items in Q2 (H-99, H-101), Q4 (H-88) and Q11 (H-28).
  The lists follow.
- **Repository change:** none in this change. Accepted beads are created by
  the session that writes the tracker, as `discovered-from` the epic
  (`coding-harness-kpo7`).
- **Architecture change:** none.

**Duplicates (closed by pointing at the open bead):**

- H-1, H-85 — `coding-harness-dwsk` (one declaration for the research program
  vocabulary); H-85 also `coding-harness-uo6s`.
- H-61 — `coding-harness-uo6s` (no honest producer name for an OpenCode
  session).
- H-24 — `coding-harness-c20s` (gate-catalog.md calls `ci_gates.py` the one
  reader).
- H-34 — `coding-harness-hg6w` (AGENTS.md 1a table names no `architectural`
  minimum).
- H-63 — `coding-harness-oqv7` (stage2-session spec still names gpt-6.1-sol).
- H-67 — `coding-harness-glqo` (a timed-out seat voids the run); ADR 0020's
  rule that only a complete run counts stands.
- H-75 — `coding-harness-36z` (D-60 write guard: one tracker writer per
  repository).
- H-92 — `coding-harness-dd3v` (template header test covers 5 of 10
  templates).

**Settled (source named):**

- H-23, H-36, H-55 — a new gate is a decision PR (house rule 8):
  `provenance.yaml` maps `decisions/gates.yaml` and `decisions/adoption.yaml`
  to human-decided (since `9446abe5`, 2026-10-21, for the gate file).
- H-32 — this page sorts research.md's open items; Q1–Q11 are the decisions.
- H-35, H-74, H-81 — run bb903f11 is complete, so the swarm's handoff can
  start.
- H-59 — the seat amendment of ADR 0020 (`c53d40f5`, `25531756`) is on
  `origin/main`.
- H-60 — the finder limit of 40 minutes is held in
  `research-swarm-limits.yaml` by decision PR #414 (open on 2026-11-19;
  `origin/main` still says 20). Related: `coding-harness-n76m` (finder limit
  follows repository size).
- H-68 — a new gate needs a seeded control test: `tests/test_ci.py:3845`
  says so in its failure message.
- H-82 — the leak check's limits and the accepted consequence (maintainer,
  2026-10-07) stand in `docs/WORKFLOW.md` (lines 1294–1303). Related:
  `coding-harness-juu`, `coding-harness-159n`.

**Bead proposals (none exists yet; each checked on 2026-11-19):**

- **B-1 (bounded) — `provenance.yaml`'s reader note is wrong.** It names
  `scripts/validate_provenance.py` (the file does not exist), says "two
  scripts" while listing three, and says nothing reads `allowed:`, but
  `scripts/pr_sync.py:242` and `scripts/stage2.py:7412` do. From H-96.
  Related: `coding-harness-c20s`.
- **B-2 (bounded) — a stale comment above `stage2.RUNNER_HELD`.** It says
  `decisions/gates.yaml` "has no provenance class of its own", but
  `provenance.yaml` has mapped it to human-decided since `9446abe5`
  (2026-10-21). Found while checking H-23.
- **B-3 (note for an existing bead) — `docs/WORKFLOW.md` says when an
  architectural change writes its ADR in two ways** (line 433 "carries its ADR
  already", line 86 "an ADR draft" in `design.md`). Recommended as a note on
  `coding-harness-hg6w`, not a new bead. From H-27.
- **B-4 (bounded) — online failure-record topics should cite dated primary
  records (such as CVE JSON).** From H-15. Recommended: **decline**, because no
  gate of this change rests on online incidents.
- **B-5 (bounded) — the mutation-exemption ratchet does not ratchet.**
  `tests/test_ci.py:3845` asserts at most 12 entries while the list holds
  seven and its docstring says "the number may fall and never rise". The cap
  should equal the current count. From H-93.

Options:

- **A — accept the sort; create B-1, B-2 and B-5; add B-3 as a note to
  `coding-harness-hg6w`; decline B-4.**
- **B — accept the sort; create no bead.** The facts stay recorded here only.
- **C — accept the sort; choose the proposals one by one** (multiple choice
  over B-1 to B-5).

Recommendation: **A**, because B-1, B-2 and B-5 are checked defects with a
clear acceptance, and B-4 has no user.

Do you accept the sort and the bead proposals as recommended?
