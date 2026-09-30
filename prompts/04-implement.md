# Phase 4 · Implement

**Model:** Sonnet 5.5 — at effort `medium` (`claude --model claude-sonnet-5-5
--effort medium`); a solid worker given a clear plan.
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
