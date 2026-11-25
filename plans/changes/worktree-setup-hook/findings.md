---
title: "Findings — worktree-setup-hook"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-wg4z
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — worktree-setup-hook

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1235 files, 5900 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1238 files, 5903 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:5ea12f48640ef7ceda22a74c4d1ffeeda77821f727307bb2752f07aab547c98b

Spec review commit: 21235d1c400086aa1daeb41e68b5c8cb58dc1d07

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md, Open decisions (first [DETAIL]); criteria 1–6 | "Without blocking checkout" can be read two ways, and the readings build different hooks. (a) Setup runs in the foreground. `git worktree add`, and the harness that called it, returns only after `make venv` (pip over the whole `requirements-ci.txt`) and `npm ci` have finished. That takes time and needs the network, and failure messages reach the caller's standard error before git returns. (b) Setup is detached into the background. The checkout returns at once, an agent may start work before `.venv` and `tools/pi/node_modules` exist, and the criterion-5 message appears after git has returned or reaches no one. Criteria 1–6 do not choose between the readings. | Opus | in spec — maintainer 2026-11-25 (decisions.md Q-1): setup runs in the foreground; git worktree add returns only after setup and its check finished | — |
| S-2 | MINOR | SPEC | base | spec.md, criteria 1–4 | The spec puts no limit on how long setup may take. `npm ci`, pip and the `tools/pi/pi --version` check can stall on a dead network or a misbehaving Pi. Under the foreground reading, that holds the checkout open. In the same file, the Beads block caps its call with `BEADS_HOOK_TIMEOUT` (default 300 s, `.beads/hooks/post-checkout:9`), and `scripts/stage2.py:290` caps `pi --version`. The spec says neither whether setup has a limit nor what is reported when one is exceeded. | Opus | in spec — [DETAIL] decided by the orchestrator: setup is capped by HARNESS_LANE_SETUP_TIMEOUT (default 600 s, the pattern of BEADS_HOOK_TIMEOUT); on timeout the hook stops setup and prints the failure line naming the step and the limit | — |
| S-3 | MINOR | SPEC | base | spec.md, criteria 1 and 9; Protected areas | "Outside the managed block" allows the setup section above the BEGIN marker or below the END marker, and the two behave differently. The managed block exits on a nonzero `bd` result (`.beads/hooks/post-checkout:34`). A section below the block is therefore skipped whenever `bd` fails. A section above it delays `bd` by the whole setup. The spec does not say whether a qualifying checkout still gets setup when the Beads integration fails, so a criterion-1 test with a failing `bd` stub has no defined expected result. | Opus | in spec — [DETAIL] decided by the orchestrator: the setup section sits above the managed Beads block, so a failing bd never skips setup; the Beads block runs after it unchanged | — |
| S-4 | MINOR | SPEC | base | spec.md, criterion 5 | "Prominently" cannot go red: the refutation checks only that a message exists and names the step. The spec also does not say where the output of `make venv`, pip and `npm ci` goes. It could pass through to standard error (git sends hook output there), be suppressed, or be written to a log. That choice decides whether the failure line can be seen at all among the install output. | Opus | in spec — [DETAIL] decided by the orchestrator: install output goes to a log file in the new worktree's git dir (lane-setup.log); stderr shows one start line, one result line and, on failure, a line starting 'LANE SETUP FAILED:' naming the step and the log path | — |
| S-5 | MINOR | SPEC | base | spec.md, criterion 7 | Only the value `1` is specified. Whether `HARNESS_NO_LANE_SETUP=0`, `true`, `yes` or an empty value skips setup is left to whoever builds it. For `0`, an "any non-empty value" reading and an "exactly `1`" reading give opposite results, and no criterion can go red on either. | Opus | in spec — [DETAIL] decided by the orchestrator: setup is skipped exactly when HARNESS_NO_LANE_SETUP is 1; any other value, empty included, runs setup | — |
| S-6 | MINOR | SPEC | base | spec.md, Definition of Done, second and fourth items | "Retire the obsolete tracker memory after the hook is available" names no point in time. Inside the pull request that closes the bead, the hook is not yet on `main`. After the merge, the change is closed and nothing checks the retirement. Unlike the other items, this one cannot be checked from the pull request. | Opus | in spec — [DETAIL] decided by the orchestrator: the tracker memory new-worktree-needs-pi is rewritten in the same pull request to point at the hook (bd remember is outside the diff; the orchestrator does it after the merge and the PR says so); the Definition of Done item is dropped from the change | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1238 files, 5914 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1238 files, 5920 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:e904592bf966170466be907459bc7d1069edda9a841f78fb05d5050f4d858be9

