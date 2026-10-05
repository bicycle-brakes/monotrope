---
title: "Plan — research-currency"
status: draft
implementation_status: partial
date: 2026-10-05
last_reviewed: 2026-10-05
updated: 2026-10-05
supersedes: null
superseded_by: null
bead: coding-harness-pu9
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-05"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, docs-research, drift-job, frontmatter]
---

# Plan — research-currency

```text
For you:     the nightly drift run lists research notes not reviewed for more than 90 days
Done when:   criteria 1–16 hold (tests, one run, one read), `make verify` green
Appetite:    2 h of phase 4, one repair round included
Not now:     the web re-check agent (part 2), anything red, the session display, other folders
Pre-mortem:  suppose it failed: most likely because nobody opens a green nightly run until part 2 reads the list
Starts unless you say stop.
```

Implements `spec.md` (criteria 1–16); the class is `bounded`, answered by
the maintainer on 2026-10-05 (`decisions.md`, `[DECISION] 1`), and nothing
below depends on it. Stage 1: no model markings. Facts read at `87daf91`.

## Decided in phase 3

No `[DECISION]` is open; the class is answered (`bounded`, 2026-10-05).

- `[DETAIL]` — **appetite 2 h**: about 1 h 50 min of steps below; the rest is
  one repair round.
- `[DETAIL]` — **a date is `YYYY-MM-DD` by pattern before `fromisoformat`**:
  Python 3.11 also accepts `20260916`, which criterion 2 does not.
- `[DETAIL]` — **a YAML timestamp with a time is unusable**: criterion 2 asks
  for a date; `datetime` is a subclass of `date`, so the check is
  `type(value) is date`.
- `[DETAIL]` — **the tests remove `GITHUB_STEP_SUMMARY` by an autouse
  fixture**: the hosted `verify` job sets it, and a test calling `main` would
  write into the real run's summary.

## Steps

Read `date` at each step boundary (`prompts/04-implement.md`).

1. **`scripts/check_research_currency.py`** (new, 40 min). Module docstring
   with usage and exit codes (0 listed, 2 usage, 3 not measured). Constants
   `CORPUS = "docs/research"`, `STALE_AFTER_DAYS = 90` (comment: same number
   as `plans_registry.py`, deliberately not imported), `SCHEMA_VERSION = 1`,
   `_BLOCK = re.compile(r"^﻿?---\r?\n(.*?)\n---\r?\n", re.S)` (the form
   of `check_frontmatter_current.py`), `_ISO = re.compile(r"\d{4}-\d{2}-\d{2}")`.
   - `review_date(text, today) -> tuple[date | None, str | None]` — the date
     or the reason, in these words: `no frontmatter`; `frontmatter is not a
     YAML mapping` (also on `yaml.YAMLError`); `no last_reviewed`;
     `last_reviewed is empty` (`None` or `""`); `last_reviewed '<v>' is not a
     YYYY-MM-DD date`; `last_reviewed <d> is in the future` (later than
     `today + 1 day`).
   - `@dataclass(frozen=True) Note(path, last_reviewed, age_days, due,
     problem)`; `measure(root, today) -> list[Note]` — `CannotMeasure` when
     `root / CORPUS` is not a directory or holds no note; notes are
     `sorted(p for p in rglob("*.md") if p.is_file() and not
     p.name.startswith("_"))`; a file that fails UTF-8 decoding gives
     `not valid UTF-8`, an `OSError` gives `cannot be read (<reason>)`; a
     problem note has `last_reviewed` and `age_days` `None` and `due` true;
     sort key `(problem is None, last_reviewed or date.min, path)`.
   - `render_text`, `render_json`, `render_markdown(notes, today) -> str`.
     Text, as in criterion 7:

     ```text
     research-currency: 15 notes under docs/research/, 1 due (review more than 90 days before 2026-12-20)
       due  2026-09-16  95 days  docs/research/x.md
     oldest: docs/research/x.md, reviewed 2026-09-16, 95 days ago
     ```

     A problem note reads `due  no date  docs/research/y.md — <reason>`, and
     as oldest `oldest: docs/research/y.md, no usable review date (<reason>)`.
     JSON: the object of criterion 8, `json.dumps(…, indent=2,
     ensure_ascii=False)`. Markdown: `### Research currency`, the first line
     as a sentence, a table `Reviewed | Days | Note` only when a note is due,
     the oldest line.
   - `main(argv=None) -> int` — `argparse` with `--root` (default the
     repository), `--today` (`date.fromisoformat`, default `date.today()`),
     `--format text|json`; prints; appends the Markdown (or
     `### Research currency` and the not-measured line) to the file named by
     `GITHUB_STEP_SUMMARY` when set; returns 0, or 3 after printing
     `research-currency: not measured — <reason>`.
