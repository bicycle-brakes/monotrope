---
title: "Plan — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-16
updated: 2026-10-16
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-16"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, research, swarm]
---

# Plan — research-swarm

```text
For you:     Larger changes get mapped sources, three repository views per topic, Flash and live-selected Go free online views, and traceable questions and spec criteria.
Done when:   Fresh Go-only selection, topic coverage, offline isolation capture and research-to-interview-to-spec checks hold, and make verify is green.
Appetite:    12 hours of phase 4 including earlier implementation and repairs; stop at the limit.
Not now:     Zen or OpenCode CLI models, model-specific perspectives, the implementation-review swarm or sibling checkouts.
Pre-mortem:  suppose it failed: most likely because an online context inherited private repository information.
Starts unless you say stop.
```

## Files

Paths are relative to the repository; existing earlier-slice files are amended,
not recreated. No file is deleted. Only the ADR is new under `docs/adr/`.

| File | Change |
|---|---|
| `scripts/stage2.py` | Preserve early-class/fallback routing; expose checked, cancellable read-only launches for Pi and official Claude. |
| `scripts/stage2_swarm.py` | Replace six pairs/Zen discovery with finder, fresh Go selection, provider queues, `33 + 3N` topic slots, typed reports, scores, handoff and frozen-state validation. |
| `scripts/stage2_research_catalog.mjs` (new) | Use pinned Pi to force a bounded Go-only refresh and return a structured, dated fresh snapshot without shipped-roster fallback. |
| `scripts/stage2_research_tools.mjs` | Retain public-only tools and receipts; verify cancellation and isolated concurrent receipt paths. |
| `scripts/check_research_handoff.py` (new) | Check v2 decision coverage, answered human links, neighbours and criterion bases; exit 0/1/3. |
| `model-endpoints.yaml` | Replace Zen endpoint/roles with explicit research roles and dynamic Go-only `online_free` policy/include/exclude; add Qwen research-only without changing the review ladder. |
| `prompts/01-explore.md` | State finder, topics, identical perspectives, evidence boundaries and class routing. |
| `prompts/01a-interview.md` | Derive linked questions from decisions/disagreements; explain that minimums are no ceiling. |
| `prompts/02-spec.md` | Require confirmed neighbours and claim/answer basis for criteria from v2 research. |
| `prompts/research-swarm/finder.md` (new) | Four locator lists, same input for the trio, no design judgement. |
| `prompts/research-swarm/finder-merge.md` (new) | Opus merges sourced lists without accepting neighbour suggestions. |
| `prompts/research-swarm/public-topic.md` (new) | Opus writes only the mechanically filtered public sentence. |
| `prompts/research-swarm/public.md` | Topics 9–11 and source priorities, fixed report contract, no private context. |
| `prompts/research-swarm/repository.md` | Topics 1–8, their exact questions/boundaries, same perspectives and template. |
| `prompts/research-swarm/report.md` (new) | Common structured template: at most seven identified claims plus counter-evidence, unread, neighbours and typed questions. |
| `prompts/research-swarm/judge.md` | All topics, source checks, per-model scoring and complete interview-obligation inventory. |
| `templates/spec.md` | Document optional given/confirmed `neighbours:` and v2 criterion-basis form. |
| `AGENTS.md` | Replace obsolete free/six-pair routing and add the handoff rule within the existing size limit. |
| `docs/WORKFLOW.md` | Align phase 1/1a/2, provider concurrency, public boundary and handoff-gate scope. |
| `decisions/gates.yaml` | Register `research-handoff`, blocking, both placements, no tracker/history dependency, floor false. |
| `.github/workflows/ci.yml` | Regenerate from the one gate list; never edit its commands by hand. |
| `scripts/kit/manifest.yaml` | Carry the new checker and its tests as mechanism; existing prompt-prefix coverage stays. |
| `scripts/kit/probe.py` | Update affected model-resolution case ids only if needed, retaining exception reasons/count/cap. |
| `tests/test_stage2_swarm.py` | Inject the pinned-wrapper stand-in explicitly, trap bare-Pi escapes, replace obsolete free/pair expectations and add finder/trio/same-brief/report/queue/failure mutations. |
| `tests/test_stage2_research_catalog.py` (new) | Offline real-pinned-Pi catalog fixtures: forced refresh, provider filtering, shipped-cache contamination, malformed/empty/error outcomes and source audit. |
| `tests/test_stage2_research_tools.py` | Keep real tool-call shape, destination/receipt faults and concurrent scratch separation checks. |
| `tests/test_stage2.py` | Retain small-class, Haiku 5.5, other-verb and exact-check regression coverage. |
| `tests/test_model_endpoints.py` | Resolve static research roles and dynamic public-only Go free permission; validate selection policy; remove Zen free-billing expectations. |
| `tests/test_research_handoff.py` (new) | Fixture-based gate tests, including lost-decision mutation, archive, neighbour/basis and unmeasured cases. |
| `tests/test_ci.py` | Verify new gate registration and generated-CI coverage without weakening existing ratchets. |
| `tests/test_kit.py` | Prove the checker and tests travel without corpus or missing imports. |
| `plans/changes/research-swarm/spec.md` | Hold the amended contract and neighbour/basis references. |
| `plans/changes/research-swarm/design.md` | Keep the shaped boundaries consistent with the implementation. |
| `plans/changes/research-swarm/plan.md` | Convert pending ledger rows when tests land and append measured phase-4 time. |
| `plans/changes/research-swarm/research.md` | Preserve past reports; append redraft facts, capture evidence and later live qualification. |
| `plans/changes/research-swarm/decisions.md` | Preserve all human answers; append only actual later answers or reasoned detail records. |
| `plans/changes/research-swarm/findings.md` | Preserve existing reviews and the open offline-capture blocker; record later review dispositions. |
| `docs/adr/0020-phase-1-research-swarm.md` (new) | Propose this complete amended subsystem in the decision PR. |
| `plans/INDEX.md` | Runner regenerates after artifact changes. |

