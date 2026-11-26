---
title: "Decisions — pi-work-route"
status: draft
implementation_status: none
date: 2026-11-25
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-363r.3
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "Opus 5.5, 2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, routing, pi, opencode-go, interview]
---

# pi-work-route — Decisions

Phase-1a interview with the maintainer, 2026-11-25 (session 9200c6b1), on the partial research of explore run 2 (run f171ca7b…; repository topics 1, 2 and 4 timed out, every other slot valid; the maintainer chose to go on with the partial research).

## Q-1 · Scope of the change

asked: 2026-11-25
answer: "All three parts: (1) fallback — when the normal implement/repair route fails, implement and repair run through Pi on OpenCode Go; (2) model choice — GLM 5.3 Flash or DeepSeek V4.1 Flash as a declared parameter of the one route (house rule 9), not a second verb; (3) GLM off Claude Code — GLM 5.3 / 5.3 Flash for explore, implement and loop start through Pi instead of Claude Code."
answered_by: maintainer
status: answered
context: |
  Topic: what this change delivers.
  Intention: implement and repair keep running when Claude Code or Z.ai is exhausted (both were on 2026-11-25).
  Today: GLM 5.3 Flash starts only through Claude Code on Z.ai; DeepSeek through Pi only interactively (session verb).
  Repository change: scripts/stage2.py routes, model-endpoints.yaml (opencode-go widened to work verbs), tests.
  Architecture change: the work verbs gain a Pi route on OpenCode Go (new ADR, Q-4).

In the context of work verbs that stop when Claude Code or Z.ai is exhausted, facing a narrow or a full scope, we decided to build all three parts (fallback, model choice, GLM off Claude Code), to achieve one Pi route for every work verb, accepting a larger architectural change. — 2026-11-25

## Q-2 · Fallback order for implement and repair

asked: 2026-11-25
answer: "Go first, then Codex, then Claude: the Pi route on OpenCode Go first, then Codex (bead coding-harness-363r.4 is taken up here), Sonnet through Claude last, so the scarce Claude budget is spared."
answered_by: maintainer
status: answered
context: |
  Topic: the order of routes when one is unavailable.
  Intention: no lane stops while any route has capacity; on 2026-11-25 Codex had capacity all day, Claude was exhausted twice.
  Today: implement falls back from GLM-through-Claude-Code to Sonnet only; no Codex implement route.
  Repository change: the route order in scripts/stage2.py and its documentation.
  Architecture change: Codex becomes an implement/repair route.

In the context of choosing the order of implement and repair routes, facing a scarce Claude budget and an available Codex, we decided Go first, then Codex, then Claude, to achieve lanes that keep running while any route has capacity, accepting a new Codex implement route. — 2026-11-25

## Q-3 · Default Go model

asked: 2026-11-25
answer: "DeepSeek V4.1 Flash is the default for implement and repair on Go, as originally wanted (2026-10-20); when its data terms lapse (valid_until in model-endpoints.yaml, today 2026-11-30, renewed monthly) the route falls back to GLM 5.3 Flash automatically."
answered_by: maintainer
status: answered
context: |
  Topic: which Go model the runner uses by default.
  Intention: the maintainer's preferred model, with no gap when its terms lapse.
  Today: DeepSeek's zero-retention agreement is valid through 2026-11-30 (OpenCode Go page, read 2026-11-25); GLM 5.3 Flash has no end date.
  Repository change: the default and its fallback in the route declaration.
  Architecture change: none beyond Q-4.

In the context of the default Go model for implement and repair, facing DeepSeek's monthly data terms and GLM's open-ended ones, we decided DeepSeek V4.1 Flash with an automatic fallback to GLM 5.3 Flash when its terms lapse, to achieve the preferred model without a gap, accepting a fallback that depends on valid_until. — 2026-11-25

## Q-4 · How the decision is recorded

