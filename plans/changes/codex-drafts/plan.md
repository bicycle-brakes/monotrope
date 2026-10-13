---
title: "Plan — codex-drafts"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-rhq
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, codex, draft, spec-review]
---

# Plan — `codex-drafts`

```text
For you:     One command, `python3 scripts/stage2.py draft <change>`, has Codex write spec, design and plan (GLM 5.3 if Codex fails twice); `spec-review` runs on Opus 5.5 instead of Codex, and you still see every plan card unchanged.
Done when:   The 37 criteria hold, each by the test the ledger names, and `make verify` is green once your answer to the ADR question is recorded.
Appetite:    8 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     phase 6 off Codex, a Stage-1 route inside `draft`, retiring the spec-planner agent, time limits on calls, confining what Codex reads.
Pre-mortem:  suppose it failed: most likely because the unmerged stage2-repair change rewrites implement's attempt loop and the same tests in scripts/stage2.py and tests/test_stage2.py, and the two drafts collide.
Starts unless you say stop.
```

Implements [`spec.md`](spec.md), criteria 1–37 (class `feature`, appetite
8 h), shaped by [`design.md`](design.md). Facts read at `02bf4b3`, the
branch's merge base with `origin/main`. Phase 1 explored on route `flash`
(GLM 5.3 Flash), so no Stage-1 fallback is carried forward.

## Decided in phase 3

No `[DECISION]` is open. The spec's `[DETAIL]`s stand; these are the plan's:

- `[DETAIL]` **`checkpoint` gains `message: str | None = None`, in exactly the
  form of the open change stage2-repair**, and `GLM` is that change's
  constant `("glm-coding-plan", "glm-5.3", "max")`: identical lines merge
  without a conflict, whichever change lands first.
- `[DETAIL]` **The draft loop is its own function, not `implement`'s loop
  with options.** A failed call moves on here and stops there, and
  stage2-repair rewrites `implement` into a shared loop; a separate loop
  touches neither.
- `[DETAIL]` **The phase-6 resume reads the last phase-2a block.** `review`
  resumes only when the last `## Phase 2a` block is Codex's and holds a
  `Reviewer session: codex` line; with no line, or after an Opus block, it
  starts fresh and says so (criteria 30, 31). A change reviewed before this
  one keeps its resume.
- `[DETAIL]` **A moved `HEAD` is tested with a monkeypatched `run_codex`**
  that commits; the shared stand-in template stays unchanged.

## Steps

