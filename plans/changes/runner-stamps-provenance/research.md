---
title: "Research — runner-stamps-provenance"
status: draft
implementation_status: none
date: 2026-11-16
last_reviewed: 2026-11-16
updated: 2026-11-16
supersedes: null
superseded_by: null
bead: coding-harness-f9sv
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-16", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# runner stamps provenance — Research

Stage-2 call, 2026-11-16: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1100 files, 4456 commits, 12 rules.

## Runner exploration — 2026-11-16

Research complete. Here is the report, ready to append to `plans/changes/runner-stamps-provenance/research.md`.

---

## What exists today

**The provenance map and its classes.** `provenance.yaml` is the single map from path to provenance class. It declares a closed enum of five classes (`human-decided`, `human-written`, `ai-drafted-reviewed`, `ai-generated`, `machine-rendered`; `classes:` block, each with `bedeutung` and `review_required`, `machine-rendered` additionally `generator_required`), roles with handles and git identities (`roles:`, `data-architect`/`framework-architect` share handle `@MPAdesso`; `data-product-owner` and `operations-owner` are vacant), and `paths:` entries with `allowed:` classes and a `frontmatter:` value `required`/`optional`/`none`. The file states itself that `allowed:` is declared but not enforced — "nothing here reads it" (`provenance.yaml`, comment before `schema_version`, and the `excluded:` block ends the file with only `docs/archive/`).

**The stamping contract for a model publication.** The archived change `plans/changes/archive/2026-11-16-explore-provenance/spec.md` (bead coding-harness-g19n, `implementation_status: done`) defines the "Metadata contract": exactly one top-level `provenance` (`ai-drafted-reviewed`), `produced_by` (records with `kind: llm-session`, a program `name`, an ISO date in `version`, optional `model`; a list for several producers), `review` pending with null approver and approval date, `date <= last_reviewed <= updated`, producer dates inside `date..updated`. The machine form of this contract is `metadata_problems()` in `scripts/research_census.py` (checks `provenance`, `produced_by`, `review`, `date`, `last_reviewed`, `updated` — exactly one each, pending review, known programs in `PROGRAMS`).

**The runner already stamps provenance in these places.**

- Explore, Flash route: `explore()` in `scripts/stage2.py` (around `prepared = research_publication(...)`) calls `research_publication()` (`scripts/stage2.py`, symbol `research_publication`), which corrects `provenance`, `produced_by`, `review` and `updated` in place, removes duplicate fields, inserts missing fields before `tags:`, refuses YAML anchors/aliases in the header, and strips the generated skeleton opening paragraph and blockquote (`_without_skeleton_opening`). `publish_research()` then appends the runner's record and replaces the file atomically (`write_atomic`), stamping `updated:` through `check_frontmatter_current.stamped`. The producer program name comes from `producer_for()` (`scripts/stage2.py`): `openai-codex` → `codex`, `claude-code-plan` and `glm-coding-plan` → `claude-code`, anything else → `pi`.
- Explore, swarm route: `publish()` in `scripts/stage2_research_run.py` prepares the same publication bytes ("truthful provenance, no skeleton notices") before the atomic replacement; the resume binding freezes the prepared publication bytes and day so a resume never recomputes the header (`scripts/stage2_research_snapshot.py`, record docstring at `publication`).
- `findings.md`: `findings_header()` in `scripts/stage2.py` writes a complete header with `provenance: ai-drafted-reviewed`, an inline `produced_by: {kind: llm-session, name: <producer>, version: "<day>"}` and pending `review` when the runner creates the file (called at four sites: two in `begin_work_call`/findings setup, two in the swarm loops around lines 10945 and 11218). Later runner writes to findings call `stamp_updated()` only, which edits only the `updated:` line (`stamp_updated` docstring; `check_frontmatter_current.stamp`).
- The audit line the runner appends before its answer lands ("Stage-2 call, … leak check clean over N files…") is written by `begin_work_call()` in `scripts/stage2.py` — this is the line already standing in this change's own `research.md`.

**The runner does not stamp provenance in these places.**