2. **`tests/test_research_currency.py`** (new, 40 min). Docstring: every test
   builds its own tree; the only files of this repository read are the ones
   that travel (`decisions/gates.yaml`, the kit manifest). Imports the module
   (`sys.path` like `tests/test_check_adr_answers.py`) and names
   `SCRIPT = REPO_ROOT / "scripts" / "check_research_currency.py"` for the
   subprocess runs. Helpers write `docs/research/<name>` with a header; all
   runs pin `--today 2026-12-20` except criterion 6's. The tests are in the
   table below. Commit.
3. **The gate** (10 min). `decisions/gates.yaml`, after
   `plans-registry-strict`:

   ```yaml
   - id: research-currency
     title: Research notes not reviewed for more than 90 days are listed
     command: python3 scripts/check_research_currency.py
     job: drift
     enforcement: report
     floor: false
     placement: both
     reason: Research about outside tools ages without a commit here, so the nightly drift run lists the notes not reviewed for more than 90 days; report is the level the maintainer chose on 2026-10-05, not a step towards block.
   ```

   Then `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`.
   `scripts/kit/manifest.yaml`: after the `check_frontmatter_current.py`
   rule, `scripts/check_research_currency.py` → `mechanismus`, reason "the
   list behind the gate research-currency — the gate file travels, so its
   script does; without docs/research/ it says not measured"; after the
   `test_frontmatter_current.py` rule, `tests/test_research_currency.py` →
   `mechanismus`, reason "builds its own trees and reads no note of this
   repository; holds in the probe copy". Commit.
4. **`docs/research/_INDEX.md`** (5 min). After the first paragraph under
   `# Research Index`, this paragraph, then
   `python3 scripts/check_frontmatter_current.py --stamp`:

   > A note's `last_reviewed:` is the day its content was last checked
   > against its sources. An edit moves `updated:`, not this date; whoever
   > re-checks a note sets it. The nightly `drift` job lists the notes whose
   > review is more than 90 days old (`scripts/check_research_currency.py`,
   > report-only).

5. **Close** (15 min). `implementation_status: partial` in the four
   artefacts of this folder, `python3 scripts/plans_registry.py --index`,
   the verification below; paste the output of the criterion-15 run under
   `## Evidence` here. Commit.

## Tests

| Criterion | Test | Goes red when |
| --- | --- | --- |
| 1 | `test_only_notes_under_docs_research_are_listed` — `_INDEX.md`, `a.txt`, `docs/other/b.md`, `docs/research/sub/c.md` | the glob covers `docs/`, skips no `_` name, or is not recursive |
| 2 | `test_the_review_date_is_last_reviewed_and_nothing_else` | `updated:` or `created:` is read |
| 3 | `test_the_list_notices_a_note_past_the_threshold` — 91 days due, 90 not (the mutation evidence of criterion 13) | `>=`, another number, no threshold |
| 4 | `test_an_unusable_review_date_is_due_with_its_reason`, parametrised over the eight cases; `test_a_date_on_the_next_day_is_usable` | a case is skipped, raises, or loses its reason; no slack or more than a day |
| 5 | `test_unusable_first_then_oldest_then_path`; `test_two_runs_give_the_same_bytes` | glob order, mtime order, ties not by path |
| 6 | `test_without_today_the_local_date_counts` — a note `date.today() - 91 days` is due | a fixed date, `--today` ignored |
| 7 | `test_the_text_names_the_oldest_even_when_none_is_due`; `test_the_text_has_a_line_per_due_note` | no oldest line on an empty list, a due note unprinted |
| 8 | `test_the_json_carries_every_note_in_order` | a key missing, only due notes, another order |
| 9 | `test_the_summary_is_written_only_when_asked` (`monkeypatch.setenv`) | no append with the variable, a file without it |
| 10 | `test_due_notes_never_turn_the_run_red`; `test_a_missing_or_empty_corpus_is_not_measured` (missing, empty, only `_INDEX.md`) | exit depends on due notes; exit 0 over nothing |
| 11 | `test_the_run_changes_no_byte_and_needs_no_git` — subprocess in `tmp_path`, tree hashed before and after | a write, a git call |
| 12 | `test_the_gate_reports_in_the_drift_job_only` — the gate entry, and `ci_gates.generate_ci()` with the step and `continue-on-error: true` in the `drift` job, not in `verify` | another job or level, no `continue-on-error` |
| 13 | the ratchets of `tests/test_ci.py` (caller, test, mutation) | the step missing from `ci.yml`, no `notices` test |
| 14 | `test_the_kit_carries_the_script_and_its_test` (`probe.rolle`); gate `leerprobe` | a role not `mechanismus`; a test that reads this repository's notes |
| 15 | the run under "Verification", output under `## Evidence` | — |
| 16 | read in phase 6 | — |

