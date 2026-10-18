---
title: "ADR 0020 — Phase 1 uses a research swarm with a checked handoff"
category: adr
status: accepted
created: 2026-10-15
last_reviewed: 2026-10-18
updated: 2026-10-18
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, research, swarm, stage-2]
---

# ADR 0020 — Phase 1 uses a research swarm with a checked handoff

* Status: accepted by the merge of the pull request that carries this file.
  Until then, open is proposed and closed is rejected. Amends the phase-1
  routing of ADR 0007 and research purpose of ADR 0011; supersedes neither
  whole ADR and amends no numbered D/O decision.
* Review: maintainer chose the amended direction in the research-swarm
  interview on 2026-10-14–18, Q-1–Q-14; acceptance is the future merge, with
  no agent-written approval. Decider: maintainer; prepared by Codex, with
  the Q-12 to Q-14 amendments drafted by Claude Code (Opus 5.5).
* Date: 2026-10-15 · takes effect on merge.

## Context

The original single explorer lacked independent evidence and reconciliation
(research-swarm research, 2026-10-14, baseline `1e29f6e`). The first unmerged
slice used six broad topic pairs and free public researchers. The maintainer
amended that on 2026-10-15: finder first, smaller topics, three same-brief
models per repository topic and a fixed report/scoring contract (Q-7).
Pi's free-model path was observed to return 403 FreeTierError by the
maintainer; Q-8 replaces it with OpenCode Go through Pi, Q-9 selects DeepSeek,
MiMo and Qwen Flash for online topics. This draft relies on that recorded
observation, not a new live probe. Public-only context survives the provider
change (Q-3, Q-6, Q-8). Q-10 adds free models offered by Go itself, selected
from a fresh Pi catalog each run, only to online topics alongside the Flash
trio; Zen stays excluded. The source was read at `6146fde` on 2026-10-16;
this draft neither probes the catalog nor claims live availability. The
repository runtime pin is now Pi 1.2.0 (ADR 0019). Q-11 (2026-10-17)
records that Pi's fresh catalog has no tool-support field and selects a second
public source, models.dev, for tool_call and deprecated status. These dated
observations are the maintainer's recorded evidence, not measurements by this
drafting call; models.dev failure excludes free seats but retains the
required ones. Q-12 (2026-10-18) replaces both fixed trios: on that day
`qwen3.8-flash`, a fixed online member, could not be called (wire API not
measured) while other Go models answered, so a fixed trio would end every
run incomplete. Each required seat now has an ordered candidate list and a
reachability check before each run, in the form of the review swarm's
availability preparation. Q-14 (2026-10-18) makes the substitutes live as
well: a seat declares one preferred model, and a substitute comes from the
admitted Go models of the fresh catalog, cheapest first. Q-13 (2026-10-18)
asks that finished research survive a run stopped by a token or quota limit.

## Decision Drivers

* Comparable independent reports with the same input and perspectives.
* Mapped repository evidence, explicit neighbouring specs and public practice.
* No private context in online research, regardless of subscription billing.
* Human decisions and sourced disagreements survive research into the spec.
* Finite concurrent work with auditable refusals and partial results.
* One unavailable model must not fail every run, changing a research model
  is a one-line edit (Q-12), and a newly admitted Go model serves as a
  substitute without any further edit (Q-14).
* Finished contributions are never paid for twice when a run is cut off
  (Q-13).

## Considered Options

* One runner with stage barriers and provider queues: one owner for state,
  context isolation, cancellation, provenance and append-only output.
* Separate finder/research/judge commands: inspectable steps, but more operator
  coordination and persisted state to prevent mixing baselines and budgets.
* Sequential execution of the same roles: simpler scheduling, but contradicts
  the maintainer's choice of concurrency in Q-7.

## Decision

Chosen option: "One runner with stage barriers and provider queues", because
it keeps the established entry point while making boundaries and handoff
checkable.

1. `stage2.py explore` dispatches features and architectural changes to the
   swarm, bounded/spike to GLM Flash; explicit Stage-1 fallback remains Haiku
   5.5 with its reason. Early research/spec/argument classes must agree.
   Swarm research headers require an explicit neighbours list; [] is valid,
   while a missing/null/non-list key refuses with exit 2 and a repair message.
