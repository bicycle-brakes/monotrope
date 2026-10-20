---
title: "Spec — runner-precheck"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-csm
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage2, verification]
class: bounded
appetite: 2
adr_files: []
---

# Spec — runner-precheck

Reject implement and repair attempts whose cheap checks already fail before
paying for full verification, and show the assertion that failed to the next
attempt (bead coding-harness-csm — runner pre-check and assertion evidence).
Sources: `research.md` and the maintainer's answered interview in `decisions.md`.

## Problem

- The measured-time requirement is checked after full verification. Research
  records four attempts lost solely to a missing time entry during the night
  of 2026-10-19/20; each had already paid for `make verify`.
- The attempt's own ledger tests have no early run. At the researched revision
  `ff1e1de`, each hopeless attempt still pays about 5–7 minutes for full
  verification (measurement recorded 2026-10-20).
- Bounded gate tails can omit pytest assertion blocks while retaining only
  truncated failure summaries (maintainer's observation of 2026-10-16,
  recorded in `research.md`). The next attempt then lacks the cause.

## Terms

- **Pre-check:** runner-owned checks before an implement or repair attempt's
  full `make verify`; a passing pre-check is not commit evidence.
- **Ledger test:** a concrete `tests/<path>::test_<function>` entry of this
  change's `## Criterion ledger`; promises and non-test proofs are excluded.
- **Assertion block:** pytest's failure heading, traceback/source context and
  assertion explanation, rather than its final `FAILED` summary alone.

## Acceptance criteria

1. When an implement or repair attempt adds no measured line under
   `## Time used` relative to its pre-call plan, it fails before `make verify`.
   *Refuted by:* full verification starts despite an absent/deleted heading,
   an unchanged time section or merely moving an old line into that section.
2. When changed Python targets remain invalid after the existing safe fixes
   and formatting, or their ruff check cannot run, the pre-check fails before
   ledger tests and `make verify`.
   *Refuted by:* unresolved lint/syntax errors or a missing checker still
   reach pytest or full verification; a clean attempt's safe fix is rejected.
3. When a readable plan has exactly one valid criterion ledger, the pre-check
   runs each distinct concrete ledger test once, with no tests selected from
   promises, non-test entries, fenced examples or other plan sections.
   *Refuted by:* a concrete selector is omitted/repeated, an unrelated test is
   selected, or a ledger with no concrete tests starts an unrestricted suite.
4. If the ledger cannot be read unambiguously, the pre-check reports that
   failure without executing an unvalidated selector or `make verify`.
   *Refuted by:* an unreadable plan, missing/duplicate ledger, malformed row,
   traversal path or target resolving outside the worktree is silently accepted.
5. When the targeted pytest run exits nonzero, cannot start or times out,
   the attempt fails with contextual diagnostics and skips `make verify`.
   *Refuted by:* a failed assertion, collection error, missing selector or
   launch failure reaches full verification or is treated as pre-check success.
6. When a pre-check passes, the existing full `make verify` verdict still
   governs whether an implement or repair attempt can reach its checkpoint.
   *Refuted by:* a green targeted run plus a red full run produces a commit,
   or a red pre-check bypasses the existing bounded retry handling.
7. When targeted pytest or full verification prints assertion blocks, failure
   evidence includes the first blocks in output order ahead of existing tails,
   retaining their assertion explanations within the declared output budget.
   *Refuted by:* a short early assertion disappears behind hundreds of later
   lines or only its truncated `FAILED` summary reaches the next attempt.
8. When diagnostic evidence is returned to retry prompts or persisted in
   findings, it is scrubbed and bounded, with explicit omission markers.
   *Refuted by:* the runner's known credential survives, evidence exceeds its
   declared line/character limits, or truncation silently removes content.
9. While the runner performs the pre-check, its subprocesses retain the
   existing verification environment and command ownership boundary.
   *Refuted by:* a caller credential is forwarded, pytest is delegated to a
   restricted model call, or draft starts requiring an implementation time line.

## Non-goals

- No replacement, relaxation or reordering of the full verification gates;
  no test retry policy, new provider route or model permissions.
- No runner-written measured time entry, timing dashboard or promised speedup.
- No change to repair's separate red-first proof or checkpoint policy.
- No targeted-test pre-check for draft: its separate validation remains intact;
  its existing use of shared full-verification evidence gains richer assertions.
- No dependency, persistent report format or ledger grammar change.
- No design phase or ADR: the bounded change preserves existing boundaries.

## Protected areas

Model endpoint declarations, leak-check rules, model tool permissions,
`decisions/`, `docs/adr/`, workflow prompts and verification gate definitions
remain untouched; they govern contracts this change does not reopen.

## Definition of Done

- Each criterion has its ledger proof and the full `make verify` is green.
- Planning artifacts moving with code: this spec, `plan.md`, `research.md`
  and runner-owned `findings.md`; the registry index is regenerated by the runner.
- The pull request file list shows protected areas and non-goals untouched.
- The pull request closes the runner pre-check work item
  (coding-harness-csm); its final commit carries `Closes-Bead: coding-harness-csm`.
- Special runs: targeted real pytest failures establish diagnostic extraction;
  subprocess stand-ins establish ordering and no checkpoint on a red full run.

## Open decisions

None open. The maintainer's interview answer fixes the scope; the following
reversible details are chosen here with their reasons.

- `[DETAIL]` Use serial targeted pytest initially: no worker startup is owed
  for a handful of tests; timing comparisons remain unmeasured.
- `[DETAIL]` Keep safe fixes and formatting, then check the resulting targets
  strictly; do not parse a human-readable formatter note as a verdict.
- `[DETAIL]` Skip pytest for an empty concrete selection and continue to full
  verification; a promise is not yet an executable proof. Fail an unreadable
  or malformed ledger explicitly so a broad or unsafe command cannot result.
- `[DETAIL]` Retain the first three assertion blocks, at most 60 lines each
  and 180 lines total including labels/omission markers; cap each diagnostic
  line at 500 characters and mark any removed suffix. Scrub before truncating.
  Existing gate and stderr budgets remain separate, preserving their context.
- `[DETAIL]` Limit the targeted subprocess to ten minutes, reusing the runner's
  existing test-proof timeout scale; a stalled cheap check must return to the
  existing retry machinery rather than run indefinitely.
