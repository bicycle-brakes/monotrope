---
title: "Findings — criterion-test-ledger"
category: findings
status: draft
implementation_status: partial
date: 2026-10-11
created: 2026-10-11
last_reviewed: 2026-10-11
updated: 2026-10-12
supersedes: null
superseded_by: null
bead: coding-harness-909
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-11"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — criterion-test-ledger

Stage-2 call, 2026-10-11: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 349 files, 805 commits, 12 rules.

## Phase 2a — Codex, 2026-10-11

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | SPEC | base | spec.md:271–274, 315–317, 336–337 | [AMBIGUITY] [DIVERGENT] The non-goals explicitly exclude design.md and phase 2b, while the Definition of Done requires design.md and Open decisions assigns the ADR draft to phase 2b. Following the first reading omits the design artifact; following the second produces it. Either reading contradicts an explicit requirement. | Codex | in spec — the non-goal now reads "no architecture beyond the ADR": phase 2b runs and its `design.md` carries the ADR draft only | — |
| F-2 | MAJOR | SPEC | base | spec.md:309–319 | [AMBIGUITY] “None beyond these” can mean an exhaustive pull-request file list, which forbids this change’s spec.md, research.md, decisions.md and findings.md, or an implementation-only list, which permits those workflow artifacts. The branch already adds the first three relative to origin/main, and the review requires findings.md. The two readings therefore produce different verdicts on the same pull request. | Codex | in spec — the Definition of Done lists this change's own workflow artefacts and states the list is the pull request's whole file list | — |

Reviewer session: codex 01a12c1e-35cf-73f3-877f-20975d77f9b1

Stage-2 call, 2026-10-11: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 353 files, 808 commits, 12 rules.

Stage-2 call, 2026-10-11: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 355 files, 810 commits, 12 rules.

Stage-2 call, 2026-10-11: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 355 files, 814 commits, 12 rules.

Stage-2 call, 2026-10-11: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 355 files, 816 commits, 12 rules.

Stage-2 call, 2026-10-11: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 355 files, 820 commits, 12 rules.

Stage-2 call, 2026-10-11: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 355 files, 825 commits, 12 rules.

Stage-2 call, 2026-10-12: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 355 files, 835 commits, 12 rules.

