---
title: "Research — research-free-paid"
status: draft
implementation_status: none
date: 2026-11-05
last_reviewed: 2026-11-05
updated: 2026-11-05
supersedes: null
superseded_by: null
bead: coding-harness-wb40
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: feature
---

# research free paid — Research

Stage-2 call, 2026-11-05: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 901 files, 3316 commits, 12 rules.

## Runner exploration — 2026-11-05

The exploration is complete. Here is the research, ready to append to `plans/changes/research-free-paid/research.md`:

---

## What exists today

The repository runs two model-cost classes on the `opencode-go` endpoint, and the two swarms read them differently. The paid class is the `modelle` list plus a passing `modelle_terms` record with a positive `anfragen_5h`; the free class is every catalog id ending in the suffix `-free`. The declaration currently holds `beam-free` — an id ending in `-free` — inside the paid `modelle` list (`model-endpoints.yaml`, entry `opencode-go`, list `modelle`), with a `modelle_terms` record marked `uebersprungen: "2026-10-30"` and the reason "not in the live Go catalog (2026-10-30)" (`model-endpoints.yaml`, `modelle_terms.beam-free`). The pinned Pi moved to 1.5.0 (`tools/pi/package.json`, decided in `plans/changes/pi-catalog-move/decisions.md` Q-1), and that version's shipped catalog lists `beam-free` again (pi-catalog-move decisions Q-2 context: "Pi 1.5.0's catalog lists `beam-free` for opencode-go for the first time (read 2026-11-04)").

The review loop already guards the collision. `free_drops` in `scripts/stage2.py` drops every free candidate that the endpoint declares paid in `modelle`, with the recorded reason "a paid model; the free class does not admit it", and its docstring states the principle: "a shipped catalog id can carry the free suffix and still be a paid model". The call boundary refuses the same case again (`_free_admission`, `scripts/stage2.py`). A proof test exists: `test_a_declared_paid_model_with_the_free_suffix_is_not_selected_free` (`tests/test_stage2_availability.py`), which plants `beam-free` in the catalog and asserts it is skipped by name, never probed, and the remaining free candidate carries the stage. The maintainer decided this in pi-catalog-move Q-2 (2026-11-04): "the paid admission wins in code; an id the `opencode-go` entry declares in `modelle` is never selected by the `free_stage` rule, whatever its suffix", achieving "a cost class set by the maintainer's admission rather than a name"; the decision calls it "a precision of the free rule of ADR 0021 in code; no data change".

The research swarm has no corresponding guard — that is the gap this change addresses. The free roster of a research run is selected by `select_research_catalog` (`scripts/stage2_swarm.py`): its candidate loop takes every id of the fresh Pi overlay ending in `-free` plus every `-free` baseline id, and filters only by fresh-Pi validity (`pi_reason`), models.dev tool-call/deprecation metadata (`metadata_reason`) and the `online_free` policy include/exclude. The function's signature receives `(bridge, policy, fixed_ids, …)` — no endpoint declaration — so it cannot see `modelle` at all. The call boundary for a research free seat, the `online_free` branch of `invocation_problem` (`scripts/stage2_swarm.py`), checks provider, suffix, policy exclude/include and the run's frozen selection, plus `exclusion_problem` (the `ausgeschlossen` list, data class `public-web`) — again no paid check. In `prepare_research` (`scripts/stage2_availability.py`), `free_selected` filters the catalog selection only by `exclusion_problem(data, m, "public-web")`, and every selected candidate is probed with the real-size online-topic request (`probe_free_research`, 120 seconds with one 360-second retry after a timeout); a failed free probe only removes the candidate, it never blocks the 39 required slots. The paid path is separate and guarded: the seat/pool classification (`_go_outcome` in the `_Selection` class, `scripts/stage2_availability.py`) requires a passing terms record and a positive `anfragen_5h`, and `-free` ids are barred from every role except `online_free` (`invocation_problem`: "a -free model never fills the <role> role"). The `preferred` set in `prepare_research` explicitly excludes declared ids ending in `-free`, so `beam-free` never reaches the paid classification either — it falls entirely into the free class of a research preparation. The report would not name the conflict: the "Unread (no data-terms record, never used)" line skips ids ending in `-free` (state building in `prepare_research`), and `research_report` prints `beam-free` only under "Free selection:".

Consequence as measured today: with Pi 1.5.0's catalog, `prepare-explore` classifies `beam-free` as a free candidate, probes it with a real-size call and, if it answers, freezes it into the selection and `N` — it then runs online topics 9–11 as a best-effort free researcher on the free class's unread-terms acceptance, while the same id is a maintainer-admitted paid model whose terms reading is marked skipped. The review loop refuses exactly this case on the same catalog. A search for any research-side refusal of a paid-declared `-free` id in `select_research_catalog`, `invocation_problem` and `prepare_research` found none, and `tests/test_stage2_research_catalog.py` contains no test planting a paid-declared `-free` id — not found is distinct from the review loop, where both the code path and the test exist.

