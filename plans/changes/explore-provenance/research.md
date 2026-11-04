---
title: "Research — explore-provenance"
status: draft
implementation_status: none
date: 2026-11-04
last_reviewed: 2026-11-04
updated: 2026-11-04
supersedes: null
superseded_by: null
bead: coding-harness-g19n
owner: framework-architect
provenance: human-written
tags: [research]
---

# explore provenance — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-04: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 888 files, 3261 commits, 12 rules.

## Runner exploration — 2026-11-04

The research is complete. Here is the prose, ready to append to `plans/changes/explore-provenance/research.md`:

---

## What exists today

**The provenance declaration of a research artefact.** `provenance.yaml` declares five closed classes under `classes:`; `ai-drafted-reviewed` means a model drafted the text and a person accepted it, with `review_required: true`. The entry `prefix: "plans/"` allows exactly `human-written` and `ai-drafted-reviewed` and holds `frontmatter: required`. The map's header comment states the governing rule — provenance is declared, never hidden — and that `allowed:` is "declared, not yet enforced; nothing here reads it". Its named readers read other parts: `scripts/check_frontmatter_current.py` reads `paths:`/`excluded:` (`load_map`), `scripts/ramp_valves.py` reads `roles:`, and `scripts/harness.py` reads the `decisions/answers/` entry's `owner_role`.

**The skeleton.** `make change` runs `scripts/new_change.py` (Makefile, `change` target), which writes `research.md` with `provenance: human-written` and **no** `produced_by:`/`review:` lines — `_frontmatter_template`, whose docstring explains: the creating call is deterministic and human-issued, and "Whoever fills the body with a language model brings both up to date; the generated text says so". The body (`BODY_TEMPLATE`) carries "this file is empty until it has run" plus the blockquote instructing whoever fills the file with a model to set `ai-drafted-reviewed`, `produced_by:` and `review:`. There is no `templates/research.md`; the skeleton lives only in `new_change.py`.

**What the runner writes on explore.** Both routes append through one function. The single-model route (`explore()` in `scripts/stage2.py`) records the audit line via `begin_work_call` ("Stage-2 call, … explore · attempt … route … endpoint … model …") and then calls `append(ctx.research, "## Runner exploration — <date> …")` with the answer passed through `quote_research_records`, which makes any forged `research-swarm/v2` marker inert because the `research-handoff` gate (`scripts/check_research_handoff.py`, `_OPEN`/`_CLOSE`/`_FENCE_V2`) trusts only runner-written envelopes. The swarm route never lets a worker write the file ("No worker writes `research.md`", `scripts/stage2_research_run.py` module docstring); `publish()` appends the fenced envelope (`compose()`, bounded by the `BLOCK` regex) through `self.runner.append`. `append()` (in `scripts/stage2.py`) appends bytes and, in the same atomic replacement (`write_atomic`), sets the header's `updated:` to today via `check_frontmatter_current.stamped` — the pure single-line header-edit helper built for exactly this use ("the research append, deep review RS-2-6"). It touches no other header line: `provenance:`, `produced_by:` and `review:` stay as the skeleton wrote them.

**The asymmetry with findings.md.** When the runner creates `findings.md`, it writes a full header at birth: `findings_header()` emits `provenance: ai-drafted-reviewed`, `produced_by: {kind: llm-session, name: <producer>, version: "<day>"}` and `review: {status: pending, …}`; `producer_for()` maps the endpoint to a producer name (`openai-codex` → `codex`; `claude-code-plan` and `glm-coding-plan` → `claude-code`; else `pi`). `begin_call` and `begin_work_call` call it when findings.md is missing. research.md has no equivalent.

**The explorer model cannot fix it.** The explore call runs the model read-only: `run_work_model(..., writable=False)` passes `WORK_READ_TOOLS` and `--permission-mode dontAsk`; the file is written only by the runner.

**Who updates the header today.** Orchestrating sessions do it by hand: filled research.md files carry `produced_by: {kind: llm-session, name: claude-code, version: "<date>"}` (for example `plans/changes/pi-pin/research.md`, whose body says it was "seeded by the orchestrating session on 2026-10-15"). Nothing instructs or checks this: greps over `docs/WORKFLOW.md` and `prompts/` found no statement about updating research.md's provenance, and no gate reads the `provenance:` value of a plans/ header (below).

**The live gap, seen in this tree (2026-11-04).** Census over every `research.md` under `plans/changes/` matching `^provenance:`: 98 files — 94 `ai-drafted-reviewed`, 3 `human-written`, 1 `ai-generated` (`plans/changes/archive/2026-10-08-runner-derived-files/research.md`). The three `human-written`:
- `plans/changes/loop-until-clean/research.md` — an active change. The header still says `provenance: human-written` with no `produced_by:`/`review:`; the body still carries the skeleton sentence and the full "Bring the provenance up to date" blockquote, directly followed by the runner's stage-2 call line (2026-10-14, route flash, model glm-5.3-flash) and a filled `## Runner exploration` section. The blockquote's instruction was never carried out.
- `plans/changes/archive/2026-09-23-tracker-access-point/research.md` and `plans/changes/archive/2026-09-23-gate-placement/research.md` — archived, same shape.

This matches the recorded lesson "Runner explore leaves the skeleton banner and a human-written header in `research.md` (seen on h5tj, p6mu and l7sc). This adds to bead coding-harness-g19n" (`docs/journal/handover/2026-10-30-three-lane-night.md`) and the bead entry "coding-harness-g19n — explore leaves the research.md skeleton in place" (`docs/journal/handover/2026-10-28-three-lane-night.md`); bead coding-harness-er46 was merged into coding-harness-g19n (`docs/journal/handover/2026-11-02-five-lane-night.md`).

