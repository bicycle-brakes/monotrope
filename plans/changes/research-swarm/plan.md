---
title: "Plan — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-17
updated: 2026-10-17
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-17"}
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
| `scripts/stage2_research_catalog.mjs` (new) | Use pinned Pi to force a bounded Go-only refresh and return a dated fresh snapshot cross-checked against credential-free models.dev tool_call/status metadata, with explicit capability-unavailable fallback. |
| `scripts/stage2_research_tools.mjs` | Retain public-only tools and receipts; verify cancellation and isolated concurrent receipt paths. |
| `scripts/check_research_handoff.py` (new) | Check v2 decision coverage, answered human links, neighbours and criterion bases; exit 0/1/3. |
| `model-endpoints.yaml` | Replace Zen endpoint/roles with explicit research roles and dynamic Go-only `online_free` policy/include/exclude; add Qwen research-only without changing the review ladder. |
| `prompts/01-explore.md` | State finder, topics, identical perspectives, evidence boundaries, class routing and the required research neighbours list (explicit [] allowed). |
| `prompts/01a-interview.md` | Derive linked questions from decisions/disagreements; explain that minimums are no ceiling. |
| `prompts/02-spec.md` | Require confirmed neighbours and claim/answer basis for criteria from v2 research. |
| `prompts/research-swarm/finder.md` (new) | Four locator lists, same input for the trio, no design judgement. |
| `prompts/research-swarm/finder-merge.md` (new) | Tool-free Opus returns the exact finder-key union with every source/reason; runner resolves refs and inserts given neighbours. |
| `prompts/research-swarm/public-topic.md` (new) | Opus writes only the mechanically filtered public sentence. |
| `prompts/research-swarm/public.md` | Topics 9–11 and source priorities, fixed report contract, no private context. |
| `prompts/research-swarm/repository.md` | Topics 1–8, their exact questions/boundaries, same perspectives and template. |
| `prompts/research-swarm/report.md` (new) | Common structured template: local claim/question ids and links, evidence floor, topic-3 class assessment, per-packet-neighbour topic-5 relations and topic-6 volatile/governance fields. |
| `prompts/research-swarm/judge.md` | All topics, source checks, per-model scoring and complete interview-obligation inventory. |
| `templates/spec.md` | Document optional given/confirmed `neighbours:` and v2 criterion-basis form. |
| `AGENTS.md` | Replace obsolete free/six-pair routing and add the handoff rule within the existing size limit. |
| `docs/WORKFLOW.md` | Align phase 1/1a/2, required research neighbours list (explicit [] allowed), provider concurrency, public boundary and handoff-gate scope; the existing kit manifest carries these phase-1 instructions. |
| `decisions/gates.yaml` | Register `research-handoff`, blocking, both placements, no tracker/history dependency, floor false. |
| `.github/workflows/ci.yml` | Regenerate from the one gate list; never edit its commands by hand. |
| `scripts/kit/manifest.yaml` | Carry the new checker and its tests as mechanism; existing prompt-prefix coverage stays. |
| `scripts/kit/probe.py` | Update affected model-resolution case ids only if needed, retaining exception reasons/count/cap. |
| `tests/test_stage2_swarm.py` | Inject the pinned-wrapper stand-in explicitly, trap bare-Pi escapes, replace obsolete free/pair expectations and add finder/trio/same-brief/report/queue/failure mutations. |
| `tests/test_stage2_research_catalog.py` (new) | Offline real-pinned-Pi catalog fixtures: forced refresh, provider filtering, shipped-cache contamination, malformed/empty/error outcomes, models.dev intersection/deprecation/failure, and both sources’ audit. |
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

0. Before phase-4 code or tests, establish the unmeasured historical repair
   span as specified under Earlier implementation time below; add measured
   spans there and under Time used to determine the remainder of 12 hours.
   If no record bounds it, raise the appetite stop immediately, build nothing
   further, and wait for the maintainer's continue with a new total. Drafting
   phases 2/3 consume no phase-4 time.
1. Write red-first fixtures for the amended graph: `39 + 3N` slots, finder
   barrier, 24 repository and `9 + 3N` online calls, identical topic task hashes
   and exact model roles. Include `N=0`, a changed catalog on the next run and
   free seats forbidden in every private role. Add the phase-2a boundary
   fixtures listed in the criterion ledger below; do not treat existing
   earlier-slice tests as proof of amended behavior.
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
   includes exit 1 at preflight before any model call, even if excluded. No list grants private permissions.
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
   models or a successful `--list-models` exit. Only freshly fetched overlay
   ids are eligible. For pinned Pi 1.2.0 use `isModelType(model, "chat")`
   (absent type means chat) and `input` containing `text`. The typed interface
   has no dedicated tool-support boolean. Q-11 instead requires an independent
   credential-free GET of https://models.dev/api.json and exact lookup under
   opencode-go.models: boolean tool_call true and status not deprecated.
   Intersect with fresh Pi text-chat -free ids, never union in models.dev-only
   ids; never infer support from Pi compat flags. Require fixed Go
   DeepSeek/MiMo/Qwen ids as text-input chat in the fresh overlay: absent,
   baseline-only or non-chat exits 1 before any model as fixed-model-unavailable,
   naming the id. Do not consult models.dev for fixed models or Claude Haiku.
   For models.dev, request failure/timeout, non-200, non-JSON/non-object root,
   absent/non-object opencode-go or models, and duplicate claimed model ids
   are document-level capability-unavailable: exclude all free candidates,
   retaining 39 fixed slots with N=0 distinct from measured eligible-empty.
   Otherwise exclude only the affected candidate: missing entry is
   metadata-missing; non-object entry, present non-boolean tool_call,
   non-string status or id/key mismatch is metadata-malformed with raw value.
   Absent/false tool_call is no-tool-support; deprecated is deprecated.
   Keep not-chat/baseline-only reasons; ignore other providers' entries.
   An explicit include is still required and exits 1 if ineligible. Start both
   reads together at catalog preflight; abort unfinished requests at its shared
   60-second deadline. Unfinished Pi exits 1 whatever models.dev did. Successful
   Pi with unfinished models.dev records capability-unavailable/timeout, N=0
   and keeps fixed slots unless an explicit include is unmet. Neither read
   retries or extends the deadline; models.dev has no Go key or private data.
   Validate Go origin, provider and identities before selection. Record version,
   both sources’ retrieval time/digest/outcome, exact tool_call/status evidence,
   eligible/policy/selected/excluded ids and reasons; freeze `N` and slots.
   Pi refresh failure/timeout/stale-only/malformed/ambiguous data exits exactly
   1 before models, never 0/2/3 or Flash-only/Zen fallback. The absence of a Pi
   tool-support field is expected under Q-11, not a Pi refresh failure.
   Valid empty selection records `N=0` and retains 39 fixed calls.
   Test with a local catalog server and actual pinned Pi refresh implementation;
   force a request despite a fresh cache and reject removed shipped free ids.
   Fixtures join Pi and models.dev by exact provider/id, covering true/false/
   absent tool_call, missing entry/provider, deprecated and non-deprecated
   status, models.dev-only ids, malformed/unreachable metadata and explicit
   includes during capability-unavailable fallback. Failure fixtures assert
   the fixed-slot graph as well as the exact exit, not just selection output.
   Add every document-level/per-candidate shape above, including string/null/
   numeric tool_call and a malformed unrelated provider. X with tool_call
   "true" must be excluded while Y with true is selected. Missing fixed Qwen
   and baseline-only Qwen must start no calls. A fake monotonic clock checks
   Pi at 5 seconds/models.dev never answers (39 fixed slots after abort at
   60) versus Pi never answers/models.dev at 1 second (exit 1, no models).
   At N=1 with a deprecated excluded candidate, require models.dev URL/UTC/
   digest and that candidate's reason/status value; deleting any fails audit.
   This drafting phase performs no network refresh; live qualification is later.
