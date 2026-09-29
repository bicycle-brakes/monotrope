---
title: "Plan — omnigent-deny-layers"
status: draft
implementation_status: none
date: 2026-09-29
last_reviewed: 2026-09-29
supersedes: null
superseded_by: null
bead: coding-harness-rex
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, omnigent, permissions, policy]
---

# Plan — omnigent-deny-layers

Implements `spec.md` (criteria 1–8). Stage 1: no model markings. Every new
file is English (house rule 1).

## S0 · Precondition

Pull request 49 (English `docs/WORKFLOW.md`, `AGENTS.md`) must be merged:
the text edits in S6 are written against its wording. Start with
`git fetch origin && git rebase origin/main`. If 49 is still open, do S1–S5,
stop before S6 and report.

## Files

**Created**

- `scripts/omnigent_policy.py` — the one list and everything derived from it
  (criteria 1–6):
  - `DENIED_TOOLS`, `ALLOWED_TOOLS`: `dict[str, str]`, tool → one-line reason,
    exactly the 27 and 17 names of the spec's tables, grouped as there;
    `PROTECTED_PATHS = {"/.omnigent/config.yaml": "…carries the Omnigent
    default policy (layer 2)"}`; `HARNESS_FILE_TOOLS = ("Write", "Edit",
    "MultiEdit")`; `OWNED_PREFIX = "coding_harness__"`.
  - `layer1_rules()` → `["mcp__omnigent__<tool>" …] + ["Edit(//**<suffix>)" …]`.
  - `render_policy_yaml()` → the text of `tools/omnigent/policy.yaml`: a
    four-line `#` header (generated, do not edit, installed by
    `tools/omnigent/install.sh`), then `policies:` with the two policies
    below, `type: function`, `handler:
    omnigent.policies.builtins.cel.cel_policy`, `factory_params:` with a
    short fallback `reason:` and `expression: |-` as a literal block, one list
    element per line, no trailing comma.
  - `coding_harness__omnigent_writing_tools`:
    `has(event.type) && event.type == "tool_call" && type(event.data) == map
    && has(event.data.name) && type(event.data.name) == string && [<denied,
    one per line>].exists(t, event.data.name == t || event.data.name ==
    "mcp__omnigent__" + t) ? {"result": "DENY", "reason": "coding-harness:
    Omnigent's " + event.data.name + " writes, runs, spawns or changes state
    outside Claude Code's permission rules — use the harness's own tools
    (list: scripts/omnigent_policy.py)"} : null`.
  - `coding_harness__protected_paths`: the same four guards, then
    `event.data.name in [<HARNESS_FILE_TOOLS>] && has(event.data.arguments)
    && type(event.data.arguments) == map && has(event.data.arguments.file_path)
    && type(event.data.arguments.file_path) == string && [<suffixes>].exists(p,
    event.data.arguments.file_path.endsWith(p)) ? {"result": "DENY",
    "reason": "coding-harness: " + event.data.arguments.file_path + " carries
    Omnigent's policy; only the maintainer changes it
    (tools/omnigent/install.sh)"} : null`. The `type(…) == …` guards are not
    measured against Omnigent's `celpy` (research addendum, preamble); if the
    offline tests show them unsupported, drop them and keep the `has()`
    guards — the no-error test decides.
  - `check()` → list of problems: `policy.yaml` differs from the render;
    `.claude/settings.json` lacks a `layer1_rules()` entry, has another
    `mcp__omnigent__*` entry, or has `mcp__omnigent`, `mcp__*` or `*`.
  - `write()` → rewrites `policy.yaml`; in `.claude/settings.json` keeps every
    `permissions.deny` entry it does not own (owned: `mcp__omnigent__*` and
    the `Edit(//**…)` rules) in its order, appends `layer1_rules()`, dumps
    `json.dumps(…, indent=2, sort_keys=True) + "\n"` (the hooks come out
    byte-identical).
  - `merge_config(path, policies=None, *, remove=False, validate=True)` →
    `"created" | "merged" | "removed" | "unchanged"`. Loads the YAML (absent →
    `{}`; not a mapping, or `policies:` neither mapping nor null → error,
    nothing written); drops every `coding_harness__*` policy, adds the file's
    (unless `remove`), keeps key order; unchanged → return without writing;
    else `validate` (import `omnigent.spec.parse_default_policies` and
    `cel_policy`, parse the whole `policies:` block with `expand_env=False` —
    a foreign policy the server could not boot with fails it too — and
    compile each owned expression; failure raises, nothing written), copy the
    old file to
    `config.yaml.bak-<YYYYmmdd-HHMMSS>`, write `<path>.tmp` with
    `yaml.safe_dump(sort_keys=False)` and rename.
  - `omnigent_python()` → `$OMNIGENT_PYTHON`, else the `#!` interpreter of
    `shutil.which("omnigent")` resolved through symlinks, if executable;
    else `None`.
  - CLI: `--check` (default; problems + "run: python3
    scripts/omnigent_policy.py --write", exit 1), `--write`, `--merge-config
    PATH [--remove]` (prints the status, the backup path, that comments are
    not carried over, and the restart advice below; validation failure exit
    1), `--installed PATH` (exit 0 if the owned policies there equal the
    file's, else 1 naming the difference), and two modes run only under
    Omnigent's interpreter: `--surface` (JSON sorted names of
    `omnigent.runner.tool_dispatch._NATIVE_RELAY_BUILTIN_TOOLS` plus
    `SysOs{Read,Write,Edit,Shell}Tool.name()`) and `--evaluate` (JSON events
    on stdin → per event and policy: the `cel_policy` result, and any
    exception `celpy` raises evaluating the raw expression).
  - Restart advice after a change: "Omnigent reads `policies:` only when its
    server starts, and a running background server is reused. If one runs,
    stop it with `omnigent server stop` (its sessions end); the next
    `omnigent claude` starts it with this policy. A foreground `omnigent
    server` reads it only with `--config <path>`." After no change: "no
    restart needed".
- `tools/omnigent/policy.yaml` — generated by `--write`; never edited by hand.
- `tools/omnigent/install.sh` — `install.sh` | `--check` | `--remove`. First,
  for install and remove: `[ -t 0 ]` or exit 2 ("run this yourself in a
  terminal — not from an agent or CI"). Then the interpreter:
  `$OMNIGENT_PYTHON`, else the first line of the resolved `omnigent`
  launcher without `#!`; missing → exit 2 ("Omnigent not found"). Target:
  `${OMNIGENT_CONFIG_HOME:-$HOME/.omnigent}/config.yaml`. `--check` runs
  `--installed`; the others run `--merge-config [--remove]`. `set -euo
  pipefail`, header comment in the style of `tools/claude-code/install.sh`.
- `tools/omnigent/README.md` — under 40 lines: what layer 2 is and is not
  (per machine, second layer, the bridge-local window, harnesses without a
  hook), install / check / remove, the restart, where the list lives and how
  to change it (edit the list, `--write`, reinstall).
- `tests/test_omnigent_deny_layers.py` — the tests below.
- `docs/research/<date>-omnigent-deny-layers-live-measurement.md` — only in
  S9, after installation.

**Changed**

- `.claude/settings.json` — `permissions.deny` from `--write`; hooks unchanged.
- `docs/WORKFLOW.md`, `AGENTS.md` — S6.
- `plans/changes/omnigent-deny-layers/{spec,plan}.md` — frontmatter in S7.
- `plans/INDEX.md` — regenerated in S7.

## Steps

- **S1** Write `scripts/omnigent_policy.py`.
- **S2** `python3 scripts/omnigent_policy.py --write`, then `--check` → exit 0.
- **S3** Write `tools/omnigent/install.sh` (`chmod +x`) and the README.
- **S4** Write the tests. Where Omnigent is installed, run the file once with
  `-rs` and confirm nothing skipped.
- **S5** Mutation proof, reverted after: drop one denied tool's rule from
  `.claude/settings.json` (criterion 3 test red); drop one name from the CEL
  list in `policy.yaml` (criteria 4 and 5 red); move the `has(event.data.name)`
  guard behind the list test (no-error test red, if guards are kept).
  Record the outcomes in the pull request body.
- **S6** Text edits, against PR 49's wording:
  - `docs/WORKFLOW.md`, note "Not all of it is here yet": replace "any
    `permissions.deny` in `.claude/settings.json`," with "the brakes on the
    irreversible that §3 names for `.claude/settings.json` (it holds only the
    Omnigent rules),".
  - §3 "Worktrees" item 5: replace the two sentences from "Omnigent's own
    tools —" to "they are not used to write." with: Omnigent's own tools
    reach the session as `mcp__omnigent__<tool>`, and neither Claude Code's
    path rules, the hooks on its file tools nor Omnigent's own Claude Code
    hook see what they do; each one that writes, runs, spawns or changes
    state is denied by name in `.claude/settings.json`, the read-only ones
    stay usable; the one list, a reason per tool, is
    `scripts/omnigent_policy.py`; an Omnigent default policy from the same
    list (`tools/omnigent/`) refuses them server-side for every Omnigent
    session on the machine, installed by the maintainer, and nothing here
    depends on it alone (ADR 0006) — Omnigent's bridge runs its own
    `sys_os_*` tools without any policy while its relay does not advertise
    them, and there only the rule in `.claude/settings.json` holds. Keep the
    "Not yet measured" sentence.
  - "What isolation consists of here", item 3: it holds two things —
    Omnigent's writing tools (see item 5 above) and
    `Edit(//**/.omnigent/config.yaml)`, so no session rewrites the policy
    that holds it; the template's brakes on the irreversible (production
    deploy, `bundle destroy`, force push, `rm -rf`, writes under
    `docs/decisions/`) are not in it — this repository deploys nothing, has
    no `docs/decisions/`, and a `Bash` pattern for a force push is passed by
    the next spelling; deny survives every permission mode,
    `bypassPermissions` included; an `Edit(…)` rule reaches Claude Code's
    file tools, the file commands it recognises in `Bash` (`sed`, `tee`) and
    redirect targets (`>`, `>>`), not a program that opens files itself
    (`python -c …`) and not a tool Claude Code does not own — which is why
    Omnigent's tools are denied by name. Keep the closing "brake against
    accidents, not a lock" sentence.
  - `AGENTS.md`, bullet "Omnigent starts inside the worktree": replace its
    second sentence with: Omnigent's own tools that write, run, spawn or
    change state are denied by name in `.claude/settings.json`, read-only
    ones stay usable; the one list is `scripts/omnigent_policy.py`; the
    Omnigent default policy from the same list (`tools/omnigent/`) is a
    second layer the maintainer installs, and nothing depends on it alone.
    Keep the pointer to `docs/WORKFLOW.md` §3. Never write the word README
    there; stay under 200 lines.
