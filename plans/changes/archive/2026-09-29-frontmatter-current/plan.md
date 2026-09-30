---
title: "Plan — frontmatter-current"
status: accepted
implementation_status: done
date: 2026-09-29
last_reviewed: 2026-09-29
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-qd7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan]
---

# Plan — frontmatter-current

Written for option 1 of `[DECISION] 1` in `spec.md` (the maintainer commits
the ADR headers). Option 2 changes step 8 only: the session commits them too.
Stage 1 is active, so the subtasks carry no model markings.

## Files

### Created

- `scripts/check_frontmatter_current.py` — the check and the stamp.
  - `load_map(root)` reads `root/provenance.yaml` (`paths:`, `excluded:`).
  - `is_held(rel, paths, excluded)` — criterion 1: `*.md`, not excluded,
    longest matching prefix says `required`.
  - `held_files(root)` — `git ls-files -z --cached --others
    --exclude-standard`, filtered by `is_held` and `Path.is_file()`.
  - `read_updated(text)` — returns `no-frontmatter`, `missing`, `duplicate`,
    `unreadable` or the date. Block pattern `^---\n(.*?)\n---\n` as in
    `check_docs.py`; a top-level line starts `updated:` at column 0; the value
    matches `^["']?(\d{4}-\d{2}-\d{2})["']?\s*$` and passes
    `date.fromisoformat`.
  - `reference_dates(root, files, today)` — dirty set is
    `git diff --name-only -z HEAD` plus `git ls-files -z --others
    --exclude-standard`; a dirty file gets `today`, a clean one
    `git log -1 --no-merges --format='%cs %h' -- <path>`.
  - `findings(root, today, utc_today)` — the `read_updated` kinds plus
    `stale` (`updated < reference`) and `future`
    (`updated > utc_today + 1 day`).
  - `stamp(path, today)` — a text edit, never a YAML round-trip: replace the
    one top-level `updated:` line with `updated: <today>`, or insert it after
    the top-level `last_reviewed:` line, else before the closing `---`; write
    only when the text changed.
  - `main()` — `--stamp`, `--root` (default: the repository root). Before
    measuring: `git rev-parse --is-inside-work-tree`, `--verify HEAD`,
    `--is-shallow-repository`; a failure, a shallow repository (message names
    `fetch-depth: 0` and `needs_history`), an unreadable map or a clean file
    `git log` cannot date → exit 3. Check mode: one line per finding, then
    `fix: python3 scripts/check_frontmatter_current.py --stamp` (and that
    `no-frontmatter`/`duplicate` need a hand edit), exit 1; else one green
    line with the count, exit 0. Stamp mode: stamps `missing`, `unreadable`,
    `stale`, `future`; names the rest and exits 1 if any remain. `today` is
    `date.today()`, `utc_today` is `datetime.now(timezone.utc).date()`, both
    passed down so tests can fix them.
- `tests/test_frontmatter_current.py` — the tests below. `_repo(tmp_path,
  map)` writes its own `provenance.yaml`; `_commit(repo, when)` commits with
  `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` set to `when`, `-c
  user.name=t -c user.email=t@example.invalid -c commit.gpgsign=false`, and
  `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`. No test reads this
  repository's files or dates, except the real `provenance.yaml`, which
  travels with the kit.

### Changed

- `provenance.yaml` — new comment lines in English. (a) The header names the
  reader that exists, `scripts/check_frontmatter_current.py`; `allowed:` is
  declared, not yet enforced. (b) The three values: `required` = a document
  header, held present and with a current `updated:`; `optional` = not yet
  classified, not held; `none` = no document header — a frontmatter a tool
  reads as configuration may stand there. (c) `docs/adr/`, `docs/how-to/`,
  `docs/governance/`: `frontmatter: required`, in place. (d) New entries
  `docs/architecture/` and `docs/research/`, `allowed: [human-written,
  ai-drafted-reviewed]`, `frontmatter: required`. (e) `.claude/agents/`:
  `frontmatter: none`, one comment line (decisions item 3).