3. Implement frozen packets and stages: finder trio → Opus merge → Opus
   sentence → all topic research → Opus judge. Finder map has code, rules,
   tests and neighbours with path/symbol/section, reason and provenance.
   Freeze HEAD plus copies/digest of every tracked file and every untracked
   non-ignored file inside the change folder. Keep copies in run scratch
   outside the repository until publication/abort, then delete them; failed
   freezing exits 1 before models. Persist full and untracked-per-path digests,
   never whole-file snapshots in research, briefs or the change folder.
   Validate the Opus merge as the exact category/reference key union of all
   finder entries, with every finder/reason retained and no duplicates.
   Dropped/added keys fail preparation (exit 1). Resolve entries using frozen
   bytes; retain unresolved marks but exclude them from topic scope. Insert
   every header-given neighbour as given even if omitted by all finders or
   labelled suggested. Runner insertions are separate from the union check.
   Resolve neighbour-category artifact paths in plans/changes/<name>/ to that
   folder's frozen spec.md, deduplicated by spec path with all finder keys
   retained. Outside a change or without its spec, keep no-spec and a gap,
   requiring no topic-5 relation. Test design.md::Data model with/without
   a sibling spec: only with it is that spec path a required packet neighbour.
   Given neighbours must be unique
   repository-relative spec.md paths present in that frozen state, otherwise
   preflight exit 2 before models. A swarm research header must explicitly
   hold neighbours: [] or a valid list; missing/null/non-list refuses with
   exit 2 and a message naming those repairs. Test missing versus empty list:
   no call versus normal finder dispatch. Single-explorer routes are unchanged.
   Suggestions remain marked; failed reads
   after valid preflight remain gaps without failing the run by themselves.
   Private brief for finders/topic author: frozen research header/body plus
   decisions/spec when present, bead id only and tracker text not read.
   Embed identical AGENTS.md for repository seats and disable automatic
   instruction loading on every runtime.
   Topic scopes/questions are exactly spec's Topic contract: 1 code/reuse,
   2 callers/interfaces, 3 rules/class, 4 architecture, 5 neighbours,
   6 history/volatility, 7 tests, 8 risks, 9 practices, 10 tools, 11 failures.
   After map merge and before any topic, collect local read-only git history
   against frozen HEAD: at most ten latest commits per resolved mapped path,
   full hash, UTC author date, subject, body capped at 4,000 characters with
   truncation flag, and touched mapped paths; mark older history not read.
   Only topic 6 gets the identical packet. A full packet hash resolves to its
   recorded excerpt; reachable-but-absent hashes and standalone PR/bead ids
   stay unsupported. Fixtures check all three cases, per-path limits, equal
   topic-6 packets and history failure (exit 1, no topic). No tracker/network.
4. Use independent provider queues capped at four across roles. Serialize
   dispatch-time declaration/exact-prompt leak checks and audit writes; recheck
   deadline/stop after scanning and before launch. Refusal exits 2, cancels
   queued work, stops/reaps running children and retains partial evidence.
   Finder/merge/topic-author failure prevents every later stage and exits 1;
   rejected topic syntax also exits 1. Topic-stage failures allow sibling
   slots to finish; required failures prevent judge and completion, whereas
   failed free seats are named best-effort outcomes and do not prevent either.
   Security refusal stops/reaps active children, retains available output and
   receipts as cancelled, and exits 2 in preference to any exit 1.
   Budget: `39 + 3N` model invocations; 5-minute sentence, 10-minute finder/
   researcher/map merge, 15-minute judge, 150-minute run including catalog
   preflight. All Go Flash/free roles share four permits; no silent roster cap,
   retries, debate or delegation. Reserve the judge's 15 minutes. Order queued
   required slots before any free seat: repository topics 1–8 then online
   Flash 9–11, topic then declared model order; free slots follow by topic then
   sorted id. Launch only with positive time before the reserve; use the
   lesser role/remainder allowance and recheck after leak scanning. Unlaunched
   slots are not-started-deadline: incomplete only if required. Large free
   rosters cannot spend the reserve or silently lose outcomes.
