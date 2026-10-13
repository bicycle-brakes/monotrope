---
title: "Plan — kit-install"
category: plan
created: 2026-10-13
updated: 2026-10-14
status: draft
implementation_status: none
date: 2026-10-13
last_reviewed: 2026-10-14
supersedes: null
superseded_by: null
bead: coding-harness-2uk
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, kit, install, report]
---

# Plan — kit-install

```text
For you:     Install a pinned workflow in a fresh repository and compare an existing instance at named commits without writing to it.
Done when:   A fresh target passes actual make verify, comparison and refusal tests hold, and this worktree's make verify is green.
Appetite:    12 hours of phase 4, including repairs; stop at the limit.
Not now:     Updating a pin, switching existing instances, building releases, or configuring agents, trackers and model endpoints.
Pre-mortem:  suppose it failed: most likely because source inventory assumptions survived in the target's verification.
Starts unless you say stop.
```

Implement from this plan and `spec.md`. The phase-2a rulings are incorporated;
Q-6 removes update work. The card widens neither scope nor the existing
12-hour appetite. No Stage-1 Explore fallback route, model or reason is
recorded in research. This drafting call ends before implementation; the
orchestrator displays the card and starts phase 4 after the runner's checks.

## Files

| Action | File | Change |
|---|---|---|
| change | `scripts/harness.py` | Add lazy `kit install`/`kit report` dispatch, leaving `decide adr` behavior intact. |
| create | `scripts/kit/install.py` | Resolve Git snapshots, compare committed trees, preflight/apply fresh installs, record the lock and invoke verification. |
| change | `scripts/kit/manifest.yaml` | Declare schema 2, the five templates, derived CI, exact starter bindings and the exclusions in the spec. |
| change | `scripts/kit/probe.py` | Extend the existing classifier/survey for four roles, derive probe CI and add portable pytest using the one exception map. |
| create | `scripts/kit/bootstrap/Makefile` | Supply only verify and opt-in hash-locked venv recipes. |
| create | `scripts/kit/bootstrap/gates.yaml` | Supply Python 3.12 and the seven specified portable blocking gates. |
| change | `scripts/ci_gates.py` | Extend the caller reason for `harness.py` and declare `kit/install.py` as a tested command helper. |
| change | `pyproject.toml` | Correct only the English travel-policy comment now that the dependency lock initializes a target; change no dependency or setting. |
| create | `tests/test_kit_payload.py` | Hold schema, roles, recipe selection, exclusions, probe contents and portable gate behavior with fixtures. |
| create | `tests/test_kit_install.py` | Hold CLI snapshots, eligibility, reports, collisions, lock truth, rollback, verification and a real fresh-target run. |
| change | `tests/test_kit.py` | Cover template/derived classification and preserve the independent-manifest and portability ratchets. |
| change | `tests/test_ci.py` | Make generic gate/schema tests use fixtures and distinguish source policy from target verification without weakening source checks. |
| change | `tests/test_regelwerk.py` | Apply the existing foreign-tree skip convention only to assertions about excluded source agent definitions. |
| change | `tests/test_model_endpoints.py` | Keep source agent discovery strict while making its absence in a foreign payload explicit. |
| change | `docs/WORKFLOW.md` | Document install/report invocations, eligibility, ownership, prerequisites, failure results and the deferred update route. |
| revise draft | `docs/adr/0018-pinned-kit-install-and-update.md` | Keep the one new-to-main MADR record, narrowing delivery/validation to install/report/pin per Q-6. |
| change | `plans/changes/kit-install/spec.md` | Preserve the revised criteria and record implementation state only when supported by evidence. |
| change | `plans/changes/kit-install/design.md` | Keep the proposed system shape aligned with the implemented spec. |
| change | `plans/changes/kit-install/plan.md` | Record phase-4 time, proof results and completed ledger entries. |
| change | `plans/changes/kit-install/findings.md` | Preserve runner audit lines and record review dispositions and later evidence. |
| change | `plans/changes/kit-install/research.md` | Preserve observations and add measured portability changes with their cut-offs. |

No source file is deleted. Target writes are only selected kit files, missing
templates, derived CI, scaffold placeholders and `harness.lock.yaml`.
The new regression suites remain `bestand` under the test catch-all; do not
ship the real-install test into a target and recursively start installation.
Keep recipe assets and `install.py` traveling under `scripts/kit/`.

## Implementation

