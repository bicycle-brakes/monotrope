---
title: "Spec — research-swarm"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-15
updated: 2026-10-15
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-15"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, research, swarm]
class: architectural
appetite: 12
adr_files: [docs/adr/0019-phase-1-research-swarm.md]
neighbours: [plans/changes/interview-context/spec.md, plans/changes/haiku-5-5/spec.md]
---

# Spec — research-swarm

Phase 1 maps the sources, compares independent topic research and carries its
questions and evidence into the interview and spec (bead coding-harness-icw).
Authority: [decisions.md](decisions.md), Q-1–Q-9; Q-7 amends the six-topic
pairs, and Q-8/Q-9 replace free research with three OpenCode Go models.
This redraft specifies the amended behavior; existing code is an earlier slice.

## Problem

Historical evidence is retained in [research.md](research.md); the redraft
addendum records the working-tree baseline `6e80ded` on 2026-10-15.

- The initial single explorer lacked independent views and assigned comparisons
  (research, original exploration, 2026-10-14 at `1e29f6e`).
- The current six-topic implementation has no finder, same-brief trio or
  structured claim evaluation; topic peers receive different angles (research,
  redraft addendum; Q-7).
- The free path in the earlier design is unusable through Pi according to the
  maintainer's observed 403; Q-8 chooses Go through Pi, Q-9 fixes the trio.
  This drafting call did not probe a provider.
- Existing interview minimums count answers but cannot prove that research
  decisions survived; prompts do not yet carry a checked research-to-spec
  link (research, redraft addendum; Q-7).

## Terms

- **Repository trio:** `deepseek-v4.1-flash` and `mimo-v2.6-flash` through
  OpenCode Go/Pi, plus `claude-haiku-5-5` through official Claude Code.
- **Online trio:** `deepseek-v4.1-flash`, `mimo-v2.6-flash`, `qwen3.8-flash`
  through OpenCode Go/Pi. Paid status does not relax their public-only context.
- **Public topic:** one Opus-written sentence of at most 20 words; words contain
  letters and apostrophes only, with an optional final period. File, path,
  code, change and bead names, including hyphenated identifiers, are refused.
- **Same perspectives:** existing state and supporting evidence, counter-evidence
  and missing evidence, and effects on the topic's documented boundaries;
  every model receives all three, with no per-model angle assignment.
- **Complete:** every required contribution and structured reconciliation is
  present and valid; unresolved human questions may still await phase 1a.
- **Claim:** a uniquely identified statement with kind `fact`, `assumption` or
  `judgement`, source, confidence and its basis; confidence is not proof.
- **Handoff item:** an interview obligation derived from a research decision
  or unresolved disagreement, linked to its originating claims.

## Topic contract

Finder 0 locates files/functions, applicable rules/ADRs, tests/gates and
neighbouring specs; each map entry is `path::symbol` or `path::section` plus
one sentence why. It locates and lists, without choosing a design.

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

All topic reports use: at most seven key claims (id, one-sentence statement,
evidence, kind, confidence with basis); counter-evidence; not read; relation
to neighbouring specs; questions for the spec classified `[DECISION]`, `[GAP]`
or `[DETAIL]`. Online reports mark the neighbour relation not assessable from
public-only input; they never receive neighbour identities to fill the field.

## Acceptance criteria

1. When Stage 2 exploration selects `feature` or `architectural`, phase 1 uses the research swarm.
   *Refuted by:* Either class produces only the single GLM exploration report.
   *Basis:* Q-4.
2. When Stage 2 exploration selects `bounded` or `spike`, phase 1 retains single GLM 5.3 Flash exploration.
   *Refuted by:* Either class starts a finder or swarm researcher.
   *Basis:* Q-4.
3. When exploration precedes the spec, the research header or explore-only `--class` argument supplies the class without requiring a spec or plan.
   *Refuted by:* Valid early input is refused because a later artifact is absent.
   *Basis:* Q-4; early-class evidence in research.md.
4. If class declarations are missing, invalid or disagree between argument, research and spec, Stage 2 exploration refuses before a model call.
   *Refuted by:* A malformed YAML header, empty class or conflicting declaration is silently overridden.
   *Basis:* Q-4; existing class contract.
