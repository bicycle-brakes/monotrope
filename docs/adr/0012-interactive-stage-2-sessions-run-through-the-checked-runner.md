---
title: "ADR 0012 — Interactive Stage 2 sessions start only through the checked runner, and OpenCode Go ones run on Pi"
category: adr
status: accepted
created: 2026-10-10
last_reviewed: 2026-10-10
updated: 2026-10-10
owner: framework-architect
provenance: human-decided
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-10"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [adr, stage-2, session, pi, opencode-go]
---

# ADR 0012 — Interactive Stage 2 sessions start only through the checked runner, and OpenCode Go ones run on Pi

* Status: accepted by the merge of the pull request that carries this file.
  Until that merge, the pull request's state is the decision's state: open is
  proposed, closed is rejected. Amends ADR 0007 decision 1 (the leak check
  "immediately before the call": for a session it runs at launch only) and
  decision 4 (the accepted residual read risk now covers a session that
  writes and runs a shell, not a read-only reviewer), and ADR 0011 decision 1
  (scope: the review loop only) and decision 5 (the OpenCode Go key reaches a
  call only as `OPENCODE_API_KEY`: a session signs in from `~/.pi/agent`
  instead, for the session verb only); supersedes no ADR.
* Review: the maintainer's answers of 2026-10-09 in a Claude Code session,
  recorded as Q-1 to Q-8 in `plans/changes/stage2-session/decisions.md`
  (confirm-load read-back; the shell asks only on dangerous patterns; file
  tools bounded to the worktree with a protected list; one decision pull
  request; `opencode-go` ids select Pi; sign-in through the maintainer's own
  `~/.pi/agent`; network programs do not ask; only `git reset --hard` and
  `git clean` ask among the git commands) and Q-9 (the discovery flags
  `--no-mcp`, `--no-skills`, `--no-prompt-templates` and `--no-themes` with
  context files on; `git checkout -- .` and `git restore .` ask too), both
  chosen as recommended options in a multiple-choice question. The code asks
  on more forms of the same two commands (`git checkout -f`, `git checkout
  <ref> -- <path>`, `git restore <path>`); those were not asked one by one and
  this merge confirms them. The acceptance is the merge commit and is written nowhere else
  (ADR 0008) · Decider: maintainer · prepared by
  a Claude Code session; the first draft was written by Codex on 2026-10-07 for
  the OpenCode CLI and re-pointed to Pi on 2026-10-09
  (`plans/changes/stage2-session/adr-0007-session-amendment.md`).
* Date: 2026-10-10 · takes effect on merge

## Context

* Budget takeover needs interactive work in a window of its own without
  skipping the declaration, the leak check and the audit that every finite
  phase call has. ADR 0007 and ADR 0011 cover finite calls; an interactive
  session was outside both.
* The maintainer wants no OpenCode CLI (2026-10-09). The review loop already
  runs on Pi (ADR 0011); the session verb was the last caller of the OpenCode
  CLI, and it was unusable under OpenCode 2.x (bead coding-harness-0al).
* Pi 1.1.0 asks for no approval and has no sandbox (its `docs/security.md`),
  so a session needs a policy the runner supplies itself.

## Decision

1. **Interactive foreign sessions start only through `python3 scripts/stage2.py
   session <change> --model <id>`** in the canonical worktree. A declared
   framework endpoint and a clean leak check over the exact initial prompt are
   prerequisites, and the audit records date, model, endpoint, handover source
   and scan counts. Terminal acceptance is success of the dispatch, not proof
   that the program started, signed in or answered.
2. **An `opencode-go/<model>` id selects Pi.** The id names the endpoint, not
   the launcher; the OpenCode CLI is never called. Pi starts at the pinned
   version only, with extensions, MCP servers, skills, prompt templates and
   themes off, and one runner-supplied policy extension
   (`scripts/stage2_session_policy.mjs`) loaded from a private copy.