1. **Roles and bootstrap.** Keep `probe.regeln`, `rolle`, `nach_rolle` and
   `geruest_ordner` as the shared classifier APIs; do not introduce another
   imported classifier module. Schema 2 adds `template` and `derived` and
   exact-file `initial_source` recipe bindings. Exactly the three Q-3 paths,
   Makefile and requirements-ci.txt become templates. Gates bind to the new
   gate starter and Makefile to the Makefile starter; the other three use
   source-original bytes. CI becomes one derived rule, generated by
   `scripts/ci_gates.py` from chosen target gates, never copied. Root provenance,
   `.claude/agents/`, all other harness/endpoint/tracker settings and the
   target lock stay inventory. Keep schema-1 classification readable;
   install/report require schema 2. Reject unknown roles/schemas, contradictory
   duplicate rules, unclassified committed files, unsafe recipes and colliding
   destinations before writes. The independent export policy stays separate.
2. **Portable verification and probe.** The starter Makefile's verify recipe
   is `bash scripts/verify_all.sh`; its opt-in venv recipe creates `.venv` and
   installs `requirements-ci.txt` with `--require-hashes`. Installation runs
   neither recipe for dependency setup. Starter gates use schema 2,
   `tools.python: ["3.12"]`, `job: verify`, `enforcement: block`, `placement:
   both`, and the following exact commands (pytest retains `floor: true`):

   | ID | Command |
   |---|---|
   | pytest | `python3 scripts/kit/probe.py --portable-tests` |
   | ruff-check | `python3 -m ruff check scripts/ tests/` |
   | ruff-format | `python3 -m ruff format --check scripts/ tests/` |
   | adr-answers | `python3 scripts/check_adr_answers.py` |
   | criterion-ledger | `python3 scripts/check_criterion_ledger.py` |
   | gate-schema | `python3 scripts/ci_gates.py --check-schema` |
   | ci-drift | `python3 scripts/ci_gates.py --check-ci` |

   Portable mode invokes pytest on all installed `tests/`, using exact
   `--deselect` node IDs converted from `REIST_NICHT` (`tests.module` becomes
   `tests/module.py`; function/parameter suffixes stay intact). Keep one map,
   forward pytest's failing/empty-collection result and add no exclusions.
   `_baue` copies source-original mechanism and template bytes at their
   original paths, then derives CI from its copied gate file; it does not
   initialize bootstrap substitutions. Full source policy checks retain
   their original assertions; generic tests requiring optional gates build
   complete fixture gate lists rather than assuming this repository's ids.
   Agent/source policy checks use the existing missing-AGENTS foreign-tree
   convention, with tests proving the checks still fail on broken source
   prerequisites. Preserve test names cited by the rule set. Measure
   disappearing/green exemptions and reduce the map/cap with evidence;
   neither exception count nor cap may grow. New failures in the initialized
   target need fixture/portability repairs, not new exemptions.
3. **Snapshot and report.** Add `--target DIR --ref REV` to both verbs,
   optional `--source LOCATION` defaulting to the command repository, and
   report-only `--target-ref REV` defaulting to `HEAD`. A local source's
   identity comes from its `origin` URL, with no checkout-path fallback;
   a URL source uses that URL. Reject absent identity and embedded secrets.
   Resolve/fetch only in an owned temporary Git repository using argument
   arrays and option-safe refs; read full commit, tracked tree, blobs and
   modes, not source working files. Report reads target Git objects at the
   resolved target commit and compares exact case-sensitive source paths for
   mechanism/template/derived roles against source-original reference bytes
   and modes. Print full commits, origin, sorted path/owner/state rows and
   totals; label templates target-owned and CI derived/reference only.
   Do not read working-tree files, depend on target lock validity, run target
   gates, or write target metadata. Exit 0 for a readable comparison despite
   differences, exit 2 for unmeasured state with a reason.
