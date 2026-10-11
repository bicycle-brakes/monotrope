---
title: "Plan — criterion-test-ledger"
status: draft
implementation_status: partial
date: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-11
supersedes: null
superseded_by: null
bead: coding-harness-909
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, gates, tests, acceptance-criteria]
---

# Plan — criterion-test-ledger

```text
For you:     a test a plan names for an acceptance criterion can no longer vanish unseen: deleting or renaming it turns `make verify` red until its ledger line changes with it
Done when:   criteria 1–28 hold — the gate finds nothing over the five live plans at the pull request's head, the 29-of-30 replay exits 1 — and `make verify` ends VERIFY GREEN
Appetite:    8 h of phase 4, one repair round included; a stop, not an estimate
Not now:     a test count per file, the change-artefact validator, ledgers for the 17 archived plans dated before 2026-10-11, running or judging a named test
Pre-mortem:  suppose it failed: most likely because mapping stage2-session's 16 criteria onto its 71 unnamed test functions by reading outruns the appetite
Starts unless you say stop.
```

Implements `spec.md` (criteria 1–28). `design.md` adds only the ADR draft,
`docs/adr/0013-every-criterion-names-its-proof.md`, written in phase 2b: the
pull request is a decision pull request, and the ADR takes effect with the
maintainer's merge (ADR 0008). Facts read on 2026-10-11 at `d4978ab`, where
`make verify` ended VERIFY GREEN (1606 passed, 16 skipped). Explore ran
without the runner (`research.md`), so no Stage-1 route is carried forward.

## Decided in phase 3

No `[DECISION]` is open.

`[GAP]`s, closed by reading at `d4978ab`:

- **`docs/adr/` keeps no index** — no list file; ADRs 0010 to 0012 were added
  without one. The spec's Definition of Done now names the ADR file instead
  of an index entry.
- **The phase-4 runner does not regenerate `ci.yml`.** `prepare_derived` in
  `scripts/stage2.py` stamps headers and renders `plans/INDEX.md` only, so a
  file-only worker writes the four `ci.yml` lines of step 2 by hand; the
  gate `ci-drift` checks them.
- **`hermes-runner` carries two per-criterion tables** (slices 4 and 5), not
  only file lists; criterion 27's line goes above both.
- **The mutation ratchet** (`MUTATIONS_NAMEN`, `tests/test_ci.py`) counts a
  test named `…goes_red…` in a file that names `check_criterion_ledger.py`.
- **The kit probe** copies `plans/changes/` and its `archive/` empty and runs
  `pytest` only; the travelling files are the gate list, `scripts/kit/`,
  `prompts/` and `docs/WORKFLOW.md`.
- **`tests/test_research_currency.py` holds 30 test functions**, as at
  `d5813ec`, and `research-currency`'s plan names all 30.
- **The gate list runs Python 3.11 and 3.12** (`decisions/gates.yaml`,
  `tools`): nothing newer than 3.11.

`[DETAIL]`s, each reversible:

1. **Order: migration, then the gate, then the texts.** The gate holds every
   live plan from the commit that wires it, so the four plans carry ledgers
   first; and a script without its gate entry fails the caller ratchet, so
   script, test file and wiring land in one commit.
2. **Own text check, not `ramp_valves._enforcer_exists`.** That function
   resolves against its own repository root, not `--root`; the regex
   `^def <function>\(` is the same.
3. **Fences as CommonMark has them**: an opening line of three or more
   backticks or tildes, indented at most three spaces; it closes on the same
   character at least as long with nothing after it. The live plans nest
   fences.
4. **Lines are split on `\n` only**, a trailing `\r` and trailing whitespace
   removed before any match, a leading byte-order mark dropped: line numbers
   then match `grep -n`.
5. **A header date exempts only alone**: exactly one header line beginning
   `date:`, reading `date: YYYY-MM-DD` with a real calendar date. Two such
   lines measure instead of exempting.
6. **A `<path>` segment** holds no whitespace, `/`, `:` or backtick, and `.`
   and `..` are refused: the path stays below `tests/`. Function names are
   ASCII.
