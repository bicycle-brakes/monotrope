---
title: "Plan — omnigent-test-not-blocking"
status: draft
implementation_status: none
date: 2026-11-12
last_reviewed: 2026-11-12
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-i9df
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-12"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, omnigent, tests]
---

# Plan — omnigent-test-not-blocking

```text
For you:     An Omnigent update adding a tool no longer turns make verify red; installation reports the difference.
Done when:   Synthetic drift is reported without failing installation, rule checks still fail on defects, and make verify is green.
Appetite:    2 hours of phase 4, repairs included — stop at the limit.
Not now:     Policy changes, weaker rule tests, package updates or an upgrade watcher.
Pre-mortem:  suppose it failed: most likely because the advisory report hid a real installation failure.
Starts unless you say stop.
```

## Scope and prerequisites

Baseline: `7bd3d64d`, 2026-11-12. Implement spec criteria 1-5 and the answered
install-time reporting choice; class stays `bounded`, with no design or ADR.
There are no phase-2a rows in `findings.md` at drafting. Explore used Stage 2,
route `flash`, endpoint `glm-coding-plan`, model `glm-5.3-flash`; no fallback
route was recorded. `templates/plan.md` does not exist at this baseline; this
plan follows the phase-3 prompt and the repository's existing plan form.

## Build sequence and files

1. Change `scripts/omnigent_policy.py`: add `--report-surface`, using `_surface()`
   and the union of the existing three lists. Print sorted names separately
   for unclassified and no-longer-offered tools, or an explicit match; catch
   discovery/import exceptions as an explicit comparison-not-performed report.
   This diagnostic returns 0 in every reported case and never writes or changes
   a list. Keep `--surface` JSON output and every existing mode's semantics.
2. Change `tools/omnigent/install.sh`: in install mode, run the existing merge
   first; only on success run the report under the already resolved interpreter,
   also after an unchanged merge. Preserve a failed merge's exit status and
   make only the report invocation advisory. Keep check/remove dispatch,
   terminal guard, interpreter resolution and target selection as they are.
3. Change `tests/test_omnigent_deny_layers.py`: keep
   `test_the_list_matches_omnigents_native_surface` by name because the archived
   criterion ledger references it, but replace its installed-interpreter fixture
   and live equality assertions with a matching synthetic `_surface` and report
   assertions. Add the ledger's tests for added/removed names and read errors,
   patching `_surface` and invoking the real reporting CLI handler in process.
   For installer wiring, use a logging fake interpreter and the existing
   pseudo-terminal pattern: assert merge then report on first/no-op installs,
   no report after a failed merge, unchanged failure status, and no report for
   check/remove. Simulate a failing report process too. All paths stay temporary;
   other installed-code evaluation tests and their skip rules stay unchanged.
4. Change `tools/omnigent/README.md`: explain that install/reinstall reports
   drift without blocking, rule checks remain blocking, and the report neither
   classifies tools nor updates Omnigent. It runs on this policy installer,
   not automatically on arbitrary package-manager upgrades. Leave dated counts alone.
5. Update `plans/changes/omnigent-test-not-blocking/spec.md` only for implementation
   status; update `plans/changes/omnigent-test-not-blocking/plan.md` for time and
   remove `not yet written` as each test lands. The runner regenerates
   `plans/INDEX.md` and stamps dates; the implementation attempt does not edit it.

No files are deleted. No held-path bootstrap edit is needed from the
orchestrator. Do not touch classification tables, generated rules, gate/CI
configuration, archived artifacts, `AGENTS.md`, other change folders or the
maintainer's real Omnigent installation/configuration. Do not suppress other tests.

## Verification

```sh
python3 scripts/omnigent_policy.py --check
.venv/bin/python3 -m pytest tests/test_omnigent_deny_layers.py -q -rs
python3 scripts/check_interview_minimums.py --change omnigent-test-not-blocking
python3 scripts/check_criterion_ledger.py
python3 scripts/plans_registry.py --check
make verify
```

Full verification belongs to the runner. Omnigent-code skips where the package
is absent are existing limits; the new synthetic report and installer tests
must run without it. The prompt's `scripts/validate_change_artefacts.py` is
absent at baseline; use the available gates above, not a claimed validator run.

## Criterion ledger

- 1: tests/test_omnigent_deny_layers.py::test_the_list_matches_omnigents_native_surface — this test still probes the installed version instead of the synthetic matching surface
- 2: tests/test_omnigent_deny_layers.py::test_the_list_matches_omnigents_native_surface — a matching synthetic surface has no explicit match report
- 2: not yet written tests/test_omnigent_deny_layers.py::test_surface_report_names_both_directions_without_blocking — an added or removed name is missing, or drift returns nonzero
- 2: not yet written tests/test_omnigent_deny_layers.py::test_installer_reports_surface_after_each_successful_install — the install or unchanged reinstall omits the report
- 3: not yet written tests/test_omnigent_deny_layers.py::test_installer_preserves_merge_failure_and_ignores_report_failure — a failed merge becomes successful or an unsuccessful report fails installation
- 4: not yet written tests/test_omnigent_deny_layers.py::test_surface_report_states_when_discovery_is_unavailable — an exception propagates or produces silence or a match claim
- 5: tests/test_omnigent_deny_layers.py::test_every_name_is_listed_once_with_a_reason — overlapping classes or an empty reason stops failing
- 5: tests/test_omnigent_deny_layers.py::test_a_hand_edit_or_a_stale_render_is_caught — tampered render no longer yields differences
- 5: tests/test_omnigent_deny_layers.py::test_settings_deny_every_denied_tool — a missing deny rule stops failing
- 5: tests/test_omnigent_deny_layers.py::test_check_names_a_missing_ask_rule_and_an_asked_tool_moved_to_deny_or_allow — broken ask classification stops failing

## Time used
