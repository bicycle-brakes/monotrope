---
title: "Plan — pi-pin"
status: draft
implementation_status: none
date: 2026-10-15
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-agx
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage2, pi]
---

# Plan — pi-pin

```text
For you:     Global Pi updates stop breaking the runner; every runner Pi uses one locked repository install.
Done when:   Real-Pi offline contracts pass locally and in CI, all 14 criteria have evidence, and make verify is green.
Appetite:    8 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     Automatic updates, live provider probes, paid Zen enablement or new confinement rules.
Pre-mortem:  suppose it failed: most likely because the contract harness imitates Pi instead of exercising its real tool exchange.
Starts unless you say stop.
```

Implements `spec.md`; `design.md` chooses manifest-derived pins and direct local
execution. The interview's six answers stand; only the maintainer's merge adopts
the new ADR. This draft neither records an ADR answer nor starts phase 4.

## Steps and files

1. **Establish the local toolchain.** Create `tools/pi/package.json` as a private
   npm project with exact `@earendil-works/pi-coding-agent: "1.2.0"`; generate
   `tools/pi/package-lock.json` with npm, preserving integrity values. Create
   `tools/pi/.node-version` with `26.9.0`; derive major 26 from that file.
   Inspect the installed package's engines, bin metadata, extension examples,
   provider defaults and CLI output before writing the real contracts. These
   candidates are not measured yet; stop/report incompatible requirements or
   failed contracts, never change a human decision or weaken the contracts.
2. Create executable `tools/pi/install.sh`: resolve its own directory, require
   the declared Node major and npm, and run `npm ci --ignore-scripts` there,
   failing on install errors. Create executable `tools/pi/pi`: resolve its own
   directory, validate Node major and installed package version against the
   manifest, then exec Node with that package's declared local bin and the
   original arguments. Refuse missing/malformed metadata, mismatched versions,
   absent files and failed version checks with setup guidance; never install,
   use `npx`, fall back to PATH Pi or change caller cwd/auth. Add only
   `tools/pi/node_modules/` to `.gitignore`.
3. In `scripts/stage2.py`, derive `PI_VERSION` from the manifest, introduce one
   repository-root wrapper path and use it in `require_pi()` and `run_reviewer()`.
   Keep bounded keyless scratch preflight and its exact-output check. In
   `scripts/stage2_session.py`, resolve that same path for Pi only, including
   confirm-load and Terminal argv; Codex/osascript lookup stays as today.
   Preserve reviewer flags, settings, retry/timeout handling, leak/declaration
   order, scrubbed diagnostics and interactive sign-in through `~/.pi/agent`.
4. Create `tests/test_pi_install.py` for installer/wrapper success and failure,
   using synthetic Node/npm/local-CLI executables and a hostile PATH Pi marker.
   Exercise lock mismatch, corrupt integrity and lifecycle-script denial with
   local fixture packages, not a second registry fetch. In `tests/test_stage2.py`
   and `tests/test_stage2_session.py`, adapt fake trees to include local wrapper
   metadata/stand-ins; preserve existing ledger-referenced test names. Add
   explicit path assertions for loop, probe, preflight, confirm-load and Terminal
   dispatch. Replace the hard-coded 1.1.0 assertion with source-of-pin validation;
   update current doctrine expectations while retaining dated historical claims.
5. Create `tests/test_pi_contract.py` with a bounded loopback HTTP/SSE stand-in
   that serves deterministic OpenAI-compatible tool-call/stop/error responses
   to the actual installed Pi via the wrapper. Use fresh scratch HOME and agent
   directories, synthetic keys and controlled project fixtures; prerequisites
   are mandatory assertions, never skip/xfail. Capture model requests and tool
   results, enforce finite turns/timeouts and kill/reap children on failure.
   Exercise production reviewer launch construction, injecting only test transport
   configuration and the network guard at the subprocess seam; do not maintain
   a second handwritten isolation-flag list that could drift from the runner.
   Create `tests/pi_contract_driver.mjs` for real extension/tool registration,
   exercising the installed API's input and result contracts rather than a mock
   API. Create `tests/pi_network_guard.mjs` as a test-only preload denying
   non-loopback HTTP/HTTPS, fetch, net and TLS connections; prove its denial with
   planted attempts, not an actual outbound request. Never preload it in production.
