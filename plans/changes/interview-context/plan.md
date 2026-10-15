---
title: "Plan — interview-context"
status: draft
implementation_status: partial
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-zs7
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, questions, context, gates]
---

# Plan — interview-context

```text
For you:     Every question explains its intention and its effects on the repository and architecture before asking.
Done when:   Missing context in new answered records makes verification fail, older answers stay exempt, and the kit probe and make verify pass.
Appetite:    4 hours of phase 4, including repairs; stop at the limit.
Not now:     Backfilling older answers, grading clarity automatically, or adding profile switches.
Pre-mortem:  suppose it failed: most likely because the gate uses change dates instead of each answer's recording day.
Starts unless you say stop.
```

## Build

Implement the separate `question-context` gate; keep interview counting intact.
Explore ran on Stage 2, route flash, endpoint glm-coding-plan, model
glm-5.3-flash, 2026-10-14; no Stage-1 fallback is recorded.

1. Write fixture-first tests for the gate's command. Discover live and archived
   `decisions.md` files without requiring specs; parse real level-two Q-records
   outside fences, and keep indented context inside its value. Check every
   `status: answered` occurrence, not just records counted toward a minimum.
2. Read the cut-off only through `adoption.adopted_on(root, "question-context")`.
   Read each recording day from exactly one em-dash date (`— YYYY-MM-DD`)
   anywhere in its top-level MADR paragraph beginning `In the context of`;
   join indented wraps and blank-separated dash/date continuations,
   including the dash/date split in this change's fifth answer. Ignore dates
   in context, fields and examples. Dates before adoption are exempt; the
   adoption day and later are subject, even with an earlier `asked` date or
   old spec. A changed answer gets its actual new recording day.
3. For subject records accept one non-blank context text scalar, including a
   multiline literal block; missing, whitespace, non-text or duplicate values
   exit 1. Decode only the context scalar, not the whole Markdown record;
   unquoted null, booleans, numbers and collections are not text. Do not score
   wording or enforce headings in the gate. Absent, invalid or ambiguous
   applicability evidence and unreadable files exit 3;
   collect all findings, with exit 3 taking precedence over exit 1. Success
   exits 0. CLI diagnostics name the file and Q-id, and support `--root`.
   Record and adoption files remain byte-for-byte unchanged by the command.
4. Publish the context form in the workflow and general instructions: Topic,
   Intention (including why now), Today, Repository change, Architecture change;
   short explanations in that order precede options, and the question stands
   last. Explain terms at first use; an unchanged area says why. Translate labels
   in conversation and preserve shown meaning in English records. Keep the MADR
   decision form and present the five-part preface before an unchanged plan card.
   The interview prompt keeps its header model line and the strings its tests
   pin (`answered_by`, `status: skipped`, `## SKIP · interview` —
   tests/test_check_interview_minimums.py::test_interview_prompt_defines_the_records,
   scripts/kit/probe.py).
5. Register the blocking gate for both placements, add its script/tests to the
   kit, and record this repository's intended merge day. Align that day before
   merging if the calendar day changes; never advance an adopted day to pass.
   The orchestrator supplies original displayed context for any existing answer
   dated on/after adoption. If it is unavailable, stop rather than fabricate
   context or change the cut-off. Review the ADR against Q-1 to Q-5.

## Files

- `AGENTS.md`: add the universal standing rule, fixed form and ADHD rationale.
- `docs/WORKFLOW.md`: state the portable rule, context record, inclusive
  recorded-answer cut-off and presence-only gate in the question protocol
  and gate table.
- `prompts/01a-interview.md`: replace the free context paragraph with the fixed
  form and show `context: |` in the record with its actual decision recording day.
- `prompts/02-spec.md`: prefix its MADR question block with the context form and
  put the actual question last without dropping the existing decision information.
- `prompts/03-plan.md`: require the context preface when showing the unchanged
  card; `plan.md` still opens with the card and asks for no additional approval.
- `scripts/check_question_context.py`: create the standalone read-only gate and
  CLI with the record/date/value rules above; import the existing adoption reader.
