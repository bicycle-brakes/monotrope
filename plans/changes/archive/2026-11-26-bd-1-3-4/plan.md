---
title: "Plan — bd-1-3-4"
status: accepted
implementation_status: done
date: 2026-11-14
last_reviewed: 2026-11-26
updated: 2026-11-26
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

- 1: tests/test_beads_install.py::test_wrapper_selects_pinned_versioned_binary — selecting PATH bd, changing arguments or swallowing the child exit code fails.
- 1: tests/test_beads_install.py::test_wrapper_falls_back_to_a_matching_path_binary — with no versioned binary, a pin-matching bd on PATH not dispatched, or its arguments or exit code changed, fails (loop row L1-11).
- 2: tests/test_beads_install.py::test_install_routes_request_canonical_release — either route requesting the old owner or another release fails.
- 3: tests/test_beads_install.py::test_install_routes_install_verified_archive — a valid platform archive failing to produce the versioned binary or overwriting unversioned bd fails.
- 3: tests/test_beads_install.py::test_install_routes_refuse_unverified_archive — missing or wrong expected checksum reaching extraction or install fails.
- 3: tests/test_beads_install.py::test_install_routes_skip_only_an_exact_pinned_binary — either route skipping the download for a versioned binary whose first version line is not exactly `bd version <pin>` (1.3.40, 11.3.4, a release candidate), or re-downloading over the exact pin, fails (loop row L2-4).
- 3: tests/test_beads_install.py::test_committed_checksums_cover_both_platforms — a missing or malformed committed 1.3.4 checksum file for Darwin arm64 or Linux amd64 fails (loop row L1-2).
- 4: tests/test_beads_install.py::test_cloud_pin_and_checksum_match_repository — cloud version or digest diverging from the committed pin and Linux checksum fails.
- 5: tests/test_beads_install.py::test_wrapper_refuses_version_mismatch — mismatched version dispatch, even with the verb bypass set, fails.
- 6: tests/test_beads_install.py::test_wrapper_blocks_schema_verbs — init, migrate or upgrade reaching the binary without the bypass fails.
- 7: tests/test_beads_install.py::test_wrapper_missing_binary_exits_127 — a different status or accepting the repository shim fails.

## Release verification — 2026-11-15

Step 1's evidence, recorded by the orchestrator (Opus subagents) for the pull
request to cite (loop rows L1-1, L1-6, L1-10, L2-1, L2-2 and L2-3; spec,
Definition of Done and "Boundary"). All times UTC, read from git and the
command output.

Chronology (loop row L2-3):

- 2026-11-14 21:51:21 — commit `78d6f738` enters both digest files and the
  cloud `BD_SHA256`, finishing runner attempt 3 by hand; its message says the
  values match the release's `checksums.txt`. No independent hash of the
  archives is recorded at this point: the values entered the repository
  before the independent check below, not after it as step 1 ordered.
- 2026-11-14 23:55 — the archives were downloaded into disposable storage and
  hashed independently (round-1 hand pass); the digests below confirmed the
  committed values. The record was committed in `c60c980d` at 23:59:39.
- 2026-11-15 00:15:26 — downloaded again (`gh release download v1.3.4 -R
  gastownhall/beads`) into a fresh disposable directory and hashed with
  `shasum -a 256`: the same two digests, equal to the release's
  `checksums.txt` and to the committed files (round-2 hand pass).

Archives and digests:

- Source: `https://github.com/gastownhall/beads/releases/download/v1.3.4/`,
  files `checksums.txt`, `beads_1.3.4_darwin_arm64.tar.gz` (48,577,082 bytes)
  and `beads_1.3.4_linux_amd64.tar.gz` (53,448,333 bytes).
  - Darwin arm64: `b08a9c15bff80c42235f32946f94a6566a7d90944fe8afe45f3fd2f350596cdb`
  - Linux amd64: `175c26904bde3ff9168d2282ff6b56f17b17f60c22fa5acb3dacc9fb3465303a`
- Both equal `tools/beads/checksums/beads_1.3.4_darwin_arm64.tar.gz.sha256`,
  `tools/beads/checksums/beads_1.3.4_linux_amd64.tar.gz.sha256` and the
  `BD_SHA256` of `tools/cloud-env/setup.sh`, unchanged since `78d6f738`.

Identity of the release (loop row L2-2), read 2026-11-15:

- The tag `refs/tags/v1.3.4` is the annotated tag object `a60c4c3a` on
  commit `7ef2fd05eb0cd3bdbde051f93cfc14ccf270cdde` (`git ls-remote`). GitHub
  reports the tag object as unsigned and the commit's signature as valid.
