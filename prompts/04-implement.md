# Phase 4 · Implement

**Model:** GLM 5.3 Flash — a solid worker given a clear plan; through the
runner and the leak check (`docs/WORKFLOW.md` §4). Until the runner starts this
phase, Sonnet 5.5 at effort `medium` (`claude --model claude-sonnet-5-5
--effort medium`) builds (`docs/WORKFLOW.md` §3).
**Input:** `@plans/changes/<name>/plan.md @plans/changes/<name>/spec.md`
**Gate:** `make verify` green.

You follow the plan. You read the spec to know what you are building against.

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
has reached the appetite, stop once, in the labels above and in this order:

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

**A foreign finding is taken on evidence.** Where a change ran stage 2, Codex
and GLM report findings (`docs/WORKFLOW.md` §4). A finding of either is taken
only when a test demonstrates it or the spec supports it; otherwise it is
rejected with its reason and stays in `findings.md` as a disagreement. This
holds in every repair round, so a finding about something the spec does not
cover needs a test, or it is rejected. `04b-review-loop.md` says how the loop
rows are decided and recorded.
