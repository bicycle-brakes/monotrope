---
title: "Research — stage2-flash-runner"
status: draft
implementation_status: none
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
supersedes: null
superseded_by: null
bead: coding-harness-qcp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, stage-2, flash-runner]
---

Phase 1 per `prompts/01-explore.md`. Facts only, read 2026-10-07 in worktree at
`1952ac8` (branch `feat/stage2-flash-runner`). Open item O-1 of bead
coding-harness-qcp: build two verbs in `scripts/stage2.py` for GLM 5.3 Flash
to run phase 1 (explore) and phase 4 (implement) against Z.ai's endpoint,
behind the leak check, with fallback to Haiku 4.5/Sonnet 5.5 when stage 2 is
off.

## 1 · How the runner works today

### 1.1 scripts/stage2.py structure

The file `scripts/stage2.py` (read 2026-10-07, lines 1–905) is the runner.
Four verbs exist:

| Verb        | Phase | Endpoint         | Model       | Handler          |
|-------------|-------|------------------|-------------|------------------|
| spec-review | 2a    | openai-codex     | gpt-6.1-sol | spec_review()    |
| review-loop | 4b    | glm-coding-plan  | glm-5.3     | review_loop()    |
| release-loop| —     | —                | —           | release_loop()   |
| review      | 6     | openai-codex     | gpt-6.1-sol | review()         |

Missing: `explore` (phase 1) and `implement` (phase 4), both for GLM 5.3 Flash.

### 1.2 GLM call pattern from review_loop

Lines 789–852 show the pattern for GLM 5.3 calls:

1. Preflight checks (line 791): folder exists, endpoint declared, bead found.
2. Leak check (line 809): `scripts/leakcheck.py` scans repository, changes,
   commits and prompt. Exit 0 required; otherwise raises `Refused`.
3. Record the call (lines 444–448): date, verb, endpoint, model, leak stats
   in `findings.md`.
4. Build prompt (lines 806–808): read from `prompts/04b-review-loop.md`,
   append `ANSWER_FORMAT` and `READ_REQUEST`, wrap diff.
5. Launch Claude Code (lines 815–835):
   - Model: `GLM[1]` = `"glm-5.3"` (line 77)
   - Effort: `GLM[2]` = `"max"` (line 77)
   - Tools: `"Read,Grep,Glob"` only (line 826)
   - Environment: `glm_env(key, config_dir)` (line 835)
6. Environment setup (lines 203–212, `glm_env()` function):
   - Base URL: `"https://api.z.ai/api/anthropic"` (line 78)
   - Auth: `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` from GLM_KEY
   - GLM_MODEL_VARIABLES (lines 108–115) set to model name
   - Empty config directory
   - `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`
7. Secret handling: GLM_KEY from `~/.config/cc-routing/secrets.env` (line
   801), scrubbed from stdout (line 838).

### 1.3 Infrastructure for Flash

`model-endpoints.yaml` (lines 111–127):

- Endpoint `glm-coding-plan` lists both `glm-5.3` and `glm-5.3-flash`
- `darf_sehen: [framework]` — framework content only
- Residency `anbieter-erklaert`, billing `abonnement`
- Note: Flash models decided for phases 1 and 4, verbs not built yet

`prompts/01-explore.md` (line 3): "Model: GLM 5.3 Flash — much input, little
output, no deep reasoning; through the runner and the leak check
(`docs/WORKFLOW.md` §4). Until the runner starts this phase, Haiku 4.5
explores."

`prompts/04-implement.md` (lines 3–6): "Model: GLM 5.3 Flash — a solid worker
given a clear plan; through the runner and the leak check (`docs/WORKFLOW.md`
§4). Until the runner starts this phase, Sonnet 5.5 at effort `medium` builds."

`WORKFLOW.md` §4 (lines 622–627): "The two Flash rows are decided and not
built. The runner has no verb that starts phase 1 or phase 4 on GLM 5.3 Flash
… Until that is built (an open item of the change that wrote this section,
`plans/changes/stage-2-codex-glm/plan.md`, Amendment 1), §3's rows run both
phases: Haiku 4.5 explores and Sonnet 5.5 implements."

ADR 0007 (lines 58–71): "Implementation runs on GLM 5.3 Flash instead of
Sonnet 5.5" and "Exploration runs on GLM 5.3 Flash too, instead of Haiku 4.5"
(maintainer decisions, 2026-10-06).

