---
title: "Research — omnigent-deny-layers"
status: accepted
implementation_status: done
date: 2026-09-29
last_reviewed: 2026-09-29
updated: 2026-09-30
supersedes: null
superseded_by: null
bead: coding-harness-rex
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by:
  kind: llm-session
  name: claude-code
  version: "2026-09-29"
review:
  status: pending
  approved_by: null
  approved_at: null
tags: [research]
---

# omnigent deny layers — Research

Phase 1 research on two protective layers against Omnigent's own tools bypassing Claude Code's hooks and permission rules. The task: Layer 1 in .claude/settings.json with a permissions.deny list; Layer 2 as an Omnigent default policy in this repository, enforcing the same denials across harnesses. Both claim that ADR 0006 says nothing may depend on Layer 2 alone.

## Question

**Layer 1 — Claude Code's permission-rule syntax:**
- Does Claude Code support patterns like `mcp__omnigent__sys_os_*` (wildcard) in permissions.deny, or must each tool be named separately?
- What is the syntax for denying MCP tools by name in .claude/settings.json?

**Layer 2 — Omnigent default policy:**
- Can a CEL policy be evaluated offline (pure function, no running server) so tests can prove deny/allow without infrastructure?
- What file path and configuration would an installer follow to place a default policy into ~/.omnigent/config.yaml or equivalent?
- Does Omnigent's server pick up changed config without restart, and if so, how?

**WORKFLOW.md claim:**
- Section 3 (line 333–339) claims .claude/settings.json already denies: prod deploy, `bundle destroy`, force-push, `rm -rf`, writes under docs/decisions/. Is this true in the working tree?

## What was measured

**Current .claude/settings.json:**
- Path: `.claude/worktrees/omnigent-deny-layers/.claude/settings.json`
- Content (full file): `{"hooks": {"SessionStart": [{"hooks": [{"command": "\"$CLAUDE_PROJECT_DIR\"/tools/bd prime --hook-json", "type": "command"}], "matcher": ""}]}}`
- Status: No `permissions.deny` block present. No settings.local.json found.

**Tests for settings:**
- Searched `.claude/worktrees/omnigent-deny-layers/tests/` and lakeswitch-ai repository root.
- Found: No test_repo_settings.py. Test suite includes test_ci.py, test_gate_machinery.py, test_regelwerk.py (17 total in worktree); none explicitly test settings.json permission rules.

**Omnigent tool names (exposed as MCP):**
- From system reminder, Omnigent exposes these as `mcp__omnigent__*`:
  - **Write/execute:** `sys_os_write`, `sys_os_edit`, `sys_os_shell`, `sys_terminal_launch`, `sys_terminal_send`, `sys_terminal_close`, `sys_terminal_read`, `sys_terminal_list`, `sys_session_create`, `sys_session_send`, `sys_session_close`, `sys_session_get_info`, `sys_session_get_history`, `sys_session_rename`, `sys_session_share`, `sys_scheduled_task_create`, `sys_scheduled_task_update`, `sys_scheduled_task_delete`, `sys_call_async`, `sys_cancel_async`, `sys_add_policy`
  - **Read-only:** `sys_agent_list`, `sys_agent_get`, `sys_agent_download`, `sys_session_list`, `sys_list_models`, `sys_cancel_task`
- Source: `/Users/mikypiky/.local/share/uv/tools/omnigent/lib/python3.12/site-packages/omnigent/` packages (tools/builtins/, native/, tools/manager.py)

**Omnigent CEL policy structure — YAML shape:**
- Location: `omnigent.policies.builtins.cel.cel_policy`
- YAML in server config (`~/.omnigent/config.yaml`) under `policies:` key:
  ```yaml
  policies:
    block_sys_os_write:
      type: function
      handler: omnigent.policies.builtins.cel.cel_policy
      factory_params:
        expression: 'event.type == "tool_call" && event.data.name == "sys_os_write"'
        reason: "File write access denied."
  ```
- Parser: `omnigent.spec.parser.parse_default_policies()` reads the `policies:` mapping from config YAML. Return type: list of PolicySpec objects.
- Source: `/Users/mikypiky/.local/share/uv/tools/omnigent/lib/python3.12/site-packages/omnigent/policies/builtins/cel.py` (lines 1–100) and schema.py