Two adjacent facts belong here. First, `step-5-preview-free`: the review loop's `free_stage.exclude` names it with a dated reason ("every call fails with 'Upstream request failed: Model is unavailable'", 2026-10-17; `model-endpoints.yaml`, `free_stage.exclude`), while the research policy `research_swarm.online_free` declares `exclude: []` (`model-endpoints.yaml`, `research_swarm` block), so the research free roster carries no such exclusion; the paid `step-5-preview` terms record notes "the catalog lists step-5-preview-free". A failed research free probe is named and non-blocking, so this is a wasted-call cost, not a refusal. Second, the wider free/paid split of the research swarm for context: `research_swarm.paid_endpoint` is `claude-code-plan` with the Opus roles `topic_author` and `judge`; the six seats are declared in `repository_seats`/`online_seats` with open Go seats since Q-18; the budget is `39 + 3N` with free models on online topics only, best-effort (AGENTS.md swarm paragraph; `docs/WORKFLOW.md` swarm row, "Preparation before a run"; research-swarm spec criteria 19, 39, 40, 42, 48 in `plans/changes/research-swarm/spec.md`).

## Where it lives

- Declaration: `model-endpoints.yaml` — `opencode-go.modelle` (paid set, holds `beam-free`), `modelle_terms` (terms readings and `anfragen_5h`), `free_stage` (review loop's free rule with its `exclude`), `research_swarm` block (`paid_endpoint`, seats, `online_free` policy, `measured_wire_apis`).
- Review-loop guard: `scripts/stage2.py` — `free_drops`, `_free_admission`; proof in `tests/test_stage2_availability.py` (`test_a_declared_paid_model_with_the_free_suffix_is_not_selected_free`).
- Research free route: `scripts/stage2_swarm.py` — `select_research_catalog`, `validate_research_free_policy`, `invocation_problem` (`online_free` branch); `scripts/stage2_availability.py` — `prepare_research`, `probe_free_research`, `free_research_probe_text`, `_Selection.fill`/`_go_outcome`, `research_report`.
- Decision precedent: `plans/changes/pi-catalog-move/decisions.md` Q-2 (bead coding-harness-vku6), its `spec.md` criterion 5 and `findings.md` notice line "free ids dropped: beam-free (a paid model; the free class does not admit it)".
- Doctrine sentences that describe the research free roster: `docs/WORKFLOW.md` (swarm row, "Preparation before a run", the `explore`/`prepare-explore` verb paragraphs), AGENTS.md (the swarm paragraph, "the free models work the online topics only"), and the neighbour spec `plans/changes/research-swarm/spec.md` (Terms "Selected Go free models", "Admitted Go model", criteria 39, 40, 42, 48, 60).

## What is unclear about it

- The bead `coding-harness-wb40` description (its class and the exact scope the maintainer gave it) was not read: this session is read-only and the tracker is a Dolt database no command may open here. The change folder records only the skeleton and the Stage-2 call line of 2026-11-05 (route flash, `glm-5.3-flash`), and `plans/INDEX.md` lists the change with implementation status none.
- Whether the research free roster should follow the review loop's rule (paid admission beats the suffix), keep suffix-only selection, or additionally import dated unavailability exclusions such as `step-5-preview-free` into `research_swarm.online_free.exclude` — no repository text decides this.
- A wording tension in the neighbour spec that a change here would touch: criterion 60 of `plans/changes/research-swarm/spec.md` says a Go model without a passing terms record or positive `anfragen_5h` "is never probed, selected or used as a substitute", without scoping itself to seats, while the Terms' "Selected Go free models" section and criteria 39 and 48 explicitly probe and select free candidates that have no terms record. The repository records no ruling reconciling the two passages.
- Whether doctrine must move with the code: the pi-catalog-move precedent settled its same-shaped question as "a precision … in code; no data change" with accepted ADRs unedited; whether the research-side precision needs a spec/header change in the research-swarm neighbour (an active change, bead coding-harness-icw) or only in this change's own artefacts is open.

## Which files a change would have to touch

- `scripts/stage2_swarm.py` — the free-candidate classification in `select_research_catalog` and/or the `online_free` branch of `invocation_problem` as the call-boundary backstop; note the selector currently receives no declaration data, so either the declaration is passed in or the guard sits in `prepare_research`, which already holds both catalog and declaration.
- `scripts/stage2_availability.py` — `prepare_research`'s free filtering and the state it reports (`free.selected`, `unread`, candidate reasons), possibly the `preferred` set.
- `tests/test_stage2_research_catalog.py` and/or `tests/test_stage2_research_availability.py` — the proof test, mirroring the review loop's test in `tests/test_stage2_availability.py`.
- `model-endpoints.yaml` — only if the declaration itself changes; today `beam-free` stands in `modelle` as the paid admission and `online_free.exclude` is empty, which the code, not the data, would have to reconcile.
- Doctrine and neighbour texts that state the free rule: `docs/WORKFLOW.md`, AGENTS.md, and `plans/changes/research-swarm/spec.md` as a neighbour, plus a `neighbours:` entry for `plans/changes/pi-catalog-move/spec.md`, whose decision this change would carry over to the research route.