Spec review commit: 5953e6581898786c305695e90bf41301b937358f

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-7 | [AMBIGUITY] | SPEC | base | spec.md, criteria 5 and 14; Open decisions (first [DETAIL]) | Criterion 14 does not say how to tell the start line and the result line apart from other stderr lines. It also does not say how the result line relates to the `LANE SETUP FAILED:` lines of criterion 5. Two readings build different output. (a) On failure, the `LANE SETUP FAILED:` line is the result line. When `make venv` fails and the yaml check then fails too (the first [DETAIL] reports each failed check), two such lines appear and criterion 14 goes red as "repeated". The only other way out is to merge every failure into one line. (b) The result line is a separate summary line that is printed on success and on failure, after zero or more `LANE SETUP FAILED:` lines. Take a test in which two steps fail and the result lines are counted: under (b) it expects exactly one, and under (a) it has no consistent expected result. Neither line has a defined form, so a test also cannot tell whether a line is "absent", and criterion 14 cannot go red as written. | Opus | in spec — [DETAIL] decided by the orchestrator under the standing grant for bounded changes (decisions.md): reading (b); every failed check prints its own 'LANE SETUP FAILED:' line, and one separate summary line 'lane setup: ok' or 'lane setup: failed (N checks)' ends the output; the start line begins 'lane setup: start' | — |
| S-8 | MINOR | SPEC | base | spec.md, criterion 11; Open decisions (second [DETAIL]) | The spec gives only the default of 600 for `HARNESS_LANE_SETUP_TIMEOUT`. It does not say what an empty, `0`, negative or non-numeric value does. Criterion 15 settles this question for the opt-out variable but not for this one, so the builder has to choose between the default, no limit, or a failed setup. The choice changes behaviour. With `${VAR:-600}` an empty value means 600, and with `${VAR-600}` it does not. A `0` passed to `timeout` or to perl `alarm` turns the limit off, and those are two of the three timeout mechanisms the Beads block in the same file uses. So with `HARNESS_LANE_SETUP_TIMEOUT=0` and a step that hangs, criterion 11 has no defined expected result. | Opus | in spec — [DETAIL] decided by the orchestrator (decisions.md): HARNESS_LANE_SETUP_TIMEOUT must be a positive whole number of seconds; empty or unset means 600; 0, negative or non-numeric values fall back to 600 and print one warning line | — |
| S-9 | MINOR | SPEC | base | spec.md, Definition of Done (third item); Protected areas | The Definition of Done names the pull request's file list as the evidence that the protected areas are untouched. But the Beads-managed block sits in `.beads/hooks/post-checkout`, a file this change has to edit. That file appears in the list whether or not anything between the `BEGIN` and `END BEADS INTEGRATION` markers changed. An edit inside the managed block, such as changed `bd hooks run` arguments or a changed `BEADS_HOOK_TIMEOUT` default, therefore passes this item. For the managed block the item cannot go red; the file list only covers the historical handovers. | Opus | in spec — [DETAIL] decided by the orchestrator (decisions.md): a test compares the text between the BEGIN and END BEADS INTEGRATION markers with origin/main and fails on any change, so the protected managed block can go red | — |

Stage-2 call, 2026-11-25: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1238 files, 5922 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1239 files, 5932 commits, 12 rules.

Stage-2 call, 2026-11-25: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1239 files, 5933 commits, 12 rules.