1. **`scripts/stage2.py`** (about 220 lines).
   - Constants: `OPUS = ("claude-code-plan", "claude-opus-5-5", "xhigh")`;
     `GLM` as above; `NEW_ADR = re.compile(r"docs/adr/\d{4}-[a-z0-9][a-z0-9-]*\.md")`;
     `CARD_LABELS = ("For you:", "Done when:", "Appetite:", "Not now:", "Pre-mortem:")`;
     `DRAFT_PROMPTS = ("02-spec.md", "02b-design.md", "03-plan.md")`;
     `DRAFT_RULES`, the text under "The drafting rules" below.
   - `run_codex(ctx, prompt, resume=None, writable=False)`: the one change is
     `sandbox_mode="workspace-write"` when `writable`, else `"read-only"`.
   - `begin_call`: the producer is `codex` for `openai-codex`, `claude-code`
     for `claude-code-plan`, `pi` otherwise (criterion 29).
   - `spec_review`: `preflight(root, change, OPUS)`, the same
     `phase_prompt`, `begin_call(ctx, "spec-review", OPUS, prompt)`,
     `run_work_model(ctx, prompt, OPUS, writable=False)`, then
     `append` of `## Phase 2a — Opus 5.5, <date>` with
     `answer_block(rows, answer, "Opus")` and no session line.
   - `checkpoint`: the `message` parameter, used as
     `message or f"feat({change}): implement accepted plan"`.
   - `draft_prompt(ctx, diagnostics)`: `work_prompt(root, "02-spec.md",
     change, extra)`, where `extra` is `## Phase 2b prompt` with
     `02b-design.md` in full, `## Phase 3 prompt` with `03-plan.md` in full,
     `DRAFT_RULES` with `<change>` filled in, and — when there are any —
     `## Earlier attempts' diagnostics` with them joined.
   - `put_back(root, baseline, keep) -> list[str]`: the sorted posix paths of
     `changed_paths(root) - keep`; when any, the same `git restore
     --source=<baseline> --staged --worktree -- . :(exclude)…` and `git clean
     -fdq -- . :(exclude)…` as `restore_baseline`, a `Refused` from git turned
     into `CallFailed`. `restore_baseline` stays as it is.
   - `draft_keep(root, ctx, baseline) -> tuple[set[Path], list[str]]`: every
     changed path under the change folder except its `decisions.md`, plus
     every changed path that `NEW_ADR` fully matches and
     `git cat-file -e <base>:<path>` does not find, `<base>` being
     `git merge-base <baseline> origin/main` (so a second draft may edit the
     ADR the first one committed); the second value is those ADR paths.
   - `red_gates(output) -> dict[str, list[str]]`: the gate id and body lines
     of each section `verify_all.sh` framed `RED (block)`, read with the frame
     logic of `red_sections` (`_frame_lines`, `GATE_START`, `GATE_END`), which
     stays as it is.
   - `only_answer_owed(output, change) -> bool`: `red_gates` has exactly the
     key `adr-answers`, and its body has at least one non-blank line and every
     non-blank line begins `adr-answers: <change>: no answer — `.
   - `card_problem(text) -> str | None`: below the header, before the first
     line starting `## `, the first fenced block must hold lines beginning
     with the five `CARD_LABELS` in that order; otherwise "`plan.md` does not
     open with the plan card (For you:, Done when:, Appetite:, Not now:,
     Pre-mortem:)".
   - `verify_draft(root, ctx, key, new_adrs) -> tuple[list[str], bool]`: the
     problems and whether the answer is owed. More than one new ADR file is a
     problem naming them; `prepare_derived` with `verify_attempt`'s
     environment, its problems returned as they are; `make verify`, whose red
     run is a problem with `verify_attempt`'s evidence (moved into a helper
     `verify_evidence(done, key)` that both call) unless `only_answer_owed`
     holds; a missing `spec.md` or `plan.md`; `card_problem`; a `plan.md`
     without `TIME_HEADING`.
   - `draft(root, change)`: `preflight(root, change, CODEX,
     bead_file="research.md", required=("decisions.md",))`; refuse changes
     outside `findings.md` with `implement`'s message; `baseline`,
     `ignored_snapshot`. Routes: `(CODEX, "codex", None)`, `(CODEX,
     "codex-repair", "the first draft attempt failed")`, `(GLM, "glm", "two
     Codex draft attempts failed")`. Per attempt: on the GLM route read
     `GLM_KEY` or raise `Refused` naming the secrets file; `draft_prompt`;
     `begin_work_call(…, "draft", …)`; the `worktree_tree` snapshot as in
     `implement`; the call (`run_codex(…, writable=True)` or
     `run_work_model(…, GLM, writable=True, key=key)`); then, in this order:
     - `HEAD` against the baseline — moved raises `CallFailed("the draft call
       moved HEAD from <a> to <b>; nothing was put back or committed")`, also
       after a failed call;
     - a failed call: `put_back(root, baseline, {findings})`, the
       diagnostic `- the call failed: <error>`, and a quoted block
       `Attempt <n> (<route>) failed its call: <error>` with the paths put
       back; next route;
     - with the key, `remove_changed_credential` as in `implement`;
     - the second snapshot and `attempt_files`;
     - `draft_keep` and `put_back`; when it put back paths, a quoted block
       `Attempt <n> (<route>): the runner put back what a draft may not
       change:` and one list line per path, the path in backticks, at most
       `ATTEMPT_FILES` lines;
     - `verify_draft`; problems become the diagnostics and the quoted
       `attempt_block`, exactly as in `implement`; the key scan again;
     - no problems: when the answer is owed, `append` the line ``ADR answer
       owed: `make verify` was red only because
       decisions/answers/<change>/adr.yaml does not exist; the answer is the
       maintainer's (python3 scripts/harness.py decide adr).``; then
       `checkpoint(…, message=f"docs({change}): draft spec and plan — route
       {route}")` and return.
     After the third: `CallFailed("the draft failed after the allowed
     attempts; why each attempt failed: <findings>")`.
   - `VERBS` gains `"draft": draft`. The module docstring: the usage lines
     gain `draft <change>   # Codex, phases 2, 2b and 3; GLM 5.3 after two
     failed attempts` and `spec-review` reads `# Opus 5.5, phase 2a`; its
     prose says Codex drafts and reviews the change (6), Opus 5.5 reviews the
     spec (2a), and that the Codex review calls run read-only while a draft's
     Codex runs in `workspace-write`, the runner putting back what lands
     outside the change folder.
