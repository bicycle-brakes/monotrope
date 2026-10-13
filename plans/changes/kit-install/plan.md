---
title: "Plan — kit-install"
category: plan
created: 2026-10-13
updated: 2026-10-13
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-2uk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, kit, install, update]
---

# Plan — kit-install

```text
For you:     Install the workflow in a fresh repository, update unchanged kit files, and compare an existing instance without writing to it.
Done when:   A fresh target passes make verify, local edits survive update, and regression tests plus this worktree's make verify are green.
Appetite:    12 hours of phase 4, including repairs; stop at the limit.
Not now:     Switching existing instances, merging local edits, building releases, or configuring trackers and model endpoints.
Pre-mortem:  suppose it failed: most likely because target-owned configuration was mistaken for an update-owned kit file.
Starts unless you say stop.
```

Build from `spec.md`; the necessary design choices are carried here so phase
4 needs these two files only. This is a draft: Opus phase 2a and incorporation
of its rows precede implementation. The card covers the spec without widening
its scope or appetite. No Stage-1 Explore fallback was recorded in research.

## Files

| Action | File | Change |
|---|---|---|
| change | `scripts/harness.py` | Add `kit install`, `kit update` and `kit report` dispatch without changing `decide adr`. |
| create | `scripts/kit/payload.py` | Share schema/role reading and committed payload construction, with template recipes and destination validation. |
| create | `scripts/kit/install.py` | Acquire a source snapshot, compare targets, apply safe files transactionally, maintain the lock and run target verification. |
| change | `scripts/kit/manifest.yaml` | Declare schema 2 and the template role, exact initial recipe bindings and the two new tested helpers. |
| change | `scripts/kit/probe.py` | Delegate classification to the shared reader and survey both traveling roles at their original source paths. |
| create | `scripts/kit/bootstrap/AGENTS.md` | Supply a generic initial entry point linking to the one workflow doctrine. |
| create | `scripts/kit/bootstrap/Makefile` | Supply verify/venv entry points using the target gate runner and hash-checked dependency lock. |
| create | `scripts/kit/bootstrap/gates.yaml` | Supply the three portable starter gates in the existing gate schema. |
| create | `scripts/kit/bootstrap/provenance.yaml` | Supply a starting provenance map without source-repository inventory claims. |
| create | `scripts/kit/bootstrap/pyproject.toml` | Supply generic project metadata and dependencies consistent with the copied dependency lock. |
| change | `scripts/ci_gates.py` | Declare the two kit helpers as tested command/library callers in its existing caller-reason table; add no gate. |
| create | `tests/test_kit_payload.py` | Exercise real manifest roles, initial recipes, source exclusion and malformed/path-unsafe payloads. |
| create | `tests/test_kit_install.py` | Exercise CLI behavior, lock ownership, snapshot transport, conflicts, rollback and actual fresh-target verification. |
| change | `tests/test_kit.py` | Hold the third role and shared-reader survey without weakening the classification or portability ratchets. |
| change | `tests/test_ci.py` | Cover the new caller declarations through the existing inventory checks, adjusting only directly affected assertions if necessary. |
| change | `docs/WORKFLOW.md` | Document the three invocations, ownership, bootstrap prerequisites, partial pins and uncommitted verification result. |
| create | `docs/adr/0017-pinned-kit-install-and-update.md` | Carry the single MADR draft for Q-1 through Q-5; acceptance is its decision PR's merge. |
| change | `plans/changes/kit-install/spec.md` | Incorporate accepted 2a clarifications and eventually record implementation state without changing intent. |
| change | `plans/changes/kit-install/design.md` | Keep the published design aligned with the revised spec and implementation. |
| change | `plans/changes/kit-install/plan.md` | Record time and turn each completed ledger entry into an existing-test entry. |
| change | `plans/changes/kit-install/findings.md` | Keep the runner audit, 2a disposition and review evidence in the change. |
| change | `plans/changes/kit-install/research.md` | Keep the drafting gap resolution and any measured portability changes with their cut-offs. |

No file is deleted in the source repository. Target operations may create
the manifest-selected payload, initial templates, scaffold placeholders and
`harness.lock.yaml`, replace recorded kit files, or delete an unchanged
retired kit file; disposable fixture repositories prove those actions.

## Implementation

