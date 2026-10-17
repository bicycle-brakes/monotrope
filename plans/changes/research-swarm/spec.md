---
title: "Spec — research-swarm"
status: draft
implementation_status: partial
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
appetite: 13.333333333333334  # hours; exact operational total: 13 hours 20 minutes
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
6. When repository topics 1–8 run, each has independent DeepSeek Flash, MiMo Flash and Haiku 5.5 contributions.
   *Refuted by:* A topic is omitted, a model substituted, or one session supplies two seats.
   *Basis:* `decisions.md#Q-7`.
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
   *Refuted by:* Another model judges, a peer session is resumed, a required topic or valid claim's excerpt disappears, any file, shell, web or MCP tool is available, a packet over the recorded character limit reaches the judge, or excerpts are shortened beyond the per-claim cap to fit.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-7`.
15. When sourced disagreement remains unresolved, reconciliation retains its opposing global claim ids and evidence without an answer field.
   *Refuted by:* An unresolved disagreement loses an opposing claim id or evidence, or judge output contains a maintainer answer field; phase 6 also checks faithful treatment of dissent.
   *Basis:* `decisions.md#Q-5`, `decisions.md#Q-7` report and interview addenda.
16. When local claims count as evidence, their path-qualified symbol or section resolves against the retained frozen bytes, or a topic-6 full commit hash resolves in that seat's bounded frozen-HEAD history packet.
   *Refuted by:* Unresolvable or line-only references, a hash absent from the topic-6 packet, or a PR number or bead id alone is valid evidence, a prose-only match in Markdown or Python or an ambiguous heading/definition/key path resolves, the excerpt differs from the type-specific extent, a line inside a fenced block or front matter counts as a heading, a duplicate or a criterion item, a dotted key, list index or value without a JSON form resolves, a date excerpt is not its ISO text or the excerpt is not canonical JSON, a claim with any unresolved citation or unreceipted URL is valid, history collection failure lets a topic start, a reference resolves against the live tree instead of scratch bytes, a report is absent, a changed frozen file permits complete publication, or a frozen-file copy is persisted in research or the change folder.
   *Basis:* `decisions.md#Q-7` report template; existing source contract.
17. While the swarm explores, only the runner appends research and pre-existing repository content outside that artifact remains unchanged.
   *Refuted by:* A participant edits a file, rewrites an answer, replaces earlier research or changes git or tracker state.
   *Basis:* `decisions.md#Q-7` finder and topic boundaries; existing writer contract.
18. If a required contribution fails, the run retains partial evidence and all missing-slot outcomes and ends incomplete with exit 1 unless a security refusal requires exit 2.
   *Refuted by:* A failed preparatory stage dispatches a later stage, missing required topic reports still reach the judge, a report with zero evidence-backed claims passes except a topic-5 report whose packet holds no neighbour, a failed free seat alone makes the run incomplete, or an oversized judge packet loses evidence or fails to end incomplete with `judge-packet-over-limit` and no judge call.
   *Basis:* `decisions.md#Q-7`; existing failure contract.
19. When a swarm executes, its maximum 39 + 3N invocations follow the finite deadlines, required-first dispatch and reserved 15-minute judge allowance without retries or debate.
   *Refuted by:* An extra invocation or retry occurs, a free slot starts ahead of queued required slots, topic work consumes the judge reserve, or unlaunched slots lack not-started-deadline outcomes.
   *Basis:* `decisions.md#Q-7` concurrency answer; `decisions.md#Q-10`; finite-budget detail below.
20. When exploration explicitly uses `--stage2-off [REASON]`, it keeps single Haiku 5.5 exploration and records route, model and reason for the plan.
   *Refuted by:* It runs a swarm, reads a foreign key, names Haiku 4.5, loses the reason, requires or validates a class or neighbours header, or accepts a `--class` argument beside `--stage2-off`.
   *Basis:* `decisions.md#Q-4`; neighbouring haiku-5-5 spec, criterion 1.
21. When outputs contain a used credential, durable records and diagnostics redact the whole credential and every fragment of eight or more characters.
   *Refuted by:* A planted fragment survives in an answer, receipt, concurrent log or error.
   *Basis:* Existing credential contract.