2. **`tests/test_stage2.py`**. The new tests the ledger names, in a section
   after the implement tests, on a helper `draft_world(world)` that removes
   the world's `spec.md` and `plan.md`, writes `decisions.md` with a bead
   and commits. A passing Codex step plants `spec.md`, a `plan.md` with the
   card and `## Time used`, and nothing else; `make` answers `green`. The
   ~20 tests that run `spec-review` against the `codex` stand-in move to a
   `claude` step; those that need a Codex 2a session (`full_flow`, the
   resume and fresh-session tests, the Codex pin) seed the line
   `Reviewer session: codex T1` in `findings.md` instead.
   `test_the_spec_review_answer_lands_as_codex_rows_with_its_session` is
   replaced by the criterion-28 test. `REVIEW_VERBS` and the
   `--stage2-off` parametrization gain `draft`. `STAGE2_ROUTING` gains `2
   Spec`, `2b Design` and `3 Plan` on `gpt-6.1-sol` and puts `2a Spec
   review` on `Opus 5.5`; `routing_problems` asks that row for effort
   `xhigh`; `class_table_problems` asks `Opus 5.5` in the 2a cells and
   `Codex, a fresh session` in the phase-6 cells;
   `review_prompt_problems` and `agents_md_problems` gain the needles of
   criteria 34 and 35; the planted replacements of
   `test_workflow_section_4_routes_the_three_reviews` follow the new rows.
3. **`tests/test_model_endpoints.py`**. `_remark_problems` asks the
   `openai-codex` remark for "Used for drafting spec, design and plan" and
   "the spec review (phase 2a) moved to Opus 5.5", and the new test of
   criterion 36.
