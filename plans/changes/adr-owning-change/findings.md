---
title: "Findings — adr-owning-change"
category: findings
status: draft
implementation_status: none
date: 2026-10-13
created: 2026-10-13
last_reviewed: 2026-10-13
updated: 2026-10-13
supersedes: null
superseded_by: null
bead: coding-harness-afa
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-13"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — adr-owning-change

Stage-2 call, 2026-10-13: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 383 files, 976 commits, 12 rules.

Stage-2 call, 2026-10-13: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 384 files, 976 commits, 12 rules.

Stage-2 call, 2026-10-13: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Claude Code 2.1.296 refused glm-5.3-flash as an unrecognized model twice on 2026-10-13 (bead coding-harness-3fc) · leak check clean over 384 files, 976 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `decisions/adoption.yaml` +5 -0
> - `docs/WORKFLOW.md` +22 -7
> - `docs/adr/0014-a-change-claims-its-adr-files.md` +181 -0
> - `plans/changes/adr-owning-change/plan.md` +23 -21
> - `plans/changes/criterion-test-ledger/plan.md` +2 -8
> - `plans/changes/criterion-test-ledger/spec.md` +1 -0
> - `prompts/02-spec.md` +7 -0
> - `provenance.yaml` +5 -0
> - `scripts/adoption.py` +67 -0
> - `scripts/check_interview_minimums.py` +149 -103
> - `scripts/ci_gates.py` +4 -0
> - `scripts/kit/manifest.yaml` +15 -0
> - `templates/spec.md` +3 -0
> - `tests/test_adoption.py` +91 -0
> - `tests/test_check_interview_minimums.py` +355 -112
>
> Diagnostics:
> ````text
> - `make verify` exited 2
> The gates that blocked, each with its last lines:
> ── [leerprobe] $ lauf_cmd
> BLOCK (2):
>   - 1 rote(r) Fall/Faelle ohne deklarierten Grund
>       ::tests.test_check_interview_minimums
>       
>       Nachtragen mit: python3 scripts/kit/probe.py --messen
>   - 35 Eintrag/Eintraege in REIST_NICHT haben keinen Fall mehr
>       tests.test_ci::test_der_echte_lesepfad_des_bead_gates_wird_erkannt
>       tests.test_ci::test_every_gate_step_has_a_mutation_test
>       tests.test_ci::test_every_script_has_a_test_or_a_declared_reason
>       tests.test_ci::test_no_declared_reason_cites_a_closed_or_unknown_bead
>       tests.test_ci::test_no_declared_reason_stands_for_a_script_that_has_a_caller
>       tests.test_ci::test_the_makefile_runs_what_the_one_list_runs
>       tests.test_feedback_channel::test_journal_index_lists_every_open_project_handover
>       tests.test_feedback_channel::test_the_field_checks_read_the_schema_instead_of_a_copy[GEMEINSAM-fehlende_gemeinsame]
>       tests.test_feedback_channel::test_the_field_checks_read_the_schema_instead_of_a_copy[PROJEKT_PFLICHT-fehlende_kanalpflicht]
>       tests.test_kit::test_the_kit_list_is_not_derivable_from_the_export_list
>       tests.test_kit::test_the_role_check_goes_red_when_a_rule_is_removed
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[code-generation-orchestrator.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[consistency-auditor.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[entity-builder.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[entity-deployer.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[migration-supervisor.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[preconditions-gate-runner.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_agent_model_resolves_to_a_declared_endpoint[reconciliation-orchestrator.md-claude-sonnet-5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[01-explore.md-GLM 5.3 Flash]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[01a-interview.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02-spec.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02a-spec-review.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[02b-design.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[03-plan.md-Opus 5.5]
>       tests.test_model_endpoints::test_every_model_in_a_phase_prompt_resolves[04-implement.md-GLM 5.3 Flash]
>         …
>       
>       Entweder wurde der Test umbenannt — dann den Eintrag nachziehen — oder seine Datei reist nicht mehr mit. Der zweite Fall ist der gefaehrliche: die Portabilitaet sinkt, und die gemeldete Quote steigt.
>
> INFO  (1):
>   - 0 von 1 Faellen tragen in ein fremdes Repo (0 %)
>       mechanismus 81 · bestand 302 Datei(en)
> ── [leerprobe] RED (block) — der Lauf ist rot.
>
> Standard error of the whole run, last lines:
> [… 7718 earlier lines left out …]
> templates/handover.md:22:81 error MD013/line-length Line length [Expected: 80; Actual: 200]
> templates/handover.md:48:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> templates/spec.md:21 error MD041/first-line-heading/first-line-h1 First line in a file should be a top-level heading [Context: "```yaml"]
> templates/spec.md:39:81 error MD013/line-length Line length [Expected: 80; Actual: 97]
> templates/spec.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 95]
> tools/claude-code/README.md:17:81 error MD013/line-length Line length [Expected: 80; Actual: 105]
> tools/claude-code/README.md:18:81 error MD013/line-length Line length [Expected: 80; Actual: 109]
> tools/claude-code/README.md:19:81 error MD013/line-length Line length [Expected: 80; Actual: 134]
> tools/claude-code/README.md:23:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:23:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:23:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:24:81 error MD013/line-length Line length [Expected: 80; Actual: 272]
> tools/claude-code/README.md:25:81 error MD013/line-length Line length [Expected: 80; Actual: 180]
> tools/claude-code/README.md:26:81 error MD013/line-length Line length [Expected: 80; Actual: 115]
> tools/claude-code/README.md:28:81 error MD013/line-length Line length [Expected: 80; Actual: 124]
> tools/claude-code/README.md:29:81 error MD013/line-length Line length [Expected: 80; Actual: 106]
> tools/claude-code/README.md:38:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:38:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:38:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:40:81 error MD013/line-length Line length [Expected: 80; Actual: 442]
> tools/claude-code/README.md:41:81 error MD013/line-length Line length [Expected: 80; Actual: 163]
> tools/claude-code/README.md:42:81 error MD013/line-length Line length [Expected: 80; Actual: 126]
> tools/claude-code/README.md:43:81 error MD013/line-length Line length [Expected: 80; Actual: 96]
> tools/claude-code/README.md:44:81 error MD013/line-length Line length [Expected: 80; Actual: 167]
> tools/claude-code/README.md:72:1 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:5 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:72:9 error MD060/table-column-style Table column style [Table pipe is missing space to the right for style "compact"]
> tools/claude-code/README.md:72:13 error MD060/table-column-style Table column style [Table pipe is missing space to the left for style "compact"]
> tools/claude-code/README.md:73:81 error MD013/line-length Line length [Expected: 80; Actual: 112]
> tools/claude-code/README.md:74:81 error MD013/line-length Line length [Expected: 80; Actual: 89]
> tools/claude-code/README.md:75:81 error MD013/line-length Line length [Expected: 80; Actual: 88]
> make: *** [verify] Error 1
> ````

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 388 files, 977 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route glm · endpoint glm-coding-plan · model glm-5.3 · leak check clean over 388 files, 978 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Claude Code 2.1.296 refused glm-5.3 as an unrecognized model on 2026-10-13 (bead coding-harness-3fc) · leak check clean over 388 files, 980 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `plans/changes/adr-owning-change/plan.md` +2 -2
> - `plans/changes/criterion-test-ledger/plan.md` +16 -19
> - `scripts/check_interview_minimums.py` +3 -3
> - `tests/test_adoption.py` +0 -6
> - `tests/test_this_repository_adoption.py` +20 -0
>
> Diagnostics:
> ```text
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 389 files, 982 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Claude Code 2.1.296 refused glm-5.3(-flash) as an unrecognized model before any call (bead coding-harness-6th) · leak check clean over 389 files, 984 commits, 12 rules.

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 389 files, 985 commits, 12 rules.

Stage-2 call, 2026-10-13: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 389 files, 986 commits, 12 rules.

Stage-2 call, 2026-10-13: repair · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason Claude Code 2.1.296 refused glm-5.3(-flash) as an unrecognized model before any call (bead coding-harness-6th) · leak check clean over 389 files, 987 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +8 -5
> - `docs/adr/0014-a-change-claims-its-adr-files.md` +3 -1
> - `scripts/kit/manifest.yaml` +1 -1
>
> Diagnostics:
> ```text
> - `plan.md` did not add a measured line below `## Time used`
> ```

Stage-2 call, 2026-10-13: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 389 files, 988 commits, 12 rules.

## Phase 6 — Codex, 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | BLOCKER | MAINT | phase-6 | docs/WORKFLOW.md:123; docs/adr/0014-a-change-claims-its-adr-files.md:152; scripts/check_interview_minimums.py:304 | [DIVERGENT] When an amendment also touches an earlier feature’s folder, the documentation prescribes removing that feature’s claim. If it has a valid “yes” answer and only that claim, removal triggers “answers yes … but claims no ADR file” and exit 1. Reproduced with criterion-test-ledger: the documented remedy contradicts the enforced agreement rule. [AC 9, 21] | Codex | fixed — tests/test_check_interview_minimums.py::test_adr_with_two_owning_changes_is_a_finding | yes |
| F-2 | BLOCKER | SPEC | phase-6 | scripts/check_interview_minimums.py:92; scripts/check_interview_minimums.py:258 | The literal-line prefilter ignores valid YAML keys written as `adr_files :` or `"adr_files":`. An archived stock spec containing `"adr_files": [plans/x.md]` produces no findings and exits 0, bypassing claim validation; a valid ADR claim using either spelling is also ignored during attribution. [AC 1, 2] | Codex | fixed — tests/test_check_interview_minimums.py::test_a_claim_key_in_any_yaml_spelling_is_seen | no |
| F-3 | MAJOR | SPEC | phase-6 | scripts/adoption.py:51; scripts/check_interview_minimums.py:261 | An impossible unquoted date such as `2026-02-30` makes the shared YAML loader raise `ValueError`, which neither caller catches. In the adoption record, the gate exits 1 with a traceback instead of exit 3 and the required remedy. In a spec containing `adr_files`, it likewise aborts without reporting the spec and expected claim form. Both cases were reproduced. [AC 2, 14] | Codex | fixed — tests/test_check_interview_minimums.py::test_an_impossible_date_in_a_claiming_header_is_a_finding; tests/test_adoption.py::test_an_impossible_date_is_refused_with_the_remedy | no |
| F-4 | MAJOR | SPEC | phase-6 | plans/changes/criterion-test-ledger/plan.md:555 | The diff also rewrites the earlier change’s “Phase 4 amendments” narrative. The protected-area boundary permits only its spec’s ADR claim and criterion-24 ledger lines; replacing this separate historical section exceeds those permitted edits. [Protected areas; Definition of Done] | Codex | fixed — not a test — a spec boundary: the rewrite stays because the old narrative described as current an interim rule this change deletes (loop row L1-3), and the spec "Protected areas" now permits it | no |

Phase 6 verdict: codex 01a1348d-d2d6-7682-a2f1-1097d8ef46c4, 2026-10-13
Reviewer session: codex 01a1348d-d2d6-7682-a2f1-1097d8ef46c4 — a fresh session reviewed: no phase-2a session was recorded

## Phase 4b — loop rows, released 2026-10-13

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | MAJOR | SPEC | code | tests/test_adoption.py:66–69 and scripts/kit/manifest.yaml (the tests/test_adoption.py rule) | The case test_this_repository_adopted_the_gate_on_2026_10_08 is declared mechanismus, but it skips only when the adoption record is absent and otherwise asserts the day equals 2026-10-08. A repository that adopts the kit and records its own day — which the ADR requires — has the record present, so the case fails there and the block pytest gate turns red; the empty-repository probe stays green only because its tree holds no record, so the cited travel evidence does not cover the case. The assertion needs a marker that stays home, or the case must not travel. | deepseek-v4.1-flash | fixed — not a test — a travel declaration: the case asserts this repository's own adoption day, so in a repository that records its own day it fails; it is to stay home (a REIST_NICHT entry with reason bestand-dieses-repos, or a manifest rule that keeps it out), and the declared category must match | no | agree |
| L1-2 | MINOR | MAINT | code | scripts/check_interview_minimums.py:9–11 | The module docstring's opening rule list still says a change whose diff creates or changes a file under docs/adr/ owes the five records, the diff-based attribution this change removes; the paragraph further down says the claim under adr_files alone decides. A maintainer reading the summary at the top of the gate is told the old rule, so the file contradicts itself. | deepseek-v4.1-flash | fixed — not a test — a false statement: the docstring's rule list is to say that the claim under adr_files decides, as the paragraph below it does | no | agree |
| L1-3 | MINOR | MAINT | code | plans/changes/criterion-test-ledger/plan.md:558–573 | The "Phase 4 amendments" prose still describes the interim owner rule as current and names test_a_folder_whose_diff_touches_only_plan_md_is_no_owner and test_an_adr_with_only_its_own_plan_md_still_has_that_one_owner as its counterpart tests; this change removes both tests and replaces the rule, and only the ledger line was updated. The plan now points a reader at tests that do not exist. | deepseek-v4.1-flash | fixed — not a test — a false statement: the "Phase 4 amendments" prose in plans/changes/criterion-test-ledger/plan.md is to name the ADR 0014 rule and its tests instead of the removed interim rule and tests | no | agree |
| L2-1 | MAJOR | MAINT | maintainer-trip | scripts/check_interview_minimums.py, the two-claimant branch of measure() | A claim is a per-file list in a spec header that never expires: this change writes adr_files: [docs/adr/0013-every-criterion-names-its-proof.md] into criterion-test-ledger's spec permanently, while ADR 0014 point 1 instructs every later change that amends an ADR to claim that same file itself. When one diff touches both folders — e.g. a change that edits ADR 0013 and also edits criterion-test-ledger/plan.md, which ADR 0013 itself mandates whenever a test a ledger names disappears — the gate reports "claimed by criterion-test-ledger, <name> in one diff" and offers only "drop the other claims or split the pull request". Neither ADR 0014 nor docs/WORKFLOW.md §2 tells a maintainer that the earlier change's claim must be retired, so following the ADR literally turns two correct claims into a red gate (held by tests/test_check_interview_minimums.py::test_adr_with_two_owning_changes_is_a_finding). | mimo-v2.6-flash | fixed — tests/test_check_interview_minimums.py::test_adr_with_two_owning_changes_is_a_finding | no | agree |
| L2-2 | MINOR | MAINT | maintainer-trip | scripts/check_interview_minimums.py, module docstring (the ten-decisions list) | The fifth bullet still reads "an architectural change owes five only when its diff touches docs/adr/", while the second bullet above it was rewritten to the claim rule; the same pre-ADR-0014 trigger without the claim stands in docs/WORKFLOW.md §2 ("creating or changing an ADR owes five, whatever the class"). The docstring is the rule list a maintainer reads beside the code, and it now states two different triggers for the same five-record duty — one of them the diff-path inference ADR 0014 point 3 removes; under the new code an architectural change that touches an ADR without claiming it gets the unclaimed finding, not the five. | mimo-v2.6-flash | fixed — not a test — the docstring's fifth bullet in `scripts/check_interview_minimums.py` and the ADR sentence in `docs/WORKFLOW.md` §2 now state the claim rule | no | agree |
| L2-3 | MINOR | SPEC | promised-not-done | plans/changes/adr-owning-change/plan.md, "The gate", step 2 | The plan promises the claim header is loaded with check_adr_answers.read_header and strict_load, so the two gates cannot disagree about what a header is; scripts/check_interview_minimums.py:_claim never calls read_header and parses the header with its own copy of the block regex (_BLOCK). Behaviour differs where the shared reader was promised: a spec with no --- header block that carries an adr_files: line claims nothing and reports nothing (_claim returns ([], None) when the block match fails), where read_header would return its "has no header" problem. | mimo-v2.6-flash | fixed — not a test — `plan.md` "The gate" step 2 now says what the code does: the gate's own block regex with `strict_load`, and a spec without a header block claims nothing | no | disagree — The spec requires validating claims in spec headers, not rejecting headerless files. The copied block regex matches the shared reader; the helper substitution establishes no acceptance-criterion failure. |
| L2-4 | MINOR | MAINT | maintainer-trip | scripts/check_interview_minimums.py, measure() feeding _disagreement() | An unreadable claim is recorded as an empty claim, so a subject feature whose answer is "yes" and whose adr_files line is malformed gets two findings for one fault: "adr_files cannot be read — …" plus "answers yes to the ADR question but claims no ADR file — list it under adr_files in its spec header", which tells the maintainer to add a claim the file already has (only malformed). The suite never shows it: test_an_unreadable_claim_is_reported puts the malformed claim in a stock change, which the agreement check skips. | mimo-v2.6-flash | fixed — tests/test_check_interview_minimums.py::test_an_unreadable_claim_does_not_also_report_a_missing_one | no | agree |
| L3-1 | BLOCKER | MAINT | base | `docs/WORKFLOW.md` §2, the claim paragraph; the new ADR's Consequences section | [DIVERGENT] The two rule texts of this change answer "what does amending an ADR cost" in opposite ways: the workflow says an earlier change's claim "is retired — the path is removed from its spec header — when a later change claims the same file", so an amendment moves two headers, while the ADR says "An amendment costs one header line in the amending change's spec; nothing else in the tree moves". Nothing holds the retirement duty — the gate names retiring only as one remedy inside a two-claimant finding — so a reader cannot tell which text is the rule. | mimo-v2.6-pro | fixed — not a test — make the two texts one rule: an amendment costs one header line in the amending change's spec; an earlier change's claim is removed only when the amending diff also touches that earlier change's folder, which the two-claimant finding names; state that exception in both docs/WORKFLOW.md §2 and the new ADR's Consequences | no | agree |
| L3-2 | MINOR | MAINT | base | `docs/WORKFLOW.md` §2, the sentence on the five records | The sentence says the adoption day is "exempting only the class minimums", but the day also exempts every change begun on or before it from the answer/claim agreement — the decision record says so and the gate follows it: `tests/test_check_interview_minimums.py::test_the_agreement_holds_subject_features_alone` passes a stock feature answering "yes" with no claim. Read globally, the workflow sentence promises a check the gate does not run for the stock. | mimo-v2.6-pro | fixed — not a test — the sentence must say the adoption day exempts a stock change from the class minimums and from the answer/claim agreement, as the decision record and the gate do | no | agree |
| L3-3 | MINOR | MAINT | fix-r1 | `scripts/kit/manifest.yaml`, the rule for `tests/test_adoption.py` | The rule's reason says "the case that reads this repository's record skips where the record stays home", but that file holds no such case and no skip at all — the record-reading case was moved to `tests/test_this_repository_adoption.py`, which no travelling rule carries, and the reason was left behind. A maintainer trusting the reason looks for a skip that does not exist, and moving that case into the travelling file would redden the empty-repository probe, whose declared-reason list may only shrink. | mimo-v2.6-pro | fixed — not a test — the manifest reason for tests/test_adoption.py describes a case that moved to tests/test_this_repository_adoption.py; rewrite the reason to what the file holds and name why the moved case stays home | no | agree |

Rounds run: 3

Stage-2 call, 2026-10-13: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 389 files, 988 commits, 12 rules.
