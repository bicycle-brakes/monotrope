---
title: "Spec — research-swarm"
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
tags: [spec, stage-2, research, swarm]
class: architectural
appetite: 12
adr_files: [docs/adr/0020-phase-1-research-swarm.md]
neighbours: [plans/changes/interview-context/spec.md, plans/changes/haiku-5-5/spec.md]
---

# Spec — research-swarm

Phase 1 maps the sources, compares independent topic research and carries its
questions and evidence into the interview and spec (bead coding-harness-icw).
Authority: [decisions.md](decisions.md), Q-1–Q-11; Q-7 amends the six-topic
pairs, Q-8/Q-9 select three Go Flash models, and Q-10 adds dynamically
selected Go free models to online topics only, excluding Zen. Q-11 obtains
tool support and deprecation from models.dev, cross-checked with fresh Pi.
This redraft specifies the amended behavior; existing code is an earlier slice.

## Problem

Historical evidence is retained in [research.md](research.md); the redraft
addenda record `6e80ded` on 2026-10-15 and `6146fde` on 2026-10-16.

- The initial single explorer lacked independent views and assigned comparisons
  (research, original exploration, 2026-10-14 at `1e29f6e`).
- The current six-topic implementation has no finder, same-brief trio or
  structured claim evaluation; topic peers receive different angles (research,
  redraft addendum; Q-7).
- The free path in the earlier design is unusable through Pi according to the
  maintainer's observed 403; Q-8 chooses Go through Pi, Q-9 fixes the trio.
  Q-10 distinguishes free models offered by Go from the refused Zen tier and
  requires a fresh Pi catalog before each run; the fixed Zen roster in the
  earlier code cannot meet that rule (research, 2026-10-16 addendum).
  This drafting call did not probe a provider.
- Pi's catalog lacks a tool-support field; the maintainer's dated public-read
  evidence and Q-11 select models.dev for that check (decisions, 2026-10-17).
  A missing capability source must exclude free seats without blocking the
  39 fixed contributions; a failed Pi refresh still blocks the run.
- Existing interview minimums count answers but cannot prove that research
  decisions survived; prompts do not yet carry a checked research-to-spec
  link (research, redraft addendum; Q-7).

## Terms

- **Repository trio:** `deepseek-v4.1-flash` and `mimo-v2.6-flash` through
  OpenCode Go/Pi, plus `claude-haiku-5-5` through official Claude Code.
- **Online researchers:** the fixed Flash trio `deepseek-v4.1-flash`,
  `mimo-v2.6-flash`, `qwen3.8-flash`, plus selected Go free models, all through
  OpenCode Go/Pi with public-only permissions regardless of billing.
- **Selected Go free models:** unique `opencode-go` ids ending exactly `-free`
  in this run's freshly fetched remote overlay, filtered by include/exclude.
  They must be text-input chat models in fresh Pi and have a matching exact id
  under models.dev's `opencode-go.models` with `tool_call: true` and without
  `status: deprecated`. Baseline-only ids, non-chat models, missing metadata,
  absent/negative support and deprecated models are excluded with reasons.
  If models.dev is unavailable or unreadable, exclude all free candidates and
  record `N=0` with that reason; subject to explicit-include requirements,
  the fixed slots remain. Pi refresh failure
  cannot use this fallback. `N` is the frozen selected count, not qualification.
- **Required contribution:** one of the 39 fixed slots (3 finder, map merge,
  public topic, 24 repository, 9 online Flash, judge). The additional `3N`
  free slots are best-effort; each still requires a recorded terminal outcome.
- **Complete:** all required contributions and reconciliation are valid and
  frozen inputs unchanged; failed free seats are named but do not invalidate
  completion. Human questions may await phase 1a. Only complete v2 runs can
  supply phase 1a or phase 2; incomplete runs require a new complete run.
- **Public topic:** one Opus sentence of at most 20 words. Words contain Unicode
  letters joined only by single internal hyphens or straight/typographic
  apostrophes (`'`, `’`) between letters. Separators may be whitespace, commas,
  semicolons, parentheses, straight/typographic double quotes, guillemets,
  apostrophes at word edges as quotes, and an en/em dash surrounded by spaces;
  one final period or question mark is allowed. Count words after separating
  punctuation, retaining internal joins. Lower-to-upper transitions inside a
  hyphen segment and every other character are refused, including digits,
  underscores, slashes, backticks, colons, other dots, `@`, `#`, `=`, `<`, `>`,
  brackets and braces; a stand-alone hyphen is not an internal join.
  A whole-token, case-insensitive deny list also covers the change name, bead
  id and every tracked path component/file stem containing a hyphen,
  underscore, dot or digit in the frozen state. Letters-only symbol names are
  not denied as ordinary words. The exact-prompt leak check is a second layer.
