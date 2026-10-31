---
title: "Research — unreadable-member-replaced"
status: draft
implementation_status: none
date: 2026-10-31
last_reviewed: 2026-10-31
updated: 2026-10-31
supersedes: null
superseded_by: null
bead: coding-harness-mfth
owner: Data Architect
provenance: human-written
tags: [research]
---

# unreadable member replaced — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-31: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 788 files, 2844 commits, 12 rules.

## Runner exploration — 2026-10-31

Research complete. Everything below is repository fact with sources; the artefact text is English and ready to append to `plans/changes/unreadable-member-replaced/research.md` (which today holds only the skeleton header plus the Stage-2 call line).

---

## What exists today

**The bead's own scope statement** lives outside the change folder: `docs/research/2026-10-28-night-run-plan.md:116` — "coding-harness-mfth (bounded): a review member with no readable content after the format feedback is replaced for that round only." Lane A, item 5, of the 2026-10-28 night run. No other artefact (spec, decisions, findings) exists for this change; `plans/INDEX.md:379` lists only the draft `research.md`.

**The mechanism chain, all in `scripts/stage2.py`:**

- **Answer classification.** `run_reviewer` (scripts/stage2.py:2533, function `run_reviewer`) raises on a nonzero Pi exit; a successful but empty answer raises `MalformedAnswer` (scripts/stage2.py:2627–2629, comment "A successful empty response is malformed too"). `run_swarm` (scripts/stage2.py:2633, function `run_swarm`) runs every member concurrently in threads and records per member either the scrubbed answer or the exception (scripts/stage2.py:2657–2667); an answer with no six-cell row that is not exactly `No finding.` raises `MalformedAnswer`, which carries the answer text (scripts/stage2.py:2660–2664). A `Refused` outcome aborts without a round (scripts/stage2.py:2679–2683). `MalformedAnswer(CallFailed)` is defined at scripts/stage2.py:568 — it is an exception subclass, so every downstream `isinstance(..., BaseException)` check sees it. The phase-6 verdict path keeps plain `CallFailed` on the same condition (function `review`, scripts/stage2.py:2939–2941) and is declared out of scope by the ancestor change.

- **The format feedback (the "asked-again" pass, bead coding-harness-70rw).** `ask_malformed_again` (scripts/stage2.py:8054–8090, function `ask_malformed_again`) retries a member exactly once when its answer is `MalformedAnswer`; the retry prompt is the member's prompt plus `FORMAT_REMINDER` and `ANSWER_FORMAT` (constants at scripts/stage2.py:261–272). The retry is leak-checked (`checked_prompt`), writes its own call line, counts in `audited`, and shares the round's one deadline (scripts/stage2.py:8048–8050; `REVIEWER_MINUTES = 45` at scripts/stage2.py:249). The first answer is quoted into the round via `malformed_blocks` and `NOT_ROWS_NOTE` (scripts/stage2.py:421, 8079–8090); a second malformed answer is quoted too and stands — today nothing replaces it except in the Flash stage. The blocks also reach the no-round audit appendix on a failed round (scripts/stage2.py:8216–8229).

