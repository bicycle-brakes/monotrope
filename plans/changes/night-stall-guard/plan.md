---
title: "Plan — night-stall-guard"
status: draft
implementation_status: none
date: 2026-11-09
last_reviewed: 2026-11-09
updated: 2026-11-09
supersedes: null
superseded_by: null
bead: coding-harness-ibde
owner: framework-architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "gpt-6.1-sol, 2026-11-09"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [plan, night-run, permissions, claude-code]
---

# Plan — night-stall-guard

```text
For you:     Night permission requests fail immediately, and merge status reads stop triggering the merge brake.
Done when:   Permission regressions pass, an isolated Claude Code probe confirms refusal without waiting, and make verify is green.
Appetite:    2 hours of phase 4, repairs included; a stop, not an estimate.
Not now:     Phone alerts, independent heartbeat calls, runner supervision or a general command parser.
Pre-mortem:  suppose it failed: most likely because an inherited ask rule still opened a permission prompt.
Starts unless you say stop.
```

Implements `spec.md` and the maintainer's answer of 2026-11-09
(`decisions.md#Q-1`, bead coding-harness-ibde). Class bounded: no design or
ADR. No `templates/plan.md` exists; use `prompts/03-plan.md`. Exploration
used Stage 2, GLM 5.3 Flash through `glm-coding-plan` on 2026-11-09;
no Stage-1 fallback is recorded. `findings.md` has no phase-2a rows as read
on 2026-11-09. Nothing here implements the deferred phone alert.

## Files and steps

1. **Runner, first safeguard:** create
   `tools/claude-code/night-settings.json` as the night settings fragment
   (`permissions.defaultMode: dontAsk`, no asks), and
   `tools/claude-code/night.py` as a standalone Python launcher installed
   beside it. Load user settings under `CLAUDE_CONFIG_DIR` or `~/.claude`,
   then the current Git worktree's `.claude/settings.json` and optional
   `.claude/settings.local.json`; use the working directory as the project
   root outside Git. Read absent optional layers as absent, but fail before
   launch on malformed or unreadable present files. Union all sourced ask
   rules into denies alongside existing denies; do not copy inherited asks
   into the overlay or add blanket allows. Keep inherited non-permission
   settings in their native layers. Write the overlay in a private temporary
   directory and invoke `claude --settings <overlay> --permission-mode dontAsk`
   with the remaining arguments as an argv list, never a shell string. Keep
   the file for the child lifetime and clean up afterwards, forwarding its
   result. Reject caller-supplied settings, permission-mode and permission
   bypass flags (both separated and `--flag=value` forms) rather than let
   them silently replace the profile. Do not rewrite any source setting.
2. Change `tools/claude-code/install.sh` to copy both assets through its
   existing backup/check mechanism; preserve the normal settings merge.
   Create `tests/test_night_profile.py` with synthetic user/project/local
   settings, a temporary home and a fake `claude` executable. Test a newly
   introduced ask in each scope, retained denies/other settings, missing
   optional files, read/parse failures, override flags, child failure,
   temporary-file lifetime, source immutability and install/check behavior.
   Never install into the maintainer's real home during tests.
3. **Runner, second safeguard:** change `scripts/merge_guard.py`, retaining
   `MERGE_ASK_RULES`, `covers()`, `samples()` and `problems()` interfaces used
   by existing callers. Replace the two whole-command `*merge*`/`*Merge*`
   API rules with targeted direct-command patterns for the spec's REST PUT
   endpoint and inline GraphQL mutations `mergePullRequest`,
   `enablePullRequestAutoMerge`, `enqueuePullRequest`. Keep the direct
   `pr merge` forms, MCP merge rule, alias and main-push brakes. Record
   reasons and samples for each rule; keep the day checker rejecting
   allow/deny rules covering day merge samples. Do not apply that day-only
   invariant to the intentional night deny overlay.
4. Change `tests/test_merge_guard.py` to exercise independently written
   positive and negative commands. Include bare/flagged `gh pr merge`,
   all existing repository-flag fixtures, REST `-X PUT` and `--method PUT`
   before/after the endpoint, and all three GraphQL mutation names through
   `-f` and `--raw-field`. Include read queries containing `mergedAt`,
   `mergeable`, `mergeStateStatus`, `isInMergeQueue`, REST GET and
   `gh pr view --json` counterparts. The incident fixture is a query such as
   `query { repository(owner:"o", name:"r") { pullRequest(number:54) { mergedAt isInMergeQueue } } }`.
   Exercise those reads against day asks and night denies, and verify every
   positive becomes a night denial. Replace the hardcoded rule count with
   assertions about required behaviors; retain missing-rule and foreign-rule
   mutation tests and the Omnigent-render preservation test.
5. **Orchestrator bootstrap, after the accepted attempt:** edit the held
   `.claude/settings.json` ask list to exactly the new merge rules, preserving
   unrelated rules, denies and hooks. The runner attempt must not edit or
   commit this file. Before this bootstrap, tests against real settings may
   be red: do not weaken them to accept the stale broad rules. Test proposed
   settings in fixtures during the runner attempt, then the actual tree after
   bootstrap. If the runner's acceptance gate cannot admit that split, return
   the patch and failing evidence to the orchestrator instead of reporting a
   green accepted implementation or editing the held path.
