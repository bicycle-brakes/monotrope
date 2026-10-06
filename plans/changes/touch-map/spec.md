---
title: "Spec — touch-map"
status: draft
implementation_status: partial
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
tags: [spec, pull-requests, review, diagrams, mermaid, templates]
class: feature
change: touch-map
adr_question: {proposed: "no", answered_by: null, reason: "It adds a pull request convention and the script that fills it, decides nothing about the architecture, and leaves ADR 0009 unchanged, as the maintainer chose on 2026-10-06."}
---

# Spec — touch-map

The first slice of bead coding-harness-5p0: every code pull request carries
a generated section "What it touches" — a list of the touched files and what
runs, imports or tests them, and a collapsed Mermaid map in the form of
ADR 0009. Inputs: [`research.md`](research.md) (read at `d5813ec`; its
section 5 adds what phase 2 measured at `a887b82`) and
[`decisions.md`](decisions.md). The class is `feature`; the maintainer
answered the ADR question "no" on 2026-10-06 (`decisions.md`, addendum), and
the orchestrating session records that answer.

## Problem

A reviewer of a pull request here sees which files changed, not what they
touch:

- Nothing in a pull request body says which code a change reaches — which
  runner starts a changed script, which tests hold it, what imports it. The
  two templates have no such section (research 1.7).
- A diagram drawn by an agent cannot be checked: the review bots show the
  failure modes, and a syntax check would need Node.js, which ADR 0009 keeps
  out of the kit (research 1.9; the note §4 (a)).
