---
title: "Decisions — kit-install"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-2uk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, interview, kit, install, lakeswitch]
---

# Kit install and update — Decisions

Phase 1a for bead coding-harness-2uk, on 2026-10-13, after the exploration in
`research.md`: of the 83 files the kit carries, lakeswitch-ai at `ce88eee`
holds 0 identical, 3 edited and 80 missing; it re-implemented the mechanism in
`src/lakeswitch/`.

## Q-1 · Who the install command is for

asked: 2026-10-13
answer: A — first for fresh repositories; for an existing instance such as lakeswitch-ai a comparison report that shows what is missing or differs, and the instance adopts piece by piece in changes of its own.
answered_by: maintainer
status: answered

In the context of a kit that lakeswitch-ai never installed (80 of 83 files
missing, its own mechanism in `src/lakeswitch/`), facing the choice between an
install for fresh repositories plus a comparison report for existing
instances, a full switch of lakeswitch-ai to the kit now, or a lakeswitch-only
command, we decided on fresh repositories first plus the report to achieve a
usable command soon without risk to lakeswitch-ai, accepting that lakeswitch
gains only step by step. — 2026-10-13

## Q-2 · How later improvements reach a target

asked: 2026-10-13
answer: A — a pinned version: the target carries a lock file with the kit commit (`harness.lock.yaml`, as lakeswitch-ai already plans); `kit update` fetches the new version, overwrites only kit files, and reports a kit file the target has changed instead of overwriting it.
answered_by: maintainer
status: answered

In the context of a kit with no version or source marker today, facing the
choice between a pinned version in a lock file, a three-way merge of kit files
the target may edit, or a vendored copy in a folder of its own, we decided on
the pinned version to achieve a simple, traceable update that fits the
planned release builder and pin (bead coding-harness-dj9), accepting that a
target's edit of a kit file stops the update for that file until someone
resolves it. — 2026-10-13

## Q-3 · Files both the kit and a target hold with their own content

asked: 2026-10-13
answer: A — the kit ships them only at the first install, as a starting template; afterwards they belong to the target and `kit update` never touches them again; the manifest gives them a role of their own ("template").
answered_by: maintainer
status: answered

In the context of `decisions/gates.yaml`, `ruff.toml` and the decision pull
request template, which the kit classifies as travelling but lakeswitch-ai
holds with heavily changed content, facing the choice between a starting
template the target owns after install, kit files whose drift every update
reports, or not shipping them at all, we decided on a starting template to
achieve that each repository keeps its own gates and rules by design,
accepting that a later improvement of such a template reaches a target only
by hand or through the comparison report. — 2026-10-13

## Q-4 · What `kit install` does with its changes at the end

asked: 2026-10-13
answer: A — it writes the files and the lock file, runs the target's `make verify`, and does not commit; a person or a session reviews the result and brings it in as a pull request.
answered_by: maintainer
status: answered

In the context of a command that writes into another repository, facing the
choice between leaving the verified changes uncommitted, committing on a new
branch and opening the pull request, or committing directly, we decided on
leaving them uncommitted to achieve that the target's own review and merge
stay the only way the kit takes effect there (ADR 0008), accepting one manual
step after every install or update. — 2026-10-13

## Q-5 · Whether the change carries an ADR

asked: 2026-10-13
answer: A — yes: the change fixes for good how the workflow reaches other repositories (a pinned version in a lock file, the "template" role, no commit by the tool), which binds every future instance and lakeswitch-ai's planned `harness.lock.yaml`; a new ADR records it.
answered_by: maintainer
status: answered

In the context of a command that decides how every instance receives and
updates the workflow, facing the choice between a new ADR and a plain feature
whose rules live only in the spec and the code, we decided on an ADR to
achieve one durable, citable record of the distribution rules, accepting a
decision pull request the maintainer merges. — 2026-10-13

## Q-6 · Whether the change is split

asked: 2026-10-13
answer: A — yes: this change delivers `kit install` for fresh repositories, the comparison report and the lock file; `kit update` follows as a change of its own.
answered_by: maintainer
status: answered

