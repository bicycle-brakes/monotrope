---
title: "Decisions — stage2-mimo"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-ymx
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions]
---

# stage2-mimo — Decisions

Phase 1a (interview) records the maintainer's request of 2026-10-06. No
formal interview is called; the task is clear in scope (add MiMo-V2.6 as a
reviewer in phase 4b) and in class (a `feature` — a new endpoint, new runner
logic, and an amendment to ADR 0007).

## What the maintainer decided on 2026-10-06

Maintainer (in a Claude Code session, bead coding-harness-ymx): "Plane das
als Stufe 2 reviewer ein — als zusätzlicher Prüfer in der Review-Schleife
(4b)." — Plan MiMo-V2.6 as a Stage 2 reviewer, as an additional reviewer in
the review loop (phase 4b).

The maintainer did not specify:
- Which endpoint to use (Xiaomi's own API, OpenRouter, or Z.ai's expansion).
- Whether MiMo runs in the same round as GLM, or in round 2 after GLM, or in
  a separate optional round.
- Whether the model family has a `pro` (reasoning) and `flash` (fast)
  variant, and which to choose for reviews.
- Whether the change also covers Codex replacement or phase 1/4 expansion (per
  ADR 0007 §5, those are open items of the stage-2-codex-glm change; the
  maintainer widened that scope on 2026-10-06, but may limit this change to 4b
  only).

> **Superseded** by the addendum "the reviewer decision, verbatim" below
> (2026-10-07, late evening). The class stands as `feature`.

## [DECISION] 1 — the class of this change (not answered yet)

The spec author must state the class. Two readings are plausible:

```text
Goal in one sentence:  Should MiMo be added to the review loop phase 4b only,
                       or to the entire stage-2 framework (review loop, spec
                       review, phase-6 review, and possibly explore/implement)?
Options:
  1. bounded.          It adds MiMo to phase 4b only, as an additional
                       reviewer running after or alongside GLM. The runner,
                       the endpoint declaration and the evidence rule change
                       for one phase. Spec review (2a) and review (6) stay
                       Codex and GLM; phases 1 and 4 stay Haiku/Sonnet (or
                       Flash when that runner verb is built). Consequence: no
                       ADR question; smaller scope; one revert removes phase-4b
                       MiMo calls only.
  2. feature.          It is a framework expansion: MiMo is added as a
                       reviewer option throughout stage 2, complementing Codex
                       (which reviews specs and code) and GLM (which reviews in
                       loops). Where each reviews depends on change class and
                       on the maintainer's stated preferences. Consequence:
                       ADR 0007 is substantially amended, not patched; the
                       architecture documents shift; every change routing may
                       change. Higher risk; more reversible by an architecture
                       decision than by a code revert.
Recommendation:        Option 1 — phase 4b only. Rationale: (a) the
                       maintainer said "in der Review-Schleife (4b)"
                       explicitly; (b) the spec-review and review phases are
                       already covered by Codex; (c) Codex and GLM track
                       well; MiMo adds a third opinion, not a replacement;
                       (d) the decision scope stays narrow; (e) if MiMo
                       findings are poor (e.g., many false positives), the
                       feature is easily disabled by the spec author,
                       requiring no ADR amendment. If findings are good and
                       want expansion, an ADR amendment comes later.
If you say "ok":       `class: feature` in spec.md; the spec header gains
                       `change: adr-0007-amendment`; an ADR 0007 amendment
                       proposal is written as part of the spec; the gate
                       `adr-answers` keeps `make verify` red until the
                       maintainer answers in the chat.
What is lost:         If this is option 1 (phase 4b only), the change is
                       reversible with one git revert and no ADR write-up. If
                       the maintainer later wants MiMo in spec review or phase
                       6, a separate `feature` change adds it.
```

The recommendation is Option 1: class `feature`, but scoped to phase 4b only.
(Note: "feature" is the class; "phase 4b only" is the implementation scope.)

> **Superseded** by the addendum "the reviewer decision, verbatim" below
> (2026-10-07, late evening): the endpoint is OpenCode Go.

