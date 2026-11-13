---
title: "Plan — kit-probe-on-kit-change"
status: draft
implementation_status: none
date: 2026-11-13
last_reviewed: 2026-11-13
updated: 2026-11-13
supersedes: null
superseded_by: null
bead: coding-harness-w2ay
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, model: gpt-6.1-sol, version: "2026-11-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, verify-speed, kit, gates]
---

# Plan — kit-probe-on-kit-change

```text
For you:     Local full checks skip the expensive kit tests when the kit is unaffected, while classification stays active and CI still tests the kit.
Done when:   Trigger and skip proofs, honest skip history, a transferred-kit check and make verify pass, with the full probe retained in hosted CI.
Appetite:    4 hours of phase 4 in total, repairs included — a stop, not an estimate.
Not now:     Caching, fewer kit tests, targeted-check changes, nightly scheduling or migrations to other repositories.
Pre-mortem:  suppose it failed: most likely because a committed or staged kit edit was mistaken for an unchanged kit.
Starts unless you say stop.
```

## Build sequence and files

1. Attempt: change `scripts/kit/probe.py` to extract the existing pre-test checks into a callable classification verdict and expose `--classification-only` (compatible with `--strict`, mutually exclusive with list/measurement modes). Keep `pruefe(faelle=...)`, the default full command and the exemption checks intact; classification must never call `fahre()`. Add classification red/strict/green and unchanged full-verdict proofs to `tests/test_kit.py`.
2. Attempt: change `scripts/ci_gates.py` to prepare schema 4 with optional `local_when: {paths: [...], kit_manifest: <path>, membership: true}`; any supplied trigger is sufficient. `paths` holds repository-relative file/directory prefixes, `kit_manifest` selects `mechanismus` paths through the existing kit classifier, and `membership` means any added/deleted path. Reject empty declarations, unknown keys, wrong types, empty/escaping/absolute paths, unsupported membership values and declarations on actions or hosted-only gates. With no field, run unconditionally. Load the kit helper only for a manifest condition; do not duplicate its role matching or make every reader import the probe.
3. Attempt: in the same reader, derive the spec's comparison base without fetching, then union NUL-delimited, rename-disabled diffs of the index and working tree against that base with nonignored untracked paths. Preserve additions/deletions from both states, mode changes and unusual filenames. On `main` use `HEAD^`; on named branches use `merge-base HEAD origin/main`; an indeterminate detached checkout, missing base or failed git/classifier read yields run-with-reason. Reevaluate on every run. A manifest/probe edit matches `paths` before loading a possibly damaged manifest; malformed gate configuration itself still fails schema validation.
4. Attempt: keep legacy three-column `--commands --tsv`, inventory and targeted callers unconditional. Add opt-in `--with-local-decisions` for `--commands --placement lokal --tsv`, returning `id`, enforcement, `run|skip`, a nonempty single-line reason and command in five tab-separated fields. Reasons identify the comparison base and the matching trigger or measured absence; sanitize tabs/newlines rather than interpreting filenames as shell input. Reject incompatible CLI combinations. Catalogue rendering exposes the declaration, not a checkout-specific result.
5. Attempt: change `scripts/verify_all.sh` to consume these decisions locally and execute only run rows. Keep `--ci` on unconditional commands. Apply the existing blocking-stop branch before handling a conditional skip: a gate never reached gets only the existing not-run summary. Print reached conditional skips outside machine gate frames, record them, and make the final green wording acknowledge declared skips. No gate IDs, kit path rules or extra commands belong in this runner.
6. Attempt: change `scripts/verify_duration.py` with an additive version-1 `gate_skip` event and CLI operation carrying run ID, gate ID, UTC, enforcement and reason (including base), with no exit or duration. Validate/group/report skips separately; preserve old history, executed-gate timing, per-gate baselines and incomplete-run detection. Use the existing safe append/warning path; unavailable storage still warns and does not change the gate verdict. Add mixed old/new history, malformed skip and reporting proofs in `tests/test_verify_duration.py`.
7. Attempt: create `tests/test_kit_probe_condition.py` for real reader/runner executions in temporary git repositories with synthetic gate lists and marker commands. Cover the ledger matrix below, schema faults independently of unrelated errors, renamed gate IDs and a recipient assembled from manifest-selected mechanism files. Extend `tests/test_gate_catalog.py`'s independent expected cells for the declared condition. Prepare all of this against synthetic schema-4 lists while the held real list remains schema 3, including its unchanged catalogue bytes and existing version-3 assertions; temporary schema-3 compatibility is bootstrap-only, removed in step 8.
8. Orchestrator bootstrap, after the accepted attempt: change held `decisions/gates.yaml` to schema 4; add `kit-classification`, seconds/block/floor/both, command `python3 scripts/kit/probe.py --classification-only --strict`, before expensive gates; retain `leerprobe` as minutes/block/floor/both with its existing full strict command. Only `leerprobe` declares `local_when: {paths: [scripts/kit/manifest.yaml, scripts/kit/probe.py], kit_manifest: scripts/kit/manifest.yaml, membership: true}`. Document this field beside the schema. Activate strict schema 4 in `scripts/ci_gates.py`, removing all schema-3 compatibility. The implement attempt never edits held paths, even to cure an expected activation mismatch.
9. Orchestrator: migrate schema fixtures in `tests/test_ci.py`, `tests/test_gate_machinery.py` and `tests/test_verify_cheap_first.py` to 4, preserving their independent fault assertions. Keep the top-level name `tests/test_ci.py::test_repository_gate_schema_is_v3` because an existing change ledger names it; update its explanation/assertions to the current schema, retaining cost pins and rejection of older schemas. Update cheap-first history assertions to distinguish conditional skips from gates not reached, and add final real-list activation checks to `tests/test_kit_probe_condition.py`. No bootstrap-only skip ships.
10. Orchestrator: regenerate held `.github/workflows/ci.yml` from `python3 scripts/ci_gates.py --generate-ci` and the generated inventory of `docs/governance/gate-catalog.md` from `python3 scripts/ci_gates.py --catalog`; keep every existing trigger and full probe step unconditional. Change the catalogue prose, `docs/testing.md` and `docs/WORKFLOW.md` to explain always-reached classification, conditional local expensive tests, fail-closed comparison, visible skip evidence and hosted measurement for such a head, retaining the fresh full local pre-phase-6 check.
11. Attempt/orchestrator: run the targeted proofs before acceptance and final checks after activation. Change only this folder's `spec.md` and `plan.md` for implementation status and removal of ledger `not yet written` markers as tests appear. The runner owns evidence in this folder's `findings.md`, measured Time used records and regeneration of `plans/INDEX.md`; it performs commits. No deletions, manifest edit, design file or ADR draft.

