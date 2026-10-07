---
title: "Plan — stage2-mimo"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-ymx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, mimo, review-loop, model-endpoints, adr]
---

# Plan — stage2-mimo

```text
For you:     MiMo-V2.6-Pro (Xiaomi) reviews each change in the loop beside GLM, and findings.md shows where they differ
Done when:   criteria 1–27 hold — tests with stand-ins, no live call — and `make verify` is green
Appetite:    8 h of phase 4, one repair round included; phase 4 starts only after pull request #60 is merged
Not now:     MiMo in other phases, OpenRouter, a live call; your Xiaomi account, key and declaration (yours, after the merge)
Pre-mortem:  suppose it failed: most likely because Xiaomi's endpoint refuses what Claude Code sends it, so every round falls back to GLM alone
Starts unless you say stop.
```

Implements `spec.md` (criteria 1–27). **Implementation waits for the merge of
pull request #60**, whose runner this change extends; slice 0 checks it. It
assumes `[DECISION]` 1 answered "ok" (pay per use) and the ADR question
answered "yes, a new ADR"; where another answer changes a step, the step says
so (*D1 option 2*, *ADR in place*). Stage 1: no model markings; phase 4 runs on
Sonnet 5.5 at effort `medium` (§3 — the Flash verb does not exist). **No real
call:** no step starts `claude` against a model endpoint; every test uses the
stand-in.

| Slice | What | Criteria | Estimate |
|---|---|---|---|
| 0 | before phase 4: #60 merged, `origin/main` merged in, answers recorded | — | 15 min |
| 1 | the declaration and the clearing | 1–4 | 45 min |
| 2 | a round with two reviewers | 4–18, 22 | 2 h 45 min |
| 3 | `Also raised` and the release | 19–21 | 1 h 30 min |
| 4 | doctrine, prompts, `AGENTS.md`, the ADR | 23–26 | 1 h 15 min |
| | **total** | | **about 6 h 30 min** |

**Appetite 8 h:** the slices and one repair round. Neither `decisions.md` nor
`spec.md` states one. The GLM loop of #60 was estimated at 4 h 30 min for
building the path this change reuses; this change adds a second caller, a
column and a fallback to it. If slice 2 passes 3 h 30 min, the session stops
after its current step, commits green and reports: an overrun there says the
record's design is wrong, not that more hours are needed.

Each slice is one session that ends with the verification command green, a
commit and a push. Each test's fault (the last column of "Test per criterion")
is planted once, seen red and restored; the slice's commit message lists them.

## Decided in phase 3

No `[DECISION]` beyond the spec's two questions. `[DETAIL]`s:

- **Clear first, then note.** `begin_call` splits into `clear_call(ctx,
  endpoint, prompt)` — the declaration, the leak check and its printed
  verdict, `Refused` when not clean — and `note_call(ctx, verb, endpoint,
  result)`, the `findings.md` line. The Codex verbs call the two in a row.
  The loop clears GLM, then MiMo, then notes both: criterion 12 needs both
  checks before any line.
- **One builder for both Claude Code calls.** `claude_env(base_url, model,
  key, config_dir)` replaces `glm_env`, and `claude_command(change,
  prompt_file, model, effort)` builds the arguments. Both calls use them, so a
  setting cannot stand in one and be missing from the other (criterion 7).
- **At the same time:** a `concurrent.futures.ThreadPoolExecutor` of two, one
  `launch` each. `launch` gains `timeout: float | None = None` for
  `subprocess.run`, which kills the child on expiry; its `TimeoutExpired`
  becomes `CallFailed("no answer within 30 minutes")`.
- **Loop columns:** `LOOP_COLUMNS = [*ROW_COLUMNS, "Also raised"]` and
  `RELEASED_COLUMNS = [*LOOP_COLUMNS, "Phase 6"]`; Codex's tables keep
  `ROW_COLUMNS`. The last place keeps cells 0–8 where they are read today.
- **Headings:** `ROUND_HEADING = re.compile(r"^## Round (\d+) — (GLM|MiMo),",
  re.M)`; rounds are counted as distinct numbers. A round without a MiMo
  heading — a record begun before this change — counts as GLM alone; its
  nine-cell rows are refused by the existing damaged-row rule, which names
  each id, and the implementer adds `| — |`. No migration code.
