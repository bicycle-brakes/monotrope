---
title: "Spec — conflict-marker-gate"
status: draft
implementation_status: none
date: 2026-11-05
last_reviewed: 2026-11-22
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-i76l
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "glm-5.3, 2026-11-22"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, gate, merge]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — conflict-marker-gate

Verification blocks merge-conflict markers in tracked text files, and the
supported main-merge helper stops safely on ordinary conflicts (bead
coding-harness-i76l — conflict-marker gate). Research: `research.md`.
Authority: the maintainer-approved scope in `decisions.md`, “SKIP · interview”.
Revised 2026-11-22 after phase 2a; the five findings (S-1 to S-5) are worked
in, each decision recorded under Open decisions.

## Problem

- The research read on 2026-11-05 finds no conflict-marker gate in the one
  gate list; the only direct detector guards plans rendering during sync,
  leaving other tracked files and already committed markers unmeasured
  (`research.md`, “What exists today”).
- The maintainer-approved scope records a merge followed by a commit and
  push of unresolved workflow-document markers at `31d35400`, on
  2026-11-05 (`decisions.md`). A clean Git status therefore does not prove
  that the committed text is conflict-free.
- The existing `merge-main` helper already reports non-index conflicts
  without updating the branch; this change must preserve that supported
  path rather than introduce a competing merger (`research.md`, “The merge
  machinery knows git conflicts, not text markers”).

## Terms

- **Marker line:** a line beginning in column one with `<<<<<<<`, `=======`
  or `>>>>>>>`, with any suffix, including no suffix or additional marker
  characters. Labels, complete conflict groups and file extensions do not
  affect detection.
- **Tracked text:** a regular file present in the working tree and listed
  by Git's index, whose contents contain no NUL byte; non-UTF-8 bytes do
  not exempt an otherwise textual file. Symlinks and submodule entries are
  not followed. Deleted paths have no working-tree text to scan.
- **Named fixture exception:** an exact repository-relative file path in
  the allowlist constant of `scripts/check_conflict_markers.py`, never a
  directory, wildcard or blanket test exemption. The list starts empty,
  travels with the kit as mechanism, and changes only through a reviewed
  pull request; a test plants a non-empty list by injecting the constant,
  never by widening production defaults.
- **Supported main-merge helper:** `python3 scripts/pr_sync.py merge-main
  --root .`, the one supported way to merge main into a change branch
  (`docs/WORKFLOW.md` §3, “Pull requests stay mergeable”). This change
  reuses it and pins its behaviour with tests; no competing merger is
  added.

## Acceptance criteria

1. When tracked text outside named fixture exceptions contains any marker
   line, the standalone check fails even with a clean index and working tree.
   *Refuted by:* a committed marker passes in a document, source file or
   plans file, including a marker inside a fenced example or a non-UTF-8 file.
2. When marker lines are found, the check reports every affected path and
   its one-based line numbers without changing repository content or refs.
   *Refuted by:* a second affected file is omitted, locations are wrong,
   or checking stages, repairs, commits or pushes anything.
3. While the measured files contain no marker lines, binary files, untracked
   files and exact named fixtures do not cause marker findings.
   *Refuted by:* clean text is rejected, a binary or untracked marker is
   scanned, or allowing one fixture also exempts a sibling or prefix match.
4. When Git's whitespace and error check, invoked with a fixed
   `core.whitespace` rule set on the command line so that a user's global
   and system Git configuration cannot change the verdict while repository
   `.gitattributes` still apply, reports a fault in staged or unstaged
   changes outside named fixture exceptions, the check fails with its
   diagnostic.
   *Refuted by:* a trailing-whitespace fault passes in either change layer,
   including a staged faulty blob whose working file has been restored, or
   the verdict changes on a machine whose Git configuration disables a
   whitespace rule.
5. If required Git inspection or reading a present tracked regular file
   fails, the check exits unsuccessfully and explains what was not measured.
   *Refuted by:* a non-repository root, failed Git command or unreadable
   tracked file produces a successful empty report.
6. When local full verification, its document subset or hosted verification
   runs, the one gate list supplies this check — declared command
   `python3 scripts/check_conflict_markers.py`, cost class `seconds`, so it
   runs before admission is requested with the other seconds gates — with
   blocking enforcement.
   *Refuted by:* any of those paths omits the gate, treats its failure as
   advisory, runs a command different from the declared one, or declares a
   cost class that moves the gate inside the admission.
7. When the supported main-merge helper encounters a conflict outside
   `plans/INDEX.md`, it exits unsuccessfully with the conflicting paths and
   leaves the target branch, Git's staging area, `plans/INDEX.md`, the
   working files and the branch on origin unchanged; its fetch may move
   local remote-tracking refs.
   *Refuted by:* the helper succeeds, omits a conflicted path, publishes a
   result, moves the staging area or the generated index, or leaves
   conflict-marker text in the invoking checkout.
8. When the workflow kit is assembled, the new gate and its tests travel
   with the gate machinery they depend on.
   *Refuted by:* a kit copy declares the gate but omits its executable or
   tests, or the isolated kit probe fails because of this addition.
