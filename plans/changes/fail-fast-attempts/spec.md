---
title: "Spec — fail-fast-attempts"
status: draft
implementation_status: none
date: 2026-10-28
last_reviewed: 2026-10-28
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-5tyh
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: gpt-6.1-sol, version: "2026-10-28"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, verification]
class: bounded
appetite: 5.5
adr_files: []
---

# Spec — fail-fast-attempts

Implement and repair attempts reject cheap, detectable failures before full
verification and retain otherwise valid work after restoring runner-owned
findings (bead `coding-harness-5tyh` — fail fast on work attempts).
Research: `research.md`. Decisions: `decisions.md`.

## Problem

- The research addendum records the maintainer's 2026-10-27 measurement:
  first Flash attempts across three lanes failed after 40–55 minutes each;
  full verification consumed 15–24 minutes under that load. One attempt
  spent 2952 seconds on already visible ruff findings and a predictable
  test failure. These are historical observations, not timing targets.
- The same record reports a 1465-second attempt rejected for editing
  `findings.md`, although the runner could restore its own file and assess
  the code. At `1cd54168`, findings snapshots exist but a body edit still
  causes rejection after full verification.
- At that commit the implementation prompt does not require the plan's
  refuting tests before handback. File-only implement and fallback repair
  attempts cannot run commands themselves (research, drafting gap check).

## Terms

- **Cheap checks:** read-only ruff lint and format checks on changed Python
  files, then pytest over explicitly selected tests, after existing safe
  formatting and before `make verify`.
- **Changed files:** changes against the invocation's HEAD, including new
  untracked files and work retained from preceding failed attempts.
- **Selected tests** (amended 2026-10-28, `decisions.md#Q-3`): in a changed
  `tests/**/test_*.py` file, the top-level test functions that are new or
  whose parsed code differs from HEAD (comments and layout alone do not count) (a new file whole); the accepted plan's
  criterion-ledger test references in either test form, as function ids;
  and, on a retry, the test ids pytest reported as failed in the previous
  attempt of the same run; without duplicates. Importers of changed
  `scripts/` modules are not selected.
- **Findings snapshot:** the runner's findings immediately before the model
  call, including this attempt's audit and all preceding evidence.

## Acceptance criteria

1. When an implement or repair attempt's cheap ruff lint or format check
   returns non-zero, that attempt fails before `make verify` starts.
   *Refuted by:* a recorded full verification for that red attempt, or an
   accepted attempt with remaining lint or format violations.

2. When an implement or repair attempt's selected pytest run returns
   non-zero, that attempt fails before `make verify` starts.
   *Refuted by:* full verification or acceptance after an assertion,
   collection or other pytest error in the selected run.

3. When an implement or repair attempt reaches cheap pytest, its explicit
   targets equal the selected tests defined above.
   *Refuted by:* omitting a new or modified test function, a ledger test
   (including one marked not yet written) or, on a retry, a test the
   previous attempt reported as failed; selecting a whole changed file that
   is not new, an importer, a deleted test file or unrelated discovery also
   refutes it. (Amended 2026-10-28, `decisions.md#Q-3`.)

4. If a cheap command's target set is empty, that command is skipped.
   *Refuted by:* invoking ruff or pytest without explicit targets, or
   refusing an otherwise valid text-only attempt merely for having none.

5. When an attempt passes its applicable cheap checks, full `make verify`
   remains required for acceptance.
   *Refuted by:* a checkpoint after cheap green without full verification,
   or acceptance despite red full verification or existing answer checks.

6. When a cheap check rejects an attempt, its identified command, exit or
   timeout and actual failure output enter the existing protected diagnostic
   path for that attempt's findings block and any next attempt's prompt.
   *Refuted by:* losing a short planted failure message, substituting a
   generic failure summary, exposing a planted credential, recording a
   successful verdict, or using a new retry route or extra model call.

7. When an implement or repair prompt is built, it identifies the accepted
   ledger's test references and requires them and ruff before handback for
   command-capable models, with execution explicitly delegated to the runner
   for file-only models.
   *Refuted by:* a missing test reference, absent must-run instruction, a
   command instruction without a file-only delegation, or extra model tools.

8. When an implement or repair attempt edits its findings file, the findings
   snapshot is restored before checks assess the remaining work, without
   the edit alone causing rejection.
   *Refuted by:* a retry solely for that edit despite valid code and answer,
   forged findings reaching checks, loss of earlier evidence, or loss of
   unrelated valid code during restoration.

9. When findings restoration occurs, the attempt's quoted bookkeeping
   records that restoration with the actual accepted or rejected outcome.
   *Refuted by:* an invisible restore, a passing restored attempt labelled
   failed, a fabricated review row, or the notice erasing an audit or an
   earlier attempt's evidence.

10. When a cheap check cannot start or exceeds its bounded execution time,
    the attempt cannot be accepted as cheap-green.
    *Refuted by:* reaching full verification or a checkpoint as though the
    command passed, or a command running without the runner's time bound.

## Non-goals

- Changing routes, models, attempt counts, leak refusal, review-loop or
  research-swarm behavior, draft verification, or model command permissions.
- Replacing or weakening full verification, repair's fixed-line validation
  and red-first proof, recovery safety checks, or protected-path guards.
- Transitive/dynamic dependency discovery, a new plan test list, gate or
  dependency, or a wall-clock speed promise and live model benchmark.
- Restoring arbitrary protected files: this package restores only the
  change's `findings.md`; other unauthorized writes remain refused.
- Design phase 2b and an ADR: this bounded change uses existing runner
  boundaries and the approved attempt ladders.

## Protected areas

- `decisions/`, `docs/adr/`, `provenance.yaml`, `model-endpoints.yaml`,
  `.beads/` and harness configuration retain their existing rules.
- `Makefile`, `scripts/verify_all.sh`, lint configuration, dependency pins
  and tool allow-lists retain their existing measurement and permissions.
- Existing recovery containment, tool-integrity and credential checks
  remain binding before new runner steps or restoration can execute.
- Prior decision records and unrelated/historical change criteria are not
  rewritten to accommodate the new behavior.

## Definition of Done

- `make verify` green with deterministic regressions for criteria 1–10;
  new behavioral tests demonstrated red against the baseline runner.
- Moved with the implementation: `prompts/04-implement.md`, the embedded
  work/repair prompts in `scripts/stage2.py`, and `docs/WORKFLOW.md` describe
  the cheap checks, must-runs, delegation and findings restoration.
- Protected areas untouched and non-goals unbuilt, shown by the PR diff.
- The completed PR closes the fail-fast work-attempt bead
  (`coding-harness-5tyh`) and carries `Closes-Bead: coding-harness-5tyh` on
  its last commit; this drafting call makes no commit or tracker write.
- Special live runs: none; process stand-ins establish command ordering
  and skipped full verification without repeating the measured costly run.

## Open decisions

None open. The maintainer-approved package stands in `decisions.md`, with
two answers of 2026-10-28: four hours of phase 4 (Q-1), raised to 5.5 hours in total the same day (Q-1, note) and the runner, not
the model, runs the must-run checks (Q-2). No ADR answer is added here.

The drafting details there choose deterministic selection, runner delegation
for file-only models, existing safe formatting before cheap checks, visible
restore notices and a phase-4 stop (four hours, raised to 5.5) because each is reversible and
keeps the approved scope. Diagnostics keep existing protection and bounds;
“actual output” does not exempt a secret or an overlong stream from them.