- **Texts:** `MIMO_NOT_REVIEWED = "MiMo did not review this round:
  {cause}."`; `RELEASE_HEADING = "## Phase 4b — loop rows, released"`;
  `NO_LOOP_LINE = "Loop rows: none — the review loop did not run for this
  change."`; `TALLY = "Disagreement: only GLM raised {a}, only MiMo raised
  {b}; raised by both: {c} of GLM's rows, {d} of MiMo's; MiMo did not review
  {e} of {n} rounds, in which GLM raised {f}."`
- **Causes, word for word** (criterion 16): `the declaration does not clear
  it (<problem>)`, `MIMO_KEY is not in the secrets file`, `the call could not
  start`, `the call failed with exit <n>`, `the answer is empty`, `no answer
  within 30 minutes`.
- **The stand-in** writes one JSON file per call under `<bin>/calls/` (start
  time in nanoseconds and pid in the name) instead of appending to the shared
  `calls.jsonl`, because two calls now run at once. Its scenario key
  `claude:<model>` comes before `claude`, with the step index counted per key;
  a step may `sleep` seconds; it records `record_at_start`, the loop record's
  text when it starts (from `XDG_STATE_HOME`).
- **`enable_mimo(world)`** fills `personal_use_declaration` in the fixture's
  copy of `model-endpoints.yaml` and adds `MIMO_KEY` — a second invented key —
  to its secrets file. The real file's empty declaration keeps every existing
  test GLM alone.
- **`declared_on`** may be a YAML date or a `YYYY-MM-DD` string; `statement`
  a string that is not blank.

## Slice 0 — before phase 4 (15 min)

1. `gh pr view 60 --json state -q .state` prints `MERGED`. Otherwise stop:
   phase 4 does not start.
2. `git fetch origin && git merge origin/main` on `feat/stage2-mimo`. A
   conflict outside `plans/changes/stage2-mimo/` stops the session and is
   reported, not resolved by guess.
3. `decisions.md` records the answer to `[DECISION]` 1, and
   `decisions/answers/stage2-mimo/adr.yaml` exists — the maintainer's answer,
   recorded with `python3 scripts/harness.py decide adr`. Otherwise stop.
4. The ADR number: the next one that neither `git ls-tree --name-only
   origin/main docs/adr/` nor a branch `origin/decide/*` holds (0011 on
   2026-10-07). If it differs, slice 4 and phase 7 use it.

## Slice 1 — the declaration and the clearing (criteria 1–4, 45 min)

**`model-endpoints.yaml`** — after the `openai-codex` entry:

```yaml
  - name: xiaomi-mimo
    betreiber: "Xiaomi Technologies Singapore Pte. Ltd.; Xiaomi Technology Netherlands B.V. for the EEA"
    residenz: anbieter-erklaert
    abrechnung: token
    darf_sehen: [framework]
    modelle:
      - mimo-v2.6-pro
    bemerkung: >-
      Xiaomi's own MiMo API Platform at its Anthropic-compatible address
      (`https://api.xiaomimimo.com/anthropic`), through Claude Code, for the
      review loop (phase 4b) only, beside GLM, through `python3
      scripts/stage2.py review-loop`; pay per use, the maintainer's account.
      For an account outside China Xiaomi states: data hosted in the
      Netherlands and Singapore — for an EEA account stored in the
      Netherlands, transferable to Singapore and to affiliates and service
      providers outside the hosting region; "Xiaomi will not use the content
      you provide for model training or any other purposes"; kept "for the
      period necessary", no period stated. An account in China falls under
      other terms, which store data in China. Read on 2026-10-07 in Xiaomi's
      privacy policy for users outside China and its service agreement of
      2026-07-07 (research of the change stage2-mimo).
    # Filled by the maintainer only, after the pull request that declares
    # this endpoint is merged; an agent never writes it. Until both values are
    # set the runner does not call MiMo. The statement covers: personal use,
    # to be obtained again on the three conditions below for GLM and Codex;
    # an account registered outside China; and that MIMO_BASE_URL in
    # scripts/stage2.py is the address the account's console shows.
    personal_use_declaration:
      declared_on: null
      statement: null