22. When delivered, phase-1 doctrine, endpoint roles and exactly one new research-swarm ADR describe the same amended workflow.
   *Refuted by:* Six-topic or Zen-free-through-Pi instructions remain operative, the review ladder changes, or an accepted ADR is edited.
   *Basis:* `decisions.md#Q-7`, `decisions.md#Q-8`, `decisions.md#Q-9`, `decisions.md#Q-10`.
23. When any online call is about to start, fresh tool-free Opus must already have supplied a recorded public topic passing the defined word and name filters and exact-prompt leak check.
   *Refuted by:* An absent, rejected or privately augmented topic reaches an online seat; the author has any tool; research-swarm, a bead id or a sentence with `[`, `{`, `@`, `=` or a digit passes; Container-Isolation für KI-Agenten-Läufe or Isolation, Prüfung und Wiederherstellung für Agentenläufe fails the character rule; rejection fails to stop pre-topic dispatch with exit 1.
   *Basis:* `decisions.md#Q-6`, retained by `decisions.md#Q-8`.
24. When finder step 0 runs, the repository trio independently receives the same private change brief and four-list locator template for Opus to merge.
   *Refuted by:* Only one finder runs, an output has fields beyond the four locator lists, an empty category lacks an unread marker, an unresolved map entry grants topic scope, a given neighbour is missing from the runner's map, or topic 5's packet-neighbour list differs from an independent derivation from the resolved map and given header; prose design judgements are off-brief and reviewed in phase 6.
   *Basis:* `decisions.md#Q-7`, topic 0, option A.
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
37. When online topics 9–11 run, each has independent DeepSeek Flash, MiMo Flash and Qwen 3.8 Flash contributions through Pi on the same public-only brief.
   *Refuted by:* A free model, OpenCode CLI, Haiku or omitted vendor replaces one of the nine mandatory Flash contributions; added free seats cannot replace them.
   *Basis:* `decisions.md#Q-8`, `decisions.md#Q-9`.
38. When any swarm model call is about to start, the two-source catalog record already holds a successful fresh pinned-Pi Go overlay with every required fixed Go id as text-input chat, Pi source/UTC time/digest, models.dev source/UTC time/digest or failure, and each free candidate's selected/excluded outcome with exclusion reason and source field/value.
   *Refuted by:* A cached/shipped list substitutes for refresh, a baseline-only free id or another provider supplies a seat, an absent/baseline-only/non-chat fixed Go id lets any model call start, or at any N the manifest lacks either source's dated provenance/outcome or an excluded candidate's reason and source value.
   *Basis:* `decisions.md#Q-10`; `decisions.md#Q-11`.
39. When N Go free models are selected, each has an independent best-effort slot on topics 9–11 with the fixed Flash brief and a recorded terminal outcome.
   *Refuted by:* A selected seat is silently omitted or failed as successful, a non-selected/no-tool-support/deprecated model runs, peer briefs differ, or a missing explicit include starts any model instead of preflight exit 1.
   *Basis:* `decisions.md#Q-7` same-perspectives addendum; `decisions.md#Q-10`; `decisions.md#Q-11`.
40. While selected Go free models participate, they receive only the public-only role permissions and cannot fill a finder, repository, author, merge or judge seat.
   *Refuted by:* A free seat inherits the Go endpoint's framework permission or receives a private packet, map or report.
   *Basis:* `decisions.md#Q-3`; `decisions.md#Q-10`.
41. If the live Pi catalog cannot be measured reliably or a required fixed Go id is unavailable as fresh text-input chat, the runner preserves diagnostics and exits 1 before any swarm model call, naming `fixed-model-unavailable` and its id for the latter case.
   *Refuted by:* A Pi timeout, stale-only, malformed or ambiguous result or unavailable fixed model becomes valid zero availability or Flash-only fallback, the failure exits 0, 2 or 3, or a successful Pi refresh with only an unfinished models.dev read exits 1, or a repeated overlay id lets any model call start; absence of a tool-support field in Pi is not a Pi failure under Q-11.
   *Basis:* `decisions.md#Q-10`; existing failure contract.
