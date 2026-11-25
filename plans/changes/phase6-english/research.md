---
title: "Research — phase6-english"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-tscc
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-22", model: "glm-5.3-flash"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# phase6 english — Research

Stage-2 call, 2026-11-22: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1167 files, 5311 commits, 12 rules.

## Runner exploration — 2026-11-22

Research complete. Here is the phase-1 research for `phase6-english`, prose ready to append to `plans/changes/phase6-english/research.md`.

---

## What exists today

The maintainer decided on 2026-11-20 how to stop the phase-6 reviewer from writing German: "phase-6 reviewer language: prompt asks for English and the runner re-asks once (bead coding-harness-tscc)", recorded in `docs/journal/handover/2026-11-20-day-run.md` ("Decisions and preferences", bullet 1). The observation that prompted it stands in the same file under what went wrong: "The Codex phase-6 reviewer wrote German verdicts three times (bead coding-harness-tscc)".

**Where German reviewer output stands today (evidence in the tree).** The phase-6 reviewer's words reach `findings.md` two ways — the six-cell finding rows of the verdict table, and the `Phase 6` cells it marks into released loop rows afterwards. Both carry German:

- `plans/changes/loop-record-other-worktree/findings.md` — finding row `F6-2` has a German Finding cell ("Wenn ein dritter Worktree … verweigern."), standing directly above the verdict line `Phase 6 verdict: codex 01a1f913-538d-73d0-b9bc-9248e7c65a52, 2026-11-20`; the released loop rows below it (`L1-1` through `L9-3`) carry German `Phase 6` mark cells throughout, of the form `disagree — Die Prüfung verlangt, …`.
- `plans/changes/slip-counter/findings.md` — German finding text inside the block `## Phase 6 — Codex, 2026-11-17` (the passage "…geprüfter Baum sich während des Laufs ändert, wird als vollständig behandelt…") and again inside `## Phase 6 — Codex, 2026-11-20` (the passage "…behandelt der Leser sie trotzdem als gültig…").
- The same mechanism is old: German `Phase 6` mark cells stand in archived findings too — `plans/changes/archive/2026-11-06-draft-gates-only/findings.md` (rows inside `## Phase 4b — loop rows, released 2026-10-31`), `plans/changes/archive/2026-11-06-swarm-time-limits/findings.md`, and `plans/changes/archive/2026-11-16-research-free-paid/findings.md`.

**The rule the change would enforce.** `AGENTS.md` house rule 1: the repository is English — documents included; German belongs only to the conversation with the maintainer and to the run-time display texts of `tools/claude-code/`. German still in `scripts/`, `tests/`, `docs/governance/` is translated in pull requests of its own (bead coding-harness-yim), never in passing.

**Where the phase-6 prompts are assembled.** `review()` in `scripts/stage2.py` makes two Codex calls, and neither prompt says anything about language:

1. The verdict call: `phase_prompt(root, "06-review.md", …)` (`scripts/stage2.py`, function `phase_prompt`) joins the prompt file `prompts/06-review.md`, "Write only your verdict now.", `PHASE6_GUARD_INSTRUCTION`, `PHASE6_ANSWER_FORMAT` (derived from `ANSWER_FORMAT`), and `READ_REQUEST` — none of these strings mentions English or German (I read `prompts/06-review.md` whole; the language ask is *not there*, not merely not found). `phase_prompt` does not append `AGENTS.md` — that is what `work_prompt` does for work phases — so the reviewer never sees house rule 1. The loop prompt states this constraint itself: `prompts/04b-review-loop.md`, section "For the reviewer": "You may not read `AGENTS.md`, so the rules you need are here: - Every row is in English." The phase-6 prompt has no such block; that line in the loop prompt is the direct precedent for the wording.
2. The marks call (`scripts/stage2.py`, `review()`, after `release`): its prompt is built inline from `MARK_FORMAT` + "Your verdict stands and is not changed." + the loop-row listing + `READ_REQUEST`, resumed on the verdict thread (`resume=thread`). No language instruction; the German mark cells above are this call's output.

**The re-ask precedent.** The review loop already re-asks once: `ask_malformed_again` (`scripts/stage2.py`, inside the loop round) retries a member whose answer is a `MalformedAnswer`, with `FORMAT_REMINDER` ("Your previous answer was not in the required format … answer once more.", bead coding-harness-70rw), and the retry is audited and under the round's one deadline. `docs/WORKFLOW.md` §4 documents it: "A member whose answer is malformed — no six-cell row and not exactly `No finding.` — is asked once more with the format reminder … a second malformed answer fails the member as today." Phase 6 has the malformed-answer path but no re-ask: on a malformed verdict `review()` appends a rejected block (`rejected_review_block`) and raises `CallFailed`; its docstring notes "a malformed verdict is out of scope" for the retry machinery.

**What the format check already does with German.** `review()` accepts only six-cell rows or exactly `No finding.` as the verdict: a fully German no-finding verdict is rejected today as malformed, while German table rows parse fine because `parse_rows` is language-agnostic. So the current check rejects one German form and passes the other.

**A boundary to keep clear.** The runner's own gate verdict line is German on purpose: `VERDICT_RED = "RED (block) — der Lauf ist rot."` (`scripts/verify_run.py`), and quoted copies of it stand inside findings attempt records (for example `plans/changes/verify-cheap-before-admission/findings.md`, a quoted `── [pytest] RED (block) — der Lauf ist rot.` line). These are maintainer display texts, not reviewer words; they belong to the translation epic (bead coding-harness-yim), not to this change. Unrelated but confusable: `tests/test_stage2_swarm.py` has a criterion about "the allowed German examples or separators are refused" — that is the swarm report format, a different German topic.