- `tests/test_check_question_context.py`: create independent fixtures, CLI
  mutations, cut-off cases, instruction/form pins and kit membership checks;
  skip only the AGENTS assertion when that inventory file is absent, retaining
  the workflow and prompt assertions in the kit probe.
- `decisions/gates.yaml`: register `question-context` with `title` and
  `reason` like its neighbours, command
  `python3 scripts/check_question_context.py`, job verify, enforcement block,
  floor false, placement both; no tracker or history hydration is needed.
- `decisions/adoption.yaml`: add the new gate's actual adoption day through the
  decision PR, preserving the interview-minimums day.
- `tests/test_this_repository_adoption.py`: add a local assertion that the
  question-context day is the merge day prepared for this PR, updating it with
  the adoption entry if that day changes; keep the interview-minimums assertion.
- `scripts/kit/manifest.yaml`: add explicit mechanism entries for the new gate
  and test file; retain the workflow/prompts prefixes and local adoption record.
- `docs/adr/0018-every-question-carries-its-context.md`: carry the draft into the
  decision PR, retaining pending review and acceptance only by merge.
- `plans/changes/interview-context/decisions.md`: only if its answers are subject,
  the orchestrator adds their actual presented contexts; this draft leaves it intact.
- `plans/changes/interview-context/spec.md`, `design.md`, `plan.md`, `research.md`
  and `findings.md`: retain the agreed contract, record verified implementation
  evidence/time and resolve review rows without inventing maintainer answers.
- `.github/workflows/ci.yml` and `plans/INDEX.md`: regenerated from their sources
  by the runner; neither is hand-edited.

No files are deleted. The orchestrator owns tracker, commits, PR and session
handover. Leave `scripts/check_interview_minimums.py`, its counting tests,
`scripts/adoption.py`, ADR-answer files, glossary pointers, other phase prompts,
card templates, harness configuration and sibling repositories untouched.

## Criterion ledger

- 1: tests/test_check_question_context.py::test_general_rule_covers_all_questions — remove conversation or review ambiguities from the rule
- 2: tests/test_check_question_context.py::test_question_forms_put_context_before_options_and_question_last — remove Intention or Architecture change from a form
- 2: tests/test_check_question_context.py::test_plan_card_requires_preface_and_preserves_veto — move the preface after the card, remove a context part, require an extra approval or alter the card's fields
- 3: not a test — phase-6 review presents a sample decision and a review ambiguity in isolation; an unexplained identifier or reliance on prior chat refutes it
- 4: tests/test_check_question_context.py::test_interview_record_has_a_dedicated_context_field — remove the context field from the record example
- 4: tests/test_check_question_context.py::test_interview_minimums_still_counts_a_record_with_a_context_field — a record with a context block stops counting toward the interview minimum
- 4: not a test — review compares recorded meaning with the context actually shown; an invented explanation or omitted part refutes fidelity
- 5: tests/test_check_question_context.py::test_missing_context_goes_red — delete only the subject record's context and require exit 1 with its file and Q-id
- 5: tests/test_check_question_context.py::test_empty_or_non_text_context_goes_red — replace context by whitespace, an empty literal block, null or a collection
- 5: tests/test_check_question_context.py::test_date_or_timestamp_context_goes_red — accept an unquoted date or timestamp as context text
- 5: tests/test_check_question_context.py::test_context_cannot_be_borrowed_from_another_record — put context only in another Q-block or outside all records
- 5: tests/test_check_question_context.py::test_every_answered_occurrence_needs_context — exempt a duplicate Q-id or an agent-attributed answered record
- 6: tests/test_check_question_context.py::test_nonblank_context_passes_without_clarity_scoring — reject a plain scalar or multiline explanation on wording alone
- 7: tests/test_check_question_context.py::test_adoption_day_and_later_answers_are_subject — change the comparison from inclusive to strict or select by spec/asked date
- 7: tests/test_check_question_context.py::test_answer_date_uses_wrapped_decision_suffix — take a date from context or fail to read an indented or blank-separated dash/date split
- 7: tests/test_check_question_context.py::test_archived_and_spec_less_answers_are_subject — move a missing-context answer into the archive or remove its spec
- 7: tests/test_check_question_context.py::test_examples_open_and_skip_records_are_not_answers — count fenced examples or skip/open blocks as answered records
- 8: tests/test_check_question_context.py::test_older_answers_stay_exempt_in_mixed_files — require backfill or let an old answer exempt the whole file
- 8: tests/test_check_question_context.py::test_gate_never_writes_records_or_adoption — fill an older record or move the adoption day while checking
- 9: tests/test_check_question_context.py::test_unreadable_evidence_is_not_a_pass — return 0 for missing/invalid adoption, absent/ambiguous decision dates or an unreadable file
- 9: tests/test_check_question_context.py::test_wrapped_date_cannot_come_from_another_field_or_example — borrow the recording day from context, a field, another paragraph or a fenced example
- 9: tests/test_check_question_context.py::test_unmeasured_evidence_takes_exit_precedence — return 1 after one context failure hides another record's unknown date
- 10: tests/test_check_question_context.py::test_gate_is_blocking_in_both_placements — omit the command or change enforcement/placement
- 10: tests/test_ci.py::test_no_blocking_gate_step_carries_continue_on_error — allow the derived hosted step to ignore a failure
- 10: tests/test_ci.py::test_every_gate_step_has_a_mutation_test — add the gate without an executable seeded failure case
- 11: tests/test_check_question_context.py::test_context_gate_and_tests_travel_with_the_principle — leave a dependency to the inventory catch-all or add a profile switch
- 11: not a test — `python3 scripts/kit/probe.py --strict` checks the portable copy; missing mechanism files or this repository's adoption data in it refute the criterion
- 12: not a test — phase-6 review compares the single claimed ADR to Q-1 through Q-5 and the PR file list; a changed answer, second draft or unmade approval refutes it

