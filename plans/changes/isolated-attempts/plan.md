---
title: "Plan — isolated-attempts"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-s9r
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, isolation, containers]
---

# Plan — isolated-attempts

```text
For you:     Every automatic writing attempt and interactive session runs in a fresh container; failed attempts leave only diagnostics.
Done when:   The live Podman boundary probes, retry/publication tests and make verify pass.
Appetite:    24 h of phase 4, repair rounds included; a stop, not an estimate.
Not now:     Containerising read-only reviews, native Windows session dispatch or a cluster runner.
Pre-mortem:  suppose it failed: most likely because an official CLI login cannot work within the selected API-only network boundary.
Starts unless you say stop.
```

Implements [spec.md](spec.md). The architecture below carries what phase 4
needs from design: fresh private volumes, one selected login, enforced API
egress, a separate verifier and validated publication. No implementation or
live boundary measurement is claimed by this draft.

## Steps and files

1. **Qualify setup before enabling a writing call.** Create
   `tools/stage2/Containerfile` with non-root model/verifier targets and
   `tools/stage2/runtime.lock.yaml` with measured immutable image/base
   identities, official Codex/Claude Code/Pi package pins/hashes and the
   Python/toolchain from `requirements-ci.txt`; do not invent pins or install
   packages during an attempt. Create `tools/stage2/README.md` with explicit
   Podman setup for macOS, Linux and Windows through WSL, backend selection,
   selected-login preparation, qualification, cleanup and refusal remedies.
   In `model-endpoints.yaml`, add exact `api_hosts` to the four used endpoint
   entries (`openai-codex`, `claude-code-plan`, `glm-coding-plan`,
   `opencode-go`) without changing their permissions, models or billing.
   Qualify the subscription clients' login export/API hosts using the official
   clients; known GLM/OpenCode addresses are `api.z.ai`/`opencode.ai`, while
   Codex/Claude profiles need measurement. A missing safe profile stops;
   sign-in/telemetry sites and token-billed substitutes are not added to make
   authentication work. Copy only the selected current login into a temporary
   secret input; never mount a host home, full sign-in directory, keychain or
   credential socket. Create `tests/test_model_endpoints.py` cases within the
   existing file for missing, wildcard, IP and unauthorized host profiles.
2. **Create the shared supervisor** in `scripts/stage2_attempt.py` and its
   behavioural tests in `tests/test_stage2_attempt.py`. Select
   `STAGE2_CONTAINER_PROGRAM` (default `podman`, or `docker`/`container`, also
   explicit paths with those basenames) through argument vectors; each adapter
   implements volume/network creation, launch, stop, safe export and removal
   with equivalent capabilities. Freeze the input baseline before model
   execution, build an explicit phase input manifest and populate fresh runtime
   volumes without host-directory mounts. Draft needs its change, templates,
   phase prompts, governance and runner/test sources; other writers need the
   repository inputs for their code/gates. Omit host ignored state and live
   tracker data; obtain only the required fresh render through
   `scripts/bead_render.py`, and include it in the outgoing leak scan.
   Construct independent Git history/refs for baseline and `origin/main`
   without hard links, alternates, source hooks/configuration or credential
   helpers; mount the worker's private Git metadata read-only.
3. **Enforce and probe egress.** Create `scripts/stage2_egress.py` and
   `tests/test_stage2_egress.py`. Run a trusted proxy attached to private and
   outbound networks, with the model attached only to the private network.
   Permit only canonical declared API hosts on HTTPS port 443; validate
   CONNECT/TLS names, reject uninspectable names, IP/wildcard destinations,
   private/local addresses and host changes. Disable direct external DNS,
   IPv4/IPv6 routes, published ports, host networking, devices and engine
   sockets. Proxy environment settings do not count as enforcement. Both
   roles use a read-only system image, non-root user, no extra capabilities
   or privilege escalation, and only owned writable volumes/tmpfs. Refuse
   unsupported adapters, missing images/logins or failed live qualification
   before any writing launch; Stage 1 follows the same refusal.
