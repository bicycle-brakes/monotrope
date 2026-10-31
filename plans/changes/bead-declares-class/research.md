---
title: "Research — bead-declares-class"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-680l
owner: Data Architect
provenance: human-written
tags: [research]
---

# bead declares class — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 788 files, 2835 commits, 12 rules.

## Runner exploration — 2026-10-31

Research complete. Here is the report, ready to append to `plans/changes/bead-declares-class/research.md`.

---

## Runner exploration — 2026-10-31

### What exists today

**The rule this change is about is prose, not code.** `AGENTS.md` states it at "A bead for a change names its class (`spike` … `architectural`) in its description (2026-10-22)" (`AGENTS.md`, section "Communication and session continuity", last bullet). The handover of that day records its origin: "New standing rule: a change bead names its class in its description (maintainer, 2026-10-22); proposed in AGENTS.md through PR #220; added as comments to nine beads of today" (`docs/journal/handover/2026-10-22-joint-window.md`, closing list). `README.md` restates it and names the gap: "Every change names its class in the bead description and in the head of its spec" — followed by "Nothing yet checks that the class itself is right: a `feature` declared as a `spike` would skip the other-vendor reviews, and only the review before the merge catches it" (`README.md`, section "Not every change is the same size"). `docs/WORKFLOW.md` §4 carries the same admission: "Nothing checks a change's class beyond explore" (§4, after the routing paragraph).

**The machine-readable class statements today are exactly two, reconciled by one function.** `declared_class(root, change, klass)` in `scripts/stage2.py` (symbol `declared_class`) reads (1) the explore-only `--class` argument — argparse `dest="klass"`, `choices=CLASSES`, refused for every verb except `explore` and `prepare-explore` (`_run` verb check) — and (2) the YAML front-matter key `class:` of `plans/changes/<change>/research.md` and `spec.md`. Its docstring states the contract: "Every statement that is present must name a class and agree with the others … none present refuses, because a silently assumed small change would keep a large change off the swarm (spec, criteria 3 and 4)". The vocabulary is `CLASSES = ("spike", "bounded", "feature", "architectural")` and `SWARM_CLASSES = ("feature", "architectural")` (module constants in `scripts/stage2.py`). Duplicate `class:` keys, an unparseable header, an unreadable file, a value outside `CLASSES`, a disagreement between files, and a contradiction with `--class` each raise `Refused` (exit 2) before any model call; an explicit argument does not cure a stated one.