In the context of a phase-2a review that found fifteen gaps, five of them in
the update path alone, facing the choice between splitting install from
update and resolving every gap in one larger change, we decided on the split
to achieve a smaller first change and an earlier report for lakeswitch-ai,
accepting that updates arrive with the follow-up change (bead
coding-harness-2uk's follow-up). — 2026-10-13

## Phase 2a rulings — 2026-10-13, orchestrator

`[DETAIL]` rulings on Opus 5.5's phase-2a rows (`findings.md`), each within
the maintainer's answers Q-1 to Q-6; the redraft carries them into the spec.

- F-1: a target is fresh when it has at least one commit, no
  `harness.lock.yaml`, and tracked files only from `README*`, `LICENSE*`,
  `.gitignore`, `.gitattributes`; any other target is refused and pointed to
  the report (Q-1: existing instances get the report, not the install).
- F-2: only what a fresh instance's `make verify` needs becomes `template`
  (Q-3's three names, plus a starter Makefile and dependency declaration if
  the kit's own are `bestand`); `AGENTS.md`, `provenance.yaml`, `.claude/`,
  `.codex/`, `tools/` and tracker pins are not installed (non-goal).
- F-3, F-4, F-5, F-13: move to the update change (Q-6).
- F-6: the report reads a named target commit (default `HEAD`) from git
  objects, never the working tree, names that commit as its cut-off, and
  compares exact tree paths, so a case-insensitive filesystem cannot fold two.
- F-7: `.github/workflows/ci.yml` gets a role of its own, `derived`: never
  copied; install generates it in the target from the target's gate file with
  the kit's generator, before the target's `make verify`.
- F-8: the starter gate file holds the kit's gates that need neither the
  source's tracker nor its inventory; its pytest gate deselects by name the
  cases the probe declares in `REIST_NICHT`. The target needs at least one
  commit (F-1), and verification sees the payload untracked (Q-4).
- F-9: the lock records the source by its `origin` remote URL and the commit
  sha; how a later run treats another URL belongs to the update change.
- F-10: the probe tree receives the templates with the source's bytes, as a
  fresh install would; `REIST_NICHT` does not grow.
- F-11: install refuses a target that holds `harness.lock.yaml` (F-1).
- F-12: install creates the manifest's `geruest_ordner` with a `.gitkeep`
  each; the lock records them as kit-owned.
- F-14: the steps are writing a file, creating a directory and writing the
  lock; on any failure install removes every file it wrote and every
  directory it created, so the target's tree is as before.
- F-15: the target's `make verify` runs with `BEAD_RENDER` and `PYTHON`
  removed from its environment, as the probe does.
- ADR number: the draft stays `docs/adr/0018-pinned-kit-install-and-update.md`
  (ADR 0017 belongs to bead coding-harness-0ga's branch, `research.md`
  amendment); its scope narrows to install, report and lock, and names
  `kit update` as the follow-up (bead coding-harness-66q).

## Phase 2a rulings — 2026-10-14, orchestrator (second round)

`[DETAIL]` rulings on Opus 5.5's second phase-2a rows (`findings.md`, F-16 to
F-24), each within the maintainer's answers Q-1 to Q-6 and the first rulings
above; the redraft carries them into the spec.

- F-16: reading B. The probe tree is exactly what install writes into an
  empty fresh target at the selected version — kit files, the five templates
  as install initializes them (the gate and Makefile starters, the source's
  bytes for the other three), CI derived from the starter gate file, the
  scaffold placeholders and the lock — and the probe commits it as today.
  This supersedes ruling F-10's "with the source's bytes": F-10 predates the
  separate starters, and its purpose, "as a fresh install would", is what
  makes `REIST_NICHT` a measurement of what a target receives, which AC 18
  then deselects exactly. Cases that read source gate ids or source Makefile
  recipes become generic with fixtures or are scoped under F-17/F-20;
  `REIST_NICHT` and its cap still do not grow (AC 18, AC 21; AC 21's
  "source-original bytes" and its "bootstrap substitution" refutation are
  replaced by this reading).
- F-17: the third disposition is a scoped skip: a shipped case that asserts
  this repository's tracked-file stock (the counts at `tests/test_kit.py:64–70`
  and `:189–200`) or a source-only policy skips when the tree root holds
  `harness.lock.yaml`, the mark of an installed instance — present in the
  probe tree (F-16) and in the target from lock publication on (AC 13), absent
  in the source, which keeps enforcing. The installer's own tests, the
  real-install test included, are `bestand` and do not ship (AC 17, 18, 21).
