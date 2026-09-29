---
title: "Spec — omnigent-deny-layers"
status: draft
implementation_status: partial
date: 2026-09-29
last_reviewed: 2026-09-29
updated: 2026-09-29
supersedes: null
superseded_by: null
bead: coding-harness-rex
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [spec, omnigent, permissions, policy]
---

# Spec — omnigent-deny-layers

Package 1a of the Omnigent work (bead coding-harness-rex). Research:
`research.md` (its "Corrections after verification" and "Addendum — gaps
closed in phase 2" hold). Decisions: `decisions.md`.

## Problem

- **Omnigent's own tools slip past the rules that watch Claude Code's
  tools.** In an `omnigent claude` session they appear as
  `mcp__omnigent__<tool>`. A path rule such as `Edit(docs/**)` or a hook on
  `Write|Edit|Bash` does not see `mcp__omnigent__sys_os_write`, and
  Omnigent's own Claude Code hook skips every `mcp__omnigent__*` tool
  (research, correction 3). Only a Claude Code rule that names the tool
  reaches it.
- **Nothing names them today.** `.claude/settings.json` has no
  `permissions.deny`, and no Omnigent policy is configured on the machine
  (research, "What was measured").
- **One path has no Omnigent check at all.** Omnigent's bridge runs its own
  `sys_os_*` tools locally, without any policy, whenever its relay does not
  advertise them — before the relay starts and outside an active turn
  (addendum 7). There, a Claude Code rule is the only thing that can hold.
- **The doctrine says more than the tree holds.** `docs/WORKFLOW.md` §3 lists
  `permissions.deny` brakes on force push, `rm -rf`, deploys and
  `docs/decisions/` that do not exist (research, correction 5), and says a
  `Bash` redirect falls through path rules, which Claude Code no longer lets
  happen (addendum 12).

The maintainer decided on two layers: the rule in the repository first, an
Omnigent default policy from a file in this repository second
(`decisions.md`). ADR 0006 bounds it: nothing may depend on an Omnigent
policy alone, so layer 1 must hold by itself everything this change promises.

## What this change promises

In a Claude Code session in this repository — under Omnigent or not, except
under an agent spec that loads no project settings (Non-goals) — no Omnigent
tool that writes, runs, spawns or changes state can be called, and Claude
Code's own file tools cannot write Omnigent's configuration file.
Layer 2 adds the same refusal, server-side, for every Omnigent session on the
machine whose calls pass Omnigent's policy check; it is never the only thing
that stops a call in this repository.

## The rule and the list

**Rule.** An Omnigent tool stays allowed only if it reads and changes nothing
— no file, process, terminal, session, scheduled job, background call,
policy, Omnigent record or outside service. Every other tool Omnigent offers a
native harness is denied. One class sits between the two: a tool that changes
nothing but may send the caller's text to an outside judge is **asked** — the
user is asked each time it is used (decisions, item 5; findings, F-1). The surface is Omnigent's
`_NATIVE_RELAY_BUILTIN_TOOLS` plus its four `sys_os_*` tools (addendum 10).

The list as of 2026-09-29, Omnigent 0.15.0 (handler lines: the read-only
classification sub-agent's report of that date, `runner/tool_dispatch.py`
unless named). After the change, `scripts/omnigent_policy.py` is the one list;
this table is the record of the first cut.

| Denied (27) | Why |
|---|---|
| `sys_os_write`, `sys_os_edit` | write or edit a file (`inner/os_env.py:1022-1054`) |
| `sys_os_shell` | runs a shell command, unconfined without a sandbox (`os_env.py:908-927`) |
| `sys_agent_download` | writes an agent archive into the working directory (`:5301-5316`) |
| `sys_terminal_launch`, `sys_terminal_send`, `sys_terminal_close` | start a shell, type into it, kill it (`tools/builtins/sys_terminal.py:685`, `:835-869`, `:1040-1074`) |
| `sys_session_create`, `sys_session_send` | start or message a child session (`:3377-3473`, `:2397-2443`) |
| `sys_session_close`, `sys_session_rename`, `sys_session_share` | archive a session and stop its processes; retitle it; expose its transcript (`:6188-6252`, `:5721-5815`, `:5068`) |
| `sys_scheduled_task_create`, `_update`, `_delete` | create, change or delete a scheduled job (`:4555-4571`) |
| `sys_call_async`, `sys_cancel_async`, `sys_cancel_task`, `sys_read_inbox` | run any granted tool in the background (`sys_os_shell` included), cancel it or a child, empty the inbox and write a receipt (`:8095-8377`, `:7942-8030`) |
| `sys_add_policy` | adds a policy to the session (`:4424-4456`) |
| `update_comment` | changes a review comment's status (`:4276-4300`) |
| `browser_navigate`, `browser_click`, `browser_type` | load a URL, act on and type into a live page (`:4303-4360`) |
| `hindsight_retain`, `hindsight_recall`, `hindsight_reflect` | send session content to an outside memory service (`tools/builtins/hindsight.py:47`) |

| Allowed (16) | Why |
|---|---|
| `sys_os_read` | reads a file inside the working directory (`os_env.py:1001-1020`, `:1120-1191`) |
| `sys_terminal_read`, `sys_terminal_list` | read a terminal's screen, list terminals |
| `sys_session_list`, `sys_session_get_info`, `sys_session_get_history` | read sessions |
| `sys_agent_list`, `sys_agent_get` | read agents |
| `sys_scheduled_task_list`, `sys_policy_registry` | list jobs, list policy types |
| `sys_list_models` | reads the model catalogue |
| `list_comments`, `load_skill`, `read_skill_file` | read comments and skills |
| `browser_snapshot`, `browser_screenshot` | capture the current page |

| Asked (1) | Why |
|---|---|
| `sys_advise_models` | changes no file, session or record, but when a routing backend is configured it sends the caller's task text to that routing judge (Omnigent 0.15.0, `server/routes/_sessions/helpers.py`, `_handle_advise_models_mcp`; findings, F-1). The first cut allowed it on its docstring; the maintainer moved it to "asked" on 2026-09-29. |

**Protected path** (layer 2, part b, and its mirror in layer 1): any file
ending in `/.omnigent/config.yaml` — in practice `~/.omnigent/config.yaml`,
which carries layer 2 itself.

## Acceptance criteria

1. **One list.** The denied tools, the asked tools, the allowed tools and the
   protected paths are each named once, in `scripts/omnigent_policy.py`, every entry with a
   one-line reason. `.claude/settings.json`'s Omnigent rules,
   `tools/omnigent/policy.yaml` and the tests derive from it or compare
   against it.
   *Refuted by:* a tool list typed into a test, the installer or a policy
   file by hand; a name in both lists; an entry without a reason.
2. **Complete against the installed Omnigent.** Every tool of the native
   surface of the Omnigent that is installed is in exactly one of the three
   lists (denied, asked, allowed), and no listed tool is missing from that surface.
   *Refuted by:* the surface test red after an Omnigent upgrade adds or drops
   a tool. It runs where Omnigent is installed and skips with a stated reason
   where it is not (CI). A misclassified tool is refuted by review against the
   table's file:line.
3. **Layer 1 holds alone.** `.claude/settings.json` denies
   `mcp__omnigent__<tool>` for every denied tool and
   `Edit(//**/.omnigent/config.yaml)`; it has no rule that denies an allowed
   tool or all of Omnigent at once (`mcp__omnigent`, `mcp__omnigent__*`,
   `mcp__*`, `*`); its `permissions.ask` names `mcp__omnigent__<tool>` for
   every asked tool, and no deny or allow rule covers an asked tool; its
   SessionStart hook is unchanged.
   *Refuted by:* the settings test red when one denied tool's rule is
   removed, an allowed tool's rule or a blanket rule is added, an ask rule is
   missing or an asked tool is moved to deny or allow, or the hook changes.
4. **Layer 2 is a file in this repository.** `tools/omnigent/policy.yaml`
   has one top-level key, `policies:`, with three `type: function` policies,
   `coding_harness__omnigent_writing_tools`,
   `coding_harness__omnigent_asked_tools` and
   `coding_harness__protected_paths`, all on
   `omnigent.policies.builtins.cel.cel_policy`, and its text is exactly what
   `scripts/omnigent_policy.py` renders from the one list.
   *Refuted by:* the CI-safe policy test red after the list changes without a
   re-render, or after a hand edit of the file.
5. **Layer 2 behaves, measured offline with Omnigent's own code.** Parsed
   with Omnigent's `parse_default_policies` and evaluated through
   `cel_policy`: a `tool_call` of every denied tool — bare or as
   `mcp__omnigent__<tool>`, with or without `arguments` — is DENY with a
   reason that names the tool; every asked tool, in both spellings, is ASK
   with a reason that names it; every allowed tool abstains; Claude Code's
   `Write`, `Edit` or `MultiEdit` with a `file_path` ending in
   `/.omnigent/config.yaml` is DENY, and on any other path abstains; no event
   shape — no `data`, `data` as text or null, `name` missing or not text,
   `arguments` as text, a request event, an empty event — makes either
   expression raise an evaluation error (an error abstains, which would open
   the gate silently).
   *Refuted by:* the offline tests, which run where Omnigent is installed and
   skip with a stated reason where it is not (CI).
6. **The installer merges safely and says what to do next.**
   `tools/omnigent/install.sh`, run by the maintainer in a terminal, merges
   the file's `policies:` into the global Omnigent config
   (`$OMNIGENT_CONFIG_HOME/config.yaml`, else `~/.omnigent/config.yaml`). It
   keeps every other key and every policy not named `coding_harness__*`,
   replaces the `coding_harness__*` policies as a set, keeps
   `config.yaml.bak-<timestamp>` before any change, changes nothing on a
   second run and says so, validates the result with Omnigent's parser and
   CEL compiler and writes nothing if that fails. `--check` says whether the
   installed policies equal the repository's and changes nothing; `--remove`
   takes the `coding_harness__*` policies out. A run that changed the file
   ends by saying that the Omnigent server must be restarted and how; one
   that did not says no restart is needed. It refuses to install or remove
   without a terminal.
   *Refuted by:* the merge tests on temporary files (a foreign key or policy
   lost, an owned policy duplicated or left behind, no backup before a
   change, a backup on an unchanged run, a file written after a failed
   validation) and the installer, run without a terminal, changing anything.
7. **The texts say what is true.** `docs/WORKFLOW.md` (the note "Not all of
   it is here yet", §3 "Worktrees" item 5, "What isolation consists of here"
   item 3) and `AGENTS.md` (the Omnigent bullet under "Sessions across
   checkouts") state which Omnigent tools are denied and by which rule, where
   the one list lives, that layer 2 is a per-machine second layer the
   maintainer installs and nothing depends on alone, that the template's
   brakes on the irreversible are not in this repository, what `Edit` path
   rules reach and what they do not, and the bridge-local window.
   *Refuted by:* a sentence there that names a deny rule
   `.claude/settings.json` does not have, says a `Bash` redirect falls
   through `Edit` rules, or says Omnigent's tools pass `permissions.deny`
   unseen; `AGENTS.md` over 200 lines or containing the word README
   (`tests/test_entry_points.py`). Held by review, not by a test of prose.
8. **Live measurement — by the maintainer, not in CI.** After installing and
   restarting Omnigent, measured once and written to
   `docs/research/<date>-omnigent-deny-layers-live-measurement.md`:
   (a) layer 1 — in an `omnigent claude --use-native-config` session started
   in this repository, `mcp__omnigent__sys_os_write` is not offered or is
   refused and creates no file, while `mcp__omnigent__sys_os_read` answers;
   (b) layer 2 — in the same kind of session started in a scratch directory
   outside any repository, `mcp__omnigent__sys_session_rename` returns
   "Denied by policy" with the reason of
   `coding_harness__omnigent_writing_tools` and the title stays, and Claude
   Code's `Write` to `<scratch>/.omnigent/config.yaml` is refused by
   `coding_harness__protected_paths` and creates no file. Recorded, not a
   criterion: whether `mcp__omnigent__sys_os_write` in the scratch session is
   refused or writes (the bridge-local window).
   *Refuted by:* a created file, a tool result without the denial, a title
   that changed, or no result file.

## Non-goals

- Porting either layer to `lakeswitch-ai` or `portfolio-agentic-engineering`.
- Harnesses Omnigent does not hook — Goose, Qwen, Kiro, Cursor, Antigravity
  (`decisions.md` point 1) — and Codex's `apply_patch`, whose target paths
  the protected-path policy does not parse.
- The D-60 write guard (ADR 0006, "Owed before this holds by tool").
- The template's brakes on the irreversible: force push, `rm -rf`,
  production deploy, `bundle destroy`, writes under `docs/decisions/`.
- Closing Omnigent's bridge-local window or any other change to Omnigent,
  and an upstream report about it.
- Sessions under an agent spec with `skills_filter: none`: Omnigent then
  loads no project settings, so layer 1 is absent (addendum 9).
- Tools Omnigent gives only its own non-native agents (timers, `web_*`,
  `upload_file`, `download_file`, `list_files`, `nimble_*`).
- Scoping layer 2 to one repository (needs a measurement of session labels,
  addendum 13).
- A new entry in `decisions/gates.yaml`; the tests run in the existing
  `pytest` gate.
- `permissions.disableBypassPermissionsMode`, `Read` denies, a sandbox.

## Open decisions

**[DECISION] Layer 2 reaches every Omnigent session on this machine.**

**Answered 2026-09-29 by the maintainer: option 2** — build it, do not install
yet (`decisions.md`, item 4). Criterion 8 shrinks to part (a); part (b) is bead
coding-harness-671, after the maintainer's return.

```
Goal in one sentence:  Omnigent keeps one policy set per machine and, as
                       read, the policy cannot tell which repository or which
                       kind of agent a call comes from — so denying
                       Omnigent's writing tools there denies them in every
                       Omnigent session on this machine, including
                       Omnigent's own agents, which write files and run
                       commands only through those tools.
Options:               1. Install on this machine now — Claude Code, Codex
                          and the other hooked harnesses keep their own file
                          and shell tools; an Omnigent
                          agent that works through Omnigent's tools (in any
                          repository on this machine) can only read until
                          the policy is removed; Omnigent's cross-harness
                          routing, which spawns through these tools, stops.
                       2. Build it, do not install yet — the file, installer
                          and tests land; this repository is held by layer 1
                          alone; Codex and the other harnesses under
                          Omnigent stay uncovered until installation.
Recommendation:        1 — because this repository's workflow runs only
                       `omnigent claude` sessions (ADR 0006), and
                       `install.sh --remove` undoes it in one command.
If you say "ok":       everything in this spec is built; after the merge the
                       maintainer runs tools/omnigent/install.sh, restarts
                       Omnigent, and criterion 8 is measured in full.
What is lost:          option 2 would keep Omnigent's own agents writing on
                       this machine without anyone touching the config.
```

With option 2, the build is the same and criterion 8 shrinks to part (a);
part (b) moves to a follow-up bead the tracker writer creates.

**Decided here — `[DETAIL]`, reversible, reason recorded:**

- **Deny by the rule, not by feel.** "Read-only stays allowed" leaves one
  rule; a per-tool judgement would drift. It costs two features in Claude
  Code sessions here: marking a review comment done (`update_comment`) and
  Omnigent's sub-sessions and cross-harness routing. Both come back by
  moving a name to the allowed list.
- **Exact names in layer 1, not a glob.** `mcp__omnigent__sys_os_*` would
  also deny `sys_os_read`; exact names cannot over-match and are what the
  test compares. Globs in deny rules are documented (addendum 11) but not
  needed.
- **The irreversible-command brakes stay out.** This repository deploys
  nothing, runs no bundle and has no `docs/decisions/`; a `Bash` pattern for
  force push or `rm -rf` is passed by the next spelling (`git push origin
  +main`, `rm -fr`). Leaving them out keeps nothing false alive because
  criterion 7 rewrites the passage that claims them.
- **Protected set: Omnigent's config file only.** It is the smallest set that
  stops an agent from switching off layer 2 with its own file tools, and it
  binds no repository's work. `.claude/settings.json` is left out: layer 2
  may not be the only thing that stops a write here, so protecting it would
  need a layer-1 rule too, and that would bar every agent session in this
  repository from changing project settings, the next update of this list
  included. Claude Code already asks before writes under `.claude/` in every
  mode except `bypassPermissions`. Matching by suffix covers
  `~/.omnigent/config.yaml` without knowing the home directory; the layer-1
  mirror is `Edit(//**/.omnigent/config.yaml)`.
- **Both spellings of a tool name.** The relay path delivers the bare name
  (addendum 6); the prefixed one is matched too because Omnigent's server
  accepts it for one tool. Hermes' `mcp_omnigent_` form is not matched: its
  hook skips Omnigent's tools, so they reach the policy on the relay path,
  bare.
- **Two policies, not one.** The refusal then names what it refused for.
- **The one list is a Python constant** in `scripts/omnigent_policy.py`, as
  the omitted keys of the bead export were (archive
  `2026-09-21-reproducible-bead-export`, criterion 4): the linter covers
  `scripts/`, the tests import it, and the installer merges the committed
  YAML, not the module.
- **Omnigent's interpreter** for the installer and the offline tests:
  `$OMNIGENT_PYTHON` if set, else the interpreter named in the first line of
  the `omnigent` launcher on the `PATH` (the uv tool environment's own
  Python, which has PyYAML, `celpy` and Omnigent). Absent → the installer
  stops, the tests skip and say so.
- **The installer refuses without a terminal.** "The maintainer runs it, not
  an agent or CI" is then a check, not only a sentence; `--check` works
  without one.
- **Comments in `config.yaml` do not survive a merge** (PyYAML); the backup
  keeps them, and the installer says so.
- **The test file is `tests/test_omnigent_deny_layers.py`**, not
  `tests/test_repo_settings.py`: `docs/WORKFLOW.md` gives that name to a
  container fence this change does not build.
- **The measurement goes to `docs/research/`**, where research about this
  repository lives (`AGENTS.md`, "Sessions across checkouts").
