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
Done when:   A fresh target passes actual make verify before and after its fixture commits the payload, comparison and refusal tests hold, and this worktree's make verify is green.
Appetite:    12 hours of phase 4, including repairs; stop at the limit.
Not now:     Updating a pin, switching existing instances, building releases, or configuring agents, trackers and model endpoints.
Pre-mortem:  suppose it failed: most likely because source inventory assumptions survived in the target's verification.
Starts unless you say stop.
```

Implement from this plan and `spec.md`. Both rounds of phase-2a rulings are incorporated;
Q-6 removes update work. The card widens neither scope nor the existing
12-hour appetite. No Stage-1 Explore fallback route, model or reason is
recorded in research. This drafting call ends before implementation; the
orchestrator displays the card and starts phase 4 after the runner's checks.

## Files

| Action | File | Change |
|---|---|---|
| change | `scripts/harness.py` | Add lazy `kit install`/`kit report` dispatch, leaving `decide adr` intact. |
| create | `scripts/kit/install.py` | Resolve Git snapshots, compare committed trees, preflight/apply fresh installs, publish the lock and invoke verification. |
| change | `scripts/kit/manifest.yaml` | Declare schema 2, five templates, derived CI, starter bindings, exclusions and inventory rules for `harness.lock.yaml` and `LICENSE`. |
| change | `scripts/kit/probe.py` | Extend classification and shared payload preparation, measure the initialized install payload and add portable pytest using the one exception map. |
| create | `scripts/kit/bootstrap/Makefile` | Supply only verify and opt-in hash-locked venv recipes. |
| create | `scripts/kit/bootstrap/gates.yaml` | Supply Python 3.12 and the seven portable blocking gates below. |
| change | `scripts/ci_gates.py` | Extend the caller reason for `harness.py` and declare `kit/install.py` as a tested command helper. |
| change | `pyproject.toml` | Correct only the English travel-policy comment for the dependency lock; change no dependency or setting. |
| create | `tests/test_kit_payload.py` | Hold roles, recipes, exclusions, initialized install/probe equality, scoped skips and portable gate behavior. |
| create | `tests/test_kit_install.py` | Hold CLI snapshots, eligibility, reports, collisions, lock truth, rollback, isolated runtimes and real verification before/after fixture adoption. |
| change | `tests/test_kit.py` | Cover new ownership roles, scope the listed stock cases and preserve independent-policy and portability ratchets. |
| change | `tests/test_ci.py` | Exercise optional gate/CI/runner behavior with fixtures and scope only the listed source-policy cases. |
| change | `tests/test_regelwerk.py` | Scope the listed source-stock and agent-policy cases while retaining their source assertions. |
| change | `tests/test_model_endpoints.py` | Scope agent discovery while keeping missing source agents red. |
| change | `docs/WORKFLOW.md` | Document install/report commands, eligibility, ownership, prerequisites, failure results and deferred updates. |
| revise draft | `docs/adr/0018-pinned-kit-install-and-update.md` | Align the one new-to-main MADR draft with install/report/pin and the recorded review rulings. |
| change | `plans/changes/kit-install/spec.md` | Preserve the revised criteria; change implementation state only with evidence. |
| change | `plans/changes/kit-install/design.md` | Keep the proposed shape aligned with the implementation. |
| change | `plans/changes/kit-install/plan.md` | Record phase-4 time, proof results and completed ledger entries. |
| change | `plans/changes/kit-install/findings.md` | Preserve runner audit lines and record review dispositions and evidence. |
| change | `plans/changes/kit-install/research.md` | Preserve observations and add measured portability changes with cut-offs. |

No source file is deleted. Target writes are selected kit files, missing
regular templates, derived CI, scaffold placeholders and `harness.lock.yaml`.
The new regression suites remain `bestand` under the test catch-all; the
real-install test never ships and recursively starts another installation.
Recipe assets and `install.py` travel under `scripts/kit/`.

## Implementation

1. **Roles and shared preparation.** Keep `probe.regeln`, `rolle`,
   `nach_rolle` and `geruest_ordner`; put common payload preparation in this
   existing module, never an import of the new installer from the probe.
   Schema 2 adds `template` and `derived`. Exactly the five spec paths become
   templates: gates bind by exact `initial_source` to
   `scripts/kit/bootstrap/gates.yaml`, Makefile to
   `scripts/kit/bootstrap/Makefile`; the other three use source-original
   bytes. CI has one derived rule, using `scripts/ci_gates.py` and
   `decisions/gates.yaml`. Exclude root provenance, agent definitions and all
   spec-listed harness/endpoint/tracker settings; add exact `bestand` rules
   for the lock and `LICENSE`. Keep schema-1 classification readable for
   existing helper callers, but install/report accept exactly schema 2 at
   the requested commit. Reject unknown roles/schemas, contradictory rules,
   unclassified committed files, unsafe recipes and destination collisions
   before application. Leave the independent export manifest unchanged.
2. **Portable verification and probe.** The starter Makefile delegates
   verify to `bash scripts/verify_all.sh`; its opt-in venv recipe creates
   `.venv` and installs `requirements-ci.txt` with `--require-hashes`.
   Installation sets up no dependencies. Starter gates use schema 2,
   `tools.python: ["3.12"]`, `job: verify`, `enforcement: block`,
   `placement: both` and these exact commands (pytest has `floor: true`):

   | ID | Command |
   |---|---|
   | pytest | `python3 scripts/kit/probe.py --portable-tests` |
   | ruff-check | `python3 -m ruff check scripts/ tests/` |
   | ruff-format | `python3 -m ruff format --check scripts/ tests/` |
   | adr-answers | `python3 scripts/check_adr_answers.py` |
   | criterion-ledger | `python3 scripts/check_criterion_ledger.py` |
   | gate-schema | `python3 scripts/ci_gates.py --check-schema` |
   | ci-drift | `python3 scripts/ci_gates.py --check-ci` |

   Portable pytest runs all installed `tests/`, converting `REIST_NICHT`
   to exact `--deselect` IDs (`tests.module` to `tests/module.py`, preserving
   function/parameter suffixes); forward failure and empty-collection exits.
   `_baue` uses the same initializer as an empty fresh install: unchanged kit
   bytes, gate/Makefile starters, source-original bytes for the other three
   templates, CI derived from starter gates, scaffolds and the complete lock.
   It invokes neither install nor target verification and commits only its
   own disposable tree before measuring pytest. Prove file-set, bytes, modes
   and lock equality against an actual fixture install of the same selected
   commit, excluding Git metadata and later verifier/measurement output.
   For unstaged runner checks, build a committed source candidate only in an
   owned temporary repository, from tracked working files plus untracked
   kit/recipe assets selected by the manifest. Resolve that candidate commit
   for preparation; change no source index or ref. Test that newly added
   installer/bootstrap assets appear in its initialized probe payload.
   Generic CI/schema/runner tests requiring optional ramp, tracker, history,
   drift, action/local-equivalent or writer-only gates use complete fixture
   gate files and the real generator/runner, including gate-step checks that
   would otherwise inspect an empty drift job. Add no skips to those generic
   cases. Source-specific cases use exactly the table below, retaining
   original source assertions and enforcer names. Keep the legacy
   mechanism/inventory partition and export verdicts independent in both
   directions; check template/derived ownership directly, without requiring
   multiple export verdicts for the single derived path. Measure obsolete,
   green or skipped exemptions and lower the map/cap with evidence. Neither
   may grow; new failures require fixture/portability repairs.
3. **Snapshot and report.** Preserve `decide adr` and expose:

   ```text
   python3 scripts/harness.py kit install --target DIR --ref REV [--source LOCATION]
   python3 scripts/harness.py kit report --target DIR --ref REV [--source LOCATION] [--target-ref REV]
   ```

   Default source is the command repository. Require its `origin` URL for
   local sources; a URL source supplies that identity. Refuse absent identity
   and embedded secret credentials, never substituting a checkout path.
   Acquire/fetch only in an owned temporary Git repository with argument
   arrays and option-safe refs. Resolve full commits and read exact tree
   paths, bytes and modes, ignoring dirty source/target files. Report defaults
   target revision to `HEAD`, compares same-path source originals for all
   three published roles and prints origin, full commits, requested refs,
   sorted path/role/owner/state rows and totals. Labels say templates and CI
   are target-owned references. Read no target working files or lock; invoke
   no target gates and write no target metadata. Exit 0 for a complete
   readable comparison despite differences, 2 for unreadable state or an
   unsupported/missing source manifest, naming the commit and observed
   schema. Never classify historical schema-1 paths with the command's roles.
4. **Install and lock.** Require a non-bare target root, readable HEAD, no
   lock of any type, and index paths only from exact root `README.md`,
   `LICENSE`, `.gitignore`, `.gitattributes`; reject `README.rst`,
   `LICENSE.txt` and every other name, directing to report. Preserve existing
   regular templates and modes; refuse template symlinks, directories,
   submodules and special files, plus every occupied kit/CI/scaffold path.
   Preflight all paths, ancestors, recipes and scaffolds for escapes, Git
   metadata, source symlinks/submodules, linked ancestors and filesystem
   aliases. Prepare CI with the selected generator in a temporary tree
   holding retained or initialized gate bytes. Generator rejection of either
   leaves the target unchanged, no lock and no verifier call. Lock schema 1
   has `source: {url, commit}` and `files` keyed by exact path with `role`,
   `owner`, `source_path` or `generated_by`, `installed` and
   `baseline: {sha256, git_mode}`. Retained templates are target-owned with
   `installed: false`, `baseline: null` and observed hash/mode. Derived CI is
   target-owned with generator/input hash and actual output baseline.
   Scaffold `.gitkeep` records are kit-owned, with null source path, scaffold
   derivation and empty-file baseline. The lock is metadata, not self-hashed;
   add no pending/update state. Recheck destinations, journal created
   files/directories, apply bytes/modes and publish the lock last. Any I/O
   failure in write/chmod/mkdir/temporary-file/lock publication removes every
   created file/directory and preserves existing content; verification never
   starts. No overwrite, deletion or update path is needed.
5. **Verification and evidence.** Invoke `["make", "verify"]` once with target
   cwd and lock present. Strip `BEAD_RENDER`/`PYTHON` and every PATH entry
   inside the command repository, including `.venv/bin`, resolving entries
   in caller context and preserving outside entries in order. The runtime
   is the target's available `.venv/bin/python3`, else the first `python3`
   on cleaned PATH. Exercise both with source interpreter directory first
   on caller PATH and assert it reaches neither verifier PATH nor runtime.
   Stream output; exit 0 only on green, else 2 with the reason and applied
   files/lock retained. Installer actions make no target Git mutations.
   Fixtures cover eligibility, pinned retry, dirty bytes, exact case paths,
   modes, all destination types, invalid retained/starter gates and failures
   at every application step. The real target fixture tracks all four allowed
   root names and provides Python 3.12/dependencies separately, never through
   source inheritance. Poison caller overrides/PATH and remove endpoint
   credentials; assert real verification, unchanged index/HEAD and untracked
   payload. The fixture then commits only recorded payload paths and the lock
   (never its venv/caches), and runs real target
   `make verify` again, including the lock's role check and all seven gates.
   Record source/target commits and output. Its committed source snapshot
   explicitly contains new installer/recipe/test assets; never depend on the
   runner staging them in this checkout first. Tracker, PR and merge work
   stays with the orchestrator.

## Scoped skips

Every added/changed skip in a shipped test is listed here by function. All
use exactly `(REPO_ROOT / "harness.lock.yaml").exists()`; no additional skip
predicate is planned. The source has no installed lock, so missing source
prerequisites still fail. Generic cases use fixtures, not these skips.

| Case | Source-only assertion |
|---|---|
| `tests/test_kit.py::test_the_kit_actually_carries_something` | At least 20 tracked mechanism files in this repository. |
| `tests/test_kit.py::test_the_two_manifests_really_disagree_somewhere` | More than 60 tracked files in both source manifests. |
| `tests/test_kit.py::test_the_kit_list_is_not_derivable_from_the_export_list` | Independence measured over the full source stock. |
| `tests/test_ci.py::test_ci_exists_and_has_gates` | Source policy has at least ten gates. |
| `tests/test_ci.py::test_no_directory_a_gate_reads_is_excluded` | Source tracked-directory inventory feeds the path survey. |
| `tests/test_ci.py::test_die_ableitung_findet_ueberhaupt_etwas` | Source gate inventory yields at least five directories. |
| `tests/test_ci.py::test_only_the_named_gates_are_writer_only` | The source declares its live ruleset gate as writer-only. |
| `tests/test_ci.py::test_the_drift_job_runs_the_plans_registry_strictly` | Source policy schedules its inventory registry gate. |
| `tests/test_ci.py::test_the_drift_job_holds_only_steps_that_can_run` | The source's nonempty drift gate list has no instance prerequisite. |
| `tests/test_regelwerk.py::test_every_rule_id_referenced_anywhere_exists` | Source tracked files provide a nonempty reference inventory. |
| `tests/test_regelwerk.py::test_rb_a1_clause_is_present_verbatim` | Excluded source agent definitions contain the exact clause. |
| `tests/test_regelwerk.py::test_agent_definitions_carry_no_instance_terms` | Excluded source agent definitions contain no instance terms. |
| `tests/test_model_endpoints.py::test_agents_are_found_at_all` | Excluded source agent discovery is nonempty. |

Audit added/changed skips against the diff from the change's merge base:
reject an unlisted case or another predicate, including an unconditional
skip. Retain existing unrelated skips unchanged. Record source execution of
each listed case without a skip; remove its probe exemption only after the
new measurement proves it green, skipped or absent, and lower the cap.

## Criterion ledger

- 1: not yet written tests/test_kit_install.py::test_install_uses_resolved_commit_bytes_and_modes — dirty source bytes or the wrong executable bit reach the target.
- 2: not yet written tests/test_kit_payload.py::test_payload_excludes_inventory_and_harness_configuration — a protected source path is published.
- 3: not yet written tests/test_kit_payload.py::test_exact_initial_configuration_has_template_role — an extra starter is added or one of the five is kit-owned.
- 4: not yet written tests/test_kit_install.py::test_install_preserves_existing_templates — matching/different regular templates or modes are replaced or kit-owned.
- 5: not yet written tests/test_kit_install.py::test_install_refuses_targets_outside_freshness_allowlist — an alternative filename, populated, unborn, pinned, bare or non-root target receives a write.
- 6: not yet written tests/test_kit_install.py::test_install_refuses_occupied_destinations_before_writes — a kit/CI/scaffold collision or non-regular template allows any target write.
- 7: not yet written tests/test_kit_install.py::test_lock_records_origin_commit_and_ownership_baselines — a URL, commit, role, recipe, hash or mode is wrong or absent.
- 8: not yet written tests/test_kit_install.py::test_report_uses_named_commits_exact_paths_and_ownership — dirty bytes, folded case or missing paths give a dishonest result.
- 9: not yet written tests/test_kit_install.py::test_report_is_read_only — target files/Git state change or a verifier starts.
- 10: not yet written tests/test_kit_payload.py::test_invalid_source_or_payload_refuses_before_application — invalid schema, origin, rules, ref, recipes or destinations allow writes.
- 10: not yet written tests/test_kit_install.py::test_invalid_target_gates_refuse_before_writes — retained or starter generator rejection leaves a target file or lock.
- 11: not yet written tests/test_kit_install.py::test_unsafe_payload_recipes_and_symlinks_refuse_before_writes — an escaping, linked or Git-metadata path receives a write.
- 12: not yet written tests/test_kit_install.py::test_each_filesystem_failure_restores_tree_before_verification — injected write/chmod/mkdir/lock failures leave content or start verification.
- 13: not yet written tests/test_kit_install.py::test_install_runs_make_verify_once_in_target_after_lock — verification is skipped, duplicated, misplaced or sees no lock.
- 14: not yet written tests/test_kit_install.py::test_target_verification_isolates_runtime_and_path — a poisoned override or source PATH directory/runtime reaches verification, including without a target venv.
- 15: not yet written tests/test_kit_install.py::test_failed_or_unavailable_verification_keeps_application — failure is hidden or applied files/lock disappear.
- 16: not yet written tests/test_kit_install.py::test_install_preserves_target_git_state — installer actions change index, HEAD, refs or remotes.
- 17: not yet written tests/test_kit_install.py::test_fresh_committed_target_passes_real_make_verify_untracked — verification needs staging, source state, credentials, inherited dependencies or an extra starter; the fixture tracks all four allowed names.
- 18: not yet written tests/test_kit_install.py::test_committed_installed_target_passes_real_make_verify — post-adoption verification fails or the committed lock/LICENSE is unclassified.
- 19: not yet written tests/test_kit_payload.py::test_starter_gates_run_shipped_tests_except_probe_exemptions — a gate/test file disappears or extra deselections hide a failing unexempted case.
- 19: not yet written tests/test_kit_payload.py::test_changed_shipped_skips_are_listed_and_scoped — a new/changed skip is unlisted or uses a forbidden predicate.
- 20: not yet written tests/test_kit_install.py::test_ci_is_derived_from_selected_target_gates — source CI is copied, retained gates are ignored or regeneration differs.
- 20: not yet written tests/test_kit_install.py::test_invalid_target_gates_refuse_before_writes — rejected CI derivation happens after a target write.
- 21: not yet written tests/test_kit_install.py::test_scaffold_placeholders_are_empty_and_kit_owned — a scaffold is missing/populated or its placeholder lacks a baseline.
- 22: not yet written tests/test_kit_payload.py::test_probe_matches_initialized_install_payload — file-set, starters, CI, modes or lock differ from an empty fresh fixture install.
- 22: not yet written tests/test_kit_payload.py::test_probe_includes_untracked_kit_assets_from_candidate_snapshot — the pre-staging probe omits a new installer/bootstrap asset or changes source Git state.
- 22: tests/test_kit.py::test_the_exemption_list_only_shrinks — the exception count exceeds its cap.
- 22: not yet written tests/test_kit_payload.py::test_changed_shipped_skips_are_listed_and_scoped — a new/changed skip is unlisted or uses a forbidden predicate.
- 22: not a test — phase-6 review compares the map/cap against input commit a1b29a0 and measured output, and source results against the skip table; a new exemption, higher cap or skipped source case refutes it.
- 23: not yet written tests/test_kit_install.py::test_report_refuses_unresolved_or_unreadable_git_state — a Git read failure yields successful absence/equality.
- 23: not yet written tests/test_kit_install.py::test_report_refuses_unsupported_source_manifest — an absent/old/other schema is compared or fails without its commit/schema named.

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

The measurement command supplies evidence, not a pass verdict; the strict
probe in `make verify` blocks unexplained, expired and orphaned exemptions.
The real integration tests invoke actual target `make verify` in both
untracked and fixture-committed states and capture all seven gate results.
The focused source run must show every listed scoped case ran without
skipping. Keep independent export and `decide adr` regressions green.

`python3 scripts/validate_change_artefacts.py --check` cannot run: the script
is absent at the 2026-10-14 drafting cut-off. Add no validator and claim no
pass. The registry/full gates reading the shared tracker run under the
orchestrator's authority and read boundary; this drafting call reads only
the worktree/Git directory and writes no tracker or ADR answer.

## Do not touch

Leave real instances/customer trees, AGENTS/provenance/live gate policies,
source dependency versions/runtime settings, harness settings, tools,
tracker, ADR answers, pre-existing ADRs/continuity mappings and independent
export manifest untouched. Only the new-to-main ADR 0018 is redrafted.
Build no update, merge/force operation, release builder, extra starter,
endpoint or tracker setup. The pyproject comment changes no pin.

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

## Draft handoff addendum — 2026-10-14, second review

Objective: redraft phases 2, 2b and 3 from the recorded rulings on F-16
through F-24. Branch `feat/kit-install`, input HEAD
`a1b29a0aa28d3a0171bf55452adf6ec5c40f7756`; local `origin/main` remains
`3199a2823f738b4305dce4b73de6aa8c8c89a6d3`. The initial dirty path was the
runner's findings audit. The remote PR query failed to connect to GitHub;
PR state is not read. This worker neither stages nor commits, changes a
branch, writes the tracker nor applies anything to a real instance; tracker
ownership and the single commit remain with the runner/orchestrator.

Completed: revised spec/design/plan, current dispositions for all 24 review
rows, local gap evidence and the same single new-to-main ADR 0018. The new
criterion 18 requires actual post-adoption verification; all four root names,
initialized probe payload/lock, enumerated scoped skips, CI preflight,
non-regular templates, schema-2-only reporting and runtime isolation are
explicit. Recorded class, ADR claim, answers and 12-hour appetite stay intact;
decisions and ADR-answer files were not edited. Local interview and criterion
ledger checks plus `git diff --check` passed on 2026-10-14. Artifact QA also
checked YAML headers, 23 triggered/refutable criteria, the opening card, five
design parts, 13 existing scoped cases, 24 closed rows, unchanged reviewer
text/audit/history, allowed changed paths and empty `Time used`. The plan
also specifies a temporary probe candidate snapshot containing untracked
kit/recipe assets without changing source Git state. Implementation, integration/runtime
evidence and new portability measurements remain undone.
The general validator is absent; registry/shared-tracker and full
`make verify` checks belong to the runner. The dated session file under
`docs/journal/handover/` is outside this call's allowed writes and remains
the orchestrator's responsibility; this addendum is the worker's handoff.

Resume: let the runner verify and commit the redraft, display the identical
opening card, then start phase 4 from this plan and `spec.md`, implementing
install/report/lock only and recording time below.

## Time used
