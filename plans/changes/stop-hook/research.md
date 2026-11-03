---
title: "Research — stop-hook"
status: draft
implementation_status: none
date: 2026-11-03
last_reviewed: 2026-11-03
updated: 2026-11-03
supersedes: null
superseded_by: null
bead: coding-harness-788
owner: Data Architect
provenance: human-written
tags: [research]
---

# stop hook — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-11-03: explore · attempt 1 · route flash · endpoint glm-coding-plan · model glm-5.3-flash · leak check clean over 837 files, 3122 commits, 12 rules.

## Runner exploration — 2026-11-03

The exploration is complete. Below is the research body for `plans/changes/stop-hook/research.md`, ready to append after the stage-2 line. First the `neighbours:` header the runner must add (spec.md paths only, per the swarm's neighbour rule):

```
neighbours:
  - plans/specs/implementation-verification/spec.md
  - plans/changes/workflow-promises/spec.md
  - plans/changes/explorer-reviewer-agents/spec.md
  - plans/changes/verify-machine-lock/spec.md
```

`plans/changes/handover-at-95/` holds only a `research.md` (no `spec.md`, per `plans/INDEX.md`), so it cannot be a `neighbours:` entry; it is named below as relevant reading.

---

## What exists today

**The doctrine promises the hook; the tree lacks it.** The header notice of `docs/WORKFLOW.md` ("Not all of it is here yet.", checked 2026-11-01 against the tree at `8ae99e50` after `explorer-reviewer-agents` merged, bead coding-harness-9ll) lists exactly two pieces as **not** in this repository: `scripts/validate_change_artefacts.py` and the stop hook `.claude/hooks/session-stop/check-tests-green.sh`. A Glob over `.claude/**` confirms the absence: `.claude/` contains only `agents/` (nine definitions), `commands/workflow-start.md`, and `settings.json` — no `hooks/` directory. This is a "not there" statement, verified by Glob, not merely "not found by search".

**What the doctrine says the hook does.** Four independent sites describe the target:
- `prompts/05-verify.md`, the phase-5 gate line: "`make verify` green; the stop hook blocks the end of the turn while anything is red."
- `docs/WORKFLOW.md` phase table, row 5: "the stop hook blocks on a red tree"; §2's verdicts paragraph counts it as one of the four phase gates that are "verdicts, not presence checks" (phase 4 `make verify`, phase 5 the stop hook, phase 6 the comparison against `spec.md`, phase 7 CI).
- `docs/WORKFLOW.md` §3 map table, row "Stop hook": path `.claude/hooks/session-stop/check-tests-green.sh`, "blocks the end of a turn on a red tree".
- `AGENTS.md` phase table, row 5: "stop-hook blocks on a red tree". `README.md` "Not built yet" states the same absence: "A validator for the change files and a stop hook that blocks a session end on a red tree."

**Scope and role are already pinned in prose.** `docs/WORKFLOW.md`, the paragraph after the verify-lock description: "The stop hook is the comfort layer, not the enforcement. It runs only when Python was touched since `HEAD`: a hook that costs a minute when nothing has happened is switched off within a week — and a switched-off hook is worse than none, because the registry keeps counting it as protection." `docs/testing.md`, table "Where tests run", row "Stop hook": "at the end of an agent's turn, only when Python changed since `HEAD` | comfort: an agent does not hand back a red tree. It is not the enforcement", and the principle "**The stop hook can be skipped.** The hosted `verify` job is the gate that cannot." The archived spec `plans/changes/archive/2026-09-29-frontmatter-current/spec.md` adds a measurement expectation: "Uncommitted and untracked files are held against today, so `make verify` and the stop hook catch a missing stamp before the commit, not after the push."

**It is deliberately not a gate.** `decisions/gates.yaml` (read in full; "THE ONE LIST (D-10)") contains no stop-hook entry — not there, consistently with the comfort-layer statement. The gate list is read by `scripts/ci_gates.py` and executed by `scripts/verify_all.sh` via `make verify` (`Makefile` target `verify`); a hook placed into that list would contradict the doctrine's enforcement/comfort split.

**The hook was split out of a package change by a recorded decision.** `plans/changes/workflow-promises/decisions.md`, `[DETAIL] The stop hook is split out`: the hook (coding-harness-788, `.claude/hooks/session-stop/check-tests-green.sh`) "fires at the end of every turn, and the full `make verify` takes about eleven minutes (CI, 2026-10-27). Which check it runs, and how long it may hold a turn, changes how every session in this repository feels; that is the maintainer's to decide, so it goes to the daily decision block and stays out of this pull request." The same split is a non-goal in `plans/changes/workflow-promises/spec.md` ("Implementing the stop hook … the stop hook is split out to the daily decision block") and its criterion 8 obliges the missing-pieces notice to keep the hook listed as absent until it is delivered.

**The bead and its assignment.** This change is bead coding-harness-788 (`research.md` frontmatter; opening commit `70e8d943` "chore(stop-hook): open the change folder"; the `plans/INDEX.md` row, draft / none / 2026-11-03). `plans/changes/explorer-reviewer-agents/decisions.md` fixes the package boundaries: "the stop hook is bead coding-harness-788, the validator bead coding-harness-jc3." Three night plans scheduled it in lane B: 2026-10-31 ("draft up to the plan card"), 2026-11-01 (backlog 2), and 2026-11-02 (backlog 2: "explore up to the interview" — this run). The handover `docs/journal/handover/2026-10-28-three-lane-night.md` records the split ("coding-harness-788 — stop hook split out of the i0l package") and carries the open maintainer question 4: "The stop hook (bead coding-harness-788): which check, and how long it may hold a turn."

**What the hook would sit on today.**
- `.claude/settings.json` wires exactly one hook, `SessionStart` → `"$CLAUDE_PROJECT_DIR"/tools/bd prime --hook-json`; there is no `Stop` entry. The file is test-pinned: `tests/test_omnigent_deny_layers.py` asserts its `permissions.deny` list, `tests/test_merge_guard.py` its `permissions.ask` list, and `tests/test_stage2.py` reads it too.
- `make verify` is the full local run: `scripts/verify_all.sh` → `scripts/ci_gates.py` → `decisions/gates.yaml` (pytest with `-n auto`, ruff check/format, kit probe `leerprobe`, plans-registry, frontmatter-current, bead-export, dangling-beads, decision-continuity, adr-answers, interview-minimums, criterion-ledger, research-handoff, gate-schema, ci-drift, ramp-valves, ruleset — 17 verify gates plus drift gates). The verify-lock paragraph in `docs/WORKFLOW.md` (bead coding-harness-p6mu) admits one protected run per user and machine, queues waiters in registration order under `${XDG_STATE_HOME:-~/.local/state}/coding-harness/`, and holds entries while free memory sits below 25 percent (floor `HARNESS_VERIFY_MEMORY_FLOOR`), refusing after 60 low minutes. A hook that runs the full verify contends with this admission; the eleven-minute duration figure above is the only recorded measurement.

**In-repository Stop-hook precedents (user-level, a different layer).** `tools/claude-code/settings.json` already wires a `Stop` event — `~/.claude/hooks/recap.sh stop`, async — beside SessionStart/UserPromptSubmit hooks. `tools/claude-code/hooks/recap.sh` shows the working pattern on this machine: stdin JSON read with `jq` (`.session_id`, `.last_assistant_message`, `.cwd`), a per-session `mkdir` lock with a five-minute staleness rule, a recursion guard (`CLAUDE_RECAP_CHILD`), and the model call from a private scratch directory so a planted project setting cannot load (comment: "bead hit"). The directory also holds `handover.sh`, `parallel-sessions.sh`, `session-scan.sh`; `tools/claude-code/README.md` documents install (merge into `~/.claude`) and the constraints bash 3.2, `jq`, `perl`, macOS. This is display tooling installed per user, not the repository-committed hook the doctrine names.

**Hook mechanics, as researched.** `plans/changes/handover-at-95/research.md` (Claude Code docs read 2026-10-14 at version 2.1.296): common hook input fields are `session_id`, `transcript_path`, `cwd`, `permission_mode`, `effort`, `hook_event_name`; hook outputs add context (`additionalContext`), block (`decision`, exit code 2), stop (`continue: false`) or warn (`systemMessage`); "A hook cannot run a slash command. … The documented way to make Claude act is a Stop hook that blocks with a reason, which keeps the session going with that reason as its next instruction." No artifact in the tree ties these mechanics to this change; they are the documented vocabulary a blocking hook has available.

**A recorded cross-change constraint that cites the hook.** `plans/changes/research-swarm/decisions.md`, item S-12: "under Reading B, `make verify` and the stop hook ('blocks on a red tree') would be red between phase 1 and the interview. That blocks an ordinary session end, such as an overnight run waiting for morning answers, without protecting anything more." That decision resolves the tension for the swarm's own handoff gate (red only once `spec.md` exists); the sentence stands in the tree as a measured statement about what an indiscriminately blocking stop hook would do to ordinary session ends.

**A test ratchet holds the hook absent.** `tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands` (docstring "Criterion 8") asserts `.claude/hooks/session-stop/check-tests-green.sh` in the notice's *absent* half. The same test shows the delivery pattern: `explorer-reviewer-agents` moved its pieces to the *supplied* half in the same test and restamped the notice's check date and commit (documented in `plans/changes/explorer-reviewer-agents/research.md` and `plan.md` step 3).

## Where it lives

Promise and description sites: `docs/WORKFLOW.md` (header notice; §2 phase table and the verdicts paragraph; §3 map table; the comfort-layer paragraph after the verify-lock section), `AGENTS.md` (phase table), `prompts/05-verify.md`, `README.md` ("Not built yet"), `docs/testing.md` ("Where tests run"). The planned implementation path named by the doctrine: `.claude/hooks/session-stop/check-tests-green.sh` — no such file, no `.claude/hooks/` directory. The wiring point for a repository-level hook: `.claude/settings.json` (committed; the `SessionStart` entry with `$CLAUDE_PROJECT_DIR` is the in-file precedent). The enforcement side it must stay out of: `decisions/gates.yaml`, `scripts/verify_all.sh`, `scripts/ci_gates.py`, `Makefile`. Tests that read the files a change would touch: `tests/test_workflow_entry.py`, `tests/test_omnigent_deny_layers.py`, `tests/test_merge_guard.py`, `tests/test_stage2.py`. Precedent implementations: `tools/claude-code/settings.json`, `tools/claude-code/hooks/recap.sh`, `tools/claude-code/README.md`, `tools/claude-code/install.sh`. Decision trail: `plans/changes/workflow-promises/decisions.md` and `spec.md`, `plans/changes/explorer-reviewer-agents/decisions.md`, `docs/journal/handover/2026-10-28-three-lane-night.md`, the night plans `docs/research/2026-10-31-run-plan.md`, `2026-11-01-night-run-plan.md`, `2026-11-02-night-run-plan.md`. Mechanics reading: `plans/changes/handover-at-95/research.md`. Older mentions: `docs/research/2026-10-20-night-run-plan.md` (the i0l audit row), `docs/research/2026-09-26-agent-sdk-and-formal-models.md` (the hook named among absent pieces whose prompts call them gates), `docs/research/2026-10-06-mattpocock-skills.md` (seam analysis of the user-level recap lock — that "stop hook" is `recap.sh`, not this change). `docs/governance/gate-catalog.md` contains no stop-hook mention (grep over the file: no match).

## What is unclear (open questions, not guesses)

- The bead's title, description and class: not read — the tracker is the Dolt database under `.beads/` and this phase reads no tracker (`AGENTS.md`, house rule 2). The tree carries no `class:` declaration for this change (`research.md` frontmatter has none); the night plans say only "explore up to the interview" / "draft up to the plan card".
- Which check the hook runs and how long it may hold a turn: not decided anywhere in the tree — explicitly recorded as the maintainer's decision (`workflow-promises/decisions.md` `[DETAIL]`; handover 2026-10-28 question 4). The only number in the tree is the eleven-minute CI figure for the *full* verify (2026-10-27).
- Whether the "only when Python was touched since `HEAD`" trigger is final scope or a target: both `docs/WORKFLOW.md` and `docs/testing.md` state it, but the hook does not exist, so it describes the aim, not a measured behaviour.
- How "red tree" would be determined short of a full run (a subset, pytest alone, gate selection): not found in the tree; this change folder holds only `research.md`, no design artifact exists.
- How the hook behaves while another verify holds the machine admission (queue wait) or memory sits below the floor: not discussed anywhere in the tree.
- The default provenance classification of a `.claude/hooks/` path: `provenance.yaml` shows prefixes for `.claude/agents/`, `.claude/commands/` and `.claude/rules/`; none for `.claude/hooks/` was found in the greps, and how unlisted paths are classified was not read.
- Whether the hook travels with the kit: `scripts/kit/manifest.yaml` classifies `.claude/` as bestand with the explicitly open decision D3; a hooks file rides that prefix until D3 is answered.
- Whether Stop-hook blocking semantics (block with a reason that becomes the session's next instruction, per the handover-at-95 research) are the intended mechanism for "blocks the end of the turn": nowhere connected to this change in the tree.
- Shell-environment requirements for the repo-level hook script (the user-level hooks are documented against bash 3.2/macOS; no requirement for this hook is stated anywhere).

## Which files a change would have to touch

The new hook at the doctrine-named path `.claude/hooks/session-stop/check-tests-green.sh`; the wiring in `.claude/settings.json` (a `Stop` entry beside the existing `SessionStart` one); the notice in `docs/WORKFLOW.md` (hook moves from absent to supplied, with a fresh check date and commit, per the criterion-8 contract in `plans/changes/workflow-promises/spec.md`); the ratchet `tests/test_workflow_entry.py::test_workflow_notice_records_supplied_commands` (flip the assertion; the agents delivery in bead coding-harness-9ll is the direct precedent); `README.md` "Not built yet" (drop the stop-hook row, the workflow-promises precedent of dropping only delivered pieces); tests for the hook itself as a new file under `tests/` (no placeholder exists — not there). Already-correct prose that a change must keep true rather than write anew: `docs/testing.md` "Where tests run" and `prompts/05-verify.md`. Whether `docs/governance/gate-catalog.md` gains an entry is unstated — the hook is explicitly not enforcement, and the catalog today holds no mention of it.