## Build sequence

1. Write red-first fixtures for the amended graph: `39 + 3N` slots, finder
   barrier, 24 repository and `9 + 3N` online calls, identical topic task hashes
   and exact model roles. Include `N=0`, a changed catalog on the next run and
   free seats forbidden in every private role.
   Replace obsolete free-discovery/pair tests rather than preserve incompatible
   assertions. Keep unchanged isolation/source/fallback regression tests.
   First repair `sworld`: inject `stage2.PI_WRAPPER` with a separately named
   stand-in, as the existing `tests/test_stage2.py::world` fixture does.
   Make a bare `pi` on PATH fail, then assert version and model calls all use
   the injected wrapper. Preserve the restricted PATH and synthetic secrets;
   do not execute the installed Pi in orchestration unit tests or disable its
   production version check to make these fixtures pass.
2. Read role identities from the declaration. Use Go Pi for repository/finder
   DeepSeek/MiMo, official read-only Claude Code for Haiku and Opus. Declare
   Qwen research-only and validate purpose/data-class per invocation, not
   endpoint capability alone; retain default framework residency checks.
   Remove Zen transport, its fixed roster/focuses and endpoint billing category.
   Declare `online_free: {provider: opencode-go, suffix: "-free", include: [],
   exclude: []}`: empty include means all eligible chat ids, nonempty narrows,
   exclude wins. Reject malformed/non-free policy with exit 2; missing explicit
   includes yield incomplete exit 1. No list grants private permissions.
   Use the one pinned Pi install, never self-update it or install another client.
   Route version checks and every repository/public model launch through
   `stage2.PI_WRAPPER`; replace the swarm's remaining bare `pi` launches.
   The catalog helper imports only that pinned install. Real-Pi tests keep
   the actual wrapper, with its declared Node and required shell utilities
   available; their offline local server replaces the provider, not Pi.
   Before model dispatch, `stage2_research_catalog.mjs` uses its ModelRuntime
   to refresh only Go with `allowNetwork: true`, `force: true`, fresh scratch
   and a 60-second bound inside the run deadline. Inspect errors/aborted state
   and the fresh provider snapshot, not just the effective union with shipped
   models or a successful `--list-models` exit. Validate Go origin/chat schema,
   provider and identities before selection. Record version/source/time/digest,
   eligible/policy/selected/excluded ids and reasons; freeze `N` and slots.
   Refresh failure or ambiguity exits 1 before models, never Flash-only or Zen
   fallback. Valid empty selection records `N=0` and retains 39 fixed calls.
   Test with a local catalog server and actual pinned Pi refresh implementation;
   force a request despite a fresh cache and reject removed shipped free ids.
   This drafting phase performs no network refresh; live qualification is later.
