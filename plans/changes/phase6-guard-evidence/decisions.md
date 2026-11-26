---
title: "Decisions — phase6-guard-evidence"
status: draft
implementation_status: none
date: 2026-11-26
last_reviewed: 2026-11-26
updated: 2026-11-26
supersedes: null
superseded_by: null
bead: coding-harness-mwzv.6
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: antigravity, version: "Gemini 4 Neon High, 2026-11-26"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [decisions, phase-6, guard-evidence]
---

# phase6-guard-evidence — Decisions

Phase-1a direction recorded from the maintainer's bug specification (2026-11-25, bead `coding-harness-mwzv.6`).

## Q-1 · Fix the phase-6 guard-evidence parser so valid Codex guard-evidence lines are never rejected

asked: 2026-11-25
answer: "Fix at one place (`GUARD_EVIDENCE_LINE` / `split_guard_evidence` in `scripts/stage2.py`) so valid Codex phase-6 answers that include `Guard evidence: ...` lines beside six-cell finding rows or `No finding.` — including a trailing full stop (`yes.`) or sentence-ending punctuation (`yes. <text>`, `no. <reason>`, `no — <reason>`) and minor harmless Markdown wrapping such as backticks around the test path or parameterized test IDs (`[param]`) — are accepted and recorded rather than discarding the whole review, while still strictly refusing genuinely malformed lines (prefix-only `Guard evidence:`, missing fault, bare `no` or `no.` without a reason, verdicts other than `yes`/`no`, or guard evidence alone with no verdict)."
answered_by: maintainer
status: answered
context: |
  Topic: Phase-6 review parser (`GUARD_EVIDENCE_LINE` in `scripts/stage2.py`) rejecting valid Codex reviews when `Guard evidence:` lines end with a period (`catches without switch: yes.`) (bead coding-harness-mwzv.6, class bounded).
  Intention: stop discarding valid Phase-6 Codex reviews and forcing redundant reruns whenever Codex punctuates a `Guard evidence:` line as a normal sentence.
  Today: Measured three times on 2026-11-25 (`plans/changes/archive/2026-11-26-detached-job-launcher/findings.md` thread `01a2132e-db23-7ed2-8005-26f930522110`, `plans/changes/worktree-setup-hook/findings.md` threads `01a213f1-5c85-7891-9b31-66ca1f15f9d2` and `01a21477-cd20-7df0-be2b-635de9f41681`), Codex returned valid six-cell finding rows followed by `Guard evidence: tests/...::test_... — fault: ... — catches without switch: yes.` and `GUARD_EVIDENCE_LINE` (which allowed `[,;:]` before prose but rejected `.` at the end of `yes.`) rejected the entire Phase-6 answer as malformed.
  Repository change: fix `GUARD_EVIDENCE_LINE` (and `PHASE6_GUARD_EVIDENCE` if clarifying examples help) at the single parser choke point in `scripts/stage2.py` so valid natural punctuation (`yes.`, `yes. <prose>`, `no. <reason>`, `no — <reason>`, optional backticks around test refs, parameterized `[...]` test suffixes) is accepted while strictly refusing malformed lines (`no` / `no.` without a reason, `maybe`, prefix-only, missing verdict), and add regression tests reproducing the real rejected Codex outputs in `tests/test_stage2.py`.
  Architecture change: none (bounded bug fix inside the existing ADR 0023 guard-evidence parser; ADR 0023 itself stays untouched).

In the context of Codex phase-6 reviews being rejected as malformed because `GUARD_EVIDENCE_LINE` forbade a trailing full stop (`yes.`) and similar natural punctuation on valid `Guard evidence:` lines, facing wasted reruns and lost verdicts on `detached-job-launcher` and `worktree-setup-hook`, we decided to widen `GUARD_EVIDENCE_LINE` at its one choke point in `scripts/stage2.py` to accept natural sentence punctuation (`yes.`, `yes. <prose>`, `no. <reason>`, `no — <reason>`, optional backticks and parametrized test ids) while preserving strict refusal of reasonless `no`/`no.`, non-yes/no verdicts, malformed lines and verdictless evidence, to achieve reliable acceptance of valid phase-6 reviews without weakening ADR 0023 guard-evidence enforcement, accepting no relaxation of the requirement that every `no` carries an explicit reason and every answer carries a verdict. — 2026-11-26
