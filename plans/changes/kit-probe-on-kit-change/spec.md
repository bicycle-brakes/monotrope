---
title: "Spec — kit-probe-on-kit-change"
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
tags: [spec, verify-speed, kit, gates]
class: bounded
appetite: 4
adr_files: []
neighbours:
  - plans/changes/verify-cheap-first/spec.md
  - plans/changes/repair-targeted-check/spec.md
  - plans/changes/archive/2026-11-06-verify-stages-new-files/spec.md
  - plans/changes/archive/2026-11-06-verify-absolute-python/spec.md
  - docs/research/2026-11-09-make-verify-long-term.md
  - docs/research/2026-11-12-test-strategy-draft.md
  - docs/research/2026-11-04-verify-duration-baseline.md
---

# Spec — kit-probe-on-kit-change

Local full verification omits the expensive empty-repository test run only
when a measured change does not affect the kit, keeping classification
unconditional and hosted verification exhaustive (bead coding-harness-w2ay).
Research: `research.md`. Maintainer decisions: `decisions.md#Q-1` through Q-4.

## Problem

- The research records a 200 s median kit probe over the local full runs
  measured through 2026-11-09, even when their changes do not affect the kit
  (`docs/research/2026-11-09-make-verify-long-term.md`). This is historical
  cost evidence, not a promised duration saving for every run.
- At `7c37d013` (2026-11-13), `scripts/kit/probe.py` combines classification
  and the throwaway test run, and `scripts/verify_all.sh` executes the whole
  selected gate. Skipping it wholesale would also lose classification.
- At that commit, schema 3 of the one gate list declares no local change
  condition, and duration history records executed gates only. Neither an
  invisible skip nor a runner-specific path list meets the four answers.

## Terms

- **Classification:** the existing cheap checks before the throwaway test
  run, including tracked/untracked classification, the nonempty travelling
  set, and exemption reasons and cap; existing strictness remains applicable.
- **Travelling file:** a path classified `mechanismus` by the kit manifest's
  existing longest-prefix rule; no independently maintained kit path list.
- **Measured change:** the union of committed branch changes, staged changes,
  unstaged changes and nonignored untracked files against the comparison base.
  Index and working-tree states are considered separately; a staged change
  cannot disappear merely because its working copy matches the base.
- **Comparison base:** the merge base of `HEAD` and `origin/main` on a named
  feature branch; the first parent on `main`. A detached checkout can use a
  distinct merge base, but one at `origin/main` is indeterminate and runs the
  probe. Missing or insufficient history is indeterminate too.
- **Membership change:** an addition or removal in any measured state,
  including a rename and a nonignored untracked file, regardless of kit role.
- **Reached gate:** a gate selected for this job and placement before a
  preceding blocking failure stops local execution.

## Acceptance criteria

1. When local full verification reaches kit classification, it applies the
   existing classification verdict without starting the throwaway tests.
   *Refuted by:* an unclassified tracked file passing, strict untracked
   drift passing, or classification invoking the expensive test runner.
   *Basis:* decisions.md#Q-2.

2. When the measured change affects a travelling file, the kit manifest or
   the probe itself, local verification runs the expensive probe when reached.
   *Refuted by:* a committed, staged, unstaged or mode-only travelling edit
   being skipped, or a new manifest rule failing to join the trigger set.
   *Basis:* decisions.md#Q-1.

3. When the measured change includes any membership change, local
   verification runs the expensive probe when reached.
   *Refuted by:* an added, removed, renamed or nonignored untracked
   nontravelling file allowing a conditional skip.
   *Basis:* decisions.md#Q-1.

4. When the measured change has no kit-affecting edit or membership change,
   local verification skips the expensive probe when reached.
   *Refuted by:* a content-only edit to an existing `bestand` file launching
   the throwaway tests, or an empty measured change launching them.
   *Basis:* decisions.md#Q-1; decisions.md#Q-4.

5. If the comparison or manifest classification cannot be measured reliably,
   local verification does not conditionally skip the expensive probe.
   *Refuted by:* a missing base, unusable git result, malformed manifest or
   indeterminate detached checkout being treated as an empty change.
   *Basis:* decisions.md, "Decided by the agent"; decisions.md#Q-1.

6. When a gate declares a local change condition, the gate-list schema
   validates that declaration and its shared reader determines applicability.
   *Refuted by:* an invalid declaration passing, a renamed gate changing the
   result, an undeclared gate becoming conditional, or a kit path list in the
   shell runner overriding the declaration.
   *Basis:* decisions.md#Q-3.

