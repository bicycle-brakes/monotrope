---
title: "Spec — night-stall-guard"
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
tags: [spec, night-run, permissions, claude-code]
class: bounded
appetite: 2
adr_files: []
neighbours: []
---

# Spec — night-stall-guard

Prevent permission questions from holding an unattended Claude Code night run,
and keep merge reads separate from merge actions (bead coding-harness-ibde).
Research: `research.md`. Maintainer scope: `decisions.md#Q-1`, answered
2026-11-09. This slice delivers the first two safeguards in that answer;
the phone alert returns afterwards with its own provider decision.

## Problem

- The maintainer's incident record in `decisions.md#Q-1` dates a permission
  wait from 22:26 UTC on 2026-11-08 to 06:04 UTC on 2026-11-09. A read-only
  GraphQL query containing `mergedAt` and `isInMergeQueue` matched the merge
  brake. Wakes and completion notices queued behind the question.
- At `e6ce9677`, `.claude/settings.json` contains
  `Bash(gh api *merge*)` and `Bash(gh api *Merge*)`.
  `scripts/merge_guard.py` explicitly documents that reads also prompt.
  The research addendum of 2026-11-09 confirms this against the tree.
- The exploration describes time-based lane supervision, not a remedy for
  a chat blocked on permission. More wakes in that same chat cannot clear
  the prompt; the maintainer chose immediate refusal first.

## Terms

- **Night profile:** explicitly selected Claude Code settings for unattended
  operation; a refused action returns control without waiting for a person.
- **Merge action:** a direct `gh pr merge` invocation, a REST request that
  writes the pull-request merge endpoint, or an inline GraphQL mutation
  `mergePullRequest`, `enablePullRequestAutoMerge` or `enqueuePullRequest`.
- **Merge brake:** the existing text-based permission rules, within the
  supported command forms described under Boundary, plus the existing
  GitHub MCP merge-tool rule.

## Acceptance criteria

1. When the night profile is prepared, every explicit ask rule read from the
   supported user, project and local settings is also an effective deny rule.
   *Refuted by:* a fixture adds an ask rule in any of those scopes and the
   resulting night settings omit its denial.
   *Basis:* `decisions.md#Q-1`.

2. While the night profile is active, an action requiring permission is
   refused without opening an interactive approval wait.
   *Refuted by:* a denied test action reaches its executor, or an otherwise
   unapproved action opens a permission prompt in the isolated runtime probe.
   *Basis:* `decisions.md#Q-1`.

3. When a supported merge action is requested in the day profile, the merge
   brake asks before that action can execute.
   *Refuted by:* the independent command matrix contains a direct merge,
   REST merge write, named GraphQL merge/auto-merge/enqueue mutation or
   existing MCP merge tool that no ask rule covers.
   *Basis:* `decisions.md#Q-1`.

4. When a supported read-only status query contains merge field names, the
   merge brake neither asks nor denies because of those names.
   *Refuted by:* `mergedAt`, `mergeable`, `mergeStateStatus` or
   `isInMergeQueue` in a GraphQL or `gh pr view` read matches a merge rule,
   including the incident query shape and a night invocation.
   *Basis:* `decisions.md#Q-1`.

5. When the merge rules are narrowed, unrelated permissions retain their
   existing day behavior.
   *Refuted by:* the Codex, Omnigent, alias-definition or main-push brake
   disappears, or an existing denial is relaxed to permit a read.
   *Basis:* `decisions.md#Q-1`; existing rules at `e6ce9677`.

6. When the maintainer starts the night profile, its selection applies only
   to that invocation and cannot be silently overridden by conflicting
   launcher arguments or unreadable settings.
   *Refuted by:* starting or ending it changes the day settings, a conflicting
   permission-mode/settings argument restores prompting, or preparation
   launches Claude Code despite a settings parse/read failure.
   *Basis:* `decisions.md#Q-1`.

7. When the Claude Code tooling is installed or checked, the night entry
   point and profile participate in its existing copy, backup and drift checks.
   *Refuted by:* an install omits either asset, a replacement loses its
   previous contents, or `--check` misses their drift or writes files.
   *Basis:* `decisions.md#Q-1`; `tools/claude-code/install.sh` at `e6ce9677`.

8. When unattended operation is documented, the instructions give the night
   start command and direct the orchestrator to continue with an authorised
   alternative or park the denied action.
   *Refuted by:* the documented start still uses day permissions, a denial
   is answered by disabling the brake, or the documentation claims a phone
   alert or independent heartbeat service already exists.
   *Basis:* `decisions.md#Q-1`.

## Non-goals

- The phone alert, permission-prompt monitoring and missing-heartbeat alert:
  return after these safeguards, when the maintainer chooses the push service.
- A scheduler, daemon, headless heartbeat architecture, automatic restart,
  lane planner, runner process watchdog, dashboard or notification service.
- Changing merge authority, approving a merge, bypassing another permission
  system, or changing permissions of Codex, Pi or Omnigent itself.
- Implementing the response to a denied call in `scripts/stage2.py`.
- Phase 2b and an ADR: this bounded change configures the existing permission
  boundary without changing the architecture, as the answered interview states.

## Boundary

The merge brake remains the documented accident brake, not a security lock.
Supported forms are literal direct `gh` commands: existing repository-flag
placements for `pr merge`, REST `repos/<owner>/<repo>/pulls/<number>/merge`
with an explicit PUT method, and inline GraphQL mutation text passed with
`-f query=…` or `--raw-field query=…`; protect bare `gh pr merge` too.
Read counterparts with the same flags must remain outside the merge rules.
The command matrix, not a promise to parse every shell or GraphQL program,
defines the exercised spellings.

Existing bypasses such as `curl`, shell wrappers, aliases, absolute executable
paths, file-supplied GraphQL and arbitrary flag reordering remain outside this
text brake. No claim is made that all merge routes are closed. The night
profile denies sourced explicit ask rules and uses non-interactive permission
handling for other unapproved calls; external policy, authentication dialogs
and a stopped or usage-limited session are outside its control. A local stub
is not evidence of actual Claude Code prompt behavior.

## Protected areas

- Runner, swarm, verify-lock and lane-state machinery: outside this incident's
  permission boundary.
- Tracker storage, model endpoints, gate definitions, provenance, ADRs, prompts,
  templates and agent instructions: no policy or workflow redesign is needed.
- Installed user files: implementation tests use isolated homes; actual
  installation is a later orchestrator operation, not a test side effect.

## Definition of Done

- `make verify` is green after the orchestrator's held-path edit.
- The same pull request updates `tools/claude-code/README.md` and
  `docs/WORKFLOW.md`, the permission rules and their tests; no ADR changes.
- An isolated Claude Code probe records its version, invocation and observed
  refusal/no-wait result without sending a real merge or changing user settings;
  unavailable runtime evidence is reported as not measured, not passed.
- Protected areas stay untouched and non-goals unbuilt in the file list.
- The pull request closes the night-stall prevention work item and carries
  `Closes-Bead: coding-harness-ibde` on its last commit; the deferred alert is
  explicitly retained as later work, not reported as delivered.

## Open decisions

None open for this slice. The unchosen push service belongs to the deferred
alert, not a default to invent here.

- [DETAIL] Select the night profile explicitly per invocation, because leaving
  day settings intact makes the change reversible and its activation visible.
- [DETAIL] Set phase-4 appetite to two hours, repairs included, because this
  is a bounded settings, launcher and regression-test change; stop rather than
  expand into a general command parser or monitoring service.
- [DETAIL] Test literal command fixtures independently of the rule generator,
  because comparing a list only with its own samples would miss this incident.
