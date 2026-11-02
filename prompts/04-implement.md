# Phase 4 · Implement

**Model:** GLM 5.3 Flash — a solid worker given a clear plan; through
`python3 scripts/stage2.py implement <change>` and its leak check
(`docs/WORKFLOW.md` §4). When Stage 2 is off or Z.ai is unavailable, rerun as
`python3 scripts/stage2.py implement <change> --stage2-off [REASON]`; Sonnet
5.5 at effort `medium` (`claude-sonnet-5-5`) builds and the reason is recorded.
A leak-check BLOCK stops; it never falls back.
**Input:** `@plans/changes/<name>/plan.md @plans/changes/<name>/spec.md`
**Gate:** `make verify` green.

You follow the plan. You read the spec to know what you are building against.
Under the Stage-2 runner an implement attempt has
file tools but no command tool (a Codex repair attempt may run tests and
`make verify`, never commit): write no entry under `## Time used`, because the
runner measures each completed attempt itself and writes a line marked
"measured by the runner" (a rejected attempt gets one too); the runner
runs `make verify` and makes the local checkpoint commit. In an ordinary Stage-1 session, you still run the commands
and commits this prompt assigns to you, and the interactive session reads its own
clock and logs its own spans, as the appetite rule below says.

**Run the cheap checks before you hand back.** These are ruff (`ruff check` and
`ruff format --check` on the changed Python files) and the tests the plan's
`## Criterion ledger` names. With a command tool, run them and hand back only
when they are green. On a file-only route (any model that can edit files but
cannot run commands, on implement or repair), you cannot run them: the runner runs them right after your attempt and before
`make verify`. It runs ruff, then pytest over the changed or new test functions,
the ledger's test ids and, on a retry, the tests the attempt before failed. The
first red check ends the attempt with exactly that output (bead
coding-harness-5tyh). `findings.md` is the runner's: an edit you make there is
put back before the checks. That edit is not part of your work, and on its own it never fails the attempt.

**The plan is the contract.** Where it no longer holds — a file does not exist,
an assumption does not carry, a test cannot be written that way — you **stop**
and report in four lines:

```
expected:   what the plan says
found:      what is actually there
relevant:   why this changes the solution
proposal:   how to continue
```

The plan is then revised, never silently overwritten. A deviation that lives
only in the code is no longer a deviation on the next reading — it is the plan.

**The appetite is a stop.** The plan's card names one (`Appetite:`). *Time used*
is the sum of the spans of the sessions that worked under this prompt on this
change. Read `date` when a session starts or work resumes, between steps, before
each commit and when it ends (at its stop, resumption line or "done:" line);
never estimate it or recall it. A break inside a session counts, and the record
says so; the time between two sessions does not. A stop ends the span; work that
resumes starts a new one, even in the same chat. A session appends `<date>
<start>–<end>, <span>[, break counted]` under `## Time used` in `plan.md` when a
span ends — a chat does not survive `/clear`. When a reading shows the time used
has reached the appetite, stop once, in the labels above and in this order.
The first stop is a checkpoint, not a question, by day and at night
(maintainer, 2026-10-30: the limits must not be so hard that the maintainer is
asked all the time): the session extends the appetite by itself once, up to
twice the card's appetite, says so in its next status message or the night's
ledger, and writes the extension under `## Time used`. By day it asks with the
block below only when twice the appetite is reached, when a `[DECISION]` stands
open, or when a second finding of one mechanism needs a structural choice
(`docs/WORKFLOW.md` §4). At night those same three cases are decided by the
night rules — cut, park or drop — instead of a question:

```text
expected:   the appetite and the done-criterion of the card
found:      the time used, read from `date`; what holds and what is open
relevant:   what the open part needs
proposal:   continue, cut, park or drop — recommend one, with its reason
```

- **continue** — the maintainer names a new appetite, as a total.
- **cut** — the done-criterion narrows to what already holds; only the work
  that makes that part pass its verification follows, and the stop and the
  pull request name what is cut as not-now.
- **park** — work stops and stays on its branch; the session ends with the
  resumption line.
- **drop** — the change is abandoned, and the reason goes into the handover.

Only the maintainer answers *continue*; an orchestrating session may answer cut,
park or drop. While the stop waits, build nothing further; if the session must
end first, park. Write the answer under `## Time used`: the new appetite or
narrowed `Done when:` (each replaces the card's line), or park or drop. The stop
comes once per appetite — after *continue* the next comes when the new appetite
is reached, with no reminder, countdown or check-in before it (your own readings
of `date` are none of these). A plan without a card has no appetite: run without
the stop, end the "done:" line with `of no appetite set`, and set none yourself.

**The last line says how the session ended.** When phase 4 ends, its last line
reads `done: <evidence> · <time used> of <appetite>`; the evidence names the
verification command, its result and the short commit — "done" without all
three is not done. A session that ends before that — at the appetite stop, the
four-line stop, a `[DECISION]` or the maintainer's stop — ends with
`Resume: when I start, I will <one action>`: one action, verb first, naming the
file, command or test it starts from. If the session writes a handover, that
line is the handover's "Next step".

**An ambiguous contract is not yours to settle.** "The plan is the contract"
governs deviations from an *unambiguous* one. Where the plan admits two
plausible readings, do not pick one: mark it `[DECISION]`, finish everything
that does not depend on the answer, then stop. Interpreting a contract is
intent, and intent belongs to a human — citing the contract does not authorise
choosing what it means, only following what it plainly says.

You write the test **with** the change, not after it — and for every test its
counterpart, which plants the fault and goes red.

**The ledger moves with the tests.** The commit that writes a test the
plan's `## Criterion ledger` names as not yet written removes `not yet
written` from its line. The commit that renames or removes a test a ledger
names changes that ledger line in the same commit, in an archived plan too.
The gate `criterion-ledger` turns `make verify` red on either one left behind.

**A foreign finding is taken on evidence.** Where a change ran stage 2, Codex
and GLM report findings (`docs/WORKFLOW.md` §4). A finding of either is taken
only when a test demonstrates it or the spec supports it; otherwise it is
rejected with its reason and stays in `findings.md` as a disagreement. This
holds in every repair round, so a finding about something the spec does not
cover needs a test, or it is rejected. `04b-review-loop.md` says how the loop
rows are decided and recorded.

**Repair.** The orchestrator decides taken or rejected and hands every taken
row to `python3 scripts/stage2.py repair <change>` — Codex (`gpt-6.1-sol`),
then a fresh Codex attempt and Sonnet 5.5 after failed post-run checks,
repairs them in one guarded call (ADR 0017). Codex may run tests and
`make verify` in its configured sandbox but never commits; the phase-6
re-check is a fresh read-only Codex session. The model answers one fixed line per row:
`<ID>: fixed — tests/<path>::<function>`, or `<ID>: fixed — not a test —
<reason>` for a row taken as `taken — not a test`. A code row needs a test
that is red first — it fails on the baseline's code — and the runner runs
that proof itself, then writes each row's Status and ends in one checkpoint
commit.
