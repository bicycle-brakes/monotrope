---
title: "Spec — research-swarm"
status: draft
implementation_status: partial
date: 2026-10-14
last_reviewed: 2026-10-18
updated: 2026-10-23
supersedes: null
superseded_by: null
bead: coding-harness-icw
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-18"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, research, swarm]
class: architectural
appetite: 17.333333333333332  # hours; exact operational total: 17 hours 20 minutes (maintainer, 2026-10-18, Q-14)
adr_files: [docs/adr/0020-phase-1-research-swarm.md]
neighbours: [plans/changes/interview-context/spec.md, plans/changes/haiku-5-5/spec.md]
---

# Spec — research-swarm

Phase 1 maps the sources, compares independent topic research and carries its
questions and evidence into the interview and spec (bead coding-harness-icw).
Authority: [decisions.md](decisions.md), Q-1–Q-14; Q-7 amends the six-topic
pairs, Q-8/Q-9 select three Go Flash models, and Q-10 adds dynamically
selected Go free models to online topics only, excluding Zen. Q-11 obtains
tool support and deprecation from models.dev, cross-checked with fresh Pi.
Q-12 replaces both fixed trios with per-seat models and a reported
reachability selection before each run; Q-14 makes each seat declare one
preferred model and draws any substitute from the admitted paid Go models of
the live catalog, cheapest first. Q-13 keeps every finished contribution
durably so a later run with the same inputs reuses it.
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
  39 required contributions; a failed Pi refresh still blocks the run.
- Existing interview minimums count answers but cannot prove that research
  decisions survived; prompts do not yet carry a checked research-to-spec
  link (research, redraft addendum; Q-7).
- Both research trios are fixed, so one unavailable member ends every run
  incomplete with exit 1; on 2026-10-18 `qwen3.8-flash`, a fixed online
  member, could not be called because its wire API is not measured, while
  DeepSeek Flash, MiMo Flash, LongCat 2.0 and MiMo Pro answered (Q-12).
- Reports stay buffered in memory until a stage ends, and nothing resumes, so
  a run cut off by a token or quota limit loses every finished contribution
  and repeats its spend (Q-13).

## Terms

- **Seat:** one of the six required model positions of a run, each
  declaring exactly one **preferred model**, an `{endpoint, model}` pair in
  `model-endpoints.yaml`, and no fallback list (Q-14). The three
  **repository seats** work the finders and topics 1–8; their model runs on
  `opencode-go` through Pi or on `claude-code-plan` through official Claude
  Code. The three **online seats** work topics 9–11; their model runs on
  `opencode-go` through Pi with public-only permissions regardless of
  billing. The repository seats form the repository trio and the online
  seats the online trio.
- **Online researchers:** the three online seats plus selected Go free
  models.
- **Admitted Go model:** an `opencode-go` id without a `-free` suffix. It
  has a `modelle_terms` record that passes the review swarm's terms check:
  a dated reading with source, retention and training "Not used", and no
  `uebersprungen` skip mark. The record carries a positive `anfragen_5h`
  cost value. This preparation's fresh Pi overlay lists the id as text-input
  chat with the declared Go origin and a wire API in the declared measured
  set (`openai-completions` as of 2026-10-18). The terms record is the only
  manual step; nothing else needs an edit. A `claude-code-plan` preferred
  model is admitted by its endpoint declaration and the endpoint's
  `framework` permission.
