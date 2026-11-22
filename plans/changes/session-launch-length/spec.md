---
title: "Spec — session-launch-length"
status: draft
implementation_status: none
date: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-22
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
   command of at most 1,023 UTF-8 bytes, without embedded line breaks, prompt
   text or environment assignments, independent of the prompt's length.
   The 1,024-byte typed-line budget includes Terminal's terminating newline.
   *Refuted by:* a near-limit prompt enlarging the dispatched command, a
   multiline command, or dispatch of a command exceeding 1,023 bytes.
2. When an otherwise valid assembled first prompt is at most 32 KiB and the
   launch-file content is at most 64 KiB, executing the dispatched command
   delivers that exact prompt as one CLI argument for both Codex and Pi.
   *Refuted by:* an eligible boundary-size or multibyte prompt losing its tail,
   being split into arguments, changing text, or being refused solely for its length.
3. If the assembled prompt contains NUL or exceeds 32 KiB, the launch-file
   content exceeds 64 KiB, the short command exceeds 1,023 UTF-8 bytes, or the
   launch-file path contains a control byte below 0x20 or 0x7F, the runner
   refuses before Terminal dispatch with exit 2 and a reason identifying the
   invalid input or exceeded bound.
   *Refuted by:* dispatch after any such input, refusal at an inclusive byte
   limit, a byte/character-count mismatch, silent truncation, or an unexplained
   refusal.
4. When prompt text, eligible paths or allowed environment values contain shell
   syntax, their contents remain data throughout launch-file execution.
   *Refuted by:* quotes, substitutions, Unicode or newlines changing the
   recorded prompt/environment or executing an extra command in a stand-in.
5. When launch files are prepared, the prompt-bearing file has mode 0700 in a
   fresh owner-only attempt directory under `.stage2-sessions/`, retained on
   accepted dispatch and removed on refusal or failed dispatch without removing
   existing user files.
   *Refuted by:* a launcher mode other than 0700, group/other access to the directory,
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
   describe the short command form, prompt-bearing local launch file, 32 KiB
   prompt limit, 64 KiB launch-file-content limit, 1,023-byte dispatched-command
   limit, file removal on refusal or failed dispatch, retention on acceptance,
   and dispatch-only acceptance.
   *Refuted by:* either description omitting or misstating any of those facts,
   claiming launch files contain no prompt, or promising CLI startup from
   dispatch acceptance.
9. When the dispatched command runs, it verifies the launch file's SHA-256
   digest recorded at preparation and refuses to execute a file whose digest
   differs or cannot be verified.
   *Refuted by:* a modified or unreadable launcher starting the CLI, or an
   unchanged launcher being rejected because of a mismatched recorded digest.

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
  the 64 KiB ceiling holds for the launch-file content and the tighter dispatch
  bound; their dispatch-only acceptance contract is preserved.

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
- [DETAIL] Include Terminal's terminating newline in the 1,024-byte typed-line
  budget, leaving at most 1,023 UTF-8 bytes for the dispatched command. Refuse
  launch-file paths containing control bytes below 0x20 or 0x7F because the
  terminal line editor can interpret them instead of passing them as data.
- [DETAIL] Retain the 64 KiB limit for the quoted launch-file content, where
  the full command now lives; quote expansion may make a smaller prompt exceed it.
- [DETAIL] Retain the prompt-bearing launcher with accepted attempt files so
  asynchronous Terminal execution cannot race cleanup; owner-only permissions
  bound the new local persistence. This follows the existing attempt lifecycle.
- [DETAIL] Set the launcher to mode 0700 and verify its recorded SHA-256 digest
  before execution, so changes made after preparation are detected at the check;
  owner-only permissions alone do not exclude another process of the same user.
  Boundary: this check does not prevent a same-user process changing the file
  between digest verification and execution.
- [DETAIL] Set phase 4's appetite to two hours including repair; stop and report
  remaining work at that limit. Neither research nor the answer sets an appetite.