## Verification

Run `make venv` once if this checkout lacks its locked environment. Then:

```bash
.venv/bin/python3 -m pytest tests/test_check_question_context.py tests/test_this_repository_adoption.py tests/test_check_interview_minimums.py tests/test_ci.py -q
.venv/bin/python3 scripts/check_question_context.py
.venv/bin/python3 scripts/check_interview_minimums.py --change interview-context
.venv/bin/python3 scripts/check_criterion_ledger.py
.venv/bin/python3 scripts/ci_gates.py --check-schema
.venv/bin/python3 scripts/kit/probe.py --strict
make verify
```

Replace each `not yet written` ledger entry with a test entry when its function
exists. Seed the missing-context mutation in a fixture that first passes, then
remove only that record's context and assert exit 1 and its diagnostic; the
test names already satisfy CI's mutation-evidence form. Keep the kit test
dependent only on mechanism files and fixture adoption days.

The runner prepares derived files before full verification; do not claim the
absent change-artefact validator ran. Recording the maintainer's ADR answer
is an orchestrator prerequisite for ordinary verification, never a guessed
answer or an implementation-side tolerance. Review semantic criteria separately.

## Draft handoff — 2026-10-14

Attempt 3 (glm) revised these three artifacts only, on `docs/interview-context`
at `c7fa059`; implementation has not started. The runner owns verification, the
one commit and tracker writes, and this call ran no command — every claim above
was read from the tree. No phase-2a rows are open in `findings.md`; it holds
the runner's attempt log.

The artifacts keep the header, ledger and record forms that attempt 2's run
left green in every gate except pytest; the two attempts' failures lie outside
this change (session-policy tests in the sandbox; a tracker render that was
not byte-stable) and are no draft repair. The artifact validator command still
exits 2 because its script is absent at this commit.

Resume: the runner runs full verification and commits only on green, then the
orchestrator presents the unchanged card and starts phase 4. Before enabling
the new gate, recover authentic context for any interview answers whose
recording day is on or after the actual merge day.

## Runner route — 2026-10-14

Stage-1 route: implement · model claude-sonnet-5-5 · reason: two Flash post-run checks failed.

## Time used

2026-10-14, span not measured: this session had file tools only and could not read `date`; no estimate is written. The appetite stop is therefore not evaluated for this span.

2026-10-15 01:11:51–01:14:38, 2m 47s (CEST, UTC+02:00).