**What the checks measure about such a header.** `scripts/check_frontmatter_current.py` (gate `frontmatter-current`) holds only `updated:` against the last change; `plans/` is `frontmatter: required`, and the runner's stamp keeps it green. `scripts/plans_registry.py` (`REQUIRED`) demands `status`, `implementation_status`, `date`, `last_reviewed`, `bead` — `provenance` is not among them and no value check exists. `scripts/check_docs.py` checks presence of `provenance`/`produced_by`/`review` keys, but only under `docs/` by default (`--base docs/`), not `plans/`. So a research.md that a model filled but that still declares `human-written` is caught by no gate today. Precedent for holding a generated artefact's provenance value by test: `tests/test_feedback_channel.py` asserts a framework-raised handover is `ai-drafted-reviewed`, not another class. The only living spec shows a third class in use under `plans/`: `plans/specs/implementation-verification/spec.md` declares `provenance: ai-generated` — outside the two classes the map's `plans/` entry allows, and unmeasured like every other value.

**Not found, and not there.** `scripts/validate_provenance.py` is *not found* (glob over `scripts/`) and *not referenced* (grep over `tests/`); the `provenance.yaml` header comment still names it as a reader, and the `provenance-location` spec already records that comment as a stale text and a non-goal. No test pins the research header after an explore run: greps over `tests/` for "human-written", "skeleton" and "Bring the provenance" found nothing touching this; the explore tests pin only the appended body (`tests/test_stage2.py`, `test_explore_uses_flash_read_only_and_appends_research` and its neighbours assert `## Runner exploration` and the audit line).

## Where it lives

- `provenance.yaml` — `classes:`, `paths:` entry for `plans/`, the `allowed:`-unenforced comment.
- `scripts/new_change.py` — `BODY_TEMPLATE`, `_frontmatter_template`, `--owner` default; wired by the Makefile `change` target.
- `scripts/stage2.py` — `explore()` (single-model route), `begin_work_call()`, `append()`, `write_atomic()`, `stamp_updated()`, `quote_research_records()`, `findings_header()`, `producer_for()`, `run_work_model()` with the `writable` flag, and `declared_class()`, which reads the `class:` of research.md's and spec.md's headers — the same header a provenance rewrite would edit.
- `scripts/stage2_research_run.py` — `publish()`, `compose()`, the `BLOCK` envelope regex, the "No worker writes research.md" docstring.
- `scripts/check_frontmatter_current.py` — `stamped()` and `stamp()` (the single-line header edit `append()` composes in), `load_map()`.
- `scripts/check_research_handoff.py` — the envelope syntax (`_OPEN`, `_CLOSE`, `_FENCE_V2`) a header rewrite must not disturb.
- Tests: `tests/test_stage2.py` (explore appends, audit line, haiku fallback), `tests/test_stage2_swarm.py` (single explorer vs swarm sections), `tests/test_stage2_research_deep_review.py` (forged-envelope quoting), `tests/test_research_handoff.py`, `tests/test_frontmatter_current.py`, `tests/test_feedback_channel.py` (provenance-value assertion precedent).

## What is unclear

- The bead's current wording and acceptance frame (coding-harness-g19n) lives in the tracker; I cannot read the Dolt database with these tools. What the merged bead coding-harness-er46 contributed is likewise tracker-only.
- Which leftovers the change covers — the header only (the change's name says provenance), the skeleton banner too (the 2026-10-30 lesson names both), or the `BODY_TEMPLATE` blockquote's future wording — is stated in no artefact I read.
- What `produced_by.name` should hold for a swarm run (many seats; `producer_for()` maps exactly one endpoint) — nothing I read states this.
- Whether the update should ride `append()` for every research write or only the explore verbs: all routes flow through `append()`, but no artefact states the intended scope.
- Whether the archive exceptions (the two 2026-09-23 changes, and `ai-generated` on `runner-derived-files`) fall in scope or stay as history — nothing I read says.
- Whether a gate should ever read `allowed:` (today nothing does, per the map's own comment) — recorded as fact, not as a gap this change must close.

## Which files a change would have to touch

- `scripts/stage2.py` — `append()` is the single choke point both routes' research writes flow through; a header rewrite there would cover both routes, with `findings_header()`/`producer_for()` as the existing shape to mirror and `check_frontmatter_current.stamped` as the precedent for a pure header-edit helper composed into the atomic write.
- `scripts/stage2_research_run.py` — only if the swarm route needs its own producer naming; the write itself flows through `runner.append`.
- `scripts/new_change.py` — `BODY_TEMPLATE` and the `_frontmatter_template` docstring must say whatever the new behaviour is.
- `scripts/check_frontmatter_current.py` — possibly, if the provenance lines get the same pure-helper treatment; today it has no function for them.
- Tests: `tests/test_stage2.py`, `tests/test_stage2_swarm.py`, `tests/test_stage2_research_deep_review.py`, `tests/test_research_handoff.py` — whichever of their pinned behaviours change.

## Neighbours

- `plans/changes/provenance-location/spec.md` (bead coding-harness-3ar.1, bounded) — the other provenance change: where `harness.py decide adr` reads the provenance *map*; it names the map's other readers (`check_frontmatter_current.py`, `ramp_valves.py`, `stage2.py`) as an explicit non-goal.
- `plans/changes/archive/2026-09-29-frontmatter-current/` — the change that delivered the `updated:`-currency gate and the stamp `append()` uses.
- `plans/changes/research-swarm/` — the swarm whose runner appends the envelopes (spec, design, findings).
- `plans/changes/explorer-reviewer-agents/` — the explorer/reviewer sub-agent definitions.
- `plans/changes/loop-until-clean/` — the live case with the un-updated header.
