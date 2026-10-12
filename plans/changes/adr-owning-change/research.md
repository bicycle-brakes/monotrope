---
title: "Research — adr-owning-change"
status: draft
implementation_status: none
date: 2026-10-12
last_reviewed: 2026-10-12
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-afa
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, gates, interview-minimums, adr]
---

# ADR owning change — Research

Phase 1 for bead coding-harness-afa, read against `origin/main` on
2026-10-12. The gate interview-minimums (`scripts/check_interview_minimums.py`)
attributes an ADR under `docs/adr/` to the change folders the same diff
touches and requires exactly one. Change criterion-test-ledger (bead
coding-harness-909, pull request #126, not merged on 2026-10-12) adds ADR 0013
and migrates four other plans; it carries an interim heuristic (a folder the
diff touches through `plan.md` alone is no owner; beside other owners the ADR
text decides) that this change replaces with an explicit statement.

## Questions for the exploration

1. How does the gate find an ADR's owner today on `main`: the code path, the
   base rule, the findings it writes, the tests that pin it.
2. Which places could state the owner explicitly, and what reads them today:
   `decisions/answers/<change>/adr.yaml` (written by `scripts/harness.py
   decide adr`), an ADR frontmatter field, `decisions.md` of the change.
3. Which existing ADRs and answer files would a new rule meet, and which of
   them carry a change name already (for a cut-off or a one-time migration).
4. Which other scripts, gates, kit files and prompts read ADR ownership or
   the answer files (`scripts/check_adr_answers.py`, `scripts/kit/`,
   `prompts/`), so a change knows what it must keep consistent.

The interview (phase 1a) needs the maintainer; this file stops before it.

Stage-2 call, 2026-10-12: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 347 files, 859 commits, 12 rules.

## Runner exploration — 2026-10-12

*Note by the orchestrating session (2026-10-12): GLM's answer opened with an English preamble, a German summary and a code fence around the findings; the preamble, the summary and the fence were removed (house rule 1). The German summary said: ownership exists today only in the diff, no artefact names an ADR's owner; two collisions for the interview — `owner:` in ADR frontmatter already means a role, and the answer-format pin (schema_version 1, eight keys) says "not now" to extending the format. The text below the heading is unchanged.*

## What the exploration found

### Q1 — How the gate attributes an ADR to its owner today

The attribution lives in `measure()` of `scripts/check_interview_minimums.py`.
`_changed_paths()` collects three diff states — the working-tree diff against
the base, the staged diff against the base, and untracked files
(`git ls-files --others --exclude-standard`), the states the module docstring
ties to `stage2.change_diff()`. From these, `adr_paths` is every path under
`docs/adr/`, and `owning` is the set of folder names at `plans/changes/<name>/`
(the path component the code names parts[2]) for any touched path with a file
inside (`len(parts) > 3`), excluding `archive`. Nothing persistent states the
owner: ownership exists only inside the measured diff. Any file inside a folder
makes that folder an owner — a diff touching only `plan.md` included; there is
no heuristic on `main`.

When `adr_paths` is non-empty and `owning` does not hold exactly one name,
`measure()` returns one finding ("N ADR path(s) changed under docs/adr/ but the
diff owns K change folder(s)"): zero owners and two-or-more owners are the same
finding shape. With exactly one owner the gate reads
`plans/changes/<owner>/decisions.md` and demands five counted records
(`_parse_records`, `_counted`) whatever the folder's class and spec date — the
code cites loop row L1-3: the cut-off exempts class minimums, never a new ADR
edit. The base comes from `_base()`: first parent (`HEAD^`) on a genuine `main`
checkout or when `GITHUB_REF` is `refs/heads/main` (`_mainline_ci`, the hosted
main-line run), else the merge base with `origin/main`; a detached HEAD at
`origin/main` raises `CannotMeasure` and the gate exits 3 unmeasured.

The attribution tests in `tests/test_check_interview_minimums.py`:
`test_adr_outside_any_change_is_a_finding` (owns 0),
`test_adr_with_two_owning_changes_is_a_finding` (owns 2),
`test_renamed_away_adr_is_seen` (P2-1 — the gate diffs with `--no-renames`, a
`git mv` out of `docs/adr/` still counts), `test_index_only_staged_adr_is_seen`
(F-16), `test_adr_edit_in_a_stock_folder_still_owes_five` (L1-3), plus the
diff-state matrix under AC 2 (committed, staged, unstaged, untracked). The gate
is declared in `decisions/gates.yaml` (entry `interview-minimums`: job verify,
enforcement block, placement both); `test_gates_yaml_declares_interview_minimums`
pins that entry, and `.github/workflows/ci.yml` is generated from
`decisions/gates.yaml` (docs/WORKFLOW.md, §2 inventory table). Origin: the ten
decisions of 2026-10-08 in
`plans/changes/archive/2026-10-08-interview-minimums/decisions.md` — G-2/G-5
(five attach to the fact of an ADR being created or changed, no class bypass),
Q-7 plus its addendum (the base rule; the phase-6 rows F-13/F-14/F-15 refined
it to today's exit-3 behaviour, pinned by
`test_detached_at_tip_without_main_line_env_is_not_measured`).

One asymmetry: `_active_changes()` includes archived folders when measuring
class minimums, but the ownership attribution excludes `archive` outright — an
archived change can never be an owner on `main` today, and an ADR edit
alongside only archived-folder changes is a "owns 0" finding.

### Q2 — Places that could state the owner, and what reads them today

`decisions/answers/<change>/adr.yaml` — eight keys (`ANSWER_KEYS` in
`scripts/check_adr_answers.py`). It names the change twice (folder and `change:`
key; `examine()` turns a mismatch into a finding) but carries no ADR number and
no field toward the ADR's owner; `question` is the constant `adr`. Writer:
`scripts/harness.py` (`render_answer`, `write`, `record_adr`; `record_adr`
refuses when the file exists — an existing answer changes only by an edit in a
decision pull request). Reader: `scripts/check_adr_answers.py` alone —
`harness.py` imports the gate so the command writes exactly what the gate
accepts (both module docstrings). The binding is change→answer, never
ADR→change. Write permission: the `provenance.yaml` `paths:` entry with prefix
`decisions/answers/` (`allowed: [human-decided]`, `frontmatter: none`,
`owner_role: framework-architect`), read by `answering_role()`. Format
constraint: `docs/research/2026-10-11-adr-answer-pin-plan.md` pins the
eight-key format as shared with LakeSwitch and lists "any extension of the
answer format beyond schema_version 1" under "Not now".

ADR frontmatter — all twelve files under `docs/adr/` carry `category: adr` and
`owner: framework-architect`; a search for a `change:` line over `docs/adr/`
finds nothing. A new header field meets two facts: `owner:` already means a
*role* (`provenance.yaml` roles block, RB-M8 comment — an owner names a role,
never a person), so a change-ownership field needs a distinct name; and while
`provenance.yaml` holds `docs/adr/` under `frontmatter: required`, the only
header check is `scripts/check_frontmatter_current.py`, which reads the
`updated:` line alone (its docstring and `read_updated`) — a new field is
neither tripped nor read by anything today.

`decisions.md` of the change — prose plus the Q-record/SKIP format of
`prompts/01a-interview.md`; `check_interview_minimums.py` parses it with
`_parse_records` for counting only. The gate never reads any file for
attribution — attribution runs over the diff alone. The spec header carries
`change:` and `adr_question:` (`read_feature()` in `check_adr_answers.py`,
`prompts/02-spec.md`); it binds a feature to its answer file, never to an ADR
file.

### Q3 — What a new rule would meet

Twelve ADRs, `docs/adr/0001` … `0012`; the next number 0013 is named today only
in `docs/research/2026-10-11-adr-answer-pin-plan.md` (package 2: criterion-
test-ledger introduces ADR 0013) and in this file's frame — `docs/adr/0013`
does not exist in this tree, and pull request #126 is not merged into it.

Prose links ADR→change exist for five ADRs (search over `docs/adr` for
`plans/changes`): 0007 → `stage-2-codex-glm`, 0008 → `harness-decide-adr`,
0010 → `hermes-runner`, 0011 → `stage2-mimo`, 0012 → `stage2-session`. Nothing
links 0001–0006 and 0009 to a change. Two of the five owning folders are
archived under dated names (`plans/changes/archive/2026-09-30-stage-2-codex-glm/`,
`plans/changes/archive/2026-10-07-stage2-mimo/`), so those prose paths no
longer resolve as written; `harness-decide-adr`, `hermes-runner` and
`stage2-session` are still active. Both gates already carry the convention of
stripping an archive date prefix from a folder name (`_active_changes` in
`check_interview_minimums.py`, `anchors()` in `check_adr_answers.py`).

Ten answer files under `decisions/answers/`, each with `change:` equal to its
folder — frontmatter-current (no), harness-decide-adr (yes), interview-minimums
(no), omnigent-deny-layers (no), project-lock (no), rb-g7-merge-freshness (no),
rb-m6-one-account (no), stage2-mimo (yes), template-bundle (no), touch-map
(no). Every one carries a change name by construction. The two yes-answers map
to ADRs only in prose: ADR 0008's header review line cites
`decisions/answers/harness-decide-adr/adr.yaml`; the stage2-mimo answer's
`reason` names the widening of ADR 0007 that became ADR 0011. docs/WORKFLOW.md
§2 ("Change classes, the ADR question and decision pull requests") states the
gap: "Nothing checks that the class is right, that a `yes` is followed by an
ADR, or that a decision pull request carries its label and block."

`scripts/check_decision_continuity.py` holds a second, hardcoded ADR map:
`AMENDMENT_ADRS` binds D-/O-decision ids to ADR filenames, and `run()` checks
each file exists and cites its key — a change that adds or renames ADR files
must keep that map green.

### Q4 — Everything a change must keep consistent

Scripts: `scripts/check_interview_minimums.py` (the attribution and its finding
text), `scripts/check_adr_answers.py`, `scripts/harness.py`,
`scripts/check_decision_continuity.py` (`AMENDMENT_ADRS`),
`scripts/check_frontmatter_current.py` (`updated:` freshness over `docs/adr/`).
Declarations: `decisions/gates.yaml` (entries `adr-answers`,
`interview-minimums`, `decision-continuity`), `provenance.yaml` (the `docs/adr/`
and `decisions/answers/` entries), `scripts/kit/manifest.yaml` —
`check_adr_answers.py`, `harness.py`, `check_decision_continuity.py` and their
tests travel with the kit (`mechanismus`), `decisions/answers/` is `bestand`
("this repository's ADR answers; another repository's answers are its own");
the manifest holds no entry naming `check_interview_minimums.py` — the
interview gate does not travel with the kit today. Prompts and templates:
`prompts/01a-interview.md`, `prompts/02-spec.md`, `prompts/07-commit.md`,
`.github/PULL_REQUEST_TEMPLATE/decision.md`. Doctrine: `docs/WORKFLOW.md` §2
(phase table and the classes section), `AGENTS.md` (the one-screen table).
Tests: `tests/test_check_interview_minimums.py`, `tests/test_check_adr_answers.py`,
`tests/test_harness_decide_adr.py` (the latter two travel in the kit manifest —
a format change ripples beyond this repository), `tests/test_touch_map.py`
(asserts the map's "Not linked" line names answer files).

## What is unclear

- The interim heuristic of pull request #126 (a folder touched through
  `plan.md` alone is no owner; beside other owners the ADR text decides) is
  recorded in this file's frame and, in outline, in
  `docs/research/2026-10-11-adr-answer-pin-plan.md`; the branch is not merged
  and its diff is not readable from this worktree — what exactly it changes in
  `measure()` is open for the interview.
- Whether an explicit owner statement covers the stock (ADR 0001–0012) or is
  prospective only — the cut-off precedent (`CUTOFF` in
  `check_interview_minimums.py`, decisions Q-4/Q-8) is the repository's
  pattern, but nothing read here decides it.
- Where the statement belongs — answer-file format, ADR header, or a third
  place; the pin plan's "Not now" on schema_version 1 extensions and the
  `owner:`-means-a-role collision are the two constraints to weigh.

## Which files a change would have to touch

`scripts/check_interview_minimums.py` (attribution rule and finding text) ·
`tests/test_check_interview_minimums.py` (attribution matrix: zero, one, two
owners, plan-only diffs, archive cases) · wherever the owner is stated —
`scripts/check_adr_answers.py` and `scripts/harness.py` with
`tests/test_check_adr_answers.py`, `tests/test_harness_decide_adr.py` if the
answer format grows; the twelve ADR headers if it lands in frontmatter ·
`scripts/kit/manifest.yaml` when kit travel changes · `docs/WORKFLOW.md` (§2
phase table row 1a, classes section) · `AGENTS.md` (workflow table) ·
`scripts/check_decision_continuity.py` when ADR 0013 arrives ·
`decisions/gates.yaml` only if a new gate joins.