- **Same perspectives:** existing state/evidence, counter-evidence/gaps, and
  effects on documented boundaries; every peer receives all three.
- **Claim:** a report-local `C1`–`C7` with statement, kind (`fact`, `assumption`,
  `judgement`), evidence and confidence/basis. The runner forms its global id
  `<run>/<topic>/<seat>/<local>`; seat identifies endpoint and model.
- **Evidence status and disposition:** the runner marks a claim `valid` or
  `unsupported`; unsupported claims remain visible but are never evidence.
  Every valid claim gets exactly one judge disposition, with `off-brief`
  taking precedence, otherwise `supported`, `refuted` or `unresolved`.
  `supported` means the attached resolved evidence supports the statement and
  no peer claim with evidence contradicts it. Opus has no tools; the runner
  attaches bounded evidence excerpts, marking truncation.
  `unique` is a separate mark only for supported claims absent from topic peers.
- **Handoff item:** `H-<n>`, unique within a run, linked to global source claim
  ids. Q-record headers link run-qualified items with `research_items:` and
  global claims with `research_claims:` beside their existing answer fields.
  Item links are `<run>/H-<n>`; criterion Q-record bases use
  `decisions.md#Q-<id>` within the owning change. Global question ids use the
  same run/topic/seat namespace with local Q ids.
- **Frozen input state:** HEAD plus a digest of every tracked file and every
  untracked non-ignored file under this change folder. Copies live only in
  run scratch outside the repository, including uncommitted input bytes;
  local references resolve there during the run. Copies are deleted after
  publication or abort. HEAD, the full digest and per-path digests of untracked
  change inputs persist in the manifest; snapshot copies never enter research
  or briefs as additional records. Selected frozen brief inputs and bounded
  cited excerpts are not snapshot records. A failed copy exits 1 before any
  model call.

## Topic contract

Finder 0 locates files/functions, applicable rules/ADRs, tests/gates and
neighbouring specs; each map entry is `path::symbol` or `path::section` plus
one sentence why. It locates and lists, without choosing a design.
The merged map is the exact deduplicated union keyed by category plus exact
reference; each key keeps all finder origins and reasons. Opus may neither
drop nor add keys. The runner resolves entries against frozen bytes; unresolved
entries stay marked `unresolved` but confer no topic scope. It inserts every
header-given neighbour as `given`, overriding any suggested label for that
path. These insertions are separate from the checked union of finder keys.

| Topic | Questions and evidence boundary |
|---|---|
| 1 Code and reuse | Existing functions/modules, analogous patterns, changes needed to reuse them and objections; mapped code plus direct imports, no new-code proposals. |
| 2 Callers and interfaces | Callers across code/tests/commands/CI/hooks/prompts, signatures/options/formats/configuration, readers versus changing callers, kit/instance consumers; connections to the map, with caller and callee cited. |
| 3 Rules and ADRs | Exact obligations, human-owned paths, required ADR changes and next number, conflicting rules, whether the declared class fits; repository rules only, no new rules; a class disagreement is a human decision. |
| 4 Architecture fit | Documented layer, prescribed runner/tracker/gate routes, framework/kit/instance responsibility and invalidated architecture statements; mapped code and documented architecture only, no target design. |
| 5 Neighbouring specs | Constraints, contradictions, overlap/order, shared resources and suggested-neighbour relevance; neighbours' spec/design/plan/decisions only; contradictions become human decisions. |
| 6 History and stale assumptions | Last change and reason, reversals/supersession, stale facts, recorded rationale, governance of repeatedly changing facts; mapped history only, proposals await the maintainer. |
| 7 Tests and gates | Existing checks, uncovered behavior, stand-in-only evidence, checks the change breaks, red-first possibilities and limits; mapped tests/gates only, no test writing or verify run. |
| 8 Risks and edge cases | Failure paths, unusual input, security boundaries, recovery and concurrent sessions; mapped places only, name risks without designing repairs. |
| 9 Best practice online | Approaches, reasons/conditions, disagreements and warnings; retrieved primary documentation/papers/projects before secondary pages; tools belong to 10, incidents to 11. |
| 10 Tools and standards online | Existing tools/services/libraries, maturity/version/release/licence, standards/formats, cost and local/remote execution; retrieved project sources with dates, no adoption recommendation. |
| 11 Failures online | Incidents and causes, vulnerabilities/advisories, traps and mitigations; retrieved issue trackers/vendor advisories/CVE records/postmortems with dates, no assertion about our code. |

