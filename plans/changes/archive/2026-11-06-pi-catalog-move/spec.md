---
title: "Spec — pi-catalog-move"
status: accepted
implementation_status: done
date: 2026-11-04
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-vku6
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-04"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, pi, model-catalog]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — pi-catalog-move

Move the repository's pinned Pi to 1.5.0 so its shipped Go catalog contains
the models needed for a separately decided admission, with the existing
offline contracts still holding (bead `coding-harness-vku6`). Research:
`research.md`; the maintainer settled what “move” means in `decisions.md#Q-1`.

## Problem

The research read Pi 1.2.0 in `tools/pi/package.json` and found that both
catalog acquisition paths and the real-runtime contracts depend on that
repository-local install (`research.md`, “What exists today”, 2026-11-04).
Its proposed registry/source moves were unresolved readings, not requirements.
The interview resolves them: the shipped 1.2.0 Go catalog lacks
`kimi-k3.1-pro`, `minimax-m3.1-flash` and `step-5-preview`, blocking their
contract-backed admission; the recorded package reading places all three in
Pi 1.5.0 (`decisions.md#Q-1`, 2026-11-04).

At baseline `c7886ea5` (2026-11-04), the manifest and installed Pi still say
1.2.0, and `test_real_opencode_provider_contracts` in
`tests/test_pi_contract.py` expects the old shipped Go base
`https://opencode.ai/zen/go/v1`. The interview records the new shipped
Chat Completions and Messages bases. Updating the dependency alone therefore
needs both catalog evidence and preserved behavioral contracts; a catalog
entry by itself grants no permission to call its model.

## Acceptance criteria

1. When the repository-local Pi is installed from the committed manifest and lock, the manifest, locked dependency graph and running wrapper agree on exactly `@earendil-works/pi-coding-agent` 1.5.0.
   *Refuted by:* a floating or different manifest dependency, a mismatched lock or installed package, a failed clean install, or a wrapper reporting another version.
   *Basis:* `decisions.md#Q-1`.

2. When the installed Pi's shipped `opencode-go` catalog is inspected offline, each of `kimi-k3.1-pro`, `minimax-m3.1-flash` and `step-5-preview` is present as an `openai-completions` model at `https://opencode.ai/inference/go/openai/v1`.
   *Refuted by:* any named id being absent, filed under another wire API, or carrying another base; a synthetic overlay or live refresh cannot supply this evidence.
   *Basis:* `decisions.md#Q-1`.

3. When the installed Pi's shipped `opencode-go` Messages entries are inspected offline, `qwen3.8-flash`, `qwen3.8-max`, `qwen3.7-plus` and `minimax-m3` each carry the `anthropic-messages` API and base `https://opencode.ai/inference/go/anthropic`.
   *Refuted by:* any named entry being absent or carrying another API or base; this is catalog evidence for the follow-up, not a measured Messages exchange or admission.
   *Basis:* `decisions.md#Q-1`.

4. When the existing offline Pi installation, real-runtime and research-catalog contract suites run against 1.5.0, their behavioral guarantees continue to pass as mandatory checks.
   *Refuted by:* a failing, skipped or weakened contract for local-install enforcement, tool/configuration isolation, credential handling, session policy, provider exchange, refreshed-definition activation, fresh catalog acquisition or redirect refusal; native Go address expectations may reflect the recorded new shipped base without weakening those guarantees.
   *Basis:* `decisions.md#Q-1`; `research.md`, “Tests that hold the catalog today”.
5. When the forced catalog refresh lists an id that the `opencode-go` entry declares as paid in `modelle` and that also matches the `free_stage` rule (suffix or include), the free selection leaves it out, and `prepare-loop` proceeds with the remaining free candidates instead of refusing.
   *Refuted by:* a free selection that contains a declared paid id, or a preparation that stops with "is a paid model; the free class does not admit it" for such an id.
   *Basis:* `decisions.md#Q-2`; measured 2026-11-04: with Pi 1.5.0, `prepare-loop pi-catalog-move` refused `beam-free`.

## Non-goals

- Admitting or calling new Go models, measuring the Messages wire API, changing
  model terms, routing, review membership or the shared Go address record;
  those return in the separate model-admission decision pull request.
- A central model registry, a catalog-source or host move, redirect-policy
  changes, new retries, stale-cache fallback, or a Node/toolchain upgrade.
- Repairing unrelated runtime regressions or redesigning the contract harness
  to accommodate the candidate. A failed contract is evidence to investigate
  or report, not permission to relax the contract.

Phase 2b does not run for this `bounded` version move; no design or ADR is due.

## Protected areas

- `model-endpoints.yaml`, `scripts/` and other change folders: admission,
  address policy, catalog acquisition and runtime behavior remain their own work —
  with one exception decided in `decisions.md#Q-2`: the free selection in
  `scripts/stage2.py` drops every id the `opencode-go` entry declares as paid
  (criterion 5), with its test in `tests/test_stage2_availability.py`.
- `tools/pi/.node-version`, `tools/pi/install.sh` and `tools/pi/pi`: keep the
  declared Node major, lifecycle-script denial and local-only execution contract.
- `docs/adr/`, `decisions/`, `provenance.yaml`, agent configuration, prompts,
  templates and CI configuration: no governance or architecture change is needed.
- Historical measurements and dated package-version statements: retain their
  dates and meaning; only a present-tense pin claim may be made version-neutral.

## Definition of Done

- Criteria 1–5 have evidence against the installed 1.5.0, with `make verify`
  green; the pull request names the tested commit and install/contract results.
- Moved in the same pull request: `tools/pi/package.json`, its npm-generated
  `package-lock.json`, `tests/test_pi_contract.py`, the current pin wording
  in `docs/WORKFLOW.md`, and the free-selection exclusion of criterion 5 in
  `scripts/stage2.py` with its test; no model declaration or ADR changes.
- The pull request's file list shows the protected areas untouched and the
  non-goals unbuilt; generated `plans/INDEX.md` is the runner's responsibility.
- The pull request closes the pinned-catalog upgrade task
  (`coding-harness-vku6`); its last commit carries
  `Closes-Bead: coding-harness-vku6`.
- No live provider probe is required; npm installation is distinct from the
  offline contract runs. No successful 1.5.0 install or test is claimed here.

## Open decisions

None open. The maintainer chose 1.5.0 and named 1.4.0 as the fallback if its
contracts fail (`decisions.md#Q-1`); that contingency is not a successful
completion of this spec's selected 1.5.0 target. Preserve failure evidence and
report the fallback separately rather than silently rewriting the criteria.

- [DETAIL] Use two hours for phase 4, repairs included, as a stop: the work is
  a locked dependency move and focused contract adaptation, not runtime repair.
- [DETAIL] Assert shipped catalog data separately from synthetic transport
  fixtures so the new addresses are measured without changing the existing
  same-host move tests' starting points.
- [DETAIL] Keep `neighbours: []`: phase 1 used the single Flash explorer, not a
  complete research-swarm run; its proposed neighbours do not create a swarm
  handoff obligation.
