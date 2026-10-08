---
title: "Plan — stage2-mimo"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-ymx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: opencode, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, opencode-go, review-loop, adr]
---

# Plan — `stage2-mimo`

```text
For you:     the review loop runs on OpenCode Go — its three rounds on rung 1, 2, 3 — and the order is one line of model-endpoints.yaml you can change in a pull request that touches nothing else; the spec review and the review stay with Codex, GLM stops reviewing
Done when:   criteria 1–26 hold and the verification command below is green; the pull request carries docs/adr/0011, the answer file re-recorded in your own words and the three probe calls, and opens as `decide(stage2): …` with the label `decision`
Appetite:    8 hours of phase 4, one repair round included
Not now:     retiring `openai-codex`; `.claude/settings.json` and its ask rule on `codex` (bead coding-harness-amp); the German keys of `model-endpoints.yaml`; the residency [GAP] beyond the probe; the continuity chain of D-13; `Also raised` and matching rows across rounds
Pre-mortem:  suppose it failed: most likely because the pattern that reads the session line proves too strict, so phase 6 starts a fresh session on every change and says so while the 2a context is quietly lost
Starts unless you say stop.
```

Implements `spec.md`, criteria 1–26, planned from `design.md` (which holds the
ADR 0011 draft). Class `feature`; the ADR question was answered "yes" on
2026-10-07. Stage 1: no route to carry — `research.md` records no
`--stage2-off` run, because this change's own spec review ran with stage 2 on.

## Steps

1. **The entry.** `model-endpoints.yaml`: add `opencode-go` with its operator,
   billing, residency and the three ids in ladder order; correct the
   `bemerkung`s of `openai-codex` and `glm-coding-plan` so each names the
   phases that still route to it.
2. **Tests for the entry.** `tests/test_model_endpoints.py`: the entry's shape
   and order, every named point of its remark, the two corrected remarks, and
   that every model id a prompt names still resolves to a declared endpoint.
3. **The ladder and the rounds.** `scripts/stage2.py`: read `modelle` from the
   entry, call `modelle[n-1]` in round *n*, `MAX_ROUNDS = 3`, round 3 only
   after a `taken` row of round 2, refusal text naming the count that ran, and
   the round heading and the `Reviewer` cell carrying the
   rung instead of the literal `GLM`.
4. **The launch.** `scripts/stage2.py`: one launch path for `review-loop` —
   Claude Code on
   `https://opencode.ai/zen/go/v1/messages`, the rung as model, effort `max`,
   the settings of criterion 8, the key from the secrets file into the
   environment only, one named 30-minute constant, and a new `probe` verb
   (step 7). `spec-review` and `review` keep the Codex launch exactly as on
   main (`codex exec`, `gpt-6.1-sol` pinned, the read-only sandbox, hooks and
   memories off — the maintainer, 2026-10-08); `run_codex` and the Codex tuple
   stay, and the ask rule on a typed `codex` and `.claude/settings.json` stay.
5. **Tests for the runner.** `tests/test_stage2.py`: stand-ins for argv,
   environment, ladder order, the three-round limit, the round-3 condition,
   the time limit, a refused rung, a failed round's silence and the record's
   rung names; the Codex tests of `spec-review` and `review` pass unchanged.
6. **The doctrine.** `docs/WORKFLOW.md` §4 (routing table, lineages, stop
   rule), `prompts/02a-spec-review.md`, `prompts/04b-review-loop.md`,
   `prompts/06-review.md` and the stage-2 paragraph of `AGENTS.md`: the loop
   on the ladder with the limit of three and the round-3 condition, while 2a
   and 6 keep naming Codex. `prompts/01-explore.md` and `prompts/04-implement.md`
   keep GLM 5.3 Flash.
7. **The compatibility probe.** `stage2.py probe` (a `[DETAIL]`: the DoD
   demands three calls through the runner and no verb of it exists for a
   measurement) runs one call per rung, declaration and leak check in front
   of each, printing the rung's id and the first line of the answer and
   writing to no record. Run once per rung on the last commit of step 5,
   before any other step builds on the address; the three lines and their
   commit go into the pull request body. A refusal stops phase 4 and is
   reported (criterion 17).
8. **The pull request (phase 7).** Copy the ADR draft out of `design.md` into
   `docs/adr/0011-stage-2-reviews-through-opencode-go.md` (renumber if a
   lower number was taken), re-record `decisions/answers/stage2-mimo/adr.yaml`
   from the maintainer's own sentence — its reason still describes the
   superseded Xiaomi wording — and open the pull request as a decision pull
   request: title `decide(stage2): …`, label `decision`, body from
   `.github/PULL_REQUEST_TEMPLATE/decision.md`, beads and probe lines in it.

## Files