All topic reports use: at most seven key claims (`C1`–`C7`, statement,
evidence, kind, confidence/basis); counter-evidence; not read; relation to
neighbouring specs; questions (`Q1` onward, unique per report, classification
`[DECISION]`, `[GAP]` or `[DETAIL]`, and a nonempty `claims:` list of local
claim ids). Duplicate local ids or references outside that report fail the
template. Online reports mark neighbour relations not assessable and receive
no neighbour identities. Topic 3 additionally requires
`class_assessment: {class, claims}`; the class is one of the four declared
classes and claims is a nonempty local-id list. Topic 6 claims require a
boolean `volatile`; each true value requires
`governance: central|runtime|dated`. Topic 5 additionally requires
`neighbour_relations`: exactly one `{path, relation, claims}` per packet
neighbour, given or suggested; relation is `related|unrelated|contradicts`,
and claims is a nonempty local-id list. Missing, extra or duplicate paths fail
the template. Every `contradicts`, and every `unrelated` header-given path,
derives a claim-linked human obligation independently of the judge; the judge
can add obligations but cannot remove them. A valid report needs at least one
evidence-backed claim. Other unsupported claims remain with that status;
a failed individual fetch alone does not reject the report.

## Acceptance criteria

1. When Stage 2 exploration selects `feature` or `architectural`, phase 1 uses the research swarm.
   *Refuted by:* Either class produces only the single GLM exploration report.
   *Basis:* `decisions.md#Q-4`.
2. When Stage 2 exploration selects `bounded` or `spike`, phase 1 retains single GLM 5.3 Flash exploration.
   *Refuted by:* Either class starts a finder or swarm researcher.
   *Basis:* `decisions.md#Q-4`.
3. When exploration precedes the spec, the research header or explore-only `--class` argument supplies the class without requiring a spec or plan.
   *Refuted by:* Valid early input is refused because a later artifact is absent.
   *Basis:* `decisions.md#Q-4`; early-class evidence in research.md.
4. If class declarations or given-neighbour headers are invalid, Stage 2 exploration refuses before a model call with exit 2.
   *Refuted by:* Malformed, missing or disagreeing classes pass, or a duplicate, escaping, non-spec or missing frozen neighbour path starts a call.
   *Basis:* `decisions.md#Q-4`; existing class contract.
5. When topic research starts, all three finders and the tool-free Opus map merge have valid recorded results whose finder keys form the exact union defined in the Topic contract.
   *Refuted by:* A failed finder/merge, missing map, dropped or added finder key, or duplicate key still lets a topic start; an Opus merge launches with any tool.
   *Basis:* `decisions.md#Q-7`, topic 0.
6. When repository topics 1–8 run, each has independent DeepSeek Flash, MiMo Flash and Haiku 5.5 contributions.
   *Refuted by:* A topic is omitted, a model substituted, or one session supplies two seats.
   *Basis:* `decisions.md#Q-7`.
7. When reconciled research is published, it contains public-practice, documented-architecture and neighbouring-spec comparison sections with named gaps for unread evidence.
   *Refuted by:* A comparison section or an unread-neighbour gap entry is absent; semantic comparison quality is also checked in phase 6.
   *Basis:* `decisions.md#Q-3`; `decisions.md#Q-7`, topics 4, 5 and 9.
8. While an online researcher runs, no repository-derived content except the accepted public topic reaches its model or web requests.
   *Refuted by:* A canary from rules, paths, identifiers, finder output, history or private reports appears in an outbound payload or query.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-6`, `decisions.md#Q-8`.
9. While an online researcher runs, no available tool or automatic context route can obtain repository files, git data or other private local content.
   *Refuted by:* A file or shell tool is available, ambient context is discovered, or fetching reaches local files or private network addresses.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-8`.
10. When a public claim counts as evidence, a successful page receipt binds its URL, title, retrieval date and excerpt or locator.
   *Refuted by:* Search-only, snippet or invented receipts support a claim, or a receiptless claim is not retained as unsupported; a report with no evidence-backed claim is accepted.
   *Basis:* `decisions.md#Q-7`, topics 9–11; existing F-3 correction.
