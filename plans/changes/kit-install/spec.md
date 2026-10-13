---
title: "Spec — kit-install"
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
produced_by: {kind: llm-session, name: codex, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, kit, install, update]
class: feature
appetite: 12
change: kit-install
adr_question: {proposed: "yes", reason: "Pinned distribution, template ownership and uncommitted installation bind future workflow instances."}
adr_files: [docs/adr/0017-pinned-kit-install-and-update.md]
---

# Spec — kit-install

Install the workflow in a fresh repository, update its unchanged kit files
from a pinned source version, and give an existing instance a comparison
report for adoption in its own changes (bead coding-harness-2uk). Research:
`research.md`. Maintainer answers: `decisions.md`, Q-1 through Q-5.

## Problem

- The kit can measure portability but cannot install or update an instance:
  its probe writes only a throwaway tree, the export directory has no
  exporter, and the command exposes only `decide adr` (research §1,
  coding-harness `3199a28`, 2026-10-13).
- An instance cannot establish which source bytes it received. Neither
  repository has a lock or per-file baseline; the existing instance names
  one historical comparison commit only in prose (research §§1 and 4,
  coding-harness `3199a28`, lakeswitch-ai `ce88eee`, 2026-10-13).
- Files with the same name have different owners. The target's gates,
  lint rules and decision pull request template are intentionally different,
  yet all three are classified as unchanged mechanism today (research §2,
  the same source and target commits).
- A whole-instance replacement would discard deliberate adaptations. Of
  the 83 source kit files measured at those commits, the target has no
  identical file, three edited files and 80 missing at the source paths
  (research §§2–3). The maintainer chose a report and gradual adoption.
- A bare repository cannot run the promised verification from the present
  payload: its manifest excludes the Makefile and dependency declarations,
  and its gate list includes source-repository prerequisites (research §2
  and the local drafting addendum, 2026-10-13).

## Terms

- **Fresh target:** a Git working tree selected for its first workflow
  adoption, without `harness.lock.yaml` or files at the proposed kit-owned
  destinations; it may already contain project files and configuration.
  Missing kit paths alone do not establish freshness: a separately
  reimplemented workflow uses the existing-instance report route (Q-1).
- **Kit file:** a published file with role `mechanismus`; updates own only
  paths whose installed baseline is recorded in the target lock.
- **Template:** a first-install starting file with role `template`; after
  installation its path belongs to the target, including when it is edited
  or removed there.
- **Source version:** the full Git commit resolved from the requested
  revision; dirty source working files do not belong to that version.
- **Conflict:** a path that cannot receive the requested change without
  replacing local work or changing its recorded ownership.

## Acceptance criteria

1. When a fresh target is installed from an available source version, every
   manifest-selected kit file is present with that version's bytes and Git
   executable bit.
   *Refuted by:* a selected file is omitted, transformed or copied from the
   dirty source working tree instead of the resolved commit.
2. While the kit is installed, source inventory classified as `bestand`
   remains outside the payload.
   *Refuted by:* a source journal, change artifact, ADR answer or tracker
   record appears in the target through installation.
3. When the manifest classifies initial configuration, the gates file, lint
   configuration and decision pull request template have the `template` role.
   *Refuted by:* any of `decisions/gates.yaml`, `ruff.toml` or
   `.github/PULL_REQUEST_TEMPLATE/decision.md` is classified as kit-owned.
4. If an initial template destination already exists as a regular file,
   installation preserves its contents and reports that the target owns it.
   *Refuted by:* an existing template is overwritten, merged or claimed as
   a kit file, even when its bytes equal the source.
5. If an unpinned target already contains a proposed kit-file destination,
   installation refuses before writing any target file.
   *Refuted by:* an existing mechanism is overwritten or silently adopted,
   or unrelated installation writes occur before the collision is refused.
6. When installation writes its lock, the lock identifies the source
   repository, full resolved commit and installed per-file ownership and
   byte/mode baselines.
   *Refuted by:* a branch name stands in place of a resolved commit, a
   published file lacks its baseline, or a preserved template is kit-owned.
