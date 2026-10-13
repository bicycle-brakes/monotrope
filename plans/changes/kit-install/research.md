---
title: "Research — kit-install"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-2uk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, kit, install, lakeswitch]
---

# Kit install and update — Research

Phase 1 for bead coding-harness-2uk (kit: install and update the workflow in
another repository, first target lakeswitch-ai). Read against coding-harness
`origin/main` at `3199a28` and lakeswitch-ai at two cut-offs, both on 2026-10-13:
local `main` `09c9d62` (2026-09-30, 87 commits behind its `origin/main`) and
its `origin/main` `ce88eee` (2026-10-08). Counts below use `ce88eee` unless
stated; the local checkout is read-only here and was only read through `git -C`.
Facts only; no design.

## 1. How the kit is defined and exported today

### The kit manifest

- `scripts/kit/manifest.yaml` (`schema_version: 1`) classifies every tracked
  path by longest matching prefix into two roles, `mechanismus` (carries the
  process and runs unchanged in a foreign repository) and `bestand` (describes
  this repository's inventory, stays). A path matching no rule blocks
  (`probe.py`, `rolle()`).
- Third list: `geruest_ordner` (`plans/changes`, `plans/changes/archive`,
  `plans/specs`) — folders that must exist empty in the target.
- The former `geruest` role was dissolved on 2026-09-23 (bead 1jg.3); the
  manifest comment says so.
- Count at `3199a28` from `probe.py --list`: 83 mechanismus, 325 bestand,
  0 unclassified. By top folder, the 83: `scripts/` 27, `tests/` 20,
  `prompts/` 12, `.claude/` 7, `templates/` 7, `.github/` 3, `docs/` 3,
  `decisions/` 1 (`gates.yaml`), `plans/` 1 (`_README.md`), and `ruff.toml`,
  `provenance.yaml`.
- The manifest has no field for adaptation, rename, merge or ownership beyond
  the two roles; it has no version or commit field.

### The probe

- `scripts/kit/probe.py` copies the mechanismus set into a throwaway
  directory, creates the `geruest_ordner`, runs `pytest`, and compares the red
  cases against `REIST_NICHT` (tests that cannot pass outside this repository,
  each with a reason from `GRUENDE`). It writes nothing into the working tree,
  installs nothing (module docstring).
- `--list` prints what would be copied; `--messen` prints the red names.
- It copies nothing into an existing repository and has no notion of an
  existing target file (not found in `probe.py`: no merge, diff or overwrite
  logic).

### The export

- `scripts/export/manifest.yaml` is a second, independent classification:
  per prefix `carry | geruest | drop`, decided by the maintainer on
  2026-09-20 ("tight core"): `scripts/kit/`, `_verdict.py`, `gate_record.py`,
  three validators, `templates/`, `provenance.yaml`, `AGENTS.md` carry;
  `model-endpoints.yaml` is `geruest`; everything else drops.
- The two manifests are deliberately not derivable from each other
  (`tests/test_kit.py`: `test_the_two_manifests_do_not_contradict_each_other`,
  `test_the_kit_list_is_not_derivable_from_the_export_list`).
- `scripts/export/` holds only `manifest.yaml`. No export script exists in
  this tree (`ls scripts/export`: one file). Not found: any code that reads
  it to write into a target. [GAP] how the 2026-09-03 clean-room instance was
  produced from it is not recorded in this repository.
- `harness.py` has one verb, `decide adr` (argparse subparsers); there is no
  `kit` verb today.

### Version or provenance marker

- Not found, in either repository's tracked files: any export marker
  recording a source commit. `harness.lock.yaml` is named as a future pin in
  lakeswitch-ai `docs/workflow.md` §9 ("Once LakeSwitch pins a Coding Harness
  version (`harness.lock.yaml`, D-21 of the decision interview), the pinned
  copy replaces this adaptation") and in `decisions/answers/pilot.yaml`; the
  file itself does not exist in either tree (searched at `3199a28` and
  `ce88eee`).
- The only recorded link is prose: lakeswitch `docs/workflow.md` §9 says it
  "was last held against Coding Harness `9f14283` on 2026-09-28".
- Kit files carry `produced_by` frontmatter (document-level), not a kit
  version.

## 2. Drift of lakeswitch-ai against the kit

### Headline

Of the 83 files the manifest says travel (as of `3199a28`), compared by git
blob at lakeswitch `ce88eee`:

| State | Count |
|---|---|
| Byte-identical at the same path | 0 |
| Present at the same path, edited | 3 |
| Absent at the same path | 80 |

At local `main` `09c9d62` it is 0 identical, 2 edited, 81 absent (the decision
pull request template was added to lakeswitch between the two cut-offs).
Lakeswitch's top-level has no `scripts/`, no `Makefile`, no `tools/`, no
`prompts/01-07`, no `.claude/agents/`; its `.claude/` holds only
`settings.json`.

### The 3 edited at the same path

1. `.github/PULL_REQUEST_TEMPLATE/decision.md` — 8 changed lines. Adapted:
   verification command is `lakeswitch verify` instead of a placeholder; the
   "What it touches" block (`scripts/touch_map.py`) is removed.
2. `ruff.toml` — 65 changed lines. Different file in kind: kit has
   `line-length = 120`, `target-version = "py312"`, German comments, an
   `exclude` list; lakeswitch has `line-length = 110`, `py311`, English
   comments, `force-exclude = true`, a narrower selected rule set. Scaffolded
   from the "nine files that travel unchanged" commit `f68cfb8` (2026-09-03)
   and since rewritten.
3. `decisions/gates.yaml` — 541 changed lines. Same filename, unrelated
   content: kit lists 21 gates for the process; lakeswitch lists 31 of its
   own (M-numbered, floor gates), pins `python: "3.11"` and its own tool
   versions (`ruff 0.9.10`, `pytest 8.3.4`). The kit manifest treats
   `decisions/gates.yaml` as mechanismus although every repository's content
   differs by design.

### The 80 absent at the same path — where the same idea lives instead

Facts from reading the lakeswitch tree; "same idea" is stated only where the
file says so.

- Workflow doctrine: `docs/WORKFLOW.md` (1173 lines) → `docs/workflow.md`
  (370 lines), self-described "LakeSwitch adaptation" with a §9 divergence
  table (see section 3). Renamed and rewritten.
- Phase prompts `prompts/01-…07`, `01a`, `02a`, `02b`, `04b`, `research-recheck`
  (12 files): absent; lakeswitch has one file, `prompts/implement-a-module.md`
  (§9 row "Phase prompts": "to come with the pin").
- `scripts/_verdict.py` (the shared exit vocabulary) → `src/lakeswitch/verdict.py`
  (own `Outcome` enum, spec/gates.md §3.1; content differs).
- All other 26 `scripts/*` (gate_record, ci_gates, harness, leakcheck,
  adoption, bead_render, touch_map, plans_registry, new_change, verify_all.sh,
  checks): absent. Lakeswitch's runner is `lakeswitch verify`
  (`src/lakeswitch/cli.py`, `suite.py`, `ruleset.py`); `scripts/harness.py
  decide adr` has a counterpart `lakeswitch decide adr` (`src/lakeswitch/adranswer.py`,
  `declared/adr_answer.py`). Whether the other counterparts are
  behaviour-equal was not compared [GAP].
- `.github/workflows/ci.yml` → `.github/workflows/verify.yml` (+ `floor.yml`);
  `.github/pull_request_template.md` → `.github/PULL_REQUEST_TEMPLATE.md`
  (capitalised, different path).
- `provenance.yaml` (root) → `decisions/provenance.yaml`, own content
  (classes `human-decided`, `ai-drafted-reviewed`, …, longest-prefix map).
- `templates/*` (7), `plans/_README.md`, `docs/governance/*` (2),
  `.claude/agents/*` (7): absent; no counterpart found by name in the tree.
- `tests/*` (20 kit tests): absent; lakeswitch tests are under
  `tests/<module>/` for its own modules.
- Not compared in a "renamed" sense: any lakeswitch file I did not match by
  name or by the §9 table.

### What lakeswitch owns that the kit must never overwrite

All read at `ce88eee` unless stated.

- `AGENTS.md`: `decisions/provenance.yaml` lists `prefix: AGENTS.md` with
  `classes: [human-decided]` (and again in a trailing list); lakeswitch's
  `AGENTS.md` carries "Never write under `decisions/`…". `CLAUDE.md` exists
  and is `@AGENTS.md` (kit repository has no `CLAUDE.md`, by rule).
- `decisions/**` entirely: `provenance.yaml`, `roster.yaml`, `floor/` (FD-001
  to 003), `ratifications/` (RC-001 to 005), `answers/` (14 ADR answer files),
  `gates.yaml`, `boundaries.yaml`, `denylist.yaml`, `human-gates.yaml`, etc.
  The decisions carry D-numbers (e.g. D-60 one-tracker-writer rule, D-21
  lock file), gate ids (M-n) and floor invariants (I-n).
- `journal/` (18 files; handover convention is `journal/<date>-<topic>.md`,
  append-only, no frontmatter — differs from the kit's
  `docs/journal/handover/` with schema).
- `plans/changes/` (21 files at `ce88eee`), `spec/` (25 module specs),
  `src/lakeswitch/`, `tests/<module>/`, `examples/`, `rendered/`, `plugin/`.
- Tracker: prefix `lakeswitch-ai-`; `.beads/` is not tracked at `ce88eee`
  (0 files); in the local checkout `.beads/` and `.beads.gate.lock` are
  untracked. lakeswitch `docs/workflow.md` §9: "none yet (branch
  `feat/beads-bootstrap`, not merged)"; its journal
  `2026-09-30-beads-tracker-bootstrap.md` exists (not read in full).
  The prefix of `bd` is fixed at init (kit `AGENTS.md`, house rule 3).
- Python floor: `pyproject.toml` `requires-python = ">=3.11,<3.12"`; `verify.yml`
  `python-version: '3.11'`; `ruff.toml` `py311`. The kit's CI matrix is
  `python: ["3.12"]` and `ruff.toml` `py312`. Whether the kit's 27 scripts and
  20 tests run on 3.11 was not tested [GAP]; `grep` for `match`/`tomllib`/
  `StrEnum` in `scripts/*.py` found no 3.12-only syntax in a first pass
  (not exhaustive).
- Worktree location: lakeswitch `~/lakeswitch-wt/<name>` (its write guard
  refuses `.claude/`), the kit `.claude/worktrees/<name>` (§9 table).
- Verification command: `lakeswitch verify` vs kit `make verify`
  (`scripts/verify_all.sh`); lakeswitch has no `Makefile`.
- `.github/CODEOWNERS`, `.github/ISSUE_TEMPLATE/{defect,proposal}.md`
  (the scaffold's `bug/doc-update/feature` were replaced), `.editorconfig`,
  `.gitattributes`, `.markdownlint.jsonc`, `requirements-ci.txt`
  (uv-compiled with hashes, pins its own set).

### Kit files the target has no use for as shipped

- 19 kit tests are listed `mechanismus` yet some pin kit-repo structure
  (`probe.REIST_NICHT` records those that fail outside; the exact set that
  fails in lakeswitch is not measured) [GAP].
- `decisions/adoption.yaml` (bestand in the kit) is the file the kit's
  `adoption.py` reads; lakeswitch has no such file at `ce88eee`
  (not in the ls-tree). The kit's gates that depend on it (e.g.
  `interview-minimums`) would have no adoption day there [GAP].

## 3. What lakeswitch changed locally in kit-derived files

Source: lakeswitch `docs/workflow.md` §9 table ("Where this workflow comes
from, and where it differs"), which says "a difference that is not listed
below is drift". Examples:

- Verification: `make verify` → `lakeswitch verify` reading
  `decisions/gates.yaml` (31 gates, "the gates are the product here").
- Phase prompts: only `prompts/implement-a-module.md`; rules cut from five to
  three; findings judged against `spec.md` without dimension/origin columns.
- Handover: `journal/<date>-<topic>.md` instead of `docs/journal/handover/`
  with schema.
- Worktrees at `~/lakeswitch-wt/<name>`.
- Identifier style: "the identifier carries the sentence" (maintainer
  decides in `AGENTS.md`) vs the kit's trailing-aside rule.
- Rows lakeswitch adds that "run against the direction" (taken from
  lakeswitch back to the kit): "Before you build" (one-page plan, appetite),
  change classes and ADR question per Feature (ratified 2026-09-26,
  RC-004), and the ADR answer pilot ending 2026-12-15.
- Ratification: lakeswitch notes the kit how-to is out of date on D-55.
- Tooling edits: `ruff.toml` (110 vs 120, py311 vs py312); decision PR
  template (section 2).
- Behaviour copied rather than shared: `lakeswitch decide adr` mirrors
  `harness.py decide adr`; the pilot "is to move to Coding Harness with the
  pin".

Marking: the §9 table is the only place target edits are marked, and it is
prose, written by hand, last held against kit `9f14283` on 2026-09-28
(coding-harness is now at `3199a28`). No machine-readable marker of an
edit exists in either repository (not found).

## 4. Facts bearing on the three update options

Three-way merge:
- A merge needs a base. The only recorded base is `9f14283` as prose in
  `docs/workflow.md` §9, covering that one document. No base commit is stored
  for any other file. Of the 83 kit files, 80 are not at the same path in the
  target, so a path-based merge has no target side for them [GAP: base for the
  files lakeswitch re-derived by hand, e.g. `verdict.py`].
- The 3 same-path files have diverged in content without a stored base
  (`gates.yaml` shares only a name).
- `provenance.yaml` is human-decided in lakeswitch for `AGENTS.md`; any tool
  that writes there is refused by lakeswitch's guard (`plugin/hooks/
  refuse_protected_write.py`, AGENTS.md rule 1).

Pinned kit version:
- `harness.lock.yaml` is named by lakeswitch (D-21) as the future pin, with
  the statement that "the pinned copy replaces this adaptation"; no schema
  or file exists. Kit-side: no tag, release or version field found in
  `manifest.yaml`, `probe.py` or git (tags not listed [GAP]).
- The lakeswitch `docs/workflow.md` §9 and `pilot.yaml` both say several rows
  "come with the pin" — the target already expects the pin to bring the
  prompts, the three-rule set, and `harness decide adr`.

Vendored copy:
- Lakeswitch's tracked `plugin/` and `rendered/` show a pattern for
  generated/guarded folders, but nothing under a vendor folder exists
  (not found). Lakeswitch's `decisions/provenance.yaml` has no prefix for a
  vendor path; a path under no prefix "is a finding, not a default"
  (its header comment) — a new location must be added there, which is
  human-decided.
- The kit's own ruff history mentions a "vendored copy in the project
  instance" (kit `ruff.toml` comment) with `force-exclude` to keep ruff from
  rewriting it: precedent for vendored files existing in an instance.

Other facts:
- The target's gates M-6 (no German prose in `.md`) and M-8 (one list) would
  read any copied file; kit files with German text (`scripts/kit/manifest.yaml`
  comments, `scripts/*` per kit house rule 1) would meet gate M-6 [GAP:
  whether M-6 scans non-`.md`].
- The kit's CI (`ci_gates.py`) derives `ci.yml` from `decisions/gates.yaml`;
  lakeswitch's `verify.yml` derives from its own gates runner. Two runners
  reading a same-named file with different schemas [GAP: schema comparison].
- Target tracker prefix and tracker state differ (kit scripts that call
  `tools/bd` assume a `tools/` folder and the pinned wrapper; lakeswitch has
  neither).
- The target is 87 commits ahead on origin of its local checkout: any
  install run must name which target commit it reads.

## Open items

- [DECISION] Which of the three update options (three-way merge, pinned
  version, vendored copy) — they interact with lakeswitch's own plan
  (`harness.lock.yaml`, D-21, "pinned copy replaces this adaptation").
- [DECISION] Is the install target "a fresh repository" only, or also an
  instance that already re-implemented the mechanism (lakeswitch has 0 of 83
  files byte-equal; 80 absent at the kit's paths)?
- [DECISION] Is `decisions/gates.yaml` (and `ruff.toml`, the decision PR
  template) really `mechanismus`, given the target's own content for the same
  name?
- [DECISION] May the install write into a repository whose `AGENTS.md` is
  `human-decided` (only a proposal text), and into `.claude/` and
  `.github/` that its guard refuses?
- [GAP] Behaviour comparison of lakeswitch's `src/lakeswitch/*` counterparts
  against the 27 kit scripts; whether the kit scripts run on Python 3.11;
  which kit tests fail in lakeswitch.
- [GAP] How the first lakeswitch instance was produced (no export code in
  `scripts/export/`).
- [GAP] Kit tags or releases (`git tag` not run).

## Files a change would have to touch

`scripts/harness.py` (new `kit` verb), `scripts/kit/probe.py` (reuse of
`regeln`, `rolle`, `nach_rolle`), `scripts/kit/manifest.yaml` (possible new
fields), `scripts/export/manifest.yaml`, `tests/test_kit.py`, `docs/WORKFLOW.md`;
on the lakeswitch side, a lock file and `decisions/provenance.yaml`
(human-decided; decision PR).