- `decisions/gates.yaml` — the schema comment gains `needs_history`
  (optional boolean: the derived CI checks out the full history,
  `fetch-depth: 0`, in the job that runs this gate). After `docs-links`:

  ```yaml
  - id: frontmatter-current
    title: Every held document's updated date is current
    command: python3 scripts/check_frontmatter_current.py
    job: verify
    enforcement: block
    floor: false
    placement: both
    needs_history: true
    reason: A header older than its document's last change misleads every reader, and the maintainer asked that a stale one cannot be merged (bead coding-harness-qd7).
  ```

- `scripts/ci_gates.py` — `validate_schema` refuses a present, non-boolean
  `needs_history`; `gates()` carries the field; `generate_ci` writes each
  job's checkout through one helper that adds `with:` / `fetch-depth: 0`
  when a gate of that job has `needs_history`.
- `.github/workflows/ci.yml` — regenerated: the `verify` checkout gains
  `fetch-depth: 0`, and the new step follows `docs-links`.
- `tests/test_ci.py` — two tests (criterion 6).
- `scripts/kit/manifest.yaml` — two `mechanismus` rules, for the script ("the
  check behind the gate frontmatter-current — the gate file travels, so its
  script does") and its test ("builds its own repositories; holds in the
  probe copy").
- `scripts/handover_schema.py` — `updated` in `OPTIONAL`, with the comment
  that `check_frontmatter_current.py` requires it under `required` prefixes.
- `templates/handover.md` — Variante A: `updated: 2026-01-01` after
  `created:`.
- `tools/claude-code/skills/uebergabe/SKILL.md` — §3a block: `updated:
  <JJJJ-MM-TT>` after `created:`. Takes effect after
  `tools/claude-code/install.sh`; the maintainer runs it.
- `scripts/new_change.py` — `_frontmatter_template`: `updated: {heute}` after
  `last_reviewed:`.
- `tests/test_workflow_entry.py` —
  `test_new_change_creates_the_folder_and_a_current_index` also asserts
  `updated: <today>` in the scaffold.
- The six ADRs — a header before the heading, values below, without
  `updated:` (the stamp adds it). Every line of the body stays.
- Every held file — `updated:` from the stamp: 49 files, measured as 45
  tracked at `9f14283` plus `research.md`, `decisions.md`, `spec.md` and
  `plan.md` of this folder. A held file added since is listed by the check.

ADR header (`produced_by.version` = `created`):

```yaml
---
title: "<the heading without '# '>"
category: adr
status: accepted
created: <created>
last_reviewed: <accepted>
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "<created>"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr]
---
```

| ADR | created | accepted |
|---|---|---|
| 0001, 0002, 0003 | 2026-09-19 | 2026-09-22 |
| 0004 | 2026-09-22 | 2026-09-23 |
| 0005 | 2026-09-23 | 2026-09-23 |
| 0006 | 2026-09-27 | 2026-09-27 |

## Steps

1. The script and its test file; `python3 -m pytest
   tests/test_frontmatter_current.py -q` green.
2. `ci_gates.py`, `gates.yaml`, regenerate `ci.yml`, the two `test_ci.py`
   tests.
3. `provenance.yaml`.
4. The writers: `handover_schema.py`, the template, the skill,
   `new_change.py` and its assertion.
5. `scripts/kit/manifest.yaml`.
6. The six ADR headers.
7. `python3 scripts/check_frontmatter_current.py --stamp`, then the check
   exits 0. This is the last edit before the final commit; if the date has
   changed since, run it again.
8. Commit everything except `docs/adr/`, leave the ADR headers uncommitted,
   and stop. The maintainer runs the stamp and `git confirm` (`spec.md`,
   `[DECISION] 1`).

## Verification command

```sh
python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml
python3 scripts/check_frontmatter_current.py
python3 scripts/check_docs.py | grep "adr/.*Frontmatter ohne"
bash scripts/verify_all.sh
```

Expected: the check exits 0; the `grep` prints nothing (baseline 2026-09-29:
22 "Frontmatter ohne" findings, none under `docs/adr/`); `VERIFY GREEN`. In
hosted CI, the pull request's `verify` job runs `frontmatter-current` green
(criterion 7).

## Test per criterion

In `tests/test_frontmatter_current.py` unless noted.

| Criterion | Test | Fault that turns it red |
|---|---|---|
| 1 | `test_only_required_prefixes_are_held` | a stale `optional`, `none`, unmapped or excluded file reported; a shorter prefix winning |
| 1, 7 | `test_the_map_holds_documents_not_harness_configuration` — `is_held` on sample paths against the real map | `.claude/agents/` still `required`; `docs/research/`, `docs/architecture/` or `docs/adr/` not held; `prompts/` or `plans/INDEX.md` held |
| 2 | `test_a_header_without_a_readable_updated_goes_red` | no frontmatter, no `updated:`, two of them or `updated: soon` exiting 0 |
| 2 | `test_a_far_future_stamp_goes_red` | `2099-01-01` passes, or tomorrow (UTC) is reported |
| 3 | `test_the_check_goes_red_when_a_later_commit_outdates_the_stamp` — a body commit, then a `git mv`, each a day after the stamp | the author date or an older commit compared; a rename seen through |
| 3 | `test_the_committers_own_offset_decides_the_day` — commit at `2026-09-20T23:30:00-05:00`, stamp `2026-09-20` | the date converted to UTC or the runner's zone |
| 3 | `test_a_merge_commit_never_counts` — branch change stamped on its day, `--no-ff` merge days later; a file changed on both sides dated by the newer side | `--no-merges` dropped; the wrong side followed |
| 3 | `test_an_uncommitted_edit_is_held_against_today` — a modified file and an untracked one | index, worktree or untracked state ignored |
| 4 | `test_a_shallow_clone_is_not_a_pass` — `git clone --depth 1 file://…` | exit other than 3, or no `fetch-depth: 0` in the message |
| 4 | `test_the_failure_names_the_stamp_command` — subprocess `python3 scripts/check_frontmatter_current.py --root <tmp>` | exit other than 1, or the fix line missing |
| 5 | `test_the_stamp_touches_only_the_updated_line` — flow mappings, comments, quoted values; missing line inserted after `last_reviewed:` and, without it, before `---` | any byte outside that line changed; wrong position |
| 5 | `test_the_stamp_is_idempotent_and_never_writes_a_header` | a second run rewrites; a header invented; exit 0 with such a file left |
| 6 | `tests/test_ci.py::test_a_gate_that_needs_history_gets_a_full_checkout_only_in_its_job` | the flag ignored, or `fetch-depth: 0` in the `drift` job |
| 6 | `tests/test_ci.py::test_the_schema_refuses_a_non_boolean_needs_history` | `needs_history: "yes"` accepted |
| 7 | the gate on the pull request; the assertion in `tests/test_workflow_entry.py`; the existing `tests/test_feedback_channel.py` field and template tests | a held file unstamped; the scaffold without `updated:`; `updated` unknown to the handover schema |

The subprocess test puts `scripts/check_frontmatter_current.py` into the
test file, and five names match `MUTATIONS_NAMEN` (`goes_red`,
`is_not_a_pass`, `never_writes`), so the gate needs no entry in
`OHNE_MUTATIONSTEST`.

## Not touched

- `scripts/check_docs.py`, `scripts/plans_registry.py` (`REQUIRED`),
  `Makefile`, `scripts/verify_all.sh`, the `drift` job,
  `scripts/export/manifest.yaml`.
- In `provenance.yaml`: every other entry, every `allowed:` list, the origin
  prefixes of directories that do not exist here.
- `OHNE_AUFRUFER`, `OHNE_TEST`, `OHNE_MUTATIONSTEST`, `REIST_NICHT` and
  `DECKEL`: the change needs no entry; needing one means a test is missing.
- The ADR bodies. markdownlint (report only) will read title plus heading as
  two top-level headings, as it already does for other documents here.
- The files under `.claude/agents/`, `prompts/`, `.agents/skills/`, and
  anything outside this repository.
- The content of `docs/WORKFLOW.md`: a parallel pull request translates it
  (`research.md`, correction 4). Whichever merges second stamps it again; the
  check names it.

## Implementation notes

Written by the implementing session on 2026-09-29, after the work. The text
above is unchanged.

**Re-measured after merging origin/main 1a6aff8 (Coding Harness PR 49).**

- Held files: 49 now, all tracked. The current map, applied to the tree at
  `9f14283`, gives 45; the four added are the files of this folder. None of
  the 45 disappeared, and PR 49 added none: the count of 49 stands.
- Baseline `check_docs.py`: 22 "Frontmatter ohne" findings before and after;
  none under `docs/adr/` after the six headers. The four other `adr/` lines
  it prints are dead links in `regelwerk.md`, as before.
- Kit probe (`python3 scripts/kit/probe.py`): 267 cases after, 254 before, so
  13 new ones travel; the red set is the same 31 cases, so `REIST_NICHT`
  needed no entry.

**Where the work differs from the plan text.**

1. **Step 8, option 2.** The maintainer answered `[DECISION] 1` with option 2.
   The six ADR headers are an ordinary commit, and the session does not stop
   before the stamp. The plan was written for option 1, as its preamble says.
2. **A test name.** `tests/test_ci.py::test_the_schema_refuses_a_non_boolean_needs_history`
   is named `test_the_schema_rejects_a_non_boolean_needs_history`. `refuses`
   is one of the words in `MUTATIONS_NAMEN`; `tests/test_ci.py` names
   `plans_registry.py` in its text, so a mutation-named test in that file made
   `test_the_mutation_ratchet_only_turns_one_way` count the two plans-registry
   gates as covered, and it stood red on their `OHNE_MUTATIONSTEST` entries.
   Renaming is smaller than touching that list, which the plan lists under
   "Not touched". The test does what the criterion 6 row says.
3. **Commits are not individually green.** The gate commit precedes the map
   and the headers, so the gate is red between them; only the last commit is
   held to `make verify`.
4. **Two details of `reference_dates`** beyond the plan text: `git diff` runs
   with `--no-renames --relative`, so a staged move shows as an added new
   path and paths are relative to `--root`.
5. **One added test.** `test_nothing_is_measured_where_the_question_cannot_be_asked`
   (not a work tree, no commit, an unparsable map; all exit 3) is not in the
   plan's table. `test_the_map_holds_documents_not_harness_configuration` is,
   but it sits in the map commit rather than the script commit, because it
   reads the changed map.

**Planted faults.** Every fault below was written into the script, the test
file was run, and the script was restored (byte-identical, checked with
`cmp`). All 16 went red on the pytest run of `tests/test_frontmatter_current.py`:
`--no-merges` dropped; author date instead of committer date; the shorter
prefix winning; the future check off; the future bound at today instead of
tomorrow; the shallow refusal off; untracked files not counted as dirty;
the index not counted as dirty; the stamp inserting at the end of the block;
the stamp rewriting an unchanged file; the stale check off; an unreadable
value passing; the fix line missing; `optional` held; the exclusion ignored;
a header written into a file without one. Three more on `ci_gates.py`: the
full checkout for every job, `needs_history` not validated, `needs_history`
not carried by `gates()`. Two on the writers: the scaffold without `updated:`
and the handover schema without `updated` (red in
`test_the_template_satisfies_the_schema_it_documents`). And one in this tree:
`docs/how-to/signed-decisions.md` with `updated: 2026-09-01` under a change
of 2026-09-29 (uncommitted, so measured against today) turned the check red;
restored, it is green again.

**Evidence, 2026-09-29, on the tree of commit `f7996d1` plus the stamp
(uncommitted when run; the commit that follows holds exactly that state).**

The stamp, first run: exit 0, 49 lines, each of the form `stamped <path>
(missing) -> updated: 2026-09-29` (the first is `docs/WORKFLOW.md`). It added
105 lines to 49 files and deleted none: 49 `updated:` lines plus this
section, which was written before the stamp. The second run: exit 0, no
output, and `git diff | shasum` identical before and after, so it changed
nothing. Then the check:

```text
$ python3 scripts/check_frontmatter_current.py
frontmatter-current: 49 held documents, every `updated:` is current.
$ echo $?
0
```

`make verify`, the relevant lines and the last line:

```text
── [pytest] gruen
── [frontmatter-current] $ lauf_cmd
frontmatter-current: 49 held documents, every `updated:` is current.
── [frontmatter-current] gruen
── [ci-drift] $ lauf_cmd
ci.yml ist genau die Ableitung der Gate-Datei.
── [ci-drift] gruen
── [ramp-valves] gruen
── [markdownlint] rot, aber nur report — er meldet, er blockiert nicht.

VERIFY GREEN — every local gate of the 'verify' job passed.
```

Hosted CI on the pull request has not run: criterion 7's last sentence (the
gate green on the pull request that introduces it) is open until it does.