4. **Install and lock.** Require a non-bare target root with readable HEAD,
   no lock of any type, and index paths only from root `README*`, `LICENSE*`,
   `.gitignore` and `.gitattributes`. Anything else refuses before writes and
   points to report. Preserve regular existing templates including modes;
   refuse any occupied kit, CI or `.gitkeep` destination. Preflight the full
   source/destination/recipe/scaffold set, Git metadata, symlinks/submodules,
   linked ancestors, escapes and filesystem aliases. Generate CI before
   application in a temporary tree using the selected generator and retained
   or initialized target gate bytes; invalid target gates refuse cleanly.
   Lock schema 1 stores `source: {url, commit}` and `files` keyed by exact
   destination with role, owner, source_path/generated_by, installed flag and
   `{sha256, git_mode}` baseline. Retained templates are target-owned with
   `installed: false`, `baseline: null` and observed hash/mode. Derived CI is
   target-owned and records generator/input hash and actual output baseline.
   Each scaffold `.gitkeep` is kit-owned with a null source path, scaffold
   derivation and the empty-file baseline. Do not self-hash the lock or add
   pending/update state. Prepare bytes, recheck absence, journal created
   files/directories, write modes, and publish the lock last. On any I/O error
   in file writes, chmod, mkdir, temporary-file/lock publication, remove every
   created file/directory and leave pre-existing contents intact; do not
   invoke verification. No overwrite/deletion/update operation is needed.
5. **Verification and evidence.** After complete application, invoke
   `["make", "verify"]` exactly once with target cwd and lock present, with
   `BEAD_RENDER` and `PYTHON` absent from the child environment. Stream output;
   exit 0 only on green verification, otherwise exit 2 and retain payload/lock
   for review. The installer's own actions make no target Git mutations.
   Use disposable committed Git fixtures for all branches, including a
   populated target that lacks kit paths, a pinned retry, dirty source and
   target files, case-distinct committed paths, mode differences, preserved
   templates and failures at every application step. For the real integration
   run, prepare the target's own Python 3.12 environment/dependencies separately
   (no installer dependency setup), seed one allowed commit, poison caller
   `PYTHON`/`BEAD_RENDER`, remove endpoint credentials, and assert actual target
   verification plus unchanged index/HEAD and an untracked payload. Record
   that fixture source commit and full output. The committed fixture snapshot
   must include all new implementation/assets explicitly: do not rely on the
   source index during the runner's unstaged verification. Declare the new
   caller reason, run the commands below, and record phase-4 time. Tracker,
   PR and merge work stays with the orchestrator.

## Criterion ledger

- 1: not yet written tests/test_kit_install.py::test_install_uses_resolved_commit_bytes_and_modes — dirty source bytes or the wrong executable bit reach the target.
- 2: not yet written tests/test_kit_payload.py::test_payload_excludes_inventory_and_harness_configuration — any protected source path is published.
- 3: not yet written tests/test_kit_payload.py::test_exact_initial_configuration_has_template_role — an extra starter is added or one of the five is kit-owned.
- 4: not yet written tests/test_kit_install.py::test_install_preserves_existing_templates — matching/different regular templates or modes are replaced or kit-owned.
- 5: not yet written tests/test_kit_install.py::test_install_refuses_targets_outside_freshness_allowlist — a populated, unborn, pinned, bare or non-root target receives a write.
- 6: not yet written tests/test_kit_install.py::test_install_refuses_occupied_destinations_before_writes — a kit/derived/scaffold collision allows any target write.
- 7: not yet written tests/test_kit_install.py::test_lock_records_origin_commit_and_ownership_baselines — a URL, full commit, role, recipe, hash or mode is wrong or absent.
- 8: not yet written tests/test_kit_install.py::test_report_uses_named_commits_exact_paths_and_ownership — dirty bytes, folded case or missing paths give a dishonest cut-off/state.
- 9: not yet written tests/test_kit_install.py::test_report_is_read_only — the report changes target files/Git metadata or starts its verifier.
- 10: not yet written tests/test_kit_payload.py::test_invalid_source_or_payload_refuses_before_application — invalid schema, origin, rules, ref or destinations allow writes.
- 11: not yet written tests/test_kit_install.py::test_unsafe_payload_recipes_and_symlinks_refuse_before_writes — an escaping, linked or Git-metadata path receives a write.
- 12: not yet written tests/test_kit_install.py::test_each_filesystem_failure_restores_tree_before_verification — injected write/chmod/mkdir/lock failures leave files/directories or start the verifier.
- 13: not yet written tests/test_kit_install.py::test_install_runs_make_verify_once_in_target_after_lock — verification is skipped, duplicated, misplaced or sees no lock.
- 14: not yet written tests/test_kit_install.py::test_target_verification_drops_source_python_and_bead_render — either poisoned caller variable reaches the target process.
- 15: not yet written tests/test_kit_install.py::test_failed_or_unavailable_verification_keeps_application — a failure is hidden or applied files/lock disappear.
- 16: not yet written tests/test_kit_install.py::test_install_preserves_target_git_state — the command changes the index, HEAD, refs or remotes.
- 17: not yet written tests/test_kit_install.py::test_fresh_committed_target_passes_real_make_verify_untracked — actual verification needs staging, source state, credentials or an undeclared starter.
- 18: not yet written tests/test_kit_payload.py::test_starter_gates_run_shipped_tests_except_probe_exemptions — a portable gate or shipped case disappears, or a failing unexempted fixture passes.
- 19: not yet written tests/test_kit_install.py::test_ci_is_derived_from_selected_target_gates — source CI is copied or the retained gate bytes are ignored.
- 20: not yet written tests/test_kit_install.py::test_scaffold_placeholders_are_empty_and_kit_owned — a scaffold is missing/populated or its placeholder lacks a lock baseline.
- 21: not yet written tests/test_kit_payload.py::test_probe_copies_source_templates_and_derives_ci — templates disappear, get bootstrap substitution, or CI is copied.
- 21: tests/test_kit.py::test_the_exemption_list_only_shrinks — the exception count exceeds its cap.
- 21: not a test — phase-6 review compares the exception map/cap with input commit 6e0ced9 and the measured probe output; any new exemption or raised cap refutes it.
- 22: not yet written tests/test_kit_install.py::test_report_refuses_unresolved_or_unreadable_git_state — a read failure yields a successful absence/equality report.

