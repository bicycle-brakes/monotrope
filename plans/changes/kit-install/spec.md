---
title: "Spec — kit-install"
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-14
updated: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-2uk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, kit, install, report]
class: feature
appetite: 12
change: kit-install
adr_question: {proposed: "yes", reason: "Pinned distribution, template ownership and uncommitted installation bind future workflow instances."}
adr_files: [docs/adr/0018-pinned-kit-install-and-update.md]
---

# Spec — kit-install

Install the workflow in a fresh repository with a source pin and give an
existing instance a comparison report for adoption in its own changes (bead
coding-harness-2uk). Research: `research.md`. Maintainer answers:
`decisions.md`, Q-1 through Q-6, including the split that defers updates.

This revision incorporates both rounds of recorded phase-2a rulings, through
2026-10-14. Q-6 defers updates; ruling F-18 adds proof after the adoption
commit as criterion 18, shifting the former criteria 18–22 to 19–23. These
changes follow the recorded scope and rulings, not a gate result. Design
runs in `design.md`.

## Problem

- The kit measures portability but cannot install an instance: the probe
  writes a throwaway tree, the export directory has no exporter, and the
  command exposes only `decide adr` (research §1, coding-harness `3199a28`,
  2026-10-13).
- An instance cannot establish which source bytes it received: neither
  repository has a lock or per-file baseline, and the existing instance names
  one historical comparison commit only in prose (research §§1 and 4,
  coding-harness `3199a28`, lakeswitch-ai `ce88eee`, 2026-10-13).
- Shared filenames hide different owners: the target's gates, lint rules and
  decision pull request template are deliberately different, yet all three
  are classified as unchanged mechanism (research §2, the same cut-offs).
- A wholesale replacement would displace deliberate adaptations: of the 83
  kit paths measured at those cut-offs, the target has none identical, three
  edited and 80 missing (research §§2–3). It needs a report for gradual
  adoption, not automatic conversion (Q-1).
- The current payload cannot give a fresh target a passing verification:
  the Makefile and dependency declaration stay behind, the source gate list
  needs its own inventory, and copied CI would describe that source list
  rather than the target's starting list (research §2 and drafting addenda).

## Terms

- **Fresh target:** the root of a non-bare Git working tree with at least one
  commit, no `harness.lock.yaml` of any file type, and tracked paths only from
  the exact root names `README.md`, `LICENSE`, `.gitignore` and
  `.gitattributes`. Other names, including `README.rst` and `LICENSE.txt`,
  are outside the allowlist. Untracked files
  do not establish ownership and still undergo destination checks.
- **Kit file:** a selected source file with role `mechanismus`; its bytes and
  executable bit remain the source version's, and the lock records kit
  ownership. Scaffold `.gitkeep` files also have kit ownership.
- **Template:** initial target configuration with role `template`; its path
  belongs to the target after install, including when the target edits or
  removes it. An existing regular template is retained.
- **Derived file:** `.github/workflows/ci.yml`, produced from the target's
  gate file rather than copied; its contents belong to the target's gate
  configuration and are recorded separately from kit-file baselines.
- **Source version:** the full Git commit resolved from an explicit requested
  revision; dirty source files do not belong to it. Source identity is the
  source repository's `origin` remote URL, never a fallback checkout path.
- **Supported manifest:** exactly kit manifest schema 2, which declares
  template and derived ownership. Install and report refuse any other or
  missing schema at the selected source commit.
- **Comparison:** exact, case-sensitive Git tree paths, committed bytes and
  Git modes at named source and target commits. Template and derived rows
  use the source's same-path committed file as a reference, not as a claim
  that target-owned content should be overwritten. Uncommitted files are
  outside the measurement; target revision defaults to `HEAD`.
- **Isolated verification environment:** neither `BEAD_RENDER` nor the
  caller's `PYTHON`, and a PATH with every entry inside the command's
  repository removed, including its `.venv/bin`. The runtime is the target
  root's available `.venv/bin/python3`, otherwise the first `python3` on that
  cleaned PATH; dependency setup belongs to the caller.