3. Implement frozen packets and stages: finder trio → Opus merge → Opus
   sentence → all topic research → Opus judge. Finder map has code, rules,
   tests and neighbours with path/symbol/section, reason and provenance.
   Given neighbours come from research header; suggestions remain marked.
   Topic scopes/questions are exactly spec's Topic contract: 1 code/reuse,
   2 callers/interfaces, 3 rules/class, 4 architecture, 5 neighbours,
   6 history/volatility, 7 tests, 8 risks, 9 practices, 10 tools, 11 failures.
4. Use independent provider queues capped at four across roles. Serialize
   dispatch-time declaration/exact-prompt leak checks and audit writes; recheck
   deadline/stop after scanning and before launch. Refusal exits 2, cancels
   queued work, stops/reaps running children and retains partial evidence.
   Ordinary call failure permits remaining slots but never a complete result.
   Budget: `39 + 3N` model invocations; 5-minute sentence, 10-minute finder/
   researcher/map merge, 15-minute judge, 150-minute run including catalog
   preflight. All Go Flash/free roles share four permits; no silent roster cap,
   retries, debate or delegation. A large roster hitting the deadline remains
   incomplete with every unfinished slot named.
5. Build identical task bodies for every seat of a topic (repository trio or
   Flash trio plus all selected Go free models), with all three common
   perspectives: state/evidence, counter-evidence/gaps, boundary effects.
   Keep transport metadata separate. Buffer reports until the stage ends or
   aborts so peers cannot read answers from appended research. Online gets
   only the filtered Opus sentence plus fixed topic/template/public data;
   repository peers get the same private packet/map. No public report enters
   private peers' initial briefs; the judge combines both sides later.
6. Reuse scratch-only public Pi, explicit public-tool allow-list, minimal
   environment, discovery/retry disablement, pinned DNS/family and redirect
   validation. Each process owns its scratch and receipt file. Collect stdout,
   stderr and receipts even on failure before cleanup; scrub all credentials.
   With the maintainer present, run the open F-1 offline capture on real pinned
   Pi and synthetic private canaries using a local mock model server; it sends
   no external request. Record version/source hashes, method, outbound model
   payloads/tool schemas, discovery and file/shell/private-address attempts,
   receipt behavior and canary outcomes in research. Use the repository pin
   (currently Pi 1.2.0), include Qwen and dynamically selected Go free transport
   envelopes, plus catalog metadata isolation. A stand-in's argv alone does not satisfy this step.
7. Validate structured topic reports: max seven claims with stable ids,
   statement/evidence/kind/confidence-basis, counter-evidence, not-read,
   neighbour relation and classified questions. Online neighbour relation is
   explicitly unknown. Finder uses four locator lists instead of this cap.
   Opus judge validates all topic coverage and source references, records
   supported/refuted/unique/off-brief claim lists/counts for all Flash/free
   models and retains dissent. No silent report truncation: insufficient judge
   context capacity yields incomplete evidence, without an extra judge call. Build interview inventory from raw decisions plus disagreements;
   class mismatch and neighbour contradiction always create obligations.
8. Persist fenced `research-swarm/v2` JSON records in research (manifest,
   catalog/selection, map, slots, reports, scores, obligations) and preserve
   original evidence; manifest slots/budget derive from frozen `N`.
   Freeze tracked files plus relevant untracked change inputs; at publication
   compare bytes/HEAD, excluding own research appends/updated restamp only.
   Changed inputs yield incomplete exit 1. No participant writes artifacts.
