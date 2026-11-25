---
title: "Findings — cheap-checks-admission"
category: findings
status: draft
implementation_status: none
date: 2026-11-25
created: 2026-11-25
last_reviewed: 2026-11-25
updated: 2026-11-25
supersedes: null
superseded_by: null
bead: coding-harness-bxxt.13
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-25"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — cheap-checks-admission

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1203 files, 5830 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5831 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:95659f4629f54592769b90cfdceffd41c8536a8adc4202d2f36409a001d337d5

Spec review commit: d4370398fadf3de5cd4ecee124c6cb89e0335873

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-1 | [AMBIGUITY] | SPEC | base | spec.md, Problem and Acceptance criterion 2; scripts/kit/probe.py:455-464; pyproject.toml:32-33 | The probe starts `pytest tests/ -q --tb=no -p no:cacheprovider --junit-xml=...` without `-n`, and `[tool.pytest.ini_options]` holds only `pythonpath`, so xdist never reads `PYTEST_XDIST_AUTO_NUM_WORKERS` there: the probe's pytest is one serial process today. Reading A: criterion 2 means the variable is present in the probe's pytest environment. That can be built through `run_gates`' `gate_env` with the probe untouched, but it bounds nothing, and the probe's load from the Problem and decisions Q-1 stays exactly as it is. Reading B: the probe's pytest actually runs with the policy's worker count. That needs `-n auto` in probe.py, which is a protected area, and it turns one process into N workers, which raises load instead of capping it. The refutation case ("receives a different worker environment") is met by A, so it cannot tell a change with no effect on load from the intent. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-1 (2026-11-25) | — |
| S-2 | [AMBIGUITY] | SPEC | base | spec.md, Acceptance criterion 3 and Non-goals; scripts/stage2.py:458-471, 1003-1007, 9368-9377 | "The caller supplies a nonempty worker setting" has two readings. A: the `env` dict passed into `cheap_checks`/`run_gates`, the way the `targeted_pytest_env` tests use it. This can only be tested by calling the function directly: in a real run `verify_attempt` builds its environment through `foreign_env`, whose `ENV_ALLOW` omits `PYTEST_XDIST_AUTO_NUM_WORKERS`, so no runner caller ever supplies one and the criterion never applies. B: the operator exports the variable before starting `stage2.py`, which is how the archived verify-worker-cap spec defines "caller value". Then criterion 3 is red by construction on both paths, and making it green is the foreign-model boundary fix that the Non-goals exclude. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-2 (2026-11-25) | — |
| S-3 | MINOR | SPEC | base | spec.md, Acceptance criterion 1 | "Either runner path" never names its paths. The research lists two `cheap_checks` call sites: the targeted body (scripts/stage2.py:9275, lock variables stripped) and the full-mode `prepare` (scripts/stage2.py:9441, environment from `verify_lock.inherit_env`). The spec does not say that both are meant. Criterion 4 is limited to the targeted check, so a test author still has to decide which call sites criterion 1's refutation case must cover, and whether the full-mode cheap pytest is in scope at all. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-3 (2026-11-25) | — |
| S-4 | MINOR | SPEC | base | spec.md, Acceptance criterion 2 and Open decisions; scripts/stage2.py:8966-8971, 9037-9080, 12702, 12753 | `run_gates` is the only gate executor for three callers: the targeted check, the draft's document check and the hand-off's document check. In a targeted check it also runs the always-selected `docs` gates and the entrypoint gates next to the kit probe. The spec does not say whether the policy goes into `gate_env` for every gate and every caller, or only into the kit probe's launch in a targeted check. "The affected subprocess boundaries" does not settle it, and no criterion refutes either choice. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-4 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5837 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5839 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:640dd29062091dd30ddfc6f08bd96a5b18f02f61f7a5fe426dd2678144612cd1

