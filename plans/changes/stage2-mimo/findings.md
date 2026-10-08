---
title: "Findings — stage2-mimo"
category: findings
status: draft
implementation_status: none
date: 2026-10-07
created: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-08
supersedes: null
superseded_by: null
bead: coding-harness-ymx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — stage2-mimo

Stage-2 call, 2026-10-07: spec-review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 271 files, 610 commits, 12 rules.

## Phase 2a — Codex, 2026-10-07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S1 | BLOCKER | SPEC | base | spec.md:46,373,383; research.md:530 | [AMBIGUITY] The compatibility gap requires one live call per model in phase 4, before implementation depends on the address, while the order of work and Definition of Done forbid live calls before merge. One reading performs the probes during implementation and violates the merge restriction; the other postpones them until after merge and leaves the required compatibility check unfinished when the change ships. Stand-ins cannot establish actual endpoint compatibility. | Codex | in spec | — |
| S2 | BLOCKER | SPEC | base | spec.md:291,344,360; decisions.md:286 | [AMBIGUITY] AC25 requires ADR 0007 to be amended when OpenCode Go is declared, but the protected-area rule forbids editing the authoritative ADR and the Definition of Done includes only a draft. One reading completes this PR with the draft, leaving the declaration contrary to the effective ADR; the other requires a separate decision PR to merge first. That dependency and merge order are missing from the delivery contract. | Codex | in spec | — |
| S3 | MAJOR | SPEC | base | spec.md:228,411; decisions.md:342,376 | [AMBIGUITY] For a rejected model ID, AC17 requires stopping without another address, while the current decisions addendum explicitly specifies the OpenAI address as fallback. One reading reports the refusal and makes no second call; the other retries through `/chat/completions`, which AC17 forbids. The spec references that same decision detail without recording that its fallback was superseded. | Codex | in spec | — |
| S4 | MAJOR | SPEC | base | spec.md:150,156 | [AMBIGUITY] Consider two completed rounds with every row decided and no taken row in round 2, then request round 3. AC6 says refusing the third round refutes the criterion; AC7 requires that refusal. One reading permits the third round whenever two rounds have completed, violating AC7; the other permits it only after a taken row, violating AC6's stated test oracle. The same fixture cannot satisfy both. | Codex | in spec | — |

Reviewer session: codex 01a116db-602e-73e2-bbee-d11f961debe4

Stage-2 call, 2026-10-07: implement · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 273 files, 618 commits, 12 rules.

Stage-2 call, 2026-10-08: implement · attempt 2 · route flash-repair · endpoint glm-coding-plan · model glm-5.3-flash · reason first Flash post-run check failed · leak check clean over 274 files, 626 commits, 12 rules.

Stage-2 call, 2026-10-08: implement · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Flash post-run checks failed · leak check clean over 274 files, 627 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 296 files, 675 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 296 files, 676 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 296 files, 677 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 309 files, 693 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 309 files, 694 commits, 12 rules.

Stage-2 call, 2026-10-08: probe · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 309 files, 694 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 309 files, 697 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 309 files, 701 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 309 files, 701 commits, 12 rules.

Stage-2 call, 2026-10-08: review-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 309 files, 702 commits, 12 rules.

Stage-2 call, 2026-10-08: review · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 309 files, 706 commits, 12 rules.