- **Scoped test skip:** a case and predicate listed in `plan.md`; an added or
  changed predicate may use only an absent path the kit does not ship or
  the root `harness.lock.yaml` marking an installed instance. The latter is
  present in the probe and target, absent in the source.

## Acceptance criteria

1. When a fresh target is installed from an available source version, every
   selected kit file has that commit's bytes and Git executable bit.
   *Refuted by:* a selected file is omitted, transformed or copied from dirty
   source files instead of the resolved commit.
2. While installation selects its payload, source inventory and the excluded
   agent, provenance, endpoint and tracker configuration stay outside it.
   *Refuted by:* installation writes source journals, change artifacts, ADR
   answers, tracker data, `AGENTS.md`, `provenance.yaml`, `.claude/`, `.codex/`,
   `.agents/`, `tools/` or `model-endpoints.yaml` into the target.
3. When initial configuration is classified, exactly `decisions/gates.yaml`,
   `ruff.toml`, `.github/PULL_REQUEST_TEMPLATE/decision.md`, `Makefile` and
   `requirements-ci.txt` are target-owned templates.
   *Refuted by:* one of these is kit-owned, or another destination is silently
   initialized as target configuration; CI has the separate derived role.
4. If a template destination already holds a regular file, installation
   preserves its bytes and executable bit and reports target ownership.
   *Refuted by:* an existing template is overwritten, merged or kit-owned,
   including when its bytes equal the starter.
5. If the target fails the freshness definition, install refuses before any
   target write and directs the caller to the comparison report.
   *Refuted by:* an unborn, non-root, bare, already pinned or populated target
   receives any installation file; repeating an install after red verification
   is also refused while its lock remains.
6. If a non-template destination is occupied or a template destination exists
   as anything other than a regular file, install refuses before any target
   write.
   *Refuted by:* an existing kit file, derived workflow or scaffold placeholder
   is overwritten or silently adopted, even with identical bytes, or a
   template symlink, directory, submodule or special file is retained or replaced.
7. When installation publishes `harness.lock.yaml`, it identifies the source
   origin URL, full commit and each installed destination's ownership,
   source or derivation, byte hash and Git mode.
   *Refuted by:* a checkout path or branch name replaces the origin URL or
   resolved commit, a file or scaffold baseline is missing, or a retained
   template is claimed as a kit file; retained-template records must identify
   that no source baseline was installed there.
8. When comparison succeeds, it names both resolved commits and reports every
   selected same-path source file as missing, identical or different with its
   kit, template or derived ownership.
   *Refuted by:* dirty target files influence the result, case-distinct tree
   paths are folded, a selected path or commit cut-off is absent, or a
   template/derived difference is called accidental kit drift.
9. While comparison runs, target files and Git state remain unchanged and no
   target verification runs.
   *Refuted by:* a lock, report file, index, ref, configuration or verifier
   output is created or changed by the report.
10. If the revision, source identity, manifest or complete proposed payload
    including CI derivation cannot be validated, install refuses before any
    target write.
    *Refuted by:* an unavailable commit, missing origin, unsupported schema,
    unclassified source file, conflicting rule or unrepresentable destination
    permits a partial install, or the selected generator rejects retained or
    starter gate bytes after a target file or lock has been written.
11. If a payload path, recipe or scaffold escapes the target, traverses a
    symlink or enters Git metadata, install refuses before writing.
    *Refuted by:* an absolute or parent-traversing path, source symlink or
    submodule, linked target ancestor, or `.git` destination receives a write.
12. If a filesystem operation fails while writing a payload file, setting its
    mode, creating a directory or publishing the lock before verification,
    install restores the target's prior files and directories.
    *Refuted by:* an injected filesystem error at any of those steps leaves
    an installer-created file, lock, temporary file or directory, or changes
    an existing template or directory; the verifier must not start.
13. When installation completes its application, it invokes `make verify`
    exactly once in the target root with the applied lock visible.
    *Refuted by:* verification is skipped, duplicated, substituted, run in the
    source, or started before lock publication.
