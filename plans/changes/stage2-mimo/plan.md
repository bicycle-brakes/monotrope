---
title: "Plan — stage2-mimo"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-08
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-ymx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-08"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, opencode-go, pi, review-loop, adr]
---

# Plan — `stage2-mimo`

```text
For you:     the review loop's rounds start through Pi 1.1.0 at OpenCode Go's chat-completions address, read-only and isolated per call; the ladder stays one line of model-endpoints.yaml, 2a and 6 stay Codex — and ADR 0011 now says in plain words that a round can read outside the worktree, for your merge to decide
Done when:   criteria 1–29 hold and the verification command below is green; the probe answered on all three rungs through Pi; the pull request opens as `decide(stage2): …` with the label `decision`, ADR 0011 as rewritten and the answer file as you stated it
Appetite:    4 hours of phase 4 from 1d22f28 — the Pi launch, its tests, the wording, the probe — one repair round included
Not now:     Claude Code or OpenCode's CLI for the loop; a real Pi in the test suite; an operating-system sandbox for Pi's reads; the session verb's OpenCode path; MiMo above `high`; the German keys of model-endpoints.yaml
Pre-mortem:  suppose it failed: most likely because OpenCode Go answers Pi's calls with a real key by refusing them, so the probe stops the run and the loop has no launcher left
Starts unless you say stop.
```

Implements `spec.md`, criteria 1–29, planned from `design.md` (which holds
the ADR 0011 draft, identical to `docs/adr/0011-…`). Class `feature`; the ADR
question was answered "yes". This is the re-plan of 2026-10-08 for Pi: the
entry, the ladder, the three rounds, the record, the doctrine and the ADR
file stand as built at `3af0c9c`; what changes is the launcher, the address
and what follows from them. Stage 1: the one route on record is the
implement fallback below ("Runner route"); nothing to carry from phase 1.

**Before step 8:** answered — this change's own loop runs on the ladder
through Pi after the probe (maintainer, "1", 2026-10-08).

## Steps

1. **The Pi launch** (`scripts/stage2.py`). `run_reviewer(ctx, model,
   prompt, key) -> str` makes one `tempfile.TemporaryDirectory(prefix="stage2-")`
   holding `agent/settings.json` (`{"retry": {"enabled": false}}`), `home/`
   and `review-prompt.md`, and launches

   ```text
   pi --print --no-session --no-approve --no-extensions --no-mcp --no-skills
      --no-context-files --no-prompt-templates --no-themes --offline
      --tools read,grep,find,ls --thinking max --model opencode-go/<rung>
      --append-system-prompt <dir>/review-prompt.md
      "Review the change <change> as the appended instructions say."
   ```

   with `foreign_env({"HOME": <dir>/home, "PI_CODING_AGENT_DIR": <dir>/agent,
   "OPENCODE_API_KEY": key})`, `timeout=REVIEWER_MINUTES * 60`; a non-zero
   exit or an empty answer raises `fail("pi", …, key)`; the answer is
   scrubbed. New constants `PI_VERSION = "1.1.0"` and `PI_TOOLS =
   "read,grep,find,ls"`. `review_loop` and `probe` take the answer as a
   string.
2. **The pin** (`scripts/stage2.py`). `require_pi(root)` runs `pi --version`
   through `launch` in a scratch directory (`HOME` and
   `PI_CODING_AGENT_DIR` there, no key) with a 30-second timeout; an
   `OSError`, a `CallFailed`, a non-zero exit or a stripped output other than
   `PI_VERSION` raises `Refused("pi <what it said> is not the pinned
   1.1.0; no call starts.")`. `review_loop` calls it after `reviewer_key()`
   and before `change_diff`; `probe` once before its loop.
3. **What goes** (`scripts/stage2.py`). `OPENCODE_BASE_URL`,
   `REVIEWER_TOOLS`, `claude_env`, `opencode_env`, `result_of`, the `resume`
   and `session` parameters of `run_reviewer`; `glm_env` and its model
   variables return to main's text, without the window-enforcement variable.
   `begin_call` writes the producer `codex` for the Codex tuple and `pi`
   otherwise. The module docstring ("What this is", "Reads"), and the
   docstrings of `run_reviewer`, `review_loop` and `probe`, say Pi and
   `…/chat/completions`, and what a round can read (criterion 28).