9. Implement `check_research_handoff.py [--root DIR] [--change NAME]`:
   enumerate v2 runs in live/archive folders, derive required ids from raw
   reports and unresolved dissent, check inventory and linked Q-records
   (`research_items:`, `research_claims:`, answered maintainer/context), then
   confirmed-neighbour parity and per-criterion `*Basis:*` references. Missing
   coverage/open or agent answers are exit 1; unread/ambiguous schema/ids/files
   exit 3; no applicable run is an explicit legacy exemption. Never generate
   answers or waive decisions. Fixture mutations must remove each link in
   turn, including class/neighbour cases; every mutation must turn red.
10. Carry the interview/spec instructions, spec template, doctrine, gate and
    kit classification together; derive CI with `ci_gates.py`. Run commands
    below, obtain spec/phase-6 reviews and repair findings within the remaining
    appetite. Keep F-1 open until actual capture passes. The runner owns the
    checkpoint commit/PR. After decision merge only, qualify real Go/Pi models
    and public retrieval; record failures honestly without a fallback model.

## Verification

The implementing session uses the locked environment (`make venv` once if
needed), records actual time including repairs, then runs:

```sh
source .venv/bin/activate
python3 -m pytest tests/test_stage2_swarm.py tests/test_stage2_research_tools.py tests/test_stage2_research_catalog.py tests/test_pi_contract.py tests/test_stage2.py tests/test_model_endpoints.py tests/test_research_handoff.py tests/test_ci.py tests/test_kit.py -q
python3 scripts/check_interview_minimums.py --change research-swarm
python3 scripts/check_criterion_ledger.py
python3 scripts/check_research_handoff.py --change research-swarm
python3 scripts/ci_gates.py --generate-ci
python3 scripts/ci_gates.py --check-ci
python3 scripts/kit/probe.py --strict
make verify
```

Offline capture is a separate pre-merge requirement (step 6), not replaced by
unit tests; the orchestrator schedules it with the maintainer and records the
exact capture command/method and tested commit before clearing F-1. Full live
qualification waits for merge. Availability, usage and cost not measured are
unknown. The absent `scripts/validate_change_artefacts.py` cannot be run; use
the existing gates and let the runner own registry regeneration/full verify.

## Criterion ledger