## Phase 6 — Codex, 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| R1 | BLOCKER | SPEC | base | docs/WORKFLOW.md:859; docs/adr/0007-stage-2-reviews-by-codex-and-glm.md:84; docs/adr/0011-stage-2-reviews-through-opencode-go.md:19 | [DIVERGENT] After the third measured run, a taken Codex finding that broke a previously green test requires fallback under ADR 0007, but the revised workflow triggers fallback only for a rung's finding. With a broken Codex repair and no broken rung repair, the two rules give opposite outcomes. ADR 0011 amends decisions 2 and 3, leaving this stop rule in decision 1 unchanged. [AC24] | Codex | taken — the stop rule counts a taken finding of Codex or of a rung; test_the_stop_rule_counts_every_rung pins both | yes |
| R2 | MAJOR | SPEC | base | tests/test_model_endpoints.py:343; tests/test_stage2.py:1736 | Swapping the first two models solely in the YAML list makes the declaration test fail because it asserts the original exact order; the launch test also fixes the first model by name. Reproduced in memory: the original declaration passes and the reordered declaration fails. The promised YAML-only pull request therefore requires Python test edits before CI can pass. [AC5] | Codex | taken — the test worlds pin their own ladder order and the declaration test pins the set; a reordered real yaml keeps verify green (measured) | yes |
| R3 | MAJOR | MAINT | base | scripts/stage2.py:815; scripts/stage2.py:1586 | After two rounds are released with every genuine round-2 row rejected, retained reviewer text can incorrectly authorize round 3. A ten-cell illustrative row named `L2-99`, with severity `annotation` and status `taken`, is excluded by the original record parser but accepted by `released_rows`, which scans the retained text too. Reproduced through the release formatting and round-selection code: MiMo Pro starts despite there being no genuine taken row. [AC7] | Codex | taken — released_rows reads only the runner's block, not the kept reviewer text; test_text_kept_from_the_record_never_authorises_round_3 | no |

Phase 6 verdict: codex 01a116db-602e-73e2-bbee-d11f961debe4, 2026-10-08

