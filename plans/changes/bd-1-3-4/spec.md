---
title: "Spec — bd-1-3-4"
status: draft
implementation_status: none
date: 2026-11-14
last_reviewed: 2026-11-14
updated: 2026-11-14
supersedes: null
superseded_by: null
bead: coding-harness-tr84
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, beads, supply-chain]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — bd-1-3-4

Pin the tracker CLI to stable bd 1.3.4 from `gastownhall/beads`, retaining verified installation and the wrapper's existing protections (bead `coding-harness-tr84` — update the tracker binary). Research: `research.md`; maintainer answer: `decisions.md#Q-1`.

## Problem

- At commit `5572158a` (2026-11-14), `tools/beads/VERSION` pins 1.3.0. The interview records the maintainer's choice of 1.3.4 for the intervening security and data-loss fixes, accepting deferral of 1.4.0 and its migration; those upstream assertions are recorded interview context, not a new measurement by this draft.
- Research identifies two installation routes: `tools/beads/install.sh` reads the pin, while `tools/cloud-env/setup.sh` duplicates the Linux version and checksum. Both still download from `steveyegge/beads`; updating only the primary installer leaves cloud sessions behind.
- Research finds no direct tests of the wrapper's version checks or of agreement between the cloud copy and the pin. Existing checksums cover Darwin arm64 and Linux amd64; 1.3.4 checksums have not been read in this draft.

## Acceptance criteria

1. When the repository wrapper dispatches a normal command with the pinned versioned binary available, it uses bd 1.3.4 ahead of a different bd on PATH and preserves the command's arguments and exit code.
   *Refuted by:* a different release is selected, or arguments or exit status change.
   *Basis:* decisions.md#Q-1; research.md, wrapper resolution.
2. When either installation route downloads bd, its requested release asset is under `https://github.com/gastownhall/beads/releases/download/v1.3.4/`.
   *Refuted by:* either route requests the old owner, another version or another host.
   *Basis:* decisions.md#Q-1; research.md, two installation routes.
3. When installing a downloaded bd archive, each route installs the versioned binary only after its archive matches the committed checksum for that platform.
   *Refuted by:* a matching fixture cannot install, or an archive with a wrong or absent expected checksum reaches extraction or installation; the repository installer must cover Darwin arm64 and Linux amd64, and cloud setup Linux amd64.
   *Basis:* decisions.md#Q-1; research.md, checksum verification and supported assets.
4. When cloud setup is prepared from the repository, its bd version and Linux amd64 checksum agree with the repository pin and its corresponding checksum file.
   *Refuted by:* either duplicated value differs or its referenced checksum file is missing.
   *Basis:* decisions.md#Q-1; research.md, cloud checksum coupling.
5. When the wrapper resolves an executable reporting a version other than the pin, it refuses the requested command with a nonzero status.
   *Refuted by:* a normal command reaches a mismatched binary, including with `BD_PIN_BYPASS=1`.
   *Basis:* research.md, wrapper version refusal.
6. When `init`, `migrate` or `upgrade` is requested without `BD_PIN_BYPASS=1`, the wrapper refuses it before dispatch.
   *Refuted by:* any blocked verb reaches the binary without that explicit bypass.
   *Basis:* research.md, wrapper schema and identity protections.
7. When no eligible executable bd is available, the wrapper exits 127.
   *Refuted by:* it exits with another status or recursively executes the repository's PATH shim.
   *Basis:* research.md, the renderer's missing-binary contract.

## Non-goals

- bd 1.4.0, schema migration, `BD_PIN_BYPASS` use against a real store, tracker mutation and hook reinstallation; a migration needs a separate maintainer decision.
- Changing wrapper policy, renderer normalization, bootstrap behavior, supported platforms, CI hydration or the global unversioned bd.
- Retrospective rewriting of version-bound historical evidence, translation of existing German messages, or redesign of the standalone cloud setup.
- Design phase 2b and an ADR: this is the interviewed `bounded` binary/source update with no architecture change.

## Protected areas

- `.beads/` and real local or remote tracker stores: no migration, hook regeneration or tracker writes belong to the binary update.
- `docs/adr/`, `docs/WORKFLOW.md`, gates, model configuration and harness configuration: their policies do not change.
- Existing 1.3.0 checksum files and historical measurements: retain their evidence without implying it was remeasured on 1.3.4.

## Definition of Done

- `make verify` green after implementation; tests exercise real scripts with isolated binaries and homes, without a shared tracker.
- Same pull request: `tools/cloud-env/README.md` reflects the new binary, checksum path and consistency test; no models or ADRs change.
- The pull request records the authoritative release checksum source and independently computed archive digests for both platforms, with the verification commit; synthetic tests alone do not establish release integrity.
- The pull request's file list demonstrates that protected areas and non-goals are untouched.
- The pull request closes the tracker-binary update (bead `coding-harness-tr84`); its last commit carries `Closes-Bead: coding-harness-tr84`.

## Open decisions

None open. The maintainer's version and repository choice is recorded in `decisions.md#Q-1`; it is not answered again here.

- [DETAIL] Update both installation routes and their current cloud documentation together, because they deliver the same pinned binary and otherwise drift.
- [DETAIL] Leave `tools/bd` unchanged unless a demonstrated compatibility fault requires revisiting this scope: it already reads the pin dynamically, so tests establish the new selection without a redundant version literal.
- [DETAIL] Use two hours of phase 4 including repairs as a stopping limit, because this is a bounded pin/source update; stop and report if release verification contradicts the interview's no-migration premise.
- [DETAIL] Use the phase-3 prompt's plan form: this tree has no `templates/plan.md` or `scripts/validate_change_artefacts.py`; the runner owns derived-file regeneration and available document gates.