5. When a swarm starts its topic research, a merged finder map precedes every topic researcher.
   *Refuted by:* A topic starts before the three finder outcomes and the Opus map are recorded.
   *Basis:* Q-7, topic 0.
6. When repository topics 1–8 run, each has independent DeepSeek Flash, MiMo Flash and Haiku 5.5 contributions.
   *Refuted by:* A topic is omitted, a model substituted, or one session supplies two seats.
   *Basis:* Q-7.
7. When reconciled research is published, it compares public practice, the documented overall architecture and neighbouring specs, naming unread evidence as gaps.
   *Refuted by:* Code summaries replace a comparison, or an unread neighbour is called absent.
   *Basis:* Q-3; Q-7, topics 4, 5 and 9.
8. While an online researcher runs, no repository-derived content except the accepted public topic reaches its model or web requests.
   *Refuted by:* A canary from rules, paths, identifiers, finder output, history or private reports appears in an outbound payload or query.
   *Basis:* Q-3, Q-6, Q-8.
9. While an online researcher runs, no available tool or automatic context route can obtain repository files, git data or other private local content.
   *Refuted by:* A file or shell tool is available, ambient context is discovered, or fetching reaches local files or private network addresses.
   *Basis:* Q-3, Q-8.
10. When public evidence supports a claim, it has a successful page-retrieval receipt containing URL, title, retrieval date and excerpt or locator.
   *Refuted by:* A snippet, invented URL, search-only receipt or memory-only report counts as retrieved evidence.
   *Basis:* Q-7, topics 9–11; existing F-3 correction.
11. If a role has an undeclared or incompatible endpoint, model or data permission, the runner refuses that call.
   *Refuted by:* Online Qwen receives the framework packet or a model outside its declared role is launched.
   *Basis:* Q-3, Q-8, Q-9.
12. If the exact-prompt leak check immediately before any model call is not clean, the run exits 2 and dispatches no further call.
   *Refuted by:* One scan covers several prompts, or queued work starts after a BLOCK.
   *Basis:* Q-7 concurrency answer; existing leak-check contract.
13. When any model invocation is attempted, its durable record identifies run, input state, role, topic, endpoint, model, individual leak check and outcome.
   *Refuted by:* Concurrent output cannot be assigned to a slot, or a failed slot is audited as successful.
   *Basis:* Q-7 concurrency answer; existing audit contract.
14. When the research is reconciled, one fresh Opus 5.5 context covers topics 1–11 and the finder map.
   *Refuted by:* Another model judges, a peer session is resumed, or a required topic disappears.
   *Basis:* Q-5, Q-7.
15. When cited evidence leaves a disagreement unresolved, the reconciliation preserves the opposing claims and evidence as unresolved.
   *Refuted by:* A majority erases a sourced objection or the judge writes a maintainer answer.
   *Basis:* Q-5, Q-7 report and interview addenda.
16. When local claims are published, their path and symbol or section references resolve against the recorded frozen input state.
   *Refuted by:* Only line numbers, nonexistent symbols, a different source state or missing original reports support a claim.
   *Basis:* Q-7 report template; existing source contract.
17. While the swarm explores, only the runner appends research and pre-existing repository content outside that artifact remains unchanged.
   *Refuted by:* A participant edits a file, rewrites an answer, replaces earlier research or changes git or tracker state.
   *Basis:* Q-7 finder and topic boundaries; existing writer contract.
18. If a required call, retrieval or structured result fails, the run preserves partial evidence and names every missing slot in an incomplete result with nonzero exit.
   *Refuted by:* Timeout receipts are discarded, a URL-free online report succeeds, or malformed output yields a complete run.
   *Basis:* Q-7; existing failure contract.
19. When a swarm executes, it respects a recorded finite invocation budget and deadlines without retries or extra debate.
   *Refuted by:* An extra role, recursive delegation, retry or invocation after the total deadline occurs.
   *Basis:* Q-7 concurrency answer; finite-budget detail below.
20. When exploration explicitly uses `--stage2-off [REASON]`, it keeps single Haiku 5.5 exploration and records route, model and reason for the plan.
   *Refuted by:* It runs a swarm, reads a foreign key, names Haiku 4.5 or loses the reason.
   *Basis:* Q-4; neighbouring haiku-5-5 spec, criterion 1.