- F-18: a new criterion after AC 17: a disposable fixture commits the
  installed payload (the adoption pull request's step, taken by the test,
  never by the installer — Q-4, AC 16) and the target's `make verify` passes
  again; the kit manifest gains a `bestand` rule for `harness.lock.yaml`, so
  the lock is classified but never selected for install. Refuted by a shipped
  case red in the committed state, the role check at `tests/test_kit.py:52–61`
  included (AC 7, 17, 19).
- F-19: the freshness allowlist becomes exact root names — `README.md`,
  `LICENSE`, `.gitignore`, `.gitattributes`; any other tracked name
  (`README.rst`, `LICENSE.txt`, …) is refused like every non-fresh target
  (Q-1). The kit manifest gains a `bestand` rule for `LICENSE` (the other
  three have one), and the evidence fixture of AC 17 and F-18 tracks all four
  names (Terms "Fresh target", AC 5, AC 17).
- F-20: every skip condition this change adds to or changes in a shipped test
  file is listed in `plan.md` by case with its predicate, and only two
  predicates are allowed: absence of a path the kit does not ship (the
  existing convention, `tests/test_handover_entry.py`) or the lock mark of
  F-17. Refuted in AC 18 and AC 21 by a skip in the change's diff against its
  merge base that the plan does not list or that uses another predicate; the
  Definition of Done's retained enforcement is shown by each listed case
  running, not skipping, in the source.
- F-21: CI derivation belongs to the proposed payload AC 10 validates: install
  runs the selected generator in the temporary preparation tree before any
  target write, and a gate file the generator rejects — retained or starter —
  refuses with nothing written and no lock (AC 10, AC 19). Ruling F-7's "in
  the target" reads "for the target", as `design.md` already prepares.
- F-22: install refuses before any target write when a template destination
  exists as anything but a regular file — a symlink (also one to a regular
  file), a directory, a submodule or a special file; only a regular file is
  retained (AC 4, AC 6, AC 11).
- F-23: the change raises the kit manifest's `schema_version` from 1 to 2 (it
  adds `template` and `derived`); install and report accept exactly 2, and a
  report against a source commit with another or no manifest schema fails,
  naming that commit and its schema, never classifying the old paths by the
  running version's roles (AC 10, AC 22). A comparison for lakeswitch-ai uses
  a source commit from this change onward.
- F-24: the target's own runtime is the target root's `.venv/bin/python3`,
  else the first `python3` on a PATH from which install has removed every
  entry inside the repository the command runs from (the source `.venv`
  included), besides removing `PYTHON` and `BEAD_RENDER`. Refuted by a test
  that starts install with the source interpreter's directory first on PATH
  and finds it in the verifier's PATH or interpreter; the AC 17 fixture
  supplies its dependencies in the target, never by inheritance (AC 14,
  AC 17).

## Phase 2a rulings — 2026-10-14, orchestrator (third round)

`[DETAIL]` rulings on the three rows of the third phase-2a review, each
within the maintainer's answers Q-1 to Q-6 and the earlier rulings; the next
redraft carries them into the spec before implementation starts.

- F-25: the shipped role check (every tracked file falls under a manifest
  rule) is a check of this repository's own tracked set, so it takes the
  ruling F-17 skip: it skips when the tree holds `harness.lock.yaml`. AC 18
  drops its clause on the role check for `harness.lock.yaml` and `LICENSE`;
  the source keeps their `bestand` rules (rulings F-18, F-19) and keeps
  enforcing the check. An instance's own files therefore never turn its
  gate red (AC 18, 19).
- F-26: a target with no tracked file is not fresh. Freshness needs at least
  one commit and at least one tracked file, every tracked file one of the
  four names of ruling F-19; install refuses an empty target before any
  write and names the remedy (commit a `README.md`). AC 22's "empty fresh
  installation" is reworded to the probe's own tree (Terms, AC 5, 17, 22).
- F-27: the fixture starts the post-commit `make verify` of ruling F-18
  under the same environment rule as AC 14 and ruling F-24: `PYTHON` and
  `BEAD_RENDER` removed, and every `PATH` entry inside the running
  command's repository removed; AC 18 and the Definition of Done say so,
  and a planted inherited `PYTHON` turns the test red (AC 14, 18).