7. When hosted verification or the runner's `--ci` mode selects the kit
   probe, it runs the full strict probe without a local change condition.
   *Refuted by:* a no-kit-change input removing or conditionally bypassing
   the probe on a pull request, main push, merge group or `--ci` execution.
   *Basis:* decisions.md#Q-1; decisions.md#Q-4.

8. When the existing standalone full probe command is invoked, it retains
   its classification and throwaway-test verdict.
   *Refuted by:* `python3 scripts/kit/probe.py --strict` becoming conditional
   or omitting existing unexplained-red, orphaned or expired exemptions.
   *Basis:* decisions.md#Q-2; research.md, "The probe itself".

9. When the expensive probe is conditionally skipped, the output and run
   history identify that skip and its measured reason as distinct from a pass.
   *Refuted by:* a missing skip, a missing comparison base in its reason,
   a fabricated exit status or test duration, or a history report counting
   skipped tests as executed tests.
   *Basis:* decisions.md#Q-4.

10. When a full local check before phase 6 conditionally skips the expensive
    probe, the workflow identifies hosted CI as that head's probe measurement.
    *Refuted by:* the workflow claiming a local probe measurement, waiving
    fresh full local verification, or catalogue/testing text promising an
    unconditional expensive local probe.
    *Basis:* decisions.md#Q-4.

11. When the mechanism is transferred with the kit manifest, the local
    condition and classification work using only the recipient's files.
    *Refuted by:* imports from the source checkout, missing transferred
    dependencies, a second trigger list, or a renamed recipient gate losing
    the declared condition.
    *Basis:* decisions.md#Q-1; decisions.md#Q-3.

12. When the runner handles execution, conditional skips preserve its
    existing enforcement, early-stop and duration-storage-failure behavior.
    *Refuted by:* a skipped gate appearing as a parsed green gate section,
    a gate after a blocking failure acquiring a conditional-skip event,
    an unrelated gate not running on green, or broken history changing the
    verification verdict rather than warning that evidence was not recorded.
    *Basis:* decisions.md#Q-4; research.md, local runner and evidence consumers.

## Non-goals

- Reusing successful probe results, caching, changing pytest parallelism,
  reducing the probe's tests or relaxing its exemption ratchet.
- Changing targeted repair selection, replacing fresh full local phase-6
  verification with hosted evidence, or adding a nightly probe schedule.
- Migrating sibling repositories, changing model routes, adding a dashboard,
  or changing other gates' applicability.
- Phase 2b and an ADR draft: the class remains `bounded`; the manifest and
  gate list retain their existing authority as the maintainer answered.

## Protected areas

- `scripts/stage2.py` and the targeted repair contract: this change concerns
  full local verification; explicit targeted probe calls remain unconditional.
- `scripts/kit/manifest.yaml`, `scripts/export/manifest.yaml`, probe exemption
  entries/cap/reasons and `scripts/verify_lock.py`: no transfer membership,
  admitted failures or admission policy changes are needed.
- ADRs, model endpoints, provenance policy and other change folders: no
  architecture decision, routing change or unrelated cleanup is authorized.

## Definition of Done

- `make verify` green after the orchestrator's gate-list/bootstrap edits.
- Updated together: `decisions/gates.yaml`, generated
  `.github/workflows/ci.yml`, `docs/governance/gate-catalog.md`,
  `docs/testing.md`, `docs/WORKFLOW.md` and this change's spec/plan/ledger.
  The runner regenerates `plans/INDEX.md` outside this drafting attempt.
- The pull request's file list shows protected areas untouched and non-goals
  unbuilt; its held gate-list edit follows the decision-PR procedure.
- The pull request closes bead coding-harness-w2ay (conditional local kit
  probe); its last commit carries `Closes-Bead: coding-harness-w2ay`.
- Evidence includes the isolated trigger/skip matrix, a transferred-kit
  proof and the full hosted probe check, each tied to its tested commit.

## Open decisions

None open. The four maintainer answers are used as recorded, not answered
again here. The following reversible details are explicit agent choices:

- [DETAIL] Compare the full branch plus index/worktree/untracked states using
  the repository's existing interview-gate base convention. This avoids
  overlooking committed or index-only edits; no previous successful run is
  needed. Recheck on every invocation, without caching.
- [DETAIL] Use an optional general local-condition field in schema 4;
  gates without it stay unconditional. A schema bump prevents an older reader
  from silently ignoring a new skip declaration.
- [DETAIL] Retain the existing full probe command and add a classification
  mode. The full mode may repeat cheap checks after the standalone cheap gate;
  preserving existing callers is preferable to another full-mode contract.
- [DETAIL] Allow four hours of phase 4 including repair rounds, as a stop;
  no appetite was set in the interview. This bounds the schema/runner/log
  change without promising a runtime speed threshold.
