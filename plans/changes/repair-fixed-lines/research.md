---
title: "Research — repair-fixed-lines"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-ugi
class: bounded
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair]
---

# The repair runner's fixed-line parser — Research

Phase 1 for bead coding-harness-ugi, seeded by the orchestrating session on
2026-10-15 against `origin/main` at `135f029`.

## The question

The `repair` verb of `scripts/stage2.py` sends every taken findings row to
Codex and reads the answer's fixed lines (`check_repair_answer`). Two faults
make a usable repair fail:

1. **Any `word:` line counts as a finding id.** The parser splits each
   non-empty answer line at its first colon and takes the left part as an id.
   A line such as `expected: …`, `found: …` or `Resume: …` then fails the
   attempt with `<word>: no taken row carries this id`. Seen on 2026-10-15 in
   the pi-pin repair, attempt 2 (`plans/changes/pi-pin/findings.md` on
   `main`, the attempt-2 diagnostics: `expected`, `found`, `relevant`,
   `proposal` and `Resume` each "no taken row carries this id").
2. **A row repaired by hand is demanded again.** `repair_targets` takes every
   row whose Status begins `taken`. A row the orchestrating session repaired
   by hand keeps a Status that begins `taken — …; fixed by …` (the precedent
   in `plans/changes/haiku-5-5/findings.md` and the pi-pin phase-6 table),
   so the next repair call asks for it again and fails with
   `<ID>: no fixed line` (haiku-5-5, 2026-10-15, row L1-1).

Needed (bead text): rows already repaired are not demanded again, and only
lines whose id is a taken row's id count as fixed lines.

## Known so far (read, not run)

- `REPAIR_ANSWER` (around line 221) asks for "one fixed line per row and no
  other text"; the parser enforces "no other text" by failing on any line
  without a colon, and by failing on any colon line whose left part is no
  taken id.
- `check_repair_answer` (around line 2202) collects `parsed[ident]` for every
  colon line; ids left over after the taken rows are matched become problems.
- `fixed_status` (around line 2179) accepts `fixed — tests/<path>::<function>`
  and `fixed — not a test — <reason>`.
- `repair_targets` (around line 1034) reads Status by prefix only: `taken`,
  `rejected`, `fixed`, blank or `open`.
- Loop row ids follow `L<n>-<m>` (`LOOP_ID`); phase-6 table ids are free
  text such as `F-1`.

## To explore

How the answer parser can tell a fixed line from prose without accepting a
malformed answer as clean (which words or shapes count as an id; whether
prose lines are ignored, named once, or still fail); how a hand-repaired row
should be recorded so `repair_targets` skips it (a Status that begins
`fixed`, or a recognised `taken — …; fixed by …` form), and what the existing
records on `main` already hold; which tests in `tests/test_stage2.py` pin the
current parser and target selection; and what `docs/WORKFLOW.md` and the
repair prompt say about the answer format.

Stage-2 call, 2026-10-15: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 458 files, 1276 commits, 12 rules.

## Runner exploration — 2026-10-15

Phase 1 complete. Here is the prose, ready to append to `plans/changes/repair-fixed-lines/research.md` (English, as the repository requires; every statement with its source):

