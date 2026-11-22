---
title: "Plan — draft-known-red"
status: draft
implementation_status: none
date: 2026-11-22
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-83e
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, draft]
---

# Plan — draft-known-red

```text
For you:     A draft runs without Stage 2: draft <change> --stage2-off [REASON] drafts through Opus 5.5 at effort xhigh, and an exhausted Codex/GLM chain names that flag as the next step on a restored tree.
Done when:   The flag starts one Opus draft attempt with its reason in the audit line, a failed last attempt saves its ref and puts the tree back, the ADR 0016 addendum and four more maintainer answers stand in the pull request, and make verify passes.
Appetite:    4 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     An automatic fallback inside the chain, route changes for other verbs, and a Runner-route block in the drafted plan.
Pre-mortem:  suppose it failed: most likely because the failure tail restored a tree the next Stage-1 run still refuses.
Starts unless you say stop.
```

## Files and steps

1. `scripts/stage2.py` — accept and route the flag for the draft. In `_run`,
   `"draft"` joins the verb set of the `--stage2-off` check and the refusal
   message names "explore, draft, implement and repair"; the dispatch passes
   the flag through an own branch, `draft(Path(args.root), args.change,
   args.stage2_off)`, as implement's. `draft(root, change, stage2_off=None)`:
   the preflight takes `OPUS if stage2_off is not None else CODEX` (criterion
   3), and `routes = [(OPUS, "stage-1", stage2_off)]` when the flag is given —
   nothing else in the attempt loop changes: the GLM key read stays bound to
   the GLM endpoint, and the put-back, the document check, the time entry and
   the checkpoint keep running through the same code. The GLM-key `Refused`
   names the next step, `python3 scripts/stage2.py draft <change>
   --stage2-off <reason>`. The failure tail: when the last attempt fails its
   document check, `save_attempt(root, baseline, ctx.change,
   f"draft-attempt-{attempt}")` runs first, then `put_back(root, baseline,
   allowed)` with `allowed` the change's `findings.md` alone, the findings
   quote names the ref, and the final `CallFailed` names the ref and — exactly
   when `stage2_off is None` — the next-step command; a Stage-1 run's failure
   names the findings file and the ref, never the flag again. The module
   docstring's two `--stage2-off` sentences (the verb list and the line
   "`--stage2-off` to explore, implement and repair") and the argparse help
   name draft, the Stage-1 sentence naming each phase's model: Haiku 5.5 for
   explore, Sonnet 5.5 for implement and repair, Opus 5.5 at effort `xhigh`
   for the draft.
2. `docs/WORKFLOW.md` — two edits, made by the implement attempt (the file is
   not held). The `draft` bullet of "The runner is the only way" becomes:
   "`draft` — Codex, phases 2, 2b and 3 in one call; GLM 5.3 (`glm-5.3`)
   after two failed Codex attempts; `--stage2-off [REASON]` uses Opus 5.5 at
   effort `xhigh` ("The draft" below)." And the closing sentences of "The
   draft (phases 2, 2b and 3)", from "The chain is three attempts:" to the
   end of that paragraph, become: "The chain is three attempts: Codex, a
   second Codex attempt with the first one's diagnostics, then `glm-5.3` with
   both — a failed call is put back and moves along the same chain, a failed
   post-run check leaves its tree and its quoted block for the next attempt,
   and three failures exit 1: the last attempt's failed document check first
   saves the tree as an attempt ref and puts the worktree back, so the run
   that follows is not refused for pre-existing changes. The GLM key is read
   only when the GLM attempt is due, and its refusal names the next step. A
   run that fails after its last allowed attempt names `--stage2-off` as the
   next step; the chain never falls through to a Stage-1 model on its own. A
   draft takes `--stage2-off [REASON]` like the other writing verbs: the
   Stage-1 route drafts on Opus 5.5 at effort `xhigh` through
   `claude-code-plan` — the model §3 assigns phases 2, 2b and 3 — in one
   recorded attempt with the reason in its audit line; the by-hand Opus draft
   of §3 stays for a maintainer who drafts without the runner."
3. `tests/test_stage2.py` — re-point the standing refusal and write the
   ledger's tests. Drop `"draft"` from
   `test_stage2_off_is_only_for_work_verbs`'s parametrization (its planted
   fault) and add `"draft"` to
   `test_a_change_name_after_the_stage2_off_flag_is_named_as_eaten`. Write the
   new tests on `draft_world`, mirroring
   `test_stage2_off_implements_with_one_sonnet_attempt_and_records_reason`
   and the existing draft tests: the accepted Stage-1 draft (one `claude`
   call at `claude-opus-5-5` effort `xhigh`, `read_secret` monkeypatched to
   fail, audit line with `route stage-1` and the reason, one commit naming
   `route stage-1`, time entry with route and model, no `## Runner route`
   block in the plan), the Stage-1 preflight clearing `claude-code-plan` where
   `openai-codex` does not, the failed Stage-1 call (exit 1, no second call,
   the tree back at the baseline except `findings.md`, a planted partial
   `spec.md` gone with it, diagnostics and ref quoted), the red document
   check failing the Stage-1 attempt, the put-back of a planted outside path,
   the failed last document check (a `refs/stage2/attempts/…` ref saved, the
   tree restored, a following `draft --stage2-off` run not refused), the
   exhausted chain's final message and the GLM-key refusal naming the
   next-step command (a Stage-1 failure not naming it), and the doctrine test
   reading the module docstring, the argparse help and `docs/WORKFLOW.md`
   (criterion 12; `AGENTS.md` is held and belongs to step 4, so no test of
   this step reads it).