## Phase 6 — Codex, 2026-10-12

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-3 | BLOCKER | MAINT | base | scripts/check_interview_minimums.py:270–280 | A diff changing one feature’s spec.md, decisions.md and plan.md, plus an ADR that does not spell the folder name, is rejected despite five valid answers and exactly one candidate owner. The same folder enters both owning and plan_only, triggering the ambiguity branch. The baseline accepts this input; the current gate reports zero changes measured. A folder touched beyond plan.md must not also count as plan-only. | Codex | open | — |
| F-4 | BLOCKER | SPEC | base | scripts/check_criterion_ledger.py:131–146 | An Acceptance criteria section containing criterion 1, the line `` ```note `example` ``, then criterion 2 is read as containing only criterion 1. That line is not a valid CommonMark opening fence because its info text contains backticks, but _fenced treats everything following it as code. A ledger covering only criterion 1 therefore exits 0 instead of reporting missing criterion 2. [Acceptance criterion 12] | Codex | open | — |
| F-5 | BLOCKER | SPEC | base | scripts/check_criterion_ledger.py:305, 419–423 | With a readable repository root and plans/changes directory, a live change directory lacking search permission makes plan_path.exists() raise PermissionError. This happens before the guarded file read, and run catches only CannotMeasure. The CLI therefore terminates with a traceback rather than reporting the unreadable plan, and subsequent plans are not examined. The gate must report this access failure as a finding. [Acceptance criterion 17] | Codex | open | — |

Phase 6 verdict: codex 01a12c1e-35cf-73f3-877f-20975d77f9b1, 2026-10-12

## Phase 4b — loop rows, released 2026-10-12

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | MAINT | base | scripts/check_criterion_ledger.py:126 | The byte-order-mark test in `_lines` calls `ord(text[:1])`; for an empty `plan.md` or `spec.md`, `text[:1]` is the empty string and `ord("")` raises `TypeError`, so the gate ends in a traceback instead of reporting the plan that has no ledger section or the spec it cannot read — the one input the new test file never feeds. `_lines` should test `text.startswith("\ufeff")` instead, and a test should cover an empty plan and an empty spec. | deepseek-v4.1-flash | taken — test_an_empty_plan_or_spec_is_reported_without_a_traceback | no | agree |
| L1-2 | MINOR | MAINT | base | scripts/check_criterion_ledger.py:318 | The more-than-one-ledger branch reads the second section's line number as `sections[1][0][0]`; when the second `## Criterion ledger` heading is the last line of the plan, that section holds no lines and the index raises `IndexError`, so a doubled section at the end of the file tracebacks instead of being reported. The covering test's second section always has content. | deepseek-v4.1-flash | taken — test_a_doubled_ledger_heading_on_the_last_line_is_reported | no | agree |
| L1-3 | MINOR | SPEC | base | scripts/check_criterion_ledger.py:375–377 | A live plan's `not yet written` entry discards the read result's reason (`found, _ = _file(...)`), so a named test file that exists but is a directory, is unreadable or is not valid UTF-8 leaves the entry accepted and the run green; the spec requires a finding for every named test file the gate cannot read or that is not valid UTF-8, while only a missing file may stay accepted as not yet written. | deepseek-v4.1-flash | taken — test_a_not_yet_written_entry_whose_file_cannot_be_read_is_reported | no | agree |
| L1-4 | MINOR | MAINT | base | plans/changes/criterion-test-ledger/plan.md:515–517 | The expected gate output recorded under "Evidence" does not match the five ledgers it will measure: they hold 270 entries (196 test, 39 not yet written, 35 not a test), not 268 (194 test), and the harness-decide-adr ledger alone lists 60 entries (57 test, 3 not a test), not the 59 (56 test) the step-1 note records. A maintainer comparing the plan's evidence with the run sees a difference no commit explains. | deepseek-v4.1-flash | taken — criterion 24; plan evidence corrected to the measured 274 entries and harness-decide-adr 60 (57 test) | no | agree |
| L1-5 | MINOR | MAINT | base | scripts/check_criterion_ledger.py:414 | The stderr summary counts distinct finding paths as plans, so one change with findings on both its `plan.md` and its `spec.md` is reported as two plans; the count should use the distinct change folders. | deepseek-v4.1-flash | taken — test_the_summary_counts_a_change_with_plan_and_spec_findings_once | no | agree |
| L2-1 | MAJOR | MAINT | base | `scripts/check_interview_minimums.py:253` | The narrowing of the ADR-owner rule is unconditional: a change folder the diff touches through its `plan.md` alone is never an owner. A later diff that touches `docs/adr/**` together with only its change's `plan.md` (an ADR landing after the change's other artefacts merged, plus the plan's status stamp) now finds zero owners, and the gate reports "owns 0 change folder(s)" — the old rule resolved that same diff to exactly one owner and ran green. The added test `test_a_folder_whose_diff_touches_only_plan_md_is_no_owner` covers only the direction that turned this change green; no test covers the direction that turns a previously green run red, and the finding text ("whose decisions.md carries the five answers") gives a maintainer hit by it nothing to follow. | mimo-v2.6-flash | taken — test_an_adr_with_only_its_own_plan_md_still_has_that_one_owner | no | agree |
| L2-2 | MINOR | MAINT | base | `scripts/check_criterion_ledger.py:334` | When `spec.md` exists but yields no criterion numbers, the gate records the single "has no criterion number" finding but keeps the empty set in `numbers`, so the per-entry check then fires for every entry of the ledger ("names criterion N, which spec.md does not have — correct the number or the spec"). One broken spec produces a finding per ledger line — a plan with 70 entries buries the one actionable finding in noise, and every extra line tells the author to fix entries that are correct. | mimo-v2.6-flash | taken — test_a_spec_without_numbers_gives_one_finding_not_one_per_entry | no | agree |
| L2-3 | MINOR | MAINT | base | `scripts/check_criterion_ledger.py:61` | The `CUTOFF` comment tells the next maintainer that changing the date is "a governance act, stated in docs/WORKFLOW.md beside this gate", but the gate's row at `docs/WORKFLOW.md:385` states no such rule — it names only what the gate holds, the archive rule and the date. The pointer a maintainer is directed to follow leads to text that is not there. | mimo-v2.6-flash | taken — test_the_workflow_row_makes_moving_the_cutoff_a_governance_act | no | agree |
| L3-1 | MAJOR | MAINT | maintainer-trip | scripts/check_interview_minimums.py:243–260 | The ADR-owner rule now drops any change folder the diff touches only through `plan.md` whenever another folder is touched through something else, so a diff carrying one change's files, another change's `plan.md` (exactly the ledger edit ADR 0013 mandates when a test is renamed) and one ADR reports exactly one owner and goes green even when the ADR belongs to the dropped folder; the finding text still promises the ADR runs inside exactly one folder whose `decisions.md` carries the answers. A tree with one folder touched through `decisions.md`, one through `plan.md` alone, and one ADR demonstrates the silent misattribution. | mimo-v2.6-pro | taken — test_a_plan_md_only_folder_does_not_hide_the_adr_owner_among_other_folders | no | agree |
| L3-2 | MAJOR | SPEC | promised-not-done | plans/changes/criterion-test-ledger/plan.md:557 against its own `## Criterion ledger` | The change's own new test `test_a_folder_whose_diff_touches_only_plan_md_is_no_owner`, named in the plan as the counterpart that holds the interview-minimums amendment, stands in no ledger entry and is not among the functions the plan sends to the pull request body as holding no criterion, so the rule the change enforces — a test disappears only through a visible edit of the plan — does not cover the test that guards the gate it loosened; deleting that test stays green. | mimo-v2.6-pro | taken — ledger entry for test_a_folder_whose_diff_touches_only_plan_md_is_no_owner (criterion 24) | no | agree |
| L3-3 | MAJOR | SPEC | promised-not-done | decisions.md Q-2 against scripts/check_criterion_ledger.py:63 (CUTOFF) | Q-2 exempts the changes archived before this change, but the gate enforces the fixed cut-off date its constant carries wherever the kit travels, so an instance receiving the gate later has every plan archived between that date and its adoption reported on arrival, and the workflow now declares moving the date a governance act, leaving retro-fitting ledgers into archived history or a decision pull request as the only ways to adopt the gate; the ADR records only that the instance case is unvalidated. | mimo-v2.6-pro | rejected — disclosed limit: the ADR records that the instance case is unvalidated; follow-up bead for the adoption date | no | disagree — Criterion 4 explicitly fixes the cutoff at 2026-10-11; an exemption based on each instance’s adoption date is not promised. |
| L3-4 | MINOR | MAINT | maintainer-trip | decisions/gates.yaml (`criterion-ledger`) with scripts/check_criterion_ledger.py:270–274 | The gate travels with `enforcement: block` and exits 3 whenever the root holds no `plans/changes/`, which this repository's own rule turns red on a block gate, so the first pinned release can block every `make verify` of an instance whose plans are laid out differently until its layout matches or the gate is switched off — shipped with no trial, as the ADR admits. | mimo-v2.6-pro | rejected — disclosed limit: shipping without a trial is stated in the ADR; follow-up bead for the layout trial | no | disagree — Criterion 18 requires exit 3 when plans/changes/ is absent; no failure under the supported directory layout is demonstrated. |
| L3-5 | MINOR | MAINT | maintainer-trip | scripts/check_criterion_ledger.py:270–277 against spec.md criterion 18 | Criterion 18 and the module docstring promise exit 3 when the root "is not a readable directory", but only `is_dir()` is tested: a `plans/changes/` that exists and cannot be listed raises `PermissionError` out of `measure()`, which `run()` does not catch, so the run ends in a traceback and exit 1 — the failure mode the spec's refuted-by list forbids; a root whose directory is made unreadable demonstrates it. | mimo-v2.6-pro | taken — test_an_unlistable_plans_changes_directory_exits_3_without_a_traceback | no | agree |

Rounds run: 3

Stage-2 call, 2026-10-12: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 355 files, 836 commits, 12 rules.
