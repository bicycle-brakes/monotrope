# Phase 3 · Plan

**Model:** Opus 5.5 — at effort `xhigh` (`claude --model claude-opus-5-5 --effort xhigh`); a mistake here is the most expensive one.
**Result:** `plans/changes/<name>/plan.md`
**Gate:** `python3 scripts/validate_change_artefacts.py --check` green.

You describe **how** the spec is met — precisely enough that the next session
needs `plan.md` and `spec.md` and nothing else. When the change has a
`design.md` (phase 2b), plan from it as well and write into `plan.md` what
phase 4 needs from it.

**Every `plan.md` opens with a card** — directly after its header and title,
before any other content. It shows the maintainer the effect, the end and the
limit of the change before a single file is named:

```text
For you:     <what changes for the maintainer>
Done when:   <the evidence that will show it holds>
Appetite:    <time for phase 4; a stop, not an estimate>
Not now:     <what is left out>
Pre-mortem:  suppose it failed: most likely because <one reason>
Starts unless you say stop.
```

The pre-mortem is one line with one reason, never a list of risks. When phase 3
ends, show the card in the closing message, identical to the one in `plan.md`.
While the maintainer has not said stop, phase 4 starts once the card is shown;
no "ok" is needed. When phase 3 runs as a subagent, the orchestrating session
shows the card to the maintainer unchanged; the veto stays the maintainer's.

A card **widens** the scope when its `For you:` or `Done when:` line includes
what `spec.md` names as a non-goal or no acceptance criterion covers, and the
appetite when its `Appetite:` is larger than one `decisions.md` or `spec.md`
states (where neither states one, the card's appetite widens nothing). A
widening card needs the maintainer's "ok" before phase 4 starts: its last line
names what widens and asks for that "ok" in place of `Starts unless you say
stop.`

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
- **Carry an Explore fallback forward.** When `research.md` records a
  Stage-1 route because Stage 2 was off or Z.ai unavailable, copy that route,
  model and reason into `plan.md`; phase 1 cannot write it here before this
  file exists.

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