### Repair round 1

2026-09-29, after the phase-6 review (`findings.md`). Findings F-1 and F-3 to
F-8 fixed; F-2 (hosted CI) is closed by the pull request.

- **F-1, corrects the earlier `[DETAIL]`.** The six ADR headers restated the
  ADR badly: `status: accepted` and `review: pending` contradicted the body's
  Status and Review lines. The corrected `[DETAIL]` is in `spec.md` ("ADR header
  values restate the ADR", the paragraph "Corrected in repair round 1"). The
  header template above is the earlier text and is unchanged; the headers on
  disk follow the corrected detail. One spelling for supersession: `status:
  superseded` with `superseded_by: "0006"` for the whole (0001);
  `status: accepted` with `superseded_in_part_by: ["0005", "0006"]` (0002) or
  `["0006"]` (0005) for a part. `check_docs.py` requires keys only, never
  values, and nothing else reads `review:` or these two fields under
  `docs/adr/`, so no check changed. ADR 0001–0003 also carry `approved`: their
  Review lines read "accepted by the maintainer, 2026-09-22", so `approved_at`
  is that date. No ADR body line changed (`git diff` shows header lines only).
- **F-3.** A map whose `required` prefixes match no file is exit 3 ("measures
  nothing"), in check and stamp mode.
- **F-4.** `_BLOCK` accepts a leading BOM and CRLF; the stamp keeps the
  file's line ending and BOM. The stamp raises `CannotStamp` for invalid UTF-8,
  and `run` names the file, leaves it unchanged and exits 1. `check_docs.py`
  keeps its own CRLF/BOM blind spot (not touched; its non-goal here).
- **F-5.** A failing `git rev-parse --is-shallow-repository` is exit 3.
- **F-6.** `test_a_root_below_the_top_of_the_repository_sees_its_own_edits`;
  with `--relative` removed it fails.
- **F-7.** The `provenance.yaml` header comment lists both readers:
  `scripts/check_frontmatter_current.py` (`paths:`, `excluded:`) and
  `scripts/ramp_valves.py` (`roles:`).
- **F-8.** A trailing YAML comment after whitespace is part of no value:
  `updated: 2026-09-10  # note` is the date (criterion 2). The stamp replaces
  the whole line, so it drops that comment when it rewrites a stale value.
  `2026-09-10# glued` is a string in YAML and stays `unreadable`.
- Six new tests in `tests/test_frontmatter_current.py`, each red on the
  faulty script: five run against the previous script, the F-6 test with
  `--relative` removed from the current one.

Evidence, 2026-09-29, in the worktree after the repair commits (`findings.md`,
this file and `plans/INDEX.md` uncommitted, so held against today). The stamp
changed no file (every `updated:` was already 2026-09-29); the index gained the
`findings.md` row. `python3 -m pytest -q tests`: 352 passed, 15 skipped. `make
verify`, the relevant lines and the last line:

```text
── [frontmatter-current] $ lauf_cmd
frontmatter-current: 50 held documents, every `updated:` is current.
── [frontmatter-current] gruen
── [ci-drift] gruen
── [markdownlint] rot, aber nur report — er meldet, er blockiert nicht.

VERIFY GREEN — every local gate of the 'verify' job passed.
```