Spec review commit: 03ff066a1591a4f61cec0baa0256bfc892b84885

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-5 | MINOR | SPEC | base | spec.md, Acceptance criterion 1, Non-goals and Definition of Done; scripts/stage2.py:9252, 9275, 9292, 9172, 9056-9061, 9441-9443; scripts/verify_run.py:717-722 | The spec pins that the cheap pytest launch uses the policy, but not whether the computed `PYTEST_XDIST_AUTO_NUM_WORKERS` stays confined to that launch. Both placements meet criteria 1-5. Placement A, inside `cheap_checks` or wrapped around its argument at the two call sites, changes only the cheap pytest. Placement B, `env = targeted_pytest_env(root, env)` next to the lock strip in `_targeted_body`, also sends the variable into `prepare_derived`, `run_gates`' `gate_env` (every selected gate, the kit probe included) and the fallback `full_verify`. There `verify_run` keeps any nonempty value (717-722) instead of computing `worker_default`, so the full check's worker count would come from the targeted readings. Placement B touches what the Non-goals exclude ("Changing `run_gates`, other gates"). But no criterion goes red under B, and the DoD's proof, "shown by the pull request's file list", cannot tell A from B: `run_gates`, `_targeted_body` and `cheap_checks` all live in `scripts/stage2.py`, which the change has to touch anyway. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-5 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5840 commits, 12 rules.

Stage-2 call, 2026-11-25: spec-review · endpoint claude-code-plan · model claude-opus-5-5 · leak check clean over 1206 files, 5841 commits, 12 rules.
## Phase 2a — Opus 5.5, 2026-11-25

Spec fingerprint: sha256:e87b09a21fe78e4c928b4d900ade26fba3895eb59d4bc4a27d69a8ad68dc380c

Spec review commit: 62017fa6fb7d389432e5412d91d0954ba1896577

| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
|---|---|---|---|---|---|---|---|---|
| S-6 | [AMBIGUITY] | SPEC | base | spec.md, Acceptance criterion 6; scripts/stage2.py:9163, 9172, 9284, 9292; scripts/verify_run.py:717-722 | The criterion's sentence limits the check to "the environment passed to later preparation, gates or full verify". Its refutation is wider: "appears in any later step's environment". Two later steps already compute `PYTEST_XDIST_AUTO_NUM_WORKERS` for their own children. The targeted pytest launches with `targeted_pytest_env(root, env)` at 9163, and the full check's scheduler sets the variable in `base_env` at 717-722. Reading A: "a later step's environment" means the environment a step's own launches get. Then criterion 6 is red on today's unchanged code whenever the readings give a count: the targeted pytest launch, and in the fallback the full-verify gates, carry a computed value the caller's environment lacks. Keeping that value out would mean changing `_targeted_commands` or `verify_run`, and the Non-goals exclude both ("worker calculation", "full-verify admission policy"). A launch-level test also cannot tell a leaked cheap-check value from the step's own value, because both come from the same readings. Reading B: only the `env` argument handed to `prepare_derived`, `targeted_selection`, `_targeted_commands`/`run_targeted`/`run_gates` and `full_verify` counts. Then the criterion can be tested by checking the dict, and a cheap-check value written back into the caller's dict turns it red. The test author has to choose which environments the refutation observes, and which launches it exempts. | Opus | in spec — [DETAIL] decided by the orchestrator: decisions.md D-6 (2026-11-25) | — |

Stage-2 call, 2026-11-25: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-terra · leak check clean over 1206 files, 5843 commits, 12 rules.

Stage-2 call, 2026-11-25: implement · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-sonnet-5-5 · reason GLM 5.3 Flash via Z.ai: weekly limit at 100 % until 2026-11-29 (bead coding-harness-b5pu) · leak check clean over 1206 files, 5845 commits, 12 rules.