4. **Run and validate candidates privately.** Adapt `scripts/stage2.py` at
   both `run_attempts` and the separate `draft` loop to use the supervisor,
   preserving route/model/effort/client-pin/fallback contracts in the spec.
   Run declaration and leak checks on the exact prompt and passed payload
   immediately before each call. Retries reconstruct the original baseline
   with accumulated scrubbed evidence/route metadata, rather than restoring
   paths in the model's old tree. Stop the writer before inspecting its
   result. A fresh verifier has no model authentication and no network;
   rebuild its Git metadata from trusted inputs, stage the candidate privately
   and run derived stamps/index, ruff safe fixes/format, `make verify`, time
   checks and baseline-red/candidate-green repair proofs there. Keep the
   draft's single missing-ADR-answer tolerance, whole-change one-ADR rule,
   input answers and existing status forms. Capture model and runner-derived
   path lists separately; preserve audits and quoted diagnostics on the host,
   discard failed statuses/trees, and never import candidate code on the host.
   Extend `tests/test_stage2.py` for all three verbs and failure points; keep
   existing top-level names referenced by other ledgers, updating obsolete
   failed-tree assertions with a comment identifying ADR 0018, without
   rewriting old change criteria to obtain a green gate.
5. **Publish and recover through the supervisor.** Read stopped output with a
   trusted exporter into a typed relative delta; reject escaping/duplicate
   paths, aliased parents, symlinks/hard links, special files and file-to-
   directory replacements before host mutation. Allow ordinary new nested
   directories/files and explicit deletions. Never extract an untrusted
   archive onto the host. Scan every exported file/diagnostic for selected
   credential values/fragments before host storage and after verification.
   Enforce draft path allowances; compare result hashes with verified bytes.
   Under an invocation lock compare host HEAD, index, worktree and permitted
   evidence with their expected state; refuse intervening changes. Journal
   old bytes/index and each owned write, materialise without following links,
   and undo only still-matching owned writes if publication/checkpoint fails.
   Disable hooks and candidate-triggered external filters in host Git;
   automatic verbs keep exactly one checkpoint, with no unverified files.
   Invocation state records ID, baseline/input/image/policy hashes, resource
   IDs, phase, owned-write journal and scrubbed diagnostics, never login
   values. Label resources per invocation, reconcile interrupted publication
   and clean only still-owned resource IDs on exit/next startup; never prune
   globally or rewrite unrelated refs. A cleanup error remains visible and
   blocks a claim of completed cleanup.
6. **Supervise the interactive lifetime.** Change `scripts/stage2_session.py`
   so macOS Terminal starts a trusted supervisor with an opaque invocation
   ID, not a direct host CLI or a command carrying prompt/login contents.
   Preserve the declared model, handover/two launch scans, interactive
   Codex/Pi transport, discovery restrictions, context and Pi policy loading
   inside the qualified image. Dispatch acceptance is only acceptance; normal
   exit invokes the private checks/publication and returns an uncommitted
   delta, while cancellation/failure discards it. Do not demand an automatic
   implement/repair time entry from `session`. Extend
   `tests/test_stage2_session.py` for attached execution, accepted dispatch
   followed by CLI/check failure, normal verified exit, cancellation and
   cleanup; preserve the existing policy tests and policy source unchanged.
7. **Measure the real boundary and keep it measured.** Create
   `scripts/check_stage2_isolation.py` and `tests/test_stage2_isolation.py`.
   The command builds locked images only when explicitly requested, then
   exercises the production supervisor/adapters with local test programs and
   synthetic login data, without a paid model call. Opt-in live tests must
   fail, never skip, when invoked by this command without prerequisites.
   Probe host/home/Git sentinels through file and shell paths, host writes,
   selected versus unrelated credentials, positive approved-API reachability
   and denied proxy/direct/DNS/IPv6/gateway paths, retry separation, verifier
   isolation, cleanup and killed-supervisor recovery. Write a scrubbed report
   with commit, platform, runtime version, image/policy hashes and every
   required outcome; qualify each endpoint profile before its real call.
   Cache only for matching runtime/image/policy/platform identities. Add the
   hosted blocking `stage2-isolation` gate to `decisions/gates.yaml` with
   command `python3 scripts/check_stage2_isolation.py --program podman --build`;
   change `scripts/ci_gates.py` to prepare rootless Podman for that hosted
   gate, and regenerate `.github/workflows/ci.yml` using
   `python3 scripts/ci_gates.py --generate-ci`. Extend `tests/test_ci.py` for
   its preparation/generation and absence of paid-model credentials. The
   normal local suite retains stand-ins; actual macOS and Linux reports are
   separate mandatory completion evidence, not inferred from skipped tests.
8. **Move doctrine and evidence with the code.** Update `AGENTS.md` concisely,
   `docs/WORKFLOW.md` at isolation/draft/repair/session and
   `prompts/04-implement.md` to explain private candidates, failed-tree
   disposal, API/login refusals and verified session return; keep read-only
   calls' remaining limitations explicit. Carry the one new draft
   `docs/adr/0018-isolated-writing-attempts.md` through review without
   editing older ADR bodies or the continuity map. In
   `plans/changes/isolated-attempts/plan.md`, replace `not yet written` only
   when the named test exists and add measured phase-4 time under `Time used`;
   `plans/changes/isolated-attempts/findings.md` holds runner/review evidence
   and links to live report identities. The existing renderer updates
   `plans/INDEX.md` only as part of a successful candidate. No files are
   deleted; no dependency-lock change outside the new runtime lock is planned.

