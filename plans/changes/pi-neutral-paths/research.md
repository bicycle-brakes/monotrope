---
title: "Research — pi-neutral-paths"
status: draft
implementation_status: none
date: 2026-10-29
last_reviewed: 2026-10-29
updated: 2026-10-29
supersedes: null
superseded_by: null
bead: coding-harness-xul8
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: glm-5.3-flash, version: "2026-10-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
---

# pi neutral paths — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md). The
section below is the runner's exploration, appended as GLM 5.3 Flash answered
it; its first sentence and its closing process note are the model's own words.

Stage-2 call, 2026-10-29: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 728 files, 2557 commits, 12 rules.

## Runner exploration — 2026-10-29

I have the full picture. Here is the research, ready to append to `plans/changes/pi-neutral-paths/research.md`.

---

## What exists today

**The mechanism the bead names.** Every Pi call embeds two local absolute paths into its system prompt, built by Pi itself, outside the runner's control through the prompt text:

- The **working directory**. The pinned Pi 1.2.0 builds its structured system prompt in `buildSystemPromptSections` and adds, unconditionally and outside every flag branch, `promptSections.cwd = cwd.replace(/\\/g, "/")` (`tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/system-prompt.js:110`, section rendered as `<cwd>…</cwd>` per lines 115–119; sections reach the model through `getSystemMessageText`, `tools/pi/node_modules/@earendil-works/pi-ai/dist/utils/text.js:11-18`, joined after the prompt content). The `cwd` value is Pi's process working directory (`dist/core/resource-loader.js:245`, `this.cwd = resolvePath(options.cwd)`).
- The **documentation paths**. Unless a custom preamble replaces the base prompt, the `<docs>` section names `getReadmePath()`, `getDocsPath()` and `getExamplesPath()` — all `resolve(join(getPackageDir(), …))`, i.e. absolute paths into the pinned install under the worktree (`dist/core/system-prompt.js:88-95`, `dist/config.js:361-371`). These point at `tools/pi/node_modules/@earendil-works/pi-coding-agent/…` inside the checkout, so the local absolute path — including the account name, as in `/Users/mikypiky/coding-harness/.claude/worktrees/<name>` (the same shape recorded in `plans/changes/pi-pin/findings.md:214`) — travels in **every** Pi call regardless of the working directory.

**What the runner passes today.** The repository's launch sites start Pi with `--append-system-prompt <file>` (Pi reads file contents for that flag, `dist/cli/args.js:75-77` and the help text at line 298) and never with `--system-prompt`. The discovery flags the runner passes (`--no-context-files`, `--no-skills`, `--no-prompt-templates`, `--no-themes`, `--no-extensions`, `--no-mcp`) suppress the other context sections but not `<cwd>` and not `<docs>` — the `<docs>` block sits in the base `else` branch, the `<cwd>` line outside both branches (`dist/core/system-prompt.js:78-110`).

**Who receives what.** Per seat, the runner sets the working directory that becomes `<cwd>`:

- Research swarm, repository seats (topics 1–8): `cwd = self.root`, the worktree itself (`scripts/stage2_research_run.py:769`, in `pi_command`), with read tools `read,grep,find,ls` (`scripts/stage2.py:244`, `PI_TOOLS`) and the path-lock extension (`scripts/stage2_repository_pathlock.mjs`, loaded at `scripts/stage2_research_run.py:750-756`). The path lock confines tool *reads* to the worktree; it says nothing about the system prompt.
- Research swarm, online seats (public topics 9–11) and free seats: `cwd = scratch`, a `tempfile.TemporaryDirectory` (`scripts/stage2_research_run.py:745` and the scratch setup at 695–699) — still a local absolute path, though not the worktree; the `<docs>` section still names the worktree install.
- Review loop (phase 4b), paid rungs (Flash swarm and ladder): `cwd = ctx.root`; free members: scratch (`scripts/stage2.py:2584-2594`, `scratch if free else ctx.root` in the `dispatch_go` call inside `run_go_reviewer`, command built at 2547–2567).
- Availability probes: a fresh scratch directory (`scripts/stage2_availability.py:482-514`) — yet the `<docs>` section still names the worktree install, so the probe payload carries more than the "fixed probe text, with no … repository content" that criterion 47 of `plans/changes/research-swarm/spec.md:459-460` promises.
- Interactive session: `cwd=root` (`scripts/stage2_session.py:299`, wrapper selected at 245).
- Catalog refresh and pin check: `pi update --models` / `--list-models` / `--version` from scratch (`scripts/stage2.py:2119, 2167, 2469`) — no model-facing prompt beyond the version output, but the same sections apply to the first two.

**Existing adjacent mechanisms, so the boundary is stated precisely:**