11. If a role has no compatible static declaration or declared dynamic Go-free selection permission, the runner refuses that call.
   *Refuted by:* Online Qwen receives the framework packet or a model outside its declared role is launched.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-8`, `decisions.md#Q-9`, `decisions.md#Q-10`.
12. If any immediately preceding exact-prompt leak check is not clean, dispatch stops and the run exits 2 after cancelling queues and stopping and reaping active children.
   *Refuted by:* One scan covers multiple prompts, a queued call starts after BLOCK, a running child is awaited instead of stopped, available partial output is lost instead of retained as cancelled, or exit 1 overrides exit 2.
   *Basis:* `decisions.md#Q-7` concurrency answer; existing leak-check contract.
13. When any model invocation is attempted, its durable record identifies run, input state, role, topic, endpoint, model, individual leak check and outcome.
   *Refuted by:* Concurrent output cannot be assigned to a slot, or a failed slot is audited as successful.
   *Basis:* `decisions.md#Q-7` concurrency answer; existing audit contract.
14. When the research is reconciled, one fresh tool-free Opus 5.5 context covers topics 1–11 and the finder map with a resolved evidence excerpt for each valid claim.
   *Refuted by:* Another model judges, a peer session is resumed, a required topic or valid claim's excerpt disappears, or any file, shell, web or MCP tool is available.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-7`.
15. When sourced disagreement remains unresolved, reconciliation retains its opposing global claim ids and evidence without an answer field.
   *Refuted by:* An unresolved disagreement loses an opposing claim id or evidence, or judge output contains a maintainer answer field; phase 6 also checks faithful treatment of dissent.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-7` report and interview addenda.
16. When local claims count as evidence, their path and symbol or section resolve against the retained frozen input state.
   *Refuted by:* Unresolvable or line-only references are supported, a reference resolves against the live tree instead of scratch bytes, a report is absent, a changed frozen file permits complete publication, or a frozen-file copy is persisted in research or the change folder.
   *Basis:* `decisions.md#Q-7` report template; existing source contract.
17. While the swarm explores, only the runner appends research and pre-existing repository content outside that artifact remains unchanged.
   *Refuted by:* A participant edits a file, rewrites an answer, replaces earlier research or changes git or tracker state.
   *Basis:* `decisions.md#Q-7` finder and topic boundaries; existing writer contract.
18. If a required contribution fails, the run retains partial evidence and all missing-slot outcomes and ends incomplete with exit 1 unless a security refusal requires exit 2.
   *Refuted by:* A failed preparatory stage dispatches a later stage, missing required topic reports still reach the judge, a report with zero evidence-backed claims passes, or a failed free seat alone makes the run incomplete.
   *Basis:* `decisions.md#Q-7`; existing failure contract.
19. When a swarm executes, its maximum 39 + 3N invocations follow the finite deadlines, required-first dispatch and reserved 15-minute judge allowance without retries or debate.
   *Refuted by:* An extra invocation or retry occurs, a free slot starts ahead of queued required slots, topic work consumes the judge reserve, or unlaunched slots lack not-started-deadline outcomes.
   *Basis:* `decisions.md#Q-7` concurrency answer; `decisions.md#Q-10`; finite-budget detail below.
20. When exploration explicitly uses `--stage2-off [REASON]`, it keeps single Haiku 5.5 exploration and records route, model and reason for the plan.
   *Refuted by:* It runs a swarm, reads a foreign key, names Haiku 4.5 or loses the reason.
   *Basis:* `decisions.md#Q-4`; neighbouring haiku-5-5 spec, criterion 1.
21. When outputs contain a used credential, durable records and diagnostics redact the whole credential and every fragment of eight or more characters.
   *Refuted by:* A planted fragment survives in an answer, receipt, concurrent log or error.
   *Basis:* Existing credential contract.
22. When delivered, phase-1 doctrine, endpoint roles and exactly one new research-swarm ADR describe the same amended workflow.
   *Refuted by:* Six-topic or Zen-free-through-Pi instructions remain operative, the review ladder changes, or an accepted ADR is edited.
   *Basis:* `decisions.md#Q-7`, `decisions.md#Q-8`, `decisions.md#Q-9`, `decisions.md#Q-10`.