1. **Payload and first-install configuration.** Put longest segment-aware
   prefix classification in `payload.py`; retain the probe helper APIs through
   wrappers. Schema 2 adds `template` and exact-file `initial_source` or the
   mutually exclusive `initial_generator: ci-gates`. Reject unknown roles,
   unsupported schemas, conflicting duplicate rules/destinations, unclassified
   committed files and unsafe paths. Classify `harness.lock.yaml` as target
   inventory. Keep schema-1 classification readable;
   installation requires schema 2. Make the Q-3 paths templates, together with
   the root provenance map, AGENTS entry point, Makefile, dependency/project
   declarations and CI workflow. Bind separate bootstrap assets where source
   configuration contains inventory; leave source originals and pins alone.
   Recipe assets themselves remain mechanism. The initial Makefile delegates
   verify to `scripts/verify_all.sh` and offers hash-locked `make venv`.
   Bootstrap gates are Python 3.12, portable pytest, gate-schema and ci-drift;
   their commands are the existing schema/CI checks and
   `python3 -m pytest tests/test_gate_record.py tests/test_check_adr_answers.py tests/test_check_criterion_ledger.py tests/test_adoption.py -q`.
   Generate an absent CI template from the chosen target gates using the
   selected snapshot's generator in an isolated preparation tree; retain
   existing templates. Probe the source originals of both traveling roles,
   separately from actual initialization. Remove only exemptions measured as
   newly green, record the run, and never raise the exemption cap as a repair.
2. **Snapshot and read-only comparison.** Add required `--target DIR --ref REV`
   to all verbs and optional `--source LOCATION` to install/report. Unpinned
   operations default to the command repository; pinned operations use the
   lock source. Store its origin URL when available, otherwise its absolute
   local path; reject embedded credentials. Acquire/fetch only in a temporary
   Git repository, with argument arrays and option-safe revisions; read the
   resolved commit's tracked blobs/modes, never dirty source files. Report
   source/target full commits, sorted missing/identical/different paths with
   ownership, scaffold state and totals, without target writes or verification.
   A report requires target HEAD; install may state an unborn target. A
   report's explicit alternate source does not alter the lock. Any unreadable
   state is an error, not absence. Exit 0 for a readable report; exit 2 for a
   refusal or unmeasured state.
3. **Install/update application.** Preflight the entire payload, lock and
   path boundary before writes: source symlinks, linked target ancestors,
   `.git`, escapes and type collisions refuse. Unpinned kit destinations
   refuse install; existing templates are retained and reported. Lock schema
   1 stores source location/completed commit, `files` keyed by destination
   with role/source path/applied commit/SHA-256/Git mode, scaffolds, and null
   or `{commit, conflicts}` pending state. Retained templates have null
   baseline fields and permanent target ownership. Updates require a valid
   lock, replace unchanged kit files of retained kit ownership, add absent
   previously unowned ones, delete unchanged paths absent from the new payload,
   and retain locally edited/deleted/retyped/mode-changed paths
   as conflicts. Template writes/removals and ownership transfers are never
   automatic. Newly introduced templates are reported for manual adoption
   and recorded as target-owned with null baselines, never initialized by
   update. Keep template entries after upstream removal. A partial update
   advances only safe per-file baselines, keeps the last completed source
   pin and records pending commit/conflicts; retries compare each actual path
   with its own baseline. Stage bytes, recheck observed states, journal
   originals and atomically publish the lock. A handled write error restores
   the batch including modes, lock and newly created empty directories. Do
   not delete directories with unrelated content, initialize trackers or
   mutate target Git metadata. One writer per target is required; crash
   recovery and concurrent application are outside this change.
4. **Verification and evidence.** After application, including a partial
   update, run `["make", "verify"]` once with target cwd and stream its
   result. Failure or a conflict yields exit 2 with reason; verification
   failure retains applied files and lock for review. A pin certifies applied
   provenance, not a green gate. Add disposable Git source/target fixtures
   with two committed versions, dirty source bytes, edited templates, local
   kit changes, deletion/addition, role changes and interrupted writes. Run
   a real bare-target install and target `make verify` with declared runtime
   dependencies available; keep the new install integration suite outside
   the starter test command to avoid recursive installation. Add caller
   reasons, run the checks below and update only the directly affected docs
   and ledger. All PR/tracker operations belong to the orchestrator.

## Criterion ledger

