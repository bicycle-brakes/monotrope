---
title: "Plan — research-swarm"
status: draft
implementation_status: partial
date: 2026-10-14
last_reviewed: 2026-10-18
updated: 2026-10-19
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, stage-2, research, swarm]
---

# Plan — research-swarm

```text
For you:     Larger changes get mapped sources, three repository and three online views per topic from per-seat preferred models with the cheapest admitted Go model as live substitute, checked before each run and shown to you first, live-selected Go free online views, traceable questions and spec criteria, and finished research kept when a run stops early.
Done when:   Reported seat selection, fresh Go-only free selection, durable resumable slot results, topic coverage, offline isolation capture and research-to-interview-to-spec checks hold, and make verify is green.
Appetite:    17 hours 20 minutes of phase 4 in total (maintainer, 2026-10-18), including earlier implementation and repairs; stop at the limit.
Not now:     Zen or OpenCode CLI models, model-specific perspectives, the implementation-review swarm or sibling checkouts.
Pre-mortem:  suppose it failed: most likely because an online context inherited private repository information.
Starts unless you say stop.
```

## Files

Paths are relative to the repository; existing earlier-slice files are amended,
not recreated. No file is deleted. Only the ADR is new under `docs/adr/`.

| File | Change |
|---|---|
| `scripts/stage2.py` | Preserve early-class/fallback routing; expose checked, cancellable read-only launches for Pi and official Claude; add the `prepare-explore` verb and `explore --availability-reported`, both refused where no swarm runs. |
| `scripts/stage2_availability.py` | One implementation for both swarms (spec criterion 50): shared rule validation, timed exclusion, tool-free probe and receipt seal/verify; research entry points for seat admission, lazy probes, the double-fill rule, the report and the bound single-use receipt. With #157 merged, an extraction that leaves review behaviour unchanged; otherwise created to #157's contract at `0c03ec0`. |
| `scripts/stage2_research_store.py` (new) | Runner-owned state store outside the repository: atomic, flushed launch and result records, owner-only modes, per-change lock, resume binding without HEAD, exact-match reuse, refused-run and complete-run rules; no model call. |
| `scripts/stage2_research_run.py` (new) | The phase-1 run `stage2_swarm.run` delegates to: lock, frozen inputs and resume lookup, finder trio, Opus map merge, public sentence, history, `33 + 3N` topic slots and the judge, each stage one dispatcher call with the store hooks; one buffered append at the end; no probe, refresh, retry or seat swap. |
| `scripts/stage2_swarm.py` | Replace six pairs/Zen discovery with finder, fresh Go selection, provider queues, `33 + 3N` topic slots, typed reports, scores, handoff and frozen-state validation; catalog selection classifies preferred and pool Go models instead of failing on fixed ids, the slot plan comes from the consumed selection, and the run looks up, reuses and marks stored results. |
| `scripts/stage2_research_catalog.mjs` (new) | Use pinned Pi to force a bounded Go-only refresh and return a dated fresh snapshot cross-checked against credential-free models.dev tool_call/status metadata, with explicit capability-unavailable fallback. |
| `scripts/stage2_research_map.py` (new) | Validate the exact finder/merge union, explicit unread provenance, frozen references and given/suggested/self/no-spec neighbour derivation; no model dispatch or file access. |
| `scripts/stage2_research_refs.py` (new) | Pure frozen-byte structural Markdown/Python and canonical YAML/JSON reference resolution, shared per-claim excerpt cap; later map/report integration consumes it. |
| `scripts/stage2_research_history.py` (new) | Local-only frozen-HEAD history packet with ten commits per mapped path, bounded Unicode bodies, explicit unread history and a shared caller deadline; no model dispatch. |
| `scripts/stage2_research_snapshot.py` (new) | Transient copies outside the repository, full working-byte and untracked-change digests, exact runner-owned append exceptions, named drift and context-managed cleanup. |
| `scripts/stage2_research_report.py` (new) | Pure closed report schema, endpoint/model-qualified namespaces, local/history/own-page evidence, all-or-nothing support and per-claim Unicode cap; no judge or dispatch. |
| `scripts/stage2_research_judge.py` (new) | Fixed documented-capacity packet bound, all-outcome preservation, security/required-failure precedence and independently derived exclusive claim-score counts; no dispatch. |
| `scripts/stage2_research_tools.mjs` | Retain public-only tools and receipts; verify cancellation and isolated concurrent receipt paths. |
| `scripts/check_research_handoff.py` (new) | Check v2 decision coverage, answered human links, neighbours and criterion bases; exit 0/1/3. |
| `model-endpoints.yaml` | Replace Zen endpoint/roles with six preferred seat models (no fallback lists, Q-14), the research `availability_preflight` rule with `measured_wire_apis` and dynamic Go-only `online_free` policy/include/exclude. A `modelle_terms` record alone admits a research model, so the review ladder never changes. |
| `prompts/01-explore.md` | State finder, topics, identical perspectives, evidence boundaries, class routing, the required research neighbours list (explicit [] allowed), prepare → report in the main conversation → explore with the id, and resume after an abort. |
| `prompts/01a-interview.md` | Derive linked questions from decisions/disagreements, record stated neighbour keep/drop/add in research_neighbours beside item/claim links, and explain that minimums are no ceiling. |
| `prompts/02-spec.md` | Require runner-derived neighbour parity and answered research_neighbours keep/drop/add fields, with claim/answer basis for criteria from v2 research. |
| `prompts/research-swarm/finder.md` (new) | Four locator lists, same input for the trio, no design judgement. |
| `prompts/research-swarm/finder-merge.md` (new) | Tool-free Opus returns the exact finder-key union with every source/reason; runner resolves refs and inserts given neighbours. |
| `prompts/research-swarm/public-topic.md` (new) | Opus writes only the mechanically filtered public sentence. |
| `prompts/research-swarm/public.md` | Topics 9–11 and source priorities, fixed report contract, no private context. |
| `prompts/research-swarm/repository.md` | Topics 1–8, their exact questions/boundaries, same perspectives and template. |
| `prompts/research-swarm/report.md` (new) | Common structured template: local claim/question ids and links, evidence floor with empty-neighbour topic-5 exception, topic-3 class assessment, exact topic-5 relations and topic-6 volatile/governance fields. |
| `prompts/research-swarm/judge.md` | All topics, source checks, per-model scoring and complete interview inventory; runner alone derives neighbour status, and the judge cannot change it. |
| `templates/spec.md` | Document optional given/confirmed `neighbours:` and v2 criterion-basis form. |
| `AGENTS.md` | Replace obsolete free/six-pair and fixed-trio routing, name the preparation step and add the handoff rule within the existing size limit. |
| `docs/WORKFLOW.md` | Align phase 1/1a/2, required research neighbours list (explicit [] allowed), seat preparation and its report, resume after an abort, provider concurrency, public boundary and handoff-gate scope; the existing kit manifest carries these phase-1 instructions. |
| `decisions/gates.yaml` | Register `research-handoff`, blocking, both placements, no tracker/history dependency, floor false. |
| `.github/workflows/ci.yml` | Regenerate from the one gate list; never edit its commands by hand. |
| `scripts/kit/manifest.yaml` | Carry the new checker and its tests as mechanism; existing prompt-prefix coverage stays. |
| `scripts/kit/probe.py` | Update affected model-resolution case ids only if needed, retaining exception reasons/count/cap. |
| `tests/test_stage2_swarm.py` | Inject the pinned-wrapper stand-in explicitly, trap bare-Pi escapes, replace obsolete free/pair expectations and add finder/trio/same-brief/report/queue/failure mutations. |
| `tests/test_stage2_research_map.py` (new) | Standalone finder union, missing/unread categories, provenance corruption, exact neighbour forms and frozen artifact-to-spec counterexamples. |
| `tests/test_stage2_research_history.py` (new) | Disposable Git fixtures for frozen identity, path/body limits, shallow history, replacements, missing local objects and shared-deadline failures. |
| `tests/test_stage2_research_snapshot.py` (new) | Disposable Git fixtures for current tracked bytes, non-ignored untracked change inputs, exact append ownership, changed path/HEAD detection, unsafe inputs and cleanup. |
| `tests/test_stage2_research_report.py` (new) | Structured report/evidence, malformed JSON/Unicode, no-fabricated-answer, namespace, topic-specific field and common-template contracts. |
| `tests/test_stage2_research_judge.py` (new) | Exact J/J+1 Unicode packet boundaries, preserved evidence/outcomes, claim coverage and exclusive per-seat score regressions. |
| `scripts/stage2_research_dispatch.py` (new) | Standalone cancellable dispatcher: provider-wide queues of four, required-first order, serialized gate/audit at dispatch, deadline reserve, security cancel and reap; no model knowledge or writes; not yet wired into `stage2_swarm.run`. Q-13 adds one `on_terminal` callback before a worker's next launch; a raising callback stops the stage with exit 1. |
| `tests/test_stage2_research_dispatch.py` (new) | Real short-lived child processes prove the four-permit cap across roles, ordering, gate-once, stop/deadline recheck, cancel/reap with partial output, exit precedence and one outcome per slot; plus callback order and the failed-write stop. |
| `tests/test_stage2_research_availability.py` (new) | Seat admission, lazy unique probes, double-fill, probe content and limits, report, receipt binding/age/single use, seat-unavailable exit 1, declaration refusals and use of the shared helpers. |
| `tests/test_stage2_research_store.py` (new) | SIGKILL durability, torn/temporary records, owner-only placement, binding and slot-key matching, refused and complete runs, lock release after a killed run and scrubbing. |
| `docs/research/2026-10-18-research-judge-capacity.md` (new) | Dated primary capacity/CLI documentation, explicit reserve/conversion estimates and qualification limits. |
| `tests/test_stage2_research_refs.py` (new) and `tests/fixtures/research_refs/plan-prompt-d862bc2.md` (new) | Structural-reference counterexamples and the verbatim historical prompt used by ruling S-47; no Git history or live-file lookup in the resolver. |
| `tests/test_stage2_research_catalog.py` (new) | Offline real-pinned-Pi catalog fixtures: forced refresh, provider filtering, shipped-cache contamination, malformed/empty/error outcomes, models.dev intersection/deprecation/failure, and both sources’ audit; the two fixed-id hard-failure tests become per-candidate outcome tests. |
| `tests/test_stage2_research_tools.py` | Keep real tool-call shape, destination/receipt faults and concurrent scratch separation checks. |
| `tests/test_stage2.py` | Retain small-class, Haiku 5.5, other-verb and exact-check regression coverage; refuse a receipt id and `prepare-explore` where no swarm runs. |
| `tests/test_model_endpoints.py` | Resolve preferred seat models and dynamic public-only Go free permission; validate selection policy and the availability rule; remove Zen free-billing expectations. |
| `tests/test_research_handoff.py` (new) | Fixture-based gate tests, including lost-decision mutation, archive, neighbour/basis and unmeasured cases. |
| `tests/test_ci.py` | Verify new gate registration and generated-CI coverage without weakening existing ratchets. |
| `scripts/ci_gates.py` | Document non-CLI research helper consumers (now including the state store) while scheduler integration is pending; retain direct test-import coverage and the existing test-exemption floor. |
| `tests/test_kit.py` | Prove the checker and tests travel without corpus or missing imports. |
| `plans/changes/research-swarm/spec.md` | Hold the amended contract and neighbour/basis references. |
| `plans/changes/research-swarm/design.md` | Keep the shaped boundaries consistent with the implementation. |
| `plans/changes/research-swarm/plan.md` | Convert pending ledger rows when tests land and append measured phase-4 time. |
| `plans/changes/research-swarm/research.md` | Preserve past reports; append redraft facts, capture evidence and later live qualification. |
| `plans/changes/research-swarm/decisions.md` | Preserve all human answers; append only actual later answers or reasoned detail records. |
| `plans/changes/research-swarm/findings.md` | Preserve existing reviews and the open offline-capture blocker; record later review dispositions. |
| `docs/adr/0020-phase-1-research-swarm.md` (new) | Propose this complete amended subsystem in the decision PR, including Q-12 seats and Q-13 resume. |
| `plans/INDEX.md` | Runner regenerates after artifact changes. |

## Build sequence