**Tests that pin the surfaces a change would move.** `tests/test_stage2.py`: `test_the_review_prompt_and_the_runner_ask_for_the_same_cells` pins cell agreement between `ANSWER_FORMAT` and the three review prompts; `test_the_review_prompts_give_both_paths` with the helper `review_prompt_problems` pins exact strings of `prompts/06-review.md` (verb name, verdict line, verdict-before-loop-rows, model line); the two-call shape of `review()` is pinned by `test_codex_marks_each_loop_row_after_its_verdict`, `test_a_failed_mark_call_leaves_the_marks_empty`, `test_no_loop_row_reaches_the_verdict_call`, `test_the_loop_marks_after_a_recheck_resume_the_fresh_verdict_thread`; the resume semantics by `test_review_resumes_the_recorded_session` and `test_the_first_phase6_review_still_resumes_the_recorded_2a_session`. A runner-logic change owes a guard test that plants a real fault under `STAGE2_PLANT_FAULT` (ADR 0023; the instruction the phase-6 reviewer enforces is `PHASE6_GUARD_INSTRUCTION` in `scripts/stage2.py`).

## Where it lives

- `prompts/06-review.md` — the phase-6 prompt (no language ask).
- `prompts/04b-review-loop.md` "For the reviewer" — the "Every row is in English." precedent.
- `scripts/stage2.py` — `review()` (both calls), `phase_prompt`, `ANSWER_FORMAT`/`PHASE6_ANSWER_FORMAT`/`MARK_FORMAT`/`FORMAT_REMINDER`/`READ_REQUEST`, `parse_rows`, `split_guard_evidence`, `rejected_review_block`, and the loop's `ask_malformed_again`.
- `docs/WORKFLOW.md` §4 — the phase-6 verdict passage (reviewer writes the table, then the verdict line, then marks the rows) and the loop's documented re-ask.
- `docs/journal/handover/2026-11-20-day-run.md` — the decision and the observation this change carries out.
- `tests/test_stage2.py` — the pinned prompt and review-flow tests named above.
- Evidence files: `plans/changes/loop-record-other-worktree/findings.md`, `plans/changes/slip-counter/findings.md`, and the archived findings named above.

## What is unclear about it

- **Detection.** No language detection exists anywhere in `scripts/` — not found (I searched `scripts/` and `tests/` for English/German/language markers; the only hits are unrelated, like git's `LC_ALL=C` diagnostics). The loop's re-ask triggers on a structural check (`MalformedAnswer`); a language check needs its own deterministic rule, and its scope (verdict rows only, or mark reasons too) is undecided.
- **"Re-asks once" — applied to which call?** German came from both phase-6 calls (verdict table and marks); the decision sentence does not split them, and does not say whether "once" is per call or per `review` run.
- **What happens after a still-German second answer.** The loop precedent fails the member ("a second malformed answer fails the member as today", `docs/WORKFLOW.md` §4); whether phase 6 fails the call or accepts is unstated.
- **Scope across phases.** The decision names the phase-6 reviewer only. The 2a prompt (`prompts/02a-spec-review.md`) likewise has no language ask — that is *not there* (I checked for AGENTS/English/rules wording); whether the change extends to 2a is undeclared.
- **Committed history.** Whether the German texts already committed in `loop-record-other-worktree`, `slip-counter` and the archives are repaired by this change or left as historical evidence is undeclared.
- **Bead detail.** The bead `coding-harness-tscc`'s own description and class were not read in this phase — reading the tracker goes through `tools/bd` (house rules 2–3), and this explorer runs no commands; the change folder's frontmatter names the bead.
- **Where the ask lives.** Prompt file, runner-side instruction, or both — the pinned prompt-agreement test (`test_the_review_prompt_and_the_runner_ask_for_the_same_cells`) requires whatever the runner appends last to be consistent with the prompt file; the split is a design question.

## Which files a change would have to touch

- `prompts/06-review.md` — the English ask in reviewer-facing rules (precedent wording in `prompts/04b-review-loop.md`).
- `scripts/stage2.py` — `PHASE6_ANSWER_FORMAT` and/or `MARK_FORMAT`/the inline marks prompt in `review()`; the once-only re-ask in `review()`, modeled on the loop's `FORMAT_REMINDER` mechanism; a language-check helper beside the verdict parsing (`parse_rows`, `split_guard_evidence`).
- `docs/WORKFLOW.md` §4 — the phase-6 passage (verdict, then marks) plus a sentence documenting the language ask and the one re-ask, beside the documented loop re-ask.
- `tests/test_stage2.py` — tests for the check and the re-ask, updates to the pinned prompt strings (`review_prompt_problems`), and a `STAGE2_PLANT_FAULT` guard test for the runner logic (ADR 0023).
- Not to touch for this change: `scripts/verify_run.py`'s `VERDICT_RED` and other runner display texts (translation epic, bead coding-harness-yim); `plans/INDEX.md` is regenerated, not written by hand (`pr_sync.py` regenerates it, per `prompts/06-review.md` "Base").

Neighbours I already know: `plans/changes/loop-record-other-worktree/` (active; its findings hold the German phase-6 cells), `plans/changes/slip-counter/` (active; same), `plans/changes/verify-cheap-before-admission/` (active; shows the runner's quoted German gate line), `plans/changes/archive/2026-11-06-malformed-answer-retry/` (the `FORMAT_REMINDER` re-ask, bead coding-harness-70rw), `plans/changes/archive/2026-11-06-review-verdict-validated/` (the verdict validation), `plans/changes/archive/2026-11-06-draft-gates-only/` (archived German marks). The living spec `plans/specs/implementation-verification/spec.md` was not read and shows no known tie to reviewer language.