6. Contracts must cover: exact four reviewer tools and rejected foreign tools;
   positive control read/search execution; ambient discovery/config traps with
   positive activation controls; custom-tool structured input/result; production
   session-policy flag plus allowed read, outside read and symlink refusal;
   real model-list table with both providers and synthetic credentials; native
   Go/Zen base URLs inspected independently from a scratch local transport
   override, and each provider's request carrying only the synthetic
   `OPENCODE_API_KEY`. No arbitrary hosted response or real key is needed.
   Also verify the runner rejects Pi 1.2.0's nonzero truncated-print result.
   Keep existing mocked policy cases in `tests/test_stage2_session_policy.py`
   and `tests/stage2_session_policy_driver.mjs` unchanged: the real suite adds
   integration evidence, not a policy redesign.
7. In `scripts/ci_gates.py`, extend toolchain provisioning with exact Node setup
   from `tools/pi/.node-version` and `bash tools/pi/install.sh` before any job
   runs pytest. Add `tests/test_ci.py` assertions for ordering, exact runtime,
   common installer and failure propagation. Regenerate `.github/workflows/ci.yml`
   with the command below; no new gate is needed because pytest already runs
   contracts. Keep `decisions/gates.yaml` and the Python matrix unchanged.
8. Create `tools/pi/README.md` with prerequisites, fresh-clone install, verification,
   offline-test versus registry-install distinction, and version-update procedure:
   change manifest/Node pin as needed, regenerate lock, install, run real contracts
   and verification, propose a PR. Update `docs/WORKFLOW.md` current Pi setup/pin
   paragraphs and `model-endpoints.yaml`'s Pi remark to reference the manifest
   rather than a duplicated version literal. Update the two dated dependency
   comments in `scripts/stage2_session_policy.mjs` to distinguish original
   measurement from current contract coverage; policy behaviour stays unchanged.
   The one new ADR is `docs/adr/0019-repository-pinned-pi-and-contract-tests.md`;
   preserve it as a merge-effective proposal, renumbering its claim/references
   only if another ADR takes that number before merge.

Two files not planned at first are named here after the phase-6 review.
`scripts/kit/probe.py` gains a `REIST_NICHT` entry and its `DECKEL` cap rises from
38 to 39: `tests/test_ci.py::test_real_pi_is_provisioned_before_contracts` reads
`tools/pi/.node-version`, which the kit does not carry, so the missing file maps
to `braucht-die-vollstaendige-suite`, and the list may only grow with a visible
cap raise. `decisions/gates.yaml` (step 7 said unchanged) now excludes
`tools/pi/node_modules` from the markdownlint globs, so third-party Markdown does
not bury this change's own findings; `.github/workflows/ci.yml` is regenerated
for it. `scripts/ci_gates.py` emits the Node and Pi steps only when `tools/pi/`
exists in the repository it generates for, since the kit leaves `tools/` behind.

No other implementation files are planned; all created/changed files are named
above. The orchestrator owns generated `plans/INDEX.md` refresh and recording the
maintainer's already-stated ADR answer through the normal harness command before
full gates; this draft does neither. Existing change artifacts may receive phase
status/evidence updates through the runner's normal lifecycle.

## Criterion ledger