asked: 2026-11-25
answer: "A new ADR 'Work verbs through Pi on OpenCode Go' records route, order Go → Codex → Claude, default model and write boundary; it explicitly supersedes the affected parts of ADR 0007, 0011 and 0015, which each get a pointer."
answered_by: maintainer
status: answered
context: |
  Topic: the decision record.
  Intention: one place that states the work-verb routing.
  Today: model routing is spread over ADR 0007, 0011 and 0015.
  Repository change: docs/adr/<next>-work-verbs-through-pi.md and three pointer lines.
  Architecture change: the routing decision moves into the new ADR.

In the context of recording the work-verb routing, facing three ADRs that each hold a part, we decided one new ADR that supersedes the affected parts with pointers, to achieve one place for the routing decision, accepting three pointer edits. — 2026-11-25

## Q-5 · Write boundary for a write-capable Pi run

asked: 2026-11-25
answer: "It must work on macOS, Linux and Windows. First our own write tools: Pi gets no shell and not its built-in write tools but our own read/edit/write tools, which refuse every path outside the lane worktree (symlinks resolved), in plain Python with tests, plus the existing runner checks. Containers (Docker or Podman) are considered later (bead coding-harness-363r.6). Herdr was checked first and offers no isolation of its own."
answered_by: maintainer
status: answered
context: |
  Topic: how a model that writes through Pi is confined.
  Intention: no write outside the lane worktree, on every platform the kit runs on.
  Today: Pi has no permission system; macOS sandbox-exec was rejected as macOS-only; Herdr is a multiplexer without isolation (web check 2026-11-25).
  Repository change: a small tool module for Pi with path checks, and its tests.
  Architecture change: the write boundary of foreign-model runs is ours, in code.

In the context of confining a write-capable Pi run on macOS, Linux and Windows, facing an OS sandbox that exists only on macOS and a multiplexer without isolation, we decided our own path-checked write tools first and containers later, to achieve the same boundary on every platform, accepting a tool module to build and test. — 2026-11-25

## Q-6 · DeepSeek valid_until fallback vs. 30-day terms-expiry reading rule (H-90, H-92)

asked: 2026-11-26
answer: "When DeepSeek's valid_until expires, automatically switch to GLM 5.3 Flash as long as GLM's 30-day read_date is still valid; if the 30-day read_date window itself has expired, refuse hard."
answered_by: maintainer
status: answered
context: |
  Topic: interaction between Q-3's automatic DeepSeek-to-GLM fallback and the terms-expiry rule (archive/2026-11-06-terms-expiry/spec.md, ADR 0022).
  Intention: resolve the contradiction surfaced by complete research run 4 (43fdfb08b4ae42db3dc9b8f89069d7d0/H-90, H-92) so DeepSeek's monthly expiry does not stall lanes while preserving zero-retention freshness.
  Today: terms-expiry refuses at dispatch on either valid_until or read_date + 30 days without fallback, and Q-3 assumed GLM has no expiry.
  Repository change: plans/changes/pi-work-route/spec.md, ADR 0027, scripts/stage2.py work-verb dispatch check, and tests.
  Architecture change: clarifies the boundary between ADR 0022 (terms expiry) and ADR 0027 (work-verb routing).

In the context of DeepSeek's monthly valid_until interacting with ADR 0022's 30-day read_date expiry, facing either a hard refusal on every expiry or silent fallback past stale readings, we decided to switch automatically from DeepSeek to GLM 5.3 Flash when DeepSeek's valid_until lapses provided GLM's 30-day read_date is still valid and to refuse hard when the 30-day read_date has expired, to achieve uninterrupted work lanes without weakening zero-retention checks, accepting an explicit carve-out in ADR 0027 for valid_until-triggered fallback. — 2026-11-26

## Q-7 · Dropping GLM_KEY and handling a missing OpenCode Go key on work verbs (H-1, H-3)