- **What happens after the format feedback, per stage kind** (`stages_of`, scripts/stage2.py:3309, function `stages_of`; three kinds):
  - **Free stage** (`kind: "free"`, members = `state["free"]["selected"]`): no replacement exists. Failed members are excluded from `succeeded` (scripts/stage2.py:8149); one valid member saves the round with the failures stated (scripts/stage2.py:8160–8165, pinned by `tests/test_stage2.py:7290–7299`, "from 1 of 2 members"); if every member failed, `CallFailed` aborts with no round written and the stage not consumed (scripts/stage2.py:8155–8156; pinned by `test_a_second_malformed_answer_fails_the_member`, tests/test_stage2.py:7371). A later `review-loop` call then starts the free stage again.
  - **Flash stage** (`kind: "paid-swarm"`): a twice-malformed member **is replaced today** — the replacement loop (scripts/stage2.py:8094–8148) walks the cheapest admitted ladder rung not in the round and not consumed while `answers[current]` is a `BaseException`, which includes the second `MalformedAnswer`. The replacement gets the same paid prompt, is leak-checked, audited, shares the deadline, and is itself asked again if malformed (scripts/stage2.py:8146). Pinned by `test_a_flash_member_malformed_twice_is_still_replaced` (tests/test_stage2.py:18332, "Criterion 3, as today", from the orchestrator's self-review 2026-10-26) and by ADR 0021 decision 4 (docs/adr/0021-review-swarms-until-clean.md:121–129). **A replacement is consumed for the whole run**: `state["consumed"]` gains `rung:<model>` (scripts/stage2.py:8213–8214), "it is no later rung" per ADR 0021.
  - **Single paid rung** (`kind: "paid"`, one member): no replacement; a second malformed answer fails the stage with no round, the same `not succeeded` path.

- **Adjacent failure-class dispatch, already landed (bead coding-harness-pj98).** `rate_limited()` (scripts/stage2.py:7797–7806, pattern `_RATE_LIMITED` at scripts/stage2.py:7790) classifies rate-limit/unavailable failures; when *every* free member failed that way, `FreeStageUnavailable` drops the whole free stage so the next stage takes the round (scripts/stage2.py:7941–7952). Its decisions explicitly keep other failures ordinary: "an empty or unreadable answer and any other exit stay ordinary failures" (plans/changes/free-member-rate-limit/decisions.md:49).

- **Raw material for a free replacement pool exists in the run state.** `discover_free` (scripts/stage2.py:2122, function `discover_free`) pins `catalog`, `selected`, `dropped` and `overlay` into the run state (scripts/stage2.py:2212–2220). Only `selected` members run; the rest of the overlay is used for notices only (`unread_catalog_ids`, scripts/stage2.py:1685 — "A notice only: such an id is never admitted").

**The doctrine sentence that states today's rule:** docs/WORKFLOW.md:1407–1409 — "a second malformed answer fails the member as today (bead coding-harness-70rw)."

## Where it lives

Runner: `scripts/stage2.py` — `_review_round` (scripts/stage2.py:7955), `ask_malformed_again` (8054), Flash replacement loop (8094–8148), consumption update (8214), `run_swarm` (2633), `run_reviewer` (2533), `MalformedAnswer` (568), constants (261–272, 421), `stages_of`/`next_stage` (3309–3327), `new_state` (3284). Tests pinning the today-contract, all in `tests/test_stage2.py`: `test_a_malformed_answer_is_asked_once_more` (7316), `test_an_empty_answer_is_asked_again_with_the_format_reminder` (7343), `test_the_first_malformed_answer_is_kept_in_the_round` (7359), `test_a_second_malformed_answer_fails_the_member` (7371), `test_the_second_call_has_its_own_call_line` (7382), `test_no_second_call_after_the_round_deadline` (7395), `test_a_replacement_that_answers_malformed_is_asked_again` (7415), `test_both_malformed_answers_reach_the_record` (7436), `test_a_leak_block_on_the_retry_prompt_makes_no_second_call` (7457), `test_a_round_failed_past_the_deadline_names_the_skipped_retry` (7483), `test_a_flash_member_malformed_twice_is_still_replaced` (18332). Ancestor change: `plans/changes/malformed-answer-retry/` (bead coding-harness-70rw; spec criterion 3 at plans/changes/malformed-answer-retry/spec.md:44–47; the maintainer's 2026-10-24 answer in plans/changes/malformed-answer-retry/decisions.md Q-1: "if the second answer is malformed too, the round fails as today"). ADR: docs/adr/0021-review-swarms-until-clean.md decision 4. Doctrine: docs/WORKFLOW.md:1407–1409.

## What is unclear

- **Which reading "replaced for that round only" carries is not settled in any artefact I read.** Two candidate readings exist: (a) it extends replacement to the stages that lack it today (free stage, single paid rung), where a member with no readable content after the format feedback currently fails the member or the round; (b) it changes the Flash replacement's consumption, since today a replacement rung is spent for the whole run (scripts/stage2.py:8214; ADR 0021 decision 4) — "for that round only" would amend that decided rule. The night-run plan line supports neither reading over the other.
- **Not found:** any statement anywhere in `plans/`, `docs/` or `AGENTS.md` about which model may replace a free-stage member, or that a free member is replaced at all. The bead's full description sits in the Dolt tracker, which this phase does not read; the one sentence in `docs/research/2026-10-28-night-run-plan.md:116` is everything the tree carries.
- **Scope of "review member":** whether the phase-6 verdict (Codex `review`, plain `CallFailed` at scripts/stage2.py:2939–2941) and the research swarm's malformed-contribution handling (a distinct mechanism, `tests/test_stage2_swarm.py:2960`) are out of scope, as the ancestor change declared them (plans/changes/malformed-answer-retry/spec.md:57–61).
- **Interaction with the deadline and the ladder:** if a round-only replacement consumes nothing, the existing "no replacement is left on the ladder" and `NotStarted`/`AdmissionRefused` skip paths (scripts/stage2.py:8105–8135) need a stated free-stage counterpart; nothing in the tree says what replaces a free member when the overlay holds no further admissible id.

## Which files a change would have to touch

`scripts/stage2.py` (`_review_round`'s asked-again and replacement flow, scripts/stage2.py:8054–8148; the consumption update at 8214; possibly `stages_of`/`new_state` if a free replacement pool is drawn from the pinned state); `tests/test_stage2.py` (the pins listed above, of which `7371` and `18332` state the behaviour most directly); `docs/WORKFLOW.md` (the doctrine sentence at 1407–1409); and — only under reading (b) — `docs/adr/0021-review-swarms-until-clean.md` decision 4.

## Neighbours (for the header)

`plans/changes/malformed-answer-retry/` (coding-harness-70rw, the ancestor mechanism) · `plans/changes/free-member-rate-limit/` (coding-harness-pj98, free-stage failure-class dispatch) · `plans/changes/loop-until-clean/` (round/stage/consumed contract) · `plans/changes/fail-fast-attempts/` (lane A sibling) · `docs/adr/0021-review-swarms-until-clean.md` · `docs/research/2026-10-28-night-run-plan.md` (the scope statement).

---

**Zur Orientierung:** Die Recherche ist fertig; der Change ist `bounded` (Nachtlauf-Plan, Lane A), also war ich der einzelne Flash-Explorer ohne Swarm. Der einzige echte Befund mit Entscheidungsbedarf: „for that round only" passt zu zwei verschiedenen Lücken (Free-Stage hat heute gar keine Ersetzung; Flash-Ersetzung wird heute für den ganzen Run verbraucht) — das gehört ins Interview. Nächster Schritt liegt beim Runner, nicht bei mir: `research.md` mit obigem Text füllen und den `research-handoff`-Gate weiterführen.