4. **Tests** (`tests/test_stage2.py`). The stand-in serves `pi` too: it
   answers `--version` from the scenario (`pi_version`, default `1.1.0`;
   `pi_version_exit`) without recording it, reads its prompt from
   `--append-system-prompt`, records the listing and the `settings.json` of
   `PI_CODING_AGENT_DIR`, and takes `@KEY@` from `OPENCODE_API_KEY`. Every
   loop and probe case scripts `pi` where it scripted `claude`; the GLM cases
   assert main's environment. Rewritten: the criterion 8, 11, 12, 13 and 17
   cases (table below); new: criterion 27, 28 and 29 cases, each with its
   planted fault; criterion 23's needles follow the new wording.
5. **The entry's remark** (`model-endpoints.yaml`,
   `tests/test_model_endpoints.py`): the `bemerkung` of criterion 2, and the
   remark test's needles for it — `…/chat/completions`, the Anthropic
   address "not used", Pi validated, `x-opencode-session`, the two quoted
   terms and `2026-10-08`; the Claude Code needles go.
6. **The doctrine.** `docs/WORKFLOW.md` §4: the opening paragraph and the 4b
   routing row say Pi; "The runner is the only way" lists `pi` among the
   programs never typed by hand; "What every call then carries", the
   credential paragraph and "Reads" describe the Pi call and its unconfined
   `read` (criterion 28); the caveat names each subscription's client
   (criterion 29). `AGENTS.md`'s stage-2 paragraph and the model line of
   `prompts/04b-review-loop.md` say "through Pi". If `kit-probe` then names a
   new or renamed case, it goes into `REIST_NICHT` of `scripts/kit/probe.py`
   with its reason and `DECKEL` rises, as at `3af0c9c`.
7. **The probe** (special run, on the maintainer's machine with the key and
   Pi 1.1.0): `python3 scripts/stage2.py probe stage2-mimo`, once, on the
   last green commit of steps 1–6. The three output lines and that commit go
   into the pull request body. A refusal stops phase 4 and is reported
   (criterion 17); no step after this one runs on a refused rung.
8. **The loop (4b)**, as the maintainer answered on 2026-10-08 (option 1) —
   `python3 scripts/stage2.py review-loop stage2-mimo` round by round,
   every row decided in the loop record, each taken row repaired, `make
   verify` green before the next round, round 3 only after a taken row of
   round 2.
9. **Phases 5 and 6.** `make verify` green; then `python3
   scripts/stage2.py review stage2-mimo` (Codex resumes session
   `01a116db-602e-73e2-bbee-d11f961debe4`), which writes the verdict,
   releases the loop rows and has them marked.
10. **Phase 7.** The decision pull request: title `decide(stage2): …`, label
    `decision`, body from `.github/PULL_REQUEST_TEMPLATE/decision.md`,
    naming bead coding-harness-ymx, the probe's lines and commit and each
    loop round; `docs/adr/0011-…` as committed here (renumbered only if a
    lower number was taken); `decisions/answers/stage2-mimo/adr.yaml` as
    recorded at `fc76287`; the last commit carries `Closes-Bead:
    coding-harness-ymx`.

## Files

| File | What happens there |
|---|---|
| `scripts/stage2.py` | The Pi launch, the pin check, the removals, the producer, the docstrings (criteria 8, 10–17, 27, 28). |
| `tests/test_stage2.py` | The `pi` stand-in; the launch, key, refusal and pin cases; the doctrine cases (criteria 8, 11–13, 17, 20, 23, 25, 27–29). |
| `model-endpoints.yaml` | The `opencode-go` remark (criterion 2). |
| `tests/test_model_endpoints.py` | The remark's needles (criterion 2). |
| `docs/WORKFLOW.md` | §4: launcher, reads, caveat (criteria 21, 23, 28, 29). |
| `AGENTS.md` | The stage-2 paragraph says Pi (criterion 23). |
| `prompts/04b-review-loop.md` | The model line says Pi (criterion 23). |
| `scripts/kit/probe.py` | Only if `kit-probe` names a new or renamed case (step 6). |
| `plans/changes/stage2-mimo/findings.md` | The probe's and the loop's call lines, the phase-6 verdict and the released rows (runner-written). |
| `plans/changes/stage2-mimo/plan.md` | `## Time used` and any detail decision of phase 4. |
| `plans/INDEX.md` | Regenerated (`python3 scripts/plans_registry.py --index`) when a header here changes. |