```markdown
## Runner exploration — 2026-10-15

**What exists today.** The answer handling has four moving parts in
`scripts/stage2.py`. `REPAIR_ANSWER` defines the answer text ("Answer with one
fixed line per row and no other text") and is embedded in both attempt
prompts, `REPAIR_FORMAT` (the Codex attempt, which adds the measured time
entry and the no-commit rule) and `REPAIR_FORMAT_FILE_TOOLS` (the stage-1
attempt). `repair()` collects targets through `repair_targets`, refuses on
waiting or doubled ids before any call, and passes `check_repair_answer` to
`run_attempts` as the `answer_check`, together with the fixed taken list, the
baseline and the pre-call findings snapshot. `check_repair_answer` reads the
answer line by line: it strips a leading list marker, splits each non-empty
line at its first colon, strips `*` and backticks from the left part, reports
a line without colon or id as "the answer holds a line that is no fixed
line", and after matching the taken rows reports every leftover id as
"`<id>`: no taken row carries this id"; a taken row with no entry is "no
fixed line", with two entries "several fixed lines". `fixed_status` accepts
exactly `fixed — tests/<path>::<function>` (file `tests/…/test_*.py`,
function `test_…`, no `.`/`..` segment) and `fixed — not a test — <reason>`.
On success `mark_repaired_findings` and `mark_repaired_record` overwrite only
the Status cell of a row whose other cells still match the pre-call reading.

**Where the prose lines come from.** `repair_prompt` builds every attempt
prompt through `work_prompt`, which inlines the whole of
`prompts/04-implement.md` and `AGENTS.md`. That prompt teaches, in its "The
plan is the contract" and appetite sections, the four-line report
`expected: … / found: … / relevant: … / proposal: …`, and under "The last
line says how the session ended" a closing `Resume: when I start, I will
<one action>`. The five stray ids in both recorded failures are exactly these
labels (`plans/changes/haiku-5-5/findings.md`, attempt-1 and attempt-2
diagnostics; `plans/changes/pi-pin/findings.md`, attempt-2 diagnostics, there
beside `F-1` to `F-14` as "no fixed line"). `REPAIR_ANSWER`'s "no other
text" and the embedded prompt's own report formats stand in the same prompt
text.

**Where the behavior is pinned.** Tests: `test_each_taken_row_needs_exactly_one_fixed_line`
in `tests/test_stage2.py` (parametrized "missing", "doubled", "unknown"; the
unknown case expects "`L9-9`: no taken row carries this id" in attempt 2's
prompt), `test_a_code_row_answered_not_a_test_fails_the_attempt`,
`test_a_reason_with_a_pipe_is_escaped_once_as_its_fixed_line_gives_it`. A
search of `tests/` for the no-colon sentence and for "no other text" found no
test for that problem. Specs: `plans/changes/stage2-repair/spec.md` defines
"Fixed line" in its vocabulary and its criterion 15 fails an answer that
"holds a fixed line for an ID that is no taken row";
`plans/changes/codex-repairs/spec.md` restates the fixed-status bookkeeping
(its criteria 14 to 16) but, per a search of that file, carries no criterion
of its own on unknown ids. `docs/WORKFLOW.md` §4 "Repairing taken findings
(repair)" states the answer form, as do the "Repair." paragraph of
`prompts/04-implement.md` and ADR 0017's decisions 3 and 4 ("Fixed rows read
`fixed — …`").

**Order and cost of the check.** In `run_attempts`, `verify_attempt` (ruff
and `make verify`) runs first and `answer_check` runs only when it found no
problems, so one prose line fails the attempt only after a green
`make verify`; the diagnostics put the runner-format line first, and the
failed attempt's findings.md edits are restored before the quoted block is
appended (visible in the haiku-5-5 attempt-2 diagnostics, which open with
"Runner format before `make verify`").

**How statuses are read elsewhere.** `repair_targets` demands every row whose
Status begins `taken` — of the record (`record_rows`), of every released
block and of every phase-6 table (`findings_rows`); `rejected` and `fixed`
are skipped; a record row with another prefix, and a phase-6 row blank or
`open`, wait and refuse the verb; a released row with any other status is
skipped without waiting. `taken_in_round`, `undecided` and
`undecided_refusal` accept the `fixed` prefix as the decided, round-counting
form, and a `fixed` row without its `Broke a test` mark is undecided with its
own refusal sentence. The hand-repair precedents keep the `taken` prefix:
haiku-5-5's tables carry `taken — criterion 2: …; fixed by
tests/test_stage2.py::…` (F-1, F-2) and `taken — not a test — metadata: …;
repaired by the orchestrating session` (L1-1), pi-pin's phase-6 table carries
`taken — …; fixed: …` forms (F-5, F-8, F-9, F-10, F-13, F-14) — both repair
failures demand exactly these rows again. The `taken — …; fixed by …` form is
defined in no prompt and no doctrine file: a search of `prompts/` and
`docs/` finds it only inside the findings records themselves, plus one
research note (`docs/research/2026-10-08-stage2-three-runs.md` names an
earlier repair "repaired by hand" after the Sonnet fallback).

**The sibling parser.** `parse_marks` reads the loop-marks answer with a
regex anchored on the id shape (`LOOP_ID`, `L<n>-<m>`) and silently skips
every line that does not match; an unmarked row surfaces as "no answer" in
`fill_marks`, not as a failed call. Phase-6 ids are free text (`F-1`), so the
taken rows' own ids are the only complete key the repair verb holds.

**What is unclear.** Whether answer prose besides fixed lines is legitimate
or must fail — `REPAIR_ANSWER` says "no other text", nothing else I read
settles it. How the pi-pin attempt 1 failed — I read attempt 2's and 3's
audit lines and attempt 2's diagnostics only. Whether any recorded
hand-repaired row anywhere uses a Status beginning `fixed` — I searched only
the two findings files named above. The exact cells of `ROW_COLUMNS` I did
not read; `findings_rows`' docstring states nine cells for phase-6 rows and
ten for released rows.

**Files a change would have to touch.** `scripts/stage2.py`
(`REPAIR_ANSWER`/`REPAIR_FORMAT`, `check_repair_answer`, `fixed_status`,
`repair_targets`, `repair_prompt`); `tests/test_stage2.py` (the repair block
from the criterion-15 test through
`test_a_failed_repair_writes_no_fixed_status`); the prose that states the
format: `docs/WORKFLOW.md` §4 repair paragraph and `prompts/04-implement.md`
("Repair." paragraph; the stop-report formats live in the same file). The
unknown-id failure is pinned by criterion 15 of
`plans/changes/stage2-repair/spec.md`, a dated change spec; the live decision
record for the repair route is ADR 0017 (`docs/adr/0017-codex-repairs-taken-findings.md`).
```