**CEL event shape for tool calls:**
- Type signature (from `omnigent.policies.schema.PolicyEvent`):
  ```python
  {
    "type": "tool_call",      # literal
    "target": str,            # tool name, e.g. "sys_os_write"
    "data": {
      "name": str,            # tool name, same as target
      "arguments": {...}      # tool arguments dict
    },
    "context": {...},         # actor, usage, model, labels, etc.
    "session_state": {...},   # mutable state dict
    "llm_client": ...,
    "request_data": ...
  }
  ```
- CEL expression to deny all sys_os_* and sys_terminal_*:
  ```cel
  event.type == "tool_call" && (event.data.name.startsWith("sys_os_") || event.data.name.startsWith("sys_terminal_"))
  ? {"result": "DENY", "reason": "File system access denied"}
  : null
  ```
- Source: omnigent/policies/schema.py lines 179–244 (PolicyEvent TypedDict)

**CEL policy offline evaluation — VERIFIED WORKING:**
- Import: `from omnigent.policies.builtins.cel import cel_policy` (no Omnigent server required)
- Test code executed:
  ```python
  policy = cel_policy(
    expression='event.type == "tool_call" && event.data.name == "sys_os_write" ? {"result": "DENY", "reason": "File write denied"} : null',
    reason="Denied"
  )
  result = policy(test_event)  # synthetic event dict
  # Output: {'result': 'DENY', 'reason': 'File write denied'}
  ```
- Conclusion: Policy callables are pure functions; they can be imported and tested offline in a unit test without a running server or session.
- Source: `/Users/mikypiky/.local/share/uv/tools/omnigent/lib/python3.12/site-packages/omnigent/policies/builtins/cel.py` (lines 86–100, function `cel_policy`)

