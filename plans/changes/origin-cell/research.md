---
title: "Research — origin-cell"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-ywbh
owner: Data Architect
provenance: human-written
tags: [research]
---

# origin cell — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-07: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 922 files, 3573 commits, 12 rules.

## Runner exploration — 2026-11-07

The exploration is complete — every path is traced. Here is the research, ready to append to `plans/changes/origin-cell/research.md`.

---

## What exists today

**The mandate.** This change carries **DL-B-9** of the review-loop deep review B: "the repair brake reads an Origin cell no loop reviewer is told how to fill" (`plans/changes/review-loop-deep-b/findings.md`, row DL-B-9; restated in full in `docs/journal/handover/2026-10-25-cloud-runner-fixes.md`, section "Findings", DL-B-9). The review-loop-deep-b change explicitly cut it: `plans/changes/review-loop-deep-b/decisions.md` ("Not here: DL-B-9 … either a prompt change (`prompts/` is `human-written`) or a new ownership rule for the cell"), `plans/changes/review-loop-deep-b/spec.md` §Non-goals ("DL-B-8, DL-B-9, DL-B-13: open questions for the maintainer") and `plans/changes/review-loop-deep-b/plan.md` ("Not now: … DL-B-9 Origin vocabulary"). The maintainer answered on 2026-10-25 — answer 4 under "Maintainer's answers, 2026-10-25 (interview, conversation)" in `docs/research/2026-10-25-night-run-plan.md`: **"Origin cell for the repair brake (DL-B-9). The orchestrator sets Origin (`base` or `fix-r<N>`) when it decides a row. The runner refuses a taken row whose Origin is neither. No prompt changes."** The same answer is restated in the handover's decision table (`docs/journal/handover/2026-10-25-cloud-runner-fixes.md`, row DL-B-9) and referenced as the bead's mandate in the night-run plan's queue ("Repair brake: the orchestrator sets Origin (coding-harness-ywbh, answer 4)"). The bead id in the research skeleton's frontmatter is `coding-harness-ywbh`; the bead database itself is not readable from the tree (no rendered copy is committed), so everything about the bead here traces to those three documents. The change folder was opened on the worktree branch `fix/origin-cell` with commit `cedc3c43` ("docs(origin-cell): open the change folder"); `plans/INDEX.md` (row `changes/origin-cell/research.md`) lists the change as draft with implementation status none.

**The vocabulary.** Origin is the fourth cell of a loop row: `ROW_COLUMNS = ["ID", "Severity", "Dimension", "Origin", "Where", "Finding", "Reviewer", "Status", "Broke a test"]` (`scripts/stage2.py`, constant `ROW_COLUMNS`; released rows add "Phase 6" in `RELEASED_COLUMNS`). The meaning is defined in two places a reviewer is not required to read: `docs/WORKFLOW.md` §2 ("**Origin** records whether a finding existed before (`base`) or was produced by a repair round (`fix-r<N>`); two consecutive rounds whose only accepted findings begin `fix-r` trip the review loop's repair brake") and `templates/findings.md` ("**Origin** — `base` — the finding existed before the last repair. — `fix-r<N>` — repair round N produced it. Two consecutive rounds whose only accepted findings begin `fix-r` trip the review loop's repair brake"). The brake rule itself is ADR 0021 decision 7 (`docs/adr/0021-review-swarms-until-clean.md`: "Two consecutive rounds each having accepted findings all caused by repairs (Origin `fix-r`) stop and go to the maintainer (Q-3)").

**The brake.** `fix_r_only` (`scripts/stage2.py`, function `fix_r_only`) reads `row[3].startswith("fix-r")` over a round's accepted rows; the stop lives in `review_loop` (`scripts/stage2.py`, function `review_loop`), which refuses with "rounds N-1 and N accepted only findings whose Origin begins `fix-r`; the repair brake stops the loop; the maintainer decides what continues." History comes from the record and from every released block via `history_rounds`, filtered to rounds after a maintainer restart floor (`restarted_fresh`, `restart_floor`); `accepted_row` counts a row accepted when its Status begins `taken` or `fixed`.

