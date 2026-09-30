# Phase 4b · Review loop

**Model:** GLM 5.3 — at effort `max`, through Claude Code against Z.ai; started
only by `python3 scripts/stage2.py review-loop <change>`.
**Input:** the change's diff against its merge base with `origin/main`,
uncommitted changes included, and this text — the runner puts both in the prompt.
**Result:** rows for the loop record, outside the repository until the phase-6
verdict.
**Gate:** at most two rounds, `make verify` green after each repair.

## For the reviewer

You read a change before its review and report what is wrong with it. You may
not read `AGENTS.md`, so the rules you need are here:

- Every row is in English.
- No customer name, schema, entity or figure appears in a row.
- A finding reads without the spec beside it: say what is wrong and where.
- Read nothing outside the worktree and the repository's git directory.

Report three kinds of finding, as phase 6 does: what the change promises and
does not do, what it does that nobody asked for, and what a maintainer who was
not there would trip over (error handling, edge cases, contracts facing
outward, security). Use the dimensions `SPEC` and `MAINT`, and the severities
`BLOCKER`, `MAJOR` and `MINOR`.

Answer with table rows only: `| ID | Severity | Dimension | Origin | Where |
Finding |` — six cells, one row per finding, no header. When you find nothing,
answer in one sentence.

## For the implementer

The rows are in the loop record, outside the worktree. Never copy them into it.

**The evidence rule.** A Codex or GLM finding is taken only when a test
demonstrates it or the spec supports it; otherwise it is rejected with its
reason and stays in `findings.md` as a disagreement. This holds in every repair
round, so a finding about something the spec does not cover needs a test or is
rejected.

1. For each row write `Status` in the record: `taken — <test or criterion>` or
   `rejected — <reason>`.
2. For a taken row also write `Broke a test`: `yes` when its repair turned a
   test red that was green before it, `no` when it did not.
3. Repair the taken rows, then run `make verify`; round 2 starts only when it
   is green.
4. After the phase-6 verdict, the rows enter `findings.md` with
   `release-loop`.