6. Change `tools/claude-code/README.md` to document installation and explicit
   night startup (`python3 ~/.claude/night.py` plus normal Claude arguments),
   invocation-only lifetime, supported settings scopes and refusal failures.
   Change `docs/WORKFLOW.md` only in the merge-brake explanation and night
   setup: describe precise merge matching, the existing text-brake limits,
   immediate refusal and continuing through an authorised alternative or
   parking. Preserve wake/keep-awake and merge-authority rules. Phone alerts
   remain future work with an unchosen service.
7. Update this `plan.md` ledger from not-yet-written to test entries as tests
   land, and append measured evidence and phase-4 time here. Regenerate
   `plans/INDEX.md` with `python3 scripts/plans_registry.py --index` after
   artifact header changes; that derived file is an implementation follow-up,
   not a change to make during this drafting call.

## Verification

First confirm the installed Claude Code accepts the planned settings and
mode options using its local help. Repository documentation of deny/ask/allow
precedence is historical evidence from 2026-09-30, not a live measurement.
If current behavior differs, record the gap and stop before changing the
permission contract; never use `bypassPermissions` as a fallback.

Run the focused suite after the held settings bootstrap:

```bash
.venv/bin/python3 -m pytest -q tests/test_night_profile.py tests/test_merge_guard.py tests/test_omnigent_deny_layers.py
```

Use isolated settings and a harmless sentinel command for a bounded live
Claude Code probe. It must show the child never executes the denied command,
an otherwise unapproved action cannot leave an interactive permission wait,
and a benign merge-field read is not caught by the merge brake. Use a fake
`gh` executable for the read; send no GitHub write. Record exact commands,
Claude Code version, timeout and observed results here. A stub demonstrates
argv/settings construction only; if live behavior cannot be measured, leave
criterion 2 and completion pending explicitly.

Final verification, after all bootstrap edits:

```bash
make verify
```

## Criterion ledger

- 1: not yet written tests/test_night_profile.py::test_inherited_asks_become_denies — a newly added ask in one supported scope is absent from the deny overlay
- 2: not yet written tests/test_night_profile.py::test_launcher_forces_noninteractive_permissions — the launched argv or overlay permits an interactive permission wait
- 2: not a test — the bounded isolated Claude Code probe above observes refusal without execution or a permission wait; missing runtime evidence leaves this pending
- 3: not yet written tests/test_merge_guard.py::test_direct_merge_actions_are_guarded — an independently written merge/auto-merge/enqueue command or MCP merge tool misses every ask rule
- 4: not yet written tests/test_merge_guard.py::test_merge_field_reads_do_not_trigger_the_brake — the incident query or another merge-field read matches a day ask or night deny merge rule
- 5: tests/test_merge_guard.py::test_the_omnigent_render_keeps_the_merge_rules — policy regeneration drops a merge rule or corrupts the day settings
- 5: not yet written tests/test_night_profile.py::test_day_permissions_remain_intact — unrelated asks or denies disappear from the day configuration
- 6: not yet written tests/test_night_profile.py::test_activation_is_scoped_and_refuses_invalid_overrides — a source file changes or an invalid/conflicting invocation starts Claude Code
- 7: not yet written tests/test_night_profile.py::test_install_backup_and_check_cover_night_assets — install omits an asset, overwrites without backup or check misses drift/writes files
- 8: not a test — phase-6 review compares both documentation changes with the explicit launch command, authorised-alternative/park response and deferred-alert non-goal; contrary instructions refute it

## Do not touch

No runner, scheduler, heartbeat state, hooks, status line, tracker storage,
models, gate/provenance configuration, ADR, prompt, template or agent-rule
changes. No edits to the installed user setup during implementation tests.
The only held implementation path is `.claude/settings.json`, owned by the
orchestrator as step 5 states; ordinary tool files under `tools/claude-code/`
are runner work. No design, ADR or phone-provider answer is manufactured.

## Draft validation — 2026-11-09

At base commit `e6ce9677`, with these uncommitted drafting artifacts:
`check_interview_minimums.py --change night-stall-guard` passed;
`check_criterion_ledger.py` passed; and
`check_research_handoff.py --change night-stall-guard` reported exemption
because no research-swarm/v2 evidence applies. `git diff --check` passed.
The one counted maintainer answer was also checked before drafting.

`plans_registry.py --check` exited 2: tracker rendering could not acquire
the shared database lock in this sandbox, and `plans/INDEX.md` still needs
regeneration by the orchestrator/runner outside this call's allowed edits.
These are not passing checks. The named
`scripts/validate_change_artefacts.py` does not exist in this tree.
`make verify`, implementation tests and the live Claude Code probe were
not run in phase 2/3; the runner owns full verification and the commit.

## Time used
