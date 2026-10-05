---
title: "Findings — research-currency"
category: findings
created: 2026-10-05
updated: 2026-10-05
status: draft
implementation_status: partial
date: 2026-10-05
last_reviewed: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-pu9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, docs-research, drift-job, frontmatter]
---

# Findings — research-currency

Phase 6, round 1, on commit `1b0c85c` (branch `feat/research-currency`,
eight commits over `origin/main` at `87daf91`), 2026-10-05. The reviewer ran
on Opus 5.5 in a fresh context, wrote nothing but this file and the
regenerated `plans/INDEX.md`, opened no pull request and wrote nothing to the
tracker. Measured against `spec.md` (criteria 1–16, the non-goals and "What
part 2 may rely on") and `decisions.md` with its addendum of 2026-10-05;
`plan.md` was read for its revisions, its planted faults and its evidence,
not as the yardstick. Phase 2a was skipped, so its three questions are
answered here as rows of dimension `SPEC`. `templates/findings.md` does not
exist on `origin/main`; the columns are those of the earlier `findings.md`
files.

**Verdict: no BLOCKER, no `[AMBIGUITY]`, no `[DIVERGENT]`.** Five MINOR, all
open; none stops the pull request. Two are holes in the tests — a planted
fault in the order and one in the choice of key both leave all 68 tests
green while the code itself is right. Three are edge cases of the header
reader that the spec does not name.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | MINOR | SPEC | base | `tests/test_research_currency.py`, `_order_tree` and `test_unusable_first_then_oldest_then_path` | The order of the unusable notes among themselves is not held to the path. Planted on `1b0c85c`: the sort key in `measure` gains the reason before the path — `(n.problem is None, n.last_reviewed or date.min, n.problem or '', n.path)` — and all 68 tests pass. The fixture's two unusable notes (`a-empty.md`, reason "last_reviewed is empty"; `z-nokey.md`, "no last_reviewed") sort the same way by reason and by path, so the suite cannot tell the two keys apart. The code is right: on a tree with `a.md` (no key) and `b.md` (empty value), measured, `a.md` comes first although its reason sorts second. One more unusable note whose reason sorts against its path closes the hole. [criterion 5] | fixed in `7813046` — reviewed at `8380d7c`, closed: `_order_tree` now opens with `1-nokey.md`, whose path sorts before `a-empty.md` and whose reason ("no last_reviewed") sorts after that note's ("last_reviewed is empty"), so path and reason disagree. Replayed on `8380d7c`: fault 57 (the reason before the path) turns `test_unusable_first_then_oldest_then_path` red, 1 of 84; an own variant that leaves the unusable notes in the order the file system hands them over turns the same test red. No code change |
| F-2 | MINOR | SPEC | base | `tests/test_research_currency.py`, `test_the_review_date_is_last_reviewed_and_nothing_else` and the `no-key` case of `UNUSABLE` | A reader that falls back to `created:` when `last_reviewed:` is missing is not caught. Planted on `1b0c85c`: `review_date` takes `header.get("last_reviewed", header.get("created"))` and says "no last_reviewed" only when both keys are missing — all 68 tests pass. No fixture has a `created:` without a `last_reviewed:`; the `no-key` case carries `updated:` only, which is why the same fallback to `updated:` is caught. Under the fault a note with `created: 2026-10-01` and no review date would be listed as reviewed four days before 2026-10-05 instead of due with "no last_reviewed". A `created:` line in the `no-key` case closes the hole. [criterion 2] | fixed in `7813046` — reviewed at `8380d7c`, closed: the `no-key` case carries `created:` beside `updated:`. Replayed on `8380d7c`: fault 58 (the fallback to `created:`) turns `test_an_unusable_review_date_is_due_with_its_reason[no-key]` red, 1 of 84. The sibling fallback to the `review:` block's `approved_at` still passes — F-7 |
| F-3 | MINOR | MAINT | base | `scripts/check_research_currency.py`, `review_date`, the YAML load | Two top-level `last_reviewed:` lines in one header give no reason: PyYAML keeps the last one without a word. Measured with `review_date` on 2026-10-05: `last_reviewed: 2026-10-01` followed by `last_reviewed: 2026-01-01` reads as 2026-01-01, the reverse order as 2026-10-01, and neither note carries a problem. The sibling reader of the same headers refuses this case for `updated:` (`scripts/check_frontmatter_current.py`, `DUPLICATE`, "no way to tell which one is meant"). Not `[DIVERGENT]`: no other script judges the `last_reviewed:` of a research note, and criterion 4 lists the unusable cases one by one without a doubled key, so the spec is met (see 2a-1). Recorded because the re-check of part 2 is to set exactly this key, and a doubled line would decide by its position which date counts. | fixed in `4c39587` — reviewed at `8380d7c`, closed: `_read_header` counts the `last_reviewed` keys of the top-level mapping node before the mapping is built, so two keys give "last_reviewed appears more than once (no way to tell which one is meant)" in either order, with the same date, with one key quoted and inside a flow mapping; a key in the `review:` block is not counted. Replayed on `8380d7c`: fault 59 (the check removed) 5 red, fault 62 (column-0 lines counted) 2 red; an own variant counting the key at every depth turns `test_the_review_date_is_last_reviewed_and_nothing_else` red. Through the command line a note with two keys is due with that reason and the run exits 0. The amendment of criterion 4 stands below its refutation, dated 2026-10-05, names F-3 and renumbers nothing; `git diff f6e0f6d..8380d7c -- plans/changes/research-currency/spec.md` adds 10 lines and removes none. A `last_reviewed` merged in through `<<:` is not counted as a second key — YAML's merge rule lets the written key win, and no criterion asks otherwise — so no row |
| F-4 | MINOR | MAINT | base | `scripts/check_research_currency.py`, `_shown` and the `isinstance(value, str)` branch of `review_date` | Two inputs get a reason that calls a well-formed date "not a YYYY-MM-DD date". (a) `last_reviewed: ' 2026-09-16 '`, with spaces inside the quotes, is rightly unusable, but `_shown` collapses the spaces, so the reason reads `last_reviewed '2026-09-16' is not a YYYY-MM-DD date`. (b) `last_reviewed: !!timestamp 2026-09-16` arrives as a `date`, not as text, and gets the same reason. Both measured with `review_date` on 2026-10-05. Both notes are due, as they should be; only the reason misleads whoever repairs the header. Rare inputs; the tag-forced impossible date (`!!timestamp 2026-02-30`, "frontmatter is not a YAML mapping") is already named in `plan.md`. [criterion 4, "with a reason naming the case"] | fixed in `27840f0` — reviewed at `8380d7c`, closed except one hole in its test, which is F-6: `' 2026-12-01 '` (spaces, leading only, a trailing `\n`) now reads "last_reviewed '2026-12-01' has whitespace around the date", a `!!timestamp` date or datetime reads "last_reviewed is a !!timestamp-tagged value, not a plain YYYY-MM-DD date", and `' soon '` keeps "is not a YYYY-MM-DD date". Replayed on `8380d7c`: fault 63 (the whitespace branch removed) 3 red, fault 67 (the tag branch removed) 2 red. Measured: `' 2026-12-01 junk '` and `' 2026-12-015 '` keep "is not a YYYY-MM-DD date", as they should |
| F-5 | MINOR | MAINT | base | `scripts/check_research_currency.py`, `review_date` (`except (yaml.YAMLError, ValueError)`) and `_shown` | One pathological header ends or stalls the whole run instead of making its note due. Measured on 2026-10-05 through the command line: a `last_reviewed:` of 1,200 nested `[` makes PyYAML raise `RecursionError`, which nothing catches — exit 1, a traceback, no list for any note. And a `last_reviewed:` that is an alias of a list built from seven chained anchors of ten aliases each (`a0: &a0 [x, …]`, `a1: &a1 [*a0, …]`, …) is listed as due with its reason, but `str(value)` in `_shown` first expands it to ten million items: 1.0 s and 626 MB peak memory, and every further anchor line multiplies both by ten. The headers are written by the maintainer and the agents, and the step carries `continue-on-error: true`, so the cost is one night's missing list. Recorded because the phase-4 revision widened the `except` precisely so that "the run goes on to the next note". [criterion 4] | fixed in `c8c58b6` — reviewed at `8380d7c`, closed for both routes it measured; a third route is F-8. A `RecursionError` while reading a header gives "frontmatter is nested too deeply to read", a `MemoryError` "frontmatter is too large to read", each for its own note; `_shown` looks at a non-text value through `reprlib` (3 levels, 6 items) and no longer through `str()`; aliases are not refused, and no other exception is caught. Replayed on `8380d7c`: faults 70 (the `RecursionError` branch removed) 3 red, 73 (the `MemoryError` branch removed) 1, 74 (`str()` again) 1, 75 (`maxlevel=100`) 1; an own variant with the default `reprlib.Repr()` 1 red. Through the command line on a tree with 1,200 nested `[`, a seven- and an eight-level alias bomb, a doubled key and one good note: exit 0, every note listed, 0.40 s, 21.7 MB peak resident memory. The tests stay small: the largest fixture is 1.2 KB, and the alias-bomb test peaks at 31 KB measured (5.8 MB with `str()`) against its 400 KB bound |
| F-6 | MINOR | SPEC | fix-r1 | `tests/test_research_currency.py`, the `padded-*` cases of `UNUSABLE`; `scripts/check_research_currency.py`, the whitespace branch of `review_date` | The test of the new whitespace reason does not hold that the stripped value is a whole date. Planted on `8380d7c`: `_ISO.fullmatch(value.strip())` becomes `_ISO.match(value.strip())`, which asks only for a date at the start — all 84 tests pass. The one counter-case, `' soon '`, does not start with a date, so it cannot tell the two apart. Under the fault `last_reviewed: ' 2026-12-01 junk '` reads "last_reviewed '2026-12-01 junk' has whitespace around the date" and sends whoever repairs the header to the spaces, although the value is no date without them either. The code is right: measured on `8380d7c`, that value reads "… is not a YYYY-MM-DD date". One fixture with more than a date inside the spaces closes it. [criterion 4, "with a reason naming the case"] | open |
| F-7 | MINOR | SPEC | base | `tests/test_research_currency.py`, `test_the_review_date_is_last_reviewed_and_nothing_else` and the `no-key` case of `UNUSABLE` | A reader that falls back to the `review:` block's `approved_at` when `last_reviewed:` is missing is not caught. Planted on `8380d7c`: `review_date` takes `review.approved_at` when the top-level key is missing and says "no last_reviewed" only when both are missing — all 84 tests pass. The fixtures with a `review:` block either carry a top-level `last_reviewed:` as well (`stale-but-edited.md`) or only a nested `last_reviewed:` (`nested-only.md`), so a fallback to the nested key is caught and one to `approved_at` is not. Under the fault a note with `review: {approved_at: 2026-12-01}` and no `last_reviewed:` would be listed as reviewed instead of due with "no last_reviewed". No note under `docs/research/` carries a date in `approved_at` on 2026-10-05, so nothing is misread today. The class of F-2, found by a variant of its replay; an `approved_at` date in the `no-key` case closes it. [criterion 2, "the provenance block `review:` … never consulted"] | open |
| F-8 | MINOR | MAINT | base | `scripts/check_research_currency.py`, `_read_header` (PyYAML's merge keys) | A header built from merge keys still stalls the whole run: F-5's repair caps what `_shown` renders, not what PyYAML builds. Measured on 2026-10-05 through the command line on `8380d7c`: a 528-byte header whose seven anchors each merge ten aliases of the one before (`a0: &a0 {k0: x, …, k9: x}`, `a1: &a1 {<<: [*a0, …]}`, …), followed by a valid `last_reviewed: 2026-09-01`, takes 4.4 s and 192 MB peak resident memory; six anchors 0.46 s and 40 MB, five 0.08 s and 22 MB — ten times more per anchor line, because PyYAML's `flatten_mapping` copies every merged pair into each level before the mapping is built. The note itself is listed as usable; the cost falls on the run, and a few more lines would exhaust a runner's memory (extrapolated, not measured). The same on `1b0c85c` (4.2 s, 192 MB), so the origin is `base`. Recorded because F-5 named the class — one pathological header stalls or ends the run — and `plan.md`'s `[DETAIL]` for it says "only `str()` of the value was the cost", which holds for aliases and not for merge keys. The headers are written by the maintainer and the agents, and the step carries `continue-on-error: true`. [criterion 4, "the run goes on to the next note"] | open |
| 2a-1 | — | SPEC | base | `spec.md`, criteria 2, 4 and 10 | *Where does the spec admit two plausible readings?* One candidate, read one way: "the top-level `last_reviewed:`" (criterion 2) for a header with two such lines — "the" could make the case unusable, or leave it to YAML's own rule (the last wins). Criterion 4 lists the unusable cases one by one and a doubled key is not among them, so the list decides it; F-3 records the consequence for the maintainer instead of an `[AMBIGUITY]`. Criterion 10 ("exits 0 whenever it produces the list") was weighed against a crash (exit 1, F-5): a crash produces no list, so it lies outside the sentence; `continue-on-error` keeps it from turning anything red. No other place. | answered |
| 2a-2 | — | SPEC | base | `plan.md`, "Decided in phase 3" and "Revisions in phase 4" | *What is missing that would have to be decided while building?* Everything the build met is written down: the pattern check before `fromisoformat`, the loader that leaves a date as text (with its reason, the `ValueError` on `2026-02-30`), the autouse fixture against the hosted summary, the not-measured line on stdout in either format, singular and plural, "today" and "tomorrow", the reason cut to 80 characters, an unwritable summary, `--today` in `YYYY-MM-DD` only, the sort by the printed path, and the one-commit deviation. Not written down, and harmless: the `\|` escape in the summary table (`_cell`) and the wording of the two not-measured reasons. | answered |
| 2a-3 | — | SPEC | base | `spec.md`, criteria 15 and 16 | *Which acceptance criterion cannot go red?* Criterion 15 is one measurement on one commit and holds, by its own wording, only until 2026-12-15; no test carries it, rightly — a test over this repository's notes would turn red on the day the first review ages, and in the kit copy, which has no notes. It is held by the evidence in `plan.md` and was re-measured here. Criterion 16 is prose, read here. Every other criterion has a test that a planted fault turns red (below), except the two holes F-1 and F-2. | answered |

Reviewer session: none — phase 2a was skipped (`spec.md`, "Phase 2a not
run"); this review ran in a fresh session.

## Checked without a finding

- **Report-only never turns red (criteria 10, 12).** Exit codes measured on
  `1b0c85c`: 0 on this repository (15 notes, 0 due) and with
  `--today 2026-12-16` (4 due); 3 with the not-measured line for a missing
  corpus, a file in its place, an empty one and one holding only
  `_INDEX.md` (tests); 2 for a malformed `--today` (tests). The gate reads
  `job: drift`, `enforcement: report`, `floor: false`, `placement: both`,
  without `needs_tracker` or `needs_history`; `ci_gates._schritt` writes
  `continue-on-error: true` for every `report` gate, so exit 3, or a crash
  (F-5), marks the step and not the job. `python3 scripts/ci_gates.py
  --check-ci` answered "ci.yml ist genau die Ableitung der Gate-Datei.",
  exit 0. In `ci.yml` the step stands under `drift` only, whose `if:` is
  `schedule || workflow_dispatch`; it carries `if: ${{ !cancelled() }}`, so
  it runs even after `plans-registry-strict` fails before it (red for four
  beads outside this change, as `plan.md` says; not re-measured). The local
  runner reports it as "rot, aber nur report" and keeps its verdict green.
- **The job summary (criterion 9).** The script appends (mode `a`) a
  `### Research currency` section to the file `GITHUB_STEP_SUMMARY` names,
  the not-measured line included, and writes nothing without the variable
  (tests; replay 40 below). The tests remove the variable twice — an
  autouse fixture for in-process calls, `run()` for subprocesses — so the
  hosted `verify` job's pytest cannot write into its own summary.
- **The loader.** `_Loader` subclasses `yaml.SafeLoader`, adds no
  constructor and builds a resolver table of its own without the timestamp
  resolver. Measured: after the module is imported, `yaml.safe_load` still
  returns a `date` (the shared table is untouched), and a
  `!!python/object/apply` tag is refused with `ConstructorError`. Against
  the repository's other header readers: `check_frontmatter_current.py`
  reads `updated:` by a line pattern (quotes and a trailing comment
  allowed, a doubled line refused); `plans_registry.py` uses plain
  `safe_load`, takes a `date` or a parsable string and reads `plans/` only;
  `check_docs.py` checks that the key exists. No two of them judge the same
  key of the same file. The new reader agrees with the line pattern on
  every case criterion 4 names, and is stricter than `plans_registry.py`
  where criterion 2 asks it to be (`2026-9-6`, a timestamp). Full-width
  digits (`２０２６-０９-１６`) are refused. Its one difference in kind is
  F-3. Sharing the reader is a stated non-goal.
- **The order and the contract for part 2 (criteria 5, 8).** The key is
  `(problem is None, last_reviewed or date.min, path)`; `notes[0]` is an
  unusable note when there is one, else the oldest, ties by path. On this
  repository on 2026-10-05:
  `docs/research/2026-09-16-review-corpus-vs-running-workflow.md` first,
  then the three intake notes of the same day by path. The JSON carries
  every note with the five keys in the spec's order, `schema_version: 1`,
  and does not escape non-ASCII text. On exit 3 stdout holds the plain
  not-measured line, not JSON; `plan.md` says a consumer checks the exit
  code first.
- **`_INDEX.md` and the German intake notes (criteria 1, 16).** A
  `_`-prefixed file is skipped at any depth (test). The three German intake
  notes (`arc42_…`, `Lake-Switch-…`, `Migrationsplan_…`) are listed like any
  note: reviewed 2026-09-16, due from 2026-12-16 together with the English
  note of that day — the spec's `[DETAIL]`. The paragraph in `_INDEX.md`
  says what criterion 16 asks and contradicts neither criterion 2 nor 3;
  its stamp changed nothing, since `updated:` was 2026-10-05 on `main`
  already.
- **Kit roles and provenance (criteria 13, 14).** `probe.rolle` gives
  `mechanismus` for the script and for its test (test; replay 55).
  `scripts/ci_gates.py`, `tests/test_ci.py` and `scripts/kit/probe.py` are
  not in the diff, so `OHNE_AUFRUFER`, `OHNE_TEST`, `OHNE_MUTATIONSTEST` and
  `REIST_NICHT` are unchanged, and
  `test_the_list_notices_a_note_past_the_threshold` matches
  `MUTATIONS_NAMEN` through `notices`. `provenance.yaml` reserves no
  touched path for `human-decided` (`decisions/gates.yaml` has no entry,
  `decisions/answers/` is untouched), so the pull request is not a
  decision pull request.
- **The one-commit deviation.** Steps 1–3 landed together in `9714b0e`.
  Its reason holds, measured: with the gate entry removed and `ci.yml`
  regenerated, `tests/test_ci.py` goes red ("Without a caller and without
  a reason"). `plan.md` recorded the deviation before this review; no
  criterion changed.
- **Language and wrap.** Code, tests, the gate reason, the kit reasons, the
  commit messages and the change's documents are English. Python wraps at
  the repository's 120 (ruff green). Markdown prose wraps at 80 except
  `plan.md` line 57 (81) and `research.md` line 125 (83); `plan.md` line 56
  and the message of `59b1862` still carry a literal U+FEFF, the invisible
  character that commit took out of the code. Style, so no row.
- **Criterion 15 and the suite.** Re-measured on `1b0c85c`: exit 0, 0 due,
  the oldest named as the criterion says; with `--today 2026-12-15` still
  0 due. `make verify` on `1b0c85c` with commit signing off: VERIFY GREEN,
  584 passed and 15 skipped; `docs-links` and `markdownlint` red but
  report-only.
- **Planted faults.** Ten of the plan's 56 replayed on `1b0c85c`, each
  planted alone, the 68 tests run, the file restored with `git checkout`;
  every count matched the plan: 7 (`>=`) 3 red; 11 (`except
  yaml.YAMLError` only) 1; 18 (timestamps parsed again) 43; 21 (unusable
  notes last) 30; 27 (the UTC date) 1; 30 (the oldest line only when a
  note is due) 2; 40 (a summary file without the variable) 2; 45 (exit 1
  when a note is due) 9; 51 (`block`) 1; 55 (kit role `bestand`) 1. Own
  variants: the future slack with `>=` instead of `>` — 3 red; a hand edit
  dropping `continue-on-error: true` from `ci.yml` — `--check-ci` exit 1;
  the gate entry removed and `ci.yml` regenerated — `tests/test_ci.py`
  red; an empty `GITHUB_STEP_SUMMARY` treated as set — green, but it only
  adds a line on stderr and still writes no file, so no fault against
  criterion 9; and the two survivors F-1 and F-2.

## Not checked

No hosted run: the `drift` job was not dispatched for the branch, so the
step's log and the summary as GitHub renders it were not seen. The plan's
other 46 planted faults were not re-run. How `rglob` treats a symlinked
directory was not measured. The maintainer's session of 2026-10-05 was not
read; the class stands as `decisions.md` records it.

## For phase 7

`plans/INDEX.md` was regenerated with `python3 scripts/plans_registry.py
--index` for this file. No row stops the pull request. F-1 and F-2 are one
fixture each and fit a repair round; F-3 to F-5 can be fixed there or
closed as named limits, the maintainer's choice. The pull request names
bead coding-harness-pu9 in its body (house rule 4) and is not a decision
pull request.

## Repair round 1 (2026-10-05)

The maintainer decided to fix all five rows in this round (`decisions.md`,
addendum of 2026-10-05). Each row is set to "fixed in <commit>, not
reviewed": the repair is the author's, and no reviewer has read it. What each
repair does, the 19 faults planted against the new tests and the evidence are
in `plan.md`, "Repair round 1". Nothing above this line was changed except
the Status column.

## Phase 6, round 2 (2026-10-05)

The repair read, on commit `8380d7c`, 2026-10-05, by a reviewer on Opus 5.5
in a fresh context that wrote nothing but this file, opened no pull request
and wrote nothing to the tracker. It read the repair diff `f6e0f6d..8380d7c`
— the script, its tests, the amendment of criterion 4, the addendum of
`decisions.md` and "Repair round 1" of `plan.md` — against the five rows.
Above this section only the Status column of F-1 to F-5 changed, and rows
F-6 to F-8 were added.

**Verdict: F-1 to F-5 are closed; three new MINOR rows, F-6 of origin
`fix-r1` and F-7 and F-8 of origin `base`. No BLOCKER, no `[AMBIGUITY]`, no
`[DIVERGENT]`: nothing here stops phase 7.** F-6 is a hole in the test of
F-4's new reason; F-7 and F-8 existed before the round and were found by
variants of its replays. Because F-6 is of `fix-r1` origin, a second repair
round that again produces rows (`fix-r2`) is the escalation
`docs/WORKFLOW.md` names, not a third round.

- **Replays.** Ten of the round's 19 planted faults, each alone on a copy of
  `8380d7c`, the 84 tests run, the file restored: 57 → 1 red, 58 → 1,
  59 → 5, 62 → 2, 63 → 3, 67 → 2, 70 → 3, 73 → 1, 74 → 1, 75 → 1 — every
  count and every test name as `plan.md` records them. Own variants: the
  key counted at every depth (F-3) 1 red; the unusable notes left in the
  file system's order (F-1) 1 red; the default `reprlib.Repr()` (F-5)
  1 red; `_ISO.match` in the whitespace branch (F-4) green, which is F-6;
  a fallback to `review.approved_at` (F-2) green, which is F-7. A
  `RecursionError` net moved from `review_date` to `measure` is an
  equivalent rewrite and stays green, as it should.
- **The suite.** `make verify` on `8380d7c` with commit signing off:
  VERIFY GREEN, 600 passed and 15 skipped; `docs-links` and `markdownlint`
  red but report-only, as in round 1.
- **The 15 errors of a plain `pytest` are older than this branch.** On a
  scratch clone of `origin/main` at `87daf91`, plain `pytest` gives 15
  errors — 10 in `tests/test_worktree_state.py` and 5 in
  `tests/test_workflow_entry.py`, not all 15 in the first. Each is a
  `git commit` in a temporary repository that fails because the SSH signing
  key asks for its passphrase (exit 128). With `commit.gpgsign=false` all
  15 pass there. On `8380d7c` plain `pytest` gives the same 15 errors in
  the same two files (585 passed, 15 skipped). The clone's four further
  failures come from its tracker database not being hydrated and are
  unrelated to signing and to this branch.

Not checked: the round's other nine planted faults (60, 61, 64–66, 68, 69,
71, 72); a hosted run of the `drift` job; a merge-key header of eight or
more anchors (F-8 extrapolates); any Python but 3.12.4 with PyYAML 6.0.2.

For phase 7: no row stops the pull request. F-6 and F-7 are one fixture
each; F-8 can be fixed in a second repair round or closed as a named limit,
the maintainer's choice, as for every row here. The pull request body names
the amendment of criterion 4 (F-3), so the maintainer sees the spec change
at the merge, and bead coding-harness-pu9 (house rule 4); it is not a
decision pull request.
