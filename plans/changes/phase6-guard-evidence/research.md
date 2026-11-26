---
title: "Research — phase6-guard-evidence"
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
produced_by: {kind: llm-session, name: claude-code, version: "2026-11-26", model: "claude-haiku-5-5"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
class: bounded
---

# phase6 guard evidence — Research

Stage-2 call, 2026-11-26: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM through Z.ai at its weekly limit until 2026-11-29 · leak check clean over 1293 files, 6061 commits, 12 rules.

## Runner exploration — 2026-11-26

## What exists today

**Phase 6 guard evidence on the Codex path is already implemented in `scripts/stage2.py`.** The constants `PHASE6_GUARD_EVIDENCE`, `PHASE6_GUARD_INSTRUCTION` and `PHASE6_ANSWER_FORMAT` build the reviewer prompt. The regex `GUARD_EVIDENCE_LINE` defines the one accepted line form: `Guard evidence: tests/<path>.py::test_<name> — fault: <text> — catches without switch: <yes…|no, reason>`. `split_guard_evidence` separates such lines from the verdict text. `phase6_rows` checks only the verdict text: six-cell rows, or exactly `No finding.`. A line that begins `Guard evidence:` but does not match the form makes the answer malformed. The `review` verb (the function that writes `## Phase 6 — Codex` blocks) keeps the full answer through `answer_block`. A malformed answer is recorded as rejected evidence and releases nothing. Source: `scripts/stage2.py`, symbols listed above.

**Tests that pin this behaviour** are in `tests/test_stage2.py`: `test_phase6_guard_evidence_survives_findings_and_no_finding_verdicts`, `test_phase6_refuses_malformed_guard_evidence_beside_findings`, `test_phase6_guard_instructions_cover_every_changed_test_without_loop_rows`, `test_phase6_guard_instructions_require_a_real_fault_and_block_empty_guards`. The first two check runner output. The last two check prompt text and the regex. The tests cite "spec, criterion 9" and "criterion 10". No spec with that numbering is in this change folder, and I did not open the archived guard-test spec to confirm the numbering.

**The Claude path has no evidence format.** `prompts/06-review.md`, section "Guard tests (ADR 0023)", asks the reviewer to record each guard test's real fault and whether it is caught without the switch. It gives no line format and no parser exists for it. `templates/findings.md` contains no `Guard evidence` text (searched across `templates/**`). The archived `plans/changes/archive/2026-11-16-guard-test/findings.md` shows the reviewer writing lines in the Codex form by hand, in its Phase 6 blocks.

**Doctrine:** `docs/adr/0023-guard-proof-for-test-only-repairs.md`, Decision item 3, says phase 6 reads every added or changed guard test, records its real fault and whether it is caught without the switch, and treats a conditional-only failure as a BLOCKER. `docs/WORKFLOW.md` (section on guard tests, ADR 0023) and `prompts/04b-review-loop.md` restate it.

**Repair-side guard proof is a separate mechanism.** `scripts/stage2.py` `guard_authorised` and `guard_test_proof` run the two proof legs (red with `STAGE2_PLANT_FAULT=1`, green without). They do not read phase-6 evidence.

**Verification gate:** `scripts/check_guard_test_environment.py`, registered as `guard-test-environment` in `decisions/gates.yaml` and in `.github/workflows/ci.yml`. It refuses the presence of `STAGE2_PLANT_FAULT` in any verification run.

## Where it lives

- Codex phase-6 behaviour: `scripts/stage2.py` (constants above, `split_guard_evidence`, `phase6_rows`, the `review` verb).
- Tests: `tests/test_stage2.py` (names above).
- Claude-path instructions: `prompts/06-review.md`. Template: `templates/findings.md`.
- Doctrine: `docs/adr/0023-guard-proof-for-test-only-repairs.md` (status accepted; review header pending), `docs/WORKFLOW.md`.
- Bead `coding-harness-mwzv.6`: its description could not be read. The Dolt database under `.beads/` is outside the read-only tools. The only readable statement of intent is in `docs/journal/handover/2026-11-25-evening-eighteen-merges-prerequisites-for-agy.md`, which lists "mwzv.6 (phase-6 answers with guard-evidence lines refused)" under new beads.

## What is unclear

- **Meaning of "refused".** The handover's wording and the current code disagree or are at least not obviously the same. The code accepts well-formed evidence beside findings and beside `No finding.`. It refuses only malformed evidence and evidence without a verdict. Whether the bead wants a stronger refusal cannot be settled from the repository.
- **Coverage is not checked.** In the code I searched, `GUARD_EVIDENCE_LINE` and `split_guard_evidence` are used only inside `scripts/stage2.py`'s `phase6_rows` and `split_guard_evidence`. I found no check that each guard test in the diff has a matching evidence line, nor that a named test exists or was added or changed in the diff. "Every one, never a sample" is enforced only by the prompt text.
- **Form details.** The regex requires a `.py` path and a function name beginning `test_`. A bare `no` without its reason is not evidence, and a bare `yes` is accepted. Whether any guard test in the repository is named outside `test_*` was not checked.
- **Claude path.** Nothing in the repository says whether the Claude path must use the same line format. The current state is informal.
- **Diff input.** `PHASE6_GUARD_INSTRUCTION` asks the reviewer to read guard tests "from the test's source and the implementation diff". How completely the runner supplies the diff was not checked.
- **Spec.** `plans/changes/phase6-guard-evidence/` contains only `research.md`. No `spec.md`, `decisions.md` or `plan.md` exists yet.

## Which files a change would have to touch

Files where the current behaviour is written, so a change would meet them: `scripts/stage2.py` (`PHASE6_*` constants, `GUARD_EVIDENCE_LINE`, `split_guard_evidence`, `phase6_rows`, the `review` verb); `tests/test_stage2.py` (the four criterion 9 and 10 tests above); `prompts/06-review.md` (Claude-path guard section); `templates/findings.md` (Phase 6 section); `docs/WORKFLOW.md` (phase-6 and guard-test sections); `docs/adr/0023-guard-proof-for-test-only-repairs.md` (accepted doctrine; a change to it is a decision question for the maintainer).

## Observations for the runner

- This `research.md` has no `neighbours:` header. The swarm gate requires one; for a `bounded` change the single explorer runs, and the header is still expected.
- The header still says `provenance: human-written`. Per the note in the file, whoever fills it with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and `review:`.

## Orchestrator verification of the measured rejections — 2026-11-26

Direct inspection of the three rejected Codex Phase-6 blocks recorded in the repository (`plans/changes/archive/2026-11-26-detached-job-launcher/findings.md` thread `01a2132e-db23-7ed2-8005-26f930522110`, `plans/changes/worktree-setup-hook/findings.md` threads `01a213f1-5c85-7891-9b31-66ca1f15f9d2` and `01a21477-cd20-7df0-be2b-635de9f41681`) and `scripts/stage2.py:385-389` (`GUARD_EVIDENCE_LINE`) confirmed the exact failure mechanism:

- `GUARD_EVIDENCE_LINE` matches `(?P<catches>yes(?:[,;:]?\s+\S.*)?|no[,;:]?\s+\S.*)$`, which accepts `yes` and `yes, <text>` / `yes; <text>` / `yes: <text>`, but rejects a trailing full stop (`yes.`) as well as `yes. <text>`, `no. <reason>`, and `no — <reason>`.
- In all three rejected Phase-6 runs, Codex produced valid six-cell finding rows followed by `Guard evidence: tests/<path>.py::test_<name> — fault: <text> — catches without switch: yes.` — ending with a period — causing `split_guard_evidence` to leave the line in `rest` and `phase6_rows` to reject the entire answer as malformed.
- Secondary brittle points in the same regex (`scripts/stage2.py:386`): test node ids wrapped in backticks (`` `tests/test_x.py::test_y` ``) or parametrized test ids (`tests/test_x.py::test_y[case]`), or `yes.` / `no.` followed by a reason, are rejected despite being standard pytest/Markdown forms.
- Existing tests (`tests/test_stage2.py:23178-23281`) explicitly require rejecting: evidence alone without a verdict, `catches without switch: maybe`, bare `no` (and by extension bare `no.`) without a reason, and prefix-only `Guard evidence: ...` lines even beside valid findings.