2. Finder step 0 uses the three repository seats as independent
   locators; Opus 5.5 merges code, rules/ADRs, tests/gates and neighbour lists.
   The merged finder keys are their exact deduplicated category/reference
   union with all origins/reasons; extra or missing keys fail preparation.
   Runner resolution against scratch frozen bytes marks unresolved entries
   without granting topic scope, then inserts all given neighbours as given.
   Finder suggestions remain marked rather than silently accepted.
   Eligible neighbour specs have three forms: plans/changes/<name>/spec.md
   (one segment other than archive),
   plans/changes/archive/<YYYY-MM-DD-name>/spec.md, and
   plans/specs/<capability>/spec.md, excluding the change's own spec. Resolved
   neighbour-category artifacts inside those folders map to the frozen spec
   if present, retaining every finder key. Own-change entries are self with
   no relation/gap; other resolved entries are no-spec with named gaps.
   Given paths outside those forms or the own spec refuse with exit 2;
   eligible given paths must exist in frozen bytes.
3. Topics 1–8 cover code/reuse, callers/interfaces, rules/class, architecture,
   neighbours, history/volatility, tests/gates and risks; each uses the
   three repository seats on identical briefs, perspectives and report
   template.
   After map merge the runner collects topic 6's local frozen-HEAD history:
   up to ten most recent commits per resolved mapped path, with full hash,
   UTC author date, subject, body capped at 4,000 characters with truncation
   marked, and touched mapped paths. Older history is not read. Only topic 6
   receives it; a full packet hash resolves to that record, but a reachable
   hash outside the packet or PR/bead id alone is unsupported. No network or
   tracker is read; collection failure prevents topics and exits 1 incomplete.
4. Topics 9–11 cover best practice, existing tools/standards and public failure
   reports. Each uses the three online seats through Pi with only the
   filtered Opus sentence, fixed questions and public sources.
   In addition, every eligible Go chat model ending `-free`, selected from a
   live-fetched Pi Go overlay with declared include/exclude lists, works each
   online topic on the same brief. No Zen provider, OpenCode CLI, fixed free
   roster or substitution for the online seats. Dynamic free
   permission applies to public-only research, never private roles. Select only
   fresh-Pi text-input chat entries with exact matching models.dev
   opencode-go.models keys, with a present id field equal to the key,
   boolean tool_call true and status not deprecated.
   Missing/negative support, missing metadata, deprecated, non-chat and
   baseline-only entries are excluded with reasons. Unavailable/unreadable
   models.dev excludes all free candidates as capability-unavailable N=0,
   retaining required slots; this is distinct from a measured empty eligible set.
   Both sources are dated/digested. Pi refresh failure exits 1 before all
   models; Pi's absent capability field is expected, never a fallback trigger. These free
   seats are best-effort: failure is named, never hidden or substituted, and
   does not alone invalidate the 39 required contributions.
   Missing/non-object provider/models, non-object root, invalid JSON,
   non-200/request failure or duplicate claimed ids are document-level
   capability-unavailable. Duplicate ids mean repeated raw keys under that
   models object or equal id fields under different keys; either excludes
   all free candidates with reason duplicate-id, using duplicate-key-aware
   parsing. Other shape faults exclude only the candidate as
   metadata-malformed (non-object entry, non-boolean present tool_call,
   non-string present status, missing id or id/key mismatch), retaining raw
   values including an absent-id marker; missing
   entries are metadata-missing, absent/false support is no-tool-support.
   Other providers' entries are not inspected. A Go seat candidate must be
   fresh-Pi text-input chat to be probed; otherwise it is skipped with its
   reason (point 11). models.dev is not consulted for seat candidates.
5. Reports hold at most seven identified claims with evidence, kind,
   confidence/basis, counter-evidence, unread sources, neighbour relation
   and typed questions with report-local ids and claim links. The runner
   namespaces identities by run/topic/endpoint-model seat. Topic 3 carries a
   class assessment; topic 5 requires exactly one path/relation/nonempty
   local claims list per packet neighbour; topic 6 marks volatile facts and their central/runtime/
   dated governance proposal. Opus reconciles all topics and records per-model
   supported/refuted/unique/off-brief scores grounded in claim ids, plus
   unresolved and unsupported. Valid claims have one disposition, off-brief
   first; unique is an extra mark only for supported claims. Bad references
   remain unsupported; a report needs at least one evidence-backed claim,
   except topic 5 with no packet neighbour. All three seats still run with
   identical empty-neighbour packets, empty neighbour_relations and a not-read
   entry naming the empty packet; any claims are checked/scored normally.
   Extra relations fail, and a nonempty packet keeps the evidence floor.
   Reconciliation records no neighbour given or found as a named gap. Every
   model starts with the same perspectives; differing angles need a later
   maintainer decision.