- 1: not yet written tests/test_kit_install.py::test_install_uses_resolved_commit_bytes_and_modes — dirty source bytes or wrong mode reach the target.
- 2: not yet written tests/test_kit_payload.py::test_payload_excludes_source_inventory — inventory paths enter the prepared payload.
- 3: not yet written tests/test_kit_payload.py::test_shared_configuration_has_template_role — one of the three Q-3 files is mechanism.
- 4: not yet written tests/test_kit_install.py::test_install_preserves_existing_templates — matching or differing target configuration is replaced or acquired.
- 5: not yet written tests/test_kit_install.py::test_install_refuses_unowned_kit_collision_before_writes — any payload or lock write precedes refusal.
- 6: not yet written tests/test_kit_install.py::test_install_lock_records_source_and_file_baselines — a selected file, owner, hash, mode or full commit is absent or wrong.
- 7: not yet written tests/test_kit_install.py::test_report_names_commits_states_and_ownership — a path/state/cut-off disappears or a template difference becomes kit drift.
- 8: not yet written tests/test_kit_install.py::test_report_is_read_only — files, Git metadata or the verifier change during comparison.
- 9: not yet written tests/test_kit_install.py::test_update_refuses_missing_or_invalid_lock — matching bytes are acquired without a valid ownership record.
- 10: not yet written tests/test_kit_install.py::test_update_replaces_unchanged_kit_files — a safe file fails to receive the selected bytes and mode.
- 11: not yet written tests/test_kit_install.py::test_update_records_new_kit_file — an absent new path is not installed and baseline-recorded.
- 12: not yet written tests/test_kit_install.py::test_update_removes_only_unchanged_retired_file — retirement leaves the file or removes unrelated directory contents.
- 13: not yet written tests/test_kit_install.py::test_update_preserves_local_kit_changes — parameterized edits, deletions, modes and types are overwritten, including when retired upstream.
- 14: not yet written tests/test_kit_install.py::test_update_never_writes_template_paths — template edits, deletions or upstream retirement provoke a target write.
- 15: not yet written tests/test_kit_install.py::test_update_refuses_ownership_transfers — either role transition silently changes the path or recorded owner.
- 16: not yet written tests/test_kit_install.py::test_partial_update_and_retry_keep_truthful_baselines — a conflict advances its baseline, a partial pin claims completion or retry misclassifies safe files.
- 17: not yet written tests/test_kit_payload.py::test_invalid_source_or_payload_refuses_before_application — invalid schema, rules, destinations or an unavailable ref permit writes.
- 18: not yet written tests/test_kit_install.py::test_unsafe_paths_and_symlinks_refuse_before_writes — manifest/lock traversal, Git metadata or linked paths receive writes.
- 19: not yet written tests/test_kit_install.py::test_write_failure_restores_files_modes_and_lock — injected write/deletion/lock-publication failures leave part of the batch applied.
- 20: not yet written tests/test_kit_install.py::test_application_runs_make_verify_once_in_target — fresh, ordinary or partial applications skip, duplicate or misplace verification.
- 21: not yet written tests/test_kit_install.py::test_failed_verification_keeps_reviewable_application — failure is hidden or payload/lock are rolled back after verification.
- 22: not yet written tests/test_kit_install.py::test_application_never_mutates_target_git_state — index, HEAD, refs or remotes change through the command's own actions.
- 23: not yet written tests/test_kit_install.py::test_bare_fresh_target_passes_real_make_verify — bootstrap needs source inventory, tracker data or credentials to pass.
- 24: not yet written tests/test_kit_install.py::test_report_refuses_unreadable_state — unreadable files or revisions produce a successful absence/equality report.

## Verification

After `make venv` once for this worktree, run these commands from its root:

```bash
.venv/bin/python3 -m pytest tests/test_kit_payload.py tests/test_kit_install.py tests/test_kit.py tests/test_harness_decide_adr.py tests/test_ci.py -q
.venv/bin/python3 scripts/check_interview_minimums.py --change kit-install
.venv/bin/python3 scripts/check_criterion_ledger.py
make verify
```

The fresh-target test executes actual `make verify` and keeps its full output
as evidence with the source commit. Keep the existing `decide adr` tests
green and the independent-manifest checks intact. The shared classifier and
new helpers need mutation-sensitive regressions; schema rejection tests must
reach command preflight, not merely assert a test fixture's own filtering.

The prompt also names `python3 scripts/validate_change_artefacts.py --check`;
that script is absent at `bb80ed0`. Do not add it in this change or claim its
gate passed. `plans_registry.py --check` remains a runner check with real
tracker rendering; this draft call must not read the main checkout's tracker.
The maintainer answered Q-5, but its formal ADR-answer file is deliberately
left to the orchestrating session. The draft runner's documented exception
does not waive that answer for the final implementation PR.

## Do not touch

Leave every real instance, source AGENTS/provenance/gate policy, source
dependency pins, legacy export manifest, existing ADRs/continuity map,
tracker, harness settings and tool installations intact. Do not create an
ADR-answer record, release builder, force/merge behavior or source-translation
cleanup. English is used for all new artifacts; existing German code is not
translated in passing.

## Time used

## Draft handoff — 2026-10-13

Objective: phases 2, 2b and 3 only. Branch `feat/kit-install`, input HEAD
`bb80ed03def5d4ec346d77904f4f06009b4c9e3c`, local `origin/main` cut-off
`3199a2823f738b4305dce4b73de6aa8c8c89a6d3`. Remote PR state was not read
under this call's worktree-only read boundary. No commit, tracker write or
instance application is made by the draft author. The existing findings
file belongs to the runner; parallel tracker ownership stays with its
orchestrator. Completed: spec, design, plan and the single ADR draft, with
local gap evidence added to research. As of 2026-10-13, the named-change
interview check and repository criterion-ledger check passed; the new headers
parse as YAML, the ADR proposal is a quoted string, and `Time used` is empty.
The general validator is absent and full `make verify` remains the runner's
next check. All implementation and phase-2a/phase-6 evidence is outstanding.
Resume: the orchestrator verifies and reads this draft, records the stated
ADR answer, runs Opus phase 2a, then requests a second draft for any review
rows before showing the revised card and starting phase 4.
