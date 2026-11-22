---
title: "Findings — session-launch-length"
category: findings
status: draft
implementation_status: none
date: 2026-11-07
created: 2026-11-07
last_reviewed: 2026-11-07
updated: 2026-11-22
supersedes: null
superseded_by: null
bead: coding-harness-rm8
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-07"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — session-launch-length

Stage-2 call, 2026-11-07: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 923 files, 3590 commits, 12 rules.

Stage-2 call, 2026-11-21: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1170 files, 5291 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1170 files, 5300 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-1 | MAJOR | SPEC | base | spec.md criterion 1 and criterion 3; Open decisions, second [DETAIL]; decisions.md Q-1 | [AMBIGUITY] "At most 1,024 UTF-8 bytes" can be read two ways. (a) The limit applies to the string handed to osascript. A command of exactly 1,024 bytes is then dispatched, and Terminal puts 1,025 bytes on the input line once it adds the Return that `do script` appends. (b) The limit applies to everything that reaches the input line, the line terminator included, so the longest accepted command is 1,023 bytes. decisions.md Q-1 names MAX_CANON as the cause, and on macOS MAX_CANON (and MAX_INPUT) is 1,024 bytes. Under (a), a command at the limit is exactly the failure this change is meant to remove: the terminator no longer fits, the command sits unexecuted, and criterion 3 refuses nothing. The [DETAIL] calls the limit "conservative", which reading (a) contradicts. The boundary tests for criteria 1 and 3 pin opposite sides of 1,024 depending on the reading. | Opus | in spec — [DETAIL] decided by the orchestrator: the limit is on the line Terminal types, including the newline it adds: the command string handed to osascript is at most 1,023 bytes; a test pins 1,023 dispatched and 1,024 refused. Reason: the tty limit applies to the typed line | — |
| F-2 | MAJOR | SPEC | base | spec.md Protected areas, third bullet ("their 64 KiB command ceiling still holds"); criteria 2, 3, 8; `scripts/stage2_session.py:62` | [AMBIGUITY] The spec does not say what happens to `COMMAND_LIMIT`. (a) The check is retired. The 1,024-byte dispatch limit trivially satisfies the neighbour's 64 KiB ceiling, and the full CLI line in the launch file has no limit beyond the 32 KiB prompt. (b) The check stays and now measures the quoted CLI line written into the launch file. Under (b), a valid prompt of at most 32 KiB that contains many single quotes is refused: `shlex.quote` turns each `'` into five bytes, so roughly 8,000 quotes push the line past 64 KiB. Criterion 2 lists that outcome as a refutation ("refused solely for its length"), and criterion 3 names no such refusal ground. The reading also decides which byte limits criterion 8 documents, and whether `docs/WORKFLOW.md:1625` ("the whole command at 64 KiB") stays. | Opus | in spec — [DETAIL] decided by the orchestrator: COMMAND_LIMIT stays and now applies to the launch file's content, where the long command lives; the 1,023-byte limit applies to the typed short command. Reason: both limits keep a meaning | — |
| F-3 | MINOR | SPEC | base | spec.md criteria 1, 3, 4 | Not decided: what happens when a path contains a line break. The new window starts in the user's home directory, so the short command has to name the launch file by its absolute path, and that path contains the worktree root. Criterion 4 requires paths with shell syntax, newlines included, to stay data. Criterion 1 forbids embedded line breaks in the dispatched command. Criterion 3 refuses only for NUL, an oversized prompt or the byte limit. For a main-checkout or worktree path containing a line break or another control character, the spec chooses neither of the two options. One is to refuse, but no criterion and no reason text cover that. The other is to encode the path without a literal newline, which depends on the shell that reads the dispatched line, and that shell is unspecified. Terminal runs the user's login shell; the stand-in runs `/bin/sh`. The implementer would have to invent this behaviour. | Opus | in spec — [DETAIL] decided by the orchestrator: a launch-file path containing a line break, carriage return or NUL is refused before dispatch with the reason. Reason: such a path cannot be typed as one line | — |
| F-4 | MINOR | SPEC | base | spec.md criterion 8 | Criterion 8 requires the docs to "accurately describe" the short command, the prompt-bearing file, the byte limits, the retained-file lifecycle and dispatch-only acceptance. Its refutation catches only two false claims: that launch files hold no prompt, and that CLI startup is promised. A documentation change that never mentions the 1,024-byte limit or the retained prompt files still passes. So does one that leaves `docs/WORKFLOW.md:1625` ("the whole command at 64 KiB") untouched. The "accurately describe" half has no case that would make it fail. | Opus | in spec — [DETAIL] decided by the orchestrator: criterion 8 gains a positive refutation — the docs must name the short command form, that the launch file carries the prompt, the two byte limits, when the file is removed, and that acceptance means dispatch only. Reason: both halves refutable | — |

Stage-2 call, 2026-11-22: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1170 files, 5302 commits, 12 rules.

Stage-2 call, 2026-11-22: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1170 files, 5307 commits, 12 rules.

## Phase 2a — Opus 5.5, 2026-11-22

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| F-5 | MAJOR | SPEC | base | spec.md criterion 5 and criterion 6; Open decisions, fourth [DETAIL]; `scripts/stage2_session.py:442`, `scripts/stage2_session_policy.mjs:41` | Not decided: whether the launcher must reach Terminal's shell unchanged between the runner writing it and that shell running it. The shell runs it asynchronously, after osascript has returned. Criterion 5 pins the file under the worktree's `.stage2-sessions/`, and owner-only modes keep out other users only, not processes of the same user. A session still open in the same worktree can therefore rewrite the next attempt's launcher. Codex runs there with `--sandbox workspace-write`, and Pi's policy keeps only its edit/write tools out of `.stage2-sessions/`, not `bash`. The rewritten file then runs in Terminal outside Codex's sandbox and can hand the CLI a prompt that neither leak scan of criterion 6 saw. Today Terminal receives the scanned command itself, from memory. The same exposure exists today only for a Pi attempt's policy copy, which Pi loads after dispatch; this change extends it to every attempt and to the prompt. The [DETAIL] "owner-only permissions bound the new local persistence" covers who can read the file, not who can change it. Because criterion 5 fixes the location, a build cannot move the file out of the writable worktree without a spec decision. An implementation that ignores integrity and one that adds a check both pass criteria 1–8, so the implementer alone would decide whether this is in scope or an accepted residual risk. | Opus | open | — |
| F-6 | MINOR | SPEC | base | spec.md criterion 3 and criterion 4; Open decisions, second [DETAIL] | Not decided: a launch-file path that holds a byte other than newline, CR or NUL which Terminal's input line does not take as data. In canonical mode, and in zsh's line editor, ^U discards what has been typed so far, DEL and ^W erase, ^C, ^Z and ^\ send signals, ^D ends input, and ^V quotes the next byte. If the main checkout's directory name contains ^U, the shell parses only the rest of the quoted path, with its quote parity flipped, so a crafted name runs a command of its own. Criterion 3 refuses only newline, CR and NUL, so such a path is eligible, and criterion 4 then requires it to stay data. Criterion 4 is refuted only "in a stand-in", and a stand-in runs the dispatched string without a terminal, so the test stays green. The [DETAIL]'s reason, that such paths "cannot be sent as the required single line", applies to these bytes too. The implementer has to choose: refuse them (a reason criterion 3 does not name), encode them for a login shell the spec does not specify, or let them through. | Opus | open | — |