23. Before any online call, fresh tool-free Opus supplies a recorded public topic passing the defined word and name filters and exact-prompt leak check.
   *Refuted by:* An absent, rejected or privately augmented topic reaches an online seat; the author has any tool; research-swarm, a bead id or a sentence with `[`, `{`, `@`, `=` or a digit passes; Container-Isolation für KI-Agenten-Läufe or Isolation, Prüfung und Wiederherstellung für Agentenläufe fails the character rule; rejection fails to stop pre-topic dispatch with exit 1.
   *Basis:* `decisions.md#Q-6`, retained by `decisions.md#Q-8`.
24. When finder step 0 runs, the repository trio independently receives the same private change brief and four-list locator template for Opus to merge.
   *Refuted by:* Only one finder runs, an output has fields beyond the four locator lists, an empty category lacks an unread marker, an unresolved map entry grants topic scope, or a given neighbour is missing from the runner's map; prose design judgements are off-brief and reviewed in phase 6.
   *Basis:* `decisions.md#Q-7`, topic 0, option A.
25. When a researcher receives a topic, its packet matches the checked-in questions and permitted evidence scope of the Topic contract.
   *Refuted by:* A packet differs from its topic prompt; report prose that proposes new code or local applicability outside that scope is scored off-brief and checked in phase 6.
   *Basis:* `decisions.md#Q-7` topic walk-through.
26. When models work the same topic, their fresh contexts contain identical task briefs, evidence packets, embedded instructions, perspectives and templates without peer reports or automatic instruction loading.
   *Refuted by:* One model receives a different map, instruction file, angle or peer report, or its runtime auto-loads instructions.
   *Basis:* `decisions.md#Q-7` same-perspectives addendum.
27. When a topic report is accepted, its fixed template and report-local identities satisfy every required field and topic-specific field.
   *Refuted by:* An eighth claim, duplicate local claim/question id, invalid question claim link, missing confidence basis or unread section, absent topic-3 class assessment, incomplete/duplicate/extra topic-5 neighbour relation or empty relation claims, or ungoverned volatile topic-6 claim is accepted.
   *Basis:* `decisions.md#Q-7` template acceptance.
28. When Opus reconciles reports, per-topic per-model claim lists and counts distinguish supported, refuted, unique, off-brief, unresolved and unsupported claims.
   *Refuted by:* A valid claim has two dispositions, a unique claim is not supported, an unsupported claim is supported, a score lacks claim ids, a valid claim lacks its resolved evidence excerpt with truncation marked where needed, or a failed seat has no named outcome.
   *Basis:* `decisions.md#Q-7` scoring acceptance.
29. When neighbour relevance is reconciled, research preserves given paths and distinguishes suggestions, confirmations and rejected suggestions with reasons.
   *Refuted by:* A suggestion becomes authoritative silently, a given neighbour disappears, or a topic-5 contradicts entry or unrelated given-neighbour entry has no human handoff item.
   *Basis:* `decisions.md#Q-7` finder and topic 5.
30. When a spec uses complete v2 research, the handoff gate requires its neighbours header to equal confirmed and given paths plus linked maintainer additions minus linked maintainer drops of given paths.
   *Refuted by:* A required path disappears, an escaping/duplicate path or unconfirmed suggestion enters, or any path neither confirmed, given nor added by a linked maintainer answer passes; such findings exit 1.
   *Basis:* `decisions.md#Q-7` neighbours addendum.
31. When a complete v2 run hands off, every accepted raw-report DECISION question, unresolved judge disagreement, class mismatch and neighbour contradiction or given-neighbour removal has a claim-linked inventory item.
   *Refuted by:* A refuted/off-brief report decision is omitted, a differing class or topic-5 contradicts/unrelated-given field lacks an independently derived item, or grouping duplicates loses a source question or claim id.
   *Basis:* `decisions.md#Q-7` interview and template addenda; topics 3 and 5.
32. When spec.md exists, the handoff gate requires coverage and linked answered maintainer records for every obligation of every complete v2 run in that change.
   *Refuted by:* Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
   *Basis:* `decisions.md#Q-7` lost-decision gate acceptance.
33. If v2 evidence or its links are unreadable or identities ambiguous, the handoff gate reports not measured with exit 3.
   *Refuted by:* Malformed manifests/inventories, duplicate global ids or report-local ids, missing linked files or ambiguous answers silently pass.
   *Basis:* `decisions.md#Q-7` lost-decision gate; repository unmeasured convention.