21. When outputs contain a used credential, durable records and diagnostics redact the whole credential and every fragment of eight or more characters.
   *Refuted by:* A planted fragment survives in an answer, receipt, concurrent log or error.
   *Basis:* Existing credential contract.
22. When delivered, phase-1 doctrine, endpoint roles and exactly one new research-swarm ADR describe the same amended workflow.
   *Refuted by:* Six-topic or free-through-Pi instructions remain operative, the review ladder changes, or an accepted ADR is edited.
   *Basis:* Q-7, Q-8, Q-9.
23. Before any online research call, a fresh Opus 5.5 call supplies a recorded public topic that passes the single-sentence, at-most-20-word, no-file-or-code-name filter and leak check.
   *Refuted by:* An absent, rejected, hyphenated-identifier-bearing or privately augmented topic reaches an online model.
   *Basis:* Q-6, retained by Q-8.
24. When finder step 0 runs, DeepSeek Flash, MiMo Flash and Haiku 5.5 independently locate the four agreed source categories for Opus 5.5 to merge.
   *Refuted by:* A finder judges the design, only one searches, or files/functions, rules/ADRs, tests/gates or neighbouring specs are missing without an unread marker.
   *Basis:* Q-7, topic 0, option A.
25. When a researcher receives a topic, its questions and permitted evidence scope match that topic in the topic contract below.
   *Refuted by:* Code/reuse proposes new code, an online report judges local applicability, or a neighbour report inspects unrelated implementation.
   *Basis:* Q-7 topic walk-through.
26. When models work the same topic, they receive identical task briefs, evidence packets, perspectives and report templates in fresh contexts without peer reports.
   *Refuted by:* One model receives a critique-only angle, a different initial map or a peer answer.
   *Basis:* Q-7 same-perspectives addendum.
27. When a topic report is accepted, it uses the fixed template with at most seven identified key claims and all required evidence and uncertainty fields.
   *Refuted by:* An eighth claim, duplicate id, missing confidence basis, omitted unread section or untyped question is accepted.
   *Basis:* Q-7 template acceptance.
28. When Opus reconciles topic reports, research retains per-topic, per-model supported, refuted, unique and off-brief scores traceable to claim ids.
   *Refuted by:* Scores have no claim basis, omit a model, or turn agreement into proof without source evaluation.
   *Basis:* Q-7 scoring acceptance.
29. When finder or topic 5 proposes neighbours, research distinguishes header-given neighbours, suggestions, confirmations and rejected suggestions with reasons.
   *Refuted by:* A finder suggestion silently becomes authoritative or a header-given neighbour is dropped.
   *Basis:* Q-7 finder and topic 5.
30. When phase 2 writes a spec from a completed swarm, its `neighbours:` header preserves the confirmed research neighbours as repository-relative spec paths.
   *Refuted by:* A confirmed neighbour disappears, a path escapes the repository, duplicates remain or a suggestion is silently promoted.
   *Basis:* Q-7 neighbours addendum.
31. When a completed swarm hands off to the interview, every research `[DECISION]` and every unresolved model disagreement has an identified interview item with its source claim ids.
   *Refuted by:* A class disagreement or neighbour contradiction is omitted, or a question loses its originating claims.
   *Basis:* Q-7 interview and template addenda; topics 3 and 5.
32. When verification checks a swarm handoff, each required interview item has a linked, answered maintainer record before the spec can pass.
   *Refuted by:* Class minimums alone pass while a research decision is lost, an open or agent-written answer is accepted, or an agent waives a required question.
   *Basis:* Q-7 lost-decision gate acceptance.
33. If a handoff or its decision links cannot be read or have ambiguous identities, the handoff gate reports not measured with exit 3.
   *Refuted by:* A malformed inventory, duplicate claim id, missing linked file or ambiguous answer silently passes.
   *Basis:* Q-7 lost-decision gate; repository unmeasured convention.
34. When phase 2 defines acceptance criteria from swarm research, each criterion names the supporting claims or answered interview records.
   *Refuted by:* A criterion lacks an origin, refers to a missing claim or depends on an unanswered research decision.
   *Basis:* Q-7 traceability acceptance.
