---
title: "Plan — touch-map"
status: draft
implementation_status: none
date: 2026-10-06
last_reviewed: 2026-10-06
updated: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-5p0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, pull-requests, review, diagrams, mermaid, templates]
---

# Plan — touch-map

```text
For you:     every code pull request shows what it touches: a generated list, and a collapsed map when a link is found, in both templates
Done when:   criteria 1–18 hold (tests with planted faults, a run on eight merges, links checked by hand on two), `make verify` green
Appetite:    4 h of phase 4, one repair round included
Not now:     the CI gate that checks the pasted section is current, the question after five pull requests, LakeSwitch, ADR 0009
Pre-mortem:  suppose it failed: most likely because sections go stale after later pushes, and nothing checks them until the freshness gate
Starts unless you say stop.
```

Implements `spec.md` (criteria 1–18). The class is `feature`, ADR answer
"no" (the maintainer, 2026-10-06); `adr-answers` stays red until the
orchestrating session records it. Stage 1: no model markings. Facts read at
`a887b82`.

## Decided in phase 3

No `[DECISION]` is open.

- `[DETAIL]` — **appetite 4 h.** The steps below sum to 3 h 40 min; 20 min
  is one repair round. It is above research 4.9's 2–3 h, which is the note's
  estimate for the prototype's rules alone; the spec adds the join rule,
  outward links, the import delta, removed files and a hand check on two
  merges. Neither `decisions.md` nor `spec.md` states an appetite.
- `[DETAIL]` — **git plumbing only:** `diff-tree`, `ls-tree`, `cat-file`,
  `merge-base`, `rev-parse`, each with `-z` where it lists paths. Porcelain
  `git diff` follows the user's `diff.renames`, `color.ui` and
  `core.quotepath`, and a name with a `"` comes back quoted.
- `[DETAIL]` — **box ids `n1`, `n2`, … in box order**, never from the file
  name: `a-b.py` and `a_b.py` would collide, and `end` closes a block.
- `[DETAIL]` — **labels replace `"` and a backtick with `'`**; the list
  keeps the real path.
- `[DETAIL]` — **output is UTF-8 whatever the locale:** `main` writes the
  encoded text to `sys.stdout.buffer` (the list uses `·` and `→`).

## Slices and steps

Three slices; each ends green and committed. Read `date` at each step
boundary (`prompts/04-implement.md`).

### S1 — the list (110 min)

1. **`scripts/touch_map.py`** (new, 70 min). Docstring: usage, the rules of
   the spec's terms in short, exit codes 0/2/3. Constants at the top — the
   one place an instance changes them: `RUNNERS = ("Makefile",
   "decisions/gates.yaml")`, `RUNNER_DIRS = (".github/workflows/",)`,
   `TESTS = "tests/"`, `CODE = (".py", ".sh")`, `PROSE_DIRS = ("docs/",
   "plans/")`, `REGISTRY_PATHS = 15`, `BASENAME_LONGER_THAN = 8`,
   `SPLIT_FROM = 15`, `MAP_MAX = 30`. Parts:
   - `git(repo, *args) -> str`; `CannotMeasure`; `resolve(repo, base, head)`
     → head, merge base and their short hashes, or `CannotMeasure` (not a
     repository, a revision that does not resolve, no merge base).
   - `changed(repo, mb, head) -> dict[str, str]` from `git diff-tree -r -z
     --no-renames --name-status`: `A` new, `D` removed, else changed.
   - `Snapshot(repo, rev)`: tracked paths, source texts (read lazily with
     `cat-file`), unique long basenames, unique `.py` stems.
   - `kind(path)`, `is_prose(path)`, `code_text(path, body)` (the
     prototype's `code_only`; for non-Python sources drop lines whose first
     non-blank character is `#`).
   - `names(snap, src)` — full path, unique basename, and for Python the
     `/` joins walked on the AST (trailing string constants of a chain of
     `ast.Div`, joined, matching exactly one tracked path or its end after a
     `/`); `imported(snap, src)` — first components of absolute imports
     through the unique stems.
   - `links(snap) -> set[tuple[str, str, str]]` — `(source, target, kind)`
     by the spec's terms, registries and self links skipped.
   - `build(repo, base, head) -> Touch` — boxes (criteria 3 and 5), drawn
     links, fold counts, `still named by`, prose, not linked, imports added
     and dropped; links of a removed file from the merge base's snapshot.
   - `render_list(touch) -> list[str]`, `main(argv=None) -> int` (argparse
     `base`, `head`, `--repo`, default `.`); `CannotMeasure` → the line on
     standard error, exit 3.