34. When a spec has complete v2 research, the handoff gate requires each criterion Basis to name only supported global claims from complete runs and/or maintainer-answered Q-records in that change.
   *Refuted by:* A criterion lacks an origin, any named claim is missing, incomplete-run, unsupported, refuted, off-brief or unresolved even alongside supported claims, or a record is unanswered; these findings exit 1, while semantic relevance is checked in phase 6.
   *Basis:* `decisions.md#Q-7` traceability acceptance.
35. When topic 6 marks a claim volatile, the accepted report carries its central, runtime or dated governance proposal for a maintainer decision.
   *Refuted by:* A volatile claim without governance passes validation or a proposal is implemented without a human answer; phase 6 also checks whether changing facts were correctly marked volatile.
   *Basis:* `decisions.md#Q-7`, topic 6 addendum.
36. While stages execute, provider-wide queues enforce four in-flight invocations and cancel and stop children on any security refusal.
   *Refuted by:* A fifth Go call starts across roles, queued work survives a leak/declaration refusal, available cancelled output is discarded, or exit 1 overrides security exit 2.
   *Basis:* `decisions.md#Q-7` concurrency option A.
37. When online topics 9–11 run, each has independent DeepSeek Flash, MiMo Flash and Qwen 3.8 Flash contributions through Pi on the same public-only brief.
   *Refuted by:* A free model, OpenCode CLI, Haiku or omitted vendor replaces one of the nine mandatory Flash contributions; added free seats cannot replace them.
   *Basis:* `decisions.md#Q-8`, `decisions.md#Q-9`.
38. Before any swarm model call, a successful live pinned-Pi Go catalog refresh records its freshly fetched overlay, source, UTC time and selection.
   *Refuted by:* A cached/shipped list substitutes for refresh, a baseline-only free id is dispatched, another provider supplies a seat, or selection lacks dated provenance.
   *Basis:* `decisions.md#Q-10`; `decisions.md#Q-11`.
39. When N Go free models are selected, each has an independent best-effort slot on topics 9–11 with the fixed Flash brief and a recorded terminal outcome.
   *Refuted by:* A selected seat is silently omitted or failed as successful, a non-selected/no-tool-support/deprecated model runs, peer briefs differ, or a missing explicit include starts any model instead of preflight exit 1.
   *Basis:* `decisions.md#Q-7` same-perspectives addendum; `decisions.md#Q-10`; `decisions.md#Q-11`.
40. While selected Go free models participate, they receive only the public-only role permissions and cannot fill a finder, repository, author, merge or judge seat.
   *Refuted by:* A free seat inherits the Go endpoint's framework permission or receives a private packet, map or report.
   *Basis:* `decisions.md#Q-3`; `decisions.md#Q-10`.
41. If the live Pi catalog cannot be measured reliably, the runner preserves the diagnostics and exits 1 before any swarm model call instead of substituting a fixed roster or another provider.
   *Refuted by:* A Pi timeout, stale-only result, malformed or ambiguous Pi catalog becomes valid zero availability or Flash-only fallback, or the failure exits 0, 2 or 3; absence of a tool-support field in Pi is not such a failure under Q-11.
   *Basis:* `decisions.md#Q-10`; existing failure contract.
42. When fresh Pi yields an empty free selection after capability checks and policy with no unmet explicit include, including models.dev absence or failure, the run records N=0 and its measured-empty or capability-unavailable reason and keeps all 39 fixed model slots.
   *Refuted by:* A missing models.dev model, absent/false tool_call or deprecated status admits a free seat, models.dev failure alone blocks the fixed slots or is recorded as measured capability absence, or N=0 revives a prior roster or omits a fixed slot.
   *Basis:* `decisions.md#Q-10`; `decisions.md#Q-11`.

## Non-goals

- Zen free models, the OpenCode CLI, other providers and disguised clients:
  Q-10 permits Go free models through Pi only; the deferred CLI route stays out.
  No cost benchmark or claim that a selected model is live-qualified follows
  from catalog discovery, and no research model changes the review ladder.
- Per-model perspectives, debate, research-selected design or automatic class
  changes; evaluation evidence may motivate a later maintainer decision.
- Changing interview minimum counts, inventing answers, automatic semantic
  grading of human answers, or replacing phase 2's research/decisions inputs.