4. **`docs/WORKFLOW.md`**.
   - §3 table: rows 2, 2b and 3 end "; where the runner drafts (§4), Codex
     writes it"; row 2a ends "; where the runner starts it (§4), a headless
     Claude Code call"; row 6 keeps "goes to Codex (§4)". The paragraphs
     "No Fable", "Spec and plan on Opus 5.5", "Spec review and review on Opus
     5.5" and "One reviewer for both" say: drafting leaves the table where
     the runner drafts; 2a is Opus 5.5 for every change since ADR 0016; one
     reviewer for both holds for a spike only, and a routed change's phase 6
     is a fresh Codex session that first checks that each 2a row arrived.
   - §4: the opening paragraph names Codex as drafter (2, 2b, 3) and phase-6
     reviewer and Opus 5.5 as spec reviewer, and "Phases 1a, 2a and 7 stay
     with Anthropic"; the class table's 2a cells read `Opus 5.5, where one is
     held` (bounded) and `Opus 5.5`, its phase-6 cells `Codex, a fresh
     session`; the sentence under it says explore, the draft and implement
     are not routed by class; "The routing" gains the rows `| 2 Spec |
     **gpt-6.1-sol** |`, `| 2b Design | **gpt-6.1-sol** |`, `| 3 Plan |
     **gpt-6.1-sol** |` (effort `max`, through the Codex CLI and `draft`, one
     call; `glm-5.3` after two failed attempts) and `| 2a Spec review |
     **Opus 5.5** |` (effort `xhigh`, Claude Code and `spec-review`,
     read-only tools), and row 6 says "a fresh Codex session"; "Eight verbs
     exist" becomes nine, with `draft` and the new `spec-review` and `review`
     bullets; the sentence "The runner starts Codex …" says read-only for a
     review and `workspace-write` for a draft, and keeps both
     "The runner starts Codex" and no "Codex also runs in the read-only
     sandbox" (`configured_not_measured_problems`).
   - §4 gains `### The draft (phases 2, 2b and 3)` before "The interactive
     session": the verb, the guards, the one tolerated gate, the chain, then
     the five steps of criterion 33 as a numbered list, then what the runner
     cannot see (Codex's reads and its unverified sandbox).
5. **`AGENTS.md`**, the stage-2 paragraph, in place: "ADR 0007 as amended by
   ADR 0011 and ADR 0016"; "Codex drafts spec, design and plan (`draft
   <change>`; GLM 5.3 after two failed attempts) and reviews 6; Opus 5.5
   reviews 2a (`spec-review <change>`)" in place of "Codex reviews 2a and 6";
   `draft <change>` joins the live verbs; "Reviews go by class; explore,
   draft and implement do not." No line is added: the file holds 200 and
   the test allows 200.
6. **`model-endpoints.yaml`**, the three English remarks: `openai-codex`
   "Used for drafting spec, design and plan (phases 2, 2b and 3, `stage2.py
   draft`, writing in the CLI's workspace-write sandbox) and for the review
   (phase 6) …; the spec review (phase 2a) moved to Opus 5.5 (ADR 0016) and
   the review loop (phase 4b) moved to `opencode-go` (ADR 0011)";
   `opencode-go` "the spec review (phase 2a) runs on Opus 5.5 and the review
   (phase 6) on Codex"; `glm-coding-plan` one sentence: "`glm-5.3` drafts
   spec, design and plan through `stage2.py draft` when two Codex attempts
   failed (ADR 0016)." No German key changes.
7. **`prompts/`**. `02-spec.md`, `02b-design.md`, `03-plan.md`: the Model
   line names Codex (`gpt-6.1-sol`) at effort `max` started by `python3
   scripts/stage2.py draft <change>` — one call for 2, 2b and 3, GLM 5.3
   after two failed attempts — and Opus 5.5 at effort `xhigh` where Stage 2
   is off, keeping each line's reason. `02-spec.md`, "After the spec
   review", one sentence: on the runner path a second `draft` does this,
   after the maintainer has answered every `[AMBIGUITY]`. `03-plan.md`: the
   card sentence says "as a subagent or through the runner".
   `02a-spec-review.md`: Model — Opus 5.5 in a fresh context, by hand for a
   spike, `python3 scripts/stage2.py spec-review <change>` (Claude Code,
   effort `xhigh`, read-only tools) otherwise; Session — the fixed-id path
   for a spike, and "through the runner no session is kept: phase 6 is
   Codex's (`gpt-6.1-sol`), in a fresh session"; the runner adds the
   reviewer and the status. `06-review.md`: Model and Session — the Codex
   session starts fresh where phase 2a ran on Opus 5.5, a recorded Codex 2a
   session is resumed, and the reviewer checks first that each 2a row
   arrived.
8. **This `plan.md`**: each `not yet written` ledger line becomes a test
   entry once its test exists; a measured line below `## Time used`. Then
   `.venv/bin/python scripts/check_frontmatter_current.py --stamp` and
   `.venv/bin/python scripts/plans_registry.py --index`.

### The drafting rules

`DRAFT_RULES`, the text the runner appends (criterion 3):

> Write, in `plans/changes/<change>/`, `spec.md`, `design.md` when
> `prompts/02b-design.md` asks for one, and `plan.md`, as the three prompts
> above say and in the form of the files under `templates/`. An ADR draft,
> when one is due, is exactly one new file `docs/adr/<NNNN>-<slug>.md`,
> numbered after the highest file there. Change nothing else: the runner
> puts back every other path git sees as changed, and the change's
> `decisions.md`. If `findings.md` holds phase-2a rows whose Status is
> `open`, work each into `spec.md` as `prompts/02-spec.md`, "After the spec
> review", says, write its Status in `findings.md`, and bring `design.md`
> and `plan.md` into line. A `[DECISION]` goes into the spec's "Open
> decisions" in the form `prompts/02-spec.md` gives. Never write an answer
> for the maintainer, never record an ADR answer, and never change a class,
> a criterion or a decision to make a gate green. `plan.md` opens with the
> card and holds a `## Time used` section, empty until phase 4. Do not
> commit and run no git command that changes the repository: the runner
> runs `make verify` and makes the one commit.

## Verification

```sh
.venv/bin/python -m pytest tests/test_stage2.py tests/test_model_endpoints.py -q
make verify
```

`make verify` stays red on `adr-answers` until the orchestrating session
records the maintainer's answer for this change.

## Criterion ledger

- 1: tests/test_stage2.py::test_a_draft_starts_codex_with_workspace_write_and_no_bypass — the draft call keeps `read-only`, or passes `--add-dir`
- 2: tests/test_stage2.py::test_codex_is_pinned_on_first_and_resumed_calls — rewritten on a seeded Codex 2a session; red when `review` passes `workspace-write`
- 3: tests/test_stage2.py::test_the_draft_prompt_carries_the_three_phase_prompts_and_the_rules — the GLM route built without `03-plan.md`
- 4: tests/test_stage2.py::test_a_draft_without_decisions_or_a_research_bead_refuses — `required` left empty
- 5: tests/test_stage2.py::test_a_draft_refuses_changes_outside_findings — the pre-existing check skipped
- 6: tests/test_stage2.py::test_each_draft_attempt_has_its_audit_line_and_reason — the reason dropped from the fallback's line
- 7: tests/test_stage2.py::test_a_leak_before_a_draft_attempt_stops_the_chain — a `Refused` caught as a failed call
- 8: tests/test_stage2.py::test_paths_outside_the_change_folder_are_put_back_and_named — the put-back skipped, or an existing ADR kept
- 9: tests/test_stage2.py::test_an_edited_decisions_file_is_put_back — `decisions.md` kept with the folder
- 10: tests/test_stage2.py::test_two_new_adr_files_fail_the_attempt — no count of new ADR files
- 11: tests/test_stage2.py::test_a_draft_call_that_moves_head_stops_the_run — the HEAD check after the put-back
- 12: tests/test_stage2.py::test_a_red_verify_fails_the_draft_attempt — the exit code of `make verify` ignored
- 13: tests/test_stage2.py::test_only_the_changes_own_missing_adr_answer_is_tolerated — any red `adr-answers` section tolerated
- 14: tests/test_stage2.py::test_a_missing_spec_or_plan_fails_the_attempt — only `plan.md` checked
- 15: tests/test_stage2.py::test_a_plan_without_its_card_fails_the_attempt — the labels looked for anywhere in the file
- 16: tests/test_stage2.py::test_a_plan_without_time_used_fails_the_attempt — the heading check left out
- 17: tests/test_stage2.py::test_a_passing_draft_makes_one_commit_and_leaves_a_clean_tree — `findings.md` written after the commit
- 18: tests/test_stage2.py::test_a_failed_first_draft_gets_one_codex_repair_with_its_diagnostics — the diagnostics not passed to the second prompt
- 19: tests/test_stage2.py::test_two_failed_codex_attempts_fall_back_to_glm_5_3 — the GLM route on `GLM_FLASH`
- 20: tests/test_stage2.py::test_a_failed_draft_call_is_put_back_and_recorded — the put-back left out after a dead call
- 21: tests/test_stage2.py::test_a_failed_draft_check_leaves_its_block_and_its_tree — the tree put back after a post-run failure
- 22: tests/test_stage2.py::test_three_failed_draft_attempts_exit_1_without_a_commit — the loop ends without raising
- 23: tests/test_stage2.py::test_a_codex_draft_never_reads_the_glm_key — the key read before the loop
- 24: tests/test_stage2.py::test_a_missing_glm_key_refuses_the_glm_draft_attempt — a `None` key passed to the GLM call
- 25: tests/test_stage2.py::test_a_glm_draft_that_writes_the_key_is_refused_without_a_commit — the scan skipped on the GLM route
- 26: tests/test_stage2.py::test_stage2_off_is_only_for_work_verbs — `draft` joins its parameters; red when `draft` accepts the flag
- 27: tests/test_stage2.py::test_the_spec_review_starts_opus_with_read_only_tools — the spec review still calls `run_codex`
- 28: tests/test_stage2.py::test_the_spec_review_answer_lands_as_opus_rows_without_a_session — the session line still appended
- 29: tests/test_stage2.py::test_a_findings_file_the_spec_review_creates_names_claude_code — the producer map left at `codex` or `pi`
- 30: tests/test_stage2.py::test_a_fresh_phase_6_session_says_so — its second half seeds the session line; red when `review` resumes without one
- 31: tests/test_stage2.py::test_review_resumes_the_recorded_session — the line seeded by hand; red when a recorded session is not resumed
- 32: tests/test_stage2.py::test_workflow_section_4_routes_the_three_reviews — `STAGE2_ROUTING` and `class_table_problems` rewritten; red on a 2a row on Codex
- 33: tests/test_stage2.py::test_the_workflow_states_the_order_of_a_drafted_change — one of the five steps removed
- 34: tests/test_stage2.py::test_the_review_prompts_give_both_paths — `review_prompt_problems` rewritten; red when 02a's Model line names gpt-6.1-sol
- 34: tests/test_stage2.py::test_the_drafting_prompts_name_the_draft_verb — a drafting prompt's Model line without `stage2.py draft <change>`
- 35: tests/test_stage2.py::test_agents_md_names_the_loop_and_the_runner — `agents_md_problems` gains the draft and Opus needles; red on "Codex reviews 2a and 6"
- 36: tests/test_model_endpoints.py::test_no_old_reviewer_remark_claims_a_review_phase — `_remark_problems` rewritten; red when the Codex remark claims phase 2a
- 36: tests/test_stage2.py::test_the_glm_remark_names_its_work_verbs_and_no_review_phase — gains the `glm-5.3` draft needle
- 36: tests/test_model_endpoints.py::test_no_remark_routes_the_spec_review_to_codex — the opencode-go remark still says 2a stays with Codex
- 37: not a test — the touch map in the decision pull request shows `docs/adr/` gaining only `0016-codex-drafts-and-opus-reviews-the-spec.md`

## Not touched

- `implement`, `verify_attempt` (except moving its evidence lines into
  `verify_evidence`), `red_sections`, `restore_baseline`, `review`,
  `review_loop`, `release`, `probe`, `session` in `scripts/stage2.py`.
- `scripts/stage2_runs.py`, `scripts/stage2_session.py`,
  `scripts/leakcheck.py`, `scripts/check_adr_answers.py`, `decisions/`,
  `provenance.yaml`, `.claude/settings.json`, `templates/`.
- `docs/adr/0007-…`, `0011-…`, `0012-…`; the ADR 0016 draft is written in
  phase 2b and phase 4 does not edit it.
- The user-level `spec-planner` definition outside the repository.

## Risks

- **Overlap with the open change stage2-repair** (branch
  `feat/stage2-repair`, bead coding-harness-g2f, not merged on 2026-10-12).
  It edits the same five files: `scripts/stage2.py` (the module docstring,
  the constants, `checkpoint`, `implement` rewritten into `run_attempts`,
  `main`), `tests/test_stage2.py` (+864 lines), `docs/WORKFLOW.md` §4,
  `AGENTS.md` — the very stage-2 paragraph step 5 edits — and the
  `glm-coding-plan` remark of `model-endpoints.yaml`. Phase 4 starts from a
  fresh merge of `origin/main`; if stage2-repair has merged, its `GLM` and
  `checkpoint(message=…)` are used as they stand and the AGENTS.md sentence
  is rewritten on top of its version; if not, the identical forms above keep
  the later merge textual, and the paragraph conflict is resolved by hand.
  One change at a time: the orchestrator lets stage2-repair merge first.
- **`AGENTS.md` sits at its bound of 200 lines.** Step 5 edits in place.
- **Test churn.** About twenty existing tests move from the Codex stand-in to
  the Claude stand-in for `spec-review`; each keeps its assertion, only the
  stand-in and, where needed, a seeded session line change.
- **Unmeasured sandbox.** `workspace-write` is configured, not measured; the
  ADR says so, and the first real draft is a later change's.

## Phase-4 notes (2026-10-13)

What the repair pass over attempt 1's diagnostics settled, for the next
reading of this plan:

- **§3's Model routing (step 4).** The plan's wording kept rows 2, 2b and 3 on
  `**Opus 5.5**` and only reworded their why-cells. The pre-existing pin test
  `test_routing_gives_2b_the_prompt_model` holds row 2b's bold cell against
  `prompts/02b-design.md`'s Model line, which now leads with `gpt-6.1-sol` —
  so the three bold cells move to `**gpt-6.1-sol**` and the why-cells carry
  effort `max` and the Stage-2-off clause. Rows 1, 1a, 2a, 4, 5, 6 and 7 are
  untouched, as `routing_problems` pins them.
- **The drafting prompts' Model lines lead with the bare id**
  (`**Model:** gpt-6.1-sol — Codex (`gpt-6.1-sol`) at effort `max`, …`): the
  model-line resolvers in `tests/test_templates.py` and
  `tests/test_model_endpoints.py` cut at the first em-dash, and the earlier
  form (`Codex (`gpt-6.1-sol`) — …`) resolved to no declared id.
- **`verify_evidence` scrubs with its `key`** (the evidence lines moved into
  it, as "Not touched" allows), and both call sites dropped their outer
  `scrub` — scrubbing twice is a no-op, once is enough.
- **Codex stand-in steps in the draft tests carry `codex_ok(...)`** (a
  `thread.started` event and the answer file) wherever the attempt's call must
  succeed; the dead first step of criterion 20's test stays bare. The failed
  runs of the multi-scenario tests leave an untracked `plans/INDEX.md` (from
  `prepare_derived`), which the next run would refuse as a pre-existing
  change; those scenarios unlink it. The two tests that read a Codex call's
  prompt take `["argv"][-1]` — `run_codex` passes the prompt as the last
  argv element, and the stand-in's `prompt_file` is a Claude-option read.
- **The planted §4 mutations of `test_workflow_section_4_routes_the_three_reviews`**
  name §4's why-cell heads for rows 2, 2b and 3 (`… | effort `max`, one call`,
  `… | effort `max`, drafted`): with §3's bold cells now `gpt-6.1-sol` too,
  the bare `| 2 Spec | **gpt-6.1-sol** |` needle matched §3's row first, and
  `text.replace(…, 1)` mutated the section `routing_problems` does not pin.
- **`REIST_NICHT`** (`scripts/kit/probe.py`) renames the three prompt cases to
  the new model-line ids and adds
  `test_no_remark_routes_the_spec_review_to_codex`; 35 -> 36, at the cap, no
  raise.

## Runner route — 2026-10-13

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-13 — phase 4 under the Stage-2 runner (`implement codex-drafts`), one
span over three context windows, the compaction breaks counted. The session
has no command tool, so no wall-clock start–end could be read; the date is the
runner's reading (2026-10-13, also on the audit lines in `findings.md`).
Attempt 1's red `make verify` — 24 pytest failures, two ruff-check errors, one
formatting rewrap, five leerprobe cases — was repaired in that window.
A further repair window (attempt 3, same date, no command tool, so no
wall-clock reading) fixed attempt 2's three draft tests: the prompt test reads
the drafting rules with whitespace flattened, and the two multi-run tests
clear `plans/INDEX.md` and `scripts/__pycache__` between runs through
`clear_derived_leftovers`; single-entry plant dicts gained their trailing
commas. The runner's `make verify` and checkpoint commit are still to come.
The appetite of 8 h is not reached.