asked: 2026-11-26
answer: "GLM_KEY is dropped for work verbs; if the OpenCode Go key is missing or OpenCode Go is unavailable, automatically continue along the Q-2 route order (Go -> Codex -> Claude) and refuse only when no route is available."
answered_by: maintainer
status: answered
context: |
  Topic: behavior when GLM_KEY (Z.ai) or the OpenCode Go key is absent once GLM leaves Claude Code/Z.ai for Pi on OpenCode Go (Q-1, Q-2).
  Intention: resolve H-1 and H-3 from research run 4 (43fdfb08b4ae42db3dc9b8f89069d7d0/H-1, H-3), where test_a_missing_glm_key_refuses_the_flash_route currently blocks implement before any fallback runs.
  Today: implement checks GLM_KEY first and refuses without falling back to Codex or Claude.
  Repository change: scripts/stage2.py work-verb route preflight, tests/test_stage2.py (replace the Z.ai GLM_KEY refusal expectation), and ADR 0027.
  Architecture change: removes Z.ai GLM_KEY as a gate for work verbs and treats a missing Go key as an unavailable first route in the Go -> Codex -> Claude chain.

In the context of moving work verbs off Z.ai/Claude Code onto Go -> Codex -> Claude, facing a legacy GLM_KEY refusal test that blocks fallback, we decided to drop GLM_KEY from work verbs and treat a missing or unavailable OpenCode Go route as a fall-through to Codex and then Claude (refusing only when every route is unavailable), to achieve resilient work lanes across providers, accepting replacement of the legacy GLM_KEY refusal test. — 2026-11-26

## Q-8 · Separation between unattended work verbs and interactive stage2-session (H-5, H-91, H-94)

asked: 2026-11-26
answer: "Keep them clearly separated: unattended work verbs (explore, implement, repair) strictly use our shell-free path-checked Python tools (Q-5); interactive stage2-session keeps its JavaScript extension with interactive bash approval unchanged."
answered_by: maintainer
status: answered
context: |
  Topic: relationship between interactive Pi sessions (plans/changes/stage2-session/spec.md, JavaScript extension permitting bash with approval prompts) and unattended work verbs (Q-5, Python path-checked tools with no shell).
  Intention: resolve the neighbour contradiction surfaced by research run 4 (43fdfb08b4ae42db3dc9b8f89069d7d0/H-5, H-91, H-94).
  Today: stage2-session uses a JavaScript Pi extension that allows bash after human confirmation; work verbs do not run through Pi yet.
  Repository change: plans/changes/pi-work-route/spec.md, design.md, and ADR 0027 explicitly scope the shell-free Python tools to unattended work verbs and leave stage2-session untouched.
  Architecture change: establishes a clear boundary between human-attended interactive Pi sessions and unattended shell-free Pi work verbs.

In the context of stage2-session allowing interactive bash via a JavaScript extension while Q-5 bans any shell for Pi work verbs, facing either unifying both under no-shell tools or separating attended from unattended use, we decided to keep stage2-session unchanged and restrict the shell-free path-checked Python tools to unattended work verbs, to achieve strong confinement for autonomous runs without breaking interactive sessions, accepting two distinct Pi tool policies for two distinct trust modes. — 2026-11-26

## Q-9 · Codex reasoning effort for the implement fallback route (H-7)

asked: 2026-11-26
answer: "medium (faster and leaner as a fallback route)."
answered_by: maintainer
status: answered
context: |
  Topic: CODEX_EFFORTS entry for the new Codex implement route introduced by Q-2.
  Intention: resolve H-7 from research run 4 (43fdfb08b4ae42db3dc9b8f89069d7d0/H-7), since every effort value in CODEX_EFFORTS is explicitly chosen by the maintainer.
  Today: CODEX_EFFORTS sets effort values for draft, repair and review, with no entry for implement.
  Repository change: CODEX_EFFORTS in scripts/stage2.py and ADR 0027.
  Architecture change: none beyond ADR 0027.

In the context of adding Codex as the second implement route behind OpenCode Go, facing a choice of medium, high or xhigh reasoning effort, we decided medium for CODEX_EFFORTS['implement'], to achieve a faster and leaner fallback while preserving full post-run verification, accepting lower reasoning depth than review. — 2026-11-26
