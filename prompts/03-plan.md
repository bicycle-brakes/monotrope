# Phase 3 · Plan

**Model:** gpt-6.1-sol — Codex (`gpt-6.1-sol`) at effort [`CODEX_EFFORTS["draft"]`](../scripts/stage2.py), started by
`python3 scripts/stage2.py draft <change>`: one call writes spec, design and
plan (phases 2, 2b and 3), and GLM 5.3 after two failed attempts; a mistake
here is the most expensive one. Where Stage 2 is off, Opus 5.5 at effort
`xhigh` (`claude --model claude-opus-5-5 --effort xhigh`) writes it.
**Result:** `plans/changes/<name>/plan.md`
**Gate:** `python3 scripts/validate_change_artefacts.py --check` green.

You describe **how** the spec is met — precisely enough that the next session
needs `plan.md` and `spec.md` and nothing else. When the change has a
`design.md` (phase 2b), plan from it as well and write into `plan.md` what
phase 4 needs from it.

**Every `plan.md` opens with a card** — directly after its header and title,
before any other content. It shows the maintainer the effect, the end and the
limit of the change before a single file is named:

When phase 3 ends, show a short contextual preface before the card — Topic,
Intention, Today, Repository change, Architecture change, as `docs/WORKFLOW.md`
sets them out — and then the card in the closing message, identical to the
one in `plan.md`; the preface names no field of the card and asks for no
approval of its own.

```text
For you:     <what changes for the maintainer>
Done when:   <the evidence that will show it holds>
Appetite:    <time for phase 4; a stop, not an estimate>
Not now:     <what is left out>
Pre-mortem:  suppose it failed: most likely because <one reason>
Starts unless you say stop.
```

The pre-mortem is one line with one reason, never a list of risks.
While the maintainer has not said stop, phase 4 starts once the card is shown;
no "ok" is needed. When phase 3 runs as a subagent or through the runner, the
orchestrating session shows the card to the maintainer unchanged; the veto
stays the maintainer's.

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
  would have to meet to go red — as entries of the criterion ledger below.
- **What you do not touch**, where the obvious reading would include it.
- **No longer than the change.** A plan with more lines than the diff it
  describes is a finding, not diligence. What fits in one sentence stays one
  sentence.
- **Carry an Explore fallback forward.** When `research.md` records a
  Stage-1 route because Stage 2 was off or Z.ai unavailable, copy that route,
  model and reason into `plan.md`; phase 1 cannot write it here before this
  file exists.

## The criterion ledger

Every `plan.md` has exactly one section headed `## Criterion ledger`, with
one line per criterion and test in one of three forms:

- a test entry, `- <n>: tests/<path>::<function>` — a top-level
  `def test_…` in a file `tests/…/test_*.py`;
- a not-yet-written entry, `- <n>: not yet written tests/<path>::<function>`
  — a test phase 4 has still to write;
- a not-a-test entry, `- <n>: not a test — <what holds it>` — a review, a
  gate or a command; where a test can hold the criterion, write the test.

`<n>` is a criterion number of `spec.md`, without a leading zero, and every
criterion has at least one entry. A test entry or a not-yet-written entry may
end in ` — ` and the fault that turns the test red; an indented line
continues an entry. For example:

```markdown
## Criterion ledger

- 1: tests/test_example.py::test_a_missing_file_is_reported — the check exits 0 without the file
- 2: not yet written tests/test_example.py::test_an_empty_file_is_reported
- 3: not a test — the phase-6 review reads the help text against the spec
```

The gate `criterion-ledger` holds the ledger of every live change, and keeps
holding it after the change is archived: a named test that is not defined, a
not-yet-written test that exists, a criterion without an entry, an entry for
no criterion and a line in none of the three forms turn `make verify` red.

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