```

In the comment block "Nutzungszweck", after the paragraph of 2026-09-30, one
English paragraph dated 2026-10-07: the Xiaomi account behind `xiaomi-mimo` is
declared in that entry's `personal_use_declaration`, by the owner, after the
merge, on the same three conditions. *D1 option 2:* `abrechnung: abonnement`,
the address `https://token-plan-ams.xiaomimimo.com/anthropic`, and the remark
names the Token Plan's limit to programming tools.

**`scripts/stage2.py`** — beside `GLM`: `MIMO = ("xiaomi-mimo",
"mimo-v2.6-pro", "max")`, `MIMO_BASE_URL =
"https://api.xiaomimimo.com/anthropic"` (*D1 option 2:* the Amsterdam
address), `MIMO_TIME_LIMIT = 30 * 60`. `personal_use_problem(entry)` returns
`no personal-use declaration`, `the personal-use declaration has no date` or
`the personal-use declaration has no statement`, or `None`;
`declaration_problem(root, endpoint, model, personal_use=False)` asks it last
when told to.

**`tests/test_stage2.py`** — the tests of criteria 1–3 and the first test of
criterion 4 in the table below. Commit.

## Slice 2 — a round with two reviewers (criteria 4–18, 22; 2 h 45 min)

**`scripts/stage2.py`**

1. The module docstring: MiMo beside GLM in phase 4b, the fallback, the time
   limit, `MIMO_KEY`.
