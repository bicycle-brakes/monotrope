# Phase 4b · Review loop

**Model:** none of its own — every round is called through Pi against
OpenCode Go; started only by `python3 scripts/stage2.py review-loop <change>`.
The loop runs until a round is clean (ADR 0021): round 1 is the **free
swarm** — every model a forced live catalog refresh (`pi update --models`
before `pi --list-models`) finds under the `opencode-go` provider that the
`free_stage` rule in `model-endpoints.yaml` selects, called in parallel; round
2 is the **Flash swarm** — up to three cheapest reachable admitted paid
members for fresh availability-enabled runs; legacy declarations use the
entry's eligible `flash_swarm` members, in parallel; one deadline of
`REVIEWER_MINUTES` covers that round's members and every replacement; every later round calls one eligible rung of the `modelle` ladder,
cheapest first: the runner orders the set by the declared cost value
`anfragen_5h`, never by list position. A Flash member that fails is replaced
in its round by the cheapest eligible rung not yet used, each model at most
once, and the swap is recorded. The rule, the set and the cost values are
data: a one-line pull request changes any of them, and this text names no
model. A round whose every row
is decided and none accepted ends the loop; two consecutive rounds whose only
accepted findings came from the repair trip the brake; a spent ladder stops
the loop for the maintainer — no model is substituted for a spent ladder's
last rung, and no model reviews twice in the completed run. Availability
probes are additional audited calls, not reviews.
**Input:** a paid round reads the change's diff against its merge base with
`origin/main`, uncommitted changes included, and this text, with its read-only
tools. The diff leaves out the loop's own records (every `findings.md` and the
generated `plans/INDEX.md`), puts every implementation input before every
prose file, and keeps each retained file's complete diff exactly once; the line
bound is applied afterwards, so a cut takes prose first, never code or tests
before it. A free round is
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
cell as `\|`. When you find nothing, answer exactly: `No finding.`

## For the orchestrator

Before a fresh run with `availability_preflight`, invoke
`python3 scripts/stage2.py prepare-loop <change>`. Report the timestamp,
reachable and failed/skipped models and the resulting stages in the main
Claude Code or Codex conversation. Then pass the printed report id to
`review-loop <change> --availability-reported <id>`. The runner checks
acknowledgment, not the UI display. Probes consume requests but are no review
round; their static input has no code or tools. The receipt expires after
900 seconds and changes to the worktree, configuration or diff invalidate it.
Up to three cheapest reachable admitted paid models form the Flash swarm;
remaining reachable models form the ladder. This supersedes the manual
membership described above for new availability-enabled runs. Old snapshots
stay fixed; preparing cannot restart a spent or released run. Honor temporary
exclusions without probing. New catalog ids still need the existing admission.

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
   green. After a repair the orchestrator made by hand, a targeted check
   stands in for it: the touched and linked test files, `ruff` and the
   gates the touched files feed; one full `make verify` runs on the final
   head before phase 6 (`docs/WORKFLOW.md`, "Hand repairs by the
   orchestrator").
4. After the phase-6 verdict, the rows enter `findings.md` with
   `release-loop`. The release carries the run's snapshot: its stops, its
   consumed stages and its round count survive a release and an edited
   configuration (ADR 0021, decision 9).
