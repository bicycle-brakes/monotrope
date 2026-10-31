---
title: "Research — free-round-clean"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-1gzo
owner: Data Architect
provenance: human-written
tags: [research]
---

# free round clean — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 788 files, 2835 commits, 12 rules.

## Runner exploration — 2026-10-31

Die Recherche ist vollständig — hier der Text zum Anhängen an `plans/changes/free-round-clean/research.md` (Englisch, wie es das Repository verlangt):

---

## What exists today

**The behavior the bead names.** The review loop ends on the first clean round, at any round number — including round 1, the free swarm. The stop order in `review_loop` (`scripts/stage2.py`, function `review_loop`, docstring and body ~7811–7864) is: undecided rows first, then the clean stop (`clean_round(...) and not round_was_cut(...) → raise CleanStop`, at the check around line 7853), then the repair brake (`fix_r_only` on two consecutive rounds), then spent stages. The clean stop is checked before any stage is taken, so a clean free round prevents the Flash stage from ever starting. `clean_round` (`scripts/stage2.py:3246`) defines clean as every row decided and none accepted; a round with no rows at all is clean, and a `fixed` row keeps the round not clean (criterion 11 of the loop-until-clean spec, `plans/changes/loop-until-clean/spec.md`). The stop is a finish, not a refusal: `CleanStop` (`scripts/stage2.py:522`, docstring "not a refusal, and told apart by its exit code") with `CLEAN_CODE = 3` (`scripts/stage2.py:251`); `docs/WORKFLOW.md` §4 documents exit 3 as "a loop that finished with a clean round" (R-11). The stop survives a release (test `test_a_clean_round_ends_the_loop`, `tests/test_stage2.py:7087`).

