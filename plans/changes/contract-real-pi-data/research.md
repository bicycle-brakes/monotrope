---
title: "Research — contract-real-pi-data"
status: draft
implementation_status: none
date: 2026-11-21
last_reviewed: 2026-11-21
updated: 2026-11-21
supersedes: null
superseded_by: null
bead: coding-harness-z4oo
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-21", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# contract real pi data — Research

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1161 files, 5235 commits, 12 rules.

Stage-2 call, 2026-11-21: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 1161 files, 5247 commits, 12 rules.

Stage-2 call, 2026-11-21: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM 5.3 Flash refused twice with claude-code:unrecognized_model on 2026-11-21 (bead coding-harness-b5pu) · leak check clean over 1161 files, 5251 commits, 12 rules.

## Runner exploration — 2026-11-21

The explorer run for `contract-real-pi-data` is done. I wrote no files; the runner appends this to `research.md`.

**Note for the runner:** the current `research.md` header has no `neighbours:` list, so a swarm run will be refused until one is added. Proposed header, taken from the sources below:
`neighbours: [plans/changes/archive/2026-11-06-pi-catalog-redirect/spec.md, plans/changes/archive/2026-10-07-stage2-mimo/spec.md]`
The `research.md` in the change folder also still says "this file is empty until it has run" and carries three Stage-2 call lines (two failed `unrecognized_model` attempts, then the Haiku fallback). Those are runner records, not findings.

## What exists today

- **The bead's topic, as recorded in the repository.** The 2026-11-01 five-lane handover lists `coding-harness-z4oo` as "contract tests read the pinned Pi's real data — the second finding of one mechanism after xul8 and 4tr4 L7-1" (`docs/journal/handover/2026-11-01-five-lane-night.md`, "Beads opened since 12:55 UTC"). The same handover says the parked fix for `coding-harness-xul8` (the working-directory override does not hold in Pi 1.2.0) waits for "the real-Pi tests" of z4oo (table row E, same file). `docs/research/2026-11-01-night-run-plan.md` ("Not tonight, and why") and `docs/research/2026-11-03-night-run-plan.md` (row C) both name z4oo as the follow-up to the Pi-path and `compaction.enabled=false` work.
- **The decision behind the contract suite.** ADR 0019 (`docs/adr/0019-repository-pinned-pi-and-contract-tests.md`, around its item 4) and the archived change `plans/changes/archive/2026-11-06-pi-pin/` (`decisions.md`) decided that a contract suite runs the real pinned Pi with synthetic credentials and a loopback server, locally and in CI.
- **The test module that reads Pi's data.** `tests/test_pi_contract.py` starts the installed Pi through the repository wrapper. Its helper at the catalog-reading function (near line 707) reads the installed package's shipped data file under `tools/pi/node_modules/@earendil-works/pi-ai/dist/providers/data/`. It fails with "run bash tools/pi/install.sh" if the file is missing or unreadable. A second check (near line 779) reads the installed `package.json` and compares its version against `PI_MOVED_PIN`. The shipped-catalog test (near line 817, `test_real_opencode_provider_contracts` and its neighbours) asserts that each `opencode-go` model is present with the expected `baseUrl`. Its docstring says the evidence is "the installed package's own data file — no live store, no overlay, no…".
- **Per-test overlay.** The same module writes a scratch `models.json` into a scratch agent directory (near lines 561–626) as the override seam for the loopback base. The runner's own `models.json` is checked not to change.
- **The Pi extension driver.** `tests/pi_contract_driver.mjs` is loaded by the installed Pi with `-e` and registers one tool, `contract-echo`. It checks that the installed Pi exposes `registerTool` and sets up a loopback network guard.

## Where it lives

- Tests: `tests/test_pi_contract.py`, `tests/pi_contract_driver.mjs`, and `tests/test_stage2.py` (the truncated-print stand-in that the 2026-11-06 findings flagged, F-8).
- Pinned install: `tools/pi/install.sh`, `tools/pi/pi` (the wrapper), `tools/pi/node_modules/…` (not in git; created by the install).
- Decision: `docs/adr/0019-repository-pinned-pi-and-contract-tests.md`.
- Tracker: bead `coding-harness-z4oo`. I could not read it. My tools are read-only and `tools/bd` is a writing-capable wrapper; the bead's description is not in this report.

## What is unclear

- **The exact scope of "real data".** The handover says "contract tests read the pinned Pi's real data". The current tests read the installed package's shipped catalog file, not a live store, and the findings in `plans/changes/archive/2026-11-06-pi-pin/findings.md` record that some contracts use only a static catalog read (finding 11, "MAJOR narrowing"). Which of these z4oo should change is not stated in any file I read. Not found: a spec, design or decisions file for z4oo. The change folder contains only `research.md`.
- **Which "second finding" mechanism.** The handover calls z4oo the second finding of one mechanism after xul8 and 4tr4 L7-1. The mechanism itself (contract tests passing against a stand-in or a static file while the real Pi behaves differently) is named, but no file I read describes the first finding in full.
- **Whether a live Pi run confirms the current pin.** I did not run the suite (no shell in this phase). The `PI_MOVED_PIN` and the installed version (1.2.0 in the 2026-11-06 findings) are not checked against `tools/pi/install.sh` here.
- **Whether `plans/changes/archive/2026-11-06-pi-pin/spec.md` exists.** My search for the topic matched that folder's `decisions.md`, `design.md`, `findings.md` and `plan.md`, not `spec.md`. A match is not an absence, so I did not state either way. It is the strongest candidate neighbour if it does exist.

## Which files a change would have to touch

- `tests/test_pi_contract.py` (the catalog helper, the version check, the shipped-catalog tests, and the scratch `models.json` seam).
- `tests/pi_contract_driver.mjs` (the extension driver, if the real extension contract changes).
- `tools/pi/install.sh` (only if the pin or the install check changes).
- `docs/adr/0019-repository-pinned-pi-and-contract-tests.md` (only if the contract scope it records changes; that would be a decision, not the explorer's to make).
- `plans/changes/contract-real-pi-data/` (the change folder itself: `research.md`, then `decisions.md`, `spec.md` as later phases require).