3. **The extension** keeps `read`, `grep`, `find`, `ls`, `edit` and `write`
   inside the worktree as Pi resolves a path, keeps `edit` and `write` off its
   own file, `.stage2-sessions/` and `.pi/`, asks before a recursive `rm`,
   `sudo`, `chmod` or `chown` with 777, `git reset --hard`, `git clean`,
   `git checkout` forms that discard (`--`, `.`, `-f`) and `git restore` (except
   `--staged` alone), blocks those when no UI can ask, and blocks the call when its own handler fails. Every other `bash`
   command runs unasked, network programs and `git push` included. `.git/`
   stays writable.
4. **The runner confirms the extension loaded** (its flag is listed by a
   separate `pi --help` run under a scratch home, not by the session process
   itself) and refuses otherwise. Whether its handlers hold inside a live
   Pi is held by tests that run the extension without Pi, not read back.
5. **The session signs in with the maintainer's own `~/.pi/agent`**; the runner
   reads nothing from it and hands Pi no key.
6. **Codex sessions** keep workspace-write with on-request approval and do not
   claim worktree-only reads. This record claims no confinement beyond what
   each harness provides itself; the runner does not verify Codex's sandbox,
   and for Pi the extension confines the file tools only, not the shell.

## Options considered

* Pi with a runner-supplied policy extension (**chosen**).
* The OpenCode CLI with its effective-policy read-back (rejected by the
  maintainer, 2026-10-09: no more OpenCode CLI).
* A Pi print or RPC mode with a dedicated agent directory (rejected: the
  session is interactive, and the maintainer chose his own sign-in, Q-6).
* A direct terminal launch relying on a manually run earlier scan (rejected:
  it skips the checked handover).

## Consequences

* The scan covers the launch only. Later prompts, edits, an approved or
  unlisted shell command and a model switched inside the session are not
  scanned; another model re-enters through the runner.
* **Unlisted shell commands run without a question**, including network
  programs (`curl`, `ssh`, `scp` and the like) and `git push`; the leak check
  does not see what such a command sends. `cat ~/.pi/agent/…` is an unlisted
  command too.
* `~/.pi/agent` may hold other providers' credentials, so a model switched
  inside the session can leave the declared endpoint unscanned. This changes
  where a session's key comes from (ADR 0011 decision 5, for the verb only).
* **Context files and the agent directory feed the session unscanned.**
  `AGENTS.md` files stay on, and the maintainer's `~/.pi/agent` still loads
  (system-prompt files, settings, `models.json`, whose key and header values
  can run commands at request time); the leak check scans the prompt and the
  tree only. Whether `models.json` can redirect the `opencode-go` address was
  not measured.
* The session starts with `env -i` and an allow-list: no `OPENCODE_API_KEY`,
  no `SSH_AUTH_SOCK` (so `git push` over SSH fails inside the session; an
  HTTPS push with a credential helper does not). A shell can also start another
  shell (`sh -c`, `eval`), which no pattern sees.
* The patterns match the command text: a quoted flag or command word
  (`rm "-rf" x`, `g""it reset --hard`) is not seen. The list is short on
  purpose and is not a parser.
* The proof of the policy is weaker than the OpenCode read-back was: a bug in
  the extension that its tests miss is not seen at launch.
* This decision approves no new endpoint and no new review order; the
  `opencode-go` declaration stays ADR 0011's, and the entry's note now also
  names the session verb. It does accept a new credential source for that verb
  (see above).
* Initial support is macOS Terminal only, with no silent fallback.
* Bead coding-harness-0al is superseded: no `opencode` call remains.

## Validation

* Merged and green on `main` before this record: the policy extension with 200
  test cases and 26 planted faults (#111), the runner port with its launch,
  version pin, read-back and cleanup tests (#112), the documents (#113).
* Not validated: any live Pi. That the extension loads and its handlers hold in
  the interactive window, what `--offline` and `--no-approve` do, and that a
  multi-line first message opens the session are the smoke test on the
  maintainer's Mac (package 7); stand-ins do not prove them.
