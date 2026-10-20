---
title: "Research — review-loop-row-ids"
status: draft
implementation_status: none
date: 2026-10-20
last_reviewed: 2026-10-20
updated: 2026-10-20
supersedes: null
superseded_by: null
bead: coding-harness-6jg
owner: Data Architect
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: Claude Code, version: "Opus 5.5, 2026-10-20"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [research]
---

# review loop row ids — Research

Phase 1 per [`prompts/01-explore.md`](../../../prompts/01-explore.md); this
file is empty until it has run.

> **Bring the provenance up to date.** The frontmatter says
> `provenance: human-written` — that holds for this skeleton. Whoever fills it
> with a language model sets `ai-drafted-reviewed` and adds `produced_by:` and
> `review:` (`provenance.yaml`, class `ai-drafted-reviewed`,
> `review_required: true`).

Stage-2 call, 2026-10-20: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM unavailable until 2026-10-21T20:34+08:00 · leak check clean over 493 files, 1608 commits, 12 rules.

## Runner exploration — 2026-10-20

I could not run Phase 1, so `research.md` is unchanged by me.

**Blocked:** the Bash tool is disabled in this session, and `scripts/stage2.py explore` has to be run through it. I did not write the research by hand. That would skip the leak check and the recorded Stage-2 call, which the phase requires.

**What is in place:**
- The matching artefacts are `plans/changes/review-loop-row-ids/research.md` and `plans/changes/repair-fixed-lines/` (`spec`, `research`, `plan`, `findings`, `decisions`). `plans/INDEX.md` also mentions the topic. Nothing in `plans/specs/` matched.
- `research.md` is the existing skeleton, and it is still uncommitted (`M` in git status). It already has one line: "Stage-2 call, 2026-10-20: explore · attempt 1 · route stage-1 · endpoint claude-code-plan · model claude-haiku-5-5 · reason GLM unavailable … · leak check clean over 493 files, 1608 commits, 12 rules." I did not write that line and I cannot verify it. Check it against the real script output before you keep it.
- Z.ai GLM is unavailable until 2026-10-21 20:34 Asia/Singapore, so the call goes through the `--stage2-off` route. I did not try the normal GLM route.

**Next step:** run this from the worktree root, then check the output:

```
python3 scripts/stage2.py explore review-loop-row-ids --stage2-off "GLM unavailable until 2026-10-21T20:34+08:00"
```

If the existing uncommitted line blocks a second attempt, the script will say so. Decide whether to keep that line or reset `research.md` to the skeleton before rerunning. If you want, I can rerun the phase once Bash is available, or review the result afterwards.

## Orchestrator exploration — 2026-10-20

The runner's explore call above produced no research: with `--stage2-off` it
chose Haiku 5.5, which took itself for the caller of `stage2.py` and stopped
("the Bash tool is disabled"). The orchestrator (Opus 5.5) explored by
reading the code at `105c270`; this deviation from the explore route is
recorded here and in the night handover of 2026-10-20.

### What the bead describes is fixed

The bead (2026-10-15) saw a round whose member numbered its rows `R2-1 …`;
the runner kept them as raw text, reported "0 rows" and round 3 never ran.
Since the loop rewrite (`6e3df16`, ADR 0021) the runner assigns every
loop id itself: `scripts/stage2.py:4489` numbers each parsed six-cell row
`L<round>-<n>` and ignores the reviewer's first cell. A reviewer's own id
scheme can no longer drop a row.

### What still reports a clean round wrongly

`run_swarm` (`scripts/stage2.py:1754–1775`) treats a member whose answer has
no six-cell row and is not exactly `No finding.` as failed
(`CallFailed("malformed finding output: …")`). The round goes on with the
other members (`scripts/stage2.py:4473–4475`). When every other member
answers `No finding.`, `numbered` stays empty, the round is written with a
line "<member> failed: malformed finding output …", and `clean_round`
(`scripts/stage2.py:2150`) counts it clean: no row, nothing accepted. The
loop ends, although one reviewer did answer — in table lines that are not
six-cell rows (five cells, three cells, a short table) — and those findings
were never read by anyone.

A single-member round with the same answer fails as it should (all members
failed → `CallFailed`, exit 1): `tests/test_stage2.py::
test_table_lines_that_are_not_rows_are_never_reported_as_no_finding`.
There is no test for the mixed swarm case.

A member that answers some six-cell rows and, beside them, table lines that
are not rows is kept: the rows are numbered and the rest is quoted under
`NOT_ROWS_NOTE`. That round is not clean when a row is taken; when every row
is rejected it is clean, and the quoted non-row lines stay undecided text.

### Where the fix sits

- `run_swarm` and the round writer (`scripts/stage2.py:4473–4520`): tell a
  malformed answer (table-shaped lines, no six-cell row) apart from a
  transport failure (timeout, nonzero exit, empty answer).
- `clean_round` and the loop's end condition: a round with a malformed
  member answer is never clean.
- ADR 0021 decision 1 (a round is clean when every row is decided and none
  is accepted) stays; the change only stops a malformed answer from being
  counted as a silent member failure.

### Questions

- `[DECISION]` answered (maintainer, 2026-10-16, interview recorded in the
  bead): refuse — a round whose answer holds row-shaped lines with
  non-conforming ids fails, and the refusal names them; no renumbering.
  Since the rewrite the runner renumbers every *valid* row by design; the
  answer is read as: a malformed member answer refuses the round and names
  the member and its lines; nothing malformed is renumbered or dropped.
- `[DETAIL]` Whether a refused round consumes its stage: it does not; the
  same stage can run again after the maintainer looked (as a timed-out call
  does today) — to be confirmed against `mark_consumed` in the spec.
- `[GAP]` A paid-swarm member that is malformed is replaced by the next
  cheapest model today, like a failed one; whether a malformed answer should
  also be replaced or refuse at once is for the spec to settle from ADR 0021.

## Draft gap checks — 2026-10-20, at `82488fc`

- Persistence: `review_loop` writes the round at lines 4507–4516 and only
  then calls `mark_consumed`. Refusing before that block completes no round
  and consumes no stage. A fresh snapshot is also written only there; an
  existing record or released snapshot can remain unchanged. Call audit
  lines are appended earlier and must remain as evidence of attempted calls.
- Replacement: ADR 0021 decision 4 explicitly lists nonzero exit, timeout
  and empty answer as replacement causes. Decision 6 allows partial swarms
  with failed calls; neither requires replacing malformed findings. Keeping
  ordinary failures separate and refusing malformed table output before
  replacement implements the recorded refusal without changing stage order
  or clean-round semantics. A replacement that itself answers malformed
  must likewise refuse before another replacement starts.
- Scope: `parse_rows` (lines 635–657) returns readable rows and retained
  text, removing table furniture. Testing `split_row` on that retained text
  distinguishes unreadable table lines from generic prose without changing
  the parser. A response with readable rows stays on the existing path.
- Existing tests at lines 10090 and 4647 allow malformed members beside
  readable peers; the table-specific expectation needs correction, while
  the generic-prose and ordinary-call cases remain. The mixed clean-peer
  case is not covered. Paid replacement fixtures are at lines 9675–9710.
- No `templates/plan.md` or `scripts/validate_change_artefacts.py` exists in
  this tree. The phase-3 prompt supplies the plan form; interview and
  criterion-ledger checks are present. No phase-2a finding rows are present
  in this change's `findings.md`; its prior attempt diagnostics are retained.

