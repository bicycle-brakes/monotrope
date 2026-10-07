---
title: "Research — stage2-mimo"
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
tags: [research, stage-2, mimo]
---

# Research — stage2-mimo

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). Facts only, read on 2026-10-07 in the worktree at the current head of `feat/stage2-mimo` (branched from `feat/stage-2-codex-glm`, 83c545a). Every statement names its source; what was not read says so.

The task (maintainer, 2026-10-06): "Plane das als Stufe 2 reviewer ein — als zusätzlicher Prüfer in der Review-Schleife (4b)" — plan MiMo-V2.6 as a Stage 2 reviewer, as an additional reviewer in the review loop (phase 4b).

## 0 · Existing artefacts on the topic

`rg -i "mimo|xiaomi|stage.?2|review.?loop"` over `plans/specs/` and `plans/changes/` (2026-10-07) finds `plans/changes/stage-2-codex-glm/` (current and related), but no artefact on MiMo specifically. Nothing to update instead of create.

## 1 · What exists today

### 1.1 Stage 2 as of 2026-10-07

ADR 0007 (`docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`, merged) sets the current stage-2 routing:

- **Codex** (`openai-codex`, model `gpt-6.1-sol`, official Codex CLI): spec review (phase 2a) and code review (phase 6) for all change classes. Declared for framework content only; runs through an ask rule; read-only request (not confined); personal ChatGPT subscription (2026-09-30).

