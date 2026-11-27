---
title: "Research — ladder-next-step"
status: draft
implementation_status: none
date: 2026-11-20
last_reviewed: 2026-11-20
updated: 2026-11-20
supersedes: null
superseded_by: null
bead: coding-harness-hwll
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-20", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# ladder next step — Research

Stage-2 call, 2026-11-20: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1145 files, 4907 commits, 12 rules.

## Runner exploration — 2026-11-20

Research complete. Below is the append-ready text for `plans/changes/ladder-next-step/research.md`, followed by the neighbour list for the runner's header.

---

## What exists today

**The requirement is already decided — it is recorded, not proposed.** `AGENTS.md:180-185` carries the house rule "An exhausted review ladder goes to phase 6" (maintainer, 2026-11-20): when `review-loop` refuses because every stage of its run is consumed and the last round was not clean, and every taken row of that round is repaired, the lane goes to the phase-6 review instead of a new loop run, and phase 6 checks that last repair; the stated reason is that a run's history cannot be reset and asking each time stopped lanes overnight. The same decision appears twice in the handover `docs/journal/handover/2026-11-20-night-run-2026-11-19-b.md`: the maintainer confirmed on 2026-11-19 that lane L1 goes to phase 6 after its consumed ladder ("das passt"), and "No loop round cap. When a run's ladder is consumed, the lane goes to phase 6 (confirmed for L1)" under "Decisions and preferences". The same handover records a second, provisional instance: findings-per-model (bead coding-harness-qut1) went to phase 6 "after the consumed ladder (round 10 repaired), phase 6 instead of a new loop run, by analogy to the confirmed L1 decision" — done in conversation, with no runner support. The change's own bead is coding-harness-hwll (`plans/changes/ladder-next-step/research.md` frontmatter; `plans/INDEX.md:620` lists the change as `draft`, implementation status `none`).

**What the runner does today when the ladder is spent.** `review_loop` (`scripts/stage2.py:10867`) raises, in order: undecided-rows refusals (`scripts/stage2.py:10883`, `:10910`), a clean-round `CleanStop` (`:10913-10914`), the repair brake for two consecutive `fix-r`-only rounds (`:10915-10924`), and then, inside the round loop, the spent-stages refusal — `next_stage(state)` returning `None` raises `Refused` with *"every stage of this run is consumed and the last round was not clean; the loop stops and reports to the maintainer. No model is substituted."* (`scripts/stage2.py:10959-10986`), with a variant message when the declaration names paid models but the snapshot holds no admissible one (`:10974-10985`). Two facts about this path matter for the rule's precondition:

- **The refusal does not distinguish repair states.** The spent-stages check (`:10959`) fires *before* the unrepaired-taken-rows check (`:10990-10997`, comment at `:10987-10989`: "Spent stages stop first"), so the same message covers "taken rows still unrepaired" and "every taken row repaired" — an orchestrator cannot read the rule's precondition ("every taken row of that round is repaired") off today's refusal text.
- **Exit codes:** `Refused` → 2, `CleanStop` → `CLEAN_CODE = 3` (`scripts/stage2.py:285`, `:11632-11642`), `CallFailed` → 1 (`:11643-11647`). A clean finish and a refusal are distinguishable; two kinds of refusal are not.

**Row-state semantics the precondition builds on.** `undecided_refusal` (`scripts/stage2.py:4092`) treats a `fixed` row whose `Broke a test` mark is missing as still waiting; `clean_round` (`:4266`) keeps a round with a `fixed` row not clean (criterion 11); the unrepaired check reads the `Status` cell (row index 7) for a `taken` prefix (`:10990-10992`). So "every taken row of that round is repaired" is today expressible as: the last round has no `taken`-prefixed status, and `undecided_refusal` (which also demands the `Broke a test` marks) is empty — both are computed by `review_loop` on every call already.

**Persistence and the contrast case.** Consumed stages and stops survive a release and an edited configuration (ADR 0021 decision 9, `docs/adr/0021-review-swarms-until-clean.md`; test `test_round_history_survives_split_releases_and_config_edits`, `tests/test_stage2.py:10110`, spent-snapshot assertion at `:10147-10148`), and availability preparation refuses a spent run ("Existing or released runs cannot be prepared again", ADR 0021 Q-16 amendment; `prompts/04b-review-loop.md:68-69`). The only mechanism that ever produces a fresh run from a stopped one is the maintainer-only restart, `release-loop --restart --reason` (`RESTART_LINE` at `scripts/stage2.py:452`, `release_loop` at `:4741`, `docs/WORKFLOW.md:1309-1313`, ADR 0021 restart amendment) — the rule this change implements is the alternative to asking for that restart.

**Phase 6 today.** `review` (`scripts/stage2.py:3812`) refuses undecided loop rows (`:3822-3825`) and requires a fresh full `make verify` before the reviewer is called (`require_fresh_full_verification`, `:3746`, called at `:3843`); the verdict is written before any loop row is read, then `release` brings the rows in and Codex marks each `agree`/`disagree` (`:3876-3887`; `prompts/06-review.md:33-47`). **Not found** in `review()` as read (`scripts/stage2.py:3812-3887`): any explicit gate that the loop actually finished — there is no check for a clean stop or a spent run; the only loop-state refusals are the undecided-rows and origin checks. "Phase 6 checks that last repair" has today no dedicated mechanism; what exists is the phase-4b gate "the repair's targeted check green after each repair … and one full `make verify` on the final head before phase 6" (`prompts/04b-review-loop.md:30-32`) plus the reviewer reading the whole diff.