42. When fresh Pi yields an empty free selection after capability checks and policy with no unmet explicit include, including models.dev absence or failure, the run records N=0 and its measured-empty or capability-unavailable reason and keeps all 39 fixed model slots.
   *Refuted by:* A missing models.dev model, missing/mismatched id, absent/false/non-boolean tool_call or deprecated status admits a free seat, one malformed models.dev or Pi candidate excludes a valid candidate or blocks the fixed slots, a repeated raw key or equal id under different keys leaves any candidate selectable instead of capability-unavailable/duplicate-id, document-level metadata failure is recorded as measured absence, models.dev failure alone blocks fixed slots, its timeout delays them beyond catalog's 60 seconds or exits nonzero by itself, or N=0 revives a prior roster or omits a fixed slot.
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

None open. The recorded phase-2a rulings in decisions.md (S-1–S-52,
2026-10-16–17) and the maintainer's Q-11 answer (2026-10-17) settle the review
ambiguities; Q-11 replaces S-21's Pi-only capability rule. I carry those
visible details into this spec; no maintainer answer is supplied here.

- [DETAIL] Criteria 23 and 38 use a When lead-in to match the phase-2 form;
  their prerequisites must still hold before any applicable call starts.
  This is wording only, with unchanged conditions, refutations and bases.

- [DETAIL] Criterion bases name the existing Q-records as
  `decisions.md#Q-<id>` so the recorded origin is explicit; this
  changes reference spelling only, not the criterion or its authority.
- [DETAIL] Keep the architectural class and ADR 0020. The current phase-4
  stop is the maintainer-approved total of 13 hours 20 minutes, recorded in
  plan.md's card and Time used on 2026-10-17. Sum retained measured historical
  spans and later Time used spans as prompts/04-implement.md defines them.
  The earlier unmeasured repair-attempt-3 span remains named, not counted;
  the maintainer answered that stop with continue and this new total.
  Preserve ruling S-30 as historical evidence rather than asking the settled
  question again. Any new unbounded phase-4 span still raises the appetite
  stop; earlier time is never zeroed or reset, and drafting phases 2/3 do not
  count.
- [DETAIL] Without `--stage2-off`, preflight validates class and given
  neighbours, then measures the catalog before swarm model dispatch. Explicit
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
  retains 39 fixed slots. Q-11's models.dev-unavailable fallback excludes
  every free candidate, records the source failure and keeps fixed slots;
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
  blocking fixed slots. A malformed fixed Go entry exits 1 as
  `fixed-model-unavailable`, naming id and raw value; other entries are not
  inspected beyond the repeated-id check (S-50).
  Per models.dev candidate: a missing entry is metadata-missing; a non-object entry,
  non-boolean present tool_call, non-string present status or an id different
  from its key is metadata-malformed, recording the raw value. Absent tool_call
  or boolean false is no-tool-support; status deprecated is deprecated.
  The exact object key is the identity; an absent `id` is metadata-malformed,
  just like an id/key mismatch, with the raw value recorded as absent.
  Other providers' entries are not inspected. Every fixed Go role model
  must independently be fresh-Pi text-input chat, else preflight exit 1 with
  fixed-model-unavailable and the id; models.dev is not consulted for fixed
  models, nor for Claude Code Haiku. Never infer support from Pi compat flags. This
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
  permits per provider across roles. Deadlines: catalog 60 seconds with both
  reads started together at catalog preflight; at the shared deadline abort
  unfinished reads without retry. Unfinished Pi exits 1 regardless of the
  other result; successful Pi plus unfinished models.dev records
  capability-unavailable/timeout and keeps fixed slots, unless an explicit
  include is unmet. Other role deadlines: topic
  author 5 minutes, finder/researcher/merge 10, judge 15, run 150 total,
  monotonically measured with no retries. Required slots precede free seats:
  repository topics 1–8 then online Flash 9–11, by topic then declared seat
  order; free seats follow by topic then sorted id. The judge's 15 minutes
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
  Historical phase-4 time stays in the plan, with Time used empty until the
  amended implementation starts.
- [DETAIL] Criteria 23 and 38 open with «Before any …»: each states a
  precondition on dispatch order, a shape the When/While/If opening marks
  elsewhere; the wording stands as reviewed in phase 2a instead of being
  reworded after the rulings, and each refutation keeps the sentence
  checkable.