7. **One finding stops a plan** when the plan cannot be read or has more
   than one ledger section; its entries are not read further.
8. **Every `## Acceptance criteria` section of a spec counts** — the union of
   their numbers.
9. **Migrated ledgers**: one entry per criterion and function, sorted by
   criterion; a function named for two criteria stands twice; the fault after
   ` — ` is optional and taken from the row when it fits.
10. **The pointer line of criterion 27** is the last line before the table,
    one blank line between them, so every renderer keeps the table.
11. **Ledger placement**: before `## Not touched` in `harness-decide-adr` and
    `hermes-runner`, before `## Verification` in `research-currency`, before
    `## Verification and review` in `stage2-session` — after the tables they
    point from.

## Steps

Read `date` at each step boundary (`prompts/04-implement.md`). Each step ends
green on its own; under the Stage-2 runner, which commits once per call, they
may land in one checkpoint.

1. **Migrate the four plans** (4 h). In each, the ledger section at the place
   of detail 11 and the pointer line above each per-criterion table, by the
   rules under "Migration". Nothing checks a ledger yet. Commit.
2. **The gate** (3 h). `scripts/check_criterion_ledger.py` and
   `tests/test_check_criterion_ledger.py` (the tests of criteria 1–20 in the
   ledger below), the wiring, the kit roles, and in the ledger below
   `not yet written` removed from every test this step writes. Correct what
   the gate then reports in the migrated ledgers. Commit.
3. **The texts** (30 min). `prompts/03-plan.md`, `prompts/04-implement.md`,
   `docs/WORKFLOW.md` as under "Texts", and the tests of criteria 21–23 with
   their markers removed. Commit.
4. **Evidence and close** (30 min). The runs under "Verification";
   `implementation_status: partial` in this folder's artefacts; output under
   `## Evidence` here. Commit.

## The gate — `scripts/check_criterion_ledger.py`

New, standard library only. The docstring states the rule (ADR 0013;
`decisions.md` Q-1, Q-2), the three entry forms, usage
(`python3 scripts/check_criterion_ledger.py [--root DIR]`) and the exit codes:
0 nothing found, 1 findings, 3 could not measure.

- **Constants**: `CHANGES_DIR = "plans/changes"`, `ARCHIVE = "archive"`,
  `HEADING = "## Criterion ledger"`, `CUTOFF = date(2026, 10, 11)` with the
  comment "the day of the maintainer's answers (decisions.md Q-2); changing
  it is a governance act, stated in docs/WORKFLOW.md beside this gate".