## Verification

Use synthetic marker commands rather than recursively running the entire probe in each test. Exercise committed-only changes, index-only changes with the working copy restored to base, unstaged content/mode edits, additions/removals/renames in both states, nonignored untracked files and ignored noise. Use an existing `bestand` file for the skip case; creating one is a membership trigger. Check main's first-parent comparison, a diverged branch, a branch equal to base, shallow/missing refs, detached ambiguity, git failure and malformed manifests. Planted classification failures must go red without calling `fahre()`.

For the general-field proof rename gate IDs and use a plain `paths` condition without kit imports; invalid declarations must fail even with no changed paths. Assert direct legacy command output and `--ci` remain unconditional. Capture skip console output, raw JSONL and the normal history report, and feed output through `stage2.red_sections` without editing `scripts/stage2.py`. A skipped probe has no gate frame, exit status or test seconds; an early-stop remainder has no conditional-skip event. Repeat the skip with refused history storage to retain the existing warning/verdict contract.

For transfer, copy the real manifest's mechanism files into an isolated recipient and use its own manifest/gate list/git history and state root, without source imports; show both skip and trigger with renamed gates. The full final `make verify` exercises the actual expensive probe because this implementation changes travelling files; confirm the hosted strict-probe result on the final PR head as well. No timing benchmark threshold or external service is part of the synthetic proofs.

```sh
python3 scripts/check_interview_minimums.py --change kit-probe-on-kit-change
.venv/bin/python3 -m ruff check scripts/ci_gates.py scripts/kit/probe.py scripts/verify_duration.py tests/test_kit_probe_condition.py tests/test_kit.py tests/test_verify_duration.py tests/test_ci.py tests/test_gate_machinery.py tests/test_verify_cheap_first.py tests/test_gate_catalog.py
.venv/bin/python3 -m ruff format --check scripts/ci_gates.py scripts/kit/probe.py scripts/verify_duration.py tests/test_kit_probe_condition.py tests/test_kit.py tests/test_verify_duration.py tests/test_ci.py tests/test_gate_machinery.py tests/test_verify_cheap_first.py tests/test_gate_catalog.py
bash -n scripts/verify_all.sh
.venv/bin/python3 -m pytest tests/test_kit_probe_condition.py tests/test_kit.py tests/test_verify_duration.py tests/test_ci.py tests/test_gate_machinery.py tests/test_verify_cheap_first.py tests/test_gate_catalog.py -q
python3 scripts/ci_gates.py --check-schema
python3 scripts/ci_gates.py --check-ci
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py
python3 scripts/plans_registry.py --check
make verify
```