> Attempt 1 (codex) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `.beads/hooks/post-checkout` +80 -0
> - `tests/test_worktree_setup_hook.py` +8 -92
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/worktree-setup-hook/plan.md, plans/changes/worktree-setup-hook/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: green) because the targeted coverage was not safe: `.beads/hooks/post-checkout` is an input kind the targeted selector does not cover
> - L1-1: tests/test_worktree_setup_hook.py::test_hook_text_uses_versioned_hook_without_injection: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/worktree-setup-hook/stage2/attempts/worktree-setup-hook/attempt-1-20261125T161937396169Z-f1a6aa7c.md
> ```

Stage-2 call, 2026-11-25: repair · attempt 2 · route codex-repair · endpoint openai-codex · model gpt-6.1-terra · reason first Codex post-run check failed · leak check clean over 1239 files, 5934 commits, 12 rules.

> Attempt 2 (codex-repair) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `tests/test_worktree_setup_hook.py` +6 -2
>
> Diagnostics:
> ```text
> - lifecycle fields: plans/changes/worktree-setup-hook/plan.md, plans/changes/worktree-setup-hook/spec.md — unchanged
> - Runner format before post-run verification: ruff changed no file.
> - Runner verification scope: full `make verify` ran (result: green) because the targeted coverage was not safe: `.beads/hooks/post-checkout` is an input kind the targeted selector does not cover
> - L1-1: tests/test_worktree_setup_hook.py::test_hook_text_uses_versioned_hook_without_injection: pytest ended 0 on the baseline's code; red first needs exit 1 with an assertion failure or pytest's own failed outcome
> - the attempt's protected answer is saved at /Users/mikypiky/coding-harness/.git/worktrees/worktree-setup-hook/stage2/attempts/worktree-setup-hook/attempt-2-20261125T161937396169Z-f1a6aa7c.md
> ```

Stage-2 call, 2026-11-25: repair · attempt 3 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason two Codex post-run checks failed · leak check clean over 1239 files, 5936 commits, 12 rules.

Runner restoration, 2026-11-25: repair · attempt 3 · route stage-1 — lifecycle fields: plans/changes/worktree-setup-hook/plan.md, plans/changes/worktree-setup-hook/spec.md — unchanged

Stage-2 call, 2026-11-25: review-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1239 files, 5937 commits, 12 rules.

Stage-2 call, 2026-11-25: review-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1239 files, 5937 commits, 12 rules.

Stage-2 call, 2026-11-25: review-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1239 files, 5937 commits, 12 rules.

## Hand steps for the orchestrator — 2026-11-25

The runner handed the taken rows below to the orchestrator before any model call: each row's `Where` names a path the runner does not commit. The runner left every Status and `Broke a test` cell of these rows unchanged.

- L2-1 — `.beads/hooks/post-checkout` — runner-held path
- L2-5 — `.beads/hooks/post-checkout` — runner-held path
- L2-10 — `.beads/hooks/post-checkout` — runner-held path
- L2-11 — `.beads/hooks/post-checkout` — runner-held path
- L2-12 — `.beads/hooks/post-checkout` — runner-held path
- L2-13 — `AGENTS.md` — runner-held path
- L2-15 — `.beads/hooks/post-checkout` — runner-held path
- L2-20 — `.beads/hooks/post-checkout` — runner-held path

Each row's Status and `Broke a test` cells live in: L2-1, L2-5, L2-10, L2-11, L2-12, L2-13, L2-15, L2-20 in the loop record `/Users/mikypiky/.local/state/coding-harness/stage2/worktree-setup-hook@c00d7e82/loop.md`.

Book each row from your own evidence as `fixed — tests/<path>::<function>`, setting its `Broke a test` mark. Book `fixed — guard test — tests/<path>::<function>` only for a row taken as `taken — guard test — <reason>` with a nonempty unquoted reason. When no test fits, retake the row as `taken — not a test — <reason>` by editing its Status in the file named above by hand (correct its `Where` cell there first when `triage` refuses it); only then book it as `fixed — not a test — orchestrator hand edit <sha>`.

Stage-2 call, 2026-11-25: repair · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1239 files, 5938 commits, 12 rules.

Runner restoration, 2026-11-25: repair · attempt 1 · route codex — lifecycle fields: plans/changes/worktree-setup-hook/plan.md, plans/changes/worktree-setup-hook/spec.md — unchanged
