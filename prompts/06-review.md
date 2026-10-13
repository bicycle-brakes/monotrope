# Phase 6 · Review

**Model:** Opus 5.5 — finds what Sonnet misses, and reads the code a change
calls instead of trusting its docstring, for a spike; for a bounded, feature or
architectural change gpt-6.1-sol at effort `max`, started by `python3
scripts/stage2.py review <change>`. A re-check after an earlier `## Phase 6`
block in `findings.md` starts a fresh read-only Codex session (ADR 0017).
The first phase-6 review starts fresh where phase 2a ran on Opus 5.5
(ADR 0016), and resumes a recorded Codex phase-2a session where one stands.
**Input:** the diff, `spec.md` and, when the change has one, `design.md` —
whether the diff makes its architecture delta true is your question (ADR 0009).
**Not** the author's reasoning.
**Result:** `plans/changes/<name>/findings.md`
**Gate:** no open `[AMBIGUITY]`, no open BLOCKER — `[DIVERGENT]` counts as
BLOCKER.
**Session:** a re-check after an earlier `## Phase 6` block in `findings.md`
starts a fresh read-only Codex session, without resuming a repair, earlier
phase-6 or historical Codex phase-2a thread (ADR 0017). The first phase-6
review starts fresh where phase 2a ran on Opus 5.5 — no phase-2a session of
yours exists, and `findings.md` says so. Only that first review resumes a
recorded Codex phase-2a session (`Reviewer session: codex <id>` in the change's
last 2a block), with
`codex exec resume`. Your yardstick is the current `spec.md` — the version
revised after the 2a review, not the one written first. Read it again, and
check first that each of the 2a rows arrived in it as `findings.md` says.

**Verdict first.** Write your verdict — the table and, under it, the line
`Phase 6 verdict: <reviewer> <session>, <date>` — before you read any loop
row. The loop rows are the findings of the loop's rounds — at most three
rounds, one rung of the ladder each, round 3 only when round 2 wrote a taken
row — the reviewers of the
loop before this phase (`docs/WORKFLOW.md` §4); they are held outside the
repository until your verdict stands, so that they cannot shape it. Only then
do the loop rows come in. On the Claude path you run
`python3 scripts/stage2.py release-loop
<change>` and mark the `Phase 6` cell of each loop row `agree` or `disagree —
<reason>`; on the Codex path the runner does both. A change that ran stage 2
has the columns `Reviewer` and `Broke a test` in `findings.md`
(`docs/WORKFLOW.md` §4). The verdict line is one line: `<date>` as `YYYY-MM-DD`
comes last on it, `<session>` is left out when you have no id, and `<reviewer>` names
who reviewed — never `pending`.

Having passed the spec in 2a is no argument now. Where the code shows the spec
itself was wrong — a caveat it rested on, a reading it did not make — that is a
finding, even if you let it through before.

You check against the **spec**, not against the diff. The question is not "is
this written cleanly" but "does this meet the acceptance criteria, and where
does it not".

Two dimensions, because a spec cannot see its own gaps:

- **`SPEC`** — measured against `spec.md`. Finds what was promised and not built.
- **`MAINT`** — the eye of a maintainer who was not there: error handling, edge
  cases, contracts facing outward, security. Finds what the spec is silent about.

Your answer **is** a table: one row per finding, `SPEC` and `MAINT` in the
dimension column. Through the runner you answer in rows of six cells — `| ID |
Severity | Dimension | Origin | Where | Finding |` — and the runner adds the
reviewer, the status and the verdict line; write a `|` inside a cell as `\|`.
On the Claude path you write the table of the change's `findings.md` yourself,
in the columns that file has. Two markers override everything: a finding that
reveals two plausible readings of spec or plan is `[AMBIGUITY]` and is never
decided locally; two places answering the same question in opposite ways are
`[DIVERGENT]` and a `BLOCKER`, however harmless each line looks alone.

A finding already rejected in an earlier round may only reappear **with new
evidence attached**. Repetition without new evidence is not a finding.

You report exactly three kinds of thing:

- **Correctness faults** — with the concrete case in which it breaks: which
  input, which state, which wrong result.
- **Gaps against the spec** — an acceptance criterion without a test, a non-goal
  that was violated.
- **Gates that cannot bite** — a check over an empty set, a test without its
  counterpart, a guard that fails open, a mode that closes a found difference
  with exit 0.

No style preferences. No renamings. No suggestions the spec does not ask for —
nothing that starts with "one could also".

**If you find nothing, say so in one sentence, and name what you checked.** A
reviewer who always finds something is not a stricter reviewer; it is an
unusable signal.

**A finding reads without the spec beside it.** It names the case in words —
which input, which result, what should hold instead. The acceptance criterion
goes in brackets at the end, never as the subject.