- The leak check (`scripts/leakcheck.py`) scans the *exact prompt* before every call (swarm: `scripts/stage2_research_run.py:490-491`; loop: `scripts/stage2.py:1386`; review of the loop's guarantees: `plans/changes/research-swarm/spec.md:354`). Its rules come from a denylist outside the repository (`default_denylist()` → `~/.config/cc-routing/denylist.txt`, `scripts/leakcheck.py:132-137`); Pi's own prompt sections are *not* part of the scanned text, so they pass unseen.
- The admission rules distinguish data classes: private roles (finder, repository, merge, topic author, judge) require an endpoint with `darf_sehen: framework` and a stated residency; the online and free roles are class `public-web` and run on OpenCode Go without that admission (`scripts/stage2_swarm.py:313-316, 382-429`). The free models' acceptance in `model-endpoints.yaml` (the `hinweis` block, lines 400–407) is purpose-bound ("diff-only review purpose alone", terms "NOT read") — local machine paths were not part of any stated purpose.
- The attended capture harness already records `cwd` and a `system_prompt_excerpt` per seat (`scripts/research_capture.py:1068, 1207, 1223-1231`), and the handover ties this bead to the capture's first live run: "First live run waits for bead coding-harness-xul8" (`docs/journal/handover/2026-10-28-three-lane-night.md:72-75`); the change itself is announced in the night plan as "the research swarm sends local absolute paths to online models through Pi's system prompt" (`docs/research/2026-10-28-night-run-plan.md:149-150`).
- Prior work covered the *incoming* direction only: the path lock (Q-16, `plans/changes/research-swarm/decisions.md:647-649`; spec detail at `plans/changes/research-swarm/spec.md:934-945`) and, for the review loop, the documented read-boundary residual risk ("the pinned Pi 1.2.0 has no sandbox, and `read` resolves absolute paths without containment", `docs/WORKFLOW.md:1277-1286`). The *outgoing* system-prompt direction is not covered anywhere in `plans/` — a search for `cwd|absolute path` across `plans/changes/research-swarm/` returns only the read-lock material.

## Where it lives

- Pi side (vendored, version-locked by `tools/pi/package.json` pin 1.2.0, install untracked per `.gitignore:41`): `dist/core/system-prompt.js:68-121` (section assembly, `<cwd>` at 110, `<docs>` at 88–95), `dist/core/resource-loader.js:244-295, 475-494` (cwd and prompt sources), `dist/cli/args.js:72-77` (the only two prompt flags), `dist/config.js:352-371` (package-dir-derived absolute doc paths).
- Runner side: `scripts/stage2_research_run.py:688-769` (`pi_command`, cwd choice), `scripts/stage2.py:2532-2594` (`run_go_reviewer`), `scripts/stage2_availability.py:482-520` (probe), `scripts/stage2_session.py:245-299` (session), `scripts/stage2.py:2119, 2167` (catalog), `scripts/research_capture.py` (capture, wrapper at 704/956).
- Prompt texts: `prompts/research-swarm/*.md` carry no absolute paths — the only placeholders are `{{TOPIC}}`, `{{TOPIC_ID}}`, `{{TOPIC_NAME}}`, `{{TOPIC_SCOPE}}` (`prompts/research-swarm/public.md`, `repository.md`). The leak arrives through Pi's sections, not through the repository's prompt templates.

## What is unclear about it

- **Whether Pi offers a supported lever.** From the installed dist: `--system-prompt` feeds `systemPromptSource` → the base prompt, which lands as the *preamble* only (`system-prompt.js:78-96`), leaving `<cwd>` and `<docs>` in place; `forceSystemPrompt` (full replacement, `system-prompt.js:126-129`) and `systemPromptOverride`/`appendSystemPromptOverride` (`resource-loader.js:275-276`) are loader options with no CLI flag in `dist/cli/args.js`. Whether a Pi *extension* can rewrite or remove sections at runtime was not examined — the extension API surface (`dist/core/extensions/types.d.ts`) is unread. This is the pivotal open question: it decides between "neutralize the cwd value" and "suppress the sections".
- **The repository-seats dependency on cwd.** The path lock takes its root from `process.cwd()` (`scripts/stage2_repository_pathlock.mjs:135`), and Pi's read/grep/find/ls default to the working directory. A change that moves the cwd must state where the lock and the tools get the worktree root instead.
- **The leak check's denylist content.** The 12 rules live in `~/.config/cc-routing/denylist.txt`, outside this repository; not read, so whether any rule already matches local absolute paths is unknown.
- **The Claude Code launcher side.** Finder merge, topic author and judge run Claude Code, not Pi (`scripts/stage2_swarm.py:318`), with the same cwd choice (`scripts/stage2_research_run.py:685`); whether Claude Code embeds the working directory in its context is not measurable from this repository. The bead names Pi's system prompt; the boundary to the `claude` launcher is undecided.
- **Scope boundary.** The night plan names the research swarm; the same mechanism serves the review loop, the probes and the session. Whether the change covers all Pi launches or only the swarm's is a decision, not a fact.
- Not found versus not there: no flag, setting or runner code that neutralizes, rewrites or suppresses Pi's `<cwd>`/`<docs>` sections was found in `scripts/`, `tests/`, `prompts/` or the pinned dist ("not found" after search); nothing in `plans/` documents a prior decision about the outgoing prompt direction ("not there" as far as `plans/changes/` and `plans/specs/` show — `plans/specs/` holds only `implementation-verification`).

## Which files a change would have to touch

- `scripts/stage2_research_run.py` — `pi_command` (and `claude_command` if the Claude side follows); the seat cwd decisions at lines 745, 769, 685.
- `scripts/stage2.py` — `run_go_reviewer`'s command construction and its `dispatch_go` cwd argument (2532–2594).
- `scripts/stage2_availability.py` — the probe launch, if probes are in scope.
- `scripts/stage2_session.py` — the session launch, if the session is in scope.
- `scripts/stage2_repository_pathlock.mjs` — only if the lock's root must decouple from `process.cwd()`.
- Tests that pin the current shape: `tests/test_stage2.py` (~5060–5090: the exact `PI_FLAGS` list, `--append-system-prompt`, the file name `review-prompt.md`), `tests/test_stage2_swarm.py:195`, `tests/test_stage2_research_availability.py:59` (fakes reading the prompt-file option), `tests/test_pi_contract.py` (a real-Pi contract would be the place a system-prompt guarantee is measured), `tests/test_research_capture.py` (capture records `cwd` and `system_prompt_excerpt`).

## Neighbours

`plans/changes/research-swarm/spec.md` (path lock Q-16, criteria 12/23/47/52, data-class admission), `plans/changes/pi-pin/spec.md` (the wrapper contract, ADR 0019 — the runner may only start the pinned Pi through `tools/pi/pi`), `plans/changes/stage2-session/spec.md` (the session route). Context, not specs: `docs/adr/0019-repository-pinned-pi-and-contract-tests.md`, `docs/adr/0020-phase-1-research-swarm.md`, `docs/adr/0021-review-swarms-until-clean.md`. Suggested header line: `neighbours: [plans/changes/research-swarm/spec.md, plans/changes/pi-pin/spec.md, plans/changes/stage2-session/spec.md]`.

---

One process note for the runner: the file's frontmatter block still says `provenance: human-written` — per the skeleton's own instruction (`plans/changes/pi-neutral-paths/research.md:21-25`), filling it with this model's output sets `ai-drafted-reviewed` with `produced_by:` and `review:`.

## Addendum 2026-10-29 — the extension lever, read by the orchestrating session

Added by a Claude Code (Opus 5.5) session after the maintainer widened the
scope; it closes the exploration's "pivotal open question" (whether a Pi
extension can rewrite the sections) by reading the pinned Pi 1.2.0 install.
Not measured on a live call.

