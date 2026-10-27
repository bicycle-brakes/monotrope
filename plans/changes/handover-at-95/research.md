---
title: "Research — handover-at-95"
status: draft
implementation_status: none
date: 2026-10-14
last_reviewed: 2026-10-14
updated: 2026-10-27
supersedes: null
superseded_by: null
bead: coding-harness-l9s
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-10-14"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research, claude-code, statusline, handover, usage-limit]
---

# The session writes its handover at 95 % of the usage window — Research

Phase 1 for bead coding-harness-l9s, read on 2026-10-14 against `origin/main`
at `3199a28`, during the third night run. Exploration only; the interview
questions below wait for the maintainer.

## The request

The maintainer, 2026-10-13: when the current usage-limit window (the
five-hour "current session" of `/usage`) reaches 95 %, the session writes its
handover automatically, as a pull request, per the handover rule.

## What Claude Code offers (read 2026-10-14)

Source: the official documentation, read through a documentation sub-agent
on 2026-10-14 — `https://code.claude.com/docs/en/statusline`,
`https://code.claude.com/docs/en/hooks` (about 200,000 of 268,801 characters
read; the rest not read) and the visible part of the changelog up to 2.1.296.
The installed version is 2.1.296 (`claude --version`). The fields were not
yet observed in a live status-line input on this machine.

- **The status line receives the windows.** Its stdin JSON carries
  `rate_limits.five_hour.used_percentage` and
  `rate_limits.seven_day.used_percentage` (numbers 0–100) and each window's
  `resets_at` (Unix epoch seconds).
  - Present only for claude.ai Pro and Max subscribers (or behind a gateway
    that sets a spend limit), and only after the first API response of the
    session.
  - Each window may be absent on its own; a window is dropped once its
    `resets_at` has passed.
  - The script re-runs when a window reaches its `resets_at`.
  - Since which version the fields exist is not documented.
  - The installed 2.1.296 has them: its binary carries the status-line
    schema with `rate_limits.five_hour.used_percentage` and builds a
    `rate_limits` object (and `rate_limits_available`) into the status-line
    input (`grep -a` over the binary, 2026-10-14). That is the code, not a
    live value: whether this subscription's session receives it is still
    the gap below.
- **No hook input carries the percentage** (not documented in the part
  read). The common hook fields are `session_id`, `transcript_path`, `cwd`,
  `permission_mode`, `effort`, `hook_event_name` and a few more; the
  `StopFailure` error type `rate_limit` signals a hit limit, not a
  percentage.
- **A hook cannot run a slash command.** Hook outputs add context
  (`additionalContext`), block (`decision`, exit code 2), stop
  (`continue: false`) or warn (`systemMessage`); none invokes `/handover`.
  The documented way to make Claude act is a Stop hook that blocks with a
  reason, which keeps the session going with that reason as its next
  instruction.

## Where it stands in this repository

- `tools/claude-code/statusline.sh` (257 lines) reads its stdin through `jq`
  (`j()` at line 12) and shows model, context use (`context_window.*`,
  lines 103–120) and the session id (line 196). It does not read
  `rate_limits` today.
- `tools/claude-code/hooks/handover.sh` is the session entry and the safety
  net (the automatic session note after every answer, through `recap.sh` on
  `Stop`); writing a handover is the `/handover` skill's job, not the
  script's.
- `tools/claude-code/settings.json` declares the status line (line 2) and
  the `Stop` hooks (line 16); `tools/claude-code/install.sh` installs them
  into `~/.claude`. A change lands here and is reinstalled, never only in
  `~/.claude` (AGENTS.md, "Sessions across checkouts").

## The shape this suggests

1. The status line reads `rate_limits.five_hour.used_percentage`, shows it
   (yellow from 80, red bold from 95) and, at 95 or more, writes a marker
   file once per session id and window (`resets_at` in its name, so the
   next window can trigger again).
2. A `Stop` hook in `tools/claude-code/hooks/` sees the marker for its
   `session_id` and blocks once, with the reason "the usage window is at
   95 %: run /handover now"; it records that it fired, so it never blocks
   twice for the same window.
3. Without `rate_limits` (an API-key session, before the first response)
   nothing is shown and nothing fires.

## Questions this change has to answer

- [DECISION] How hard the trigger is: a `Stop` hook that blocks once and
  makes the session write the handover (recommended: the only documented
  way to make it act), only an injected reminder, or only a notification to
  the maintainer.
- [DECISION] Whether the seven-day window triggers too, and at which level.
- [DECISION] Whether 95 % leaves enough of the window for a handover pull
  request, or the threshold is lower (for example 90 %). To be measured on
  one real handover before the interview, if the maintainer wants a number.
- [GAP] Whether this machine's subscription session receives a value
  (2.1.296 has the field, see above): one logged status-line input settles it. Logging it means a
  change in `tools/claude-code/statusline.sh` and a reinstall, so it waits
  for the maintainer's go.
- [DETAIL] Marker files live under `~/.claude/` next to the session notes,
  one per session id and window; they are never committed.