- **GLM** (`glm-coding-plan`, model `glm-5.3` for review loop / `glm-5.3-flash` for phases 1 and 4, Z.ai's Anthropic-compatible endpoint at `https://api.z.ai/api/anthropic`): review loop (phase 4b) for all changes; started by `python3 scripts/stage2.py review-loop <change>`; for framework content only; through Claude Code only; reads broadly, writes code.

- **Leak check** (`scripts/leakcheck.py`): required before every call, enforced by `scripts/stage2.py` at lines 437–440. Checks three rules: framework content only, no customer schema or figures, no secrets planted in fixtures.

- **Max rounds**: 2 (line 117 of `scripts/stage2.py`).

- **Evidence rule** (`prompts/04b-review-loop.md`, §For the implementer): a GLM or Codex finding is taken only when a test demonstrates it or the spec supports it; otherwise it is rejected with reason and stays in findings.md as a disagreement.

- **Disagreement recording** (`docs/WORKFLOW.md` §2.3): disagreements are recorded, not resolved. One reviewer flags something and another does not — that is the information.

### 1.2 The call path (phase 4b)

`scripts/stage2.py review-loop` (lines 789–852) prepares and runs a GLM call:

1. Preflight: change exists, spec.md has a `bead`, endpoint `glm-coding-plan` is declared for framework with residency (line 791–801).
2. Leak check (line 809): `scripts/leakcheck.py` runs; exits 2 if not clean.
3. Diff build (line 804): `change_diff()` constructs the merge-base diff against `origin/main`, uncommitted and untracked files included.
4. Prompt build (lines 806–808): prompt is `04b-review-loop.md` body, answer format, read request, the diff again, read request again.
5. Claude Code call (lines 815–835): `claude` command with `--model glm-5.3`, `--effort max`, `-p` and `--append-system-prompt-file` for the prompt, `--tools Read,Grep,Glob`, restricted sandbox, no session persistence, permission mode `dontAsk`. Environment: `ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic`, `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` from `~/.config/cc-routing/secrets.env`, GLM model name set in all model variables.
6. Rows written to loop record (lines 843–851): outside the repository at `~/.local/state/coding-harness/stage2/<change>/loop.md`, numbered `L<round>-<k>`, GLM marked as reviewer, status and test mark left empty for the implementer.
7. `findings.md` entry (line 445–447): date, verb, endpoint, model, leak check stats.

### 1.3 How a MiMo call would fit

The task says "zusätzlicher Prüfer" — an additional reviewer. The current architecture (ADR 0007, section 4, phase 4b):

> "Disagreements are recorded, not resolved. That one reviewer flags something and another does not *is* the information."

So MiMo could be a second or third foreign reviewer in the loop, alongside or after GLM. The `findings.md` already distinguishes reviewers by name (`Reviewer` column in tables, line 118).

What the task asks for is not yet in ADR 0007: the amendment (section 4) covers Codex and GLM only. Where MiMo would sit — after GLM, both on the same diff, a fallback condition, or a separate optional path — is open and marked in the current ADR as a detail for the maintainer to decide.

## 2 · MiMo-V2.6 hosting and access

### 2.1 Xiaomi's MiMo models — not read

Xiaomi's official model page and API documentation: not read from the web (2026-10-07). The model's public announcement, supported vendors, residency, auth method and API shape are unknown.

[GAP: Is MiMo-V2.6 (or MiMo-V2.*) a product Xiaomi offers to external developers, and if so, through which endpoints? Is there an official Xiaomi API, and is it Anthropic- or OpenAI-compatible?]

### 2.2 Aggregators — OpenRouter status

**OpenRouter** (openrouter.ai): [not read from web, 2026-10-07] Whether OpenRouter currently lists any MiMo model and which regions it serves are unknown.

[GAP: Does OpenRouter host MiMo-V2.6 or any MiMo model, and if so, is it OpenAI-compatible? Which data policy does OpenRouter apply to MiMo calls?]

### 2.3 Z.ai (the current GLM host) — not read

Whether Z.ai hosts MiMo-V2.6 or any Xiaomi model is unknown (2026-10-07).

[GAP: Does Z.ai offer MiMo models alongside GLM, and if so, under what terms?]

### 2.4 Data retention and training — vendor claims not verified

Xiaomi's terms for data use, retention and training use on any of its models are unknown (2026-10-07).

[GAP: What is Xiaomi's stated data policy for personal-use API access? Is there an opt-out for training use?]

## 3 · How MiMo would integrate

### 3.1 model-endpoints.yaml

To run a MiMo call, a new endpoint must be declared (or MiMo added to an existing endpoint). The declaration would follow lines 293–335 for GLM and 347–358 for Codex:

```yaml
- name: mimo-endpoint-name  # TBD: Xiaomi's official API, OpenRouter, or Z.ai?
  betreiber: Xiaomi  # or "aggregator (OpenRouter)" etc.
  residenz: [TBD: where data stays]
  abrechnung: token  # or abonnement
  darf_sehen: [framework]
  modelle:
    - mimo-v2.6
    # or mimo-v2-*, depending on the model family
  bemerkung: >-
    [TBD: access method, data terms, auth]
```

### 3.2 scripts/stage2.py changes

Lines 75–78 define the endpoints and models for Codex and GLM:

```python
CODEX = ("openai-codex", "gpt-6.1-sol", "max")
GLM = ("glm-coding-plan", "glm-5.3", "max")
GLM_BASE_URL = "https://api.z.ai/api/anthropic"
```

A MiMo endpoint would need similar constants (or a third verb). If MiMo is OpenAI-compatible, it could reuse the `foreign_env()` pattern; if it is something else, new launch logic is needed.

Where MiMo runs (after GLM in round 2, both in round 1, a separate optional round) would shape how the runner schedules it. Currently, `MAX_ROUNDS = 2` (line 117) counts GLM rounds; if MiMo runs after GLM's verdict, that limit may change.

### 3.3 Verb: `review-loop-mimo` or `review-loop-all`?

The maintainer's request says "zusätzlicher Prüfer" (additional reviewer), which suggests MiMo runs in the same loop as GLM, not instead of it. The runner would then have two options:

- **`review-loop` stays GLM-only, and a new verb `review-loop-mimo` runs MiMo.** Implementer decides the order; could run `review-loop` then `review-loop-mimo` in sequence.
- **`review-loop-all` runs both GLM and MiMo in one call** (the maintainer decides the order). Simpler for the implementer; less flexible.

Current `review-loop` (lines 789–852) would need adaptation either way.

## 4 · Pro vs Flash for review

### 4.1 GLM in phase 4b: 5.3 (current) or 5.3-flash?

ADR 0007 section 5 notes that exploration and implementation on GLM 5.3 Flash are decided but not built. The review loop (phase 4b) uses `glm-5.3` at effort `max` (lines 76–77, line 824). Why the distinction is not explained in the current tree.

[DETAIL: Whether MiMo's model family has a "pro" (reasoning) and "flash" (fast) variant, and whether the review loop should choose speed or reasoning capability for finding defects, depends on Xiaomi's model line-up and the maintainer's risk tolerance. A faster model means lower cost per round; a reasoning model means potentially deeper findings. The current GLM choice (not Flash) suggests reasoning is preferred for reviews.]

### 4.2 Cost estimate — not measured

No benchmark data for cost or latency of MiMo-V2.6 (or any MiMo model) in a review context is known (2026-10-07). GLM 5.3 at effort `max` on a typical diff size in this repository is not measured either.

[GAP: What is the estimated cost per review round (input + output tokens × rate) for MiMo-V2.6 versus GLM 5.3, at typical diff sizes in this repository?]

## 5 · Where MiMo sits in phase 4b

### 5.1 Same round, both GLM and MiMo?

If both reviewers run on the same diff in round 1, the implementer gets two columns of findings, both marked as "open" until decided. The loop record would have two sets of rows, distinguished by reviewer. The evidence rule still applies: a finding is taken only when a test demonstrates it or the spec supports it.

**Consequence:** one round, two verdict columns, double the findings to filter. Cost is 2× the review cost per round. With `MAX_ROUNDS = 2`, up to 4 total rounds is possible if one reviewer needs repair feedback.

### 5.2 Sequential: GLM then MiMo?

Round 1 GLM, round 2 MiMo, both on the same merged-base diff. If GLM finds something, the implementer decides whether to fix it before MiMo sees the same code (or the original code). This keeps the current verb structure (one `review-loop` call = one reviewer).

**Consequence:** up to 2 rounds each, 4 rounds total; serial, so longer wall-clock time; implementer can fix GLM findings before MiMo sees them, which may reduce MiMo findings.

### 5.3 After phase-6 verdict

Both GLM and MiMo as pre-phase-6 reviewers, but a third optional round if needed. Lines 529–572 of `scripts/stage2.py` release the loop rows into findings.md after Codex's phase-6 verdict; the phase-6 reviewer (Codex) reads the loop findings and marks them agree/disagree.

If MiMo runs before phase 6, its rows are part of the loop; if it runs after the loop but before phase 6, it would need new machinery.

**[DECISION] In phase 4b, where should MiMo run relative to GLM?**

Recommendation: **GLM round 1, MiMo round 2, both on the same merged-base diff**, keeping the serial structure (one `review-loop` call per reviewer). This limits `MAX_ROUNDS` to 2 rounds per reviewer, 4 total. Rationale: (a) lower total cost than running both in parallel; (b) implementer can see GLM's verdict first, fixing obvious issues before MiMo sees the code; (c) disagree/agree marks from both reviewers in one findings.md table.

Consequence: the current `MAX_ROUNDS = 2` may need to clarify that it is per reviewer, or the limit changes to 2 total (one per reviewer). The maintainer will decide after seeing the first live runs.

## 6 · What ADR 0007 must gain

ADR 0007 section 4 (page 9) covers Codex and GLM only. The amendment needed:

> "**Where framework content may flow.** This repository's tree — the class `framework` of `model-endpoints.yaml`: rules, templates, process, tests — may go to `openai-codex` through the official Codex CLI, and to `glm-coding-plan` through Claude Code: ... Nothing else goes, and nowhere else."

Must be widened to include MiMo if it is added as a stage-2 reviewer. The new text would be:

> "... and to `glm-coding-plan` through Claude Code, and to `[mimo-endpoint-name]` [through OpenRouter|through Xiaomi's API|...]: the reviews to Codex, GLM and MiMo, ... Nothing else goes, and nowhere else."

The endpoint declaration, residency, data policy and auth method must be added before the amendment is complete (open questions in section 2 above).

The current decision continuity map (`docs/architecture/` and `scripts/check_decision_continuity.py`, line 56) maps D-13 to ADR 0007; if ADR 0007 is amended, the D-13 row in the target document must be updated to name the addition.

## 7 · Open questions, tagged

**[DECISION]** Whether a new endpoint or an aggregator is preferred, and which vendor Xiaomi should flow through (Xiaomi's own API, OpenRouter, Z.ai). Consequence: the endpoint declaration and the runner's environment setup differ.

**Recommendation:** Check whether Z.ai (the current GLM vendor) offers MiMo-V2.6, and if so, use that endpoint to reduce credential management (one secrets file, one Anthropic-compatible base URL). If not, OpenRouter is the next choice for compatibility. Xiaomi's own API is a fallback only if it is OpenAI-compatible; otherwise, new runner logic is needed.

**[DECISION]** Whether both GLM and MiMo run in round 1 (parallel, same diff), or GLM round 1 and MiMo round 2 (sequential, both on merged-base diff), or another order. Consequence: cost, wall-clock time, implementer decision flow, and whether `MAX_ROUNDS` is per-reviewer or total.

**Recommendation:** Sequential (GLM round 1, MiMo round 2) as described in section 5.2. Rationale: compatible with current runner structure; lower cost; implementer sees GLM verdict first.

**[DETAIL]** The exact model name if Xiaomi has a model family (e.g., `mimo-v2.6` or `mimo-v2` or `mimoR7`). Decided by vendor's official listing once the endpoint is chosen.

**[DETAIL]** Whether MiMo-V2.6's API is Anthropic-compatible (like GLM), OpenAI-compatible (like Codex), or something else. Impacts the runner's environment setup and the launch logic. Decided by reading the endpoint's API docs once the endpoint is chosen.

**[DETAIL]** The auth method (API key, OAuth, subscription token). Decided by the endpoint's documentation and the secrets file format.

## 8 · Files a change would touch

- `model-endpoints.yaml`: add MiMo endpoint declaration
- `scripts/stage2.py`: add MiMo endpoint constants, GLM/MiMo scheduling logic, possibly a new verb or conditional in `review-loop`
- `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md`: amend section 4 ("Where framework content may flow") to include MiMo
- `docs/architecture/target-architecture.md` or its successor: update the D-13 row to reflect the MiMo addition
- `tests/test_stage2.py`: test the new endpoint declaration and the MiMo scheduling
- `tests/test_leakcheck.py`: if MiMo is a new data class, verify leakcheck still holds
- Possible: `prompts/04b-review-loop.md`, if a separate prompt for MiMo is needed (unlikely; the answer format and evidence rule are universal)
- Possible: `~/.config/cc-routing/secrets.env` (user setup, not in the repository): add `MIMO_KEY` or equivalent

## 9 · Next steps

1. Read Xiaomi's documentation on MiMo-V2.6: model card, API shape (Anthropic or OpenAI compatible), access methods, data residency, data use terms, pricing.
2. Check Z.ai's current model roster: does it list MiMo, and if so, what terms?
3. Check OpenRouter's current model roster and pricing for MiMo, and compare with direct access.
4. (Blocked on [DECISION]s above) Measure cost and latency of a typical phase-4b call with the chosen endpoint.
5. Propose the endpoint declaration and runner changes (phase 2, Spec).

## Gaps closed in phase 2 (2026-10-07)

Read on 2026-10-07 by the phase-2 session; this section holds where it
disagrees with the text above. The maintainer's answers (`decisions.md`,
addendum 2026-10-07) stand: Xiaomi's own platform, GLM and MiMo independent
on the same diff.

**How it was read.** The platform (<https://platform.xiaomimimo.com>) links its
documentation at <https://mimo.mi.com/docs/>. Both sites render in the browser
only, so the page text was read from the documentation site's published
JavaScript (its search index, which carries every English page, and the
compiled "Claude Code Configuration" page). The two privacy policies were read
as HTML at privacy.mi.com. **Not read:** the console behind the login — the
API keys page, the Token Plan page, and so the base URL Xiaomi shows for the
maintainer's own account.

### A · API shape, address, model, authentication

- **Both protocols.** "Xiaomi MiMo API Open Platform is compatible with OpenAI
  API and Anthropic API formats." (page "First API Call").
- **Pay-per-use addresses** (given as examples): OpenAI-compatible
  `https://api.xiaomimimo.com/v1`, Anthropic-compatible
  `https://api.xiaomimimo.com/anthropic`; request address
  `https://api.xiaomimimo.com/anthropic/v1/messages`; key format `sk-…`.
- **Token Plan addresses:** `https://token-plan-cn.xiaomimimo.com/anthropic`
  ("China Cluster"), `…token-plan-sgp…` ("Singapore Cluster"),
  `…token-plan-ams…` ("European Cluster"); keys `tp-…` (individual), `ttp-…`
  (team).
- **The address depends on the account:** "Return different Base URLs + Keys
  based on the region where the account is located, which are not
  interoperable." (FAQ "Account and Authentication"). The address of the
  maintainer's account: not read.
- **Authentication:** "api-key: $MIMO_API_KEY or Authorization: Bearer
  $MIMO_API_KEY" (FAQ "API Integration"); for Claude Code the key goes into
  `ANTHROPIC_AUTH_TOKEN`.
- **Claude Code is documented:** "Pay-as-you-go MiMo API and Token Plan both
  support Claude Code." The page sets `ANTHROPIC_BASE_URL`,
  `ANTHROPIC_AUTH_TOKEN`, and `ANTHROPIC_MODEL` and the three
  `ANTHROPIC_DEFAULT_*_MODEL` variables to `mimo-v2.6-pro`.
- **Model:** `mimo-v2.6-pro` — context 1M tokens, output up to 128K, 100
  requests and 10M tokens per minute per account (page "Models").
  `mimo-v2.5-pro` and `mimo-v2.5` are withdrawn on 2026-10-21.
- **Parameters of the Anthropic-compatible API:** `thinking` is `enabled` by
  default for `mimo-v2.6-pro`; `tool_choice` other than `auto` is removed by
  the backend; an `effort` parameter is not documented.

### B · Price and terms of use

- **Pay-per-use, outside China, `mimo-v2.6-pro`:** USD 0.435 per million
  input tokens (cache miss), 0.0036 (cache hit), 0.87 per million output tokens
  (page "Pay-As-You-Go API"); the same as OpenRouter's figure in
  `decisions.md`. Estimate, not measured: a round of 200 000 to 500 000 input
  and 10 000 output tokens costs USD 0.10 to 0.23.
- **Token Plan (individual):** from USD 6 a month (Lite, 4.1 billion credits;
  `mimo-v2.6-pro` costs 300 credits per input and 600 per output token);
  "non-refundable and non-cancellable upon purchase" (service agreement 3.13).
  "The quota of the Token Plan package is only available for use in
  programming tools (such as OpenClaw, OpenCode, etc.), and it is prohibited to
  use it in the form of API calls for request behaviors in obvious non-coding
  scenarios such as automated scripts and custom application backends." (page
  "Individual Subscription").
- **Accounts:** "Currently, the platform only provides personal account
  login." (page "First API Call"); "Your account is limited to your own use"
  (service agreement 2.3). No clause limiting the pay-per-use API to personal
  or non-commercial use was found in the English service agreement and the FAQ
  pages read.
- **Tools:** the service agreement forbids using the service "through any
  third-party software, plug-ins, cheats or systems not developed or authorized
  by Xiaomi" (3.2.9); Xiaomi's own pages list Claude Code among the supported
  tools.

### C · Operator, data use, residency, retention

Xiaomi publishes two privacy policies, and the documentation site links one
for international users and one for users in China:

- **Outside the PRC** (<https://privacy.mi.com/XiaomiMiMoPlatformos/en_GB/>,
  "updated on June 25, 2026"): the service is provided "by Xiaomi Technology
  Netherlands B.V., Xiaomi Technologies Singapore Pte. Ltd. and its
  affiliates"; "Xiaomi will not use the content you provide for model training
  or any other purposes."; "Xiaomi uses regional data hosting infrastructure
  located in the Netherlands and Singapore." For the EEA, UK and Switzerland
  the controller is Xiaomi Technology Netherlands B.V., data "will be stored in
  data centres located in the Netherlands. We may transfer your personal
  information to Singapore"; Xiaomi "also transfers personal information to
  affiliated companies, third-party service providers and business partners
  located outside the region in which the information is hosted". Retention:
  "for the period necessary for the purposes described in this Privacy Policy,
  or as required by applicable law" — no period is stated.
- **Inside the PRC** (<https://privacy.mi.com/XiaomiMiMoPlatform/en_GB/>,
  version v20260806): operated by Beijing Xiaomi Mobile Software Co., Ltd.;
  "This agreement applies to your use of Xiaomi MiMo services within the
  territory of the People's Republic of China. Accordingly, your personal
  information will be stored within the territory of the People's Republic of
  China."; "Without your prior consent, Xiaomi will not use the text content
  provided by you for model training or any other purposes."
- **Service agreement outside the PRC** ("updated on July 7, 2026"): "Xiaomi
  MiMo is operated by Xiaomi Technologies Singapore Pte. Ltd." (1.1), a storage
  region can be requested and "may incur additional service fees" (1.1);
  "Xiaomi acts as a Processor … you are the Data Controller" (4.1); "When
  providing services outside the Chinese Mainland, Xiaomi will store the
  relevant data on servers located in Europe and Singapore." (4.4); the laws of
  Singapore govern (8.1).

So the residency depends on where the account is registered: an account
outside China is under the Netherlands–Singapore terms, an account in China
under the PRC terms. Which one the maintainer has: not read.

### D · Corrections to the text above

- §2.1–§2.4 and the `[DETAIL]`s of §7 are answered by A–C: Xiaomi serves
  MiMo itself, Anthropic- and OpenAI-compatible, key in a header, the model id
  is `mimo-v2.6-pro`.
- §3.1 cites lines 293–335 and 347–358 of `model-endpoints.yaml`; the file has
  196 lines. The GLM entry stands at lines 111–127, the Codex entry at 129–144.
- §6 assumes ADR 0007 would be amended in place and the D-13 row edited. The
  spec proposes a new ADR instead (its section "The ADR question"); the next
  free number on 2026-10-07 is 0011, because 0010 is held by an open decision
  branch (`origin/decide/adr-0010-hermes`).

## Addendum 2026-10-07 (evening): OpenCode Go is the vehicle

The maintainer decided the same evening (bead coding-harness-ymx, notes): every
review — phase 2a, phase 4b and phase 6 — runs through OpenCode Go, in rounds;
the models must be changeable by a one-line edit to `model-endpoints.yaml`;
Codex leaves the reviewer roles; the loop limit rises from two rounds to three.
That decision replaces §2 (Xiaomi's platform), §7's two `[DECISION]`s and §8's
file list as written there. Nothing below reopens an answer; it adds facts for
phase 2.

**Read on 2026-10-07.** <https://opencode.ai/docs/go/> (the page ends with
"Last updated: Oct 6, 2026"), <https://opencode.ai/docs/zen/>, and
`GET https://opencode.ai/zen/go/v1/models` without a key (HTTP 200). The
legal pages at <https://opencode.ai/legal/terms-of-service> and
<https://opencode.ai/legal/privacy-policy> were read only through search
summaries that day — the contract party is Anomaly Innovations, Inc.
("OpenCode"), which is what the summary says; the full text was not read.

### E · The three models and their ids

| Round | Name on the Go page | Model id | In `GET /zen/go/v1/models` |
|---|---|---|---|
| 1 | DeepSeek V4.1 Flash | `deepseek-v4.1-flash` | yes |
| 2 | MiMo-V2.6-Flash | `mimo-v2.6-flash` | yes |
| 3 | MiMo-V2.6-Pro | `mimo-v2.6-pro` | yes |

The model list that endpoint returned held 44 ids on 2026-10-07, among them
all three above and `glm-5.3`, `glm-5.3-flash`. The Go page states the config
format `opencode-go/<model-id>` — the id in `model-endpoints.yaml` is the part
after the slash, as `glm-5.3` is today.

There is no `mimo v2.6 pro flash` on the page, and no id that could be it.
What the maintainer wrote for round 2 reads as MiMo-V2.6-Flash
(`mimo-v2.6-flash`); the reading is put to the maintainer as the first
`[DECISION]` of `decisions.md`.

### F · The endpoints, and what the page does not say about ours

The Go page carries an endpoint table with one row per model: the id, an
endpoint URL and the AI SDK package. All three of ours are listed there as
`https://opencode.ai/zen/go/v1/chat/completions` with
`@ai-sdk/openai-compatible`. `https://opencode.ai/zen/go/v1/messages` — the
Anthropic-compatible address the maintainer's decision names — is listed on
that page for MiniMax M3 and M2.7, Qwen3.8 Max and Flash, and Qwen3.7 Plus,
not for the three above. The Zen page shows the same split on its own
addresses (`/zen/v1/messages` for the Anthropic models, `/zen/v1/chat/completions`
for the OpenAI-compatible ones).

**Not read:** whether the Anthropic-compatible address accepts the three model
ids. The table shows the address OpenCode recommends per model, and a
recommendation is not a refusal; nothing readable says whether
`POST https://opencode.ai/zen/go/v1/messages` with `model:
deepseek-v4.1-flash` is answered. It cannot be answered without a key, and
this session does not read the secrets file. This is the one fact phase 4 has
to measure before the runner depends on it (see the tagged question at the
end of this section).

Also read on the same page: `GET https://opencode.ai/zen/go/v1/models` needs
no key and lists the ids, so the ids can be checked without a call that costs
anything.

### G · Terms, limits and privacy of OpenCode Go

- **Client conditions.** The page is explicit: a client should "send typical
  coding agent traffic", identify itself with its own user agent rather than a
  generic SDK name, and send a stable session id in `x-opencode-session`. Two
  of the clients it lists as validated are the two this repository already
  runs: **Claude Code** ("Go recognizes its native session header. No
  custom-header wrapper is needed.") and **Codex** ("Go recognizes its native
  session header."). Hermes and Pi are listed as well, with a per-version note
  each.
- **Plans.** Go USD 10 a month, Go Plus USD 40 a month; token prices are the
  same on both. Each model's monthly limit is cut into 5-hour (20%), weekly
  (50%) and monthly (100%) allowances.
- **Prices of the three (per million tokens, Go plan).** DeepSeek V4.1 Flash
  USD 0.15 input / 0.60 output off-peak and 0.30 / 1.20 in peak hours (peak is
  01:00–04:00 and 06:00–10:00 UTC, Monday to Friday), monthly limit USD 60.
  MiMo-V2.6-Flash 0.14 / 0.28, monthly limit USD 60. MiMo-V2.6-Pro 0.435 /
  0.87, monthly limit USD 15. A 5-hour allowance is a fifth of those.
- **Privacy table.** All three: model training "Not used", data retention
  "0 days". The DeepSeek rows carry `0 days*` and the footnote: "ZDR
  agreement is renewed monthly. The current agreement is valid through
  October 31, 2026." — so DeepSeek's zero retention is a dated contract, not a
  standing property, and it has to be read again after that date.
- **Where the models are hosted: not on the Go page.** The Go page's privacy
  section is the training and retention table and nothing else. The Zen page
  states "All our models are hosted in the US and EU." — a statement about
  Zen, on Zen's page. Whether it covers the Go plan was not read.
- **Who is Anomaly Innovations, Inc.** The terms of service are that company's
  (search summary, 2026-10-07); the full text was not read.

### H · How the runner starts a reviewer today

`python3 scripts/stage2.py review-loop <change>` is the closest model for
OpenCode Go: the same Anthropic-compatible shape, so that only the address,
the key and the model ids change.

1. `preflight` — the change folder exists, its `spec.md` carries a `bead` in
   its header, and `declaration_problem` clears the endpoint for `framework`
   content: the entry present, the model listed, `framework` among what it may
   see, a residency that is neither absent nor `nicht-erklaert`.
2. `review_loop` — the round limit, then any undecided rows (each holds the
   next round), then `GLM_KEY` read from the secrets file; a refusal there
   stops the run before anything is written.
3. `change_diff` — the diff against the merge base with `origin/main`,
   uncommitted and untracked files included.
4. One prompt: the body of `prompts/04b-review-loop.md`, the answer format,
   the read request, the diff, the read request again.
5. `begin_call` — the declaration again, then the leak check, then the line in
   `findings.md`.
6. `launch` — the program, started with an empty standard input, in the
   worktree, with an environment built from an allow-list and then the call's
   own variables. `glm_env` sets `ANTHROPIC_BASE_URL`,
   `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`, a fresh empty
   `CLAUDE_CONFIG_DIR` and the model name in all six model variables; the
   arguments pin `--model`, `--effort`, `--tools Read,Grep,Glob`,
   `--restricted`, `--strict-mcp-config`, `--permission-mode dontAsk`,
   `--no-session-persistence` and `--output-format text`.
7. The answer is scrubbed of the key, parsed into rows, numbered
   `L<round>-<k>`, and appended to the loop record outside the worktree.

`CODEX` and `GLM` are the two endpoint tuples the runner pins
(`(endpoint, model, effort)`), and `GLM_BASE_URL` is the one address
constant. The verbs `spec-review` and `review` go through the Codex CLI and
`codex exec resume`; the decision of 2026-10-07 takes both out of the reviewer
roles.

### I · What the leak check needs per call

`begin_call(ctx, verb, endpoint, prompt)` runs, for this one call, in this
order and immediately before it:

1. `declaration_problem(root, endpoint, model)` again — a declaration that
   was cleared at preflight and has since changed is caught here.
2. `leakcheck.check(ctx.change, leakcheck.default_denylist(), ctx.root,
   [("prompt", prompt)])` — the change's folder, every file the tree tracks or
   lists as untracked and not ignored (a symbolic link as its target's text),
   the staged changes, the message and patch of every commit reachable from a
   local or a remote-tracking branch, and the call's own prompt, against the
   denylist the machine keeps outside the repository.
3. The verdict is printed; a non-zero exit raises `Refused` and no call starts.
4. The line is appended to `findings.md`: date, verb, endpoint, model, and the
   three numbers (files, commits, rules).

So one check per call, not one per run: a second reviewer of a round is a
second call and gets its own check, with its own prompt in the list. A rule
whose name starts with `secret:` is not applied under the top-level `tests/`
folder; every other rule is. What cannot be measured is BLOCK, never clean.

### J · What the endpoint declaration looks like

Every entry carries `name`, `betreiber`, `residenz`, `abrechnung`,
`darf_sehen`, `modelle` and `bemerkung` — `tests/test_model_endpoints.py`
fails an endpoint without one of them. The vocabularies are fixed there:
`residenz` one of `anbieter-erklaert`, `region-waehlbar`, `nicht-erklaert`;
`abrechnung` one of `token`, `abonnement`. `declaration_problem` in
`scripts/stage2.py` refuses an entry whose `residenz` is absent or
`nicht-erklaert`, so an entry the runner may call must state one of the other
two. `modelle` is a YAML list; today only membership is read, order carries no
meaning — the decision of 2026-10-07 asks for order to mean the round.

The GLM entry stands beside the `openai-codex` entry, under the comment block
that says `darf_sehen: [framework]` is the line that matters here, not the
residency, and that the leak check — not this file — is what keeps customer
content out. The German keys and comments of the file are translated in a pull
request of their own (house rule 1).

### K · What a change touches

- `model-endpoints.yaml` — the entry `opencode-go`, its ordered `modelle`, and
  the comment block behind it.
- `scripts/stage2.py` — the endpoint tuple(s), the address constant, the
  reading of the ordered list, the round limit, and the verbs `spec-review`
  and `review` moving off the Codex CLI.
- `docs/adr/0007-stage-2-reviews-by-codex-and-glm.md` — amended by a decision
  pull request; `docs/adr/` is `human-decided`, so the amendment text is
  drafted in this folder and never edited in place.
- `docs/WORKFLOW.md` §4, `prompts/01-explore.md` is untouched (explore and
  implement stay on GLM 5.3 Flash), `prompts/02-spec.md`, `prompts/04b-review-loop.md`,
  `prompts/06-review.md`, `AGENTS.md` — who reviews what.
- `tests/test_stage2.py`, `tests/test_model_endpoints.py` — the declaration,
  the ordered list and the verbs.

### Tagged questions

**[GAP]** Does `POST https://opencode.ai/zen/go/v1/messages` accept the model
ids `deepseek-v4.1-flash`, `mimo-v2.6-flash` and `mimo-v2.6-pro`, or only the
ids the page lists under that address? Not answerable by reading (§F) and not
without the key. Measured in phase 4, before any step builds on it: one call
per model id through the runner, the leak check in front of it. If the address
refuses a model id, the run stops and is reported — no second design is
invented in this change.

**[GAP]** Where OpenCode hosts the Go models. The Go page states no region
(§G); Zen states "US and EU" for Zen's models. Not closed by reading here.

**[DETAIL]** OpenCode's terms of service and privacy policy in full — read by
search summary only on 2026-10-07. The part that matters for the declaration
(the client conditions and the retention table) is on the Go page and was read
there; the contract text is named in the entry's `bemerkung` with the date it
was looked at, and is read in full before phase 7 writes the pull request.

**[DETAIL]** What DeepSeek's ZDR agreement looks like after 2026-10-31. The
Go page dates it (§G); the check is a calendar entry for the maintainer, not a
code path.

