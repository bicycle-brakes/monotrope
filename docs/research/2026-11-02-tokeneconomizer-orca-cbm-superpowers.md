---
title: "Evaluation — TokenEconomizer, Orca, Codebase Memory MCP and Superpowers, against the harness"
category: research
created: 2026-11-02
updated: 2026-11-02
last_reviewed: 2026-11-02
status: draft
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-02"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-52pd
tags: [spike, evaluation, outside-practice, tools]
---

# TokenEconomizer, Orca, Codebase Memory MCP and Superpowers

Two evaluation spikes answered together: bead coding-harness-52pd (evaluate
microsoft/TokenEconomizer, maintainer 2026-10-21) and bead coding-harness-c97e
(weigh a community report on cheap-worker orchestration — Orca, Codebase
Memory MCP, Superpowers — maintainer 2026-10-26). A reading by the
orchestrating session on 2026-11-02 through the GitHub API and the projects'
pages, not the research swarm (blocked that day by a full disk and the Pi
path leak, bead coding-harness-xul8). Nothing was installed or run.

## TokenEconomizer (bead coding-harness-52pd)

**What it is** (README and repository metadata, read 2026-11-02):
microsoft/TokenEconomizer, Apache-2.0, created 2026-10-13, 4,365 stars on
2026-11-02 (18 when the bead was filed on 2026-10-21), with a paper
(arXiv 2610.22732). A plugin for Claude Code, Codex, Copilot CLI and Pi that
learns from a repository's finished sessions:

- **Micro-skills:** repository facts (the command spelling that works here,
  a build step that must run first) learned from repeated failures and from a
  model that reviews recent sessions; a fact is stated at session start once
  three sessions have confirmed it, and dropped when later sessions
  contradict it.
- **Tool pruning:** a tool unused over a threshold is left out of later
  sessions through the agent's own settings.
- **Loop guard:** a judge model checks a turn that keeps hitting the same
  failure and, above a confidence threshold, adds one redirect note; it never
  stops a turn itself.
- **Measured:** 18.4–30.9 % lower mean cost on 277 SWE-Bench tasks across
  five agent–model combinations, Pass@1 up in four of five (the paper's own
  measurement).

**Against the harness:**

- The session-start facts are a second instruction source beside `AGENTS.md`,
  which is the only instruction file here (`tests/test_entry_points.py`), and
  they live in `~/.tokeneconomizer`, outside the repository — against "a
  standing rule belongs in the repository's `AGENTS.md`".
- Tool pruning edits the agent's settings by itself; `.claude/settings.json`
  here is curated (denied tools by name, ask rules for merges) and documented
  in `tools/claude-code/`.
- It reads the finished session logs of every repository the machine works
  in, including private ones; the content stays local, but what it learns
  from one repository must not surface in another (house rule 6).
- Its measurements are short single-task sessions; this harness's cost
  driver is long orchestrating sessions (bead coding-harness-jeg). The saving
  here is unmeasured.
- **What fits:** the confirmation rule — a fact counts after three
  confirming sessions and is dropped on contradiction — is a sound rule for
  the consolidation run (bead coding-harness-g4iq) and for the memory pointer
  pass (bead coding-harness-uzjq). The facts it would learn are the kind this
  repository's sessions keep rediscovering (2026-11-01/02: `make index` needs
  the venv's Python; waiters need `/usr/bin/grep`).

**Verdict:** do not install now. Take the confirmation rule into
coding-harness-g4iq. Revisit only with a measured trial on one long session
type, in a throwaway account, pinned to a reviewed commit.

## The cheap-worker report (bead coding-harness-c97e)

The report (a community post shared on 2026-10-26, text only) described one
orchestrator delegating implementation to many DeepSeek V4.1 Flash workers on
OpenCode Go through Orca. Its five questions, answered:

1. **Codebase Memory MCP as an index for workers**
   (DeusData/codebase-memory-mcp, MIT, C, created 2026-02-24, 47,992 stars on
   2026-11-02). A local code graph exposed through 17 MCP tools; "source
   analysis and graph storage run on your machine". Its `install` also writes
   client configuration, "durable guidance, skills" and context hooks — a
   second instruction layer again, unless installed with `--skip-config`.
   Worth noting for one narrow use: its experimental "change-aware test
   selection" is the question bead coding-harness-gxwg answers by hand
   (touched and linked tests per repair). **Verdict:** no adoption; a possible
   probe for gxwg's test selection, binary only.
2. **A pre-launch check of the declared model, and no silent substitution.**
   The harness already probes every candidate before a fresh review run
   (`prepare-loop`) and records every route change (ADR 0017, ADR 0021; bead
   coding-harness-6ie makes a failed call's fall-through visible). Orca's page
   says nothing about model verification. **Verdict:** nothing to adopt.
3. **Superpowers as a planning and verification skill pack**
   (obra/superpowers, MIT, created 2025-10-09, 310,990 stars on 2026-11-02).
   Fifteen skills that trigger automatically — brainstorming, writing and
   executing plans, test-driven development, worktrees, verification before
   completion, code review. Prompt text, like Matt Pocock's skills
   (`2026-11-02-mattpocock-skills-and-sandcastle.md`, PR #311): its
   "verification-before-completion" asks the model for "evidence before
   claims" and a "red-green cycle verified" for a regression test — the
   harness's runner performs both checks itself. **Verdict:** do not install;
   auto-triggered skills would compete with the phase prompts.
4. **Orca as the dispatcher** (onorca.dev, MIT, a desktop app). Runs agent
   CLIs side by side, "each in its own worktree", fans one prompt across
   several agents and lets the user merge the winner; 27 agents supported. It
   hosts agents; it does not gate them — no leak check, no admission, no
   post-run checks. **Verdict:** not a replacement for the runner; at most a
   human view over worktrees, a candidate for the editor-interface
   qualification (bead coding-harness-25h.1).
5. **DeepSeek's zero-retention timing.** Settled: data terms now carry an
   expiry date and an expired reading stops calls (ADR 0022; bead
   coding-harness-abra, closed).

## Summary

| Source | Verdict | Taken into |
| --- | --- | --- |
| TokenEconomizer | not now | the confirmation rule → coding-harness-g4iq |
| Codebase Memory MCP | no adoption | a possible test-selection probe → coding-harness-gxwg |
| Model verification | already covered | — |
| Superpowers | do not install | — |
| Orca | not a runner | a human view → coding-harness-25h.1 |