14. When target verification starts, it uses the isolated verification
    environment and target runtime defined above.
    *Refuted by:* either source-session variable or any PATH entry inside the
    command repository reaches the verifier, or it chooses that repository's
    interpreter; tests put the source interpreter directory first on the
    caller's PATH and cover both target-venv and cleaned-PATH selection.
15. If target verification fails or cannot start, install returns failure with
    the reason and leaves the applied files and lock available for review.
    *Refuted by:* an unavailable or red `make verify` produces success, hides
    its failure or rolls back the reviewable application.
16. While install performs its own actions, the target's index, HEAD, branches
    and remotes remain unchanged.
    *Refuted by:* the command stages, commits, switches, fetches into the
    target, pushes, merges or opens a pull request.
17. When an eligible target tracking all four allowed root names uses the
    supplied starters and has Git, make, Python 3.12 and the declared
    dependencies available in its own environment, actual target
    `make verify` passes with the installed payload untracked.
    *Refuted by:* it needs staging, source inventory or tracker data, model
    endpoint credentials, an extra starter, a command absent from the payload,
    or dependencies inherited from the source; omitting an allowed root name
    from the evidence fixture does not meet this criterion.
18. When a disposable fixture commits the reviewed installed payload,
    including the lock, actual target `make verify` passes again.
    *Refuted by:* a shipped case fails after commit, including the role check
    for `harness.lock.yaml` or `LICENSE`, or only the untracked state is tested;
    the fixture's commit is not an installer action.
19. When the starting gate file is supplied, its blocking local gates are
    portable pytest, ruff check, ruff format, ADR answers, criterion ledger,
    gate schema and CI drift, with pytest running all shipped test files and
    deselecting exactly the named cases in the selected version's `REIST_NICHT`
    alongside only the explicitly listed scoped skips.
    *Refuted by:* a gate is replaced by an always-green command, a shipped
    test file is silently dropped, or extra cases are deselected to hide a
    target failure; an added or changed skip absent from the plan or using
    another predicate also refutes it. Source inventory gates are not starters.
20. When install supplies `.github/workflows/ci.yml`, it derives the file
    from the selected target gate contents using that kit version's generator
    before any target write.
    *Refuted by:* the source workflow is copied, retained templates are
    ignored, regenerating CI from the target gate file yields other bytes,
    or rejected gate contents leave target files or a lock.
21. When installation supplies the manifest's scaffold folders, each contains
    an empty `.gitkeep` recorded as kit-owned in the lock.
    *Refuted by:* a declared folder or placeholder is absent, source contents
    populate a scaffold, or its placeholder has no kit baseline.
22. When the portability probe builds and commits its disposable tree, the
    payload equals an empty fresh installation of the selected version,
    without growing `REIST_NICHT` or its cap and with only listed scoped skips.
    *Refuted by:* a kit file, initialized template, derived CI, scaffold
    placeholder or lock differs or is missing; source gates/Makefile replace
    their starters; exceptions or the cap grow; or an added/changed skip is
    unlisted or uses another predicate. The probe commits for measurement;
    the installer does not. Exemption removals require measured evidence.
23. If comparison cannot resolve or read required Git state or the selected
    source has no supported manifest, it returns failure and identifies what
    was not measured.
    *Refuted by:* an unresolved revision or unreadable object is reported as
    absence, equality or a successful empty comparison, or schema 1/absent
    schema is compared using the running version's classification instead of
    failing with the selected commit and observed schema named.

## Non-goals

- `kit update`, retry/conflict resolution, role transfers, retired-file
  removal and partial pins. They resume in the separate update change,
  including findings F-3, F-4, F-5 and F-13 (Q-6; bead coding-harness-66q).
- Converting lakeswitch-ai or any existing instance, rewriting counterparts,
  semantic matching at renamed paths, or working-tree drift measurement.
  Adoption uses separate instance changes after the report (Q-1).