## Verification

```bash
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
python3 scripts/check_research_currency.py
python3 scripts/check_research_currency.py --format json | python3 -m json.tool > /dev/null
```

`bash scripts/verify_all.sh --job drift` is not the check: its
`plans-registry-strict` is red for four beads outside this change
(research 1.4).

## Not touched

`scripts/ci_gates.py` (the step comes from the gate file alone;
`OHNE_AUFRUFER` and `OHNE_TEST` stay), `tests/test_ci.py`
(`OHNE_MUTATIONSTEST` stays), `scripts/kit/probe.py` and `REIST_NICHT`,
`scripts/ramp_valves.py` (no valve: `report` is the target),
`scripts/plans_registry.py`, `scripts/check_docs.py`,
`scripts/check_frontmatter_current.py`, `scripts/export/manifest.yaml` (its
catch-all drops it, as for the sibling check), `provenance.yaml`,
`tools/claude-code/`, `AGENTS.md`, and every note's header —
`_INDEX.md` gets only its paragraph and the stamp.

## Revisions in phase 4

The plan held except in two places, both revised here and neither changing a
criterion. Planted-fault runs, the verification and the clock follow below.

- **Steps 1–3 are one commit, not two.** The plan commits after step 2
  (script, tests) and after step 3 (gate, `ci.yml`, kit roles). Alone, the
  first would be red: `tests/test_ci.py` demands a caller for every script
  (the generated workflow), and the kit probe a role for every tracked file.
  The script, its tests, the gate entry, the regenerated `ci.yml` and the two
  kit roles went in together (`9714b0e`).
