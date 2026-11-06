---
title: "Findings — night-machine-facts"
category: findings
status: draft
implementation_status: none
date: 2026-11-06
created: 2026-11-06
last_reviewed: 2026-11-06
updated: 2026-11-06
supersedes: null
superseded_by: null
bead: coding-harness-yql7
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: codex, version: "2026-11-06"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, stage-2]
---

# Findings — night-machine-facts

Stage-2 call, 2026-11-06: draft · attempt 1 · route codex · endpoint openai-codex · model gpt-6.1-sol · leak check clean over 910 files, 3355 commits, 12 rules.

## Draft validation — 2026-11-06

Drafted `spec.md` and `plan.md` against research and the reasoned interview
skip at base `fcbff4a3`. Class remains bounded; no design or ADR is due, no
maintainer answer was added, and no phase-2a finding rows were present.

- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_interview_minimums.py --change night-machine-facts`: green; this change measured.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_criterion_ledger.py`: green, including the draft's not-yet-written tests.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_frontmatter_current.py`: green.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python3 scripts/check_research_handoff.py --change night-machine-facts`: explicitly exempt, no research-swarm/v2 evidence; not a measured swarm handoff.
- Local structural inspection: required headers, eight refuting cases and an
  empty `## Time used` section hold. Implementation tests have not been run;
  they do not exist yet.

`templates/plan.md` and `scripts/validate_change_artefacts.py` are absent at
this base. The plan follows the phase-3 prompt and existing plan form; the
absent validator was not reported green. Index regeneration, the full
registry/tracker check, document verification and the commit remain with the
runner. No files outside this change folder were changed.