- Installing agent entry points, provenance maps, harness settings, trackers,
  endpoint declarations, runtimes or packages. The caller provides runtime
  dependencies; missing dependencies produce an explicit verification failure.
- A release builder, bundles, public releases, automatic version selection,
  three-way merging, vendor folders or force overwrites (Q-2; release work
  follows separately, bead coding-harness-dj9).
- Crash/power-loss recovery and simultaneous writers in one target. The
  filesystem-error rollback criterion covers one uninterrupted writer.
- Changing phase routing, interview rules, the independent legacy export
  policy or implementing the absent general change-artifact validator.

## Protected areas

- All real instances and customer repositories: implementation operates only
  on disposable fixture repositories; comparison itself remains read-only.
- Source inventory, journals, tracker data, ADR answers and all pre-existing
  ADRs: this change owns only its still-unmerged ADR 0018 draft.
- Source `AGENTS.md`, `provenance.yaml`, `decisions/gates.yaml`, dependency
  versions, runtime settings, `.claude/`, `.codex/`, `.agents/` and `tools/`:
  their live policies and pins are not changed to bootstrap an instance.
- `scripts/export/manifest.yaml` and decision-continuity mappings: installation
  does not reinterpret their independent migration and amendment policies.

## Definition of Done

- `make verify`, the named-change interview check and criterion ledger pass
  in the locked source environment.
- The real fresh-target install passes target `make verify` before and after
  the fixture commits its payload, with all four allowlisted names tracked;
  fixture reports,
  refusals, failure injection and environment isolation have test evidence
  naming the source commit in the PR. No real instance is installed.
- The PR carries the implementation files listed in `plan.md`, revised spec,
  design and plan, review dispositions, `docs/WORKFLOW.md` and the single
  new-to-main ADR draft `docs/adr/0018-pinned-kit-install-and-update.md`.
- The protected policies remain intact and the PR's file list excludes the
  non-goals. Every added or changed skip matches the case/predicate list in
  `plan.md`; each listed case runs without skipping in the source, with its
  original source assertions enforced.
- The decision PR records the already stated choices; merge is acceptance.
  No ADR answer is authored or changed by this drafting call.
- The PR closes the install/report work item with the final commit trailer
  `Closes-Bead: coding-harness-2uk`; update remains its separate work item.
- `scripts/validate_change_artefacts.py` is absent at the 2026-10-14 drafting
  cut-off, so its named gate is not claimed green; the runner checks the
  available registry and full verification gates.

## Open decisions

None open. The six maintainer answers and the orchestrator's phase-2a rulings
are recorded in `decisions.md`; this revision incorporates them without
writing an answer or an ADR-answer record.

- [DETAIL] Keep `class: feature`, the existing quoted ADR proposal, the
  claimed ADR 0018 and the 12-hour appetite. Q-6 narrows the deliverable; it
  does not reclassify it, renumber its reserved ADR or enlarge its appetite.
- [DETAIL] Require `--ref` for install/report and add `--target-ref` to report,
  defaulting to `HEAD`, so each measurement has an honest commit cut-off.
- [DETAIL] Compare source-original template and derived files in the report,
  visibly labelled as target-owned references, so an existing instance with
  a different gate schema can still receive the promised comparison.
- [DETAIL] Use separate Makefile and gate starters; the dependency template
  uses the selected source's hash-checked declaration. Both install and probe
  initialize these same starters (F-16), while report compares source-original
  references, so portability measures what an instance receives.
- [DETAIL] Use the installed lock to scope the plan's source-stock/policy
  cases (F-17/F-20); this keeps missing source prerequisites red without
  treating an instance's untracked payload as missing source inventory.
- [DETAIL] Let the probe select a complete temporary candidate snapshot for
  pending-tree measurement, so newly added kit assets are measured before
  the runner stages them; this changes no source Git state or install/report
  commit contract.
- [DETAIL] Distinguish a completed readable comparison (success, even with
  differences) from a refusal or failed verification (failure), so missing
  paths in an existing instance do not themselves make measurement fail.

These reversible details are chosen here with their reasons; none supplies
another maintainer answer.