**Where we are:** Exploring (Phase 1) for `repair-fixed-lines` is finished — all facts about the parser (`check_repair_answer`), target selection (`repair_targets`), the prompt conflict (`prompts/04-implement.md` teaches `expected:`/`found:`/`Resume:` lines while `REPAIR_ANSWER` forbids them), the hand-repair precedent statuses, and the pinning tests/specs are collected above.

**Next step for you:** append the block to `research.md`, commit on `explore/repair-fixed-lines`, and continue with Phase 1a (interview; class *bounded* per the seed's frontmatter — minimum 1 topic or a reasoned skip).

**Needed from you:** nothing right now.

## Draft gap checks — 2026-10-15

Read at draft baseline `b3e5810`:

- `scripts/stage2.py` defines `LOOP_ID` as `L\d+-\d+`; phase-6 rows keep
  their free-text identifiers. Exact active identifiers must therefore be
  recognized before applying a shape filter to unknown identifiers.
- `repair` obtains all selected rows before dispatch, and `repair_targets`
  already excludes statuses beginning `fixed` in every row location. The
  legacy-marker check can refuse before an attempt without changing target
  selection or adding status vocabulary.
- `tests/test_stage2.py` supplies deterministic repair and row-building
  helpers plus existing missing/duplicate/unknown, test-reference and
  red-first regressions. Add cases there without renaming tests referenced
  by other changes' ledgers.
- `templates/` has no plan template, and
  `scripts/validate_change_artefacts.py` is absent. The phase-3 prompt supplies
  the plan form; the existing interview and criterion-ledger checks remain
  available. `scripts/plans_registry.py --check` delegates tracker reads to
  `scripts/bead_render.py`; it is left to the runner because this draft may
  read only the worktree and repository git directory.
- The change's `findings.md` holds the draft call's audit line and no
  phase-2a review rows to resolve.
