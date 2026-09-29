---
title: "Findings — omnigent-deny-layers"
category: findings
created: 2026-09-29
updated: 2026-09-29
status: draft
implementation_status: partial
date: 2026-09-29
last_reviewed: 2026-09-29
supersedes: null
superseded_by: null
bead: coding-harness-rex
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: claude-code, version: "2026-09-29"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, omnigent, permissions, policy]
---

# Findings — omnigent-deny-layers

Phase 6, round 1, on commit `6e311af` (branch `feat/omnigent-deny-layers`,
seven commits over `origin/main`), 2026-09-29. The reviewer ran in a fresh
context, wrote nothing but this file, and never started, stopped or called
Omnigent. Measured against `spec.md` (criteria 1–8, non-goals) and the
maintainer's answers in `decisions.md`; the plan's "Implementation notes" were
read for the two departures, not as the yardstick.

**Verdict: no BLOCKER, no MAJOR, no `[AMBIGUITY]`, no `[DIVERGENT]`.** Seven
MINOR findings, all open; none stops a pull request.

Repair round 1 (origin fix-r1): five of the seven are fixed (F-2, F-3, F-4,
F-6, F-7; the commit is in each Status). F-1 and F-5 stay open, each with its
reason in the Status.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | MINOR | SPEC | base | `scripts/omnigent_policy.py`, `ALLOWED_TOOLS["sys_advise_models"]`; `spec.md`, table "Allowed (17)" | The spec allows `sys_advise_models` on its docstring and says its body was not read. The body is now read (Omnigent 0.15.0, `server/routes/_sessions/helpers.py`, `_handle_advise_models_mcp`): it changes no file, session or record, but when a routing backend is configured it sends the caller's task text to that judge (`routing_client.route(task_text, harness_models)`); without one it answers `router_on: false` and nothing leaves. The spec's rule denies a tool that reaches an outside service, and it denied the hindsight tools for sending session content out. Whether a routing judge counts as such a service is the maintainer's call; on this machine no routing backend is configured (research, "What was measured"), so today the tool sends nothing. Recorded as a disagreement with the table, not resolved. The two "body was not read" caveats (spec table, list reason) can now carry this reading instead. [criterion 2, "a misclassified tool is refuted by review"] | open — the classification of a tool that may send task text to a routing judge is the maintainer's call; the list is unchanged |
| F-2 | MINOR | MAINT | base | `scripts/omnigent_policy.py`, `_is_owned_rule` and `write` | Every deny rule that starts with `Edit(//**` counts as owned. A rule the maintainer adds by hand in that form for another path (say `Edit(//**/secrets/**)`) is dropped silently by the next `--write`, and `check()` never reports the loss, because it only looks for the rules the list wants and for Omnigent rules it does not want. Today no such rule exists, and the idempotence test proves the point only for a `Bash(…)` rule. The spec says the rewrite keeps every entry it does not own; the plan defines "own" wider than the one rule the list renders. | fixed in 2652fd5 |
| F-3 | MINOR | MAINT | base | `tools/omnigent/install.sh`, the `py=` resolution; `scripts/omnigent_policy.py`, `omnigent_python` | Two resolvers answer "which interpreter is Omnigent's" differently. The installer takes the launcher's shebang text literally after `#!`, so `#!/usr/bin/env python3` is rejected as not executable ("Omnigent not found") and an interpreter path with a space is cut at the space; the module handles the `env` form and quoting. Today's launcher (`~/.local/bin/omnigent`, read 2026-09-29) names the uv environment's Python directly, so both agree on this machine. The installer's tests cover only the direct form and the missing form. | fixed in 9fcf3c2 |
| F-4 | MINOR | MAINT | base | `scripts/omnigent_policy.py`, `merge_config` with `remove=True` | Removal validates what remains: the foreign policies go through Omnigent's parser before the owned ones are taken out. A foreign policy the parser rejects (an unknown `type:`, a malformed block a later Omnigent no longer accepts) therefore blocks `install.sh --remove` with "nothing written", the one moment the maintainer wants the owned policies gone. The way out is the backup or a hand edit, and the message names neither. The spec asks validation of the merge; it is silent on removal. | fixed in 3f60919 |
| F-5 | MINOR | SPEC | base | `.claude/settings.json`, the rule `Edit(//**/.omnigent/config.yaml)`; `spec.md`, criterion 8 (a) | The second half of layer 1 is never measured. Criterion 8 (a) probes `sys_os_write` and `sys_os_read` only; the `Edit(//**…)` rule rests on the documented syntax (research addendum 12) and on no test that can tell a matching glob from one Claude Code ignores. Layer 2's mirror of the same suffix is measured offline (criterion 5), so the rule that must hold *alone* in this repository (ADR 0006) is the one without a measurement. Not a fault of the build; recorded so the live-measurement session can add one `Write` probe to `<worktree>/.omnigent/config.yaml`. | open — the live probe of the Edit rule belongs to the live measurement after the merge (bead coding-harness-671) |
| F-6 | MINOR | MAINT | base | `docs/WORKFLOW.md`, note "Not all of it is here yet"; §3 "What isolation consists of here", item 3 | The note lists "the brakes on the irreversible that §3 names for `.claude/settings.json`" among the pieces that are *not here yet*, which reads as pending migration; §3 item 3, the spec's non-goals and its decided `[DETAIL]` say the brakes stay out by decision (this repository deploys nothing, the next spelling passes a `Bash` pattern). Both say the brakes are absent, so this is not `[DIVERGENT]`; but the note's frame and §3's reasoning point in different directions, and §3 no longer "names" the brakes as being in the file. The plan's S6 prescribed this wording; the implementation followed it. [criterion 7] | fixed in 1962a4c |
| F-7 | MINOR | MAINT | base | `scripts/kit/probe.py`, `DECKEL` | The trailing comment on the `DECKEL = 32` line still explains the raise of 2026-09-20 to 31 ("die 7 neuen Faelle …"); the block comment above it explains the raise to 32 of 2026-09-29. A reader of the line alone gets the earlier reason for the current number. Departure 3 of the implementation notes is otherwise as described: the cap rose by exactly the one case the new `OHNE_AUFRUFER` entry adds, with its reason beside it. | fixed in 54e4c9c |

