---
title: "Spec — stage2-session"
status: draft
implementation_status: partial
date: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-09
supersedes: null
superseded_by: null
bead: coding-harness-amp
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-10-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, stage-2, session]
class: architectural
appetite: 4
---

# Spec — stage2-session

Start a declared interactive Pi (for OpenCode Go models) or Codex session from
one checked runner invocation, in the change's worktree, with an auditable
handover. Research and settled instructions: `research.md`, `decisions.md`
(coding-harness-amp). Since 2026-10-09 the OpenCode Go path launches Pi, not
the OpenCode CLI (maintainer, German: "ich will keine opencode mehr
benutzen"; answers Q-1 to Q-6 in `decisions.md`). The OpenCode Go service and
its endpoint declaration are unchanged.

## Problem

The runner has no interactive launch verb on main at `1c79860`. Direct TUI
launches skip its declaration, prompt scan and audit. Budget takeover must
not open a second unchecked entry point. The incoming Flash runner (`11abf42`,
PR #89) changes the same file and must land first. Pi asks for no approval and has no sandbox
(`docs/security.md` of the pinned Pi 1.1.0), so the repository must supply
the session policy itself, as an extension loaded explicitly by the runner
(`research.md`, addendum of 2026-10-09).

## Terms

- **Dispatch:** Terminal accepted the launch command; not evidence that the
  CLI started, model authenticated, answered, finished the workflow or passed
  verification. Executables must exist at preflight; later startup failures
  appear in the new window.
- **Launch snapshot:** the state scanned before dispatch, not later edits,
  later prompts or later UI model switches.

## Supported models and prerequisites

The currently usable positive path is `--model gpt-6.1-sol`, through the
declared `openai-codex` endpoint and official Codex CLI. The Pi path accepts
`opencode-go/<model>` only when the `opencode-go` endpoint lists that model
for framework content in `model-endpoints.yaml` (declared by ADR 0011; the
id names the endpoint, not the launcher, Q-5). The runner does not invent a
review ordering and starts only the Pi pinned by `require_pi` (1.1.0); any
other Pi is refused before dispatch. Fixture-only positive tests supply an
explicitly declared endpoint, not a production allow-list.

The dedicated worktree of change `<change>` is the canonical path
`<main checkout>/.claude/worktrees/<change>`, where the main checkout is the
parent of git's shared `.git` directory. A change folder copied into another
worktree does not confer ownership; only this path with an attached branch
qualifies. The invocation's working directory and runner root must both be
that canonical worktree root, not a subdirectory, another worktree or main.

## Acceptance criteria

1. When `python3 scripts/stage2.py session <change> --model <id>` runs in the
   change's dedicated worktree, it accepts the declared supported model.
   *Refuted by:* no session parser, or dispatch from the main checkout,
   detached HEAD or a different root than the validated change.
2. If the endpoint/model declaration is absent, ambiguous, unreadable or
   disallows framework content, the command refuses before terminal dispatch.
   *Refuted by:* an unknown model, unapproved transport, missing residency
   or malformed declaration reaching the terminal stand-in.
3. When the handover is supplied, its actual text becomes the first prompt;
   otherwise the change-local `handover.md` is used.
   *Refuted by:* an empty/missing/unreadable/nonregular file being accepted,
   only a pathname being sent, or an unrelated handover silently selected.
   Prompts over 32 KiB UTF-8 or containing NUL refuse before dispatch; the
   complete dispatch command is bounded to 64 KiB to fit the launch transport.
4. If a handover path resolves outside the validated worktree, it is refused.
   *Refuted by:* traversal or a symlink sending outside-file text to a model.
5. When dispatch is attempted, the runner checks the change, visible tree,
   index, history and the exact outgoing prompt with the existing leak check
   in the same invocation before any terminal or model starts.
   *Refuted by:* a planted forbidden value in the handover or index reaching
   the stand-in, or a stale preflight result being reused.
6. If the leak check cannot measure or finds a match, nothing is dispatched.
   *Refuted by:* missing denylist or failed scan producing a terminal call
   or an audit claiming a clean check.
7. When dispatch succeeds, a findings audit names date, requested model,
   endpoint, handover source and the measured file/commit/rule counts.
   *Refuted by:* missing or invented counts, wrong model, lost prior findings
   or an audit indistinguishable from a completed review verdict.
8. If dispatch fails after clean preflight, the command returns failure and
   records a failed dispatch rather than claiming an interactive model ran.
   *Refuted by:* denied automation or terminal dispatch failure
   returning success or leaving a success-only audit.
   A missing CLI/terminal executable is a prerequisite refusal (exit 2).
   Successful Terminal acceptance is exit 0, not a CLI-start acknowledgment;
   a subsequent CLI/login/model failure is reported in the new window.
9. When a supported model is launched, the terminal runs the official CLI
   interactively with that model and the checked worktree as its directory.
   *Refuted by:* a non-interactive Pi mode (`--print`, `--mode`),
   `codex exec`, any `opencode` call, wrong cwd, automatic fallback, or a
   runner waiting for the interactive session to terminate.
10. When a terminal command includes paths or handover text, those values
    remain data rather than executable shell or AppleScript instructions.
    *Refuted by:* quotes, shell substitutions or newlines in a temporary
    path/prompt executing an extra command in a launch stand-in test.
11. When Pi is dispatched, it runs with discovery off (`--no-extensions`,
    no project-local files) and one runner-supplied policy extension loaded
    explicitly, with `--offline` and `--no-approve`. The extension (a) blocks
    `read`, `grep`, `find`, `ls`, `edit` and `write` on a path outside the
    worktree, (b) blocks writes to its own file, to `.stage2-sessions/` and
    to `.pi/` (Q-3; `.git/` is not blocked), (c) asks before a `bash` call
    that matches a dangerous pattern and blocks that call when no UI exists
    (Q-2), and (d) blocks the call when its own handler fails. The runner
    confirms that the extension *loaded* (Q-1); the handlers' behaviour is
    held by tests that run without Pi and without a model.
    *Refuted by:* a path outside the worktree, or a write to a protected
    path, passing the handler; a listed dangerous pattern running without a
    question or without a UI; a failing handler letting the call through; a
    launch whose extension did not load; a second extension, a discovered
    project extension or a Pi off the pin reaching the terminal.
12. When Codex is dispatched, it uses workspace-write and on-request approval
    without bypass flags or additional writable directories.
    *Refuted by:* danger-full-access, bypass, auto-approval or extra-dir flags
    in recorded arguments. This does not promise worktree-only read isolation.
13. When the runner prepares launch files/configuration/environment, it does
    not read the maintainer's credential file, copy credentials into the
    worktree or overwrite existing user configuration. The Pi session signs
    in with the maintainer's own Pi agent directory (`~/.pi/agent`, Q-6),
    which the maintainer fills with `/login`; the runner neither reads nor
    writes it and sets no `PI_CODING_AGENT_DIR`.
    *Refuted by:* a credential-file read in a stand-in test, caller API tokens
    copied into launch files, `OPENCODE_API_KEY` or another key handed over
    by the runner, or conflicting project config destroyed.
14. If prerequisite launch preparation fails, no model starts and any
    runner-owned partial files are cleaned without deleting user files.
    *Refuted by:* a config or audit write failure followed by terminal dispatch,
    or cleanup that removes an existing project configuration.
15. When documenting the command, the help and workflow explicitly say that
    the leak check covers launch only and that tool permissions do not prove
    OS confinement, including arbitrary approved shell code and later UI
    model switches; re-entry for another model uses the runner again. For
    Pi it also says that the maintainer's `~/.pi/agent` may hold other
    providers' credentials, so a model switched inside the session can leave
    the declared endpoint unscanned (Q-6), and that a `bash` command outside
    the dangerous patterns runs without a question (Q-2), which includes a
    network program and `git push` (Q-7, Q-8).
    *Refuted by:* docs claiming continuous scanning, guaranteed whole-disk
    isolation or permission to switch to an undeclared model in the TUI.
16. When the change is proposed for merge, it includes the ADR 0007 amendment
    draft and workflow documentation in a decision PR, without editing the
    protected ADR directory or changing the reviewer-round routing. The one
    decision PR carries the Pi move (Q-4).
    *Refuted by:* an ordinary PR, edited `docs/adr/`, or a second OpenCode Go
    ordering added here instead of the reviewer change.

## Non-goals

Continuous leak checking, automatic session completion, credential setup,
Claude display/hooks parity, installing CLIs, non-macOS terminal backends,
reviewer migration and new endpoint approvals. The wider workflow-parity bead
must stay open when only this scoped verb is implemented. A supported model
still needs valid CLI authentication; the runner does not provision it.

## Protected areas

- `feat/stage2-flash-runner` and PR #89: another completed change.
- `docs/adr/` and `provenance.yaml`: human-decided; amendment draft only here.
- Maintainer credential and global harness configuration files: neither read
  nor edited. Customer repository content remains out of bounds.

## Definition of Done

- Dedicated tests use fake terminal/CLI launchers, never real model endpoints.
- Full `make verify` green; a real GUI/model smoke test is either measured
  through this runner or explicitly named as unrun, never implied by tests.
- Phase 2a, architectural design, plan, implementation, verification and
  review follow the workflow. No implementation before PR #89 is on main.
- Draft ADR amendment and workflow/help move with the code, with the touch
  map in the decision PR. No merge by this session.
- Record the session-verb milestone on the bead but do not close the wider
  parity task without evidence of that remaining scope.

## Open decisions

None open. The maintainer's "mach weiter" accepted the immediately preceding
recommendation: Terminal acceptance after prerequisite checks, not a program-
start acknowledgment (F-2; `decisions.md`). The six Pi questions are answered
(Q-1 to Q-6, 2026-10-09). Policy becomes binding only by the decision PR merge.
