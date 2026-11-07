---
title: "Spec — session-launch-length"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-07
supersedes: null
superseded_by: null
bead: coding-harness-rm8
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, session]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — session-launch-length

Interactive sessions receive the complete checked first prompt without putting
that prompt through Terminal's input-line transport (bead `coding-harness-rm8`
— truncated interactive launches). Research: `research.md`. Decisions:
`decisions.md`, Q-1 — the maintainer-approved interview skip for this fix.

## Problem

At baseline `da2e7cd0` (2026-11-07), `terminal_command` puts the assembled
handover, repository rules, launch limits, environment and CLI arguments into
the text sent through AppleScript's `do script`. Research records two truncated
launches on 2026-10-20 despite an accepted dispatch; the CLI did not start.
The runner permits a 32 KiB prompt and a 64 KiB command, which do not protect
this terminal-input hop (`research.md`, “What exists today”).

The interview record identifies the terminal input-line limit as the cause.
Research does not contain a measured numeric threshold or the failed commands'
byte sizes. This spec therefore fixes exposure to that limit without claiming
an independently measured threshold. Acceptance remains dispatch acceptance,
as the existing session contract requires.

## Acceptance criteria

1. When either supported session transport dispatches, Terminal receives one
   command of at most 1,024 UTF-8 bytes, without embedded line breaks, prompt
   text or environment assignments, independent of the prompt's length.
   *Refuted by:* a near-limit prompt enlarging the dispatched command, a
   multiline command, or dispatch of a command exceeding that byte budget.
2. When an otherwise valid assembled first prompt is at most 32 KiB, executing
   the dispatched command delivers that exact prompt as one CLI argument for
   both Codex and Pi.
   *Refuted by:* a boundary-size or multibyte prompt losing its tail, being
   split into arguments, changing text, or being refused solely for its length.
3. If the assembled prompt contains NUL, exceeds 32 KiB, or its short launch
   command cannot fit criterion 1's budget, the runner refuses before Terminal
   dispatch with exit 2 and a reason naming the invalid input or exceeded bound.
   *Refuted by:* dispatch after such input, a byte/character-count mismatch,
   silent truncation, or an unexplained refusal.
4. When prompt text, paths or allowed environment values contain shell syntax,
   their contents remain data throughout launch-file execution.
   *Refuted by:* quotes, substitutions, Unicode or newlines changing the
   recorded prompt/environment or executing an extra command in a stand-in.
5. When launch files are prepared, the prompt-bearing file is confined to a
   fresh owner-only attempt directory under `.stage2-sessions/`, retained on
   accepted dispatch and removed on refusal or failed dispatch without removing
   existing user files.
   *Refuted by:* group/other access to the directory or prompt-bearing file,
   a failed write followed by dispatch, a failed attempt leaving its files, or
   cleanup deleting a pre-existing sibling file.
6. When the new launch route runs, it preserves the session's existing checks
   and CLI contract: both leak checks, endpoint/model binding, sanitized CLI
   environment, worktree, interactive arguments and policy/approval flags.
   *Refuted by:* a leaking second scan reaching Terminal, a wrong model or
   directory, a caller token reaching a launch file/CLI, missing Pi policy
   binding, or changed safety/discovery flags in recorded CLI calls.
7. When Terminal accepts or rejects the short command, the runner retains the
   existing pending/accepted/failed audit and exit semantics, with accepted
   meaning only that Terminal took the command.
   *Refuted by:* a rejected dispatch returning success, a lost audit, or an
   accepted dispatch being reported as proof that the CLI authenticated or ran.
8. When the new transport is documented, the workflow and module description
   accurately describe the short command, local prompt-bearing file, byte
   bounds, retained-file lifecycle and dispatch-only acceptance.
   *Refuted by:* either description claiming that launch files contain no
   prompt, or promising successful CLI startup from dispatch acceptance.

## Non-goals

- Detecting CLI startup, login or a model response; no readiness handshake or
  new audit state. A stand-in execution proves transport, not real model startup.
- Fixing unrelated unexecuted-shell-input failures or adding a VS Code terminal
  transport (the separate launch work described in `research.md`).
- Raising the prompt limit, changing prompt assembly, model selection, sign-in,
  policy enforcement, review routing or continuous leak scanning.
- Unattended real-terminal/model qualification or automatic deletion after an
  accepted session ends. Any attended live qualification is separate work.
- A design phase or ADR: this is a bounded transport repair, so phase 2b does
  not run and no architecture decision record is created.

## Protected areas

- `model-endpoints.yaml`, `decisions/`, `docs/adr/`, `provenance.yaml` and
  `AGENTS.md`: no endpoint approval, governance or architectural decision changes.
- `scripts/stage2.py`, `scripts/stage2_session_policy.mjs`, `tools/pi/`,
  `prompts/`, `templates/` and harness configuration: reuse existing boundaries.
- Neighbouring change artifacts, including `plans/changes/stage2-session/`:
  their 64 KiB command ceiling still holds under the tighter dispatch bound;
  their dispatch-only acceptance contract is preserved.

## Definition of Done

- The criterion ledger's tests pass and `make verify` is green at the final head.
- Documentation moved with the code: `docs/WORKFLOW.md` and the module
  description in `scripts/stage2_session.py`; no models or ADRs change.
- The pull request's file list demonstrates the protected areas and non-goals.
- The implementation pull request closes `coding-harness-rm8` — truncated
  interactive launches — and its last commit carries
  `Closes-Bead: coding-harness-rm8`.
- Special runs: none; no live Terminal or model launch is required here.

## Open decisions

None open. The agent chose the following reversible details and recorded why:

- [DETAIL] Use a local shell launcher with the prompt quoted as argument data:
  it removes the large payload from Terminal input while preserving interactive
  stdin and existing CLI arguments, without changing either CLI's prompt format.
- [DETAIL] Set the dispatched-command budget to 1,024 UTF-8 bytes, a conservative
  engineering bound rather than a claim about a measured Terminal threshold;
  refuse unusually long paths instead of sending a larger line.
- [DETAIL] Retain the prompt-bearing launcher with accepted attempt files so
  asynchronous Terminal execution cannot race cleanup; owner-only permissions
  bound the new local persistence. This follows the existing attempt lifecycle.
- [DETAIL] Set phase 4's appetite to two hours including repair; stop and report
  remaining work at that limit. Neither research nor the answer sets an appetite.