**Where Origin content comes from today — the reviewer, nobody else.** `parse_rows` takes the six cells of an answer as they came; the round writer builds each record row as `[ident, *row[1:], member, "", ""]`, so the Origin cell travels verbatim from the reviewer's text into the record. `ANSWER_FORMAT` (the runner's answer instruction, embedded in every paid and free round prompt via `free_round_prompt`) names the Origin column to reviewers but defines no values — it says only that the severity cell is free text. `FREE_REVIEW_BODY` contains no Origin word at all. The orchestrator-facing prompt `prompts/04b-review-loop.md` likewise: its reviewer section gives the six-cell format without values for Origin, and its four orchestrator steps instruct writing `Status` and `Broke a test` only — no step says to write Origin. The runner itself never writes Origin: the only runner write into row cells is `_mark_record_rows` (called by `mark_repaired_record`), which rewrites `[*cells[:7], fixes[…], mark]` — Status and the test mark, leaving cells 1–7 (Origin included) untouched. There is no Origin validation anywhere in the runner: no refusal, check or normalisation of the Origin cell exists (`scripts/stage2.py` has no such code — "not there", verified by reading every `Origin`/`fix-r` occurrence in the file). The test suite compensates with `set_round_origin` (`tests/test_stage2.py`), whose docstring says it rewrites the cell "as a repair's provenance would" — i.e. the tests simulate a write that no code performs; the brake test `test_two_fix_r_rounds_stop_the_loop` uses it to trip and to quiet the brake. The tests' `decide_record` helper decides rows "the way the implementer would: by editing the file", writing Status and `Broke a test` only.

**How decided rows are handled today.** `undecided` treats a row as decided when its Status begins `rejected`, or `taken`/`fixed` with a `Broke a test` mark; `undecided_refusal` names the allowed Status values in its refusal text and is enforced at four places: `review_loop` entry, `review_loop`'s last-round stop, phase-6 `review`, and `release` ("nothing is released"). `record_rows` parses the record's own rows and already refuses two malformed shapes (too few cells; a Status whose mark moved out of its column) — the established pattern for this kind of refusal. Released rows are parsed by `findings_rows`; repair targets are collected from record, released and phase-6 tables by `repair_targets`. `fix_r_only` compares Origin case-sensitively, whereas every Status and Severity read in the same code paths lower-cases first.

## Where it lives