- **The header is read with a loader that leaves a date as text.** The plan
  has `yaml.safe_load` and `type(value) is date`. PyYAML raises `ValueError`
  — not `YAMLError` — on `last_reviewed: 2026-02-30`, which would have ended
  the run on one bad note, against criterion 4 ("the run goes on to the next
  note"). `_Loader` (a `SafeLoader` without the timestamp resolver) hands every
  date-like scalar over as a string, and `_ISO` plus `date.fromisoformat`
  judge it: the same verdict for every case the plan names (`datetime`
  and `20260916` stay unusable), and an impossible date gets the reason
  `last_reviewed '2026-02-30' is not a YYYY-MM-DD date`. A tag-forced
  timestamp (`!!timestamp 2026-02-30`) still raises `ValueError` and reads as
  "frontmatter is not a YAML mapping" (fault 11).

`[DETAIL]`s phase 4 decided, each one reversible and covered by a test:

- The not-measured line goes to stdout in either format; a consumer checks the
  exit code first.
- `1 note`, not `1 notes`; the oldest line says `today` for age 0 and
  `tomorrow` for age −1 (the one day of slack) instead of `0 days ago`.
- A value in a reason is cut to one line of at most 80 characters.
- A summary file that cannot be written gives one line on stderr and changes
  neither the list nor the exit code.
- `--today` takes `YYYY-MM-DD` only, like a header (`20261220` is a usage
  error, exit 2); notes sort by their printed path string, not by `Path`
  parts.

## Planted faults

Every test has its counterpart: a fault planted on its own, the suite run, the
file restored. Before every fault: `python3 -m pytest
tests/test_research_currency.py -q` — **68 passed**. After: **56 faults, 56
red, none green.** Planted on `59b1862`.

Replay: make the edit in the file of the column `File` — `script` is
`scripts/check_research_currency.py`, `gates.yaml` is `decisions/gates.yaml`,
`ci_gates.py` is `scripts/ci_gates.py`, `manifest` is
`scripts/kit/manifest.yaml` — run `python3 -m pytest
tests/test_research_currency.py -q --tb=no`, and restore with
`git checkout -- <file>`. "Red" is the number of failing tests of 68; the
tests named are the first three that failed.

| # | Crit. | File | Fault | Red | Tests that went red |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | script | `rglob("*.md")` → `glob("*.md")`: not recursive | 3 | `test_only_notes_under_docs_research_are_listed`, `test_unusable_first_then_oldest_then_path`, `test_the_json_carries_every_note_in_order` |
| 2 | 1 | script | drop `and not p.name.startswith("_")`: `_` names are notes | 3 | `test_only_notes_under_docs_research_are_listed`, `test_a_missing_or_empty_corpus_is_not_measured` |
| 3 | 1 | script | `root / CORPUS` → `root / "docs"`: the glob covers `docs/` | 5 | `test_only_notes_under_docs_research_are_listed`, `test_a_missing_or_empty_corpus_is_not_measured` |
| 4 | 2 | script | `header["last_reviewed"]` → `header.get("updated", header["last_reviewed"])`: `updated:` is read first | 1 | `test_the_review_date_is_last_reviewed_and_nothing_else` |
| 5 | 2 | script | `last_reviewed` also looked up inside the `review:` block | 1 | `test_the_review_date_is_last_reviewed_and_nothing_else` |
| 6 | 2 | script | header regex without BOM and CRLF: `^---\n(.*?)\n---\n` | 1 | `test_a_header_with_a_byte_order_mark_and_crlf_line_endings_is_read` |
| 7 | 3 | script | `age > STALE_AFTER_DAYS` → `age >= STALE_AFTER_DAYS`: 90 days is due | 3 | `test_the_list_notices_a_note_past_the_threshold`, `test_the_threshold_is_one_named_constant`, `test_the_json_carries_every_note_in_order` |
| 8 | 3 | script | `STALE_AFTER_DAYS = 90` → `91` | 9 | `test_the_list_notices_a_note_past_the_threshold`, `test_the_threshold_is_one_named_constant`, `test_today_names_the_day_whatever_the_clock_says` (+5) |
| 9 | 3 | script | `age > STALE_AFTER_DAYS` → `age > 90`: the constant is bypassed | 1 | `test_the_threshold_is_one_named_constant` |
| 10 | 3 | script | `age > STALE_AFTER_DAYS` → `False` in the `Note`: a due note is not listed | 10 | `test_the_review_date_is_last_reviewed_and_nothing_else`, `test_the_list_notices_a_note_past_the_threshold`, `test_the_threshold_is_one_named_constant` (+5) |
| 11 | 4 | script | `except (yaml.YAMLError, ValueError)` → `except yaml.YAMLError`: an impossible date ends the run | 1 | `test_an_unusable_review_date_is_due_with_its_reason` |
| 12 | 4 | script | `today + timedelta(days=1)` → `today`: no slack for tomorrow | 3 | `test_a_date_on_the_next_day_is_usable`, `test_the_oldest_line_reads_naturally_for_today_and_tomorrow`, `test_the_json_carries_every_note_in_order` |
| 13 | 4 | script | `today + timedelta(days=1)` → `today + timedelta(days=2)`: too much slack | 2 | `test_an_unusable_review_date_is_due_with_its_reason`, `test_a_date_on_the_next_day_is_usable` |
| 14 | 4 | script | the reason `"no last_reviewed"` → `""`: due without its reason | 4 | `test_the_review_date_is_last_reviewed_and_nothing_else`, `test_an_unusable_review_date_is_due_with_its_reason`, `test_the_text_has_a_line_per_due_note` (+1) |
| 15 | 4 | script | `except UnicodeDecodeError` → `except KeyError`: a non-UTF-8 note ends the run | 4 | `test_an_unusable_review_date_is_due_with_its_reason`, `test_due_notes_never_turn_the_run_red`, `test_the_run_changes_no_byte_and_needs_no_git` |
| 16 | 4 | script | `except OSError` → `except FileNotFoundError` in `measure`: an unreadable note ends the run | 1 | `test_a_note_that_cannot_be_read_is_due_with_its_reason` |
| 17 | 4 | script | drop `or not _ISO.fullmatch(value)`: `'20261201'` counts as a date | 1 | `test_an_unusable_review_date_is_due_with_its_reason` |
| 18 | 4 | script | `if tag != _TIMESTAMP_TAG` → `if tag`: the loader parses timestamps again | 43 | `test_the_review_date_is_last_reviewed_and_nothing_else`, `test_a_header_with_a_byte_order_mark_and_crlf_line_endings_is_read`, `test_the_list_notices_a_note_past_the_threshold` (+13) |
| 19 | 4 | script | `value is None or value == ""` → `value is None`: `''` is not "empty" | 1 | `test_an_unusable_review_date_is_due_with_its_reason` |
| 20 | 4 | script | `_shown` returns `str(value)`: a value is not cut to one short line | 1 | `test_a_reason_is_one_short_line` |
| 21 | 5 | script | sort key `(False, … or date.max, path)`: unusable dates sort last | 30 | `test_an_unusable_review_date_is_due_with_its_reason`, `test_unusable_first_then_oldest_then_path`, `test_the_text_has_a_line_per_due_note` (+2) |
| 22 | 5 | script | sort key with `-(…).toordinal()`: newest first | 5 | `test_unusable_first_then_oldest_then_path`, `test_without_today_the_local_date_counts`, `test_the_text_names_the_oldest_even_when_none_is_due` (+1) |
| 23 | 5 | script | sort key without `n.path`: no tie-break | 2 | `test_unusable_first_then_oldest_then_path`, `test_the_text_names_the_oldest_even_when_none_is_due` |
| 24 | 5 | script | sort key with `n.path[::-1]`: ties by the reversed path | 1 | `test_unusable_first_then_oldest_then_path` |
| 25 | 5 | script | the first output line ends with `[{os.getpid()}]`: two runs differ | 5 | `test_two_runs_give_the_same_bytes`, `test_today_names_the_day_whatever_the_clock_says`, `test_the_text_has_a_line_per_due_note` (+1) |
| 26 | 6 | script | `args.today or date.today()` → `args.today or date(2026, 12, 20)`: a fixed day | 2 | `test_without_today_the_local_date_counts` |
| 27 | 6 | script | `date.today()` → the UTC date: not the local date | 1 | `test_without_today_the_local_date_counts` |
| 28 | 6 | script | `args.today or date.today()` → `date.today()`: `--today` ignored | 9 | `test_the_list_notices_a_note_past_the_threshold`, `test_today_names_the_day_whatever_the_clock_says`, `test_the_text_has_a_line_per_due_note` (+5) |
| 29 | 6 | script | `_day` without the `_ISO` pattern check: `--today 20261220` accepted | 1 | `test_a_malformed_today_is_a_usage_error` |
| 30 | 7 | script | the `oldest:` line only when a note is due | 2 | `test_the_text_names_the_oldest_even_when_none_is_due`, `test_the_oldest_line_reads_naturally_for_today_and_tomorrow` |
| 31 | 7 | script | `if not n.due:` → `if True:` in `render_text`: no due line printed | 4 | `test_the_list_notices_a_note_past_the_threshold`, `test_today_names_the_day_whatever_the_clock_says`, `test_the_text_has_a_line_per_due_note` |
| 32 | 7 | script | age −1 printed as `-1 days ago`, not `tomorrow` | 1 | `test_the_oldest_line_reads_naturally_for_today_and_tomorrow` |
| 33 | 7 | script | `_count` always plural: `1 notes` | 4 | `test_today_names_the_day_whatever_the_clock_says`, `test_the_oldest_line_reads_naturally_for_today_and_tomorrow`, `test_the_summary_has_a_table_only_when_a_note_is_due` |
| 34 | 8 | script | JSON without `threshold_days` | 2 | `test_the_threshold_is_one_named_constant`, `test_the_json_carries_every_note_in_order` |
| 35 | 8 | script | JSON lists due notes only | 3 | `test_without_today_the_local_date_counts`, `test_the_json_carries_every_note_in_order` |
| 36 | 8 | script | JSON lists notes in reverse order | 3 | `test_without_today_the_local_date_counts`, `test_the_json_carries_every_note_in_order` |
| 37 | 8 | script | `ensure_ascii=False` → `True` | 1 | `test_the_json_carries_every_note_in_order` |
| 38 | 8 | script | JSON `corpus` is `docs/research` without the slash | 1 | `test_the_json_carries_every_note_in_order` |
| 39 | 9 | script | `target = os.environ.get("GITHUB_STEP_SUMMARY")` → `None`: the variable is ignored | 4 | `test_the_summary_is_written_only_when_asked`, `test_the_summary_has_a_table_only_when_a_note_is_due`, `test_the_summary_carries_the_not_measured_line` (+1) |
| 40 | 9 | script | without the variable the summary goes to `research-currency-summary.md` | 2 | `test_the_summary_is_written_only_when_asked`, `test_the_run_changes_no_byte_and_needs_no_git` |
| 41 | 9 | script | the not-measured line is not appended to the summary | 1 | `test_the_summary_carries_the_not_measured_line` |
| 42 | 9 | script | `except OSError` → `except FileNotFoundError` in the summary write: an unwritable summary ends the run | 1 | `test_an_unwritable_summary_does_not_end_the_run` |
| 43 | 9 | script | `if due:` → `if True:` in `render_markdown`: a table without a due note | 1 | `test_the_summary_has_a_table_only_when_a_note_is_due` |
| 44 | 9 | script | summary opened with `"w"`, not `"a"`: earlier steps' text is lost | 1 | `test_the_summary_is_written_only_when_asked` |
| 45 | 10 | script | `return 0` → `return 1 if any(n.due for n in notes) else 0`: due notes turn the run red | 9 | `test_without_today_the_local_date_counts`, `test_the_text_has_a_line_per_due_note`, `test_the_json_carries_every_note_in_order` (+4) |
| 46 | 10 | script | `if not files:` → `if False:`: nothing to list is no longer "not measured" | 6 | `test_a_missing_or_empty_corpus_is_not_measured` |
| 47 | 10 | script | `if not corpus.is_dir():` → `if False:`: a missing corpus gives another reason | 4 | `test_a_missing_or_empty_corpus_is_not_measured` |
| 48 | 10 | script | `return 3` → `return 0` after the not-measured line | 11 | `test_the_summary_carries_the_not_measured_line`, `test_a_missing_or_empty_corpus_is_not_measured` |
| 49 | 11 | script | `main` writes `_stamp` into the root: the run changes a byte | 2 | `test_the_summary_carries_the_not_measured_line`, `test_the_run_changes_no_byte_and_needs_no_git` |
| 50 | 11 | script | `main` calls `git rev-parse`: the run needs git | 1 | `test_the_run_changes_no_byte_and_needs_no_git` |
| 51 | 12 | gates.yaml | gate `enforcement: report` → `block` | 1 | `test_the_gate_reports_in_the_drift_job_only` |
| 52 | 12 | gates.yaml | gate `job: drift` → `job: verify` | 1 | `test_the_gate_reports_in_the_drift_job_only` |
| 53 | 12 | ci_gates.py | `scripts/ci_gates.py`: `report` no longer gets `continue-on-error: true` | 1 | `test_the_gate_reports_in_the_drift_job_only` |
| 54 | 12 | gates.yaml | gate reason without "the level the maintainer chose … not a step towards block" | 1 | `test_the_gate_reports_in_the_drift_job_only` |
| 55 | 14 | manifest | kit rule of the script: `rolle: mechanismus` → `bestand` | 1 | `test_the_kit_carries_the_script_and_its_test` |
| 56 | 14 | manifest | kit rule of the test: `rolle: mechanismus` → `bestand` | 1 | `test_the_kit_carries_the_script_and_its_test` |

## Evidence

Criterion 15, run on 2026-10-05 at 19:22 on `c1884d4` plus the edits of the
close step (any day before 2026-12-16 gives the same list):

```text
$ python3 scripts/check_research_currency.py
research-currency: 15 notes under docs/research/, 0 due (review more than 90 days before 2026-10-05)
oldest: docs/research/2026-09-16-review-corpus-vs-running-workflow.md, reviewed 2026-09-16, 19 days ago
$ echo $?
0
$ python3 scripts/check_research_currency.py --format json | python3 -m json.tool > /dev/null
$ echo $?
0
$ python3 scripts/ci_gates.py --check-ci
ci.yml ist genau die Ableitung der Gate-Datei.
```

`GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false
make verify` ended `VERIFY GREEN — every local gate of the 'verify' job
passed`: 584 passed, 15 skipped (68 of them in
`tests/test_research_currency.py`); `ruff-check`, `ruff-format`, `leerprobe`,
`plans-registry`, `frontmatter-current`, `adr-answers`, `gate-schema`,
`ci-drift` and `ramp-valves` green. `docs-links` (51 findings, none in a file
of this change) and `markdownlint` are report-only gates and red, as they
were in the run before the plan was edited.

`OHNE_AUFRUFER`, `OHNE_TEST`, `OHNE_MUTATIONSTEST` and `REIST_NICHT` are
unchanged: `git diff origin/main` shows no change in `scripts/ci_gates.py`,
`tests/test_ci.py` or `scripts/kit/probe.py` (criterion 13).

## Time used

Appetite: 2 h of phase 4, one repair round included. Read from `date`.

- 2026-10-05 19:08–19:23, 15 min