**Call sites of that contract.** `explore()` calls it first when Stage 2 is on, then routes: swarm classes through `consume_research` (the receipt) plus `stage2_swarm.run`, bounded/spike to GLM Flash; with `--stage2-off` the class derivation and all class/neighbour header checks are skipped entirely and Haiku explores (`scripts/stage2.py`, function `explore`; the `--stage2-off` branch's comment cites "spec, criterion 20"). `prepare_explore()` delegates to `prepare_research` in `scripts/stage2_availability.py`, which calls `runner.declared_class` and refuses non-swarm classes ("prepare-explore belongs to feature or architectural changes"); the selection receipt is "bound to worktree, change, configuration, class and neighbours" (ADR 0020 point 11, `docs/adr/0020-phase-1-research-swarm.md`). The acceptance basis is the research-swarm spec: criterion 3 ("the research header or explore-only `--class` argument supplies the class without requiring a spec or plan") and criterion 4 (invalid declarations refuse before a model call with exit 2 and a header-repair message) (`plans/changes/research-swarm/spec.md`, criteria 3 and 4).

**Three more consumers read the class independently, each with its own copy of the vocabulary.** `scripts/check_interview_minimums.py` keeps its own `CLASSES` tuple and parses `class:` from the spec header with a line regex (`_CLASS_LINE`, `_spec_class_and_date`), not the YAML loader; a folder whose class is absent or not in `CLASSES` is silently skipped from the minimums measurement. `scripts/check_adr_answers.py` defines the same four-tuple constant of its own. The research-handoff side records the class in the v2 run manifest (`"class": self.klass` in `scripts/stage2_research_run.py`), re-derives the inventory from it (`check_research_handoff.py`, `declared_class=parsed.manifest["class"]`), and derives an obligation item when topic 3's `class_assessment` differs from the declared class (`scripts/research_handoff.py`, function `derive_inventory`, reason `"class"`); ADR 0020 point 7 makes class mismatches human decisions. `docs/WORKFLOW.md` §2 documents the `class:` header itself ("Every change says in its spec header what kind of change it is"), and `prompts/02-spec.md` instructs the drafter to write it.

**The bead side has no machine reader at all.** A search across `scripts/` for `description` finds only argparse keyword arguments — no script reads a bead's description field. The two existing readers of the tracker render consume exactly two fields: `plans_registry._bead_statuses` builds `id -> status` from the JSON Lines export, and `check_bead_export.run` requires each line to be an object with non-empty string `id` and `status` — nothing else is contract-checked. Tracker access is centralised: `scripts/bead_render.py` is "the ONE access point for the tracker render (bead 1jg.3)" — `BEAD_RENDER` preset in CI, otherwise a fresh render through the one-writer `scripts/render_beads_export.py` via the pinned `tools/bd export` (exit 127 = no binary; `RendererNichtMöglich` = nothing measurable); the fresh render is written to a temporary directory outside the repository. Existing reader precedents differ in severity: `plans_registry` reports a missing render as its own BLOCK ("the artefact↔bead coupling measures nothing", RB-G7), while `new_change.py` refuses outright without the export and additionally refuses a bead whose status is `closed`.

**What links artifacts and beads today is one-directional.** The required frontmatter field `bead:` (in `plans_registry.REQUIRED`, rendered as the index's bead column) points artifact → bead. The reverse — bead → change folder — is not machine-readable anywhere in the tree; that is the companion bead `coding-harness-fmir`, queued together with this one: "coding-harness-680l with coding-harness-fmir (the class in a bead becomes machine-readable; a bead names its change folder)" (`docs/research/2026-10-26-night-run-plan.md`, queue item after m98e). No change folder for `coding-harness-fmir` exists (search over `plans/changes/*/research.md`, 2026-10-31).

**This change's own recorded intent.** The interview queue of 2026-10-21 frames the scope as a decision: "Every change has a bead and an explicit workflow class (`coding-harness-680l`): decide storage and agreement with change artifacts" (`docs/research/2026-10-21-night-run-plan.md`, "Interview queue after the bounded repairs", item 2); the same plan's stop list says "the class in every bead (coding-harness-680l). Each needs an interview first." The handover of 2026-10-27 lists it among beads "not started from the night plan" (`docs/journal/handover/2026-10-27-night-run.md`). The change folder holds only the skeleton `research.md` (bead `coding-harness-680l`, `implementation_status: none`, Stage-2 log line of today) and its header carries no `class:` field.

### Where it lives

- Contract and routing: `scripts/stage2.py` — `CLASSES`/`SWARM_CLASSES` (module constants), `declared_class` (the two-source reconciliation), `explore` (routing by class), `prepare_explore`, the `--class` argparse declaration and the verb restriction in `_run`.
- Preparation and receipt: `scripts/stage2_availability.py` (`prepare_research`, class check and refusal, receipt binding).
- Gate and inventory: `scripts/stage2_research_run.py` (manifest `class`), `scripts/check_research_handoff.py`, `scripts/research_handoff.py` (topic-3 class assessment).
- Independent class consumers: `scripts/check_interview_minimums.py` (`_CLASS_LINE`, `_spec_class_and_date`, `MINIMUMS`), `scripts/check_adr_answers.py` (own `CLASSES`).
- Tracker access: `scripts/bead_render.py` (one access point), `scripts/render_beads_export.py` (one writer), `scripts/check_bead_export.py` (line check, `id`/`status` only), `scripts/plans_registry.py` (`_bead_export_path`, `_bead_statuses`, `REQUIRED` with `bead:`), `scripts/new_change.py` (refusals on missing/closed bead), `tools/bd` (pinned wrapper).
- Tests pinning today's behavior: `tests/test_stage2_swarm.py` (duplicate header classes refuse, unreadable spec refuses class selection, unterminated header refuses, Unicode-separator fence cases), `tests/test_workflow_entry.py` (`_write_bead_export` fixtures write only `id`/`status`), `tests/test_research_handoff.py` (declared-class parameter of `derive_inventory`).
- Doctrine and prompts: `docs/WORKFLOW.md` (§2 "Change classes…", §4 routing paragraphs and the verb list), `README.md` ("Not every change is the same size"), `docs/adr/0020-phase-1-research-swarm.md` (points 1, 7, 11), `AGENTS.md` (the 2026-10-22 rule), `prompts/02-spec.md` (`class:` in the spec header), `prompts/02b-design.md` (design by class).

### What is unclear

- **The bead description of `coding-harness-680l` was not read.** The tracker is the Dolt database under `.beads/` and no rendered copy is committed (AGENTS.md house rule 2); nothing in this worktree quotes it, and whether it already names a class in which wording is unknown. The same wall is recorded verbatim in the sibling research of `plans/changes/fail-fast-attempts/research.md`.
- **The class of this change itself is not stated anywhere in the tree** — no `class:` in the skeleton header, and the night-run plan says only "each runs the full workflow for its class". Whether the bead description will be the first machine-read source is exactly what the interview must settle ("decide storage and agreement with change artifacts", `docs/research/2026-10-21-night-run-plan.md`).
- **The export row schema beyond `id`/`status` is not verified.** The line check pins only those two fields (`scripts/check_bead_export.py`); fixtures write only those two (`tests/test_workflow_entry.py`). The field name a description travels in is an open question — "not verified" here, not "absent".
- **Whether the bead statement is a third co-equal declaration** in `declared_class`'s must-agree set, a fallback behind the headers, or advisory — no artifact states it. `docs/WORKFLOW.md` §4 names exactly two sources today ("the class is read wherever stated in `--class` and the headers of `research.md` and `spec.md`").
- **Whether the runner should read the tracker render at all on the explore path.** The swarm's evidence collection deliberately reads no tracker ("No network or tracker is read", ADR 0020 point 3), `.beads/` is a runner-held checkpoint prefix and a review-diff skip part in `scripts/stage2.py`, and a fresh render materialises outside the worktree — none of the existing class checks touches it. Severity when nothing is measurable is likewise undecided: `plans_registry` measures-nothing-as-BLOCK versus `new_change.py` refusal are the two precedents, and `stage2.py` imports neither today.
- **Whether the class-reading gates follow** — `check_interview_minimums.py` and `check_adr_answers.py` each keep their own `CLASSES` tuple and their own header parser; whether they would also read a bead statement is unstated.
- **The exact wording of the nine bead comments of 2026-10-22** is not readable from this tree (the handover records only that they were added).

### Which files a change would have to touch

`scripts/stage2.py` (`declared_class`, `explore`, the `--class` argument, possibly `prepare_explore`); `scripts/stage2_availability.py` (class check before receipt sealing); a tracker-read helper beside or generalising `plans_registry._bead_statuses` through the `bead_render` access point, with `scripts/new_change.py` and `scripts/check_bead_export.py` as the neighboring readers/writers of the same format; `scripts/check_interview_minimums.py` and `scripts/check_adr_answers.py` if gates follow; tests `tests/test_stage2_swarm.py`, `tests/test_workflow_entry.py`, `tests/test_research_handoff.py`; doctrine `docs/WORKFLOW.md` §4 (both "wherever stated" passages), `README.md`, `AGENTS.md`, and `prompts/02-spec.md` if the declaration convention's wording changes. `plans/INDEX.md` is generated output of `render_index` and is never edited by hand.

### Neighbouring artifacts (candidates for the `neighbours:` header)

- `plans/changes/research-swarm/spec.md` — active, `class: architectural`; criteria 3, 4, 31 and 44 are the contract `declared_class` implements; the `declared_class` docstring cites its "criteria 3 and 4".
- `plans/changes/fail-fast-attempts/research.md` — active; the only sibling research that documents the same wall (bead description unreadable from the worktree, class supplied via `--class`) and cites `declared_class` for that inference.
- `plans/changes/archive/2026-09-21-reproducible-bead-export/spec.md` — archived; the byte-exact export line format (`_wie_der_tracker`, `MASCHINENLOKAL` in `scripts/render_beads_export.py`) that any new export reader inherits.
- `plans/changes/archive/2026-09-23-tracker-access-point/research.md` — archived; research behind the one-access-point contract (bead 1jg.3); it has no `spec.md` in the tree.
- `plans/specs/implementation-verification/spec.md` — living spec; read only in passing here (attempt preparation doctrine), and no relation to class declaration was found in what was read; listed as a known living spec, relation unestablished.