- **Entry forms**, matched with `fullmatch` on the stripped line, `re.ASCII`:

  ```python
  _N = r"(?P<n>[1-9][0-9]*)"
  _REF = r"(?P<path>tests/(?:[^\s/:`]+/)*test_[^\s/:`]*\.py)::(?P<function>test_[A-Za-z0-9_]*)"
  _FAULT = r"(?: — (?P<text>\S.*))?"
  TEST = re.compile(rf"- {_N}: {_REF}{_FAULT}")
  NOT_YET = re.compile(rf"- {_N}: not yet written {_REF}{_FAULT}")
  NOT_A_TEST = re.compile(rf"- {_N}: not a test — (?P<text>\S.*)")
  ```

- `Entry` (frozen dataclass: `line`, `kind` — `"test"`, `"not yet written"`
  or `"not a test"` — `number`, `path`, `function`) and the public
  `parse_entry(text, line=0) -> Entry | None`, which the prompt test uses.
- `ledger_sections(lines)`: every `HEADING` line outside a fence, each to the
  next `^#{1,2}(?:[ \t]|$)` line outside a fence or the end. In a section a
  line is blank, an entry, a continuation line (`^[ \t]` and not
  `^[ \t]+- `, directly below an entry or a continuation line; a blank line
  ends the chain) or a finding.
- `criterion_numbers(spec_text)`: `^(\d+)\. ` lines outside fences, from a
  `## Acceptance criteria` line to the next `^##(?:[ \t]|$)` line outside a
  fence.
- `exempt_by_date(plan_text)`: detail 5, header from a first line `---` to
  the next `---`.
- `read(path)`: the text, or "is not valid UTF-8" / "cannot be read
  (<reason>)" on `UnicodeDecodeError` / `OSError`. A named test file is read
  once per run; defined means a match of `^def <function>\(` (`re.M`).
- `measure(root)`: `CannotMeasure` unless `root` is a readable directory
  holding `plans/changes/`. Live: every directory under `plans/changes/`
  except `archive/`; archived: every directory under `plans/changes/archive/`;
  a folder without `plan.md` is skipped. Per plan, in this order: read it; its
  sections (none — exempt when archived and `exempt_by_date`, else a finding;
  two or more — a finding); `spec.md` beside it (missing, unreadable, or no
  criterion number — a finding); each section line; each entry (number
  unknown to the spec; a test entry not defined; a not-yet-written entry in an
  archived plan, or defined in a live one; a named file that cannot be read);
  each spec number without an entry.
- **Output.** A finding is one stdout line,
  `<plan>[:<line>]: <what is wrong> — <what to do>`, path relative to the
  root, sorted by path and line; the line of a form finding lists the three
  forms; then `criterion-ledger: <k> findings in <p> plans` on stderr and
  exit 1. Clean, exit 0 and one line:

  ```text
  criterion-ledger: held 5 plans (5 live, 0 archived); read 310 entries (230 test, 50 not yet written, 30 not a test); 17 archived plans dated before 2026-10-11 exempt
  criterion-ledger: examined nothing — no plan.md under plans/changes/ is held; 0 archived plans dated before 2026-10-11 exempt
  ```

  (the second when no plan is held; numbers invented). Not measured:
  `criterion-ledger: not measured — <reason>`, exit 3.

## The tests — `tests/test_check_criterion_ledger.py`

New. Docstring: criteria 1–23 of this spec; every test builds its own tree
in `tmp_path`; the files of this repository it reads are the ones that travel
(the gate list, `scripts/kit/manifest.yaml`, two phase prompts,
`docs/WORKFLOW.md`). It imports the module as `tests/test_check_adr_answers.py`
does (`sys.path`, plus `scripts/kit` for `probe`), names
`SCRIPT = REPO_ROOT / "scripts" / "check_criterion_ledger.py"` and runs it as a
subprocess with `--root`. Helpers write a change (`spec.md` with criteria
1..n, `plan.md` with a header `date:` and a ledger, optionally under
`archive/`) and a test file with given top-level functions. Each test and the
fault that turns it red stand in the ledger below.

## Wiring

- `decisions/gates.yaml`, after `interview-minimums`:

  ```yaml
    - id: criterion-ledger
      title: Every test a plan names for an acceptance criterion still exists
      command: python3 scripts/check_criterion_ledger.py
      job: verify
      enforcement: block
      floor: false
      placement: both
      reason: Deleting 29 of 30 criterion tests left make verify green (bead coding-harness-909), so every test a plan's criterion ledger names must still exist, while the change is live and after it is archived (ADR 0013).
  ```

- `.github/workflows/ci.yml`, after the `interview-minimums` step — by
  `python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml`
  where a shell exists, else these lines by hand:

  ```yaml
        - name: Every test a plan names for an acceptance criterion still exists
          id: criterion-ledger
          if: ${{ !cancelled() }}
          run: python3 scripts/check_criterion_ledger.py
  ```

- `scripts/kit/manifest.yaml`: after the `scripts/check_adr_answers.py` rule,
  `scripts/check_criterion_ledger.py` → `mechanismus`, reason "the check
  behind the gate criterion-ledger — the gate file travels, so its script
  does (ADR 0013)"; after the `tests/test_check_adr_answers.py` rule,
  `tests/test_check_criterion_ledger.py` → `mechanismus`, reason "builds its
  own trees and reads only files that travel; holds in the probe copy".

## Texts

`prompts/03-plan.md`: the bullet "**Per acceptance criterion the test** that
holds it, …" ends "— as entries of the criterion ledger below."; after the
"Required:" list, before `## Questions`, this section:

````markdown
## The criterion ledger

Every `plan.md` has exactly one section headed `## Criterion ledger`, with
one line per criterion and test in one of three forms:

- a test entry, `- <n>: tests/<path>::<function>` — a top-level
  `def test_…` in a file `tests/…/test_*.py`;
- a not-yet-written entry, `- <n>: not yet written tests/<path>::<function>`
  — a test phase 4 has still to write;
- a not-a-test entry, `- <n>: not a test — <what holds it>` — a review, a
  gate or a command; where a test can hold the criterion, write the test.

`<n>` is a criterion number of `spec.md`, without a leading zero, and every
criterion has at least one entry. A test entry or a not-yet-written entry may
end in ` — ` and the fault that turns the test red; an indented line
continues an entry. For example:

```markdown
## Criterion ledger

- 1: tests/test_example.py::test_a_missing_file_is_reported — the check exits 0 without the file
- 2: not yet written tests/test_example.py::test_an_empty_file_is_reported
- 3: not a test — the phase-6 review reads the help text against the spec
```

The gate `criterion-ledger` holds the ledger of every live change, and keeps
holding it after the change is archived: a named test that is not defined, a
not-yet-written test that exists, a criterion without an entry, an entry for
no criterion and a line in none of the three forms turn `make verify` red.
````

`prompts/04-implement.md`, after the paragraph "You write the test **with**
the change, …":

```markdown
**The ledger moves with the tests.** The commit that writes a test the
plan's `## Criterion ledger` names as not yet written removes `not yet
written` from its line. The commit that renames or removes a test a ledger
names changes that ledger line in the same commit, in an archived plan too.
The gate `criterion-ledger` turns `make verify` red on either one left behind.
```

`docs/WORKFLOW.md`, a row after "Interview" in the table of "What stands in
the repository for it", then the stamp:

```markdown
| Criterion tests | `scripts/check_criterion_ledger.py` | the gate `criterion-ledger`: every test a plan's `## Criterion ledger` names is defined, every criterion of the spec has an entry, a not-yet-written entry stands only while the change is live; ledgers stay held after archiving, and archived plans dated before 2026-10-11 without one are exempt (ADR 0013) |
```

## Migration

For each of `harness-decide-adr` (15 criteria), `hermes-runner` (59),
`research-currency` (16) and `stage2-session` (16):

- **Every function the plan names for a criterion** — in a per-criterion
  table, a planted-fault table with a criterion column, or the tests a step
  or slice builds — is an entry for that criterion: a test entry when
  `grep -rn "^def <name>(" tests/` finds it, a not-yet-written entry when it
  does not. Its file is the one the plan names for it; where the plan names
  none, the one `grep` finds.
- **A criterion the plan holds without naming a function** gets a not-a-test
  entry saying what holds it (check number, command, gate, review) — unless
  the plan names a test file for it: then the functions of that file that
  fail on the criterion's "Refuted by", found by reading, as test entries
  (criterion 26).
- **Pointer line** above each per-criterion table, as detail 10 places it:
  `The list the gate criterion-ledger holds is the section "Criterion ledger" below; this table is the earlier record.`

Per plan, on 2026-10-11:

- `harness-decide-adr` — "Test per criterion": 49 functions, all defined
  (gate tests in `tests/test_check_adr_answers.py`, command tests in
  `tests/test_harness_decide_adr.py`, unless a row names a file). Criterion
  15 names `tests/test_entry_points.py`:
  `test_instruction_file_is_under_200_lines`. 11 and 14 are not-a-test. The
  plan names 11 more functions outside the table, in its implementation
  notes; each enters for the criterion the note gives it, or the pull request
  body names it as holding none.
- `hermes-runner` — slice 1 holds 8 by
  `tests/test_model_endpoints.py::test_every_model_in_a_phase_prompt_resolves`
  and 11 by `tests/test_kit.py::test_the_workflow_itself_travels`, besides
  its checks; criteria 1–17 are otherwise not-a-test (checks 1–11, slice 2's
  and 3's commands, `make verify`). Slices 4 and 5: 39 not-yet-written
  entries from their two tables; 43 is not-a-test (the fixture); 44 names
  `tests/test_ci.py`, so its three ratchet functions. 57–59 are not-a-test
  (the maintainer's slices 6 and 7).
- `research-currency` — all 30 functions of `tests/test_research_currency.py`,
  17 from "Tests" and 13 from the planted-fault tables and repair round 1
  (a function there enters for its row's criterion, or the criterion its
  finding amends); the two names `tests/test_touch_map.py` also defines stay
  with `tests/test_research_currency.py`. 13 holds the three ratchets of
  `tests/test_ci.py`; 15 and 16 are not-a-test.
- `stage2-session` — "Tests and faults" names no function: read
  `tests/test_stage2_session.py` (50 functions) and
  `tests/test_stage2_session_policy.py` (21) against each criterion's
  "Refuted by" and the planted-fault records of packages 3 and 4; every row
  1–14 gets at least one test entry; 15 and 16 their doc tests plus a
  not-a-test entry for the review.

## Verification

```bash
.venv/bin/python -m pytest tests/test_check_criterion_ledger.py -q
.venv/bin/python scripts/check_criterion_ledger.py
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
```

Criterion 24 is the second line's output: exit 0, 5 held, 17 exempt.

Criterion 27:

```bash
grep -n -B2 -E '^\| (Criterion|Criteria|Spec) \|' plans/changes/{harness-decide-adr,hermes-runner,research-currency,stage2-session}/plan.md
```

Criterion 25, a reading aid — prints, per plan, the function names the plan
mentions outside its ledger that the ledger lacks; each one printed is added,
or named in the pull request body as holding no criterion:

```bash
for c in harness-decide-adr hermes-runner research-currency stage2-session; do
  .venv/bin/python - "plans/changes/$c/plan.md" <<'EOF'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
before, _, rest = text.partition("\n## Criterion ledger\n")
ledger, _, after = rest.partition("\n## ")
named = set(re.findall(r"\b(test_[A-Za-z0-9_]+)\b(?!\.py)", before + after))
print(sys.argv[1], sorted(named - set(re.findall(r"::(test_[A-Za-z0-9_]+)", ledger))))
EOF
done
```

Criterion 28, on the pull request's head commit:

```bash
R=$(mktemp -d) && git archive HEAD | tar -x -C "$R"
.venv/bin/python - "$R/tests/test_research_currency.py" <<'EOF'
import ast, pathlib, sys
p = pathlib.Path(sys.argv[1])
lines = p.read_text(encoding="utf-8").split("\n")
tests = [n for n in ast.parse("\n".join(lines)).body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]
for n in reversed(tests[1:]):  # keep the first, delete the other 29
    del lines[min([n.lineno] + [d.lineno for d in n.decorator_list]) - 1 : n.end_lineno]
p.write_text("\n".join(lines), encoding="utf-8")
print(len(tests), "test functions,", len(tests) - 1, "deleted")
EOF
.venv/bin/python scripts/check_criterion_ledger.py --root "$R"; echo "exit $?"
```

Expected: `30 test functions, 29 deleted`, then a finding for each deleted
function `research-currency`'s ledger names, and `exit 1`.

## Not touched

`scripts/ramp_valves.py` (detail 2), `scripts/ci_gates.py` (`OHNE_AUFRUFER`,
`OHNE_TEST`), `tests/test_ci.py` (`OHNE_MUTATIONSTEST`), `scripts/kit/probe.py`
(`REIST_NICHT`, `DECKEL`), `scripts/export/manifest.yaml` (its catch-all keeps
the new files, as for `check_adr_answers.py`), `provenance.yaml`, `AGENTS.md`
(198 of 200 lines), `plans/_README.md` and `templates/` (no plan template
exists), `scripts/check_decision_continuity.py` and the continuity table (the
ADR amends no decision), `decisions/answers/` (the answer is recorded), every
existing file under `tests/` and `plans/changes/archive/`, and the four live
changes beyond their `plan.md`.

## Criterion ledger

- 1: tests/test_check_criterion_ledger.py::test_every_live_plan_is_held_whatever_its_date_and_class
  — a live plan dated 2026-09-01 in a `bounded` change, without a ledger, exits 0
- 1: tests/test_check_criterion_ledger.py::test_a_live_change_without_a_plan_is_not_examined
  — a live folder holding only `research.md` is reported
- 2: tests/test_check_criterion_ledger.py::test_a_plan_without_exactly_one_ledger_section_is_reported
- 2: tests/test_check_criterion_ledger.py::test_a_doubled_ledger_heading_on_the_last_line_is_reported
  — no heading, the heading twice, or the heading only inside a fence exits 0
- 3: tests/test_check_criterion_ledger.py::test_an_archived_ledger_is_held_whatever_its_date
  — an archived plan dated 2026-10-01 whose ledger names a deleted test exits 0
- 4: tests/test_check_criterion_ledger.py::test_an_archived_plan_without_a_ledger_is_exempt_only_by_an_earlier_plain_date
  — 2026-10-11, or a quoted, commented, missing, impossible or doubled date, exempted; 2026-10-10 reported
- 5: tests/test_check_criterion_ledger.py::test_a_line_in_no_entry_form_is_reported_with_the_three_forms
  — one of the eleven lines of criterion 5 accepted, or its finding without the three forms
- 5: tests/test_check_criterion_ledger.py::test_the_three_entry_forms_and_continuation_lines_are_read
  — a well-formed entry, a fault after the em dash or a continuation line reported
- 6: tests/test_check_criterion_ledger.py::test_the_gate_goes_red_when_a_named_test_is_deleted
  — exit 0 after the named function, or its file, is deleted (the gate's mutation test)
- 6: tests/test_check_criterion_ledger.py::test_a_prefix_or_an_indented_def_is_not_defined
  — `test_b_more` taken for `test_b`; a `def` inside a class or a function counted
- 7: tests/test_check_criterion_ledger.py::test_the_gate_never_imports_a_named_test_file
  — a named module's top-level code leaves its file behind
- 8: tests/test_check_criterion_ledger.py::test_a_live_not_yet_written_entry_is_accepted
  — a live plan reported for a test that does not exist yet
- 9: tests/test_check_criterion_ledger.py::test_a_not_yet_written_entry_whose_test_exists_is_reported
  — exit 0, or a finding that does not say to remove the marker
- 10: tests/test_check_criterion_ledger.py::test_an_archived_not_yet_written_entry_is_reported
  — exit 0 for the entry, its test defined or not
- 11: tests/test_check_criterion_ledger.py::test_a_not_a_test_entry_is_accepted_on_its_form
  — a well-formed entry whose text names a missing test reported
- 12: tests/test_check_criterion_ledger.py::test_a_criterion_without_an_entry_is_reported
  — exit 0 after a criterion's only entry is deleted
- 13: tests/test_check_criterion_ledger.py::test_an_entry_for_an_unknown_criterion_is_reported
  — `- 99: …` beside a spec of 16 criteria exits 0
- 14: tests/test_check_criterion_ledger.py::test_a_plan_without_a_spec_or_its_criteria_is_reported
  — a missing spec, or one without `## Acceptance criteria`, exits 0
- 14: tests/test_check_criterion_ledger.py::test_criterion_numbers_are_read_across_level_3_headings_and_outside_fences
  — a level-3 heading ends the section, or a numbered line inside a fence counts
- 15: tests/test_check_criterion_ledger.py::test_a_clean_run_names_its_counts
  — a count missing from the line
- 15: tests/test_check_criterion_ledger.py::test_an_empty_tree_says_it_examined_nothing
  — "OK", "pass" or "green" printed, or no "examined nothing"
- 16: tests/test_check_criterion_ledger.py::test_each_finding_is_one_line_with_path_line_and_remedy
- 16: tests/test_check_criterion_ledger.py::test_the_summary_counts_a_change_with_plan_and_spec_findings_once
  — exit 0 or 3 with a finding; a line without the path, the line number or the remedy
- 17: tests/test_check_criterion_ledger.py::test_an_unreadable_or_non_utf8_file_is_a_finding
- 17: tests/test_check_criterion_ledger.py::test_a_not_yet_written_entry_whose_file_cannot_be_read_is_reported
- 17: tests/test_check_criterion_ledger.py::test_an_empty_plan_or_spec_is_reported_without_a_traceback
  — a traceback or exit 0 for a plan, spec or named test file that is a directory or not UTF-8
- 18: tests/test_check_criterion_ledger.py::test_a_root_it_cannot_measure_exits_3
  — exit 0 or 1 for an empty directory, a missing one or a file as the root
- 19: tests/test_check_criterion_ledger.py::test_gates_yaml_declares_criterion_ledger
  — green with the entry removed or one of its four fields changed
- 19: tests/test_ci.py::test_every_gate_step_has_a_mutation_test — the gate without a `goes_red` test
- 19: tests/test_ci.py::test_every_script_has_a_test_or_a_declared_reason
- 19: tests/test_ci.py::test_every_script_has_a_caller_or_a_declared_reason
- 19: not a test — the gate `ci-drift` in `make verify` holds `ci.yml` to the gate list
- 20: tests/test_check_criterion_ledger.py::test_the_kit_carries_the_script_and_its_test
  — either file's role not `mechanismus`
- 20: not a test — the gate `leerprobe` in `make verify` runs the new test in the empty-repository copy
- 21: tests/test_check_criterion_ledger.py::test_the_plan_prompt_requires_the_ledger
  — the heading, the gate or the pointer from the test requirement missing; an example the parser refuses
- 22: tests/test_check_criterion_ledger.py::test_the_implement_prompt_moves_the_ledger_with_the_tests
  — either of the two rules missing
- 23: tests/test_check_criterion_ledger.py::test_the_workflow_names_the_gate_and_its_exemption
  — no row for the gate, or a row without the archive rule or 2026-10-11
- 24: not a test — the gate's run over this repository at the head, under "Verification"; output in the pull request body
- 25: not a test — the reading aid under "Verification", and the phase-6 review of each migrated ledger
- 26: not a test — the phase-6 review of the `stage2-session` ledger against its "Tests and faults"
- 27: not a test — the `grep` under "Verification" shows the pointer line above each table
- 28: not a test — the replay under "Verification"; command, output and commit in the pull request body

## Evidence

This worker has file tools and no shell: the runner runs the commands and
makes the checkpoint commit. What it will see:

- **Step 1 — the four plans migrated.** A `## Criterion ledger` section in
  each, at the place of detail 11, and the pointer line above every
  per-criterion table: `harness-decide-adr` (60 entries — 57 test,
  3 not-a-test), `hermes-runner` (65 — 5 test, 39 not-yet-written,
  21 not-a-test), `research-currency` (35 — 33 test, 2 not-a-test),
  `stage2-session` (72 — 70 test, 2 not-a-test). Every named function was
  checked against the `^def <name>(` line of its file; every criterion number
  of each spec (1–15, 1–59, 1–16, 1–16) is covered.
- **Step 2 — the gate.** `scripts/check_criterion_ledger.py` (standard
  library only) and `tests/test_check_criterion_ledger.py` (28 tests against
  criteria 1–23, each with its planted fault; the mutation test is
  `test_the_gate_goes_red_when_a_named_test_is_deleted`). Wired into
  `decisions/gates.yaml`, `.github/workflows/ci.yml` (the four lines by
  hand — the phase-4 runner does not regenerate it; `ci-drift` checks them)
  and `scripts/kit/manifest.yaml` (both files `mechanismus`). Every
  `not yet written` marker of this step is removed from the ledger above.
- **Step 3 — the texts.** `prompts/03-plan.md` (the test bullet ends "— as
  entries of the criterion ledger below."; the section `## The criterion
  ledger` with the three forms, the example and the gate paragraph),
  `prompts/04-implement.md` ("The ledger moves with the tests."),
  `docs/WORKFLOW.md` (the `Criterion tests` row after `Interview`). The
  tests of criteria 21–23 stand in the ledger without a marker.
- **Step 4 — close.** `implementation_status: partial` in the six artefacts
  of this folder.
- **Attempt 2 — the repairs after attempt 1 ran red.** Six tests crashed on a
  `_tree` helper that could not build its tree twice (`mkdir` without
  `exist_ok`); fixed. The gate reported a change folder without a `plan.md`
  instead of not examining it (one live test, and the three archive folders
  `2026-09-20-2ee-triage`, `2026-09-23-gate-placement` and
  `2026-09-23-tracker-access-point`, which carry only a `research.md`);
  fixed — a folder whose `plan.md` does not exist is skipped. The finding for
  a named test file that cannot be read now names the criterion and the
  function, so an archived ledger naming a deleted test is readable as such.
  An indented `- <n>: …` line is no longer parsed as an entry after
  stripping. `ruff`'s SIM108 is answered with the ternary it asks for, and
  both new files are rewritten with exactly one trailing newline. The
  `interview-minimums` amendment below closes the last block.

```bash
.venv/bin/python -m pytest tests/test_check_criterion_ledger.py -q
.venv/bin/python scripts/check_criterion_ledger.py
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
```

Expected green line of the second command at the head (criterion 24):
`held 5 plans (5 live, 0 archived); read 274 entries (200 test, 39 not yet
written, 35 not a test); 17 archived plans dated before 2026-10-11 exempt`
(measured 2026-10-11 after review-loop round 1, which added four tests to
this change's own ledger; the count before it was 270 with 196 test).
Criterion 28's replay runs on the head commit; its command, output and
commit go into the pull request body.

**For the pull request body** (the plan's migration rule): four functions
the plan names in its implementation notes hold no criterion of the spec and
stand in no ledger line — `test_no_declared_reason_stands_for_a_script_that_has_a_caller`,
`test_no_declared_reason_cites_a_closed_or_unknown_bead`,
`test_the_mutation_ratchet_only_turns_one_way`,
`test_the_two_manifests_really_disagree_somewhere`.

## Phase 4 amendments

Recorded here so the plan and the code say the same thing (a deviation that
lives only in the code is the plan on the next reading):

- **`scripts/check_interview_minimums.py` counts a change folder as the ADR's
  owner only when the diff touches more than its `plan.md`** (amended
  2026-10-11, second phase-4 session). As accepted, this change's diff
  touches `docs/adr/0013-…` and five change folders — its own plus the four
  migrated `plan.md` files — and the gate's owner rule demanded exactly one,
  which made the card's "make verify ends VERIFY GREEN" unreachable, on this
  branch and after the merge. A plan-only folder carries no spec, no
  decisions and no research: it is the migration this plan orders, and the
  gate `criterion-ledger` now polices those very edits. The five answers
  still answer for exactly one folder, and the gate's finding text is
  unchanged. Its counterpart test stands in
  `tests/test_check_interview_minimums.py::test_a_folder_whose_diff_touches_only_plan_md_is_no_owner`;
  counting the plan-only folder again turns it red with
  "owns 2 change folder(s)".

## Runner route — 2026-10-11

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-11 — two sessions worked under this prompt; neither has a clock and
neither claims a span. Each read the date 2026-10-11 at its start and again
at its stop; the runner's clock measures the real span against the appetite
of 8 h, and no duration is invented here.

2026-10-11 — a third repair session (no clock): the count line said "entrys"
for "entries"; fixed in `_s` of the gate, and two escaped quotes in the test
file written as ruff format has them.