## Verification

After `make venv` once for this worktree, run from its root:

```bash
.venv/bin/python3 -m pytest tests/test_kit_payload.py tests/test_kit_install.py tests/test_kit.py tests/test_harness_decide_adr.py tests/test_ci.py tests/test_regelwerk.py tests/test_model_endpoints.py -q
.venv/bin/python3 scripts/check_interview_minimums.py --change kit-install
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/kit/probe.py --messen
.venv/bin/python3 scripts/plans_registry.py --check
make verify
```

The measurement command emits evidence, not a pass verdict; the strict probe
in `make verify` holds unexplained, expired and orphaned exemptions. Keep the
independent-export and existing `decide adr` regressions green. The real
fresh-target test executes target `make verify`, asserts the seven-gate
baseline and captures failure output instead of accepting a mock verifier.

The general command `python3 scripts/validate_change_artefacts.py --check`
cannot run: its script is absent at the drafting cut-off, 2026-10-14. Do not
add it or claim its gate passed. The registry/full gates requiring the shared
tracker run under the orchestrator's authority; this draft call reads only
the worktree and Git directory and writes no tracker or ADR answer.

## Do not touch

Leave real instances/customer trees, AGENTS/provenance/live gate policies,
source dependency versions and runtime settings, harness settings, tools,
tracker, ADR answers, pre-existing ADRs/continuity mappings and the independent
export manifest untouched. Only the new-to-main ADR 0018 is redrafted. Build
no update, merge/force operation, release builder, extra starter, endpoint or
tracker setup. The pyproject comment correction changes no source pin.

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

## Draft handoff addendum — 2026-10-14

Objective: redraft phases 2, 2b and 3 after Q-6 and the phase-2a rulings.
Input branch `feat/kit-install`, HEAD
`6e0ced9b8ce0012d9c79281a38d7a1d6e3df337f`; local `origin/main` cut-off
`3199a2823f738b4305dce4b73de6aa8c8c89a6d3`. The PR state was not read under
the worktree-only boundary. The only initial dirty path was the runner's
findings audit for this attempt. The runner is the active orchestrator in
this checkout; this drafting worker creates no parallel writer, commits,
branches, tracker writes or real-instance applications.

Completed: narrowed spec/design/plan, the reserved single ADR draft, local gap
addendum and dispositions for every phase-2a row. Decisions and ADR-answer
files remain unchanged; Q-1 to Q-6, the freshness/template/CI rulings and the
12-hour appetite are carried forward. Post-redraft checks passed on 2026-10-14:
the named-change interview check, repository criterion-ledger check and
`git diff --check`; YAML headers, the 22 triggered/refutable criteria, opening
card, five design parts, 15 dispositions and empty `Time used` were also
checked. The general artifact validator and plan template remain absent.
Implementation and its test evidence remain outstanding. Full verification,
registry/tracker checks and the one commit belong to the runner. A dated
repository-wide handover outside this call's write boundary belongs to the
orchestrator; this addendum preserves this worker's resumption context.

Resume: let the runner verify and commit this draft, display the exact opening
card, then implement install/report only from this plan and `spec.md`.

## Time used