2. `clear_call`, `note_call`, `claude_env`, `claude_command` and `launch(…,
   timeout=None)` as decided above; the GLM path moves onto them with the same
   effect (the tests of #60 hold it).
3. `mimo_cause(root)` — the declaration with `personal_use=True`, then
   `MIMO_KEY`; the cause text, or `None`.
4. `review_loop`, in this order: `preflight` as today; the round limit and the
   undecided rows; `GLM_KEY` (the refusal as today); `cause =
   mimo_cause(root)`; the diff and the one prompt as today; `clear_call` for
   GLM, then for MiMo unless `cause`; `note_call` for each cleared one; per
   call its own prompt file and empty configuration directory in one temporary
   directory; both `launch`es at once, MiMo's with `MIMO_TIME_LIMIT`. GLM's
   result is handled as today; when it failed and MiMo answered, the runner
   prints `MiMo's answer of this attempt is not kept.` to standard error
   before raising. A MiMo failure becomes `cause`, and the tail of its
   standard error is printed scrubbed of its key. Rows are numbered on (GLM
   `1..n`, MiMo `n+1..`) with `Also raised` per criterion 19. The record gets
   `## Round N — GLM, <date>` with GLM's parts, then `## Round N — MiMo,
   <date>` with MiMo's parts or `MIMO_NOT_REVIEWED`. It prints `review-loop:
   round N written to <path>: GLM <a> rows, MiMo <b> rows` or `…, MiMo did not
   review: <cause>`.
5. The record reads ten cells from here on: `_record_lines` resets at either
   heading; `rounds_run` counts distinct numbers; `record_rows` returns
   `[*cells[:7], " \\| ".join(cells[7:-2]), cells[-2], cells[-1]]` and
   refuses a row of fewer cells as today; the furniture of `kept_lines` is the
   `LOOP_COLUMNS` table; `RECORD_INTRO` gains one sentence on `Also raised`;
   `RELEASE_HEADING` and `NO_LOOP_LINE` take their new texts.

**`tests/test_stage2.py`**

6. The stand-in and `World` as decided: `World.calls(name=None, model=None)`
   reads the per-call files in start order; the line that unlinks
   `calls.jsonl` (today line 712) removes `<bin>/calls/` instead; `enable_mimo`
   and the second invented key.
7. The existing helpers to ten cells: `write_record` (its rows end in `—`,
   built with `LOOP_COLUMNS`), `decide_record`'s pattern, the pattern in
   `test_a_third_round_is_refused`; the `Phase 6` cell read as `[-1]` (today
   lines 742–744 and 933); the release heading's new text (line 929).
8. The tests of criteria 5–18 and the round test of criterion 4 in the table
   below; `test_the_runner_finds_only_stand_ins`
   and `test_the_suite_never_reaches_the_real_denylist_or_secrets` run once
   more with `enable_mimo`. Commit.

## Slice 3 — `Also raised` and the release (criteria 19–21; 1 h 30 min)

**`scripts/stage2.py`**

1. `alone_rounds(record)` — the rounds with a GLM heading whose MiMo heading
   is missing or opens with `MiMo did not review`, read from the runner's own
   lines only (`_record_lines`).
2. `undecided(rows, alone)` — today's rule, or an `Also raised` that is none
   of: `no`; `—` in a round of `alone`; comma-separated ids of the other
   reviewer's rows of the same round, each naming this row back. The refusal
   names the row and why (`L1-2: Also raised names L1-1, which does not name
   it back`). `review_loop`, `review` and `release` pass
   `alone_rounds(record)`.
3. `release` writes the table in `RELEASED_COLUMNS`, `Rounds run:` (distinct
   numbers), the `TALLY` line and the kept lines — the cause lines are the
   runner's and are kept. `fill_marks` reads `len(RELEASED_COLUMNS)` as
   today.

**`tests/test_stage2.py`** — the slice-3 tests of the table below. Commit.

## Slice 4 — doctrine, prompts, `AGENTS.md`, the ADR (criteria 23–26; 1 h 15 min)

- **`docs/WORKFLOW.md`** — §2, "The evidence rule": "A Codex, GLM or MiMo
  finding". §4: the heading `## 4 · Stage 2 — Codex, GLM and MiMo (active for
  framework content)`; the opening paragraph names MiMo-V2.6-Pro
  (`mimo-v2.6-pro`, Xiaomi) beside GLM in the loop; the class table's 4b
  cells read `GLM and MiMo`; the 4b routing row keeps `**GLM 5.3**`, and its
  last cell adds "; beside it MiMo-V2.6-Pro (`mimo-v2.6-pro`), effort `max`,
  through Claude Code against Xiaomi and the runner"; the verb `review-loop`
  reads "GLM and MiMo, one round of phase 4b"; "What every call then carries"
  adds MiMo's start and `MIMO_KEY`; "The review loop (phase 4b)" gains one
  paragraph — the same prompt, at the same time, neither sees the other,
  `Also raised`, the fallback and its 30 minutes; "Two columns" names MiMo
  among the reviewers and adds `Also raised` for loop rows; "Measuring": "a
  taken Codex, GLM or MiMo finding".
- **`prompts/04b-review-loop.md`** — the `**Model:**` line keeps `GLM 5.3 —`
  first (the resolver of `tests/test_model_endpoints.py` reads up to the dash)
  and names MiMo beside it; "For the implementer": the evidence rule names
  MiMo, a step for `Also raised`, one sentence on the fallback.
- **`prompts/04-implement.md`** — "Codex, GLM and MiMo report findings … A
  finding of any of them is taken only when …".
- **`prompts/06-review.md`** — "The loop rows are the findings of GLM and
  MiMo, the reviewers of the loop before this phase".
- **`AGENTS.md`** — the stage-2 sentence: "a reviewer, Codex, GLM or MiMo".
- **`docs/adr/0011-mimo-reviews-beside-glm-in-the-loop.md`** (new) — the
  header and sections of ADR 0007 (`provenance: human-decided`, `review`
  empty, ADR 0008); "Amends ADR 0007 (decisions 1, 2 and 4); supersedes no
  ADR"; Context: the request of 2026-10-06, the answers of 2026-10-07, what
  Xiaomi states (research, C); Decision: the points of criterion 26; Options
  considered: its five options and the chosen one; Consequences: nothing
  leaves before the merge and the declaration, a third vendor's unconfined
  reads, the cost per round, the address confirmed by the maintainer;
  Validation: the tests. *ADR in place:* no new file — ADR 0007's title,
  decisions 1, 2 and 4 and its options gain MiMo, and the needle `neither
  endpoint` of `test_d13_is_amended_by_adr_0007` becomes `none of the three
  endpoints`.
- **`tests/test_stage2.py`** — `class_table_problems` expects `GLM and
  MiMo`; the slice-4 tests of the table below.
- **Close:** `implementation_status: partial` in this folder's artefacts,
  `python3 scripts/plans_registry.py --index`, `python3
  scripts/check_frontmatter_current.py --stamp`, the verification command.
  Commit.

## Phase 7 — the pull request

A decision pull request (house rule 8): title `decide(stage-2): MiMo reviews
beside GLM in the review loop (ADR 0011)`, label `decision`, body from
`.github/PULL_REQUEST_TEMPLATE/decision.md`, naming bead coding-harness-ymx.
It says that no MiMo call ran and that the declaration is empty, and lists the
maintainer's steps after the merge: an account registered outside China, a
top-up, an `sk-` key as `MIMO_KEY` in `~/.config/cc-routing/secrets.env`, the
console's address compared with `MIMO_BASE_URL`, then
`personal_use_declaration` filled in a pull request of its own.

## Verification command

```sh
export PATH=/Users/mikypiky/.venvs/portfolio-agentic-engineering/bin:$PATH
python3 -m ruff format --check scripts/ tests/ && python3 -m ruff check scripts/ tests/
python3 -m pytest tests/test_model_endpoints.py tests/test_stage2.py tests/test_leakcheck.py -q
python3 scripts/check_decision_continuity.py
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
```

Expected after slice 4: every test passes, the continuity check as before,
`VERIFY GREEN`. Without `decisions/answers/stage2-mimo/adr.yaml` the gate
`adr-answers` is red, and only it.

## Test per criterion

`S` = `tests/test_stage2.py`, `M` = `tests/test_model_endpoints.py`.

| # | Test | Goes red when |
|---|---|---|
| 1 | S `test_xiaomi_mimo_is_declared_as_decided`; M's endpoint tests as they stand | a value missing or different; `kundencode` seen; a second model |
| 2 | S the same test: the remark holds `Claude Code`, `phase 4b`, `Netherlands`, `Singapore`, `model training`, `no period`, `China`, `2026-10-07` | a needle removed from the remark |
| 3 | S `test_the_personal_use_declaration_is_the_maintainers_field` (both keys; both values `null`, or a date and a statement; the comment above holds `only`, `after`, `outside China`, `MIMO_BASE_URL`); review of the diff for set values | the key or a comment point removed; `declared_on: yesterday` |
| 4 | S `test_a_declaration_without_a_filled_personal_use_does_not_clear_mimo` (on `declaration_problem`); S `test_mimo_is_not_called_unless_cleared` (a round per case: entry missing, model absent, no `framework`, `nicht-erklaert`, empty declaration, blank statement, date `soon`) | the personal-use check dropped, or reduced to "the key exists" |
| 5 | S `test_a_round_calls_glm_and_mimo_once_with_one_prompt` | MiMo's prompt built apart with two parts swapped; a second MiMo call |
| 6 | S `test_neither_reviewer_sees_the_others_answer` (answers carry `GLM-MARK-1`, `MIMO-MARK-1`; each stand-in scans `record_at_start`, `findings.md` and the worktree) | GLM's block written to the record before MiMo is launched |
| 7 | S `test_the_mimo_call_is_the_glm_call_at_xiaomi` (arguments equal once model and prompt-file path are masked; environments equal once address, key, model variables and configuration directory are masked; the address is `MIMO_BASE_URL`; effort `max`) | `--restricted` dropped from the MiMo call only; effort `high` for MiMo |
| 8 | S `test_no_key_on_a_command_line` (both calls of a round; no 8-gram of either key in the arguments) | the key passed on the command line as `--settings` JSON |
| 9 | S `test_each_call_carries_its_own_key` | MiMo's environment built by updating GLM's |
| 10 | S `test_the_mimo_credential_never_leaves_the_runner` (the stand-in echoes its key on both streams, exit 0 and exit 1) | MiMo's output scrubbed with GLM's key |
| 11 | S `test_each_mimo_call_runs_its_own_leak_check` (`leakcheck.check` wrapped: two checks a round, both before the first call file appears, the second over MiMo's prompt) | one check for both calls; MiMo's check after the launch |
| 12 | S `test_a_check_that_is_not_clean_starts_no_call` (the wrapped second check not clean) | GLM's line noted before MiMo's check; GLM launched before it |
| 13 | S `test_every_call_leaves_its_line_in_findings`, extended to a round both reviewed | `note_call` skipped for MiMo |
| 14 | S `test_a_round_of_both_lands_by_reviewer` (GLM two rows, MiMo one: `L1-1` to `L1-3`, reviewers, two headings, nothing in the worktree) | MiMo's numbers restart at 1; MiMo's rows marked GLM |
| 15 | S `test_a_round_of_both_counts_once` (two rounds; the third refused, also after the release) | rounds counted by headings |
| 16 | S `test_mimo_falls_back_to_glm_alone` (per cause: not cleared, no key, cannot start — `launch` wrapped to raise for Xiaomi's address —, exit 1, empty answer) | MiMo's `CallFailed` let through; the cause missing from the record or the output |
| 17 | S `test_a_mimo_call_past_its_limit_is_stopped` (`MIMO_TIME_LIMIT` 1 s, the stand-in sleeps 30 s; the run ends within 20 s, exit 0) | no `timeout` passed to MiMo's `launch` |
| 18 | S `test_a_failed_glm_call_writes_nothing_even_when_mimo_answered` | MiMo's block written although GLM failed; exit 0 |
| 19 | S `test_also_raised_is_prefilled_as_the_round_requires` (both: empty; the other without rows: `no`; GLM alone: `—`) | `—` written in every round |
| 20 | S `test_an_unmatched_also_raised_holds_the_loop` (empty, `maybe`, own reviewer's id, another round's id, not named back, `—` in a round both reviewed); S `test_a_matched_also_raised_passes` (`no`; ids both ways; two ids) | any non-empty cell accepted; the name-back check dropped |
| 21 | S `test_release_records_the_disagreement` (a fixed record: the tally's numbers, each cell, the cause line in `findings.md`) | MiMo-only rows counted as GLM's; the cause line dropped from the kept lines |
| 22 | S `test_the_runner_finds_only_stand_ins`, `test_the_suite_never_reaches_the_real_denylist_or_secrets`, both with `enable_mimo` | the fixture reading the real secrets file |
| 23 | S `test_mimo_is_named_in_phase_4b_only` (MiMo in §4's 4b row, class table and loop section, `04b`, `06`, `AGENTS.md`; in no other routing row and no `**Model:**` line of `01`, `02a`, `04`, `06`); `class_table_problems` with `GLM and MiMo` | MiMo removed from `06-review.md`; MiMo planted in the 2a row |
| 24 | S `test_the_evidence_rule_stands_where_findings_are_taken`, extended: the rule's sentence names MiMo in all three texts | "A Codex or GLM finding" back in one text |
| 25 | S `test_the_stop_rule_counts_mimo` (§4 "Measuring" holds "Codex, GLM or MiMo finding") | the old wording back |
| 26 | S `test_the_mimo_adr_amends_adr_0007` (`provenance: human-decided`; `Amends ADR 0007`, `xiaomi-mimo`, `review loop`, `a request, not a lock`, `OpenRouter`, `Token Plan`, `direct API call`, `Netherlands`, `Singapore`, `falls back`); review for the rest | a needle removed |
| 27 | the verification command on the last commit | any gate red |

## Not touched

- GLM's and Codex's calls beyond moving GLM onto the shared builders; the
  tests of #60 for them stay as they are, apart from the helpers of slice 2,
  step 7.
- `scripts/leakcheck.py` (called as it is), `.claude/settings.json` (MiMo,
  like GLM, is started by the runner only), `decisions/gates.yaml`,
  `.github/workflows/ci.yml`, `scripts/kit/manifest.yaml` — no new script and
  no new test file.
- `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` (unless *ADR in
  place*), `scripts/check_decision_continuity.py`, the D-13 row of
  `docs/architecture/2026-09-17-omnigent-first-target.md`.
- `tests/test_model_endpoints.py`, the German keys and comments of
  `model-endpoints.yaml`, `ROADMAP.md`, `docs/architecture/`.
- `~/.config/cc-routing/secrets.env`, the Xiaomi account, the declaration's
  values — the maintainer's.
- `research.md`, `decisions.md` and `spec.md` beyond
  `implementation_status`; the tracker.