2. **Tests, ratchets, kit** (40 min). `tests/test_touch_map.py` (new):
   docstring — every test builds its own repository, so the file holds in
   the probe copy. Helpers as in `tests/test_frontmatter_current.py` (git
   with `-c user.name=t -c user.email=t@example.invalid -c
   commit.gpgsign=false`, `GIT_CONFIG_GLOBAL=/dev/null`,
   `GIT_CONFIG_NOSYSTEM=1`): `_repo`, `_commit(repo, {path: text | None})`,
   `_branch`, and `_run(repo) -> str` calling `touch_map.main(["main",
   "feat", "--repo", …])`. The S1 rows of the table below.
   `scripts/ci_gates.py`: `OHNE_AUFRUFER["touch_map.py"] = "Entry point,
   not a gate — an agent runs it before a pull request and pastes its
   output (prompts/07-commit.md); tests/test_touch_map.py runs it"`.
   `scripts/kit/manifest.yaml`: after the `check_research_currency.py`
   rule, `scripts/touch_map.py` → `mechanismus` ("the pull request
   templates name it, and they travel"); after the
   `test_research_currency.py` rule, `tests/test_touch_map.py` →
   `mechanismus` ("builds its own repositories; holds in the probe copy").
   Verify, commit.

### S2 — the map (70 min)

3. **Map, size lines, lists, caption** (40 min). `render(touch) -> str`
   assembles the whole output below; `render_map` numbers the boxes —
   changed boxes in list order, then unchanged boxes by path, then fold
   boxes in the order of their target — and sorts links by (source number,
   target number, kind). (25 min map and size lines, 15 min lists and
   caption.)
4. **Tests** (30 min): the S2 rows of the table, with the structure check
   `_mermaid_problems(block) -> list[str]` in the test file. Verify,
   commit.

### S3 — the convention and the measurement (40 min)

5. **Templates, template test, prompt** (20 min).
   - Both templates, between the sections the spec names (criterion 14):

     ```markdown
     ## What it touches
     <the output of `python3 scripts/touch_map.py origin/main HEAD`, pasted unchanged after the last push>
     <for a change with a design.md: "Architecture delta: `plans/changes/<name>/design.md`">
     ```

   - `tests/test_pr_templates.py`: `test_both_templates_carry_what_it_touches`
     — the heading once, between its neighbours, the command in the
     section, `(REPO / "scripts" / "touch_map.py").is_file()`; the docstring
     says it reads the script's presence too.
   - `prompts/07-commit.md`, after "The pull request text explains
     itself":

     ```markdown
     - **What it touches is generated, never drawn.** After the last push,
       run `python3 scripts/touch_map.py origin/main HEAD` and paste its
       output under "What it touches" unchanged, in either template. Never
       edit it, and never draw a map by hand or have a model draw one. When
       the branch moves, run it again and replace the whole section. A
       change with a `design.md` adds one line below it:
       `Architecture delta: plans/changes/<name>/design.md`.
     ```

     and "What it touches" after "What changes for you" in the sentence
     that follows the multi-decision form. Verify, commit.
6. **Measurement and close** (20 min). The runs under "Verification"; under
   `## Evidence` here, per merge: boxes, links, size line, map or not; for
   #73 and #65 each drawn link with the `file:line` that makes it, marked
   "dependency" or "fixture path". `implementation_status: partial` in the
   four artefacts of this folder (the freshness gate is still open),
   `python3 scripts/plans_registry.py --index`, verify, commit.

## The output, exactly

The tests assert these texts. A prose-only change prints only its line:

```text
Prose only: no code, runner or test changed.
```

Otherwise (an example; lines in brackets appear only when they apply):

````text
Touched at `a1b2c3d`, against the merge base `e4f5a6b`:

- `scripts/ci_gates.py` (changed) · run by `Makefile`, `scripts/verify_all.sh` · imported by `scripts/harness.py` · tested by `tests/test_ci.py`, +2 unchanged
- `scripts/old.py` (removed) · run by `Makefile` · still named by `Makefile`
- `tests/test_kit.py` (changed) · tests `kit/probe.py`, `Makefile`
- `prompts/07-commit.md` (changed) · tested by +1 unchanged
[- Not linked: `.gitignore`]
[- Prose, not drawn: 4 files]

[Large change: consider splitting it.]
[Map left out: 34 boxes, more than 30.]

<details><summary>Map at a1b2c3d</summary>

```mermaid
flowchart LR
  n1["code: scripts/ci_gates.py (changed)"]:::changed
  n5["code: Makefile"]:::same
  n9(["code: +2 unchanged tests"]):::same
  n5 -->|runs| n1
  n9 -.->|tests| n1
  classDef added fill:#d9f2d9,stroke:#2e7d32,color:#000
  classDef changed fill:#fff2cc,stroke:#b58900,color:#000
  classDef removed fill:#f7d4d4,stroke:#a02a2a,color:#000
  classDef same fill:#f2f2f2,stroke:#999,color:#000
```

- **Added:** none. New imports: `scripts/a.py` → `scripts/b.py`.
- **Changed:** `prompts/07-commit.md`, `scripts/ci_gates.py`, `tests/test_kit.py`.
- **Removed:** `scripts/old.py`. Imports dropped: none.

<sub>Generated by scripts/touch_map.py from the commit a1b2c3d and the merge base e4f5a6b; nothing drawn by hand. Links are found by reading the code, so some may be missing. A box is a file at C4 level code; new, changed and removed show in words and in colour.</sub>
</details>
````

- Lines of changed boxes: code, tests, runners, other; each group by path.
  Groups within a line in this order: `run by`, `read by`, `imported by`,
  `tested by`, `runs`, `reads`, `imports`, `tests`, `still named by`; names
  sorted. A neighbour is named by its label (folder and file); the line's
  own file by its full path.
- A label is `code: ` plus folder and file (`Makefile` alone at the root),
  plus ` (new)`, ` (changed)` or ` (removed)` for a changed box.
- The three lists and the imports in them by path; `1 file` /
  `<n> files`; `none` where a list or delta is empty.

## Tests

| Crit. | Test (in `tests/test_touch_map.py` unless named) | Goes red when (the planted fault) |
| --- | --- | --- |
| 1 | `test_the_working_tree_does_not_count`, `test_two_runs_give_the_same_bytes`, `test_only_the_standard_library` | sources read from disk; a set iterated unsorted; `import yaml` |
| 2 | `test_the_merge_base_is_the_start`, `test_a_rename_is_removed_and_new` | the diff taken from base, not the merge base; rename detection on |
| 3 | `test_which_changed_files_are_boxes` | a code file without links dropped; a script's path naming kept as a link |
| 4 | `test_each_kind_of_link` (import, runner, shell, test path, basename, join, `reads`); `test_what_makes_no_link` (comment, docstring, `#` line, script naming, 8-character basename, basename twice, join ending two paths, registry of 15) | `code_text` returns the raw body; `> 8` becomes `>= 8`; a join takes the first of two paths; the registry threshold off by one |
| 5 | `test_a_tests_only_change_shows_the_code_it_tests`, `test_unchanged_tests_fold`, `test_a_fixture_path_is_not_a_box`, `test_one_hop_only`, `test_no_link_between_two_unchanged_boxes` | links only into changed code (the prototype's rule); one fold per test; an unchanged Markdown target drawn; a second hop; an unchanged pair linked |
| 6 | `test_a_removed_script_still_named` | a removed file's links read at head; no `still named by` |
| 7 | `test_prose_only_is_one_line` | an empty `flowchart LR` printed |
| 8 | `test_the_list_and_the_map_hold_the_same_links`, `test_no_table_or_checkbox` | a link left out of the list; a line starting with `\|` |
| 9 | `test_the_size_lines` at (1 box, no link), 14, 15, 30, 31 boxes — one changed module and unchanged importers — and 14 files plus one fold box | `>= 15` becomes `> 15`; `<= 30` becomes `< 30`; fold boxes not counted |
| 10 | `test_boxes_carry_level_and_status_in_words` | the status word dropped from a label |
| 11 | `test_the_block_holds_by_structure` (`a"b.py`, a backtick name, `end.sh`, `a-b.py` and `a_b.py`); `test_the_structure_check_can_go_red` | labels not cleaned; ids made from names; the check passes an undeclared end |
| 12 | `test_imports_added_and_dropped`, `test_the_caption_names_both_commits` | the delta from head alone; the merge base's hash missing |
| 13 | `test_not_measured` (no repository, unknown revision, unrelated histories), `test_a_usage_error_is_2` | an exception escapes (exit 1); the message on standard output |
| 14 | `tests/test_pr_templates.py::test_both_templates_carry_what_it_touches` | the section below `## Where it fits`; the script renamed |
| 16 | `test_the_kit_carries_the_script_and_its_test` (`probe.rolle`); the ratchets of `tests/test_ci.py`; gate `leerprobe` | a role `bestand`; the `OHNE_AUFRUFER` entry missing |
| 15, 17 | read in phase 6; the runs below, recorded under `## Evidence` | — |
| 18 | `make verify` | — |

Each fault is planted on its own, the suite run, the file restored with
`git checkout`, and the result recorded under `## Planted faults`.

## Verification

```bash
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false make verify
for m in 6c5d51a 3715528 d5813ec a847516 00d7c31 ba940fb 017ec56 87daf91; do echo "== $m"; python3 scripts/touch_map.py "$m^1" "$m^2"; done
```

## Not touched

`decisions/gates.yaml` and `.github/workflows/ci.yml` (no gate: the
freshness gate is a later change), `tests/test_ci.py` (its lists stay;
`OHNE_TEST` and `OHNE_MUTATIONSTEST` do not grow), `scripts/kit/probe.py`
and `REIST_NICHT`, `scripts/export/manifest.yaml` (its catch-all drops the
script, as for the sibling checks), `provenance.yaml`,
`docs/adr/0009-architecture-delta-in-design-md.md`, `docs/WORKFLOW.md`,
`AGENTS.md`, the templates' `Where it fits` line and `DECISION_PARTS` in
`tests/test_pr_templates.py`, and anything in LakeSwitch.

## Planted faults

Every test has its counterpart: a fault planted on its own, the suite run, the
file restored with `git checkout`. Before every fault of slice S1: `python3 -m
pytest tests/test_touch_map.py -q` — **19 passed** at `a21717a`. After: **24
faults, 24 red, none green.** Planted on `a21717a`.

Replay: make the edit in the file of the column `File` — `script` is
`scripts/touch_map.py`, `manifest` is `scripts/kit/manifest.yaml`,
`ci_gates.py` is `scripts/ci_gates.py` — run `python3 -m pytest
tests/test_touch_map.py -q --tb=no` (`tests/test_ci.py` for fault 24), and
restore with `git checkout -- <file>`. "Red" is the number of failing tests;
the tests named are up to three of them, in alphabetical order.

| # | Crit. | File | Fault | Red | Tests that went red |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | script | sources read from disk, not from the commit | 4 | `test_a_removed_script_still_named`, `test_a_rename_is_removed_and_new`, `test_the_merge_base_is_the_start` |
| 2 | 1 | script | a set iterated unsorted (boxes in set order) | 2 | `test_two_runs_give_the_same_bytes`, `test_which_changed_files_are_boxes` |
| 3 | 1 | script | import yaml | 1 | `test_only_the_standard_library` |
| 4 | 2 | script | diff taken from the base tip, not the merge base | 2 | `test_not_measured`, `test_the_merge_base_is_the_start` |
| 5 | 2 | script | rename detection on | 1 | `test_a_rename_is_removed_and_new` |
| 6 | 3 | script | a code file without links dropped | 5 | `test_a_rename_is_removed_and_new`, `test_the_merge_base_is_the_start`, `test_the_working_tree_does_not_count` |
| 7 | 3 | script | a Python code file's path naming kept as a link | 4 | `test_each_kind_of_link`, `test_no_link_between_two_unchanged_boxes`, `test_one_hop_only` |
| 8 | 4 | script | code text is the raw body (comments and docstrings stay) | 1 | `test_what_makes_no_link` |
| 9 | 4 | script | basename rule `> 8` becomes `>= 8` | 1 | `test_what_makes_no_link` |
| 10 | 4 | script | a join takes the first of two paths | 1 | `test_what_makes_no_link` |
| 11 | 4 | script | registry threshold off by one | 1 | `test_what_makes_no_link` |
| 12 | 5 | script | links only into changed code (the prototype's rule) | 2 | `test_a_fixture_path_is_not_a_box`, `test_a_tests_only_change_shows_the_code_it_tests` |
| 13 | 5 | script | an unchanged test drawn as its own box | 3 | `test_the_working_tree_does_not_count`, `test_unchanged_tests_fold`, `test_what_makes_no_link` |
| 14 | 5 | script | an unchanged Markdown target of a changed test drawn | 1 | `test_a_fixture_path_is_not_a_box` |
| 15 | 5 | script | a second hop | 2 | `test_a_tests_only_change_shows_the_code_it_tests`, `test_one_hop_only` |
| 16 | 5 | script | a link between two unchanged boxes drawn | 1 | `test_no_link_between_two_unchanged_boxes` |
| 17 | 6 | script | a removed file's links read at head, not the merge base | 1 | `test_a_removed_script_still_named` |
| 18 | 6 | script | no `still named by` | 1 | `test_a_removed_script_still_named` |
| 19 | 7 | script | no prose-only line: the full list is printed with an empty header | 1 | `test_prose_only_is_one_line` |
| 20 | 13 | script | an exception escapes (exit 1) | 1 | `test_not_measured` |
| 21 | 13 | script | the not-measured line on standard output | 1 | `test_not_measured` |
| 22 | 13 | script | usage error exits 1 | 1 | `test_a_usage_error_is_2` |
| 23 | 16 | manifest | kit role of the script is `bestand` | 1 | `test_the_kit_carries_the_script_and_its_test` |
| 24 | 16 | ci_gates.py | the OHNE_AUFRUFER entry missing | 1 | `test_every_script_has_a_caller_or_a_declared_reason` |


Slice S2 (the map), planted on `badb919`. Before every fault: `python3 -m pytest
tests/test_touch_map.py -q` — **27 passed**. After: **21 faults, 21 red, none
green** — after one repair: fault 41 (the structure check passes a duplicate
id) stayed **green** on the first run, because its bad block also broke the
link-end rule and so still raised a problem. The test was sharpened (each bad
block breaks one rule and the test asserts the problem that names it, commit
`test(touch-map): each bad block …`), the fault was planted again and went red.
`test file` in the column `File` is `tests/test_touch_map.py` itself: the fault
is planted in the structure check, and the test that must go red is the one that
feeds it bad blocks.

| # | Crit. | File | Fault | Red | Tests that went red |
| --- | --- | --- | --- | --- | --- |
| 25 | 8 | script | a link left out of the list (the last drawn link) | 8 | `test_a_fixture_path_is_not_a_box`, `test_a_removed_script_still_named`, `test_a_tests_only_change_shows_the_code_it_tests` |
| 26 | 8 | script | a list line starting with `\|` (the prose line) | 3 | `test_no_table_or_checkbox`, `test_the_list_and_the_map_hold_the_same_links`, `test_which_changed_files_are_boxes` |
| 27 | 8 | script | the fold links left out of the map | 1 | `test_the_list_and_the_map_hold_the_same_links` |
| 28 | 9 | script | `>= 15` becomes `> 15` | 1 | `test_the_size_lines` |
| 29 | 9 | script | `<= 30` becomes `< 30` | 1 | `test_the_size_lines` |
| 30 | 9 | script | fold boxes not counted | 1 | `test_the_size_lines` |
| 31 | 9 | script | `> 30` becomes `>= 30` in the left-out line | 1 | `test_the_size_lines` |
| 32 | 9 | script | a map printed for boxes without a link | 1 | `test_the_size_lines` |
| 33 | 10 | script | the status word dropped from a label | 1 | `test_boxes_carry_level_and_status_in_words` |
| 34 | 10 | script | the level `code:` dropped from a label | 1 | `test_boxes_carry_level_and_status_in_words` |
| 35 | 10 | script | the map outside `<details>` | 3 | `test_boxes_carry_level_and_status_in_words`, `test_no_table_or_checkbox`, `test_the_size_lines` |
| 36 | 10 | script | a link without its kind | 2 | `test_the_block_holds_by_structure`, `test_the_list_and_the_map_hold_the_same_links` |
| 37 | 11 | script | labels not cleaned of `"` and backtick | 1 | `test_the_block_holds_by_structure` |
| 38 | 11 | script | ids made from the file names | 1 | `test_the_block_holds_by_structure` |
| 39 | 11 | script | control characters not flattened (a newline in a name) | 1 | `test_the_block_holds_by_structure` |
| 40 | 11 | test file | the structure check passes an undeclared link end | 1 | `test_the_structure_check_can_go_red` |
| 41 | 11 | test file | the structure check passes a duplicate id | 1 | `test_the_structure_check_can_go_red` |
| 42 | 12 | script | the import delta taken from head alone | 1 | `test_imports_added_and_dropped` |
| 43 | 12 | script | imports dropped not reported | 1 | `test_imports_added_and_dropped` |
| 44 | 12 | script | the merge base's hash missing from the caption | 1 | `test_the_caption_names_both_commits` |
| 45 | 1 | script | unchanged boxes in set order (numbers differ by hash seed) | 3 | `test_a_tests_only_change_shows_the_code_it_tests`, `test_no_link_between_two_unchanged_boxes`, `test_two_runs_give_the_same_bytes` |