## Checked without a finding

- **Criterion 1, one list.** The tool names are typed once, in
  `scripts/omnigent_policy.py`; `.claude/settings.json`, `tools/omnigent/policy.yaml`
  and every test read or render from it (`check()` compares the tree to the
  render; `test_every_name_is_listed_once_with_a_reason` refuses a name in both
  lists or an empty reason). `--check` on `6e311af`: "the tree is what the list
  renders".
- **Criterion 2, the surface.** `--surface` under Omnigent 0.15.0's interpreter
  returns the 44 names of `_NATIVE_RELAY_BUILTIN_TOOLS` plus the four `sys_os_*`
  tools; the test passes here and skips with a stated reason without Omnigent.
  Read against the installed source: `_TERMINAL_TOOLS`, `_ASYNC_INBOX_TOOLS`,
  `_SESSION_QUERY_TOOLS`, `_AGENT_TOOLS`, `_POLICY_TOOLS`, `_SCHEDULED_TASK_TOOLS`,
  `BROWSER_TOOL_NAMES`, `_HINDSIGHT_TOOLS`, `_SKILL_TOOLS`, `_COMMENT_TOOLS`. Every
  tool that writes a file, runs a command, starts, messages, closes, retitles or
  shares a session, touches a scheduled job, runs or cancels background work,
  drains the inbox (which writes a delivery receipt), adds a policy, changes a
  comment, acts on a live page or sends content to the memory service is denied;
  no read-only tool is (F-1 is the one judgment left to the maintainer).
- **Criterion 3, layer 1 alone.** The 27 `mcp__omnigent__<tool>` rules and the
  `Edit(//**/.omnigent/config.yaml)` rule are in `.claude/settings.json`; no
  blanket rule; the diff adds only the `permissions` block, the `SessionStart`
  hook is byte-identical. `check()` flags an allowed tool, `mcp__omnigent`,
  `mcp__omnigent__*`, `mcp__*` and `*` (planted in a temporary tree by
  `test_check_names_an_allowed_tool_or_a_blanket_rule_in_the_settings`).
- **Criterion 4.** `policy.yaml` has one top-level key and the two `type: function`
  policies on `omnigent.policies.builtins.cel.cel_policy`; its text equals the
  render. Omnigent's `spec/parser.py` (`_parse_function_policy`) reads
  `handler:` and a sibling `factory_params:` — the shape the server loads from
  `--config` is the shape committed.
