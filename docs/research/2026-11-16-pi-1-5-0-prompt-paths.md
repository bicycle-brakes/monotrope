---
title: "Pi 1.5.0 system prompt — local absolute paths in every launch shape, and the personal AGENTS.md in the session"
category: research
created: 2026-11-16
updated: 2026-11-16
last_reviewed: 2026-11-16
owner: framework-architect
status: current
implementation_status: none
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-11-16"}
review: {status: pending, approved_by: null, approved_at: null}
bead: coding-harness-xul8
tags: [pi, stage-2, leak, system-prompt, paths, context-files, measurement]
---

# Pi 1.5.0 system prompt — local absolute paths per launch shape

**Result (measured 2026-11-16, against `origin/main` at the time, pinned Pi
1.5.0 from `tools/pi/package.json`):** every launch shape the runner uses sends
the absolute install path of Pi's own documentation in `<docs>`, which carries
the home directory, the account name and the checkout or worktree name. Shapes
that start in the repository also send that path as `<cwd>`. A session with
context files on additionally sends the personal `~/AGENTS.md` from outside the
repository. A `before_agent_start` handler that sets
`systemPromptOptions.cwd` now reaches the first request (the 1.2.0 defect is
gone), but it does not touch `<docs>`.

Paths below are redacted: `<HOME>` is the home directory (it contains the
account name), `<WT>` the checkout the runner starts from (here the throwaway
worktree `<HOME>/coding-harness/.claude/worktrees/pi-measure`), `<SCRATCH>` a
`tempfile` directory under the macOS `TMPDIR` (`/var/folders/…/T/stage2-…`,
which carries no account name).

## Method

- No online model contact. A loopback OpenAI-compatible recorder (Python
  `ThreadingHTTPServer` on 127.0.0.1, one SSE answer `ok`) recorded the full
  request body. The scratch `models.json` pointed provider `opencode-go` at it;
  `tests/pi_network_guard.mjs` was preloaded through `NODE_OPTIONS`, as in
  `tests/test_pi_contract.py`. Every launch exited 0 with exactly one request.
- The real pinned Pi through `tools/pi/pi`, scratch `HOME` and
  `PI_CODING_AGENT_DIR`, the runner's `PI_AGENT_SETTINGS`.
- Argv rebuilt by hand from the builders (not by calling them, which need a
  refreshed model store and an address record): `run_reviewer` in
  `scripts/stage2.py` (free: `--no-tools`, cwd scratch; paid: `--tools
  read,grep,find,ls`, cwd the root), `Run.pi_command` in
  `scripts/stage2_research_run.py` (repository seat: path-lock extension, read
  tools, cwd the root; public seat: research-tools extension, public tools, cwd
  scratch), `probe_go` in `scripts/stage2_availability.py` (`--no-tools`, cwd
  scratch), `cli_argv` in `scripts/stage2_session.py` (context files on, cwd
  the root).
- Limits: the session was measured with `--print` instead of the interactive
  window, and without its own `-e` session extension; the research seats ran
  without the `@research-data.md` attachment. These parts are not measured.

## 1. Paths in the request, per launch shape

| Launch shape | cwd | `<docs>` install path | `<cwd>` | `<project_context>` | home dir / account / worktree name sent |
|---|---|---|---|---|---|
| free reviewer (`run_reviewer`, free) | scratch | yes | `<SCRATCH>` | none | yes / yes / yes (via `<docs>`) |
| paid reviewer (`run_reviewer`, paid) | root | yes | `<WT>` | none | yes / yes / yes |
| research repository seat | root | yes | `<WT>` | none | yes / yes / yes |
| research public seat | scratch | yes | `<SCRATCH>` | none | yes / yes / yes (via `<docs>`) |
| `probe_go` | scratch | yes | `<SCRATCH>` | none | yes / yes / yes (via `<docs>`) |
| session (`cli_argv`, context files on) | root | yes | `<WT>` | `~/AGENTS.md` and `<WT>/AGENTS.md` | yes / yes / yes |

In no shape did the home path appear outside the system message (user turn
and tool schemas were checked). Occurrences of the home path per body: 3 for
the scratch shapes, 4 for root shapes, 6 for the session.

The `<docs>` section, identical in all shapes:

```
<docs>
- Main documentation: <WT>/tools/pi/node_modules/@earendil-works/pi-coding-agent/README.md
- Additional docs: <WT>/tools/pi/node_modules/@earendil-works/pi-coding-agent/docs
- Examples: <WT>/tools/pi/node_modules/@earendil-works/pi-coding-agent/examples (extensions, custom tools, SDK)
- When reading pi docs or examples, resolve docs/... under Additional docs and examples/... under Examples, not the current working directory
...
</docs>
```

`<cwd>` for scratch shapes is `/private<SCRATCH>`; for root shapes `<WT>`.

## 2. Context files on: discovery walks up to the home directory

Yes. With context files on and cwd `<WT>`, the request carried:

```
<project_context>
<project_instructions path="<HOME>/AGENTS.md">
… (the maintainer's personal instruction file, outside the repository) …
<project_instructions path="<WT>/AGENTS.md">
… (the repository's AGENTS.md) …
</project_context>
```

So the session sends a personal file that lives outside the repository to the
online model, together with its absolute path.

## 3. `before_agent_start` editing `systemPromptOptions.cwd`

Source (1.5.0, `dist/core/agent-session.js` `_prepareRun`, and
`dist/core/extensions/runner.js` `emitBeforeAgentStart`): the handlers receive
and mutate one options object; `_prepareRun` passes the result to
`_preparePromptAndToolLoadout` before the first request is built. So the edit
should reach the first rendering.

Live proof: a throwaway extension (`pi.on("before_agent_start", e => {
e.systemPromptOptions.cwd = "/workspace" })`) on the paid-reviewer shape gave
`<cwd>\n/workspace\n</cwd>` in the first and only request. The 1.2.0 defect
does not reproduce on 1.5.0. The same request still carried the home path three
times, all in `<docs>`: the cwd hook alone does not remove the leak.

## Consequence for the bead

- Rewriting `cwd` through an extension is now viable, but `<docs>` needs its own
  treatment (another option field, a forced system prompt, or starting Pi from
  an install path without the home directory). Which field holds the docs paths
  in 1.5.0 is not read.
- The session needs either context files off outside the repository or a
  discovery boundary at the repository root.