- Decision (mandate): `docs/research/2026-10-25-night-run-plan.md`, "Maintainer's answers, 2026-10-25", item 4; `docs/journal/handover/2026-10-25-cloud-runner-fixes.md`, decision table and findings.
- Originating defect report: `plans/changes/review-loop-deep-b/findings.md` (DL-B-9), `plans/changes/review-loop-deep-b/decisions.md` (scope cut).
- Doctrine: `docs/WORKFLOW.md` (Origin paragraph in §2; the phase-4b "review loop" section that describes Status/Broke-a-test writing), `docs/adr/0021-review-swarms-until-clean.md` decision 7, `templates/findings.md` (Origin vocabulary).
- Runner: `scripts/stage2.py` — `ROW_COLUMNS`/`RELEASED_COLUMNS`, `ANSWER_FORMAT`, `FREE_REVIEW_BODY`, `free_round_prompt`, `parse_rows`, `record_rows`, `undecided`, `undecided_refusal`, `round_rows`, `accepted_row`, `fix_r_only`, `history_rounds`, `findings_rows`, `repair_targets`, `mark_repaired_record`/`_mark_record_rows`, `review_loop`, `review`, `release`.
- Prompt: `prompts/04b-review-loop.md` (reviewer format + orchestrator steps).
- Tests: `tests/test_stage2.py` — `set_round_origin`, `decide_record`, `test_two_fix_r_rounds_stop_the_loop`, the doctrine guard `loop_doctrine_problems` with `test_the_loop_doctrine_names_both_swarms_until_clean` and `adr_0021_problems` with `test_adr_0021_amends_the_round_budget` (these pin phrases in WORKFLOW, template and ADR, among them "repair brake" and the template's "trip the review loop's repair brake").

## What is unclear about it

- **Scope of the new refusal.** The answer names "a taken row" without saying where. Accepted rows feed the brake from the record and from released blocks (`history_rounds`), and taken rows also exist in released and phase-6 tables as repair targets (`repair_targets`). Whether the Origin check covers record rows only — at `review_loop`, `review` and `release` entry, where `record_rows`/`undecided_refusal` already run — or also released/phase-6 rows via `findings_rows`, no source I read states. Open question for the interview/spec.
- **Does "taken" include `fixed`?** The brake's own notion of accepted (`accepted_row`) counts `fixed` like `taken`; whether a `fixed` row with a bad Origin cell is refused too is not stated anywhere.
- **Case.** `fix_r_only` reads `row[3].startswith("fix-r")` case-sensitively; Status/Severity reads lower-case first. Whether the Origin vocabulary is lower-case-only (`FIX-R1` would not trip the brake today) is not addressed by any source.
- **What "no prompt changes" covers.** `prompts/` is reserved `human-written` (`provenance.yaml`, prefix `prompts/`), and the decision excludes it. `ANSWER_FORMAT` is runner text that every reviewer prompt embeds; whether it may stop naming Origin (or name its values) under the "no prompt changes" answer is not stated. Same question for the WORKFLOW §4b sentence that would carry the ownership rule (`docs/WORKFLOW.md` allows `ai-drafted-reviewed`, `provenance.yaml` prefix `docs/WORKFLOW.md`).
- **Phase-6 rows.** The nine-cell phase-6 table shares the first six cells, Origin included; its Origin is reviewer text as well. Whether the ownership rule reaches it is not stated.
- **Records recovered by hand.** A lost record cannot be recovered by a verb today: `recover-loop` does not exist in `scripts/stage2.py` ("not there"); answer 5 of the same night plans one as an ADR 0021 decision-9 amendment. Whether hand-mended rows must then carry Origin, and whether the refusal should say so, is open.
- **I have not read** `docs/WORKFLOW.md` in full, `model-endpoints.yaml`, the DL-A change artefacts, or the bead itself; the bead's description is unreadable from the tree. What those hold about this topic is an open question, not a guess.

## Which files a change would have to touch

- `scripts/stage2.py` — the Origin check beside the existing row-refusal helpers (`record_rows`, `undecided`, `undecided_refusal`), wired at the entry points that already refuse (`review_loop`, `review`, `release`), possibly `findings_rows`/`repair_targets` if released and phase-6 rows are covered, and `fix_r_only` if case handling changes.
- `tests/test_stage2.py` — refusal tests beside `test_two_fix_r_rounds_stop_the_loop` and its helpers `set_round_origin`/`decide_record`; the doctrine guards (`loop_doctrine_problems`, `adr_0021_problems`) constrain any wording the change adds to WORKFLOW, the template or the ADR (pinned needles include "repair brake").
- `docs/WORKFLOW.md` — the phase-4b section that today tells the orchestrator to write Status and `Broke a test` would carry the Origin ownership sentence.
- `prompts/04b-review-loop.md` — excluded by the decision ("No prompt changes"); named here because it is where the gap was found.
- `templates/findings.md` — already defines the vocabulary; no change is evident from what I read.

**Neighbours** (for the `neighbours:` header): `plans/changes/review-loop-deep-b/spec.md` (bead coding-harness-pc7g — the review that opened DL-B-9, merged as PR #250 per the 2026-10-25 handover), `plans/changes/review-loop-deep-a/` (the DL-A sibling rows), `plans/changes/go-access-point/` (bead coding-harness-4tr4 — closed DL-B-8 with the "warn only" answer; its comment stands at the `OVERLAY_FIELDS` definition in `scripts/stage2.py`), `plans/changes/terms-expiry/` (bead coding-harness-abra — closed DL-B-13, answer 2), `plans/changes/free-member-rate-limit/` (the #247 mixed-case ADR 0021 amendment). The ADR names the restart command's own change as bead coding-harness-0xjr; a `plans/changes/` folder for it was not found in `plans/INDEX.md` (the runner command itself exists: `restart_loop` in `scripts/stage2.py`, `--restart` flag).