6. Independent topic reports stay buffered until their stage ends. Each role
   is fresh/read-only, declaration-checked and exact-prompt leak-checked.
   Online Pi has scratch-only discovery-disabled context and public tools
   that refuse private/local sources and retain successful retrieval receipts.
   The accepted repository-Pi read risk is not called public-context isolation.
   Opus merge, topic author and judge have no tools and see only their packets.
   The runner joins resolved source/packet-commit/receipt excerpts in citation
   order and caps their total at 4,000 Unicode characters per claim, marking
   truncation. Local resolution is file-type-specific: exact unique Markdown
   heading sections or numbered criteria; Python AST definitions/module-level
   assignments with dotted nested names; YAML/JSON dotted keys as canonical
   JSON values; other files' whole-word first-match tails. Missing, ambiguous
   or unparseable references remain unsupported. The same rules govern map
   scope and evidence floors; prose-only matches in Markdown/Python do not
   resolve. One fixed whole-judge-packet character limit is derived in
   phase 4 from pinned-Claude Opus capacity minus a fixed output reserve,
   with capacity/conversion/source/date recorded. Above that limit, no judge
   is called: retain all evidence, exit 1 incomplete as judge-packet-over-limit.
   Exactly the limit allows dispatch; no further shortening, N reduction or
   extra judge call. A supported score means that evidence supports the claim and
   no evidence-backed peer claim contradicts it.
7. Research carries every accepted raw-report decision (even refuted or
   off-brief) and unresolved judge disagreement into an interview inventory
   with global claim/question links, grouping duplicates without source loss.
   Class mismatches and neighbour
   contradictions are human decisions. Topic-5 contradicts and
   unrelated-given fields derive obligations independently of Opus. The
   runner alone derives suggested status from the three topic-5 relations:
   every seat related/contradicts means confirmed, all unrelated means
   rejected, otherwise split. Every split creates a neighbour decision item;
   contradicts still creates its own item, and given paths stay given. The
   judge cannot set/change status; structured findings can add but never
   waive obligations. Phase 1a may exceed class minima;
   only actual maintainer answers settle obligations. Phase 2 carries confirmed
   and given neighbours in `neighbours:` and names claims/answers behind
   criteria. Direct claim bases must all be supported from complete runs;
   any other disposition needs an answered maintainer Q-record as the basis,
   even when mixed with supported claims. Neighbour parity is exact: confirmed
   or given in any complete run plus keep/add paths minus drop paths from
   maintainer-answered Q-records' research_neighbours fields. The recording
   session writes these lists from the stated answer; no answer prose is
   semantically graded. A neighbour item closes only with an item link AND
   its path in keep/drop. Split paths need human keep to enter the header.
   Add needs no item link, allowing drafting discoveries. Paths outside the
   three permitted forms exit 1; later existence is not checked, preserving
   historical answers after archival. A path in two lists of one record or
   incompatible inclusion/drop directives across answered records exits 3.
   Confirmation/rejection
   conflicts between complete runs and later omission of an earlier given
   path derive neighbour DECISION items independently of the judge. The path
   stays required until an item-linked structured human drop; an unanswered
   item fails even
   when the header keeps the path. Runtime instruction auto-loading
   is disabled; finders/topic author share the frozen research/decisions/spec
   brief and repository seats receive identical embedded AGENTS.md.
8. A blocking `research-handoff` gate checks v2 inventory coverage, answered
   human links, neighbours and criterion bases in live/archive changes.
   Only complete runs support interview/spec and carry obligations; prior
   complete runs remain binding across reruns. Before a spec exists, valid
   pending items are listed with exit 0; with a spec, missing answers or no
   complete v2 run exit 1. Incomplete-run claims cannot support criteria.
   Older unstructured evidence is exempt; unread/ambiguous inputs are not
   success. The gate and tests travel with the kit. Review still checks
   semantic fidelity and source applicability.