5. Build identical task bodies for every seat of a topic (repository trio or
   Flash trio plus all selected Go free models), with all three common
   perspectives: state/evidence, counter-evidence/gaps, boundary effects.
   Keep transport metadata separate. Buffer reports until the stage ends or
   aborts so peers cannot read answers from appended research. Online gets
   only the filtered Opus sentence plus fixed topic/template/public data;
   its <=20 words use Unicode letters and single internal hyphens/apostrophes,
   allow whitespace, comma/semicolon/parentheses, double quotes/guillemets,
   word-edge apostrophes as quotes, spaced en/em dashes and one final period
   or question mark. Internal straight/typographic apostrophes require letters
   on both sides. Count words after separators, preserving internal joins;
   reject every other character and lower-to-upper transition inside a
   hyphen segment, as spec’s allow-list requires. Reject whole case-insensitive
   tokens
   matching the frozen change/bead names or tracked path components/stems
   containing hyphen/underscore/dot/digit. Do not deny ordinary letters-only
   symbol words. Test Q-6's German example and multi-agent as accepted by the
   character rule, plus Isolation, Prüfung und Wiederherstellung für
   Agentenläufe, word-edge quotes and typographic apostrophes; reject digits,
   research-swarm/bead names and unsupported punctuation such as [, {, @, =.
   Leak check remains
   independent. Filter rejection prevents the whole topic stage (exit 1);
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
7. Validate topic reports before judge: C1–C7 and Q1… ids unique within
   each report, questions with classification and nonempty local claims list,
   confidence basis/counter-evidence/not-read/neighbour fields, topic-3
   class_assessment {class, claims}, topic-5 neighbour_relations (exactly one
   path/relation/nonempty local claims list per packet neighbour; reject
   missing/extra/duplicate paths or bad links), topic-6 volatile and governance
   central|runtime|dated when true. Template violations fail the slot; bad
   citations mark claims unsupported without dropping them. Require one
   evidence-backed claim per report (one successful page-backed claim online),
   not success for every fetch. Runner namespaces claims/questions as
   <run>/<topic>/<endpoint-qualified-model-seat>/<local>.
   Launch all Opus roles (merge, author, judge) with --tools "", restricted,
   safe-mode and strict MCP settings; assert no file/shell/web/MCP tool or
   ambient discovery in their launches. Judge sees only its packet: required
   valid reports/all free outcomes/map and runner-resolved evidence excerpts
   per valid claim (frozen symbol/section, topic-6 packet commit record or
   receipt), joined in citation order and capped at 4,000 Unicode characters
   per claim in total with explicit truncation flags. Persist bounded
   excerpts, not whole-file snapshots. Supported means that evidence supports
   the claim and no evidence-backed peer claim contradicts it; one exclusive
   disposition per valid claim (off-brief precedes
   supported/refuted/unresolved), unique only as a supported subset, and
   unsupported separately. Keep counts and global-id lists per model/topic,
   opposing ids/evidence for disagreements, three comparison sections and gaps;
   reject answer fields. Phase 6 checks semantic scope, faithful dissent,
   volatility classification and comparison/basis quality. Before enabling
   judge dispatch, derive one fixed whole-packet Unicode-character limit J
   from documented/reported pinned-Claude Opus context capacity minus a fixed
   output reserve. Record numeric capacity/reserve, conservative conversion,
   J, source and read-on date; this draft has not measured the capacity.
   Measure the full assembled packet, including instructions, before the
   judge. Above J: no judge, retain all reports/excerpts, incomplete exit 1
   as judge-packet-over-limit; at J: dispatch subject to normal preconditions.
   No additional excerpt shortening, N reduction or extra judge call.
   Fixtures check J and J+1 and three 4,000-character sources producing one
   4,000-character claim excerpt in citation order, flagged truncated.
8. Persist fenced research-swarm/v2 manifest, catalog, map, slot, report,
   reconciliation and inventory records append-only in research.md. Mark the
   fixed 39 slots required and free slots best-effort, each with one terminal
   outcome. Compare HEAD and full frozen digest before publication, excluding
   only runner-owned research appends/updated restamp. Other drift names
   changed paths and exits incomplete 1, preserving reports/excerpts/digests
   while deleting scratch frozen copies after publication or abort.
   Derive obligations from every accepted raw DECISION question (even scored
   off-brief/refuted), unresolved judge disagreements, runner-detected class
   mismatches, and topic-5 neighbour_relations: every contradicts and every
   unrelated given path derives an item even without a DECISION question or
   judge mention. Judge findings may add but cannot remove obligations.
   Group duplicates into H-<n> but preserve all global question/claim sources.
9. Implement check_research_handoff.py [--root DIR] [--change NAME] over live
   and archive folders with no tracker/network/model dependency. Parse all v2
   records; malformed/unreadable evidence or ambiguous ids/links exit 3.
   Only complete runs support interview/spec and carry obligations, including
   earlier complete runs after reruns; incomplete claims cannot support bases.
   Check coverage independently of judge inventory, then Q-record headers
   research_items/research_claims, actual answer, maintainer and context. One
   Q-record can answer items from multiple runs. Item links are <run>/H-<n>,
   claim links are global ids and criterion Q bases are decisions.md#Q-<id>; explicit human rejection
   counts, no agent waiver does. Valid pending items before spec.md exists
   are listed with exit 0; once it exists missing answers or v2 runs with none
   complete exit 1. Legacy without v2 is an explicit exemption. With a spec,
   resolve each Basis to supported complete-run claims or maintainer-answered
   decisions.md Q-records. Every direct claim must be supported; a mixed Basis
   still exits 1 if any named claim is unsupported/refuted/off-brief/unresolved.
   Those claims need an answered Q-record basis, optionally linked through
   research_claims. Enforce exact neighbour parity: confirmed + given + linked
   maintainer additions - linked maintainer drops of given or confirmed
   paths, taking confirmed/given from every complete run, never just latest.
   Derive a neighbour DECISION item independently of the judge for cross-run
   confirmation/rejection conflicts and later omission of an earlier given
   path. Bind path, both complete run ids, source manifests and available
   claims. Until a linked maintainer answer drops it the path stays required;
   open items fail even with the path present. Fixtures run confirmation then
   rejection with/without the header: both fail unanswered, keep passes only
   with the path, drop only without it. Also test given-header removal across
   runs and confirmed-path drops. Arbitrary
   drafting additions, even never suggested, exit 1 unless human-answered or
   confirmed by a new complete run; use research_items for linked additions.
   Review judges relevance and fidelity, the gate checks identities.
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
- 4: tests/test_stage2_swarm.py::test_missing_invalid_or_conflicting_class_refuses — Malformed, missing or disagreeing classes pass, or a duplicate, escaping, non-spec or missing frozen neighbour path starts a call.
- 5: not yet written tests/test_stage2_swarm.py::test_finder_merge_precedes_every_topic — A topic starts before three valid finder results and a validated exact-union Opus map.
- 6: not yet written tests/test_stage2_swarm.py::test_repository_topics_have_three_independent_models — A topic is omitted, a model substituted, or one session supplies two seats.
- 7: tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons — A comparison section or an unread-neighbour gap entry is absent; semantic comparison quality is also checked in phase 6.
- 8: not yet written tests/test_stage2_swarm.py::test_online_requests_exclude_private_inputs_and_ambient_paths — A canary from rules, paths, identifiers, finder output, history or private reports appears in an outbound payload or query.
- 9: tests/test_stage2_research_tools.py::test_public_tools_cannot_read_local_or_private_sources — A file or shell tool is available, ambient context is discovered, or fetching reaches local files or private network addresses.
- 10: not yet written tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts — Search-only, snippet or invented receipts support a claim, or a receiptless claim is not retained as unsupported; a report with no evidence-backed claim is accepted.
- 11: not yet written tests/test_stage2_swarm.py::test_role_permissions_do_not_follow_endpoint_privileges — Online Qwen receives the framework packet or a model outside its declared role is launched.
- 12: not yet written tests/test_stage2_swarm.py::test_leak_block_cancels_queued_dispatch — One scan covers multiple prompts, a queued call starts after BLOCK, a running child is awaited instead of stopped, available partial output is lost instead of retained as cancelled, or exit 1 overrides exit 2.
- 13: not yet written tests/test_stage2_swarm.py::test_concurrent_slots_keep_distinct_audits_and_outcomes — Concurrent output cannot be assigned to a slot, or a failed slot is audited as successful.
- 14: not yet written tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map — Another model judges, a peer session resumes, a required topic disappears or Opus has any tool.
- 15: tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation — An unresolved disagreement loses an opposing claim id or evidence, or judge output contains a maintainer answer field; phase 6 also checks faithful treatment of dissent.
- 16: tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol — Unresolvable or line-only references become supported rather than unsupported.
- 17: tests/test_stage2_swarm.py::test_only_the_runner_appends_research — A participant edits a file, rewrites an answer, replaces earlier research or changes git or tracker state.
- 18: tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence — A failed preparatory stage dispatches a later stage, missing required topic reports still reach the judge, a report with zero evidence-backed claims passes, or a failed free seat alone makes the run incomplete.
- 19: not yet written tests/test_stage2_swarm.py::test_amended_graph_and_deadlines_bound_every_launch — An extra invocation or retry occurs, a free slot starts ahead of queued required slots, topic work consumes the judge reserve, or unlaunched slots lack not-started-deadline outcomes.
- 20: tests/test_stage2.py::test_explore_stage2_off_uses_haiku_without_reading_the_glm_key — It runs a swarm, reads a foreign key, names Haiku 4.5 or loses the reason.
- 21: tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential — A planted fragment survives in an answer, receipt, concurrent log or error.
- 22: not yet written tests/test_stage2_swarm.py::test_amended_doctrine_and_research_roles_agree — Six-topic or Zen-free-through-Pi instructions remain operative, the review ladder changes, or an accepted ADR is edited.
- 23: not yet written tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_online_calls — Invalid/missing/private topics or forbidden punctuation pass; allowed German examples or separators fail; rejection fails to stop topics with exit 1.
- 24: not yet written tests/test_stage2_swarm.py::test_finder_trio_locates_four_categories_without_judging — Only one finder runs, a fifth locator field passes, or an empty category lacks an unread marker.
- 25: not yet written tests/test_stage2_swarm.py::test_each_topic_uses_its_agreed_questions_and_scope — A packet differs from its topic prompt; report prose that proposes new code or local applicability outside that scope is scored off-brief and checked in phase 6.
- 26: not yet written tests/test_stage2_swarm.py::test_peers_receive_identical_frozen_briefs_without_reports — One model receives a different map, instruction file, angle or peer report, or its runtime auto-loads instructions.
- 27: not yet written tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim — Required fields, topic-5 per-neighbour relations or confidence basis are missing, or an eighth claim passes.
- 28: not yet written tests/test_stage2_swarm.py::test_model_scores_name_the_claims_they_count — A valid claim has two dispositions, a unique claim is not supported, an unsupported claim is supported, a score lacks claim ids, or a failed seat has no named outcome.
- 29: not yet written tests/test_stage2_swarm.py::test_given_and_suggested_neighbours_keep_their_provenance — A suggestion becomes authoritative, a given path vanishes or its proposed removal loses the human item.
- 30: not yet written tests/test_research_handoff.py::test_spec_neighbours_match_confirmed_research_paths — A required path disappears or an extra path outside confirmed/given/linked-human sets passes.
- 31: not yet written tests/test_stage2_swarm.py::test_decisions_and_dissent_enter_the_interview_inventory — A refuted/off-brief report decision is omitted, a differing class lacks an automatically derived item, or grouping duplicates loses a source question or claim id.
- 32: not yet written tests/test_research_handoff.py::test_a_lost_research_decision_turns_the_gate_red — Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
- 33: not yet written tests/test_research_handoff.py::test_unread_or_ambiguous_handoff_is_not_measured — Malformed manifests/inventories, duplicate global ids or report-local ids, missing linked files or ambiguous answers silently pass.
- 34: not yet written tests/test_research_handoff.py::test_every_criterion_names_existing_claims_or_answers — Missing/incomplete/non-supported claim ids or unanswered Q-records pass, including mixed direct bases.
- 35: not yet written tests/test_stage2_swarm.py::test_volatile_fact_governance_remains_a_human_proposal — A volatile claim without governance passes validation or a proposal is implemented without a human answer; phase 6 also checks whether changing facts were correctly marked volatile.
- 36: not yet written tests/test_stage2_swarm.py::test_provider_limit_is_shared_across_topics_and_roles — A fifth Go call starts across roles, queued work survives a leak/declaration refusal, available cancelled output is discarded, or exit 1 overrides security exit 2.
- 37: not yet written tests/test_stage2_swarm.py::test_online_topics_use_the_three_declared_go_models — A free or other model replaces one of the nine mandatory Flash contributions.
- 38: not yet written tests/test_stage2_research_catalog.py::test_each_run_forces_a_fresh_go_catalog — A cached/shipped list substitutes for refresh, a baseline-only free id is dispatched, another provider supplies a seat, or selection lacks dated provenance.
- 38: not yet written tests/test_stage2_research_catalog.py::test_removed_shipped_free_ids_do_not_return — A cached/shipped list substitutes for refresh, a baseline-only free id is dispatched, another provider supplies a seat, or selection lacks dated provenance.
- 39: not yet written tests/test_stage2_swarm.py::test_selected_free_models_cover_all_online_topics_on_identical_briefs — A selected seat is silently omitted or failed as successful, a non-selected or no-tool-support model runs, peer briefs differ, or a missing explicit include starts any model instead of preflight exit 1.
- 39: not yet written tests/test_stage2_swarm.py::test_go_free_policy_filters_and_freezes_each_run — A selected seat is silently omitted or failed as successful, a non-selected or no-tool-support model runs, peer briefs differ, or a missing explicit include starts any model instead of preflight exit 1.
- 40: not yet written tests/test_stage2_swarm.py::test_dynamic_free_permission_is_public_only — A Go free model fills a private role or receives private context through the endpoint's framework permission.
- 41: not yet written tests/test_stage2_research_catalog.py::test_unmeasured_catalog_never_becomes_zero_availability — A Pi refresh timeout, stale-only, malformed or ambiguous result becomes N=0 or exits other than 1.
- 41: not yet written tests/test_stage2_swarm.py::test_catalog_failure_stops_before_all_model_calls — Pi catalog failure starts models, uses a cached/Zen roster or exits 0/2/3 instead of 1.
- 42: not yet written tests/test_stage2_swarm.py::test_measured_empty_catalog_keeps_all_fixed_slots — Valid zero selection is refused or drops one of the 39 fixed slots.
- 4: tests/test_stage2_swarm.py::test_an_unreadable_header_or_empty_class_refuses — Malformed, missing or disagreeing classes pass, or a duplicate, escaping, non-spec or missing frozen neighbour path starts a call.
- 8: not a test — step 6 real-Pi offline capture; a private canary in an outbound request refutes isolation.
- 9: not a test — step 6 real-Pi offline capture; any available local tool or discovered private context refutes isolation.
- 9: tests/test_stage2_research_tools.py::test_the_tools_run_as_pi_calls_them — the actual tool signature loses parameters or yields an invalid result.
- 10: tests/test_stage2_research_tools.py::test_search_results_carry_the_decoded_destination — Search-only, snippet or invented receipts support a claim, or a receiptless claim is not retained as unsupported; a report with no evidence-backed claim is accepted.
- 16: tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state — Citations resolve against live instead of frozen bytes, or mid-run edits still allow complete publication.
- 18: not yet written tests/test_stage2_swarm.py::test_every_failed_slot_keeps_partial_output_before_cleanup — A failed preparatory stage dispatches a later stage, missing required topic reports still reach the judge, a report with zero evidence-backed claims passes, or a failed free seat alone makes the run incomplete.
- 19: tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent — An extra invocation or retry occurs, a free slot starts ahead of queued required slots, topic work consumes the judge reserve, or unlaunched slots lack not-started-deadline outcomes.
- 22: not a test — phase-6 review and PR file list; an accepted ADR edit or second new ADR refutes the delivery contract.
- 32: not yet written tests/test_research_handoff.py::test_live_archive_and_legacy_handoff_scope — Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
- 32: not yet written tests/test_ci.py::test_research_handoff_blocks_local_and_hosted_verification — Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
- 32: not yet written tests/test_kit.py::test_research_handoff_checker_and_tests_travel — Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
- 36: not yet written tests/test_stage2_swarm.py::test_stages_dispatch_concurrently_within_provider_limits — A fifth Go call starts across roles, queued work survives a leak/declaration refusal, available cancelled output is discarded, or exit 1 overrides security exit 2.

- 4: not yet written tests/test_stage2_swarm.py::test_invalid_given_neighbours_refuse_before_models — Missing, duplicate, escaping or non-spec paths start a call.
- 18: not yet written tests/test_stage2_swarm.py::test_preparatory_failure_prevents_dependent_stages — Finder, merge or sentence failure still dispatches a topic or judge.
- 18: not yet written tests/test_stage2_swarm.py::test_failed_free_seat_is_named_without_failing_completion — A provider failure, timeout or receiptless free report either vanishes or fails an otherwise valid run.
- 19: not yet written tests/test_stage2_swarm.py::test_required_slots_precede_free_and_reserve_judge_time — Free work starts ahead of required work, spends judge reserve, or unlaunched seats lack outcomes.
- 16: not yet written tests/test_stage2_swarm.py::test_frozen_digest_detects_tracked_and_change_input_edits — A mid-run edit to tracked or untracked change input still publishes complete.
- 10: not yet written tests/test_stage2_swarm.py::test_unsupported_claims_are_retained_and_report_requires_evidence — One bad claim fails a valid report, or a zero-evidence report passes.
- 27: not yet written tests/test_stage2_swarm.py::test_report_ids_are_local_and_questions_link_existing_claims — Duplicate local ids or dangling question claims pass; matching ids across distinct seats collide globally.
- 31: not yet written tests/test_stage2_swarm.py::test_raw_off_brief_decisions_and_class_mismatches_cannot_disappear — Judge filtering hides accepted-report decisions or a class mismatch lacks a derived item.
- 32: not yet written tests/test_research_handoff.py::test_pending_handoff_is_green_only_before_spec — Pre-spec pending items fail, or the same unanswered items pass with a spec.
- 32: not yet written tests/test_research_handoff.py::test_only_complete_runs_supply_handoff_and_prior_obligations_survive — Incomplete claims support a spec, no complete run passes, or rerunning erases obligations.
- 28: not yet written tests/test_stage2_swarm.py::test_dispositions_are_exclusive_and_unique_is_supported_subset — Unresolved evidence is forced supported/refuted, or unique marks unsupported claims.
- 35: not yet written tests/test_stage2_swarm.py::test_topic_specific_class_and_volatile_fields_are_required — Topic 3 omits its class or a volatile topic-6 claim omits governance.
- 29: not yet written tests/test_research_handoff.py::test_given_neighbour_drop_requires_linked_human_answer — A judge rejection removes a given neighbour without an answered item.
- 39: not yet written tests/test_stage2_research_catalog.py::test_free_eligibility_requires_text_chat_and_explicit_tools — Non-chat, baseline-only, missing/false models.dev tool_call or deprecated entries yield a selected seat.
- 39: not yet written tests/test_stage2_swarm.py::test_missing_explicit_include_stops_before_models — Missing included id starts fixed slots instead of preflight exit 1.
- 7: not a test — phase-6 review checks comparison meaning; code summaries presented as comparisons refute it.
- 15: not a test — phase-6 review checks faithful dissent; a majority erasing a sourced objection refutes it.
- 24: not a test — phase-6 review checks finder prose; choosing a design exceeds the locator role.
- 25: not a test — phase-6 review checks topic scope; new-code proposals or local online applicability refute it.
- 34: not a test — phase-6 review checks that resolved criterion bases actually support the criterion.
- 35: not a test — phase-6 review checks volatile classification; repeatedly changing facts treated as timeless refute it.

- 5: not yet written tests/test_stage2_swarm.py::test_merge_is_exact_finder_union_with_all_origins — A dropped, added or duplicate key dispatches topics, or deduplication loses a finder/reason.
- 24: not yet written tests/test_stage2_swarm.py::test_map_resolution_excludes_unresolved_and_inserts_given_neighbours — Live-tree resolution grants scope, or a given neighbour omitted by finders vanishes.
- 16: not yet written tests/test_stage2_swarm.py::test_frozen_copies_are_scratch_only_and_removed_after_run — Success or abort retains copies, whole-file snapshots enter research/briefs, or copy failure launches models.
- 27: not yet written tests/test_stage2_swarm.py::test_topic_five_relations_cover_exact_packet_neighbours — Missing, extra or duplicate paths or empty/dangling local claims pass.
- 31: not yet written tests/test_stage2_swarm.py::test_neighbour_relations_derive_items_without_judge_or_question — A contradicts or unrelated-given field loses its obligation when Opus omits it.
- 34: not yet written tests/test_research_handoff.py::test_every_direct_basis_claim_must_be_supported — Any non-supported disposition passes, including alongside a supported claim; answered Q-record mediation fails.
- 30: not yet written tests/test_research_handoff.py::test_neighbour_parity_allows_only_linked_additions_and_given_drops — Arbitrary extra paths pass, or linked maintainer additions fail.
- 5: not yet written tests/test_stage2_swarm.py::test_all_opus_roles_have_empty_tools_and_packet_only_context — Merge has file, shell, web or MCP access.
- 14: not yet written tests/test_stage2_swarm.py::test_all_opus_roles_have_empty_tools_and_packet_only_context — Judge has file, shell, web or MCP access.
- 23: not yet written tests/test_stage2_swarm.py::test_all_opus_roles_have_empty_tools_and_packet_only_context — Public-topic author reads beyond its private packet.
- 28: not yet written tests/test_stage2_swarm.py::test_judge_gets_resolved_excerpts_with_bounded_truncation — Valid claims lack evidence excerpts, excerpt source mismatches or cap/truncation flags fail.
- 39: not yet written tests/test_stage2_research_catalog.py::test_models_dev_capabilities_intersect_only_fresh_pi_ids — Missing/false tool_call, deprecated status, wrong provider or models.dev-only ids are selected.
- 42: not yet written tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_fixed_slots — Source failure launches free models, aborts fixed slots or masquerades as measured empty metadata.
- 42: not yet written tests/test_stage2_swarm.py::test_capability_unavailable_keeps_fixed_slots_unless_include_is_required — Default fallback blocks fixed slots, or an ineligible explicit include starts models.


- 4: not yet written tests/test_stage2_swarm.py::test_swarm_requires_neighbour_key_but_accepts_empty_list — Missing/null/non-list header starts models or explicit [] refuses; repair message omits the required key.
- 16: not yet written tests/test_stage2_swarm.py::test_history_packet_binds_only_mapped_frozen_head_commits — A hash outside the bounded packet or PR/bead id alone becomes evidence, ten-per-path/body caps fail, or history reaches another topic.
- 18: not yet written tests/test_stage2_swarm.py::test_history_collection_failure_prevents_all_topics — Failed read-only git collection starts any topic or loses partial evidence.
- 26: not yet written tests/test_stage2_swarm.py::test_history_packet_binds_only_mapped_frozen_head_commits — Topic-6 peers receive different history packets.
- 29: not yet written tests/test_stage2_swarm.py::test_neighbour_artifacts_normalize_to_change_specs_or_no_spec_gaps — A design entry is lost with a spec present, or without it becomes a packet neighbour instead of a no-spec gap.
- 27: not yet written tests/test_stage2_swarm.py::test_neighbour_artifacts_normalize_to_change_specs_or_no_spec_gaps — Topic 5 accepts a missing relation for a normalized spec path or requires a relation for no-spec.
- 29: not yet written tests/test_research_handoff.py::test_cross_run_neighbour_conflicts_require_linked_human_answers — A confirmed/rejected path or omitted prior given path loses its derived human item.
- 30: not yet written tests/test_research_handoff.py::test_cross_run_neighbour_conflicts_require_linked_human_answers — Latest-only parity passes; unanswered conflict passes with either header, keep passes without the path or drop passes with it.
- 31: not yet written tests/test_research_handoff.py::test_cross_run_neighbour_conflicts_require_linked_human_answers — Either cross-run conflict lacks path, both source runs or source evidence.
- 32: not yet written tests/test_research_handoff.py::test_cross_run_neighbour_conflicts_require_linked_human_answers — An unanswered cross-run item passes despite a spec, or a prior complete run loses authority.
- 38: not yet written tests/test_stage2_research_catalog.py::test_fixed_go_models_require_fresh_text_chat_entries — Absent, baseline-only or non-chat DeepSeek/MiMo/Qwen starts a model; models.dev is required for a fixed seat.
- 41: not yet written tests/test_stage2_research_catalog.py::test_fixed_go_models_require_fresh_text_chat_entries — Unavailable fixed id is not named as fixed-model-unavailable with exit 1 before calls.
- 42: not yet written tests/test_stage2_research_catalog.py::test_capability_document_faults_and_candidate_faults_are_distinct — A malformed candidate excludes a valid peer, a non-boolean tool_call selects a seat, or a document-level fault is treated as measured absence.
- 39: not yet written tests/test_stage2_research_catalog.py::test_capability_document_faults_and_candidate_faults_are_distinct — Candidate eligibility ignores exact metadata shape or an unrelated provider's malformed entry disables selection.
- 41: not yet written tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — Pi unfinished at 60 seconds dispatches calls or successful Pi plus timed-out models.dev aborts fixed work.
- 42: not yet written tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — Models.dev timeout extends 60 seconds, retries, lacks timeout reason or blocks 39 fixed slots without an explicit include.
- 19: not yet written tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — Reads start sequentially or receive separate 60-second budgets.
- 38: not yet written tests/test_stage2_research_catalog.py::test_nonempty_selection_keeps_both_sources_and_exclusion_evidence — At N=1, removing models.dev URL/UTC/digest or a deprecated candidate's reason and raw status fails to turn audit red.
- 39: not yet written tests/test_stage2_research_catalog.py::test_nonempty_selection_keeps_both_sources_and_exclusion_evidence — An excluded candidate is omitted while another candidate remains eligible.
- 14: not yet written tests/test_stage2_swarm.py::test_judge_packet_limit_refuses_before_launch_without_shortening — J+1 reaches the judge, J fails size validation, excerpts shrink to fit or a second call/N reduction occurs.
- 18: not yet written tests/test_stage2_swarm.py::test_judge_packet_limit_refuses_before_launch_without_shortening — Oversize loses reports/excerpts or does not end incomplete exit 1 as judge-packet-over-limit.
- 28: not yet written tests/test_stage2_swarm.py::test_judge_excerpt_cap_is_per_claim_in_citation_order — Three 4,000-character sources yield more than 4,000 excerpt characters for one claim, lose citation order or lack truncation marking.

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

## Draft handoff — 2026-10-17, third phase-2a incorporation

Baseline `63dd5d4`, branch `explore/research-swarm`. Incorporated recorded
rulings S-31–S-39 into spec, design, plan and the existing sole new ADR 0020;
findings statuses name the spec sections. Human answers and decision rulings
are unchanged; class, all 42 criterion identities and the 12-hour appetite
remain. The numeric judge-context limit is an explicit phase-4 measurement,
not a capacity invented by this draft. Earlier draft records below are
historical. The opening card remains unchanged.

The runner owns full verification, registry generation and the commit.
Hosted PR state and current parallel-session ownership were not read under
the worktree-only restriction. No tracker, provider or live model was called.
The separate attended isolation capture remains open (phase-6 F-1).
Before phase 4, establish the historical unmeasured span or raise its appetite
stop; code and test repairs remain outside this drafting call.

Artifact checks passed on 2026-10-17 against baseline `63dd5d4`:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_interview_minimums.py --change research-swarm
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_criterion_ledger.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_frontmatter_current.py
git diff --check
```

Structural comparison confirmed all 42 criterion/refutation/basis triples,
all nine round-3 status changes with original findings text preserved, other
findings (including F-1) unchanged, unchanged card/class/appetite/ADR claim/
neighbours, one ledger and empty Time used. Only decisions.md's `updated:`
metadata was restamped to 2026-10-17; every answer and ruling is byte-for-byte
unchanged. ADR 0020 remains the sole new ADR relative to local origin/main,
pending approval; no second ADR, human answer or code/test change was made.
The named artifact-validator script is absent. The tracker-backed registry
was not read because this call may not read outside the worktree/git metadata.
Full `make verify`, runtime qualification and the known pinned-wrapper
fixture repair remain the runner/implementation session's work.

## Draft retry — 2026-10-17, third phase-2a incorporation

Rechecked the retained spec, design, plan and sole ADR draft against baseline
`63dd5d4` and the supplied attempt-1 diagnostics. Restamped only
`decisions.md`'s `updated:` to 2026-10-17; all answers and rulings remain
unchanged. The interview-minimums, criterion-ledger, frontmatter-current and
`git diff --check` commands above passed again in this retry.

The supplied full run still reports 46 failing swarm tests at the pinned-Pi
wrapper check. Source inspection confirms that `require_pi` uses the absolute
`stage2.PI_WRAPPER`, while `sworld` supplies a PATH stand-in without injecting
that wrapper. Steps 1–2 retain the required implementation repair. No code or
test was changed, and the full suite was not rerun here; artifact checks do
not establish green runtime verification. The runner owns that check and the
commit. The named artifact validator remains absent, and the tracker-backed
registry remains unread under the worktree-only restriction.

## Draft handoff — 2026-10-17, second phase-2a incorporation

Baseline 9beb00d, branch explore/research-swarm. Spec, design and this plan
incorporate recorded rulings S-21–S-30 and maintainer answer Q-11, preserving
class, 42 criterion numbers, appetite and all human answers. ADR 0020 remains
the single new ADR relative to the local origin/main reference. Its two-source
selection, scratch lifetime and handoff terms move with this redraft; no
second ADR or approval is created. Findings statuses point to spec locations.

The runner owns full verification, registry regeneration and the commit.
Hosted PR state and current parallel-session ownership were not read under
the worktree-only restriction. No tracker access, external catalog/model call
or offline capture occurs here. Phase-6 F-1 still requires the separately
scheduled maintainer-attended capture. Before code resumes, establish historical
time or raise the appetite stop; then repair the pinned-wrapper seam and
implement the amended graph within the measured remaining appetite.

Artifact validation on 2026-10-17 at baseline 9beb00d passed:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_interview_minimums.py --change research-swarm
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_criterion_ledger.py
git diff --check
```

Read-only structural checks also passed for all 42 criterion/refutation/basis
triples, S-21–S-30 incorporation with original finding text preserved, unchanged
F-1 and human answers, fixed class/appetite/ADR claim/neighbours, opening card,
single ledger, empty Time used, metadata/design sections, local links and
permitted paths. These are artifact checks, not runtime qualification. The
named validate_change_artefacts.py is absent; no full suite or registry gate
is claimed here.

## Draft retry — 2026-10-17

Rechecked the retained redraft at baseline `9beb00d` after the supplied
attempt-1 diagnostics. Updated only the stale `updated:` date in decisions.md
to 2026-10-17; its human answers and recorded rulings are byte-for-byte
unchanged. Spec, design and ADR 0020 retain the incorporated S-21–S-30 rulings
and Q-11 answer. No criterion, class, appetite or ADR claim changes for a gate.

Artifact checks passed on 2026-10-17:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_interview_minimums.py --change research-swarm
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_criterion_ledger.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_frontmatter_current.py
git diff --check
```

Read-only structural checks confirmed 42 criterion/refutation/basis triples,
all 30 phase-2a statuses `in spec` with original finding text preserved,
unchanged human answers and open phase-6 F-1, the sole new ADR 0020 relative
to local origin/main, required metadata/design sections, the opening card,
one ledger, empty Time used and valid local links.

The supplied full-run result remains red on 46 swarm tests. Reading
tests/test_stage2_swarm.py::sworld and scripts/stage2.py::require_pi confirms
the fixture provides a PATH stand-in while the version check invokes the
absolute PI_WRAPPER. Build steps 1–2 already own that code/test repair;
drafting cannot perform it. This retry ran no runtime tests, full verifier,
tracker-backed registry check, provider query or model call. The artifact
validator is absent. The runner owns registry generation, full verification
and the commit; no git mutation or new handover file occurs in this bounded
draft call.

## Draft attempt 3 — 2026-10-17

Third attempt of this round (route glm), after two failed Codex post-run
checks. The retained redraft was reviewed against the recorded S-21–S-30
rulings, the Q-11 answer and the phase-2/2b/3 prompts, and kept: no
criterion, class, appetite, ADR claim, neighbour or human answer changes.
The ledger was re-verified statically: all seventeen named tests are defined
(`test_stage2_swarm.py`, `test_stage2_research_tools.py`, `test_stage2.py`),
every `not yet written` function is undefined under `tests/`, and the two
new test files (`tests/test_research_handoff.py`,
`tests/test_stage2_research_catalog.py`) do not yet exist. The stale
`updated:` stamp in `decisions.md` was set to 2026-10-17, the one line the
frontmatter gate measures; the recorded answers are byte-for-byte unchanged.

The supplied full-run result remains red on 46 swarm tests. The cause sits
in the committed code/test seam, outside this change folder:
`scripts/stage2.py::require_pi` (from line 1013) launches the absolute
`tools/pi/pi` wrapper (line 1027), whose shell needs `dirname`, `sed` and
`node`, while
`tests/test_stage2_swarm.py::sworld` narrows `PATH` to its stand-ins and
git — so the version check refuses and every swarm test that reaches it
fails. Build step 1 of this plan owns that repair (inject
`stage2.PI_WRAPPER` as a stand-in, as `tests/test_stage2.py::world` does);
drafting cannot perform it. This attempt ran no tests, no tracker access,
no model call and no git mutation; the runner owns `make verify` and the
checkpoint commit.

## Draft handoff — 2026-10-16, after phase 2a (historical)

Baseline e1b54de, branch explore/research-swarm. Apply all 20 phase-2a rulings
from decisions.md into spec, design and this plan; findings statuses name their
spec locations. ADR 0020 remains the sole new ADR relative to local origin/main,
with no maintainer approval added. Existing answers, class, 42 criterion
numbers and appetite remain; criterion wording now incorporates the recorded
rulings rather than being weakened for a gate. No v2 reports are fabricated.

The real-Pi tool-support metadata mapping remains an implementation
qualification gap: type/input are read, a dedicated typed support flag is
absent. No external catalog, live model or capture was run. Phase-6 F-1 remains
open for attended offline isolation capture. Hosted PR state and current
parallel-session ownership were not read under this call's worktree-only
boundary. No tracker access, commit or git mutation occurs here; the runner
owns registry regeneration, full make verify and the checkpoint commit.

Resume by implementing the amended graph and boundary fixtures, including
the already identified pinned-wrapper mismatch in steps 1–2, within the
existing appetite; schedule the attended offline capture before merge.
Artifact-only validation on 2026-10-16 at e1b54de: the commands
`.venv/bin/python scripts/check_interview_minimums.py --change research-swarm`,
`.venv/bin/python scripts/check_criterion_ledger.py` and `git diff --check`
passed. Structural checks passed for 42 numbered criteria with refutations
and bases, all 20 phase-2a rows incorporated, required metadata/design
sections, opening card, one ledger, local links, empty Time used, unchanged
human answers/class/appetite, allowed paths and sole new ADR 0020 relative
to local origin/main. These results validate artifacts, not amended runtime
behavior. The named validate_change_artefacts.py is absent. No full suite,
registry/tracker read, offline capture, provider query or live model call
was run; full verification and checkpointing remain the runner's work.

## Draft retry — 2026-10-16

Rechecked the retained artifacts against HEAD `e1b54de` and the supplied
failed-run diagnostics. The spec now spells its existing interview bases as
`decisions.md#Q-<id>`; no criterion, answer, class or appetite changes.
All 20 phase-2a statuses remain `in spec`; the original finding text and the
open phase-6 isolation-capture blocker remain unchanged.

Artifact checks passed in this retry:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_interview_minimums.py --change research-swarm
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_criterion_ledger.py
git diff --check
```

The supplied full-verification failure is still unresolved: the swarm unit
fixture supplies a PATH-based Pi stand-in, but `require_pi` launches the
absolute `stage2.PI_WRAPPER`. Steps 1–2 already require explicit injection
and pinned launches. That code/test repair is outside this drafting call;
no test bypass or green full-suite verdict is claimed. The runner reruns
full verification. No provider call, tracker access or git mutation was made.

## Draft attempt 3 — 2026-10-16

Third attempt of this round (route glm), after two failed Codex runs. The
retained artifacts were reviewed against the recorded S-1–S-20 rulings and
kept; one wording choice is recorded in the spec's Open decisions. The
ledger was re-verified statically: all seventeen named tests are defined,
every `not yet written` function is undefined under `tests/`, and the two
new test files do not yet exist. No criterion, answer, class, appetite,
ADR claim or file list changed. The 46 red swarm tests remain the known
`PI_WRAPPER`/PATH seam fault that build step 1 repairs; this drafting scope
cannot touch tests. The runner owns `make verify` and the checkpoint commit.
Evidence: research.md, "Incorporation-round attempt 3 evidence — 2026-10-16".

## Earlier implementation time

Historical phase-4 entries are retained below; this redraft adds no phase-4
time and does not reset the 12-hour stop. The unmeasured span prevents a
claim about the exact remaining appetite; establish it before resuming.
Before any phase-4 work, read the attempt-3 runner audit start/end; if absent,
try that attempt’s commit timestamps. Append the bounded span and exact source
as a new historical line; retain the unmeasured entry below as history. Sum
all established historical spans and every later Time used span; do not count
phases 2/3 or time between sessions. If no record bounds attempt 3, stop at once
using prompts/04-implement.md’s expected/found/relevant/proposal block with
found: time used not measurable. Build no code/tests while it waits; only a
maintainer continue with a new total permits more phase 4. The known entries
below are about 78 minutes in total (recorded 2026-10-16, plan at 42e5975),
not evidence that the unmeasured span was zero.

2026-10-15 repair attempt 3, span not measured: this session had no command tool to read `date`.
2026-10-15 completion (Opus 5.5): 05:15–05:31 CEST, about 16 minutes including one `make verify` run (05:20:38–05:30:25, green: 2038 passed, 16 skipped).

2026-10-15 05:49:28–06:00:30 CEST, 11 minutes 2 seconds (Codex repair of L1-1–L1-8; no break).

2026-10-15 09:40–10:31 CEST, about 51 minutes (Opus 5.5 sub-agent repair of phase-6 F-2 to F-10 outside `stage2.py repair`, maintainer-approved; four `make verify` runs of about 8–10 minutes each, the first red on formatting and a stale `updated:`; no break).

The earlier plan cited `docs/journal/handover/2026-10-15-research-swarm-loop-one-repair.md`; that file is not present in this worktree and was not read by this redraft.

## Time used
