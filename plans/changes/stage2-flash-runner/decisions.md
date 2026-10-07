---
title: "Decisions — stage2-flash-runner"
status: draft
implementation_status: none
date: 2026-10-07
created: 2026-10-07
last_reviewed: 2026-10-07
updated: 2026-10-07
bead: coding-harness-qcp
tags: [decisions, stage-2]
---

Interview for bead coding-harness-qcp: stage 2 runner verbs for explore
(phase 1) and implement (phase 4) on GLM 5.3 Flash. Maintainer statements
recorded 2026-10-06 and 2026-10-07.

## Maintainer statements

**2026-10-06** (bead coding-harness-bib, ADR 0007 widened):

- "Bau soll zukünftig mit GLM Flash passieren" (Implementation should run on
  GLM Flash)
- "Und Recherche soll auch glm 5.3 Flash sein" (Exploration should also be
  GLM 5.3 Flash)

**2026-10-07** (this session):

- "was muss gemacht werden, damit glm den code implementiert statt sonnet?"
  (What needs to be done so GLM implements the code instead of Sonnet?)

## [DECISION] 1: Fallback when stage 2 is off

**Options:**

1. Check a flag/config to detect whether stage 2 is live; fall back to Haiku
   4.5 / Sonnet 5.5 if off or Z.ai unreachable.
2. No fallback; new verbs only exist when stage 2 is live (post-ADR-0007). If
   Z.ai fails, call fails with clear error. Stage 1 continues Haiku 4.5 /
   Sonnet 5.5.

**Recommendation:** Option 2 (no fallback). The new verbs are only reachable
when stage 2 is live. Simpler code, clearer error messages. Stage 1 continues
unchanged.

**Consequence:** No route between models. Clear error when Z.ai unreachable
helps diagnosis.

## [DECISION] 2: Error handling from GLM implementation

**Options:**

1. If Claude Code exits non-zero or returns empty, fail the entire verb (exit
   1, like review-loop).
2. Record partial output; implementer decides whether to retry or fix.
3. Run `make verify` after call; if it fails, log output and let next GLM
   round see test failures.

**Recommendation:** Option 1, consistent with review_loop (lines 836–837).
Verb fails if call fails. Implementer re-runs verb after diagnosing, or
continues manually.

**Consequence:** Implement verb does not run `make verify` itself. No
partial-output recovery.

## [DECISION] 3: Commit discipline during implement

**Context:** prompts/04-implement.md (lines 27–50) and AGENTS.md house rule
4 require commits per green step. Current design: Claude Code (implementer)
creates commits, not runner.

**Options:**

1. Runner checks for commits per step after call (no enforcement; could warn).
2. Implementer responsible. Diff shows whether discipline held.
3. Verb sets flag/hook in worktree to enforce per-step commits.

**Recommendation:** Option 2. Runner launches Claude Code; Claude Code's
prompts enforce per-step commits. Diff will be evidence.

**Consequence:** Review of PR verifies commit discipline. No runner-side
enforcement; discipline in phase prompt and implementer's session.

## [DETAIL] agent decides

### detail-a: Model constant refactoring

Should `scripts/stage2.py` have separate `GLM_FLASH` constant or parameter
to `glm_env()`?

**Recommendation:** Separate constants for clarity. Parallel with existing
`GLM` constant. Makes model choice visible at call site.

### detail-b: Prompt input for implement

Should runner read `spec.md` and `plan.md` and append, or ask Claude Code to
read via `@file` references?

**Recommendation:** Append file contents, consistent with how review_loop
appends diff (line 808). Claude Code will have full context without
independent file reads.

### detail-c: Make verify after implement

Should verb run `make verify` after call succeeds, or should implementer run
it?

**Recommendation:** Implementer runs `make verify` after call succeeds. Phase
prompt (line 8, "gate: `make verify` green") is implementer responsibility.
Implementer sees test failures and can ask GLM to fix in next round if needed.

### detail-d: Output recording for explore

Where should explore record its output? Options:

1. `findings.md` (like Codex calls), though phase 1 does not expect it
2. `research.md` directly
3. Temporary location, import to research.md

**Recommendation:** Option 2, `research.md` directly. Phase output is
`research.md`. Record call line in `research.md` as metadata, not
`findings.md`. Metadata with research, not separate review artifact.

## Addendum 2026-10-07: the maintainer's answers

Asked one at a time in the Claude Code session on 2026-10-07; both answers
replace the research's recommendations for [DECISION] 1 and 3:

1. **Fallback: "Z.ai weg → Sonnet, Leak → Stopp (Empfohlen)".** When Z.ai is
   unreachable or stage 2 is off, the orchestrating session explores with
   Haiku 4.5 and implements with Sonnet 5.5 and records that in plan.md. A
   leak-check BLOCK stops the run and is reported to the maintainer; no
   silent fallback. Not chosen: no fallback.
2. **[DECISION] 2** (a failed GLM call fails the verb) is a `[DETAIL]`,
   consistent with `review-loop`; not asked.
3. **Discipline: "Runner prüft danach (Empfohlen)".** The runner passes the
   agent rules in the prompt and checks after the run: `make verify` green,
   at least one new commit, the time log in plan.md. If anything is missing
   the verb exits red; GLM Flash gets one more try, then Sonnet 5.5 takes
   over. Not chosen: rules in the prompt only.