- 1: tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm — Either class produces only the single GLM exploration report.
- 1: not yet written tests/test_stage2_swarm.py::test_swarm_uses_only_the_injected_pi_wrapper — A version or model call bypasses the wrapper, executes the real install in a unit test or resolves bare Pi from PATH.
- 2: tests/test_stage2_swarm.py::test_small_classes_keep_the_single_explorer — Either class starts a finder or swarm researcher.
- 3: tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan — Valid early input is refused because a later artifact is absent.
- 4: tests/test_stage2_swarm.py::test_missing_invalid_or_conflicting_class_refuses — A malformed YAML header, empty class or conflicting declaration is silently overridden.
- 5: not yet written tests/test_stage2_swarm.py::test_finder_merge_precedes_every_topic — A topic starts before the three finder outcomes and the Opus map are recorded.
- 6: not yet written tests/test_stage2_swarm.py::test_repository_topics_have_three_independent_models — A topic is omitted, a model substituted, or one session supplies two seats.
- 7: tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons — Code summaries replace a comparison, or an unread neighbour is called absent.
- 8: not yet written tests/test_stage2_swarm.py::test_online_requests_exclude_private_inputs_and_ambient_paths — A canary from rules, paths, identifiers, finder output, history or private reports appears in an outbound payload or query.
- 9: tests/test_stage2_research_tools.py::test_public_tools_cannot_read_local_or_private_sources — A file or shell tool is available, ambient context is discovered, or fetching reaches local files or private network addresses.
- 10: not yet written tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts — A snippet, invented URL, search-only receipt or memory-only report counts as retrieved evidence.
- 11: not yet written tests/test_stage2_swarm.py::test_role_permissions_do_not_follow_endpoint_privileges — Online Qwen receives the framework packet or a model outside its declared role is launched.
- 12: not yet written tests/test_stage2_swarm.py::test_leak_block_cancels_queued_dispatch — One scan covers several prompts, or queued work starts after a BLOCK.
- 13: not yet written tests/test_stage2_swarm.py::test_concurrent_slots_keep_distinct_audits_and_outcomes — Concurrent output cannot be assigned to a slot, or a failed slot is audited as successful.
- 14: not yet written tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map — Another model judges, a peer session is resumed, or a required topic disappears.
- 15: tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation — A majority erases a sourced objection or the judge writes a maintainer answer.
- 16: tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol — Only line numbers, nonexistent symbols, a different source state or missing original reports support a claim.
- 17: tests/test_stage2_swarm.py::test_only_the_runner_appends_research — A participant edits a file, rewrites an answer, replaces earlier research or changes git or tracker state.
- 18: tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence — Timeout receipts are discarded, a URL-free online report succeeds, or malformed output yields a complete run.
- 19: not yet written tests/test_stage2_swarm.py::test_amended_graph_and_deadlines_bound_every_launch — The frozen `39 + 3N` budget is exceeded, or a call starts after its deadline.
- 20: tests/test_stage2.py::test_explore_stage2_off_uses_haiku_without_reading_the_glm_key — It runs a swarm, reads a foreign key, names Haiku 4.5 or loses the reason.
- 21: tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential — A planted fragment survives in an answer, receipt, concurrent log or error.
- 22: not yet written tests/test_stage2_swarm.py::test_amended_doctrine_and_research_roles_agree — Six-topic or Zen-free-through-Pi instructions remain operative, the review ladder changes, or an accepted ADR is edited.
- 23: not yet written tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_online_calls — An absent, rejected, hyphenated-identifier-bearing or privately augmented topic reaches an online model.
- 24: not yet written tests/test_stage2_swarm.py::test_finder_trio_locates_four_categories_without_judging — A finder judges the design, only one searches, or files/functions, rules/ADRs, tests/gates or neighbouring specs are missing without an unread marker.
- 25: not yet written tests/test_stage2_swarm.py::test_each_topic_uses_its_agreed_questions_and_scope — Code/reuse proposes new code, an online report judges local applicability, or a neighbour report inspects unrelated implementation.
- 26: not yet written tests/test_stage2_swarm.py::test_peers_receive_identical_frozen_briefs_without_reports — One model receives a critique-only angle, a different initial map or a peer answer.
- 27: not yet written tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim — An eighth claim, duplicate id, missing confidence basis, omitted unread section or untyped question is accepted.
- 28: not yet written tests/test_stage2_swarm.py::test_model_scores_name_the_claims_they_count — Scores have no claim basis, omit a model, or turn agreement into proof without source evaluation.
- 29: not yet written tests/test_stage2_swarm.py::test_given_and_suggested_neighbours_keep_their_provenance — A finder suggestion silently becomes authoritative or a header-given neighbour is dropped.
- 30: not yet written tests/test_research_handoff.py::test_spec_neighbours_match_confirmed_research_paths — A confirmed neighbour disappears, a path escapes the repository, duplicates remain or a suggestion is silently promoted.
- 31: not yet written tests/test_stage2_swarm.py::test_decisions_and_dissent_enter_the_interview_inventory — A class disagreement or neighbour contradiction is omitted, or a question loses its originating claims.
- 32: not yet written tests/test_research_handoff.py::test_a_lost_research_decision_turns_the_gate_red — Class minimums alone pass while a research decision is lost, an open or agent-written answer is accepted, or an agent waives a required question.
- 33: not yet written tests/test_research_handoff.py::test_unread_or_ambiguous_handoff_is_not_measured — A malformed inventory, duplicate claim id, missing linked file or ambiguous answer silently passes.
- 34: not yet written tests/test_research_handoff.py::test_every_criterion_names_existing_claims_or_answers — A criterion lacks an origin, refers to a missing claim or depends on an unanswered research decision.
- 35: not yet written tests/test_stage2_swarm.py::test_volatile_fact_governance_remains_a_human_proposal — A model id is silently replaced, a changing fact is treated as timeless, or a repository-wide policy is implemented without a human answer.
- 36: not yet written tests/test_stage2_swarm.py::test_provider_limit_is_shared_across_topics_and_roles — A fifth OpenCode Go call starts across role groups, or queued work starts after a leak/declaration refusal.
- 37: not yet written tests/test_stage2_swarm.py::test_online_topics_use_the_three_declared_go_models — A free or other model replaces one of the nine mandatory Flash contributions.
- 38: not yet written tests/test_stage2_research_catalog.py::test_each_run_forces_a_fresh_go_catalog — A cached/shipped list or wrong provider supplies undated seats; the real pinned refresh never reaches the fixture server.
- 38: not yet written tests/test_stage2_research_catalog.py::test_removed_shipped_free_ids_do_not_return — A shipped id absent from the fresh remote snapshot is selected.
- 39: not yet written tests/test_stage2_swarm.py::test_selected_free_models_cover_all_online_topics_on_identical_briefs — A selected model misses a topic, an excluded model runs, or peer brief hashes differ.
- 39: not yet written tests/test_stage2_swarm.py::test_go_free_policy_filters_and_freezes_each_run — Include/exclude precedence is lost, a missing explicit include passes, duplicates run, or mid-run discovery mutates the roster.
- 40: not yet written tests/test_stage2_swarm.py::test_dynamic_free_permission_is_public_only — A Go free model fills a private role or receives private context through the endpoint's framework permission.
- 41: not yet written tests/test_stage2_research_catalog.py::test_unmeasured_catalog_never_becomes_zero_availability — Timeout, malformed data, refresh errors or stale-only responses become success.
- 41: not yet written tests/test_stage2_swarm.py::test_catalog_failure_stops_before_all_model_calls — Catalog failure starts any model or falls back to a fixed/Zen roster.
- 42: not yet written tests/test_stage2_swarm.py::test_measured_empty_catalog_keeps_all_fixed_slots — Valid zero selection is refused or drops one of the 39 fixed slots.
- 4: tests/test_stage2_swarm.py::test_an_unreadable_header_or_empty_class_refuses — malformed or empty class input is routed.
- 8: not a test — step 6 real-Pi offline capture; a private canary in an outbound request refutes isolation.
- 9: not a test — step 6 real-Pi offline capture; any available local tool or discovered private context refutes isolation.
- 9: tests/test_stage2_research_tools.py::test_the_tools_run_as_pi_calls_them — the actual tool signature loses parameters or yields an invalid result.
- 10: tests/test_stage2_research_tools.py::test_search_results_carry_the_decoded_destination — redirect wrappers stand in for destination URLs.
- 16: tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state — citations use another state or supporting reports vanish.
- 18: not yet written tests/test_stage2_swarm.py::test_every_failed_slot_keeps_partial_output_before_cleanup — cancelled or failed Claude/Pi children lose partial evidence or leave a complete run.
- 19: tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent — a spent allowance still starts a process.
- 22: not a test — phase-6 review and PR file list; an accepted ADR edit or second new ADR refutes the delivery contract.
- 32: not yet written tests/test_research_handoff.py::test_live_archive_and_legacy_handoff_scope — archival or a second v2 run lets an unanswered obligation escape.
- 32: not yet written tests/test_ci.py::test_research_handoff_blocks_local_and_hosted_verification — the gate is absent, advisory or not generated into CI.
- 32: not yet written tests/test_kit.py::test_research_handoff_checker_and_tests_travel — the kit carries a gate whose checker or dependencies are absent.
- 36: not yet written tests/test_stage2_swarm.py::test_stages_dispatch_concurrently_within_provider_limits — all independent slots are serialized despite free provider capacity.