- **S7** Set `implementation_status: partial` in `spec.md` and `plan.md`
  (built, live measurement open); `python3 scripts/plans_registry.py --index`.
- **S8** Verification (below), then the pull request. Its body names bead
  coding-harness-rex and the open [DECISION] of the spec.
- **S9** After the merge, maintainer and one session, not CI — the live
  measurement below.

## Verification command

```
python3 scripts/omnigent_policy.py --check
python3 -m pytest tests/test_omnigent_deny_layers.py -v -rs
bash scripts/verify_all.sh
```

Locally, with Omnigent installed, the test file skips nothing. In CI the
Omnigent tests skip and say why; that is expected, not green evidence for
criteria 2 and 5.

## Test per criterion

| Criterion | Test | Fault that turns it red |
|---|---|---|
| 1 | `test_every_name_is_listed_once_with_a_reason` | a name in both lists; an empty reason |
| 1, 4 | `test_the_tree_is_what_the_list_renders` (`check() == []`) | `policy.yaml` or the settings' Omnigent rules edited by hand, or the list changed without `--write` |
| 2 | `test_the_list_matches_omnigents_native_surface` · Omnigent | Omnigent adds or drops a tool; a typo in a name |
| 3 | `test_settings_deny_every_denied_tool` | one `mcp__omnigent__<tool>` rule or the `Edit(//**…)` rule missing |
| 3 | `test_settings_deny_no_allowed_tool_and_no_blanket_rule` | `mcp__omnigent__sys_os_read`, `mcp__omnigent__*`, `mcp__omnigent`, `mcp__*` or `*` added |
| 3 | `test_settings_keep_the_session_start_hook` | `--write` drops or rewrites the `tools/bd prime` hook |
| 4 | `test_policy_file_has_only_the_two_owned_policies` | another top-level key; a third policy; wrong handler |
| 5 | `test_policy_denies_denied_tools_and_leaves_allowed_ones` · Omnigent | a name missing from the CEL list; the prefixed form not matched; `arguments` read before the name test |
| 5 | `test_policy_protects_omnigents_config_file` · Omnigent | wrong suffix or tool names; another path denied |
| 5 | `test_no_event_shape_raises_an_evaluation_error` · Omnigent | a field read without its guard |
| 6 | `test_merge_keeps_foreign_keys_and_policies` | a foreign key or policy lost |
| 6 | `test_merge_replaces_owned_policies_as_a_set` | a stale `coding_harness__*` policy kept, or one doubled |
| 6 | `test_merge_backs_up_before_a_change_and_not_on_a_rerun` | no backup, or a backup on an unchanged run |
| 6 | `test_remove_takes_out_only_owned_policies` | a foreign policy removed |
| 6 | `test_installed_check_tells_match_from_drift` | `--installed` passes a tampered config |
| 6 | `test_merge_writes_nothing_omnigent_rejects` · Omnigent | validation skipped or run after the write |
| 6 | `test_installer_refuses_without_a_terminal` | the `[ -t 0 ]` guard removed (run with stdin from `/dev/null`, `HOME` and `OMNIGENT_CONFIG_HOME` in `tmp_path`: exit 2, no file) |
| 7 | review in phase 6; `tests/test_entry_points.py` for `AGENTS.md` | — |
| 8 | S9, by the maintainer | — |