Done in this phase, not in phase 4: `spec.md`, `design.md`, this file,
`research.md` (§S), `docs/adr/0011-stage-2-reviews-through-opencode-go.md`,
and the needles of `test_the_adr_draft_states_every_point`.

## Verification

```bash
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
```

Green after every step, green on the last commit (criterion 26). Beside it:
`python3 scripts/touch_map.py origin/main HEAD` for the pull request's "What
it touches", and `python3 scripts/check_adr_answers.py`.

## The test each criterion is held by

| # | Test | Red when |
|---|---|---|
| 1 | `test_the_opencode_go_entry_is_declared` | any field differs, a fourth model, another order, a customer class |
| 2 | `test_the_opencode_go_remark_names_every_source` | a point missing; Claude Code or `…/v1/messages` named as the path |
| 3 | `test_no_old_reviewer_remark_claims_a_review_phase` | a remark claiming the loop, or Codex's without 2a and 6 |
| 4 | `test_a_round_calls_its_rung_from_the_entry` | round *n* calling another id; an id as a literal in the runner |
| 5 | `test_reordering_the_ladder_touches_no_code` | a reordered fixture's rounds calling the old model |
| 6 | `test_the_loop_stops_at_three_rounds` | a fourth round, or a stop at two |
| 7 | `test_round_three_starts_only_after_a_taken_row` | round 3 without a taken row, or none after one |
| 8 | `test_the_review_loop_launches_pi_isolated` | a flag missing or added; another tool, model or level; an agent directory shared or holding another file; the caller's `HOME`; an `ANTHROPIC_*` or `CLAUDE_*` variable; argv starting `claude` or `codex` |
| 9 | `test_review_resumes_the_recorded_session`, `test_a_fresh_phase_6_session_says_so` | unchanged |
| 10 | `test_each_call_runs_its_own_leak_check`, `test_an_endpoint_the_declaration_does_not_clear_refuses` | unchanged |
| 11 | `test_the_opencode_key_never_leaves_the_runner` | the key in argv, under another variable, or in the agent directory; `--api-key` in argv |
| 12 | `test_a_key_fragment_never_survives_the_relayed_streams` | the key in stdout, stderr, the loop record or `findings.md` |
| 13 | `test_no_call_carries_another_endpoints_key` | the GLM key in a `pi` call's environment, or the reverse |
| 14 | `test_a_round_that_did_not_review_writes_nothing` | a block written, exit 0, or no cause named |
| 15 | `test_a_call_over_the_time_limit_is_stopped` | a `pi` stand-in outlasting the shortened limit and the run waiting |
| 16 | `test_a_leak_refuses_the_call` | unchanged |
| 17 | `test_a_refused_rung_stops_the_run_without_fallback` | any call after the refused `pi` call — `claude`, `codex`, another `pi` |
| 18 | `test_a_round_is_written_as_its_rung` | unchanged |
| 19 | `test_the_release_carries_each_rows_reviewer` | unchanged |
| 20 | `test_the_runner_finds_only_stand_ins`, `test_the_suite_never_reaches_the_real_denylist_or_secrets` | a `pi` on `PATH` that is not the stand-in |
| 21 | `test_workflow_section_4_routes_the_three_reviews` | unchanged |
| 22 | `test_workflow_section_4_keeps_the_lineage_argument` | unchanged |
| 23 | `test_the_prompts_name_the_ladder_and_the_limit` | the loop prompt or `AGENTS.md` without Pi, or naming Claude Code as the loop's launcher |
| 24 | `test_the_stop_rule_counts_every_rung` | unchanged |
| 25 | `test_the_adr_draft_states_every_point` | a point or option of criterion 25 missing from the draft; "through Claude Code" as the launcher |
| 26 | the verification command | any gate red |
| 27 | `test_a_pi_off_the_pin_is_refused` | `1.1.1`, a failing or absent `pi`, and a round that starts, a call line, or an exit other than 2 |
| 28 | `test_section_4_says_what_a_round_can_read` | §4 or the docstring calling every call confined, or the loop among the `--restricted` calls |
| 29 | `test_section_4_caveat_names_each_client` | the caveat naming Claude Code for every subscription, or OpenCode Go without its accepted risk |

## Not touched

