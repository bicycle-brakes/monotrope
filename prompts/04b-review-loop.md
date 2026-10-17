# Phase 4b · Review loop

**Model:** none of its own — every round is called through Pi against
OpenCode Go; started only by `python3 scripts/stage2.py review-loop <change>`.
The loop runs until a round is clean (ADR 0021): round 1 is the **free
swarm** — every model a forced live catalog refresh (`pi update --models`
before `pi --list-models`) finds under the `opencode-go` provider that the
`free_stage` rule in `model-endpoints.yaml` selects, called in parallel; round
2 is the **Flash swarm** — the entry's eligible `flash_swarm` members, in
parallel; every later round calls one eligible rung of the `modelle` ladder,
cheapest first: the runner orders the set by the declared cost value
`anfragen_5h`, never by list position. A Flash member that fails is replaced
in its round by the cheapest eligible rung not yet used, each model at most
once, and the swap is recorded. The rule, the set and the cost values are
data: a one-line pull request changes any of them, and this text names no
model. A round whose every row
is decided and none accepted ends the loop; two consecutive rounds whose only
accepted findings came from the repair trip the brake; a spent ladder stops
the loop for the maintainer — no model is substituted for a spent ladder's
last rung, and no model is called twice.
**Input:** a paid round reads the change's diff against its merge base with
`origin/main`, uncommitted changes included, and this text. A free round is
confined to the implementation diff alone — source and test code in bounded
hunks, no tools, no repository access, and nothing else in its prompt.
**Result:** rows for the loop record, outside the repository until the phase-6
verdict.
**Gate:** rounds until a clean round, bounded by the declared ladder; the
repair brake and the maintainer stop stand above it; `make verify` green after
each repair.

## For the reviewer

You read a change before its review and report what is wrong with it. You may
not read `AGENTS.md`, so the rules you need are here:

- Every row is in English.
- No customer name, schema, entity or figure appears in a row.
- A finding reads without the spec beside it: say what is wrong and where.
- Read nothing outside the worktree and the repository's git directory.
- A free-swarm member reads nothing at all beyond the diff in its prompt: it
  has no tools and asks for none.

Report three kinds of finding, as phase 6 does: what the change promises and
does not do, what it does that nobody asked for, and what a maintainer who was
not there would trip over (error handling, edge cases, contracts facing
outward, security). Use the dimensions `SPEC` and `MAINT`, and the severities
`BLOCKER`, `MAJOR` and `MINOR`.

Answer with table rows only: `| ID | Severity | Dimension | Origin | Where |
Finding |` — six cells, one row per finding, no header; write a `|` inside a
cell as `\|`. When you find nothing, answer in one sentence.

## For the orchestrator

The rows are in the loop record, outside the worktree. Never copy them into it.
A swarm round carries one row series for all answering members; a member that
failed is named beside their rows and its failure is no finding.

**The evidence rule.** A finding of a member is taken only when a test
demonstrates it or the spec supports it; otherwise it is rejected with its
reason and stays in `findings.md` as a disagreement. This holds in every repair
round, so a finding about something the spec does not cover needs a test or is
rejected. A duplicate report keeps one row per member — reject the copies
explicitly, do not delete them.

1. For each row write its `Status` in the record: `taken — <test or
   criterion>`, `taken — not a test — <reason>` for a finding no test can
   show, or `rejected — <reason>`.
2. Hand the taken rows to the repair: `python3 scripts/stage2.py repair
   <change>` gives them to Codex in one call; the runner runs `make verify`
   and writes each row's `Status` (`docs/WORKFLOW.md` §4, "Repairing taken
   findings").
3. For each row the repair marked `fixed`, write `Broke a test` from the run's
   evidence: `yes` when its repair turned a test red that was green before it,
   `no` when it did not; the next round starts only when `make verify` is
   green.
4. After the phase-6 verdict, the rows enter `findings.md` with
   `release-loop`. The release carries the run's snapshot: its stops, its
   consumed stages and its round count survive a release and an edited
   configuration (ADR 0021, decision 9).