**How this repository installs tools:**
- Script: `tools/claude-code/install.sh`
- Pattern (lines 36–48, 64–84):
  1. Read current `~/.claude/settings.json` (or empty dict if absent)
  2. Merge in hooks from `./settings.json` (add new hooks unless command already exists)
  3. Copy files (`statusline.sh`, hooks/*.sh, skills/*`) to ~/.claude/
  4. Write merged settings back to ~/.claude/settings.json.tmp, then move to final location
  5. Preserve backups as `<file>.bak-<timestamp>`
- For an Omnigent policy installer, the pattern would be:
  1. Write policy YAML to a stable path (e.g., `~/.omnigent/policies.d/coding-harness-deny.yaml` or embed in config.yaml)
  2. Verify or restart Omnigent server to pick up the new policies
- No current implementation exists; ~/.omnigent/config.yaml has only `host:` and `telemetry:` sections (no `policies:`)

**Omnigent server config reload behavior:**
- Not directly verified. The `parse_default_policies()` function is called at server startup (cli.py line 4465), suggesting policies are loaded once at boot.
- No evidence found of hot-reload or watch mechanism for config.yaml changes.
- Source: `/Users/mikypiky/.local/share/uv/tools/omnigent/lib/python3.12/site-packages/omnigent/cli.py` line 4456–4465

## What exists

**In this worktree (.claude/worktrees/omnigent-deny-layers):**
- `.claude/settings.json`: hooks only, no permissions.deny (verified)
- `docs/WORKFLOW.md`: section 3 claims permissions.deny for "prod deploy, bundle destroy, force-push, rm -rf, decisions" (line 333–339), but no evidence of implementation yet
- `docs/adr/0006-parallel-work-without-a-pilot.md`: Explicitly states "The layers that hold it, none of them an Omnigent setting" (line 78). Supersedes ADR 0005's layer 2 (Omnigent session policy) — the write guard of D-60 takes its place, not an Omnigent default policy. Consequential: "Layer 2's `…validation 'in M0'` lapses" (line 99).
- No plugin/ directory yet (would be needed for write guards mentioned in ADR 0006)

**In Omnigent 0.15.0 installation:**
- CEL policy factory: fully implemented, offline-testable
- No default policies configured in ~/.omnigent/config.yaml
- Policy schema supports both server-wide defaults and per-session policies

**Permission syntax in Claude Code:**
- Not found. No documentation, no examples in repo, no tests. [DETAIL: may exist in Claude Code docs or cli help; see Open Points]

## Risks and edge cases

1. **Omnigent policy is not a hard boundary.** ADR 0006 (line 124–127): "Worktrees are not a security boundary. Without an Omnigent sandbox, a worktree keeps sessions from colliding; it does not confine what an agent can reach. The target document's trust contracts that assume a sandbox are open, not settled by this ADR." A policy in Omnigent denies tool invocation at call time but does not prevent file system access if the agent has direct access to the shell or via Bash tool.

2. **CEL policy evaluation error abstains (fails open).** Earlier read-only research noted: "a CEL evaluation error abstains (fails open)"; a malformed expression in the policy would not block the tool. Must be tested.

3. **Wildcard patterns.** The task asks whether `mcp__omnigent__sys_os_*` works in Claude Code's permissions.deny. This is not yet verified. Claude Code uses different naming (file_path vs. Omnigent's path), and permission rule syntax may not support wildcards — or may require a specific glob or regex syntax.

4. **Installation and config merge.** A policy file placed in ~/.omnigent/ must be picked up by parse_default_policies(); unclear whether admin-level or user-level config takes precedence, or whether Omnigent merges multiple policy sources.

5. **Multi-harness scope.** The task says Layer 2 is "across harnesses" — Omnigent loads policies from ~/.omnigent/config.yaml, which is machine-wide. An omnigent claude session, omnigent codex session, and omnigent with a custom harness all read the same server config. This is breadth, not narrowness — policies apply everywhere Omnigent runs on that machine, not scoped to "this repository only."

## Corrections after verification (orchestrating session, 2026-09-29)

Checked against the tree at `9f14283` and the Omnigent 0.15.0 source. Where
these disagree with the text above, these hold.

1. **The "[DECISION]" below is not open.** The maintainer decided on
   2026-09-29 to build both layers, with the repository layer first and the
   Omnigent policy as a second layer (`decisions.md`). ADR 0006's three layers
   hold the *tracker* rules (who writes the tracker); its driver says nothing
   may depend on an Omnigent policy. Layer 1 alone must therefore hold what
   this change promises; layer 2 adds coverage for harnesses other than
   Claude Code and is never the only thing that stops a write. That is
   consistent with ADR 0006, not a change to it.
2. **The default-policy YAML accepts both spellings.**
   `spec/parser.py`, the `type: function` branch: the callable path comes from
   `function:` or its alias `handler:`, and arguments from
   `function: {path, arguments}` or a sibling `factory_params:` — not both.
   `cel_policy` takes `(*, expression: str, reason: str = "Denied by policy.")`
   (measured with `inspect.signature`).
3. **In a Claude Code session, Omnigent's own tools are checked on the relay
   path, not by the native hook.** `native/native_policy_hook.py`,
   `hook_payload_to_evaluation_request`: a `tool_name` starting with
   `mcp__omnigent__` returns `None` ("already policy-checked by the relay path
   … `_evaluate_tool_call_policy`"). Claude's own `Write`, `Edit`, `Bash` go
   through the native hook. A policy therefore has to name both families, and
   the tool name the relay path puts into `event.data.name` for an Omnigent
   tool has to be measured, not assumed (`sys_os_write` or the prefixed name).
4. **Claude Code's rule syntax for MCP tools** is documented as the exact name
   `mcp__<server>__<tool>`, or `mcp__<server>` for every tool of a server; a
   glob inside the tool name (`mcp__omnigent__sys_os_*`) is not a documented
   form. Treat it as unverified and name each tool, or measure it.
5. **The WORKFLOW claim is false in this tree**, as measured above; pull
   request 49 now says so in a note at the top of `docs/WORKFLOW.md`.

## Open points

**[DECISION]** Whether Layer 1 (Claude Code permissions.deny) is sufficient alone, or Layer 2 (Omnigent default policy) is needed for multi-harness defense.
- Context: ADR 0006 (line 78–87) lists three layers, "none of them an Omnigent setting." It does not list a fourth layer (Omnigent policy). If a policy is added, it changes the architecture described in ADR 0006.
- Risk: Depending on an Omnigent policy violates ADR 0006's decision driver (line 45): "nothing here may depend on an Omnigent policy or sandbox the maintainer does not run."

**[GAP]** Claude Code permission-rule syntax for MCP tools — specifically, whether Claude Code supports wildcard patterns like `mcp__omnigent__sys_os_*` in permissions.deny, or requires individual tool names.
- Could not find in: repo docs, local help, installed Claude Code docs, system reminder
- Recommendation: Read or call Claude Code help (`claude --help` or Claude API docs on permissions); check whether pattern matching is supported and what the syntax is (glob, regex, or exact-match only)

**[GAP]** Omnigent policy hot-reload — whether ~/.omnigent/config.yaml is watched for changes or requires a server restart.
- Not found in: cli.py, policies/ package, server harness code
- Recommendation: Test with a running server; add or modify a policy in config.yaml and check whether it takes effect

**[DETAIL]** Path and naming convention for Layer 2's policy file.
- Options: (1) embedded in ~/.omnigent/config.yaml under policies:; (2) separate file ~/.omnigent/policies.d/coding-harness-deny.yaml (if Omnigent supports config.d pattern); (3) generated at install time and written to a stable path
- Recommendation: Check Omnigent loader code (cli.py parse_default_policies) to see whether it can read multiple sources or only --config

**[DETAIL]** Whether a policy file placed in the repository (e.g., config/omnigent-default-policy.yaml) can be installed as a machine-wide ~/.omnigent/config policy, and what the installer pattern is.
- The coding-harness install script (tools/claude-code/install.sh) copies files to ~/.claude/ and merges settings.json. A similar pattern for Omnigent would copy/merge into ~/.omnigent/, but this is machine-wide, not project-scoped.

## Addendum — gaps closed in phase 2 (spec session, 2026-09-29)

Read in the Omnigent 0.15.0 source (`$P` =
`~/.local/share/uv/tools/omnigent/lib/python3.12/site-packages/omnigent`) and
in the Claude Code documentation (code.claude.com, fetched 2026-09-29).
Nothing was run against Omnigent; an offline run of the draft expression with
Omnigent's interpreter needed an approval this session did not have, so the
CEL features the plan uses are **not measured** yet (the plan's offline test
measures them). Where this disagrees with the text above, this holds.

1. **Where the server reads `policies:`.** Only from the file given with
   `--config`; without it the config is `{}` (`$P/cli.py:121-129`, `:4395`,
   `:4456-4465`). The managed background server — the one `omnigent claude`
   starts or reuses — is spawned with `--config <global config>` when that
   file exists (`$P/host/local_server.py:836`); the global config is
   `$OMNIGENT_CONFIG_HOME/config.yaml`, else `~/.omnigent/config.yaml`
   (`$P/cli.py:755-762`). A bare foreground `omnigent server` reads no
   policies. A project `.omnigent/config.yaml` never carries policies.
2. **Reload: none; a restart is needed.** Policies are parsed once at start
   into `RuntimeCaps` (`$P/cli.py:4463-4466`). A running background server is
   reused as long as its signature matches, and the signature covers auth
   source, features, title instructions, version and base path — not
   policies (`$P/host/local_server.py:164-205`, `:610-622`). A changed
   `policies:` block takes effect after `omnigent server stop` and the next
   start.
3. **Order and precedence.** Session policies, then agent policies, then
   server defaults (`$P/runtime/policies/builder.py:348-353`, `:452-454`); a
   DENY short-circuits, an ALLOW never overrides a later DENY
   (`$P/policies/types.py:244-252`, `$P/runner/policy.py:275-283`).
4. **The list has to be literal in the expression.** `cel_policy` returns a
   one-argument callable; a policy's `config:` is passed only to two-argument
   callables (`$P/policies/function.py:179-187`), so CEL cannot read a list
   from the YAML. An evaluation error or a non-map result abstains
   (`$P/policies/builtins/cel.py:156-171`).
5. **The event a tool call produces.** `event.type == "tool_call"`,
   `event.data == {"name": …, "arguments": {…}}` on both paths: the native
   hook path (`$P/server/routes/_sessions/helpers.py:8538-8550`) and the
   `/mcp` relay path (`$P/server/routes/_sessions/orchestration.py:10048-10056`).
6. **Which name reaches `event.data.name` for an Omnigent tool** — the bare
   name. Claude Code sends the MCP `tools/call` with the server's own tool
   name; the bridge forwards that name to the relay
   (`$P/harnesses/claude_native/bridge.py:6843-6844`, `:6892-6911`), the
   runner hands it to `ProxyMcpManager.call_tool` (`$P/runner/app.py:8280-8289`),
   which posts it as `params.name` (`$P/runner/proxy_mcp_manager.py:347-357`),
   and the server evaluates that name (`orchestration.py:9918`,
   `:10048-10056`). The server itself also accepts the prefixed form for one
   tool (`orchestration.py:10118`), so a policy matches both spellings.
7. **A path with no Omnigent policy at all.** The bridge executes a tool
   that the relay does not currently advertise locally, without any policy
   (`bridge.py:6843-6857`); its own `sys_os_*` tools are offered "outside an
   active turn" (`bridge.py:6747-6752`) and before the relay starts
   (`$P/runner/app.py:8304-8311`, read by the classification sub-agent), and
   the native hook skips every `mcp__omnigent__*` tool
   (`$P/native/native_policy_hook.py:326-331`). In such a window a
   `sys_os_write` in a Claude Code session passes no Omnigent policy. Only a
   Claude Code rule naming the tool holds there.
8. **The MCP server is called `omnigent`** (`bridge.py:205`, `:2034-2036`),
   so Claude Code names its tools `mcp__omnigent__<tool>`. Omnigent itself
   disallows none of them (`_OMNIGENT_DISALLOWED_TOOLS = ()`, `bridge.py:2455`).
9. **`omnigent claude` loads the project's `.claude/settings.json`.** It adds
   its own `--settings <file>` as a further source (`bridge.py:2543-2553`) and
   passes `--setting-sources ""` only for an agent spec with
   `skills_filter: none` (`$P/inner/bundle_skills.py:80-113`); `omnigent
   claude`'s own spec does not set it. A session under such a spec loads no
   project settings, so layer 1 is absent there.
10. **The tool surface a native harness gets** is `_NATIVE_RELAY_BUILTIN_TOOLS`
    plus the four `sys_os_*` tools (`$P/runner/tool_dispatch.py:443-486`,
    `:515-639`): 44 names. The classification (a read-only sub-agent,
    2026-09-29, every entry with file:line) is in `spec.md`. Timer tools and
    `web_*`, `upload_file`, `download_file`, `list_files`, `nimble_*` never
    reach a native harness (`tool_dispatch.py:458-486`, `:577`). Omnigent's
    "auto-harness" routing pre-approves `sys_session_create`, `sys_agent_list`,
    `sys_session_send`, `sys_read_inbox` for its cross-harness redirect
    (`$P/runner/native/orchestration.py:7144-7156`).
11. **Correction 4 above is corrected.** Claude Code's permissions page
    documents globs in the tool-name position of deny and ask rules
    (`"mcp__*"`); allow rules need a literal `mcp__<server>__` prefix. A bare
    tool name or a matching glob in a deny rule removes the tool from
    Claude's context. Deny rules from any scope beat allow rules from any
    scope, and "Deny rules block in every mode, including
    `bypassPermissions`" (permission-modes page). `mcp__` rules with
    parentheses are skipped.
12. **What `Edit(path)` deny rules reach** (permissions page, "Read and
    Edit", "Redirections"): Claude Code's own file tools, the file commands it
    recognises in Bash (`sed`, `tee`, …) and the targets of `>`/`>>`; not a
    program that opens files itself (a Python or Node script). `Write(path)`
    rules are never consulted. `//` anchors at the filesystem root, `~/` at
    home. So the sentence in `docs/WORKFLOW.md` §3 that a write through `Bash`
    (`echo … >> docs/decisions/x.md`) falls through the path rules is no
    longer true for redirects.
13. **Not established:** whether the relay is always advertised in an
    `omnigent claude --use-native-config` session (item 7), which Claude Code
    version runs here (`claude --version` needed an approval), and whether a
    session label could scope a default policy to one repository (the event
    carries `context.labels`, `$P/policies/function.py:215-250`; which labels a
    native session carries was not read).