| File | What happens there |
|---|---|
| `model-endpoints.yaml` | The `opencode-go` entry is added; two existing remarks stop claiming reviewer phases (criteria 1–3). |
| `scripts/stage2.py` | Ladder, three-round loop, one launch path for the loop, the 30-minute constant, the generalized headings and session line, the `probe` verb; the Codex path stays for 2a and 6 (criteria 4–20). |
| `tests/test_model_endpoints.py` | Holds the entry, its remark, the corrected remarks and the prompt ids (criteria 1–3). |
| `tests/test_stage2.py` | Holds the launch, the ladder, the limits, the key and the record (criteria 4–20). |
| `docs/WORKFLOW.md` | §4's routing table, lineage argument and stop rule follow the ladder (criteria 21, 22, 24). |
| `prompts/02a-spec-review.md` | Keeps Codex as its reviewer and names the loop's three-round limit (criterion 23). |
| `prompts/04b-review-loop.md` | Names the ladder, the three rounds and the round-3 condition (criterion 23). |
| `prompts/06-review.md` | Keeps Codex as its reviewer and names the loop's rounds and their reviewers (criterion 23). |
| `AGENTS.md` | The stage-2 paragraph names the ladder and the three rounds (criterion 23). |
| `plans/changes/stage2-mimo/design.md` | Holds the ADR 0011 draft; copied out in step 8 (criterion 25). |
| `docs/adr/0011-stage-2-reviews-through-opencode-go.md` | Created in step 8 from that draft; makes the pull request a decision pull request (criterion 25). |
| `decisions/answers/stage2-mimo/adr.yaml` | Re-recorded in step 8 from the maintainer's own words (criterion 25, house rule 8). |
| `plans/changes/stage2-mimo/findings.md` | Gains the 4b rows and the phase-6 verdict of this change (criteria 19, 20). |
| `plans/INDEX.md` | Regenerated (`--index`) whenever an artefact of this folder changes. |

## Verification

```bash
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
```

Green after every step above, green on the last commit (criterion 26). Two
more run beside it: `python3 scripts/touch_map.py origin/main HEAD` for the
pull request's "What it touches" (the DoD's protected-area line), and
`python3 scripts/check_decision_continuity.py`, which stays green because
this change adds no amendment to the continuity map (`[DETAIL]` 7).

## The test each criterion is held by

| # | Test | Red when |
|---|---|---|
| 1 | `test_the_opencode_go_entry_is_declared` | any field differs, a fourth model, another order, a customer class inside `darf_sehen` |
| 2 | `test_the_opencode_go_remark_names_every_source` | one of the named points missing or not stated by its source |
| 3 | `test_no_old_reviewer_remark_claims_a_review_phase` | either entry misstating which phases still route to it |
| 4 | `test_a_round_calls_its_rung_from_the_entry` | round *n* calling another id; a reviewer id as a literal in the runner |
| 5 | `test_reordering_the_ladder_touches_no_code` | a reordered fixture's rounds calling the old model, or the change needing a line in `scripts/stage2.py` |
| 6 | `test_the_loop_stops_at_three_rounds` | a fourth round starting, or the loop still stopping at two |
| 7 | `test_round_three_starts_only_after_a_taken_row` | round 3 without a `taken` row, or none after one |
| 8 | `test_the_review_loop_launches_claude_on_the_anthropic_address` | another base URL, model or effort, one of the settings missing, `codex` in the loop's argv |
| 9 | `test_review_resumes_the_recorded_session` and `test_a_fresh_phase_6_session_says_so` | a recorded session not resumed; a fresh session without its sentence; a line naming no reviewer |
| 10 | `test_each_call_runs_its_own_leak_check` and `test_an_endpoint_the_declaration_does_not_clear_refuses` | a call without its own check, the check after it, one check for two calls |
| 11 | `test_the_opencode_key_never_leaves_the_runner` | eight consecutive characters of the key in any argv |
| 12 | `test_a_key_fragment_never_survives_the_relayed_streams` | the key in stdout, stderr, the loop record or `findings.md` |
| 13 | `test_no_call_carries_another_endpoints_key` | the GLM key in an OpenCode Go call's environment, or the reverse |
| 14 | `test_a_round_that_did_not_review_writes_nothing` | a block in the loop record, exit 0, or an unnamed cause |
| 15 | `test_a_call_over_the_time_limit_is_stopped` | a stand-in outlasting the shortened limit with the run waiting or exiting 0 |
| 16 | `test_a_leak_refuses_the_call` | a call after a red check, a written round, or another exit |
| 17 | `test_a_refused_rung_stops_the_run_without_fallback` | a fallback to the OpenAI address, another rung or another endpoint |
| 18 | `test_a_round_is_written_as_its_rung` | a heading naming another model, another reviewer cell, a row inside the worktree |
| 19 | `test_the_release_carries_each_rows_reviewer` | a released row with another reviewer, or the release before the verdict |
| 20 | `test_the_runner_finds_only_stand_ins` and `test_the_suite_never_reaches_the_real_denylist_or_secrets` | either of them red |
| 21 | `test_workflow_section_4_routes_the_three_reviews` | a table routing 4b to GLM or one rung, or 2a or 6 to the ladder, or a `spike` given a review |
| 22 | `test_workflow_section_4_keeps_the_lineage_argument` | the argument gone, or a sentence naming two reviewers of one round |
| 23 | `test_the_prompts_name_the_ladder_and_the_limit` | the loop prompt without the ladder; a review prompt naming a rung as its reviewer; the instruction file sending 2a or 6 to the ladder; `01-explore` or `04-implement` without GLM |
| 24 | `test_the_stop_rule_counts_every_rung` | the measurement naming only the two former reviewers |
| 25 | `test_the_adr_draft_states_every_point` | one of the six points of criterion 25 missing from the draft in `design.md` |
| 26 | the verification command above | any gate red on the last commit |