"· Omnigent" tests get the interpreter from `omnigent_python()` and run
`--surface` or `--evaluate` in a subprocess with `OMNIGENT_CONFIG_HOME` and
`OMNIGENT_DATA_DIR` in `tmp_path`. No interpreter → `pytest.skip("Omnigent is
not installed here (no OMNIGENT_PYTHON, no omnigent on PATH) — the policy was
not evaluated with Omnigent's code")`; an interpreter that cannot import
`omnigent.spec` and `omnigent.policies.builtins.cel` → skip naming it and the
import error. The merge tests call `merge_config(…, validate=False)` directly;
PyYAML is in CI.

## S9 · Live measurement (maintainer; not in CI)

1. In a terminal, in the main checkout at the merge commit:
   `tools/omnigent/install.sh` → "merged …", restart advice.
2. When no Omnigent session is working: `omnigent server stop`.
3. `tools/omnigent/install.sh --check` → the installed policies match.
4. Layer 1: `cd ~/coding-harness && omnigent claude --use-native-config`.
   Ask: "Read AGENTS.md with mcp__omnigent__sys_os_read, then write the word
   probe to deny-probe.txt here with mcp__omnigent__sys_os_write." **Pass:**
   the read answers; the write is not offered or is refused; afterwards
   `test ! -e ~/coding-harness/deny-probe.txt`.