- `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` — amended by the new
  record, never edited in place.
- `scripts/stage2_session.py` and its tests — the `session` verb's OpenCode
  path is its own (bead coding-harness-amp).
- `run_work_model`, `explore`, `implement` beyond `glm_env` returning to
  main's text; `run_codex`, `spec_review`, `review`.
- `scripts/check_decision_continuity.py`, the continuity table of
  `docs/architecture/2026-09-17-omnigent-first-target.md`, and decision
  D-13.
- `scripts/leakcheck.py`, the denylist; `scripts/harness.py`,
  `scripts/touch_map.py`, `scripts/new_change.py`; `.claude/settings.json`.
- `~/.pi`, the Pi install, the secrets file.
- `prompts/02a-spec-review.md`, `prompts/06-review.md`,
  `prompts/01-explore.md`, `prompts/04-implement.md` — no launcher named
  there.
- The German keys and comments of `model-endpoints.yaml`.

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

`[DETAIL]` 2026-10-08 — the rung ids are no ids of Claude Code's model
catalog, and its window enforcement refuses such a model before the request
leaves (the probe's first rung: `[claude-code:unrecognized_model]`, exit 1,
measured 2026-10-08; `GET /zen/go/v1/models` lists all three ids, so the
endpoint knows them). The vendor's own message names the variable that
restores waiting for the API, so the runner sets
`CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1` in every Claude Code
call's environment; the ids stay exactly as `model-endpoints.yaml` lists
them, and no settings file is touched (criterion 5). The probe measures the
address again after this line.

`[DETAIL]` 2026-10-08 (afternoon, phase-3 re-plan) — the window-enforcement
variable of the entry above goes with Claude Code as the loop's launcher:
its one recorded reason was the rungs through Claude Code, Pi replaces that
launcher (`decisions.md`, addendum of the afternoon), and GLM's environment
returns to main's, which never carried it (spec, `[DETAIL]`s; step 3).

`[DETAIL]` 2026-10-08 (phase 4, steps 1–6 at `b3799cd`) — `require_pi()` takes
no argument. The plan wrote `require_pi(root)`, but the check runs in a
scratch directory with no key and reads nothing from the worktree, so `root`
was unused and the lint gate (`ARG001`) refused it.

`[DETAIL]` 2026-10-08 (phase 4, steps 1–6) — `glm_env(key, config_dir, model)`
keeps the `model` parameter and `GLM_MODEL_VARIABLES` keeps main's name, and
only the window-enforcement variable and the shared `claude_env` go. Main's
`glm_env` read the model from its `GLM` tuple, which this branch replaced by
`GLM_FLASH` (explore and implement pass the model they run), so the model
stays an argument; everything else is main's text.

`[DETAIL]` 2026-10-08 (phase 4, steps 1–6) — `launch` takes an optional
`limit` text for the stop message. The version check's 30-second stop and the
reviewer's 30-minute stop both raise `CallFailed` from `launch`; without the
text the version check would have reported "the reviewer time limit after 30
minutes". The reviewer message is unchanged, so criterion 15's test still
reads the same words.

`[DETAIL]` 2026-10-08 (phase 4, steps 1–6) — one commit for steps 1–6. Steps 1
to 4 cannot be green apart (the removals of step 3 and the stand-in of step 4
change together), and the doctrine tests that hold steps 5 and 6 live in
`tests/test_stage2.py`; `make verify` was green on the combined tree only.

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

2026-10-08 15:27–15:53, 26 min, plan steps 1–6 (Sonnet 5.5 sub-agent session; `date` read at start and before the commit; background `make verify` waits counted).

## Probe — 2026-10-08

`python3 scripts/stage2.py probe stage2-mimo` on `b3bd6fd`, through Pi 1.1.0
with the real key: all three rungs answered (`probe: 3 rungs answered`, exit
0), the leak check clean before each call (309 files, 693–694 commits, 12
rules). Each model described itself as "Claude (Anthropic)" — self-report,
not evidence. Measured the same day with one extra call per rung (`pi --print
--mode json --no-tools`, prompt "Reply with the single word OK.", approved
by the maintainer): every answer came back as `provider: opencode-go`, `api:
openai-completions`, `model` equal to the rung, and Pi recorded no
`responseModel` — which it sets only when the server's chunk names a model
other than the one requested. So the server reported no other model.