- The prototype that generates such a list draws nothing for a pull request
  that changes only tests (#65), misses paths that tests build with `/`
  joins (6 links at `d5813ec`), counts tested Markdown as prose, and prints
  an empty map for a prose-only change (research 1.4, 1.5).
- The maintainer asked for "a diagram of the module's code in every PR, as a
  standard for PR reviews", as a pull request convention, not an amendment
  of ADR 0009 (`decisions.md`, items 1 and 2).

## Terms

- **Base, head, merge base.** The command gets two revisions, base and
  head; the merge base is git's merge base of the two.
- **Changed file.** A path in the difference between the merge base and
  head, with its status in words: `new`, `changed` or `removed`.
- **Code file** — a `.py` or `.sh` file outside `tests/`. **Test** — a `.py`
  file under `tests/`. **Runner** — `Makefile`, `decisions/gates.yaml`, or a
  file under `.github/workflows/`. These three are the **sources**: the files
  whose text is read for links. A file that is none of them is **other**.
- **Code text.** A source's text without its comments; for a Python file
  also without docstrings.
- **Names.** A source names a tracked file when its code text holds the
  file's full path; or holds the file's basename, where that basename is
  unique among the tracked files and longer than eight characters; or — in a
  Python source — holds a chain of `/` joins whose trailing string segments,
  joined by `/`, are the whole path of exactly one tracked file or its end
  after a `/`.
- **Imports.** A Python source imports a tracked `.py` file when an absolute
  `import` or `from … import` has that file's stem as its first component,
  and no other tracked `.py` file has that stem.
- **Link.** From a source to another tracked file, of one kind:
  `tests` — a test names or imports it; `runs` — a runner or shell script
  names a code file or test; `reads` — a runner or shell script names any
  other file; `imports` — a Python code file imports it. A Python code file
  makes no link by naming a path, and a **registry** — a source other than a
  runner that names 15 or more tracked files by full path — makes none.
- **Box.** A node of the map. A **fold box** stands for the unchanged tests
  that link to one changed file. The box count includes fold boxes.

"Tracked" means at the revision being read: head, or the merge base for a
removed file. "A fixture" is a git repository a test builds in a temporary
directory.

## Acceptance criteria

Each criterion names what would refute it.

1. **Only the two commits count.** The command
   `python3 scripts/touch_map.py BASE HEAD [--repo PATH]` reads the
   repository through git objects only — never its working tree, never the
   network — and imports nothing outside Python's standard library. The same
   base and head give byte-identical output.
   *Refuted by:* a fixture whose uncommitted edit, which would add a link,
   changes the output; two runs that differ; an import outside
   `sys.stdlib_module_names`.

2. **The changed files.** They are the difference between the merge base
   and head, without rename detection: a renamed file is one `removed` and
   one `new` file. A commit on base after the fork is not a change.
   *Refuted by:* a fixture where a file changed only on base after the fork
   is listed, or a rename is shown as one changed file.

3. **Which changed files are boxes.** Every changed code file, test and
   runner is a box, with or without links. A changed other file is a box
   when a test, runner or shell script links to it.
   *Refuted by:* a changed code file without links missing from the list;
   a changed YAML file a test names not drawn; a changed Markdown file that
   only a Python code file names drawn.

4. **The links.** Exactly the links of the terms above are found, each with
   its kind. A name in a comment or docstring, a path a Python code file
   only names, a basename outside a join that has eight characters or fewer
   or is not unique, a join that ends more than one tracked path, and every
   name in a registry make no link.
   *Refuted by:* a fixture for each kind and each exclusion in which a link
   is missing, appears where it must not, or has another kind.

5. **One hop from the change.** An unchanged runner, shell script or Python
   code file that links to a changed box is a box. An unchanged code file or
   runner that a changed test links to is a box — so a change of tests alone
   still shows the code they test. The unchanged tests that link to a
   changed box fold into one fold box, `+k unchanged tests`, per changed
   box. No other unchanged file is a box, and a link is drawn only when at
   least one of its ends is a changed file.
   *Refuted by:* a fixture changing only a test that draws no box for the
   code it imports; an unchanged test drawn as its own box; an unchanged
   Markdown file a changed test names drawn as a box; a file two links away
   from every changed file drawn; a link between two unchanged boxes drawn.

6. **Removed files.** A removed file's links are read at the merge base.
   When a source at head still holds its path or imports its stem, its line
   says `still named by` with those sources.
   *Refuted by:* a fixture removing a script that `Makefile` ran and still
   names, whose line does not say `still named by` with `Makefile`, or that
   shows no `runs` link from `Makefile`.

7. **Prose only.** When no changed file is a box, the output is exactly the
   one line `Prose only: no code, runner or test changed.`
   *Refuted by:* a fixture changing only Markdown under `docs/` whose output
   is anything else — an empty map, a list, a second line.

8. **The list.** Otherwise the output begins with a line naming the head
   and the merge base by short hash; then one line per changed box with its
   path, its status, and every drawn link it has, by kind, with the other
   end's name — folded tests as `+k unchanged`; then, when there are any,
   one line naming the changed files that are neither boxes nor prose, and
   one line with the number of prose files — Markdown, or under `docs/` or
   `plans/` — that are not boxes. No line of the output starts with `|`, and
   none is a checkbox.
   *Refuted by:* a fixture where a link drawn in the map is missing from the
   list or a link in the list is not drawn; a changed file in no line; a
   table or checkbox line.

9. **When the map is drawn.** The map is printed when the boxes have at
   least one link and number at most 30. From 15 boxes on, the output
   carries the line `Large change: consider splitting it.` Above 30 boxes it
   carries `Map left out: <n> boxes, more than 30.` and no map.
   *Refuted by:* fixtures with one box and no link (a map printed), 14 boxes
   (a hint), 15 and 30 boxes (no hint or no map), 31 boxes (a map, or no
   hint, or no left-out line), or one in which a fold box is not counted.

10. **The map's form.** The map follows the list inside
    `<details><summary>Map at <head short hash></summary>` and
    `</details>`, as a fenced `mermaid` block holding a `flowchart LR`.
    Every box is labelled with its C4 level `code:` (ADR 0009) and the file
    — a fold box `code: +k unchanged tests` — and a changed box also with
    its status in words, `(new)`, `(changed)` or `(removed)`, besides its
    colour. Every link carries its kind as its label.
    *Refuted by:* a box without `code:`, a changed box whose status shows
    only as colour, a link without its kind, or a map outside `<details>`.

11. **The block holds by structure.** Every line of the Mermaid block is
    `flowchart LR`, a box, a link or a class definition. Box ids are unique,
    match `[A-Za-z0-9_]+`, and none is `end`. Every label stands in double
    quotes and holds no `"` and no backtick, whatever the file is called.
    Both ends of every link are declared boxes. The tests hold this with a
    structure check of their own, standard library only; whether GitHub
    renders the block stays the maintainer's look on the phone.
    *Refuted by:* a fixture with files named with a `"`, with a backtick,
    `end.sh`, or `a-b.py` beside `a_b.py`, whose block breaks one rule; or a
    structure check that passes a block with an undeclared link end.

12. **The three lists and the caption.** Inside the same `<details>`,
    below the block: **Added**, **Changed** and **Removed** — the changed
    boxes by status — with the `imports` links of changed code files that
    exist at head but not at the merge base under Added, and those gone
    since the merge base under Removed. Then one caption line that names the
    head and the merge base by short hash, says the map is generated by
    `scripts/touch_map.py` and nothing is drawn by hand, and says the links
    are found by reading the code, so some may be missing.
    *Refuted by:* a fixture where a changed module gains an import that is
    not under Added, or loses one that is not under Removed; a caption
    without both hashes.

13. **Exit codes.** 0 when the output is printed. 2 on a usage error. 3 —
    with a line on standard error beginning `touch-map: not measured` and
    nothing on standard output — when the path is not a git repository, a
    revision does not resolve, or the two revisions have no merge base.
    *Refuted by:* a fixture for each case with another exit code, output on
    standard output, or no such line.

14. **The template section.** Both pull request templates carry
    `## What it touches` once: the ordinary one between `## What changes`
    and `## Where it fits`, the decision one between `## What changes for
    you` and `## Where it fits`. The section holds the placeholder for the
    output of `python3 scripts/touch_map.py origin/main HEAD`, pasted
    unchanged, and one optional line `Architecture delta:
    plans/changes/<name>/design.md` for a change with a `design.md`; nothing
    else belongs in the section. The script it names exists beside the
    templates. The templates' existing rules still hold.
    *Refuted by:* `tests/test_pr_templates.py` red; the section missing,
    doubled or misplaced in either template; the named script absent.

15. **The prompt.** `prompts/07-commit.md` carries one bullet: after the
    last push, run `python3 scripts/touch_map.py origin/main HEAD`, paste
    its output under "What it touches" unchanged in either template, never
    edit it and never draw a map by hand or by a model, and run it again and
    replace the whole section when the branch moves; a change with a
    `design.md` adds the `Architecture delta:` line below it. The closing
    sentence of the multi-decision form names "What it touches" among the
    sections that appear once.
    *Refuted by:* reading in phase 6 — the bullet missing, one of its parts
    missing, or the sentence without the section.

16. **No ratchet grows, and the kit carries it.** The script has a test and
    a reason in `ci_gates.OHNE_AUFRUFER` (an entry point, not a gate);
    `OHNE_TEST`, `OHNE_MUTATIONSTEST` and the kit's `REIST_NICHT` are
    unchanged. `scripts/touch_map.py` and `tests/test_touch_map.py` have the
    kit role `mechanismus`; the tests build their own repositories and read
    no history of this one, so they hold in the probe copy.
    *Refuted by:* `tests/test_ci.py` red, one of the three lists longer, a
    role other than `mechanismus`, or the gate `leerprobe` red.

17. **On this repository.** Run on merges of `main` as
    `<merge>^1 <merge>^2`: #68 (`6c5d51a`) and #72 (`3715528`) print the
    prose-only line; #65 (`017ec56`, five tests changed) draws each of the
    five tests with at least one link to code it tests; every link drawn for
    #73 (`d5813ec`) and #65 is checked by hand against the line in its
    source that makes it, and none comes from a comment, a docstring or a
    registry. The six merges of research 1.4 are run, and their boxes and
    links are recorded in `plan.md`.
    *Refuted by:* another output for #68 or #72; a test of #65 without a
    link; a drawn link whose line does not exist in its source's code text.

18. **Green.** `make verify` is green once the ADR answer is recorded.
    *Refuted by:* `make verify` red.

## Non-goals

In this change, not now:

- **The freshness gate** — a CI step that compares the pasted section with
  a fresh run, the `edited` pull request event, its mutation test (research
  4.6; a later change of the same bead).
- **The stop rule** — asking the maintainer after five pull requests with
  the section whether it changed what they looked at (the note §6.3,
  item 5); that is a question in a session, not code.
- **ADR 0009 and `design.md`** — no amendment for the C4 level `code`, no
  `templates/design.md` (bead coding-harness-9qo).
- **LakeSwitch** — its template and `modgraph.py` stay as they are.
- **A Mermaid parse on Node.js**, and any rendering check beyond the
  maintainer's phone.
- **What the rules cannot see** — what changed inside a file, a "writes"
  link (`ci_gates.py` generates `ci.yml`), dynamic imports, paths assembled
  at run time or joined from a tuple of bare names, a path a Python code
  file passes to `subprocess`, and telling a fixture path from the
  repository's file.
- **LakeSwitch's readability rules** — the hub rule and the transitive
  reduction (see `[DETAIL]`s).
- **Rename detection.**
- **Pull requests already open or merged** — no section is filled in
  retroactively.
- **`docs/WORKFLOW.md`, `AGENTS.md`** and the templates' line `Where it
  fits`.

## Open decisions

### `[DECISION]`

None open. Both are answered by the maintainer on 2026-10-06
(`decisions.md`, addendum): class `feature` with the ADR answer "no"; a map
in every code pull request with at least one link, "consider splitting"
from 15 boxes, the list only above 30.

### `[GAP]`s — closed by reading

Each is recorded in `research.md`, section 5.

- **The phase gate.** `scripts/validate_change_artefacts.py` does not
  exist; `python3 scripts/plans_registry.py --check` stands in (5.9).
- **Registries and stems today.** Only `ci.yml`, a runner, crosses 15
  named paths; no two `.py` stems collide (5.1, 5.2).
- **How far a changed test reaches, and fixture paths.** Up to 12 files
  per test, many of them paths written into temporary trees (5.3, 5.4).
- **Which merges are prose-only under these rules.** #68 and #72, not #71
  (5.5).
- **Whether a `design.md` is owed.** Not on `main` today (5.7).

### `[DETAIL]`s — decided here, with the reason

Each is reversible and binds nothing beyond this change.

- **"From 15 boxes" includes 15.** The maintainer's words in
  `decisions.md` ("from 15 boxes the section says consider splitting")
  govern over research 4.3's "above 15".
- **Fold boxes count.** The thresholds are about what a screen holds, and
  a fold box takes the room of a box.
- **A changed test reaches outward only to code and runners.** Research
  4.1 lets it reach every file it names; measured, that draws fixture paths
  as boxes (research 5.4). Changed other files a test names are still
  drawn (criterion 3).
- **A Python code file links only by import.** Research 4.1 counts files
  a code file "reads"; the note §5.1 measured that a path inside a message
  made false links, and the prototype dropped them. Runners and shell
  scripts still link by name.
- **No hub rule, no transitive reduction.** Research 4.1 takes both from
  LakeSwitch. Here the map centres on the changed files, so a hub's arrows
  are the importers of the changed module — what a reviewer needs; import
  links are thin here (research 1.6); and with every link drawn, the map
  and the list hold the same links (criterion 8). LakeSwitch keeps its own
  script.
- **Registries are sources only, runners exempt.** A registry as the
  target of a link is a true link (`test_kit.py` reads the kit manifest);
  the prototype's exemption of runners is what keeps `ci.yml` drawing.
- **The full path counts as a plain substring**, as in the prototype,
  where 14 of 14 drawn links were right (the note §5.1); a boundary rule
  would miss `$ROOT/scripts/…` in shell.
- **No rename detection.** Git's rename detection is a similarity guess; a
  removed and a new file are exact, and the removed one gets its
  `still named by` check.
- **No map without a link.** The maintainer's answer is "at least one
  link"; a map of loose boxes repeats the list.
- **Above 30 boxes, the three lists go with the map.** They describe the
  map; the touch list already carries every status.
- **Only links with a changed end.** Two unchanged neighbours are context
  of each other, not of the change.
- **The command:** base and head as positional arguments, `--repo` for
  the tests, the direction fixed to `LR` (the note §5.2: left to right
  read better for this shape).
- **Only the `Architecture delta:` line may follow the output** in the
  section, so a later freshness gate can compare the rest with a fresh run.
- **Exit 3 for "not measured"**, as the checks here do (research 5.8).
- **Standard library only**, so the script travels to an instance without
  a dependency.
- **Names:** `scripts/touch_map.py`, `tests/test_touch_map.py`, the section
  "What it touches" (research 4.4).
- **Phase 2a not run:** it is optional; eighteen criteria each carry their
  refutation, and phase 6 reads the result against them.