## Phase 4b — loop rows, released 2026-10-08

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
|---|---|---|---|---|---|---|---|---|---|
| L1-1 | BLOCKER | SPEC | base | docs/adr/0011-stage-2-reviews-through-opencode-go.md:137-145,188-193; plans/changes/stage2-mimo/design.md:264-266,310-315; plans/changes/stage2-mimo/decisions.md:470-474 | [DIVERGENT] The ADR's Consequences still say "Nothing leaves before the merge except the probe" and "every other call is a stage-2 run after the merge", while its own decision 7 — and decisions.md, the spec's Definition of Done and the plan's step 8 — say this change's own review loop also runs before the merge, and findings.md already carries its review-loop call lines; the same stale paragraph stands in the design.md draft, and the ADR test reads only the draft, so nothing turns it red. | deepseek-v4.1-flash | taken — the ADR's and the design's Consequences now name the probe and this change's own loop (answer "1", 2026-10-08), as decision 7 does | no | — |
| L1-2 | MINOR | SPEC | base | scripts/stage2.py:1614-1645; plans/changes/stage2-mimo/spec.md:366-370; plans/changes/stage2-mimo/design.md:77-80; docs/WORKFLOW.md:652 | The spec's criterion 27 and the design's Interfaces say `pi --version` runs before the leak check of each `probe` call, but `probe` runs `require_pi()` once before its loop, so the second and third rung calls start without a version check; the plan (step 2) and the WORKFLOW verb list say "once first", so the change answers the same question two ways. | deepseek-v4.1-flash | taken — criterion 27 and the design say the pin runs once per verb run, as the plan and the code do | no | — |
| L1-3 | MINOR | MAINT | base | docs/WORKFLOW.md:136 | The evidence rule still reads "A Codex or GLM finding", but the loop's reviewers are the ladder's rungs; §4's loop section points to this rule and prompts/04b-review-loop.md was updated to "A finding of a rung", so the canonical statement of the rule no longer names the findings it governs. | deepseek-v4.1-flash | taken — the evidence rule in docs/WORKFLOW.md names Codex and the rungs of the review loop | no | — |
| L1-4 | MINOR | MAINT | base | tests/test_stage2.py:135,1804-1812 | The `@pytest.mark.parametrize` block belonging to `test_a_failed_codex_call_writes_no_session_line` is duplicated onto the `codex_ok` helper, where it is inert because the helper is not collected, and the unused `claude_ok` helper is left behind; the move also puts `codex_ok` about 1700 lines below its first use. | deepseek-v4.1-flash | taken — the stray parametrize block and the unused claude_ok helper are gone, codex_ok stands beside the other step helpers | no | — |
| L1-5 | MINOR | MAINT | base | tests/test_model_endpoints.py:405-406 | The planted fault in `test_no_old_reviewer_remark_claims_a_review_phase` is followed only by an assertion that the phrase the `str.replace` just removed is absent from its own output, which cannot fail; the test runs no checker over the planted remark, so it cannot catch the fault it claims to plant. | deepseek-v4.1-flash | taken — the planted remark now runs through the same checker as the real one and must produce exactly the planted problem | no | — |
| L2-1 | MAJOR | SPEC | base | plans/changes/stage2-mimo/spec.md:256; scripts/stage2.py:711; docs/WORKFLOW.md:721 | Criterion 15 promises "a time limit for every reviewer call … a call that has not ended 30 minutes after it started is stopped", and §4 states it in the same general breath as "a failed model process stops", but only `run_reviewer` (the Pi loop call) passes `timeout=REVIEWER_MINUTES * 60`. `run_codex` launches `codex exec` with no timeout, so the spec review (2a), the review (6) and the loop-marks call can block the pipeline for ever; design.md even scopes criterion 15 to the "Runner → Pi → OpenCode Go" interface, so spec and design contradict each other. No test can refute it: criterion 15's test drives a `pi` stand-in only. | mimo-v2.6-flash | taken — criterion 15 and §4 now scope the limit to the review-loop call through Pi; run_codex is unchanged | no | — |
| L2-2 | MINOR | MAINT | base | templates/findings.md:127,135; scripts/stage2.py:194-195 | The change renames the runner's artefact strings to `## Phase 4b — loop rows, released` and `Loop rows: none — the loop did not run for this change.`, but the findings template — the documented form of that file, shipped to target repos as kit mechanismus — still shows `## Phase 4b — GLM loop rows, released <date>` and `Loop rows: none — the GLM loop did not run for this change.` No test ties template to runner (test_stage2 reads `stage2.RELEASE_HEADING` from the code), so verify stays green while the template documents a heading and a "GLM loop" the runner can no longer write. | mimo-v2.6-flash | taken — templates/findings.md names the heading and none-line the runner writes | no | — |
| L2-3 | MINOR | MAINT | base | prompts/04b-review-loop.md:3 | The prompt file is placed verbatim into every round's prompt, so rounds 2 and 3 open with "**Model:** deepseek-v4.1-flash — the ladder's first rung" although the call runs `mimo-v2.6-flash` and `mimo-v2.6-pro`; the runner injects no rung name anywhere in the prompt (only `--model` and the record's `Reviewer` cell carry the truth), so the model reviewing round 2 is told it is a different model. The phase-prompt test pins that line to rung 1, so no test can catch the mismatch. | mimo-v2.6-flash | taken — the prompt's model line names all three rungs by round | yes | agree |
| L2-4 | MINOR | MAINT | base | plans/changes/stage2-mimo/plan.md:185-199,305; plans/changes/stage2-mimo/spec.md:475 | plan.md's "Not touched" section excludes `prompts/02a-spec-review.md`, `prompts/06-review.md` and `scripts/stage2_session.py` "and its tests", and its Files table omits them, yet the diff edits all three — the two prompts because criterion 23 demands the three-round sentences (recorded only in plan.md's Time used repair log), the session test because declaring `opencode-go` broke its "the production declaration names no opencode-go" case. The spec's Definition of Done, "Moved in the same pull request, each by name", likewise lists twelve files and omits `tests/test_stage2_session.py`, so a maintainer diffing the PR against plan or DoD finds files the change says it does not touch. | mimo-v2.6-flash | taken — plan Files table, Not touched and the spec's Definition of Done list the files | no | agree |
| L3-1 | BLOCKER | SPEC | base | ADR 0011 decision 3; spec criterion 5; tests/test_stage2.py (`STAGE2_ROUTING`, `test_workflow_section_4_routes_the_three_reviews`), prompts/04b-review-loop.md | The change promises that reordering the ladder is a one-line pull request touching `model-endpoints.yaml` and nothing else, but the round-to-rung mapping is written out as literals in `docs/WORKFLOW.md` §4, `AGENTS.md` and the loop prompt's model line, and tests pin those literals (the routing table must read `deepseek-v4.1-flash` for 4b and its cell must name all three rungs; the phase-prompt test resolves the prompt's model line against the declaration). A reorder or an id replacement that changes only the yaml turns `make verify` red and leaves the doctrine naming a mapping that no longer holds, so the central "the ladder is data" promise is not delivered. | mimo-v2.6-pro | taken — the ladder lives in model-endpoints.yaml only: AGENTS.md, WORKFLOW §4 and the loop prompt name no id; the runner names the round's id in the prompt; test_no_doctrine_text_repeats_the_ladder_order guards it (maintainer chose this over rewording the promise) | yes | agree |
| L3-2 | MAJOR | SPEC | base | tests/test_stage2.py `test_the_adr_draft_states_every_point`; docs/adr/0011-stage-2-reviews-through-opencode-go.md | Criterion 25 is refuted by a point missing "from the ADR or from its draft in design.md", but the only test reads the draft inside `plans/changes/stage2-mimo/design.md`. The file the decision pull request actually merges, `docs/adr/0011-…`, has no needle check at all, so it can lose a point or drift from the tested draft while `make verify` stays green. Nothing verifies the design's claim that the two texts are identical. | mimo-v2.6-pro | taken — test_the_adr_draft_states_every_point now checks docs/adr/0011 as well as the draft | no | agree |
| L3-3 | MAJOR | MAINT | base | scripts/stage2.py (`ROUND_HEADING`, `rounds_run`) | The round heading pattern was widened from a fixed reviewer name to `## Round <n> — \S+,`, and `rounds_run` counts its matches over the whole loop record, including the reviewer's own prose — which the change's own tests show can carry `## …` headings. A rung that quotes a round heading in its words inflates the round count: the ladder mapping (round n → `modelle[n-1]`) shifts to the wrong rung, and the loop can stop early with "n rounds have run". `_record_lines` already separates the reviewer's words from the runner's lines; the counter does not use it. | mimo-v2.6-pro | rejected — a reviewer line shaped like a round heading cannot be told from one; the limit is stated in _record_lines and a rung's words carry no such heading in practice | no | agree |
| L3-4 | MINOR | MAINT | base | docs/WORKFLOW.md §4 (`probe` verb); scripts/stage2.py `probe`/`begin_call` | The doctrine says the `probe` "writes no record", but `probe` goes through `begin_call`, which appends a `Stage-2 call … probe` line to `findings.md` and may create its header. The change's own findings file carries several such probe lines with nothing marking which run is the declared special run of the Definition of Done, so a maintainer cannot tell which three calls the pull request body is supposed to quote. | mimo-v2.6-pro | taken — WORKFLOW §4 says the probe writes no loop record and its call lines go to findings.md; the pull request body names the three special-run commits (decision 1) | no | agree |
| L3-5 | MINOR | SPEC | base | plans/changes/stage2-mimo/decisions.md, `[DETAIL]` 1 ("Which rung phase 2a and phase 6 take") | This detail decision says phases 2a and 6 call rung 1 of the ladder and warns that the phase-6 verdict would come from the ladder's weakest model, contradicting the shipped routing (2a and 6 stay with Codex). Unlike the `[DECISION]` sections above it, it is not marked superseded, so a reader who was not there takes it as current. | mimo-v2.6-pro | taken — decisions.md marks DETAIL 1 superseded | no | agree |
| L3-6 | MINOR | MAINT | base | tests/test_stage2.py `test_an_endpoint_the_declaration_does_not_clear_refuses` (fault `no-model`) | The "no-model" fault was changed from an entry listing a model the call does not use to an entry listing none, so the case "the declaration lists models but not the one this call asks for" is no longer exercised for any verb. The check that refuses a call whose rung the entry does not list lost its test, and a regression there would pass the suite. | mimo-v2.6-pro | rejected — the ladder is read from the entry's own list, so a call can never use a model the entry does not list; the planted case fails to refuse for that reason, not for a gap | no | disagree — Work-verb tests still reject a nonempty list containing another model, and session tests reject unlisted models; the claimed absence across all verbs is false. |

Rounds run: 3

Stage-2 call, 2026-10-08: review (loop marks) · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 309 files, 706 commits, 12 rules.