## [DECISION] 2 — the endpoint: Xiaomi API, OpenRouter, or Z.ai?

Three vendors could serve MiMo-V2.6:

1. **Xiaomi's official API** — if it exists and is accessible to external
   developers. Unknown: whether it is Anthropic-compatible (like GLM),
   OpenAI-compatible (like Codex), or a third API shape. Auth: unknown.
   Residency: unknown. Data policy: unknown.

2. **OpenRouter** (openrouter.ai) — an aggregator serving hundreds of models.
   If MiMo is listed there, it is likely OpenAI-compatible; OpenRouter's data
   policy is known. Cost is typically higher than direct access. One credential
   (API key) handles all OpenRouter models.

3. **Z.ai** (the current GLM host, `https://api.z.ai/api/anthropic`) — if it
   has expanded to host MiMo alongside GLM. Anthropic-compatible. Uses the
   same subscription and auth as GLM. No new credential to manage.

**Recommendation:** Check Z.ai first; if MiMo is listed there, use that
endpoint (reduces credential management to one file, auth method is known,
residency is China like GLM). If not, OpenRouter is next (aggregator,
OpenAI-compatible likely, documented data policy). Xiaomi's own API is a
fallback only if it is shown to be OpenAI-compatible or the maintainer wants
to manage a third endpoint.

Consequence: endpoint declaration, runner's environment variables, and the
launch logic differ by vendor. The spec will propose one; the maintainer will
decide.

> **Superseded** by the addendum "the reviewer decision, verbatim" below
> (2026-10-07, late evening): one reviewer per round, three rounds.

## [DECISION] 3 — scheduling: same round as GLM, or round 2?

If both GLM and MiMo run in phase 4b, they can run in parallel (same round,
same diff) or sequentially (GLM round 1, MiMo round 2, both on merged-base
diff).

1. **Parallel (same round).** Both see the same code. Two reviewers, two
   verdict columns. Rows marked open for the implementer to decide. Cost: 2×
   review cost per round; `MAX_ROUNDS = 2` means up to 4 rows per round, all
   from two reviewers. Wall-clock: fast (both calls in parallel). Implementer
   sees all findings at once.

2. **Sequential (GLM round 1, MiMo round 2).** GLM runs first on merged-base
   diff; implementer decides GLM rows (taken/rejected); then MiMo runs on the
   same merged-base diff (original code, not repaired). Two separate
   `review-loop` calls. Rows marked open for the implementer. Cost: 2× review
   cost per round, but less wall-clock; implementer can fix GLM findings
   before MiMo runs. Wall-clock: slower (serial); implementer sees GLM verdict
   first, may reduce MiMo findings if the fixes address the root cause.

**Recommendation:** Sequential (option 2). Rationale: (a) compatible with
current runner structure (one `review-loop` call per reviewer); (b) lower
wall-clock time is less important than seeing one reviewer's verdict before
the next; (c) cost per round is the same, but implementer can act on GLM
findings before MiMo sees the code, which may improve both sets of findings;
(d) the current `MAX_ROUNDS = 2` is clear per reviewer; if both run, two
rounds each is four total, which is acceptable given the two-reviewer constraint
(ADR 0007 §1 names a fallback rule on the third run).

Consequence: the runner gains a new verb (`review-loop-mimo`) or a scheduler
that calls both in order. The spec will propose the verb structure; the
maintainer will decide.

## No [DETAIL] is open yet

All details (model name, API shape, auth method, data residency) depend on
reading the endpoint's documentation, which is blocked on [DECISION] 2. Once
the endpoint is chosen, those details are looked up and recorded in the spec.


## Addendum 2026-10-07: the maintainer's answers, and gaps closed by reading