35. When topic 6 finds a stale fact that changes repeatedly, it proposes central declaration, runtime lookup or dated evidence with an age warning, for a maintainer decision.
   *Refuted by:* A model id is silently replaced, a changing fact is treated as timeless, or a repository-wide policy is implemented without a human answer.
   *Basis:* Q-7, topic 6 addendum.
36. While a stage executes concurrently, at most four invocations per provider are in flight and new dispatch stops on a security refusal.
   *Refuted by:* A fifth OpenCode Go call starts across role groups, or queued work starts after a leak/declaration refusal.
   *Basis:* Q-7 concurrency option A.
37. When online topics 9–11 run, each has independent DeepSeek Flash, MiMo Flash and Qwen 3.8 Flash contributions through Pi on the same public-only brief.
   *Refuted by:* A free model, OpenCode CLI, Haiku or omitted vendor replaces one of the nine scheduled contributions.
   *Basis:* Q-8, Q-9.

## Non-goals

- Free models or the OpenCode CLI: Q-8 defers that separately; no dynamic free
  discovery, disguised client or automatic substitution is built here.
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
  move with `docs/adr/0019-phase-1-research-swarm.md`; approvals remain pending.
- The offline capture on real pinned Pi with synthetic private canaries,
  outbound payloads, tool schemas and failure probes passes before merge;
  stand-ins alone do not qualify isolation. Open phase-6 finding F-1 remains
  open until this evidence exists; the maintainer attends that separate step.
- After merge, a public-only live qualification records actual model and web
  outcomes; until success no complete live swarm is claimed. This draft calls
  no external model and does not claim runtime availability.
- PR file review confirms protected areas/non-goals, names the bead, records
  test/capture commits and keeps final `Closes-Bead: coding-harness-icw`.

## Open decisions

None open. The maintainer's Q-7–Q-9 explicitly amend the earlier topic/model
criteria; this redraft does not change them to pass a gate. I choose and
record the following reversible details with their reasons.

- [DETAIL] Keep `architectural`, the existing 12-hour phase-4 appetite and ADR
  claim; the new finder and handoff boundary strengthen the same subsystem.
  Earlier implementation time counts; a redraft does not reset that stop.
- [DETAIL] Stages are finder trio, Opus map merge, Opus topic sentence, topic
  research, Opus reconciliation. Repository and online topics may share the
  topic stage because neither consumes the other's reports; the judge alone
  combines them. Same-topic peers see identical frozen inputs and no answers.
- [DETAIL] The fixed run has 39 invocations: 3 finder, 1 map merge, 1 public
  topic, 24 repository, 9 online and 1 judge (Q-7–Q-9, 2026-10-15). Provider
  queues cap OpenCode Go and Claude separately at four, across all roles.
  Deadlines remain 5 minutes for topic author, 10 for finder/researcher/map
  merge, 15 for judge and 150 total, monotonically measured, no retries.
- [DETAIL] The report template and identical perspectives above implement
  the comparison baseline the maintainer requested, without model ranking.
  Finder output uses the four locator lists instead of the seven-claim cap.
- [DETAIL] Use `neighbours:` as a unique YAML list of worktree-relative spec
  paths; missing means no given neighbours, an unread/invalid path is a gap
  that prevents a complete comparison. Suggestions remain separate until
  topic 5 and the judge confirm them with evidence; no human choice is
  inferred. The two header entries here were read locally for this redraft.
- [DETAIL] Version new run manifests as `research-swarm/v2`. Retain all raw
  claims and a distinct handoff inventory; the gate checks every such run
  in live and archived change folders, leaving pre-schema evidence intact.
  A required item links to an answered maintainer Q-record via claim/item
  ids; an explicit human rejection can be that answer, an agent waiver cannot.
- [DETAIL] Review checks the fidelity of a question/answer and criterion
  rationale; the gate checks identities, coverage and answered status only.
  Minimum counts stay minima: all derived obligations may need more questions.
- [DETAIL] Online contexts retain scratch isolation and only public-web tools
  even though their Go endpoint also permits framework roles; permission is
  selected per role and never inferred from billing or discovery.