- `https://github.com/steveyegge/beads` answers 301 to
  `https://github.com/gastownhall/beads`, and `gh repo view` resolves both
  names to the same repository node id `R_kgDOQAyAEg` (created 2025-10-12):
  a transfer of one repository, not a second repository.
- `gh attestation verify <archive> --repo gastownhall/beads` (gh 2.102.1)
  accepts both archives: one SLSA v1 build-provenance attestation each,
  issuer `https://token.actions.githubusercontent.com`, signer
  `gastownhall/beads/.github/workflows/release.yml@refs/tags/v1.3.4`, source
  commit `7ef2fd05`, run `41804108426`.
- Not verified: a signature on the tag; a statement of the move by the
  project itself; anything independent of GitHub and of the account that
  controls `gastownhall`. The spec names this as a Boundary.

Migrations (loop row L2-1), read 2026-11-15 from `gh release view v1.3.1`
… `v1.3.4 -R gastownhall/beads` and from `CHANGELOG.md` at tag `v1.3.4`
(`raw.githubusercontent.com/gastownhall/beads/v1.3.4/CHANGELOG.md`):

- 1.3.1 (2026-09-30): "There is no schema migration. Upgrading from v1.3.0
  … is a binary swap."
- 1.3.2 (2026-10-24): "There is no schema migration, and the embedded Dolt
  engine is unchanged"; upgrade note: run `bd recompute-blocked` once per
  workspace whose store crossed migration 0059 under 1.3.0 (a data repair,
  not a migration; nothing in 1.3.2 runs it automatically).
- 1.3.3 (2026-11-03): "no new migration file … upgrading from 1.3.x is a
  binary swap"; known issue, unfixed in 1.3.4: do not run `bd compact` or
  `bd flatten` on a clone that adopted migration 0062 by `bd dolt pull` or
  `bd bootstrap`.
- 1.3.4 (2026-11-04): "no new migration file … upgrading from 1.3.x is a
  binary swap"; one fix (`GT_ROOT` from `.beads/.env`).
- The migrations the changelog names (0059, 0061, 0062, 0065, 0066) shipped
  in 1.3.0. Step 1's stop condition does not apply. The two notes are
  tracker-side work outside this change (spec, Protected areas); the pull
  request names them for the maintainer.

## Route and draft checks

Explore used Stage 2, route `flash`, endpoint `glm-coding-plan`, model `glm-5.3-flash`, on 2026-11-14; no Stage-1 fallback is recorded. The class and version/source choice come from `decisions.md#Q-1`. There are no phase-2a review rows in the current findings file. `templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at `5572158a`; use the phase-3 prompt and existing interview, research-handoff and criterion-ledger gates. Registry/index regeneration belongs to the runner outside this draft's allowed paths.

Draft checks on 2026-11-14: `python3 scripts/check_interview_minimums.py --change bd-1-3-4` and `python3 scripts/check_criterion_ledger.py` passed; `python3 scripts/check_research_handoff.py --change bd-1-3-4` passed with the explicit legacy exemption (no research-swarm/v2 evidence). Full `make verify` and the commit remain the runner's work.

## Runner route — 2026-11-14

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-11-14 18:27:47–18:31:32 UTC, 225 s — draft · attempt 1 · route codex · model gpt-6.1-sol · accepted · document checks only, no tests ran; result: green; gates `plans-registry` (block), `docs-links` (report), `frontmatter-current` (block), `dangling-beads` (block), `decision-continuity` (block), `adr-answers` (block), `interview-minimums` (block), `question-context` (block), `criterion-ledger` (block), `research-handoff` (block), `markdownlint` (report); not the full `make verify`; a fresh full `make verify` is still required before phase 6; reported without blocking: `docs-links` exited 1, `markdownlint` exited 1 · measured by the runner
2026-11-14 18:33:47–18:52:29 UTC, 1122 s — implement · attempt 1 · route flash · model glm-5.3-flash · rejected · measured by the runner
2026-11-14 18:52:37–18:59:35 UTC, 418 s — implement · attempt 2 · route flash-repair · model glm-5.3-flash · rejected · measured by the runner
2026-11-14 18:59:59–19:00:50 UTC, 51 s — implement · attempt 3 · route stage-1 · model claude-sonnet-5-5 · rejected · measured by the runner
2026-11-16 06:06:11–07:30:37 UTC, 5066 s — repair · attempt 1 · route codex · model gpt-6.1-sol · accepted · full `make verify` ran (result: green) because the targeted coverage was not safe: `tools/bd` is an input kind the targeted selector does not cover · measured by the runner