> Attempt 1 (stage-1) failed its post-run checks.
>
> Files the attempt changed (lines added, removed):
> - `docs/WORKFLOW.md` +11 -2
> - `scripts/stage2.py` +3 -1
> - `tests/test_kit_probe.py` +38 -0
> - `tests/test_stage2.py` +20 -0
> - `tests/test_stage2_fail_fast.py` +117 -0
>
> Diagnostics:
> ```text
> - Runner format before post-run verification: ruff changed no file; ruff check left findings without a safe fix or a file that does not parse.
> - Runner cheap checks before post-run verification: `.venv/bin/ruff check` exited 1
> tests/test_kit_probe.py:27:28: ARG001 Unused function argument: `args`
>    |
> 25 |     launched: list[list[str]] = []
> 26 |
> 27 |     def fake_run(command, *args, **kwargs):
>    |                            ^^^^ ARG001
> 28 |         launched.append([str(part) for part in command])
> 29 |         return subprocess.CompletedProcess(command, 0, "", "")
>    |
>
> tests/test_kit_probe.py:27:36: ARG001 Unused function argument: `kwargs`
>    |
> 25 |     launched: list[list[str]] = []
> 26 |
> 27 |     def fake_run(command, *args, **kwargs):
>    |                                    ^^^^^^ ARG001
> 28 |         launched.append([str(part) for part in command])
> 29 |         return subprocess.CompletedProcess(command, 0, "", "")
>    |
>
> Found 2 errors.
> ```

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1207 files, 5848 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1207 files, 5850 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1207 files, 5850 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1207 files, 5850 commits, 12 rules.

Stage-2 call, 2026-11-25: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1207 files, 5851 commits, 12 rules.

Loop attempt: 2026-11-25 — no round was written; the review-loop calls above consumed no stage; audit calls: 2

Notice: free ids dropped: beam-free (a paid model; the free class does not admit it).

Notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base.

Notice: paid models skipped: gpt-6-luna (the model gpt-6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); claude-haiku-5-5 (the model claude-haiku-5-5 was skipped on 2026-11-06: Messages API measured 2026-11-06, but this model refuses Pi's request: 400 "thinking.type.enabled is not supported for this model; use thinking.type.adaptive" (a Pi adapter setting, bead coding-harness-36za evidence)); gpt-5.6-luna (the model gpt-5.6-luna was skipped on 2026-11-06: Responses API measured 2026-11-06 (grok-4.7), but this model answered 403 "Model access is disabled"); gemini-4-argon (the model gemini-4-argon was skipped on 2026-10-30: wire API not measured (the Go page names the Google endpoint; its measurement is bead coding-harness-twdu); the live catalog of 2026-11-08 lists gemini-4-argon again); kimi-k3.1-pro (the model kimi-k3.1-pro was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)); beam-free (the model beam-free was skipped on 2026-10-30: not in the live Go catalog (2026-10-30)).

Notice: in the live catalog without a terms reading: hy4, muse-spark-1.2-contributor, muse-spark-1.3-contributor, qwen4-max.

Notice: the data terms of deepseek-v4.1-flash expire on 2026-11-30 (5 days left).

Notice: the data terms of deepseek-v4-pro expire on 2026-11-30 (5 days left).

hy4-flash-free was asked again with the format reminder: the first answer was malformed

Address notice: opencode-go/gemini-4-argon: wire api "google-generative-ai" has no recorded base; the record declares anthropic-messages, openai-completions, openai-responses; running on with the definition's own base

From hy4-flash-free:

hy4-flash-free's first answer, which was not in the required format:

The answer was not only six-cell rows; what is not one is kept below as it came.

> No finding

From hy4-flash-free:

hy4-flash-free's second answer, which was not in the required format:

The answer was not only six-cell rows; what is not one is kept below as it came.

> No finding

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model deepseek-v4.1-flash · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.5 · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.6-flash · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model glm-5.3-flash · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model qwen3.8-flash · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model hy3 · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model qwen3.7-plus · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model minimax-m3.1-flash · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.5-pro · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model mimo-v2.6-pro · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model minimax-m3 · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model hy4-preview · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model kimi-k2.7-code · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model deepseek-v4-pro · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model step-5-preview · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model glm-5.3 · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model grok-4.7 · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model qwen3.8-max · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: prepare-loop · endpoint opencode-go · model kimi-k3 · leak check clean over 1207 files, 5851 commits, 12 rules.

Stage-2 call, 2026-11-25: review-loop · endpoint opencode-go · model hy4-flash-free · leak check clean over 1207 files, 5851 commits, 12 rules.