### 1.4 Environment allow-list

`ENV_ALLOW` (lines 94–107): PATH, HOME, USER, LOGNAME, SHELL, TMPDIR, LANG,
LC_ALL, LC_CTYPE, TERM, TZ, CODEX_HOME. Only these from caller's environment
are passed.

`GLM_MODEL_VARIABLES` (lines 108–115): ANTHROPIC_MODEL,
ANTHROPIC_DEFAULT_OPUS_MODEL, ANTHROPIC_DEFAULT_SONNET_MODEL,
ANTHROPIC_DEFAULT_HAIKU_MODEL, ANTHROPIC_SMALL_FAST_MODEL,
CLAUDE_CODE_SUBAGENT_MODEL. All set to model name for GLM (line 211).

### 1.5 Preconditions before each call

`preflight()` (lines 395–404) and `begin_call()` (lines 432–448):

1. Change folder exists
2. `spec.md` has bead in header
3. Endpoint declared in `model-endpoints.yaml`: present, model listed,
   framework in `darf_sehen`, residency not "nicht-erklaert"
4. Leak check passes
5. `findings.md` created if missing, with proper header
6. Call line recorded

### 1.6 Explore vs. implement

Explore (phase 1):

- Reads repository broadly
- Writes only `research.md` (no code)
- No `make verify` gate
- Input: change name only
- Output: research findings

Implement (phase 4):

- Reads tree and writes code to worktree
- Reads `spec.md` and `plan.md`
- Must commit per green step (AGENTS.md house rule, prompts/04-implement.md)
- Runs `make verify` after changes (WORKFLOW.md §4, line 583)
- Input: spec.md, plan.md, appetite
- Output: code + tests

Both Flash calls:

- Same Z.ai endpoint (`glm-coding-plan`)
- Same Flash model (`glm-5.3-flash`)
- Leak check before call
- Tools restricted to Read, Grep, Glob
- Full repository context

## 2 · What must change in scripts/stage2.py

### 2.1 Model constants

Currently: `GLM = ("glm-coding-plan", "glm-5.3", "max")` (line 77) for
review-loop.

Need: Separate constants:

```python
GLM = ("glm-coding-plan", "glm-5.3", "max")        # review-loop (4b)
GLM_FLASH = ("glm-coding-plan", "glm-5.3-flash", "max")  # explore, implement
```

### 2.2 Two new verbs

`explore(root: Path, change: str)`:

- Like `spec_review()` but for phase 1, GLM Flash
- Input: phase prompt from `prompts/01-explore.md`, change name
- Reads full repository context
- Output: `plans/changes/<change>/research.md`
- No `make verify` gate

`implement(root: Path, change: str)`:

- Like `review_loop()` but for phase 4, GLM Flash
- Input: `prompts/04-implement.md`, spec.md, plan.md
- Reads tree, writes code to worktree
- Output: code + tests + commits
- Gate: `make verify` green after call

### 2.3 Prompt building

Both use `phase_prompt()` (lines 451–458):

- Read prompt file
- Append change name
- Append format instructions and read request
- Implement: also append spec.md and plan.md content

### 2.4 Make verify after implement

Implement must run `make verify` after the call (WORKFLOW.md §4, line 583).

Not read: whether runner runs it or implementer does. Current design: runner
launches, implementer checks. Recommendation for plan: implementer runs
`make verify` after call returns.

## 3 · Files touched by this change

- `scripts/stage2.py`: add two verbs, add `GLM_FLASH` constant
- `prompts/01-explore.md`: no change (already names Flash)
- `prompts/04-implement.md`: no change (already names Flash)
- `model-endpoints.yaml`: no change (already declares Flash)
- Tests: defer to phase 4 plan

## 4 · Reuse from review_loop

| Piece            | Source           | Reuse   |
|------------------|------------------|---------|
| Preflight checks | preflight()      | Yes     |
| Leak check       | begin_call()     | Yes     |
| Prompt building  | phase_prompt()   | Partial |
| Environment      | glm_env()        | Yes     |
| Launch command   | review_loop()    | Yes     |
| Tool restrictions| line 826         | Yes     |
| Secret scrubbing | scrub()          | Yes     |

Largest reuse: environment setup, launch, secret handling, preconditions.
New work: prompt building (different inputs), output recording
(research.md/code vs. loop.md).
