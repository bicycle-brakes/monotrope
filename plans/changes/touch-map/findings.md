---
title: "Findings — touch-map"
category: findings
created: 2026-10-06
updated: 2026-10-06
status: draft
implementation_status: partial
date: 2026-10-06
last_reviewed: 2026-10-06
supersedes: null
superseded_by: null
bead: coding-harness-5p0
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, pull-requests, review, diagrams, mermaid, templates]
---

# Findings — touch-map

Phase 6, round 1, on commit `f06caf4` (branch `feat/touch-map`, eleven
commits over `origin/main` at `d5813ec`), 2026-10-06. The reviewer ran on
Opus 5.5 in a fresh context and wrote no file: the harness refused this one,
so it was returned as text for the orchestrating session to commit. It opened
no pull request and wrote nothing to the tracker. Measured against `spec.md`
(criteria 1–18, the terms, the non-goals and the `[DETAIL]`s) and
`decisions.md`; `plan.md` was read for its rules, its deviations, its planted
faults and its evidence, not as the yardstick. The implementation was read as
`git diff ca597ab..f06caf4`. `templates/findings.md` does not exist on
`origin/main`; the columns are those of
`plans/changes/research-currency/findings.md`, and each finding ends with what
should hold instead.

**Verdict: no BLOCKER, no `[DIVERGENT]`; one `[AMBIGUITY]` (F-3) that needs
one sentence from the maintainer before phase 7.** One MAJOR: drawn links can
be false, and the section tells its reader only that links may be missing
(F-1). Four MINOR: a trailing comment in a shell script, `Makefile` or YAML
runner still makes a link (F-2), the prose-only line hides changed
configuration files (F-4), `still named by` raises a false alarm when a module
moves (F-5), and a dead helper carries the name the plan gives the comment
rule (F-6).

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | MAJOR | MAINT | base | `scripts/touch_map.py`, `render` (the caption) and the naming rules in `names` and `_joins`; `spec.md`, criterion 12 and the non-goal "telling a fixture path from the repository's file" | A drawn link can be false, and nothing in the pasted section says so. The caption says only "Links are found by reading the code, so some may be missing"; when the map is left out (above 30 boxes) or no link is found, the output carries no caveat at all. Measured on 2026-10-06, each line read in its source at the merge's head: **#73 and #65** — 7 of the 37 rows of `plan.md`'s hand check are fixture paths, and I agree with every mark (`tmp_path / "ci.yml"` in `tests/test_gate_machinery.py:222`, a list of paths a test writes into a temporary tree in `tests/test_research_currency.py:119` and `tests/test_frontmatter_current.py:521`, `root / "INDEX.md"` in `tests/test_workflow_entry.py:77`, the rule prefix `"Makefile"` in `tests/test_kit.py:303`, a reason string in `tests/test_ci.py:1088`). **#54** (`ba940fb`) — all four `reads` links are false: `Makefile:25` is an `echo` text ("see AGENTS.md"), `tools/claude-code/hooks/handover.sh:313` a message string, and `tools/claude-code/install.sh:58` and `tools/claude-code/statusline.sh:120` name `~/.claude/settings.json`, the user's home copy, which the plain-substring rule reads as the repository's `.claude/settings.json`. **This branch** (`origin/main HEAD` at `f06caf4`, the section this pull request will carry) — `tests/test_touch_map.py` "tests" `Makefile`, `decisions/gates.yaml` and `workflows/ci.yml`, three of its six links, all file contents of its own fixtures (lines 162, 327, 337). **#66** (`00d7c31`) — none of its 14 links is false. A reviewer reading "`.github/workflows/ci.yml` · tested by +3 unchanged" counts three tests guarding the workflow where two do; the maintainer asked for this section as a review aid, and a wrong arrow sends the eye to the wrong file. The spec admits the rules cannot tell a fixture path from a dependency, so this is not a coding fault; the fault is that the reader is told the opposite direction only. Should hold: wherever the output prints links, it tells its reader that a drawn link can be false — a name in text, not a dependency — as plainly as it says that links can be missing. [criterion 12; non-goals] | fixed in `01ab55d` — reviewed at `4a16cae`, closed: the caption says "Links are found by reading the code, so some may be missing and a shown one can be false (a name in text, not a dependency)." — one sentence, and the same words stand on a line of their own below `Map left out: …` when the list prints links and no map follows (#54 at `ba940fb`, measured). The eight merges of criterion 17, run with the script of `043023a` and of `4a16cae`, differ in that clause alone. Replayed on `4a16cae`: faults 52 and 53 1 red each, as recorded; an own variant that prints the caveat before the left-out line 1 red. Fault 54 planted at the guard the repair added (`if has_links:` in the left-out branch) stays green — F-8 |
| F-2 | MINOR | SPEC | base | `scripts/touch_map.py`, `read_code`, the branch for sources that are not Python; `tests/test_touch_map.py`, `test_what_makes_no_link` | A name in a trailing comment of a shell script, a `Makefile` or a YAML runner makes a link. Measured on `f06caf4` with a fixture of its own: `echo hi  # see scripts/subject_tool.py` in `scripts/run_all.sh` gives `scripts/subject_tool.py` "run by `scripts/run_all.sh`"; the recipe line `echo build # scripts/other_tool.py` in `Makefile` gives "run by `Makefile`"; `steps: [] # data/config.yaml` in `decisions/gates.yaml` gives "read by `decisions/gates.yaml`". The code drops only lines whose first non-blank character is `#`, as `plan.md` step 1 says; the spec's code text is the text "without its comments", and criterion 4 says a name in a comment makes no link. The test holds whole-line comments only, so the gap stays green. No effect today: at `f06caf4` and at the heads of #73, #65, #54 and #66, no link of a runner or shell script comes from a name that follows ` # ` alone (cut naively, measured). Not marked `[DIVERGENT]`: the plan gives its rule as the way to build the spec's term, not as a second answer to it; the spec stays the yardstick and the code falls short of it. Should hold: a name after a `#` that starts a comment in a non-Python source makes no link — or the spec narrows its term to whole-line comments, which is the maintainer's amendment, not the reviewer's. [criterion 4; terms, "Code text"] | fixed in `a696b03` — reviewed at `4a16cae`, closed for trailing comments: `echo hi  # x`, `steps: [] # x` and a recipe comment are cut; `$#`, `${#x}`, `${path#scripts/}`, `$(( 16#ff ))`, `a#b`, a URL fragment, `\#`, `"x # y"`, `'x # y'` and YAML's `'it''s # x'` stay code. At the heads of this repository (`4a16cae`), portfolio-agentic-engineering (`20a279c`) and lakeswitch-ai (`09c9d62`) the rule cuts 35 lines in mid-line, every one a true trailing comment, and against the whole-line rule it loses and adds no link (measured). Replayed: faults 56 and 57 2 red each, 58 1, 60 1, 61 2, as recorded; an own variant that takes a tab for no blank 1 red. The same cut can take a name the shell reads — F-7 |
| F-3 | MINOR | SPEC | base | `spec.md`, terms, "Link", the kind `reads`; `plan.md`, "Deviations of phase 4", first bullet; `scripts/touch_map.py`, `links` | `[AMBIGUITY]` Does a runner or shell script that names another runner make a link? The spec says "`reads` — a runner or shell script names any other file". Read as plain English, "any other file" is any file that `runs` does not cover, runners included, so `Makefile` naming `decisions/gates.yaml` reads it. Read as the bold term defined three lines above ("A file that is none of them is **other**"), a runner is not "other", and the naming makes no link. Criterion 4's list of what makes no link does not name this case, so the list does not decide it. Phase 4 chose the second reading in the code and recorded it as a deviation; the review rule is that two plausible readings are not decided locally. No effect today: no runner or shell script names a runner at `f06caf4` or at the heads of #73, #65, #54, #66, #70 and #71 (measured). Should hold: the maintainer picks one reading. Recommended: the second, as built — no code changes, one clause in the spec's terms ("a runner names no runner"); the first means one branch in `links` and a fixture. | decided 2026-10-06 (maintainer: no link) — recorded in `29ff487`, reviewed at `4a16cae`, closed: the addendum of `decisions.md` states the question and the answer as given ("Kein Pfeil", no arrow); the term "Link" in `spec.md` carries "a runner names no runner — a runner or shell script that names another runner makes no link", with Amendment 1; the code makes no link from a runner or shell script to a runner and changed nowhere for it. The exclusion has no fixture — F-9 |
| F-4 | MINOR | SPEC | base | `spec.md`, criterion 7; `scripts/touch_map.py`, `render`; `tests/test_touch_map.py`, `test_prose_only_is_one_line` | The prose-only line is printed when files changed that are not prose, and it names none of them. Measured on `f06caf4`: a fixture that changes only `pyproject.toml`, `.gitignore` and `docs/a.md` prints exactly `Prose only: no code, runner or test changed.`; the two configuration files appear nowhere, although criterion 8 would list them under "Not linked" as "neither boxes nor prose". In this repository: `python3 scripts/touch_map.py 2ab9faf ca597ab`, the commit that adds `decisions/answers/touch-map/adr.yaml` alone, prints the prose-only line — and a pull request that adds an ADR answer is a decision pull request (house rule 8). The code follows criterion 7 to the letter, and the test asserts it (`data/x.json` and `docs/new.txt` among the changed files); the spec calls "prose" what criterion 8 says is not. Should hold: a changed file that is neither prose nor a box is named even when no box exists, so "Prose only" is said only of prose — a spec amendment, the maintainer's choice. [criteria 7, 8] | fixed in `b7e532f` — reviewed at `4a16cae`, closed: `python3 scripts/touch_map.py 2ab9faf ca597ab` (the ADR answer alone) prints the header line and ``- Not linked: `decisions/answers/touch-map/adr.yaml` ``, nothing else; #68 and #72 (`3715528`, `6c5d51a`), prose alone, still print the one line. Amendment 4 rewrites criterion 7 as the code does. Replayed: faults 65 and 67 1 red each, as recorded; an own variant that prints the prose line only beside a box 1 red |
| F-5 | MINOR | MAINT | base | `scripts/touch_map.py`, `still_named` | `still named by` raises a false alarm when a module moves to another folder. Measured on `f06caf4` with a fixture: `scripts/helper_mod.py` becomes `lib/helper_mod.py`, and `scripts/user_mod.py` keeps `import helper_mod`, which now resolves to the moved file. The output says `scripts/helper_mod.py` (removed) · … · still named by `scripts/user_mod.py`, and in the same list `lib/helper_mod.py` (new) · imported by `scripts/user_mod.py`. A reviewer reads a dangling import that does not exist. Criterion 6 asks for "imports its stem" without asking whether the stem still resolves to another file, so the code meets the letter. Should hold: an import counts as still naming a removed file only when its stem resolves to no tracked file at head. [criterion 6] | fixed in `fd9dab2` — reviewed at `4a16cae`, closed: an import counts only when no tracked `.py` file at head has the stem (`Snapshot.py_stems`, shared stems included); a path in text counts as before. Replayed: faults 62 and 63 1 red each, as recorded; an own variant that drops the path-in-text half 2 red. The trade is the one this row asked for: a removed file whose stem another tracked file keeps is no longer `still named by` an import, even one that reached it; at `4a16cae` no `.py` stem is shared in this repository (measured), so no row |
| F-6 | MINOR | MAINT | base | `scripts/touch_map.py`, `code_text` (line 217); `plan.md`, "Tests", the row of criterion 4 | `code_text` is defined and called nowhere; the comment rule lives in `read_code`. `plan.md`'s test table names `code_text` as the place of the criterion-4 fault ("`code_text` returns the raw body"). Planted there on `f06caf4` (`return body`), all 27 tests of `tests/test_touch_map.py` stay green; planted in `read_code`, as `plan.md`'s fault 8 actually was, one goes red. A maintainer who changes the comment rule where the plan points changes nothing, and a replay that follows the plan's table measures nothing. Should hold: the function the plan names as the comment rule is the one the links are read through. [criterion 4] | fixed in `7262704` — reviewed at `4a16cae`, closed: no `code_text` is left in `scripts/` or `tests/`; step 1 and the criterion-4 row of the test table in `plan.md` name `read_code` and `_strip_comment`, and a raw body planted in `read_code` turns the tests red (faults 60 and 61, replayed). The table's test column for criterion 4 still lists the phase-4 tests only; the two new ones stand in the round's fault table, so a replay finds them — no row |
| F-7 | MINOR | SPEC | fix-r1 | `scripts/touch_map.py`, `_strip_comment`; `plan.md`, "Repair round 1", "The comment rule of F-2" | The new comment rule also cuts names the shell reads as code, and the plan says it never does ("Two limits, both on the side of a link kept (never of a link lost)"). Measured on `4a16cae` with a fixture of its own, `scripts/run_all.sh` holding three lines the shell does not treat as comments: an inner line of a quote that runs over two lines (`MSG="usage:` / `  run_all.sh # then scripts/quote_tool.py"`), a heredoc body line (`step # scripts/heredoc_tool.py`), and a `#` after an escaped blank (`sed -e s/\ #.*// scripts/escaped_tool.py`, where sed reads the file). The script of `043023a` gives each of the three new files "run by `scripts/run_all.sh`"; the script of `4a16cae` gives none of them a link. Shell agrees with the rule on a single line — an apostrophe in plain text (`don't`) opens a quote there too — so the per-line quote is a limit on both sides: it keeps a comment after a closing quote's line and cuts a name on a quote's inner line. No effect today: at the heads of this repository, portfolio-agentic-engineering and lakeswitch-ai the rule loses no link (F-2's status). Not `[DIVERGENT]`: the plan describes the rule's limits wrongly; it does not give a second rule. Should hold: the plan names the side each limit errs on as measured — a name after a blank-preceded `#` on an inner line of a quote or heredoc, or after an escaped blank, makes no link though the shell reads it — or the rule leaves those cases uncut. [criterion 4; terms, "Code text"] | open |
| F-8 | MINOR | SPEC | fix-r1 | `tests/test_touch_map.py`, `test_links_may_be_false_wherever_they_are_printed`; `scripts/touch_map.py`, `render`, the left-out branch | The amended rule "where no link is printed there is none" (Amendment 2) is held by no test where it was added, the case of more than 30 boxes and no link. Planted on `4a16cae`: `if has_links:` in the left-out branch becomes `if True:` — all 32 tests of the file pass. The test's only no-link case is one box (`_star(tmp_path, 0)`), which never reaches that branch. Under the fault, a fixture adding 31 unlinked code files prints "Links are found by reading the code, so some may be missing and a shown one can be false …" below a list that shows no link; at `4a16cae` it prints no such line (both measured). `plan.md` records fault 54 ("the caveat line printed whether or not a link is printed") as 1 red; planted as a caveat appended to every output, it is (measured), so the record holds for that plant and says nothing of the guard. Should hold: a fixture with more than 30 boxes and no link whose output carries no caveat line. [criterion 9; Amendments, 2] | open |
| F-9 | MINOR | SPEC | fix-r1 | `tests/test_touch_map.py`, `test_what_makes_no_link`; `spec.md`, terms, "Link", and Amendments, 1 | The exclusion the maintainer decided for F-3, "a runner names no runner", has no fixture, though criterion 4 asks for "a fixture for each kind and each exclusion". Planted on `4a16cae`: in `links`, a runner or shell script that names a runner makes a `reads` link (`target in ("other", "runner")`) — all 32 tests pass. No fixture has a runner name a runner, so the decided reading and the rejected one are the same to the tests, and a later change to `links` can flip the decision unseen. Amendment 1 says "the code already did this; only the clause is new", which is true of the code and leaves the test out. Should hold: one fixture in which `Makefile` names `decisions/gates.yaml` (or a shell script names a workflow) and neither gets a link from it. [criterion 4; terms, "Link"] | open |

Reviewer session: none — phase 2a was skipped (`spec.md`, "Phase 2a not
run"); this review ran in a fresh session.

## Checked without a finding

- **Links against their lines (criterion 17).** All 37 rows of `plan.md`'s
  hand check for #73 and #65 were found again by an independent search of
  each source at the merge's head; every `file:line` matches, and none
  comes from a comment, a docstring or a registry. Samples from #54 and #66
  were read the same way (F-1 for the false ones). Re-run on 2026-10-06:
  the eight merges give exactly the counts of `plan.md`'s table (#73 13
  boxes, 11 + 4 links; #70 4, 2 + 1; #66 17, 9 + 5; #54 36, 30 + 9, map
  left out; #65 21, 17 + 1; #71 4, 0 + 2); #68 and #72 print the prose-only
  line; each of the five tests of #65 has a link to code it tests. Two runs
  on `origin/main HEAD` gave the same bytes.
- **The Mermaid block (criteria 10, 11).** Parsed — not rendered — with the
  parser of mermaid 11.17.2 under jsdom (an install in another session's
  scratchpad, used read-only; nothing installed): the maps of #73, #70, #66,
  #65, #71, this branch's own section, and a fixture with 20 odd names
  (`a"b.py`, a backtick, `end.sh`, `a-b.py` beside `a_b.py`, `pi|pe.py`,
  `br[ack]et.py`, `cu{rl}y.py`, `pa(re)n.py`, `ha#sh.py`, `semi;colon.py`,
  `<b>tag.py`, `%%pct.py`, a space, an umlaut, `click.py`, `o.py`, `x.py`) —
  all seven parse. The parser bites: a block with a `"` inside a label and
  one with a box called `end` are both refused. Ids are `n1`, `n2`, … and
  unique; every label stands in double quotes with `"` and backtick turned
  into `'`. Two names parse but would not show as written: `#quot;` is a
  Mermaid entity and `<b>` an HTML tag inside a label; no tracked name
  carries either, so no row. Whether GitHub renders the block stays the
  maintainer's look on the phone.
- **The deviations of phase 4.** None is `[DIVERGENT]`. The first is F-3.
  The control character turned into `?`, the two extra tests, `main`
  returning argparse's code (`--help` gives 0 and help text, which is not a
  usage error), the registry count without the source's own path, the
  `--full-tree` listing, and `still named by` reading registries too
  (criterion 6 says "a source", registries included) each fill a gap the
  spec leaves and contradict no criterion.
- **Templates and prompt (criteria 14, 15).** Both templates carry
  `## What it touches` once, between the sections criterion 14 names, with
  the placeholder for `python3 scripts/touch_map.py origin/main HEAD`
  "pasted unchanged after the last push" and the optional `Architecture
  delta:` line, nothing else; `test_both_templates_carry_what_it_touches`
  holds the order, the count, the two lines and the script's presence.
  The bullet in `prompts/07-commit.md` carries every part criterion 15
  lists: after the last push, the command, paste unchanged in either
  template, never edit, never draw a map by hand or by a model, run again
  and replace the whole section when the branch moves, and the
  `Architecture delta:` line for a change with a `design.md`; the closing
  sentence of the multi-decision form names "What it touches". The
  templates set the path of the delta line in backticks, the prompt and
  the spec do not; GitHub shows the same words, so no row.
- **Ratchets, kit and provenance (criterion 16).** `scripts/ci_gates.py`
  gains one `OHNE_AUFRUFER` entry; `tests/test_ci.py` and
  `scripts/kit/probe.py` are not in the diff, so `OHNE_TEST`,
  `OHNE_MUTATIONSTEST` and `REIST_NICHT` are unchanged. Both new files have
  the role `mechanismus` (test; replay of fault 23 not repeated), and the
  gate `leerprobe` is green. The export manifest drops `.github/`,
  `prompts/` and the script alike, so no exported file names a missing
  one. Only standard-library imports (test).
- **Determinism, git and exit codes (criteria 1, 2, 13).** Plumbing only,
  with `-z` and `--no-renames`; sources come from `cat-file --batch`;
  every set is sorted before it is printed. Exit 3 with the not-measured
  line and nothing on standard output for a plain directory, a missing one,
  an unknown revision and unrelated histories; exit 2 for usage (tests).
- **Language.** The script, the test, the template lines, the prompt
  bullet, the kit and gate reasons and the commit messages of the
  implementation are English; the added lines carry no German. The commit
  `ca597ab` (the ADR answer) quotes the maintainer's answer "Nein", which
  is a quotation.
- **Planted faults.** Fifteen of the plan's 51 replayed on a clone of
  `f06caf4`, each planted alone, the test file run, the file restored with
  `git checkout`: 5 (rename detection on) 1 red; 8 (code text is the raw
  body, in `read_code`) 1; 9 (`>=` for the basename) 1; 11 (registry off
  by one) 1; 17 (a removed file's links read at head) 2; 19 (no prose-only
  line) 1; 22 (usage exits 1) 1; 28 (`> 15`) 1; 30 (fold boxes not counted)
  1; 33 (status word dropped) 1; 38 (ids from names) 1; 40 (the structure
  check passes an undeclared end) 1; 43 (imports dropped not reported) 1;
  44 (the merge base's hash missing from the caption) 1; 46 (the section
  below `## Where it fits`, ordinary template) 1. Every count matches
  `plan.md` except fault 17: 2 red here against 1 recorded, because it was
  planted on `a21717a`, before `test_the_list_and_the_map_hold_the_same_links`
  existed, and that test now goes red too. Own variants: runners counted as
  registries — 1 red; only column-0 `#` lines treated as comments — 1;
  a basename that need not be unique — 1; the split hint from 14 — 1; a
  fold box without `code:` — 1; `still named by` ignoring the import stem —
  1; the fold arrow solid instead of dotted — green, and no criterion asks
  for a dotted arrow, so no row. The trailing-comment fixture of F-2 and
  the plant in `code_text` of F-6 are the two that a criterion needs.
- **Green (criterion 18).** `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign
  GIT_CONFIG_VALUE_0=false make verify` on `f06caf4`: VERIFY GREEN, 628
  passed and 15 skipped; `docs-links` and `markdownlint` red but report-only,
  as `plan.md` says.

## Not checked

No rendering: the blocks were parsed, not drawn, and not on GitHub. The
other 36 planted faults were not re-run. A partial clone, where
`cat-file --batch` may fetch from the network, was not tried. Labels that
two boxes share after shortening to folder and file (`a/x/b.py`, `c/x/b.py`)
were not built.

## For phase 7

`plans/INDEX.md` is to be regenerated with `python3 scripts/plans_registry.py
--index` when this file is committed. No BLOCKER and no `[DIVERGENT]`; the
gate waits for one sentence: the maintainer's reading of F-3. F-1 is the row
that matters for the maintainer's use of the section: it fits a repair round
of one caption clause before the convention takes hold, or stands as a named
limit — the maintainer's choice. F-2, F-5 and F-6 fit the same round; F-4
needs a spec amendment or stands as a limit. The pull request adds
`decisions/answers/touch-map/adr.yaml`, a path `provenance.yaml` reserves
for `human-decided`, so under house rule 8 it is a decision pull request
(`decide(…)` title, label `decision`, the decision template); it names bead
coding-harness-5p0 in its body.

## Repair round 1 (2026-10-06)

The maintainer answered the `[AMBIGUITY]` F-3 ("Kein Pfeil", recorded in
`decisions.md` and `spec.md`) and set the standing rule that MAJOR rows are
repaired and MINOR rows on tests, security or false statements are repaired
without asking. All six rows are therefore set to "fixed" or "decided", each
"not reviewed": the repair is the author's, and no reviewer has read it. What
each repair does, the 16 faults planted against the new tests (all red) and
the comparison of the eight merges are in `plan.md`, "Repair round 1".
`spec.md` gained a section "Amendments" with four dated entries (F-3, F-1,
F-5, F-4). Nothing above this line was changed except the Status column.

## Phase 6, round 2 (2026-10-06)

The repair read on commit `4a16cae` (branch `feat/touch-map`), 2026-10-06,
by a reviewer on Opus 5.5 in a fresh context that wrote nothing but this
file, opened no pull request and wrote nothing to the tracker. It read the
repair diff `043023a..4a16cae` — the script, its tests, the addendum of
`decisions.md`, the four amendments of `spec.md` and "Repair round 1" of
`plan.md` — against rows F-1 to F-6. Above this section only the Status
column of F-1 to F-6 changed, and rows F-7 to F-9 were added.

**Verdict: F-1 to F-6 are closed; three new MINOR rows, all of origin
`fix-r1` (F-7, F-8, F-9). No BLOCKER, no `[AMBIGUITY]`, no `[DIVERGENT]`:
nothing here stops phase 7.** F-7 is a false sentence in `plan.md` about the
limits of the new comment rule, with a measured case behind it; F-8 and F-9
are one missing fixture each. All three fall under the maintainer's standing
rule of 2026-10-06 (MINOR rows on tests or false statements are repaired
without asking). One more repair round may take them; a row that round
produces is `fix-r2` and goes to the maintainer.

- **Amendments 2 and 3: acceptable `[DETAIL]`s, not scope creep.** Each
  follows from a repair the standing rule covers, only adds, is dated, names
  its row, and `plan.md` records the reason. Amendment 3 is needed: criterion
  6 says a source that "imports its stem" is reported as `still named by`,
  and the repair of F-5 stops saying so when the stem resolves to another
  file — without the amendment the code would fall short of the criterion's
  letter. Amendment 2 is not needed by the letter (criterion 12 asks for the
  "missing" clause at least, and criterion 9 forbids no further line), but
  it makes the caveat a promise of the spec that the tests hold, where the
  yardstick belongs. `spec.md` lies under `plans/`, which `provenance.yaml`
  classes `ai-drafted-reviewed`, so an agent may amend it; `git diff
  043023a..4a16cae -- plans/changes/touch-map/spec.md` adds 46 lines and
  removes none, and the maintainer sees all four amendments at the merge.
- **Replays.** Twelve of the round's 16 planted faults, each alone on a clone
  of `4a16cae`, the 32 tests of `tests/test_touch_map.py` run, the file
  restored: 52 → 1 red, 53 → 1, 54 → 0, 56 → 2, 57 → 2, 58 → 1, 60 → 1,
  61 → 2, 62 → 1, 63 → 1, 65 → 1, 67 → 1. Every count and test name but
  fault 54's is as `plan.md` records it; 54 was planted at the guard the
  repair added and is red (1) only when planted as a caveat in every output
  — F-8. Own variants: a tab not taken for a blank 1 red; the caveat line
  before the left-out line 1 red; the prose line only beside a box 1 red;
  `still named by` without the path in text 2 red; a runner naming a runner
  makes `reads` — green, which is F-9; a backslash that escapes inside
  single quotes too — green, but that plant only keeps a comment as code (a
  link kept, never lost) and no criterion speaks of escapes, so no row.
- **The Mermaid block.** The saved section `touch-map-section.md` — the
  output of `python3 scripts/touch_map.py origin/main HEAD` at `4a16cae`
  against `d5813ec`; a fresh run gives the same bytes — parsed, not
  rendered, with the parser of mermaid 11.17.2 under jsdom (the install in
  another session's scratchpad, used read-only; nothing installed): ok. The
  parser still bites: a label holding `"` and a box id `end` are both
  refused.
- **The suite.** `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign
  GIT_CONFIG_VALUE_0=false make verify` on `4a16cae`: VERIFY GREEN, 633
  passed and 15 skipped; `docs-links` and `markdownlint` red but
  report-only, as in round 1.
- **Seen, not a row.** When a map is drawn, the caveat stands in the
  collapsed `<details>` caption beside the "missing" clause it was asked to
  match, and the list above prints links without it. `still named by` is a
  name in text as well and can be false, and no caveat follows it when the
  change draws no link; it is no link in the spec's terms, and F-1 asked
  for links.

Not checked: faults 55, 59, 64 and 66 of this round; rendering on GitHub or
the phone; any Python but 3.12.4.

For phase 7: no row stops the pull request. F-7 is one sentence in
`plan.md` (or a narrower cut in `_strip_comment`), F-8 and F-9 one fixture
each — one more repair round, or named limits, the maintainer's choice.
What round 1 said for phase 7 still holds: the pull request adds
`decisions/answers/touch-map/adr.yaml`, so it is a decision pull request
under house rule 8; its body names bead coding-harness-5p0 and the four
amendments of `spec.md`.