**The rule questioned is a recorded decision.** ADR 0021 decision 1 (`docs/adr/0021-review-swarms-until-clean.md`, decision 1): "A clean free round ends the loop before any paid review", decided in Q-10 (`plans/changes/loop-until-clean/decisions.md` as referenced by the ADR header and the spec's adr_question). The maintainer reopened Q-10 on 2026-10-23 — recorded in `docs/research/2026-10-24-weekend-run-plan.md` (waiting table, row coding-harness-1gzo): "intended by ADR 0021 decision 1 (Q-10); the maintainer reopened Q-10 on 2026-10-23: research runs this weekend (clean free rounds against later phase-6 findings), the interview waits for the next joint window."

**Stage schedule the change would sit in.** `stages_of` (`scripts/stage2.py:3309`) orders the run's stages: free swarm → Flash swarm (`paid-swarm`) → one stage per remaining `modelle` rung. `new_state` (`scripts/stage2.py:3284`) pins the snapshot; with `availability_preflight` enabled (it is, for `opencode-go`: `model-endpoints.yaml`, entry `opencode-go`, block `availability_preflight`, `flash_size: 3`) the state comes from `stage2_availability.consume`, where free members are filtered to the reachable and the Flash swarm is the first `flash_size` cheapest reachable admitted paid models (`scripts/stage2_availability.py`, `prepare` state building ~1408–1412; rule validation in `rule_problem`, `flash_size` 1..3, ~173–191).

**Guard-rails that bound any rework (all read, all current):**

- The free round is confined to the implementation diff, no tools (`prompts/04b-review-loop.md`, "Input" and "For the reviewer" sections; `docs/WORKFLOW.md` §4: bounded hunks up to `REVIEW_DIFF_MAX_LINES`, 2000 lines; machinery in `free_diff`, `scripts/stage2.py:2330`, with `FREE_DIFF_TEXT_SUFFIXES` at 2229).
- A round over a cut diff never counts as clean: `round_was_cut` (`scripts/stage2.py:3236`) — DL-A-1 of the deep review (`plans/changes/review-loop-deep-a/spec.md`, criterion 1; planted-fault test `tests/test_stage2.py:16518`).
- No implementation diff → the free stage is skipped and the next stage takes the round (`scripts/stage2.py:7894–7898`, "free stage skipped: no implementation source diff").
- Every free member failing with rate-limit/unavailability drops the free stage and the Flash swarm takes the round (`plans/changes/free-member-rate-limit/spec.md`, criterion 1; `docs/WORKFLOW.md` §4, bead coding-harness-pj98).
- An empty eligible Flash stage is skipped without a round (ADR 0021 decision 5; `new_state` docstring `scripts/stage2.py:3288`); a paid model enters only with a dated terms reading in `modelle_terms` (`model-endpoints.yaml`, entry `opencode-go`; `paid_problem`, `scripts/stage2.py:1734`).
- All-failed preparation refuses and never creates a clean round (`scripts/stage2_availability.py:1428–1429`; test `test_all_failed_preparation_never_creates_a_clean_round_or_reuses_receipt`, `tests/test_stage2_availability.py:189`).
- The free swarm's membership is unbounded in code (R-12 of the review-swarm runner review, `docs/journal/handover/2026-10-20-review-swarm-runner-review.md`; also bead coding-harness-3ql, `docs/journal/handover/2026-10-21-merge-day.md`).
- Today's only path to paid review after a clean free round is the maintainer's explicit restart (`release-loop --restart --reason`, ADR 0021 restart amendment, `docs/adr/0021` end section; test `tests/test_stage2.py:7115`).

**Observed occurrences in practice:**

- PR #223, 2026-10-22/23: the loop ended after round 1 (free swarm, `cat-jam-free`, no finding); "neither the Flash swarm nor a paid rung read this change. Worth checking against ADR 0021's intent" (`docs/journal/handover/2026-10-23-night-run.md`, morning section). This produced bead coding-harness-1gzo (same handover, bead list of 2026-10-23).
- PR #232 ("A4"), 2026-10-24: the free model answered on the second try, its round had no finding, the loop ended; phase 6 found no finding; the maintainer approved the merge with only the free round run (`docs/journal/handover/2026-10-23-night-run.md`, "Update — 2026-10-24 10:45 UTC").
- The #158 research-swarm live test saw a "free round clean over a cut diff" while the Flash round still ran (`docs/journal/handover/2026-10-22-joint-window.md`) — the case DL-A-1 then closed.

**Doctrine and configuration stating the current rule** (a change to the behavior contradicts each of these today): `AGENTS.md` table row 4b and the stage-2 paragraph; `docs/WORKFLOW.md` table row 4b and §4 ("until a round is clean — every row of a round decided and none accepted", the swarm descriptions); `prompts/04b-review-loop.md` (header paragraph and "For the orchestrator"); the `opencode-go` `bemerkung` in `model-endpoints.yaml` ("The loop runs until a round is clean … round 1 is the discovered free-model swarm, round 2 the parallel `flash_swarm`…"); `README.md` (the loop sentences) and `docs/how-it-works.md` (the stage table and the loop flow diagram).

## Where it lives

Runner logic in `scripts/stage2.py` (`review_loop`, `clean_round`, `fix_r_only`, `round_was_cut`, `stages_of`, `next_stage`, `new_state`, `CleanStop`/`CLEAN_CODE`); availability preparation in `scripts/stage2_availability.py` (`rule_problem`, `prepare`, `consume`, `report`); configuration in `model-endpoints.yaml` (entry `opencode-go`: `availability_preflight`, `free_stage`, `flash_swarm`, `modelle`, `modelle_terms`); doctrine in `AGENTS.md`, `docs/WORKFLOW.md` §4, `prompts/04b-review-loop.md`, `README.md`, `docs/how-it-works.md`; tests in `tests/test_stage2.py` and `tests/test_stage2_availability.py` (also `tests/test_stage2_terms_expiry.py` touches the loop's expiry stops). The decision record is ADR 0021 with the answer file `decisions/answers/loop-until-clean/adr.yaml`.

## What is unclear

- **The bead's own text is not read, not absent.** The tracker is the Dolt database under `.beads/` and this explorer runs no command, so the description and notes of coding-harness-1gzo were not read directly; the scope above is reconstructed from the handover and research-plan references to it (`docs/journal/handover/2026-10-23-night-run.md`, `docs/research/2026-10-24-weekend-run-plan.md`, `docs/research/2026-10-28-night-run-plan.md`).
- **The intended shape is an open decision, not a fact.** The research scope recorded for the bead asks "the best approach for a review swarm; above all whether free models are used at all, and if so together with the Flash swarm in one round", with the maintainer's leaning "a ladder of 4, 3, 2, 1 models per round with rounds 1 and 2 mandatory" recorded under bead coding-harness-r3b6 (`docs/research/2026-10-24-weekend-run-plan.md`). No repository file decides between these shapes; the interview owes that answer.
- **ADR 0021 amendment path.** Reopening Q-10 means decision 1 changes only through a recorded maintainer answer. Precedents: the restart amendment appended to ADR 0021; the 45-minute `REVIEWER_MINUTES` episode, where an ADR edit without its own interviewed change was refused by `interview-minimums` (`docs/journal/handover/2026-10-23-night-run.md`, reviewer-limit entry); and the pj98 non-goal naming "an ADR 0021 amendment and its own interview" for loop-stage changes (`plans/changes/free-member-rate-limit/spec.md`, non-goals).
- **Interaction with the paid gates is undecided.** A mandatory paid round collides with the terms gate (an empty eligible Flash stage is skipped, not an error), the all-failed rules (no reachable reviewer refuses rather than counting clean), and rate-limit drops that hand the round to Flash — the guard-rails above are facts; how a mandatory-round rule reorders them is not written anywhere I read.
- **Cost consequence is unquantified.** ADR 0021's Q-16 amendment already notes probes cost requests "even when the first review round will be clean"; no repository text quantifies what mandatory paid rounds cost per change. Not found — and distinct from "not there": I did not search the vendor pages, only the repository.

## Which files a change would have to touch

`scripts/stage2.py` (the clean stop in `review_loop`, `stages_of`/`next_stage` scheduling, `clean_round`, `new_state`, `CleanStop`/`CLEAN_CODE` if stop semantics move) · `scripts/stage2_availability.py` (`rule_problem` flash_size, `prepare` state building, `report`) · `model-endpoints.yaml` (entry `opencode-go`: `availability_preflight`, `flash_swarm`, `free_stage`, `bemerkung`) · `tests/test_stage2.py`, `tests/test_stage2_availability.py` · doctrine: `AGENTS.md` (mind its 200-line cap), `docs/WORKFLOW.md` (table row and §4), `prompts/04b-review-loop.md`, `README.md`, `docs/how-it-works.md` · decision record: a new amendment in `docs/adr/0021-review-swarms-until-clean.md` plus a new answer file under `decisions/answers/free-round-clean/` recorded via `scripts/harness.py decide adr` (house rule 8); `decisions/answers/loop-until-clean/adr.yaml` stays untouched · `plans/INDEX.md` regenerates by the runner.

**Neighbours** (known specs of neighbouring changes): `plans/changes/loop-until-clean/spec.md`, `plans/changes/free-member-rate-limit/spec.md`, `plans/changes/terms-expiry/spec.md`, `plans/changes/review-loop-deep-a/spec.md`. The living spec `plans/specs/implementation-verification/spec.md` was checked and covers derived-file preparation, not the review loop. No existing artefact in `plans/changes/` covers this topic — the only match is this change's own empty `research.md` skeleton, so appending is correct, nothing to update.

---

Zwei Hinweise für den Lauf: Das Skelett verlangt beim Befüllen `provenance: ai-drafted-reviewed` mit `produced_by:` und `review:` (Eigernote in `plans/changes/free-round-clean/research.md`), und die bestehende Stage-2-Aufrufzeile (Zeile 27) bleibt stehen. Offen bleibt der Wortlaut des Beads selbst — Dolt-Datenbank, von hier aus nicht gelesen; das steht oben ausdrücklich als offene Frage.