9. Queues permit at most four calls per provider across roles, and a security
   refusal cancels queued work and stops/reaps active children, retaining
   available partial evidence as cancelled; exit 2 takes precedence. Freeze `N`
   selected Go free
   models before model calls; the budget is at most `39 + 3N` invocations. A
   bounded Go-only Pi catalog refresh must succeed in each run's preparation; failures exit 1
   before models and never use cached/shipped rosters or Zen. Both catalog
   reads start together and share 60 seconds; abort unfinished requests at
   the deadline. Unfinished Pi exits 1; successful Pi plus unfinished
   models.dev records capability-unavailable/timeout and keeps required slots
   unless an explicit include is unmet. No retries or extension; models.dev
   receives no credentials/private data.
   Valid zero availability and capability-unavailable models.dev fallback keep
   the 39 required slots with distinct recorded reasons. Defaults select all eligible models; explicit include
   narrows and exclude wins. Record dated source, freshness, policy and roster;
   missing explicit includes exit 1 before models; no silent truncation of
   models/reports to fit the deadline or judge context.
   Preparation (catalog 60 seconds, each probe 60 seconds) precedes the
   finite per-role and 150-minute total deadlines;
   no retry, recursive delegation or debate. Required topic slots precede free
   slots, by topic and declared seat order (free ids sorted); reserve the
   judge's 15 minutes. Every unlaunched slot has a deadline outcome. Failed
   finder/merge/topic-author stages prevent later stages; filter rejection
   exits 1. Topic siblings finish after ordinary failures, but the judge
   requires all required reports. Failed/incomplete runs retain evidence
   and exit nonzero; only the runner appends research and writes audit records.
10. Endpoint role lists are separate from the review ladder. Qwen is declared
    for research without changing that ladder. Every output is scrubbed of
    used credentials; HEAD plus a full digest of all tracked files and
    untracked non-ignored change-folder inputs bind local evidence. Copies
    exist only in run scratch outside the repository and are deleted after
    publication/abort; failed freezing exits 1 before models. Persist HEAD,
    full/untracked-per-path digests and reports/excerpts, never frozen-file
    snapshots in research or briefs.
    Changed inputs invalidate publication with named paths and exit 1; only
    runner research appends/restamping are ignored. Invalid given neighbours
    refuse preflight (exit 2); later unread evidence stays a named gap.
11. The six required seats (three repository, three online) each declare
    exactly one preferred `{endpoint, model}` in `model-endpoints.yaml`, with
    no fallback list, beside an availability rule with the review swarm's
    field names (`max_age_seconds`, dated `exclude_until`) and a
    `measured_wire_apis` list. A separate step, `prepare-explore`, refreshes
    the catalog and admits Go models. Each needs a `modelle_terms` record
    passing the review swarm's terms check and a cost value, no `-free` id,
    and fresh text-input chat in Pi on a measured wire API. Repository seats
    need `framework` permission, and online seats need Pi. The terms record
    is the only manual step; it stays deliberate because repository seats
    receive private content. Substitutes form one pool for both trios: the
    admitted Go models with models.dev tool support, ordered by
    `anfragen_5h`, cheapest first, ties by id. Online admission is not
    loosened. Preparation probes lazily, one probe per distinct model, with
    the fixed text alone, no tools, no repository content, 60 seconds,
    leak-checked and audited; a Claude Code preferred model is probed
    through official Claude Code. Within each trio the reachable preferred
    models are kept first. Each remaining seat takes the cheapest reachable,
    unexcluded pool model that no seat of its trio holds, reported as
    "substitute for <seat>". The selection is printed for the main conversation and sealed
    in a single-use receipt bound to worktree, change, configuration, class
    and neighbours; `explore --availability-reported <id>` consumes it within
    the maximum age, and the selection stays frozen for the run, with no swap,
    re-probe or retry. A seat without a candidate stops preparation with
    exit 1 and names the seat; receipt, declaration and argument faults
    refuse with exit 2. Go free models and Opus roles are not probed. Probes
    are not research invocations. Rule validation, timed exclusion, the
    probe and receipt sealing are one implementation shared with the review
    swarm's availability preparation.
12. Every slot's launch and terminal records go atomically to a runner-owned
    state store outside the repository, owner-only, before its worker takes
    another slot. A later run of the change, under its own lock, run id,
    receipt and deadlines, reuses a stored `ok` result whose report
    validates, from the latest stored run only. Reuse needs equal input
    digests, ignoring that run's own research append and HEAD, and the same
    stage, topic, seat, endpoint, model and prompt hash. The run launches
    the rest within `39 + 3N` and marks reused and interrupted slots. A
    stored run with a security refusal is never resumed; a complete
    publication clears the store; a failed store write stops the run with
    exit 1.

## Consequences

* More calls and subscription/Claude quota buy independently comparable
  evidence; concurrency reduces waiting but no duration/cost saving is measured.