Gaps closed by the orchestrating session on 2026-10-07 (OpenRouter public API
`/api/v1/models/xiaomi/mimo-v2.6-{flash,pro}/endpoints` and
`/api/v1/providers`, read that day): MiMo-V2.6 is **not** served by Z.ai (the
research note's guess is withdrawn). It is served by Xiaomi's own MiMo API
Platform (headquarters CN, datacenters SG and NL per OpenRouter; privacy
policy https://platform.xiaomimimo.com/#/docs/terms/privacy-policy, not read)
and through OpenRouter by GMICloud (US, bf16), DeepInfra (US), Venice (US),
Novita, io.net, Darkbloom and Xiaomi. Pro: USD 0.435 / 0.87 per million
tokens (input/output); Flash: USD 0.14 / 0.28 (Darkbloom 0.10). OpenRouter's
API is OpenAI-compatible.

Asked one at a time in the Claude Code session on 2026-10-07:

1. **Endpoint: "Xiaomi direkt"** — Xiaomi's own MiMo API Platform, with an
   account and key of the maintainer's. Not chosen: OpenRouter pinned to a US
   provider (the recommendation), OpenRouter with free provider choice.
   Consequence for phase 2: the endpoint entry declares Xiaomi as operator
   (residency per its terms: SG/NL datacenters, CN headquarters — to be read
   from Xiaomi's own documentation), and the maintainer's personal-use
   declaration covers Xiaomi's data policy, which phase 2 must read and quote.
2. **Scheduling: "Beide unabhängig, gleicher Diff"** (recommended) — GLM and
   MiMo review the same state in phase 4b without seeing each other's
   findings; disagreements are recorded ("MiMo flagged it, GLM did not"); one
   repair follows for both lists. Not chosen: GLM first, MiMo after GLM's
   repair.

Not asked, recorded as `[DETAIL]` for phase 2: the class is `feature` (a new
foreign endpoint and an amendment of ADR 0007); MiMo-V2.6-Pro is the
reviewer (71.9 vs Flash 67.9 on DeepSWE v1.1, vendor-reported; the cost
difference per review is a fraction of a cent).

## Addendum 2026-10-07 (later): [DECISION] 1 and the ADR question

Asked one at a time in the Claude Code session on 2026-10-07:

1. **Payment: "Token Plan"** — Xiaomi's subscription for programming tools.
   Not chosen: pay per use (the recommendation). The question named the
   consequence: the Token Plan's terms forbid "automated scripts", and the
   stage-2 runner is one, so the choice carries a terms risk the maintainer
   accepts; the ADR states it.
2. **ADR question: "yes — widen ADR 0007"** — Xiaomi is added to ADR 0007's
   own text (endpoint, data classes, the Token Plan terms risk, unconfined
   reads through Claude Code as for GLM). Not chosen: a new ADR 0011 that
   amends ADR 0007 (the recommendation); no ADR. The orchestrating session
   records the answer with `scripts/harness.py decide adr`.

## Addendum 2026-10-07 (evening): MiMo through OpenCode Go

The maintainer, in the Claude Code session on 2026-10-07: "ich möchte mimo
über opencode go anbinden" — MiMo is reached through the OpenCode Go
subscription. This replaces the answer "Xiaomi direct" and [DECISION] 1
"Token Plan" above; the ADR answer "yes — widen ADR 0007" stands, and the
ADR's text names OpenCode Go instead of Xiaomi.

Facts read on 2026-10-07 from <https://opencode.ai/docs/go/>, for phase 2:

- Model `opencode-go/mimo-v2.6-pro` (a Flash variant also exists); the
  `[DETAIL]` choice of Pro above is unchanged.
- Endpoints: Anthropic-compatible `https://opencode.ai/zen/go/v1/messages`,
  OpenAI-compatible `https://opencode.ai/zen/go/v1/chat/completions`.
- Data: retention "0 days", not used for training, for both MiMo-V2.6
  variants. The page does not name the provider that hosts the models.
- Cost: subscription Go $10 a month (first month $5); MiMo-V2.6-Pro capped
  at $15 a month on Go, $60 on Go Plus.
- Terms: "designed for OpenCode and other coding agents"; outside use sends
  "typical coding agent traffic", identifies itself with its own user agent
  and sends a stable session id in `x-opencode-session`. The Token Plan's
  "automated scripts" risk falls away; this condition replaces it.
- Not read: whether the maintainer already holds a Go subscription (Hermes
  is planned on OpenCode Go); the secrets file holds no OpenCode key name
  on 2026-10-07.

## Addendum 2026-10-07 (late evening): the reviewer decision, verbatim

**Superseded** by the decision below: the three `[DECISION]` sections above
and their answers — "Xiaomi direct", "Token Plan", "Beide unabhängig, gleicher
Diff", "MiMo-V2.6-Pro is the reviewer". **Stands**: "yes — widen ADR 0007",
with the ADR's text naming OpenCode Go instead of Xiaomi, and the class
`feature`.

Recorded in bead coding-harness-ymx (NOTES) on 2026-10-07, verbatim:

> Maintainer, 2026-10-07 (Claude Code session, German): every review — 2a, 4b
> and 6 — runs through OpenCode Go in rounds: round 1 DeepSeek V4.1 Flash,
> round 2 MiMo-V2.6-Flash (the maintainer wrote 'mimo v2.6 pro flash';
> OpenCode Go lists no such model, read as MiMo-V2.6-Flash — to confirm in the
> interview), round 3 only when needed MiMo-V2.6-Pro. The models must be easy
> to change as OpenCode Go's models perform or new ones arrive: an ordered
> list in model-endpoints.yaml, a one-line pull request, no code change.
> Consequences: Codex leaves the reviewer roles; the loop limit rises from two
> to three rounds; ADR 0007 needs amending (docs/adr is human-decided, so a
> decision PR). Needs an OpenCode Go key in the secrets file (maintainer adds
> it). Starts after the Flash runner (coding-harness-qcp) merges.

### Settled by it — no question

- **Every review phase calls OpenCode Go.** `spec-review` (phase 2a) and
  `review` (phase 6) leave Codex; `review-loop` (phase 4b) leaves GLM 5.3 on
  `glm-coding-plan`. Read from the rounds, which name DeepSeek and MiMo only
  and no fourth reviewer: GLM leaves the loop. GLM 5.3 Flash keeps explore
  and implement (bead coding-harness-bib), which this change does not touch.
  If a fourth reviewer was meant, that is the sentence to correct.
- **The rungs are one ordered list** in `model-endpoints.yaml`: the entry's
  `modelle:` is already a list, its position is the rung, and
  `declaration_problem()` (scripts/stage2.py:351) takes the model from it.
  Moving a rung is a one-line pull request, no code change.
- **`MAX_ROUNDS` rises from 2 to 3** (scripts/stage2.py:117), and every call
  is still launched by the runner, with the leak check and the declaration
  before it.
- **The key** enters the secrets file by the maintainer's hand; the runner
  reads it, no agent does. Name: `OPENCODE_GO_KEY` ([DETAIL] 4).
- **Nothing starts before** bead coding-harness-qcp (the Flash runner) is
  merged.
- **ADR 0007** is amended as a decision PR by the maintainer: OpenCode Go,
  the three rungs, Codex and GLM out of the reviewer roles.

### [DECISION] 1 — round 2's model id — answered 2026-10-07

The bead records your round 2 as written "mimo v2.6 pro flash" and reads it
as MiMo-V2.6-Flash, marked in the bead itself "to confirm in the interview".
`GET https://opencode.ai/zen/go/v1/models` on 2026-10-07 holds
`deepseek-v4.1-flash`, `mimo-v2.6-flash` and `mimo-v2.6-pro`; no id combines
both words.

Question: **MiMo-V2.6-Flash** in round 2 (the bead's reading), or
**MiMo-V2.6-Pro** (the word you wrote)?

Recommendation: Flash. Consequence: Flash is the cheaper and the weaker of
the two (USD 0.14 / 0.28 per million tokens against 0.435 / 0.87; DeepSWE
v1.1 67.9 against 71.9, vendor-reported), so the choice sets both what a
second opinion costs and what it sees. Pro in round 2 and again in round 3
would give the third round nothing new over the second.

**Answer: "runde 2 flash"** (maintainer, Claude Code session, 2026-10-07) —
round 2 is MiMo-V2.6-Flash, as the bead reads it, and the bead's "to confirm
in the interview" is closed. The ladder is therefore, in order:
`deepseek-v4.1-flash`, `mimo-v2.6-flash`, `mimo-v2.6-pro`.

### [DECISION] 2 — the residency the OpenCode Go entry declares — answered 2026-10-07

`model-endpoints.yaml` accepts three values. `nicht-erklaert` makes
`declaration_problem()` refuse the call before it is made
(scripts/stage2.py:364), so it would mean no reviewer runs at all; the
`ausgeschlossen` list forbids that value only for `kundencode`, a class this
change never sends.

Exploration on 2026-10-07 for this gap: the Go docs page states no region
(it carries region notes for Meta and Qwen models only); `opencode.ai/privacy`
answers 404; the Zen docs state "All our models are hosted in the US and EU."
— a sentence about Zen, a different product from Go.

Question: declare **`anbieter-erklaert`**, resting on that sentence of
OpenCode's, or **`region-waehlbar`**?

Recommendation: `anbieter-erklaert`. Consequence: `region-waehlbar` would
declare a region the maintainer can choose, and Go offers none — a statement
of record that is false on its face. `anbieter-erklaert` quotes OpenCode's
own words with their page and date in the entry's `bemerkung`, and is
corrected the day OpenCode says where Go runs. `nicht-erklaert` is the honest
value of today, and it stops every call.

**Answer: "anbieter erklärt"** (maintainer, Claude Code session, 2026-10-07)
— the entry declares `residenz: anbieter-erklaert`, resting on OpenCode's own
sentence about its models, with that page and its date in the entry's
`bemerkung`. Every `[DECISION]` in this file is now answered; what stays open
are the two `[GAP]`s, which phase 4 measures instead of asking.

### [GAP] — open, explored, not asked

1. Does `POST https://opencode.ai/zen/go/v1/messages` accept the three ids?
   The Go docs list them under `/v1/chat/completions`
   (`@ai-sdk/openai-compatible`) and name the Anthropic address only in
   passing. Measured in phase 4 with the maintainer's key; the fallback is
   the OpenAI address ([DETAIL] 5).
2. Whether OpenCode publishes a residency statement for Go later. Re-read
   before the entry is written; correct `residenz` then.

### [DETAIL] — decided here, reason recorded

1. **Which rung phase 2a and phase 6 take.** Both are one call each today
   (`spec_review`, `review` — no rounds). Taken: **rung 1**,
   `deepseek-v4.1-flash`. Reason: the decision gives the three rungs as
   rounds and names a limit of three for the loop, so the escalation belongs
   to phase 4b; a single call has no round to climb. Risk recorded: rung 1
   is the cheapest of the three, so the phase-6 verdict would come from the
   weakest model of the ladder — a stronger rung for phase 6 takes one
   sentence from the maintainer.
2. **When round 3 of the loop runs.** "round 3 only when needed" names no
   trigger. Taken: rounds 1 and 2 always run, as the loop runs them today
   (undecided rows still hold the next round); **round 3 runs only when round
   2 produced at least one taken row**, and the ceiling is three. Reason: a
   repair after round 2 is new code a third lineage should see, while a round
   that produced nothing new gives the next model the same diff again — and
   the two unconditional rounds keep today's behaviour unchanged, so the
   decision adds exactly one conditional rung.
3. **The rounds are a ladder over repaired code.** Round 2 sees round 1's
   repair, as `review_loop` does today, and each round has one reviewer. The
   answer "Beide unabhängig, gleicher Diff" goes with the superseded
   sections, and with it the `Also raised` column of the old spec.
4. **The entry's other fields**: `name: opencode-go`, `betreiber: "OpenCode
   (Operator Anomaly Innovations, Inc.)"`, `abrechnung: abonnement`,
   `darf_sehen: [framework]` — as `glm-coding-plan` and `openai-codex` stand
   today; key `OPENCODE_GO_KEY`.
5. **The request shape**: the Anthropic address first, with OpenCode's own
   user agent and a stable `x-opencode-session`, which its terms describe as
   the way a coding agent identifies itself; if it refuses a rung, the OpenAI
   address. Measured in phase 4, not asked.
6. **The class stays `feature`**, and the spec's `adr_question` is rewritten
   from Xiaomi and OpenRouter to OpenCode Go.