**Doctrine texts carrying today's behavior** (each names the spent ladder as a stop "for the maintainer"):
- `prompts/04b-review-loop.md:20-23`: "a spent ladder stops the loop for the maintainer — no model is substituted for a spent ladder's last rung".
- `docs/WORKFLOW.md:1709-1710` (§4): "When every stage of a run is consumed and the last round was not clean, the loop stops and reports to the maintainer — no model is substituted."
- `docs/WORKFLOW.md:89` (phase-4b table row) and `docs/WORKFLOW.md:1297-1303` (`review-loop` verb, exit codes 0/2/3, R-11).
- `prompts/06-review.md:35-39` describes the loop as "runs until a round is clean … free-model swarm, a Flash swarm, then the paid ladder" with no spent-ladder sentence.

**Tests pinning today's behavior** (all in `tests/test_stage2.py`, asserting the exact refusal strings): `test_the_loop_stops_at_three_rounds` (`:8923`, assertions `:8934-8938`, also after release), `test_the_loop_stops_when_the_ladder_ends` (`:9669`, solo rung, assertions `:9684-9688`), `test_round_history_survives_split_releases_and_config_edits` (`:10110`, spent-snapshot assertion `:10147-10148`), `test_a_failed_flash_member_is_replaced_by_the_cheapest_unconsumed_rung` (`:21582`, consumed-replacement and spent assertions `:21604-21609`).

**Nothing implements the rule yet.** A search of `scripts/` for `consumed|exhausted|ladder` found no path that steers a spent run to phase 6; the only "exhausted" hits are unrelated (`scripts/close_merged_beads.py:371` startup budget, `scripts/research_capture.py:221` `script_exhausted`). This is "not there", checked in this worktree at commit `8cfb9de8`.

## Where it lives

- Runner: `scripts/stage2.py` — `review_loop` (`:10867`, refusal block `:10959-10986`, unrepaired check `:10987-10997`), row predicates `undecided_refusal` (`:4092`), `clean_round` (`:4266`), exits (`:11632-11647`), restart contrast `release_loop` (`:4741`).
- Prompt texts: `prompts/04b-review-loop.md` (whole file read; spent-ladder sentence `:20-23`, gate `:30-32`), `prompts/06-review.md` (whole file read; verdict-first block `:33-47`).
- Doctrine: `docs/WORKFLOW.md` (`:89`, `:1297-1313`, `:1331-1335`, `:1668-1716`).
- Decision record: `AGENTS.md:180-185`; `docs/journal/handover/2026-11-20-night-run-2026-11-19-b.md` ("Needed from the maintainer" item 1 row findings-per-model, "Decisions and preferences"); ADR `docs/adr/0021-review-swarms-until-clean.md` (decisions 1, 7, 8, 9, Q-16 amendment, restart amendment).
- Tests: `tests/test_stage2.py` (four functions named above).

## What is unclear about it

- The bead coding-harness-hwll's own description was **not read** — the tracker is the Dolt database under `.beads/` and this phase has file-read tools only; the scope statement beyond the AGENTS.md rule (title, class, appetite) is an open question for the interview.
- **Not found anywhere**: a statement of *how* the orchestrator is told "the ladder is spent and repaired — go to phase 6" — whether the runner should say it (a distinct message or exit) or the doctrine alone should instruct the orchestrator. No artifact decides this; it is a `[DECISION]`-class question.
- Whether the maintainer has confirmed the findings-per-model provisional decision (handover item 1, still "provisional agent decision, autonomous run 2026-11-19" as of that handover's 07:15 cut-off) — not readable from this worktree.
- Whether parallel lanes touch the same lines: mandatory-spec-review's plan step 3 edits `docs/WORKFLOW.md` and `AGENTS.md` line 20 (handover addendum, 2026-11-20 09:20) — those branches were **not read** (they live in other worktrees); merge-conflict exposure of the lines named above is unmeasured.
- The exact reading of "phase 6 checks that last repair" — whether it means only the existing pre-phase-6 full `make verify` plus the reviewer's whole-diff read, or an additional explicit check, is stated nowhere; open for the interview.

## Which files a change would have to touch

`scripts/stage2.py` (the spent-stages block and its exits, `review_loop`); `tests/test_stage2.py` (the four tests above assert today's strings and would stand beside new ones); `prompts/04b-review-loop.md` (spent-ladder sentence and gate line); `prompts/06-review.md` (only if the phase-6 text must carry the rule); `docs/WORKFLOW.md` (the four locations named). `AGENTS.md` already carries the decision text (`:180-185`) and is the maintainer's file — the handover's AGENTS.md proposal precedent (item 3) shows it is changed only by proposal, not by a lane.

---

**Neighbours (for the `neighbours:` header):**

- `plans/changes/review-loop-deep-a/spec.md` — active, class `bounded`; the DL-A control/state rows its spec defines are cited inside `review_loop`'s comments (DL-A-2, DL-A-8) and shaped the stop order this change touches
- `plans/changes/loop-structure-first/research.md` — active draft research on the same verb's round prompt
- `plans/changes/slip-counter/spec.md` — active; loop-record validity rules, same record mechanics
- `plans/changes/verify-cheap-before-admission/spec.md` — merged (#416); the availability/preparation path adjacent to the spent-run refusal
- `plans/changes/archive/2026-11-06-loop-until-clean/` — ADR 0021's originating change (spec, research, design, decisions)
- `plans/changes/archive/2026-11-06-review-loop-deep-b/spec.md` — the deep review's part B on the same loop
- `docs/adr/0021-review-swarms-until-clean.md`, `docs/adr/0017-codex-repairs-taken-findings.md`, `docs/adr/0025-targeted-check-after-repair.md`, `docs/adr/0011-stage-2-reviews-through-opencode-go.md`, `docs/adr/0023-guard-proof-for-test-only-repairs.md`
- `docs/journal/handover/2026-11-20-night-run-2026-11-19-b.md` — the requirement's source record (not a spec, but the rule's provenance)
