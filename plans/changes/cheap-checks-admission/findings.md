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