7. When an instance is compared with a source version, the report identifies
   both repository commits and each expected destination's ownership and
   state as missing, identical or different.
   *Refuted by:* a missing or changed path is omitted, template differences
   are labelled accidental kit drift, or the report has no source/target
   commit cut-off.
8. While a comparison report runs, the command leaves target files and Git
   state unchanged.
   *Refuted by:* reporting creates a lock, writes a proposal into the target,
   invokes verification there or changes its index, refs or configuration.
9. If update has no readable, supported lock, it refuses before writing.
   *Refuted by:* update infers ownership from matching filenames or hashes,
   repairs a malformed lock silently, or begins applying files without it.
10. When the selected version retains a recorded kit file whose byte/mode
    baseline is unchanged locally, update replaces it with that version's file.
    *Refuted by:* unchanged files stay at the old version or receive bytes or
    executable bits from a different revision.
11. When the selected version adds a kit file at an absent, previously unowned
    target path, update installs it and records its baseline.
    *Refuted by:* the new file is omitted or remains outside the lock.
12. When the selected payload no longer contains an unchanged installed kit
    path, update removes that file.
    *Refuted by:* the retired file remains, or its containing directory and
    unrelated target content are removed with it.
13. If an installed kit path has changed locally, update preserves that path
    and reports its conflict.
    *Refuted by:* edited bytes, a local deletion, a changed executable bit or
    a replacement file type is overwritten, including on upstream removal.
14. While a path belongs to the target as a template, update never writes or
    deletes it.
    *Refuted by:* a newer, removed or locally deleted template changes the
    target path during update.
15. If an upstream change would transfer a recorded path between kit and
    target ownership, update reports an ownership conflict without changing
    that path or its recorded owner.
    *Refuted by:* a template is acquired as mechanism or a kit file is
    silently released into target ownership.
16. If an update applies safe files while other paths conflict, the lock
    retains each conflicted file's prior baseline and identifies the
    incomplete requested version.
    *Refuted by:* a blocked file is recorded as newly installed, or a partial
    update is presented as a fully applied source pin.
17. If the source revision, manifest or planned payload cannot be validated,
    the command refuses before writing target files.
    *Refuted by:* an unavailable revision, unsupported schema, unclassified
    source file or conflicting destination produces a partial installation.
18. If a published or locked path escapes the target, traverses a symlink or
    enters its Git metadata, the command refuses before writing.
    *Refuted by:* an absolute path, `..`, a linked ancestor, source symlink
    or `.git` destination causes a write outside the validated payload.
19. If a handled payload write fails before verification, the command restores the
    target files and lock to their state before that application's writes.
    *Refuted by:* an injected write failure leaves advanced lock entries,
    replaced files, deletions or newly created payload files behind.
20. When install or update reaches the end of an application, the command
    invokes `make verify` once in the target working directory.
    *Refuted by:* verification is skipped, run in the source repository,
    substituted with a different command or run before the applied lock is
    visible; a partial update also requires this run.
21. If target verification fails or cannot start, the command returns failure
    with the reason and leaves the applied files available for review.
    *Refuted by:* a red or unavailable `make verify` yields success, hides
    its failure or rolls back the reviewable result as if application failed.
22. While install or update performs its own actions, it leaves the target's
    Git index, HEAD, branches and remotes unchanged.
    *Refuted by:* the tool stages, commits, switches branches, pushes, merges
    or opens a pull request automatically.
23. When a bare fresh target has Git, make and the declared Python runtime
    dependencies available, the supplied initial configuration gives it a
    passing `make verify` without source tracker data or endpoint credentials.
    *Refuted by:* the bootstrap needs this repository's inventory, a tracker
    bootstrap, a model key or a verification command missing from the payload.
24. If comparison cannot read a source or target state, it reports the
    unmeasured state and returns failure.
    *Refuted by:* a permission error, unreadable file or unresolved commit is
    reported as absence, equality or a successful empty comparison.

## Non-goals

