# Phase 3 · Plan

**Model:** Fable 5.1 — a mistake here is the most expensive one.
**Result:** `plans/changes/<name>/plan.md`
**Gate:** `python3 scripts/validate_change_artefacts.py --check` green.

You describe **how** the spec is met — precisely enough that the next session
needs `plan.md` and `spec.md` and nothing else.

Required:

- **Every file by name** that is created, changed or deleted, with one sentence
  on what happens there.
- **The verification command**, verbatim, as it stands in the shell.
- **Per acceptance criterion the test** that holds it, and the fault that test
  would have to meet to go red.
- **What you do not touch**, where the obvious reading would include it.
- **No longer than the change.** A plan with more lines than the diff it
  describes is a finding, not diligence. What fits in one sentence stays one
  sentence.

## Model markings (stage 2 only)

Where stage 2 is active, every subtask carries exactly one marking — `[FLASH]`,
`[GLM5.3]` or `[SONNET]`. Format and decision rules: `templates/plan-marking.md`.
The orchestrator groups consecutive same-marking lines into one segment; an
unmarked line is ignored, which makes it a gap in the plan rather than a
surprise at runtime. Under stage 1 the markings are ignored.

## Questions

Classify before you ask (`docs/WORKFLOW.md`):

```
[DECISION] → human   irreversible · external contract · risk · or the spec
                     admits two plausible readings
[GAP]      → explore answerable from the repository → extend research.md
[DETAIL]   → agent   freely revisable → decide it, record the reason
```

A `[DECISION]` at this stage means the spec did not settle something the plan
cannot avoid. It goes back to `decisions.md`, not into the plan as an aside.

Then `/clear`. The plan is a file; whoever executes it does not need your
reasoning, and fresh context beats continuity.