5. Layer 2: `mkdir -p /tmp/omnigent-deny-probe && cd /tmp/omnigent-deny-probe
   && omnigent claude --use-native-config`. Ask (a) "Rename this session to
   deny probe with mcp__omnigent__sys_session_rename" — **pass:** "Denied by
   policy" with the writing-tools reason, the title unchanged; (b) "Write x to
   /tmp/omnigent-deny-probe/.omnigent/config.yaml with your Write tool" —
   **pass:** refused with the protected-paths reason, and `test ! -e
   /tmp/omnigent-deny-probe/.omnigent/config.yaml`; (c) recorded only: "Write
   x to /tmp/omnigent-deny-probe/probe.txt with mcp__omnigent__sys_os_write"
   — refused or written, and whether `probe.txt` exists.
6. A session writes `docs/research/<date>-omnigent-deny-layers-live-measurement.md`
   (frontmatter like the other files there): date, commit, `omnigent
   --version`, `claude --version`, the text each step returned, pass or fail
   per step. Pull request; then `implementation_status: done`, archive the
   folder, and the tracker writer closes the bead.

With option 2 of the spec's [DECISION], only steps 4 and 6 run now.

## Not touched

`decisions/gates.yaml` and `.github/workflows/ci.yml` (the tests run in the
existing `pytest` gate); `scripts/kit/manifest.yaml` (the catch-alls
`scripts/`, `tools/`, `tests/` classify the new files); `tools/claude-code/`;
`~/.omnigent/config.yaml` and `~/.claude/settings.json` (the maintainer's,
through the installer); ADR 0006; the tracker; `lakeswitch-ai` and
`portfolio-agentic-engineering`; Omnigent itself.