## Not touched

Accepted ADRs, numbered-decision continuity map, adoption records, human answer
content, session runtime/policy, review-ladder membership/order, sibling
checkouts, tracker and user configuration stay. No automatic global model
policy or Zen/free CLI transport. Only interview/spec traceability changes beyond
phase 1; other workflow phases and their model routes stay. Existing kit
exception allowance is not increased to hide new failures.

## Explore fallback

This change's original exploration used Stage 2 GLM 5.3 Flash on 2026-10-14;
research records no Stage-1 exploration fallback. Keep the earlier implementation
fallback as dated evidence: Stage-1 `implement`, `claude-sonnet-5-5`, reason
"two Flash post-run checks failed" (runner route, 2026-10-15). It is not the
new exploration route. Future explicit exploration fallbacks carry route,
model and reason into their plan.

## Draft handoff — 2026-10-16

Baseline `6146fde`, branch `explore/research-swarm`; local `origin/main`
comparison shows ADR 0020 as the sole new ADR. Q-10 adds Go free online seats
and live selection; Q-1–Q-9 and prior phase-4 records remain unchanged.
No phase-2a open rows exist in the read findings; phase-6 F-1 remains open
for its attended capture. Hosted PR state and parallel-session ownership were
not read outside this worktree; no tracker access is assumed.