9. If the fixture allowlist names a repository-relative path that Git's
   index does not track, the check fails naming that path.
   *Refuted by:* a stale or pre-registered allowlist entry is silently
   ignored, waiting to exempt a file that does not exist or is not tracked.

## Non-goals

- No Git hook, push interception, server-side merge integration, automatic
  conflict resolution, new merge command or changes to sync eligibility.
  A caller must stop on the existing helper's unsuccessful exit; this
  change cannot prevent an arbitrary later shell command from being run.
- No historical commit scan or general whitespace cleanup; whitespace is
  checked in current staged and unstaged changes, markers across current
  tracked text. No independent scan for diff3 base markers or indented
  marker fragments beyond whatever `git diff --check` already reports.
- No global fence exemption, user-supplied skip flag, tracker changes,
  endpoint changes or changes to the existing plans-renderer detector.
- No design phase or ADR: the bounded package adds a check to existing
  verification machinery and reuses the existing merge helper.

## Protected areas

`scripts/stage2.py`, `scripts/pr_sync.py`, `scripts/plans_registry.py`,
`provenance.yaml`, existing ADRs, endpoint configuration, installed harness
configuration and tracker data remain unchanged. The orchestrator alone
edits the held gate declaration and generated hosted workflow.

## Definition of Done

- `make verify` green after orchestrator bootstrap; targeted tests show
  clean controls and planted marker, whitespace and measurement failures.
- Move together: `scripts/check_conflict_markers.py`,
  `tests/test_check_conflict_markers.py`, `tests/test_pr_sync.py`,
  `scripts/kit/manifest.yaml`, `decisions/gates.yaml`, the generated
  `.github/workflows/ci.yml` and `docs/governance/gate-catalog.md`, this
  change's artefacts and regenerated `plans/INDEX.md`; no file is deleted.
- The pull-request file list demonstrates protected areas and non-goals.
- The decision pull request names the conflict-marker gate task
  (coding-harness-i76l); its final commit carries
  `Closes-Bead: coding-harness-i76l`, with closure left to the tracker writer.
- Special runs: offline disposable-Git gate and merge regressions, recorded
  with the tested commit; no live branch is merged or pushed as a test.

## Open decisions

None open. The phase-2a findings of 2026-11-22 (S-1 to S-5 in
`findings.md`) are decided as `[DETAIL]`s; each is worked into the terms and
criteria above, and its status stands in `findings.md`. I chose the
following reversible `[DETAIL]` defaults and recorded why; none changes the
maintainer's approved scope:

- Helper (S-1): the existing `merge-main` is the approved helper — reading
  A in the finding; it is pinned by regression tests and already named in
  `docs/WORKFLOW.md` §3 as the supported way to merge main into a change
  branch, not rebuilt.
- Unchanged-by-merge wording (S-2): “index” means Git's staging area and
  `plans/INDEX.md`, each unchanged; “remote branch” means the branch on
  origin, unchanged; local remote-tracking refs may move by the helper's
  fetch.
- Allowlist (S-3): a constant in `scripts/check_conflict_markers.py`,
  starting empty, travelling with the kit as mechanism, naming exact
  tracked paths only, changed through a reviewed pull request alone. An
  entry naming no tracked path is itself a finding (criterion 9) — my
  sub-decision, so a stale or pre-registered entry cannot wait silently to
  exempt a future file.
- Gate metadata (S-4): cost class `seconds` — the schema's closed
  vocabulary, so the gate runs before admission is requested with the other
  seconds gates; declared command `python3 scripts/check_conflict_markers.py`
  with an optional `--root` defaulting to the repository root, which
  criterion 5's non-repository-root refutation exercises.
- Whitespace verdict (S-5): every `git diff --check` invocation carries a
  fixed `core.whitespace` rule set on the command line — Git's built-in
  default `blank-at-eol,blank-at-eof,space-before-tab` — so global and
  system configuration cannot change the verdict; repository
  `.gitattributes` still apply.
- Use the marker prefixes exactly as approved, in every tracked text path,
  including fenced blocks: a fence must not hide an accidental conflict.
  The fixture allowlist starts empty because the current tracked prefix
  search at `2d4b1a3d` on 2026-11-05 found no file needing an exception.
- Define text by absence of NUL and inspect marker prefixes as bytes to
  avoid silently dropping text solely because UTF-8 decoding fails.
- Check both staged and unstaged differences with `git diff --check`;
  the full scan catches markers already committed, while diff checking
  avoids turning historical whitespace into unrelated cleanup work.
- Register a `verify` gate, placement `both`, subset `docs`, `floor: false`:
  it blocks all supported verification paths without expanding the
  separately governed non-negotiable floor. Carry it as kit mechanism.
- Reuse `python3 scripts/pr_sync.py merge-main --root .` and extend its
  regression; its current non-index conflict refusal already satisfies
  the approved helper requirement, including index regeneration's exception.
- Stop phase 4 after two hours including repairs; neither source gives
  an earlier appetite. No separate design artefact is due for `bounded`.
