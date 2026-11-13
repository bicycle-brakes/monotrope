---
title: "Spec — targeted-check-more-verbs"
status: draft
implementation_status: none
date: 2026-11-11
last_reviewed: 2026-11-11
updated: 2026-11-12
supersedes: null
superseded_by: null
bead: coding-harness-0swp
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, model: gpt-6.1-sol, version: "2026-11-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, verification]
class: bounded
appetite: 6
adr_files: [docs/adr/0025-targeted-check-after-repair.md]
neighbours:
  - docs/research/2026-11-09-make-verify-long-term.md
  - plans/changes/repair-targeted-check/spec.md
  - plans/changes/adr-repair-check/decisions.md
---

# Spec — targeted-check-more-verbs

Implement attempts and draft post-checks use targeted verification without
weakening the full checks before phase 6 and in CI; missing tests are refused
early and locally observed misses are counted (bead coding-harness-0swp).
Research: `research.md`. Maintainer answers: `decisions.md`, Q-1 through Q-5.

## Problem

- Implement attempts still request full verification, while draft document
  checks enter the same machine admission as full runs; repair alone uses
  targeted verification (`research.md`, exploration dated 2026-11-10,
  confirmed at baseline `e635f03b` on 2026-11-11). The intent quotes waits of
  44–59 minutes and a 92-minute draft wait; these are attributed observations,
  not measurements repeated by this draft.
- Shared-runner changes cannot safely take the narrow route: both
  `scripts/stage2.py` and selection of the whole `tests/test_stage2.py`
  require full verification. The maintainer explicitly retained this boundary
  (`research.md`, "Why a scripts/stage2.py change always fell back"; Q-3).
- Selection follows direct test links only. An untested new file currently
  buys an expensive full fallback rather than an immediate request for its
  test, and an importer can hide an existing indirect test (`research.md`,
  "How the targeted selection decides"; Q-4).
- The local duration history records full-run outcomes but does not associate
  them with an earlier targeted green; the measurement duty in ADR 0025
  therefore lacks automatic evidence (`research.md`, "Repository follow-up";
  Q-5).

## Terms

- **Targeted check:** whole selected test files, touched-Python lint and
  formatting checks, and applicable gates from the existing gate registry;
  it is never evidence that the full suite passed.
- **Draft document check:** the locally runnable document subset of that
  registry, with existing enforcement, without pytest or other code gates.
- **Reachable test:** a surviving runnable test module linked by the existing
  touch-map rules directly to code, or to an importer connected to that code
  through one or more Python import links. These are static links, not proof
  of runtime coverage. New production code means added Python or shell code
  recognised by the existing inventory, relative to the attempt baseline.

## Acceptance criteria

1. When an implement attempt has safely selectable coverage, every implement
   route uses targeted post-run verification.
   *Refuted by:* a covered attempt on the initial, retry or fallback model
   route launches full verification instead.
   *Basis:* decisions.md#Q-1.
2. When a draft reaches its document check, it runs exactly the locally
   runnable document gates outside machine-wide verification admission.
   *Refuted by:* draft checks wait for admission, inherit its ownership
   markers, launch pytest or a non-document gate, or omit a document gate.
   *Basis:* decisions.md#Q-1; decisions.md#Q-2.
3. When targeted verification replaces an existing post-run route, the
   route's existing prerequisite and acceptance guards remain mandatory.
   *Refuted by:* acceptance bypasses tool integrity, formatting, cheap ledger
   and retry checks, derived preparation, answer proofs, protected-path or
   checkpoint guards; or a draft loses its artifact/card/time-heading checks
   or tolerates any missing ADR answer except its own through the gate's
   existing explicit tolerance.
   *Basis:* decisions.md#Q-1.
4. When an implement or repair delta has safe coverage, selection includes
   every whole surviving touched or reachable test file for the entire delta.
   *Refuted by:* a staged, untracked, retained-retry, deleted or renamed path
   loses its test; a transitive importer is missed; cycles do not terminate;
   or an unchanged failing sibling in a selected file is not run.
   *Basis:* decisions.md#Q-1; decisions.md#Q-4.
5. When the current inventory establishes that new production code in an
   implement attempt has no reachable test, the attempt is refused before
   test execution or admitted full fallback with an instruction to add its test.
   *Refuted by:* a baseline-only or deleted test licenses the new file, an
   unrelated cycle counts as coverage, the attempt checkpoints, or it queues
   for full verification instead of reporting the uncovered file.
   *Basis:* decisions.md#Q-4.
