---
title: "Research — test-strength-rows"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-y17
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage2, repair, red-first, test-strength, planted-fault]
---

# A test-strength finding has no red-first form — Research

Phase 1 for bead coding-harness-y17, read on 2026-10-14 against `origin/main`
at `3199a28` and the unmerged branch `origin/feat/codex-repairs` (pull
request #138) at `135cb8e`. Exploration only, during the night run; the
questions below wait for the maintainer.

## Result first

- The repair verb knows two answers: a test that must be **red on the
  baseline's code**, or `not a test`, which is allowed only for a row the
  orchestrator took as `taken — not a test`. A row that says "this test is
  too weak, the code is right" fits neither: the strengthened test is green on
  the baseline by construction, so the red-first proof can never pass.
- Today such rows are re-taken as `not a test` by hand and carry no proof at
  all. Three rows in this tree (`3199a28`) say so in their Status ("a
  test-strength row"); the handover of 2026-10-13 counts five across two
  changes (the other two not found in the tree; not read where they stand).
- The check is unchanged on PR #138: same `red_first`, same
  `check_repair_answer`, same answer text (moved into `REPAIR_ANSWER`).
- The repository already has the idea the bead names: tests carry
  "Planted fault:" comments (139 in `tests/test_stage2.py`), and
  `prompts/05-verify.md` requires every new gate to be shown red against a
  planted fault. What is missing is a form the runner can execute.

## What exists today

### The answer form and its check (`scripts/stage2.py`, `main`)

- `REPAIR_FORMAT`: "`<ID>: fixed — tests/<path>::<function>` or `<ID>: fixed
  — not a test — <reason>` … A code row needs a test that fails on the
  baseline's code, which the runner runs; only a row taken as `taken — not a
  test — <reason>` may be answered `not a test`."
- `RECORD_INTRO` (the loop record): Status is `taken — <test or criterion>`,
  `taken — not a test — <reason>` or `rejected — <reason>`. There is no
  third kind of taken row.
- `fixed_status` parses the line; `FIXED_TEST` matches
  `tests/<file>.py::test_<name>`.
- `check_repair_answer`: a `not a test` answer on a row not taken as `not a
  test` fails ("the row is a code row; it needs a test that was red first");
  every named test goes to `red_first`.
- `red_first`: a temporary `git worktree` at the **baseline**, the attempt's
  whole `tests/` copied over it, one `pytest` of the named function; exit 1
  or 2 is red, anything else fails the attempt with "pytest ended <n> on the
  baseline's code; red first is exit 1 or 2". It never sees the attempt's
  code — only the attempt's tests.

### PR #138 (`135cb8e`)

- `REPAIR_ANSWER` carries the same sentences; `REPAIR_FORMAT` (Codex, may run
  commands) and `REPAIR_FORMAT_FILE_TOOLS` (Sonnet) prepend to it.
- `red_first` and `check_repair_answer` unchanged in substance; the
  "pytest ended … on the baseline's code" message is the same.

### Doctrine

- `prompts/04-implement.md`, "Repair": "A code row needs a test that is red
  first — it fails on the baseline's code".
- `prompts/04b-review-loop.md`, "The evidence rule": a finding is taken only
  when a test demonstrates it or the spec supports it; Status forms as in
  `RECORD_INTRO`.
- `docs/WORKFLOW.md`, "Two columns for every stage-2 change": `Broke a test`
  excludes the finding's own new test, "the evidence rule expects it to be
  red first".
- `prompts/05-verify.md`: "Every new gate comes with its mutation: plant the
  fault, watch it go red, take it back."

### Evidence of the bug

- `plans/changes/stage2-format/findings.md`, row L1-1 (deepseek-v4.1-flash):
  three attempt blocks with "pytest ended 0 on the baseline's code"; Status
  finally "fixed — not a test — a test-strength row: … green on the
  baseline's code, for the runner records every attempt's line already, so no
  red-first proof exists".
- Same file, row L2-1 (mimo-v2.6-flash), and
  `plans/changes/codex-drafts/findings.md`, row L1-6 (deepseek-v4.1-flash):
  both closed as "not a test — a test-strength row … (bead
  coding-harness-y17)".
- `docs/journal/handover/2026-10-13-night-run-second.md`, section 4: "Red
  first has no form for a test-strength row … the repair verb failed all
  attempts on them until they were taken as `not a test`."
- Note: L1-1 and L2-1 each name the fault the weak test misses in the
  finding text itself ("a run that dropped an earlier attempt's format line";
  "the second snapshot taken after `verify_attempt`"). The fault is usually
  already in the row.

## What a red-first proof of a test-strength row can be

For a code row the runner shows: new test, old code → red. For a
test-strength row the code is right, so the comparison has to be: new test,
**the attempt's code with the named fault planted** → red; and the same test
on the attempt's code → green (which `make verify` already shows).

## Candidate forms

1. **A planted fault as a patch, run by the runner.** The answer line names
   the test and a fault file, e.g. `<ID>: fixed — tests/<path>::<function> —
   fault <change folder>/faults/<ID>.patch`; the runner checks out the
   attempt's tree in a temporary worktree, applies the patch, and requires
   exit 1 or 2.
   - For: mechanical, same machinery as `red_first`; the patch is evidence
     that stays in the change folder.
   - Against: who guarantees the patch plants the fault the row names, not a
     trivial one (a deleted function makes any test red)? A reviewer or the
     orchestrator must read it. A model without command tools has to write a
     unified diff by hand.
2. **The orchestrator names the fault when taking the row.** A new Status
   `taken — test strength — <fault>`; the repair model writes the patch; the
   runner applies it as in 1.
   - For: the fault is chosen by the side that decided the finding, not by
     the model being checked; the reviewer's finding text usually holds it.
   - Against: one more Status form across `RECORD_INTRO`,
     `prompts/04b-review-loop.md`, the record parser and the release.
3. **Old test versus new test on the planted fault.** As 1 or 2, plus: the
   baseline's version of the test must be **green** on the planted fault.
   - For: the strongest statement — the old test missed the fault, the new
     one catches it; a trivial fault fails this.
   - Against: needs the old test to exist under the same name; a renamed or
     new test has no old version.
4. **Formalise the workaround.** A taken `test strength` row may be answered
   with a named test that must be green; no red proof.
   - For: smallest change; ends the failed attempts.
   - Against: the evidence rule loses its proof exactly for rows about weak
     evidence.

## Which files a change would touch

- `scripts/stage2.py`: `REPAIR_FORMAT` (on #138 `REPAIR_ANSWER`),
  `RECORD_INTRO`, `FIXED_TEST`/`fixed_status`, `check_repair_answer`, a
  sibling of `red_first` that checks out the attempt's tree instead of the
  baseline; the record parsing (`record_rows`, `undecided`) if a Status form
  is added.
- `tests/test_stage2.py`: beside `test_a_named_test_that_is_not_red_first_fails_the_attempt`.
- `prompts/04-implement.md` (Repair), `prompts/04b-review-loop.md` (Status
  forms, evidence rule), `docs/WORKFLOW.md` §4 ("Repairing taken findings",
  "Two columns").
- With PR #138 unmerged, the repair verb's prompt and answer constants move
  there; this change waits for it or rebases onto it.

## Questions this change has to answer

- [DECISION] Does a test-strength row need a red proof at all? (a) yes,
  against a planted fault the runner applies (candidates 1–3, recommended:
  candidate 2 — the orchestrator names the fault when taking the row, the
  repair model writes it as a patch); (b) no, a named green test suffices
  (candidate 4).
- [DECISION] Whether the proof also requires the baseline's version of the
  test to stay green on the planted fault (candidate 3). Recommended: yes
  where the old test exists under the same name, because it is the only check
  that rejects a trivial fault without a human reading the patch.
- [DECISION] Whether this change waits for pull request #138 (recommended:
  yes — it rewrites the repair verb's prompt constants).
- [GAP] The two test-strength rows the handover counts beyond the three
  found: in which change they stand (not read; perhaps in the loop record
  outside the tree, `~/.local/state/coding-harness/stage2/<change>/loop.md`).
- [GAP] Whether `git apply` of a model-written patch is reliable enough for
  the Sonnet route, which has file tools only; a fault expressed as
  "replace this exact text in this file with that" may be safer. One trial on
  the L1-1 case settles it.
- [DETAIL] The planted-fault run reuses `red_first`'s guards (temporary
  worktree, ref comparison, time limit, interpreter check), started from the
  attempt's tree rather than the baseline; no second mechanism.
- [DETAIL] The fault patch lives in the change folder, so it is part of the
  checkpoint commit and readable in review; it is never applied outside the
  temporary worktree.