- Global centralization of model settings, new freshness policy or follow-up
  tracker writes by researchers; topic 6 only makes sourced proposals.
- Implementation-review swarm, other runner verbs, persistent web cache,
  paid search API, cost benchmark or opening sibling checkouts.

## Protected areas

- Accepted ADRs, `provenance.yaml`, existing human answers and adoption records:
  retain their meaning and history; only the named new ADR is proposed.
- Session runtime/policy and the review ladder's membership/order: research
  roles are declared separately, including Qwen without changing the ladder.
- Tracker, user configuration and sibling repositories: no research writer.

## Definition of Done

- `make verify` and hosted CI are green with the new blocking handoff check.
- The plan's named routing, prompt, schema, gate, kit and documentation paths
  move with `docs/adr/0020-phase-1-research-swarm.md`; approvals remain pending.
- The offline capture on real pinned Pi (currently 1.2.0, read 2026-10-16)
  with synthetic private canaries,
  outbound payloads, tool schemas and failure probes passes before merge;
  stand-ins alone do not qualify isolation. Open phase-6 finding F-1 remains
  open until this evidence exists; the maintainer attends that separate step.
- Phase-6 review records semantic comparison quality, faithful dissent and
  answer/basis relevance, finder/topic scope, and volatile-fact classification.
- After merge, a public-only live qualification records catalog refresh,
  actual Flash/free model and web outcomes; until success no complete live
  swarm is claimed. This draft calls no external model and does not claim
  runtime availability.
- PR file review confirms protected areas/non-goals, names the bead, records
  test/capture commits and keeps final `Closes-Bead: coding-harness-icw`.

## Open decisions

None open. The recorded phase-2a rulings in decisions.md (S-1–S-30,
2026-10-16) and the maintainer's Q-11 answer (2026-10-17) settle the review
ambiguities; Q-11 replaces S-21's Pi-only capability rule. I carry those
visible details into this spec; no maintainer answer is supplied here.

- [DETAIL] Criterion bases name the existing Q-records as
  `decisions.md#Q-<id>` so the recorded origin is explicit; this
  changes reference spelling only, not the criterion or its authority.
- [DETAIL] Keep the architectural class, ADR 0020 and 12-hour phase-4 stop;
  sum measured historical spans in plan.md's Earlier implementation time and
  later Time used spans as prompts/04-implement.md defines them. Before any
  phase-4 work, establish the unmeasured repair-attempt-3 span from its runner
  audit start/end, otherwise its commit timestamps, and append source/result.
  If neither bounds it, raise the appetite stop immediately with `found:`
  "time used not measurable"; only the maintainer's continue with a new total
  permits more phase 4. Earlier time is never zeroed or reset, and drafting
  time in phases 2/3 does not count. This prevents an unknowable remainder
  silently extending the stop (S-30).
- [DETAIL] Preflight validates class and given neighbours, then measures the
  catalog before model dispatch. Invalid neighbour entries (not unique
  repository-relative existing frozen `spec.md` paths) exit 2. Include/exclude
  are unique exact-id lists: empty include selects all eligible ids, exclude
  wins; malformed policy exits 2. Any explicit include missing from the fresh
  eligible set exits 1 before models, even if also excluded. Valid `N=0`
  retains 39 fixed slots. Q-11's models.dev-unavailable fallback excludes
  every free candidate, records the source failure and keeps fixed slots;
  an explicit include remains a hard requirement and still exits 1 if it is
  ineligible. Read models.dev without credentials or repository data, retain
  source/time/digest and per-model reasons. Missing entries/absent or false
  tool_call/deprecated status exclude those ids; malformed/unreachable
  metadata excludes all. Never infer support from Pi compat flags. This
  carries the maintainer's two-source choice without weakening Pi freshness.
  No Zen, baseline fallback or silent truncation.
- [DETAIL] The private change brief is frozen research.md header/body plus
  decisions.md and spec.md when present; the bead is id-only and its tracker
  text is not read. Finders and public-topic author get that same brief.
  Repository seats embed the same AGENTS.md. All runtimes disable automatic
  instruction discovery. This fixes the common input without tracker access.
- [DETAIL] Stages are catalog → finder trio → Opus map merge → Opus public
  topic → topics → Opus judge. Any failed finder, merge or topic-author result,
  including topic-filter rejection, prevents later stages and exits 1.
  Required topic failures allow remaining topic siblings to finish but prevent
  the judge; failed free slots are named and do not block it. A security
  refusal always cancels queues, stops/reaps children, keeps available partial
  output as cancelled and exits 2 in preference to exit 1.