## Not touched

The obvious reading of the files above would reach further. It does not:

- `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` — amended by a new
  record, never edited in place; `docs/adr/` gains one file, in step 8.
- `scripts/check_decision_continuity.py`, the continuity table of
  `docs/architecture/2026-09-17-omnigent-first-target.md`, and decision
  D-13 — no criterion of D-13 changes here (`[DETAIL]` 7).
- `scripts/leakcheck.py`, the denylist and where it lives; `scripts/harness.py`,
  `scripts/touch_map.py`, `scripts/new_change.py` — machinery, not reviews.
- `.claude/settings.json` and the ask rule on `codex` — bead
  coding-harness-amp; the runner stops starting that binary on its own.
- `ROADMAP.md`, `docs/architecture/` beyond the line above, and the Omnigent
  wiring; `prompts/01-explore.md` and `prompts/04-implement.md`.
- The German keys and comments of `model-endpoints.yaml` — a pull request of
  its own (house rule 1).
- The loop record's place, the evidence rule and verdict-first-release-after;
  `openai-codex` itself, which stays declared for what still routes to it.

## Runner route — 2026-10-08

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Detail decision — 2026-10-08

`[DETAIL]` — which side of the two red review-loop tests was wrong: the
tests, not the code. The spec lets every round read its model from the ladder
and writes each round as its own reviewer (criteria 4 and 18), so a round
without a finding still stamps its rung into the record — the runner does
that (`answer_parts`, `scripts/stage2.py`). The first test asserted the loop
record from a read taken before the second round had run, so it could never
see that round's line; it now re-reads after the run. The spec lets round 3
start only on a taken row of round 2 (criterion 7), which the runner checks
before launching anything; the second test meant to rewrite one row of round
2 into a taken one, but its pattern expected an empty test-broke cell where
the test's own decision helper had written `no`, so the substitution matched
nothing and round 2 stayed without a taken row. Both repairs change
`tests/test_stage2.py` only; the runner code is untouched.

`[DETAIL]` 2026-10-08 — the reasons behind the empty-repo probe's travel
list: its three new entries all read the endpoint inventory
(`model-endpoints.yaml`), which the kit leaves at home exactly as it did for
the prompt cases, so they carry the standing reason `bestand-dieses-repos`;
the fourth change is a rename, since the loop prompt's model line names the
ladder's first rung (`deepseek-v4.1-flash`) where it named GLM 5.3 before
(`scripts/kit/probe.py`, `REIST_NICHT` and its cap).

`[DETAIL]` 2026-10-08 — the stream a failed call reports on. The implement
run had moved the `failed:` line to standard output to follow criterion 14's
wording, which broke the session verb's tests that read standard error (the
runner has printed the failure line there since before the session verb
merged). At the maintainer's word (2026-10-08) the line goes to standard
error again, the tests read there, and criterion 14's sentence says "standard
error" so the artifact set agrees again.

`[DETAIL]` 2026-10-08 — the undeclared case of the session tests
(`test_a_model_no_declaration_clears_for_a_session_refuses`) relied on the
production declaration naming no `opencode-go` entry at all; this change
declares that entry, so the case now names a rung no entry lists
(`opencode-go/never-listed-rung`) and keeps the same refusal it always
asserted. The test fixture copies the production declaration, so a case may
not depend on what production happens to omit.

## Time used

2026-10-08, phase-4 session under the Stage-2 runner — start and end clock
times not readable in it (the runner's session has file tools and no command
tool, so `date` could not be read; the span is not estimated). The session
covered plan steps 1–6 and the file part of step 8 (entry, runner, tests,
doctrine, `docs/adr/0011`, the re-recorded answer file); step 7 (the probe)
and the pull request remain for a session with command access.

2026-10-08, phase-4 repair session under the Stage-2 runner (attempt 2, after
the first `make verify` came back red) — start and end clock times not
readable in it either (file tools, no command tool; the span is not
estimated). The session audited the red gates from the file side and
repaired them: the `updated:` stamps of `docs/WORKFLOW.md`, `plan.md` and
`design.md` (frontmatter-current measures a modified file against today),
the AGENTS.md checker whose third planted fault could not fail, and the
missing "three rounds" needles in `prompts/02a-spec-review.md` and
`prompts/06-review.md`. Step 7 (the probe) and the pull request remain for a
session with command access.

2026-10-08, phase-4 repair session under the Stage-2 runner (attempt 3) —
start and end clock times not readable (file tools, no command tool; the span
is not estimated). The diagnostics are all markdownlint output on files this
change does not touch (`README.md`, `templates/`,
`tools/claude-code/README.md`), and the `markdownlint` gate is
`enforcement: report` in `decisions/gates.yaml`, so it cannot be what turned
`make verify` red. The blocking gate is not named in the diagnostics tail; no
other file was changed.