* Finder, two-source catalog qualification, queue cancellation, templates, gate
  and kit integration add maintenance. Large free rosters may leave named
  best-effort slots unfinished at the deadline; that alone does not invalidate
  completion. Missing required slots still do. No seat silently disappears.
* Pi refresh failure exits 1 before any model call. models.dev failure instead
  excludes free candidates and retains required slots with a recorded reason;
  explicit includes remain hard requirements and exit 1 if ineligible.
* Each run gains a preparation step and a report the orchestrator relays
  before the run; the selected models are reported, not fixed in the spec.
  Probes cost a few small calls outside `39 + 3N`, a Claude Code seat's
  probe included. Changing a preferred model is a one-line pull request; a
  substitute needs only an admitted terms record, so the pool follows the
  Go catalog by itself.
* Finished research survives a stopped run, at the cost of a runner-owned
  store outside the repository, an input-binding check and a per-change
  lock. A repository seat that deliberately reads an absolute path outside
  its working directory could reach the store, which is the accepted paid-Pi
  residual read risk, now also covering stored results.
* Questions may exceed minimum counts; the gate cannot invent answers or
  establish that a recorded answer faithfully reflects a human conversation.
* Same-brief scoring is evidence for later evaluation, not automatic model
  selection or architecture/class changes. Volatile-fact governance remains
  a maintainer-approved proposal, not a global policy installed by research.
* Isolation must be demonstrated with the actual pinned runtime. An earlier
  phase-6 blocker for the offline capture remains until measured evidence
  exists; changing the online provider does not waive it.

## Validation

* Runner tests plant wrong roles, early dispatch, unequal briefs, missing
  claims/receipts, frozen-state drift, expired budgets and queued leak refusals.
  They explicitly inject the pinned-wrapper stand-in and trap bare-Pi launches;
  actual-runtime qualification continues to use the real repository pin.
* Handoff mutations delete decisions/answers/bases/neighbours, including class
  mismatches and neighbour contradictions; local and hosted checks must fail.
  Cross-run confirmation/rejection and given-header omission fixtures require
  linked structured human keep/drop answers and the corresponding exact
  header set. Split-status fixtures ignore judge confirmations; prose-only
  answers cannot close neighbour items, answered add needs no item link,
  conflicting directives exit 3, and valid historical forms survive archival.
* `make verify`, generated CI and kit probe hold the same blocking contract.
* Phase-6 review checks prose scope, comparison meaning, faithful dissent,
  volatile-fact classification and the relevance of resolved criterion bases.
* Before merge, the maintainer attends an offline real-pinned-Pi capture with
  synthetic canaries and a local mock model server; record version, source
  hashes, payload/tool-schema capture, attempted escapes and outcomes.
* Offline real-Pi catalog tests prove forced refresh despite fresh caches,
  Go-only selection and removal of obsolete shipped ids; malformed/timeouts
  in Pi never become zero availability or a fixed-roster fallback. Independent
  models.dev fixtures prove exact-id intersection, support/deprecation checks,
  and capability-unavailable fallback without credentials or private data.
  They distinguish document/entry faults, shared-deadline outcomes, unavailable
  seat candidates skipped from the fresh overlay and exclusion provenance even when N is nonzero. Raw duplicate
  keys/equal claimed ids exclude all candidates; missing id excludes only
  its candidate. Independent map-to-neighbour fixtures cover active/archive/
  living specs, self entries and spec-backed entries wrongly labelled gaps;
  empty-topic-5 fixtures retain all 39 required slots. Type-specific resolver
  fixtures hold exact excerpts and refuse ambiguous or prose-only evidence.
  Judge-packet fixtures exercise the exact limit, one character over it and per-claim caps.
* Selection fixtures cover lazy unique probes, preferred-first and
  cost-ordered substitutes, determinism for a frozen catalog, a model added
  by one terms record, double-fill, unadmitted, unmeasured and excluded
  models, probe content canaries, receipt binding, age and
  single use, the seat-unavailable stop and the shared helpers. The review
  swarm's availability tests run unchanged where they are on the base.
* Store fixtures kill the runner with SIGKILL after a terminal outcome and
  find the record whole. They cover torn files, input-binding and slot-key
  mismatches, non-`ok` outcomes, refused and complete runs, and lock
  release after a killed run.
* After merge, public-only live qualification records the refreshed catalog,
  the reported seat selection, actual seat/free models, search/fetch
  outcomes and one resumed run. Until success no complete live swarm is
  claimed.