The draft's `plans/changes/isolated-attempts/spec.md` fixes the 24 criteria,
`plans/changes/isolated-attempts/design.md` records the proposed boundaries,
and `plans/changes/isolated-attempts/research.md` adds the dated repository-gap
checks; implementation does not change their intent to satisfy a gate.

Stop at the 24-hour phase-4 appetite with a written resumption state; a missing
runtime, unsupported official login or unmeasured boundary is unfinished work,
not permission for a broader mount/network. This draft installs nothing.

The orchestrator opens the decision PR from
`.github/PULL_REQUEST_TEMPLATE/decision.md`, titled
`decide(isolated-attempts): Isolate writing attempts and publish validated results`,
with label `decision`. It names both `coding-harness-s9r` and the absorbed
`coding-harness-b5w`, and handles their tracker closure under the one-writer
rule with tracker push before Git push. This architectural class owes no
feature ADR-question answer; the new ADR is accepted only by merge.

## Do not touch

Do not containerise read-only calls, add a native Windows/Linux session UI,
change subscriptions/providers/model efforts/CLI pins/loop limits, weaken
existing gates or alter tracker ownership. Keep `.claude/settings.json`,
the Pi policy source, existing ADR bodies, governance continuity/adoption
records, prior change criteria/decisions, host homes/shared Git settings,
unrelated ignored files and runtime resources outside the change. Image pins
must preserve the existing Pi pin; adding a runtime lock is not an excuse to
upgrade clients or the Python verification toolchain.

## Explore route carried forward

Explore ran on 2026-10-14 through Stage 2, route `flash`, endpoint
`glm-coding-plan`, model `glm-5.3-flash`, attempt 1. Research records no
Stage-1 Explore fallback to carry forward. The absorbed exploration was read
from Git at `c8b009b`; this is repository evidence, not another model call.

## Verification

Run `make venv` once in a new worktree before the commands below. The live
command requires explicit runtime setup and produces evidence only for its
actual platform; run it on both macOS and Linux at the tested commit.

```sh
.venv/bin/python -m pytest tests/test_stage2_attempt.py tests/test_stage2_egress.py tests/test_stage2.py tests/test_stage2_session.py tests/test_stage2_isolation.py tests/test_model_endpoints.py tests/test_ci.py -q
python3 scripts/check_interview_minimums.py --change isolated-attempts
python3 scripts/check_criterion_ledger.py
python3 scripts/check_stage2_isolation.py --program podman --build
make verify
```

The drafting runner performs its own `make verify` and checkpoint; this
drafting call performs neither. The prompt's
`python3 scripts/validate_change_artefacts.py --check` is not executable in
this tree because the file has not landed. Existing interview/ledger checks
and runner validation apply; no replacement gate or fictitious green result
is introduced. Registry/index work remains with the runner so this call does
not read the shared tracker outside its allowed worktree boundary.

## Criterion ledger