Repair attempt 2 (Codex) retained and verified the first attempt's
plan-card and YAML date/timestamp fixes. The plan-card test rejects moving
the preface after the card, deleting any of its five parts, reversing the
ordering instruction, or adding text after the veto. The scalar test
rejects four unquoted date/timestamp forms while accepting quoted and
literal-block text. The criterion ledger now names this regression test.

A temporary copy of baseline f47745d with the current tests produced five
expected failures: the plan-card test and four date/timestamp cases. The
current question-context test module passed all 36 tests. The adjacent
adoption, interview-minimums and CI test modules produced 150 passed,
2 skipped and 1 failure: the CI exception-reason test could not open the
tracker database under the sandbox permissions. No tracker repair was
attempted.

The metadata correction in f47745d already sets all six artifacts and
the generated index to partial, and records the adoption-day author and
reason. This attempt refreshed stale updated headers in the four
artifacts reported by the first post-run check and in this plan. The
frontmatter-current, criterion-ledger and question-context gates, Ruff
checks and git diff --check passed. The inherited findings file was not
edited. The runner owns full verification and the checkpoint commit.

Resume: when I start, I will run `make verify` through the repair runner.


### Repair of L2-1 and L2-2 — 2026-10-15

2026-10-15 03:08:14–03:15:29, 7m 15s (CEST, UTC+02:00).

L2-1 uses the explicitly permitted documentation correction: exactly one
em-dash date anywhere in the decision statement supplies the recording day.
A historical answer includes a recording note after its date; requiring the
date at the end made that readable evidence unmeasured. The module and
function docstrings, workflow protocol and gate table, diagnostic and Build
step 2 now describe the accepted position. Historical answers were not edited.
The orchestrator records the choice and row status in findings.md.

L2-2 joins indented statement continuations and blank-separated dash/date
lines without borrowing dates from fields, another paragraph or fenced
examples. The existing ledger test now plants both wraps, verifies a readable
record passes, then removes its context and checks both its failure and an
archived record's failure without an unmeasured verdict. The added boundary
test is named in the ledger.

Before the script changed from baseline f3b00bd, the wrapped-date regression
produced five expected failures and one passing flush-left split. After the
repair, the question-context, repository-adoption and interview-minimums test
modules passed all 121 tests. The repository question-context command read
55 answered records successfully. The criterion-ledger, frontmatter-current,
interview-minimums and gate-schema checks, Ruff check/format checks and
`git diff --check` passed. No make verify or kit probe is claimed here; the
runner owns full verification and the checkpoint commit. This attempt made
no commit and did not edit the inherited findings file.

Measured repair spans now total 10m 2s; the earlier unmeasured
implementation span remains unknown and is not estimated.

Resume: when I start, I will run `make verify` through the repair runner.

### Repair of L3-1 and L3-2 — 2026-10-15

2026-10-15 03:44:23–03:47:40, 3m 17s (CEST, UTC+02:00).

L3-1 checks inline context by its parsed YAML scalar type and value rather
than the raw line. Block-scalar headers recognize trailing comments before
their content is checked. Empty blocks, empty quoted strings and block
sequences are rejected with and without comments; non-blank plain, quoted,
literal and folded text still passes, including a hash inside quoted text.

The expanded empty/non-text and non-blank tests ran before the script
changed from baseline 7b3e46c: nine expected failures demonstrated the
bypasses and 21 cases passed. Each invalid-value case first verifies a
non-blank value passes, then plants the fault and requires exit 1 with its
file and question id.

L3-2 removes the false agreement claim from the heading comment and states
in the _records docstring that this gate skips fenced content while the
interview-minimums counting gate does not. The counting gate is unchanged;
this row is the accepted documentation correction.

After repair, the question-context, repository-adoption and
interview-minimums test modules passed all 142 tests. The repository
question-context command read 55 answered records successfully. The
criterion-ledger, frontmatter-current, interview-minimums and gate-schema
checks, Ruff check/format checks and git diff --check passed.
This attempt did not run make verify or the kit probe, make a commit or
edit findings.md. The runner owns full verification and the checkpoint
commit; the orchestrator owns the tracker, pull request and handover.

Measured repair spans now total 13m 19s; the earlier unmeasured
implementation span remains unknown and is not estimated.

Resume: when I start, I will run `make verify` through the repair runner.