- [DETAIL] The budget is at most `39 + 3N` calls. Provider queues share four
  permits per provider across roles. Deadlines: catalog 60 seconds, topic
  author 5 minutes, finder/researcher/merge 10, judge 15, run 150 total,
  monotonically measured with no retries. Required slots precede free seats:
  repository topics 1–8 then online Flash 9–11, by topic then declared seat
  order; free seats follow by topic then sorted id. The judge's 15 minutes
  are reserved. A topic launches only with positive pre-reserve time left;
  its allowance is the lesser of role limit and that remainder. Unlaunched
  slots are not-started-deadline, incomplete only when required. No silent
  roster truncation; large free rosters can leave named missing seats.
- [DETAIL] Local references resolve against retained frozen bytes. Before
  publication compare HEAD and the full digest; ignore only the runner's own
  research appends and updated restamp. Other changes name paths and yield
  incomplete exit 1 with outputs retained. Copies stay outside the repository
  in run scratch and are deleted after publication/abort; only HEAD/digests,
  reports and resolved excerpts persist. Failed freezing exits 1 before
  models. This covers uncommitted inputs without copying the tree into briefs
  or invalidating its own digest (S-22).
- [DETAIL] Opus map merge, topic author and judge have empty tool lists and
  see only their packets. The runner attaches resolved symbol/section or
  receipt excerpts for each valid claim, capped at 4,000 Unicode characters
  per cited source with a truncation flag; no private excerpt goes online.
  This makes supported scores reviewable without reading live files (S-29).
- [DETAIL] Template breaches reject a report. Bad citations mark individual
  claims unsupported; one evidence-backed claim is the report floor. An
  online report thus needs one successful page retrieval, not success for
  every attempted fetch. Partial receipts and unsupported claims remain.
- [DETAIL] The runner assigns global claim/question ids using run, topic,
  endpoint-qualified model seat and local id. Handoff items H-<n> link the
  full global source ids. Q-record headers carry research_items and
  research_claims lists. Duplicate decisions may share one item, preserving
  every source question/claim, including decisions scored off-brief/refuted.
  Class mismatches derive obligations independently of the judge; neighbour
  contradictions and proposed removal of given neighbours derive directly
  from topic-5 neighbour_relations, even with no explicit DECISION question;
  judge findings may add items but cannot waive them (S-24).
- [DETAIL] Version manifests research-swarm/v2. Complete runs alone supply
  phase 1a/2; incomplete runs require a new complete run and their claims
  cannot support criteria. Every complete run keeps its obligations across
  later runs and archival; one answered Q-record may link several runs.
  Before spec.md exists, valid pending obligations are listed with exit 0.
  Once it exists, missing answers or no complete v2 run exit 1. Malformed or
  unreadable evidence exits 3 even before a spec. Legacy changes without v2
  runs are a reported exemption, including this redraft.
- [DETAIL] The gate derives coverage from accepted raw-report questions,
  class/neighbor fields and unresolved judge disagreements, not the judge's
  inventory alone. Once a spec exists it also resolves every criterion's
  Basis: every named direct claim must be supported and complete-run, even in
  a mixed list; other dispositions require a maintainer-answered Q-record
  basis (which may link the original claim in research_claims). It enforces
  exact neighbour parity: confirmed plus given plus linked maintainer additions
  minus linked maintainer drops of given paths; arbitrary phase-2 additions
  fail unless human-answered or confirmed by a new complete run (S-23, S-27).
  Review checks faithful questions/answers,
  basis relevance, comparison quality and off-brief prose; structure checks
  never claim to judge those meanings.
- [DETAIL] Repository online roles keep scratch isolation and public tools
  independent of Go's private-role permission. Wrapper stand-ins test runner
  orchestration; real pinned-Pi offline capture still owes isolation evidence.
  Historical phase-4 time stays in the plan, with Time used empty until the
  amended implementation starts.
- [DETAIL] Criteria 23 and 38 open with «Before any …»: each states a
  precondition on dispatch order, a shape the When/While/If opening marks
  elsewhere; the wording stands as reviewed in phase 2a instead of being
  reworded after the rulings, and each refutation keeps the sentence
  checkable.