- `spec.md`, `design.md`, `plan.md` from the `draft` verb are written by the drafting model session itself, not by runner code: the runner only decides which changed paths to keep (`draft_keep()` in `scripts/stage2.py` — every changed path under the change folder except `decisions.md`, plus new ADR files). The header form those artifacts carry comes from `templates/spec.md` (its yaml block shows `provenance: ai-drafted-reviewed`, `produced_by: {kind: llm-session, name: <agent>, …}`, `review: {status: pending, …}`) and from `prompts/02-spec.md` (frontmatter paragraph listing `status`, `implementation_status`, `date`, `last_reviewed`, `bead`, `class:`, `adr_question`, `adr_files` — the prompt names no provenance field; `templates/spec.md` supplies it).
- Plan time entries and other runner appends stamp only `updated:` (`stamp_updated` call sites at `scripts/stage2.py` — findings, plan time entries, route evidence blocks).
- `decisions.md` is the maintainer's answers file; `draft_keep()` explicitly excludes it from keeps, and no runner code writes or stamps it was found.
- The loop record lives outside the worktree and the git directory (`record_dir()` returning `record_base() / record_key(...)`, `scripts/stage2.py`) and has no frontmatter at all — `stamp_updated`'s docstring states "A file without a header, like the loop record, is left as it is."
- No code path sets `review:` to approved: the only occurrences of `approved_by` in `scripts/` are the two pending-write sites (`research_publication`, `findings_header`). Approval happens as a human edit.

**The deterministic new-change skeleton stays `human-written` on purpose.** `scripts/new_change.py` writes `provenance: human-written` and no `produced_by` (`_frontmatter_template`, whose docstring explains the deliberate choice and its history), and its `BODY_TEMPLATE` carries the blockquote instructing whoever fills the file with a language model to set `ai-drafted-reviewed`, `produced_by:` and `review:`. The explore-provenance spec lists as a non-goal: "No alteration of the deterministic new-change skeleton: an untouched, unpublished human-issued skeleton may remain `human-written`."

**What holds this today (checks and gates).**

- `scripts/research_census.py` — a read-only library over active research (`plans/changes/<name>/research.md`, `archive/` excluded). It reports metadata-contract violations and retained skeleton notices for model-written research, with the stock exemption decided by git history against the adoption day recorded in `decisions/adoption.yaml` (spec criterion 9). Held by `tests/test_explore_provenance.py` (twenty-plus tests over the contract, exemptions, line endings, quoted fences).
- `scripts/check_frontmatter_current.py` — the `frontmatter-current` gate: under prefixes declared `frontmatter: required` in `provenance.yaml`, a Markdown file must carry a header with a current `updated:`; `stamp()`/`stamped()` edit only that one line.
- `scripts/check_docs.py` — under `docs/` only: when frontmatter exists, the keys `provenance`, `produced_by`, `review` (among `PFlicht`) must be *present*; truthfulness is not measured, and `plans/` is not in its default scope.
- `scripts/plans_registry.py` — `REQUIRED = ("status", "implementation_status", "date", "last_reviewed", "bead")`; no provenance field is mandatory for `plans/` artifacts (`plans/_README.md` documents the same list).
- `scripts/handover_schema.py` — handover required fields include `provenance` and `produced_by` (nested blocks read with their prefix).

**Held paths.** A stage-2 attempt never writes `provenance.yaml` and the other runner-held paths (the `RUNNER_HELD` set near `scripts/stage2.py` line 7376; `prompts/03-plan.md`, "Held paths go to the orchestrator"), and the classes a route may touch come from the *committed* `provenance.yaml`, never from the tree the attempt wrote (`scripts/stage2.py`, `_held_classes` area reading `git show HEAD:provenance.yaml`).

## Where it lives

- Map: `provenance.yaml` (`classes:`, `roles:`, `paths:`, `excluded:`).
- Stamp, research publication: `scripts/stage2.py` — `research_publication`, `publish_research`, `research_header_producers`, `research_producer_field`, `producer_for`, `_without_skeleton_opening`, `_header_field_spans`; `scripts/stage2_research_run.py` — `publish` (buffered record); `scripts/stage2_research_snapshot.py` — resume binding of prepared publication bytes.
- Stamp, findings: `scripts/stage2.py` — `findings_header`.
- Stamp, `updated:` only: `scripts/check_frontmatter_current.py` — `stamped`, `stamp`; call sites `scripts/stage2.py` — `stamp_updated`.
- Skeleton: `scripts/new_change.py` — `_frontmatter_template`, `BODY_TEMPLATE`.
- Contract check: `scripts/research_census.py` — `metadata_problems`, `publication_evidence`, `research_opening_notices`; test `tests/test_explore_provenance.py`.
- Presence checks: `scripts/check_docs.py` — `PFlicht`; `scripts/plans_registry.py` — `REQUIRED`; `scripts/handover_schema.py` — required-field set.
- Header forms the drafting model copies: `templates/spec.md` (yaml block), `templates/design.md`, `templates/findings.md` (same directory); instructions `prompts/02-spec.md`.
- Predecessor spec: `plans/changes/archive/2026-11-16-explore-provenance/spec.md` (metadata contract, stock exemption, non-goals, Q-1 through Q-8 in its `decisions.md`).

## What is unclear