The final schema/CI/registry/full checks follow bootstrap and runner index regeneration. At draft base `7c37d013` (2026-11-13), `templates/plan.md` and `scripts/validate_change_artefacts.py` do not exist; this plan follows the phase-3 prompt and existing neighbouring plans. Phase 1 records Stage 2 route `flash`, endpoint `glm-coding-plan`, model `glm-5.3-flash`; no Explore fallback is recorded. `findings.md` contains call evidence only, with no phase-2a rows. Live PR state could not be read because GitHub was unreachable during drafting; current parallel-session state was not read outside this runner's worktree boundary.

Draft checks on 2026-11-13, working tree based on `7c37d013`: the interview-minimums, criterion-ledger and research-handoff commands above passed. Research handoff reports this change exempt because it has no research-swarm/v2 run. The complete registry check was not run: it needs the tracker render, not read beyond this worktree boundary, and the runner has yet to regenerate the index. Full `make verify` and the commit belong to the runner, not this drafting call.

## Criterion ledger

- 1: not yet written tests/test_kit.py::test_classification_mode_keeps_verdict_without_running_tests — planted unclassified/strict-drift or exemption faults pass, or the expensive runner is called
- 2: not yet written tests/test_kit_probe_condition.py::test_manifest_changes_and_travelling_edits_run_probe — committed/index-only/unstaged/mode edits or a newly travelling prefix are skipped
- 3: not yet written tests/test_kit_probe_condition.py::test_membership_changes_always_run_probe — a nontravelling addition/removal/rename/untracked file is skipped
- 4: not yet written tests/test_kit_probe_condition.py::test_only_nontravelling_content_or_no_changes_skip_probe — the expensive marker appears after measured irrelevant or empty changes
- 5: not yet written tests/test_kit_probe_condition.py::test_indeterminate_comparison_runs_probe — missing history, git failure, detached ambiguity or bad manifest yields a skip
- 6: not yet written tests/test_kit_probe_condition.py::test_local_condition_schema_rejects_invalid_declarations — empty, mistyped, escaping or unsupported declarations pass
- 6: not yet written tests/test_kit_probe_condition.py::test_condition_comes_from_declaration_for_any_gate_id — renaming a gate or omitting its condition changes general semantics
- 7: not yet written tests/test_kit_probe_condition.py::test_hosted_and_ci_mode_ignore_local_conditions — generated full probe or --ci execution depends on local path applicability
- 8: not yet written tests/test_kit.py::test_default_full_probe_keeps_all_existing_checks — the standalone strict command skips tests or loses exemption verdicts
- 9: not yet written tests/test_kit_probe_condition.py::test_skip_output_and_history_name_reason_without_pass — a missing skip/base or fabricated pass/timing reaches the output or stored evidence
- 9: not yet written tests/test_verify_duration.py::test_skip_history_is_separate_and_old_history_stays_readable — old records break or skips are counted as executions or accepted without required fields
- 10: not a test — phase-6 review reads docs/WORKFLOW.md, docs/testing.md and docs/governance/gate-catalog.md against criterion 10; false local measurement or a waived fresh full check refutes it
- 11: not yet written tests/test_kit_probe_condition.py::test_transferred_kit_uses_recipient_manifest_and_condition — source-tree dependencies or renamed IDs defeat recipient skip/trigger behavior
- 12: not yet written tests/test_kit_probe_condition.py::test_skip_preserves_early_stop_parser_and_storage_failure_contracts — unreached gates gain skip events, parsed green frames appear, or history failure changes enforcement

## Limits and ownership

The Stage-2 attempt owns unheld implementation/tests and synthetic proofs; the orchestrator owns the held gate list and CI file plus their activation-dependent fixture changes. The declaration is implemented in the reader, never by a gate-ID branch in the runner. Leave `scripts/stage2.py`, `scripts/verify_lock.py`, both kit/export manifests, probe exemptions, all ADRs, model routes, prompts, templates, agent configuration and other change folders untouched. The new test file is already classified by the manifest's `tests/` fallback; no transfer-rule edit is needed. A new manifest-selected test prefix in a synthetic fixture proves dynamic membership without altering real classifications. The orchestrator presents the card unchanged and owns the decision PR for the gate-list edit; this draft neither implements nor commits it.

## Time used