- **An extension can rewrite the prompt before every run.** The extension API
  declares a `before_agent_start` event whose `systemPromptOptions` are
  "Mutable prompt sections. Later handlers observe mutations made by earlier
  handlers", and whose result may carry `systemPrompt`, which will "Replace the
  complete system prompt for this turn"
  (`tools/pi/node_modules/@earendil-works/pi-coding-agent/dist/core/extensions/types.d.ts:720-743, 1125-1129`).
  The options include `cwd` and `customPrompt`
  (`dist/core/system-prompt.d.ts:5-50`).
- **What the two fields do to the leaking sections.** `<cwd>` renders
  `options.cwd` unconditionally; `<docs>` renders only when `customPrompt` is
  empty (`dist/core/system-prompt.js:78-110`). A handler that sets `cwd` to a
  neutral literal and `customPrompt` to the default preamble would drop both
  paths and leave the tools, rules and addendum in place. Whether Pi's tools
  read their root from these options or from the session's own working
  directory was not read; the latter is what the repository seats' path lock
  relies on (`scripts/stage2_repository_pathlock.mjs:135`).
- **Two further hooks exist** if the system prompt is not the only carrier:
  `context_with_system` (the full transcript including system messages,
  "sent as returned") and `before_provider_request` (can replace the provider
  payload) (`types.d.ts:679-697`). The second sees exactly what leaves the
  machine and is the natural place for a capture check.
- **Explicit extensions load under `--no-extensions`.** The repository seats
  already start Pi with `--no-extensions` and `-e <path lock>`
  (`scripts/stage2_research_run.py:747-757`), and the session does the same
  (`scripts/stage2_session.py:383-391`). The review loop
  (`scripts/stage2.py:2548-2567`) and the availability probe
  (`scripts/stage2_availability.py:499-514`) load no extension today.
- **Which launches send a model call through Pi** (the maintainer's scope,
  read at `6bbe4fbf`): the research swarm's seats
  (`stage2_research_run.py:701`), the review loop's free, Flash and ladder
  members (`stage2.py:2548`), the availability probes
  (`stage2_availability.py:499`) and the interactive session
  (`stage2_session.py:384`). `pi update --models`, `--list-models` and
  `--version` (`stage2.py:2119, 2167, 2469`) call no model. GLM 5.3 Flash's
  explore and implement run through Claude Code, not Pi
  (`stage2.py:1360`, producer `claude-code` for `glm-coding-plan`).
- **Tool results were not read.** Whether `ls`, `find` or `grep` results of a
  repository seat carry absolute paths is not measured; a payload-level
  capture would show it.