- The bead `coding-harness-f9sv`'s own title and description could not be read: the tracker is an embedded Dolt database (`.beads/metadata.json`: `"backend": "dolt"`, `"dolt_mode": "embedded"`), and this phase runs without a shell, so `scripts/bead_render.py` cannot be invoked. What stands in the tree is the registration in `plans/INDEX.md` (row for `changes/runner-stamps-provenance/research.md`, bead `coding-harness-f9sv`) and the change name itself. Which artifacts the change means beyond research — and which verb's behaviour it concerns — is an open question for the interview, not derivable from the tree. *Not read*, not *absent*.
- `provenance.yaml`'s header comment says the map "wird von `scripts/validate_provenance.py` gelesen und von `tests/test_provenance.py` geprueft". No `scripts/validate_provenance.py` exists in this tree (glob over `scripts/validate_provenance.py`: no files found), and the `tests/test_provenance.py` that exists here checks journal date citations (its docstring: RB-P5, `journal-date-citation`), not provenance classes. Unclear whether the comment describes the origin repository `portfolio-agentic-engineering` or is stale drift here. Two statements: the named validator script is *not there*; a differently-scoped test file holds the name.
- The class declaration of this change (`spike`/`bounded`/`feature`/`architectural`) is not yet written anywhere in the tree: the change folder holds only the skeleton `research.md`, whose generated frontmatter (`scripts/new_change.py`, `_frontmatter_template`) carries no `class:` field, and no `spec.md` exists yet. The runner reads the class from `--class` and the two headers wherever stated (AGENTS.md, ADR 0020 section).
- `allowed:` classes in `provenance.yaml` are declared but unread by any script — stated by the file itself; whether this change should touch that was a declared non-goal of the predecessor (`explore-provenance/spec.md`, non-goals: "No new provenance class, general provenance validator or enforcement of `allowed:`").
- The living spec `plans/specs/implementation-verification/spec.md` carries `provenance: ai-generated` with `review` pending — a class whose own `bedeutung` in `provenance.yaml` says it "wird nie zitiert, nur datiert gelesen". Whether that header is deliberate (spec of the predecessor era) or a census-eligible defect was not investigated; the census covers active research only, not `plans/specs/`.

## Which files a change would have to touch

Facts about the surfaces a runner-stamping change lands on, each already named above:

- Stamp sites in the runner: `scripts/stage2.py` (`research_publication`, `publish_research`, `findings_header`, `stamp_updated`, `producer_for`, `begin_work_call`), `scripts/stage2_research_run.py` (`publish`), `scripts/stage2_research_snapshot.py` (publication bytes in the resume binding).
- The contract check and its test: `scripts/research_census.py`, `tests/test_explore_provenance.py`.
- The `updated:` stamp and its gate: `scripts/check_frontmatter_current.py`, `tests/test_frontmatter_current.py`.
- The header sources a drafting model copies: `templates/spec.md` (and sibling templates), `prompts/02-spec.md`; the deterministic skeleton: `scripts/new_change.py` — noting the predecessor spec's non-goal that protects the untouched skeleton.
- Presence-only checks that would need widening if their scope moved: `scripts/check_docs.py`, `scripts/plans_registry.py`.
- Held/protected, touched only by the orchestrator at a human decision: `provenance.yaml` (runner-held, `RUNNER_HELD`; classes for `plans/` are `[human-written, ai-drafted-reviewed]`, `frontmatter: required`), `decisions/gates.yaml`, `prompts/`, `templates/`, `AGENTS.md`.

## Neighbours

- `plans/changes/archive/2026-11-16-explore-provenance/` (spec accepted, done; bead coding-harness-g19n) — the direct predecessor: metadata contract, publication, census, stock exemption, and the Q-1..Q-8 maintainer answers in its `decisions.md`.
- `plans/specs/implementation-verification/spec.md` (living spec, bead coding-harness-mfv, `class: bounded`) — the runner's derived-file preparation contract, carried `provenance: ai-generated` in its own header.
- The deferred history-based correction of existing research (named as bead coding-harness-2i7x inside the explore-provenance spec's Terms and Non-goals) — no active change folder of its own exists under `plans/changes/` (a grep for `2i7x` over `plans/` matches only the three archived explore-provenance files).
- `provenance.yaml` itself and `docs/WORKFLOW.md` (workflow doctrine; not opened this run — *not read*, not judged).

## Open questions for the interview

- What exactly does bead `coding-harness-f9sv` scope — which runner verb and which artifacts? (Not readable from this tree; the tracker must be rendered.)
- Does the change extend runner stamping to artifacts a model session writes directly (`spec.md`/`design.md`/`plan.md` after `draft`), keep the deterministic skeleton `human-written` as the predecessor decided, or concern the approval side of `review:` that today only a human edit can set?
- Is the stale `scripts/validate_provenance.py` / `tests/test_provenance.py` reference in `provenance.yaml`'s header comment in scope, or separate drift housekeeping?
