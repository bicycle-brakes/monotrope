---
title: "Pi 1.2.0 on a context overflow — compaction off fails, compaction on summarises and retries"
category: research
created: 2026-11-03
updated: 2026-11-03
last_reviewed: 2026-11-03
owner: framework-architect
status: current
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-03"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-ut8q
tags: [review-loop, stage-2, diff-bound, pi, compaction, context-window, adr-0021, spike]
---

# Pi 1.2.0 on a context overflow

**Result: with `compaction.enabled: false` in the agent settings, the pinned
Pi fails cleanly on a prompt over the model's context window.** In the
runner's own output mode (`--print`, text) Pi exits 1, prints the provider's
400 error on stderr and nothing on stdout; `run_reviewer` raises `CallFailed`.
No summary is written and no second request is sent. With compaction left on
(today's runner), Pi does not fail at once: it asks the model for a summary,
retries once, and only then gives up. On today's prompt layout the retry
cannot succeed, because the oversized text sits in the system prompt, which
compaction never shortens. The risk of a silent summary is in the tool reads
a paid reviewer makes, not in the diff itself.

This answers point 2 of bead coding-harness-ut8q (a diff over the 2000-line
bound can never end the review loop cleanly): what Pi does on a provider
overflow once compaction is off.

## Method

Measured on 2026-11-03 between 01:12 and 01:15 UTC, origin/main at
`019853f1`, Pi `@earendil-works/pi-coding-agent` 1.2.0 through
`tools/pi/pi`, endpoint `opencode-go`.

1. **Catalog.** `stage2.discover_free` ran the runner's forced live refresh
   (`pi update --models`) and returned the store the runner activates as its
   overlay. Each model's `contextWindow`, `maxTokens` and `cost` were read
   from there (01:12 UTC).
2. **Calls only through the runner.** A small driver imported
   `scripts/stage2.py` and called, per call, `preflight` (the declaration),
   `begin_call` (the leak check and the audit line) and `run_reviewer`
   (Pi's launch), in that order. The leak check was clean on every call
   (838 files, 3107 commits, 12 rules). The driver changed one function:
   it wrapped `stage2.launch` so that, for the Pi `--print` call only, the
   agent `settings.json` gained `"compaction": {"enabled": false}` (or
   `true`), next to the runner's `"retry": {"enabled": false}`. Two calls
   also got `--mode json` after `--print`, for Pi's event stream. Each call
   ran with `--no-tools` (`run_reviewer(..., free=True)`), so the prompt was
   the only content.
3. **Prompt.** One header line, then `docs/WORKFLOW.md` repeated to
   1.2 × the catalog window × 4 characters (1.23–1.26 million characters).
   The runner's layout: the text goes in through `--append-system-prompt`,
   the user message is one short line.
4. **Bound on cost.** No oversized call went to a model whose catalog
   window is above 300,000 tokens. At most two calls per model.

The audit lines the runner wrote (into a scratch change folder that is not
committed):

```
Stage-2 call, 2026-11-03: probe · endpoint opencode-go · model hy3 · leak check clean over 837 files, 3107 commits, 12 rules.
Stage-2 call, 2026-11-03: probe · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 838 files, 3107 commits, 12 rules.
Stage-2 call, 2026-11-03: probe · endpoint opencode-go · model hy3 · leak check clean over 838 files, 3107 commits, 12 rules.
```

## The calls

| # | Time (UTC) | Model | Compaction | Output mode | Exit | What came back |
|---|---|---|---|---|---|---|
| 1 | 01:12:55 | hy3 | off | json | 0 | One assistant message, `stopReason: "error"`, no text. Provider: `400 … This endpoint's maximum context length is 262144 tokens. However, you requested about 314571 tokens`. No `compaction_*` event. One request. 3.4 s. |
| 2 | 01:13:39 | kimi-k2.7-code | off | text (the runner's) | **1** | stdout empty; stderr `400: … Your request exceeded model token limit: 262144 (requested: 316150)`. `run_reviewer` raised `CallFailed`: `pi call failed: exit 1 (400: …)`. 4.2 s. |
| 3 | 01:14:11 | hy3 | **on** | json | 0 | First request: the same 400. Then `compaction_start` (reason `overflow`), a summary request (1,544 tokens, 0.0008 USD by the catalog price), a `compaction_end` with the summary `No prior history. … The user asked the assistant to answer … in one short line.` (`tokensBefore` 307,774, `estimatedTokensAfter` 307,915), a retry, the same 400, and a last `compaction_end`: `Context overflow recovery failed after one compact-and-retry attempt.` No assistant text. 18.2 s. |

What the three calls show:

- **Compaction off: one request, one error, no summary.** Pi sends the
  oversized request (it does not refuse it before the call), the provider
  rejects it, and Pi stops. In text mode the exit code is 1, so the runner
  already counts it as a failed member (`CallFailed`), not as an empty
  answer.
- **Compaction on: the summary happens, it just cannot help here.** Pi's
  overflow recovery (`_checkCompaction`, `dist/core/agent-session.js`
  around line 2361) summarised the messages — the one-line user message —
  and retried. The system prompt holding the filler stayed whole, so the
  retry overflowed again. A reviewer whose context grows through **tool
  reads** (messages, not system prompt) is the case where this summary can
  succeed silently and the member answers on a summary. That case was not
  measured (below).
- **In `--mode json` Pi exits 0 even on the error.** Only text mode turns the
  error into exit 1. The runner uses text mode; a future change to json
  mode would have to read `stopReason` itself.
- **The catalog can be smaller than the endpoint.** hy3: catalog 256,000,
  endpoint 262,144. kimi-k2.7-code: catalog and endpoint both 262,144. Both
  differences are on the safe side.
- **Token count.** The providers counted 314,570 and 316,150 tokens for
  1,229,028 and 1,258,519 characters: about 3.9 characters per token on
  this repository's English Markdown.

The code agrees with the measurement: `shouldCompact`
(`dist/core/compaction/compaction.js:173`) and `_checkCompaction` both return
early when `compaction.enabled` is false, and the between-turn check
(`_compactBeforeNextAssistantResponse`) uses `shouldCompact`. So all three
automatic paths — threshold before a turn, threshold after a turn, overflow
recovery — are off together. The project-level `.pi/settings.json` is not a
way to set this: the runner passes `--no-approve`, which ignores
project-local files; the agent directory's `settings.json`, which the runner
already writes, is the place.

## Context windows of the admitted models

From Pi's live catalog, 2026-11-03 01:12 UTC. "Endpoint" is the limit the
provider stated in its 400; only measured where a call was sent.

| Model | Stage | Catalog window | Endpoint window | Oversized call |
|---|---|---|---|---|
| deepseek-v4.1-flash | Flash, ladder | 1,000,000 | not measured | not sent (window > 300k) |
| mimo-v2.6-flash | ladder | 1,048,576 | not measured | not sent (window > 300k) |
| longcat-2.0 | Flash, ladder | 1,000,000 | not measured | not sent (window > 300k) |
| glm-5.3-flash | ladder | 1,000,000 | not measured | not sent (window > 300k) |
| hy3 | ladder | 256,000 | **262,144** | sent, calls 1 and 3 |
| mimo-v2.6-pro | Flash, ladder | 1,048,576 | not measured | not sent (window > 300k) |
| hy4-preview | ladder | 1,024,000 | not measured | not sent (window > 300k) |
| kimi-k2.7-code | ladder | 262,144 | **262,144** | sent, call 2 |
| deepseek-v4-pro | ladder | 1,000,000 | not measured | not sent (window > 300k) |
| glm-5.2 | ladder | 1,000,000 | not measured | not sent (window > 300k) |
| glm-5.3 | ladder | 1,000,000 | not measured | not sent (window > 300k) |
| kimi-k3 | ladder | 1,048,576 | not measured | not sent (window > 300k) |
| mimo-v2.5, mimo-v2.5-pro | ladder (not reachable since 2026-10-30) | 1,000,000 / 1,048,576 | not measured | not sent |
| cat-jam-free | free (selected by the free rule today) | 262,144 | not measured | not sent (free class) |
| longcat-2.5-preview-free | free (selected by the free rule today) | 1,000,000 | not measured | not sent (free class) |

The ladder order and the Flash members are `stage2.ladder` and the entry's
`flash_swarm` on 2026-11-03. Declared paid models the runner skips (wire API
not measured or no terms) were not looked at.

## Not measured, and why

- **The overflow from tool reads.** A paid reviewer reads files; their
  content enters as tool results, which compaction does summarise. Building
  that case needs a model that reads past its window on purpose — more
  calls and a cost the brief did not cover. The code path is the same
  `enabled` check, so compaction off should fail there too; this is read,
  not measured.
- **Text-mode exit code with compaction on.** Call 3 ran in json mode for the
  events; json mode exits 0 regardless. Not repeated in text mode (two calls
  per model).
- **The windows above 300,000 tokens.** Ten of the twelve reachable models
  (2026-11-03): the brief capped the probe there on cost; their endpoint
  limits are unknown and could be lower than the catalog, as hy3's was not.
- **The free models.** The free class is admitted for one purpose only: a
  tool-free review of the implementation diff (`free_stage` in
  `model-endpoints.yaml`, ADR 0021 decision 3; their data terms are not
  read). A documentation filler is outside that purpose, so no call went to
  them.
- **Whether Go counts a rejected request against the subscription.** The
  rejected requests reported zero usage; what Go's quota counted was not
  read.
- **The control call.** Not needed: both oversized calls with compaction off
  failed clearly.

## A finding on the side: Pi's own system prompt

Every call carried Pi's own `<docs>` section with the absolute path of the
pinned install (it names the home directory and the worktree) and a
`<cwd>` scratch path. The runner's leak check never sees that text. This is
the known bug coding-harness-xul8 (Pi's system prompt sends local absolute
paths to online models), which the review loop shares; these three calls
carried it like every review-loop call does. It needs no new bead, but it
means the fix in coding-harness-xul8 covers the review loop too.

## Recommendation for the 2000-line bound

**Keep the bound for now, switch compaction off, and count an overflow as a
member failure.** In order:

1. **Write `"compaction": {"enabled": false}` into the agent
   `settings.json` that `run_reviewer` already writes** (next to
   `retry`), and in `discover_free`'s and every other Pi agent directory
   the runner writes. Measured: an overflow then ends as exit 1 and
   `CallFailed` — a failed member, never an answer on a summary. This
   removes the reason the bound was introduced (R-15 of the review-swarm
   review). One test should pin the settings file's content.
2. **Keep `REVIEW_DIFF_MAX_LINES` and the split the maintainer chose
   (2026-10-26: at most four parts of 2000 lines, each reviewed in full).**
   The bound is no longer a guard against summaries but a guard on cost and
   on how much a member can attend to. It is far below every window: a
   diff line of this repository averages about 86 characters (the last 30
   commits on origin/main, `019853f1`), so 2000 lines are about 44,000
   tokens, and four parts about 176,000 — under the smallest admitted
   window (256,000) even before tool reads.
3. **Do not derive a per-model bound from `contextWindow` yet.** The
   catalog was right or low on the two models measured, but ten endpoint
   limits are not measured, and the tool reads, not the diff, decide when a
   member overflows. With compaction off a wrong guess costs one failed
   member, not a wrong clean round, so a per-model bound buys little today.

ADR 0021 needs an amendment only if the runner should name the overflow as
its own failure kind in the round record; counting it as an ordinary failed
member, as `CallFailed` already does, fits the ADR as it stands (not checked
against the ADR's text clause by clause).