- **Substitute pool:** every admitted Go model whose models.dev entry under
  `opencode-go.models` has `tool_call: true` and no `status: deprecated`
  (Q-11's source and rules), ordered by cost: `anfragen_5h` descending,
  ties by id, the review swarm's order. Both trios draw on the same pool.
  Without a usable models.dev result the pool is empty; preferred models
  stay unaffected.
- **Reachable:** an admitted model whose reachability probe in this
  preparation ended successfully within 60 seconds. A probe sends the fixed
  probe text alone, with no tools and no repository content.
- **Selection:** per trio, first every seat takes its preferred model when
  it is admitted, not under a timed exclusion and reachable. Then each
  remaining seat, in declared order, takes the first pool model that is not
  under a timed exclusion, is reachable and is not already selected for a
  seat of the same trio, reported as "substitute for <seat>". Preparation
  records the selection with the catalog result in a single-use **selection
  receipt** that a run consumes; the selection is then frozen for that run.
- **Selected Go free models:** unique `opencode-go` ids ending exactly `-free`
  in this run's freshly fetched remote overlay, filtered by include/exclude.
  They must be text-input chat models in fresh Pi and have an entry keyed by
  the exact Pi id
  under models.dev's `opencode-go.models`, with a present `id` equal to its
  key, `tool_call: true` and without
  `status: deprecated`. Baseline-only ids, non-chat models, missing metadata,
  absent/negative support and deprecated models are excluded with reasons.
  A malformed Pi candidate is excluded as `pi-malformed`; a malformed
  models.dev candidate is excluded as `metadata-malformed`. A repeated overlay
  id is an ambiguous Pi result and blocks every model call; document-level
  failures and per-entry rules are listed under Open decisions.
  If models.dev is unavailable or unreadable, exclude all free candidates and
  record `N=0` with that reason; subject to explicit-include requirements,
  the 39 required slots remain. Pi refresh failure
  cannot use this fallback. Preparation probes every policy-selected, unexcluded
  free candidate with the real-size online-topic request, using a fixed public
  sentence and asking only for OK, without tools or private content. The first
  attempt allows 120 seconds; only a timeout gets one retry of 360 seconds.
  Failed candidates are named with their reasons and removed before freezing
  the selection and `N`. `N` is the count that passed preparation, not a
  guarantee that later topic calls succeed (maintainer, 2026-10-22).
- **Required contribution:** one of the 39 required slots (3 finder, map
  merge, public topic, 24 repository-seat, 9 online-seat, judge). The
  additional `3N` free slots are best-effort; each still requires a recorded
  terminal outcome.
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
  Evidence forms are `path::symbol`, `path::section`, a full commit hash in
  topic 6's runner-collected history packet, or a receipt-backed public URL.
  A PR number or bead id alone is unsupported, since neither service is read.
- **Resolves:** `path::X` uses the frozen file's type, with exact,
  case-sensitive identities. In Markdown (`.md`), X equals exactly one
  heading's text after removing leading `#` marks, an optional closing run
  of `#` marks and outer whitespace; inline formatting remains literal.
  Headings are ATX lines outside front matter and fenced code blocks; setext
  and HTML forms are not recognised. The exact scan is recorded below. Its excerpt ends before the next heading
  of the same or higher level, or at EOF. `criterion <n>` also resolves to
  numbered item `<n>.` under the file's one `## Acceptance criteria` heading,
  ending before the next numbered item or heading. In Python (`.py`), X names
  an AST `def`, `async def`, `class` or module-level assignment target; dotted
  names select nested definitions such as `Class.method`. Its excerpt is the
  node's lines. In YAML (`.yaml`, `.yml`) and JSON (`.json`), X is a parsed
  dotted key path split at every dot, each segment matching a string mapping
  key exactly; dotted keys and list indices cannot be named, so cite their
  nearest citable parent. Dates/timestamps become ISO 8601 text. Duplicate
  keys, JSON NaN/infinity, or values without a JSON form (including binary,
  sets or any non-string key) make the reference unsupported. Canonical JSON
  uses sorted keys, unescaped non-ASCII, two-space indentation, separators
  `,` and `: `, and no trailing newline. Duplicate
  matching headings, criterion items, definitions or key paths are ambiguous
  and unsupported.
  For other files, including shell, Makefile, JavaScript and TOML, X must
  occur as a whole word; the excerpt starts at the first matching line and
  runs to EOF before applying the claim cap. Missing, unparseable or otherwise
  unsupported references confer no evidence or map scope. All excerpts share
  the 4,000-character per-claim cap and truncation flag. These same rules
  govern finder resolution, topic scope, report evidence floors and bases.
- **Neighbour spec:** exactly `plans/changes/<name>/spec.md` (one segment,
  excluding `archive`), `plans/changes/archive/<YYYY-MM-DD-name>/spec.md`,
  or `plans/specs/<capability>/spec.md`. The change's own spec is excluded.
  Given paths must also exist in frozen bytes; handoff paths are checked for
  form without a later existence requirement, so archival does not invalidate
  historical answers.
- **Neighbour status:** the runner alone derives each suggested packet
  neighbour's status from all three topic-5 relations in a complete run:
  a relation counts only if at least one of its listed claims is `valid`.
  `confirmed` requires three counting relations, all `related` or
  `contradicts`; `rejected` requires three counting relations, all `unrelated`;
  every other case, including fewer than three counting relations, is `split`. Each split
  derives a human neighbour item independently of the judge. A counting `contradicts` counts
  toward confirmation and still derives its own item. Given paths remain
  `given`; their relations derive obligations without changing that status.
  The judge describes relevance but cannot set or change status. A split
  enters the spec header only through a maintainer's structured keep answer.
- **Evidence status and disposition:** the runner marks a claim `valid` or
  `unsupported`; a claim is valid only if all its citations resolve locally
  or have successful online page receipts. One failing citation makes the
  whole claim unsupported, with no excerpt, disposition or criterion Basis;
  unsupported claims remain visible but are never evidence.
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
  same run/topic/seat namespace with local Q ids. A neighbour answer also
  carries `research_neighbours:` with up to three spec-path lists, `keep`,
  `drop` and `add`, beside the free-text answer. The recording session copies
  the maintainer's stated choice into these fields; the gate never infers it
  from answer prose. Each neighbour item closes only when a maintainer-answered
  Q-record links the item and names its path in `keep` or `drop`. `keep` and
  `add` require inclusion; `drop` requires omission, including for split paths.
  An `add` needs no item link, allowing drafting discoveries. A path in two
  lists of one record, or conflicting inclusion/drop directives across
  answered records, is ambiguous (exit 3). Paths outside the three neighbour
  forms fail with exit 1; form checking does not require later existence.
- **Frozen input state:** HEAD plus a digest of every tracked file and every
  untracked non-ignored file under this change folder. Copies live only in
  run scratch outside the repository, including uncommitted input bytes;
  local references resolve there during the run. Copies are deleted after
  publication or abort. HEAD, the full digest and per-path digests of untracked
  change inputs persist in the manifest; snapshot copies never enter research
  or briefs as additional records. Selected frozen brief inputs and bounded
  cited excerpts are not snapshot records. A failed copy exits 1 before any
  model call.
- **State store:** runner-owned durable storage outside the repository,
  its git directory and every model's working, home and agent directories.
  It holds one record per launch and one per terminal slot outcome of each
  run of the change. A slot's terminal record holds its identity, seat,
  endpoint, model, exact prompt hash, resume binding, outcome, UTC start
  and end, report or partial output, receipts and leak-check record.
- **Resume binding:** the per-path byte digests of the frozen input state.
  `research.md` is counted without the stored run's own exact appended
  bytes and without the `updated:` restamp. HEAD is not part of it: the
  prompt hash carries what HEAD changes in a packet, such as topic 6's
  history.
- **Reused slot:** a planned slot of a new run that takes a stored `ok`
  result instead of launching. The result must come from the latest stored
  run of the change. Its resume binding, stage, topic, seat, endpoint, model
  and prompt hash must equal the planned slot's, and its report must pass
  this run's validation.

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
Resolved neighbour-category entries inside an active change, archived change
or living-spec folder of the three Neighbour spec forms suggest that folder's
`spec.md` when it exists in frozen bytes. Entries for any of its artifacts
merge into one packet neighbour identified by that spec path, retaining all
map keys. Entries in this change's own folder are marked `self`, without
neighbour status, relation or gap. Other resolved entries outside those forms
or without a spec stay `no-spec` with a neighbour-comparison gap. Unresolved
entries grant no neighbour status. Topic 5 covers exactly the independently
derived union of these packet neighbours and header-given paths.

| Topic | Questions and evidence boundary |
|---|---|
| 1 Code and reuse | Existing functions/modules, analogous patterns, changes needed to reuse them and objections; mapped code plus direct imports, no new-code proposals. |
| 2 Callers and interfaces | Callers across code/tests/commands/CI/hooks/prompts, signatures/options/formats/configuration, readers versus changing callers, kit/instance consumers; connections to the map, with caller and callee cited. |
| 3 Rules and ADRs | Exact obligations, human-owned paths, required ADR changes and next number, conflicting rules, whether the declared class fits; repository rules only, no new rules; a class disagreement is a human decision. |
| 4 Architecture fit | Documented layer, prescribed runner/tracker/gate routes, framework/kit/instance responsibility and invalidated architecture statements; mapped code and documented architecture only, no target design. |
| 5 Neighbouring specs | Constraints, contradictions, overlap/order, shared resources and suggested-neighbour relevance; neighbours' spec/design/plan/decisions only; contradictions become human decisions; an empty packet still gets all three seats, with empty relations and an empty-packet not-read entry. |
| 6 History and stale assumptions | Last change and reason, reversals/supersession, stale facts, recorded rationale, governance of repeatedly changing facts; runner-collected mapped history only, cited by full packet commit hash or frozen `path::section`; proposals await the maintainer. |
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
can add obligations but cannot remove them. Suggested-neighbour statuses
follow the runner's Neighbour status rule, including a human item for each
split. A valid report needs at least one evidence-backed claim, except topic 5
when its packet holds no neighbour: all three seats still run with the same
"no packet neighbour" packet, `neighbour_relations: []` and a `not read` entry
naming that empty packet. Any claims remain checked and scored, including
off-brief claims; a nonempty relation list still fails the template. With any
packet neighbour, the evidence floor applies unchanged. Reconciliation records
"no neighbour given or found" as a named gap for the empty case. Other
unsupported claims remain with that status; a failed individual fetch alone
does not reject the report.

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
4. When exploration runs without `--stage2-off`, invalid class declarations or a swarm's invalid given-neighbour header, including a missing or non-list `neighbours:` key in research.md, cause refusal before a model call with exit 2 and a header-repair message.
   *Refuted by:* Malformed, missing or disagreeing classes pass, a missing/null/non-list neighbour key or duplicate, escaping, non-spec or missing frozen neighbour path starts a call, a given path outside the three Neighbour spec forms or this change's own spec starts a call, the message omits adding `neighbours: []` or a list of specs, or explicit `neighbours: []` is refused.
   *Basis:* `decisions.md#Q-4`; existing class contract.
5. When topic research starts, all three finders and the tool-free Opus map merge have valid recorded results whose finder keys form the exact union defined in the Topic contract.
   *Refuted by:* A failed finder/merge, missing map, dropped or added finder key, or duplicate key still lets a topic start; an Opus merge launches with any tool.
   *Basis:* `decisions.md#Q-7`, topic 0.
6. When repository topics 1–8 run, each has independent contributions from the three repository seats, each seat filled by its frozen selection.
   *Refuted by:* A topic is omitted, a seat runs a model other than its frozen selection, one session supplies two seats, or one candidate fills two seats of the topic.
   *Basis:* `decisions.md#Q-7`; `decisions.md#Q-12`.
7. When reconciled research is published, it contains public-practice, documented-architecture and neighbouring-spec comparison sections with named gaps for unread evidence.
   *Refuted by:* A comparison section or an unread-neighbour gap entry is absent, or an empty topic-5 packet lacks the named "no neighbour given or found" gap; semantic comparison quality is also checked in phase 6.
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
11. If a call's endpoint and model are not its seat's frozen selection, or a role has no compatible declaration or declared dynamic Go-free selection permission, the runner refuses that call.
   *Refuted by:* An online seat's model receives the framework packet, a model outside its seat's frozen selection or its role is launched, or a seat declaration or substitute grants a role a permission its endpoint lacks.
   *Basis:* `decisions.md#Q-3`, `decisions.md#Q-8`, `decisions.md#Q-9`, `decisions.md#Q-10`, `decisions.md#Q-12`.
12. If any immediately preceding exact-prompt leak check is not clean, dispatch stops and the run exits 2 after cancelling queues and stopping and reaping active children.
   *Refuted by:* One scan covers multiple prompts, a queued call starts after BLOCK, a running child is awaited instead of stopped, available partial output is lost instead of retained as cancelled, or exit 1 overrides exit 2.
   *Basis:* `decisions.md#Q-7` concurrency answer; existing leak-check contract.
13. When any model invocation is attempted, its durable record identifies run, input state, role, topic, endpoint, model, individual leak check and outcome.
   *Refuted by:* Concurrent output cannot be assigned to a slot, or a failed slot is audited as successful.
   *Basis:* `decisions.md#Q-7` concurrency answer; existing audit contract.
14. When the research is reconciled, one fresh tool-free Opus 5.5 context covers topics 1–11 and the finder map with a resolved evidence excerpt for each valid claim.
   *Refuted by:* Another model judges, a peer session is resumed, a required topic or valid claim's excerpt disappears, any file, shell, web or MCP tool is available, a packet over the recorded character limit reaches the judge, or excerpts are shortened beyond the per-claim cap to fit.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-7`.
15. When sourced disagreement remains unresolved, reconciliation retains its opposing global claim ids and evidence without an answer field.
   *Refuted by:* An unresolved disagreement loses an opposing claim id or evidence, or judge output contains a maintainer answer field; phase 6 also checks faithful treatment of dissent.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-7` report and interview addenda.
16. When local claims count as evidence, their path-qualified symbol or section resolves against the retained frozen bytes, or a topic-6 full commit hash resolves in that seat's bounded frozen-HEAD history packet.
   *Refuted by:* Unresolvable or line-only references, a hash absent from the topic-6 packet, or a PR number or bead id alone is valid evidence, a prose-only match in Markdown or Python or an ambiguous heading/definition/key path resolves, the excerpt differs from the type-specific extent, a line inside a fenced block or front matter counts as a heading, a duplicate or a criterion item, a dotted key, list index or value without a JSON form resolves, a date excerpt is not its ISO text or the excerpt is not canonical JSON, a claim with any unresolved citation or unreceipted URL is valid, history collection failure lets a topic start, a reference resolves against the live tree instead of scratch bytes, a report is absent, a changed frozen file permits complete publication, or a frozen-file copy is persisted in research or the change folder.
   *Basis:* `decisions.md#Q-7` report template; existing source contract.
17. While the swarm explores, only the runner appends research and pre-existing repository content outside that artifact remains unchanged.
   *Refuted by:* A participant edits a file, rewrites an answer, replaces earlier research or changes git or tracker state, or reachability preparation or the state store writes inside the worktree.
   *Basis:* `decisions.md#Q-7` finder and topic boundaries; `decisions.md#Q-12`; `decisions.md#Q-13`; existing writer contract.
18. If a required contribution fails, the run retains partial evidence and all missing-slot outcomes and ends incomplete with exit 1 unless a security refusal requires exit 2.
   *Refuted by:* A failed preparatory stage dispatches a later stage, missing required topic reports still reach the judge, a report with zero evidence-backed claims passes except a topic-5 report whose packet holds no neighbour, a failed free seat alone makes the run incomplete, or an oversized judge packet loses evidence or fails to end incomplete with `judge-packet-over-limit` and no judge call.
   *Basis:* `decisions.md#Q-7`; existing failure contract.
19. When a swarm executes, its maximum 39 + 3N invocations follow the finite deadlines, required-first dispatch and reserved 15-minute judge allowance without retries or debate.
   *Refuted by:* An extra invocation or retry occurs, a free slot starts ahead of queued required slots, topic work consumes the judge reserve, or unlaunched slots lack not-started-deadline outcomes.
   *Basis:* `decisions.md#Q-7` concurrency answer; `decisions.md#Q-10`; finite-budget detail below.
20. When exploration explicitly uses `--stage2-off [REASON]`, it keeps single Haiku 5.5 exploration and records route, model and reason for the plan.
   *Refuted by:* It runs a swarm, reads a foreign key, names Haiku 4.5, loses the reason, requires or validates a class or neighbours header, or accepts a `--class` or `--availability-reported` argument beside `--stage2-off`.
   *Basis:* `decisions.md#Q-4`; `decisions.md#Q-12`; neighbouring haiku-5-5 spec, criterion 1.
21. When outputs contain a used credential, durable records and diagnostics redact the whole credential and every fragment of eight or more characters.
   *Refuted by:* A planted fragment survives in an answer, receipt, concurrent log, error, probe record, selection receipt or state-store record.
   *Basis:* Existing credential contract; `decisions.md#Q-12`; `decisions.md#Q-13`.
22. When delivered, phase-1 doctrine, endpoint roles and exactly one new research-swarm ADR describe the same amended workflow.
   *Refuted by:* Six-topic, fixed-trio or Zen-free-through-Pi instructions remain operative, the preparation and resume steps are missing from phase-1 doctrine, the review ladder changes, or an accepted ADR is edited.
   *Basis:* `decisions.md#Q-7`, `decisions.md#Q-8`, `decisions.md#Q-9`, `decisions.md#Q-10`, `decisions.md#Q-12`, `decisions.md#Q-13`.
23. When any online call is about to start, fresh tool-free Opus must already have supplied a recorded public topic passing the defined word and name filters and exact-prompt leak check.
   *Refuted by:* An absent, rejected or privately augmented topic reaches an online seat; the author has any tool; research-swarm, a bead id or a sentence with `[`, `{`, `@`, `=` or a digit passes; Container-Isolation für KI-Agenten-Läufe or Isolation, Prüfung und Wiederherstellung für Agentenläufe fails the character rule; rejection fails to stop pre-topic dispatch with exit 1.
   *Basis:* `decisions.md#Q-6`, retained by `decisions.md#Q-8`.
24. When finder step 0 runs, the three repository seats, each with its frozen selection, independently receive the same private change brief and four-list locator template for Opus to merge.
   *Refuted by:* Only one finder runs, an output has fields beyond the four locator lists, an empty category lacks an unread marker, an unresolved map entry grants topic scope, a given neighbour is missing from the runner's map, or topic 5's packet-neighbour list differs from an independent derivation from the resolved map and given header; prose design judgements are off-brief and reviewed in phase 6.
   *Basis:* `decisions.md#Q-7`, topic 0, option A; `decisions.md#Q-12`.
25. When a researcher receives a topic, its packet matches the checked-in questions and permitted evidence scope of the Topic contract.
   *Refuted by:* A packet differs from its topic prompt; report prose that proposes new code or local applicability outside that scope is scored off-brief and checked in phase 6.
   *Basis:* `decisions.md#Q-7` topic walk-through.
26. When models work the same topic, their fresh contexts contain identical task briefs, evidence packets, embedded instructions, perspectives and templates without peer reports or automatic instruction loading.
   *Refuted by:* One model receives a different map, instruction file, angle or peer report, or its runtime auto-loads instructions.
   *Basis:* `decisions.md#Q-7` same-perspectives addendum.
27. When a topic report is accepted, its fixed template and report-local identities satisfy every required field and topic-specific field.
   *Refuted by:* An eighth claim, duplicate local claim/question id, invalid question claim link, missing confidence basis or unread section, absent topic-3 class assessment, incomplete/duplicate/extra topic-5 neighbour relation or empty relation claims, a topic-5 empty packet with any relation or without its empty-packet not-read entry, a nonempty topic-5 packet with no evidence-backed claim, or ungoverned volatile topic-6 claim is accepted.
   *Basis:* `decisions.md#Q-7` template acceptance.
28. When Opus reconciles reports, per-topic per-model claim lists and counts distinguish supported, refuted, unique, off-brief, unresolved and unsupported claims.
   *Refuted by:* A valid claim has two dispositions, a unique claim is not supported, an unsupported claim is supported, a score lacks claim ids, a valid claim lacks its resolved evidence excerpt with truncation marked where needed, or a failed seat has no named outcome.
   *Basis:* `decisions.md#Q-7` scoring acceptance.
29. When neighbour relevance is reconciled, research preserves given paths and distinguishes suggested neighbours as runner-derived confirmed, rejected or split statuses with reasons.
   *Refuted by:* A suggestion with any unrelated seat is confirmed, an all-unrelated suggestion with three counting relations is not rejected, a relation whose claims are all unsupported counts toward confirmed or rejected, a split lacks a human item, a judge verdict sets or changes status, a given neighbour disappears, a topic-5 contradicts or unrelated-given entry has no human item even when all its claims are unsupported, a cross-run confirmation/rejection conflict or later omission of a given path yields no human item, an ineligible suggestion becomes a packet neighbour, or a resolved eligible-folder entry with a frozen spec is wrongly marked no-spec/self or yields no packet neighbour even when a gap is listed.
   *Basis:* `decisions.md#Q-7` finder and topic 5.
30. When a spec uses complete v2 research, the handoff gate requires its neighbours header to equal paths confirmed or given in any complete run, plus keep and add paths, minus drop paths, in maintainer-answered Q-records' research_neighbours fields.
   *Refuted by:* A required path disappears, an escaping/duplicate path or unkept split/unconfirmed suggestion enters, a path outside those sets passes, a linked neighbour item closes without its path in keep/drop, a prose-only addition passes, an add without an item link is refused, an earlier confirmation rejected later yields no handoff item, or a prior given path leaves the required set without a structured human drop; such findings exit 1, while conflicting inclusion/drop directives must exit 3.
   *Basis:* `decisions.md#Q-7` neighbours addendum.
31. When complete v2 research hands off, every accepted raw-report DECISION question, unresolved judge disagreement, class mismatch, neighbour contradiction or split, cross-run confirmation/rejection conflict or omission of an earlier given neighbour has a claim-linked inventory item.
   *Refuted by:* A refuted/off-brief report decision is omitted, a differing class, topic-5 contradicts/unrelated-given field, split or either cross-run neighbour conflict lacks an independently derived item, or grouping duplicates loses a source question or claim id.
   *Basis:* `decisions.md#Q-7` interview and template addenda; topics 3 and 5.
32. When spec.md exists, the handoff gate requires coverage and linked answered maintainer records for every obligation of every complete v2 run in that change.
   *Refuted by:* Class minimums hide a lost item, a later run erases an earlier obligation, an open/agent answer passes, no complete run exists despite v2 runs, or pending items turn a pre-spec change red.
   *Basis:* `decisions.md#Q-7` lost-decision gate acceptance.
33. If v2 evidence or its links are unreadable or identities ambiguous, the handoff gate reports not measured with exit 3.
   *Refuted by:* Malformed manifests/inventories, duplicate global ids or report-local ids, missing linked files, ambiguous answers, a neighbour path in two lists of one Q-record or conflicting inclusion/drop directives across answered records silently pass.
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
37. When online topics 9–11 run, each has independent contributions from the three online seats through Pi on the same public-only brief, each seat filled by its frozen selection.
   *Refuted by:* A free model, OpenCode CLI, Claude Code, an omitted seat or a model other than the seat's frozen selection supplies one of the nine required online contributions; added free seats cannot replace them.
   *Basis:* `decisions.md#Q-8`, `decisions.md#Q-9`, `decisions.md#Q-12`.
38. When any swarm model call is about to start, including a reachability probe, the two-source catalog record of this run's preparation already holds a successful fresh pinned-Pi Go overlay, Pi source/UTC time/digest, models.dev source/UTC time/digest or failure, the catalog outcome of each preferred Go model and each paid Go model of the overlay, and each free candidate's selected/excluded outcome with exclusion reason and source field/value.
   *Refuted by:* A cached/shipped list substitutes for refresh, a baseline-only free id or another provider supplies a seat, a preferred or pool Go model absent, baseline-only, non-chat or malformed in the fresh overlay is probed or selected instead of skipped with its reason and raw value, models.dev decides a preferred model's eligibility, or at any N the manifest lacks either source's dated provenance/outcome or an excluded candidate's reason and source value.
   *Basis:* `decisions.md#Q-10`; `decisions.md#Q-11`; `decisions.md#Q-12`; `decisions.md#Q-14`.
39. When N Go free models are selected, each has an independent best-effort slot on topics 9–11 with the online seats' brief and a recorded terminal outcome.
   *Refuted by:* A selected seat is silently omitted or failed as successful, a non-selected/no-tool-support/deprecated model runs, peer briefs differ, or a missing explicit include starts any model instead of preflight exit 1.
   *Basis:* `decisions.md#Q-7` same-perspectives addendum; `decisions.md#Q-10`; `decisions.md#Q-11`.
40. While selected Go free models participate, they receive only the public-only role permissions and cannot fill a finder, repository-seat, online-seat, author, merge or judge position.
   *Refuted by:* A free seat inherits the Go endpoint's framework permission or receives a private packet, map or report, or a `-free` id is accepted as a seat's preferred model or substitute.
   *Basis:* `decisions.md#Q-3`; `decisions.md#Q-10`; `decisions.md#Q-12`.
41. If the live Pi catalog cannot be measured reliably, the runner preserves diagnostics and exits 1 before any swarm model call, reachability probes included.
   *Refuted by:* A Pi timeout, stale-only, malformed or ambiguous result becomes valid zero availability, a fallback roster or a probe, the failure exits 0, 2 or 3, a successful Pi refresh with only an unfinished models.dev read exits 1, or a repeated overlay id lets any model call start; absence of a tool-support field in Pi is not a Pi failure under Q-11.
   *Basis:* `decisions.md#Q-10`; `decisions.md#Q-12`; existing failure contract.
42. When fresh Pi yields an empty free selection after capability checks and policy with no unmet explicit include, including models.dev absence or failure, the run records N=0 and its measured-empty or capability-unavailable reason and keeps all 39 required slots.
   *Refuted by:* A missing models.dev model, missing/mismatched id, absent/false/non-boolean tool_call or deprecated status admits a free seat, one malformed models.dev or Pi candidate excludes a valid candidate or blocks the required slots, a repeated raw key or equal id under different keys leaves any candidate selectable instead of capability-unavailable/duplicate-id, document-level metadata failure is recorded as measured absence, models.dev failure alone blocks required slots, its timeout delays them beyond catalog's 60 seconds or exits nonzero by itself, or N=0 revives a prior roster or omits a required slot.
   *Basis:* `decisions.md#Q-10`; `decisions.md#Q-11`.
43. When a swarm run is prepared, each of the six seats receives its Selection as defined in Terms, and the three finder slots use the repository seats' selections.
   *Refuted by:* A substitute replaces a preferred model that is admitted, unexcluded and reachable; a substitute takes a model that is another seat's reachable preferred model; a model that is not admitted, lies outside the fresh overlay, uses an unmeasured wire API or is under a timed exclusion is probed or selected; one model fills two seats of the repository trio or two of the online trio; a finder runs a model other than its repository seat's selection.
   *Basis:* `decisions.md#Q-12`; `decisions.md#Q-14`.
44. When preparation fills every seat, it prints a selection report and writes a single-use receipt bound to the worktree, change, endpoint configuration, class and given neighbours. A swarm run starts only when `--availability-reported` names that receipt's id within the declared maximum age.
   *Refuted by:* The report omits a seat's selection, the "substitute for <seat>" mark of a substitute, a skipped, excluded, unreachable or unprobed model's reason, the substitute pool in cost order, the free selection or the UTC check time; a research call starts without the matching id, after the maximum age, after a change to any bound input, from another worktree or from an already consumed or corrupt receipt; that refusal exits other than 2; a bounded, spike or `--stage2-off` exploration requires or accepts a receipt id.
   *Basis:* `decisions.md#Q-12`; `decisions.md#Q-14`.
45. If any seat is left without its preferred model and without a reachable, unexcluded pool model not already selected in its trio, preparation names each such seat with the reasons for its preferred model and every pool model, leaves no usable receipt and exits 1 before any research call.
   *Refuted by:* A receipt from this or an earlier preparation stays usable, a research call starts, an empty seat is not named, the exit code is not 1, or the seat is filled by a model outside its preferred model and the substitute pool, such as a free model or a model without a terms record.
   *Basis:* `decisions.md#Q-12`; `decisions.md#Q-14`; the exit scheme of criteria 41 and 18.
46. While a run executes, every required slot uses its seat's selection from the consumed receipt, and the run manifest records the receipt id, check time, each seat's selection and every candidate's outcome.
   *Refuted by:* A selected model that fails or times out is replaced by another model, retried or probed again; a later preparation changes a running run's models; the manifest lacks the receipt id, a seat's selection with its preferred or substitute mark, or a model's reason.
   *Basis:* `decisions.md#Q-12`; `decisions.md#Q-14`; existing no-retry contract.
47. When a required-seat reachability probe runs, it sends only the fixed probe text, with no tools, no repository content and no change identity, from a fresh scratch working directory without instruction auto-loading, through the pinned Pi wrapper or official Claude Code, within 60 seconds and after its own exact-prompt leak check and audit record.
   *Refuted by:* A canary from the change, AGENTS.md, a repository path, the map or the public topic reaches a probe's payload, argv or environment; any tool is available; a bare `pi` or an unofficial Claude client runs; a probe lacks its leak check or audit record or runs past 60 seconds; a Claude Code preferred model counts as reachable without a probe.
   *Basis:* `decisions.md#Q-12`.
48. When preparation probes, required-seat and pool probing stays lazy and shared across trios. A pool model is probed only while a seat needs a substitute and every cheaper usable pool model is known unreachable or already selected in that trio. Every policy-selected, unexcluded Go free candidate is also probed with the real-size online-topic request and a fixed public sentence, asking only for OK without tools or private content: 120 seconds, with one 360-second retry only after a timeout. A failed free probe names its reason and removes the candidate from the frozen selection and N without blocking required seats. Opus roles are never probed; records stay outside the worktree and probes count outside the run's `39 + 3N` invocations.
   *Refuted by:* A pool model is probed while no seat needs it or a cheaper usable model is untried; a selected free candidate escapes probing, receives a short probe instead of the real-size request, exceeds those limits or retries a non-timeout failure; a failed free candidate remains in N or blocks required seats; an excluded or ineligible candidate or Opus role is probed; preparation changes a worktree file; probes consume run slots.
   *Basis:* `decisions.md#Q-12`; `decisions.md#Q-14`; maintainer decision of 2026-10-22 to probe free models with the real-size request (bead coding-harness-k9rw).
49. If a seat declares no preferred model, more than one model or any fallback or substitute list, or its preferred model is undeclared by its endpoint, a `-free` id, an online model outside `opencode-go` or a repository model on an endpoint without `framework`, or the maximum age, the measured wire-API set or a timed exclusion is malformed, preparation and explore refuse with exit 2 before any model call.
   *Refuted by:* Such a declaration lets a probe or research call start, a declared fallback or substitute list is accepted or consulted, or the refusal exits other than 2.
   *Basis:* `decisions.md#Q-12`; `decisions.md#Q-14`; existing declaration contract.
50. When research preparation is delivered, its rule validation, timed-exclusion matching, tool-free probe and receipt sealing and verification are the functions the review swarm's availability preparation uses wherever that preparation exists on the base branch, and the review swarm's availability tests pass unchanged.
   *Refuted by:* A branch that holds both swarms carries two implementations of any of these functions, or a review availability test is changed or fails.
   *Basis:* `decisions.md#Q-12`, "the same form as the review swarm's availability preparation".
51. When a slot reaches its terminal outcome, its State store record is written atomically and durably before the worker that ran it launches another slot, and every launch is preceded by a durable launch record.
   *Refuted by:* After the runner is killed with SIGKILL following a slot's terminal outcome, that slot's record is missing or torn; a temporary or torn file reads as a result; a launch has no prior launch record; the same worker launches its next slot before the write returns.
   *Basis:* `decisions.md#Q-13`.
52. While any model of a run is running, no store path, run directory name or stored result reaches a model's prompt, argv, environment or working directory before its stage barrier, and the store is readable by its owner only.
   *Refuted by:* The store lies inside the worktree, its git directory or a model's working, home or agent directory; a planted store canary or a peer's stored report reaches a model before the barrier; a store directory or file grants group or other access.
   *Basis:* `decisions.md#Q-13`; `decisions.md#Q-7` same-perspectives addendum.
53. When a run starts and the change's state store holds results, the run uses each stored result that meets the Reused slot rule as a reused slot, launches every other planned slot, and names every stored result it does not reuse with the reason.
   *Refuted by:* A result with a different resume binding, stage, topic, seat, endpoint, model or prompt hash is reused; a byte change outside the stored run's own research append permits reuse; a commit that only records that append discards matching results; a cancelled, failed, timed-out, refused, not-started, interrupted or validation-failing result is reused; a discarded result is not named; a matching valid result is launched again; results of a run published complete are reused.
   *Basis:* `decisions.md#Q-13`.
54. When a run reuses stored results, it is a new run with its own run id, manifest, receipt and deadlines; reused slots fill their planned places without a call, and no slot launches twice within the run.
   *Refuted by:* Launched plus reused slots exceed `39 + 3N`, a reused slot also launches, a slot launches twice, or the run continues the earlier run's deadline, manifest or receipt.
   *Basis:* `decisions.md#Q-13`; `decisions.md#Q-7` budget.
55. When a run publishes reused results, each is marked reused with its source run id, original UTC start and end and original leak-check record, and the manifest names every slot of the source run that has a launch record without a terminal record as interrupted.
   *Refuted by:* A reused result appears as launched by this run, loses its source run or original times, or an interrupted source slot is missing from the manifest.
   *Basis:* `decisions.md#Q-13`.
56. If the latest stored run of the change recorded a security refusal, the next run reuses none of its results and names that run, its refused slot and the reason before any model call and in its manifest.
   *Refuted by:* Any result of such a run is reused, or the refusal is not named in the output or the manifest.
   *Basis:* `decisions.md#Q-13`; criterion 12.
57. If a state-store write fails, the runner launches no further slot, cancels queued slots, stops and reaps running children with their partial output kept, and ends incomplete with exit 1 and reason `state-store-unwritable` unless a security refusal requires exit 2.
   *Refuted by:* A slot launches after the failed write, the failure is not named, or the run exits 0, or exits 2 without a security refusal.
   *Basis:* `decisions.md#Q-13`; criterion 12's stop behaviour.
58. If another run of the same change holds the state-store lock, explore refuses with exit 2 before any model call.
   *Refuted by:* Two runs of one change write its store at once, or the lock of a killed run blocks the next run.
   *Basis:* `decisions.md#Q-13`.
59. When a seat needs a substitute, it takes the first substitute-pool model in cost order (`anfragen_5h` descending, ties by id) that is unexcluded, reachable and not selected for another seat of its trio; for one frozen catalog, terms, exclusion set and set of probe outcomes the whole selection is the same every time.
   *Refuted by:* A costlier pool model is chosen while a cheaper one is unexcluded, reachable and unused; equal ties are not broken by id; two preparations with identical inputs and probe outcomes select differently; a pool model without models.dev `tool_call: true`, with `status: deprecated`, or with an unmeasured wire API becomes a substitute; an unavailable models.dev yields any substitute.
   *Basis:* `decisions.md#Q-14`; the review swarm's cost order.
60. If a Go model has no `modelle_terms` record that passes the terms check, or no positive `anfragen_5h`, it is never probed, selected or used as a substitute, and the report names it with that reason when the fresh overlay lists it.
   *Refuted by:* Such a model is probed, preferred-selected or substituted, or an unread overlay model is missing from the report.
   *Basis:* `decisions.md#Q-14`; `decisions.md#Q-3` (repository seats receive private content).
61. When one admitted `modelle_terms` record is added for a Go model in the fresh overlay with a measured wire API and models.dev tool support, the next preparation includes that model in the substitute pool at its cost position, with no other edit.
   *Refuted by:* The model is not offered as a substitute until code, a seat declaration, `modelle` or a research list changes, or adding the record changes the review ladder.
   *Basis:* `decisions.md#Q-14`.

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
- Implementation-review swarm, runner verbs other than the research
  preparation verb, persistent web cache, paid search API, cost benchmark or
  opening sibling checkouts.
- Mid-run probing or reselecting Go free models, model swaps, topic-call
  retries, automatic admission of a Go model without a dated
  terms reading, a looser admission for online seats, or one shared
  selection for the review and research swarms: Q-12 shares the form and the
  implementation, not the seats or the selection.
- Resuming across changed inputs, partial reuse of a failed or cancelled
  slot, a cross-run spend limit, or reuse after a complete publication: Q-13
  keeps finished work for the same inputs only.

## Protected areas

- Accepted ADRs, `provenance.yaml`, existing human answers and adoption records:
  retain their meaning and history; only the named new ADR is proposed.
- Session runtime/policy and the review ladder's membership/order: research
  roles are declared separately, including Qwen without changing the ladder.
  Sharing the availability helpers with the review swarm leaves its
  preparation, receipt and ladder behaviour unchanged.
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
  the reported seat selection, actual seat/free model and web outcomes, and
  one resumed run after a deliberately stopped run; until success no
  complete live swarm is claimed. This draft calls no external model and does
  not claim runtime availability.
- Where the review swarm's availability preparation is on the base branch,
  its tests pass unchanged beside the research preparation tests.
- PR file review confirms protected areas/non-goals, names the bead, records
  test/capture commits and keeps final `Closes-Bead: coding-harness-icw`.

## Open decisions

None open. The recorded phase-2a rulings in decisions.md (S-1–S-52,
2026-10-16–17) and the maintainer's Q-11 answer (2026-10-17) settle the review
ambiguities; Q-11 replaces S-21's Pi-only capability rule. Q-12 and Q-13
(2026-10-18) leave only mechanism choices, each recorded below as a
`[DETAIL]` with its reason. I carry those visible details into this spec; no
maintainer answer is supplied here.

- [DETAIL] Criteria 23 and 38 use a When lead-in to match the phase-2 form;
  their prerequisites must still hold before any applicable call starts.
  This is wording only, with unchanged conditions, refutations and bases.

- [DETAIL] Criterion bases name the existing Q-records as
  `decisions.md#Q-<id>` so the recorded origin is explicit; this
  changes reference spelling only, not the criterion or its authority.
- [DETAIL] Keep the architectural class and ADR 0020. The current phase-4
  stop is the maintainer-approved total of 17 hours 20 minutes (Q-14,
  2026-10-18; before that 13 hours 20 minutes from 2026-10-17), recorded in
  plan.md's card and Time used. Sum retained measured historical
  spans and later Time used spans as prompts/04-implement.md defines them.
  The earlier unmeasured repair-attempt-3 span remains named, not counted;
  the maintainer answered that stop with continue and the 13-hour-20 total,
  and raised it to 17 hours 20 minutes on 2026-10-18.
  Preserve ruling S-30 as historical evidence rather than asking the settled
  question again. Any new unbounded phase-4 span still raises the appetite
  stop; earlier time is never zeroed or reset, and drafting phases 2/3 do not
  count.
- [DETAIL] Without `--stage2-off`, preflight validates class and given
  neighbours; for a swarm, preparation then measures the catalog and selects
  the seats before any model call (Q-12 details below). Explicit
  `--stage2-off [REASON]` skips class derivation and every class and neighbour
  header check, retaining single Haiku 5.5 and its route/model/reason record.
  Combining it with `--class` exits 2 before any call, saying that class has
  no effect on that route (S-52). Invalid neighbour entries (not unique
  repository-relative existing frozen Neighbour spec paths in the three
  permitted forms, excluding this change's own spec) exit 2. Thus
  `templates/spec.md` and the change's own spec refuse before models. For a swarm,
  research.md must have a list-valued `neighbours:` key; missing, null or
  non-list values exit 2 with a message to add `neighbours: []` or a spec list.
  The explicit empty list is valid. Include/exclude
  are unique exact-id lists: empty include selects all eligible ids, exclude
  wins; malformed policy exits 2. Any explicit include missing from the fresh
  eligible set exits 1 before models, even if also excluded. Valid `N=0`
  retains 39 required slots. Q-11's models.dev-unavailable fallback excludes
  every free candidate, records the source failure and keeps required slots;
  an explicit include remains a hard requirement and still exits 1 if it is
  ineligible. Read models.dev without credentials or repository data, retain
  source/time/digest and per-model reasons at every N. Document-level
  capability-unavailable means request failure/timeout, non-200 response,
  invalid JSON/non-object root, absent/non-object opencode-go or its models,
  or duplicate claimed ids under that models object. Duplicates mean either
  repeated keys in its raw JSON or equal `id` fields under different keys;
  parse with duplicate-key reporting rather than silently keeping one. Either
  excludes all candidates as capability-unavailable with reason `duplicate-id`.
  Only these models.dev document-level faults exclude all free candidates.
  A Pi refresh failure/timeout, Pi-rejected response, unparseable body or
  repeated overlay id (raw repeated key or one id under two entries) exits 1
  before all models, preserving diagnostics. Otherwise judge entries alone:
  malformed typed `input` or `type` excludes a `-free` candidate as
  `pi-malformed`, recording its raw value without excluding valid peers or
  blocking required slots. A malformed entry of a preferred or pool Go model is skipped the
  same way and never probed; Q-12 replaces S-50's exit 1 for a malformed
  fixed entry. Other entries are not inspected beyond the repeated-id check
  (S-50).
  Per models.dev candidate: a missing entry is metadata-missing; a non-object entry,
  non-boolean present tool_call, non-string present status or an id different
  from its key is metadata-malformed, recording the raw value. Absent tool_call
  or boolean false is no-tool-support; status deprecated is deprecated.
  The exact object key is the identity; an absent `id` is metadata-malformed,
  just like an id/key mismatch, with the raw value recorded as absent.
  Other providers' entries are not inspected. Every preferred Go model and
  every pool model must independently be fresh-Pi text-input chat to be
  probed, else it is skipped with its reason and raw value (Q-12 replaces
  S-37's fixed-model exit; a seat left without a model stops under criterion
  45). models.dev does not decide a preferred model or a Claude Code one;
  pool models need it (Q-14). Never infer support from Pi compat flags. This
  carries the maintainer's two-source choice without weakening Pi freshness.
  No Zen, baseline fallback or silent truncation.
- [DETAIL] The private change brief is frozen research.md header/body plus
  decisions.md and spec.md when present; the bead is id-only and its tracker
  text is not read. Finders and public-topic author get that same brief.
  Repository seats embed the same AGENTS.md. All runtimes disable automatic
  instruction discovery. This fixes the common input without tracker access.
- [DETAIL] Stages are preparation (catalog, seat selection, report) →
  receipt consumption → frozen inputs and resume lookup → finder trio → Opus
  map merge → Opus public topic → topics → Opus judge. Any failed finder, merge or topic-author result,
  including topic-filter rejection, prevents later stages and exits 1.
  Required topic failures allow remaining topic siblings to finish but prevent
  the judge; failed free slots are named and do not block it. A security
  refusal always cancels queues, stops/reaps children, keeps available partial
  output as cancelled and exits 2 in preference to exit 1.
- [DETAIL] The budget is at most `39 + 3N` calls. Provider queues share four
  permits per provider across roles. Preparation runs before the run's
  150 minutes: catalog 60 seconds with both
  reads started together at catalog preflight; at the shared deadline abort
  unfinished reads without retry. Unfinished Pi exits 1 regardless of the
  other result; successful Pi plus unfinished models.dev records
  capability-unavailable/timeout and keeps required slots, unless an explicit
  include is unmet. Required-seat probes use the fixed 60-second request;
  free probes use the real-size request with 120 seconds and one 360-second
  retry only after a timeout, before the selection and N are frozen. Other role deadlines: topic
  author 5 minutes, finder/researcher/merge 10, judge 15, run 150 total,
  monotonically measured with no retries. Required slots precede free seats:
  repository topics 1–8 then online seats 9–11, by topic then declared seat
  order; free seats follow by topic then sorted id. Reused slots (Q-13)
  launch nothing and keep their place in this order. The judge's 15 minutes
  are reserved. A topic launches only with positive pre-reserve time left;
  its allowance is the lesser of role limit and that remainder. Unlaunched
  slots are not-started-deadline, incomplete only when required. No silent
  roster truncation; large free rosters can leave named missing seats.
- [DETAIL] Local references use the type-specific Resolves rules against
  retained frozen bytes, replacing the earlier whole-file substring check;
  explicit extents give the tool-free judge reproducible evidence. Scan
  Markdown once: skip initial front matter from a first-line `---` through
  the next `---`; outside it, a fence opens with at least three backticks or
  tildes indented at most three spaces, and closes with the same character
  at least as long (unclosed means through EOF). Outside fences, headings
  have at most three leading spaces, one to six `#` marks, then space, tab
  or line end. Strip marks, optional closing `#` run and outer whitespace.
  The same scan governs uniqueness, excerpt ends, the one acceptance heading
  and its numbered items; quoted examples never supply structure (S-47).
  YAML uses a safe duplicate-reporting loader; JSON reports duplicate keys
  and refuses NaN/infinity. Split every path dot without list indexing,
  convert dates/timestamps to ISO text, and refuse non-JSON values before
  rendering the fixed canonical form; a citable parent retains keys that
  cannot themselves be addressed (S-48). Before
  publication compare HEAD and the full digest; ignore only the runner's own
  research appends and updated restamp. Other changes name paths and yield
  incomplete exit 1 with outputs retained. Copies stay outside the repository
  in run scratch and are deleted after publication/abort; only HEAD/digests,
  reports and resolved excerpts persist. Failed freezing exits 1 before
  models. This covers uncommitted inputs without copying the tree into briefs
  or invalidating its own digest (S-22).
- [DETAIL] After map merge and before any topic, the runner reads history
  locally against frozen HEAD, with no network or tracker: at most the ten
  most recent commits reaching each resolved mapped path. Each record holds
  full hash, UTC author date, subject, body capped at 4,000 characters with
  truncation marked, and touched mapped paths; older history is not read.
  Only topic 6's identical peer packets receive it. Only a full packet hash
  resolves, attaching that commit record as evidence; reachable hashes absent
  from the packet and standalone PR/bead ids stay unsupported. History-read
  failure is preparatory: no topics, incomplete exit 1 (S-32).
- [DETAIL] Opus map merge, topic author and judge have empty tool lists and
  see only their packets. The runner attaches resolved symbol/section,
  packet commit records or receipt excerpts for each valid claim, joined in
  citation order and capped at 4,000 Unicode characters per claim in total,
  with truncation marked; no private excerpt goes online. The design owns
  one fixed whole-packet character limit derived in phase 4 from documented
  or reported pinned-Claude Opus context capacity minus a fixed output
  reserve, recording source/date and conversion. Measure the assembled packet
  before launch: above the limit, keep all reports/excerpts, call no judge
  and end incomplete exit 1 as judge-packet-over-limit. Exactly the limit
  permits dispatch subject to the other preconditions. No further shortening,
  N reduction or extra judge call fits this rule (S-29, S-38).
- [DETAIL] Template breaches reject a report. Any bad citation makes its
  entire claim unsupported, without excerpt, disposition or criterion Basis;
  one evidence-backed claim is the report floor, except
  the specified empty topic-5 packet. The exception retains all three seats
  and a not-read record without inventing evidence. An online report thus needs one successful page retrieval, not success for
  every attempted fetch. Partial receipts and unsupported claims remain.
- [DETAIL] The runner assigns global claim/question ids using run, topic,
  endpoint-qualified model seat and local id. Handoff items H-<n> link the
  full global source ids. Q-record headers carry research_items and
  research_claims lists; neighbour answers additionally carry
  research_neighbours keep/drop/add lists, never inferred from answer prose.
  Duplicate decisions may share one item, preserving
  every source question/claim, including decisions scored off-brief/refuted.
  Class mismatches derive obligations independently of the judge; neighbour
  contradictions and proposed removal of given neighbours derive directly
  from topic-5 neighbour_relations, even with no explicit DECISION question;
  suggested statuses use three relations each backed by at least one
  runner-valid claim. Fewer than three counting relations is split, as is
  disagreement. Every contradicts or unrelated-given relation still derives
  its human item even with only unsupported claims; judge dispositions never
  affect this calculation. Every split derives a neighbour item with kind
  `split` (S-51). The judge cannot set or change status.
  This preserves peer disagreement rather than letting one verdict accept a
  path. Judge findings may add items but cannot waive them (S-24).
- [DETAIL] Version manifests research-swarm/v2. Complete runs alone supply
  phase 1a/2; incomplete runs require a new complete run and their claims
  cannot support criteria. Every complete run keeps its obligations across
  later runs and archival; one answered Q-record may link several runs.
  Before spec.md exists, valid pending obligations are listed with exit 0.
  Neighbours use runner-derived statuses and the union across all complete
  runs; split paths are not required absent a structured keep answer. A
  confirmation versus
  rejection between runs, or omission of an earlier given path from a later
  run's header, derives a neighbour DECISION item independently of the judge.
  The path stays required until an item-linked maintainer answer names it in
  research_neighbours.drop, whether originally given or confirmed (S-31).
  Once it exists, missing answers or no complete v2 run exit 1. Malformed or
  unreadable evidence exits 3 even before a spec. Legacy changes without v2
  runs are a reported exemption, including this redraft.
- [DETAIL] The gate derives coverage from accepted raw-report questions,
  class/neighbor fields and unresolved judge disagreements, not the judge's
  inventory alone. Once a spec exists it also resolves every criterion's
  Basis: every named direct claim must be supported and complete-run, even in
  a mixed list; other dispositions require a maintainer-answered Q-record
  basis (which may link the original claim in research_claims). It enforces
  exact neighbour parity: (confirmed or given in any complete run plus
  research_neighbours.keep and .add from maintainer-answered Q-records) minus
  their .drop paths. A neighbour item closes only with research_items linking
  it and keep/drop naming its path; an answered record without that field
  leaves it open (exit 1). An add needs no item link, but does need an actual
  maintainer answer. Check path form without current existence so historical
  records survive archival; paths outside the three forms exit 1. A path in
  two lists of one record or conflicting inclusion/drop directives across
  answered records exits 3. Unresolved split/cross-run items fail with exit 1
  even if the header keeps the path. Arbitrary phase-2 additions fail unless
  structurally human-added or confirmed by a new complete run. Phase-6 review
  checks that structured keep/drop/add matches the maintainer's answer;
  this prevents automatic semantic grading of prose (S-40, S-41).
  Review checks faithful questions/answers,
  basis relevance, comparison quality and off-brief prose; structure checks
  never claim to judge those meanings.
- [DETAIL] Repository online roles keep scratch isolation and public tools
  independent of Go's private-role permission. Wrapper stand-ins test runner
  orchestration; real pinned-Pi offline capture still owes isolation evidence.
  Historical phase-4 time stays in the plan; Time used holds each measured
  span since the amended implementation started.
- [DETAIL] Criteria 23 and 38 open with «Before any …»: each states a
  precondition on dispatch order, a shape the When/While/If opening marks
  elsewhere; the wording stands as reviewed in phase 2a instead of being
  reworded after the rulings, and each refutation keeps the sentence
  checkable.
- [DETAIL] Q-12 preparation is its own verb, `stage2.py prepare-explore
  <change> [--class CLASS]`, mirroring the review swarm's `prepare-loop`.
  It validates class and neighbours, refreshes the catalog, selects the free
  candidates by Q-10/Q-11, probes them under criterion 48, selects the six
  seats, prints the report and seals
  the receipt. `explore <change> --availability-reported ID` consumes it:
  it checks version, id, binding, timezone-aware time and age, then deletes
  the receipt before the first model call. The run uses the receipt's
  catalog and free selection instead of refreshing again, so seats and free
  seats come from one catalog that is at most the maximum age old. Receipt
  and probe records live in the runner-owned state directory beside the
  review loop record, never in the worktree; preparation therefore leaves
  `research.md` and the Q-13 resume binding unchanged. The review swarm
  writes its probe lines into `findings.md`; research deliberately does not.
  `prepare-explore` for a `bounded` or `spike` class, or beside
  `--stage2-off`, refuses with exit 2: no swarm runs there.
- [DETAIL] Exit codes keep this spec's scheme (S-28): a seat without a
  reachable preferred model or substitute is a measured result, so exit 1 with reason
  `seat-unavailable`, as for a failed Pi refresh and the replaced
  `fixed-model-unavailable`. A missing, stale, mismatched, consumed or
  corrupt receipt, a malformed seat declaration and an
  `--availability-reported` id where no swarm runs are refusals before
  anything is sent, so exit 2, as the review swarm's `review-loop` refuses
  without a valid receipt. The review swarm's `prepare-loop` exits 2 when no
  reviewer is reachable; research keeps exit 1 for that measured case. The
  difference is recorded here, not hidden.
- [DETAIL] A `claude-code-plan` preferred model is probed through official Claude
  Code with an empty tool list, the restricted, safe-mode and strict MCP
  settings of the Opus roles and a scratch working directory. That costs one
  Haiku call. Subscription quota can run out (Q-13's context records short
  Claude budgets on 2026-10-17/18), so treating the seat as reachable by
  declaration would bring back the failure Q-12 removes. Its substitute, if
  needed, comes from the Go pool like any other seat's. Opus merge, topic
  author and judge are roles, not seats, with nothing to choose from; they
  are not probed, and an unavailable Opus still fails its preparatory stage
  with exit 1.
- [DETAIL] Probing is lazy and deterministic. The repository trio comes
  before the online trio. Within a trio, the preferred models are probed
  first, in seat order. Then each seat still empty walks the pool in cost
  order. Probes run one at a time as in the review swarm, one per distinct
  model, and a result is shared across seats and trios. Preferred models go
  first so that a substitute never takes another seat's reachable preferred
  model. The cheapest reachable model is found without probing the rest, and
  every model is still reported: selected, substitute for a seat, skipped,
  excluded, unreachable or not probed. Preparation is bounded by 60 seconds
  of catalog plus the required-seat probe allowances and up to 480 seconds
  per selected free candidate (120 seconds, then 360 only after a timeout).
  The free request has the real online-topic size, a fixed public sentence
  and an OK-only instruction, without tools or private content. Failed
  candidates are named and removed before freezing N (maintainer,
  2026-10-22; supersedes the no-free-probe detail). A later failing free
  topic slot remains a named best-effort outcome.
- [DETAIL] Admission mirrors the review swarm (Q-14). A Go model needs a
  `modelle_terms` record that passes the review swarm's `terms_problem`,
  the rule under which it admits paid ladder models, and a positive
  `anfragen_5h`, because the cost order needs it. The record alone admits
  the model for research: it need not stand in `modelle`, so a research
  addition never changes the review ladder and the record stays the one
  manual step. That step stays deliberate because repository seats receive
  private framework content (Q-3), and reading a model's retention and
  training terms is a human judgement. The wire API is checked
  automatically: the fresh overlay's `api` must be in
  `measured_wire_apis`, declared as `[openai-completions]`. That is the one
  route measured through Pi on Go; `anthropic-messages` at `/zen/go` was
  refused on 2026-10-08, and `openai-responses` is unmeasured. Without this
  check a newly admitted model on an unmeasured route would become a
  substitute that fails every call. The review swarm's `uebersprungen` mark
  still excludes a model by hand. `-free` ids are refused as preferred
  models: required seats never rest on unread free-model terms, and no model
  is required and best-effort at once. Repository models need `framework` on
  their endpoint, and online models must be on `opencode-go`, because only
  the Pi public path yields retrieval receipts (Q-9, option B).
- [DETAIL] One substitute pool for both trios, without a looser online rule.
  Online seats see only the public sentence, so a looser admission would be
  defensible in principle, as Q-10 allows for free models. It would add no
  usable substitute, though: the cost order needs `anfragen_5h`, which lives
  in the same `modelle_terms` record, so a model without a reading has no
  place in the order. Loosening would also change who may decide admission,
  so it is not proposed here. A later wish for it is a decision for the
  maintainer. Pool models need models.dev tool support (`tool_call: true`,
  not deprecated), read from the same document as Q-11, because every seat
  works with tools: read tools on the repository side, public search and
  fetch online. Preferred models skip that check, as before (S-37): their
  declaration is the maintainer's deliberate choice, and a models.dev
  outage must not block them. An unavailable models.dev therefore empties
  the pool and leaves the preferred models working.
- [DETAIL] Configuration has the review swarm's shape:
  `research_swarm.availability_preflight` holds `max_age_seconds` (1 to
  3600, proposed 900) and `exclude_until` entries with `model_prefix`, a
  timezone-aware `until` and a `reason`, validated as the review swarm
  validates them; `flash_size` has no research meaning and is absent.
  `measured_wire_apis` lists the measured wire APIs. `repository_seats` and
  `online_seats` each hold exactly three preferred `{endpoint, model}`
  pairs and no fallback lists (Q-14). Research keeps its own exclusion list: a timed
  exclusion records a maintainer statement for one route, and the review
  swarm's GLM exclusion names an outage the maintainer later limited to
  Z.ai (Q-12 context), so sharing it would silently drop a reachable Go GLM
  from research. The initial preferred models are proposed in design.md;
  each later change is a one-line edit.
- [DETAIL] One implementation for both swarms (criterion 50). The selection
  step first merges `origin/main`. With the review swarm's pull request
  #157 merged there, it moves the swarm-independent parts of
  `scripts/stage2_availability.py` (rule validation, timed-exclusion
  matching, the tool-free probe, receipt sealing and verification) into
  shared functions, keeps review behaviour unchanged with its tests
  untouched, and adds the research entry points beside them. Without #157 on
  main, it writes the shared functions and research entry points under that
  same file name, to #157's contract as read at `0c03ec0`. Whichever pull
  request merges second then resolves the add/add conflict by keeping one
  copy and runs both test files. No state of main ever holds two
  implementations, and #158 never carries #157's unreviewed review changes.
- [DETAIL] Q-13 store: `record_dir(change)/research/`, the runner-owned
  place outside the worktree where the review loop record already lives;
  directories 0700, files 0600, one directory per run named by its random
  run id. Each launch and terminal record is scrubbed (criterion 21), written
  to a temporary file, flushed to disk, renamed and its directory flushed, so
  a crash leaves either the whole record or none. The standalone dispatcher
  gets one `on_terminal` callback, called once per slot in the thread that
  produced the outcome before it takes the next slot; its existing
  pre-launch `audit` callback writes the launch record. Reused slots are not
  passed to dispatch; the runner merges them into the stage results. This is
  the smallest change to the built dispatcher and keeps storage out of it.
- [DETAIL] The resume source is only the latest stored run of the change.
  Each run stores every result it used, launched or reused, with its source
  metadata, so a chain of aborted runs needs no deeper search and the report
  stays one comparison. The binding leaves out HEAD because AGENTS.md has
  sessions commit after each green step: a commit that only records the
  runner's own research append must not discard finished work. Each stored
  run records its frozen per-path digests and the digest and length of the
  bytes it appended to `research.md`; the next run strips exactly that tail
  and the `updated:` restamp before comparing. Packet content that depends
  on HEAD, such as topic 6's history, changes the prompt hash, so those slots
  launch again.
- [DETAIL] Reuse needs outcome `ok` and a report that passes this run's
  validation: a resumed run spends calls only where a valid contribution is
  missing. Results that do not match stay stored, because a reverted edit may
  match again, and are named at each run start. A run published complete
  clears the change's store, so a deliberate rerun starts fresh. A stored run
  with a security refusal is never a resume source: refused input must be
  fixed first, which normally changes the binding anyway, and Q-13 forbids a
  silent resume.
- [DETAIL] A failed store write stops the run with exit 1 and
  `state-store-unwritable`: going on would spend calls whose results could be
  lost, and exit 2 stays reserved for security refusals. One OS advisory
  lock per change store is held for the run; the operating system releases
  it when the process dies, so a killed run never blocks the next one, and a
  second concurrent run refuses with exit 2.
- [DETAIL] Residual read risk: stored results lie outside every directory a
  model is given and are never named to a model. A repository seat runs with
  the path lock `scripts/stage2_repository_pathlock.mjs` (decision Q-16): its
  read, grep, find and ls calls are refused when the path, with `..`
  collapsed and symbolic links followed, lies outside the worktree, so an
  absolute path to the store, the home directory or the git directory does
  not reach a model on any platform Pi runs on. The lock judges the path a
  tool is called with, not what a directory walk then visits; that remainder
  is the residual read risk design.md records. Probes and online seats have
  no file tools.

## Amendment — 2026-10-21, the maintainer chooses the seat models (Q-18)

This amendment supersedes, where they conflict, the "preferred model" wording
of the seat definition, the selection paragraph and criterion 49 above. A seat
is either pinned (`{endpoint, model}`) or open (`{endpoint: opencode-go}`
alone); the declared Go seats are open, the Haiku repository seat stays pinned.

62. When a seat is open, preparation fills it with the first pool model in cost order that is unexcluded, reachable and not selected for another seat of its trio, and marks it "cheapest".
   *Refuted by:* An open seat stays empty while such a model exists, takes a costlier model first, or one model fills two seats of a trio.
63. When preparation ends, its report lists every reachable candidate with its request cost and its Artificial Analysis Intelligence Index (or "not read" with the reason), the index source and reading time, and a recommendation; the API key appears in no output.
   *Refuted by:* A reachable candidate lacks cost or index, the source is missing, the key is printed, or a missing key or failed request stops the preparation.
64. When the maintainer's answer differs from the recommendation, `prepare-explore --seats TRIO=models` fills that trio's Go seats in order with exactly those models, marked "maintainer's choice"; a chosen model that is not admitted or not reachable stops preparation with exit 1 and is never replaced.
   *Refuted by:* A chosen model is swapped for another, ignored, or an unreachable choice yields a receipt.
65. If `--seats` names an unknown trio, a trio twice, a model twice, or not exactly as many models as the trio has Go seats, or an open seat names an endpoint other than `opencode-go`, preparation refuses with exit 2 before any probe.
   *Refuted by:* Such an input starts a probe or exits other than 2.
