---
title: "Plan — bd-1-3-4"
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
tags: [plan, beads, supply-chain]
---

# Plan — bd-1-3-4

```text
For you:     Local and cloud tracker installations use stable bd 1.3.4 from gastownhall/beads with the existing protections.
Done when:   Both release archives are checksum-verified, isolated installation and wrapper tests pass, and make verify is green.
Appetite:    2 hours of phase 4, repairs included — stop at the limit.
Not now:     bd 1.4.0, schema migration, tracker writes, hook regeneration or wrapper policy changes.
Pre-mortem:  suppose it failed: most likely because the standalone cloud copy kept an old version or checksum.
Starts unless you say stop.
```

## Files and sequence

1. Verify the official `gastownhall/beads` v1.3.4 release metadata and published SHA-256 values for `beads_1.3.4_darwin_arm64.tar.gz` and `beads_1.3.4_linux_amd64.tar.gz`; download both to disposable storage and independently hash them before trusting either value. Record source URLs, date, digests and verification commit in the PR. Never infer hashes from version strings or from test fixtures. Stop if the release requires a migration or cannot be authenticated; do not open the shared store to find out.
2. Create `tests/test_beads_install.py` with the ledger tests below, then update `tools/beads/VERSION` to `1.3.4`, create `tools/beads/checksums/beads_1.3.4_darwin_arm64.tar.gz.sha256` and `tools/beads/checksums/beads_1.3.4_linux_amd64.tar.gz.sha256` from the verified values, and change only the release owner in `tools/beads/install.sh`.
3. Change `tools/cloud-env/setup.sh` to the same version, verified Linux digest, updated checksum-path comment and canonical release owner. Update `tools/cloud-env/README.md` to name 1.3.4 and its checksum file, replacing the obsolete assertion that no consistency check exists with the new test reference; keep historical test dates intact.
4. In `plans/changes/bd-1-3-4/plan.md`, replace each `not yet written` marker as its test is defined. The runner owns measured `Time used` entries, `plans/changes/bd-1-3-4/findings.md` call evidence and regeneration of `plans/INDEX.md`; this draft changes none of those derived records. No files are deleted and no design or ADR is due.

## Test construction and boundaries

Copy the real scripts and pin into a disposable repository layout; run them under a temporary HOME and controlled PATH. Parameterize installer cases for Darwin arm64, Linux amd64 and the standalone cloud route. A recording curl stand-in supplies local executable-bd tarballs and records the requested URL; use actual archive hashes and extraction tools. Stub uname for the platform cases and provide the appropriate hash command on the test host. In the test copy only, redirect cloud's hardcoded `/home/user` paths to an empty temporary root, and stub unrelated cloud commands; never execute setup against real repositories or the person's home.

The success cases assert the versioned destination and a preserved sentinel at the unversioned bd path. Corrupt/missing-checksum cases assert no extraction or install occurs; cloud's current overall exit-0 convention is not changed. The cloud consistency test reads the real tracked declarations and verifies the pin plus the Linux digest, so independently valid but divergent installs go red. Wrapper cases run its real dynamic-pin logic with recording stand-in binaries, preserving argument boundaries and child status; cover mismatched versioned and PATH binaries, blocked verbs, missing executables and rejection of the repository shim. Only temporary fixtures may set `BD_PIN_BYPASS=1`, to prove it cannot bypass the version check.

No production change is planned for `tools/bd`: the pin file already drives it. Do not touch CI, hooks, renderer scripts, historical research, old checksum files, ADRs or held paths. If a held-path change becomes necessary, stop the attempt and assign it to the orchestrator as a bootstrap edit after an accepted attempt; none is currently planned. Do not install binaries into the real home or run bootstrap, migration or tracker commands as a smoke test; release-archive verification and isolated script tests are the evidence for this change.

## Verification

```sh
bash -n tools/bd tools/beads/install.sh tools/cloud-env/setup.sh
.venv/bin/python3 -m ruff check tests/test_beads_install.py
.venv/bin/python3 -m ruff format --check tests/test_beads_install.py
.venv/bin/python3 -m pytest tests/test_beads_install.py -q
make verify
```

The orchestrator supplies the release-verification evidence before completion. `make verify` remains the final gate; the focused script tests do not replace it.

## Criterion ledger

- 1: not yet written tests/test_beads_install.py::test_wrapper_selects_pinned_versioned_binary — selecting PATH bd, changing arguments or swallowing the child exit code fails.
- 2: not yet written tests/test_beads_install.py::test_install_routes_request_canonical_release — either route requesting the old owner or another release fails.
- 3: not yet written tests/test_beads_install.py::test_install_routes_install_verified_archive — a valid platform archive failing to produce the versioned binary or overwriting unversioned bd fails.
- 3: not yet written tests/test_beads_install.py::test_install_routes_refuse_unverified_archive — missing or wrong expected checksum reaching extraction or install fails.
- 4: not yet written tests/test_beads_install.py::test_cloud_pin_and_checksum_match_repository — cloud version or digest diverging from the committed pin and Linux checksum fails.
- 5: not yet written tests/test_beads_install.py::test_wrapper_refuses_version_mismatch — mismatched version dispatch, even with the verb bypass set, fails.
- 6: not yet written tests/test_beads_install.py::test_wrapper_blocks_schema_verbs — init, migrate or upgrade reaching the binary without the bypass fails.
- 7: not yet written tests/test_beads_install.py::test_wrapper_missing_binary_exits_127 — a different status or accepting the repository shim fails.

## Route and draft checks

Explore used Stage 2, route `flash`, endpoint `glm-coding-plan`, model `glm-5.3-flash`, on 2026-11-14; no Stage-1 fallback is recorded. The class and version/source choice come from `decisions.md#Q-1`. There are no phase-2a review rows in the current findings file. `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at `5572158a`; use the phase-3 prompt and existing interview, research-handoff and criterion-ledger gates. Registry/index regeneration belongs to the runner outside this draft's allowed paths.

Draft checks on 2026-11-14: `python3 scripts/check_interview_minimums.py --change bd-1-3-4` and `python3 scripts/check_criterion_ledger.py` passed; `python3 scripts/check_research_handoff.py --change bd-1-3-4` passed with the explicit legacy exemption (no research-swarm/v2 evidence). Full `make verify` and the commit remain the runner's work.

## Time used

2026-11-14 18:27:47–18:31:32 UTC, 225 s — draft · attempt 1 · route codex · model gpt-6.1-sol · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