- 1: tests/test_stage2.py::test_writing_retries_use_distinct_container_state — an automatic attempt reuses a volume/home or launches on the host
- 1: tests/test_stage2_session.py::test_session_uses_fresh_attached_container — interactive dispatch starts a host CLI or reuses state
- 2: tests/test_stage2_isolation.py::test_live_host_files_are_unreadable — a file or shell read obtains a host/home/Git sentinel through the production adapter
- 3: tests/test_stage2_isolation.py::test_live_attempt_cannot_write_host_state — a host sentinel, worktree, index, config, hook or ref changes
- 4: tests/test_stage2_attempt.py::test_only_the_selected_login_is_passed — another token, sign-in directory or agent socket is supplied
- 4: tests/test_stage2_isolation.py::test_live_attempt_sees_only_selected_credentials — a synthetic unrelated login becomes readable
- 5: tests/test_stage2_isolation.py::test_live_egress_allows_only_the_selected_api — approved traffic fails or proxy/direct/DNS/IPv6/gateway traffic escapes
- 5: tests/test_stage2_egress.py::test_proxy_refuses_host_and_tls_name_bypasses — wildcard, IP, local, mismatched or uninspectable names are accepted
- 6: tests/test_stage2_attempt.py::test_backend_selection_preserves_required_capabilities — a setting is ignored or a backend receives weaker requirements
- 7: tests/test_stage2_attempt.py::test_missing_boundary_prerequisites_never_launch_a_writer — a missing runtime/image/login/profile launches a host or Stage-1 writer
- 8: tests/test_stage2.py::test_every_attempt_scans_its_exact_outgoing_payload — a changed prompt or visible payload escapes its own declaration/leak check
- 8: tests/test_stage2_session.py::test_isolated_session_keeps_both_launch_scans — dispatch occurs after a blocked or omitted final scan
- 9: tests/test_stage2.py::test_isolated_retry_starts_from_the_run_baseline — failed edits/instructions/statuses/ignored or Git state reach a retry
- 9: tests/test_stage2_isolation.py::test_live_retry_has_no_prior_attempt_state — a real second container sees the first one's marker
- 10: tests/test_stage2.py::test_failed_runs_discard_model_and_derived_changes — a failure leaves edits/stamps/index/format/route or ignored files and the next invocation refuses them
- 11: tests/test_stage2_attempt.py::test_publication_rejects_untrusted_topology — traversal, aliases, links, special files or a file-to-directory replacement reaches the host
- 11: tests/test_stage2_attempt.py::test_safe_nested_file_changes_can_be_published — the validator rejects an ordinary new directory/file or safe deletion
- 12: tests/test_stage2.py::test_isolated_draft_keeps_its_existing_output_allowance — answers/outside files or two new ADRs are published, or a second draft cannot revise its own ADR
- 13: tests/test_stage2_isolation.py::test_live_verifier_has_no_host_access_credentials_or_egress — candidate gate/proof code reaches host state, model tokens, live tracker or network
- 14: tests/test_stage2_attempt.py::test_publication_requires_the_exact_clean_verified_bytes — red, unmeasured, credential-bearing or changed-after-validation bytes are published
- 15: tests/test_stage2_attempt.py::test_publication_preserves_intervening_host_work — a concurrent HEAD/index/file/evidence change is overwritten or reset
- 16: tests/test_stage2_attempt.py::test_publication_failure_undoes_only_owned_writes — injected failure leaves partial files/index or removes another writer's work/ref
- 17: tests/test_stage2.py::test_isolated_success_makes_one_clean_checkpoint — zero/multiple commits, model-owned host HEAD changes or unverified leftovers count as success
- 18: tests/test_stage2.py::test_isolated_repair_preserves_red_first_proof_and_status_forms — missing/baseline-green/candidate-red proof marks a row fixed or changes the not-a-test contract
- 19: tests/test_stage2.py::test_only_the_successful_attempts_new_measured_time_is_published — an old/invented/lost measurement satisfies the successful attempt
- 20: tests/test_stage2_session.py::test_session_returns_verified_edits_without_a_host_commit — dispatch/failed exit publishes early, valid edits are lost or normal exit creates a host commit
- 21: tests/test_stage2.py::test_attempt_evidence_survives_discard_and_names_derived_paths — audits/diagnostics vanish, failed statuses survive or derived edits are called model edits
- 22: tests/test_stage2_attempt.py::test_recovery_cleans_only_recorded_owned_resources — cleanup deletes another invocation's resources or falsely reports completion
- 22: tests/test_stage2_isolation.py::test_live_cleanup_and_interrupted_attempt_recovery — controlled exit or next-start recovery retains candidate/login/helper state
- 23: tests/test_stage2_isolation.py::test_qualification_report_requires_all_probes_and_exact_identities — skipped/missing probes or another image/policy/platform qualify a call
- 23: not a test — the hosted Podman gate and macOS report run python3 scripts/check_stage2_isolation.py --program podman --build at named commits; missing either live report refutes completion
- 24: tests/test_stage2.py::test_container_boundary_preserves_existing_routes_and_proof_guards — routes/efforts/pins/fallback triggers/rounds/statuses or ADR tolerance change
- 24: not a test — phase 6 compares the doctrine and ADR against Q-1 to Q-5 and confirms read-only routes and protected areas remain; a contradictory statement refutes this review

## Time used

2026-10-14 and 2026-10-15, phase-4 sessions of the Stage-2 implement worker
(route `flash`, endpoint `glm-coding-plan`), working across one continued
chat with a context break. The worker holds file tools only — no clock, no
command tool — so it records no span or sum of its own and estimates nothing;
the Stage-2 runner appends the measured span with its checkpoint commit, and
its `make verify` is the gate. The 24-hour appetite stop has not been
declared: no reading of `date` under this prompt has shown it reached.