6. If targeted coverage cannot safely be established, verification requires
   the existing admitted full fallback, except for the proven missing-test
   refusal in criterion 5.
   *Refuted by:* a shared-infrastructure edit (including scripts/stage2.py),
   whole tests/test_stage2.py selection, shared test configuration, unsupported
   input, unsafe path, unreadable inventory or uncovered existing code gets a
   targeted green; or absence is asserted from an unreadable inventory.
   *Basis:* decisions.md#Q-1; decisions.md#Q-3; decisions.md#Q-4.
7. If a required targeted command is red, cannot launch or times out, the
   attempt follows the existing failed-attempt path.
   *Refuted by:* the runner checkpoints, marks repair rows fixed, suppresses
   the protected diagnostic, or runs full verification to override that red.
   *Basis:* decisions.md#Q-1.
8. When an implement, repair or draft post-check completes, its runner-owned
   evidence identifies the actual check scope and outcome.
   The evidence adds no block to findings.md: a passing attempt's scope
   stands in the runner's time line in plan.md, a failed attempt's inside its
   one diagnostics block (decisions.md#Q-6).
   *Refuted by:* selected tests/gates or a full-fallback reason are absent,
   draft claims tests it did not run, targeted green is called full green, or
   a passing attempt leaves anything after its audit line in findings.md.
   *Basis:* decisions.md#Q-1.
9. When phase 6 starts or repeats, a fresh full check of the committed head
   must pass before the reviewer is called.
   *Refuted by:* targeted evidence admits the reviewer, a red or moved tree
   reaches it, or CI ceases to run the complete verification suite.
   *Basis:* decisions.md#Q-1.
    (Criteria 10 to 12, the local slip counter, left this change on
    2026-11-13: decisions.md#Q-9; bead coding-harness-bxxt.7 takes them up.)
13. When this change is proposed for merge, the workflow, prompts and
    amendment of ADR 0025 describe the same verification boundaries.
    *Refuted by:* any still requires full verification after every implement
    attempt, requires draft admission, drops the final full gates, or presents
    the amendment as effective before the maintainer merges its decision PR.
    *Basis:* decisions.md#Q-1; decisions.md#Q-2; decisions.md#Q-3;
    decisions.md#Q-4; decisions.md#Q-5.

## Non-goals

- Splitting the runner or its monolithic test file; their full fallback
  remains until the separately tracked split is delivered.
- Coverage instrumentation, new language/import analysis, runtime tracing,
  model-route changes, new gates, changed retry budgets or a reduced CI suite.
- Changing admission internals or unlocking arbitrary calls of
  `verify_all.sh --job docs`; this change removes admission from the draft's
  own document-check path.
- A dashboard, service, uploaded log, CI-slip collector, or a performance
  guarantee derived from the quoted historical waits.
- Phase 2b: no design file is produced because the recorded class is bounded.

## Protected areas

- `scripts/verify_lock.py`, `scripts/verify_all.sh`, `decisions/gates.yaml`,
  `.github/` and `model-endpoints.yaml`: admission, gate declarations, CI and
  endpoint policy retain their existing contracts.
- Other changes' specs, decisions and archived ledgers: preserve their
  historical records and the names of tests they reference.
- Held instructions and ADRs are orchestrator-only bootstrap work after the
  accepted attempt; the implementation model must not edit them.

## Definition of Done

- Criterion regressions and `make verify` are green after bootstrap edits;
  phase 6 still performs its own fresh full check.
- Move `docs/WORKFLOW.md`, `AGENTS.md`, `prompts/04-implement.md`,
  `prompts/04b-review-loop.md`, the local handover skill
  `tools/claude-code/skills/handover/SKILL.md`, and the amendment to
  `docs/adr/0025-targeted-check-after-repair.md` with the code.
- The decision PR uses the decision template and label; only its merge
  accepts the ADR amendment. No new ADR or maintainer answer is invented.
- The file list demonstrates the protected areas and non-goals were respected.
- The PR closes the targeted-verification extension work item
  (coding-harness-0swp); its final commit carries
  `Closes-Bead: coding-harness-0swp`.

## Open decisions

None open. The five maintainer answers are recorded in `decisions.md`.

- [DETAIL] Six hours is the initial phase-4 appetite, including repairs,
  because the change combines routing, graph selection and local measurement;
  this is a stop governed by the existing appetite protocol.
- [DETAIL] Draft uses the shared selector's document-only projection, because
  Q-2 explicitly describes text checks without tests; additions of plan
  Markdown do not summon the code/kit probe in this projection.
- [DETAIL] Reuse existing static link semantics, including their limits for
  ambiguous or dynamic imports; add transitive traversal without claiming
  runtime coverage. An unreadable graph remains unmeasured, not empty.
