---
title: "Plan — research-currency"
status: draft
implementation_status: none
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