- 1: tests/test_pi_install.py::test_install_obeys_lock_integrity_and_disables_scripts — changed graph, corrupt integrity or lifecycle sentinel accepted
- 2: tests/test_pi_install.py::test_wrapper_ignores_global_pi_from_any_cwd — hostile PATH Pi runs
- 3: tests/test_pi_install.py::test_wrapper_refuses_unusable_local_pi — missing/mismatched/broken Pi launches, installs or falls back
- 4: tests/test_pi_install.py::test_wrapper_checks_node_major — wrong major starts Pi or same-major patch is refused
- 5: tests/test_stage2.py::test_loop_and_probe_use_repository_pi — preflight/reviewer argv resolves global Pi
- 5: tests/test_stage2_session.py::test_all_session_pi_launches_use_repository_wrapper — confirmation or Terminal argv bypasses wrapper
- 6: tests/test_pi_contract.py::test_real_reviewer_tool_contract — extra tool declared or forbidden call executes
- 7: tests/test_pi_contract.py::test_real_reviewer_ignores_discovery_traps — an armed trap affects the clean reviewer call
- 8: tests/test_pi_contract.py::test_real_extension_tool_input_and_result — changed execute signature loses input or result
- 9: tests/test_pi_contract.py::test_real_session_policy_blocks_foreign_reads — outside/symlink sentinel appears or positive read fails
- 10: tests/test_pi_contract.py::test_real_model_listing_is_a_provider_table — JSON assumption or missing Go/Zen provider passes
- 11: tests/test_pi_contract.py::test_real_opencode_provider_contracts — wrong native address/key mapping passes
- 11: tests/test_pi_contract.py::test_contract_network_guard_denies_external_destinations — external destination accepted by test transport
- 12: tests/test_pi_contract.py::test_contract_prerequisites_and_failures_are_mandatory — absent runtime, timeout or malformed exchange becomes skip/success
- 12: tests/test_ci.py::test_real_pi_is_provisioned_before_contracts — CI omits exact Node, shared installer or failure propagation
- 13: tests/test_stage2.py::test_each_call_runs_its_own_leak_check — a request starts without its leak check
- 13: tests/test_stage2.py::test_no_call_carries_another_endpoints_key — foreign environment includes another key
- 13: tests/test_stage2.py::test_the_opencode_key_never_leaves_the_runner — key reaches argv/output/records
- 13: tests/test_stage2_session.py::test_the_pi_session_hands_over_no_key_and_writes_no_credential — session copies auth or injects runner keys
- 13: tests/test_stage2.py::test_truncated_pi_print_failure_is_refused — nonzero truncated answer accepted
- 13: tests/test_pi_contract.py::test_real_truncated_pi_print_failure_is_refused — real Pi's truncated answer accepted
- 10: tests/test_pi_contract.py::test_contract_environment_excludes_parent_provider_keys — a parent provider key reaches real Pi
- 2: tests/test_stage2.py::test_pi_wrapper_is_repository_local — the runner's wrapper path points anywhere but tools/pi/pi
- 14: not a test — phase-6 review and PR file list check current documentation, unchanged historical ADRs, the new amendment and absence of Zen enablement; stale guidance or an unsupported confinement/live-Zen claim refutes it

## Verification

Run from the repository root, after the runner/orchestrator supplies the normal
tracker render and the maintainer's stated ADR answer. Setup may download npm
packages; the contract executions use no external network or model credentials.

```sh
make venv
bash tools/pi/install.sh
.venv/bin/python3 -m pytest tests/test_pi_install.py tests/test_pi_contract.py tests/test_stage2.py tests/test_stage2_session.py tests/test_ci.py -q
.venv/bin/python3 scripts/ci_gates.py --generate-ci > .github/workflows/ci.yml
.venv/bin/python3 scripts/check_interview_minimums.py --change pi-pin
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/plans_registry.py --check
make verify
git diff --check
```

`validate_change_artefacts.py` and a plan template are absent at baseline
`40934c1` (2026-10-15); use the present interview, registry and ledger checks,
without adding a validator to this change. Do not claim full gates green while
an answer, index refresh, installation or tracker measurement is outstanding.
The runner owns verification/commit; this drafting call makes no commit.

## Boundaries and route

Do not touch existing ADRs, human answer records, policy logic, customer files,
user configuration, leak-check rules, `.claude/settings.json`, decision-continuity
maps, endpoint permissions or ladder/model choices. The kit manifest's existing
`tools/`, `scripts/`, `tests/` catch-alls already classify additions; no kit policy
change is included. No live session/provider probe is planned.

Explore used Stage 2 on 2026-10-15, attempt 1, route `flash`, endpoint
`glm-coding-plan`, model `glm-5.3-flash`; research records no Stage-1 fallback.

## Runner route — 2026-10-15

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Runner route — 2026-10-15

Stage-1 route: repair · model claude-sonnet-5-5 · reason: two Codex post-run checks failed.

## Time used

2026-10-15 — phase-4 repair after the runner's third failed attempt, measured with `date` on the writer machine: 16:03 (phase-4 start) to 17:56 (this commit) = 1 h 53 min. Spent on the executable bits, the npm-generated lock file, the pinned install, three contract assertions repaired against the installed Pi 1.2.0, the ledger and one `make verify`; appetite 8 h of phase 4, not reached.

2026-10-15 — phase-6 repair round 1, completed by the orchestrating session after the runner's repair failed three times: 20:40 (findings commit 5dfbf31) to 22:31 (this commit) = 1 h 51 min.