This drafting call changes only artifacts inside the change folder and the
existing unmerged ADR 0020. No implementation, model call, commit, git mutation
or full verification is performed; the runner owns verification/checkpoint
and the orchestrator shows the card unchanged before phase 4. Resume with
spec review, then implement within the existing remaining appetite and run
the attended offline capture before merge. Validation evidence from this
redraft follows; runtime implementation and qualification remain unmeasured.

Draft validation, 2026-10-16: `.venv/bin/python
scripts/check_interview_minimums.py --change research-swarm` and
`.venv/bin/python scripts/check_criterion_ledger.py` passed. Structural checks
confirmed 42 numbered criteria with refutations/bases, required metadata and
design sections, the opening card, one ledger, retained phase-4 time history,
local links and pending ADR approval. `git diff --check` passed. The named
change-artifact validator is absent; tracker-backed registry, full
`make verify`, offline capture and live qualification are left to the runner
and the later attended implementation step, not claimed green here.

### Draft retry — 2026-10-16

The supplied earlier-attempt verifier is red: 46 swarm tests fail while the
real pinned wrapper runs under `sworld`'s restricted PATH. Read-source evidence
in research identifies the unpatched `PI_WRAPPER` and remaining bare-Pi
launches. Steps 1–2 now name the fixture and runtime repairs explicitly.
No code is repaired in this draft, no failing test is removed, and the
runner's next `make verify` may remain red until phase 4 performs those
repairs. Unrelated Markdown diagnostics are not treated as fixed here.

The retry leaves all 42 acceptance criteria, class, appetite and human answers
unchanged. Earlier implementation time stays below; the final `Time used`
section is reserved for execution of this amended plan.

Retry validation, 2026-10-16 at baseline `6146fde`: interview-minimums,
criterion-ledger and `git diff --check` pass. Local structural checks confirm
all required headers/sections, criterion refutations/bases, the opening card,
one ledger, empty `Time used`, resolved local links and pending ADR approval.
SHA-256 comparison with this retry's entry state confirms the acceptance
criteria, human-answer file and findings are unchanged. This is artifact
validation; no new runtime, full-suite or isolation-capture result is claimed.

Attempt 3 (route glm, glm-5.3, 2026-10-16) changed artifacts only and ran no
command. Its read-only check confirmed every named ledger test is defined,
every promised test is absent and criteria 1–42 stay covered; the 46 verifier
failures remain the pre-existing wrapper-fixture mismatch that step 1 repairs.
No criterion, maintainer answer, class or appetite changed. The verification
is recorded in research.md ("Third draft attempt evidence", 2026-10-16).

## Earlier implementation time

Historical phase-4 entries are retained below; this redraft adds no phase-4
time and does not reset the 12-hour stop. The unmeasured span prevents a
claim about the exact remaining appetite; establish it before resuming.

2026-10-15 repair attempt 3, span not measured: this session had no command tool to read `date`.
2026-10-15 completion (Opus 5.5): 05:15–05:31 CEST, about 16 minutes including one `make verify` run (05:20:38–05:30:25, green: 2038 passed, 16 skipped).

2026-10-15 05:49:28–06:00:30 CEST, 11 minutes 2 seconds (Codex repair of L1-1–L1-8; no break).

2026-10-15 09:40–10:31 CEST, about 51 minutes (Opus 5.5 sub-agent repair of phase-6 F-2 to F-10 outside `stage2.py repair`, maintainer-approved; four `make verify` runs of about 8–10 minutes each, the first red on formatting and a stale `updated:`; no break).

The earlier plan cited `docs/journal/handover/2026-10-15-research-swarm-loop-one-repair.md`; that file is not present in this worktree and was not read by this redraft.

## Time used