- Switching lakeswitch-ai to the kit, rewriting its counterparts, discovering
  semantic equivalence at renamed paths, or writing proposals into it. Its
  owner uses the report in separate adoption changes (Q-1).
- Three-way merging, a vendor directory, a force-overwrite option or changing
  ownership automatically (Q-2 and Q-3).
- A release builder, public releases, automatic version selection or the
  planned distribution bundle; that work can consume the resolved-commit
  interface later (bead coding-harness-dj9).
- Installing runtimes, packages, trackers, model endpoints or local harness
  settings. Missing runtime dependencies make verification fail explicitly.
- Crash recovery or simultaneous writers in one target. The application
  assumes one writer and restores its own batch on handled write failures.
- Enabling every source-repository gate in a new instance. Its initial gate
  list checks the portable baseline; its owner adopts repository-dependent
  gates in that instance. Existing configuration takes precedence (Q-3).
- Changing phase routing, interview rules, the legacy export policy or the
  unavailable general change-artifact validator.

## Protected areas

- All existing instances and customer repositories: this change tests
  disposable repositories only; existing instances receive read-only reports.
- Source journals, tracker data, ADR answers and project inventory: they are
  excluded from the delivered workflow and are not rewritten by this change.
- `AGENTS.md`, `provenance.yaml`, `decisions/gates.yaml`, source dependency
  pins, `.claude/`, `.codex/` and `tools/`: their live policies stay intact;
  fresh-instance starting content is kept separately in the kit.
- `scripts/export/manifest.yaml`: its independent migration/export decision
  remains separate from installing the role-defined kit.
- Existing ADRs and their continuity map: this change adds one new record
  and amends no numbered interview decision.

## Definition of Done

- `make verify` is green in this worktree using its locked environment; the
  interview check and criterion ledger also hold for this change.
- The fresh-install integration run passes actual target `make verify`;
  update regressions prove local edits survive and the lock tells the truth
  after a partial update. Evidence names the tested source commit in the PR.
- The code PR carries these spec, design and plan files, the implementation
  paths listed in the plan, the updated workflow instructions and
  `docs/adr/0017-pinned-kit-install-and-update.md` together.
- The protected areas and non-goals remain outside the PR's file list.
- The decision PR records the distribution rules chosen in Q-1 through Q-5;
  merge is acceptance. Any required ADR-answer file is recorded by the
  orchestrating session from Q-5, never by this drafting call.
- The PR closes the install/update work item and its final commit carries
  `Closes-Bead: coding-harness-2uk`; only the authorized tracker writer closes
  it after the workflow gates (bead coding-harness-2uk).
- The general artifact-validator command cannot run in this checkout because
  its script is absent; no implementation step fabricates that gate. Its
  availability must be checked again before claiming that particular gate.

## Open decisions

None open. All five intent choices are recorded in `decisions.md`; Q-5 is
the maintainer's stated ADR choice, without an ADR-answer file authored here.
No phase-2a finding row exists in the input `findings.md` as of 2026-10-13.

- [DETAIL] Use `class: feature`: this adds delivery to the existing kit and
  command rather than replacing a subsystem or breaking an existing command;
  its durable distribution contract still requires the proposed ADR.
- [DETAIL] Require an explicit revision for install, update and report so
  selection is visible; resolve it to a full commit before comparing or
  writing. Command spelling and transport staging stay reversible details.
- [DETAIL] Keep per-file baselines and a pending version after partial
  updates: Q-2 stops the edited file, and this makes safe progress traceable
  without claiming that the blocked file received new bytes.
- [DETAIL] Supply separate portable bootstrap templates for missing initial
  configuration, retaining existing files. Copying the source's inventory
  dependent gate list would prevent the fresh repository promised by Q-1 and
  Q-4 from verifying; template ownership permits later instance adaptation.
- [DETAIL] Set a 12-hour phase-4 appetite, repair rounds included, as the stop
  for the installer, update safety and disposable-repository evidence; no
  earlier artifact sets an appetite for this change.

These reversible details are chosen here with their reasons; they do not
answer a new question on the maintainer's behalf.