4. Orchestrator bootstrap edits — held paths, made by the orchestrating
   session after the accepted attempt and never told to a model attempt:
   - `docs/adr/0016-codex-drafts-and-opus-reviews-the-spec.md` — the header's
     `updated:` moves to `2026-11-22`, and this addendum is appended after
     the 2026-11-01 amendment note, closing the Decision section:

     > Amended 2026-11-22 (bead coding-harness-83e, maintainer answer B
     > recorded as Q-1 in `plans/changes/draft-known-red/decisions.md`):
     > decision 9 no longer holds as written — `draft` takes `--stage2-off
     > [REASON]` like the other writing verbs, and the Stage-1 draft runs on
     > Opus 5.5 at effort `xhigh` through `claude-code-plan`, the model §3
     > assigns phases 2, 2b and 3, in one recorded attempt; the by-hand Opus
     > draft of §3 stays for a maintainer who drafts without the runner. The
     > failure tail follows: a last attempt that fails its document check
     > saves its tree as an attempt ref and puts the worktree back, a run
     > that fails after its last allowed attempt — the GLM-key refusal on
     > the third route included — names `--stage2-off` as the next step, and
     > the chain itself never falls through to a Stage-1 model.
   - `AGENTS.md` — the `--stage2-off` sentence of the Stage-2 paragraph
     becomes: "`--stage2-off [REASON]` uses the phase's §3 model — Haiku 5.5
     for explore, Sonnet 5.5 for implement and repair, Opus 5.5 at effort
     `xhigh` for the draft — and records why when Stage 2 is off or Z.ai
     unavailable."

What is not touched: `run_attempts` and the implement and repair route lists
(their Stage-1 stays Sonnet 5.5 at effort `medium`); the draft's guards,
`draft_keep`, `put_back`, `document_gates` and `verify_draft`; `prompts/`,
`templates/`, `AGENTS.md`, `README.md`, `CLAUDE.md`, `decisions/`,
`docs/adr/`, `model-endpoints.yaml`, `provenance.yaml`, `.github/`,
`.claude/`, `.beads/` — the two held-path edits are step 4's, so no model
attempt is told to make them; and `plans/INDEX.md`, which the runner renders.

## Owed before the pull request goes green

The claimed ADR edit owes five counted maintainer-answered records in this
change's `decisions.md` whatever the class (`check_interview_minimums.py`;
Q-1 stands, four more are owed). The orchestrating session asks them with the
question protocol once the maintainer's window opens (2026-11-23 10:00); no
model writes an answer. Until then the pull request's `make verify` stays red
on exactly that gate, next to nothing else.

## Criterion ledger

- 1: not yet written tests/test_stage2.py::test_stage2_off_drafts_with_one_opus_attempt_and_records_reason — the run exits 2 with the old refusal, or no model call starts
- 1: tests/test_stage2.py::test_a_change_name_after_the_stage2_off_flag_is_named_as_eaten — a change name after the flag is taken as the draft's reason without the refusal
- 2: not yet written tests/test_stage2.py::test_stage2_off_drafts_with_one_opus_attempt_and_records_reason — a Codex or GLM call starts, the GLM key is read, or the model or effort differs
- 3: not yet written tests/test_stage2.py::test_a_stage_one_draft_preflights_the_opus_declaration — the Stage-1 draft exits 2 on the openai-codex declaration
- 4: not yet written tests/test_stage2.py::test_stage2_off_drafts_with_one_opus_attempt_and_records_reason — the audit line lacks route stage-1 or the given reason
- 5: not yet written tests/test_stage2.py::test_a_failed_stage_one_draft_call_stops_without_fallback — a retry runs, the exit is 0, a path other than findings.md stays changed, or the diagnostics or ref are missing
- 6: not yet written tests/test_stage2.py::test_a_red_document_check_fails_a_stage_one_draft_attempt — a red check exits 0 or hides its problems
- 7: not yet written tests/test_stage2.py::test_a_stage_one_draft_puts_back_paths_outside_the_change_folder — an outside path stays changed or reaches the commit
- 8: not yet written tests/test_stage2.py::test_stage2_off_drafts_with_one_opus_attempt_and_records_reason — the commit message or time entry names another route or model, or a second commit appears
- 9: not yet written tests/test_stage2.py::test_a_failed_last_draft_check_saves_a_ref_and_restores_the_tree — the tree is left with no saved ref, or the next draft --stage2-off run is refused for pre-existing changes
- 10: not yet written tests/test_stage2.py::test_an_exhausted_draft_chain_names_stage2_off_as_the_next_step — the chain's final message or the GLM-key refusal names no next step, or a Stage-1 failure names one
- 11: tests/test_stage2.py::test_stage2_off_is_only_for_work_verbs — a verb outside explore, draft, implement and repair accepts the flag
- 12: not yet written tests/test_stage2.py::test_the_runner_texts_name_draft_among_the_stage2_off_verbs — a text still excludes draft, names another Stage-1 model for it, or keeps the old refusal sentence
- 13: not a test — the two held-text edits (the ADR 0016 addendum, the AGENTS.md sentence) are the orchestrator's bootstrap edits from step 4's verbatim text; the phase-6 review reads them against the criterion

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py -k 'stage2_off or draft'
make verify
```

## Runner route — 2026-11-22

Stage-1 route: explore · model claude-haiku-5-5 · reason: research swarm
refuses: its state store must lie outside the home directory (XDG_STATE_HOME),
not set up for this night run (`research.md`, 2026-11-22).

## Time used

2026-11-22 15:30:11–15:42:22 UTC, 730 s — draft · attempt 3 · route glm · model glm-5.3 · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-22 21:27:14–21:39:13 UTC, 719 s — draft · attempt 3 · route glm · model glm-5.3 · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