0. Before phase-4 code or tests, read the maintainer's answered appetite
   stop under Time used: continue with 17 hours 20 minutes in total
   (raised from 13 hours 20 minutes on 2026-10-18, Q-14).
   Preserve the named unmeasured historical span without counting it;
   sum measured historical and later Time used spans, adding each new span.
   Do not re-ask that settled stop or reset earlier time. A new unbounded
   span raises the appetite stop. Drafting phases 2/3 do not count.
   Next order (2026-10-18): steps 11 (Q-12) and 12 (Q-13) come before the
   dispatcher and catalog are wired into the run in steps 2–5 and 7–8,
   because that wiring consumes the frozen selection and the state store.
   Steps 1–10 keep their numbers because spec and rulings cite them.
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
2. Read role identities from the run's frozen seat selection (step 11) and
   the declaration: Go Pi for `opencode-go` candidates, official read-only
   Claude Code for `claude-code-plan` candidates and Opus. Validate
   purpose/data-class per invocation, not endpoint capability alone; retain
   default framework residency checks.
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
   ids; never infer support from Pi compat flags. Classify every Go seat
   candidate against the fresh overlay (Q-12): an absent, baseline-only,
   non-chat or malformed typed entry is skipped with its reason and raw value
   and never probed; step 11 stops a seat left without a candidate. Do not
   let models.dev decide a preferred model or a Claude Code one; pool models
   need it (Q-14).
   For models.dev, request failure/timeout, non-200, non-JSON/non-object root,
   absent/non-object opencode-go or models, and duplicate claimed model ids
   are document-level capability-unavailable: exclude all free candidates,
   retaining 39 required slots with N=0 distinct from measured eligible-empty.
   Otherwise exclude only the affected candidate: missing entry is
   metadata-missing; non-object entry, present non-boolean tool_call,
   non-string status or id/key mismatch is metadata-malformed with raw value.
   Absent/false tool_call is no-tool-support; deprecated is deprecated.
   Keep not-chat/baseline-only reasons; ignore other providers' entries.
   An explicit include is still required and exits 1 if ineligible. Start both
   reads together at catalog preflight, now part of preparation (step 11);
   abort unfinished requests at its shared
   60-second deadline. Unfinished Pi exits 1 whatever models.dev did. Successful
   Pi with unfinished models.dev records capability-unavailable/timeout, N=0
   and keeps required slots unless an explicit include is unmet. Neither read
   retries or extends the deadline; models.dev has no Go key or private data.
   Validate Go origin, provider and identities before selection. Record version,
   both sources’ retrieval time/digest/outcome, exact tool_call/status evidence,
   eligible/policy/selected/excluded ids and reasons; freeze `N` and slots.
   Pi refresh failure/timeout/stale-only/malformed/ambiguous data exits exactly
   1 before models, never 0/2/3 or Flash-only/Zen fallback. The absence of a Pi
   tool-support field is expected under Q-11, not a Pi refresh failure.
   Distinguish Pi document faults from candidate faults: failed/timed-out
   refresh, Pi-rejected response, unparseable body or repeated overlay id
   (raw repeated key or one id under two entries) exits 1 before any model.
   Otherwise malformed typed input/type excludes just that -free entry as
   pi-malformed, recording raw value; a malformed preferred or pool Go model is
   skipped the same way. Other entries are inspected only
   for repeated ids. Do not merge duplicate catalog entries during selection.
   Fixture cat-jam-free with input: "text": exclude it as pi-malformed,
   retain valid peers and all 39 required slots. Repeated longcat-2.5-preview-free
   entries start no model and exit 1. A preferred qwen3.8-flash with a
   string input is skipped as pi-malformed with its raw value. A Pi runtime
   rejection remains document-level even when triggered by one entry (S-50).
   Valid empty selection records `N=0` and retains 39 required calls.
   Test with a local catalog server and actual pinned Pi refresh implementation;
   force a request despite a fresh cache and reject removed shipped free ids.
   Fixtures join Pi and models.dev by exact provider/id, covering true/false/
   absent tool_call, missing entry/provider, deprecated and non-deprecated
   status, models.dev-only ids, malformed/unreachable metadata and explicit
   includes during capability-unavailable fallback. Failure fixtures assert
   the required-slot graph as well as the exact exit, not just selection output.
   Add every document-level/per-candidate shape above, including string/null/
   numeric tool_call and a malformed unrelated provider. The object key is
   identity: exact Pi id lookup, required present/equal id field. Parse with
   duplicate-key reporting: repeated raw keys under opencode-go.models or
   equal id fields under different keys exclude every free candidate as
   capability-unavailable/duplicate-id. Missing id is metadata-malformed with
   an absent-value marker, and must not exclude a valid peer. Fixture raw
   duplicate JSON before parsing, a-free/b-free both claiming a-free, and
   x-free without id alongside valid y-free. X with tool_call
   "true" must be excluded while Y with true is selected. A missing or
   baseline-only Qwen candidate is never probed. A fake monotonic clock checks
   Pi at 5 seconds/models.dev never answers (39 required slots after abort at
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
   Eligible spec paths have exactly three forms:
   plans/changes/<name>/spec.md (one segment other than archive),
   plans/changes/archive/<YYYY-MM-DD-name>/spec.md, and
   plans/specs/<capability>/spec.md. Given paths must also be unique,
   repository-relative and present in frozen bytes; this change's own spec,
   templates/spec.md and all other forms refuse with exit 2 before models.
   Resolve neighbour-category artifacts inside any of these folder kinds to
   the folder's frozen spec.md, deduplicated with all map keys retained.
   Own-change entries are self, with no relation or gap; other resolved
   entries outside those forms or without a spec are no-spec with a gap.
   Unresolved entries grant no neighbour status. Derive expected packet
   neighbours independently from fixture map/header, compare with topic 5's
   packet and manifest, and fail even if a wrongly dropped neighbour has a
   gap. Cover active design.md::Data model with/without sibling spec, an
   archived plan and a living spec; all valid spec-backed entries must yield
   packet neighbours and relations, while own-change design.md is self.
   Resolve citations and map entries with one type-specific resolver:
   .md uses one structural scan: skip first-line --- front matter through
   the next ---; fences open with at least three backticks/tildes indented
   at most three spaces and close with the same character at least as long,
   or continue through EOF. ATX headings outside these blocks have at most
   three leading spaces, one to six # marks, then space/tab/end; strip
   opening marks, optional closing # run and outer whitespace, retaining case
   and inline formatting. Setext/HTML forms are unrecognised. Require one
   exact heading and end its excerpt before the next same/higher scanned
   heading or EOF; the same scan decides uniqueness and criterion items.
   criterion <n> selects its numbered item under the one
   ## Acceptance criteria heading until the next item/heading. .py uses AST
   def/async def/class/module-level assignment, dotted nested definitions,
   excerpt the node's lines. .yaml/.yml uses safe duplicate-reporting loading;
   JSON reports duplicate keys and refuses NaN/infinity. Split every path dot
   into exact string mapping keys: literal dotted keys/list indices are
   unsupported, so cite the nearest citable parent. Convert dates/timestamps
   to ISO 8601 text; reject binary, sets, non-finite values and non-string
   keys anywhere in the value. Canonical JSON sorts keys, keeps non-ASCII
   unescaped, uses two-space indentation, comma/colon-space separators and
   no trailing newline before the per-claim cap. Duplicate matching headings,
   criterion items, definitions or keys are
   unsupported; parse failures do not fall back to word search. Other files
   use a whole-word match, from first matching line to EOF before the common
   4,000-character per-claim cap. Replace the earlier symbol_problem substring
   check. Fixtures reject prose-only Markdown/Python and duplicate targets;
   verify nested methods, assignments, formatted headings, criterion extents,
   YAML/JSON key/value excerpts, shell/Makefile/JS/TOML first-word excerpts
   and frozen rather than live resolution. Add S-47 fixtures: at baseline
   d862bc2, prompts/03-plan.md::The criterion ledger yields lines 65–94,
   while ::Criterion ledger is unsupported; real ## X plus fenced ## X
   resolves only the real heading; fenced-only ## Acceptance criteria cannot
   supply criterion 1; a front-matter # comment is not a heading. Add S-48
   fixtures: research_swarm.free_focuses.longcat-2.5-preview-free cannot
   address that literal dotted key but its free_focuses parent resolves;
   decisions/adoption.yaml::adopted.interview-minimums yields the JSON
   string "2026-10-08"; a.0 on a list and duplicate YAML keys are unsupported;
   JSON produces byte-exact canonical text. Retain the baseline mapping in
   a fixture because implementation replaces free_focuses. A swarm research
   header must explicitly
   hold neighbours: [] or a valid list; missing/null/non-list refuses with
   exit 2 and a message naming those repairs. Test missing versus empty list:
   no call versus normal finder dispatch. Without --stage2-off retain class
   checks for bounded/spike too. Explicit --stage2-off skips class derivation
   and all class/neighbour header checks, making one Haiku 5.5 call and
   recording route/model/reason. Beside it, --class exits 2 before any call
   with a message that class has no effect on this route. Fixture a bead-only
   research header with no class/neighbours, plus invalid/conflicting class
   and neighbour headers: fallback still runs. --class bounded beside
   --stage2-off "quota" with feature in the header must refuse (S-52).
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
   researcher/map merge, 15-minute judge, 150-minute run after preparation
   (catalog and probes, step 11). All Go roles share four permits; no silent roster cap,
   retries, debate or delegation. Reserve the judge's 15 minutes. Order queued
   required slots before any free seat: repository topics 1–8 then online
   seats 9–11, topic then declared seat order; free slots follow by topic then
   sorted id. Launch only with positive time before the reserve; use the
   lesser role/remainder allowance and recheck after leak scanning. Unlaunched
   slots are not-started-deadline: incomplete only if required. Large free
   rosters cannot spend the reserve or silently lose outcomes.
5. Build identical task bodies for every seat of a topic (repository seats
   or online seats plus all selected Go free models), with all three common
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
   (currently Pi 1.2.0), include online-seat and dynamically selected Go free
   transport envelopes, one reachability probe, plus catalog metadata isolation. A stand-in's argv alone does not satisfy this step.
7. Validate topic reports before judge: C1–C7 and Q1… ids unique within
   each report, questions with classification and nonempty local claims list,
   confidence basis/counter-evidence/not-read/neighbour fields, topic-3
   class_assessment {class, claims}, topic-5 neighbour_relations (exactly one
   path/relation/nonempty local claims list per packet neighbour; reject
   missing/extra/duplicate paths or bad links), topic-6 volatile and governance
   central|runtime|dated when true. Template violations fail the slot; bad
   citations make the whole claim unsupported without dropping it: all its
   citations must resolve locally or have successful online page receipts
   before any excerpt, disposition or criterion Basis is allowed. Fixture a
   claim with scripts/stage2.py::explore and ::no_such_symbol: unsupported,
   no excerpt; as the only claim it fails the evidence floor, while another
   valid claim lets the report pass. One receipted plus one unreceipted URL
   also makes the entire online claim unsupported. Only valid claims join
   all resolved sources in citation order for excerpts (S-49). Require one
   evidence-backed claim per report (one successful page-backed claim online),
   not success for every fetch. Only when topic 5 has no packet neighbour,
   still run its three required seats with identical "no packet neighbour"
   packets; require neighbour_relations: [] and a not-read entry naming the
   empty packet, but waive the claim floor. Any claims still get checked and
   scored; any relation is an extra path and fails. With a neighbour, the floor
   stays. Fixtures cover complete 39-slot empty-neighbour runs, empty packets
   with extra relations/missing not-read, and nonempty packets without valid
   evidence. Record "no neighbour given or found" in the comparison gap. Runner namespaces claims/questions as
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
   39 required slots required and free slots best-effort, each with one terminal
   outcome. Compare HEAD and full frozen digest before publication, excluding
   only runner-owned research appends/updated restamp. Other drift names
   changed paths and exits incomplete 1, preserving reports/excerpts/digests
   while deleting scratch frozen copies after publication or abort.
   Derive obligations from every accepted raw DECISION question (even scored
   off-brief/refuted), unresolved judge disagreements, runner-detected class
   mismatches, and topic-5 neighbour_relations: every contradicts and every
   unrelated given path derives an item even without a DECISION question or
   judge mention. For each suggested neighbour, runner alone derives status
   from runner-valid evidence: a relation counts only when at least one
   listed claim is valid; three counting related/contradicts means confirmed,
   three counting unrelated means rejected, otherwise split, including fewer
   than three counting relations. Every contradicts and unrelated-given
   relation retains its human item even with only unsupported claims; judge
   dispositions never affect this calculation (S-51). Contradicts
   still derives its own item; every split derives a neighbour DECISION item
   with kind split, path and source claims, regardless of judge prose. Given
   remains given. The judge may add obligations but cannot set/change status
   or remove items. Group duplicates into H-<n> but preserve all global
   question/claim sources.
9. Implement check_research_handoff.py [--root DIR] [--change NAME] over live
   and archive folders with no tracker/network/model dependency. Parse all v2
   records; malformed/unreadable evidence or ambiguous ids/links exit 3.
   Only complete runs support interview/spec and carry obligations, including
   earlier complete runs after reruns; incomplete claims cannot support bases.
   Check coverage independently of judge inventory, then Q-record headers
   research_items/research_claims and research_neighbours, actual answer,
   maintainer and context. One
   Q-record can answer items from multiple runs. Item links are <run>/H-<n>,
   claim links are global ids and criterion Q bases are decisions.md#Q-<id>; explicit human rejection
   counts, no agent waiver does. Valid pending items before spec.md exists
   are listed with exit 0; once it exists missing answers or v2 runs with none
   complete exit 1. Legacy without v2 is an explicit exemption. With a spec,
   resolve each Basis to supported complete-run claims or maintainer-answered
   decisions.md Q-records. Every direct claim must be supported; a mixed Basis
   still exits 1 if any named claim is unsupported/refuted/off-brief/unresolved.
   Those claims need an answered Q-record basis, optionally linked through
   research_claims. Recompute each suggested status from the three raw
   topic-5 relation fields and runner validity marks, never judge dispositions:
   only relations with a valid listed claim count; fewer than three means
   split, without filtering contradicts/unrelated-given human items. Enforce exact parity:
   (union of confirmed/given paths from every complete run + keep + add) - drop,
   taking keep/add/drop only from maintainer-answered Q-records'
   research_neighbours. The recording session writes up to three path lists
   from the stated answer; the checker never infers intent from answer prose.
   A neighbour item (contradiction, unrelated given, split or cross-run
   conflict) closes only when research_items links it AND keep/drop names
   its path. A linked answered record with neither leaves it open (exit 1).
   Add needs no item link, allowing drafting discoveries without fabricated
   research items. Every directive path must have one of the three permitted
   forms (invalid form exits 1); do not require current existence, so archival
   cannot invalidate historical decisions. A path in two lists of one record,
   or incompatible inclusion/drop directives across answered records, exits 3.
   A split is not required and may not enter the header until human keep;
   unanswered split items fail with or without the path once a spec exists.
   Derive a neighbour DECISION item independently of the judge for cross-run
   confirmation/rejection conflicts and later omission of an earlier given
   path. Bind path, both complete run ids, source manifests and available
   claims. Until an item-linked maintainer answer names it in
   research_neighbours.drop the path stays required;
   open items fail even with the path present. Fixtures run confirmation then
   rejection with/without the header: both fail unanswered, keep passes only
   with the path, drop only without it. Also test given-header removal across
   runs and confirmed-path drops. Arbitrary
   drafting additions, even never suggested, exit 1 unless structured as a
   human add or confirmed by a new complete run. Fixtures: related/unrelated/
   related plus a judge-confirmed verdict remains split and fails either
   header unanswered; keep passes only with the path, drop only without it.
   Test all-related, all-unrelated, and mixed related/contradicts confirmation
   with its separate contradiction item. Also fixture three related for P
   with one seat citing only an unresolved claim: split plus an open item,
   exit 1 once spec exists until item-linked structured keep/drop. Three
   unrelated with one unsupported-only relation is also split, not rejected;
   an unsupported-only unrelated-given relation still derives its item. The
   fixture seat needs another valid claim so it passes the report floor.
   A judge-supported mark cannot rescue invalid evidence. A linked prose-only "keep P" leaves
   the item open; keep:[P] and drop:[P] enforce opposite headers. An answered
   add:[X] passes without an item link; prose-only addition fails. Keep+drop in
   one record or conflicting answered records exits 3. Invalid path forms
   fail, while a valid formerly existing path does not fail existence after
   archival. Review checks field/answer fidelity, relevance and source intent;
   the gate checks identities and structured directives.
10. Carry the interview/spec instructions, spec template, doctrine, gate and
    kit classification together; derive CI with `ci_gates.py`. Run commands
    below, obtain spec/phase-6 reviews and repair findings within the remaining
    appetite. Keep F-1 open until actual capture passes. The runner owns the
    checkpoint commit/PR. After decision merge only, qualify real Go/Pi models
    and public retrieval; record failures honestly without a fallback model.
11. Seat selection and its reported receipt (Q-12, Q-14; spec criteria 6,
    11, 17, 20, 37, 38, 40, 41, 43–50, 59–61; design «Preparation →
    selection → receipt»). First merge `origin/main` and check whether #157's
    `scripts/stage2_availability.py` is on it; follow the spec's
    «One implementation for both swarms» [DETAIL] either way.
    Red first: write the ledger's not-yet-written tests in
    `tests/test_stage2_research_availability.py`, `tests/test_model_endpoints.py`
    and `tests/test_stage2.py`. Turn the two fixed-id hard-failure tests in
    `tests/test_stage2_research_catalog.py` into the per-candidate tests the
    ledger names. Run them and record the failures before touching source.
    Fixtures:
    - The pinned-wrapper stand-in, scripted per model like the review swarm's
      `world.script(pi=[...])`, plus a Claude Code stand-in and a fake clock
      for receipt age.
    - Fixture catalog: preferred models plus at least four admitted pool
      models with distinct and tied `anfragen_5h` values, one model with a
      terms record but no cost value, one overlay model without a terms
      record, one with `uebersprungen`, one on `anthropic-messages` and one
      that models.dev marks `tool_call: false` or deprecated.
    - Selection: an unreachable preferred model gets the cheapest reachable
      pool model, reported as "substitute for <seat>" and named unreachable
      with a scrubbed error. A tie is broken by id. A substitute never takes
      another seat's reachable preferred model, and one model never fills
      two seats of a trio. A model in both trios is probed once. Running the
      same fixture twice gives the same selection.
    - Admission: every model of the fixture catalog's last four kinds, and
      any undeclared, absent, baseline-only, non-chat, malformed or timed-out
      one, is never probed and is reported with its reason. With models.dev
      unavailable the pool is empty and the preferred models still serve.
    - Dynamic pool: adding one `modelle_terms` record to the fixture puts that
      model into the pool at its cost position, with no other edit and an
      unchanged review ladder.
    - Stop: an unreachable preferred model with an empty or unreachable pool
      gives exit 1 with `seat-unavailable`. The seat is named, no receipt is
      left (an earlier one is deleted) and no research call starts.
    - Probe content: a canary set (change name, an AGENTS.md line, a path,
      map text, the public topic) never reaches a probe's payload, argv or
      environment. Each probe has `--no-tools` or `--tools ""`, a scratch
      working directory, a 60-second limit, and its own leak check and audit.
    - Receipt: a wrong id, age 901 s, an edited `model-endpoints.yaml`, a
      changed class or neighbours, another root, corrupt JSON or a second use
      each refuse with exit 2 and zero model calls.
    - Declaration faults of criterion 49 each give exit 2, a second model or
      fallback list in a seat included. A receipt id or
      `prepare-explore` beside bounded, spike or `--stage2-off` gives exit 2.
    - Never probed: Go free models and Opus. Probes add no run slots, and
      preparation leaves the worktree bytes unchanged.
    - A spy shows the research path calling the shared helpers.

    Then implement: the per-model outcomes in `select_research_catalog`,
    including `api` against `measured_wire_apis`; the substitute pool built
    from #157's `terms_problem`, `request_value` and `ordered_models`; the
    shared helpers with `prepare_research` and `consume_research`; the
    `prepare-explore` verb and `--availability-reported`; and
    `research_slot_plan` built from the consumed selection. Enter the six
    preferred models and the rule from design.md in `model-endpoints.yaml`.
    Where #157 is merged, run `tests/test_stage2_availability.py` unchanged.
    Estimate (agent's, not measured): 2 h 45 min, including two full `make
    verify` waits of about 15 minutes each; Q-14's pool adds about 30
    minutes to the 2 h 15 min estimated for Q-12 alone.
12. Durable slot results and resume (Q-13; spec criteria 17, 21, 51–58;
    design «Slot results → state store → resume»). Red first: write the
    ledger's not-yet-written tests in `tests/test_stage2_research_store.py`
    and the two new ones in `tests/test_stage2_research_dispatch.py`. Run
    them and record the failures before touching source. Fixtures: a
    temporary `XDG_STATE_HOME`, the disposable Git repository of the
    snapshot tests, and real short-lived children for the dispatcher.
    - SIGKILL: a driver subprocess dispatches two slots with the store hook.
      Its `on_terminal` writes the first record, then prints a marker. The
      test reads the marker from the pipe with a timeout (no sleep loop),
      kills the driver with SIGKILL, and asserts that the first record is
      whole and the second slot has a launch record only, read as
      interrupted.
    - Torn and temporary record files are never read as results.
    - Callback order: a blocking `on_terminal` holds back that worker's next
      launch until it returns. A raising one stops the stage with exit 1 and
      the reason named; with a security refusal the exit is 2.
    - Placement: the store is outside the root, the git directory and the
      model directories, with modes 0700 and 0600. A store-path canary never
      reaches a payload, argv or environment.
    - Binding: equal bytes, a foreign tracked edit, an untracked change-input
      edit, a foreign `research.md` tail, the run's own tail with the
      `updated:` restamp, and HEAD moved by a commit of the own tail.
    - Each slot-key field changed once. Outcomes cancelled, failed,
      timed-out, refused, not-started, interrupted and invalid-report are
      never reused.
    - Runs: a complete run clears the store; a refused run is named and
      never reused.
    - Lock: a second lock attempt refuses with exit 2; a holder killed with
      SIGKILL releases its lock.
    - Credential fragments are scrubbed from every store record.
    - Swarm level: a resumed run launches only missing slots and stays
      within `39 + 3N`. Reused slots carry their source run and original
      times; interrupted slots are listed. Every resumed run has a new run
      id, manifest and receipt.

    Then implement `stage2_research_store.py`, the `on_terminal` callback in
    `dispatch`, the comparison of the snapshot digests with stored ones, and
    the runner's lookup, copy-forward, marking and clear-after-complete.
    Register the store module in `scripts/ci_gates.py`. Estimate (agent's,
    not measured): 2 h, including two full `make verify` waits.

## Appetite fit — 2026-10-18

Measured phase-4 time, summed as step 0 says (retained measured history plus
every Time used span, the unmeasured 2026-10-15 span named but not counted):
historical 1 h 18 min 2 s (16 min, 11 min 2 s and 51 min, the first and last
"about"); since 2026-10-17 3 h 38 min 8 s (38:37, 24:56, 40:51, 19:08, 19:09,
16:45, 24:57, 16:36, 17:09). Total 4 h 56 min 10 s; 8 h 23 min 50 s of the
13 h 20 min appetite remain. Steps 11 and 12 add about 4 h 15 min. That
leaves about 4 h 9 min for the work still open from before: wiring finder,
topics, reports, judge and publication into the run (steps 2–5, 7, 8), the
role prompts, the handoff gate (step 9), doctrine, kit and CI (step 10), the
attended F-1 capture (step 6), and review repairs. By this plan's own
estimate (agent's, not measured), that open work needs about 7 to 8 hours.
**The appetite does not fit**: the expected shortfall is 3 to 4 hours. The
Appetite line stays the maintainer's 13 h 20 min, and this plan does not
widen it. Phase 4 raises the stop when the limit is reached
(`prompts/04-implement.md`), with steps 11 and 12 already done, because they
change the run's interfaces.

2026-10-18, after this section was shown: the maintainer answered "erhöhe
das zeizbudget" (Q-14) and set the total to 17 h 20 min, against the
recommended 17 h 20 min. With the measured 4 h 56 min 10 s above, 12 h 23 min
50 s remain. Q-14 raises step 11 to about 2 h 45 min, so steps 11 and 12
need about 4 h 45 min. That leaves about 7 h 39 min for the older open work
estimated at 7 to 8 hours: it fits at the low end of that estimate and runs
about 20 minutes short at the high end. The stop rule stays as above.

## Verification

The implementing session uses the locked environment (`make venv` once if
needed), records actual time including repairs, then runs:

```sh
source .venv/bin/activate
python3 -m pytest tests/test_stage2_swarm.py tests/test_stage2_research_tools.py tests/test_stage2_research_catalog.py tests/test_pi_contract.py tests/test_stage2.py tests/test_model_endpoints.py tests/test_research_handoff.py tests/test_ci.py tests/test_kit.py -q
python3 -m pytest tests/test_stage2_research_availability.py tests/test_stage2_research_store.py tests/test_stage2_research_dispatch.py tests/test_stage2_research_snapshot.py -q
if [ -f tests/test_stage2_availability.py ]; then python3 -m pytest tests/test_stage2_availability.py -q; fi
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

- 18: tests/test_stage2_research_judge.py::test_judge_packet_one_fixed_unicode_limit_allows_J_and_refuses_J_plus_one — Whole-packet size is measured without instructions, counts bytes instead of Unicode characters or permits J+1; actual launch/barrier integration remains pending.
- 28: tests/test_stage2_research_judge.py::test_judge_packet_retains_all_valid_reports_free_failures_and_full_instructions — A free failure, accepted report, map entry or instruction disappears from the bounded packet.
- 18: tests/test_stage2_research_judge.py::test_judge_packet_required_failure_blocks_even_with_a_valid_partial_report — A required failure permits the prepared judge packet.
- 18: tests/test_stage2_research_judge.py::test_judge_packet_ok_without_report_cannot_look_complete — A reported successful topic has no validated report yet passes preparation.
- 18: tests/test_stage2_research_judge.py::test_judge_empty_or_free_only_outcomes_cannot_allow_a_judge_call — No required topic evidence can look like a permitted packet.
- 12: tests/test_stage2_research_judge.py::test_judge_security_refusal_blocks_even_a_free_seat_and_takes_exit_two_precedence — A free-seat declaration/leak refusal permits the judge or loses security exit 2 to ordinary failure exit 1.
- 28: tests/test_stage2_research_judge.py::test_judge_scores_are_derived_per_topic_and_seat_with_every_claim_once — Counts/ids omit seats or duplicate exclusive claim scores.
- 28: tests/test_stage2_research_judge.py::test_judge_unsupported_claims_are_scored_without_judgement_and_raw_decisions_survive — An unsupported claim receives a judge disposition or its raw human question disappears.
- 28: tests/test_stage2_research_judge.py::test_judge_cannot_lose_double_score_or_promote_a_claim — A valid claim is omitted or double-scored, an unsupported claim is promoted, or unique is not a supported subset.
- 16: tests/test_stage2_research_history.py::test_history_metadata_output_is_utf8_despite_local_display_encoding — A local display-encoding setting breaks valid Unicode history metadata or changes its retained text.
- 10: tests/test_stage2_research_report.py::test_report_online_claim_requires_all_own_successful_page_receipts — A search/error/unfetched source supplies a standalone report's evidence floor; dispatcher/receipt ownership integration remains pending.
- 10: tests/test_stage2_research_report.py::test_report_retains_online_unsupported_claim_without_any_partial_page_excerpt — One failed page citation leaves another excerpt attached to the unsupported claim.
- 16: tests/test_stage2_research_report.py::test_report_bad_citation_invalidates_whole_claim_without_dropping_it — A bad local citation retains a partial excerpt or drops its claim/question.
- 16: tests/test_stage2_research_report.py::test_report_one_shared_unicode_excerpt_cap_in_citation_order — Sources receive separate 4000-character budgets or reordered excerpts.
- 16: tests/test_stage2_research_report.py::test_report_absent_history_and_external_identifiers_are_unsupported — A hash absent from the packet, bare PR/bead id or line-only reference becomes evidence.
- 16: tests/test_stage2_research_report.py::test_report_commit_evidence_is_only_the_topic_six_packet_record — A non-topic-6 hash or a missing packet record supplies evidence.
- 18: tests/test_stage2_research_report.py::test_report_without_any_supported_claim_fails_except_empty_neighbours — A report without valid evidence passes outside the exact empty-neighbour exception.
- 27: tests/test_stage2_research_report.py::test_report_topic_five_relations_cover_exact_neighbour_packet_and_local_claims — A missing/extra/duplicate neighbour relation or dangling claim link is accepted.
- 31: tests/test_stage2_research_report.py::test_report_namespaces_claims_and_questions_without_changing_raw_report — Raw human questions disappear or claim/question ids are not bound to the trusted seat.
- 31: tests/test_stage2_research_report.py::test_report_questions_have_unique_local_links_and_no_answers — A question has missing/duplicate local links, invalid identity/classification or fabricated answer fields.
- 31: tests/test_stage2_research_report.py::test_report_same_local_ids_in_two_endpoint_seats_are_distinct — Different endpoint/model seats collide on local ids.
- 31: tests/test_stage2_research_report.py::test_report_requires_one_endpoint_qualified_seat_identity — A missing or ambiguous endpoint/model identity can produce global claim ids.
- 31: tests/test_stage2_research_report.py::test_report_seat_encoding_distinguishes_reserved_model_and_endpoint_characters — Reserved characters collide or escape the endpoint/model namespace.
- 35: tests/test_stage2_research_report.py::test_report_topic_specific_class_and_volatile_fields_are_required — Topic 3 class assessment or topic 6 volatility fields are missing.
- 35: tests/test_stage2_research_report.py::test_report_true_volatile_claim_requires_one_governance_proposal — A volatile claim lacks the required governance proposal.
- 18: tests/test_stage2_research_report.py::test_report_raw_duplicate_and_nonfinite_json_is_not_a_valid_template — Ambiguous or non-finite raw JSON becomes an accepted report.
- 18: tests/test_stage2_research_report.py::test_report_lone_surrogate_cannot_enter_a_utf8_artifact — Escaped JSON or object text persists an unrepresentable Unicode value.
- 18: tests/test_stage2_research_report.py::test_report_documented_base_object_matches_the_validated_contract — The common prompt's example and the report validator disagree.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_keeps_uncommitted_tracked_and_nonignored_change_bytes — Standalone freezing omits current tracked/change inputs, includes ignored/unrelated untracked inputs or persists snapshots in its manifest; dispatcher integration remains pending.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_copies_stay_frozen_and_are_deleted_on_exit — Local citation sources follow live edits or transient copies survive publication cleanup.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_copies_are_deleted_on_consumer_abort — Transient copies survive a failed consumer context.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_digest_binds_working_bytes_and_manifest_does_not_alias — Working bytes change without changing the full digest or a caller can mutate the internal digest record.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_detects_untracked_change_input_set_and_byte_drift — Added, removed or changed untracked change inputs are invisible to the publication check.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_detects_new_tracked_paths_and_changed_head — A changed HEAD or newly tracked file leaves the frozen state valid.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_does_not_treat_any_research_append_as_runner_owned — Foreign appended bytes disappear under a prefix-only publication exception.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_runner_restamp_may_not_rewrite_frozen_research_body — A caller-owned restamp/append rewrites the frozen research body.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_missing_tracked_file_refuses_and_cleans_preparation — Missing tracked bytes silently vanish from a successful snapshot or partial copies survive failure.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_never_follows_file_or_parent_symlink — A file or parent-directory symlink reads ambient input outside the frozen repository boundary.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_refuses_copies_inside_repository — Whole-source copies can be persisted inside the repository.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_mid_freeze_change_refuses_and_cleans_copies — Mid-preparation input changes leave a usable snapshot or partial copies behind.
- 16: tests/test_stage2_research_snapshot.py::test_snapshot_interrupt_during_preparation_deletes_copies — An interrupted preparation leaves transient source copies behind.
- 16: tests/test_stage2_research_history.py::test_history_uses_frozen_head_and_never_current_working_bytes — A standalone history packet includes commits after frozen HEAD or uncommitted bytes; topic integration remains pending.
- 16: tests/test_stage2_research_history.py::test_history_ten_per_path_and_shared_commits_preserve_all_mapped_touches — More than ten commits per path are retained, shared records duplicate or mapped touches disappear.
- 16: tests/test_stage2_research_history.py::test_history_author_date_is_utc_and_body_cap_counts_unicode — Author dates retain a non-UTC offset or the body exceeds 4000 Unicode characters without a truncation flag.
- 16: tests/test_stage2_research_history.py::test_history_pathspec_magic_is_a_literal_filename — A mapped filename is interpreted as a Git pathspec expression.
- 16: tests/test_stage2_research_history.py::test_history_untracked_mapped_file_has_measured_empty_history — A complete local read with no committed path history loses its measured-empty distinction.
- 16: tests/test_stage2_research_history.py::test_history_shallow_boundary_is_not_complete_or_measured_empty — A shallow boundary is reported as complete or as proven empty history.
- 16: tests/test_stage2_research_history.py::test_history_replace_objects_cannot_change_frozen_commit_evidence — A local replacement object changes evidence associated with a frozen commit identity.
- 16: tests/test_stage2_research_history.py::test_history_all_commands_are_local_and_ignore_ambient_repository_overrides — History inherits a different Git repository, ambient credentials or fetch/config overrides.
- 16: tests/test_stage2_research_history.py::test_history_missing_objects_cannot_invoke_a_promisor_remote — An absent frozen object invokes a configured transport instead of failing locally.
- 16: tests/test_stage2_research_history.py::test_history_rechecks_shared_deadline_before_every_command — Later commands receive fresh time instead of stopping at the caller's deadline.
- 16: tests/test_stage2_research_history.py::test_history_timeout_is_one_failure_without_retry — A history command timeout is retried or treated as empty successful evidence.
- 16: tests/test_stage2_research_history.py::test_history_deadline_must_be_a_finite_number_before_git — An invalid or unbounded deadline reaches Git instead of refusing preparation.
- 16: tests/test_stage2_research_history.py::test_history_repository_wide_dot_is_not_a_mapped_file — A repository-wide dot expands scope beyond resolved mapped files.
- 5: tests/test_stage2_research_map.py::test_map_merge_cannot_change_keys_or_finder_evidence — Standalone preparation accepts added/dropped/duplicate keys or changed/missing finder reasons; actual dispatch-barrier integration remains pending.
- 24: tests/test_stage2_research_map.py::test_map_exact_union_retains_all_origins_without_persisting_frozen_snapshots — Exact overlapping origins disappear or source snapshots enter the audit map.
- 24: tests/test_stage2_research_map.py::test_map_unresolved_locator_stays_visible_but_grants_no_scope_or_neighbour — A nonresolving locator grants a mapped region or neighbour relation.
- 24: tests/test_stage2_research_map.py::test_map_given_neighbour_is_inserted_even_when_all_finders_omit_it — The runner's given neighbour disappears because finders omitted it.
- 24: tests/test_stage2_research_map.py::test_map_empty_categories_keep_explicit_unread_provenance — An empty category, blank unread marker or lost/changed unread origin is accepted.
- 24: tests/test_stage2_research_map.py::test_map_unread_categories_preserve_each_finder_reason — Unread reasons lose their originating seat in the prepared map.
- 24: tests/test_stage2_research_map.py::test_map_locator_schema_accepts_only_locators_and_meaningful_reasons — Extra decision fields or whitespace reasons enter the structural locator protocol.
- 24: tests/test_stage2_research_map.py::test_map_resolved_neighbour_artifact_maps_to_frozen_sibling_spec — A resolved active/archive/living artifact loses its frozen neighbouring specification.
- 24: tests/test_stage2_research_map.py::test_map_own_and_spec_less_artifacts_do_not_gain_neighbour_status — Own or spec-less artifacts acquire a neighbouring specification or the wrong comparison gap.
- 4: tests/test_stage2_research_map.py::test_map_given_neighbour_header_missing_and_empty_are_distinct — Standalone header validation accepts missing/null values or rejects explicit empty neighbours.
- 4: tests/test_stage2_research_map.py::test_map_given_neighbours_refuse_own_missing_escape_and_non_spec_forms — Own, absent, escaping or non-spec given paths pass standalone validation.
- 16: tests/test_stage2_research_refs.py::test_reference_assignment_reads_do_not_define_module_variables — An attribute/subscript read is mistaken for a module variable definition.
- 16: tests/test_stage2_research_refs.py::test_reference_augmented_assignment_counts_as_an_ambiguous_rebinding — A later augmented assignment silently leaves the original definition unambiguous.
- 16: tests/test_stage2_research_refs.py::test_reference_python_type_alias_has_its_module_assignment_extent — A Python 3.12 type alias lacks its exact assignment extent or duplicate aliases become unambiguous.
- 38: tests/test_stage2_research_catalog.py::test_preflight_free_definition_cannot_redirect_its_declared_go_origin — A free definition changes provider/origin instead of being excluded with raw evidence.
- 38: tests/test_stage2_research_catalog.py::test_preflight_seat_candidate_definition_cannot_redirect_its_go_origin — A preferred or pool Go model whose definition redirects its declared origin is probed or selected instead of skipped as pi-malformed with its raw value.


- 16: tests/test_stage2_research_refs.py::test_reference_markdown_rejects_nonstructural_or_ambiguous_heading — Standalone resolution treats prose, frontmatter, fences, Setext or duplicate titles as an exact ATX heading.
- 16: tests/test_stage2_research_refs.py::test_reference_markdown_extent_ignores_frontmatter_fences_and_lower_headings — Structural extent stops on a fenced heading or excludes a child section.
- 16: tests/test_stage2_research_refs.py::test_reference_criterion_selects_one_item_and_ignores_fenced_items — A fenced/duplicate item resolves or the excerpt crosses its next structural boundary.
- 16: tests/test_stage2_research_refs.py::test_reference_recorded_plan_prompt_extent_uses_exact_structural_title — The historical S-47 title resolves to the fenced example or a different extent than lines 65–94.
- 16: tests/test_stage2_research_refs.py::test_reference_python_uses_ast_definition_extent — A nested Python symbol resolves outside its exact AST extent.
- 16: tests/test_stage2_research_refs.py::test_reference_python_never_falls_back_to_word_search — Prose or an ambiguous/invalid Python definition is accepted as a symbol.
- 16: tests/test_stage2_research_refs.py::test_reference_mapping_has_exact_canonical_json — A YAML date, Unicode mapping or selected value has a noncanonical excerpt.
- 16: tests/test_stage2_research_refs.py::test_reference_mapping_rejects_ambiguous_or_uncitable_values — Dotted keys, indices, duplicate keys, unsafe YAML values or non-finite JSON resolve.
- 16: tests/test_stage2_research_refs.py::test_reference_claim_has_one_shared_unicode_budget_and_no_partial_support — Standalone claim assembly exceeds 4000 Unicode characters or retains an excerpt after any unresolved reference.
- 16: tests/test_stage2_research_refs.py::test_reference_reads_only_frozen_bytes_and_refuses_escape — The resolver reads live bytes or accepts a path escaping the frozen packet.
- 42: tests/test_stage2_research_catalog.py::test_preflight_duplicate_unrelated_metadata_fields_do_not_disable_go — A duplicate foreign-provider/property key disables an otherwise valid Go intersection.
- 42: tests/test_stage2_research_catalog.py::test_preflight_raw_duplicate_keys_inside_models_are_document_ambiguity — A repeated raw key within Go models leaves a free identity eligible instead of duplicate-id capability-unavailable.
- 42: tests/test_stage2_research_catalog.py::test_preflight_non_model_pi_entries_are_not_candidate_faults — An unrelated ignored Pi entry excludes valid free peers.
- 42: tests/test_stage2_research_catalog.py::test_preflight_non_object_capability_keeps_raw_value_evidence — A local malformed entry loses its exact source value.


- 38: tests/test_stage2_research_catalog.py::test_preflight_uses_fresh_pinned_go_snapshot_without_cache_date — Standalone preflight substitutes a shipped list or fabricates Last-Modified; this is not dispatcher integration evidence.
- 38: tests/test_stage2_research_catalog.py::test_preflight_refreshes_despite_fresh_store_and_never_revives_cached_ids — A current cache prevents the forced refresh or revives removed identities in standalone selection.
- 39: tests/test_stage2_research_catalog.py::test_preflight_candidate_fault_does_not_exclude_a_valid_peer — A malformed capability field selects a candidate or removes its valid peer.
- 39: tests/test_stage2_research_catalog.py::test_preflight_missing_metadata_field_is_local_and_explicit — Missing identity or tool support is silently accepted or loses its absence marker.
- 39: tests/test_stage2_research_catalog.py::test_preflight_ignores_unrelated_provider_and_never_adds_metadata_only_ids — Metadata outside the fresh Go intersection selects a free identity.
- 39: tests/test_stage2_research_catalog.py::test_preflight_include_is_checked_before_exclude_and_both_are_audited — Exclude hides an unmet explicit include or selection loses policy dispositions.
- 38: tests/test_stage2_research_catalog.py::test_preflight_missing_or_non_chat_seat_candidate_is_skipped — A missing or non-chat preferred or pool Go model fails the whole preflight or is probed instead of being skipped with its reason.
- 41: tests/test_stage2_research_catalog.py::test_preflight_unsuccessful_pi_response_is_not_measured_empty_or_retried — An unsuccessful public Pi GET becomes an empty roster or performs a second network attempt.
- 41: tests/test_stage2_research_catalog.py::test_preflight_rejects_raw_pi_duplicate_identity_before_selection — Raw repeated Pi keys or equal identities survive permissive runtime parsing.
- 42: tests/test_stage2_research_catalog.py::test_preflight_shared_deadline_has_asymmetric_failure_rules — The local-source reads use independent deadlines or metadata timeout blocks fixed eligibility.
- 42: tests/test_stage2_research_catalog.py::test_preflight_duplicate_metadata_identity_disables_all_free_candidates — Duplicate models.dev identity leaves a free candidate eligible.
- 42: tests/test_stage2_research_catalog.py::test_preflight_unavailable_capabilities_preserve_fixed_model_eligibility — Document-level capability failure removes fixed eligibility or hides an unmet include.
- 42: tests/test_stage2_research_catalog.py::test_preflight_zero_selection_retains_policy_and_measured_outcome — A measured-empty standalone selection loses its policy, zero count or fresh identity record.


- 1: tests/test_stage2_swarm.py::test_large_classes_dispatch_the_swarm — Either class produces only the single GLM exploration report.
- 1: tests/test_stage2_swarm.py::test_swarm_uses_only_the_injected_pi_wrapper — A version or model call bypasses the wrapper, executes the real install in a unit test or resolves bare Pi from PATH.
- 2: tests/test_stage2_swarm.py::test_small_classes_keep_the_single_explorer — Either class starts a finder or swarm researcher.
- 3: tests/test_stage2_swarm.py::test_explicit_class_explores_without_spec_or_plan — Valid early input is refused because a later artifact is absent.
- 4: tests/test_stage2_swarm.py::test_missing_invalid_or_conflicting_class_refuses — Malformed, missing or disagreeing classes pass, or a duplicate, escaping, non-spec or missing frozen neighbour path starts a call.
- 5: tests/test_stage2_swarm.py::test_finder_merge_precedes_every_topic — A topic starts before three valid finder results and a validated exact-union Opus map.
- 6: tests/test_stage2_swarm.py::test_repository_topics_have_three_independent_models — A topic is omitted, a seat runs a model other than its frozen selection, one session supplies two seats, or one candidate fills two seats.
- 7: tests/test_stage2_swarm.py::test_research_carries_practice_architecture_and_adjacent_spec_comparisons — A comparison section or an unread-neighbour gap entry is absent; semantic comparison quality is also checked in phase 6.
- 8: tests/test_stage2_swarm.py::test_online_requests_exclude_private_inputs_and_ambient_paths — A canary from rules, paths, identifiers, finder output, history or private reports appears in an outbound payload or query.
- 9: tests/test_stage2_research_tools.py::test_public_tools_cannot_read_local_or_private_sources — A file or shell tool is available, ambient context is discovered, or fetching reaches local files or private network addresses.
- 10: tests/test_stage2_swarm.py::test_online_claims_require_successful_page_receipts — Search-only, snippet or invented receipts support a claim, or a receiptless claim is not retained as unsupported; a report with no evidence-backed claim is accepted.
- 11: tests/test_stage2_swarm.py::test_role_permissions_do_not_follow_endpoint_privileges — An online seat's model receives the framework packet, or a model outside its seat's frozen selection or role is launched.
- 12: tests/test_stage2_swarm.py::test_leak_block_cancels_queued_dispatch — One scan covers multiple prompts, a queued call starts after BLOCK, a running child is awaited instead of stopped, available partial output is lost instead of retained as cancelled, or exit 1 overrides exit 2.
- 13: tests/test_stage2_swarm.py::test_concurrent_slots_keep_distinct_audits_and_outcomes — Concurrent output cannot be assigned to a slot, or a failed slot is audited as successful.
- 14: tests/test_stage2_swarm.py::test_fresh_opus_reconciles_eleven_topics_and_map — Another model judges, a peer session resumes, a required topic disappears or Opus has any tool.
- 15: tests/test_stage2_swarm.py::test_unresolved_dissent_and_human_questions_survive_reconciliation — An unresolved disagreement loses an opposing claim id or evidence, or judge output contains a maintainer answer field; phase 6 also checks faithful treatment of dissent.
- 16: tests/test_stage2_swarm.py::test_local_citations_name_a_path_and_a_symbol — Unresolvable or line-only references become supported rather than unsupported.
- 17: tests/test_stage2_swarm.py::test_only_the_runner_appends_research — A participant edits a file, rewrites an answer, replaces earlier research or changes git or tracker state.
- 18: tests/test_stage2_swarm.py::test_failed_pi_calls_preserve_partial_evidence — A failed preparatory stage dispatches a later stage, missing required topic reports still reach the judge, a report with zero evidence-backed claims passes outside empty-neighbour topic 5, or a failed free seat alone makes the run incomplete.
- 19: tests/test_stage2_swarm.py::test_amended_graph_and_deadlines_bound_every_launch — An extra invocation or retry occurs, a free slot starts ahead of queued required slots, topic work consumes the judge reserve, or unlaunched slots lack not-started-deadline outcomes.
- 20: tests/test_stage2.py::test_explore_stage2_off_uses_haiku_without_reading_the_glm_key — It runs a swarm, reads a foreign key, names Haiku 4.5 or loses the reason.
- 21: tests/test_stage2_swarm.py::test_all_outputs_scrub_every_used_credential — A planted fragment survives in an answer, receipt, concurrent log or error.
- 22: tests/test_stage2_swarm.py::test_amended_doctrine_and_research_roles_agree — Six-topic or Zen-free-through-Pi instructions remain operative, the review ladder changes, or an accepted ADR is edited.
- 23: tests/test_stage2_swarm.py::test_public_topic_is_filtered_before_online_calls — Invalid/missing/private topics or forbidden punctuation pass; allowed German examples or separators fail; rejection fails to stop topics with exit 1.
- 24: tests/test_stage2_swarm.py::test_finder_trio_locates_four_categories_without_judging — Only one finder runs, a fifth locator field passes, or an empty category lacks an unread marker.
- 25: tests/test_stage2_swarm.py::test_each_topic_uses_its_agreed_questions_and_scope — A packet differs from its topic prompt; report prose that proposes new code or local applicability outside that scope is scored off-brief and checked in phase 6.
- 26: tests/test_stage2_swarm.py::test_peers_receive_identical_frozen_briefs_without_reports — One model receives a different map, instruction file, angle or peer report, or its runtime auto-loads instructions.
- 27: tests/test_stage2_swarm.py::test_report_template_refuses_missing_fields_and_eighth_claim — Required fields, topic-5 per-neighbour relations or confidence basis are missing, or an eighth claim passes.
- 28: tests/test_stage2_swarm.py::test_model_scores_name_the_claims_they_count — A valid claim has two dispositions, a unique claim is not supported, an unsupported claim is supported, a score lacks claim ids, or a failed seat has no named outcome.
- 29: tests/test_stage2_swarm.py::test_given_and_suggested_neighbours_keep_their_provenance — A suggestion becomes authoritative, a given path vanishes or its proposed removal loses the human item.
- 30: tests/test_research_handoff.py::test_spec_neighbours_match_confirmed_research_paths — A required path disappears or an extra path outside confirmed/given/linked-human sets passes.
- 31: tests/test_stage2_swarm.py::test_decisions_and_dissent_enter_the_interview_inventory — A refuted/off-brief report decision is omitted, a differing class lacks an automatically derived item, or grouping duplicates loses a source question or claim id.
- 32: tests/test_research_handoff.py::test_a_lost_research_decision_turns_the_gate_red — Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
- 33: tests/test_research_handoff.py::test_unread_or_ambiguous_handoff_is_not_measured — Malformed manifests/inventories, duplicate global ids or report-local ids, missing linked files or ambiguous answers silently pass.
- 34: tests/test_research_handoff.py::test_every_criterion_names_existing_claims_or_answers — Missing/incomplete/non-supported claim ids or unanswered Q-records pass, including mixed direct bases.
- 35: tests/test_stage2_swarm.py::test_volatile_fact_governance_remains_a_human_proposal — A volatile claim without governance passes validation or a proposal is implemented without a human answer; phase 6 also checks whether changing facts were correctly marked volatile.
- 36: tests/test_stage2_swarm.py::test_provider_limit_is_shared_across_topics_and_roles — A fifth Go call starts across roles, queued work survives a leak/declaration refusal, available cancelled output is discarded, or exit 1 overrides security exit 2.
- 37: tests/test_stage2_swarm.py::test_online_topics_use_the_three_online_seat_selections — A free model, Claude Code or a model other than the seat's selection supplies one of the nine required online contributions.
- 38: tests/test_stage2_research_catalog.py::test_each_run_forces_a_fresh_go_catalog — A cached/shipped list substitutes for refresh, a baseline-only free id is dispatched, another provider supplies a seat, or selection lacks dated provenance.
- 38: tests/test_stage2_research_catalog.py::test_removed_shipped_free_ids_do_not_return — A cached/shipped list substitutes for refresh, a baseline-only free id is dispatched, another provider supplies a seat, or selection lacks dated provenance.
- 39: tests/test_stage2_swarm.py::test_selected_free_models_cover_all_online_topics_on_identical_briefs — A selected seat is silently omitted or failed as successful, a non-selected or no-tool-support model runs, peer briefs differ, or a missing explicit include starts any model instead of preflight exit 1.
- 39: tests/test_stage2_swarm.py::test_go_free_policy_filters_and_freezes_each_run — A selected seat is silently omitted or failed as successful, a non-selected or no-tool-support model runs, peer briefs differ, or a missing explicit include starts any model instead of preflight exit 1.
- 39: tests/test_stage2_swarm.py::test_selected_free_models_ride_only_the_public_role_under_the_policy — An unselected, excluded, off-suffix, off-provider or non-included id is launched as a free online seat (per-invocation permission).
- 39: tests/test_stage2_swarm.py::test_malformed_online_free_policy_is_a_declaration_fault — A malformed or non-free `online_free` policy reaches a launch instead of exit 2.
- 6: tests/test_stage2_swarm.py::test_role_launches_read_identities_from_the_frozen_selection_and_declaration — A launch names a model other than its frozen seat, a Go seat does not ride Pi, an Opus role does not ride Claude Code (identity part only of criteria 6 and 37; the run-level rows stay not yet written).
- 11: tests/test_stage2_swarm.py::test_a_role_launch_set_with_one_unpermitted_role_starts_none — A set with one unpermitted role is partly returned, so earlier roles could launch.
- 40: tests/test_stage2_swarm.py::test_dynamic_free_permission_is_public_only — A Go free model fills a private role or receives private context through the endpoint's framework permission.
- 41: tests/test_stage2_research_catalog.py::test_unmeasured_catalog_never_becomes_zero_availability — A Pi refresh timeout, stale-only, malformed or ambiguous result becomes N=0 or exits other than 1.
- 41: tests/test_stage2_swarm.py::test_catalog_failure_stops_before_all_model_calls — Pi catalog failure starts a model or probe, uses a cached/Zen roster or exits 0/2/3 instead of 1.
- 42: tests/test_stage2_swarm.py::test_measured_empty_catalog_keeps_all_required_slots — Valid zero selection is refused or drops one of the 39 required slots.
- 4: tests/test_stage2_swarm.py::test_an_unreadable_header_or_empty_class_refuses — Malformed, missing or disagreeing classes pass, or a duplicate, escaping, non-spec or missing frozen neighbour path starts a call.
- 8: not a test — step 6 real-Pi offline capture; a private canary in an outbound request refutes isolation.
- 9: not a test — step 6 real-Pi offline capture; any available local tool or discovered private context refutes isolation.
- 9: tests/test_stage2_research_tools.py::test_the_tools_run_as_pi_calls_them — the actual tool signature loses parameters or yields an invalid result.
- 10: tests/test_stage2_research_tools.py::test_search_results_carry_the_decoded_destination — Search-only, snippet or invented receipts support a claim, or a receiptless claim is not retained as unsupported; a report with no evidence-backed claim is accepted.
- 16: tests/test_stage2_swarm.py::test_local_citations_bind_to_the_frozen_input_state — Citations resolve against live instead of frozen bytes, or mid-run edits still allow complete publication.
- 18: tests/test_stage2_swarm.py::test_every_failed_slot_keeps_partial_output_before_cleanup — A failed preparatory stage dispatches a later stage, missing required topic reports still reach the judge, a report with zero evidence-backed claims passes outside empty-neighbour topic 5, or a failed free seat alone makes the run incomplete.
- 19: tests/test_stage2_swarm.py::test_no_call_starts_once_the_run_deadline_is_spent — An extra invocation or retry occurs, a free slot starts ahead of queued required slots, topic work consumes the judge reserve, or unlaunched slots lack not-started-deadline outcomes.
- 22: not a test — phase-6 review and PR file list; an accepted ADR edit or second new ADR refutes the delivery contract.
- 32: tests/test_research_handoff.py::test_live_archive_and_legacy_handoff_scope — Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
- 32: tests/test_ci.py::test_research_handoff_blocks_local_and_hosted_verification — Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
- 32: tests/test_kit.py::test_research_handoff_checker_and_tests_travel — Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
- 36: tests/test_stage2_swarm.py::test_stages_dispatch_concurrently_within_provider_limits — A fifth Go call starts across roles, queued work survives a leak/declaration refusal, available cancelled output is discarded, or exit 1 overrides security exit 2.

- 4: tests/test_stage2_swarm.py::test_invalid_given_neighbours_refuse_before_models — Missing, duplicate, escaping or non-spec paths start a call.
- 18: tests/test_stage2_swarm.py::test_preparatory_failure_prevents_dependent_stages — Finder, merge or sentence failure still dispatches a topic or judge.
- 18: tests/test_stage2_swarm.py::test_failed_free_seat_is_named_without_failing_completion — A provider failure, timeout or receiptless free report either vanishes or fails an otherwise valid run.
- 19: tests/test_stage2_swarm.py::test_required_slots_precede_free_and_reserve_judge_time — Free work starts ahead of required work, spends judge reserve, or unlaunched seats lack outcomes.
- 16: tests/test_stage2_swarm.py::test_frozen_digest_detects_tracked_and_change_input_edits — A mid-run edit to tracked or untracked change input still publishes complete.
- 10: tests/test_stage2_swarm.py::test_unsupported_claims_are_retained_and_report_requires_evidence — One bad claim fails a valid report, or a zero-evidence report passes outside empty-neighbour topic 5.
- 27: tests/test_stage2_swarm.py::test_report_ids_are_local_and_questions_link_existing_claims — Duplicate local ids or dangling question claims pass; matching ids across distinct seats collide globally.
- 31: tests/test_stage2_swarm.py::test_raw_off_brief_decisions_and_class_mismatches_cannot_disappear — Judge filtering hides accepted-report decisions or a class mismatch lacks a derived item.
- 32: tests/test_research_handoff.py::test_pending_handoff_is_green_only_before_spec — Pre-spec pending items fail, or the same unanswered items pass with a spec.
- 32: tests/test_research_handoff.py::test_only_complete_runs_supply_handoff_and_prior_obligations_survive — Incomplete claims support a spec, no complete run passes, or rerunning erases obligations.
- 28: tests/test_stage2_swarm.py::test_dispositions_are_exclusive_and_unique_is_supported_subset — Unresolved evidence is forced supported/refuted, or unique marks unsupported claims.
- 35: tests/test_stage2_swarm.py::test_topic_specific_class_and_volatile_fields_are_required — Topic 3 omits its class or a volatile topic-6 claim omits governance.
- 29: tests/test_research_handoff.py::test_given_neighbour_drop_requires_linked_human_answer — A judge rejection removes a given neighbour without an answered item.
- 39: tests/test_stage2_research_catalog.py::test_free_eligibility_requires_text_chat_and_explicit_tools — Non-chat, baseline-only, missing/false models.dev tool_call or deprecated entries yield a selected seat.
- 39: tests/test_stage2_swarm.py::test_missing_explicit_include_stops_before_models — Missing included id starts fixed slots instead of preflight exit 1.
- 7: not a test — phase-6 review checks comparison meaning; code summaries presented as comparisons refute it.
- 15: not a test — phase-6 review checks faithful dissent; a majority erasing a sourced objection refutes it.
- 24: not a test — phase-6 review checks finder prose; choosing a design exceeds the locator role.
- 25: not a test — phase-6 review checks topic scope; new-code proposals or local online applicability refute it.
- 34: not a test — phase-6 review checks that resolved criterion bases actually support the criterion.
- 35: not a test — phase-6 review checks volatile classification; repeatedly changing facts treated as timeless refute it.

- 5: tests/test_stage2_swarm.py::test_merge_is_exact_finder_union_with_all_origins — A dropped, added or duplicate key dispatches topics, or deduplication loses a finder/reason.
- 24: tests/test_stage2_swarm.py::test_map_resolution_excludes_unresolved_and_inserts_given_neighbours — Live-tree resolution grants scope, a given neighbour vanishes, or packet/manifest neighbours differ from the independent fixture derivation.
- 16: tests/test_stage2_swarm.py::test_frozen_copies_are_scratch_only_and_removed_after_run — Success or abort retains copies, whole-file snapshots enter research/briefs, or copy failure launches models.
- 27: tests/test_stage2_swarm.py::test_topic_five_relations_cover_exact_packet_neighbours — Missing, extra or duplicate paths or empty/dangling local claims pass.
- 31: tests/test_stage2_swarm.py::test_neighbour_relations_derive_items_without_judge_or_question — A contradicts or unrelated-given field loses its obligation when Opus omits it.
- 34: tests/test_research_handoff.py::test_every_direct_basis_claim_must_be_supported — Any non-supported disposition passes, including alongside a supported claim; answered Q-record mediation fails.
- 30: tests/test_research_handoff.py::test_neighbour_parity_allows_only_linked_additions_and_given_drops — Arbitrary extra paths pass, or linked maintainer additions fail.
- 5: tests/test_stage2_swarm.py::test_all_opus_roles_have_empty_tools_and_packet_only_context — Merge has file, shell, web or MCP access.
- 14: tests/test_stage2_swarm.py::test_all_opus_roles_have_empty_tools_and_packet_only_context — Judge has file, shell, web or MCP access.
- 23: tests/test_stage2_swarm.py::test_all_opus_roles_have_empty_tools_and_packet_only_context — Public-topic author reads beyond its private packet.
- 28: tests/test_stage2_swarm.py::test_judge_gets_resolved_excerpts_with_bounded_truncation — Valid claims lack evidence excerpts, excerpt source mismatches or cap/truncation flags fail.
- 39: tests/test_stage2_research_catalog.py::test_models_dev_capabilities_intersect_only_fresh_pi_ids — Missing/false tool_call, deprecated status, wrong provider or models.dev-only ids are selected.
- 42: tests/test_stage2_research_catalog.py::test_models_dev_failure_excludes_free_and_keeps_required_slots — Source failure launches free models, aborts required slots or masquerades as measured empty metadata.
- 42: tests/test_stage2_swarm.py::test_capability_unavailable_keeps_required_slots_unless_include_is_required — Default fallback blocks required slots, or an ineligible explicit include starts models.


- 4: tests/test_stage2_swarm.py::test_swarm_requires_neighbour_key_but_accepts_empty_list — Missing/null/non-list header starts models or explicit [] refuses; repair message omits the required key.
- 16: tests/test_stage2_swarm.py::test_history_packet_binds_only_mapped_frozen_head_commits — A hash outside the bounded packet or PR/bead id alone becomes evidence, ten-per-path/body caps fail, or history reaches another topic.
- 18: tests/test_stage2_swarm.py::test_history_collection_failure_prevents_all_topics — Failed read-only git collection starts any topic or loses partial evidence.
- 26: tests/test_stage2_swarm.py::test_history_packet_binds_only_mapped_frozen_head_commits — Topic-6 peers receive different history packets.
- 29: tests/test_stage2_swarm.py::test_neighbour_artifacts_normalize_to_change_specs_or_no_spec_gaps — Independent fixture derivation finds an eligible active/archive/living spec omitted or wrongly marked no-spec/self, even with a gap; own-change entries gain neighbour status.
- 27: tests/test_stage2_swarm.py::test_neighbour_artifacts_normalize_to_change_specs_or_no_spec_gaps — Topic 5 accepts a missing relation for a normalized spec path or requires a relation for no-spec.
- 29: tests/test_research_handoff.py::test_cross_run_neighbour_conflicts_require_linked_human_answers — A confirmed/rejected path or omitted prior given path loses its derived human item.
- 30: tests/test_research_handoff.py::test_cross_run_neighbour_conflicts_require_linked_human_answers — Latest-only parity passes; unanswered conflict passes with either header, keep passes without the path or drop passes with it.
- 31: tests/test_research_handoff.py::test_cross_run_neighbour_conflicts_require_linked_human_answers — Either cross-run conflict lacks path, both source runs or source evidence.
- 32: tests/test_research_handoff.py::test_cross_run_neighbour_conflicts_require_linked_human_answers — An unanswered cross-run item passes despite a spec, or a prior complete run loses authority.
- 38: tests/test_stage2_research_catalog.py::test_go_seat_candidates_require_fresh_text_chat_entries — An absent, baseline-only or non-chat preferred or pool Go model is probed or selected, or models.dev decides a preferred model.
- 45: tests/test_stage2_research_availability.py::test_a_seat_whose_candidates_all_miss_the_fresh_catalog_stops — A seat whose preferred model and whole pool miss the fresh overlay is not named as seat-unavailable with exit 1 before any call.
- 42: tests/test_stage2_research_catalog.py::test_capability_document_faults_and_candidate_faults_are_distinct — A malformed candidate excludes a valid peer, a non-boolean tool_call selects a seat, or a document-level fault is treated as measured absence.
- 39: tests/test_stage2_research_catalog.py::test_capability_document_faults_and_candidate_faults_are_distinct — Candidate eligibility ignores exact metadata shape or an unrelated provider's malformed entry disables selection.
- 41: tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — Pi unfinished at 60 seconds dispatches calls or successful Pi plus timed-out models.dev aborts fixed work.
- 42: tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — Models.dev timeout extends 60 seconds, retries, lacks timeout reason or blocks 39 required slots without an explicit include.
- 19: tests/test_stage2_research_catalog.py::test_catalog_shared_deadline_keeps_asymmetric_failure_rules — Reads start sequentially or receive separate 60-second budgets.
- 38: tests/test_stage2_research_catalog.py::test_nonempty_selection_keeps_both_sources_and_exclusion_evidence — At N=1, removing models.dev URL/UTC/digest or a deprecated candidate's reason and raw status fails to turn audit red.
- 39: tests/test_stage2_research_catalog.py::test_nonempty_selection_keeps_both_sources_and_exclusion_evidence — An excluded candidate is omitted while another candidate remains eligible.
- 14: tests/test_stage2_swarm.py::test_judge_packet_limit_refuses_before_launch_without_shortening — J+1 reaches the judge, J fails size validation, excerpts shrink to fit or a second call/N reduction occurs.
- 18: tests/test_stage2_swarm.py::test_judge_packet_limit_refuses_before_launch_without_shortening — Oversize loses reports/excerpts or does not end incomplete exit 1 as judge-packet-over-limit.
- 28: tests/test_stage2_research_refs.py::test_reference_claim_has_one_shared_unicode_budget_and_no_partial_support — Three 4,000-character sources yield more than 4,000 excerpt characters for one claim, lose citation order or lack truncation marking.

- 4: tests/test_stage2_swarm.py::test_neighbour_paths_use_only_active_archive_and_living_specs — Templates, own spec or a fourth path form starts a call; a valid frozen active/archive/living spec refuses.
- 16: tests/test_stage2_research_refs.py::test_reference_python_uses_ast_definition_extent — Prose-only or duplicate targets resolve, or Markdown/criterion/Python/YAML/JSON/other-file excerpts have the wrong extent.
- 24: tests/test_stage2_swarm.py::test_neighbour_artifacts_normalize_to_change_specs_or_no_spec_gaps — Packet or manifest omits an eligible spec-backed entry even though it lists a gap.
- 29: tests/test_stage2_swarm.py::test_neighbour_artifacts_normalize_to_change_specs_or_no_spec_gaps — A living spec or archived artifact is no-spec, or own-change self is mistaken for a neighbour/gap.
- 29: tests/test_stage2_swarm.py::test_neighbour_status_uses_three_relations_and_never_judge_verdict — Any unrelated seat permits confirmation, three counting unrelated relations are not rejected, or Opus overrides runner status.
- 31: tests/test_stage2_swarm.py::test_neighbour_status_uses_three_relations_and_never_judge_verdict — A split or contradicts entry loses its independent human item.
- 30: tests/test_research_handoff.py::test_structured_neighbour_answers_enforce_keep_drop_and_unlinked_add — Prose-only or path-free linked answers close items, keep/drop allow the wrong header, or an answered add requires a fabricated item link.
- 32: tests/test_research_handoff.py::test_split_neighbours_need_item_link_and_structured_keep_or_drop — An unanswered split passes either header or a judge confirmation substitutes for the maintainer.
- 33: tests/test_research_handoff.py::test_conflicting_neighbour_directives_are_not_measured — A path in two directive lists or incompatible answered records passes instead of exit 3.
- 33: tests/test_research_handoff.py::test_duplicate_keys_in_records_are_not_measured — A JSON or nested YAML key stated twice in a handoff record is read as its last value instead of not measured (exit 3).
- 30: tests/test_research_handoff.py::test_neighbour_directives_check_form_without_current_existence — Invalid forms pass, or archival invalidates a structurally valid historical path.
- 42: tests/test_stage2_research_catalog.py::test_duplicate_raw_keys_or_claimed_ids_exclude_all_free_candidates — Repeated raw model keys or equal ids under different keys leave a seat selectable instead of capability-unavailable/duplicate-id.
- 42: tests/test_stage2_research_catalog.py::test_missing_metadata_id_excludes_only_that_candidate — A missing id admits a seat, loses its absent marker, or excludes a valid peer.
- 7: tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence — An empty packet lacks the named no-neighbour comparison gap.
- 18: tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence — Empty-neighbour topic 5 prevents completion or changes the 39 fixed slots.
- 18: tests/test_stage2_swarm.py::test_a_run_longer_than_the_preparation_deadline_still_publishes_complete — A successful run over 60 seconds is reported incomplete although no input changed.
- 18: tests/test_stage2_swarm.py::test_a_failed_store_write_keeps_every_outcome_and_still_publishes_incomplete — After a failed terminal store write the cancelled siblings' outcomes are dropped and a failed binding write loses the incomplete publication.
- 18: tests/test_stage2_swarm.py::test_an_aborted_run_names_every_expected_slot_with_its_outcome — An aborted run's manifest lacks the identities and not-started outcomes of the slots of later stages.
- 27: tests/test_stage2_swarm.py::test_empty_neighbour_topic_runs_three_seats_without_invented_evidence — Empty-packet relations or missing not-read pass, or a nonempty packet waives the evidence floor.

- 16: tests/test_stage2_research_refs.py::test_reference_markdown_extent_ignores_frontmatter_fences_and_lower_headings — A quoted heading becomes structure, changes uniqueness/extent or supplies a criterion; the five S-47 cases resolve wrongly.
- 16: tests/test_stage2_research_refs.py::test_reference_mapping_has_exact_canonical_json — Dotted keys/list indices or duplicate/non-JSON values resolve, dates lose ISO text, or canonical bytes differ.
- 10: tests/test_stage2_swarm.py::test_claim_requires_every_citation_before_excerpts_or_scoring — One successful page receipt hides another unreceipted URL in the same claim.
- 16: tests/test_stage2_swarm.py::test_claim_requires_every_citation_before_excerpts_or_scoring — One resolving citation hides an unresolved citation, grants an excerpt or satisfies the report floor.
- 16: tests/test_stage2_swarm.py::test_a_run_longer_than_the_preparation_deadline_still_publishes_complete — A successful run over 60 seconds ends incomplete because the publication drift check reuses the expired freezing deadline.
- 28: tests/test_stage2_swarm.py::test_claim_requires_every_citation_before_excerpts_or_scoring — An unsupported mixed-citation claim gets an excerpt or disposition.
- 38: tests/test_stage2_research_catalog.py::test_pi_overlay_duplicates_block_but_malformed_candidates_are_local — A malformed preferred or pool Go model entry is probed or selected instead of skipped as pi-malformed with its raw value.
- 38: tests/test_stage2_swarm.py::test_the_receipt_keeps_each_candidates_evidence_and_exclusion — The receipt drops a free candidate's id, source field value and exclusion reason.
- 38: tests/test_stage2_swarm.py::test_the_manifest_publishes_preparation_time_pool_candidates_and_probe_audit — The published manifest omits preparation time, pool, candidate outcomes or probe audit lines.
- 38: tests/test_stage2_swarm.py::test_the_measured_catalog_reaches_pis_agent_directory_for_probes_and_launches — Probes start Pi with an agent directory holding no measured model definitions.
- 41: tests/test_stage2_research_catalog.py::test_pi_overlay_duplicates_block_but_malformed_candidates_are_local — A repeated overlay id starts any model or is silently merged.
- 42: tests/test_stage2_research_catalog.py::test_pi_overlay_duplicates_block_but_malformed_candidates_are_local — One bad Pi candidate blocks 39 required slots, excludes valid peers or loses pi-malformed/raw value.
- 29: tests/test_stage2_swarm.py::test_neighbour_status_ignores_relations_without_valid_claims — Unsupported-only evidence confirms/rejects a path instead of split, or judge disposition changes runner validity.
- 31: tests/test_stage2_swarm.py::test_neighbour_status_ignores_relations_without_valid_claims — Unsupported-only contradicts or unrelated-given fields lose human items.
- 30: tests/test_research_handoff.py::test_neighbour_evidence_gap_requires_structured_answer — An evidence-gap split joins the required header without structured keep or passes an incompatible header after keep/drop.
- 32: tests/test_research_handoff.py::test_neighbour_evidence_gap_requires_structured_answer — Once a spec exists, an unsupported-relation split passes without an item-linked maintainer keep/drop.
- 4: tests/test_stage2.py::test_stage2_off_skips_class_and_neighbours_but_refuses_class_argument — Class checks leak into explicit fallback or an ineffective --class is accepted beside it.
- 20: tests/test_stage2.py::test_stage2_off_skips_class_and_neighbours_but_refuses_class_argument — Bead-only or invalid class/neighbour headers block fallback, route/model/reason disappear, or --class permits any call.

- 43: tests/test_stage2_research_availability.py::test_preferred_models_come_first_and_substitutes_never_take_them — A substitute replaces an admitted, unexcluded, reachable preferred model or takes another seat's reachable preferred model, or one model fills two seats of a trio.
- 43: tests/test_stage2_research_availability.py::test_unadmitted_or_excluded_models_are_never_probed_or_selected — A model with a skip mark, undeclared, absent from the fresh overlay, on an unmeasured wire API or under a timed exclusion is probed or selected.
- 43: tests/test_stage2_swarm.py::test_finders_use_the_repository_seat_selection — A finder runs a model other than its repository seat's selection.
- 43: tests/test_stage2_swarm.py::test_the_measured_catalog_reaches_pis_agent_directory_for_probes_and_launches — A seat is probed or selected under an unmeasured transport because Pi resolves shipped metadata.
- 44: tests/test_stage2_research_availability.py::test_report_names_every_seat_candidate_and_check_time — The printed report omits a seat, a substitute's "substitute for <seat>" mark, a model's reason, the pool in cost order, the free selection or the UTC check time.
- 44: tests/test_stage2_research_availability.py::test_receipt_is_bound_single_use_and_fresh — A research call starts without the id, after the maximum age, after a bound input changed, from another worktree or from a consumed or corrupt receipt, or the refusal exits other than 2.
- 44: tests/test_stage2.py::test_receipt_id_is_refused_where_no_swarm_runs — Bounded, spike or --stage2-off exploration requires or accepts --availability-reported, or prepare-explore runs there.
- 20: tests/test_stage2.py::test_receipt_id_is_refused_where_no_swarm_runs — An --availability-reported id beside --stage2-off is accepted.
- 45: tests/test_stage2_research_availability.py::test_a_seat_without_candidate_stops_before_research_with_exit_one — A receipt stays usable, a research call starts, the empty seat is unnamed, the exit is not 1, or the seat is filled from outside its preferred model and the pool.
- 46: tests/test_stage2_swarm.py::test_selection_is_frozen_for_the_run_and_recorded — A failing selected model is replaced, retried or probed again, a later preparation changes a running run, or the manifest lacks the receipt id, a selection with its preferred or substitute mark, or a model's reason.
- 46: tests/test_stage2_swarm.py::test_the_manifest_publishes_preparation_time_pool_candidates_and_probe_audit — The manifest lacks the check time, pool or any candidate's outcome of the consumed receipt.
- 47: tests/test_stage2_research_availability.py::test_probes_send_only_the_fixed_text_without_tools — A private canary reaches a probe's payload, argv or environment, a tool is available, a bare pi or unofficial Claude client runs, or a probe lacks its leak check, audit record or 60-second limit.
- 47: tests/test_stage2_research_availability.py::test_claude_code_candidate_is_probed_through_official_claude — A Claude Code preferred model counts as reachable without a probe or is probed with a tool.
- 47: not a test — step 6's real-Pi offline capture also records one probe's outbound payload; a private canary in it refutes the criterion.
- 48: tests/test_stage2_research_availability.py::test_probes_are_lazy_unique_and_outside_the_run_budget — A model is probed twice, a pool model is probed while no seat needs it or a cheaper usable one is untried, a free model or Opus role is probed, a worktree file changes, or probes reduce the run's slots.
- 17: tests/test_stage2_research_availability.py::test_probes_are_lazy_unique_and_outside_the_run_budget — Preparation changes a file in the worktree.
- 49: tests/test_model_endpoints.py::test_seat_candidate_lists_and_availability_rule_are_validated — A seat without a preferred model or with a second model or fallback list, an undeclared, -free, off-Go online or no-framework repository model, or a malformed maximum age, wire-API set or exclusion, passes declaration validation.
- 40: tests/test_model_endpoints.py::test_seat_candidate_lists_and_availability_rule_are_validated — A -free id as a seat's preferred model passes.
- 49: tests/test_stage2_research_availability.py::test_malformed_seat_declaration_refuses_before_any_call — A malformed declaration lets a probe or research call start, a declared fallback list is consulted, or the refusal exits other than 2.
- 50: tests/test_stage2_research_availability.py::test_research_preparation_uses_the_shared_availability_helpers — The research path defines its own rule validation, timed-exclusion matching, probe or receipt sealing instead of the shared functions.
- 50: not a test — phase-6 review and the verification run of tests/test_stage2_availability.py wherever the review swarm's preparation is on the base branch; a changed or failing review availability test refutes the criterion.
- 59: tests/test_stage2_research_availability.py::test_substitute_is_the_cheapest_reachable_unused_pool_model — A costlier pool model wins while a cheaper one is unexcluded, reachable and unused, or a tie is not broken by id.
- 59: tests/test_stage2_research_availability.py::test_frozen_inputs_give_the_same_selection_twice — Two preparations with the same catalog, terms, exclusions and probe outcomes select differently.
- 59: tests/test_stage2_research_availability.py::test_pool_requires_tool_support_and_a_measured_wire_api — A pool model without models.dev tool_call true, deprecated, on an unmeasured wire API, or offered while models.dev is unavailable becomes a substitute.
- 60: tests/test_stage2_research_availability.py::test_a_model_without_admitted_terms_or_cost_is_never_used — A Go model without a passing terms record or a positive anfragen_5h is probed, selected or substituted, or an unread overlay model is missing from the report.
- 61: tests/test_stage2_research_availability.py::test_one_terms_record_admits_a_new_substitute_without_other_edits — A fixture that adds only a modelle_terms record does not see the model in the pool at its cost position, or the review ladder changes.
- 61: tests/test_stage2_swarm.py::test_research_launches_install_the_consumed_catalog_store — A research launch resolves its model from shipped metadata instead of the measured catalog.
- 51: tests/test_stage2_research_store.py::test_terminal_record_survives_sigkill_after_the_outcome — A runner killed with SIGKILL after a slot's terminal outcome loses or tears that slot's record.
- 51: tests/test_stage2_research_store.py::test_temporary_or_torn_files_never_read_as_results — A temporary or truncated record is read as a finished result.
- 51: tests/test_stage2_research_dispatch.py::test_terminal_callback_precedes_the_workers_next_launch — The same worker launches its next slot before the terminal callback returns, or a launch lacks a prior launch record.
- 52: tests/test_stage2_research_store.py::test_store_is_owner_only_outside_every_model_directory — The store lies inside the worktree, its git directory or a model directory, or grants group or other access.
- 17: tests/test_stage2_research_store.py::test_store_is_owner_only_outside_every_model_directory — The state store writes inside the worktree.
- 52: tests/test_stage2_swarm.py::test_store_paths_and_peer_results_never_reach_a_model — A store canary or a peer's stored report reaches a model's prompt, argv, environment or working directory before the barrier.
- 52: tests/test_stage2_swarm.py::test_a_store_inside_the_real_home_is_refused_and_one_outside_it_is_accepted — The default store beneath the home directory Claude research processes inherit passes the placement guard.
- 53: tests/test_stage2_research_store.py::test_reuse_requires_the_exact_binding_seat_model_and_prompt — A result with another binding, stage, topic, seat, endpoint, model or prompt hash is reused, or a matching valid result is launched again.
- 53: tests/test_stage2_research_store.py::test_binding_ignores_only_the_own_research_append_and_head — A foreign byte change permits reuse, or a commit recording only the runner's own append discards matching results.
- 53: tests/test_stage2_swarm.py::test_only_finished_valid_results_are_reused_and_others_are_named — A cancelled, failed, timed-out, refused, not-started, interrupted or invalid result is reused, a discarded result is unnamed, or a complete run's results are reused.
- 54: tests/test_stage2_swarm.py::test_a_resumed_run_is_a_new_run_within_its_slot_budget — Launched plus reused slots exceed 39 + 3N, a reused slot also launches, a slot launches twice, or the earlier run's deadline, manifest or receipt is continued.
- 55: tests/test_stage2_swarm.py::test_reused_and_interrupted_slots_are_marked_in_the_manifest — A reused result looks launched by this run, loses its source run or original times, or an interrupted source slot is missing.
- 56: tests/test_stage2_research_store.py::test_a_refused_run_is_never_a_resume_source — Any result of a run with a security refusal is reused, or the refusal is not named.
- 57: tests/test_stage2_research_dispatch.py::test_failed_terminal_write_stops_the_stage_with_exit_one — A slot launches after a failed write, the failure is unnamed, or the stage exits 0, or 2 without a security refusal.
- 58: tests/test_stage2_research_store.py::test_one_run_per_change_and_a_killed_runs_lock_is_released — Two runs of one change write the store at once, or a killed run's lock blocks the next run.
- 21: tests/test_stage2_research_store.py::test_store_receipt_and_probe_records_are_scrubbed — A planted credential fragment survives in a probe record, selection receipt or store record.
- 53: tests/test_stage2_research_store.py::test_binding_names_an_untracked_change_input_edit_added_or_removed — An untracked change-input edit, addition or removal permits reuse.
- 53: tests/test_stage2_research_store.py::test_binding_refuses_a_foreign_research_tail — A foreign research.md tail permits reuse.
- 53: tests/test_stage2_research_store.py::test_binding_survives_head_moving_by_a_commit_of_the_own_tail — A commit that only records the runner's own append discards matching results.
- 53: tests/test_stage2_research_store.py::test_unfinished_outcomes_are_never_reused_and_are_named — A cancelled, failed, timed-out, refused or not-started result is reused or not named.
- 53: tests/test_stage2_research_store.py::test_interrupted_and_invalid_results_are_not_reused_and_are_named — An interrupted or validation-failing result is reused or not named.
- 53: tests/test_stage2_research_store.py::test_a_complete_run_clears_the_store_and_a_cleared_store_has_no_source — The results of a run published complete are reused.
- 54: tests/test_stage2_research_store.py::test_a_matching_valid_result_is_never_also_a_launch — A reused slot also launches.
- 55: tests/test_stage2_research_store.py::test_adopted_results_carry_their_source_run_and_original_times — A copied-forward result loses its source run, original times or leak-check record.
- 55: tests/test_stage2_swarm.py::test_a_reused_result_keeps_its_original_start_and_leak_check_in_the_published_manifest — A completed resumed run loses the original start time or the original leak-check record of a reused slot.
- 57: tests/test_stage2_research_dispatch.py::test_a_failed_launch_record_write_stops_without_launching_that_slot — A slot launches after its launch record failed to write.
- 57: tests/test_stage2_swarm.py::test_a_failed_store_write_keeps_every_outcome_and_still_publishes_incomplete — A persistent store-write failure loses the incomplete record or the partial evidence of siblings.
- 44: tests/test_stage2_research_availability.py::test_fresh_receipt_is_consumed_once_and_returns_the_frozen_selection — A receipt at the maximum age is refused, survives its first use, or consumption returns something other than the prepared selection.
- 44: tests/test_stage2_swarm.py::test_the_receipt_keeps_each_candidates_evidence_and_exclusion — The sealed receipt omits the candidate evidence behind the selection report.
- 48: tests/test_stage2_research_availability.py::test_slot_plan_is_built_from_the_consumed_selection_and_probes_add_no_slots — The slot plan ignores a substitute or probes change the `39 + 3N` slot count.
- 47: tests/test_stage2_research_availability.py::test_a_leak_stops_preparation_before_any_probe — A leak-check BLOCK lets a probe start or leaves a receipt.
- 49: tests/test_model_endpoints.py::test_the_repository_declaration_carries_six_seats_and_the_rule — The shipped declaration drops a preferred model, the rule or the dynamic free permission, or carries a shape or permission fault.
- 59: tests/test_stage2_research_catalog.py::test_preflight_pool_candidates_need_models_dev_tool_support — A pool candidate is judged by a missing, failed or malformed models.dev answer as if it supported tools.
- 41: tests/test_stage2_research_availability.py::test_a_catalog_failure_stops_before_any_probe_and_leaves_no_receipt — A Pi catalog failure starts a probe, keeps an earlier receipt usable or exits other than 1.
- 29: tests/test_stage2_swarm.py::test_the_inventory_is_persisted_in_the_fenced_run_block — The runner derives neighbour statuses but never persists them, or persists them outside the one fenced run block.
- 31: tests/test_stage2_swarm.py::test_the_inventory_is_persisted_in_the_fenced_run_block — The runner derives the obligation inventory but never persists it, or persists it outside the one fenced run block.

## Not touched

Accepted ADRs, numbered-decision continuity map, adoption records, human answer
content, session runtime/policy, review-ladder membership/order, sibling
checkouts, tracker and user configuration stay. `tests/test_stage2_availability.py`
(the review swarm's, #157) is not edited; where it is on the base it runs
unchanged as the regression proof for the shared availability helpers. No automatic global model
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

## Draft handoff — 2026-10-18, Q-12 and Q-13 redraft

Baseline `4d11136`, branch `explore/research-swarm`, drafted by an Opus 5.5
sub-agent with Stage 2 off for this redraft (no foreign model call). Q-13 was
recorded first (`99e3ed2`). The spec gains criteria 43–58 and amends 6, 11,
17, 20–22, 24 and 37–42. The design adds the preparation and state-store
interfaces, the plan steps 11–12 and the appetite fit, and the ADR 0020 draft
follows. Read for it: #157's availability module, its endpoint block and its
tests at `0c03ec0` (read-only `git show`); this branch's catalog selection,
dispatcher, snapshot and `record_dir`. Not read: live catalogs, any
credential file, the tracker. No `[DECISION]` remains; the mechanism choices
are spec `[DETAIL]`s. Addendum, same day: Q-14 (`620c89e`) replaces the
fixed fallbacks with a live substitute pool (criteria 59–61; 11, 38, 40,
43–49 amended) and raises the appetite to 17 h 20 min.

## Draft handoff — 2026-10-17, fifth phase-2a incorporation

Baseline `769b1b8`, branch `explore/research-swarm`. Incorporated recorded
rulings S-47–S-52 into spec, design and this plan: structural Markdown and
canonical structured-data resolution, all-citation claim validity, Pi catalog
fault boundaries, evidence-backed neighbour status and explicit fallback
preflight. Findings retain their original text; only the six Status and
repair-location cells change. ADR 0020 and decisions.md remain unchanged.
The runner's pre-existing draft audit line remains. The 42 criterion numbers,
bases, architectural class, card, 12-hour appetite and empty Time used remain.
These are proposed artifacts, not implemented behavior or runtime evidence.

Artifact checks passed on 2026-10-17 against that baseline:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_interview_minimums.py --change research-swarm
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_criterion_ledger.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_frontmatter_current.py
git diff --check
```

Structural checks confirmed all 42 criterion/refutation/basis triples, fixed
class/appetite/card, one ledger, empty Time used, unchanged earlier findings
and four changed paths inside this change folder. ADR 0020 remains the sole
added ADR relative to local origin/main; no new ADR is due for these details.
The artifact-validator script is absent. The tracker-backed registry, hosted
PR state and current cross-checkout session ownership were not read. No
runtime tests, full verifier, provider call, tracker access, commit or git
mutation occurred; earlier runner-reported red checks remain historical,
not a green implementation verdict. The runner owns verification, generated
files and the commit. Phase-6 F-1 remains open for attended real-Pi isolation
capture before merge.

Resume phase 4 by establishing the historical unmeasured time span or raising
the appetite stop; then repair the pinned-wrapper fixture seam and implement
this plan within the measured remainder. No phase-4 work starts in this draft.

## Draft retry — 2026-10-17, fifth phase-2a incorporation

Rechecked the retained draft at `769b1b8` against the recorded S-47–S-52
rulings. Criteria 23 and 38 now open with When instead of Before, retaining
the same prerequisites before dispatch, refutations and bases. No requirement,
criterion number, class, human answer, appetite or ADR claim changes in this
retry. The sole added ADR relative to the local
`origin/main` reference remains ADR 0020; this round requires no second draft.

The supplied runner diagnostics report 46 failing swarm tests in attempt 1:
the fixture does not intercept the absolute pinned Pi wrapper, which then
fails under its restricted PATH. Source inspection confirms that
`sworld` lacks the `PI_WRAPPER` injection used by `tests/test_stage2.py`.
Build steps 1–2 already own that repair and the remaining bare-Pi launches.
This artifact-only retry cannot change those files or qualify the runtime.

On 2026-10-17, the interview-minimums, criterion-ledger and
frontmatter-current commands listed above passed again, as did
`git diff --check`. No runtime test or full verifier was rerun; the supplied
red result is not superseded. The runner still owns full verification,
derived files and the commit. Time used stays empty until phase 4; the
historical-time stop and attended isolation capture remain required.

## Draft handoff — 2026-10-17, fourth phase-2a incorporation

Baseline `a68bbd0`, branch `explore/research-swarm`. Incorporated the recorded
rulings on neighbour status, structured answers, exact evidence resolution,
spec path forms, catalog identities, empty topic 5 and independent packet
checks (S-40–S-46). Spec, design, plan and the sole new ADR 0020 agree;
findings statuses locate each repair in the spec. Original findings text,
all human answers and earlier rulings remain unchanged. The 42 criterion
numbers, architectural class, card, 12-hour stop and empty Time used remain.
These are proposed artifacts, not implemented or runtime-tested behavior.

The runner owns full verification, registry generation and the commit.
Hosted PR state and parallel-session ownership were not read under the
worktree-only restriction. Phase-6 F-1 remains open for the separate attended
real-Pi isolation capture. Resume phase 4 by establishing the historical
unmeasured time span or raising the appetite stop, then repair the pinned-Pi
fixture seam and implement this plan within the measured remainder.

Artifact checks passed on 2026-10-17 against baseline `a68bbd0`:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_interview_minimums.py --change research-swarm
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_criterion_ledger.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/check_frontmatter_current.py
git diff --check
```

Structural checks confirmed all 42 criterion/refutation/basis triples,
unchanged bases/answers/class/appetite/card, one ledger and empty Time used.
Only the seven round-4 finding statuses changed; their original text and all
other review rows, including open F-1, are preserved. The diff has exactly
five permitted paths and ADR 0020 remains the sole new ADR relative to local
origin/main. Required template sections, metadata and local links hold.
The named artifact-validator script is absent; the tracker-backed registry
and hosted PR state were not read. No runtime tests, full verifier, capture,
provider call, tracker access, commit or git mutation occurred in this draft.

## Draft retry — 2026-10-17, fourth phase-2a incorporation

Attempt 1's runner post-check remains red: the supplied diagnostics report
46 failed, 2,254 passed and 16 skipped tests, plus Markdown diagnostics.
These are runner-reported results, not a test run by this retry. The seven
round-4 spec repairs remain proposed; a green artifact check is not a green
implementation verdict.

The reported Pi failure matches the read source at baseline `a68bbd0`:
`tests/test_stage2_swarm.py::sworld` supplies a PATH `pi` stand-in but never
injects `stage2.PI_WRAPPER`. The production version check therefore reaches
`tools/pi/pi` under the fixture's restricted PATH, where `dirname` is absent.
The existing `tests/test_stage2.py::world` explicitly injects a distinct
`pin-pi` stand-in. The swarm also still launches bare `pi` in
`scripts/stage2_swarm.py::free_transport`. Build steps 1–2 already require
repairing both seams and trapping bypasses; adding shell utilities or
disabling the production pin would not verify that contract.

This draft-only retry cannot repair those code/test paths. It retains the
failure and the existing phase-4 repair plan, without changing criteria,
decisions, gate definitions or tests to manufacture a green check. The
reported Markdown tail names templates and tool documentation outside this
draft's write scope; the omitted diagnostics were not read and are not
claimed to be unrelated. No full-verifier success is claimed. The runner
still owns registry generation, full verification and the commit.

Rechecked on 2026-10-17: interview minimums, criterion ledger, current
frontmatter and `git diff --check` all pass. The named
`scripts/validate_change_artefacts.py` is absent. The tracker-backed registry,
hosted PR state and other checkouts were not read. Phase-6 F-1, the attended
real-Pi isolation capture, remains open. No phase-4 time is added, and the
Time used section stays empty.

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

## How to run the F-1 capture

Tool: `scripts/research_capture.py` (built 2026-10-19, bead coding-harness-icw; tests `tests/test_research_capture.py`). It is the attended offline capture of step 6 and finding F-1. The real pinned Pi has not been started by it yet; only the stand-in dry run (`--dry-run-stand-in`) has run.

Command, from this change's worktree, with the maintainer present (the tool refuses without `--attended`):

```bash
.venv/bin/python scripts/research_capture.py --attended \
  --scratch "$TMPDIR/f1-capture-$(date -u +%Y%m%dT%H%M%SZ)" \
  --out "$TMPDIR/f1-capture-report"
```

Optional: add `--os-sandbox` on macOS to wrap every command in `sandbox-exec` (outbound network denied except localhost; not self-tested).

- Duration: not measured with the real Pi. Expect a few minutes: one catalog helper run, five seat processes (online, two dynamically selected Go free seats, repository) and one probe, each limited to 300 seconds (`--timeout`).
- What the tool does: builds a scratch repository, HOME and `XDG_STATE_HOME` with synthetic canaries; starts a loopback mock server; runs the real catalog helper and `select_research_catalog` against it; starts the seats through the swarm's own `Run.pi_command` and the probe through `probe_go`, all via `stage2.PI_WRAPPER`; writes `<out>.json` and `<out>.md`.
- What the maintainer watches: the terminal for an unexpected process; the printed verdict lines (criteria 8, 9, 47, repository seat, state-store guard; exit 0 = all PASS, 1 = a FAIL, 2 = refused or unusable); and, before pasting anything, the Markdown report's "Not enforced" list. Name resolution, native subprocesses and other processes are not blocked; the Node network guard denies non-loopback connections of Pi itself.
- Afterwards: the orchestrator copies the Markdown report into `research.md` (version and source hashes, method, outbound payloads, tool schemas, attempts, receipts, canary outcomes) with the tested commit and the exact command, then asks for the fresh phase-6 re-check. F-1 is closed by the maintainer's ruling, not by the tool.
- A FAIL is a finding, not a tool fault: do not edit the verdict logic to turn it green. A `repository-seat` OBSERVED line (an absolute-path read outside the worktree succeeded) is reported, not judged: criteria 8, 9 and 47 concern free contexts and the probe.

## Earlier implementation time

Historical phase-4 entries remain below. The maintainer answered the
unmeasured-time stop on 2026-10-17 with continue and a new total of 13 hours
20 minutes, recorded under Time used. The old span stays named and is not
counted; it is not measured zero. Count retained measured history and each
new phase-4 span against that current total, without counting phases 2/3 or
time between sessions. The three recorded historical entries total about
78 minutes (as recorded on 2026-10-16 at 42e5975). Their dated evidence is
preserved verbatim. Any new unbounded implementation span raises a new stop.

2026-10-15 repair attempt 3, span not measured: this session had no command tool to read `date`.
2026-10-15 completion (Opus 5.5): 05:15–05:31 CEST, about 16 minutes including one `make verify` run (05:20:38–05:30:25, green: 2038 passed, 16 skipped).

2026-10-15 05:49:28–06:00:30 CEST, 11 minutes 2 seconds (Codex repair of L1-1–L1-8; no break).

2026-10-15 09:40–10:31 CEST, about 51 minutes (Opus 5.5 sub-agent repair of phase-6 F-2 to F-10 outside `stage2.py repair`, maintainer-approved; four `make verify` runs of about 8–10 minutes each, the first red on formatting and a stale `updated:`; no break).

The earlier plan cited `docs/journal/handover/2026-10-15-research-swarm-loop-one-repair.md`; that file is not present in this worktree and was not read by this redraft.

## Time used

2026-10-17, appetite stop answered: the span of the three implement attempts of 2026-10-15 (ended 04:53:50, `cf848ee`) has no start record, so time used was not measurable (78 minutes measured). Maintainer, 2026-10-17: "Ja, halt die zeitgrenze fest" — **continue** with a new appetite of 13 hours 20 minutes in total (the measured 78 minutes plus 12 hours); the unmeasured span stays named, not counted. This replaces the card's `Appetite:` line.


### Initial pinned-wrapper checkpoint — 2026-10-17

Codex took over the previous Claude tasks at the maintainer's request.
The sworld fixture now injects a separately named pinned-wrapper double
and traps bare Pi. Inventory, public and repository launches all use
runner.PI_WRAPPER. The regression checks infrastructure and model paths;
existing timeout/environment interceptors follow that same path. The
append-only check permits only the required updated-date restamp.

Red-first evidence: the first class-routing test failed on the original
fixture; after injecting the pin it still failed at the bare inventory
launch, before the production fix. The nine affected cases then passed.
Full make verify passed on 2026-10-17: 2301 passed, 16 skipped; every
blocking local gate green. The final command used process-local
GIT_CONFIG_COUNT=1, GIT_CONFIG_KEY_0=commit.gpgsign and
GIT_CONFIG_VALUE_0=false, with local test servers permitted. Earlier
runs hit sandbox socket restrictions and inherited SSH-signing setup
errors; the affected Git fixtures passed separately (13 and 5 tests).
No global Git setting was changed. Markdownlint remains report-only.

This checkpoint repairs the initial fixture/pin seam. The amended
39 + 3N graph, its new catalog and handoff checks, and the attended
F-1 capture remain unfinished. No criterion-ledger entry is promoted
from not-yet-written by this checkpoint.

2026-10-17 10:33:55–11:12:32 UTC, 0:38:37, break counted
(requested availability instructions and research delegation during
verification). Add this measured span to the historical measured time;
the total appetite remains 13 hours 20 minutes.


### Night implementation order — 2026-10-17

[DETAIL] The first amended slice builds the catalog boundary and immutable
planned-seat description, tested through the real pinned Pi against local
catalog/metadata servers. Node owns only the Pi runtime bridge and the shared
fetch deadline; Python validates duplicate identities, policy, capability
intersection and the planned graph. It does not dispatch models. This keeps
raw response evidence available to Python's duplicate-aware JSON reader and
keeps selection policy in the existing Python runner. The later scheduler
must consume the checked graph; passing preflight/graph tests alone never
proves the actual 39 + 3N dispatch, barriers, isolation or handoff complete.
Keep the old end-to-end tests until the dispatcher is replaced, and leave
pending integration ledger entries pending. No live provider qualification
or change to fixed role identities is part of this slice.


### Fresh-catalog foundation — 2026-10-17

Measured phase-4 span: 21:15:16–21:40:12 UTC, 24 minutes
56 seconds, including implementation, local contract checks and the
full verification wait. Baseline e9ec953. Add this to the retained measured
history and earlier 38 minutes 37 seconds; the total appetite stays 13 hours
20 minutes. The old named unmeasured span remains excluded by the recorded
maintainer continuation, not measured zero.

Implemented standalone catalog selection and a planned 39 + 3N seat graph.
The real pinned Pi management runtime is exercised against local HTTP
fixtures; it uses an in-memory catalog-only sentinel to enter its configured
refresh branch without a credential file or an authenticated request. Both
public reads share one deadline; raw bodies retain duplicate-key evidence.
Python distinguishes hard Pi/fixed-model failure, capability-unavailable,
candidate-local exclusion, explicit-include failure and measured-empty.
No model is invoked. The legacy dispatcher remains unchanged; none of this
claims the amended graph, runtime barriers or handoff complete.

Evidence at the staged source checkpoint: initial missing-API tests 9 failed;
first working catalog set 43 passed; expanded set 56 passed in 20.60 seconds;
earlier combined catalog/legacy-swarm check 122 passed in 123.48 seconds.
Full make verify GREEN: 2357 passed, 16 skipped in 756.26 seconds, followed by
all blocking gates green. Process-local commit.gpgsign=false and local test
servers were enabled. A separately launched kit probe without that signing
override failed 17 Git fixtures; the complete correctly configured run
passed its kit gate. Documentation/Markdown findings remain report-only.
Ruff check/format, Node syntax, frontmatter and criterion ledger passed.

Next: add the narrow counterexample for duplicate keys belonging to an
unrelated metadata provider, then scope identity ambiguity checks accordingly;
implement and test the structural frozen-source resolver. These are pending,
not qualified by this checkpoint. No GLM/Claude model call or live provider
qualification ran. Attended F-1 capture remains open; PR #158 stays draft.


### Structural-reference foundation order — 2026-10-17

[DETAIL] Put the new pure frozen-byte resolver in stage2_research_refs.py,
separate from model transport and scheduling. It parses the selected file
type, returns complete extents, and assembles claim excerpts only after
every citation resolves. This is a new responsibility, not the queued
general runner refactor. Its standalone tests and historical S-47 fixture
are framework content. The later amended map/report validator must consume
this helper; the legacy substring citation path remains until that
dispatcher/report replacement. Keep those integration ledger rows pending.
No standalone result proves the full research evidence/handoff pipeline.


### Finder-map protocol and intermediate verification — 2026-10-17

[DETAIL] The pure stage2_research_map.py helper consumes four JSON lists
(code, rules, tests, neighbours). A finder locator has exactly path,
reference and reason. A merge locator has path, reference and origins,
each origin holding finder and reason. An unread marker is a singleton
object with not_read: a reason in finder output, the exact originating
finder/reason list in merge output. Empty lists are invalid; locators and
unread markers may coexist to retain partial coverage. Raw JSON uses
duplicate-key and non-finite-value refusal. The caller supplies the trusted
three finder identities. The runner validates the exact locator/unread
union, then resolves frozen references and independently inserts given
neighbours. It returns scope, extents/digests, neighbour membership,
comparison gaps and source unread reasons, never whole source snapshots.
The amended scheduler and prompts must consume this protocol later.

The first full check of the reference slice was RED: 2414 passed, 16
skipped, two CI registration tests failed in 745.38 seconds. The helper
needed a documented non-CLI caller and a direct test import detectable by
the existing AST-based check. Those registrations/imports are fixed; all
five relevant CI ratchet tests pass. A progress message briefly claimed the
suite green from its transition into later gates; this was corrected
immediately after inspecting the actual result. No source checkpoint was
published from that red run. Six additional red-first Python assignment
cases fixed attribute/subscript false definitions, augmented rebinding
and type-alias extents. The finder-map fixture schema now preserves the
required unread markers and origins, with red-first loss/change cases.

Go catalog origin/provider checks are candidate-local: a malformed free
definition is excluded as pi-malformed with raw field evidence, while a
malformed required fixed definition fails preflight. No catalog field
authorizes a different endpoint. Store definitions remain retrieval
evidence; later Pi config activation must retain literal header values
as established by the implementation-review safety repair, not interpret
retrieval metadata as executable configuration. Actual amended dispatch,
frozen snapshot/history construction, model isolation qualification and
handoff remain pending. Keep integration ledger rows pending.


### Boundary foundations verified — 2026-10-18 Europe/Berlin

Measured phase-4 interval: 2026-10-17 21:41:24–22:22:15 UTC,
40 minutes 51 seconds, including the intermediate red full run,
all repairs, preparation of the next history slice and the final full
verification wait. Count this once after the earlier 24m56s, 38m37s and
retained measured history. Total appetite remains 13h20m; the named older
unmeasured span is preserved and excluded by the maintainer's continuation.

Implemented and tested standalone typed frozen references, exact finder
union with unread provenance and neighbour derivation, scoped metadata
ambiguity/raw-value evidence, and declared Go origin/provider binding.
The helpers perform no model call. Actual amended dispatch, frozen-copy/
history construction, prompt replacement, report/judge/handoff integration
and attended isolation capture remain unfinished; PR #158 stays draft.

Red-first evidence: six Python assignment counterexamples; 34 initially
missing map cases; four ingestion/schema failures beside two passing
duplicate guards; four invalid own-context cases; twelve failures when the
required unread-marker schema was introduced; five origin/provider
counterexamples. Final focused boundary set: 175 passed in 22.83 seconds.
The five caller/test-registration ratchet checks pass. Full make verify
GREEN: 2476 passed, 16 skipped in 749.26 seconds, then every blocking gate
green. Ruff checks/format (76 files), generated-CI check, frontmatter and
criterion ledger passed; documentation/Markdown findings remain report-only.
Source stayed fixed throughout the final verification. Process-local
commit.gpgsign=false and local loopback servers were enabled. No GLM/Claude
call, live provider qualification, credential-file read or merge occurred.

Next prepared, not implemented: a bounded local frozen-HEAD history helper
and disposable-Git fixtures, drafted outside the repository during the
verification wait. Its preparation time is already included in this span.
It must first get red tests in this worktree, caller/test registration and
full qualification before any completion claim. Git's official environment
and pretty-format references were checked on 2026-10-18 local:
https://git-scm.com/docs/git and https://git-scm.com/docs/pretty-formats.
The measured local Git version is 2.56.0. The intended history policy is
local-only, literal mapped paths, frozen full commit identity, at most ten
records per path, author UTC, body cap 4000 Unicode characters, no retry and
the run's shared monotonic deadline. No history implementation was qualified
by the preceding boundary test result.


### Bounded local history verified — 2026-10-18

Measured phase-4 span: 09:27:02–09:46:10 UTC, 19 minutes 8 seconds,
including red-first implementation, full verification waits and preparation
of the next frozen-copy prototype outside the repository. Count this once
after the retained history and earlier spans; the approved total stays
13h20m. Preparation of that next prototype must not be counted again.

Implemented standalone stage2_research_history.py. It binds records to a
full frozen commit identity and literal mapped paths, retains ten commits
per path, deduplicates shared records, normalizes author UTC and caps bodies
at 4000 Unicode characters with explicit truncation. An eleventh identity
marks unread older history without retaining its body. Shallow repositories
never certify complete or measured-empty history. All Git commands share
the caller's finite monotonic deadline; ambient repository/auth/config
overrides, replacement objects, transports and lazy fetch are disabled.
Missing objects/timeouts fail preparation without a retry. The amended
topic dispatcher still needs to consume this packet; its integration
ledger entries remain pending. No existing test was changed.

Red-first evidence: 18 missing-module failures, followed by 18 passes;
six added assertion failures exposed invalid/unbounded deadlines and the
repository-wide dot path. After repair, history plus CI contracts passed
106 tests with 2 skipped. Full make verify GREEN: 2505 passed, 16 skipped
in 895.87 seconds, then every blocking gate green, including the kit probe.
Ruff check/format, generated CI and criterion ledger passed. Process-local
commit.gpgsign=false and local test servers were enabled. Source bytes
stayed fixed during full verification. Documentation/Markdown findings
remain report-only. No credential file, tracker history, live provider,
GLM/Claude call or customer instance was read/called; no merge occurred.

Next prepared, not yet implemented in the repository: a transient frozen
input-state helper and disposable-Git fixtures. Its separate temporary
prototype passed 23 tests; this is not repository integration or full
qualification. It must get red tests here before source adoption. Actual
amended scheduling, prompts, reports/judge/handoff, attended F-1 capture
and fresh phase-6 review remain unfinished; PR #158 stays draft.


### Transient frozen inputs verified — 2026-10-18

Measured phase-4 span: 09:48:20–10:07:29 UTC, 19 minutes 9 seconds,
including adoption, focused/full verification waits and preparation of the
next report-validator/prompt prototype outside the repository. Count this
once after the retained earlier intervals and 19m08s history span; approved
total stays 13h20m. Do not count report-prototype preparation again.

Implemented standalone stage2_research_snapshot.py and disposable-Git
contracts. Copies remain in an owner-only temporary directory outside the
repository and are deleted after context exit or failed preparation. The
snapshot retains current tracked bytes plus non-ignored untracked change
inputs, full and per-path digests, and exact tracked/untracked inventory.
Changed path sets, working bytes or HEAD invalidate publication. A research
append/restamp is exempt only for the exact runner-owned expected bytes,
preserving the frozen body; arbitrary matching-prefix foreign appends are
not accepted. File and parent symlinks refuse rather than read ambient
sources. Git inventory shares the history helper's local-only transport.
The dispatcher must still own and consume this context; no complete amended
run, publication or handoff is qualified by the standalone API.

Red-first evidence: 23 missing-module failures in this repository before
source adoption. Final focused snapshot/history contracts: 52 passed in
4.57 seconds; six relevant CI registration checks pass. An intermediate
focused combination had one missing non-CLI registration (128 passed,
2 skipped), repaired by restoring a documented library reason. No gate
was weakened. The parent-directory symlink fixture was strengthened before
the complete run; existing tests were not changed. Complete make verify
GREEN: 2528 passed, 16 skipped in 867.97 seconds, then every blocking gate
including kit green. Ruff check/format, criterion ledger and generated CI
passed. Source bytes remained fixed throughout full verification. Process-
local commit.gpgsign=false and loopback test servers were enabled;
documentation/Markdown findings remain report-only.

Prepared next, not yet adopted here: structured report/evidence validation
and a common report template. The separate temporary prototype passed
41 tests after one escaped-JSON Unicode counterexample went red and was
fixed. It keeps unsupported claims/questions, separates local/history/page
evidence, applies the shared excerpt cap and topic-specific field contracts.
Repository red tests and full qualification are still required. Actual
amended scheduling/prompts/report integration, judge/handoff, attended F-1
capture and fresh phase-6 review remain unfinished. No GLM/Claude/live
provider call, credential-file read, customer access or merge occurred.


### Structured report foundation order — 2026-10-18

[DETAIL] Use one closed JSON object per topic report, documented in the new
common report prompt. Claims hold local C1–C7 ids, statement, kind, evidence
citation strings, confidence and basis text. Counter-evidence/unread entries
are string lists; neighbour_relation is text, exactly not-assessable online.
Questions keep literal bracketed classifications and nonempty unique local
claim links, including unsupported claims. Topic 3/5/6 use the spec's exact
assessment, relations and volatility/governance additions. Empty-neighbour
topic 5 has the exact unread marker no packet neighbour and can waive only
the evidence floor, not malformed syntax or links.

Keep raw report text/data distinct from runner-resolved global claims and
questions. Separately percent-encode endpoint and model components and join
with one colon for a collision-free endpoint-qualified seat. The runner
alone supplies the namespace and validity. Resolve every citation before
attaching any excerpt; one invalid reference removes every excerpt from
the claim. Public evidence uses only that seat's successful fetch receipts,
whose actual extension field is retrieved, never search receipts or peer
data. Frozen local references and topic-6 packet records remain separate.
This pure validator does not call a model or a judge and does not activate
the amended dispatcher; retain its integration rows as pending.


### Structured reports verified — 2026-10-18

Measured phase-4 span: 10:09:20–10:26:05 UTC, 16 minutes 45 seconds,
including adoption, red counterexamples, full verification waits, official
capacity-document reading and temporary judge-packet/score preparation.
Count this once after retained earlier spans under unchanged 13h20m total.
Do not count that prototype preparation again.

Implemented pure report validation and the common report prompt. Exact
closed JSON, local C/Q links, topic-specific fields, raw decision retention,
endpoint-qualified encoded namespaces and runner-only evidence status are
checked. Local frozen references, topic-6 packet hashes and a seat's own
successful public fetch receipts are distinct evidence boundaries. One
unresolved citation removes all excerpts from that claim without dropping
its question; valid excerpts share one 4000-character budget. Required
evidence floors retain the exact empty-neighbour exception. No existing
test was changed and the legacy dispatcher/parser remains active.

Red first: 41 repository failures before adopting source/template; four
additional failures exposed unqualified/ambiguous endpoint/model identities
and missing reserved-character encoding. A separate escaped-JSON Unicode
case failed during prototype preparation before its fix was adopted. Final
report/CI contracts: 123 passed, 2 skipped in 13.88 seconds. Complete make
verify GREEN: 2574 passed, 16 skipped in 711.84 seconds, then every blocking
gate including kit green. Source stayed fixed during full verification.
Process-local signing override and loopback test servers were enabled;
documentation/Markdown findings remain report-only.

The separate next judge-packet/score prototype passed 23 tests after three
empty/malformed-outcome regressions went red and were fixed. This is not
repository adoption, complete reconciliation or runtime qualification.
Record the newly read official capacity evidence under docs/research before
enabling any derived limit. A local-only temporary reproducer also found
that i18n.logOutputEncoding=ISO-8859-1 makes otherwise valid non-ASCII commit
metadata fail the history API with UnicodeDecodeError. It fails closed;
it is not silently accepted. Next write a regression and explicitly request
UTF-8 output at the shared Git transport, then qualify it with the next
slice. The reproducer is /tmp/coding-harness-research-history-encoding-check.py.
Amended scheduling/role prompts, full judge/handoff integration, attended
F-1 capture and fresh phase-6 review remain unfinished. No live provider,
GLM/Claude call, credential-file read, customer access or merge occurred.


### Judge packet and score foundation order — 2026-10-18

[DETAIL] The next phase-4 interval begins at 10:26:05 UTC, immediately after
the preceding interval, and includes intermediate checkpoint publication
and subsequent preparation without an uncounted gap. The pure judge helper
counts its complete rendered instructions/data packet against one fixed
documented-capacity-derived limit and preserves all supplied reports and
outcomes even when refused. It does not prove complete graph membership;
the amended dispatcher must independently check the expected 39 + 3N slots.
Empty/free-only outcome sets and malformed identities cannot certify a
permitted packet. A declared successful topic must have its validated report.

Outcome refused means a declaration/leak barrier refusal and always carries
security exit 2, including optional seats and alongside ordinary failure.
A provider refusal is a failed contribution, not that security outcome.
Required topic failure and oversize packets carry exit 1; free contribution
failure alone does not block preparation. Independently derive per-topic/
endpoint/model score counts and ids from exactly one disposition per valid
claim; unsupported has no judgement and unique is a supported subset.
No composite ranking, semantic verdict or completed reconciliation is added.

Persist dated primary capacity evidence in docs/research before relying on
the derived bound. Explicitly label four tokens per character and 72,000
transport tokens as agent estimates, and account/actual capacity as not
measured. Client/fallback/isolation qualification remains a later integration
duty. Repair the red local display-encoding regression with a process-local
UTF-8 Git output override, without changing user/repository Git config.


### Judge packet and score foundation verified — 2026-10-18

Measured phase-4 span: 10:26:05–10:51:02 UTC, 24 minutes 57 seconds.
Count once after the preceding retained intervals under unchanged 13h20m
appetite. Includes intermediate publication, preparation and full verification
waits. The maintainer now requests stopping and handing over; no new slice
starts. Subsequent source/handover publication is session closure.

Implemented the pure complete-packet bound and exclusive per-seat score
foundation, not judge dispatch or semantic reconciliation. Dated official
capacity evidence and explicit agent estimates derive J = 200,000 Unicode
characters; account/client capacity remains unmeasured. Security refusal has
exit 2 precedence over ordinary incomplete outcomes. Empty/free-only sets
cannot certify preparation; exact graph completeness remains the dispatcher's
duty. The Git boundary now requests UTF-8 independently of local display
encoding without changing repository/user configuration.

Red evidence: 23 repository missing-module assertions before adoption, then
the security-precedence assertion; three prior prototype regressions covered
empty/malformed outcomes. Two added encoding cases exposed an ISO-8859-1
failure before the UTF-8 repair. A JSON substring fixture assertion was
corrected to decode JSON, not a production defect. Focused history/snapshot/
judge set: 78 passed; six CI registration checks passed. Complete make verify
GREEN: 2600 passed, 16 skipped in 923.35 seconds; every blocking gate,
including kit, green and process exit 0. Source bytes stayed fixed during
full verification; only this accounting record is appended afterward.
Documentation/Markdown findings remain report-only. No prior test was
removed or weakened. Later frontmatter/criterion/whitespace checks qualify
this accounting update; no broad code rerun is needed.

The later session notification reports coding-harness-e7 waiting in the main
checkout. Stay in owned worktrees; no further shared tracker write is made.
The bounded research-swarm task remains in progress (coding-harness-icw),
with no new issue or closure. Earlier tracker checkpoint comments were
already pushed. Actual amended runtime, role prompts, complete judge/handoff,
attended F-1 capture and fresh independent phase-6 review remain unfinished;
PR #158 stays draft. No model call, credential-file read, customer-instance
access, stash, amend, force push or merge occurred.


### Cancellable dispatcher foundation verified — 2026-10-18

Measured phase-4 span: 11:44:49–12:01:25 UTC, 16 minutes 36 seconds. Count
once after the preceding retained intervals under the unchanged 13h20m
appetite. Includes the full verification wait.

Implemented a standalone cancellable dispatcher (`scripts/stage2_research_dispatch.py`),
not yet wired into `stage2_swarm.run`: provider-wide queues of four shared across
roles and topics, required-first order, gate and audit serialized under one lock
immediately before launch with stop/deadline checked before and after gating,
the judge reserve with a child allowance of the lesser of role limit and
remaining time, security refusal that cancels queued slots and terminates and
reaps running process groups while keeping partial output as cancelled, exit
precedence 2 over 1 over 0, one terminal outcome and one identity per slot,
no retries. Criterion-ledger rows 12, 13, 19 and 36 stay pending: they name
wired-runner tests in `tests/test_stage2_swarm.py`.

Red evidence: 18 of 18 new tests failed on the missing module before the
implementation; all 18 then passed with no test weakened or changed in meaning
(afterwards only lint renames of unused arguments). Focused: 18 passed in about
3.4 seconds; `tests/test_ci.py` 95 passed, 2 skipped with the new registration.
Complete make verify GREEN: 2618 passed, 16 skipped in 709.20 seconds, every
gate green, process exit 0. Documentation/Markdown findings remain report-only.


### Dispatcher robustness repair — 2026-10-18

Measured phase-4 span: 12:02:48–12:19:57 UTC, 17 minutes 9 seconds, counted
once after the preceding intervals. Orchestrator review found two defects in
the dispatcher foundation, repaired red-first. An audit-writer failure now
refuses the call fail-closed (not launched, outcome refused, security stop,
exit 2); an unexpected supervision error reaps the child, keeps partial output,
ends the slot failed with started true, and the worker continues; a final guard
gives any slot a terminal outcome so the dispatcher never raises KeyError.
Reaping signals the child's own process group only when it leads one and falls
back to signalling the child itself, with bounded waits after SIGKILL.

Red evidence: of four new tests, three failed with KeyError on the lost slot
(audit failure, supervision error, worker-killing exception) and the
no-new-session test failed an assertion; all then passed. Focused: 22 dispatcher
tests passed, 99 passed with the CI registration tests (2 skipped). Complete
make verify GREEN: 2622 passed, 16 skipped in 811.40 seconds, every gate green,
exit 0. No test was weakened.


### Appetite raised — 2026-10-18

Maintainer, 2026-10-18: "erhöhe das zeizbudget" (Q-14), after being shown
the 3 to 4 hour shortfall under «Appetite fit — 2026-10-18» and the
recommendation of 17 hours 20 minutes. New total appetite: **17 hours 20
minutes** of phase 4. All measured spans above still count (4 h 56 min 10 s
by this date). The unmeasured 2026-10-15 repair-attempt-3 span stays named
and is not counted. This replaces the card's `Appetite:` line of 2026-10-17.

### Seat selection verified — 2026-10-18

Span 2026-10-18 15:35:08Z–16:34:30Z, about 59 min (measured with `date -u`;
no break), counted against the 17 h 20 min appetite. Plan step 11 only.

- Red first: the new tests were written before any source. Result: 1
  collection error (`tests/test_stage2_research_availability.py`,
  `ModuleNotFoundError: stage2_availability`, so its 44 tests did not run) and
  16 failures in `test_model_endpoints.py` (2), `test_stage2_research_catalog.py`
  (12, unknown `models` outcome key and the old hard failure on a fixed id) and
  `test_stage2.py` (3, `prepare-explore` unknown and `--class` beside
  `--stage2-off` still accepted).
- Green: availability file 44 passed; catalog 74 passed; model endpoints 60
  passed; the two new `test_stage2.py` tests passed; `test_stage2_swarm.py`
  247 passed together with the first three files. Baseline of the four large
  files before the change: 769 passed.
- Full `make verify` (process-local `commit.gpgsign=false`): first run red on
  one blocking gate (kit probe: the two new `test_model_endpoints.py` tests
  need the runner, which the kit does not carry; fixed with `importorskip`).
  Second run at `e386d25`: 2679 passed, 16 skipped in 15 min 1 s; ruff clean;
  `VERIFY GREEN`, exit 0.
- [DETAIL] #157 is not on `origin/main`: `scripts/stage2_availability.py` is
  written to its contract (`terms_problem`, `request_value`, `ordered_models`
  live there, not in `stage2.py`). Whichever pull request merges second
  resolves the add/add conflict to one copy.
- [DETAIL] The old `research_swarm` keys stay beside the new seat keys,
  because the unwired old `run()` still reads them; steps 2-8 remove them.
  `explore` on a swarm class now requires a valid receipt; `sworld` stubs
  `consume_research` until the run consumes its selection.
- [DETAIL] No `modelle_terms` records were added to `model-endpoints.yaml`
  (they are the maintainer's data readings, held by #157). Until #157 merges,
  `prepare-explore` on the shipped declaration reports every Go seat model as
  unadmitted and stops with `seat-unavailable`.
- Not done in step 11: the ledger rows on the run itself (criteria 6, 11, 37,
  43 finders, 46 frozen-and-recorded) stay "not yet written"; they need the
  run wiring of steps 2-8. Docs/prompts (step 10) are untouched.

### Run wiring step 2 verified — 2026-10-18 (partial: sub-boundary)

Span (measured, `date -u`): 2026-10-18T21:31:06Z to 2026-10-18T21:52:03Z, about 21 min (including one full make verify of 13 min 14 s), counted against the 17 h 20 min appetite. Code commit `d9965ba`. Full make verify at `d9965ba`: 2859 passed, 16 skipped, VERIFY GREEN (markdownlint report-only as before).

- Scope done: plan step 1 for the identity and permission graph, and the
  per-invocation part of step 2. Not done (needs the new run of steps 3-8):
  removing the Zen transport, the fixed roster/focuses and the `opencode-free`
  endpoint, and the replacement of the old run's roster tests.
- Red first: five new test groups failed before any source (18 failed, 7
  passed in the selected set; `role_launches` and `invocation_problem` did not
  exist). The wrapper test was already green, since the `sworld` fixture
  already injects `stage2.PI_WRAPPER` (stand-in `pin-pi`) beside a failing bare
  `pi` on the restricted PATH; it was renamed to the ledger name and given the
  premise assertions (injected path is not the installed Pi, bare `pi` resolves
  to the trap and fires).
- Code: `stage2_swarm.invocation_problem` (role, endpoint, model, data class,
  frozen free selection) and `stage2_swarm.role_launches` (the whole launch
  set, nothing returned when one role is refused).
- [DETAIL] The role fixes the data class (private roles `framework`, online and
  online_free `public-web`) and the launcher (Go: pinned Pi, plan: Claude
  Code); an endpoint's own `darf_sehen` never widens a role. A `-free` model is
  permitted only for `online_free`, under the declared policy (provider, suffix,
  exclude wins, nonempty include narrows) and the run's frozen selection.
- [DETAIL] Opus roles (merge, author, judge) must be `claude-opus*` on
  `claude-code-plan`; a repository seat on that endpoint may be any declared
  model (the shipped seat is Haiku 5.5).
- [DETAIL] `role_launches` always validates the declared `online_free` policy,
  even at N=0, so a malformed policy is exit 2 before any model; the catalog
  and receipt paths already did so at preparation.
- [DETAIL] The step-11 catalog refresh (forced Go refresh, models.dev
  intersection, per-candidate outcomes) and the wrapper routing of version and
  model calls were already in place (steps 11 and earlier); nothing was redone.

## Main sync after #157 — 2026-10-18

- Span (measured, `date -u`): 2026-10-18T20:19:29Z to 2026-10-18T20:50:46Z,
  about 31 min, counted against the 17 h 20 min appetite. Merge commit
  `f179d9c`.
- Conflicts: `AGENTS.md` (Stage 2 paragraph: #157 loop text plus the ADR 0020
  class sentence), `scripts/ci_gates.py` (one `stage2_availability.py` entry
  naming both test files), `scripts/stage2.py` (module docstring; one shared
  `--availability-reported` flag, allowed for `explore` and `review-loop`),
  `tests/test_stage2.py` (both test blocks kept) and the add/add
  `scripts/stage2_availability.py` (one module: #157's `settings`, `binding`,
  `report`, `prepare`, `consume` beside the research entry points; research
  helpers renamed `research_binding` and `research_report`).
- Superseded [DETAIL] of step 11: `terms_problem`, `request_value` and
  `ordered_models` live in `stage2.py` (as on main), not in the availability
  module; research reaches them through the runner. The review loop now reuses
  `excluded_reason`, `seal`, `verify`, `write_receipt` and `PROBE_TEXT`.
- Two step-11 swarm tests adapted to the merged ladder: `modelle` is now a set,
  and `glm-5.3-flash` is declared, so the planted off-endpoint id is
  `undeclared-flash-9`. The GLM exclusion is unchanged.
- Evidence: focused set 1077 passed, 2 skipped, 2 failed (the two above, fixed;
  `test_stage2_swarm.py` then 70 passed); full `make verify` at `f179d9c`:
  VERIFY GREEN.

## Resumable store verified — 2026-10-18

Step 12 (Q-13): durable slot results and resume, built and verified.

- Span (measured, `date -u`): 2026-10-18T20:56:41Z to 2026-10-18T21:29:45Z (about 35 min, including one full make verify of 13 min 58 s), counted against
  the 17 h 20 min appetite. Commit `35cff56` (store, dispatcher hook, binding
  functions, tests, ledger rows); this section is the closing note.
- Red first: before any source existed, `tests/test_stage2_research_store.py`
  and the five new dispatch tests failed (17 failed, 21 errors from the
  fixture's missing module, 22 existing dispatch tests passed). Then green:
  focused set 294 passed, 2 skipped; full make verify at `35cff56`: 2841 passed, 16 skipped, VERIFY GREEN (markdownlint report-only, as before).
- Files: `scripts/stage2_research_store.py` (new; registered in
  `scripts/ci_gates.py`), `scripts/stage2_research_dispatch.py`
  (`on_terminal`, `DispatchResult.reason`/`detail`),
  `scripts/stage2_research_snapshot.py` (`stored_binding`,
  `changed_against_stored`).
- [DETAIL] Dispatcher stays free of storage knowledge: an exception from
  `on_terminal`, or from `audit` carrying a `stage_stop_reason` attribute, is
  a stage stop without a security refusal (exit 1, reason from the attribute,
  default `state-store-unwritable`). An `audit` exception without the attribute
  stays a security refusal (exit 2) as before. After the first store failure
  no further callback runs (the store is what failed); the failed slot's
  launch is cancelled, queued slots cancel, running children are stopped and
  reaped with partial output kept.
- [DETAIL] The binding keeps a second research digest, of the frozen bytes
  with the `updated:` line normalised (`research_normalised_sha256`), because
  the frozen per-path digest is of the raw bytes and the restamp changes them.
  The runner records the exact intended append (length and SHA-256) with
  `Store.set_append` before writing it; if the crash falls between the two,
  the comparison also accepts the unappended bytes.
- [DETAIL] The latest run is chosen by `started` time inside `run.json`. A run
  directory with an unreadable `run.json` fails closed (nothing is reused,
  named); a directory with no `run.json` at all (crash before the first
  write) is ignored. Older runs are never pruned by a resume (design: the
  latest run only); a complete publication calls `Store.clear`.
- [DETAIL] Slot ids become file names, so `Store` refuses ids outside
  `[A-Za-z0-9][A-Za-z0-9._+-]{0,119}`. A torn launch record still counts as a
  launch (the slot is listed as interrupted). The store takes an injected
  `scrub` callable; the runner passes its credential scrub. The scrub test
  skips where the runner is absent (kit probe).
- [DETAIL] `Store.assert_outside(*dirs)` is the placement check the runner
  calls with the worktree, its git directory and every model home/agent/working
  directory; the module cannot know those directories itself.
- Not done (later steps, ledger rows stay "not yet written"): the
  swarm-level tests (criteria 52 store-canary through the run, 53/54/55 on the
  run) need the run wiring of steps 2-8: calling `acquire_lock`, `resume_source`
  and `plan_reuse` after the freeze, `adopt` for reused slots, `finish_run`,
  `clear`, the manifest marks and the `39 + 3N` count. The probe-record and
  receipt part of criterion 21's row belongs to `stage2_availability.py`; the
  store test covers store records only.

### New run verified — 2026-10-18

Plan steps 3 (frozen packets, finder trio, map merge, sentence, topics, judge), the run-level fixtures of step 1, the store wiring of step 12 and the Zen removal of step 2. Not done: step 8's obligation inventory and neighbour-status items, step 9 (handoff gate), step 10 (docs and prompt prefixes beyond the run's own prompts), step 6 (real-Pi capture).

- Span (measured, `date -u`): 2026-10-18T21:53:11Z to 2026-10-18T23:25:20Z, 1 h 32 min 09 s, counted against the 17 h 20 min appetite. It includes three full `make verify` runs (about 15 to 16 min each).
- Commits: `bb9d556` (new run, prompts, tests), `e37b60f` (Zen removal), `c901f29` (ledger tests restored), `f80d262` (concurrency checks made load-proof). Full `make verify` at `f80d262`: 2901 passed, 16 skipped, VERIFY GREEN (markdownlint report-only, as before).
- Red first, with a stated limit: the new run module was drafted before its tests, so the recorded red is the absent module. `tests/test_stage2_swarm.py` failed to collect with `ModuleNotFoundError: stage2_research_run`; afterwards the first verify was red on the criterion-ledger gate (eight ledger entries named tests of the deleted old run), and the second on one load-dependent concurrency test. Each was repaired in its own round (two repair rounds in all, the limit).
- Counts: `tests/test_stage2_swarm.py` 138 tests (the old pair/Zen tests are replaced); 60 ledger rows converted from "not yet written" to their tests; 8 rows that named deleted tests now name rewritten ones; 61 "not yet written" rows remain (preparation catalog rows, step 8/9 handoff and inventory, step 10 doctrine, the refs/markdown rows covered by the pure-module tests).
- Wiring (step 12 open items): `acquire_lock` before the freeze, `resume_source` after it, `plan_reuse` per stage, `adopt` for reused slots, `set_append` before the one research append, `finish_run` and `clear` after publication; `Store.assert_outside` checks the worktree and its git directory.
- [DETAIL] The run id is the store's 128-bit run id; claims are namespaced by it, so a resumed run has new global claim ids and the judge packet (which holds the run id) is never reused.
- [DETAIL] `research.md` is appended once, by the runner, at the end or abort of the run (audit lines, reports, partial output, manifest). A SIGKILL leaves the file untouched, which is what the store's exact-tail binding needs; the audit trail of a killed run lives in the store's launch records.
- [DETAIL] The private brief holds the frozen `research.md` without earlier runner blocks (marked by `<!-- research-swarm/v2 run ... -->`) and without the `updated:` value, so a resumed run builds byte-identical prompts. The topic-6 history packet names the frozen HEAD, so a moved HEAD re-runs topic 6 only.
- [DETAIL] The judge answers one closed JSON object: `claim_judgements`, `supported_facts`, `assumptions`, `applicability`, `gaps`, `human_questions`, three comparison strings and `disagreements` (two or more known global claim ids and a summary each). No answer field is allowed. Validation reuses `research_claim_scores`.
- [DETAIL] Model JSON may arrive as the bare object or as one fenced block; the fence is stripped before validation.
- [DETAIL] The public sentence uses the S-26 allow-list (letters, whitespace, separators, internal hyphens and apostrophes, spaced dashes, one final period or question mark) plus the whole-token name list of the change, the bead and tracked path components.
- [DETAIL] Persistence is minimal: fenced `research-swarm/v2` blocks for manifest, map, history, each report, the reconciliation with scores and each failed slot's partial output. The runner-derived obligation inventory and H-items (step 8) are not written yet.
- [DETAIL] `model-endpoints.yaml` keeps `paid_endpoint`, `topic_author` and `judge`; `finder_merge` falls back to the judge model. `test_model_endpoints.py::swarm_block_problems` now checks those roles, the `public-web` class and that the removed keys stay gone.
- Open: step 8 inventory and neighbour statuses (ledger rows 29 to 31), step 9 and step 10, the real-Pi capture, and the preparation-level rows (`test_catalog_failure_stops_before_all_model_calls` and similar).

### Steps 8 and 9 verified — 2026-10-18

Plan step 8 (obligation inventory and neighbour statuses persisted) and step 9 (the `research-handoff` gate). Step 10 (docs, prompt prefixes, kit doctrine), step 6 (real-Pi capture) and the preparation-level catalog rows are not done.

- Span (measured, `date -u`): 2026-10-18T23:25:20Z (taken as the end of the previous span, because the first command of this slice was not timestamped; an upper bound) to 2026-10-18T23:57:37Z, 32 min 17 s, counted against the 17 h 20 min appetite. It includes one full `make verify` (2026-10-18T23:39:44Z to 23:57:25Z).
- Commits: `f00bf27` (step 8), `a72521c` (step 9). Full `make verify` at `a72521c`: 2926 passed, 16 skipped, VERIFY GREEN (markdownlint report-only, as before).
- Red first: for step 8 the new function `research_handoff.derive_inventory` was a stub returning an empty inventory; six tests failed on assertions (no neighbour records, no `decision` items, no persisted inventory block). For step 9 `check_research_handoff.main` was a stub returning 0; 17 tests were red (assertion failures, plus one `AttributeError` for the then-missing `parse_text`).
- Focused counts: `tests/test_stage2_swarm.py` 144 passed (six new); `tests/test_research_handoff.py` 17 passed; `tests/test_ci.py` and `tests/test_kit.py` one new test each.
- Ledger: 7 step-8 rows and 22 step-9 rows (including the `test_ci` and `test_kit` rows) converted from "not yet written"; 6 rows (judge excerpt cap, type-specific references, Markdown resolver, structured references, two neighbour-packet rows) repointed to the pure-module tests that already cover them; two new rows for the persisted inventory block. 27 "not yet written" rows remain (catalog and preparation rows, step 10 doctrine).
- [DETAIL] The derivation lives in `scripts/research_handoff.py` (standard library only), shared by the runner and the gate so the checker's independent derivation cannot drift; it takes no judge disposition. It travels with the gate (kit manifest) and is listed in `ci_gates.OHNE_AUFRUFER` as a library.
- [DETAIL] Items: `decision` (every accepted `[DECISION]` question, grouped by whitespace- and case-normalised text, all question and claim ids kept), `class` (one per differing assessed class), `disagreement` (judge disagreements, deduplicated by claim set), `neighbour` kinds `contradicts`, `unrelated-given` and `split`. Ids `H-<n>` follow a fixed order. The judge's free-text `human_questions` stay prose; only structured disagreements add items.
- [DETAIL] Cross-run neighbour items (a path confirmed in one complete run and rejected in another, a given path a later run omits) are derived by the gate only and belong to the later run under the id `<run>/X-<n>`; the runner never sees other runs.
- [DETAIL] The inventory block is written for every run that has a map and reports, complete or not; the gate ignores incomplete runs. A complete run without an inventory block, or whose block differs from the independent derivation, is a finding (exit 1); an unreadable or malformed block is exit 3.
- [DETAIL] A Q-record closes an item only when it is answered by the maintainer with a nonblank answer and a nonblank context; a criterion Basis naming a Q-record needs the answer and maintainer only. A link to an item or claim that no run holds, a repeated Q id carrying research links, a field twice and conflicting directives are exit 3.
- [DETAIL] Not done by design: steps 4, 5 and 7 needed no new run behaviour beyond step 3 (their open ledger rows were repointed, see above).
- Open: step 10, step 6 real-Pi capture, catalog and preparation ledger rows, a hosted-CI run of the new gate.

### Step 10 verified — 2026-10-19

Plan step 10 (doctrine, prompts, spec template; gate and kit text were carried by step 9). No review was requested; step 6 (real-Pi capture, finding F-1) stays open and the doctrine says so.

- Span (measured, `date -u`): 2026-10-18T23:59:07Z to about 2026-10-19T00:25Z including one full `make verify` (started 00:04:16Z, VERIFY GREEN, log in the scratchpad `step10-verify.log`), counted against the 17 h 20 min appetite. Commit `6750869`.
- Red first: the extended `test_amended_doctrine_and_research_roles_agree` and the verb-count check failed before any doc change.
- Ledger: row 22 converted; 19 "not yet written" lines remain (catalog and preparation rows, blocked on the catalog/preparation tests, not on step 10).
- [DETAIL] `prepare-explore` is a twelfth verb; the verb-count test now expects "Twelve verbs exist".
- [DETAIL] Kit manifest, `gates.yaml` and CI were already done in step 9; no `ci_gates.py` change was needed.
- [DETAIL] `research.md` needs a `neighbours:` header (`[]` allowed); a missing one refuses with exit 2.
- Open: step 6 (F-1), catalog/preparation ledger rows, hosted-CI run of the gate.

### Remaining ledger rows — 2026-10-19

The 19 criterion-ledger rows that still read "not yet written" (catalog and preparation rows) now name tests. No source code changed: every new test passed on its first run against the existing code, so all 19 rows are "already held" (the behaviour predates the test); none needed a fix. No row was skipped.

- Span (measured, `date -u`): 2026-10-19T07:40:04Z to 2026-10-19T08:18:00Z (upper bound; verify finished before 08:17:56Z), about 38 min, counted against the 17 h 20 min appetite. It includes one full `make verify` (started 07:47:10Z). Commit `b530ee5`; full `make verify` at that commit: VERIFY GREEN (markdownlint report-only, as before), log `ledger-rows-verify.log` in the scratchpad.
- Rows converted: 19 ledger lines, 15 distinct tests.
  - `tests/test_stage2_research_catalog.py` (11 tests, over the actual pinned wrapper and loopback servers): `test_each_run_forces_a_fresh_go_catalog`, `test_removed_shipped_free_ids_do_not_return`, `test_unmeasured_catalog_never_becomes_zero_availability` (seven faults), `test_free_eligibility_requires_text_chat_and_explicit_tools`, `test_models_dev_capabilities_intersect_only_fresh_pi_ids`, `test_models_dev_failure_excludes_free_and_keeps_required_slots` (six faults), `test_capability_document_faults_and_candidate_faults_are_distinct`, `test_catalog_shared_deadline_keeps_asymmetric_failure_rules`, `test_nonempty_selection_keeps_both_sources_and_exclusion_evidence`, `test_duplicate_raw_keys_or_claimed_ids_exclude_all_free_candidates`, `test_missing_metadata_id_excludes_only_that_candidate`.
  - `tests/test_stage2_swarm.py` (4 tests, through the real `prepare-explore` verb with the catalog helper replaced by a document of its shape): `test_catalog_failure_stops_before_all_model_calls`, `test_missing_explicit_include_stops_before_models`, `test_go_free_policy_filters_and_freezes_each_run`, `test_capability_unavailable_keeps_required_slots_unless_include_is_required`.
  - The ledger line of criterion 39 on the free-model role test also dropped its note that the run-level policy row was still unwritten.
- Red first, with a stated limit: the behaviour was already built, so no test was red against the code; each test was checked for a real assertion by reading what it pins, not by planting a fault.
- [DETAIL] A baseline-only or cache-only free id is not absent from the audit: it appears as a candidate with reason `not-in-fresh-pi` and is never selected. The tests pin that, not omission.
- [DETAIL] The preparation tests live in `test_stage2_swarm.py` as the ledger named them, and reuse the fixture of `test_stage2_research_availability.py` (imported, not copied).
- Open: step 6 (real-Pi capture, F-1), hosted-CI run of the handoff gate. Rows of criteria 6 and 37 still carry the note that their run-level part is identity-only.

### Phase-6 repairs — 2026-10-19

Hand repair of the phase-6 BLOCKER rows F-11 to F-18 (`stage2.py repair` refuses while F-1, the attended real-Pi capture, stays open). Row F-1 was not touched.

- Span (measured, `date -u`): 2026-10-19T08:22:32Z to 2026-10-19T09:02:41Z (upper bound), about 40 min, counted against the 17 h 20 min appetite. It includes one full `make verify` (started 08:43:05Z). Commits `47764cf` (F-16) and `bc4e776` (F-11, F-13, F-14, F-15, F-17, F-18); full `make verify` at `bc4e776`: VERIFY GREEN (markdownlint report-only, as before), log `p6-handrepair-verify.log` in the scratchpad.
- Fixed, each with a test shown red against the unrepaired code first:
  - F-16: handoff gate reads JSON and nested YAML with duplicate-key detection, so a repeated key is not measured (exit 3).
  - F-11: the publication drift check gets its own checking deadline (`changed_paths(deadline=...)`).
  - F-15: outcomes the dispatcher could not deliver after a failed store write are kept in memory and published; a failed binding write no longer escapes `publish()`.
  - F-17: the manifest lists all `39 + 3N` expected slot identities; unstarted ones read `not-started`.
  - F-18: result records carry `started_at`; the published manifest keeps `started_at`, `ended_at` and `leak_check` per slot, so a reused slot keeps its original provenance after the store is cleared.
  - F-14: the receipt keeps the catalog's per-candidate evidence and the seat models; the manifest adds a `preparation` block (check time, pool, model states, unread ids, probe audit).
  - F-13: probes and research launches write the measured model store and its model definitions into Pi's fresh agent directory (`install_measured_models`); the receipt carries the store, the manifest does not.
- F-12 (store placement against the model's home directory) was first stopped for a decision; the maintainer answered "Ja zu Option 1" on 2026-10-19 (`decisions.md` Q-15), and it is fixed below.
- [DETAIL] The fake Pi of `test_stage2_research_availability.py` now also records its agent directory listing.

### F-12 repair — 2026-10-19

Maintainer ruling Q-15 recorded in `decisions.md`; the placement guard now also refuses a store inside the real home directory that Claude research processes inherit, with a message naming `XDG_STATE_HOME`; the design line for the default store path is amended.

- Test: `tests/test_stage2_swarm.py::test_a_store_inside_the_real_home_is_refused_and_one_outside_it_is_accepted` (red against the unrepaired code: the run exited 0 instead of 1). Row F-12 booked `fixed`; ledger line under criterion 52.
- Span (measured, `date -u`): 2026-10-19T09:06:45Z to 2026-10-19T09:26:50Z (upper bound), about 20 min, counted against the 17 h 20 min appetite. It includes one full `make verify` (started 09:08:08Z): VERIFY GREEN (markdownlint report-only), log `f12-verify.log` in the scratchpad.

### Capture tool built — 2026-10-19

Built `scripts/research_capture.py` and `tests/test_research_capture.py` (the attended F-1 offline capture tool; usage in "How to run the F-1 capture"). The real pinned Pi was not started; only the stand-in dry run ran. F-1 stays open.

- Span (measured, `date -u`): 2026-10-19T09:54:18Z to 2026-10-19T10:27:30Z (upper bound), about 33 min, counted against the 17 h 20 min appetite. It includes one full `make verify` (10:04:29Z to 10:26:51Z): VERIFY GREEN (markdownlint report-only), log `capture-tool-verify.log` in the scratchpad.
- Tests: 19 in `tests/test_research_capture.py`, written red first (collection error: no module `research_capture`), green after the tool.
- [DETAIL] Not in the kit: declared in `scripts/ci_gates.py` under `OHNE_AUFRUFER` as a framework-only entry point.