- **Criterion 5, measured with Omnigent's code.** Under Omnigent's interpreter
  the offline tests deny every denied tool in both spellings, with and without
  arguments, name the tool in the reason, leave every allowed tool alone, deny
  `Write`, `Edit` and `MultiEdit` on a path ending in `/.omnigent/config.yaml`
  and nothing else, and raise no evaluation error on 23 odd event shapes. The
  fail-open class is real: `cel_policy` abstains on `CELEvalError`, and a
  condition that evaluates to an error makes the ternary itself raise. Server
  defaults are appended to the evaluation order (`runtime/policies/builder.py`,
  `admin_policy_specs`), and the relay path evaluates the bare tool name, so
  the two spellings cover what reaches `event.data.name`.
- **Planted faults, in a temporary copy of the tree (removed after):** dropping
  `sys_session_share` from the list turned `test_the_list_matches_omnigents_native_surface`
  red ("Omnigent offers tools this list does not classify"); dropping the
  `has(event.data.name) && type(event.data.name) == string` guard turned
  `test_no_event_shape_raises_an_evaluation_error` red with a `CELEvalError` on
  `{"type": "tool_call", "data": {}}`. The implementation notes' own mutation
  table was not re-run.
- **The evaluation-time departure.** The `in [...]` form over 54 literal names
  replaces the plan's `.exists(...)`; the whole odd-event run takes under three
  seconds here, and the test's 120 s subprocess limit turns a regression to the
  hanging form into a failure, not a hang.
- **Criterion 6, the installer, against a temporary HOME only.** The end-to-end
  test runs `install.sh` with a pseudo-terminal, `HOME` and `OMNIGENT_CONFIG_HOME`
  under `tmp_path`, and asserts the target lies there: `--check` red before,
  install, `--check` green, a rerun makes no backup and changes nothing,
  `--remove`, `--check` red again. The merge tests prove foreign keys and
  policies kept, owned policies replaced as a set, a backup before a change and
  none on a rerun, a rejected validation leaving the file and no backup, a
  config that is not a mapping refused. Without a terminal, install and remove
  exit 2 and create nothing. The real `~/.omnigent` was not touched by this
  review and, per the implementation notes, not by the build.
- **ADR 0006.** Nothing in the tree, the tests or the gates needs layer 2 to be
  installed; `check()` and the settings tests read only the repository. The
  texts say layer 2 is a second layer the maintainer installs and nothing
  depends on it alone.
- **Departure 3 (`ci_gates.OHNE_AUFRUFER`, the kit probe).** The reason names
  the test that runs the script and the installer that calls it; the probe
  entry is the one case the entry adds, with the cap raised by one and the
  reason beside it (F-7 is the stale trailing comment).
- **Criterion 7, the texts.** `docs/WORKFLOW.md` §3 item 5 and item 3 and the
  `AGENTS.md` bullet name the rule, the list, the second layer, the absent
  brakes, what `Edit(…)` reaches and the bridge-local window; no sentence names
  a deny rule the file does not have, says a `Bash` redirect falls through
  `Edit` rules, or says Omnigent's tools pass `permissions.deny` unseen.
  `AGENTS.md` has 167 lines and no word README (`tests/test_entry_points.py`
  green in `make verify`). F-6 is the one frame left to the maintainer.
- **Non-goals.** No port to a sibling repository, no D-60 guard, no gates.yaml
  entry, no change to Omnigent, no `Read` deny, no sandbox.
- **Suite.** `python3 -m pytest tests/test_omnigent_deny_layers.py -q -rs`:
  28 passed, 0 skipped (Omnigent installed). `make verify` on `6e311af`:
  VERIFY GREEN; `docs-links` and `markdownlint` report-only reds are in files
  this change does not touch (`tools/claude-code/README.md`).

## For phase 7

This file is a new artefact under `plans/changes/`, so `plans/INDEX.md` is
stale until `python3 scripts/plans_registry.py --index` runs; the reviewer did
not run it (nothing but this file was to be written). Criterion 8 (a) stays
open by design until the live measurement after the merge; part (b) is bead
coding-harness-671.
